"""Resampling correctness (stub bars, session boundaries, no overnight
spanning) + a full synthetic run of the backtest loop through
ClockGatedFeed."""

import json
import os

import numpy as np
import pandas as pd

from helpers import scenario_cfg

from engine.resample import cash_sessions, exec_bars, resample_bars
from backtest.loop import run_backtest


def _synthetic_clean_store(tmp_path, n_sessions=14, seed=5):
    """Clean-store-shaped 1min CSV: cash sessions 08:00-16:30 London (UTC+1
    dates in August => 07:00-15:30 UTC), plus overnight rows (in_cash=False).
    Prices get a daily two-phase drift so labels/hypotheses actually fire."""
    rng = np.random.default_rng(seed)
    rows = []
    px = 100.0
    day0 = pd.Timestamp("2026-07-06", tz="UTC")
    d = 0
    made = 0
    while made < n_sessions:
        day = day0 + pd.Timedelta(days=d)
        d += 1
        if day.dayofweek >= 5:
            continue
        made += 1
        drift = rng.choice([-0.02, 0.0, 0.02])
        for m in range(510):
            ts = day + pd.Timedelta(hours=7, minutes=m)
            burst = 5.0 if rng.random() < 0.01 else 1.0
            o = px
            c = px + drift + rng.normal(0, 0.12)
            w = abs(rng.normal(0.15, 0.1)) * (2 if burst > 1 else 1)
            rows.append({"time": ts, "open": o, "high": max(o, c) + w,
                         "low": min(o, c) - w, "close": c,
                         "volume": abs(rng.normal(100, 30)) * burst + 1,
                         "in_cash": True,
                         "ldate": str(day.date())})
            px = c
        # a few overnight rows (must be excluded from cash resampling)
        for m in range(30):
            ts = day + pd.Timedelta(hours=17, minutes=m)
            rows.append({"time": ts, "open": px, "high": px + 0.1,
                         "low": px - 0.1, "close": px, "volume": 5,
                         "in_cash": False, "ldate": str(day.date())})
    df = pd.DataFrame(rows).set_index("time")
    root = str(tmp_path)
    os.makedirs(os.path.join(root, "clean_finsa"), exist_ok=True)
    with open(os.path.join(root, "lockbox.json"), "w") as f:
        json.dump({"boundary_utc": "2027-01-01T00:00:00+00:00"}, f)
    df.to_csv(os.path.join(root, "clean_finsa", "synth_1min.csv"))
    return root, df


def test_resample_sessions_stubs_and_boundaries(tmp_path):
    root, df = _synthetic_clean_store(tmp_path, n_sessions=3)
    cash = cash_sessions(df)
    assert cash["session_id"].nunique() == 3
    b15 = resample_bars(cash, 15, "15min")
    b60 = resample_bars(cash, 60, "1h")
    per15 = len(b15) // 3
    assert per15 == 34 and not any(b.is_stub for b in b15), \
        "8.5h / 15min = 34 full bars, no stub"
    per60 = [b for b in b60 if b.session_id == 0]
    assert len(per60) == 9
    assert [b.is_stub for b in per60] == [False] * 8 + [True], \
        "1h leaves a 30-minute stub at session end"
    # bars never span the overnight gap: each session starts fresh
    for sid in range(3):
        first = [b for b in b60 if b.session_id == sid][0]
        assert first.tod_bin == 0
    ex = exec_bars(cash)
    assert len(ex) == 3 * 510
    assert max(b.tod_bin for b in ex) == 509


def test_backtest_loop_runs_on_synthetic_store(tmp_path):
    root, _ = _synthetic_clean_store(tmp_path, n_sessions=14)
    cfg = scenario_cfg({
        "features.baseline_mode": "session_time",
        "features.baseline_sessions": 6,
        "features.min_baseline_obs": 4,
        "instruments.synth": {
            "session_start_london": 8.0, "session_end_london": 16.5,
            "tick_size": 0.1, "point_value": 1.0, "auction_exclusion_min": 10},
    })
    engine, info = run_backtest(cfg, "synth", root=root)
    assert info["sessions"] == 14
    ev_types = {e["type"] for e in engine.narrative.events}
    assert "LABEL" in ev_types and "PHASE" in ev_types
    # stub bars must never carry labels: the 1h stub closes 16:30 London
    for e in engine.narrative.events:
        if e["type"] == "LABEL" and e.get("tf") == "1h":
            lon = pd.Timestamp(e["ts"]).tz_convert("Europe/London")
            assert not (lon.hour == 16 and lon.minute == 30), \
                "stub bar emitted a LABEL event"
    # loop respected the clock: no exception from ClockGatedFeed monotonicity
    assert engine.broker.equity is not None
