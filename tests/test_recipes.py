"""Register 41 honest-fill rules — each rule pinned as the incident class
it prevents — plus twin-run bit-identity (the determinism doctrine)."""
import json

import numpy as np
import pandas as pd

from backtest.recipes import simulate


def _arrs(bars):
    """bars: list of (o,h,l,c) at 1-min spacing from a fixed origin."""
    t0 = pd.Timestamp("2026-08-17 09:00", tz="UTC").value
    ts = np.array([t0 + i * 60_000_000_000 for i in range(len(bars))])
    o, h, l, c = (np.array([b[i] for b in bars], float) for i in range(4))
    return ts, o, h, l, c


def _fire(i=0, d=1):
    return [{"ts": pd.Timestamp("2026-08-17 09:00", tz="UTC")
             + pd.Timedelta(minutes=i), "dir": d, "name": "X"}]


ATR = lambda t: 10.0
NO_EOD = lambda n: np.zeros(n, bool)


def test_rule1_both_reachable_stop_fills():
    # entry 100; stop 95, target 110; one wide bar spans both -> STOP
    bars = [(100, 100, 100, 100), (100, 100, 100, 100),
            (100, 120, 90, 105)]
    arrs = _arrs(bars)
    tr = simulate(_fire(0, 1), arrs, ATR,
                  {"stop": ("fixed_pts", 5.0), "target": ("fixed_pts", 10.0)},
                  0.0, NO_EOD(3))
    assert tr[0]["reason"] == "stop" and tr[0]["exit"] == 95.0


def test_rule2_gap_fills_at_worse_price():
    # entry 100, stop 95; next bar OPENS at 88 (gap through) -> filled at 88
    bars = [(100, 100, 100, 100), (100, 101, 99, 100),
            (88, 89, 87, 88)]
    arrs = _arrs(bars)
    tr = simulate(_fire(0, 1), arrs, ATR,
                  {"stop": ("fixed_pts", 5.0), "target": None},
                  0.0, NO_EOD(3))
    assert tr[0]["reason"] == "stop_gap" and tr[0]["exit"] == 88.0


def test_rule3_trailing_ratchets_only_on_settled_bars():
    # long; trail = low of 2nd previous bar. Lows rise then fall — the
    # stop must never move DOWN after the fall.
    bars = [(100, 101, 95, 100), (100, 101, 96, 100), (100, 101, 97, 100),
            (100, 101, 98, 100), (100, 101, 90, 100), (100, 101, 98.4, 99)]
    arrs = _arrs(bars)
    tr = simulate(_fire(0, 1), arrs, ATR,
                  {"stop": ("trail_nth", 2, ("pts", 0.0)), "target": None},
                  0.0, NO_EOD(6))
    # ratcheted stop reaches 97 (low of bar 2, seen from bar 4) then the
    # bar-4 low of 90 must NOT lower it; bar 4's own low 90 <= 97 stops out
    assert tr[0]["reason"] == "stop" and tr[0]["exit"] == 97.0


def test_rule4_eod_flat_at_native_close():
    bars = [(100, 100, 100, 100), (100, 101, 99, 100), (100, 102, 99, 101)]
    arrs = _arrs(bars)
    eod = np.array([False, False, True])
    tr = simulate(_fire(0, 1), arrs, ATR,
                  {"stop": ("fixed_pts", 50.0), "target": None}, 0.0, eod)
    assert tr[0]["reason"] == "eod" and tr[0]["exit"] == 101.0


def test_one_position_per_hypothesis_and_spread():
    bars = [(100, 100, 100, 100)] + [(100, 101, 99, 100)] * 8
    arrs = _arrs(bars)
    fires = _fire(0, 1) + _fire(1, 1) + _fire(2, 1)   # overlapping fires
    eod = np.zeros(9, bool)
    eod[-1] = True
    tr = simulate(fires, arrs, ATR,
                  {"stop": ("fixed_pts", 50.0), "target": None}, 0.8, eod)
    assert len(tr) == 1                    # one position per hypothesis
    assert tr[0]["pts"] == round((100.0 - 100.0) - 0.8, 2)   # spread charged


def test_twin_run_bit_identity():
    bars = [(100 + (i % 5) * 0.3, 100.6 + (i % 5) * 0.3,
             99.4 + (i % 3) * 0.2, 100.1 + (i % 4) * 0.25)
            for i in range(200)]
    arrs = _arrs(bars)
    fires = [f for i in range(0, 180, 7) for f in _fire(i, 1 if i % 2 else -1)]
    eod = np.zeros(200, bool)
    eod[100] = eod[199] = True
    r = {"stop": ("trail_nth", 6, ("atr", 0.5)), "target": ("atr", 3.0)}
    a = simulate(fires, arrs, ATR, r, 0.8, eod)
    b = simulate(fires, arrs, ATR, r, 0.8, eod)
    assert json.dumps(a, sort_keys=True) == json.dumps(b, sort_keys=True)
