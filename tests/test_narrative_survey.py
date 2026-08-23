"""Register 73 pins: vocabulary precedence, the pinned null seed set,
and null-calibration determinism (twin-run)."""
import json

import numpy as np

from backtest.narrative_survey import (CLASSES, CONS_MIN_CELLS,
                                       CONS_MIN_LIFT_PP, CONS_MIN_N,
                                       CONS_PCTL, FOCAL, NULL_SEEDS,
                                       NULL_SHUFFLES, SEQUEL_WINDOWS,
                                       _pair_qualifies, classify,
                                       survey_nulls)


def test_instrumentation():
    assert SEQUEL_WINDOWS == (5, 15)
    assert NULL_SHUFFLES == 100
    assert NULL_SEEDS == tuple(range(100))
    assert FOCAL == ("S0-H1", "absorption")
    assert CLASSES == ("absorption", "opposing", "effortless-same",
                       "trend-flip", "map-arrival", "none")


def _arrs(n, **kw):
    a = {"quad": np.array(["narrow-quiet"] * n, dtype=object),
         "closedir": np.ones(n, int),
         "test": np.zeros(n, bool),
         "eff_dir": np.zeros(n, int),
         "flip": np.zeros(n, bool),
         "h11": np.array(["neither"] * n, dtype=object),
         "h3": set()}
    a.update(kw)
    return a


def test_precedence_within_bar_and_first_bar():
    n = 10
    # one bar carrying flip + effortless-same + opposing signatures:
    # opposing outranks effortless outranks flip
    a = _arrs(n)
    a["quad"][2] = "wide-loud"
    a["closedir"][2] = -1          # anchor bar close dir = -1 (below)
    a["eff_dir"][2] = 1
    a["flip"][2] = True
    assert classify(0, 1, -1, 5, a, n) == "opposing"
    a["quad"][2] = "narrow-quiet"
    assert classify(0, 1, -1, 5, a, n) == "effortless-same"
    a["eff_dir"][2] = 0
    assert classify(0, 1, -1, 5, a, n) == "trend-flip"
    a["flip"][2] = False
    a["h11"][2] = "node"
    assert classify(0, 1, -1, 5, a, n) == "map-arrival"
    # map-arrival requires a CLASS CHANGE from the anchor bar
    a2 = _arrs(n)
    a2["h11"][:] = "node"
    assert classify(0, 1, -1, 5, a2, n) == "none"
    # earlier bar wins over later higher-precedence bar
    a3 = _arrs(n)
    a3["flip"][1] = True
    a3["test"][3] = True
    assert classify(0, 1, -1, 5, a3, n) == "trend-flip"


def test_null_calibration_deterministic_and_shaped():
    rs = np.random.RandomState(7)
    pairs = [(CLASSES[i % 3], bool(rs.randint(2))) for i in range(120)]
    cba = {("S0-Hx", 5, "backtest"): pairs,
           ("S0-Hx", 15, "forward"): pairs[:60]}
    bases = {(W, w, c): 45.0 for W in (5, 15)
             for w in ("backtest", "forward") for c in CLASSES}
    a = survey_nulls(cba, bases)
    b = survey_nulls(cba, bases)
    assert json.dumps(a, sort_keys=True) == json.dumps(b, sort_keys=True)
    assert a["shuffles"] == 100
    assert a["expected_max_abs_lift_pp"] > 0
    assert a["null_expected_glow_cells"] >= 0
    assert len(a["_cons_counts"]) == 100


def test_consistency_pair_rule():
    assert (CONS_MIN_CELLS, CONS_MIN_N, CONS_MIN_LIFT_PP, CONS_PCTL) \
        == (3, 15, 3.0, 95.0)
    # 3 measurable same-signed strong cells spanning both windows
    ok, nm, spans = _pair_qualifies(
        [("backtest", 30, 5.0), ("backtest", 25, 4.0),
         ("forward", 20, 6.0)])
    assert ok and nm == 3 and spans
    # a sub-threshold cell breaks it
    ok2, _, _ = _pair_qualifies(
        [("backtest", 30, 5.0), ("backtest", 25, 2.0),
         ("forward", 20, 6.0)])
    assert not ok2
    # mixed sign breaks it
    ok3, _, _ = _pair_qualifies(
        [("backtest", 30, 5.0), ("backtest", 25, -4.0),
         ("forward", 20, 6.0)])
    assert not ok3
    # n<15 cells don't count toward the 3
    ok4, nm4, _ = _pair_qualifies(
        [("backtest", 30, 5.0), ("backtest", 10, 9.0),
         ("forward", 20, 6.0)])
    assert not ok4 and nm4 == 2
