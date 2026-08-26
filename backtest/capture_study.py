"""Capture study (register 88 item 4; pre-registered
prereg_capture_study, counted 2026-08-28). THE QUESTION: when a trade
has shown +X, what protection maximizes kept-points per family x
session x tape-character? MOTIVATING OBSERVATION (recorded): the
register-87 breakeven continent split (+2.9k EU / -15.8k US net delta
at rung 0.25). EXPECTED OUTCOME, stated at commissioning: SCOPED
POLICIES, NOT UNIVERSAL RULES. The three-thread convergence behind the
commission: the give-back class holds most losses (register 87), the
exit-efficiency tables (register 84), and the +216 class (register 88
grade record).

PROTECTION LADDER (10 policies, pre-registered): BE at
+{0.25,0.5,1.0,1.5}xATR MFE; TRAIL(arm r, distance t) for r in
{0.5,1.0} x t in {0.5,1.0}xATR (ratchet-only); RATCHET schedules
arm-1.0 with stop = maxMFE-{1.0,0.5}xATR floored at entry. All on the
register-87 array-walk conventions: SETTLED arming (the arming bar and
the prior running max govern the level; a bar's own extension never
tightens its own exit), touch fills, spread inside the journal points.
Base = the R-NOTRAIL journal slice ex-lockbox (the unmanaged full-hold
path). TAPE-CHARACTER from the underwater census machinery: clean (no
underwater close) / quiet-dip / loud-dip (any loud underwater close
before first positive; register-66 loud = rel_volume >= 1.5).

BASELINES: B-RANDOM members under R-NOTRAIL with each identical
policy — member net-delta bands (the floor pattern). LUCK BUDGET:
tape-character labels permuted within family x session strata, 100
pinned seeds; field statistic = count of measurable quiet/loud
cell-pairs whose per-trade best-policy net-delta gap >= GAP_MIN_PTS
(threshold implementer-proposed, FLAGGED). STATISTIC SHAPES (74-B):
per-policy per-cell net-delta vs the member band (descriptive vs
floor); the differentiation claim = field count vs permutation null.
Ex-lockbox (register 85); sealed counted; twin-run pinned
(tests/test_capture_study.py); FRONT-DOOR-ONLY OUTCOMES — a scoped
policy becomes a registered variant only via its own Q-number and
forward grade. Weekly under Part C after first emission.
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

from engine.store_loader import in_lockbox_span
from backtest.recipes import (RECIPE_SET_VERSION, RECIPE_SETS,
                              simulate)
from backtest.signal_points import baseline_fires
from backtest.underwater_census import (BASE_VARIANT, FAMILY_OF,
                                        MIN_CELL_N, NULL_SEEDS,
                                        NULL_SHUFFLES, build_instrument,
                                        load_journal, join_trades,
                                        trajectory)

OUT = os.path.join(ROOT, "reports", "scoreboard")

# the pre-registered protection ladder: (name, kind, arm_r, dist_t)
POLICIES = tuple(
    [(f"BE@{r:g}", "BE", r, None) for r in (0.25, 0.5, 1.0, 1.5)]
    + [(f"TRAIL-{r:g}-{t:g}", "TRAIL", r, t)
       for r in (0.5, 1.0) for t in (0.5, 1.0)]
    + [("RATCHET-1.0-1.0", "RATCHET", 1.0, 1.0),
       ("RATCHET-1.0-0.5", "RATCHET", 1.0, 0.5)])
GAP_MIN_PTS = 5.0        # differentiation threshold — implementer-
                         # proposed at prereg, FLAGGED
NEVER_AGAIN_BOUND_ATR = 1.0   # register 89 item 1: the operator's
                              # never-again bound (no trade exceeds
                              # +1.0xATR MFE unprotected)


def day_regimes(A):
    """Register 89 item 1 (AMENDMENT_capture_regime_neveragain): a
    trade's UTC day classified by the MAJORITY 1M phase-tracker state
    over that day's bars — the conditioning-matrix trending/ranging
    reduction; majority is the parameter-free reduction (the 'day'
    interpretation, stated, operator-correctable). No new thresholds."""
    days = pd.DatetimeIndex(pd.to_datetime(A["ts"], utc=True)).date
    trending = A["t1"] != 0
    out = {}
    df = pd.DataFrame({"day": days, "tr": trending})
    for day, g in df.groupby("day"):
        out[day] = "trending-day" if g["tr"].mean() > 0.5 \
            else "ranging-day"
    return out


def _policy_agg(groups, spread):
    res = {}
    for reg, ts_ in sorted(groups.items()):
        per = {}
        for p in POLICIES:
            cf = [protect_outcome(t, spread, p) for t in ts_]
            per[p[0]] = {
                "n": len(ts_),
                "net_delta": round(float(sum(
                    c - t["pts"] for c, t in zip(cf, ts_))), 1),
                "median_kept_pts": round(float(np.median(cf)), 2)}
        res[reg] = per
    return res


def regime_split(base, spread, regimes, A):
    """DAY-LEVEL regime cut — stands as the RECORDED FIRST ATTEMPT
    (register 90 item 1) with its saturation finding: 98% of days
    classify trending on three legs, no contrast available.
    Superseded as the regime lens by phase_regime_split."""
    ts = A["ts"]
    out = {}
    for t in base:
        day = pd.Timestamp(ts[t["ei"]], tz="UTC").date()
        out.setdefault(regimes.get(day, "ranging-day"), []).append(t)
    return _policy_agg(out, spread)


def phase_regime_split(base, spread, A):
    """Register 90 item 1 (operator ruling, re-registered): regime =
    PHASE-AT-ENTRY — trending/ranging by the 1M phase tracker at the
    FIRE BAR (the enrichment column's convention; existing field, no
    new thresholds). The question unchanged: do protection rules
    scope by tape-character rather than by geography?"""
    out = {}
    for t in base:
        fi = max(t["ei"] - 1, 0)
        reg = ("trending-at-entry" if A["t1"][fi] != 0
               else "ranging-at-entry")
        out.setdefault(reg, []).append(t)
    return _policy_agg(out, spread)


def never_again_pricing(base, spread):
    """Register 89 item 1: per BE rung, the amputation cost (forfeited
    points on would-be winners) per 100 base trades of guaranteeing no
    trade exceeds +NEVER_AGAIN_BOUND_ATR MFE unprotected. Rungs above
    the bound do not guarantee it (printed NON-QUALIFYING). The
    guarantee holds up to the register-87 single-bar span exception
    (arming and stop in one bar), restated."""
    out = {}
    n = len(base)
    for p in POLICIES:
        if p[1] != "BE":
            continue
        rung = p[2]
        amput = 0.0
        n_amput = 0
        for t in base:
            cf = protect_outcome(t, spread, p)
            if cf != t["pts"] and t["pts"] > cf:
                amput += t["pts"] - cf
                n_amput += 1
        out[p[0]] = {
            "rung_atr": rung,
            "qualifies": rung <= NEVER_AGAIN_BOUND_ATR,
            "winners_amputated": n_amput,
            "amputation_pts_total": round(amput, 1),
            "amputation_pts_per_100_trades": (round(100 * amput / n, 1)
                                              if n else None)}
    return out


def protect_outcome(t, spread, policy):
    """Counterfactual points under one protection policy on the actual
    hold. Settled arming; the prior running max governs the level; a
    bar's own extension never tightens its own exit; touch fill."""
    _name, kind, r, tdist = policy
    atr0 = t["atr0"]
    if not atr0:
        return t["pts"]
    fav_run = np.maximum.accumulate(np.maximum(t["mfe_path"], 0.0))
    adv = t["traj"]["adv"]
    armed = np.nonzero(fav_run >= r * atr0)[0]
    if not len(armed):
        return t["pts"]
    for j in range(int(armed[0]) + 1, len(adv)):
        if kind == "BE":
            level = 0.0
        else:
            level = float(fav_run[j - 1]) - tdist * atr0
            if kind == "RATCHET":
                level = max(0.0, level)
        if -adv[j] <= level:
            return float(level - spread)
    return t["pts"]


