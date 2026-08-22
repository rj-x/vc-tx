"""Register 59 pins: the stop-width ladder is instrumentation registered
once — its values are pinned; the ladder simulation is deterministic
(twin-run bit-identity); R-NOSTOP genuinely never stops."""
import json

import numpy as np
import pandas as pd

from backtest.recipes import Env, simulate
from backtest.signal_points import LADDER_WIDTHS, ladder_recipes


def _env(bars, eod=None):
    t0 = pd.Timestamp("2026-08-17 09:00", tz="UTC").value
    ts = np.array([t0 + i * 60_000_000_000 for i in range(len(bars))])
    o, h, l, c = (np.array([b[i] for b in bars], float) for i in range(4))
    atr = {"15min": {"keys": np.array([t0 - 1]), "vals": [10.0]}}
    rung = {"1min": (ts, h, l)}
    e = np.zeros(len(bars), bool) if eod is None else eod
    return Env((ts, o, h, l, c), atr, rung, e)


def _fires(idxs):
    return [{"ts": pd.Timestamp("2026-08-17 09:00", tz="UTC")
             + pd.Timedelta(minutes=i), "dir": 1 if i % 2 else -1,
             "name": "X"} for i in idxs]


def test_ladder_values_are_the_registered_instrumentation():
    assert LADDER_WIDTHS == (1.5, 2.0, 3.0, 4.0, 5.0)
    r = ladder_recipes()
    assert set(r) == {"1.5x", "2x", "3x", "4x", "5x", "nostop"}
    for w in LADDER_WIDTHS:
        st = r[f"{w:g}x"]["stages"]
        assert st == [{"stop": [("atr", w, "15min")], "target": None}]
    assert r["nostop"]["stages"] == [{"stop": [], "target": None}]


def test_nostop_never_stops_only_eod():
    # a violent adverse run (for a LONG) that would hit every ladder stop
    bars = [(100, 100, 100, 100)] + [(100 - i * 8, 100 - i * 8,
                                      90 - i * 8, 92 - i * 8)
                                     for i in range(10)]
    eod = np.zeros(11, bool)
    eod[-1] = True
    fire = [{"ts": pd.Timestamp("2026-08-17 09:00", tz="UTC"), "dir": 1,
             "name": "X"}]
    tr = simulate(fire, _env(bars, eod=eod),
                  ladder_recipes()["nostop"], 0.0)
    assert tr[0]["reason"] == "eod"
    tr15 = simulate(fire, _env(bars, eod=eod),
                    ladder_recipes()["1.5x"], 0.0)
    assert tr15[0]["reason"] in ("stop", "stop_gap")


def test_ladder_twin_run_bit_identity():
    bars = [(100 + (i % 7) * 0.4, 100.8 + (i % 7) * 0.4,
             99.2 + (i % 5) * 0.3, 100.1 + (i % 3) * 0.35)
            for i in range(300)]
    eod = np.zeros(300, bool)
    eod[150] = eod[299] = True
    env = _env(bars, eod=eod)
    fires = _fires(range(0, 280, 11))
    for recipe in ladder_recipes().values():
        a = simulate(fires, env, recipe, 0.8)
        b = simulate(fires, env, recipe, 0.8)
        assert json.dumps(a, sort_keys=True) == json.dumps(b,
                                                           sort_keys=True)


def test_baseline_constants_and_fence():
    """Register 60 pins: B-RANDOM's seed and the cadence are registered
    values; the controls live outside the hypothesis namespace (fence:
    never candidates, never countable as signals)."""
    import re
    from backtest.signal_points import (BASELINE_INTERVAL_BARS,
                                        BASELINE_NAMES, BASELINE_SEED,
                                        DRIFT_SKEW_SHARE, TREND_FAMILY)
    assert BASELINE_SEED == 60
    assert BASELINE_INTERVAL_BARS == 60
    assert DRIFT_SKEW_SHARE == 0.8
    assert TREND_FAMILY == ("S0-H10", "S0-H14")
    assert set(BASELINE_NAMES) == {"B-TREND", "B-RANDOM", "B-ALWAYS-LONG"}
    for b in BASELINE_NAMES:
        assert not re.fullmatch(r"S\d+-H\d+", b)     # outside the namespace


def test_baseline_fires_deterministic():
    from backtest.signal_points import baseline_fires
    bars = [(100 + (i % 9) * 0.3, 100.5 + (i % 9) * 0.3,
             99.5 + (i % 4) * 0.2, 100.1) for i in range(400)]
    env = _env(bars)
    t0 = pd.Timestamp("2026-08-17 09:00", tz="UTC").value
    events = [{"type": "PHASE_EVAL", "tf": "1min",
               "ts": pd.Timestamp(t0 + i * 60_000_000_000, tz="UTC"),
               "trend": 1 if i > 50 else 0} for i in range(400)]
    a = baseline_fires(env, events)
    b = baseline_fires(env, events)
    assert json.dumps(a, sort_keys=True, default=str) \
        == json.dumps(b, sort_keys=True, default=str)
    assert len(a["B-ALWAYS-LONG"]) > 0 and len(a["B-RANDOM"]) > 0
    # B-TREND respects the establishment gate: no fires before the trend
    # has run ESTABLISHED_TREND_AGE bars
    assert all(f["ts"].value >= t0 + 60 * 60_000_000_000
               for f in a["B-TREND"])
