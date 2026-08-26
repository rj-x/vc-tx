"""Trade-forensics pins (register 84): twin-run bit-identity of the
report layer on a synthetic enriched journal; scratch classification;
lockbox/sealed exclusion counting; null-percentile determinism."""
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

from backtest.trade_forensics import (FEATURES, outcome_of, report,
                                      usable)


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
