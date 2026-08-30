"""Register 114 pins: the session-standardized base (register-47
method), the two-sided within-session permutation null (twin-run,
significance direction, no-shift worlds stay quiet), the swing-leg
arrival/departure classification, and the >= 3-of-4-leg claim rule with
single-leg findings routed to WATCH."""
import numpy as np

from backtest.zone_anatomy import (ANATOMY_MIN_BARS, ANATOMY_MIN_LEGS,
                                   CLAIM_MIN_LEGS, _cell_result,
                                   cell_shift, claims_and_watch,
                                   leg_zone_flags, legs_from_log,
                                   perm_null)


def _world(n=4000, shift=0.0, seed=0):
    rs = np.random.RandomState(seed)
    vals = rs.normal(1.0, 0.3, n)
    valid = np.ones(n, bool)
    sess = np.array(["london", "asia"] * (n // 2), dtype=object)
    in_mask = np.zeros(n, bool)
    in_mask[:400] = True
    vals[in_mask] += shift
    return vals, valid, sess, in_mask, ~in_mask


def test_session_standardized_base():
    # out bars: london metric ~2.0, asia ~1.0; in bars all-london ->
    # the matched base must be the LONDON out value, not the pooled mix
    n = 2000
    sess = np.array(["london"] * (n // 2) + ["asia"] * (n // 2),
                    dtype=object)
    vals = np.where(sess == "london", 2.0, 1.0).astype(float)
    valid = np.ones(n, bool)
    in_mask = np.zeros(n, bool)
    in_mask[:100] = True                       # london only
    vals[in_mask] = 5.0
    iv, base, sh, w = cell_shift("median", vals, valid, in_mask,
                                 ~in_mask, sess)
    assert (iv, base, sh) == (5.0, 2.0, 3.0)
    assert w == {"london": 1.0}


def test_perm_null_twin_run_and_directions():
    vals, valid, sess, im, om = _world(shift=0.5)
    n1 = perm_null("median", vals, valid, im, om, sess)
    n2 = perm_null("median", vals, valid, im, om, sess)
    assert np.allclose(n1, n2, equal_nan=True)         # twin-run
    iv, base, sh, _ = cell_shift("median", vals, valid, im, om, sess)
    c = _cell_result("median", "u", int(im.sum()), int(om.sum()),
                     iv, base, sh, n1, ANATOMY_MIN_BARS)
    assert c["significant"] and c["pct_vs_null"] == 100.0
    # a no-shift world stays quiet
    vals0, valid0, sess0, im0, om0 = _world(shift=0.0)
    iv0, b0, sh0, _ = cell_shift("median", vals0, valid0, im0, om0, sess0)
    c0 = _cell_result("median", "u", int(im0.sum()), int(om0.sum()),
                      iv0, b0, sh0,
                      perm_null("median", vals0, valid0, im0, om0, sess0),
                      ANATOMY_MIN_BARS)
    assert not c0["significant"]
    # thin in-zone population is unmeasurable however bright
    c_thin = _cell_result("median", "u", ANATOMY_MIN_BARS - 1, 100,
                          5.0, 1.0, 4.0, n1, ANATOMY_MIN_BARS)
    assert not c_thin["measurable"] and not c_thin["significant"]


def test_leg_machinery():
    log = [dict(conf_ts=10, type="L", idx=0, price=100.0),
           dict(conf_ts=20, type="H", idx=10, price=110.0),
           dict(conf_ts=30, type="L", idx=15, price=104.0),
           dict(conf_ts=40, type="H", idx=25, price=112.0)]
    legs = legs_from_log(log)
    assert [round(g["velocity"], 2) for g in legs] == [1.0, 1.2, 0.8]
    ts = np.array([5, 15, 25, 35, 45])
    state = np.array([False, True, False, False, False])
    fl = leg_zone_flags(legs, ts, state)
    assert [f["arriving"] for f in fl] == [True, False, False]
    assert [f["departing"] for f in fl] == [False, True, False]
    assert ANATOMY_MIN_LEGS == 25


def test_claims_three_of_four_and_watch_routing():
    def cell(shift, sig=True, meas=True):
        return {"unit": "u", "in_n": 500, "out_n": 5000,
                "in_value": 1.0 + shift, "base_value": 1.0,
                "shift": shift, "null_p95_abs": 0.05,
                "pct_vs_null": 99.0, "null_valid_seeds": 100,
                "significant": sig, "measurable": meas}
    key = "4h|D|forward"
    results = [
        {"instrument": "uk100fut", "cells": {key: {"loud_rate": cell(0.2)}}},
        {"instrument": "ger40fut", "cells": {key: {"loud_rate": cell(0.3)}}},
        {"instrument": "nas100fut", "cells": {key: {"loud_rate": cell(0.1)}}},
        {"instrument": "us30fut",
         "cells": {key: {"loud_rate": cell(-0.4, sig=False),
                         "test_rate": cell(1.5)}}}]
    claims, watch = claims_and_watch(results, {"us30fut": {
        "seed_maxes": [1.0] * 99 + [40.0]}})
    assert len(claims) == 1 and claims[0]["metric"] == "loud_rate"
    assert claims[0]["legs"] == ["uk100fut", "ger40fut", "nas100fut"]
    assert CLAIM_MIN_LEGS == 3
    # the us30 test_rate cell is single-leg -> WATCH with selection stat
    assert len(watch) == 1 and watch[0]["metric"] == "test_rate"
    assert watch[0]["sel_pct"] == 99.0 and watch[0]["beats_selection"]
    # mixed signs never claim: flip one leg's sign
    results[1]["cells"][key]["loud_rate"]["shift"] = -0.3
    claims2, watch2 = claims_and_watch(results, {})
    assert not claims2 and len(watch2) == 4
