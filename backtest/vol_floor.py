"""Minimum-volatility gate counterfactual (register 137; pre-registered
2026-09-07 from the operator's pivot discovery of 2026-09-05).
OBSERVATIONAL. The register-132 machinery with the predicate INVERTED.

ORIGIN, the fence before the build: an operator pivot cut, post-hoc-
selected BY RESULTS — the backtest half is MOTIVATING, NOT EVIDENTIAL;
evidence reads forward/sealed only. MECHANISM EX-ANTE, scalp-specific:
sub-median volatility cannot travel the 0.5xATR target before costs —
entries there are spread donations; the asymmetric bracket STARVES at
the bottom of the distribution (the mirror of register 130's violence
mechanism at the top).

THE COUNTERFACTUAL: all journal arms replayed in strict fill order,
entries SKIPPED under three predicate forms — pooled-only
(atr_pctl < X), tod-only (atr_pctl_tod < X, the register-134
companion field), and the operator's joint form (BOTH < JOINT_X) —
X in FLOOR_X = {30, 50}, joint fixed at 50: five grid points. A None
percentile NEVER gates. Row-level per registers 102/103: skipped =
foregone; no resurrection of unblocked trades (stated limitation).

PER CELL (variant x leg x window x form x X; ex-lockbox; DISTINCT
PATHS per register 113): the register-132 accounting verbatim via
vol_pause.skip_accounting. FLOORS, the decisive column: B-RANDOM
members under the IDENTICAL gate, SCALP ARMS (the mechanism's
subject); the context ladder prints WITHOUT floors (implementer-
scoped, FLAGGED — as register 132). ENACTMENT, if a cell ever clears
its floor band on forward/sealed tape at measurable n: composes as
vol_gate(min=X) onto specific variant x market combinations — the
register-132 gate-not-clones ruling verbatim; NOTHING changes in any
live recipe here. Weekly under Part C; sealed untouched; twin-run
pinned (tests/test_vol_floor.py). Statistic shapes per 74-B: net
delta vs the member band (floor pattern); counts descriptive.
"""

import argparse
import json
import os
import subprocess
import sys

import numpy as np
import pandas as pd

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "scripts"))

from engine.store_loader import in_lockbox_span, lockbox_boundary, zones
from backtest.recipes import (RECIPE_SET_VERSION, RECIPE_SETS,
                              simulate, specialize)
from backtest.signal_points import baseline_fires
from backtest.vol_pause import skip_accounting
from backtest.vol_regime import (SCALP_ARMS, atr_pctl_fn,
                                 atr_pctl_tod_fn, journal_rows)

OUT = os.path.join(ROOT, "reports", "scoreboard")

FLOOR_X = (30, 50)       # register 137: the minimum-gate grid (the
                         # order's own values)
JOINT_X = 50             # register 137: the operator's joint form —
                         # both fields below this


def gate_grid():
    """The five pre-registered (form, X) grid points."""
    return tuple([("pooled", x) for x in FLOOR_X]
                 + [("tod", x) for x in FLOOR_X]
                 + [("joint", JOINT_X)])


def gated(pc, pt, form, x):
    """True iff the entry is skipped. A None percentile never gates."""
    if form == "pooled":
        return pc is not None and pc < x
    if form == "tod":
        return pt is not None and pt < x
    return (pc is not None and pt is not None
            and pc < x and pt < x)


def gate_cell(rows, form, x):
    """One cell's counterfactual on distinct paths (register-132
    accounting via the shared helper)."""
    return skip_accounting(
        rows, lambda r: gated(r["atr_pctl"], r.get("atr_pctl_tod"),
                              form, x))


def scalp_floor_bands(instr):
    """Member net-delta bands per arm x window x grid point — B-RANDOM
    members replayed under the IDENTICAL gate (the decisive column)."""
    from backtest.underwater_census import build_instrument
    A = build_instrument(instr)
    env = A["env"]
    p_fn, t_fn = atr_pctl_fn(instr), atr_pctl_tod_fn(instr)
    members = baseline_fires(env, A["engine_events"])["B-RANDOM"]
    boundary, gl = lockbox_boundary(), zones()["go_live"]
    grid = gate_grid()
    bands = {}
    for arm in SCALP_ARMS:
        recipe = specialize(RECIPE_SETS[RECIPE_SET_VERSION][arm], instr)
        deltas = {}          # (window, form, x) -> [member net deltas]
        shares = {}
        for mf in members:
            agg = {}
            cnt = {}
            tot = {}
            for t in simulate(mf, env, recipe, A["spread"]):
                if in_lockbox_span(t["entry_ts"]):
                    continue
                ts = pd.Timestamp(t["entry_ts"])
                w = ("backtest" if ts < boundary
                     else "forward" if ts >= gl else None)
                if w is None:
                    continue
                a = env.atr_at("15min", ts.value)
                pc = p_fn(ts.value, a) if a is not None else None
                pt = t_fn(ts.value, a) if a is not None else None
                tot[w] = tot.get(w, 0) + 1
                for form, x in grid:
                    if gated(pc, pt, form, x):
                        k = (w, form, x)
                        agg[k] = agg.get(k, 0.0) - float(t["pts"])
                        cnt[k] = cnt.get(k, 0) + 1
            for w in ("backtest", "forward"):
                for form, x in grid:
                    k = (w, form, x)
                    deltas.setdefault(k, []).append(
                        round(agg.get(k, 0.0), 1))
                    shares.setdefault(k, []).append(
                        round(cnt.get(k, 0) / tot[w], 3)
                        if tot.get(w) else 0.0)
        bands[arm] = {
            f"{w}|{form}|{x}": {"members": len(v),
                                "median": round(float(np.median(v)), 1),
                                "min": round(float(min(v)), 1),
                                "max": round(float(max(v)), 1),
                                "median_skip_share": round(float(
                                    np.median(shares[k])), 3)}
            for k, v in sorted(deltas.items())
            for w, form, x in [k]}
    return bands


