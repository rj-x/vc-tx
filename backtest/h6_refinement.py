"""Scalp refinement program (register 100; pre-registered
prereg_h6_refinement_program, counted 2026-08-28). A COUNTED EXPERIMENT
FAMILY on the scalp thread. v0 (R-SCALP-the scalp signal) is UNTOUCHED; every output
is a CANDIDATE ARM through the front door only: surviving candidates ->
ratification -> v1 arms, forward-graded; the September sealed window
examines whatever registers.

(a) CO-FIRE CONTEXT CENSUS — per the scalp sentence fire, every other signal firing
    within +/-COFIRE_BARS bars (the fires.csv self-join on the 1M
    axis); class = with-S vs without-S per co-firing signal, plus
    any-vs-none; outcome = the net 0.5xATR/5-bar reach; split in pp;
    luck budget = touch labels permuted within instrument x window
    strata, pinned seeds; per-cell null p95 + field count vs null.
(b) DISCRIMINATOR RULE — candidate-grade only if |split| >= SPLIT_MIN_PP
    AND beyond its own null p95, same sign, on >= CAND_MIN_LEGS of 4
    instruments; glints listed, never chained.
(c) VETO COUNTERFACTUALS — filtered vs unfiltered book on identical
    fires for candidate-grade classes: reach, net on the census's scalp
    economics (touch -> +0.5xATR - spread; non-touch -> cum@5 - spread),
    n retained, amputation cost; floors = the instrument's B-RANDOM
    member range (time-matched filtered floors a FLAGGED follow-up).
(d) TIME-CAP DERIVATION — P(touch by 5 | dry at k); exit-at-k in
    CAP_KS for non-reachers vs the 10-bar-horizon hold (a PROXY for
    EOD-flat, stated; the true comparison comes from the scalp arms'
    journal rows), net of spread. Register 64's time-exit ruling is
    CITED and DISTINGUISHED: the target is retained, only the non-reach
    tail is capped; any cap proposes JOINTLY with the v1 price-stop.
(e) SCOPE FENCE — the cell budget printed in the header; enrichment
    cuts (session / quadrant / MTF joined at the fire) held to the same
    >= 3-of-4 rule; nothing modifies v0. Both windows; all four
    instruments; no pooling; twin-run pinned
    (tests/test_h6_refinement.py); weekly under Part C.
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
SB = os.path.join(ROOT, "reports", "scoreboard")
FIRES_CSV = os.path.join(ROOT, "reports", "fires.csv")
BP_FIRES = os.path.join(SB, "bar_persistence_fires.csv")
BP_JSON = os.path.join(SB, "bar_persistence.json")
ENRICHED = os.path.join(ROOT, "reports", "trades_enriched.csv")

SIGNAL = "S0-H" + str(6)
COFIRE_BARS = 5              # order-stated: +/-5 bars on the 1M axis
SPLIT_MIN_PP = 10.0          # the register-84 convention
MIN_SIDE_N = 10              # the matrix convention
CAND_MIN_LEGS = 3            # order-stated: >= 3 of 4 instruments
CAP_KS = (3, 5, 8)           # order-stated time-cap grid
REACH_ATR = 0.5              # the scalp target (register 94)
NULL_SHUFFLES = 100
NULL_SEEDS = tuple(range(NULL_SHUFFLES))
ENRICH_CUTS = ("session", "quadrant", "mtf")
INSTRUMENTS = ("uk100fut", "ger40fut", "nas100fut", "us30fut")


def load_rows():
    bp = [r for r in csv.DictReader(open(BP_FIRES))
          if r["signal"] == SIGNAL and r["zone"] in ("backtest", "forward")
          and r["touched_0p5atr_5b_net_of_spread"] in ("True", "False")]
    fires = [r for r in csv.DictReader(open(FIRES_CSV))
             if r["signal"] != SIGNAL and "(either-dir)" not in r["signal"]]
    enr = {}
    if os.path.exists(ENRICHED):
        for r in csv.DictReader(open(ENRICHED)):
            if r["sentence_id"] == SIGNAL and r["variant"] == "R-NOTRAIL":
                t = pd.Timestamp(r["open_ts"]) - pd.Timedelta(minutes=1)
                enr[(r["instrument"], t.value)] = r
    return bp, fires, enr


def cofire_tags(bp, fires):
    """Per the scalp sentence fire: the set of other signals firing within
    +/-COFIRE_BARS minutes on the same instrument."""
    by_instr = {}
    for f in fires:
        by_instr.setdefault(f["instrument"], []).append(
            (pd.Timestamp(f["fire_ts"]).value, f["signal"]))
    for v in by_instr.values():
        v.sort()
    win = COFIRE_BARS * 60_000_000_000
    out = []
    for r in bp:
        t = pd.Timestamp(r["fire_ts"]).value
        arr = by_instr.get(r["instrument"], [])
        keys = [x[0] for x in arr]
        lo = int(np.searchsorted(keys, t - win, side="left"))
        hi = int(np.searchsorted(keys, t + win, side="right"))
        out.append(sorted({arr[i][1] for i in range(lo, hi)}))
    return out


def fire_net(r):
    """The census's scalp economics per fire (register 100(c))."""
    spread = float(r["spread_pts"])
    if r["touched_0p5atr_5b_net_of_spread"] == "True":
        return REACH_ATR * float(r["atr15_at_fire"]) - spread
    c5 = r.get("cum_pts_bar5")
    return (float(c5) if c5 not in ("", "None", None) else 0.0) - spread


