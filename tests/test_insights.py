"""Register 109 pins: the INSIGHTS ledger indexes only what its sources
say (a WATCH cell clears exactly the statistics its flags say; a
tail-carried cell never indexes), the DELTA is a set difference against
the previous ledger line with first-seen dates riding forward, ages are
whole weeks, and a same-date re-emission replaces its own line (twin
runs idempotent)."""
import json
import os

from backtest.insights import (age_weeks, clearing_cells, delta,
                               load_ledger, watch_entries, write_ledger)


def _pmw():
    cell = {"variant": "R-ARM15", "session": "dead", "slot": "none", "n": 35,
            "median": 21.74, "win_rate": 0.63, "weeks_pos": 2,
            "weeks_meas": 2, "net_pts": 612.5, "max_win_share": 0.22,
            "tail_carried": False, "sel_pct_win": 96.0,
            "sel_pct_median": 100.0, "beats_field_null_win": True,
            "beats_field_null_median": False}
    tail = dict(cell, variant="R-NOTRAIL", tail_carried=True,
                beats_field_null_median=True)
    return {"markets": {"ger40fut|backtest": {"cells": [cell, tail]}},
            "ladder_handoffs": [{"instrument": "uk100fut", "arm": "R-SCALP-H6",
                                 "statistic": "win_rate", "rung": 0.25,
                                 "n": 47, "value": 0.872, "sel_pct": 100.0,
                                 "beats_field_null": True,
                                 "null_kind": "members' best-over-rungs"}],
            "census_watch": [{"instrument": "ger40fut", "signal": "S0-H6",
                              "window": "forward", "n": 96,
                              "net_reach_pct": 32.3, "sel_pct": 100.0,
                              "beats_field_null": True, "measurable": True,
                              "n_to_measurable": 0}],
            "candidate_pool": [{"cell": "x", "legs": "ger40fut",
                                "mechanism": ""}]}


def test_clearing_cells_follow_source_flags():
    out = clearing_cells(_pmw(), {}, {}, {}, {}, {}, {}, {})
    keys = [c["key"] for c in out]
    assert "pmw:ger40fut|backtest|R-ARM15|dead|none:win_rate" in keys
    assert "pmw:ger40fut|backtest|R-ARM15|dead|none:median" not in keys
    assert not any("R-NOTRAIL" in k for k in keys)      # tail-carried
    assert "handoff:uk100fut|R-SCALP-H6|win_rate" in keys
    assert "census:ger40fut|forward|S0-H6" in keys
    # a field-level reading indexes only when the source says significant
    survey = {"results": [{"instrument": "uk100fut", "cells": {},
                           "null": {"consistency": {
                               "field_significant": False,
                               "percentile_vs_null": 89.0}}}]}
    assert not any(c["key"].startswith("survey-field")
                   for c in clearing_cells({}, survey, {}, {}, {}, {}, {}, {}))
    survey["results"][0]["null"]["consistency"]["field_significant"] = True
    assert any(c["key"] == "survey-field:uk100fut:consistency"
               for c in clearing_cells({}, survey, {}, {}, {}, {}, {}, {}))


def test_delta_and_ages():
    prev = {"date": "2026-08-23", "clearing": ["a", "b"], "watch": ["w1"],
            "first_seen": {"a": "2026-08-16", "b": "2026-08-23",
                           "w1": "2026-08-23"}}
    d = delta(prev, ["b", "c"], ["w1", "w2"], "2026-08-30")
    assert (d["crossed"], d["aged"], d["died"]) == (["c"], ["b"], ["a"])
    assert (d["watch_new"], d["watch_died"]) == (["w2"], [])
    assert d["first_seen"]["a"] == "2026-08-16"        # rides forward
    assert d["first_seen"]["c"] == "2026-08-30"
    assert age_weeks(d["first_seen"], "a", "2026-08-30") == 2
    assert age_weeks(d["first_seen"], "c", "2026-08-30") == 0
    d0 = delta(None, ["b"], [], "2026-08-30")
    assert d0["crossed"] == ["b"] and d0["previous_date"] is None


def test_ledger_same_date_replaces(tmp_path):
    p = str(tmp_path / "ledger.jsonl")
    art = {"date": "2026-08-30", "clearing": [{"key": "a"}],
           "watch": [{"key": "w"}], "delta": {"first_seen": {"a": "2026-08-30",
                                                             "w": "2026-08-30"}}}
    write_ledger(art, "abc", p)
    write_ledger(art, "abc", p)
    lines = load_ledger(p)
    assert len(lines) == 1 and lines[0]["clearing"] == ["a"]
    art2 = dict(art, date="2026-09-06", clearing=[])
    write_ledger(art2, "abc", p)
    assert [l["date"] for l in load_ledger(p)] == ["2026-08-30", "2026-09-06"]


def test_watch_entries_carry_pool_and_census():
    w, fw = watch_entries(_pmw(), {}, {}, {}, {})
    kinds = {e["kind"] for e in w}
    assert {"candidate pool", "HELD sentence", "ladder hand-off",
            "census clear"} <= kinds
    assert any("EMPTY" in e["status"] for e in w if e["kind"] == "candidate pool")
    assert fw == {}
