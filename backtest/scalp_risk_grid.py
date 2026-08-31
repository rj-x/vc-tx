"""Scalp risk-grid v1 (register 103; pre-registered
prereg_scalp_risk_grid_v1, counted 2026-08-29). REFINEMENT PROGRAM
EXTENSION — measurement only; v0 (the registered scalp arm) UNTOUCHED.

(a) STOP LADDER — the scalp arms' journal fires (reconstructed from
    trades.csv rows: fire = open_ts - 1M; the refined arm's rows carry
    the transformed entry) RE-SIMULATED with the identical recipe
    engine under initial SL in STOP_RUNGS x ATR(15M); INCUMBENT_STOP is
    the reference and its re-simulation reconciles to the journal
    (printed). Per rung x instrument x arm x window: stops taken,
    reachers AMPUTATED (v0 reachers stopped under the rung), eod-drift
    changes, net vs v0; members under the same recipe at the same rung
    as the floor. The REACHER MAE DISTRIBUTION prints once per leg per
    arm — how much pain winners endure — the rung's principled read;
    register 101's v1 derivation is the standing arbiter when its
    sample measures.
(b) COOLDOWN LADDER — halt new entries for T in COOLDOWN_MIN after a
    full-stop exit; strict fill-order replay on the actual rows; stops
    dodged / targets forfeited / eod forfeited in-window, net vs
    no-cooldown; members with the identical replay as the floor. Beside
    it the MECHANISM CUT: net reach rate of fires arriving within T of
    a full-stop exit vs the arm's base rate — if post-stop fires reach
    at base, the ladder's verdict is pre-explained and no rung chains.
(c) FIELD HONESTY — the cell count in the header; glints listed never
    chained; >= CAND_MIN_LEGS-of-4 rule for any candidate; survivors
    propose JOINTLY with (or against) the register-101 derivation as one
    ratification package, front door. Twin-run pinned
    (tests/test_scalp_risk_grid.py). Weekly under Part C.
"""

import argparse
import copy
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
ENRICHED = os.path.join(ROOT, "reports", "trades_enriched.csv")

ARMS = ("R-SCALP-H" + str(6), "R-SCALP-H" + str(6) + "-REF")
STOP_RUNGS = (1.0, 1.5, 1.75)          # order-stated
INCUMBENT_STOP = 2.5                   # the registered disaster cap
COOLDOWN_MIN = (15, 30, 60, 120, 180, 240)   # order-stated
CAND_MIN_LEGS = 3                      # the >= 3-of-4 rule
STOP_REASONS = ("stop", "stop_gap")
REACH_REASONS = ("target", "target_gap")
INSTRUMENTS = ("uk100fut", "ger40fut", "nas100fut", "us30fut")


def with_stop(recipe, rung):
    """The scalp recipe with its initial stop re-rung (the target and
    everything else untouched)."""
    r = copy.deepcopy(recipe)
    for st in r["stages"]:
        st["stop"] = [("atr", rung, "15min") if c[0] == "atr" else c
                      for c in st["stop"]]
    return r


def journal_rows():
    boundary, gl = lockbox_boundary(), zones()["go_live"]
    out = {}
    for r in csv.DictReader(l for l in open(TRADES_CSV) if not l.startswith("#")):
        if r["variant"] not in ARMS or in_lockbox_span(r["open_ts"]):
            continue
        t = pd.Timestamp(r["open_ts"])
        w = "backtest" if t < boundary else "forward" if t >= gl else None
        if w is None:
            continue
        out.setdefault((r["instrument"], r["variant"]), []).append(
            {"open_ts": t, "close_ts": pd.Timestamp(r["close_ts"]),
             "window": w, "dir": int(r["direction"]),
             "pts": float(r["points"]), "reason": r["exit_reason"],
             "mae_atr": None})
    if os.path.exists(ENRICHED):
        idx = {}
        for r in csv.DictReader(open(ENRICHED)):
            if r["variant"] in ARMS and r["mae_atr"] not in ("", "None"):
                idx[(r["instrument"], r["variant"],
                     pd.Timestamp(r["open_ts"]).value)] = float(r["mae_atr"])
        for (instr, arm), rows in out.items():
            for row in rows:
                row["mae_atr"] = idx.get((instr, arm, row["open_ts"].value))
    return out


def fires_from_rows(rows):
    """Journal rows -> fire dicts the recipe engine enters at the next
    open: fire ts = open_ts - 1M (the trade layer's convention)."""
    return [{"ts": r["open_ts"] - pd.Timedelta(minutes=1),
             "dir": r["dir"], "name": "S0-H" + str(6)} for r in rows]


