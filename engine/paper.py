"""Forward paper executor: venv/bin/python -m engine.paper [--instr uk100fut]

Definition #1 (definitions/frozen_v1.yaml) against real-time bars via the
existing collector polling (collector rate discipline; signals uk100fut,
quote leg uk100 bid/ask). ONE ENGINE: the identical code path as lab and
narrate — zero configurable strategy surface (knobs: instrument, on/off).

Fills: cash-CFD vehicle (basis-at-entry mapping, GBP/pt sizing). EOD
force-flat + entry embargo enforced. Trades logged schema-identical to
backtest records, tagged FORWARD_PAPER, appended to reports/paper/ledger.jsonl
(append-only; per-run commits are the operator's standing step).

Restart/crash: state warms from the store; an open paper position found in
the ledger is CLOSED-ON-RECONCILE at the first available quote and logged
RECONCILE_CLOSE (downtime = honest holes, never backfilled decisions);
coverage gaps between last processed bar and warm-start are logged
COVERAGE_GAP. First start stamps go_live_utc into lockbox.json — the
lockbox's terminal boundary (zone model, register item 14).
"""

import argparse
import json
import os
import sys
import time

import pandas as pd

from .bars import Bar
from .config import load as load_cfg
from .pipeline import MTFEngine
from .narrate import build_all_bars, feed
from .resample import trading_sessions
from .store_loader import load_frame, stamp_go_live
from .strategy import load_definition, apply_definition
from backtest.loop import session_fns

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LEDGER = os.path.join(ROOT, "reports", "paper", "ledger.jsonl")


def _led(rec, path=None):
    path = path or LEDGER
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "a") as f:
        f.write(json.dumps(rec, default=str) + "\n")


def guarded(fn, ledger_path=None):
    """Loud-death wrapper (World A fix, 2026-08-14): the poll loop must not
    die silently. Exceptions -> EXECUTOR_ERROR (ledger + stderr), loop
    continues; a dead witness must announce itself."""
    try:
        return True, fn()
    except KeyboardInterrupt:
        raise
    except Exception as e:
        msg = f"{type(e).__name__}: {e}"
        print(f"# EXECUTOR_ERROR {msg}", file=sys.stderr)
        try:
            _led({"event": "EXECUTOR_ERROR", "error": msg,
                  "ts": str(pd.Timestamp.now(tz='UTC'))}, ledger_path)
        except Exception:
            pass
        return False, None


SUSPENSION_THRESHOLD = pd.Timedelta(minutes=5)


def suspension_check(last_poll, now, ledger_path=None):
    """Register finding 26: the laptop travels daily — machine sleep freezes
    both live loops silently (observed 2026-08-18 07:03-07:40Z: 38 min store
    hole, one EXECUTOR_ERROR from network teardown, no crash). A wall-clock
    jump between polls > threshold = suspension; log ONE gap event with the
    span before processing resumes. Decisions hole — never backfilled."""
    if last_poll is None or now - last_poll <= SUSPENSION_THRESHOLD:
        return None
    ev = {"event": "SUSPENSION_GAP", "from": str(last_poll), "to": str(now),
          "span": str(now - last_poll),
          "note": "machine suspend (wall-clock jump between polls); "
                  "decisions hole - never backfilled",
          "ts": str(now)}
    _led(ev, ledger_path)
    return ev


def expect_prints(ts):
    """Watchdog calendar in PROVIDER TIME — UTC, not London (register
    finding 24). The feed's day is UTC-anchored (DATA.md ~22:00->~21:00
    UTC); encoding the pause in London hours fired 11 false
    WATCHDOG_STALLs 2026-08-17 21:11-22:03Z during the one-hour BST
    offset (and would have looked "fixed" in GMT months). Measured from
    the store (2026-08-17): last pre-pause bar opens 20:59Z, first
    post-pause bar 22:05Z; Sunday reopen 22:05Z. Quiet window
    [21:00, 22:10) UTC = measured + 5 min reopen margin; weekend quiet
    Fri 21:00Z -> Sun 22:10Z."""
    u = pd.Timestamp(ts).tz_convert("UTC")
    m = u.hour * 60 + u.minute
    pause_start, pause_end = 21 * 60, 22 * 60 + 10
    dow = u.dayofweek
    if dow == 5:                        # Saturday
        return False
    if dow == 4:                        # Friday: quiet from the close
        return m < pause_start
    if dow == 6:                        # Sunday: quiet until the reopen
        return m >= pause_end
    return not (pause_start <= m < pause_end)


