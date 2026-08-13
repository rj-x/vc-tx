"""Truncation-equivalence test (Non-Negotiable #3): the vectorized feature
precompute must equal the streaming FeatureEngine recomputed on data
truncated at each sampled bar — in BOTH baseline modes, explicitly covering
session-time bins. Float comparisons use rtol 1e-9 (summation-order ulps);
flags/ints are exact."""

import numpy as np
import pandas as pd

from helpers import scenario_cfg

from engine.bars import Bar
from engine.features import FeatureEngine
from engine.precompute import precompute_features

N_BARS = 600
SAMPLES = 40


def _random_bars(seed, n=N_BARS, bins=26):
    rng = np.random.default_rng(seed)
    px = 100 + np.cumsum(rng.normal(0, 0.8, n))
    spread = np.abs(rng.normal(1.5, 0.7, n))
    spread[rng.random(n) < 0.02] = 0.0            # zero-spread edge cases
    o = px + rng.normal(0, 0.3, n)
    c = px + rng.normal(0, 0.3, n)
    h = np.maximum(o, c) + spread * rng.random(n)
    l = h - np.where(spread > 0, spread, 0.0)
    h = np.where(spread == 0, np.maximum(o, c), h)
    l = np.where(spread == 0, h, l)
    o = np.clip(o, l, h)
    c = np.clip(c, l, h)
    v = np.abs(rng.normal(100, 40, n)) + 1
    df = pd.DataFrame({"open": o, "high": h, "low": l, "close": c, "volume": v})
    df["tod_bin"] = np.arange(n) % bins           # synthetic session grid
    df["session_id"] = np.arange(n) // bins
    return df


def _stream_at(df, cfg, i):
    """Streaming features for bar i using ONLY data truncated at bar i."""
    fe = FeatureEngine(cfg)
    feats = None
    for j in range(i + 1):
        r = df.iloc[j]
        b = Bar(j, r.open, r.high, r.low, r.close, r.volume,
                tod_bin=int(r.tod_bin), session_id=int(r.session_id))
        feats = fe.update(b)
    return feats


def _compare(feats, row, where):
    def close(a, b):
        if a is None and (b is None or (isinstance(b, float) and np.isnan(b))):
            return True
        if a is None or b is None:
            return False
        return np.isclose(a, b, rtol=1e-9, atol=1e-12)

    assert feats.valid == bool(row["valid"]), where
    assert close(feats.rel_volume, row["rel_volume"]), (where, "rel_volume")
    assert close(feats.rel_spread_pct, row["rel_spread_pct"]), (where, "rel_spread_pct")
    assert close(feats.close_pos, row["close_pos"]), (where, "close_pos")
    assert close(feats.rel_vol_per_point, row["rel_vol_per_point"]), (where, "vpp")
    assert feats.direction == int(row["direction"]), where
    assert close(feats.upper_wick_frac, row["upper_wick_frac"]), (where, "uw")
    assert close(feats.lower_wick_frac, row["lower_wick_frac"]), (where, "lw")
    assert close(feats.gap, row["gap"]), (where, "gap")
    assert feats.vol_is_trailing_max == bool(row["vol_is_trailing_max"]), where


def _run_mode(mode, seed):
    cfg = scenario_cfg({"features.baseline_mode": mode,
                        "features.min_baseline_obs": 5,
                        "features.baseline_sessions": 8,
                        "features.simple_baseline_window": 30})
    df = _random_bars(seed)
    pre = precompute_features(df, cfg)
    rng = np.random.default_rng(seed + 1)
    idxs = sorted(set(rng.integers(1, N_BARS, SAMPLES)) | {0, 1, N_BARS - 1})
    for i in idxs:
        feats = _stream_at(df, cfg, i)
        _compare(feats, pre.iloc[i], where=f"{mode} bar {i}")


def test_truncation_equivalence_simple_mode():
    _run_mode("simple", seed=7)


def test_truncation_equivalence_session_time_bins():
    _run_mode("session_time", seed=11)
