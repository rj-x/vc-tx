"""Journal field survey (register 80; pre-registered
prereg_journal_survey). The narrative-survey statistics applied to the
TRADE JOURNAL: the sentence × variant × session cell grid (n≥25,
instruments POOLED; per-instrument breakdown in the JSON).

(a) PERMUTATION NULL for the CONCENTRATION statistic: variant labels
    shuffled within sentence×session strata (pinned seeds, 100
    shuffles); statistic = the max count of positive-median cells
    landing in ONE variant. The observed concentration prints against
    the null distribution.
(b) SESSION-SCOPED BASELINE FLOORS: ensembles under identical
    management, per session, for every positive-median cell (member
    medians persisted by the trade layer in journal_baselines.json —
    same run, no re-simulation).
(c) Both statistics print in the LUCK-BUDGET block. Cells surviving
    null + floor become QUESTION CANDIDATES through the front door —
    LISTED, NOT MINTED.

Statistic shapes declared (74-B): concentration = field count vs
permutation null; floors = single-cell median vs session-scoped
ensemble range. Counts, dimming, twin-run pinned. Weekly under Part C
(runs after the trade layer).

LOCKBOX-SPAN RULING (register 85, 2026-08-27): journal rows OPENING
inside the legacy lockbox span are excluded here — the span is its own
zone, neither backtest nor forward. The pre-ruling emissions pooled
those rows ("inherited from the journal", caught by the forensics
build's flag); the register-80 headline findings were declared
TAINTED-RERUNNABLE and re-verified on the excluded cut at the ruling
(outcome in register 85). Row counts reconcile in the header.
"""

import argparse
import csv
import json
import os
import subprocess
import sys

import numpy as np
import pandas as pd

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "scripts"))

from engine.store_loader import in_lockbox_span
from backtest.signal_points import DRIFT_SKEW_SHARE, TREND_FAMILY

OUT = os.path.join(ROOT, "reports", "scoreboard")
TRADES_CSV = os.path.join(ROOT, "reports", "trades.csv")
BASE_JSON = os.path.join(OUT, "journal_baselines.json")

MIN_CELL_N = 25
NULL_SHUFFLES = 100
NULL_SEEDS = tuple(range(NULL_SHUFFLES))


def build_cells(rows):
    """Pooled sentence×variant×session cells + per-instrument split."""
    cells, per_instr = {}, {}
    for r in rows:
        k = (r["sentence_id"], r["variant"], r["session"])
        cells.setdefault(k, []).append(float(r["points"]))
        per_instr.setdefault(k + (r["instrument"],), []).append(
            float(r["points"]))
    return cells, per_instr


def concentration(cells):
    """(variant -> positive-median measurable-cell count, max)."""
    pos = {}
    tot = {}
    for (sent, var, sess), pts in cells.items():
        if len(pts) < MIN_CELL_N:
            continue
        tot[var] = tot.get(var, 0) + 1
        if float(np.median(pts)) > 0:
            pos[var] = pos.get(var, 0) + 1
    return pos, tot, (max(pos.values()) if pos else 0)


def null_concentration(rows):
    """Shuffle variant labels within sentence×session strata; the null
    distribution of max-positive-cells-in-one-variant. Deterministic."""
    strata = {}
    for r in rows:
        strata.setdefault((r["sentence_id"], r["session"]), []).append(
            (r["variant"], float(r["points"])))
    maxima = []
    for seed in NULL_SEEDS:
        rs = np.random.RandomState(seed)
        cells = {}
        for (sent, sess), pairs in strata.items():
            labels = [p[0] for p in pairs]
            pts = [p[1] for p in pairs]
            perm = rs.permutation(len(labels))
            for i, j in enumerate(perm):
                cells.setdefault((sent, labels[j], sess),
                                 []).append(pts[i])
        _pos, _tot, mx = concentration(cells)
        maxima.append(mx)
    return maxima


