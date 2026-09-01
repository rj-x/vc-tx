"""Trade-forensics pins (register 84): twin-run bit-identity of the
report layer on a synthetic enriched journal; scratch classification;
lockbox/sealed exclusion counting; null-percentile determinism."""
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

from backtest.trade_forensics import (ENRICH_COLS, FEATURES, net_ledger,
                                      outcome_of, report, usable,
                                      zone_of)


def test_registered_columns_are_emitted():
    # the register-column inventory pin (operator column check,
    # 2026-09-01): every per-trade column the register orders must be
    # in ENRICH_COLS — atr_pctl (register 130) was ordered and not
    # emitted until this pin existed; atr_pctl_tod (register 134) is
    # covered per that entry's follow-through rule
    assert {"spans_high_event", "atr_pctl",
            "atr_pctl_tod"} <= set(ENRICH_COLS)


def _rows():
    rows = []
    for i in range(120):
        win = i % 3 != 0                    # 2/3 winners
        rows.append({
            "instrument": "uk100fut", "sentence_id": "S0-H1",
            "variant": "R-ARM15", "session": "london",
            "open_ts": "2026-08-20 10:%02d:00+00:00" % (i % 60),
            "points": 12.0 if win else -9.0,
            "exit_reason": "stop", "outcome": "win" if win else "loss",
            "mae_atr": 0.4, "postexit_mfe_60m_pts": 3.0,
            "cont_60m_pts": 1.0,
            # a feature that separates perfectly, and neutral fillers
            "quadrant": "narrow-quiet" if win else "wide-loud",
            **{f: "x" for f in FEATURES
               if f not in ("quadrant",)}})
    return rows


def test_twin_run_bit_identity():
    a = json.dumps(report(_rows(), "head")[2], default=str)
    b = json.dumps(report(_rows(), "head")[2], default=str)
    assert a == b


def test_scratch_win_loss():
    assert outcome_of(0.5, 1.3) == "scratch"
    assert outcome_of(-1.2, 1.3) == "scratch"
    assert outcome_of(1.4, 1.3) == "win"
    assert outcome_of(-1.4, 1.3) == "loss"


def test_lockbox_and_sealed_excluded():
    rows = [{"open_ts": "2026-08-20 10:00:00+00:00"},   # forward: kept
            {"open_ts": "2026-08-05 10:00:00+00:00"},   # lockbox span
            {"open_ts": "2026-09-03 10:00:00+00:00"},   # sealed
            {"open_ts": "2026-07-20 10:00:00+00:00"}]   # working set
    keep, n_lock, n_seal = usable(rows)
    assert (len(keep), n_lock, n_seal) == (2, 1, 1)


def test_net_ledger_zones_verdict_and_floor():
    # register 84 amendment: pooled = W+L+F; verdict thin below n=25;
    # floor clearance on the EX-LOCKBOX median only
    def _r(ts, pts):
        return {"sentence_id": "S0-H1", "variant": "R-X",
                "session": "london", "open_ts": ts, "points": pts}
    rows = ([_r("2026-07-20 10:00:00+00:00", 5.0)] * 10
            + [_r("2026-08-05 10:00:00+00:00", 3.0)] * 5
            + [_r("2026-08-20 10:00:00+00:00", -2.0)] * 8)
    assert [zone_of(r["open_ts"]) for r in rows[:1] + rows[10:11]
            + rows[15:16]] == ["working", "lockbox", "forward"]
    nl = net_ledger(rows, {"R-X|B-RANDOM|london": [0.0]}, {})
    assert len(nl) == 1
    r = nl[0]
    assert (r["working_net"], r["lockbox_net"], r["forward_net"]) \
        == (50.0, 15.0, -16.0)
    assert r["pooled_net"] == 49.0
    assert (r["working_n"], r["lockbox_n"], r["forward_n"]) == (10, 5, 8)
    assert r["verdict"] == "forward-thin"          # forward n < 25
    assert r["clears_floor"] is True               # ex-lockbox med 1.5
    # forward-deep cells key on the forward median's sign
    rows2 = [_r("2026-08-20 10:00:00+00:00", -2.0)] * 30
    assert net_ledger(rows2, {}, {})[0]["verdict"] == "forward-negative"


def test_separator_survives_and_luck_budget_prints():
    per_instr, _cm, art = report(_rows(), "head")
    res = per_instr["uk100fut"]
    surv = [c for c in res["separators"] if c["survivor"]]
    assert surv, "perfect separator must survive its null"
    assert all(c["feature"] == "quadrant" for c in surv)
    lk = res["luck"]
    assert lk["measurable_cells"] > 0
    assert lk["percentile_vs_null"] is not None
    assert lk["observed_qualifying"] >= 2
