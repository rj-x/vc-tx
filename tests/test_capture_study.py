"""Register 88 item 4 pins: protection-policy counterfactual fills
(settled arming, prior-max levels, touch fill), tape classes, and
twin-run determinism of the cell grid."""
import json

import numpy as np

from backtest.capture_study import (POLICIES, cell_grid,
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


def test_cell_grid_twin_run():
    ts_ = [_trade([100, 103, 100.4], -0.6),
           _trade([99, 101, 102], 1.0)] * 15
    a = json.dumps(cell_grid(ts_, 1.0), sort_keys=True)
    b = json.dumps(cell_grid(ts_, 1.0), sort_keys=True)
    assert a == b
    g = cell_grid(ts_, 1.0)
    assert all("best_policy" in c for c in g.values())
