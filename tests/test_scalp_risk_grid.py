"""Register 103 pins: the stop re-rung leaves the target untouched; the
stop-ladder decomposition on shared fires; the cooldown replay in
strict order; the mechanism cut; the reacher-MAE curve; twin-run."""
import json

import pandas as pd

from backtest.scalp_risk_grid import (STOP_RUNGS, cooldown_replay,
                                      mechanism_cut, reacher_mae,
                                      stop_ladder_cell, with_stop)


def test_with_stop_rerungs_only_the_atr_stop():
    recipe = {"stages": [{"stop": [("atr", 2.5, "15min")],
                          "target": ("atr_haircut", 0.5, "15min", 0.5)}]}
    r = with_stop(recipe, 1.5)
    assert r["stages"][0]["stop"] == [("atr", 1.5, "15min")]
    assert r["stages"][0]["target"] == ("atr_haircut", 0.5, "15min", 0.5)
    assert recipe["stages"][0]["stop"][0][1] == 2.5     # original intact


def test_stop_ladder_decomposition():
    v0 = {1: (4.0, "target"), 2: (-9.0, "stop"), 3: (-1.0, "eod"),
          4: (4.0, "target")}
    alt = {1: (-4.0, "stop"), 2: (-4.0, "stop"), 3: (-4.0, "stop"),
           4: (4.0, "target")}
    c = stop_ladder_cell(v0, alt)
    assert c["n"] == 4 and c["n_reachers_v0"] == 2
    assert c["reachers_amputated"] == 1 and c["reachers_amputated_delta"] == -8.0
    assert c["reachers_amputated_share"] == 0.5
    assert c["stops_taken"] == 3 and c["stops_taken_pts"] == -12.0
    assert c["eod_changed"] == 1 and c["eod_delta"] == -3.0
    assert c["net_delta"] == -8.0 + 5.0 - 3.0


def _rows():
    t0 = pd.Timestamp("2026-08-20 08:00:00+00:00")
    seq = [(-9.0, "stop", 5), (3.0, "target", 3), (-9.0, "stop", 4),
           (3.0, "target", 2), (-2.0, "eod", 60)]
    out = []
    for i, (p, r, dur) in enumerate(seq):
        o = t0 + pd.Timedelta(minutes=20 * i)
        out.append({"open_ts": o, "close_ts": o + pd.Timedelta(minutes=dur),
                    "pts": p, "reason": r, "window": "forward",
                    "mae_atr": 0.4 if r == "target" else 1.2})
    return out


def test_cooldown_replay_and_mechanism():
    rows = _rows()
    # stop 0 closes 08:05; T=30 blocks opens before 08:35 -> rows 1
    # (08:20) foregone; row 2 (08:40) taken (a stop, closes 08:44,
    # blocks until 09:14) -> rows 3 (09:00) foregone; row 4 (09:20) ok
    c = cooldown_replay(rows, 30)
    assert c["foregone"] == 2 and c["targets_forfeited"] == 2
    assert c["targets_forfeited_pts"] == 6.0 and c["net_delta"] == -6.0
    c15 = cooldown_replay(rows, 15)          # 08:05+15 = 08:20: not < ->
    assert c15["foregone"] == 0              # row 1 taken (open == bound)
    m = mechanism_cut(rows, 30)
    assert m["n_post_stop"] == 2 and m["post_stop_reach"] == 1.0
    a = json.dumps(cooldown_replay(rows, 60), sort_keys=True)
    b = json.dumps(cooldown_replay(rows, 60), sort_keys=True)
    assert a == b


def test_reacher_mae_curve():
    rows = [{"reason": "target", "mae_atr": 0.1 * i} for i in range(1, 21)]
    m = reacher_mae(rows)
    assert m["n"] == 20 and abs(m["p50"] - 1.05) < 1e-6
    assert set(m["share_breaching"]) == {f"{r:g}" for r in STOP_RUNGS}
    assert reacher_mae(rows[:5])["note"] == "unmeasurable"
