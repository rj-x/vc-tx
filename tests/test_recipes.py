"""Register 41/42 honest-fill rules — each rule pinned as the incident
class it prevents — plus composition, staging, narrative-exit capability,
and twin-run bit-identity (the determinism doctrine)."""
import json

import numpy as np
import pandas as pd

from backtest.recipes import Env, simulate


def _env(bars, eod=None, narr=None):
    t0 = pd.Timestamp("2026-08-17 09:00", tz="UTC").value
    ts = np.array([t0 + i * 60_000_000_000 for i in range(len(bars))])
    o, h, l, c = (np.array([b[i] for b in bars], float) for i in range(4))
    atr = {"15min": {"keys": np.array([t0 - 1]), "vals": [10.0]},
           "5min": {"keys": np.array([t0 - 1]), "vals": [4.0]}}
    rung = {"1min": (ts, h, l)}
    e = np.zeros(len(bars), bool) if eod is None else eod
    return Env((ts, o, h, l, c), atr, rung, e, narr)


def _fire(i=0, d=1):
    return [{"ts": pd.Timestamp("2026-08-17 09:00", tz="UTC")
             + pd.Timedelta(minutes=i), "dir": d, "name": "X"}]


def _stage(stop, target=None, **kw):
    return {"stages": [{"stop": stop, "target": target, **kw}]}


def test_rule1_both_reachable_stop_fills():
    bars = [(100, 100, 100, 100), (100, 100, 100, 100),
            (100, 120, 90, 105)]
    tr = simulate(_fire(0, 1), _env(bars),
                  _stage([("fixed_pts", 5.0)], ("fixed_pts", 10.0)), 0.0)
    assert tr[0]["reason"] == "stop" and tr[0]["exit"] == 95.0


def test_rule2_gap_fills_at_worse_price():
    bars = [(100, 100, 100, 100), (100, 101, 99, 100), (88, 89, 87, 88)]
    tr = simulate(_fire(0, 1), _env(bars),
                  _stage([("fixed_pts", 5.0)]), 0.0)
    assert tr[0]["reason"] == "stop_gap" and tr[0]["exit"] == 88.0


def test_rule3_composed_stop_ratchets_only():
    # initial ATR stop 100-15=85 composed with a rising 2nd-bar trail; the
    # effective stop takes the TIGHTER and never loosens when lows fall
    bars = [(100, 101, 95, 100), (100, 101, 96, 100), (100, 101, 97, 100),
            (100, 101, 98, 100), (100, 101, 90, 100), (100, 101, 98.4, 99)]
    tr = simulate(_fire(0, 1), _env(bars),
                  _stage([("atr", 1.5, "15min"),
                          ("trail_nth", 2, ("pts", 0.0), "1min")]), 0.0)
    assert tr[0]["reason"] == "stop" and tr[0]["exit"] == 97.0


def test_rule4_eod_flat_at_native_close():
    bars = [(100, 100, 100, 100), (100, 101, 99, 100), (100, 102, 99, 101)]
    eod = np.array([False, False, True])
    tr = simulate(_fire(0, 1), _env(bars, eod=eod),
                  _stage([("fixed_pts", 50.0)]), 0.0)
    assert tr[0]["reason"] == "eod" and tr[0]["exit"] == 101.0


def test_stage_transition_arms_trail():
    # stage 1: wide fixed stop until +0.5xATR(5min)=+2pts progress; then
    # stage 2: tight 1-pt fixed stop. Progress at bar1 high 103 -> armed
    # from bar 2; bar 3 low 98.5 hits the tightened stop at 99.
    bars = [(100, 100, 100, 100), (100, 103, 100, 102),
            (102, 102.5, 101, 102), (102, 102, 98.5, 99)]
    r = {"stages": [
        {"stop": [("fixed_pts", 50.0)], "target": None,
         "until": ("progress_atr", 0.5, "5min")},
        {"stop": [("fixed_pts", 1.0)], "target": None}]}
    tr = simulate(_fire(0, 1), _env(bars), r, 0.0)
    assert tr[0]["reason"] == "stop" and tr[0]["exit"] == 99.0


def test_narrative_exit_capability():
    t0 = pd.Timestamp("2026-08-17 09:00", tz="UTC").value
    bars = [(100, 100, 100, 100)] + [(100, 101, 99, 100)] * 5
    narr = {"opposing_signal_fire": [(t0 + 3 * 60_000_000_000, -1)]}
    tr = simulate(_fire(0, 1), _env(bars, narr=narr),
                  _stage([("fixed_pts", 50.0)],
                         exit_on=[("opposing_signal_fire",)]), 0.0)
    assert tr[0]["reason"] == "narrative"


