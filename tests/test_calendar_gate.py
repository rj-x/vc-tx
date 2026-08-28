"""Register 104 part 3 pins: the calendar merge gate fails on a live
max date not in the future and warns on newer staging rows."""
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "scripts"))

from macro_fetch import calendar_gate


def _w(tmp_path, name, rows):
    p = tmp_path / name
    p.write_text("utc_time,currency,impact,name\n" + "\n".join(rows) + "\n")
    return str(p)


def test_gate_fails_when_live_max_in_past_and_warns_backlog(tmp_path):
    live = _w(tmp_path, "live.csv", ["2026-08-28T14:00:00Z,USD,High,a"])
    stg = _w(tmp_path, "stg.csv", ["2026-08-28T14:00:00Z,USD,High,a",
                                   "2026-09-02T12:30:00Z,USD,High,b",
                                   "2026-09-03T12:30:00Z,USD,High,c"])
    rc, msgs = calendar_gate(live, stg, now="2026-08-29T10:00:00Z")
    assert rc == 1 and any("CALENDAR STALE" in m for m in msgs)
    assert any("UNMERGED BACKLOG: 2" in m for m in msgs)


def test_gate_passes_with_future_entry(tmp_path):
    live = _w(tmp_path, "live.csv", ["2026-09-02T12:30:00Z,USD,High,b"])
    stg = _w(tmp_path, "stg.csv", ["2026-09-02T12:30:00Z,USD,High,b"])
    rc, msgs = calendar_gate(live, stg, now="2026-08-29T10:00:00Z")
    assert rc == 0 and not any("BACKLOG" in m for m in msgs)
