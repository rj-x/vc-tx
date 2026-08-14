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
    iid = collector.INSTRUMENTS[a.instr]
    qid = collector.INSTRUMENTS[cfg.execution_vehicle.quote_slug]

    embargo_fn, eod_fn = session_fns(cfg, a.instr)
    inst = cfg.instruments[a.instr]
    engine = MTFEngine(cfg, embargo_fn=embargo_fn, eod_fn=eod_fn,
                       tick_size=inst.tick_size,
                       point_value=inst.point_value)

    # reconcile any open position from a prior run
    reconcile(LEDGER)

    # warm from store (working+lockbox+forward all visible to a LIVE
    # process — paper is the forward zone's only legitimate consumer)
    df1 = load_frame(a.instr, "1min", narrative_scope=True,
                     log_fn=lambda m: print(m, file=sys.stderr))
    cash = trading_sessions(df1, cfg.session_model.trading_day_anchor_london)
    bars = build_all_bars(cfg, cash)
    feed(engine, bars, lambda e: None)
    last_ts = max((b.ts for b in bars["execution"]), default=None)
    gap = pd.Timestamp.now(tz="UTC") - last_ts if last_ts is not None else None
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
    try:
        while True:
            try:
                fut = collector.fetch_page("minute", "mid", n=10, instr=iid)
                qb = collector.fetch_page("minute", "bid", n=10, instr=qid)
                qa = collector.fetch_page("minute", "ask", n=10, instr=qid)
            except Exception as e:
                print(f"# poll failed: {e}", file=sys.stderr)
                time.sleep(60)
                continue
            if fut is not None and len(fut) > 1:
                for _, r in fut.iloc[:-1].iterrows():
                    close_ts = r["time"] + pd.Timedelta(minutes=1)
                    if last_ts is not None and close_ts <= last_ts:
                        continue
                    if session_open is None or r["time"].date() != session_open.date():
                        session_open, sid = r["time"], sid + 1
                    tod = int((r["time"] - session_open).total_seconds() // 60)
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