def reconcile(ledger_path):
    """Dangling ENTRY without EXIT -> RECONCILE_CLOSE (honest hole)."""
    if not os.path.exists(ledger_path):
        return 0
    entries = [json.loads(l) for l in open(ledger_path)]
    closes = {e.get("entry_ts") for e in entries if e.get("event") == "EXIT"}
    n = 0
    for e in entries:
        if e.get("event") == "ENTRY" and e["entry_ts"] not in closes:
            _led({"event": "RECONCILE_CLOSE", "entry_ts": e["entry_ts"],
                  "note": "position open at crash/restart; closed on "
                          "reconcile - honest hole, not a backfilled decision",
                  "ts": str(pd.Timestamp.now(tz='UTC'))}, ledger_path)
            n += 1
    return n


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--instr", default="uk100fut")
    a = ap.parse_args()
    d = load_definition(os.path.join(ROOT, "definitions", "frozen_v1.yaml"))
    cfg = apply_definition(load_cfg(), d)
    go = stamp_go_live(pd.Timestamp.now(tz="UTC"))
    print(f"# PAPER go-live boundary: {go} (terminal for lockbox)",
          file=sys.stderr)

    sys.path.insert(0, os.path.join(ROOT, "scripts"))
    import collect as collector
    import store as store_mod
    iid = collector.INSTRUMENTS[a.instr]
    qid = collector.INSTRUMENTS[cfg.execution_vehicle.quote_slug]
    qslug = cfg.execution_vehicle.quote_slug

    embargo_fn, eod_fn = session_fns(cfg, a.instr)
    inst = cfg.instruments[a.instr]
    engine = MTFEngine(cfg, embargo_fn=embargo_fn, eod_fn=eod_fn,
                       tick_size=inst.tick_size,
                       point_value=inst.point_value)

    # reconcile any open position from a prior run
    reconcile(LEDGER)
    # (1)+(3) 2026-08-17: predecessor-anchored coverage. Anchor = clean
    # STOP's last_processed, else crash checkpoint, else predecessor
    # warm_through — NEVER this run's warm_through (a post-crash sync can
    # erase downtime; "warm==last-processed" is false after crash+sync).
    ck_path = os.path.join(ROOT, "reports", "paper", "checkpoint.json")
    pred_anchor, unclean = None, False
    if os.path.exists(LEDGER):
        evs = [json.loads(l) for l in open(LEDGER)]
        life = [e for e in evs if e.get("event") in ("START", "STOP")]
        if life and life[-1]["event"] == "START":
            unclean = True
            ck = (json.load(open(ck_path)) if os.path.exists(ck_path) else {})
            pred_anchor = (ck.get("last_processed")
                           or life[-1].get("warm_through"))
            _led({"event": "UNCLEAN_PREDECESSOR",
                  "predecessor_start": life[-1].get("ts"),
                  "last_recoverable_activity": str(pred_anchor),
                  "ts": str(pd.Timestamp.now(tz='UTC'))})
        elif life and life[-1]["event"] == "STOP":
            pred_anchor = life[-1].get("last_processed")

    # warm from store (working+lockbox+forward all visible to a LIVE
    # process — paper is the forward zone's only legitimate consumer)
    df1 = load_frame(a.instr, "1min", narrative_scope=True,
                     log_fn=lambda m: print(m, file=sys.stderr))
    cash = trading_sessions(df1, cfg.session_model.trading_day_anchor_london)
    bars = build_all_bars(cfg, cash)
    feed(engine, bars, lambda e: None)
    if engine.broker.position is not None:
        engine.broker.position = None
        _led({"event": "WARM_RESIDUAL_CLEARED",
              "note": "warm replay left a simulated open position; cleared "
                      "before live decisions - warm state is context only"})
    last_ts = max((b.ts for b in bars["execution"]), default=None)
    # forward coverage begins at go_live_utc: gap measured from the LATER of
    # (warm_through, go_live); pre-stamp time is zone-irrelevant, not downtime
    from .store_loader import zones as _zones
    _gl = _zones()["go_live"]
    pa = pd.Timestamp(pred_anchor) if pred_anchor else None
    ref = max([t for t in (pa, _gl) if t is not None], default=None) or last_ts
    gap = pd.Timestamp.now(tz="UTC") - ref if ref is not None else None
    _led({"event": "START", "ts": str(pd.Timestamp.now(tz='UTC')),
          "warm_through": str(last_ts), "coverage_gap": str(gap),
          "definition": d["name"], "hash": d["_hash"]})
    if gap is not None and gap > pd.Timedelta(minutes=5):
        _led({"event": "COVERAGE_GAP", "from": str(last_ts),
              "note": "downtime hole - decisions never backfilled"})

    n_trades = len(engine.broker.trades)
    sid = int(cash["session_id"].max()) if len(cash) else 0
    sig_min = 15
    partial = []
    session_open = None
    print("# paper loop: 1 poll/min (fut mid + cash bid/ask)", file=sys.stderr)
    quiet_polls = 0
    pending_confirm = {}      # time -> (o,h,l,c,v) from previous poll
    last_poll = None
    try:
        while True:
            _now = pd.Timestamp.now(tz="UTC")
            if suspension_check(last_poll, _now):
                print(f"# SUSPENSION_GAP: {last_poll} -> {_now}",
                      file=sys.stderr)
            last_poll = _now
            ok, pages = guarded(lambda: (
                collector.fetch_page("minute", "mid", n=10, instr=iid),
                collector.fetch_page("minute", "bid", n=10, instr=qid),
                collector.fetch_page("minute", "ask", n=10, instr=qid)))
            if not ok:
                time.sleep(60)
                continue
            fut, qb, qa = pages
            if fut is None or len(fut) <= 1 or (
                    last_ts is not None
                    and fut.iloc[-2]["time"] + pd.Timedelta(minutes=1) <= last_ts):
                quiet_polls += 1
                if quiet_polls >= 5 and expect_prints(pd.Timestamp.now(tz="UTC")):
                    print(f"# WATCHDOG_STALL: {quiet_polls} polls, no new "
                          f"bars during expected-printing hours",
                          file=sys.stderr)
                    _led({"event": "WATCHDOG_STALL", "quiet_polls": quiet_polls,
                          "ts": str(pd.Timestamp.now(tz='UTC'))})
                    quiet_polls = 0
            else:
                quiet_polls = 0
            if fut is not None and len(fut) > 1:
                # (processing exceptions also route through guarded below)
                # PERSIST-THEN-FEED (2026-08-14 finding): steady-state polls
                # go through the SAME raw->clean collector path as catch-up
                # and sync (idempotent, deduped), so warm-from-store always
                # equals last-processed. Persist BEFORE the engine sees bars.
                try:
                    collector.merge_store("minute", "mid", fut.iloc[:-1],
                                          a.instr)
                    if qb is not None and len(qb) > 1:
                        collector.merge_store("minute", "bid", qb.iloc[:-1],
                                              qslug)
                    if qa is not None and len(qa) > 1:
                        collector.merge_store("minute", "ask", qa.iloc[:-1],
                                              qslug)
                    store_mod.build_one(a.instr, verbose=False)
                    store_mod.build_one(qslug, verbose=False)
                except Exception as e:
                    print(f"# PERSIST FAILED (feeding engine anyway; sync "
                          f"will recover): {e}", file=sys.stderr)
                confirmed, nxt = [], {}
                for _, r in fut.iloc[:-1].iterrows():
                    key = (r["open"], r["high"], r["low"], r["close"],
                           r["volume"])
                    if pending_confirm.get(r["time"]) == key:
                        confirmed.append(r)       # two successive polls agree
                    else:
                        nxt[r["time"]] = key      # await confirmation
                pending_confirm = nxt
                for r in confirmed:
                    close_ts = r["time"] + pd.Timedelta(minutes=1)
                    if last_ts is not None and close_ts <= last_ts:
                        continue
                    from .resample import canonical_tod
                    tod, tday = canonical_tod(r["time"])
                    if session_open is None or tday != session_open:
                        session_open, sid = tday, sid + 1
                    eb = Bar(close_ts, r["open"], r["high"], r["low"],
                             r["close"], r["volume"], tf="1min",
                             session_id=sid, tod_bin=tod)
                    quote = None
                    if qb is not None and qa is not None:
                        b = qb[qb["time"] == r["time"]]
                        aa = qa[qa["time"] == r["time"]]
                        if len(b) and len(aa):
                            mid = (b.iloc[0] [["open","high","low","close"]].values
                                   + aa.iloc[0][["open","high","low","close"]].values) / 2
                            quote = {"open": mid[0], "high": mid[1],
                                     "low": mid[2], "close": mid[3],
                                     "spread": float(aa.iloc[0]["close"]
                                                     - b.iloc[0]["close"])}
                    partial.append(eb)
                    slot = {}
                    if (tod + 1) % sig_min == 0 and partial:
                        blk = partial[-sig_min:]
                        slot["signal_bar"] = Bar(
                            close_ts, blk[0].open, max(x.high for x in blk),
                            min(x.low for x in blk), blk[-1].close,
                            sum(x.volume for x in blk), tf="15min",
                            session_id=sid, tod_bin=tod // sig_min)
                    engine.process(close_ts, exec_bar=eb, exec_quote=quote,
                                   **slot)
                    last_ts = close_ts
                    json.dump({"last_processed": str(last_ts)},
                              open(ck_path, "w"))
                    while n_trades < len(engine.broker.trades):
                        t = engine.broker.trades[n_trades]
                        _led({"event": "EXIT", "tag": "FORWARD_PAPER", **t})
                        n_trades += 1
                    for e in engine.narrative.events[-6:]:
                        if e["type"] == "ENTRY" and e["ts"] == close_ts:
                            _led({"event": "ENTRY", "tag": "FORWARD_PAPER", **e})
            time.sleep(60)
    except KeyboardInterrupt:
        _led({"event": "STOP", "ts": str(pd.Timestamp.now(tz='UTC')),
              "last_processed": str(last_ts)})


if __name__ == "__main__":
    main()