def main():
    ap = argparse.ArgumentParser()
    ap.parse_args()
    os.makedirs(OUT, exist_ok=True)
    head = subprocess.run(["git", "rev-parse", "HEAD"], cwd=ROOT,
                          capture_output=True, text=True).stdout.strip()
    all_rows = list(csv.DictReader(l for l in open(TRADES_CSV) if not l.startswith("#")))
    rows = [r for r in all_rows
            if not in_lockbox_span(r["open_ts"])]   # register 85
    n_excl = len(all_rows) - len(rows)
    floors = (json.load(open(BASE_JSON))["floors"]
              if os.path.exists(BASE_JSON) else {})
    cells, per_instr = build_cells(rows)
    pos, tot, mx = concentration(cells)
    maxima = null_concentration(rows)
    pctl = round(100 * float(np.mean([mx > m for m in maxima])), 1)
    # long-share per sentence for baseline matching (register 60 rule)
    share = {}
    for r in rows:
        share.setdefault(r["sentence_id"], []).append(
            int(r["direction"]) == 1)
    candidates = []
    detail = []
    for (sent, var, sess), pts in sorted(cells.items()):
        if len(pts) < MIN_CELL_N:
            continue
        med = round(float(np.median(pts)), 2)
        if med <= 0:
            continue
        bname = ("B-TREND" if sent in TREND_FAMILY else
                 "B-ALWAYS-LONG"
                 if float(np.mean(share[sent])) >= DRIFT_SKEW_SHARE
                 else "B-RANDOM")
        # pooled session floor: union of every instrument's member
        # medians for this variant/baseline/session
        fl = []
        for instr, fs in floors.items():
            fl.extend(fs.get("|".join((var, bname, sess)), []))
        fmax = round(float(max(fl)), 2) if fl else None
        fmed = round(float(np.median(fl)), 2) if fl else None
        clears = (fmax is not None and med > fmax)
        row = {"sentence": sent, "variant": var, "session": sess,
               "n": len(pts), "median_pts": med,
               "floor_baseline": bname, "floor_median": fmed,
               "floor_max": fmax, "clears_floor_range": clears,
               "per_instrument": {
                   i: {"n": len(v),
                       "median": round(float(np.median(v)), 2)}
                   for (s2, v2, se2, i), v in per_instr.items()
                   if (s2, v2, se2) == (sent, var, sess)}}
        detail.append(row)
        if clears:
            candidates.append(row)
    art = {"STAMP": ("OBSERVATIONAL journal field survey — luck priced; "
                     "survivors are QUESTION CANDIDATES, listed not "
                     "minted; never validation"),
           "engine_commit": head, "min_cell_n": MIN_CELL_N,
           "null_shuffles": NULL_SHUFFLES,
           "ex_lockbox": {"journal_rows": len(all_rows),
                          "excluded_lockbox_span": n_excl,
                          "rows_used": len(rows),
                          "ruling": "register 85 (2026-08-27)"},
           "concentration": {"positive_by_variant": pos,
                             "measurable_by_variant": tot,
                             "observed_max": mx,
                             "null_median": float(np.median(maxima)),
                             "null_p95": float(np.percentile(maxima,
                                                             95)),
                             "percentile_vs_null": pctl},
           "positive_cells": detail, "question_candidates": candidates}
    with open(os.path.join(OUT, "journal_survey.json"), "w") as f:
        json.dump(art, f, indent=2, default=str)
    c = art["concentration"]
    L = ["# Journal Field Survey (GENERATED by backtest.journal_survey)",
         "", "Terms: [docs/GLOSSARY.md](../../docs/GLOSSARY.md).", "",
         f"Engine `{head[:9]}` — OBSERVATIONAL, pre-registered "
         "(prereg_journal_survey, register 80). Sentence × variant × "
         f"session cells, n≥{MIN_CELL_N}, instruments pooled "
         "(per-instrument split in the JSON). STATISTIC SHAPES (74-B): "
         "concentration = field count vs permutation null (variant "
         "labels shuffled within sentence×session strata, "
         f"{NULL_SHUFFLES} pinned shuffles); floors = single-cell "
         "median vs the session-scoped baseline ensemble range under "
         "IDENTICAL management. Survivors are QUESTION CANDIDATES "
         "through the front door — LISTED, NOT MINTED. EX-LOCKBOX "
         "(register 85): the lockbox span is its own zone — "
         f"{len(rows)} of {len(all_rows)} journal rows used, "
         f"{n_excl} lockbox-span opens excluded.", "",
         "**Luck budget:** positive-median cells by variant: "
         f"{c['positive_by_variant']} of {c['measurable_by_variant']} "
         f"measurable; observed max-in-one-variant {c['observed_max']} "
         f"vs null median {c['null_median']:g} / p95 "
         f"{c['null_p95']:g}; percentile {c['percentile_vs_null']}.",
         "",
         "| sentence | variant | session | n | median pts | floor "
         "(med/max) | clears range | candidate |",
         "|---|---|---|---|---|---|---|---|"]
    for r in detail:
        dim = "°" if r["n"] < MIN_CELL_N else ""
        L.append(f"| {r['sentence']} | {r['variant']} | {r['session']} "
                 f"| {dim}{r['n']} | {r['median_pts']} "
                 f"| {r['floor_median']}/{r['floor_max']} "
                 f"| {'YES' if r['clears_floor_range'] else 'no'} "
                 f"| {'**CANDIDATE**' if r in candidates else '—'} |")
    L.append("")
    with open(os.path.join(OUT, "journal_survey.md"), "w") as f:
        f.write("\n".join(L))
    print(f"OBSERVATIONAL journal survey -> {OUT}/journal_survey.md "
          f"({len(candidates)} candidates)")


if __name__ == "__main__":
    main()