def tape_class(traj):
    if traj["first_pos"] == 1:
        return "clean"
    return "loud-dip" if traj["first_loud_dip"] is not None \
        else "quiet-dip"


def cell_grid(base, spread):
    """(family, session, tape) -> per-policy {n, median_kept,
    net_delta}; plus per-trade deltas for the null."""
    cells = {}
    for t in base:
        k = (t["family"], t["r"]["session"], tape_class(t["traj"]))
        cells.setdefault(k, []).append(t)
    out = {}
    for k, ts_ in sorted(cells.items()):
        pol = {}
        for p in POLICIES:
            cf = [protect_outcome(t, spread, p) for t in ts_]
            pol[p[0]] = {
                "n": len(ts_),
                "median_kept_pts": round(float(np.median(cf)), 2),
                "net_delta": round(float(sum(
                    c - t["pts"] for c, t in zip(cf, ts_))), 1)}
        best = max(pol, key=lambda name: pol[name]["net_delta"])
        out["|".join(k)] = {"n": len(ts_), "policies": pol,
                            "best_policy": best,
                            "best_net_delta": pol[best]["net_delta"]}
    return out


def diff_statistic(base, spread):
    """Field statistic: measurable quiet/loud pairs whose per-trade
    best-policy net-delta gap >= GAP_MIN_PTS; null = tape labels
    permuted within family x session strata (pinned seeds)."""
    strata = {}
    for i, t in enumerate(base):
        strata.setdefault((t["family"], t["r"]["session"]),
                          []).append(i)
    tapes0 = [tape_class(t["traj"]) for t in base]
    # per-trade per-policy deltas, computed once
    deltas = {p[0]: [protect_outcome(t, spread, p) - t["pts"]
                     for t in base] for p in POLICIES}

    def count(tapes):
        n_q = 0
        for (fam, sess), idxs in sorted(strata.items()):
            q = [i for i in idxs if tapes[i] == "quiet-dip"]
            lo = [i for i in idxs if tapes[i] == "loud-dip"]
            if len(q) < MIN_CELL_N or len(lo) < MIN_CELL_N:
                continue

            def best_per_trade(sel):
                return max(sum(deltas[p[0]][i] for i in sel) / len(sel)
                           for p in POLICIES)
            if abs(best_per_trade(q) - best_per_trade(lo)) \
                    >= GAP_MIN_PTS:
                n_q += 1
        return n_q
    obs = count(tapes0)
    null = []
    for seed in NULL_SEEDS:
        rs = np.random.RandomState(seed)
        tapes = list(tapes0)
        for idxs in strata.values():
            perm = rs.permutation(len(idxs))
            vals = [tapes0[idxs[j]] for j in perm]
            for j, i in enumerate(idxs):
                tapes[i] = vals[j]
        null.append(count(tapes))
    return {"observed": obs, "null_median": float(np.median(null)),
            "null_p95": float(np.percentile(null, 95)),
            "percentile_vs_null": round(
                100 * float(np.mean([obs > m for m in null])), 1)}


