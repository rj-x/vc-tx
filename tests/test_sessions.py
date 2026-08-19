"""Register 37 session partition: boundary truth table in BOTH DST regimes
(the partition is defined in native exchange timezones)."""
import pandas as pd

from backtest.sessions import session_of, SESSIONS


def _s(ts):
    return session_of(pd.Timestamp(ts, tz="UTC"))


def test_bst_era_boundaries():
    # summer (BST/EDT): london 07:00Z-13:30Z, overlap ->15:30Z,
    # ny_only ->20:00Z, dead ->00:00Z (Tokyo 09:00), asia ->07:00Z
    assert _s("2026-08-17 07:00") == "london"
    assert _s("2026-08-17 13:29") == "london"
    assert _s("2026-08-17 13:30") == "overlap"      # 09:30 New York
    assert _s("2026-08-17 15:29") == "overlap"
    assert _s("2026-08-17 15:30") == "ny_only"      # 16:30 London
    assert _s("2026-08-17 19:59") == "ny_only"
    assert _s("2026-08-17 20:00") == "dead"         # 16:00 New York
    assert _s("2026-08-17 23:59") == "dead"
    assert _s("2026-08-18 00:00") == "asia"         # 09:00 Tokyo
    assert _s("2026-08-18 06:59") == "asia"


def test_gmt_era_boundaries():
    # winter (GMT/EST): london 08:00Z-14:30Z, overlap ->16:30Z,
    # ny_only ->21:00Z, dead ->00:00Z, asia ->08:00Z
    assert _s("2026-01-12 07:59") == "asia"
    assert _s("2026-01-12 08:00") == "london"
    assert _s("2026-01-12 14:29") == "london"
    assert _s("2026-01-12 14:30") == "overlap"
    assert _s("2026-01-12 16:30") == "ny_only"
    assert _s("2026-01-12 21:00") == "dead"
    assert _s("2026-01-13 00:00") == "asia"


def test_partition_is_total():
    for h in range(24):
        assert _s(f"2026-08-17 {h:02d}:07") in SESSIONS
        assert _s(f"2026-01-12 {h:02d}:07") in SESSIONS
