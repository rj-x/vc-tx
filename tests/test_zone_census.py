"""Register 95/96 pins: the deceleration detector (three successive
new extremes, strictly declining leg velocity, registered swing legs);
the H4 zone ladder (fractal swings, qualifying reversal at the rung's
multiple, significance filter, activation at confirmation,
invalidation beyond); scalar and vectorized tagging agreeing; visit
numbering; twin-run."""
import json

import numpy as np
import pandas as pd

from backtest.intra_trade_census import deceleration_flags
from backtest.zone_census import (active_at_once, build_zones,
                                  fractal_swings, in_zone,
                                  significant, session_ordinals,
                                  tag_bars, visit_numbers)


def test_deceleration_three_decelerating_up_legs():
    ts = np.arange(60) * 60_000_000_000
    log = [{"conf_ts": ts[3], "type": "L", "idx": 0, "price": 100.0},
           {"conf_ts": ts[13], "type": "H", "idx": 10, "price": 110.0},
           {"conf_ts": ts[18], "type": "L", "idx": 15, "price": 104.0},
           {"conf_ts": ts[28], "type": "H", "idx": 25, "price": 112.0},
           {"conf_ts": ts[33], "type": "L", "idx": 30, "price": 108.0},
           {"conf_ts": ts[48], "type": "H", "idx": 45, "price": 114.0}]
    up, dn = deceleration_flags(log, ts)
    assert up[48] and up.sum() == 1 and not dn.any()
    log[3]["price"] = 120.0
    up2, _ = deceleration_flags(log, ts)
    assert not up2.any()


def _h4(prices, bars_per_day=6):
    n = len(prices)
    t = pd.date_range("2026-01-01", periods=n, freq="4h", tz="UTC")
    p = np.array(prices, float)
    ldate = [str((i // bars_per_day)) for i in range(n)]
    return pd.DataFrame({"time": t, "open": p, "high": p + 1.0,
                         "low": p - 1.0, "close": p, "ldate": ldate})


def _peak_series():
    return ([100 + i for i in range(21)]
            + [120 - 3 * i for i in range(1, 30)]
            + [34 + i for i in range(10)])


def test_zone_builder_ladder_and_significance():
    df = _h4(_peak_series())
    sw = fractal_swings(df["high"].to_numpy(), df["low"].to_numpy(), 3)
    assert any(s[1] == "H" and s[0] == 20 for s in sw)
    zs = build_zones(df, 3, 14, 1.5)
    highs = [z for z in zs if z["type"] == "H"]
    assert highs and abs(highs[0]["level"] - 121.0) < 1e-9
    ts = df["time"].astype("int64").to_numpy()
    assert highs[0]["active_from"] > ts[20]          # no lookahead
    # the peak is the 5-session high when formed (monotone rise)
    sess = session_ordinals(df["ldate"].tolist())
    assert significant(20, "H", df["high"].to_numpy(),
                       df["low"].to_numpy(), sess, 5)
    assert build_zones(df, 3, 14, 1.5, 5)          # survives the filter
    # a stricter multiple still qualifies this deep reversal; a
    # ridiculous one does not
    assert build_zones(df, 3, 14, 3.0)
    assert not build_zones(df, 3, 14, 300.0)


def test_scalar_and_vector_tagging_agree_and_visits():
    df = _h4(_peak_series())
    zs = build_zones(df, 3, 14, 1.5)
    z = [x for x in zs if x["type"] == "H"][0]
    t0 = int(z["active_from"])
    ts = np.array([t0 + 1 + i * 60_000_000_000 for i in range(8)])
    cl = np.array([121.2, 121.1, 140.0, 140.0, 121.0, 121.3, 150.0,
                   121.0])
    atr = np.full(8, 4.0)                            # band 1.0
    zid = tag_bars(ts, cl, atr, zs)
    for i in range(8):
        iz, _d, zi = in_zone(float(cl[i]), int(ts[i]), 4.0, zs)
        assert (zid[i] >= 0) == iz
    v = visit_numbers(zid)
    assert list(v[:2]) == [1, 1] and v[2] == -1
    assert list(v[4:6]) == [2, 2] and v[7] == 3


def test_zone_twin_run():
    df = _h4([100 + (i % 17) * 3 for i in range(120)])
    a = json.dumps(build_zones(df, 3, 14, 1.5, 3), sort_keys=True)
    b = json.dumps(build_zones(df, 3, 14, 1.5, 3), sort_keys=True)
    assert a == b


def test_active_at_once_seeds_with_pre_span_zones():
    zs = [{"active_from": 0, "invalidated_at": None},
          {"active_from": 5, "invalidated_at": 50},
          {"active_from": 20, "invalidated_at": 30},
          {"active_from": 200, "invalidated_at": None}]
    assert active_at_once(zs, 10, 100) == 3     # two live at 10, +1 at 20
    assert active_at_once(zs, 60, 100) == 1     # only the perpetual one
    assert active_at_once([], 0, 1) == 0
