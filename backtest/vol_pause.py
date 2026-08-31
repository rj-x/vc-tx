"""Volatility-pause counterfactual (register 132; pre-registered
prereg_vol_pause, counted 2026-08-31; extends the register-130 cut —
the operator's SEEING-vs-BELIEVING ruling: changes visible in the next
campaign on all data; enactment bars read FORWARD). OBSERVATIONAL.

THE COUNTERFACTUAL: the journal's ACTUAL rows replayed in strict fill
order with entries SKIPPED when atr_pctl at fire > X, X in PAUSE_X =
{80, 95} (the register-130 percentile field reused verbatim — the fire
sits one minute inside the same 15M ATR bar as the entry stamp, so the
field re-anchors nothing; no new thresholds). The scalp arms are the
EVIDENCE rows; the full ladder (all fourteen arms) prints as CONTEXT.
Row-level convention per registers 102/103: skipped = foregone; no
resurrection of trades the skipped position would have unblocked
(stated limitation, as there).

PER CELL (variant x instrument x window x X; DISTINCT PATHS per
register 113 throughout): entries skipped (count, share), points
foregone from skipped winners, losses avoided from skipped losers, net
delta vs no-pause, stops dodged (count, points, the worst single stop
dodged). FLOORS: B-RANDOM members under the IDENTICAL pause rules —
the "would random books also improve?" floor — computed for the SCALP
ARMS (the evidence rows); the context ladder prints WITHOUT floors
(implementer-scoped coverage limitation, FLAGGED — the register-105
stop-axis pattern; a context row that wants evidence status buys its
own floor first). The worst-27 forensic rows tabled: which land in
each skip set (lockbox rows shown with their zone label, row display
only — no aggregate touches them).

FENCES: characterization on backtest, EVIDENCE ON FORWARD — enactment
of any pause still requires the register-130 forward/top-bucket
evidence (unmeasurable at n=1-2 this emission; the sealed window
accrues it); NOTHING changes in any live recipe; the counterfactual
re-emits weekly under Part C so each new week's tape retests it;
any surviving cell proposes the pause as a COMPOSABLE ENTRY-GATE
component — vol_gate(X) — ratified onto specific variant x market
combinations, NEVER as cloned variants (operator + reviewer scoping
ruling 2026-08-31, recorded in the register). Ex-lockbox for every
aggregate; sealed untouched; twin-run pinned
(tests/test_vol_pause.py). Statistic shapes per 74-B: counterfactual
net delta vs the member band (floor pattern); counts descriptive.
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

from engine.store_loader import in_lockbox_span, lockbox_boundary, zones
from backtest.per_market_watch import distinct_paths
from backtest.recipes import (RECIPE_SET_VERSION, RECIPE_SETS,
                              simulate, specialize)
from backtest.signal_points import baseline_fires
from backtest.vol_regime import SCALP_ARMS, atr_pctl_fn, journal_rows

OUT = os.path.join(ROOT, "reports", "scoreboard")
TRADES_CSV = os.path.join(ROOT, "reports", "trades.csv")

PAUSE_X = (80, 95)       # the register-130 bucket edges reused; no new
                         # thresholds
WORST_N = 27             # the operator's forensic set size (the order's)


def pause_cell(rows, x):
    """One cell's counterfactual on distinct paths: skip atr_pctl > x."""
    ded = distinct_paths(rows)
    skip = [r for r in ded
            if r["atr_pctl"] is not None and r["atr_pctl"] > x]
    sk_pts = np.array([r["pts"] for r in skip], float)
    stops = [r for r in skip if r["stopped"]]
    return {"n": len(rows), "n_distinct": len(ded),
            "skipped": len(skip),
            "skip_share": (round(len(skip) / len(ded), 3) if ded
                           else None),
            "foregone_win_pts": round(float(sk_pts[sk_pts > 0].sum()), 1)
            if len(sk_pts) else 0.0,
            "avoided_loss_pts": round(float(-sk_pts[sk_pts < 0].sum()),
                                      1) if len(sk_pts) else 0.0,
            "net_delta": round(float(-sk_pts.sum()), 1)
            if len(sk_pts) else 0.0,
            "stops_dodged": len(stops),
            "stops_dodged_pts": round(float(sum(r["pts"]
                                                for r in stops)), 1),
            "worst_stop_dodged": (round(min(r["pts"] for r in stops), 1)
                                  if stops else None)}


