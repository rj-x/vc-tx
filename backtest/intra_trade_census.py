"""In-trade narrative census (register 78; pre-registered
prereg_intra_trade_census). MEASUREMENT BEFORE MACHINERY, per the
flip-gate precedent: no narrative-management recipe registers until
this reports.

For every journal trade (reports/trades.csv — sentences + anchors,
the v0.3 incumbent and the v2 variants), classify OPPOSING narrative
events during the hold using the survey vocabulary (register 73):
  opposing-effort   — wide-loud bar closing against the trade;
  absorption-against— absorption-class bar (S0-H3 signature,
                      narrow-loud, TEST) during the hold;
  opposing-sentence — a MINTED COMPOSITE sentence firing opposite the
                      trade (register 82 amendment: composites only;
                      atoms stay in their own classes);
  trend-flip        — 1M phase flip (either direction; continuity);
  deceleration-against (register 95 item 1) — the third successive new
                      extreme in the position's direction whose leg
                      velocity declined strictly across three legs
                      (registered swing convention; INDICATOR-FREE —
                      the docketed source's RSI divergence is a proxy
                      for this quantity, recorded verbatim in the
                      trial log; three legs = the source's structure).
First event of each class per trade recorded; a trade may carry
several classes (classes are analysis splits, not a partition).

(a) CONDITIONAL OUTCOME — remaining excursion after the (first) event
    vs holds without that class, class-conditioned floors (B-RANDOM
    members under the INCUMBENT variant — the v1 floor; per-variant
    floors are a flagged follow-up), split EARLY-HOLD vs POST-ARMING
    (the flip-cut timing lesson; arming = the ratified R-FLIPGUARD
    transition: +1.0×ATR(15M) progress OR 45 min age, cited).
(b) COUNTERFACTUAL LEDGER — exit-at-event (event bar close, spread
    already inside the journal points) vs the actual outcome, same
    trades.
(c) THE REVERSE LEG, graded separately — each opposing event's
    hypothetical reverse trade under the same management vs the
    B-RANDOM floor; the flip trade (exit-and-reverse) EXISTS ONLY IF
    BOTH LEGS CLEAR.

Counts, dimming, both windows, all instruments; sealed/lockbox
excluded (inherited from the journal); twin-run pinned; weekly under
Part C. FILL MODEL: PESSIMISTIC (register 65; ladder family).
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

from engine.signal_watch import COMPOSITE_SENTENCES, SignalWatch
from engine.store_loader import lockbox_boundary, zones
from backtest.conditioning_matrix import quadrant_of
from backtest.recipes import (RECIPE_SET_VERSION, RECIPE_SETS,
                              _spread_median, build_env, simulate)
from backtest.scoreboard import (PROVISIONAL_INSTRS, PROVISIONAL_STAMP,
                                 _replay, event_derived_fires, make_cfg)
from backtest.signal_points import baseline_fires
from backtest.narrative_survey import _SurveyRecorder

OUT = os.path.join(ROOT, "reports", "scoreboard")
TRADES_CSV = os.path.join(ROOT, "reports", "trades.csv")

# register 82 amendment: the opposing-SENTENCE class means MINTED
# COMPOSITES ONLY (atoms stay in their own classes) — the sentence-
# warning's information content prints apart from the atomic noise
EVENT_CLASSES = ("opposing-effort", "absorption-against",
                 "opposing-sentence", "trend-flip",
                 "deceleration-against")   # register 95 item 1


class _SwingRecorder:
    """Register 95 item 1: the engine's confirmed swing registry as a
    confirmation-ordered log (confirm bar ts, type, idx, price) —
    trailing-confirmed, no lookahead. Feeds the decelerating-thrust
    class (indicator-free: per-leg velocity from the swing registry;
    the source's oscillator is a proxy for this quantity)."""

    def __init__(self):
        self.log = []
        self._seen = set()

    def attach(self, engine):
        orig = engine.exec_pipe.on_close
        ctx = engine.exec_pipe.ctx

        def observed(bar, ctx_tf=None, signal_ctx=None):
            out = orig(bar, ctx_tf=ctx_tf, signal_ctx=signal_ctx)
            if out is not None and not bar.is_stub:
                for sw in ctx.swings:
                    key = (sw["type"], sw["idx"])
                    if key not in self._seen:
                        self._seen.add(key)
                        self.log.append({"conf_ts": bar.ts.value,
                                         "type": sw["type"],
                                         "idx": sw["idx"],
                                         "price": float(sw["price"])})
            return out
        engine.exec_pipe.on_close = observed


def deceleration_flags(log, ts):
    """Per-bar flags: decel_up[j] / decel_dn[j] True at the confirmation
    bar of the THIRD successive new extreme in that direction whose leg
    velocity (|extreme - preceding opposite swing| / bars) declined
    strictly across the three legs. Three legs = the source's own
    structure, not a tuned number; legs = the registered swing
    convention. Deterministic."""
    n = len(ts)
    up, dn = np.zeros(n, bool), np.zeros(n, bool)
    hist = {"H": [], "L": []}          # all swings by type, in order
    runs = {"H": [], "L": []}          # successive new-extreme legs
    for sw in log:
        t = sw["type"]
        opp = [x for x in hist["L" if t == "H" else "H"]
               if x["idx"] < sw["idx"]]
        hist[t].append(sw)
        if not opp:
            continue
        o = opp[-1]
        bars = sw["idx"] - o["idx"]
        if bars <= 0:
            continue
        vel = abs(sw["price"] - o["price"]) / bars
        prev = hist[t][-2] if len(hist[t]) >= 2 else None
        new_ext = prev is None or (
            sw["price"] > prev["price"] if t == "H"
            else sw["price"] < prev["price"])
        if not new_ext:
            runs[t] = [vel]
            continue
        runs[t].append(vel)
        r = runs[t]
        if len(r) >= 3 and r[-1] < r[-2] < r[-3]:
            j = int(np.searchsorted(ts, sw["conf_ts"], side="right") - 1)
            if 0 <= j < n:
                (up if t == "H" else dn)[j] = True
    return up, dn
# arming split: the RATIFIED R-FLIPGUARD transition, cited (register 46)
ARM_PROGRESS_ATR = 1.0
ARM_AGE_MIN = 45


def build_arrays(instr):
    """Replay once: per-bar event arrays + fire stream + env."""
    cfg = make_cfg({"session_model.extended_hours": True,
                    "session_model.ladder": True,
                    "debug.structure": True})
    watch = SignalWatch()
    rec = _SurveyRecorder()
    swr = _SwingRecorder()

    def _hook(engine):
        watch.attach(engine)
        rec.attach(engine)
        swr.attach(engine)
    engine, bars, _ = _replay(cfg, instr, engine_hook=_hook)
    env = build_env(instr, cfg, bars)
    ts = env.ts
    decel_up, decel_dn = deceleration_flags(swr.log, ts)
    n = len(ts)
    getm = rec.map.get
    quad = np.array([quadrant_of(*getm(t, (None,) * 4)[:2],
                                 cfg.labels.wide_spread_pctile,
                                 cfg.labels.high_volume_mult)
                     if t in rec.map else "unclassified"
                     for t in ts], dtype=object)
    test_mask = np.array([getm(t, (None,) * 4)[3] == "TEST" for t in ts])
    closedir = np.sign(env.c - env.o).astype(int)
    flips = np.zeros(n, bool)
    prev = 0
    for e in engine.narrative.events:
        if e["type"] == "PHASE_EVAL" and e.get("tf") == "1min":
            t = e.get("trend", 0)
            if t != prev and t != 0:
                j = np.searchsorted(ts, pd.Timestamp(e["ts"]).value,
                                    side="right") - 1
                if 0 <= j < n:
                    flips[j] = True
            prev = t
    all_fires = watch.fires + event_derived_fires(
        engine.narrative.events, cfg, bars, instr=instr)
    fire_dir_by_bar = {}
    for f in all_fires:
        if f["name"] not in COMPOSITE_SENTENCES:
            continue                        # register 82: sentences only
        j = int(np.searchsorted(ts, f["ts"].value, side="right") - 1)
        fire_dir_by_bar.setdefault(j, set()).add(int(f["dir"]))
    h3_bars = {int(np.searchsorted(ts, f["ts"].value, side="right") - 1)
               for f in watch.fires if f["name"] == "S0-H3"}
    events = engine.narrative.events
    return {"env": env, "ts": ts, "quad": quad, "test": test_mask,
            "closedir": closedir, "flips": flips,
            "fires_by_bar": fire_dir_by_bar, "h3": h3_bars,
            "decel_up": decel_up, "decel_dn": decel_dn,
            "spread": _spread_median(instr), "events": events,
            "atr_at": lambda t_ns: env.atr_at("15min", t_ns)}


def classify_hold(A, i_entry, i_exit, d, entry, atr0):
    """First bar index of each opposing-event class inside the hold
    (i_entry, i_exit]; plus the arming bar (ratified transition)."""
    firsts = {}
    arm_bar = None
    fav = -np.inf
    for j in range(i_entry, min(i_exit + 1, len(A["ts"]))):
        fav = max(fav, (A["env"].h[j] - entry) if d == 1
                  else (entry - A["env"].l[j]))
        if arm_bar is None and atr0 and (
                fav >= ARM_PROGRESS_ATR * atr0
                or (A["ts"][j] - A["ts"][i_entry]) / 60e9 >= ARM_AGE_MIN):
            arm_bar = j
        if j == i_entry:
            continue                          # entry bar isn't a sequel
        wide_loud = A["quad"][j] == "wide-loud"
        if "opposing-effort" not in firsts and wide_loud \
                and A["closedir"][j] == -d:
            firsts["opposing-effort"] = j
        if "absorption-against" not in firsts and (
                j in A["h3"] or A["quad"][j] == "narrow-loud"
                or A["test"][j]):
            firsts["absorption-against"] = j
        if "opposing-sentence" not in firsts \
                and -d in A["fires_by_bar"].get(j, set()):
            firsts["opposing-sentence"] = j
        if "trend-flip" not in firsts and A["flips"][j]:
            firsts["trend-flip"] = j
        # register 95 item 1: the thrust in the position's favor
        # decelerating (third successive new extreme in d, velocities
        # strictly declining) — the trader's exit rule, measured
        if "deceleration-against" not in firsts and (
                A["decel_up"][j] if d == 1 else A["decel_dn"][j]):
            firsts["deceleration-against"] = j
    return firsts, arm_bar


def run_instrument(instr, journal):
    A = build_arrays(instr)
    ts = A["ts"]
    boundary, gl = lockbox_boundary(), zones()["go_live"]
    out = {"instrument": instr,
           "status": ("provisional" if instr in PROVISIONAL_INSTRS
                      else "canonical"),
           "cells": {}, "counterfactual": {}, "reverse_leg": {},
           "floors": {}}
    rows = [r for r in journal if r["instrument"] == instr]
    recs = []
    for r in rows:
        i_entry = int(np.searchsorted(
            ts, pd.Timestamp(r["open_ts"]).value, side="left"))
        i_exit = int(np.searchsorted(
            ts, pd.Timestamp(r["close_ts"]).value, side="left"))
        if i_entry >= len(ts):
            continue
        d = int(r["direction"])
        entry = float(r["open_price"])
        atr0 = (float(r["atr_entry"])
                if r.get("atr_entry") not in (None, "", "None") else None)
        firsts, arm_bar = classify_hold(A, i_entry, i_exit, d, entry,
                                        atr0)
        recs.append({"r": r, "i_entry": i_entry, "i_exit": i_exit,
                     "d": d, "entry": entry, "firsts": firsts,
                     "arm_bar": arm_bar})
    # B-RANDOM incumbent floor trades, classified identically (v1 floor)
    floor_recs = []
    recipe = RECIPE_SETS[RECIPE_SET_VERSION]["R-OP2"]
    for mf in baseline_fires(A["env"], A["events"])["B-RANDOM"]:
        for t in simulate(mf, A["env"], recipe, A["spread"]):
            i_entry = int(np.searchsorted(
                ts, pd.Timestamp(t["entry_ts"]).value, side="left"))
            i_exit = min(len(ts) - 1, i_entry
                         + int(t["duration_min"]))
            d = t["dir"]
            atr0 = A["atr_at"](pd.Timestamp(t["entry_ts"]).value)
            firsts, arm_bar = classify_hold(A, i_entry, i_exit, d,
                                            t["entry"], atr0)
            floor_recs.append({"pts": t["pts"], "d": d,
                               "entry": t["entry"], "i_entry": i_entry,
                               "i_exit": i_exit, "firsts": firsts,
                               "arm_bar": arm_bar})
    for w_lo, w_hi, wname in (
            (pd.Timestamp.min.tz_localize("UTC"), boundary, "backtest"),
            (gl, pd.Timestamp.max.tz_localize("UTC"), "forward")):
        wrecs = [x for x in recs
                 if w_lo <= pd.Timestamp(x["r"]["open_ts"]) < w_hi]
        for variant in sorted({x["r"]["variant"] for x in wrecs}):
            vrecs = [x for x in wrecs if x["r"]["variant"] == variant]
            for cls in EVENT_CLASSES:
                withe = [x for x in vrecs if cls in x["firsts"]]
                without = [x for x in vrecs if cls not in x["firsts"]]
                if not withe:
                    continue

                def rem(x):
                    j = x["firsts"][cls]
                    return x["d"] * (float(A["env"].c[x["i_exit"]])
                                     if x["i_exit"] < len(ts)
                                     else float(A["env"].c[-1])) \
                        - x["d"] * float(A["env"].c[j])
                rem_w = [rem(x) for x in withe]
                base_pts = [float(x["r"]["points"]) for x in without]
                early = [x for x in withe
                         if x["arm_bar"] is None
                         or x["firsts"][cls] < x["arm_bar"]]
                late = [x for x in withe
                        if x["arm_bar"] is not None
                        and x["firsts"][cls] >= x["arm_bar"]]
                # floors: B-RANDOM incumbent trades with the same class
                fl = [f["d"] * (float(A["env"].c[min(f["i_exit"],
                                                     len(ts) - 1)])
                                - float(A["env"].c[f["firsts"][cls]]))
                      for f in floor_recs if cls in f["firsts"]]
                # (b) counterfactual: exit at event close vs actual
                cf = [float(x["r"]["points"]) - (
                    x["d"] * (float(A["env"].c[x["firsts"][cls]])
                              - x["entry"]) - 0.0)
                    for x in withe]
                out["cells"]["|".join((variant, wname, cls))] = {
                    "n_with": len(withe), "n_without": len(without),
                    "remaining_median_pts": round(
                        float(np.median(rem_w)), 2),
                    "without_hold_median_pts": (round(
                        float(np.median(base_pts)), 2)
                        if base_pts else None),
                    "floor_remaining_median_pts": (round(
                        float(np.median(fl)), 2) if fl else None),
                    "early_n": len(early), "post_arming_n": len(late),
                    "early_remaining_median": (round(float(np.median(
                        [rem(x) for x in early])), 2) if early
                        else None),
                    "post_arming_remaining_median": (round(
                        float(np.median([rem(x) for x in late])), 2)
                        if late else None),
                    "counterfactual_actual_minus_exit_median": round(
                        float(np.median(cf)), 2)}
        # (c) reverse leg per class (incumbent management), graded vs
        # the B-RANDOM floor median of the SAME management
        rev_recipe = recipe
        for cls in EVENT_CLASSES:
            ev_fires = []
            for x in wrecs:
                if x["r"]["variant"] != "R-OP2" or cls not in x["firsts"]:
                    continue
                j = x["firsts"][cls]
                if j + 1 < len(ts):
                    ev_fires.append({"ts": pd.Timestamp(ts[j], tz="UTC"),
                                     "dir": -x["d"], "name": "REV"})
            if not ev_fires:
                continue
            rt = simulate(ev_fires, A["env"], rev_recipe, A["spread"])
            pts = [t["pts"] for t in rt]
            fl_pts = [f["pts"] for f in floor_recs]
            out["reverse_leg"]["|".join((wname, cls))] = {
                "n": len(pts),
                "median_pts": (round(float(np.median(pts)), 2)
                               if pts else None),
                "floor_median_pts": (round(float(np.median(fl_pts)), 2)
                                     if fl_pts else None),
                "both_legs_clear": None}    # filled at read: needs (a)
    return out


def _emit(results, head):
    L = ["# In-Trade Narrative Census (GENERATED by "
         "backtest.intra_trade_census)", "",
         "Terms: [docs/GLOSSARY.md](../../docs/GLOSSARY.md).", "",
         f"Engine `{head[:9]}` — OBSERVATIONAL, pre-registered "
         "(prereg_intra_trade_census, register 78). MEASUREMENT BEFORE "
         "MACHINERY (the flip-gate precedent): no narrative-management "
         "recipe registers until this reports. Event classes are "
         "ANALYSIS SPLITS, not a partition. Arming split cites the "
         "ratified R-FLIPGUARD transition (+1.0×ATR(15M) OR 45 min). "
         "Floors: B-RANDOM members under the INCUMBENT variant (v1 "
         "floor; per-variant floors flagged follow-up). The flip trade "
         "exists only if BOTH legs clear — reverse-leg medians print "
         "beside their floor. FILL MODEL: PESSIMISTIC. ° = n<20. "
         "deceleration-against (register 95): the docketed "
         "divergence exit measured indicator-free — third successive "
         "new extreme in the position's direction with strictly "
         "declining leg velocity (registered swing convention, no new "
         "thresholds); measured here BEFORE any standalone hypothesis.",
         ""]
    for res in results:
        inst = res["instrument"]
        L += [f"## {inst} ({res['status'].upper()})"]
        if res["status"] == "provisional":
            L += [f"> {PROVISIONAL_STAMP}"]
        L += ["", "| variant | window | event | n w/ | n w/o | remaining "
              "med (pts) | w/o-hold med | floor rem med | early rem "
              "| post-arm rem | actual−exit med |",
              "|---|---|---|---|---|---|---|---|---|---|---|"]
        for key in sorted(res["cells"]):
            variant, wname, cls = key.split("|")
            c = res["cells"][key]
            dim = "°" if c["n_with"] < 20 else ""
            L.append(f"| {variant} | {wname} | {cls} | {dim}"
                     f"{c['n_with']} | {c['n_without']} "
                     f"| {c['remaining_median_pts']} "
                     f"| {c['without_hold_median_pts']} "
                     f"| {c['floor_remaining_median_pts']} "
                     f"| {c['early_remaining_median']} "
                     f"| {c['post_arming_remaining_median']} "
                     f"| {c['counterfactual_actual_minus_exit_median']} "
                     f"|")
        if res["reverse_leg"]:
            L += ["", "| window | event | reverse n | reverse med pts "
                  "| floor med pts |", "|---|---|---|---|---|"]
            for key in sorted(res["reverse_leg"]):
                wname, cls = key.split("|")
                c = res["reverse_leg"][key]
                dim = "°" if (c["n"] or 0) < 20 else ""
                L.append(f"| {wname} | {cls} | {dim}{c['n']} "
                         f"| {c['median_pts']} | {c['floor_median_pts']} "
                         f"|")
        L.append("")
    with open(os.path.join(OUT, "intra_trade_census.md"), "w") as f:
        f.write("\n".join(L))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--instr", nargs="*",
                    default=["uk100fut", "ger40fut", "nas100fut", "us30fut"])
    a = ap.parse_args()
    os.makedirs(OUT, exist_ok=True)
    head = subprocess.run(["git", "rev-parse", "HEAD"], cwd=ROOT,
                          capture_output=True, text=True).stdout.strip()
    journal = list(csv.DictReader(l for l in open(TRADES_CSV) if not l.startswith("#")))
    results = []
    for instr in a.instr:
        print(f"# intra_trade_census: {instr} ...", file=sys.stderr)
        results.append(run_instrument(instr, journal))
    art = {"STAMP": ("OBSERVATIONAL in-trade narrative census — "
                     "measurement before machinery; never validation"),
           "engine_commit": head, "event_classes": list(EVENT_CLASSES),
           "arming": {"progress_atr": ARM_PROGRESS_ATR,
                      "age_min": ARM_AGE_MIN,
                      "cite": "R-FLIPGUARD ratified transition "
                              "(register 46)"},
           "results": results}
    with open(os.path.join(OUT, "intra_trade_census.json"), "w") as f:
        json.dump(art, f, indent=2, default=str)
    _emit(results, head)
    print(f"OBSERVATIONAL in-trade census -> "
          f"{OUT}/intra_trade_census.md")


if __name__ == "__main__":
    main()
