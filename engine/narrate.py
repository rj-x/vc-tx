"""narrate — the human front door to the narrative engine.

Two modes, one code path (both build the standard pipeline in
narrative-only mode and stream events as bars close):

Replay:
  venv/bin/python -m engine.narrate --instr uk100fut \\
      --start 2026-08-13T05:00Z --end 2026-08-13T09:40Z \\
      [--stack H1/15M/1M] [--show-tf 15M,H1] [--format txt|jsonl] \\
      [--narrative-only]
  Runs the pipeline over the window with normal warmup from prior
  sessions; pre-cash-open segments are marked baseline-only. Windows past
  the lockbox boundary REQUIRE --narrative-only (scoped loader access,
  logged; labels/phases/hypotheses/dump only — no metrics, no event-study
  rows, no trade records, nothing aggregated). Without the flag,
  post-boundary requests refuse loudly.

Live:
  venv/bin/python -m engine.narrate --instr uk100fut --live
  Same loop against a polling watcher: newest 1M bars fetched each minute
  via the existing collector (its rate discipline respected), narrative
  emitted on each bar close, ALWAYS narrative-only, state warmed from the
  store at startup. Observed feed latency (bar close -> availability) is
  reported as a finding.

Diagnostic/non-evidential by register ruling: no thresholds, rulings, or
tracked signals may be touched off any narrate output.
"""

import argparse
import json
import sys
import time

import pandas as pd

from .config import load as load_cfg
from .pipeline import MTFEngine
from .resample import cash_sessions, exec_bars, resample_bars, session_bars
from .store_loader import load_frame, lockbox_boundary

TF_ALIASES = {"1M": "1min", "3M": "3min", "5M": "5min", "10M": "10min",
              "15M": "15min", "30M": "30min", "H1": "1h", "D1": "1d"}
TF_MINUTES = {"1min": 1, "3min": 3, "5min": 5, "10min": 10, "15min": 15,
              "30min": 30, "1h": 60, "1d": None}   # None = whole session


def _tf(name):
    if name in TF_ALIASES:
        return TF_ALIASES[name]
    if name in TF_MINUTES:
        return name
    sys.exit(f"unknown timeframe '{name}' (known: {sorted(TF_ALIASES)})")


def build_cfg(args):
    cfg = load_cfg()
    # same comparability overrides as the campaign (flagged there)
    from backtest.campaign import BASE_OVERRIDES
    for k, v in BASE_OVERRIDES.items():
        cfg = cfg.override(k, v)
    cfg = cfg.override("session_model.extended_hours", True)   # Part B default
    if getattr(args, "ladder", False):
        cfg = cfg.override("session_model.ladder", True)
    if getattr(args, "debug_structure", False):
        cfg = cfg.override("debug.structure", True)
    if args.stack:
        parts = [p.strip() for p in args.stack.split("/")]
        if len(parts) != 3:
            sys.exit("--stack must be CONTEXT/SIGNAL/EXEC, e.g. H1/15M/1M")
        cfg = (cfg.override("mtf.context_tf", _tf(parts[0]))
                  .override("mtf.signal_tf", _tf(parts[1]))
                  .override("mtf.execution_tf", _tf(parts[2])))
    return cfg


def make_bars(cfg, cash, tf):
    minutes = TF_MINUTES[tf]
    if minutes is None:
        return session_bars(cash, tf)
    if minutes == 1:
        return exec_bars(cash, tf)
    return resample_bars(cash, minutes, tf)


def build_all_bars(cfg, cash):
    out = {role: make_bars(cfg, cash, getattr(cfg.mtf, f"{role}_tf"))
           for role in ("context", "signal", "execution")}
    if cfg.session_model.get("ladder"):
        stack = {getattr(cfg.mtf, f"{r}_tf") for r in out}
        for tf in ("1min", "3min", "5min", "15min", "30min", "1h"):
            if tf not in stack:
                out["ladder:" + tf] = make_bars(cfg, cash, tf)
    return out


def feed(engine, bars, emit, lo=None, upto=None):
    """One code path for replay and live: feed bars chronologically by
    close-ts (same-ts bars in one process() call — descending-TF order is
    enforced inside), emitting each new narrative event via `emit`.
    Bars with lo < ts <= upto are fed (None = unbounded)."""
    merged = {}
    for role in bars:
        for b in bars.get(role, []):
            if upto is not None and b.ts > upto:
                continue
            if lo is not None and b.ts <= lo:
                continue
            merged.setdefault(b.ts, {})[role] = b
    n_seen = len(engine.narrative.events)
    for ts in sorted(merged):
        slot = merged[ts]
        lb = {k.split(":")[1]: v for k, v in slot.items()
              if k.startswith("ladder:")}
        engine.process(ts, context_bar=slot.get("context"),
                       signal_bar=slot.get("signal"),
                       exec_bar=slot.get("execution"),
                       ladder_bars=lb or None)
        for e in engine.narrative.events[n_seen:]:
            emit(e)
        n_seen = len(engine.narrative.events)
    return n_seen


