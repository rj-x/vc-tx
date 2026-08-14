"""Capture-all/consume-filtered refactor: uk100fut's tagged-row behavior is
pinned bit-identical (GBP/USD x High)."""
import json
import pandas as pd
from helpers import scenario_cfg
import backtest.campaign as C


def test_uk100fut_tagging_unchanged_by_capture_all(tmp_path, monkeypatch):
    cal = tmp_path / "cal.csv"
    cal.write_text(
        "utc_time,currency,impact,name\n"
        "2026-08-13T06:00:00Z,GBP,High,UK GDP\n"
        "2026-08-13T06:00:00Z,EUR,High,DE ZEW\n"          # filtered: currency
        "2026-08-13T06:05:00Z,GBP,Medium,UK minor\n"      # filtered: impact
        "2026-08-13T12:30:00Z,USD,High,US CPI\n")
    monkeypatch.setattr(C, "MACRO_CSV", str(cal))
    cfg = scenario_cfg()
    rel = cfg.instruments["uk100fut"].macro_relevance
    events = [
        {"type": "SPAWNED", "ts": pd.Timestamp("2026-08-13T06:03Z"),
         "h": {"spec": "H2", "dir": -1, "id": 1}},
        {"type": "LABEL", "ts": pd.Timestamp("2026-08-13T12:31Z"),
         "tf": "15min", "label": "UPTHRUST"},
    ]
    out = C.macro_tags(events, "15min", rel)
    tagged = out["per_release_tag_counts"]
    # old behavior: only GBP/USD High rows tag; EUR-High and GBP-Medium
    # (both within +-15min of the spawn) must NOT appear
    assert set(tagged) == {"2026-08-13 06:00:00+00:00 UK GDP",
                           "2026-08-13 12:30:00+00:00 US CPI"}, tagged
    assert out["funnel"]["SPAWNED"] == {"near_GBP": 1}
    assert out["funnel"]["LABEL"] == {"near_USD": 1}
