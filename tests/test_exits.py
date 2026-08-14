"""Part-1 exit-scheme library units."""
from engine.exits import ExitScheme


def test_initial_stops_and_targets():
    s = ExitScheme({"name": "r_multiple", "r": 2.0,
                    "stop": {"name": "atr_k", "k": 1.5}}, tick=0.5)
    stop = s.initial_stop(1, 100.0, 95.0, atr=2.0, swings={})
    assert stop == 97.0
    assert s.target(1, 100.0, stop) == 106.0
    f = ExitScheme({"name": "fixed_points", "points": 10,
                    "stop": {"name": "fixed_points", "points": 5}})
    assert f.initial_stop(-1, 100.0, None, None, {}) == 105.0
    assert f.target(-1, 100.0, 105.0) == 90.0
    sw = ExitScheme({"stop": {"name": "beyond_swing_n", "buffer_ticks": 2}},
                    tick=0.5)
    assert sw.initial_stop(1, 100.0, 90.0, None, {"low": 97.0}) == 96.0
    assert sw.initial_stop(1, 100.0, 90.0, None, {}) == 90.0   # fallback


def test_trailing_tightens_only_and_breakeven():
    s = ExitScheme({"trail": {"name": "trail_atr", "k": 2.0},
                    "breakeven_at_r": 1.0})
    pos = {"dir": 1, "stop": 95.0, "entry": 100.0, "stop_dist": 5.0}
    assert s.update_stop(pos, 102.0, 99.0, atr=2.0, swings={}) == 98.0
    pos["stop"] = 98.0
    assert s.update_stop(pos, 101.0, 99.0, atr=2.0, swings={}) == 98.0  # never loosens
    # +1R touch: breakeven pulls to entry, but trail_atr (105.5-4=101.5)
    # is tighter and wins — schemes compose, tightest stop stands
    assert s.update_stop(pos, 105.5, 99.0, atr=2.0, swings={}) == 101.5
    sw = ExitScheme({"trail": {"name": "trail_swing", "buffer_ticks": 0}})
    pos2 = {"dir": -1, "stop": 110.0, "entry": 100.0, "stop_dist": 10.0}
    assert sw.update_stop(pos2, 104.0, 99.0, None, {"high": 106.0}) == 106.0
