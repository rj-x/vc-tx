"""Register 91 pin: the fire-level ledger reconciles to the aggregate
artifacts — aggregates propose, rows confirm. Spot-cell equality
between reports/fires.csv and hypothesis_performance.json (initiation
hits/of, precision hits/of, capture medians), and between
bar_persistence_fires.csv and bar_persistence.json (reach pcts)."""
import csv
import json
import os

import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SB = os.path.join(ROOT, "reports", "scoreboard")

SPOT_SIGNALS = ("S0-H1", "S0-H2", "S0-H6")
SPOT_INSTRUMENTS = ("uk100fut", "ger40fut")


def test_fires_csv_reconciles_to_hypothesis_performance():
    rows = list(csv.DictReader(
        open(os.path.join(ROOT, "reports", "fires.csv"))))
    doc = json.load(open(os.path.join(
        SB, "hypothesis_performance.json")))
    checked = 0
    for instr in SPOT_INSTRUMENTS:
        blk = doc["instruments"][instr]["signals"]
        for sig in SPOT_SIGNALS:
            for w in ("backtest", "forward"):
                cell = blk[w].get(sig)
                if not cell or "precision" not in cell:
                    continue
                sub = [r for r in rows if r["instrument"] == instr
                       and r["signal"] == sig and r["zone"] == w]
                assert cell["precision"]["of"] == len(sub), \
                    (instr, sig, w, "row count")
                assert cell["precision"]["hits"] == sum(
                    r["participation_hit"] == "True" for r in sub), \
                    (instr, sig, w, "participation hits")
                assert cell["initiation"]["of"] == len(sub), \
                    (instr, sig, w, "initiation of")
                assert cell["initiation"]["hits"] == sum(
                    r["initiation_hit"] == "True" for r in sub), \
                    (instr, sig, w, "initiation hits")
                caps = [float(r["participation_capture_pts"])
                        for r in sub
                        if r["participation_hit"] == "True"
                        and r["participation_capture_pts"]
                        not in ("", "None")]
                med = cell["participation_capture_median_pts"]
                if caps and med is not None:
                    assert round(float(np.median(caps)), 1) == med, \
                        (instr, sig, w, "capture median")
                checked += 1
    assert checked >= 6, "too few spot cells checked"


def test_bar_persistence_fires_reconcile():
    rows = list(csv.DictReader(open(os.path.join(
        SB, "bar_persistence_fires.csv"))))
    doc = json.load(open(os.path.join(SB, "bar_persistence.json")))
    checked = 0
    for res in doc["results"]:
        instr = res["instrument"]
        if instr not in SPOT_INSTRUMENTS:
            continue
        for sig in SPOT_SIGNALS:
            cell = res["signals"].get(sig, {})
            for w in ("backtest", "forward"):
                agg = (cell.get(w) or {}).get("whole") or {}
                rp = (agg.get("reach_pct") or {}).get(
                    "atr_0.5", {}).get("5")
                if rp is None:
                    continue
                sub = [r for r in rows if r["instrument"] == instr
                       and r["signal"] == sig and r["zone"] == w
                       and r["touched_0p5atr_5b"] in ("True", "False")]
                assert rp["n"] == len(sub), (instr, sig, w, "n")
                g = round(100 * float(np.mean(
                    [r["touched_0p5atr_5b"] == "True"
                     for r in sub])), 1)
                assert g == rp["gross"], (instr, sig, w, "gross pct")
                nt = round(100 * float(np.mean(
                    [r["touched_0p5atr_5b_net_of_spread"] == "True"
                     for r in sub])), 1)
                assert nt == rp["net"], (instr, sig, w, "net pct")
                checked += 1
    assert checked >= 4, "too few spot cells checked"
