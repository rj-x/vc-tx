"""Register finding 26 (2026-08-18): daily commute = daily machine sleep =
daily silent hole in both live loops. Pin = the incident, store-measured
(provenance rule 25b): span 2026-08-18 07:03Z -> 07:40Z (last persisted bar
opens 07:02, first post-wake bar 07:40; one EXECUTOR_ERROR from network
teardown at 07:17:11Z inside the envelope). A frozen span must produce
EXACTLY ONE SUSPENSION_GAP event with correct bounds — not an error stream
— and normal poll cadence must produce none."""
import json

import pandas as pd

from engine.paper import suspension_check, SUSPENSION_THRESHOLD


def _t(s):
    return pd.Timestamp(s, tz="UTC")


def test_incident_span_one_event_correct_bounds(tmp_path):
    led = str(tmp_path / "ledger.jsonl")
    # poll cadence ~60s up to the last pre-sleep poll, then the frozen span,
    # then normal cadence resumes on wake
    polls = [_t("2026-08-18 07:01:05"), _t("2026-08-18 07:02:06"),
             _t("2026-08-18 07:03:07"),                  # last pre-sleep
             _t("2026-08-18 07:40:30"),                  # first post-wake
             _t("2026-08-18 07:41:31"), _t("2026-08-18 07:42:32")]
    events = []
    last = None
    for now in polls:
        ev = suspension_check(last, now, led)
        if ev:
            events.append(ev)
        last = now
    assert len(events) == 1                              # one event, no stream
    ev = events[0]
    assert ev["event"] == "SUSPENSION_GAP"
    assert ev["from"] == str(_t("2026-08-18 07:03:07"))
    assert ev["to"] == str(_t("2026-08-18 07:40:30"))
    assert pd.Timedelta(ev["span"]) == _t("2026-08-18 07:40:30") - _t(
        "2026-08-18 07:03:07")
    # and it reached the ledger exactly once
    rows = [json.loads(l) for l in open(led)]
    assert len(rows) == 1 and rows[0]["event"] == "SUSPENSION_GAP"


def test_normal_cadence_silent(tmp_path):
    led = str(tmp_path / "ledger.jsonl")
    assert suspension_check(None, _t("2026-08-18 07:00:00"), led) is None
    assert suspension_check(_t("2026-08-18 07:00:00"),
                            _t("2026-08-18 07:01:02"), led) is None
    # threshold boundary: exactly at threshold does not fire
    assert suspension_check(_t("2026-08-18 07:00:00"),
                            _t("2026-08-18 07:00:00") + SUSPENSION_THRESHOLD,
                            led) is None
    import os
    assert not os.path.exists(led)