def policy_floors(A):
    """B-RANDOM members under BASE_VARIANT + each identical policy:
    member net-delta bands."""
    recipe = RECIPE_SETS[RECIPE_SET_VERSION][BASE_VARIANT]
    members = baseline_fires(A["env"], A["engine_events"])["B-RANDOM"]
    ts = A["ts"]
    nets = {p[0]: [] for p in POLICIES}
    for mf in members:
        trades = []
        for t in simulate(mf, A["env"], recipe, A["spread"]):
            if in_lockbox_span(t["entry_ts"]):
                continue
            ei = int(np.searchsorted(
                ts, pd.Timestamp(t["entry_ts"]).value, side="left"))
            xi = min(len(ts) - 1, ei + int(t["duration_min"]))
            d = t["dir"]
            atr0 = A["env"].atr_at(
                "15min", pd.Timestamp(t["entry_ts"]).value)
            traj = trajectory(ei, xi, d, t["entry"], atr0, A["h"],
                              A["l"], A["c"], A["loud"])
            fav = ((A["h"][ei:xi + 1] - t["entry"]) if d == 1
                   else (t["entry"] - A["l"][ei:xi + 1]))
            trades.append({"pts": t["pts"], "traj": traj,
                           "atr0": atr0, "mfe_path": fav})
        for p in POLICIES:
            nets[p[0]].append(round(float(sum(
                protect_outcome(t, A["spread"], p) - t["pts"]
                for t in trades)), 1))
    return {k: {"members": len(v),
                "median": round(float(np.median(v)), 1),
                "min": round(float(min(v)), 1),
                "max": round(float(max(v)), 1)}
            for k, v in nets.items()}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--instr", nargs="*",
                    default=["uk100fut", "ger40fut", "nas100fut",
                             "us30fut"])
    a = ap.parse_args()
    os.makedirs(OUT, exist_ok=True)
    head = subprocess.run(["git", "rev-parse", "HEAD"], cwd=ROOT,
                          capture_output=True, text=True).stdout.strip()
    all_rows, kept_rows = load_journal()
    art = {"STAMP": ("OBSERVATIONAL capture study — scoped policies "
                     "expected, none adopted; front-door-only "
                     "outcomes; never validation"),
           "engine_commit": head,
           "policies": [p[0] for p in POLICIES],
           "gap_min_pts_FLAGGED": GAP_MIN_PTS,
           "per_instrument": {}}
    for instr in a.instr:
        print(f"# capture_study: {instr} ...", file=sys.stderr)
        A = build_instrument(instr)
        rows = [r for r in kept_rows if r["instrument"] == instr]
        base = [t for t in join_trades(rows, A)
                if t["r"]["variant"] == BASE_VARIANT]
        art["per_instrument"][instr] = {
            "n_base": len(base), "spread": A["spread"],
            "cells": cell_grid(base, A["spread"]),
            "policy_totals": {
                p[0]: round(float(sum(
                    protect_outcome(t, A["spread"], p) - t["pts"]
                    for t in base)), 1) for p in POLICIES},
            "floors": policy_floors(A),
            "luck_budget": diff_statistic(base, A["spread"]),
            "phase_regime_split": phase_regime_split(base, A["spread"],
                                                     A),
            "day_regime_split_first_attempt": regime_split(
                base, A["spread"], day_regimes(A), A),
            "never_again": never_again_pricing(base, A["spread"])}
    with open(os.path.join(OUT, "capture_study.json"), "w") as f:
        json.dump(art, f, indent=2, default=str)
    _emit(art, head)
    print(f"OBSERVATIONAL capture study -> {OUT}/capture_study.md")


