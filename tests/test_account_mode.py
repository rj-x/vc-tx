"""Register 83 pins: the risk gate (pass, never shrink), the provider
closeout (before the stop), ruin semantics, recipe TF transformation
(signals untouched), and twin-run determinism. Register 86 pins: the
combined-open-risk collision rule, scope slugs, and layout twin-run."""
import json

import pandas as pd

from backtest.account_mode import (INITIAL_STOP_ATR, LEVERAGE_DEFAULT,
                                   MAINTENANCE_PCT, MIN_STAKE_DEFAULT,
                                   STAKE_DEFAULT, account_pass,
                                   attribution, scope_slug,
                                   transform_recipe)

T0 = pd.Timestamp("2026-08-17 09:00", tz="UTC")


def _t(i, pts, stop_pts, mae, entry=100.0):
    return {"entry_ts": T0 + pd.Timedelta(minutes=i),
            "exit_ts": T0 + pd.Timedelta(minutes=i + 10),
            "instrument": "x", "name": "S", "entry": entry,
            "pts": pts, "stop_pts": stop_pts, "mae_pts": mae,
            "reason": "close"}


def test_defaults_pinned():
    assert (STAKE_DEFAULT, LEVERAGE_DEFAULT, MAINTENANCE_PCT,
            MIN_STAKE_DEFAULT, INITIAL_STOP_ATR) \
        == (0.5, 200, 0.5, 0.5, 2.5)


def test_risk_gate_passes_never_shrinks():
    # pot 100, risk 2% -> budget GBP2; stake 0.5 -> stop 5pts risk 2.5
    # = REFUSED (not shrunk); stop 3pts risk 1.5 = taken
    rows, s = account_pass([_t(0, 4.0, 5.0, 1.0), _t(20, 4.0, 3.0, 1.0)],
                           100, 2.0, 0.5, 200, 0.5, 0.5)
    assert rows[0]["gate"] == "SKIPPED_RISK"
    assert rows[1]["gate"] == "TAKEN" and s["end_balance"] == 102.0


def test_provider_closeout_before_stop_and_ruin():
    # deposit = 0.5*100/200 = 0.25; maintenance 0.125. A deep MAE drags
    # equity below maintenance -> closes there (loss = balance - maint),
    # not at the stop
    rows, s = account_pass([_t(0, -3.0, 1.0, 500.0)],
                           1.0, 100.0, 0.5, 200, 0.5, 0.5)
    assert rows[0]["exit_reason"] == "PROVIDER_CLOSEOUT"
    assert s["provider_closeouts"] == 1
    assert s["end_balance"] == 0.12   # the maintenance level
    assert s["ruin"] is not None      # below min-stake viability


def test_twin_run_bit_identity():
    trades = [_t(i * 30, (-1) ** i * 2.0, 3.0, 1.5) for i in range(40)]
    a = account_pass(trades, 100, 2.0, 0.5, 200, 0.5, 0.5)
    b = account_pass(trades, 100, 2.0, 0.5, 200, 0.5, 0.5)
    assert json.dumps(a, sort_keys=True) == json.dumps(b, sort_keys=True)


def test_combined_open_risk_collision():
    # register 86: budget GBP2 at pot 100 / risk 2%; stop 3pts at
    # stake 0.5 = GBP1.5 each. Overlapping second entry -> combined
    # GBP3.0 breaches -> SKIPPED_RISK; sequential -> both TAKEN.
    rows, _s = account_pass([_t(0, 4.0, 3.0, 1.0), _t(5, 4.0, 3.0, 1.0)],
                            100, 2.0, 0.5, 200, 0.5, 0.5)
    assert [r["gate"] for r in rows] == ["TAKEN", "SKIPPED_RISK"]
    rows2, _s2 = account_pass([_t(0, 4.0, 3.0, 1.0),
                               _t(20, 4.0, 3.0, 1.0)],
                              100, 2.0, 0.5, 200, 0.5, 0.5)
    assert [r["gate"] for r in rows2] == ["TAKEN", "TAKEN"]


def test_scope_slugs():
    assert scope_slug(["uk100fut", "ger40fut", "nas100fut",
                       "us30fut"]) == "all4"
    assert scope_slug(["ger40fut", "nas100fut", "us30fut"]) == "ex-uk100"
    assert scope_slug(["nas100fut", "us30fut"]) == "nas-us30"
    assert scope_slug(["ger40fut"]) == "ger40"


def test_layout_twin_run_and_attribution():
    # register 86: bundled multi-instrument stream, twin-run
    # bit-identical; attribution conserves takens/refusals
    tl = []
    for i in range(30):
        t = _t(i * 7, (-1) ** i * 2.0, 3.0, 1.5)
        t["instrument"] = "uk100fut" if i % 2 else "us30fut"
        tl.append(t)
    a = account_pass(tl, 100, 2.0, 0.5, 200, 0.5, 0.5)
    b = account_pass(tl, 100, 2.0, 0.5, 200, 0.5, 0.5)
    assert json.dumps(a, sort_keys=True, default=str) \
        == json.dumps(b, sort_keys=True, default=str)
    per = attribution(a[0])
    assert sum(x["taken"] + x["refused"] for x in per.values()) \
        == len(a[0])


def test_transform_recipe_rescales_management_only():
    r = {"provenance": "x",
         "stages": [{"stop": [("atr", 2.5, "15min"),
                              ("trail_nth", 1, ("atr", 1.0, "15min"),
                               "15min")], "target": None}]}
    t = transform_recipe(r, "1min")
    st = t["stages"][0]["stop"]
    assert st[0] == ("atr", 2.5, "1min")
    assert st[1] == ("trail_nth", 1, ("atr", 1.0, "1min"), "1min")