def scalp_floor_bands(instr):
    """Member net-delta bands per arm x window x X (the floor)."""
    from backtest.underwater_census import build_instrument
    A = build_instrument(instr)
    env = A["env"]
    pctl = atr_pctl_fn(instr)
    members = baseline_fires(env, A["engine_events"])["B-RANDOM"]
    boundary, gl = lockbox_boundary(), zones()["go_live"]
    bands = {}
    for arm in SCALP_ARMS:
        recipe = specialize(RECIPE_SETS[RECIPE_SET_VERSION][arm], instr)
        deltas = {}          # (window, x) -> [member net deltas]
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
                pc = pctl(ts.value, a) if a is not None else None
                tot[w] = tot.get(w, 0) + 1
                for x in PAUSE_X:
                    if pc is not None and pc > x:
                        agg[(w, x)] = agg.get((w, x), 0.0) - float(t["pts"])
                        cnt[(w, x)] = cnt.get((w, x), 0) + 1
            for w in ("backtest", "forward"):
                for x in PAUSE_X:
                    deltas.setdefault((w, x), []).append(
                        round(agg.get((w, x), 0.0), 1))
                    shares.setdefault((w, x), []).append(
                        round(cnt.get((w, x), 0) / tot[w], 3)
                        if tot.get(w) else 0.0)
        bands[arm] = {
            f"{w}|{x}": {"members": len(v),
                         "median": round(float(np.median(v)), 1),
                         "min": round(float(min(v)), 1),
                         "max": round(float(max(v)), 1),
                         "median_skip_share": round(float(np.median(
                             shares[(w, x)])), 3)}
            for (w, x), v in sorted(deltas.items())}
    return bands


def worst_forensic_rows(pctls):
    """The operator's worst-N scalp-REF rows (all zones; lockbox rows
    DISPLAYED with their zone label, never aggregated) with skip-set
    membership."""
    boundary, gl = lockbox_boundary(), zones()["go_live"]
    ref = "R-SCALP-H" + str(6) + "-REF"
    rows = []
    for r in csv.DictReader(l for l in open(TRADES_CSV)
                            if not l.startswith("#")):
        if r["variant"] != ref:
            continue
        rows.append(r)
    rows.sort(key=lambda r: float(r["points"]))
    out = []
    for r in rows[:WORST_N]:
        t = pd.Timestamp(r["open_ts"])
        zone = ("lockbox" if in_lockbox_span(r["open_ts"]) else
                "backtest" if t < boundary else
                "forward" if t >= gl else "?")
        instr = r["instrument"]
        if instr not in pctls:
            pctls[instr] = atr_pctl_fn(instr)
        pc = pctls[instr](t.value, float(r["atr_entry"])
                          if r["atr_entry"] not in ("", "None")
                          else None)
        out.append({"open_ts": r["open_ts"], "instrument": instr,
                    "points": float(r["points"]), "zone": zone,
                    "atr_pctl": pc,
                    "skipped_at_80": bool(pc is not None and pc > 80),
                    "skipped_at_95": bool(pc is not None and pc > 95)})
    return out


def run():
    rows = journal_rows()      # register 130: atr_pctl on every row
    strata = {}
    for r in rows:
        strata.setdefault((r["instrument"], r["variant"],
                           r["window"]), []).append(r)
    cells = {}
    for key, rr in sorted(strata.items()):
        for x in PAUSE_X:
            cells["|".join(key) + f"|{x}"] = pause_cell(rr, x)
    pctls = {}
    forensic = worst_forensic_rows(pctls)
    floors = {}
    for instr in ("uk100fut", "ger40fut", "nas100fut", "us30fut"):
        print(f"# vol_pause floors: {instr} ...", file=sys.stderr)
        floors[instr] = scalp_floor_bands(instr)
    return {"pause_x": list(PAUSE_X),
            "rows_ex_lockbox": len(rows),
            "cells": cells, "scalp_floors": floors,
            "worst_forensic": forensic}


