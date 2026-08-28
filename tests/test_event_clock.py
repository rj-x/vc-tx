"""Register 104 pins: news tagging by currency and window, coverage
exclusion vs the verified-empty exception, auction-slot tagging per
instrument, the hit definition per variant class, and twin-run of the
luck budget on a synthetic field."""
import json

import pandas as pd

from backtest.event_clock import (auction_tag, cells, hit_of, in_coverage,
                                  luck, news_tag, tag_row)


def _rel():
    return sorted([(pd.Timestamp("2026-08-05 12:30:00+00:00").value, "USD",
                    "High", "x"),
                   (pd.Timestamp("2026-08-05 06:00:00+00:00").value, "GBP",
                    "High", "y")])


def test_news_tag_currency_and_window():
    rel = _rel()
    t = pd.Timestamp("2026-08-05 12:40:00+00:00").value
    assert news_tag(t, "USD", rel, 15) and not news_tag(t, "USD", rel, 5)
    assert not news_tag(t, "GBP", rel, 30)


def test_coverage_and_verified_empty():
    span = ("2026-07-14", "2026-08-19")
    assert in_coverage("2026-08-01", span)
    assert not in_coverage("2026-08-25", span)          # uncovered gap
    assert in_coverage("2026-08-21", span)               # verified-empty
    r = {"instrument": "ger40fut", "open_ts": "2026-08-25 10:00:00+00:00"}
    tags, covered = tag_row(r, _rel(), span)
    assert not covered and tags["news15:native"] is None \
        and tags["news15:cross"] is None
    r2 = {"instrument": "ger40fut", "open_ts": "2026-08-05 12:35:00+00:00"}
    tags2, cov2 = tag_row(r2, _rel(), span)
    assert cov2 and tags2["news15:native"] is None       # no native ccy
    assert tags2["news15:cross"] is True                  # USD cross


def test_auction_tags():
    t = pd.Timestamp("2026-08-05 13:40:00+00:00")
    assert auction_tag(t, "nas100fut", "open", 15)
    assert not auction_tag(t, "uk100fut", "open", 30)
    assert auction_tag(pd.Timestamp("2026-08-05 21:10:00+00:00"),
                       "ger40fut", "close", 15)


def test_hit_definition_and_luck_twin_run():
    assert hit_of({"variant": "R-SCALP-H" + "6", "reason": "target",
                   "pts": -0.5})
    assert not hit_of({"variant": "R-NOTRAIL", "reason": "eod", "pts": -1.0})
    rows, tags = [], []
    for i in range(40):
        inw = i % 2 == 0
        rows.append({"instrument": "uk100fut", "variant": "R-NOTRAIL",
                     "window": "forward", "pts": 2.0 if inw else -2.0,
                     "reason": "eod"})
        tags.append({"open15": inw})
    res = cells(rows, tags)
    k = ("uk100fut", "R-NOTRAIL", "forward", "open15")
    assert res[k]["measurable"] and res[k]["hit_gap_pp"] == 100.0
    a = json.dumps(luck(rows, tags, res), sort_keys=True)
    b = json.dumps(luck(rows, tags, cells(rows, tags)), sort_keys=True)
    assert a == b