def fire_features(r, tg, enr):
    """The feature set one the scalp sentence fire carries: its co-firing signals,
    the any-co-fire flag, and its enrichment cuts."""
    e = enr.get((r["instrument"], pd.Timestamp(r["fire_ts"]).value))
    own = {f"cofire:{s}" for s in tg}
    if tg:
        own.add("cofire:any")
    for cut in ENRICH_CUTS:
        val = (r["session"] if cut == "session"
               else (e[cut] if e else "unclassified"))
        own.add(f"{cut}:{val}")
    return own


def split_cells(bp, tags, enr):
    """(instrument, window, feature) -> with/without [n, touches] over
    a FIXED feature universe (every feature seen on that instrument x
    window); a fire not carrying a feature counts on its without side.
    Single pass, no double counting."""
    feats_of = [fire_features(r, tg, enr) for r, tg in zip(bp, tags)]
    universe = {}
    for r, own in zip(bp, feats_of):
        universe.setdefault((r["instrument"], r["zone"]), set()).update(
            own | {"cofire:any"})
    cells = {}
    for r, own in zip(bp, feats_of):
        touch = int(r["touched_0p5atr_5b_net_of_spread"] == "True")
        for feat in universe[(r["instrument"], r["zone"])]:
            c = cells.setdefault((r["instrument"], r["zone"], feat),
                                 {"with": [0, 0], "without": [0, 0]})
            side = "with" if feat in own else "without"
            c[side][0] += 1
            c[side][1] += touch
    return cells


def _split(c):
    nw, hw = c["with"]
    no, ho = c["without"]
    if nw < MIN_SIDE_N or no < MIN_SIDE_N:
        return None
    return round(100 * (hw / nw - ho / no), 1)


