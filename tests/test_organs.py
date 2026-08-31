"""Register 119/120/122 pins: organ #4's signed-volume fields (doji
zero, trailing window, day reset), organ #2-half's efficiency ratio
(straight line = 1, chop < 1, day reset), organ #5's dwell episodes
(maximal runs, day-broken, window keyed at the first bar) — and
twin-run determinism for each."""
import json

import numpy as np

from backtest.dwell_census import dwell_episodes
from backtest.efficiency import EFF_WINDOW_BARS, eff15, eff_session
from backtest.signed_volume import (SV_WINDOW_BARS, sv15, sv_bar,
                                    sv_session)

DAY = 86_400_000_000_000
MIN = 60_000_000_000


def test_sv_bar_and_window():
    o = np.array([100.0, 100.0, 100.0])
    c = np.array([101.0, 99.0, 100.0])          # up, down, doji
    v = np.array([10.0, 20.0, 30.0])
    assert sv_bar(o, c, v).tolist() == [10.0, -20.0, 0.0]
    a = sv15(o, c, v, window=2)
    assert a.tolist() == [10.0, -10.0, -20.0]   # trailing-2 sums
    assert SV_WINDOW_BARS == 15


def test_sv_session_resets_at_day_change():
    ts = np.array([0, MIN, DAY, DAY + MIN])
    o = np.array([100.0] * 4)
    c = np.array([101.0, 101.0, 101.0, 99.0])
    v = np.array([5.0, 5.0, 7.0, 3.0])
    s = sv_session(o, c, v, ts)
    assert s.tolist() == [5.0, 10.0, 7.0, 4.0]  # reset at the new day
    assert json.dumps(s.tolist()) == json.dumps(
        sv_session(o, c, v, ts).tolist())        # twin-run


def test_efficiency_straight_line_and_chop():
    line = np.arange(100.0, 130.0)               # straight: eff = 1
    e = eff15(line, window=10)
    assert np.allclose(e[10:], 1.0)
    chop = np.array([100.0, 101.0] * 15)         # pure chop: eff ~ 0
    ec = eff15(chop, window=10)
    assert np.nanmax(ec[10:]) <= 0.11
    assert np.isnan(e[:10]).all()                # warmup carries NaN
    assert EFF_WINDOW_BARS == 15
    ts = np.array([i * MIN for i in range(4)])
    es = eff_session(np.array([100.0, 101.0, 102.0, 103.0]), ts)
    assert np.isnan(es[0]) and np.allclose(es[1:], 1.0)
    ts2 = np.array([0, MIN, DAY, DAY + MIN])
    es2 = eff_session(np.array([100.0, 101.0, 105.0, 104.0]), ts2)
    assert np.isnan(es2[2])                      # day reset re-anchors


def test_dwell_episodes_day_broken_and_window_keyed():
    state = np.array([True, True, False, True, True, True, True])
    days = np.array([0, 0, 0, 0, 0, 1, 1])      # day change inside a run
    wmask = {"w": np.array([True] * 7),
             "late": np.array([False, False, False, True, True, True,
                               True])}
    runs = dwell_episodes(state, days, wmask)
    assert sorted(runs["w"]) == [2, 2, 2]        # the day break splits 4
    assert sorted(runs["late"]) == [2, 2]        # keyed at the FIRST bar
    assert dwell_episodes(np.zeros(3, bool), np.zeros(3),
                          {"w": np.ones(3, bool)}) == {"w": []}
