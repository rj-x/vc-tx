"""Register 111 pins: the departure-base builder (>= swing_k-bar base
inside 1xATR, impulsive departure within swing_k bars, active from the
NEXT bar's open, dead on a close through the far edge), scalar/vector
tagging agreement on ranges, the scarcity verdicts including FAILED at
hundreds, and twin-run determinism."""
import json

import numpy as np
import pandas as pd

from backtest.zone_census_v3 import (BASE_RANGE_ATR, EXPECTED_ACTIVE_D1,
                                     SCARCITY_FAIL_AT, active_over_span,
                                     departure_bases, in_zone_v3,
                                     scarcity, tag_bars_v3)


def _frame(prices, spread=1.0):
    p = np.array(prices, float)
    t = pd.date_range("2026-01-01", periods=len(p), freq="D", tz="UTC")
    return pd.DataFrame({"time": t, "open": p, "high": p + spread,
                         "low": p - spread, "close": p,
                         "ldate": [str(x.date()) for x in t]})


def _world():
    # 20 warmup bars (ATR ~2), a 4-bar base at 100, an impulsive
    # departure up, then a drift back down THROUGH the base (full
    # trade-through) at the end
    warm = [100 + (i % 2) * 2 for i in range(20)]
    base = [100.0, 100.2, 99.9, 100.1]
    depart = [108.0, 109.0]
    revisit = [104.0, 100.0, 98.0, 90.0]
    return _frame(warm + base + depart + revisit)


def test_departure_base_builder_and_invalidation():
    df = _world()
    zs = departure_bases(df, 3, 14, 1.5)
    assert len(zs) == 1
    z = zs[0]
    assert z["type"] == "D" and z["base_bars"] >= 3
    assert abs(z["lo"] - 98.9) < 1e-9 and abs(z["hi"] - 101.2) < 1e-9
    ts = df["time"].astype("int64").to_numpy()
    assert z["active_from"] == ts[z["depart_idx"] + 1]   # next bar's open
    # dead at the first CLOSE below the base low (98.0 at index 28)
    assert z["invalidated_at"] == int(ts[28])
    # the x3 rung needs a 3xATR departure — this world has ~8 pts on
    # ATR ~2, so it still qualifies; shrink the departure to kill it
    df2 = _world()
    df2.loc[24:25, ["open", "high", "low", "close"]] -= 5.0
    assert departure_bases(df2, 3, 14, 3.0) == []


def test_tagging_scalar_vector_agree_and_next_bar_activation():
    df = _world()
    zs = departure_bases(df, 3, 14, 1.5)
    z = zs[0]
    ts = np.array([z["active_from"] - 1, z["active_from"],
                   z["invalidated_at"] - 1, z["invalidated_at"]])
    cl = np.array([100.0, 100.0, 100.0, 100.0])
    zid = tag_bars_v3(ts, cl, zs)
    assert zid.tolist() == [-1, 0, 0, -1]     # not before active, not after dead
    for t, c, expect in zip(ts, cl, [False, True, True, False]):
        got, _ = in_zone_v3(c, int(t), zs)
        assert got is expect
    # out-of-range price never tags
    assert tag_bars_v3(ts[1:2], np.array([150.0]), zs).tolist() == [-1]
    a = json.dumps(departure_bases(df, 3, 14, 1.5), sort_keys=True)
    b = json.dumps(departure_bases(df, 3, 14, 1.5), sort_keys=True)
    assert a == b                              # twin-run


def test_scarcity_verdicts_and_span_counts():
    lo, hi = EXPECTED_ACTIVE_D1
    assert "WITHIN" in scarcity("1d", lo) and "WITHIN" in scarcity("1d", hi)
    assert "BELOW" in scarcity("1d", lo - 1)
    assert "ABOVE" in scarcity("1d", hi + 1)
    assert "FAILED" in scarcity("1d", SCARCITY_FAIL_AT)
    assert "FAILED" in scarcity("4h", SCARCITY_FAIL_AT)   # H4 can still fail
    assert "no stated band" in scarcity("4h", 50)
    zs = [{"active_from": 10, "invalidated_at": 20},
          {"active_from": 15, "invalidated_at": None},
          {"active_from": 30, "invalidated_at": 40}]
    alive, peak = active_over_span(zs, 12, 35)
    assert (alive, peak) == (3, 2)
    alive2, peak2 = active_over_span(zs, 21, 25)   # seeded: only the open one
    assert (alive2, peak2) == (1, 1)
    assert BASE_RANGE_ATR == 1.0