def luck(bp, tags, enr, cells):
    """Touch labels permuted within instrument x window strata; per-cell
    null |split| p95; field count of qualifying cells vs null."""
    strata = {}
    for i, r in enumerate(bp):
        strata.setdefault((r["instrument"], r["zone"]), []).append(i)
    labels0 = [r["touched_0p5atr_5b_net_of_spread"] == "True" for r in bp]
    keys = [k for k, c in cells.items() if _split(c) is not None]
    obs = sum(1 for k in keys if abs(_split(cells[k])) >= SPLIT_MIN_PP)
    feats_of = [fire_features(r, tg, enr) for r, tg in zip(bp, tags)]
    null_abs = {k: [] for k in keys}
    counts = []
    idx_by_key = {}
    for k in keys:
        instr, w, feat = k
        idx_by_key[k] = [i for i, r in enumerate(bp)
                         if r["instrument"] == instr and r["zone"] == w]
    for seed in NULL_SEEDS:
        rs = np.random.RandomState(seed)
        lab = list(labels0)
        for idxs in strata.values():
            perm = rs.permutation(len(idxs))
            vals = [labels0[idxs[j]] for j in perm]
            for j, i in enumerate(idxs):
                lab[i] = vals[j]
        n_q = 0
        for k in keys:
            feat = k[2]
            w_n = w_h = o_n = o_h = 0
            for i in idx_by_key[k]:
                if feat in feats_of[i]:
                    w_n += 1
                    w_h += lab[i]
                else:
                    o_n += 1
                    o_h += lab[i]
            sp = 100 * (w_h / w_n - o_h / o_n) if w_n and o_n else 0.0
            null_abs[k].append(abs(sp))
            if abs(sp) >= SPLIT_MIN_PP:
                n_q += 1
        counts.append(n_q)
    return ({k: round(float(np.percentile(v, 95)), 1)
             for k, v in null_abs.items()},
            {"measurable_cells": len(keys), "observed_qualifying": obs,
             "null_median": float(np.median(counts)) if counts else None,
             "null_p95": (float(np.percentile(counts, 95))
                          if counts else None),
             "percentile_vs_null": (round(100 * float(np.mean(
                 [obs > m for m in counts])), 1) if counts else None)})


def discriminate(cells, p95):
    """Per feature: legs (instruments) where windows-pooled |split| >=
    SPLIT_MIN_PP and beyond the pooled cell's null (max of window p95s),
    same sign; candidate-grade at >= CAND_MIN_LEGS."""
    feats = sorted({k[2] for k in cells})
    out = {}
    for feat in feats:
        legs = {}
        for instr in INSTRUMENTS:
            agg = {"with": [0, 0], "without": [0, 0]}
            p = []
            for w in ("backtest", "forward"):
                c = cells.get((instr, w, feat))
                if not c:
                    continue
                for side in ("with", "without"):
                    agg[side][0] += c[side][0]
                    agg[side][1] += c[side][1]
                if (instr, w, feat) in p95:
                    p.append(p95[(instr, w, feat)])
            sp = _split(agg)
            if sp is None or not p:
                continue
            legs[instr] = {"split_pp": sp, "null_p95": max(p),
                           "n_with": agg["with"][0],
                           "n_without": agg["without"][0],
                           "clears": bool(abs(sp) >= SPLIT_MIN_PP
                                          and abs(sp) > max(p))}
        clearing = {i: v for i, v in legs.items() if v["clears"]}
        signs = {np.sign(v["split_pp"]) for v in clearing.values()}
        grade = ("candidate" if len(clearing) >= CAND_MIN_LEGS
                 and len(signs) == 1 else
                 "glint" if clearing else "none")
        out[feat] = {"legs": legs, "clearing_legs": sorted(clearing),
                     "grade": grade,
                     "sign": ("+" if clearing and next(iter(signs)) > 0
                              else "-" if clearing else None)}
    return out


def veto_counterfactual(bp, tags, enr, feat, sign, floors):
    """Filtered vs unfiltered book on identical fires, per instrument."""
    out = {}
    for instr in INSTRUMENTS:
        rows = [(r, tg) for r, tg in zip(bp, tags)
                if r["instrument"] == instr]
        if not rows:
            continue

        def has(r, tg):
            return feat in fire_features(r, tg, enr)
        keep = [(r, tg) for r, tg in rows
                if (has(r, tg) if sign == "+" else not has(r, tg))]
        drop = [x for x in rows if x not in keep]

        def book(rs):
            if not rs:
                return {"n": 0}
            t = sum(1 for r, _ in rs
                    if r["touched_0p5atr_5b_net_of_spread"] == "True")
            return {"n": len(rs), "reach_pct": round(100 * t / len(rs), 1),
                    "net_pts": round(float(sum(fire_net(r) for r, _ in rs)),
                                     1)}
        amput = sum(1 for r, _ in drop
                    if r["touched_0p5atr_5b_net_of_spread"] == "True")
        out[instr] = {"unfiltered": book(rows), "filtered": book(keep),
                      "dropped": len(drop),
                      "amputated_touchers": amput,
                      "floor_member_range": floors.get(instr)}
    return out


