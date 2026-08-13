"""Lockbox-exclusion and clock-gating tests (prompt Part 8 / Non-Negotiable).
All on synthetic CSVs — no real-data engine runs before authorization."""

import json
import os

import pandas as pd
import pytest

from helpers import scenario_cfg  # noqa: F401  (sys.path setup)

from engine.store_loader import ClockGatedFeed, load_frame, lockbox_boundary

FROZEN_BOUNDARY = "2026-08-04T00:00:00+00:00"


def _fake_store(tmp_path, slug="synth", tf="1min"):
    root = str(tmp_path)
    os.makedirs(os.path.join(root, "clean_finsa"), exist_ok=True)
    with open(os.path.join(root, "lockbox.json"), "w") as f:
        json.dump({"boundary_utc": FROZEN_BOUNDARY}, f)
    idx = pd.date_range("2026-07-28", periods=14 * 24 * 60, freq="1min", tz="UTC")
    df = pd.DataFrame({"open": 1.0, "high": 2.0, "low": 0.5, "close": 1.5,
                       "volume": 10}, index=idx)
    df.index.name = "time"
    df.to_csv(os.path.join(root, "clean_finsa", f"{slug}_{tf}.csv"))
    return root, df


def test_frozen_boundary_matches_lockbox_json():
    """Guards against accidental drift of the REAL lockbox boundary."""
    assert str(lockbox_boundary()) == "2026-08-04 00:00:00+00:00"


def test_loader_excludes_lockbox(tmp_path):
    root, full = _fake_store(tmp_path)
    df = load_frame("synth", "1min", root=root)
    boundary = pd.Timestamp(FROZEN_BOUNDARY)
    assert len(df) > 0
    assert df.index.max() < boundary
    assert (full.index >= boundary).any(), "fixture must span the boundary"


def test_lockbox_evaluation_is_explicit_and_logged(tmp_path):
    root, full = _fake_store(tmp_path)
    logged = []
    df = load_frame("synth", "1min", root=root, lockbox_evaluation=True,
                    log_fn=logged.append)
    assert len(df) == len(full)
    assert logged and "LOCKBOX ACCESS" in logged[0]


def test_clock_gated_feed_visibility_and_monotonicity(tmp_path):
    idx = pd.date_range("2026-07-01 08:00", periods=120, freq="1min", tz="UTC")
    df = pd.DataFrame({"open": range(120), "close": range(120)}, index=idx)
    feed = ClockGatedFeed({"1min": df})
    with pytest.raises(RuntimeError):
        feed.bars("1min")                     # no clock set yet
    # a 1min bar opening 08:00 CLOSES 08:01 — invisible before its close
    feed.advance_to("2026-07-01 08:00:30+00:00")
    assert len(feed.bars("1min")) == 0
    feed.advance_to("2026-07-01 08:30:00+00:00")
    vis = feed.bars("1min")
    assert len(vis) == 30
    assert vis.index.max() == pd.Timestamp("2026-07-01 08:29", tz="UTC")
    with pytest.raises(ValueError):
        feed.advance_to("2026-07-01 08:00:00+00:00")   # clock never rewinds
    # mutating the returned copy cannot poison the feed
    vis.iloc[0, 0] = 999
    assert feed.bars("1min").iloc[0, 0] != 999
