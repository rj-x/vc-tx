"""Core architectural requirement (item 14): one engine, multiple feeds —
the same definition over the same bars via the lab path (bulk run_backtest)
and via a simulated-clock incremental path (paper-style per-timestamp
process calls) produces bit-identical decisions and fills."""

from helpers import scenario_cfg
from test_resample_loop import _synthetic_clean_store

from backtest.loop import run_backtest, build_bars, session_fns
from engine.pipeline import MTFEngine


def _cfg():
    return scenario_cfg({
        "features.baseline_mode": "session_time",
        "features.baseline_sessions": 6,
        "features.min_baseline_obs": 4,
        "instruments.synth": {
            "session_start_london": 8.0, "session_end_london": 16.5,
            "tick_size": 0.1, "point_value": 1.0, "auction_exclusion_min": 10},
    })


def test_lab_vs_simulated_clock_paper_identical(tmp_path):
    root, _ = _synthetic_clean_store(tmp_path, n_sessions=12)
    cfg = _cfg()
    lab_engine, _ = run_backtest(cfg, "synth", root=root)

    # simulated-clock paper path: same bars, incremental per-close calls
    bars, _ = build_bars(cfg, "synth", root=root)
    embargo_fn, eod_fn = session_fns(cfg, "synth")
    inst = cfg.instruments["synth"]
    eng = MTFEngine(cfg, embargo_fn=embargo_fn, eod_fn=eod_fn,
                    tick_size=inst.tick_size, point_value=inst.point_value)
    merged = {}
    role_of = {cfg.mtf.context_tf: "context_bar",
               cfg.mtf.signal_tf: "signal_bar",
               cfg.mtf.execution_tf: "exec_bar"}
    for tf, blist in bars.items():
        for b in blist:
            merged.setdefault(b.ts, {})[role_of[tf]] = b
    for ts in sorted(merged):
        eng.process(ts, **merged[ts])

    assert lab_engine.narrative.events == eng.narrative.events, \
        "decisions diverge between lab and simulated-clock paths"
    assert lab_engine.broker.trades == eng.broker.trades, \
        "fills diverge between lab and simulated-clock paths"
