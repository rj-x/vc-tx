"""Register 88 item 4 pins: protection-policy counterfactual fills
(settled arming, prior-max levels, touch fill), tape classes, and
twin-run determinism of the cell grid."""
import json

import numpy as np

from backtest.capture_study import (GATE_PCTL, NEVER_AGAIN_BOUND_ATR,
                                    POLICIES, REGIME_GATE_POLICY,
                                    cell_grid, never_again_pricing,
                                    phase_regime_split, regime_floors,
                                    regime_gate, regime_of,
                                    protect_outcome, tape_class)
from backtest.underwater_census import trajectory


def _trade(closes, pts, atr0=4.0, entry=100.0, hi_off=0.5,
           lo_off=0.5, loud=None):
    c = np.array(closes, float)
    h, l = c + hi_off, c - lo_off
    ld = np.array(loud, bool) if loud is not None \
        else np.zeros(len(c), bool)
    traj = trajectory(0, len(c) - 1, 1, entry, atr0, h, l, c, ld)
    return {"traj": traj, "pts": pts, "atr0": atr0,
            "mfe_path": h - entry, "family": "event",
            "r": {"session": "london"}}


def test_be_and_trail_fills():
    # closes 100,103,100.4: bar1 high 103.5 arms everything <=0.875x;
    # bar2 low 99.9 touches entry -> BE scratch at -spread
    t = _trade([100.0, 103.0, 100.4], 0.4 - 1.0)
    be = next(p for p in POLICIES if p[0] == "BE@0.5")
    assert protect_outcome(t, 1.0, be) == -1.0
    # TRAIL arm 0.5 dist 0.5: level = prior max 3.5 - 2.0 = 1.5;
    # bar2 rel low -0.1 <= 1.5 -> exit at 1.5 - spread = 0.5
    tr = next(p for p in POLICIES if p[0] == "TRAIL-0.5-0.5")
    assert protect_outcome(t, 1.0, tr) == 0.5
    # RATCHET floors at entry: arm 1.0 (4pts) never reached -> actual
    ra = next(p for p in POLICIES if p[0] == "RATCHET-1.0-1.0")
    assert protect_outcome(t, 1.0, ra) == t["pts"]


def test_tape_classes():
    assert tape_class(_trade([101, 102], 2.0)["traj"]) == "clean"
    assert tape_class(_trade([99, 101], 1.0)["traj"]) == "quiet-dip"
    assert tape_class(_trade([99, 101], 1.0,
                             loud=[True, False])["traj"]) == "loud-dip"


def test_never_again_pricing_qualifies_and_costs():
    # winner 100->103->100.4 amputated by BE@0.5 (kept -1 vs +2.4-ish
    # actual); rung 1.5 marked non-qualifying vs the 1.0 bound
    ts_ = [_trade([100.0, 103.0, 100.4], 2.4)] * 4
    na = never_again_pricing(ts_, 1.0)
    assert na["BE@0.5"]["qualifies"] is True
    assert na["BE@1.5"]["qualifies"] is False
    assert na["BE@0.5"]["winners_amputated"] == 4
    assert na["BE@0.5"]["amputation_pts_per_100_trades"] == round(
        100 * 4 * (2.4 - -1.0) / 4, 1)
    assert NEVER_AGAIN_BOUND_ATR == 1.0


def test_phase_regime_split_at_fire_bar():
    # register 90: regime from the 1M phase at the FIRE BAR (ei-1)
    ts_ = [dict(_trade([100, 101], 1.0), ei=5),
           dict(_trade([100, 101], 1.0), ei=10)]
    t1 = np.zeros(20, int)
    t1[4] = 1                       # fire bar of the first trade only
    res = phase_regime_split(ts_, 1.0, {"t1": t1})
    assert set(res) == {"trending-at-entry", "ranging-at-entry"}
    assert res["trending-at-entry"]["BE@0.25"]["n"] == 1
    assert res["ranging-at-entry"]["BE@0.25"]["n"] == 1


