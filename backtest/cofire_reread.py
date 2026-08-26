"""Co-fire consistency re-read (register 88 item 7; the 74-A5 queued
audit item, ORDERED at the 2026-08-28 sitting; pre-registered
prereg_cofire_consistency_reread, counted). ONE EMISSION, dated
artifact — results to the next sitting, archive-bound after it.

The standing co-fire census (register 45) read under the register-73
CONSISTENCY yardsticks: a pair qualifies with >= CONS_MIN_CELLS cells
at cell-n >= CONS_MIN_N, same-signed, |lift| > CONS_MIN_LIFT_PP;
field-significant at percentile > CONS_PCTL vs the null. Cell = pair x
window x zone x instrument from the standing cofire.json; lift =
with-stack precision minus without-stack precision; CELL n = the
WITH-STACK n (the lift-bearing leg). RECONCILIATION, stated: the
sitting's "248 cells at n>=15" matches the TOTAL-n (with+without)
count, which accrues weekly; the lift-bearing subset at with-n >=
CONS_MIN_N is what the statistic can read — the thinness census
prints either way. NULL: pinned sign-randomization of measurable cell
lifts within pair strata (the same-signedness luck), 100 seeds.
STATISTIC SHAPE (74-B): cross-window consistency (field count vs
null). No pair mints from this read — results to the sitting.
"""

import json
import os
import subprocess

import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "reports", "scoreboard")
DATED = "cofire_reread_2026-08-28"

CONS_MIN_CELLS = 3       # register 73 consistency yardsticks, reused
CONS_MIN_N = 15
CONS_MIN_LIFT_PP = 3.0
CONS_PCTL = 95.0
NULL_SHUFFLES = 100
NULL_SEEDS = tuple(range(NULL_SHUFFLES))


def collect_cells(art):
    """(pair -> [ (cell_id, with_n, lift_pp) ]) + the thinness census."""
    pairs = {}
    census = {"cells_total": 0, "total_n_ge_15": 0,
              "with_n_ge_5": 0, "with_n_ge_10": 0, "with_n_ge_15": 0,
              "max_with_n": 0}
    for res in art["results"]:
        instr = res["instrument"]
        for pair, ws in res["pairs"].items():
            for w, wins in ws.items():
                for zone, c in wins.items():
                    if not isinstance(c, dict):
                        continue
                    wt, wo = c.get("with", {}), c.get("without", {})
                    nw = wt.get("n") or 0
                    no = wo.get("n") or 0
                    census["cells_total"] += 1
                    if nw + no >= 15:
                        census["total_n_ge_15"] += 1
                    for th in (5, 10, 15):
                        if nw >= th:
                            census[f"with_n_ge_{th}"] += 1
                    census["max_with_n"] = max(census["max_with_n"],
                                               nw)
                    if (nw >= CONS_MIN_N
                            and wt.get("pct") is not None
                            and wo.get("pct") is not None):
                        pairs.setdefault(pair, []).append(
                            (f"{instr}|{w}|{zone}", nw,
                             round(wt["pct"] - wo["pct"], 1)))
    return pairs, census


def qualifying(pairs):
    out = []
    for pair, cells in sorted(pairs.items()):
        strong = [c for c in cells
                  if abs(c[2]) > CONS_MIN_LIFT_PP]
        if len(strong) < CONS_MIN_CELLS:
            continue
        pos = [c for c in strong if c[2] > 0]
        neg = [c for c in strong if c[2] < 0]
        side = pos if len(pos) >= len(neg) else neg
        if len(side) >= CONS_MIN_CELLS:
            out.append({"pair": pair, "cells": side,
                        "sign": "+" if side is pos else "-"})
    return out


def null_counts(pairs):
    counts = []
    keys = sorted(pairs)
    for seed in NULL_SEEDS:
        rs = np.random.RandomState(seed)
        perm = {p: [(cid, n, abs(l) * rs.choice((-1, 1)))
                    for cid, n, l in pairs[p]] for p in keys}
        counts.append(len(qualifying(perm)))
    return counts


