"""Register 130 pins: the bucket edges, the top-bucket degradation
statistic (rest-minus-top, one-sided, distinct paths, top-bucket
measurability), and the within-stratum permutation null (twin-run; a
real degradation clears, a flat world does not)."""
import json

import numpy as np

from backtest.vol_regime import (MIN_TOP_N, TRAIL_SESSIONS, VOL_BUCKETS,
                                 bucket_of, cell, degradation,
                                 stratum_null)


def _rows(spec, seed=0):
    rs = np.random.RandomState(seed)
    out, i = [], 0
    for bucket, base, n in spec:
        for p in rs.normal(base, 1.0, n):
            out.append({"bucket": bucket, "pts": float(p),
                        "stopped": p < 0, "path": f"p{i}"})
            i += 1
    return out


def test_bucket_edges():
    assert [bucket_of(x) for x in (0, 49.9, 50, 79.9, 80, 94.9, 95,
                                   100)] == \
        ["<50", "<50", "50-80", "50-80", "80-95", "80-95", ">=95",
         ">=95"]
    assert bucket_of(None) is None
    assert (TRAIL_SESSIONS, VOL_BUCKETS) == (20, (50, 80, 95))


def test_degradation_direction_and_measurability():
    rows = _rows([("<50", 5.0, 30), ("50-80", 5.0, 30),
                  (">=95", -5.0, 15)])
    gap, sgap, ct, cr = degradation(rows)
    assert gap > 8 and sgap > 0.5          # top bucket worse, more stops
    thin = _rows([("<50", 5.0, 30), (">=95", -5.0, MIN_TOP_N - 1)])
    assert degradation(thin)[0] is None    # top bucket unmeasurable
    # duplicated paths count once (register 113 rides in)
    dup = _rows([(">=95", -5.0, 12)])
    for r in dup[1:]:
        r["path"] = dup[0]["path"]
    assert cell(dup)["n_distinct"] == 1


def test_stratum_null_twin_run_and_significance():
    hot = _rows([("<50", 5.0, 60), ("50-80", 5.0, 40),
                 (">=95", -6.0, 20)])
    n1, n2 = stratum_null(hot), stratum_null(hot)
    assert json.dumps(n1.tolist()) == json.dumps(n2.tolist())
    gap = degradation(hot)[0]
    valid = n1[~np.isnan(n1)]
    assert gap > np.percentile(valid, 95)          # a real split clears
    flat = _rows([("<50", 0.0, 60), ("50-80", 0.0, 40),
                  (">=95", 0.0, 20)], seed=3)
    gf = degradation(flat)[0]
    vf = stratum_null(flat)
    vf = vf[~np.isnan(vf)]
    assert not gf > np.percentile(vf, 95)          # a flat world stays quiet