def _gate_world(n_each=30):
    """Register 107 fixture: ranging-entry trades run +0.3xATR then
    collapse (BE@0.25 saves them); trending-entry trades run clean.
    Members (B-RANDOM stand-ins) never benefit from BE."""
    t1 = np.zeros(1000, int)
    base = []
    for i in range(n_each):
        # fire bar (ei-1) ranging: t1 == 0 at index 2*i+1... keep ei even
        ei = 2 * (i + 1)
        base.append(dict(_trade([100.0, 101.3, 98.0], -2.0 - 1.0),
                         ei=ei, r={"session": "london", "variant": "X"}))
        ej = 2 * (i + 1) + 400
        t1[ej - 1] = 1                      # trending at the fire bar
        base.append(dict(_trade([100.0, 101.3, 103.0], 3.0 - 1.0),
                         ei=ej, r={"session": "london", "variant": "X"}))
    members = []
    for m in range(5):
        mt = []
        for reg in ("ranging-at-entry", "trending-at-entry"):
            for _ in range(10):
                mt.append(dict(_trade([100.0, 101.3, 103.0], 2.0),
                               session="london", regime=reg, ei=0))
        members.append(mt)
    return base, members, {"t1": t1}


def test_regime_floors_and_gate_pass():
    base, members, A = _gate_world()
    fl = regime_floors(members, 1.0)
    assert set(fl) >= {"ranging-at-entry|whole", "ranging-at-entry|london",
                       "trending-at-entry|whole"}
    band = fl["ranging-at-entry|whole"]["policies"][REGIME_GATE_POLICY]
    assert band["members"] == 5 and band["max"] == 0.0    # BE never fires
    rg = regime_gate(base, 1.0, A, fl)
    g = rg["gate"]
    assert (g["ranging_n"], g["trending_n"]) == (30, 30)
    # ranging: BE@0.25 arms at +1xATR(4) -> +1.3 high arms 0.25x; bar 2
    # low 97.5 touches entry -> -spread (-1) vs actual -3: delta +2
    assert g["ranging_per_trade_delta"] == 2.0
    assert g["ranging_clears_floor"] and g["gap_per_trade"] == 2.0
    assert g["percentile_vs_null"] == 100.0 and g["beyond_luck"]
    assert g["PASS"] and g["sessions_ranging_clear"] == ["london"]
    # twin-run
    a = json.dumps(regime_gate(base, 1.0, A, fl), sort_keys=True)
    b = json.dumps(regime_gate(base, 1.0, A, fl), sort_keys=True)
    assert a == b


def test_regime_gate_fails_inside_band_or_luck():
    base, members, A = _gate_world()
    # a band whose max exceeds the arm's advantage -> not a clear
    fl = regime_floors(members, 1.0)
    fl["ranging-at-entry|whole"]["policies"][REGIME_GATE_POLICY]["max"] = 5.0
    g = regime_gate(base, 1.0, A, fl)["gate"]
    assert not g["ranging_clears_floor"] and not g["PASS"]
    # regime labels carry no information -> the gap sits inside luck
    A2 = {"t1": np.zeros(1000, int)}
    rs = np.random.RandomState(1)
    for t in base:
        if rs.rand() < 0.5:
            A2["t1"][t["ei"] - 1] = 1
    g2 = regime_gate(base, 1.0, A2, regime_floors(members, 1.0))["gate"]
    assert g2["percentile_vs_null"] is not None
    assert not (g2["beyond_luck"] and g2["percentile_vs_null"] <= GATE_PCTL)
    assert regime_of(5, np.array([0] * 4 + [1] + [0] * 5)) == \
        "trending-at-entry"
    assert regime_of(5, np.zeros(10, int)) == "ranging-at-entry"


def test_cell_grid_twin_run():
    ts_ = [_trade([100, 103, 100.4], -0.6),
           _trade([99, 101, 102], 1.0)] * 15
    a = json.dumps(cell_grid(ts_, 1.0), sort_keys=True)
    b = json.dumps(cell_grid(ts_, 1.0), sort_keys=True)
    assert a == b
    g = cell_grid(ts_, 1.0)
    assert all("best_policy" in c for c in g.values())
