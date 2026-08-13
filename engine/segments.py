"""Session segments (Part B): boundaries defined on the FUTURES trading
day (provider day, ~21:30 London anchor), not just cash hours."""

import pandas as pd

SEGMENTS = ("overnight_asia", "pre_open", "cash", "post_close")


def segment_of(ts, cash_start=8.0, cash_end=16.5):
    """Segment for a bar OPEN timestamp (London wall time)."""
    lon = pd.Timestamp(ts).tz_convert("Europe/London")
    lt = lon.hour + lon.minute / 60.0
    if 7.0 <= lt < cash_start:
        return "pre_open"
    if cash_start <= lt < cash_end:
        return "cash"
    if cash_end <= lt < 21.5:
        return "post_close"
    return "overnight_asia"