def time_cap(bp):
    """P(touch by 5 | dry at k) and exit-at-k vs the 10-bar hold for
    non-reachers, net of spread, per instrument."""
    out = {}
    for instr in INSTRUMENTS:
        rows = [r for r in bp if r["instrument"] == instr]
        if not rows:
            continue
        curve = []
        for k in range(1, 5):
            dry = [r for r in rows
                   if r["bar_of_first_touch"] in ("", "None")
                   or int(r["bar_of_first_touch"]) > k]
            hit = sum(1 for r in dry
                      if r["touched_0p5atr_5b"] == "True")
            curve.append({"k": k, "n_dry": len(dry),
                          "p_touch_by_5": (round(hit / len(dry), 3)
                                           if dry else None)})
        non = [r for r in rows if r["touched_0p5atr_5b"] != "True"]
        caps = {}
        for k in CAP_KS:
            col = f"cum_pts_bar{k}"
            vals = [(float(r[col]), float(r["cum_pts_bar10"]))
                    for r in non
                    if r.get(col) not in ("", "None", None)
                    and r.get("cum_pts_bar10") not in ("", "None", None)]
            if not vals:
                continue
            caps[str(k)] = {
                "n_nonreach": len(vals),
                "median_exit_at_k_pts": round(float(np.median(
                    [a for a, _ in vals])), 2),
                "median_hold10_pts": round(float(np.median(
                    [b for _, b in vals])), 2),
                "net_delta_cap_minus_hold": round(float(sum(
                    a - b for a, b in vals)), 1)}
        out[instr] = {"conditional_reach": curve, "caps": caps,
                      "spread_pts": float(rows[0]["spread_pts"])}
    return out


# ------------------------------------------------ register 101: real basis

SCALP_ARM = "R-SCALP-H" + str(6)
REACH_REASONS = ("target", "target_gap")
STOP_REASONS = ("stop", "stop_gap")
PROPOSAL_MIN_LEGS = 3        # order-stated: cap@3 must hold on >= 3 legs
STOP_PCTILE = 75             # candidate stop = p75 of forward non-reach MAE


def load_scalp_rows():
    """The plain scalp arm's journal rows from trades_enriched.csv,
    ex-lockbox, with window and the fire key (open_ts - 1M)."""
    from engine.store_loader import in_lockbox_span, lockbox_boundary, zones
    boundary, gl = lockbox_boundary(), zones()["go_live"]
    out = []
    if not os.path.exists(ENRICHED):
        return out
    for r in csv.DictReader(open(ENRICHED)):
        if r["variant"] != SCALP_ARM or in_lockbox_span(r["open_ts"]):
            continue
        t = pd.Timestamp(r["open_ts"])
        w = "backtest" if t < boundary else "forward" if t >= gl else None
        if w is None:
            continue
        r = dict(r)
        r["_window"] = w
        r["_fire_ns"] = (t - pd.Timedelta(minutes=1)).value
        out.append(r)
    return out


