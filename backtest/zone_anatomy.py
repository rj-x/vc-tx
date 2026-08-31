"""Arrival anatomy — does the tape's character change at higher-TF
structure? (register 114; pre-registered prereg_zone_anatomy, counted
2026-08-30; the zone-census-v3 addendum, emitted in the same weekly
Part C slot). OBSERVATIONAL.

PURPOSE (the order's line): tests the v3 zones' MECHANISM independently
of signal conditioning — if anatomy is flat in-zone, v3's conditioning
nulls are pre-explained; if anatomy shifts, the shifts are hypothesis
material through the front door. Nothing minted here.

THE POPULATIONS: every v3 zone as emitted at the ANCHOR departure
multiple (x1.5 — the loosest rung; a x3 departure is a x1.5 departure
at the same base, so the anchor set carries the anatomy; per-mult
anatomy is a re-registration if ever wanted). H4-primary; the sparse
D1 zones included with register 111's starvation verdict standing (
1-6 zones/leg, 0.0% in-zone D1 bars — their cells print unmeasurable).
1M closes tagged in-zone (the base's range) / out-of-zone; bars inside
the OTHER side's zones belong to neither population.

THE BASE (register-47 method): out-of-zone bars, SESSION-STANDARDIZED
to the in-zone bars' session mix (per-session statistic over the out
population, weighted by the in population's session shares) — and the
per-bar features are ALREADY time-of-day matched by the engine's
tod-binned baselines (rel_volume = multiple of the tod-bin mean;
rel_spread_pct = percentile within the tod bin), so "same session,
time-matched" holds at both levels.

THE METRICS, per source-TF x leg x zone-side x window:
(a) rel_volume median + loud-bar rate (rel_volume >= LOUD_MULT);
(b) spread percentile median + the effort x result quadrant's
    narrow-loud share (the absorption fingerprint);
(c) velocity into / out of the zone — points per context-bar by
    swing leg (the register-95 deceleration-class machinery relocated
    to a location): a leg ARRIVES when its confirmation bar is in-zone
    and the prior leg's was not; DEPARTS when out following in;
(d) VSA label rates per 100 measured bars: TEST / ND / NS / climax;
(e) reversal-print clustering: 1M phase-flip rate per 100 bars (the
    registered flip idiom — a flip requires the new trend nonzero).

LUCK: per cell, in/out labels permuted within session strata (100
pinned seeds), two-sided — |shift| vs the null's |shift|; significant
above the null p95. CLAIMS need >= 3 of 4 legs same-signed significant
on the identical cell axis. SINGLE-LEG findings route to the
per-market WATCH page wearing a SELECTION-NULL: the leg's whole
anatomy field's best fake per seed (max |fake shift| / cell p95),
listed, never rules. Measurability: ANATOMY_MIN_BARS per bar cell /
ANATOMY_MIN_LEGS per leg cell (implementer-proposed, FLAGGED).
Ex-lockbox by window construction; sealed bars excluded; twin-run
pinned (tests/test_zone_anatomy.py). Weekly under Part C with v3.
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

from engine.store_loader import is_sealed, lockbox_boundary, zones
from backtest.scoreboard import _replay, make_cfg
from backtest.conditioning_matrix import quadrant_of
from backtest.narrative_survey import _SurveyRecorder
from backtest.intra_trade_census import _SwingRecorder
from backtest.underwater_census import LOUD_MULT
from backtest.sessions import sessions_of_index
from backtest.per_market_watch import NULL_SEEDS
from backtest.zone_census_v3 import (DEPART_MULTS, SOURCE_TFS,
                                     departure_bases, source_frame,
                                     tag_bars_v3)

OUT = os.path.join(ROOT, "reports", "scoreboard")

ANATOMY_MIN_BARS = 100   # bar-cell measurability — implementer-proposed
                         # at prereg, FLAGGED (a session-hour of 1M bars)
ANATOMY_MIN_LEGS = 25    # leg-cell measurability — the trade convention's
                         # count reused, FLAGGED
CLAIM_MIN_LEGS = 3       # the >= 3-of-4-leg replication bar (standing)

# (name, kind, unit): kind 'median' | 'share' (x100) | leg metrics apart
BAR_METRICS = (
    ("rel_volume_median", "median", "x tod-normal"),
    ("loud_rate", "share", "% bars"),
    ("spread_pctile_median", "median", "pctile"),
    ("narrow_loud_share", "share", "% classified"),
    ("test_rate", "share", "per 100 bars"),
    ("nd_rate", "share", "per 100 bars"),
    ("ns_rate", "share", "per 100 bars"),
    ("climax_rate", "share", "per 100 bars"),
    ("phase_flip_rate", "share", "per 100 bars"),
    # register 119 (organ #4 — the anatomy (a)/(b) customer): raw
    # signed-volume medians; the axis (tf x side x window) keeps sign
    # semantics consistent within any claim
    ("svol15_median", "median", "signed vol"),
    ("svol_sess_median", "median", "signed vol"),
)
LEG_METRICS = (("velocity_arriving", "pts/bar"),
               ("velocity_departing", "pts/bar"))


def _stat(kind, vals):
    if not len(vals):
        return None
    if kind == "median":
        return float(np.median(vals))
    return 100.0 * float(np.mean(vals))


def std_base(kind, vals, valid, out_mask, sess_codes, weights):
    """Register-47 base: per-session statistic over the OUT population,
    weighted by the IN population's session shares. Sessions with no
    valid out bars are dropped and the weights renormalized (the count
    of matched sessions travels with the cell)."""
    num = den = 0.0
    matched = 0
    for s, w in weights.items():
        m = out_mask & valid & (sess_codes == s)
        if not m.any():
            continue
        num += w * _stat(kind, vals[m])
        den += w
        matched += 1
    return (num / den if den else None), matched


def cell_shift(kind, vals, valid, in_mask, out_mask, sess_codes):
    """(in_value, base_value, shift, weights) for one metric/cell."""
    iv = in_mask & valid
    if not iv.any():
        return None, None, None, {}
    codes, counts = np.unique(sess_codes[iv], return_counts=True)
    weights = {c: n / counts.sum() for c, n in zip(codes, counts)}
    in_val = _stat(kind, vals[iv])
    base, matched = std_base(kind, vals, valid, out_mask, sess_codes,
                             weights)
    if base is None:
        return in_val, None, None, weights
    return in_val, base, in_val - base, weights


def perm_null(kind, vals, valid, in_mask, out_mask, sess_codes):
    """Two-sided permutation null: in/out labels shuffled within
    session strata (pinned seeds); the fake |shift| distribution."""
    universe = (in_mask | out_mask)
    strata = {}
    for s in np.unique(sess_codes[universe & valid]):
        idxs = np.nonzero(universe & valid & (sess_codes == s))[0]
        n_in = int((in_mask & valid & (sess_codes == s)).sum())
        strata[s] = (idxs, n_in)
    fakes = []
    for seed in NULL_SEEDS:
        rs = np.random.RandomState(seed)
        fin = np.zeros(len(vals), dtype=bool)
        for idxs, n_in in strata.values():
            if n_in and len(idxs):
                pick = rs.choice(len(idxs), size=min(n_in, len(idxs)),
                                 replace=False)
                fin[idxs[pick]] = True
        fout = universe & valid & ~fin
        _iv, _b, sh, _w = cell_shift(kind, vals, valid, fin, fout,
                                     sess_codes)
        fakes.append(np.nan if sh is None else abs(sh))
    return np.array(fakes, dtype=float)


def legs_from_log(log):
    """Swing legs from the register-95 machinery: consecutive
    opposite-type swings; velocity = |dprice| / context-bars; leg
    positioned at its END swing's confirmation bar."""
    out = []
    last = {"H": None, "L": None}
    for sw in sorted(log, key=lambda s: (s["conf_ts"], s["idx"])):
        o = last["L" if sw["type"] == "H" else "H"]
        if o is not None and sw["idx"] > o["idx"]:
            out.append({"conf_ts": sw["conf_ts"],
                        "velocity": abs(sw["price"] - o["price"])
                        / (sw["idx"] - o["idx"])})
        last[sw["type"]] = sw
    return out