def stop_ladder_cell(v0, alt):
    """v0 and alt: dicts entry_ts -> (pts, reason) from simulate under
    the incumbent and the rung. Decomposition on the shared fires."""
    agg = {"n": 0, "stops_taken": 0, "stops_taken_pts": 0.0,
           "reachers_amputated": 0, "reachers_amputated_delta": 0.0,
           "eod_changed": 0, "eod_delta": 0.0, "net_delta": 0.0,
           "n_reachers_v0": 0}
    for k, (p0, r0) in v0.items():
        if k not in alt:
            continue
        p1, r1 = alt[k]
        agg["n"] += 1
        d = p1 - p0
        agg["net_delta"] += d
        if r0 in REACH_REASONS:
            agg["n_reachers_v0"] += 1
            if r1 in STOP_REASONS:
                agg["reachers_amputated"] += 1
                agg["reachers_amputated_delta"] += d
        if r1 in STOP_REASONS:
            agg["stops_taken"] += 1
            agg["stops_taken_pts"] += p1
        if r0 == "eod" and r1 != r0:
            agg["eod_changed"] += 1
            agg["eod_delta"] += d
    for key in ("stops_taken_pts", "reachers_amputated_delta",
                "eod_delta", "net_delta"):
        agg[key] = round(agg[key], 1)
    agg["reachers_amputated_share"] = (
        round(agg["reachers_amputated"] / agg["n_reachers_v0"], 3)
        if agg["n_reachers_v0"] else None)
    return agg


def reacher_mae(rows):
    m = [r["mae_atr"] for r in rows
         if r["reason"] in REACH_REASONS and r["mae_atr"] is not None]
    if len(m) < 10:
        return {"n": len(m), "note": "unmeasurable"}
    a = np.array(m)
    return {"n": len(a),
            **{f"p{q}": round(float(np.percentile(a, q)), 3)
               for q in (50, 75, 90, 95)},
            "share_breaching": {f"{r:g}": round(float(np.mean(a >= r)), 3)
                                for r in STOP_RUNGS}}


def cooldown_replay(rows, T_min):
    """Strict fill order: after a full-stop exit, fires opening before
    close_ts + T are foregone (priced from their actual rows)."""
    agg = {"n": len(rows), "foregone": 0, "stops_dodged": 0,
           "stops_dodged_pts": 0.0, "targets_forfeited": 0,
           "targets_forfeited_pts": 0.0, "eod_forfeited": 0,
           "eod_forfeited_pts": 0.0, "net_delta": 0.0}
    block_until = None
    T = pd.Timedelta(minutes=T_min)
    for r in sorted(rows, key=lambda x: x["open_ts"].value):
        if block_until is not None and r["open_ts"] < block_until:
            agg["foregone"] += 1
            agg["net_delta"] -= r["pts"]
            if r["reason"] in STOP_REASONS:
                agg["stops_dodged"] += 1
                agg["stops_dodged_pts"] += -r["pts"]
            elif r["reason"] in REACH_REASONS:
                agg["targets_forfeited"] += 1
                agg["targets_forfeited_pts"] += r["pts"]
            else:
                agg["eod_forfeited"] += 1
                agg["eod_forfeited_pts"] += r["pts"]
            continue
        if r["reason"] in STOP_REASONS:
            block_until = r["close_ts"] + T
    for key in ("stops_dodged_pts", "targets_forfeited_pts",
                "eod_forfeited_pts", "net_delta"):
        agg[key] = round(agg[key], 1)
    return agg


def mechanism_cut(rows, T_min):
    """Net reach rate of fires arriving within T of ANY full-stop exit
    vs the arm's base reach rate."""
    stops = sorted(r["close_ts"].value for r in rows
                   if r["reason"] in STOP_REASONS)
    T = T_min * 60_000_000_000
    post = []
    for r in rows:
        t = r["open_ts"].value
        j = np.searchsorted(stops, t, side="left") - 1
        post.append(j >= 0 and t - stops[j] <= T)
    reach = np.array([r["reason"] in REACH_REASONS for r in rows])
    post = np.array(post)
    base = round(float(reach.mean()), 3) if len(rows) else None
    n_post = int(post.sum())
    return {"n_post_stop": n_post, "base_reach": base,
            "post_stop_reach": (round(float(reach[post].mean()), 3)
                                if n_post else None),
            "delta_pp": (round(100 * (float(reach[post].mean()) - base), 1)
                         if n_post and base is not None else None)}