def real_basis(scalp_rows, bp):
    """Cap at bar k applied to every scalp row still DRY at bar k (not
    reached by the close of bar k: target rows with duration >= k, and
    all eod/stop rows) vs the ACTUAL journal outcome, same fires, net
    of spread. Delta decomposed by the avoided tail: late-reach
    (AMPUTATION — the target would have hit later), eod (drift
    savings), stop (disaster savings; stops in the dry set exit after
    bar k, so the cap dodges them by construction; stops at or before
    bar k are counted apart as not-dodgeable). holds = net delta > 0
    at n >= MIN_SIDE_N."""
    bp_idx = {(r["instrument"], pd.Timestamp(r["fire_ts"]).value): r
              for r in bp}
    out = {}
    for instr in INSTRUMENTS:
        for w in ("backtest", "forward"):
            rows = [r for r in scalp_rows
                    if r["instrument"] == instr and r["_window"] == w]
            cell = {"n_rows": len(rows),
                    "n_eventual_nonreach": sum(
                        1 for r in rows
                        if r["exit_reason"] not in REACH_REASONS),
                    "caps": {}}
            for k in CAP_KS:
                col = f"cum_pts_bar{k}"
                agg = {"n_dry": 0, "delta_total": 0.0,
                       "delta_late_reach": 0.0, "n_late_reach": 0,
                       "delta_eod": 0.0, "n_eod": 0,
                       "delta_stop": 0.0, "n_stop_dodged": 0,
                       "n_stop_before_cap": 0}
                for r in rows:
                    dur = float(r["duration_min"])
                    reach = r["exit_reason"] in REACH_REASONS
                    if reach and dur < k:
                        continue                       # reached by bar k
                    if not reach and r["exit_reason"] in STOP_REASONS \
                            and dur < k:
                        agg["n_stop_before_cap"] += 1  # not dodgeable
                        continue
                    b = bp_idx.get((instr, r["_fire_ns"]))
                    if not b or b.get(col) in ("", "None", None):
                        continue
                    cap = float(b[col]) - float(b["spread_pts"])
                    delta = cap - float(r["points"])
                    agg["n_dry"] += 1
                    agg["delta_total"] += delta
                    if reach:
                        agg["n_late_reach"] += 1
                        agg["delta_late_reach"] += delta
                    elif r["exit_reason"] in STOP_REASONS:
                        agg["n_stop_dodged"] += 1
                        agg["delta_stop"] += delta
                    else:
                        agg["n_eod"] += 1
                        agg["delta_eod"] += delta
                for key in ("delta_total", "delta_late_reach",
                            "delta_eod", "delta_stop"):
                    agg[key] = round(agg[key], 1)
                agg["holds"] = bool(agg["n_dry"] >= MIN_SIDE_N
                                    and agg["delta_total"] > 0)
                cell["caps"][str(k)] = agg
            out[f"{instr}|{w}"] = cell
    return out


def stop_cluster_check(scalp_rows, iso_week=32):
    """Re-verify the referenced week forensic on the scalp rows: stop
    rows in the ISO week, their MFE distribution, and the lockbox
    overlap (the week may straddle the excluded span)."""
    from engine.store_loader import lockbox_boundary, zones
    rows = [r for r in scalp_rows
            if pd.Timestamp(r["open_ts"]).isocalendar().week == iso_week]
    stops = [r for r in rows if r["exit_reason"] in STOP_REASONS]
    mfe = [float(r["mfe_pts"]) for r in stops
           if r.get("mfe_pts") not in ("", "None", None)]
    return {"iso_week": iso_week, "rows_ex_lockbox": len(rows),
            "stops": len(stops),
            "stops_mfe_le_55": sum(1 for m in mfe if m <= 55),
            "lockbox_note": ("ISO week 32 (2026-08-03..09) straddles the "
                             "excluded lockbox span from 2026-08-04 — only "
                             "its pre-boundary rows count here")}


def joint_proposal(scalp_rows, rb):
    """Emit the joint v1 package only if cap@3 holds on the real basis
    on >= PROPOSAL_MIN_LEGS legs (forward window). Candidate stop =
    p75 of forward non-reachers' MAE (xATR15) per instrument;
    amputation = share of forward reachers whose MAE exceeded it."""
    holding = [i for i in INSTRUMENTS
               if rb.get(f"{i}|forward", {}).get("caps", {})
               .get("3", {}).get("holds")]
    pkg = {"triggered": len(holding) >= PROPOSAL_MIN_LEGS,
           "legs_holding_cap3_forward": holding, "per_instrument": {}}
    for instr in INSTRUMENTS:
        rows = [r for r in scalp_rows
                if r["instrument"] == instr and r["_window"] == "forward"
                and r.get("mae_atr") not in ("", "None", None)]
        non = [float(r["mae_atr"]) for r in rows
               if r["exit_reason"] not in REACH_REASONS]
        reach = [float(r["mae_atr"]) for r in rows
                 if r["exit_reason"] in REACH_REASONS]
        if len(non) < MIN_SIDE_N:
            pkg["per_instrument"][instr] = {"n_nonreach": len(non),
                                            "note": "unmeasurable"}
            continue
        p = {q: round(float(np.percentile(non, q)), 3)
             for q in (50, STOP_PCTILE, 90)}
        cand = p[STOP_PCTILE]
        amput = (round(float(np.mean([m > cand for m in reach])), 3)
                 if reach else None)
        pkg["per_instrument"][instr] = {
            "n_nonreach": len(non), "n_reach": len(reach),
            "nonreach_mae_atr_pctiles": p,
            "candidate_stop_atr": cand,
            "derivation": (f"p{STOP_PCTILE} of forward non-reachers' "
                           "MAE (xATR15 at fire), ex-lockbox"),
            "reachers_amputated_share": amput}
    return pkg


