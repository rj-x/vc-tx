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