def leg_zone_flags(legs, ts, state):
    """Per leg: (bar j of confirmation, in-zone at j, arriving,
    departing) — arriving = in after the prior leg's out; departing =
    out after the prior leg's in."""
    out = []
    prev_in = False
    for lg in legs:
        j = int(np.searchsorted(ts, lg["conf_ts"], side="right") - 1)
        if j < 0 or j >= len(ts):
            continue
        cur = bool(state[j])
        out.append({"j": j, "in": cur, "velocity": lg["velocity"],
                    "arriving": cur and not prev_in,
                    "departing": (not cur) and prev_in})
        prev_in = cur
    return out


def prepare_instrument(instr):
    """One replay: per-1M-bar feature arrays + swing legs + windows."""
    cfg = make_cfg({"session_model.extended_hours": True,
                    "session_model.ladder": True,
                    "debug.structure": True})
    rec = _SurveyRecorder()
    swr = _SwingRecorder()

    def _hook(engine):
        rec.attach(engine)
        swr.attach(engine)
    engine, bars, _ = _replay(cfg, instr, engine_hook=_hook)
    b1m = [x for x in bars[cfg.mtf.execution_tf] if not x.is_stub]
    ts = np.array([x.ts.value for x in b1m])
    cl = np.array([x.close for x in b1m])
    op = np.array([x.open for x in b1m])
    vol = np.array([x.volume for x in b1m], dtype=float)
    n = len(ts)
    getm = rec.map.get
    measured = np.array([t in rec.map for t in ts])
    rs_ = np.array([(getm(t, (None,) * 4)[0] or np.nan)
                    if t in rec.map else np.nan for t in ts], dtype=float)
    rv = np.array([(getm(t, (None,) * 4)[1] or np.nan)
                   if t in rec.map else np.nan for t in ts], dtype=float)
    wide_p = float(cfg.labels.wide_spread_pctile)
    quad = np.array([quadrant_of(*getm(t, (None,) * 4)[:2], wide_p,
                                 LOUD_MULT) if t in rec.map
                     else "unmeasured" for t in ts], dtype=object)
    structural = np.array([getm(t, (None,) * 4)[2] if t in rec.map
                           else None for t in ts], dtype=object)
    qualified = np.array([getm(t, (None,) * 4)[3] if t in rec.map
                          else None for t in ts], dtype=object)
    # the registered flip idiom (a flip requires the new trend nonzero)
    flips = np.zeros(n, dtype=bool)
    prev = 0
    for e in engine.narrative.events:
        if e["type"] == "PHASE_EVAL" and e.get("tf") == "1min":
            t = e.get("trend", 0)
            if t != prev and t != 0:
                j = int(np.searchsorted(ts, pd.Timestamp(e["ts"]).value,
                                        side="right") - 1)
                if 0 <= j < n:
                    flips[j] = True
            prev = t
    sess = np.array(sessions_of_index(
        pd.DatetimeIndex(pd.to_datetime(ts, utc=True))), dtype=object)
    boundary, gl = lockbox_boundary(), zones()["go_live"]
    days = pd.DatetimeIndex(pd.to_datetime(ts, utc=True)).normalize()
    sealed_days = {d: bool(is_sealed(pd.Timestamp(d)))
                   for d in days.unique()}
    unsealed = ~np.array([sealed_days[d] for d in days])
    wmask = {"backtest": (ts < boundary.value) & unsealed,
             "forward": (ts >= gl.value) & unsealed}
    legs = legs_from_log(swr.log)
    from backtest.signed_volume import sv15 as _sv15, sv_session
    return {"instr": instr, "cfg": cfg, "ts": ts, "cl": cl,
            "measured": measured, "rs": rs_, "rv": rv, "quad": quad,
            "structural": structural, "qualified": qualified,
            "flips": flips, "sess": sess, "wmask": wmask, "legs": legs,
            "sv15": _sv15(op, cl, vol),
            "sv_sess": sv_session(op, cl, vol, ts)}