def run_instrument(instr, jr):
    cfg = make_cfg({"session_model.extended_hours": True,
                    "session_model.ladder": True,
                    "debug.structure": True})
    engine, bars, _ = _replay(cfg, instr)
    env = build_env(instr, cfg, bars)
    spread = _spread_median(instr)
    members = baseline_fires(env, engine.narrative.events)["B-RANDOM"]
    boundary, gl = lockbox_boundary(), zones()["go_live"]

    def win(t):
        t = pd.Timestamp(t)
        return ("backtest" if t < boundary else
                "forward" if t >= gl else None)

    def sim_map(fires, recipe):
        return {pd.Timestamp(t["entry_ts"]).value: (float(t["pts"]),
                                                    t["reason"], t)
                for t in simulate(fires, env, recipe, spread)
                if not in_lockbox_span(t["entry_ts"])}
    out = {"stop_ladder": {}, "reconciliation": {}, "reacher_mae": {},
           "cooldown": {}, "mechanism": {}, "floors": {}}
    for arm in ARMS:
        rows = jr.get((instr, arm), [])
        if not rows:
            continue
        recipe = RECIPE_SETS[RECIPE_SET_VERSION][arm]
        fires = fires_from_rows(rows)
        v0 = sim_map(fires, recipe)
        # reconciliation: the incumbent re-simulation vs the journal
        jmap = {r["open_ts"].value: r["pts"] for r in rows}
        diffs = [abs(v0[k][0] - jmap[k]) for k in jmap if k in v0]
        out["reconciliation"][arm] = {
            "journal_rows": len(rows), "resimulated": len(diffs),
            "max_abs_pts_diff": (round(max(diffs), 3) if diffs else None),
            "exact_matches": sum(1 for d in diffs if d < 1e-6)}
        for rung in STOP_RUNGS:
            alt = sim_map(fires, with_stop(recipe, rung))
            for w in ("backtest", "forward"):
                v0w = {k: v[:2] for k, v in v0.items()
                       if win(v[2]["entry_ts"]) == w}
                altw = {k: v[:2] for k, v in alt.items()}
                out["stop_ladder"][f"{arm}|{w}|{rung:g}"] = \
                    stop_ladder_cell(v0w, altw)
        out["reacher_mae"][arm] = {
            w: reacher_mae([r for r in rows if r["window"] == w])
            for w in ("backtest", "forward")}
        for w in ("backtest", "forward"):
            wrows = [r for r in rows if r["window"] == w]
            for T in COOLDOWN_MIN:
                out["cooldown"][f"{arm}|{w}|{T}"] = cooldown_replay(wrows, T)
                out["mechanism"][f"{arm}|{w}|{T}"] = mechanism_cut(wrows, T)
        # floors: members under the same recipe, same rung / cooldown
        fl_stop = {}
        fl_cool = {}
        for mf in members:
            m0 = sim_map(mf, recipe)
            mrows = [{"open_ts": pd.Timestamp(t["entry_ts"]),
                      "close_ts": pd.Timestamp(t["entry_ts"])
                      + pd.Timedelta(minutes=t["duration_min"]),
                      "window": win(t["entry_ts"]), "pts": float(t["pts"]),
                      "reason": t["reason"]} for _p, _r, t in m0.values()]
            for rung in STOP_RUNGS:
                malt = sim_map(mf, with_stop(recipe, rung))
                for w in ("backtest", "forward"):
                    m0w = {k: v[:2] for k, v in m0.items()
                           if win(v[2]["entry_ts"]) == w}
                    cell = stop_ladder_cell(m0w, {k: v[:2]
                                                  for k, v in malt.items()})
                    fl_stop.setdefault(f"{arm}|{w}|{rung:g}", []).append(
                        cell["net_delta"])
            for w in ("backtest", "forward"):
                mw = [r for r in mrows if r["window"] == w]
                for T in COOLDOWN_MIN:
                    fl_cool.setdefault(f"{arm}|{w}|{T}", []).append(
                        cooldown_replay(mw, T)["net_delta"])

        def band(v):
            return {"members": len(v),
                    "median": round(float(np.median(v)), 1),
                    "min": round(float(min(v)), 1),
                    "max": round(float(max(v)), 1)}
        out["floors"].update({f"stop|{k}": band(v)
                              for k, v in fl_stop.items()})
        out["floors"].update({f"cool|{k}": band(v)
                              for k, v in fl_cool.items()})
    return out


