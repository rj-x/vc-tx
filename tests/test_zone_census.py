"""Register 95 pins: the deceleration detector (three successive new
extremes, strictly declining leg velocity, registered swing legs), the
H4 zone builder (fractal swings, qualifying reversal, activation at
confirmation, invalidation beyond), in-zone tagging, and twin-run."""
import json

import numpy as np
import pandas as pd

from backtest.intra_trade_census import deceleration_flags
from backtest.zone_census import build_zones, fractal_swings, in_zone


def test_deceleration_three_decelerating_up_legs():
    ts = np.arange(60) * 60_000_000_000
    # L(0,100) -> H(10,110) v=1.0 ; L(15,104) -> H(25,112) v=0.8 ;
    # L(30,108) -> H(45,114) v=0.4 : three HHs, velocities declining
    log = [{"conf_ts": ts[3], "type": "L", "idx": 0, "price": 100.0},
           {"conf_ts": ts[13], "type": "H", "idx": 10, "price": 110.0},
           {"conf_ts": ts[18], "type": "L", "idx": 15, "price": 104.0},
           {"conf_ts": ts[28], "type": "H", "idx": 25, "price": 112.0},
           {"conf_ts": ts[33], "type": "L", "idx": 30, "price": 108.0},
           {"conf_ts": ts[48], "type": "H", "idx": 45, "price": 114.0}]
    up, dn = deceleration_flags(log, ts)
    assert up[48] and up.sum() == 1 and not dn.any()
    # break the monotone decline -> no flag
    log[3]["price"] = 120.0          # second leg faster (1.6)
    up2, _ = deceleration_flags(log, ts)
    assert not up2.any()


def _h4(prices):
    n = len(prices)
    t = pd.date_range("2026-01-01", periods=n, freq="4h", tz="UTC")
    p = np.array(prices, float)
    return pd.DataFrame({"time": t, "open": p, "high": p + 1.0,
                         "low": p - 1.0, "close": p})


def test_zone_builder_and_tagging():
    # a peak at idx 20 followed by a deep fall qualifies; k=3
    prices = [100 + i for i in range(21)] + [120 - 3 * i for i in range(1, 30)] \
        + [34 + i for i in range(10)]
    df = _h4(prices)
    sw = fractal_swings(df["high"].to_numpy(), df["low"].to_numpy(), 3)
    assert any(s[1] == "H" and s[0] == 20 for s in sw)
    zs = build_zones(df, 3, 14, 1.5)
    highs = [z for z in zs if z["type"] == "H"]
    assert highs and abs(highs[0]["level"] - 121.0) < 1e-9
    z = highs[0]
    ts = df["time"].astype("int64").to_numpy()
    assert z["active_from"] > ts[20]             # no lookahead
    # tagging: at the level within band -> in; far away -> out;
    # before activation -> not counted
    iz, _ = in_zone(121.2, int(z["active_from"]) + 1, 4.0, zs)
    assert iz is True                             # band 0.25*4 = 1.0
    iz2, _ = in_zone(140.0, int(z["active_from"]) + 1, 4.0, zs)
    assert iz2 is False
    iz3, _ = in_zone(121.0, int(z["active_from"]) - 1, 4.0, [z])
    assert iz3 is False


def test_zone_twin_run():
    df = _h4([100 + (i % 17) * 3 for i in range(120)])
    a = json.dumps(build_zones(df, 3, 14, 1.5), sort_keys=True)
    b = json.dumps(build_zones(df, 3, 14, 1.5), sort_keys=True)
    assert a == b
