"""Register 133 pins: the stratum edges, the conditional-gate reuse
(off-window rows carry no pctl so the register-132 pause_cell skips
only in-open rows), stratum-gap measurability, and the day-permutation
null (twin-run; a real concentration clears; flat stays quiet)."""
import json

import numpy as np

from backtest.open_pause import (MIN_STRATUM_N, OPEN_W_MIN, STRATA,
                                 TRAIL_SESSIONS, day_perm_null,
                                 stratum_gap, stratum_of)
from backtest.vol_pause import pause_cell


def _r(pts, day, pct, in_open, path):
    return {"pts": pts, "day": day, "open_pctl": pct,
            "in_open": in_open,
            "stratum": stratum_of(pct) if in_open else None,
            "atr_pctl": pct if in_open else None,
            "stopped": pts < 0, "path": path}


def test_stratum_edges_and_constants():
    assert [stratum_of(x) for x in (0, 79.9, 80, 94.9, 95, 100)] == \
        ["<80", "<80", "80-95", "80-95", ">=95", ">=95"]
    assert stratum_of(None) is None
    assert (OPEN_W_MIN, TRAIL_SESSIONS) == (30, 20)
    assert STRATA == ("<80", "80-95", ">=95")


def test_conditional_gate_reuses_pause_cell():
    rows = [_r(-10.0, "d1", 99.0, True, "a"),   # in-open, hot: skipped
            _r(-10.0, "d1", 99.0, False, "b"),  # OFF-window, hot: kept
            _r(5.0, "d2", 40.0, True, "c")]     # in-open, calm: kept
    c = pause_cell(rows, 95)
    assert c["skipped"] == 1 and c["net_delta"] == 10.0
    assert c["stops_dodged"] == 1


def test_gap_and_day_null():
    rs = np.random.RandomState(0)
    rows, pctls, i = [], {}, 0
    for k in range(40):
        day = f"2026-07-{k % 28 + 1:02d}x{k}"
        hot = k % 4 == 0
        pctls[day] = 99.0 if hot else 40.0
        base = -6.0 if hot else 4.0
        for p in rs.normal(base, 1.0, 4):
            rows.append(_r(float(p), day, pctls[day], True, f"p{i}"))
            i += 1
    g, cl, ch = stratum_gap(rows)
    assert g > 8 and cl["n_distinct"] >= MIN_STRATUM_N
    n1, n2 = day_perm_null(rows, pctls), day_perm_null(rows, pctls)
    assert json.dumps(n1.tolist()) == json.dumps(n2.tolist())
    valid = n1[~np.isnan(n1)]
    assert g > np.percentile(valid, 95)            # concentration clears
    flat = [dict(r, pts=float(rs.normal(0, 1))) for r in rows]
    gf, _a, _b = stratum_gap(flat)
    vf = day_perm_null(flat, pctls)
    vf = vf[~np.isnan(vf)]
    assert not gf > np.percentile(vf, 95)          # flat stays quiet
    thin = [r for r in rows if r["stratum"] == "<80"][:12] \
        + [r for r in rows if r["stratum"] == ">=95"][:MIN_STRATUM_N - 1]
    assert stratum_gap(thin)[0] is None            # measurability floor