def run():
    rows = journal_rows()      # registers 130/134: both fields per row
    strata = {}
    for r in rows:
        strata.setdefault((r["instrument"], r["variant"],
                           r["window"]), []).append(r)
    cells = {}
    for key, rr in sorted(strata.items()):
        for form, x in gate_grid():
            cells["|".join(key) + f"|{form}|{x}"] = \
                gate_cell(rr, form, x)
    floors = {}
    for instr in ("uk100fut", "ger40fut", "nas100fut", "us30fut"):
        print(f"# vol_floor floors: {instr} ...", file=sys.stderr)
        floors[instr] = scalp_floor_bands(instr)
    return {"floor_x": list(FLOOR_X), "joint_x": JOINT_X,
            "rows_ex_lockbox": len(rows),
            "cells": cells, "scalp_floors": floors}


def _emit(art, head):
    L = ["# Minimum-Volatility Gate Counterfactual (GENERATED by "
         "backtest.vol_floor)", "",
         "Terms: [docs/GLOSSARY.md](../../docs/GLOSSARY.md).", "",
         f"Engine `{head[:9]}` — OBSERVATIONAL, pre-registered "
         "(register 137; the register-132 machinery, predicate "
         "INVERTED). ORIGIN: an operator pivot cut, post-hoc-selected "
         "BY RESULTS — the backtest half is MOTIVATING, NOT "
         "EVIDENTIAL; evidence reads forward/sealed only. MECHANISM "
         "EX-ANTE, scalp-specific: sub-median volatility cannot "
         "travel the 0.5xATR target before costs — entries there are "
         "spread donations; the bracket STARVES at the bottom of the "
         "distribution (the mirror of register 130's violence at the "
         "top). Entries SKIPPED under pooled-only (atr_pctl < X), "
         "tod-only (atr_pctl_tod < X, register 134), and the joint "
         f"form (both < {JOINT_X}); X in {list(FLOOR_X)}; a None "
         "percentile never gates; row-level per registers 102/103 "
         "(skipped = foregone, no resurrection, stated). DISTINCT "
         "PATHS throughout (register 113). FLOORS: B-RANDOM members "
         "under the identical gate, SCALP ARMS ONLY (the mechanism's "
         "subject; the context ladder prints without floors — "
         "implementer-scoped, FLAGGED). A surviving forward/sealed "
         "cell composes as vol_gate(min=X) — gate-not-clones "
         "(register 132); NOTHING changes in any live recipe. "
         "Ex-lockbox; weekly under Part C.", "",
         "## Scalp arms — the evidence rows (net delta vs the member "
         "band; positive delta = the gate helped)", "",
         "| arm | leg | window | form | X | n (distinct) | skipped "
         "(share) | foregone wins | avoided losses | net Δ | member "
         "band med [min..max] (skip share) | beats band max |",
         "|---|---|---|---|---|---|---|---|---|---|---|"]
    n_beats = 0
    for key, c in art["cells"].items():
        instr, var, w, form, x = key.split("|")
        if var not in SCALP_ARMS:
            continue
        fb = art["scalp_floors"].get(instr, {}).get(var, {}) \
            .get(f"{w}|{form}|{x}")
        band = (f"{fb['median']} [{fb['min']}..{fb['max']}] "
                f"({fb['median_skip_share']})" if fb else "—")
        beats = ("YES" if fb and c["net_delta"] > fb["max"] else "no"
                 if fb else "—")
        n_beats += beats == "YES"
        L.append(f"| {var} | {instr} | {w} | {form} | {x} "
                 f"| {c['n']} ({c['n_distinct']}) "
                 f"| {c['skipped']} ({c['skip_share']}) "
                 f"| {c['foregone_win_pts']} | {c['avoided_loss_pts']} "
                 f"| {c['net_delta']:+.1f} | {band} | {beats} |")
    L += ["", "## Context ladder (all arms; characterization — no "
          "floors here, stated; full grid in the JSON)", "",
          "| leg | variant | window | form | X | n (distinct) | "
          "skipped (share) | net Δ |",
          "|---|---|---|---|---|---|---|---|"]
    for key, c in art["cells"].items():
        instr, var, w, form, x = key.split("|")
        if var in SCALP_ARMS or c["skipped"] == 0:
            continue
        L.append(f"| {instr} | {var} | {w} | {form} | {x} "
                 f"| {c['n']} ({c['n_distinct']}) "
                 f"| {c['skipped']} ({c['skip_share']}) "
                 f"| {c['net_delta']:+.1f} |")
    L += ["", f"Evidence cells beating their band max: {n_beats}.", ""]
    with open(os.path.join(OUT, "vol_floor.md"), "w") as f:
        f.write("\n".join(L))
    return n_beats


def main():
    ap = argparse.ArgumentParser()
    ap.parse_args()
    head = subprocess.run(["git", "rev-parse", "HEAD"], cwd=ROOT,
                          capture_output=True, text=True).stdout.strip()
    art = {"STAMP": ("OBSERVATIONAL minimum-volatility gate "
                     "counterfactual — pivot-cut origin recorded, "
                     "motivating not evidential; vol_gate(min=X) "
                     "composes, never clones; never validation"),
           "engine_commit": head, **run()}
    with open(os.path.join(OUT, "vol_floor.json"), "w") as f:
        json.dump(art, f, indent=2, default=str)
    n = _emit(art, head)
    print(f"OBSERVATIONAL vol floor -> {OUT}/vol_floor.md "
          f"({n} evidence cells beat their band max)")


if __name__ == "__main__":
    main()