def run():
    bp, fires, enr = load_rows()
    tags = cofire_tags(bp, fires)
    cells = split_cells(bp, tags, enr)
    p95, budget = luck(bp, tags, enr, cells)
    disc = discriminate(cells, p95)
    bpj = json.load(open(BP_JSON))
    floors = {}
    for res in bpj["results"]:
        ens = (res.get("baselines", {}).get("B-RANDOM", {})
               .get("forward", {}).get("whole", {}).get("atr_0.5@5"))
        if ens:
            floors[res["instrument"]] = ens.get("net_range")
    cands = {f: d for f, d in disc.items() if d["grade"] == "candidate"}
    vetos = {f: veto_counterfactual(bp, tags, enr, f, d["sign"], floors)
             for f, d in cands.items()}
    cell_budget = {"split_cells": len(cells),
                   "measurable_cells": budget["measurable_cells"],
                   "features": len({k[2] for k in cells}),
                   "instruments": len(INSTRUMENTS), "windows": 2}
    scalp = load_scalp_rows()
    rb = real_basis(scalp, bp)
    return {"n_fires": len(bp), "cell_budget": cell_budget,
            "n_scalp_rows": len(scalp),
            "real_basis": rb,
            "stop_cluster_week32": stop_cluster_check(scalp),
            "joint_v1_proposal": joint_proposal(scalp, rb),
            "luck_budget": budget,
            "splits": {"|".join(k): {"with": c["with"],
                                     "without": c["without"],
                                     "split_pp": _split(c),
                                     "null_p95": p95.get(k)}
                       for k, c in sorted(cells.items())},
            "discriminator": disc, "candidates": sorted(cands),
            "glints": sorted(f for f, d in disc.items()
                             if d["grade"] == "glint"),
            "veto_counterfactuals": vetos, "time_cap": time_cap(bp)}