def bar_metric_arrays(P):
    """(vals, valid) per bar metric — denominators stated per family."""
    m = P["measured"]
    classified = m & (P["quad"] != "unclassified")
    return {
        "rel_volume_median": (P["rv"], m & ~np.isnan(P["rv"])),
        "loud_rate": ((P["rv"] >= LOUD_MULT).astype(float),
                      m & ~np.isnan(P["rv"])),
        "spread_pctile_median": (P["rs"], m & ~np.isnan(P["rs"])),
        "narrow_loud_share": ((P["quad"] == "narrow-loud").astype(float),
                              classified),
        "test_rate": ((P["qualified"] == "TEST").astype(float), m),
        "nd_rate": ((P["structural"] == "NO_DEMAND").astype(float), m),
        "ns_rate": ((P["structural"] == "NO_SUPPLY").astype(float), m),
        "climax_rate": (np.isin(P["structural"],
                                ("SELLING_CLIMAX", "BUYING_CLIMAX"))
                        .astype(float), m),
        "phase_flip_rate": (P["flips"].astype(float),
                            np.ones(len(P["ts"]), dtype=bool)),
        "svol15_median": (P["sv15"],
                          np.ones(len(P["ts"]), dtype=bool)),
        "svol_sess_median": (P["sv_sess"],
                             np.ones(len(P["ts"]), dtype=bool)),
    }


