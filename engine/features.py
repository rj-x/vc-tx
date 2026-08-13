"""Streaming per-TF feature computation. Trailing-only by construction:
each bar's features are computed against baselines that contain ONLY prior
bars — the current bar is appended to the baselines afterwards. There is no
code path through which a later bar can influence an earlier bar's features.

Two baseline modes (config features.baseline_mode):
  simple       — one trailing window of the last W bars (synthetic tests).
  session_time — per time-of-day bin, values from the same bin over the
                 prior N sessions (Part 2 session-time normalization).
"""

from collections import deque

from .bars import Bar, Features


class _Baseline:
    """Trailing distribution of (spread, volume, vol_per_point) values."""

    def __init__(self, maxlen):
        self.spreads = deque(maxlen=maxlen)
        self.volumes = deque(maxlen=maxlen)
        self.vpps = deque(maxlen=maxlen)

    def add(self, bar: Bar):
        self.spreads.append(bar.spread)
        self.volumes.append(bar.volume)
        if bar.spread > 0:
            self.vpps.append(bar.volume / bar.spread)

    @property
    def n(self):
        return len(self.volumes)


def _pct_rank(values, x):
    """Percentile rank of x within values (0-100), midpoint convention."""
    if not values:
        return None
    below = sum(1 for v in values if v < x)
    equal = sum(1 for v in values if v == x)
    return 100.0 * (below + 0.5 * equal) / len(values)


def _ratio(values, x):
    if not values:
        return None
    m = sum(values) / len(values)
    return None if m <= 0 else x / m


class FeatureEngine:
    """One instance per timeframe."""

    def __init__(self, cfg):
        f = cfg.features
        self.mode = f.baseline_mode
        self.min_obs = f.min_baseline_obs
        self.climax_lookback = cfg.labels.climax_lookback
        if self.mode == "simple":
            self._bl = _Baseline(f.simple_baseline_window)
        else:
            self._bins = {}                 # tod_bin -> _Baseline
            self._bin_len = f.baseline_sessions
        self._recent_volumes = deque(maxlen=self.climax_lookback)
        self._prev_close = None

    def _baseline_for(self, bar: Bar) -> _Baseline:
        if self.mode == "simple":
            return self._bl
        if bar.tod_bin not in self._bins:
            self._bins[bar.tod_bin] = _Baseline(self._bin_len)
        return self._bins[bar.tod_bin]

    def update(self, bar: Bar) -> Features:
        """Compute bar's features vs PRIOR data, then absorb the bar."""
        bl = self._baseline_for(bar)
        s = bar.spread
        feats = Features(
            valid=bl.n >= self.min_obs,
            rel_volume=_ratio(bl.volumes, bar.volume),
            rel_spread_pct=_pct_rank(bl.spreads, s),
            close_pos=bar.close_pos,
            rel_vol_per_point=(_ratio(bl.vpps, bar.volume / s) if s > 0 else None),
            direction=bar.direction,
            upper_wick_frac=((bar.high - max(bar.open, bar.close)) / s if s > 0 else 0.0),
            lower_wick_frac=((min(bar.open, bar.close) - bar.low) / s if s > 0 else 0.0),
            gap=(bar.open - self._prev_close if self._prev_close is not None else 0.0),
            vol_is_trailing_max=(len(self._recent_volumes) > 0
                                 and bar.volume >= max(self._recent_volumes)),
            raw_spread=s,
            raw_volume=bar.volume,
        )
        # absorb AFTER computing — the bar never sees itself in its baseline
        bl.add(bar)
        self._recent_volumes.append(bar.volume)
        self._prev_close = bar.close
        return feats
