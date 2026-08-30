"""Register 63 pins: the bar-persistence measurement is deterministic
(twin-run), the horizons/ladders are the registered instrumentation, and
the spread netting genuinely shifts the reach threshold (the scalp
economics is not the gross column relabeled)."""
import json

import numpy as np
import pandas as pd

from backtest.bar_persistence import (ATR_LADDER, CENSUS_MIN_N, HORIZONS,
                                      PTS_LADDER, census_clears,
                                      persistence)


def test_census_clears_full_range_with_n():
    # register 108: a clear = net reach above the floor's range MAX (not
    # its median); n and the member count travel with the block;
    # measurable at CENSUS_MIN_N
    res = {"matched": {
        "S0-H7": {"forward": {"name": "B-RANDOM", "n": 61, "net": 18.0,
                              "delta_net_pp": 4.8,
                              "floor_net_median": 13.2,
                              "floor_net_range": [9.4, 17.5],
                              "floor_members": 20, "clears_range": True,
                              "measurable": True}},
        "S0-H3": {"forward": {"name": "B-RANDOM", "n": 20, "net": 20.0,
                              "delta_net_pp": 6.8,
                              "floor_net_median": 13.2,
                              "floor_net_range": [9.4, 17.5],
                              "floor_members": 20, "clears_range": True,
                              "measurable": False}},
        "S0-H1": {"forward": {"name": "B-RANDOM", "n": 90, "net": 13.3,
                              "delta_net_pp": 0.1,
                              "floor_net_median": 13.2,
                              "floor_net_range": [9.4, 17.5],
                              "floor_members": 20, "clears_range": False,
                              "measurable": True}}}}
    cc = census_clears(res)
    assert [c["signal"] for c in cc] == ["S0-H3", "S0-H7"]
    h7 = next(c for c in cc if c["signal"] == "S0-H7")
    assert h7["measurable"] and h7["delta_vs_range_max_pp"] == 0.5
    assert h7["floor_members"] == 20 and h7["n"] == 61
    assert not next(c for c in cc if c["signal"] == "S0-H3")["measurable"]
    assert CENSUS_MIN_N == 25

T0 = pd.Timestamp("2026-08-17 09:00", tz="UTC")


def _arrs(bars):
    ts = np.array([T0.value + i * 60_000_000_000 for i in range(len(bars))])
    o, h, l, c = (np.array([b[i] for b in bars], float) for i in range(4))
    return ts, o, h, l, c


def _fire(i=0, d=1):
    return [{"ts": T0 + pd.Timedelta(minutes=i), "dir": d, "name": "X"}]


def test_instrumentation_values():
    assert HORIZONS == (1, 3, 5, 10)
    assert PTS_LADDER == (2.0, 5.0, 10.0)
    assert ATR_LADDER == (0.25, 0.5, 1.0)


def test_spread_netting_shifts_the_threshold():
    # entry 100; high reaches 102.3 at bar 2: +2pts gross YES; with
    # spread 0.5 the net threshold is 102.5 -> net NO
    bars = [(100, 100, 100, 100), (100, 101, 99.8, 100.5),
            (100.5, 102.3, 100.2, 101), (101, 101.5, 100.5, 101)]
    ts, o, h, l, c = _arrs(bars)
    rows = persistence(_fire(0, 1), ts, o, h, l, c,
                       lambda t: 8.0, 0.5, home=True)
    r = rows[0]["reach"]["pts_2"][3]
    assert r["gross"] is True and r["net"] is False
    # ATR ladder: 0.25 x 8.0 = 2.0 -> same shape
    ra = rows[0]["reach"]["atr_0.25"][3]
    assert ra["gross"] is True and ra["net"] is False


def test_favorable_close_fraction_and_touch():
    # long from 100: closes 100.5, 101, 99 -> 2/3 favorable at N=3;
    # first touch of +0.25xATR(=2.0) at bar 2 (index offset 2)
    bars = [(100, 100, 100, 100), (100, 100.6, 99.8, 100.5),
            (100.5, 102.1, 100.2, 101), (101, 101.2, 98.9, 99)]
    ts, o, h, l, c = _arrs(bars)
    rows = persistence(_fire(0, 1), ts, o, h, l, c,
                       lambda t: 8.0, 0.0, home=False)
    assert abs(rows[0]["fav_frac"][3] - 2 / 3) < 1e-9
    assert rows[0]["touch_min"]["atr_0.25"] == 2


def test_twin_run_bit_identity():
    bars = [(100 + (i % 7) * 0.4, 100.9 + (i % 7) * 0.4,
             99.1 + (i % 5) * 0.3, 100.2 + (i % 3) * 0.3)
            for i in range(120)]
    ts, o, h, l, c = _arrs(bars)
    fires = [f for i in range(0, 100, 9)
             for f in _fire(i, 1 if i % 2 else -1)]
    a = persistence(fires, ts, o, h, l, c, lambda t: 6.0, 0.8, home=True)
    b = persistence(fires, ts, o, h, l, c, lambda t: 6.0, 0.8, home=True)
    assert json.dumps(a, sort_keys=True, default=str) \
        == json.dumps(b, sort_keys=True, default=str)


def test_expectancy_curve_and_spread_once():
    """Register 64 pins: cumulative expectancy = signed points at
    bar+k's close; increments telescope back to the cumulative; spread
    is charged ONCE (net = gross − spread at every k; only bar+1's
    increment nets it)."""
    from backtest.bar_persistence import _agg
    bars = [(100, 100, 100, 100), (100, 100.6, 99.8, 100.5),
            (100.5, 102.1, 100.2, 101), (101, 101.2, 98.9, 99),
            (99, 100.1, 98.5, 100)]
    ts, o, h, l, c = _arrs(bars)
    rows = persistence(_fire(0, 1), ts, o, h, l, c,
                       lambda t: 8.0, 0.4, home=False)
    cum = rows[0]["cum"]
    assert cum[1] == 0.5 and cum[2] == 1.0 and cum[3] == -1.0
    inc = rows[0]["inc"]
    assert abs(sum(inc[k] for k in sorted(inc)[:3]) - cum[3]) < 1e-9
    a = _agg(rows, spread=0.4)
    e = a["expectancy"]
    assert e[1]["cum_median_net"] == round(0.5 - 0.4, 2)
    assert e[3]["cum_median_net"] == round(-1.0 - 0.4, 2)
    assert e[1]["inc_median_net"] == round(0.5 - 0.4, 2)
    assert e[2]["inc_median_net"] == e[2]["inc_median_gross"]
    # peak-k = the bar where the cumulative net median tops out
    assert a["expectancy_peak"]["k"] == 2


def test_quadrant_conventions_mirror():
    """Register 68 pin: the fade convention is the exact sign mirror of
    the same-direction convention (same entries, flipped direction)."""
    bars = [(100, 100.6, 99.8, 100.5), (100.5, 101.2, 100.1, 101),
            (101, 101.4, 100.2, 100.4), (100.4, 100.9, 99.9, 100.6),
            (100.6, 101.1, 100.0, 100.2)]
    ts, o, h, l, c = _arrs(bars)
    fires = [{"ts": T0, "dir": 1, "name": "QUAD-x"}]
    fires_f = [{**f, "dir": -f["dir"]} for f in fires]
    a = persistence(fires, ts, o, h, l, c, lambda t: 6.0, 0.0)
    b = persistence(fires_f, ts, o, h, l, c, lambda t: 6.0, 0.0)
    for k in a[0]["cum"]:
        assert abs(a[0]["cum"][k] + b[0]["cum"][k]) < 1e-9