def _fmt_txt(e):
    core = {k: v for k, v in e.items() if k not in ("ts", "tf", "type")}
    h = core.pop("h", None)
    hs = ""
    if h:
        tag = f" tag={h['tag']}" if h.get("tag") else ""
        hs = (f" [{h['spec']}#{h['id']} {'LONG' if h['dir'] == 1 else 'SHORT'}"
              f" s={h['strength']:.1f} {h['state']}{tag}]")
    extra = f" {core}" if core else ""
    ts = pd.Timestamp(e["ts"]).strftime("%H:%M") if e["ts"] is not None else "--:--"
    seg = e.get("segment")
    segs = f" <{seg}>" if seg and seg != "cash" else ""
    return f"{ts}Z {e.get('tf') or '':<6} {e['type']:<28}{hs}{extra}{segs}"


def make_emitter(args, start, end, show_tfs, out=sys.stdout):
    def emit(e):
        ts = e.get("ts")
        if ts is None or not (start <= pd.Timestamp(ts) <= end):
            return
        if show_tfs and e.get("tf") and e["tf"] not in show_tfs:
            return
        if args.format == "jsonl":
            out.write(json.dumps(e, default=str) + "\n")
        else:
            if e["type"] == "LABEL" and e.get("label") is None:
                return                      # txt mode: quiet bars stay quiet
            out.write(_fmt_txt(e) + "\n")
        out.flush()
    return emit


# ---------------------------------------------------------------- replay

def _parse_ts(s, name):
    try:
        ts = pd.Timestamp(s)
    except (ValueError, TypeError):
        sys.exit(f"{name}: cannot parse '{s}' - use e.g. 2026-08-13T05:00Z")
    # naive input is taken as UTC (all engine timestamps are UTC)
    return ts.tz_localize("UTC") if ts.tzinfo is None else ts.tz_convert("UTC")


def replay(args):
    cfg = build_cfg(args)
    start = _parse_ts(args.start, "--start")
    end = _parse_ts(args.end, "--end")
    boundary = lockbox_boundary()
    if end >= boundary and not args.narrative_only:
        sys.exit(f"REFUSED: window end {end} is at/after the lockbox "
                 f"boundary {boundary}. Post-boundary narration requires "
                 f"--narrative-only (labels/phases/hypotheses/dump only; "
                 f"no metrics, no event-study rows, no trade records).")

    df1 = load_frame(args.instr, "1min", narrative_scope=args.narrative_only,
                     log_fn=lambda m: print(m, file=sys.stderr))
    from .resample import trading_sessions
    cash = trading_sessions(df1, cfg.session_model.trading_day_anchor_london)
    bars = build_all_bars(cfg, cash)
    engine = MTFEngine(cfg, narrative_only=True)

    # pre-cash-open marker: cash bars inside the window vs the window start
    win_cash = cash[(cash.index >= start) & (cash.index < end)]
    hdr = sys.stdout
    hdr.write(f"# narrate replay {args.instr} {start} -> {end} "
              f"stack {cfg.mtf.context_tf}/{cfg.mtf.signal_tf}/"
              f"{cfg.mtf.execution_tf} (narrative-only="
              f"{bool(args.narrative_only)})\n"
              f"# convention: bars stamped by CLOSE time; store/TradingView "
              f"open-time stamp = close - TF\n")
    if len(win_cash) == 0:
        hdr.write("# WINDOW CONTAINS NO CASH BARS - baseline-only segment "
                  "(pre-open/closed); nothing for the engine to narrate\n")
    else:
        first_cash = win_cash.index.min()
        if first_cash > start:
            hdr.write(f"# {start.strftime('%H:%M')}Z-"
                      f"{first_cash.strftime('%H:%M')}Z pre-cash-open: "
                      f"baseline-only (extended-hours data is outside the "
                      f"v1 engine; cash opens "
                      f"{first_cash.strftime('%H:%M')}Z)\n")

    show_tfs = ({_tf(t.strip()) for t in args.show_tf.split(",")}
                if args.show_tf else None)
    emit = (lambda e: None) if args.ledger else make_emitter(
        args, start, end, show_tfs)

    # warmup runs silently up to (exclusive of) the window start
    feed(engine, bars, lambda e: None, upto=start - pd.Timedelta(1, "ns"))
    hdr.write(_state_line(engine, "state @ window start") + "\n")
    feed(engine, bars, emit, lo=start - pd.Timedelta(1, "ns"), upto=end)
    if args.ledger:
        import csv as _csv
        from backtest.ledger import (CSV_COLS, hypothesis_rows,
                                     signature_moment_rows)
        evs = [e for e in engine.narrative.events
               if e["ts"] is not None and start <= pd.Timestamp(e["ts"]) <= end]
        rows = (hypothesis_rows(evs, [], cfg.mtf.signal_tf, "narrate")
                + signature_moment_rows(
                    evs, cfg.mtf.execution_tf, "narrate",
                    scope=args.ledger_scope.replace("-", "_")))
        w = _csv.DictWriter(sys.stdout, fieldnames=CSV_COLS)
        w.writeheader()
        for r in rows:
            w.writerow(r)
    hdr.write(_state_line(engine, "state @ window end") + "\n")
    hdr.write(f"# end of window - {args.instr} narrated through "
              f"{min(end, max(b.ts for b in bars['execution'])).strftime('%Y-%m-%d %H:%M')}Z\n")


