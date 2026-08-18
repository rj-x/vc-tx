"""Register 30: standing sealed-window schedule — first two weeks of each
quarter born sealed, anchored 2026-09-01 (months Sep/Dec/Mar/Jun, days 1-14
inclusive, UTC). Declared forward-only, by calendar never by content. The
Aug 4-14 legacy lockbox is separate and unchanged."""
import pandas as pd
import pytest

from engine.store_loader import is_sealed, refuse_if_sealed
from backtest.forward_migration import zone_fence


def test_schedule_truth_table():
    assert is_sealed("2026-09-01 00:00+00:00")       # first window opens
    assert is_sealed("2026-09-14 23:59+00:00")       # last sealed day
    assert not is_sealed("2026-09-15 00:00+00:00")   # window closed
    assert not is_sealed("2026-08-20 12:00+00:00")   # pre-schedule
    assert is_sealed("2026-12-05 12:00+00:00")       # Dec window
    assert is_sealed("2027-03-10 12:00+00:00")       # Mar window
    assert is_sealed("2027-06-01 12:00+00:00")       # Jun window
    assert not is_sealed("2026-06-05 12:00+00:00")   # before schedule start
    assert not is_sealed("2026-10-05 12:00+00:00")   # non-anchor month


def test_refusal_on_explicit_sealed_target():
    with pytest.raises(SystemExit, match="SEALED WINDOW"):
        refuse_if_sealed("2026-09-03 10:00+00:00")
    refuse_if_sealed("2026-09-20 10:00+00:00")       # open span passes


def test_forward_readout_fence_refuses_sealed_start():
    with pytest.raises(SystemExit, match="SEALED WINDOW"):
        zone_fence("2026-09-02 08:00+00:00")


def test_legacy_lockbox_untouched():
    # the Aug 4-14 lockbox is governed by lockbox.json, not this schedule
    assert not is_sealed("2026-08-10 12:00+00:00")
