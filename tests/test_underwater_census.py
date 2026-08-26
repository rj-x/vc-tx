"""Register 87 pins: trajectory/path-class mechanics, the cut and BE
counterfactual fills, the probe simulator, thesis-campaign extraction,
the backoff walk, and twin-run determinism on synthetic arrays."""
import json

import numpy as np

from backtest.underwater_census import (be_outcome, campaigns_of,
                                        cut_counterfactuals,
                                        path_class, probe_sim,
                                        run_campaign, survival_curve,
                                        trajectory, underwater_at)


def _mk(closes, entry=100.0, d=1, hi_off=0.5, lo_off=0.5):
    c = np.array(closes, float)
    h = c + hi_off
    l = c - lo_off
    loud = np.zeros(len(c), bool)
    return h, l, c, loud


def _trade(closes, pts, atr0=4.0, entry=100.0, d=1, loud=None):
    h, l, c, ld = _mk(closes, entry, d)
    if loud is not None:
        ld = np.array(loud, bool)
    traj = trajectory(0, len(c) - 1, d, entry, atr0, h, l, c, ld)
    fav = (h - entry) if d == 1 else (entry - l)
    return {"traj": traj, "pts": pts, "atr0": atr0, "mfe_path": fav,
            "ei": 0}


def test_trajectory_and_path_class():
    t = _trade([99, 98.5, 101, 102], 2.0)          # underwater then up
    assert t["traj"]["first_pos"] == 3
    assert path_class(2.0, 1.0, 3) == "winner-after-underwater"
    assert path_class(2.0, 1.0, 1) == "winner-clean"
    assert path_class(-3.0, 1.0, None) == "loser-never-positive"
    assert path_class(-3.0, 1.0, 2) == "loser-after-positive"
    assert path_class(0.5, 1.0, 1) == "scratch"
    assert underwater_at(t["traj"], 2) and not underwater_at(
        t["traj"], 3)


def test_cut_counterfactuals_fills():
    # underwater at 2 (closes 99, 98.5) -> cut@2 exits at 98.5 close:
    # pts = (98.5-100) - spread(1) = -2.5; MAE cut 0.5xATR(=2pts)
    # touch-fill at 98: pts = -2 - 1 = -3
    t = _trade([99, 98.5, 101, 102], 2.0)
    cf = cut_counterfactuals(t, 1.0, 4.0)
    assert cf["cut@2"] == -2.5
    assert cf["cut@3"] is None                      # positive at bar 3
    assert cf["cut-mae0.5"] == -3.0
    assert cf["cut-loud"] is None                   # no loud bars
    t2 = _trade([99, 98.5, 101], 1.0, loud=[False, True, False])
    assert cut_counterfactuals(t2, 1.0, 4.0)["cut-loud"] == -2.5


def test_be_outcome_arming_and_touch():
    # rung 0.25x4 = 1pt; bar0 high 100.5 (fav .5), bar1 high 101.5
    # arms; bar2 low 99.5 touches entry -> scratch at -spread
    t = _trade([100.0, 101.0, 100.0, 103.0], 3.0)
    cf, trig, mfe = be_outcome(t, 1.0, 0.25)
    assert trig and cf == -1.0
    # never arms at rung 1.0 (needs 4pts fav; max high 103.5 -> 3.5)
    cf2, trig2, _ = be_outcome(t, 1.0, 1.0)
    assert not trig2 and cf2 == 3.0


def test_probe_sim_stop_scratch_flip():
    A = {"h": np.array([100.5, 102.0, 100.2, 104.0]),
         "l": np.array([99.5, 100.8, 99.9, 103.0]),
         "c": np.array([100.0, 101.5, 100.1, 103.5]),
         "eod": np.zeros(4, bool), "spread": 1.0}
    # rung 0.25x4=1: bar1 fav 2.0 arms; bar2 low 99.9 <= entry ->
    # scratch
    j, pts, reason = probe_sim(0, 1, 100.0, 4.0, A, 0.25, 3)
    assert (reason, pts) == ("scratch", -1.0)
    # no BE: runs to end_idx -> flip close-fill at 103.5
    j2, pts2, reason2 = probe_sim(0, 1, 100.0, 4.0, A, None, 3)
    assert (reason2, pts2) == ("flip", 2.5)
    # tight ATR -> stop touch-fill
    j3, pts3, reason3 = probe_sim(0, 1, 100.0, 0.2, A, None, 3)
    assert reason3 == "stop" and pts3 == -1.5      # 2.5x0.2 + spread


def test_campaigns_and_backoff_walk():
    t15 = np.array([0, 1, 1, 1, -1, -1, 0, 1])
    assert campaigns_of(t15) == [(1, 4, 1), (4, 6, -1), (7, 8, 1)]
    n = 40
    A = {"h": np.full(n, 100.2), "l": np.full(n, 99.0),
         "c": np.full(n, 99.5), "eod": np.zeros(n, bool),
         "spread": 0.5, "eff_dir": np.zeros(n, int)}
    fires = [(i, 1, 100.0, 0.4) for i in (0, 5, 10, 15, 20)]
    camp = (0, n, 1)
    no_bo = run_campaign(camp, fires, A, None)
    assert no_bo["probes"] == 5 and no_bo["stops"] == 5
    bo = run_campaign(camp, fires, A, None, backoff=(2, 30))
    assert bo["probes"] < 5 and bo["suppressed"] > 0
    assert bo["suppressed_losses_avoided"] > 0
    # twin-run bit-identity
    a = json.dumps(run_campaign(camp, fires, A, None, backoff=(2, 5)),
                   sort_keys=True)
    b = json.dumps(run_campaign(camp, fires, A, None, backoff=(2, 5)),
                   sort_keys=True)
    assert a == b


def test_survival_curve_counts():
    ts_ = [_trade([99, 98, 101], 1.0), _trade([99, 98, 97], -3.0),
           _trade([101, 102], 2.0)]
    sv = survival_curve(ts_)
    assert sv[0]["n"] == 2 and sv[0]["p_win"] == 0.5   # two underwater
    assert sv[2]["n"] == 1 and sv[2]["p_win"] == 0.0   # loser only
