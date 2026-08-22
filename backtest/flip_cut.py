"""Post-flip continuation cut (register 43; pre-registered
prereg_post_flip_continuation_cut BEFORE computation). OBSERVATIONAL —
the RATIFICATION GATE for any flip-exit rule.

QUESTION, STATED: is the opposing 1M trend flip early enough that acting
on it beats the existing stops?

(a) For every flip-marked fire window: further adverse excursion from the
    flip's CONFIRMATION timestamp (settled 1M bar close) to the 60-min
    window end. Distributions per hypothesis x instrument.
(b) Counterfactual on the SAME trades: for each v0.1 recipe, each trade
    holding through an opposing flip — exit-at-flip (settled close of the
    flip bar, spread already charged in both legs) vs the actual
    hold-to-rule outcome. Flips confirming on the actual exit bar are
    EXCLUDED (the rule exit preceded confirmation — boundary convention in
    the pre-registration).

GATE: the narrative-exit values discussion convenes ONLY if (b) shows
exit-at-flip winning on real n. No recipe changes without ratification.
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

from engine.signal_watch import AGNOSTIC_ROWS, SignalWatch
from engine.store_loader import is_sealed, lockbox_boundary, zones
from backtest.excursions import WINDOW_NS, _dist, _narr_streams
from backtest.recipes import (RECIPE_SETS, RECIPE_SET_VERSION, build_env,
                              simulate, _spread_median)
from backtest.scoreboard import (PROVISIONAL_INSTRS, PROVISIONAL_STAMP,
                                 _replay, _series, event_derived_fires,
                                 make_cfg)

OUT = os.path.join(ROOT, "reports", "scoreboard")


def _first_opposing_flip(flips_ts, flips_dir, lo_ns, hi_ns, d):
    """First flip AGAINST direction d strictly inside (lo_ns, hi_ns)."""
    i = np.searchsorted(flips_ts, lo_ns, side="right")
    while i < len(flips_ts) and flips_ts[i] < hi_ns:
        if flips_dir[i] == -d:
            return flips_ts[i]
        i += 1
    return None


def run_instrument(instr):
    cfg = make_cfg({"session_model.extended_hours": True,
                    "session_model.ladder": True,
                    "debug.structure": True})       # flip confirmations
    watch = SignalWatch()
    engine, bars, _ = _replay(cfg, instr, engine_hook=watch.attach)
    env = build_env(instr, cfg, bars)
    ts, o, h, l, c = env.ts, env.o, env.h, env.l, env.c
    fires = watch.fires + event_derived_fires(engine.narrative.events, cfg, bars, instr=instr)
    fires = [f for f in fires
             if f["name"] not in AGNOSTIC_ROWS and not is_sealed(f["ts"])]
    narr = _narr_streams(engine.narrative.events, fires)
    flips = narr["trend_flip"]
    flips_ts = np.array([e[0] for e in flips])
    flips_dir = np.array([e[1] for e in flips])
    spread = _spread_median(instr)
    boundary, gl = lockbox_boundary(), zones()["go_live"]

    def window_of(t):
        return ("backtest" if t < boundary else
                "forward" if t >= gl else None)

    # ---- (a) further adverse excursion after flip confirmation
    part_a = {}
    for f in fires:
        i = np.searchsorted(ts, f["ts"].value, side="right") - 1
        if i < 0:
            continue
        end = np.searchsorted(ts, ts[i] + WINDOW_NS, side="right")
        ft = _first_opposing_flip(flips_ts, flips_dir, ts[i],
                                  ts[i] + WINDOW_NS, f["dir"])
        if ft is None or end <= i + 1:
            continue
        k = np.searchsorted(ts, ft, side="left")
        if k >= end or ts[k] != ft:
            continue
        d = f["dir"]
        ref = c[k]                          # price at flip confirmation
        sl = slice(k + 1, end)
        if sl.start >= sl.stop:
            further = 0.0
        else:
            further = float(max(0.0, (ref - l[sl].min()) if d == 1
                                else (h[sl].max() - ref)))
        w = window_of(f["ts"])
        if w:
            part_a.setdefault(w, {}).setdefault(
                f["name"], []).append(further)
    part_a = {w: {n: _dist(v) for n, v in per.items()}
              for w, per in part_a.items()}

    # ---- (b) counterfactual per recipe on the same trades
    part_b = {}
    rset = RECIPE_SETS[RECIPE_SET_VERSION]
    names = sorted({f["name"] for f in fires})
    for rname, recipe in rset.items():
        for hname in names:
            hf = [f for f in fires if f["name"] == hname]
            for t in simulate(hf, env, recipe, spread):
                d = t["dir"]
                e_ns = pd.Timestamp(t["entry_ts"]).value
                exit_ns = e_ns + int(t["duration_min"] * 60e9)
                # strictly before the exit bar's close (prereg convention)
                ft = _first_opposing_flip(flips_ts, flips_dir, e_ns,
                                          exit_ns, d)
                if ft is None:
                    continue
                k = np.searchsorted(ts, ft, side="left")
                if k >= len(ts) or ts[k] != ft:
                    continue
                cf_pts = round(float((c[k] - t["entry"]) * d - spread), 2)
                w = window_of(pd.Timestamp(t["entry_ts"]))
                if not w:
                    continue
                part_b.setdefault(w, {}).setdefault(rname, {}).setdefault(
                    hname, []).append(
                        {"actual": t["pts"], "cf": cf_pts,
                         "delta": round(cf_pts - t["pts"], 2)})
    b_summary = {}
    for w, per_r in part_b.items():
        for rname, per_h in per_r.items():
            for hname, rows in per_h.items():
                a = np.array([r["actual"] for r in rows])
                cf = np.array([r["cf"] for r in rows])
                dl = cf - a
                b_summary.setdefault(w, {}).setdefault(rname, {})[hname] = {
                    "n_flip_marked": len(rows),
                    "net_actual": round(float(a.sum()), 1),
                    "net_exit_at_flip": round(float(cf.sum()), 1),
                    "delta_net": round(float(dl.sum()), 1),
                    "delta_median": round(float(np.median(dl)), 2),
                    "flip_wins_pct": round(100 * float((dl > 0).mean()), 1)}
    return {"instrument": instr,
            "status": ("provisional" if instr in PROVISIONAL_INSTRS
                       else "canonical"),
            "spread_charged_pts": spread,
            "further_adverse_after_flip": part_a,
            "counterfactual": b_summary}


def _emit(results, head):
    L = ["# Post-Flip Continuation Cut (GENERATED by backtest.flip_cut)",
         "",
         f"Engine `{head[:9]}` — OBSERVATIONAL, pre-registered "
         "(prereg_post_flip_continuation_cut). THE QUESTION: is the "
         "opposing 1M trend flip early enough that acting on it beats the "
         "existing stops? GATE: the narrative-exit values discussion "
         "convenes only if the counterfactual shows exit-at-flip WINNING "
         "on real n. Spread charged on both legs; flips confirming on the "
         "exit bar excluded; sealed/lockbox excluded.", "",
         "**GATE RULED NOT PASSED for a universal flip-exit (operator, "
         "2026-08-19; register 44): net points is the deciding currency; "
         "home net negative both windows; the flip is a median manager "
         "and a tail amputator — incompatible with the excursion finding "
         "that only tails are harvestable. THIS ARTIFACT IS THE STANDING "
         "REFERENCE for why narrative exits must be stage-scoped. "
         "Per-hypothesis cherry-picks from these tables are a FORBIDDEN "
         "MOVE (post-hoc fitting on tiny cells).**", ""]
    for res in results:
        inst = res["instrument"]
        L += [f"## {inst} ({res['status'].upper()}; spread "
              f"{res['spread_charged_pts']} pts)"]
        if res["status"] == "provisional":
            L += [f"> {PROVISIONAL_STAMP}"]
        L.append("")
        for w in ("backtest", "forward"):
            pa = res["further_adverse_after_flip"].get(w)
            if pa:
                L += [f"### {inst} / {w} — (a) further adverse excursion "
                      f"AFTER flip confirmation (pts to window end)",
                      "", "| H | n | median | p75 | p90 |",
                      "|---|---|---|---|---|"]
                for hname, dist in sorted(pa.items()):
                    if dist:
                        L.append(f"| {hname.replace('S-', '')} "
                                 f"| {dist['n']} | {dist['median']} "
                                 f"| {dist['p75']} | {dist['p90']} |")
                L.append("")
            cf = res["counterfactual"].get(w)
            if cf:
                L += [f"### {inst} / {w} — (b) exit-at-flip vs "
                      f"hold-to-rule, same trades, net of spread",
                      "", "| recipe | H | n flip-marked | net actual "
                      "| net exit-at-flip | Δnet | Δmedian | flip wins |",
                      "|---|---|---|---|---|---|---|---|"]
                for rname, per_h in cf.items():
                    for hname, v in sorted(per_h.items()):
                        L.append(
                            f"| {rname} | {hname.replace('S-', '')} "
                            f"| {v['n_flip_marked']} | {v['net_actual']} "
                            f"| {v['net_exit_at_flip']} | {v['delta_net']} "
                            f"| {v['delta_median']} "
                            f"| {v['flip_wins_pct']}% |")
                L.append("")
    L += ["---", "", "Raw per-trade pairs in flip_cut.json (same run)."]
    with open(os.path.join(OUT, "flip_cut.md"), "w") as f:
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
        print(f"# flip_cut: {instr} ...", file=sys.stderr)
        results.append(run_instrument(instr))
    art = {"STAMP": ("OBSERVATIONAL post-flip continuation cut — "
                     "pre-registered; the flip-exit ratification gate; "
                     "never validation"),
           "engine_commit": head, "results": results}
    with open(os.path.join(OUT, "flip_cut.json"), "w") as f:
        json.dump(art, f, indent=2, default=str)
    _emit(results, head)
    print(f"OBSERVATIONAL flip cut -> {OUT}/flip_cut.md")


if __name__ == "__main__":
    main()
