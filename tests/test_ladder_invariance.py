"""Evidential-path invariance (2026-08-14 order): ladder-on vs ladder-off
runs must produce IDENTICAL evidential outputs — trades, funnel events,
event-study inputs. Makes "observational build touched nothing evidential"
a tested fact, not a design intention."""

from helpers import scenario_cfg
from test_resample_loop import _synthetic_clean_store

from backtest.loop import run_backtest

EVIDENTIAL = ("SPAWNED", "CONFIRM", "GATE", "GATE_RECHECK", "GRADUATED",
              "REFUTED", "EXPIRED", "CONFIRMED_PENDING_GATE", "ENTRY", "EXIT",
              "STRENGTH", "PHASE", "LABEL")


def _run(root, ladder):
    cfg = scenario_cfg({
        "features.baseline_mode": "session_time",
        "features.baseline_sessions": 6,
        "features.min_baseline_obs": 4,
        "session_model.ladder": ladder,
        "instruments.synth": {
            "session_start_london": 8.0, "session_end_london": 16.5,
            "tick_size": 0.1, "point_value": 1.0, "auction_exclusion_min": 10},
    })
    engine, _ = run_backtest(cfg, "synth", root=root)
    stack = {cfg.mtf.context_tf, cfg.mtf.signal_tf, cfg.mtf.execution_tf, None}
    ev = [e for e in engine.narrative.events
          if e["type"] in EVIDENTIAL and e.get("tf") in stack]
    return ev, engine.broker.trades


def test_ladder_on_off_evidential_outputs_identical(tmp_path):
    root, _ = _synthetic_clean_store(tmp_path, n_sessions=12)
    ev_off, tr_off = _run(root, False)
    ev_on, tr_on = _run(root, True)
    assert len(ev_off) > 100, "synthetic run too quiet to be meaningful"
    assert ev_off == ev_on, "ladder build leaked into evidential events"
    assert tr_off == tr_on, "ladder build leaked into trade records"
