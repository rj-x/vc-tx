"""Pre-flight (go-live gate): (1) simulated-clock full-session drill of the
paper mechanics — open, embargo, force-flat, close, mid-session kill +
restart reconciliation + coverage-gap logging; ledger delivered to
reports/paper/drill/. (2) migration-stub fence."""

import json
import os

import pandas as pd
import pytest

from helpers import scenario_cfg
from test_resample_loop import _synthetic_clean_store

from backtest.loop import build_bars, session_fns
from engine.pipeline import MTFEngine
from engine.paper import _led, reconcile
from engine.strategy import load_definition

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DRILL = os.path.join(ROOT, "reports", "paper", "drill", "drill_ledger.jsonl")


def _mk_engine(cfg):
    embargo_fn, eod_fn = session_fns(cfg, "synth")
    inst = cfg.instruments["synth"]
    return (MTFEngine(cfg, embargo_fn=embargo_fn, eod_fn=eod_fn,
                      tick_size=inst.tick_size,
                      point_value=inst.point_value), embargo_fn)


def test_simulated_clock_session_drill(tmp_path):
    if os.path.exists(DRILL):
        os.remove(DRILL)
    _led({"event": "DRILL_BANNER",
          "note": "SYNTHETIC DRILL - NOT A LIVE LEDGER"}, DRILL)
    root, _ = _synthetic_clean_store(tmp_path, n_sessions=10)
    cfg = scenario_cfg({
        "features.baseline_mode": "session_time",
        "features.baseline_sessions": 6, "features.min_baseline_obs": 4,
        "execution_vehicle.mode": "direct",
        "instruments.synth": {
            "session_start_london": 8.0, "session_end_london": 16.5,
            "tick_size": 0.1, "point_value": 1.0, "auction_exclusion_min": 10},
    })
    bars, _ = build_bars(cfg, "synth", root=root)
    engine, embargo_fn = _mk_engine(cfg)
    merged = {}
    role_of = {cfg.mtf.context_tf: "context_bar",
               cfg.mtf.signal_tf: "signal_bar",
               cfg.mtf.execution_tf: "exec_bar"}
    for tf, bl in bars.items():
        for b in bl:
            merged.setdefault(b.ts, {})[role_of[tf]] = b
    ts_all = sorted(merged)
    last_session = max(b.session_id for b in bars[cfg.mtf.execution_tf])
    sess_ts = [t for t in ts_all
               if merged[t].get("exec_bar")
               and merged[t]["exec_bar"].session_id == last_session]
    kill_at = sess_ts[len(sess_ts) // 3]

    # ---- run 1: process into the final session; force a position at
    # mid-morning (mechanics drill); kill mid-session with position open
    opened = False
    for t in ts_all:
        if t > kill_at:
            break
        engine.process(t, **merged[t])
        eb = merged[t].get("exec_bar")
        if (not opened and eb is not None and eb.session_id == last_session
                and len([x for x in sess_ts if x <= t]) > 60):
            ok = engine.broker.open_position({
                "entry_ts": t, "dir": 1, "price": eb.close, "fill": None,
                "stop": eb.close - 5, "tag": "DRILL", "gate_tag": None,
                "h": {"spec": "DRILL", "dir": 1}})
            assert ok
            _led({"event": "ENTRY", "tag": "FORWARD_PAPER", "entry_ts": str(t),
                  "price": eb.close}, DRILL)
            opened = True
    assert opened and engine.broker.position is not None
    _led({"event": "STOP", "note": "mid-session kill (drill)",
          "last_processed": str(kill_at)}, DRILL)

    # ---- restart: reconcile dangling position + coverage gap
    n = reconcile(DRILL)
    assert n == 1
    _led({"event": "COVERAGE_GAP", "from": str(kill_at),
          "note": "downtime hole - decisions never backfilled"}, DRILL)
    engine2, embargo_fn = _mk_engine(cfg)
    for t in ts_all:                                  # warm + resume
        engine2.process(t, **merged[t])
        eb = merged[t].get("exec_bar")
        if (t > kill_at and engine2.broker.position is None
                and eb is not None and eb.session_id == last_session
                and not embargo_fn(t)
                and len([x for x in sess_ts if x <= t]) > len(sess_ts) - 90):
            engine2.broker.open_position({
                "entry_ts": t, "dir": 1, "price": eb.close, "fill": None,
                "stop": eb.close - 5, "tag": "DRILL2", "gate_tag": None,
                "h": {"spec": "DRILL", "dir": 1}})
    # EOD force-flat must have closed any late position
    assert engine2.broker.position is None, "force-flat failed"
    eods = [tr for tr in engine2.broker.trades if tr["reason"] == "EOD_EXIT"]
    stops = [tr for tr in engine2.broker.trades if "STOP" in tr["reason"]]
    assert eods or stops, "drill position neither force-flattened nor stopped"
    for tr in engine2.broker.trades:
        _led({"event": "EXIT", "tag": "FORWARD_PAPER", **tr}, DRILL)
    # embargo check: attempted entry inside embargo is refused by router
    # (router path exercised in s-suite); here assert fn behavior directly
    late = sess_ts[-1]
    assert embargo_fn(late), "embargo must be active at session end"
    _led({"event": "DRILL_COMPLETE", "eod_exits": len(eods),
          "trades": len(engine2.broker.trades)}, DRILL)
    assert os.path.exists(DRILL)


def test_migration_stub_fence(tmp_path):
    p = tmp_path / "m.yaml"
    p.write_text("name: mtest\nmode: signal_rules\nrules:\n"
                 "  - direction: 1\n    all:\n"
                 "      - {type: migration, min_rungs: 2}\n")
    with pytest.raises(NotImplementedError, match="v1.1 STUB"):
        load_definition(str(p))
