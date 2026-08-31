"""Register 121 pins (census half): rung-parent arithmetic (UTC grid),
the k-lag floor, per-event rv survival breaking on unmeasured or quiet
parents, and same-direction arrival within the registered window."""
import numpy as np

from backtest.aggregation_decay import (arrivals_by_rung, klag_floor_min,
                                        parent_open, survival_depth)
from backtest.migration import LADDER, _MIN

MIN = 60_000_000_000


def test_parent_open_and_klag_floor():
    t = 7 * MIN                                   # 00:07 UTC
    assert parent_open(t, 5) == 5 * MIN
    assert parent_open(t, 15) == 0
    assert klag_floor_min(t, 5) == 3              # 00:10 close
    assert klag_floor_min(t, 15) == 8             # 00:15 close
    assert klag_floor_min(parent_open(t, 60), 60) == 60


def test_survival_depth_breaks_on_quiet_or_unmeasured():
    t = 7 * MIN
    rv = {tf: {parent_open(t, _MIN[tf]): 2.0} for tf in LADDER}
    assert survival_depth(t, rv) == 6             # loud at every rung
    rv["5min"][parent_open(t, 5)] = 1.0           # quiet at rung 3
    assert survival_depth(t, rv) == 2
    del rv["3min"][parent_open(t, 3)]             # unmeasured at rung 2
    assert survival_depth(t, rv) == 1


def test_arrivals_same_direction_within_window():
    t = 0
    labels = {"3min": [(2 * MIN, -1), (4 * MIN, 1)],
              "15min": [(90 * MIN, 1)],           # beyond the window
              "1h": [(50 * MIN, 1)]}
    a = arrivals_by_rung(t, 1, labels, window_min=60)
    assert a["3min"] == 4                         # the -1 is skipped
    assert a["15min"] is None                     # outside 60 min
    assert a["1h"] == 50
    assert a["5min"] is None and a["30min"] is None