def _emit(art, head):
    n_all = sum(r["n_base"]
                for r in art["per_instrument"].values())
    L = ["# Capture Study (GENERATED by backtest.capture_study)", "",
         "Terms: [docs/GLOSSARY.md](../../docs/GLOSSARY.md).", "",
         f"Engine `{head[:9]}` — OBSERVATIONAL, pre-registered "
         "(prereg_capture_study, register 88 item 4). THE QUESTION: "
         "when a trade has shown +X, what protection maximizes "
         "kept-points per family x session x tape-character? "
         "MOTIVATING OBSERVATION: the register-87 breakeven continent "
         "split (+2.9k EU / -15.8k US at rung 0.25). EXPECTED "
         "OUTCOME, stated at commissioning: SCOPED POLICIES, NOT "
         "UNIVERSAL RULES — and no policy registers without its own "
         "Q-number and forward grade. STATISTIC SHAPES (74-B): "
         "per-policy per-cell net-delta vs the B-RANDOM member band "
         "under the identical policy (floor pattern); tape "
         "differentiation = field count vs permutation null "
         f"({NULL_SHUFFLES} pinned seeds; gap >= {GAP_MIN_PTS:g} pts "
         "per trade, threshold FLAGGED). Base = the "
         f"{BASE_VARIANT} slice ex-lockbox ({n_all} trades). "
         "Settled arming, touch fills (register-87 conventions). "
         f"° = n<{MIN_CELL_N}.", ""]
    for instr, res in sorted(art["per_instrument"].items()):
        lb = res["luck_budget"]
        L += [f"## {instr} ({res['n_base']} base trades)", "",
              f"**Luck budget:** {lb['observed']} measurable "
              "quiet/loud pairs differentiate at >= "
              f"{GAP_MIN_PTS:g} pts/trade vs null median "
              f"{lb['null_median']:g} / p95 {lb['null_p95']:g} "
              f"(percentile {lb['percentile_vs_null']}).", "",
              "### Policy totals (net delta vs actual, all base "
              "trades; floor = member band)", "",
              "| policy | net delta | floor med (min..max) |",
              "|---|---|---|"]
        for pname, net in res["policy_totals"].items():
            fb = res["floors"][pname]
            L.append(f"| {pname} | {net} | {fb['median']} "
                     f"({fb['min']}..{fb['max']}) |")
        L += ["", "### Regime split — PHASE-AT-ENTRY (register 90 "
              "item 1, re-registered by operator ruling: the "
              "enrichment convention, 1M phase at the fire bar; the "
              "generalize-vs-geography test — if trails clear on "
              "trending entries regardless of continent, the scope "
              "generalizes)", "",
              "| regime | n | best policy | best net delta | BE@0.25 "
              "net delta |", "|---|---|---|---|---|"]
        for reg, per in sorted(res["phase_regime_split"].items()):
            best = max(per, key=lambda k: per[k]["net_delta"])
            n_ = per[best]["n"]
            dim = "°" if n_ < MIN_CELL_N else ""
            L.append(f"| {reg} | {dim}{n_} | {best} "
                     f"| {per[best]['net_delta']} "
                     f"| {per['BE@0.25']['net_delta']} |")
        L += ["", "### Day-level regime cut — the RECORDED FIRST "
              "ATTEMPT (register 89/90: saturation finding — 98% of "
              "days classified trending on three legs, no contrast "
              "available; stands as history, superseded as the "
              "regime lens)", "",
              "| regime | n | best policy | best net delta | BE@0.25 "
              "net delta |", "|---|---|---|---|---|"]
        for reg, per in sorted(
                res["day_regime_split_first_attempt"].items()):
            best = max(per, key=lambda k: per[k]["net_delta"])
            n_ = per[best]["n"]
            dim = "°" if n_ < MIN_CELL_N else ""
            L.append(f"| {reg} | {dim}{n_} | {best} "
                     f"| {per[best]['net_delta']} "
                     f"| {per['BE@0.25']['net_delta']} |")
        L += ["", "### NEVER-AGAIN pricing (register 89 item 1: the "
              f"cost of guaranteeing no trade exceeds "
              f"+{NEVER_AGAIN_BOUND_ATR:g}xATR MFE unprotected — a "
              "risk-rule pricing, separable from the edge question; "
              "guarantee holds up to the register-87 single-bar span "
              "exception). FIAT DEFERRED (register 90 item 2, "
              "operator ruling: option c) — NOT ENACTED at any "
              "scope; the per-cell grid may deliver the guarantee as "
              "a byproduct of scoped policies; this table stands as "
              "the decision's evidence base, revisit when cells "
              "measure; the +216 class remains possible in the "
              "interim — accepted, dated.", "",
              "| rung | qualifies | winners amputated | amputation "
              "pts | per 100 trades |", "|---|---|---|---|---|"]
        for name, d_ in sorted(res["never_again"].items(),
                               key=lambda x: x[1]["rung_atr"]):
            q = ("YES" if d_["qualifies"]
                 else "NO (above the bound)")
            L.append(f"| {name} | {q} | {d_['winners_amputated']} "
                     f"| {d_['amputation_pts_total']} "
                     f"| {d_['amputation_pts_per_100_trades']} |")
        L += ["", "### Best policy per cell (measurable cells; full "
              "grid in the JSON)", "",
              "| family | session | tape | n | best policy | best "
              "net delta | median kept |", "|---|---|---|---|---|---|"
              "---|"]
        for key, c in sorted(res["cells"].items()):
            if c["n"] < MIN_CELL_N:
                continue
            fam, sess, tape = key.split("|")
            bp = c["policies"][c["best_policy"]]
            L.append(f"| {fam} | {sess} | {tape} | {c['n']} "
                     f"| {c['best_policy']} | {c['best_net_delta']} "
                     f"| {bp['median_kept_pts']} |")
        L.append("")
    with open(os.path.join(OUT, "capture_study.md"), "w") as f:
        f.write("\n".join(L))


if __name__ == "__main__":
    main()