def candidates(results):
    """>= 3-of-4-leg rule on forward cells: net vs v0 (or vs no-cooldown)
    clearing the member band, same sign."""
    out = {}
    for ladder, prefix in (("stop_ladder", "stop"), ("cooldown", "cool")):
        keys = sorted({k for res in results.values()
                       for k in res[ladder] if "|forward|" in k})
        for k in keys:
            legs = {}
            for instr, res in results.items():
                c = res[ladder].get(k)
                fb = res["floors"].get(f"{prefix}|{k}")
                if not c or not fb:
                    continue
                nd = c["net_delta"]
                clear = (nd > fb["max"]) if nd > 0 else (nd < fb["min"])
                legs[instr] = {"net_delta": nd, "band": [fb["min"], fb["max"]],
                               "clears": bool(clear and nd != 0)}
            cl = {i: v for i, v in legs.items() if v["clears"]}
            signs = {np.sign(v["net_delta"]) for v in cl.values()}
            grade = ("candidate" if len(cl) >= CAND_MIN_LEGS
                     and len(signs) == 1 else "glint" if cl else "none")
            out[f"{ladder}|{k}"] = {"legs": legs, "clearing": sorted(cl),
                                    "grade": grade}
    return out


def _emit(art, head):
    n_cells = sum(len(r["stop_ladder"]) + len(r["cooldown"])
                  for r in art["results"].values())
    L = ["# Scalp Risk-Grid v1 (GENERATED by backtest.scalp_risk_grid)", "",
         "Terms: [docs/GLOSSARY.md](../../docs/GLOSSARY.md).", "",
         f"Engine `{head[:9]}` — OBSERVATIONAL, pre-registered "
         "(prereg_scalp_risk_grid_v1, register 103). Refinement-program "
         "extension; v0 UNTOUCHED; measurement only. FIELD HONESTY: "
         f"{n_cells} cells across both ladders (rungs x legs x arms x "
         "windows); single-leg glints listed never chained; a candidate "
         f"needs >= {CAND_MIN_LEGS} of 4 forward legs clearing its member "
         "band, same sign; any survivor proposes JOINTLY with (or "
         "against) the register-101 derivation as one ratification "
         "package — nothing registers here. STATISTIC SHAPES (74-B): "
         "per-cell net vs v0 (stop ladder) / vs no-cooldown (cooldown "
         "ladder) against B-RANDOM member bands under identical rules; "
         "the reacher-MAE curve and the mechanism cut are descriptive. "
         "The stop ladder RE-SIMULATES the arms' own fires with the "
         "recipe engine — the incumbent rung reconciles to the journal "
         "(printed per leg). Register 101's v1 derivation (p75 of forward "
         "non-reach MAE) is the standing arbiter when its sample "
         "measures.", ""]
    for instr, res in sorted(art["results"].items()):
        L += [f"## {instr}", "",
              "Reconciliation (incumbent re-simulation vs journal): "
              + "; ".join(f"{arm}: {v['exact_matches']}/{v['resimulated']} "
                          f"exact, max |Δ| {v['max_abs_pts_diff']}"
                          for arm, v in res["reconciliation"].items()), "",
              "### Stop ladder (net vs v0; floor = member band at the "
              "same rung)", "",
              "| arm | window | rung xATR | n | stops taken (pts) | "
              "reachers amputated (share, Δ) | eod changed (Δ) | net vs v0 "
              "| floor med (min..max) |", "|---|---|---|---|---|---|---|---|---|"]
        for k, c in res["stop_ladder"].items():
            arm, w, rung = k.split("|")
            fb = res["floors"].get(f"stop|{k}", {})
            fs = (f"{fb['median']} ({fb['min']}..{fb['max']})" if fb else "—")
            L.append(f"| {arm} | {w} | {rung} | {c['n']} "
                     f"| {c['stops_taken']} ({c['stops_taken_pts']}) "
                     f"| {c['reachers_amputated']} "
                     f"({c['reachers_amputated_share']}, "
                     f"{c['reachers_amputated_delta']}) "
                     f"| {c['eod_changed']} ({c['eod_delta']}) "
                     f"| {c['net_delta']:+.1f} | {fs} |")
        L += ["", "### Reacher MAE (xATR15) — how much pain winners "
              "endure", "",
              "| arm | window | n | p50 | p75 | p90 | p95 | share "
              "breaching 1.0 / 1.5 / 1.75 |", "|---|---|---|---|---|---|---|---|"]
        for arm, per in res["reacher_mae"].items():
            for w, m in per.items():
                if "note" in m:
                    L.append(f"| {arm} | {w} | {m['n']} | — | — | — | — | "
                             f"{m['note']} |")
                    continue
                sb = m["share_breaching"]
                L.append(f"| {arm} | {w} | {m['n']} | {m['p50']} | {m['p75']} "
                         f"| {m['p90']} | {m['p95']} | {sb['1']} / {sb['1.5']} "
                         f"/ {sb['1.75']} |")
        L += ["", "### Cooldown ladder (net vs no-cooldown; floor = member "
              "band under the identical replay) + the mechanism cut", "",
              "| arm | window | T min | n | foregone | stops dodged (pts) | "
              "targets forfeited (pts) | eod forfeited (pts) | net | floor "
              "med (min..max) | post-stop reach vs base (n) |",
              "|---|---|---|---|---|---|---|---|---|---|---|"]
        for k, c in res["cooldown"].items():
            arm, w, T = k.split("|")
            fb = res["floors"].get(f"cool|{k}", {})
            fs = (f"{fb['median']} ({fb['min']}..{fb['max']})" if fb else "—")
            m = res["mechanism"][k]
            mc = (f"{m['post_stop_reach']} vs {m['base_reach']} "
                  f"({m['delta_pp']:+.1f}pp, n={m['n_post_stop']})"
                  if m["delta_pp"] is not None else
                  f"— (n={m['n_post_stop']})")
            L.append(f"| {arm} | {w} | {T} | {c['n']} | {c['foregone']} "
                     f"| {c['stops_dodged']} ({c['stops_dodged_pts']}) "
                     f"| {c['targets_forfeited']} ({c['targets_forfeited_pts']}) "
                     f"| {c['eod_forfeited']} ({c['eod_forfeited_pts']}) "
                     f"| {c['net_delta']:+.1f} | {fs} | {mc} |")
        L.append("")
    L += ["## Candidates (>= 3-of-4 forward legs clearing the band, same "
          "sign) and glints", "",
          "| ladder | cell | grade | clearing legs |", "|---|---|---|---|"]
    for k, d in sorted(art["candidates"].items()):
        if d["grade"] == "none":
            continue
        L.append(f"| {k.split('|')[0]} | {'/'.join(k.split('|')[1:])} "
                 f"| {d['grade']} | {', '.join(d['clearing'])} |")
    if not any(d["grade"] != "none" for d in art["candidates"].values()):
        L.append("| (no cell clears its band on any forward leg) | | | |")
    L.append("")
    with open(os.path.join(OUT, "scalp_risk_grid.md"), "w") as f:
        f.write("\n".join(L))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--instr", nargs="*", default=list(INSTRUMENTS))
    ap.add_argument("--from-json", action="store_true",
                    help="re-emit the md from the stored JSON (layout "
                         "refresh; no replay)")
    a = ap.parse_args()
    head = subprocess.run(["git", "rev-parse", "HEAD"], cwd=ROOT,
                          capture_output=True, text=True).stdout.strip()
    if a.from_json:
        art = json.load(open(os.path.join(OUT, "scalp_risk_grid.json")))
        _emit(art, art["engine_commit"])
        print(f"risk-grid md re-emitted from JSON -> {OUT}")
        return
    jr = journal_rows()
    results = {}
    for instr in a.instr:
        print(f"# scalp_risk_grid: {instr} ...", file=sys.stderr)
        results[instr] = run_instrument(instr, jr)
    art = {"STAMP": ("OBSERVATIONAL scalp risk-grid v1 — measurement "
                     "only; v0 untouched; survivors propose jointly "
                     "with the register-101 derivation via the front "
                     "door; never validation"),
           "engine_commit": head, "stop_rungs": list(STOP_RUNGS),
           "incumbent_stop": INCUMBENT_STOP,
           "cooldown_min": list(COOLDOWN_MIN), "results": results}
    art["candidates"] = candidates(results)
    with open(os.path.join(OUT, "scalp_risk_grid.json"), "w") as f:
        json.dump(art, f, indent=2, default=str)
    _emit(art, head)
    n_c = sum(1 for d in art["candidates"].values()
              if d["grade"] == "candidate")
    print(f"OBSERVATIONAL scalp risk grid -> {OUT}/scalp_risk_grid.md "
          f"({n_c} candidates)")


if __name__ == "__main__":
    main()