def _emit(art, head):
    L = ["# Volatility-Pause Counterfactual (GENERATED by "
         "backtest.vol_pause)", "",
         "Terms: [docs/GLOSSARY.md](../../docs/GLOSSARY.md).", "",
         f"Engine `{head[:9]}` — OBSERVATIONAL, pre-registered "
         "(prereg_vol_pause, register 132; extends register 130). "
         "SEEING vs BELIEVING (the operator's ruling, the standing "
         "expectation for measurement builds): the change is VISIBLE "
         "here on all data at the next campaign; ENACTMENT BARS READ "
         "FORWARD — any pause still requires the register-130 forward/"
         "top-bucket evidence (unmeasurable at n=1-2 this emission; "
         "the sealed window accrues it). The counterfactual: journal "
         "rows replayed in strict fill order, entries SKIPPED at "
         f"atr_pctl > X, X in {list(PAUSE_X)} (the register-130 field "
         "verbatim; row-level per registers 102/103 — skipped = "
         "foregone, no resurrection of unblocked trades, stated). "
         "DISTINCT PATHS throughout (register 113). FLOORS: B-RANDOM "
         "members under the identical pause, SCALP ARMS ONLY (the "
         "evidence rows; the context ladder prints without floors — "
         "implementer-scoped, FLAGGED). NOTHING changes in any live "
         "recipe; a surviving cell proposes vol_gate(X) — a COMPOSABLE "
         "ENTRY-GATE component ratified onto specific variant x market "
         "combinations, NEVER cloned variants (the scoping ruling, "
         "register 132). Ex-lockbox; weekly under Part C.", "",
         "## Scalp arms — the evidence rows (net delta vs the member "
         "band; positive delta = the pause helped)", "",
         "| arm | leg | window | X | n (distinct) | skipped (share) | "
         "foregone wins | avoided losses | net Δ | member band med "
         "[min..max] (skip share) | beats band max | stops dodged "
         "(pts; worst) |",
         "|---|---|---|---|---|---|---|---|---|---|---|---|"]
    for key, c in art["cells"].items():
        instr, var, w, x = key.split("|")
        if var not in SCALP_ARMS:
            continue
        fb = art["scalp_floors"].get(instr, {}).get(var, {}) \
            .get(f"{w}|{x}")
        band = (f"{fb['median']} [{fb['min']}..{fb['max']}] "
                f"({fb['median_skip_share']})" if fb else "—")
        beats = ("YES" if fb and c["net_delta"] > fb["max"] else "no"
                 if fb else "—")
        L.append(f"| {var} | {instr} | {w} | {x} "
                 f"| {c['n']} ({c['n_distinct']}) "
                 f"| {c['skipped']} ({c['skip_share']}) "
                 f"| {c['foregone_win_pts']} | {c['avoided_loss_pts']} "
                 f"| {c['net_delta']:+.1f} | {band} | {beats} "
                 f"| {c['stops_dodged']} ({c['stops_dodged_pts']}; "
                 f"{c['worst_stop_dodged']}) |")
    L += ["", "## Context ladder (all arms; characterization — no "
          "floors here, stated; full grid in the JSON)", "",
          "| leg | variant | window | X | n (distinct) | skipped "
          "(share) | net Δ | stops dodged (pts) |",
          "|---|---|---|---|---|---|---|---|"]
    for key, c in art["cells"].items():
        instr, var, w, x = key.split("|")
        if var in SCALP_ARMS or c["skipped"] == 0:
            continue
        L.append(f"| {instr} | {var} | {w} | {x} "
                 f"| {c['n']} ({c['n_distinct']}) "
                 f"| {c['skipped']} ({c['skip_share']}) "
                 f"| {c['net_delta']:+.1f} "
                 f"| {c['stops_dodged']} ({c['stops_dodged_pts']}) |")
    L += ["", f"## The worst-{WORST_N} forensic rows (scalp-REF, all "
          "zones; lockbox rows DISPLAYED with their zone, never "
          "aggregated) — skip-set membership", "",
          "| open_ts | leg | points | zone | atr_pctl | skipped@80 | "
          "skipped@95 |", "|---|---|---|---|---|---|---|"]
    n80 = n95 = 0
    for r in art["worst_forensic"]:
        n80 += r["skipped_at_80"]
        n95 += r["skipped_at_95"]
        L.append(f"| {r['open_ts']} | {r['instrument']} "
                 f"| {r['points']:+.1f} | {r['zone']} | {r['atr_pctl']} "
                 f"| {'Y' if r['skipped_at_80'] else 'n'} "
                 f"| {'Y' if r['skipped_at_95'] else 'n'} |")
    L += ["", f"Skip-set coverage of the forensic: {n80}/{WORST_N} at "
          f"X=80, {n95}/{WORST_N} at X=95.", ""]
    with open(os.path.join(OUT, "vol_pause.md"), "w") as f:
        f.write("\n".join(L))


def main():
    ap = argparse.ArgumentParser()
    ap.parse_args()
    head = subprocess.run(["git", "rev-parse", "HEAD"], cwd=ROOT,
                          capture_output=True, text=True).stdout.strip()
    art = {"STAMP": ("OBSERVATIONAL volatility-pause counterfactual — "
                     "seeing now, believing on accrual; enactment bars "
                     "read forward; vol_gate composes, never clones; "
                     "never validation"),
           "engine_commit": head, **run()}
    with open(os.path.join(OUT, "vol_pause.json"), "w") as f:
        json.dump(art, f, indent=2, default=str)
    _emit(art, head)
    n80 = sum(1 for r in art["worst_forensic"] if r["skipped_at_80"])
    print(f"OBSERVATIONAL vol pause -> {OUT}/vol_pause.md "
          f"(forensic coverage {n80}/{WORST_N} at X=80)")


if __name__ == "__main__":
    main()
