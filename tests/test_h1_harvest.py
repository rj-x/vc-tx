"""Register 128 pins: the entry-offset grammar component (deferred
entry, validation), per-instrument derived stops (specialize; the
frozen mae60-p90 values; simulate refuses un-specialized components),
the confirm transform (first qualifying print, direction matching,
window expiry = no entry), the knife arm's stage composition (ratified
arming values), and the H1 scoping."""
import numpy as np
import pandas as pd
import pytest

from backtest.recipes import (H1_MAE60_P90_ATR, RECIPE_SET_VERSION,
                              RECIPE_SETS, Env, normalize, simulate,
                              specialize)
from backtest.trade_layer import (H1_SENTENCE, H1_VARIANTS, VARIANTS,
                                  confirm_transform)

T0 = pd.Timestamp("2026-08-17 09:00", tz="UTC")
MIN = 60_000_000_000


def _env(closes, atr=10.0):
    n = len(closes)
    ts = np.array([T0.value + i * MIN for i in range(n)])
    c = np.array(closes, float)
    o = np.concatenate([[c[0]], c[:-1]])
    h, l = np.maximum(o, c) + 0.2, np.minimum(o, c) - 0.2
    return Env((ts, o, h, l, c),
               {"15min": {"keys": np.array([0]),
                          "vals": np.array([atr])}},
               {"15min": (np.array([0]), np.array([1e9]),
                          np.array([-1e9])),
                "1min": (np.array([0]), np.array([1e9]),
                         np.array([-1e9]))},
               np.zeros(n, bool))


def _fire(i=0, d=1):
    return [{"ts": T0 + pd.Timedelta(minutes=i), "dir": d, "name": "X"}]


def test_entry_offset_defers_the_entry():
    closes = [100.0 + i for i in range(30)]
    env = _env(closes)
    base = {"stages": [{"stop": [("atr", 2.5, "15min")], "target": None}]}
    t0 = simulate(_fire(0), env, base, 0.0)[0]
    t3 = simulate(_fire(0), env,
                  {**base, "entry_offset_bars": 3}, 0.0)[0]
    assert pd.Timestamp(t3["entry_ts"]) \
        == pd.Timestamp(t0["entry_ts"]) + pd.Timedelta(minutes=3)
    assert t3["entry"] == t0["entry"] + 3.0        # later open
    with pytest.raises(ValueError, match="entry_offset_bars"):
        normalize({**base, "entry_offset_bars": -1})


def test_specialize_and_unspecialized_refusal():
    r = RECIPE_SETS[RECIPE_SET_VERSION]["R-H1-OWNCURVE"]
    s = specialize(r, "uk100fut")
    assert s["stages"][0]["stop"][0] == ("atr", 2.06, "15min")
    assert specialize(RECIPE_SETS[RECIPE_SET_VERSION]["R-NOTRAIL"],
                      "uk100fut") is RECIPE_SETS[RECIPE_SET_VERSION][
                          "R-NOTRAIL"]                 # pass-through
    assert H1_MAE60_P90_ATR == {"uk100fut": 2.06, "ger40fut": 2.96,
                                "nas100fut": 3.13, "us30fut": 2.23}
    env = _env([100.0] * 20)
    with pytest.raises(ValueError, match="un-specialized"):
        simulate(_fire(0), env, r, 0.0)


def test_confirm_transform_first_print_direction_and_expiry():
    fires = _fire(0, 1) + _fire(0, -1)
    labels = [((T0 + pd.Timedelta(minutes=2)).value, "NO_DEMAND", None),
              ((T0 + pd.Timedelta(minutes=4)).value, None, "TEST"),
              ((T0 + pd.Timedelta(minutes=6)).value, "NO_SUPPLY", None)]
    out = confirm_transform(fires, labels, 10)
    # the long skips the ND (wrong direction), takes the TEST at +4
    assert out[0]["dir"] == 1 and out[0]["ts"] \
        == T0 + pd.Timedelta(minutes=4)
    # the short's first qualifying print is the ND at +2
    assert out[1]["dir"] == -1 and out[1]["ts"] \
        == T0 + pd.Timedelta(minutes=2)
    # expiry = no entry (the -REF precedent)
    assert confirm_transform(_fire(0, 1),
                             [((T0 + pd.Timedelta(minutes=11)).value,
                               "NO_SUPPLY", None)], 10) == []


def test_knife_stage_composition_and_scoping():
    r = RECIPE_SETS[RECIPE_SET_VERSION]["R-H1-KNIFE"]
    s1, s2 = r["stages"]
    assert s1["exit_on"] == [("trend_flip",)]
    assert s1["until"] == ("progress_or_age", 1.0, "15min", 45)
    assert ("trail_nth", 1, ("atr", 1.0, "15min"), "15min") in s2["stop"]
    assert set(H1_VARIANTS) <= set(VARIANTS)
    assert H1_SENTENCE == "S0-H1"
    delay = RECIPE_SETS[RECIPE_SET_VERSION]["R-H1-DELAY10"]
    assert delay["entry_offset_bars"] == 10
    assert delay["stages"] is RECIPE_SETS[RECIPE_SET_VERSION][
        "R-ARM15"]["stages"]                     # the incumbent's base
