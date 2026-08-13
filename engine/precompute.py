"""Vectorized per-bar feature precompute (prompt Part 6 performance note).

MUST be bar-for-bar equivalent to the streaming FeatureEngine — the
truncation-equivalence test (tests/test_precompute.py) enforces this. The
known leak vectors this implementation explicitly avoids:

- every rolling statistic is computed over a window of STRICTLY PRIOR bars
  (shift-by-one before windowing) — never centered, never including self;
- session-time bins draw from the same time-of-day bin over PRIOR sessions
  only (per-bin shift-by-one), mirroring the streaming per-bin deques;
- percentile ranks are ranked against the trailing window only, never the
  full sample.
"""

import numpy as np
import pandas as pd


def _trailing_mean(values, maxlen):
    """Mean over the last <= maxlen PRIOR values (deque semantics)."""
    s = pd.Series(values, dtype="float64")
    return s.shift(1).rolling(maxlen, min_periods=1).mean().to_numpy()


def _trailing_count(n, maxlen):
    """How many PRIOR values the deque holds at each position."""
    idx = np.arange(n)
    return np.minimum(idx, maxlen)


def _trailing_pct_rank(values, maxlen):
    """Midpoint percentile rank of values[i] vs the last <= maxlen PRIOR
    values. NaN where no prior values exist."""
    v = np.asarray(values, dtype="float64")
    n = len(v)
    out = np.full(n, np.nan)
    # small-i region (partial windows) — cheap loop
    head = min(n, maxlen)
    for i in range(1, head):
        win = v[:i]
        out[i] = 100.0 * ((win < v[i]).sum() + 0.5 * (win == v[i]).sum()) / i
    if n > maxlen:
        win = np.lib.stride_tricks.sliding_window_view(v[:-1], maxlen)
        x = v[maxlen:, None]
        out[maxlen:] = 100.0 * ((win < x).sum(axis=1)
                                + 0.5 * (win == x).sum(axis=1)) / maxlen
    return out


def _per_group(values, groups, fn, maxlen):
    """Apply a trailing statistic within each group (session-time bins),
    scattering results back to original positions."""
    v = np.asarray(values, dtype="float64")
    out = np.full(len(v), np.nan)
    for g in np.unique(groups):
        pos = np.nonzero(groups == g)[0]
        out[pos] = fn(v[pos], maxlen)
    return out


def precompute_features(df, cfg):
    """df: open/high/low/close/volume (+ tod_bin ints for session_time mode),
    chronologically sorted. Returns a DataFrame aligned to df with the same
    fields the streaming FeatureEngine emits."""
    f = cfg.features
    mode = f.baseline_mode
    maxlen = (f.simple_baseline_window if mode == "simple"
              else f.baseline_sessions)
    o = df["open"].to_numpy(dtype="float64")
    h = df["high"].to_numpy(dtype="float64")
    l = df["low"].to_numpy(dtype="float64")
    c = df["close"].to_numpy(dtype="float64")
    v = df["volume"].to_numpy(dtype="float64")
    n = len(df)
    spread = h - l
    pos_spread = spread > 0

    if mode == "simple":
        groups = np.zeros(n, dtype="int64")
    else:
        groups = df["tod_bin"].to_numpy(dtype="int64")

    # per-bin trailing counts -> validity (matches _Baseline.n >= min_obs,
    # where n counts volume observations)
    valid = np.zeros(n, dtype=bool)
    vol_mean = np.full(n, np.nan)
    spread_pct = np.full(n, np.nan)
    for g in np.unique(groups):
        pos = np.nonzero(groups == g)[0]
        m = len(pos)
        valid[pos] = _trailing_count(m, maxlen) >= f.min_baseline_obs
        vol_mean[pos] = _trailing_mean(v[pos], maxlen)
        spread_pct[pos] = _trailing_pct_rank(spread[pos], maxlen)

    with np.errstate(invalid="ignore", divide="ignore"):
        rel_volume = np.where(vol_mean > 0, v / vol_mean, np.nan)

    # vol-per-point: baseline holds only PRIOR bars WITH spread > 0, per bin
    rel_vpp = np.full(n, np.nan)
    for g in np.unique(groups):
        pos = np.nonzero((groups == g) & pos_spread)[0]
        if len(pos) == 0:
            continue
        vpp = v[pos] / spread[pos]
        mean = _trailing_mean(vpp, maxlen)
        with np.errstate(invalid="ignore", divide="ignore"):
            rel_vpp[pos] = np.where(mean > 0, vpp / mean, np.nan)

    # global (bin-independent) fields — identical to streaming
    prev_close = np.concatenate(([np.nan], c[:-1]))
    gap = np.where(np.isnan(prev_close), 0.0, o - prev_close)
    prior_max = (pd.Series(v).shift(1)
                 .rolling(cfg.labels.climax_lookback, min_periods=1)
                 .max().to_numpy())
    vol_is_max = np.zeros(n, dtype=bool)
    vol_is_max[1:] = v[1:] >= prior_max[1:]

    with np.errstate(invalid="ignore", divide="ignore"):
        close_pos = np.where(pos_spread, (c - l) / spread, 0.5)
        upper = np.where(pos_spread, (h - np.maximum(o, c)) / spread, 0.0)
        lower = np.where(pos_spread, (np.minimum(o, c) - l) / spread, 0.0)
    direction = np.sign(c - o).astype("int64")

    return pd.DataFrame({
        "valid": valid,
        "rel_volume": rel_volume,
        "rel_spread_pct": spread_pct,
        "close_pos": close_pos,
        "rel_vol_per_point": rel_vpp,
        "direction": direction,
        "upper_wick_frac": upper,
        "lower_wick_frac": lower,
        "gap": gap,
        "vol_is_trailing_max": vol_is_max,
        "raw_spread": spread,
        "raw_volume": v,
    }, index=df.index)
