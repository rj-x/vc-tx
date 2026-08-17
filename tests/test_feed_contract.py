"""Measured feed contract (probe 2026-08-17, capture archived): served
index 0 = FORMING bar (newest-stamped, 107/107 polls, same-minute accrual);
index >=1 immutable. Pin: drop-last-POST-SORT discards exactly the forming
bar. Fixture = archived raw page from the probe capture."""
import json, os
import pandas as pd

FIX = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                   "fixtures_probe_page.json")


def test_drop_last_post_sort_drops_the_forming_bar():
    rows = json.load(open(FIX))
    df = pd.DataFrame([r.split(",") for r in rows],
                      columns=["time", "o", "h", "l", "c", "v"])
    df["time"] = pd.to_datetime(df["time"], utc=True)
    served_index0 = df["time"].iloc[0]
    assert served_index0 == df["time"].max(), \
        "measured contract: served index 0 is the newest (forming) bar"
    df_sorted = df.sort_values("time").reset_index(drop=True)
    assert df_sorted["time"].iloc[-1] == served_index0, \
        "post-sort last row == served index 0 -> iloc[:-1] drops the forming bar"
