"""Register 123 pins: the expanding percentile is strictly-prior (no
lookahead) with a warmup floor; the scalp day-state split computes on
distinct paths with a deterministic day-state permutation null; the
alarm constants are the flagged registered values."""
import json

import numpy as np

from backtest.stress_organ import (MOM_SESSIONS, STRESS_PCTILE,
                                   WARMUP_DAYS, _expanding_pctile,
                                   scalp_split)


def test_expanding_pctile_no_lookahead_and_warmup():
    vals = np.arange(100, dtype=float)
    p = _expanding_pctile(vals)
    assert np.isnan(p[:WARMUP_DAYS]).all()       # warmup floor
    assert p[WARMUP_DAYS] == 1.0                 # max of its priors
    # a low value late reads low regardless of what follows (no lookahead)
    vals2 = np.arange(100, dtype=float)
    vals2[80] = -5.0
    p2 = _expanding_pctile(vals2)
    assert p2[80] == 0.0
    assert (MOM_SESSIONS, STRESS_PCTILE) == (5, 0.80)


def _rows(day_pts):
    out = []
    i = 0
    for day, pts in day_pts:
        for p in pts:
            out.append({"instrument": "uk100fut",
                        "variant": "R-SCALP-H" + str(6),
                        "window": "forward", "pts": p,
                        "week": "2026-W35", "day": day,
                        "path": f"p{i}"})
            i += 1
    return out


def test_scalp_split_gap_and_null_twin_run():
    rs = np.random.RandomState(0)
    days, states = [], {}
    day_pts = []
    for k in range(30):
        d = f"2026-08-{k + 1:02d}" if k < 28 else f"2026-09-{k - 27:02d}"
        st = ("stressed", "calm", "mixed")[k % 3]
        states[d] = st
        base = {"stressed": -8.0, "calm": 8.0, "mixed": 0.0}[st]
        day_pts.append((d, list(rs.normal(base, 1.0, 12))))
    rows = _rows(day_pts)
    s1 = scalp_split(rows, states)
    s2 = scalp_split(rows, states)
    assert json.dumps(s1, sort_keys=True, default=str) == \
        json.dumps(s2, sort_keys=True, default=str)   # twin-run
    cell = s1["uk100fut|R-SCALP-H" + str(6) + "|forward"]
    assert cell["best_state"] == "calm" and cell["gap"] > 10
    assert cell["clears"] is True                 # a real split clears
    # a state map carrying no information stays inside its null
    flat = {d: "calm" if i % 2 else "stressed"
            for i, d in enumerate(sorted(states))}
    rows2 = _rows([(d, list(rs.normal(0.0, 1.0, 12)))
                   for d in sorted(states)])
    s3 = scalp_split(rows2, flat)
    c3 = s3["uk100fut|R-SCALP-H" + str(6) + "|forward"]
    assert not c3["clears"]
