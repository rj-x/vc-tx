"""Forward-zone migration readout — OBSERVATIONAL (prereg_forward_migration_
readout, authorized 2026-08-18).

Replays the forward zone (go-live ->) through the campaign's Part B config
(extended_hours + ladder, frozen definition) with a NARRATIVE-ONLY engine,
runs the migration detector over the replay narrative, and grades the
pre-registered 11:46Z expectation.

Zone discipline, stated precisely:
  - Warm context uses FULL store visibility via load_frame(narrative_scope=
    True) — the live-equivalent warm the running paper/narrate processes
    have (lockbox rows enter baselines/context exactly as they streamed
    past the live consumers; established by the regrade/cascade replays).
  - EVERY emitted row and aggregate is strictly from the forward span
    (>= go_live): chain events filtered, study bars filtered, no
    lockbox-span quantity is computed or reported.
  - ZONE FENCE: a readout start before go_live is refused outright.

Forward readouts are EXHIBITS/EVIDENCE, NEVER VALIDATION — small-n forward
observation; the walk-forward and the lockbox remain the only verdict
machinery. Feeds no thresholds or rules.
"""

import argparse
import json
import os
import subprocess

import pandas as pd

from engine.pipeline import MTFEngine
from engine.resample import exec_bars, resample_bars, trading_sessions
from engine.store_loader import is_sealed, load_frame, refuse_if_sealed, zones
from backtest.campaign import make_cfg
from backtest.migration import migration_events, migration_study

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "reports", "forward")

_TFMIN = {"1min": 1, "3min": 3, "5min": 5, "15min": 15, "30min": 30, "1h": 60}

# pre-registered expectation (trial log 2026-08-18): the 2026-08-17 11:46Z
# decline registers as a DEEP, PREDOMINANTLY UNRECRUITED chain
EXPECT_WINDOW = ("2026-08-17 11:40:00+00:00", "2026-08-17 13:45:00+00:00")
EXPECT_DIR = -1
EXPECT_MIN_DEPTH = 3          # "deep" = chain spanning >=3 rungs
EXPECT_UNRECRUITED_FRAC = 0.5  # "predominantly unrecruited"


def zone_fence(start):
    """Refuse any readout span touching the lockbox (or working set)."""
    gl = zones()["go_live"]
    if gl is None:
        raise SystemExit("ZONE FENCE: no go_live stamp - forward zone "
                         "undefined")
    start = pd.Timestamp(start) if start is not None else gl
    if start < gl:
        raise SystemExit(f"ZONE FENCE: readout start {start} precedes "
                         f"go_live {gl} - forward readouts may not touch "
                         f"the lockbox or working set")
    refuse_if_sealed(start, what="forward readout start")
    return start


def _replay(cfg, instr):
    """Narrative-only replay over the FULL store (live-equivalent warm);
    mirrors backtest.loop's clock-ordered feed without broker/router."""
    df1 = load_frame(instr, "1min", narrative_scope=True)
    cash = trading_sessions(df1, cfg.session_model.trading_day_anchor_london)
    sig_tf, ctx_tf, ex_tf = (cfg.mtf.signal_tf, cfg.mtf.context_tf,
                             cfg.mtf.execution_tf)
    bars = {ex_tf: exec_bars(cash, tf=ex_tf),
            sig_tf: resample_bars(cash, _TFMIN[sig_tf], sig_tf),
            ctx_tf: resample_bars(cash, _TFMIN[ctx_tf], ctx_tf)}
    if cfg.session_model.get("ladder"):
        for tf, m in (("3min", 3), ("5min", 5), ("30min", 30),
                      ("1min", 1), ("15min", 15), ("1h", 60)):
            if tf not in bars:
                bars["ladder:" + tf] = (exec_bars(cash, tf=tf) if m == 1
                                        else resample_bars(cash, m, tf))
    engine = MTFEngine(cfg, narrative_only=True)
    by_ts = {}
    for key, blist in bars.items():
        for b in blist:
            by_ts.setdefault(b.ts, {})[key] = b
    for ts in sorted(by_ts):
        closed = by_ts[ts]
        kw = {}
        if ctx_tf in closed:
            kw["context_bar"] = closed[ctx_tf]
        if sig_tf in closed:
            kw["signal_bar"] = closed[sig_tf]
        if ex_tf in closed:
            kw["exec_bar"] = closed[ex_tf]
        lb = {k.split(":")[1]: v for k, v in closed.items()
              if k.startswith("ladder:")}
        if lb:
            kw["ladder_bars"] = lb
        engine.process(ts, **kw)
    n_sessions = int(cash["session_id"].nunique())
    return engine, bars, n_sessions