def _state_line(engine, tag):
    parts = []
    for pipe in (engine.context_pipe, engine.signal_pipe):
        c = pipe.ctx
        if c.idx < 0:
            parts.append(f"{pipe.tf}: (no bars)")
            continue
        pc = (f", post_climax_dir={c.post_climax_dir}"
              if c.phase == "POST_CLIMAX" else "")
        parts.append(f"{pipe.tf}: phase={c.phase}{pc} trend={c.trend:+d} "
                     f"age={c.trend_age} atr={c.atr:.1f} close={c.close:.1f}"
                     if c.atr else f"{pipe.tf}: phase={c.phase} (warming)")
    hyps = [h.describe() for h in engine.manager.active]
    hs = ("; active: " + ", ".join(
        f"{h['spec']}#{h['id']} {'L' if h['dir'] == 1 else 'S'} "
        f"{h['state']} s={h['strength']:.1f}" for h in hyps)
        if hyps else "; active hypotheses: none")
    return f"# {tag}: " + " | ".join(parts) + hs


# ------------------------------------------------------------------ live

def live(args):
    cfg = build_cfg(args)
    import os
    sys.path.insert(0, os.path.join(os.path.dirname(
        os.path.dirname(os.path.abspath(__file__))), "scripts"))
    import collect as collector

    iid = collector.INSTRUMENTS[args.instr]
    boundary = lockbox_boundary()
    print(f"# narrate LIVE {args.instr} (id {iid}) - narrative-only by "
          f"construction; polling 1/min via the collector; Ctrl-C to stop",
          file=sys.stderr)

    # warm state from the store (scoped access - live is always post-boundary)
    df1 = load_frame(args.instr, "1min", narrative_scope=True,
                     log_fn=lambda m: print(m, file=sys.stderr))
    cash = cash_sessions(df1)
    engine = MTFEngine(cfg, narrative_only=True)
    bars = build_all_bars(cfg, cash)
    silent = lambda e: None                             # noqa: E731
    feed(engine, bars, silent)
    last_ts = max((b.ts for b in bars["execution"]), default=None)
    n_sessions = cash["session_id"].nunique()
    sid = int(cash["session_id"].max()) if n_sessions else 0
    print(f"# warmed from store: {n_sessions} sessions, last bar "
          f"{last_ts}", file=sys.stderr)

    show_tfs = ({_tf(t.strip()) for t in args.show_tf.split(",")}
                if args.show_tf else None)
    emit = make_emitter(args, pd.Timestamp.min.tz_localize("UTC"),
                        pd.Timestamp.max.tz_localize("UTC"), show_tfs)

    # live incremental state: partial signal/context blocks
    sig_min = TF_MINUTES[cfg.mtf.signal_tf]
    ctx_min = TF_MINUTES[cfg.mtf.context_tf]
    from engine.bars import Bar
    partial = {"signal": [], "context": []}
    latencies = []

    inst = cfg.instruments[args.instr]

    def in_cash(ts_open):
        lon = ts_open.tz_convert("Europe/London")
        lt = lon.hour + lon.minute / 60.0
        return inst.session_start_london <= lt < inst.session_end_london

    def flush_block(role, minutes):
        blk = partial[role]
        if not blk:
            return None
        b = Bar(blk[-1].ts, blk[0].open, max(x.high for x in blk),
                min(x.low for x in blk), blk[-1].close,
                sum(x.volume for x in blk), tf=getattr(cfg.mtf, f"{role}_tf"),
                session_id=blk[0].session_id, tod_bin=blk[0].tod_bin // minutes
                if minutes else 0, is_stub=len(blk) < (minutes or len(blk)))
        partial[role] = []
        return b

    session_open_ts = None
    first_poll = True       # startup catch-up bars would poison the latency
    try:                    # stat (their delay is store staleness, not feed)
        while True:
            try:
                page = collector.fetch_page("minute", "mid", n=30, instr=iid)
            except Exception as e:
                print(f"# poll failed: {e}", file=sys.stderr)
                time.sleep(60)
                continue
            now = pd.Timestamp.now(tz="UTC")
            if page is not None and len(page) > 1:
                settled = page.iloc[:-1]                 # last bar still forming
                for _, r in settled.iterrows():
                    ts_open = r["time"]
                    close_ts = ts_open + pd.Timedelta(minutes=1)
                    if last_ts is not None and close_ts <= last_ts:
                        continue
                    if not in_cash(ts_open):
                        continue
                    if not first_poll:
                        latencies.append((now - close_ts).total_seconds())
                    if session_open_ts is None or ts_open.date() != session_open_ts.date():
                        session_open_ts = ts_open
                        sid += 1
                    tod = int((ts_open - session_open_ts).total_seconds() // 60)
                    eb = Bar(close_ts, r["open"], r["high"], r["low"],
                             r["close"], r["volume"],
                             tf=cfg.mtf.execution_tf, session_id=sid,
                             tod_bin=tod)
                    partial["signal"].append(eb)
                    partial["context"].append(eb)
                    slot = {"execution": eb}
                    if (tod + 1) % sig_min == 0:
                        slot["signal"] = flush_block("signal", sig_min)
                    if ctx_min and (tod + 1) % ctx_min == 0:
                        slot["context"] = flush_block("context", ctx_min)
                    n0 = len(engine.narrative.events)
                    engine.process(close_ts,
                                   context_bar=slot.get("context"),
                                   signal_bar=slot.get("signal"),
                                   exec_bar=eb)
                    for e in engine.narrative.events[n0:]:
                        emit(e)
                    last_ts = close_ts
            first_poll = False
            time.sleep(60)
    except KeyboardInterrupt:
        pass
    finally:
        if latencies:
            s = pd.Series(latencies)
            print(f"\n# FEED LATENCY (bar close -> availability, n={len(s)}): "
                  f"min {s.min():.0f}s / median {s.median():.0f}s / "
                  f"max {s.max():.0f}s - this sets the floor for any future "
                  f"live use", file=sys.stderr)
        else:
            print("\n# no new bars observed (closed session?)", file=sys.stderr)


def main():
    ap = argparse.ArgumentParser(prog="narrate", description=__doc__)
    ap.add_argument("--instr", required=True)
    ap.add_argument("--start")
    ap.add_argument("--end")
    ap.add_argument("--stack", help="CONTEXT/SIGNAL/EXEC, e.g. H1/15M/1M")
    ap.add_argument("--show-tf", help="comma list, e.g. 15M,H1")
    ap.add_argument("--format", choices=("txt", "jsonl"), default="txt")
    ap.add_argument("--ledger-scope", choices=("signatures", "all-labels"),
                    default="signatures",
                    help="section-2 rows: reversal signatures only (default) "
                         "or every structural label at every running TF "
                         "(add --ladder for ladder-rung rows)")
    ap.add_argument("--ladder", action="store_true",
                    help="classify and display all ladder rungs (observational)")
    ap.add_argument("--ledger", action="store_true",
                    help="emit opportunity-ledger CSV rows for the window "
                         "instead of the narrative stream")
    ap.add_argument("--debug-structure", action="store_true",
                    help="emit SWING_CONFIRMED (k-lag) + per-bar PHASE_EVAL")
    ap.add_argument("--narrative-only", action="store_true",
                    help="scoped post-lockbox access: narration only")
    ap.add_argument("--live", action="store_true")
    args = ap.parse_args()
    if args.live:
        live(args)
    else:
        if not args.start or not args.end:
            sys.exit("replay mode requires --start and --end")
        replay(args)


if __name__ == "__main__":
    main()