def main():
    head = subprocess.run(["git", "rev-parse", "HEAD"], cwd=ROOT,
                          capture_output=True, text=True).stdout.strip()
    art_in = json.load(open(os.path.join(OUT, "cofire.json")))
    pairs, census = collect_cells(art_in)
    qual = qualifying(pairs)
    nulls = null_counts(pairs)
    pctl = (round(100 * float(np.mean(
        [len(qual) > m for m in nulls])), 1) if nulls else None)
    art = {"STAMP": ("OBSERVATIONAL co-fire consistency re-read "
                     "(74-A5, one emission) — results to the next "
                     "sitting; no pair mints from this read; "
                     "never validation"),
           "engine_commit": head,
           "source_cofire_commit": art_in.get("engine_commit"),
           "yardsticks": {"min_cells": CONS_MIN_CELLS,
                          "min_n": CONS_MIN_N,
                          "min_lift_pp": CONS_MIN_LIFT_PP,
                          "pctl": CONS_PCTL},
           "thinness_census": census,
           "measurable_pairs": {p: c for p, c in sorted(pairs.items())},
           "qualifying_pairs": qual,
           "luck": {"observed": len(qual),
                    "null_median": (float(np.median(nulls))
                                    if nulls else None),
                    "null_p95": (float(np.percentile(nulls, 95))
                                 if nulls else None),
                    "percentile_vs_null": pctl}}
    with open(os.path.join(OUT, f"{DATED}.json"), "w") as f:
        json.dump(art, f, indent=2, default=str)
    L = ["# Co-fire Consistency Re-read — 2026-08-28 (GENERATED by "
         "backtest.cofire_reread)", "",
         "Terms: [docs/GLOSSARY.md](../../docs/GLOSSARY.md).", "",
         f"Engine `{head[:9]}` — OBSERVATIONAL, pre-registered "
         "(prereg_cofire_consistency_reread, register 88 item 7; the "
         "74-A5 queued audit item). ONE EMISSION, dated; results to "
         "the next sitting; archive-bound after it. STATISTIC SHAPE "
         "(74-B): cross-window consistency — field count of "
         "qualifying pairs (register-73 yardsticks: >= "
         f"{CONS_MIN_CELLS} cells at with-stack n >= {CONS_MIN_N}, "
         f"same-signed, |lift| > {CONS_MIN_LIFT_PP:g}pp) vs a pinned "
         "sign-randomization null. RECONCILIATION: the sitting's "
         f"'248 cells at n>=15' matches the TOTAL-n count "
         f"({census['total_n_ge_15']} at this emission, accruing); "
         "the lift-bearing subset (with-stack n) is what the "
         "statistic reads.", "",
         f"**Thinness census:** {census['cells_total']} cells; "
         f"with-stack n >= 5: {census['with_n_ge_5']}, >= 10: "
         f"{census['with_n_ge_10']}, >= {CONS_MIN_N}: "
         f"{census['with_n_ge_15']}; max with-stack n "
         f"{census['max_with_n']}.", "",
         f"**Luck budget:** {len(qual)} qualifying pairs vs null "
         f"median {art['luck']['null_median']} / p95 "
         f"{art['luck']['null_p95']}; percentile {pctl}.", ""]
    if qual:
        L += ["| pair | sign | cells (instr / window / zone: n, "
              "lift) |", "|---|---|---|"]
        for q in qual:
            cs = "; ".join(f"{cid} n={n} {l:+.1f}pp"
                           for cid, n, l in q["cells"])
            L.append(f"| {q['pair']} | {q['sign']} | {cs} |")
    else:
        L.append("No pair qualifies at the registered yardsticks — "
                 "the with-stacks remain too thin for the "
                 "consistency lens; the thinness census above is the "
                 "read.")
    L.append("")
    with open(os.path.join(OUT, f"{DATED}.md"), "w") as f:
        f.write("\n".join(L))
    print(f"OBSERVATIONAL co-fire re-read -> {OUT}/{DATED}.md "
          f"({len(qual)} qualifying pairs)")


if __name__ == "__main__":
    main()
