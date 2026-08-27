"""Register 94 pins: the atr_haircut target semantics (fill only
beyond the level by the haircut; exit at the level; EOD-flat on
non-reach), the v0.7 set, and the scalp variants' presence."""
import numpy as np
import pandas as pd

from backtest.recipes import (RECIPE_SET_VERSION, RECIPE_SETS, Env,
                              simulate)
from backtest.trade_layer import SCALP_SENTENCE, SCALP_VARIANTS, VARIANTS


def _env(highs, eod_idx=None):
    n = len(highs)
    ts = np.array([i * 60_000_000_000 for i in range(n)])
    h = np.array(highs, float)
    o = np.full(n, 100.0)
    l = o - 0.5
    c = o + 0.1
    eod = np.zeros(n, bool)
    if eod_idx is not None:
        eod[eod_idx] = True
    atr = {"15min": {"keys": [ts[0]], "vals": [4.0]}}
    return Env((ts, o, h, l, c), atr, {}, eod)


def _fire():
    return [{"ts": pd.Timestamp(0, tz="UTC"), "dir": 1, "name": "S"}]


def test_haircut_fill_semantics():
    recipe = RECIPE_SETS["recipe_set_v0.7"]["R-SCALP-H6"]
    # level = 100 + 0.5*4 = 102; haircut 0.5 -> needs high >= 102.5;
    # bar2 102.4 must NOT fill, bar3 102.5 fills AT 102
    t = simulate(_fire(), _env([100.2, 101.9, 102.4, 102.5, 102.6]),
                 recipe, 1.0)
    assert len(t) == 1 and t[0]["reason"] == "target"
    assert t[0]["exit"] == 102.0 and t[0]["pts"] == 1.0   # 2 - spread


def test_nonreach_is_eod_flat():
    recipe = RECIPE_SETS["recipe_set_v0.7"]["R-SCALP-H6"]
    t = simulate(_fire(), _env([100.2, 101.0, 101.5, 101.9],
                               eod_idx=3), recipe, 1.0)
    assert len(t) == 1 and t[0]["reason"] == "eod"


def test_v07_registered_and_scoped():
    assert RECIPE_SET_VERSION == "recipe_set_v0.7"
    for v in ("R-SCALP-H6", "R-SCALP-H6-REF"):
        assert v in RECIPE_SETS[RECIPE_SET_VERSION]
        assert v in VARIANTS and v in SCALP_VARIANTS
    assert SCALP_SENTENCE == "S0-H" + str(6)
