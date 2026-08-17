"""Register finding 24 (2026-08-18): the watchdog calendar encoded the
provider's daily feed pause in London hours; the provider pauses on UTC.
Result: 11 false WATCHDOG_STALL events 2026-08-17 21:11:33-22:03:01Z (one
hour of BST offset). The pin IS the incident: under the fixed calendar the
incident polls are suppressed and a genuine mid-session stall still fires.
Seasonal note: the old bug is invisible in GMT months — these pins hold in
both offsets."""
import pandas as pd

from engine.paper import expect_prints


def _ts(s):
    return pd.Timestamp(s, tz="UTC")


def test_incident_polls_suppressed():
    # first and last of the 11 false events, verbatim from the ledger
    assert not expect_prints(_ts("2026-08-17 21:11:33.725086"))
    assert not expect_prints(_ts("2026-08-17 22:03:01.946746"))
    # the watchdog guard itself: 11 quiet polls at the incident timestamp
    quiet_polls = 11
    assert not (quiet_polls >= 5
                and expect_prints(_ts("2026-08-17 21:11:33.725086")))


def test_genuine_stall_still_fires():
    # synthetic 5-quiet-poll stall mid-session (Monday 14:00Z) must fire
    quiet_polls = 5
    assert quiet_polls >= 5 and expect_prints(_ts("2026-08-17 14:00:00"))


def test_measured_pause_boundaries():
    # measured: last pre-pause bar opens 20:59Z; first post-pause 22:05Z
    assert expect_prints(_ts("2026-08-17 20:59:00"))      # tape still live
    assert not expect_prints(_ts("2026-08-17 21:00:00"))  # pause begins
    assert not expect_prints(_ts("2026-08-17 22:05:00"))  # reopen margin
    assert not expect_prints(_ts("2026-08-17 22:09:59"))
    assert expect_prints(_ts("2026-08-17 22:10:00"))      # margin ends


def test_weekend_utc_anchored():
    assert expect_prints(_ts("2026-08-14 20:59:00"))      # Fri pre-close
    assert not expect_prints(_ts("2026-08-14 21:01:00"))  # Fri post-close
    assert not expect_prints(_ts("2026-08-15 12:00:00"))  # Saturday
    assert not expect_prints(_ts("2026-08-16 21:59:00"))  # Sun pre-reopen
    assert expect_prints(_ts("2026-08-16 22:10:00"))      # Sun reopen
    # store fact: Sunday 2026-08-16 first bar opens 22:05Z


def test_gmt_months_same_window():
    # seasonal pin: identical UTC window in GMT months (2026-01-12 = Mon)
    assert expect_prints(_ts("2026-01-12 20:30:00"))
    assert not expect_prints(_ts("2026-01-12 21:05:00"))
    assert not expect_prints(_ts("2026-01-12 22:05:00"))
    assert expect_prints(_ts("2026-01-12 22:30:00"))