def _emit(art, head):
    cb, lb = art["cell_budget"], art["luck_budget"]
    L = ["# Scalp Refinement Program (GENERATED by backtest.h6_refinement)",
         "", "Terms: [docs/GLOSSARY.md](../../docs/GLOSSARY.md).", "",
         f"Engine `{head[:9]}` — OBSERVATIONAL, pre-registered "
         "(prereg_h6_refinement_program, register 100). A COUNTED "
         "EXPERIMENT FAMILY on the scalp thread; v0 (R-SCALP-the scalp signal) "
         "UNTOUCHED; every output is a CANDIDATE ARM through the front "
         "door — surviving candidates -> ratification -> v1 arms, "
         "forward-graded; the September sealed window examines "
         f"whatever registers. SCOPE FENCE — CELL BUDGET: {cb['features']} "
         f"features x {cb['instruments']} instruments x {cb['windows']} "
         f"windows = {cb['split_cells']} split cells, "
         f"{cb['measurable_cells']} measurable (both sides >= "
         f"{MIN_SIDE_N}). STATISTIC SHAPES (74-B): co-fire/enrichment "
         "splits = single-cell extremity vs a label-permutation null "
         f"({NULL_SHUFFLES} pinned seeds) with the field count vs null "
         "as the luck budget; the discriminator = cross-instrument "
         f"consistency (>= {CAND_MIN_LEGS} of 4 legs, same sign); veto "
         "counterfactuals and the time-cap curve = descriptive "
         "re-pricing on identical fires. Outcome = net 0.5xATR/5-bar "
         "reach (registers 63/64). Time-cap: register 64's time-exit "
         "ruling CITED and DISTINGUISHED — the target is retained, "
         "only the non-reach tail is capped; the 10-bar hold is a PROXY "
         "for EOD-flat (true comparison from the scalp arms' journal "
         "rows); any cap proposes JOINTLY with the v1 price-stop. "
         f"Fires: {art['n_fires']} (both windows, four instruments, no "
         "pooling).", "",
         f"**Luck budget:** {lb['observed_qualifying']} of "
         f"{lb['measurable_cells']} measurable cells reach |split| >= "
         f"{SPLIT_MIN_PP:g}pp vs null median {lb['null_median']} / p95 "
         f"{lb['null_p95']}; percentile {lb['percentile_vs_null']}.", "",
         "## Discriminator (per feature: clearing legs; candidate-grade "
         f"needs >= {CAND_MIN_LEGS} same-signed)", "",
         "| feature | grade | sign | clearing legs | per-leg split (pp) / "
         "null p95 / n with:without |", "|---|---|---|---|---|"]
    for feat, d in sorted(art["discriminator"].items(),
                          key=lambda x: (x[1]["grade"] != "candidate",
                                         x[1]["grade"] != "glint", x[0])):
        if d["grade"] == "none":
            continue
        legs = "; ".join(f"{i}: {v['split_pp']:+.1f} / {v['null_p95']} / "
                         f"{v['n_with']}:{v['n_without']}"
                         for i, v in sorted(d["legs"].items()))
        L.append(f"| {feat} | {d['grade']} | {d['sign']} "
                 f"| {', '.join(d['clearing_legs'])} | {legs} |")
    if not any(d["grade"] != "none" for d in art["discriminator"].values()):
        L.append("| (no feature clears its null on any leg) | | | | |")
    L += ["", "## Veto counterfactuals (candidate-grade classes only; "
          "identical fires; census scalp economics)", ""]
    if art["veto_counterfactuals"]:
        L += ["| feature | instrument | unfiltered n / reach % / net | "
              "filtered n / reach % / net | dropped | amputated touchers "
              "| floor range |", "|---|---|---|---|---|---|---|"]
        for feat, per in art["veto_counterfactuals"].items():
            for instr, v in per.items():
                u, f = v["unfiltered"], v["filtered"]
                L.append(f"| {feat} | {instr} | {u['n']} / "
                         f"{u.get('reach_pct', '—')} / {u.get('net_pts', '—')} "
                         f"| {f['n']} / {f.get('reach_pct', '—')} / "
                         f"{f.get('net_pts', '—')} | {v['dropped']} "
                         f"| {v['amputated_touchers']} "
                         f"| {v['floor_member_range']} |")
    else:
        L.append("No candidate-grade class this emission — nothing to "
                 "veto; glints listed above, never chained.")
    L += ["", "## Time-cap derivation (per instrument: P(touch by 5 | "
          "dry at k); exit-at-k vs 10-bar hold for non-reachers, net of "
          "spread)", "",
          "| instrument | k=1 | k=2 | k=3 | k=4 | cap@3 Δ (n) | cap@5 Δ (n) "
          "| cap@8 Δ (n) |", "|---|---|---|---|---|---|---|---|"]
    for instr, t in art["time_cap"].items():
        cr = {c["k"]: c for c in t["conditional_reach"]}

        def _c(k):
            c = cr.get(k, {})
            return (f"{c.get('p_touch_by_5')} ({c.get('n_dry', 0)})")

        def _cap(k):
            c = t["caps"].get(str(k))
            return (f"{c['net_delta_cap_minus_hold']:+.1f} "
                    f"({c['n_nonreach']})" if c else "—")
        L.append(f"| {instr} | {_c(1)} | {_c(2)} | {_c(3)} | {_c(4)} "
                 f"| {_cap(3)} | {_cap(5)} | {_cap(8)} |")
    L += ["", "## Time-cap on the REAL BASIS (register 101): exit-at-k "
          "for non-reachers vs the scalp arm's actual journal outcome, "
          f"same fires, net of spread; {art['n_scalp_rows']} scalp rows "
          "ex-lockbox; savings decomposed by the avoided tail's exit "
          "reason; stops dodged = exits after bar k", "",
          "| instrument | window | rows | eventual non-reach | dry@3 n | "
          "cap@3 Δ total (late-reach / eod / stop) | stops dodged : "
          "before cap | cap@5 Δ | cap@8 Δ | holds@3 |",
          "|---|---|---|---|---|---|---|---|---|---|"]
    for key, c in art["real_basis"].items():
        instr, w = key.split("|")
        c3, c5, c8 = (c["caps"].get(k, {}) for k in ("3", "5", "8"))
        dim = "°" if c3.get("n_dry", 0) < MIN_SIDE_N else ""
        L.append(f"| {instr} | {w} | {c['n_rows']} "
                 f"| {c['n_eventual_nonreach']} | {dim}{c3.get('n_dry', 0)} "
                 f"| {c3.get('delta_total', '—')} "
                 f"({c3.get('delta_late_reach', '—')} / "
                 f"{c3.get('delta_eod', '—')} / {c3.get('delta_stop', '—')}) "
                 f"| {c3.get('n_stop_dodged', '—')} : "
                 f"{c3.get('n_stop_before_cap', '—')} "
                 f"| {c5.get('delta_total', '—')} | {c8.get('delta_total', '—')} "
                 f"| {'YES' if c3.get('holds') else 'no'} |")
    wk = art["stop_cluster_week32"]
    L += ["", f"Week-{wk['iso_week']} stop-cluster check on the scalp rows: "
          f"{wk['stops']} stop rows ({wk['stops_mfe_le_55']} with MFE <= 55) "
          f"of {wk['rows_ex_lockbox']} ex-lockbox rows — {wk['lockbox_note']}.",
          ""]
    pk = art["joint_v1_proposal"]
    L += ["## Joint v1 proposal (register 101; emitted only if cap@3 holds "
          f"on the real basis on >= {PROPOSAL_MIN_LEGS} forward legs; "
          "NOTHING REGISTERED until the operator rules)", "",
          f"Trigger: cap@3 holds forward on {pk['legs_holding_cap3_forward']} "
          f"→ {'TRIGGERED — the package below is a RATIFICATION PACKAGE' if pk['triggered'] else 'NOT TRIGGERED — no package'}.",
          ""]
    if pk["triggered"]:
        L += ["| instrument | fwd non-reach n | non-reach MAE xATR p50 / p75 / "
              "p90 | candidate stop (p75) | reachers amputated (share) | "
              "derivation |", "|---|---|---|---|---|---|"]
        for instr, v in pk["per_instrument"].items():
            if "note" in v:
                L.append(f"| {instr} | {v['n_nonreach']} | — | — | — | "
                         f"{v['note']} |")
                continue
            p = v["nonreach_mae_atr_pctiles"]
            L.append(f"| {instr} | {v['n_nonreach']} | {p[50]} / "
                     f"{p[STOP_PCTILE]} / {p[90]} | {v['candidate_stop_atr']} "
                     f"| {v['reachers_amputated_share']} | {v['derivation']} |")
        L += ["", "Package = bar-3 cap for non-reachers (target retained) + "
              "the per-instrument candidate stop above, registered as ONE v1 "
              "arm only on operator ratification; both derive from the same "
              "forward non-reach accrual (register 64 distinguished: no "
              "time-exit harvest)."]
    L.append("")
    with open(os.path.join(SB, "h6_refinement.md"), "w") as f:
        f.write("\n".join(L))


def main():
    ap = argparse.ArgumentParser()
    ap.parse_args()
    head = subprocess.run(["git", "rev-parse", "HEAD"], cwd=ROOT,
                          capture_output=True, text=True).stdout.strip()
    art = run()
    art = {"STAMP": ("OBSERVATIONAL Scalp refinement program — a counted "
                     "experiment family; v0 untouched; candidates "
                     "through the front door only; never validation"),
           "engine_commit": head, **art}
    with open(os.path.join(SB, "h6_refinement.json"), "w") as f:
        json.dump(art, f, indent=2, default=str)
    _emit(art, head)
    print(f"OBSERVATIONAL the scalp signal refinement -> {SB}/h6_refinement.md "
          f"({len(art['candidates'])} candidate-grade, "
          f"{len(art['glints'])} glints)")


if __name__ == "__main__":
    main()