def leg_cells(P, state, win_mask):
    """(c) velocity into/out of the zone vs the out-leg base,
    session-standardized at the leg's confirmation bar."""
    flags = leg_zone_flags(P["legs"], P["ts"], state)
    flags = [f for f in flags if win_mask[f["j"]]]
    if not flags:
        return {}
    vel = np.array([f["velocity"] for f in flags])
    sessc = np.array([P["sess"][f["j"]] for f in flags], dtype=object)
    valid = np.ones(len(flags), dtype=bool)
    outm = np.array([not f["in"] and not f["departing"] for f in flags])
    cells = {}
    for name, sel in (("velocity_arriving",
                       np.array([f["arriving"] for f in flags])),
                      ("velocity_departing",
                       np.array([f["departing"] for f in flags]))):
        in_val, base, shift, _w = cell_shift("median", vel, valid, sel,
                                             outm, sessc)
        null = perm_null("median", vel, valid, sel, outm, sessc)
        cells[name] = _cell_result("median", "pts/bar", int(sel.sum()),
                                   int(outm.sum()), in_val, base, shift,
                                   null, ANATOMY_MIN_LEGS)
    return cells


def _cell_result(kind, unit, in_n, out_n, in_val, base, shift, null,
                 min_n):
    valid_null = null[~np.isnan(null)]
    p95 = (float(np.percentile(valid_null, 95)) if len(valid_null)
           else None)
    pct = (round(100 * float(np.mean(valid_null < abs(shift))), 1)
           if shift is not None and len(valid_null) else None)
    measurable = in_n >= min_n and shift is not None
    return {"unit": unit, "in_n": in_n, "out_n": out_n,
            "in_value": None if in_val is None else round(in_val, 3),
            "base_value": None if base is None else round(base, 3),
            "shift": None if shift is None else round(shift, 3),
            "null_p95_abs": None if p95 is None else round(p95, 3),
            "pct_vs_null": pct,
            "null_valid_seeds": int(len(valid_null)),
            "significant": bool(measurable and p95 is not None
                                and abs(shift) > p95),
            "measurable": bool(measurable)}


