"""R2 refinement experiment (register 57; design counted at register 56;
APPROVED to run 2026-08-22). OBSERVATIONAL, counted. Grades the FOUNDING
open question R2: does the execution-refinement micro-loop's entry
improvement pay for its spread burden?

IDENTICAL directional fires harvested twice under R-OP1's ratified stop
composition, honest fills, EOD-flat:
  ARM A (unrefined): entry at the next 1M bar's open after the fire.
  ARM B (refined):   the founding micro-loop — within execution.window
    (10) bars, trigger on a with-direction bar with close_pos beyond
    execution.close_pos_trigger (0.7); entry at the NEXT bar's open after
    the trigger; fallback ENTER at the window's end (founding fallback).
READOUT per signal x instrument x window: entry improvement in
stop-distance units (stop = 1.5 x ATR15 at the original fire — the
R-geometry gain), spread burden (spread as % of the signature stop and of
the exec-local stop = refined entry to the refinement window's adverse
extreme), net points A vs B (paired), counts everywhere. No recipe
changes flow without ratification.
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

from engine.config import load as load_cfg
from engine.signal_watch import AGNOSTIC_ROWS, SignalWatch
from engine.store_loader import is_sealed, lockbox_boundary, zones
from backtest.recipes import (RECIPE_SETS, RECIPE_SET_VERSION, build_env,
                              simulate, _spread_median)
from backtest.scoreboard import (PROVISIONAL_INSTRS, PROVISIONAL_STAMP,
                                 _replay, event_derived_fires, make_cfg)

OUT = os.path.join(ROOT, "reports", "scoreboard")


def refine(fires, env, window, cp_trigger):
    """Founding micro-loop over settled bars: returns arm-B pseudo-fires
    (fire bar = trigger bar, so simulate() enters at the next open) plus
    per-pair entry/exec-extreme bookkeeping."""
    ts, o, h, l, c = env.ts, env.o, env.h, env.l, env.c
    n = len(ts)
    out = []
    for f in sorted(fires, key=lambda x: x["ts"].value):
        i = np.searchsorted(ts, f["ts"].value, side="right") - 1
        if i < 0 or i + 2 >= n:
            continue
        d = f["dir"]
        trig = None
        for k in range(i + 1, min(i + 1 + window, n - 1)):
            with_dir = (c[k] > o[k]) if d == 1 else (c[k] < o[k])
            rng = h[k] - l[k]
            cp = (c[k] - l[k]) / rng if rng > 0 else 0.5
            if with_dir and (cp > cp_trigger if d == 1
                             else cp < 1 - cp_trigger):
                trig = k
                break
        if trig is None:
            trig = min(i + window, n - 2)          # founding fallback: enter
        sl = slice(i + 1, trig + 1)
        exec_ext = float(l[sl].min() if d == 1 else h[sl].max()) \
            if sl.start <= sl.stop - 1 else None
        out.append((f, {"ts": pd.Timestamp(ts[trig], tz="UTC"),
                        "dir": d, "name": f["name"]}, exec_ext))
    return out


def run_instrument(instr):
    cfg = make_cfg({"session_model.extended_hours": True,
                    "session_model.ladder": True})
    watch = SignalWatch()
    engine, bars, _ = _replay(cfg, instr, engine_hook=watch.attach)
    env = build_env(instr, cfg, bars)
    fires = watch.fires + event_derived_fires(engine.narrative.events, cfg,
                                              bars, instr=instr)
    fires = [f for f in fires
             if f["name"] not in AGNOSTIC_ROWS and not is_sealed(f["ts"])]
    spread = _spread_median(instr)
    base_cfg = load_cfg()
    window = int(base_cfg.execution.window)
    cp_trigger = float(base_cfg.execution.close_pos_trigger)
    recipe = RECIPE_SETS[RECIPE_SET_VERSION]["R-OP1"]
    boundary, gl = lockbox_boundary(), zones()["go_live"]
    pairs = refine(fires, env, window, cp_trigger)
    rows = {}
    names = sorted({f["name"] for f in fires})
    for name in names:
        sub = [p for p in pairs if p[0]["name"] == name]
        if not sub:
            continue
        trA = {t["fire_ts"]: t for t in simulate(
            [p[0] for p in sub], env, recipe, spread)}
        simB = simulate([p[1] for p in sub], env, recipe, spread)
        # net-points columns are per-arm sums over the window (one-position
        # blocking makes strict per-trade pairing lossy; the paired metric
        # is the entry-improvement column, computed per pair above)
        for w in ("backtest", "forward"):
            sel = [p for p in sub
                   if (p[0]["ts"] < boundary if w == "backtest"
                       else p[0]["ts"] >= gl)]
            imp, burdA, burdB, ptsA, ptsB = [], [], [], [], []
            for orig, pseudo, exec_ext in sel:
                a = trA.get(str(orig["ts"]))
                if a is None:
                    continue
                i = np.searchsorted(env.ts, pseudo["ts"].value,
                                    side="right") - 1
                if i + 1 >= len(env.ts):
                    continue
                d = orig["dir"]
                entryB = env.o[i + 1]
                a0 = env.atr_at("15min", env.ts[
                    np.searchsorted(env.ts, orig["ts"].value,
                                    side="right") - 1])
                if not a0:
                    continue
                stop_sig = 1.5 * a0
                imp.append(float((a["entry"] - entryB) * d) / stop_sig)
                burdA.append(100 * spread / stop_sig)
                if exec_ext is not None:
                    dloc = abs(entryB - exec_ext)
                    if dloc > 0:
                        burdB.append(100 * spread / dloc)
                ptsA.append(a["pts"])
            bt = [t["pts"] for t in simB
                  if (pd.Timestamp(t["fire_ts"]) < boundary
                      if w == "backtest"
                      else pd.Timestamp(t["fire_ts"]) >= gl)]
            if not imp and not bt:
                continue
            rows.setdefault(name, {})[w] = {
                "n_pairs": len(imp),
                "entry_improvement_stopunits": {
                    "median": round(float(np.median(imp)), 3),
                    "mean": round(float(np.mean(imp)), 3)} if imp else None,
                "spread_pct_of_signature_stop_median": (
                    round(float(np.median(burdA)), 1) if burdA else None),
                "spread_pct_of_exec_local_stop_median": (
                    round(float(np.median(burdB)), 1) if burdB else None),
                "net_pts_unrefined": round(float(np.sum(ptsA)), 1)
                if ptsA else None,
                "net_pts_refined": round(float(np.sum(bt)), 1)
                if bt else None,
                "n_refined_trades": len(bt)}
    return {"instrument": instr,
            "status": ("provisional" if instr in PROVISIONAL_INSTRS
                       else "canonical"),
            "spread_pts": spread, "rows": rows}


def _emit(results, head):
    L = ["# R2 Refinement Experiment (GENERATED; register 57)", "",
         f"Engine `{head[:9]}` — OBSERVATIONAL, counted (design register "
         "56; approved 2026-08-22). Identical fires, unrefined vs the "
         "founding refinement micro-loop, under R-OP1 stops. Entry "
         "improvement in signature-stop units; spread burden on both stop "
         "bases; net points paired. Grades founding open question R2.",
         ""]
    for res in results:
        inst = res["instrument"]
        L += [f"## {inst} ({res['status'].upper()}; spread "
              f"{res['spread_pts']} pts)"]
        if res["status"] == "provisional":
            L += [f"> {PROVISIONAL_STAMP}"]
        L += ["", "| signal | window | n | entry-imp med (stop-units) "
              "| spread% sig-stop | spread% exec-stop | net A (unref) "
              "| net B (ref) |",
              "|---|---|---|---|---|---|---|---|"]
        for name, per_w in sorted(res["rows"].items()):
            for w, v in per_w.items():
                ei = v["entry_improvement_stopunits"]
                L.append(
                    f"| {name} | {w} | {v['n_pairs']} "
                    f"| {ei['median'] if ei else '—'} "
                    f"| {v['spread_pct_of_signature_stop_median']} "
                    f"| {v['spread_pct_of_exec_local_stop_median']} "
                    f"| {v['net_pts_unrefined']} "
                    f"| {v['net_pts_refined']} ({v['n_refined_trades']}) |")
        L.append("")
    with open(os.path.join(OUT, "r2_experiment.md"), "w") as f:
        f.write("\n".join(L))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--instr", nargs="*",
                    default=["uk100fut", "ger40fut", "nas100fut", "us30fut"])
    a = ap.parse_args()
    os.makedirs(OUT, exist_ok=True)
    head = subprocess.run(["git", "rev-parse", "HEAD"], cwd=ROOT,
                          capture_output=True, text=True).stdout.strip()
    results = []
    for instr in a.instr:
        print(f"# r2_experiment: {instr} ...", file=sys.stderr)
        results.append(run_instrument(instr))
    art = {"STAMP": ("OBSERVATIONAL R2 experiment — counted; grades the "
                     "founding open question; never validation"),
           "engine_commit": head, "results": results}
    with open(os.path.join(OUT, "r2_experiment.json"), "w") as f:
        json.dump(art, f, indent=2, default=str)
    _emit(results, head)
    print(f"OBSERVATIONAL R2 experiment -> {OUT}/r2_experiment.md")


if __name__ == "__main__":
    main()