def test_atr_component_requires_declared_tf():
    import pytest
    with pytest.raises(ValueError, match="declared TF"):
        simulate(_fire(0, 1), _env([(100, 100, 100, 100)] * 3),
                 {"stages": [{"stop": [("atr", 1.5)], "target": None}]}, 0.0)


def test_one_position_and_spread():
    bars = [(100, 100, 100, 100)] + [(100, 101, 99, 100)] * 8
    eod = np.zeros(9, bool)
    eod[-1] = True
    fires = _fire(0, 1) + _fire(1, 1) + _fire(2, 1)
    tr = simulate(fires, _env(bars, eod=eod),
                  _stage([("fixed_pts", 50.0)]), 0.8)
    assert len(tr) == 1 and tr[0]["pts"] == round(0.0 - 0.8, 2)


def test_twin_run_bit_identity():
    bars = [(100 + (i % 5) * 0.3, 100.6 + (i % 5) * 0.3,
             99.4 + (i % 3) * 0.2, 100.1 + (i % 4) * 0.25)
            for i in range(200)]
    eod = np.zeros(200, bool)
    eod[100] = eod[199] = True
    env = _env(bars, eod=eod)
    fires = [f for i in range(0, 180, 7)
             for f in _fire(i, 1 if i % 2 else -1)]
    r = {"stages": [
        {"stop": [("atr", 1.5, "15min"),
                  ("trail_nth", 6, ("atr", 0.5, "15min"), "1min")],
         "target": ("atr", 3.0, "15min"),
         "until": ("progress_atr", 1.0, "15min")},
        {"stop": [("breakeven", 0.0)], "target": None}]}
    a = simulate(fires, env, r, 0.8)
    b = simulate(fires, env, r, 0.8)
    assert json.dumps(a, sort_keys=True) == json.dumps(b, sort_keys=True)


def test_progress_or_age_transition_arms_by_time():
    # no progress; stage 1 (wide stop + narrative exit) must expire by AGE
    # after 3 min, after which the narrative event no longer exits
    t0 = pd.Timestamp("2026-08-17 09:00", tz="UTC").value
    bars = [(100, 100, 100, 100)] + [(100, 100.4, 99.6, 100)] * 9
    narr = {"trend_flip": [(t0 + 6 * 60_000_000_000, -1)]}
    eod = np.zeros(10, bool)
    eod[-1] = True
    r = {"stages": [
        {"stop": [("fixed_pts", 50.0)], "target": None,
         "exit_on": [("trend_flip",)],
         "until": ("progress_or_age", 5.0, "15min", 3)},
        {"stop": [("fixed_pts", 50.0)], "target": None}]}
    tr = simulate(_fire(0, 1), _env(bars, eod=eod, narr=narr), r, 0.0)
    assert tr[0]["reason"] == "eod"        # flip at min 6 ignored: stage 2
    # and the mirror: flip BEFORE arming exits
    narr2 = {"trend_flip": [(t0 + 2 * 60_000_000_000, -1)]}
    tr2 = simulate(_fire(0, 1), _env(bars, eod=eod, narr=narr2), r, 0.0)
    assert tr2[0]["reason"] == "narrative"


def test_geometry_twin_run_and_stop_wins_race():
    """Register 52 pins: geometry() is deterministic (twin-run) and the
    -6xATR bound wins an intrabar tie per honest-fill rule 1."""
    import json as _json
    from backtest.excursion_geometry import geometry
    t0 = pd.Timestamp("2026-08-17 09:00", tz="UTC").value
    ts = np.array([t0 + i * 60_000_000_000 for i in range(50)])
    o = np.full(50, 100.0); c = o.copy()
    h = o + 0.5; l = o - 0.5
    # bar 3 spans BOTH +0.5*ATR target (105) and -6*ATR stop (40): stop wins
    h[3], l[3] = 200.0, 30.0
    eod = np.zeros(50, bool); eod[-1] = True
    fires = [{"ts": pd.Timestamp(t0, tz="UTC"), "dir": 1, "name": "X"}]
    r1 = geometry(fires, ts, o, h, l, c, lambda t: 10.0, eod)
    r2 = geometry(fires, ts, o, h, l, c, lambda t: 10.0, eod)
    assert _json.dumps(r1, default=str) == _json.dumps(r2, default=str)
    assert r1[0]["reached"]["atr_0.5"] is False   # stop won the tie