def run_instrument(P, frames):
    """All cells for one instrument + the selection-null seed maxima:
    every measurable bar-metric cell's per-seed |fake shift| / its own
    null p95, elementwise-maxed over the leg's whole field (pinned
    seeds align by index). Leg metrics wear their own nulls only —
    they do not enter the selection field (stated)."""
    k = int(P["cfg"].context.swing_k)
    period = int(P["cfg"].context.atr_period)
    marrays = bar_metric_arrays(P)
    out = {"instrument": P["instr"], "cells": {}}
    ratio_stack = []
    for tf in SOURCE_TFS:
        zs = departure_bases(frames[tf], k, period, DEPART_MULTS[0])
        zid = tag_bars_v3(P["ts"], P["cl"], zs)
        side_of = np.array([zs[z]["type"] if z >= 0 else ""
                            for z in zid], dtype=object)
        state_any = zid >= 0
        for side in ("D", "S"):
            in_side = side_of == side
            for w, wm in P["wmask"].items():
                key = f"{tf}|{side}|{w}"
                cells = {}
                in_mask = in_side & wm
                out_mask = (~state_any) & wm
                days = (P["ts"] // 86_400_000_000_000).astype(int)
                in_zones = int(len(np.unique(zid[in_mask]))) \
                    if in_mask.any() else 0
                in_days = int(len(np.unique(days[in_mask]))) \
                    if in_mask.any() else 0
                for name, kind, unit in BAR_METRICS:
                    vals, valid = marrays[name]
                    in_val, base, shift, _wts = cell_shift(
                        kind, vals, valid, in_mask, out_mask, P["sess"])
                    null = perm_null(kind, vals, valid, in_mask,
                                     out_mask, P["sess"])
                    c = _cell_result(
                        kind, unit, int((in_mask & valid).sum()),
                        int((out_mask & valid).sum()), in_val, base,
                        shift, null, ANATOMY_MIN_BARS)
                    # HONESTY (the 1M label-study autocorrelation
                    # caveat): n is BARS; bars cluster within zone
                    # visits — the shuffle treats them as exchangeable,
                    # so per-cell significance is OVERSTATED; the
                    # distinct zone/day counts travel with the cell and
                    # the 3-of-4-leg rule is the real guard
                    c["in_zones"] = in_zones
                    c["in_days"] = in_days
                    cells[name] = c
                    if c["measurable"] and c["null_p95_abs"]:
                        ratio_stack.append(null / c["null_p95_abs"])
                # (c) legs: arrival/departure on this side's zones
                cells.update(leg_cells(P, in_side, wm))
                out["cells"][key] = cells
    seed_maxes = (np.nanmax(np.vstack(ratio_stack), axis=0).tolist()
                  if ratio_stack else [])
    return out, seed_maxes


def _emit(art, head):
    L = ["# Arrival Anatomy — tape character at v3 zones (GENERATED by "
         "backtest.zone_anatomy)", "",
         "Terms: [docs/GLOSSARY.md](../../docs/GLOSSARY.md).", "",
         f"Engine `{head[:9]}` — OBSERVATIONAL, pre-registered "
         "(prereg_zone_anatomy, register 114; the zone-census-v3 "
         "addendum, same weekly slot). PURPOSE: tests the zones' "
         "mechanism independently of signal conditioning — if anatomy "
         "is flat in-zone, v3's conditioning nulls are pre-explained; "
         "if anatomy shifts, the shifts are hypothesis material "
         "through the front door. Zones = the v3 anchor rung (x"
         f"{DEPART_MULTS[0]:g}; a x{DEPART_MULTS[1]:g} departure is an "
         "anchor departure at the same base). D1 included with the "
         "register-111 starvation verdict standing (cells print "
         "unmeasurable). BASE (register-47 method): out-of-zone bars "
         "session-standardized to the in-zone session mix; rel_volume "
         "and spread percentile are tod-matched by the engine "
         "baseline already. STATISTIC SHAPES (74-B): per-cell shift "
         "vs a two-sided in/out permutation null (100 pinned seeds, "
         "within-session); claims need >= "
         f"{CLAIM_MIN_LEGS}-of-4 legs same-signed significant; "
         "single-leg findings route to per_market_watch.md wearing a "
         "selection-null. Measurable at >= "
         f"{ANATOMY_MIN_BARS} in-zone bars / {ANATOMY_MIN_LEGS} legs "
         "(implementer-proposed, FLAGGED). **HONESTY — the 1M "
         "label-study autocorrelation caveat: n counts BARS, and bars "
         "cluster within zone visits (the distinct zone/day counts "
         "print beside n); the permutation null treats bars as "
         "exchangeable, so per-cell significance is OVERSTATED by "
         "construction — a cell fed by one or two zones describes "
         "those days, not zones in general. The 3-of-4-leg rule is "
         "the real guard.** Ex-lockbox; sealed bars excluded. "
         "MINT-ON-LIFT ONLY.", ""]
    for res in art["results"]:
        L += [f"## {res['instrument']}", "",
              "| tf | side | window | metric | in n (zones/days) | in "
              "| matched base | shift | null p95 (abs) | pct vs null "
              "| significant |",
              "|---|---|---|---|---|---|---|---|---|---|---|"]
        thin = 0
        for ck, cells in res["cells"].items():
            tf, side, w = ck.split("|")
            for mn, c in cells.items():
                if not c["measurable"]:
                    thin += 1
                    continue
                zd = (f" ({c['in_zones']}z/{c['in_days']}d)"
                      if "in_zones" in c else "")
                L.append(f"| {tf} | {side} | {w} | {mn} ({c['unit']}) "
                         f"| {c['in_n']}{zd} | {c['in_value']} "
                         f"| {c['base_value']} | {c['shift']:+g} "
                         f"| {c['null_p95_abs']} | {c['pct_vs_null']} "
                         f"| {'YES' if c['significant'] else 'no'} |")
        L += ["", f"(unmeasurable cells this leg: {thin} — thin in-zone "
              "populations print in the JSON with their counts)", ""]
    L += ["## Claims (>= 3-of-4 legs, same-signed significant)", "",
          "| tf | side | window | metric | legs | shifts |",
          "|---|---|---|---|---|---|"]
    for c in art["claims"]:
        L.append(f"| {c['tf']} | {c['side']} | {c['window']} "
                 f"| {c['metric']} | {', '.join(c['legs'])} "
                 f"| {', '.join(f'{s:+g}' for s in c['shifts'])} |")
    if not art["claims"]:
        L.append("| (no metric clears on 3 of 4 legs) | | | | | |")
    L += ["", "## Single-leg findings (routed to per_market_watch.md "
          "with selection-nulls; listed, never rules)", "",
          "| instrument | tf | side | window | metric | shift | pct vs "
          "null | sel-pct | beats selection |", "|---|---|---|---|---|---|---|---|---|"]
    for r in art["watch_rows"]:
        L.append(f"| {r['instrument']} | {r['tf']} | {r['side']} "
                 f"| {r['window']} | {r['metric']} | {r['shift']:+g} "
                 f"| {r['pct_vs_null']} | {r['sel_pct']} "
                 f"| {'YES' if r['beats_selection'] else 'no'} |")
    if not art["watch_rows"]:
        L.append("| (none) | | | | | | | | |")
    L.append("")
    with open(os.path.join(OUT, "zone_anatomy.md"), "w") as f:
        f.write("\n".join(L))


def claims_and_watch(results, sel_ratios):
    claims, watch = [], []
    axes = {}
    for res in results:
        for ck, cells in res["cells"].items():
            for mn, c in cells.items():
                if c["measurable"] and c["significant"]:
                    axes.setdefault((ck, mn), []).append(
                        (res["instrument"], c["shift"]))
    claimed = set()
    for (ck, mn), legs in sorted(axes.items()):
        signs = {np.sign(s) for _i, s in legs}
        if len(legs) >= CLAIM_MIN_LEGS and len(signs) == 1:
            tf, side, w = ck.split("|")
            claims.append({"tf": tf, "side": side, "window": w,
                           "metric": mn,
                           "legs": [i for i, _s in legs],
                           "shifts": [s for _i, s in legs]})
            claimed.add((ck, mn))
    for res in results:
        instr = res["instrument"]
        for ck, cells in res["cells"].items():
            for mn, c in cells.items():
                if not (c["measurable"] and c["significant"]) \
                        or (ck, mn) in claimed:
                    continue
                tf, side, w = ck.split("|")
                sp = sel_ratios.get(instr, {})
                ratio = (abs(c["shift"]) / c["null_p95_abs"]
                         if c["null_p95_abs"] else None)
                maxes = sp.get("seed_maxes")
                sel_pct = beats = None
                if ratio is not None and maxes is not None \
                        and len(maxes):
                    sel_pct = round(100 * float(
                        np.mean(np.array(maxes) < ratio)), 1)
                    beats = bool(ratio > np.percentile(maxes, 95))
                watch.append({"instrument": instr, "tf": tf,
                              "side": side, "window": w, "metric": mn,
                              "in_zones": c.get("in_zones"),
                              "in_days": c.get("in_days"),
                              "in_n": c["in_n"], "in_value": c["in_value"],
                              "base_value": c["base_value"],
                              "shift": c["shift"],
                              "pct_vs_null": c["pct_vs_null"],
                              "sel_pct": sel_pct,
                              "beats_selection": bool(beats)})
    return claims, watch


def run_all(instrs):
    results = []
    sel_ratios = {}
    for instr in instrs:
        print(f"# zone_anatomy: {instr} ...", file=sys.stderr)
        P = prepare_instrument(instr)
        frames = {tf: source_frame(instr, tf) for tf in SOURCE_TFS}
        res, seed_maxes = run_instrument(P, frames)
        if seed_maxes:
            sel_ratios[instr] = {"seed_maxes": seed_maxes}
        results.append(res)
    return results, sel_ratios


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--instr", nargs="*",
                    default=["uk100fut", "ger40fut", "nas100fut",
                             "us30fut"])
    a = ap.parse_args()
    os.makedirs(OUT, exist_ok=True)
    head = subprocess.run(["git", "rev-parse", "HEAD"], cwd=ROOT,
                          capture_output=True, text=True).stdout.strip()
    results, sel_ratios = run_all(a.instr)
    claims, watch = claims_and_watch(results, sel_ratios)
    art = {"STAMP": ("OBSERVATIONAL arrival anatomy — the v3 zones' "
                     "mechanism test, independent of signal "
                     "conditioning; mint-on-lift only; never "
                     "validation"),
           "engine_commit": head,
           "anchor_mult": DEPART_MULTS[0],
           "min_bars_FLAGGED": ANATOMY_MIN_BARS,
           "min_legs_FLAGGED": ANATOMY_MIN_LEGS,
           "claim_min_legs": CLAIM_MIN_LEGS,
           "results": results, "claims": claims, "watch_rows": watch}
    with open(os.path.join(OUT, "zone_anatomy.json"), "w") as f:
        json.dump(art, f, indent=2, default=str)
    _emit(art, head)
    print(f"OBSERVATIONAL arrival anatomy -> {OUT}/zone_anatomy.md "
          f"({len(claims)} claims; {len(watch)} single-leg findings)")


if __name__ == "__main__":
    main()
