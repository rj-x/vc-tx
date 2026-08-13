"""Bar and feature types shared across the engine."""

from dataclasses import dataclass, field
from typing import Optional


@dataclass(frozen=True)
class Bar:
    ts: int                     # monotonic timestamp (engine-agnostic units)
    open: float
    high: float
    low: float
    close: float
    volume: float
    tf: str = ""                # timeframe tag, e.g. "15min"
    session_id: int = 0         # trading-session ordinal (per-instrument calendar)
    tod_bin: int = 0            # time-of-day bin within session (session_time mode)
    is_stub: bool = False       # partial bar at session end: context-only
    segment: str = "cash"       # overnight_asia | pre_open | cash | post_close

    @property
    def spread(self):
        return self.high - self.low

    @property
    def close_pos(self):
        s = self.spread
        return 0.5 if s <= 0 else (self.close - self.low) / s

    @property
    def direction(self):
        return 1 if self.close > self.open else (-1 if self.close < self.open else 0)


@dataclass
class Features:
    """Per-bar trailing-relative features (Part 2). valid=False during warmup."""
    valid: bool = False
    rel_volume: Optional[float] = None       # volume vs baseline mean (ratio)
    rel_spread_pct: Optional[float] = None   # spread percentile vs trailing dist (0-100)
    close_pos: float = 0.5
    rel_vol_per_point: Optional[float] = None  # None for zero-spread bars
    direction: int = 0
    upper_wick_frac: float = 0.0
    lower_wick_frac: float = 0.0
    gap: float = 0.0                          # open vs prior close
    vol_is_trailing_max: bool = False         # volume >= max of prior `climax_lookback` bars
    raw_spread: float = 0.0
    raw_volume: float = 0.0
    flags: dict = field(default_factory=dict)  # diagnostic flags (evidence both-fired, etc.)