def grade_1146(fwd_events):
    """Mechanical grade of the pre-registered expectation; numbers only."""
    lo, hi = (pd.Timestamp(EXPECT_WINDOW[0]), pd.Timestamp(EXPECT_WINDOW[1]))
    win = [e for e in fwd_events
           if e["dir"] == EXPECT_DIR and lo <= e["ts"] <= hi]
    if not win:
        return {"window_events": 0, "matched": False,
                "note": "no dir=-1 chain events in the 11:46Z window"}
    max_depth = max(e["chain_rungs"] for e in win)
    unrec = sum(1 for e in win if not e["recruited"]) / len(win)
    # honesty split (instrument finding 2026-08-18): structural-only parent
    # labels carry no rel_volume, and recruited defaults False when rv is
    # unmeasured — "unrecruited" conflates measured-quiet with unmeasured
    measured = [e for e in win if e["recruitment_margin"] is not None]
    return {"window_events": len(win), "max_chain_rungs": max_depth,
            "unrecruited_fraction": round(unrec, 2),
            "rv_measured_events": len(measured),
            "rv_unmeasured_events": len(win) - len(measured),
            "recruitment_margins": [e["recruitment_margin"] for e in win],
            "expected": {"min_depth": EXPECT_MIN_DEPTH,
                         "unrecruited_frac >=": EXPECT_UNRECRUITED_FRAC},
            "matched": bool(max_depth >= EXPECT_MIN_DEPTH
                            and unrec >= EXPECT_UNRECRUITED_FRAC),
            "grading_caveats": [
                ("recruitment clause is VACUOUS when rv_measured_events=0: "
                 "unrecruited-by-default is not evidence about recruitment"),
                ("the instrument's depth = persistence chains (>=2 child "
                 "labels per parent window), NOT label-arrival cascades — "
                 "a single-label-per-rung cascade scores depth 1 by design"),
            ]}


def run(instr="uk100fut", start=None):
    start = zone_fence(start)
    cfg = make_cfg({"session_model.extended_hours": True,
                    "session_model.ladder": True})
    engine, bars, n_sessions = _replay(cfg, instr)
    mev = migration_events(engine.narrative.events, cfg)
    # sealed windows skipped automatically (register 30): forward reads
    # never touch a sealed span; skipped rows counted, never reported
    fwd_all = [e for e in mev if e["ts"] >= start]
    fwd = [e for e in fwd_all if not is_sealed(e["ts"])]
    n_sealed_skipped = len(fwd_all) - len(fwd)
    sig_fwd = [b for b in bars[cfg.mtf.signal_tf]
               if b.ts >= start and not is_sealed(b.ts)]
    head = subprocess.run(["git", "rev-parse", "HEAD"], cwd=ROOT,
                          capture_output=True, text=True).stdout.strip()
    end = max((b.ts for b in bars[cfg.mtf.execution_tf]), default=None)
    return {
        "STAMP": ("OBSERVATIONAL - forward-zone exhibit/evidence, NEVER "
                  "validation; small-n forward observation. The walk-forward "
                  "and the lockbox remain the only verdict machinery."),
        "engine_commit": head,
        "zone_statement": ("warm = full-store live-equivalent visibility "
                           "(narrative_scope load, logged); every emitted "
                           "row/aggregate strictly >= go_live"),
        "readout_span": [str(start), str(end)],
        "forward_sessions_total": n_sessions,
        "sealed_windows_skipped_events": n_sealed_skipped,
        "n_chain_events_forward": len(fwd),
        "graded_1146Z_expectation": grade_1146(fwd),
        "log": [{k: str(v) if isinstance(v, pd.Timestamp) else v
                 for k, v in e.items()} for e in fwd],
        "study": migration_study(fwd, sig_fwd),
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--instr", default="uk100fut")
    ap.add_argument("--start", default=None,
                    help="readout start (default go_live; earlier = refused)")
    a = ap.parse_args()
    os.makedirs(OUT, exist_ok=True)
    res = run(a.instr, a.start)
    s0, s1 = (pd.Timestamp(res["readout_span"][0]).strftime("%Y%m%d"),
              pd.Timestamp(res["readout_span"][1]).strftime("%Y%m%d"))
    path = os.path.join(OUT, f"migration_forward_{s0}_{s1}.json")
    with open(path, "w") as f:
        json.dump(res, f, indent=2, default=str)
    print(json.dumps({k: res[k] for k in
                      ("readout_span", "n_chain_events_forward",
                       "graded_1146Z_expectation")}, indent=1, default=str))
    print(f"OBSERVATIONAL readout -> {path}")


if __name__ == "__main__":
    main()
