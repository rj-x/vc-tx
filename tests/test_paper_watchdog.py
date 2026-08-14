"""World A fixes: injected exception -> EXECUTOR_ERROR logged, never mute;
watchdog calendar excludes the daily feed pause + weekends."""
import json
import pandas as pd
from engine.paper import guarded, expect_prints


def test_guarded_logs_and_returns(tmp_path):
    led = str(tmp_path / "l.jsonl")
    ok, _ = guarded(lambda: 1 / 0, led)
    assert ok is False
    evs = [json.loads(l) for l in open(led)]
    assert evs[0]["event"] == "EXECUTOR_ERROR" and "ZeroDivision" in evs[0]["error"]
    ok, val = guarded(lambda: 42, led)
    assert ok and val == 42


def test_watchdog_calendar():
    assert expect_prints(pd.Timestamp("2026-08-14 16:10Z"))        # Friday cash
    assert not expect_prints(pd.Timestamp("2026-08-14 20:30Z"))    # 21:30 London pause
    assert not expect_prints(pd.Timestamp("2026-08-15 10:00Z"))    # Saturday
