"""Circuit-breaker counterfactual (register 102; pre-registered
prereg_circuit_breaker, counted 2026-08-28). MEASUREMENT ONLY on the
scalp thread — EXPOSURE CONTROL, not harvest timing (register 64
distinguished: no time-based exit; the target is untouched).

On the scalp arms' ACTUAL journal rows (trades.csv; the plain and
refined-entry arms), replayed per instrument x arm in STRICT FILL ORDER
within each native trading day (the instrument's session-timezone
date): halt the rest of the day after k FULL-STOP exits (k in HALT_K)
or after N CONSECUTIVE LOSERS (N in HALT_N, the milder cousin). Per
rule x leg x arm x window: stops dodged (count, points saved) in the
halted remainder; targets and eod outcomes FORFEITED there (the
amputation line, priced from the actual foregone rows); net vs
no-halt; halt-day count and dates. BASELINES under identical rules:
B-RANDOM members simulated under each scalp recipe per instrument
(ex-lockbox), the same halt rules in the same order — member net-delta
bands beside every real cell (the module's one replay per instrument).
Motivating anatomy: the week-32 stop-cluster days (register 101).
Emits circuit_breaker.json before h6_refinement, which embeds the
section weekly. Any surviving rule proposes as a v1 arm COMPONENT
alongside the price-stop — one ratification package, front door;
nothing registers here. Twin-run pinned (tests/test_circuit_breaker.py).
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
from backtest.recipes import (RECIPE_SET_VERSION, RECIPE_SETS,
                              _spread_median, build_env, simulate)
from backtest.scoreboard import _replay, make_cfg
from backtest.signal_points import baseline_fires

OUT = os.path.join(ROOT, "reports", "scoreboard")
TRADES_CSV = os.path.join(ROOT, "reports", "trades.csv")

ARMS = ("R-SCALP-H" + str(6), "R-SCALP-H" + str(6) + "-REF")
HALT_K = (1, 2)              # order-stated: full-stop exits per day
HALT_N = (3, 5)              # order-stated: consecutive losers per day
STOP_REASONS = ("stop", "stop_gap")
REACH_REASONS = ("target", "target_gap")
INSTRUMENTS = ("uk100fut", "ger40fut", "nas100fut", "us30fut")


def rules():
    return ([(f"halt@{k}stops", "stops", k) for k in HALT_K]
            + [(f"halt@{n}losers", "losers", n) for n in HALT_N])


def local_day(ts, tz):
    return str(pd.Timestamp(ts).tz_convert(tz).date())


def apply_rule(day_rows, kind, thresh):
    """day_rows: [(points, exit_reason)] in strict fill order for one
    day. Returns the index at which the halt trips (rows from there on
    are foregone) or None. The tripping row itself is TAKEN (the halt
    starts after it)."""
    stops = consec = 0
    for i, (pts, reason) in enumerate(day_rows):
        if kind == "stops":
            if reason in STOP_REASONS:
                stops += 1
                if stops >= thresh:
                    return i + 1
        else:
            consec = consec + 1 if pts < 0 else 0
            if consec >= thresh:
                return i + 1
    return None


def replay(rows, tz):
    """rows: [(ts, points, exit_reason)] for one instrument x arm x
    window. Per rule: dodged/forfeited/net/halt days. Deterministic."""
    by_day = {}
    for ts, pts, reason in sorted(rows, key=lambda r: r[0]):
        by_day.setdefault(local_day(ts, tz), []).append((pts, reason))
    out = {}
    for name, kind, thresh in rules():
        agg = {"days": len(by_day), "halt_days": 0, "halt_dates": [],
               "stops_dodged": 0, "stops_dodged_pts": 0.0,
               "targets_forfeited": 0, "targets_forfeited_pts": 0.0,
               "eod_forfeited": 0, "eod_forfeited_pts": 0.0,
               "rows_foregone": 0, "net_delta": 0.0}
        for day, drows in sorted(by_day.items()):
            cut = apply_rule(drows, kind, thresh)
            if cut is None or cut >= len(drows):
                continue
            agg["halt_days"] += 1
            agg["halt_dates"].append(day)
            for pts, reason in drows[cut:]:
                agg["rows_foregone"] += 1
                agg["net_delta"] -= pts
                if reason in STOP_REASONS:
                    agg["stops_dodged"] += 1
                    agg["stops_dodged_pts"] += -pts
                elif reason in REACH_REASONS:
                    agg["targets_forfeited"] += 1
                    agg["targets_forfeited_pts"] += pts
                else:
                    agg["eod_forfeited"] += 1
                    agg["eod_forfeited_pts"] += pts
        for k in ("stops_dodged_pts", "targets_forfeited_pts",
                  "eod_forfeited_pts", "net_delta"):
            agg[k] = round(agg[k], 1)
        out[name] = agg
    return out


def journal_cells(tz_of):
    boundary, gl = lockbox_boundary(), zones()["go_live"]
    rows = {}
    for r in csv.DictReader(open(TRADES_CSV)):
        if r["variant"] not in ARMS or in_lockbox_span(r["open_ts"]):
            continue
        t = pd.Timestamp(r["open_ts"])
        w = "backtest" if t < boundary else "forward" if t >= gl else None
        if w is None:
            continue
        rows.setdefault((r["instrument"], r["variant"], w), []).append(
            (t, float(r["points"]), r["exit_reason"]))
    return {"|".join(k): replay(v, tz_of(k[0]))
            for k, v in sorted(rows.items())}


def baseline_bands(instr, tz):
    """B-RANDOM members under each scalp recipe, identical rules:
    per arm x window x rule, the member net-delta band."""
    cfg = make_cfg({"session_model.extended_hours": True,
                    "session_model.ladder": True,
                    "debug.structure": True})
    engine, bars, _ = _replay(cfg, instr)
    env = build_env(instr, cfg, bars)
    spread = _spread_median(instr)
    members = baseline_fires(env, engine.narrative.events)["B-RANDOM"]
    boundary, gl = lockbox_boundary(), zones()["go_live"]
    out = {}
    for arm in ARMS:
        recipe = RECIPE_SETS[RECIPE_SET_VERSION][arm]
        per_rule = {}
        for mf in members:
            trades = [t for t in simulate(mf, env, recipe, spread)
                      if not in_lockbox_span(t["entry_ts"])]
            for w, sel in (("backtest",
                            lambda t: pd.Timestamp(t["entry_ts"]) < boundary),
                           ("forward",
                            lambda t: pd.Timestamp(t["entry_ts"]) >= gl)):
                rows = [(pd.Timestamp(t["entry_ts"]), float(t["pts"]),
                         t["reason"]) for t in trades if sel(t)]
                rep = replay(rows, tz)
                for rule, agg in rep.items():
                    per_rule.setdefault((w, rule), []).append(
                        agg["net_delta"])
        out[arm] = {f"{w}|{rule}": {
            "members": len(v),
            "median": round(float(np.median(v)), 1),
            "min": round(float(min(v)), 1),
            "max": round(float(max(v)), 1)}
            for (w, rule), v in sorted(per_rule.items())}
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--instr", nargs="*", default=list(INSTRUMENTS))
    ap.add_argument("--no-baselines", action="store_true",
                    help="skip the member replay (tests / quick reads; "
                         "the artifact then states floors as absent)")
    a = ap.parse_args()
    import store as store_mod
    tz_of = lambda i: store_mod.SESSION_TZ.get(i, "Europe/London")
    head = subprocess.run(["git", "rev-parse", "HEAD"], cwd=ROOT,
                          capture_output=True, text=True).stdout.strip()
    cells = journal_cells(tz_of)
    floors = {}
    if not a.no_baselines:
        for instr in a.instr:
            print(f"# circuit_breaker baselines: {instr} ...",
                  file=sys.stderr)
            floors[instr] = baseline_bands(instr, tz_of(instr))
    art = {"STAMP": ("OBSERVATIONAL circuit-breaker counterfactual — "
                     "exposure control measured, never adopted; "
                     "surviving rules propose as v1 arm components via "
                     "the front door; never validation"),
           "engine_commit": head, "rules": [r[0] for r in rules()],
           "arms": list(ARMS), "day_convention": "native session-tz date",
           "register_64_note": ("exposure control, not harvest timing — "
                                "no time-based exit; target untouched"),
           "cells": cells, "floors": floors}
    with open(os.path.join(OUT, "circuit_breaker.json"), "w") as f:
        json.dump(art, f, indent=2, default=str)
    n_halt = sum(v["halt_days"] for c in cells.values()
                 for v in c.values())
    print(f"OBSERVATIONAL circuit breaker -> {OUT}/circuit_breaker.json "
          f"({len(cells)} cells, {n_halt} halt-days across rules; "
          f"floors {'present' if floors else 'ABSENT'})")


if __name__ == "__main__":
    main()
