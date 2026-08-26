"""Underwater census + thesis-campaign study (register 87;
pre-registered prereg_underwater_census + prereg_thesis_campaign,
counted 2026-08-28). Loser-cutting and the operator's trading loop,
MEASURED — the flip-cut precedent (register 44) governs: measurement
before machinery, and no cut/BE/re-entry/backoff rule registers
without its own Q-number and forward grade.

PART 1 — WHERE LOSSES LIVE. Per journal trade on the *fut 1M path:
bars-to-first-positive-close (close-based, direction-adjusted; 1 =
entry bar closes positive); MAE at bars 1..10 in xATR(15M at entry);
register-66 quadrant per underwater bar (loud = rel_volume >= the
founding 1.5 cut); path class winner-clean / winner-after-underwater /
loser-never-positive / loser-after-positive (scratches counted apart).
(a) four-class loss decomposition (the early-cut theoretical maximum
is the loser-never-positive share, stated as such); (b) survival
curves P(win | still underwater at bar k) with n at every k — the
operator's motivating hypothesis ("winners become positive within 2
bars") is RECORDED and graded by the curve, never assumed; (c) the
discrimination frontier (separation vs residual avoidable loss by k);
(d) quiet-dip vs loud-dip conditional win rates (the in-trade VSA
question, stated as motivation: a quiet dip is the story breathing, a
loud dip is the story changing — the numbers decide); (e) the
counterfactual rule ladder (cut@k in {2,3,5}; cut-if-underwater-AND-
loud; cut@MAE>{0.5,1.0}xATR in the 10-bar window).

PART 2 — THE BREAKEVEN LADDER + RE-ENTRY (operator practice recorded:
fast BE, re-enter on the next setup; R-BE's scratch-machine record and
the register-42d literature caution stand as opposing evidence; this
census arbitrates). (f) BE at +{0.25,0.5,1.0,1.5}xATR MFE on the
R-NOTRAIL base; the NEVER-AGAIN table: max MFE of eventual losers per
rung — which rung makes the +216-class structurally impossible, and
at what amputation cost. (g) re-entry measured on the UNDEDUPED fire
stream (the 5-bar dedup hides the near re-fires — stated); the
complete policy BE@0.25 + re-enter vs hold-through, doubled spread.

PART 3 — THE THESIS-CAMPAIGN STUDY (artifact named thesis_campaign:
the name "campaign" collides with the weekly pipeline, stated).
Thesis v1 = the 15M phase-tracker trend state (existing instrument);
v2 candidate states (sentence-family states) RECORDED, NOT BUILT.
Invalidation = the state flipping. Probes = journal fires agreeing
with the live thesis, one position at a time, per the operator loop;
random-direction theses on the SAME campaign windows are the
MANDATORY control (sticky random theses in a trending month look
clever — the stated confound). (iii) the attribution ladder
one-shot -> +BE -> +re-entry; (iv) the backoff grid with the
abstained counterfactual (backoff's price) mandatory.

FILL CONVENTIONS (register 65 discipline, declared): journal points
are PESSIMISTIC and carry spread once. Counterfactuals run on the
census's array-walk probe simulator — stop 2.5xATR touch-fill, BE
armed on SETTLED favorable excursion (arming bar excluded from the
touch), BE fill at entry, EOD close-fill, thesis-flip close-fill;
bar-count cuts are close-fill; MAE-threshold cuts are touch-fill at
the threshold (OPTIMISTIC class — within-ladder comparisons only).
The simulator's no-BE outcomes reconcile against the journal's
R-NOTRAIL rows (drift stat printed in the header).

Ex-lockbox throughout (register 85), both windows, all instruments,
sealed skipped and counted, zone reconciliation in every header,
twin-run pinned (tests/test_underwater_census.py), statistic shapes
per 74-B in each section. Weekly under Part C after first emission.
Nothing here changes any live recipe, label, or signal.
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

from engine.signal_watch import AGNOSTIC_ROWS, SignalWatch
from engine.store_loader import (in_lockbox_span, is_sealed,
                                 lockbox_boundary, zones)
from backtest.narrative_survey import _SurveyRecorder
from backtest.recipes import (RECIPE_SET_VERSION, RECIPE_SETS,
                              _spread_median, build_env, simulate)
from backtest.scoreboard import _replay, event_derived_fires, make_cfg
from backtest.signal_points import baseline_fires

OUT = os.path.join(ROOT, "reports", "scoreboard")
TRADES_CSV = os.path.join(ROOT, "reports", "trades.csv")

TRAJ_BARS = 10               # trajectory window (order-stated)
CUT_KS = (2, 3, 5)           # bars-underwater cut grid (order-stated)
MAE_CUTS_ATR = (0.5, 1.0)    # MAE cut grid (order-stated)
BE_RUNGS_ATR = (0.25, 0.5, 1.0, 1.5)   # BE ladder (order-stated)
REENTRY_WINDOWS_MIN = (15, 30, 60)     # re-fire windows (order-stated)
BACKOFF_KS = (2, 3)          # consecutive-failure grid (order-stated)
BACKOFF_WS = (5, 15, 30)     # suppression bars (order-stated)
LOOP_RUNG_ATR = 0.25         # the operator's fast BE (loop + backoff
                             # grids run here; other rungs flagged)
STOP_ATR = 2.5               # the registered ladder-v2 initial stop
LOUD_MULT = 1.5              # register 66 founding volume cut
MIN_CELL_N = 25              # measurability convention
REF_K = 3                    # declared reference bar for the nulls
SPLIT_MIN_PP = 10.0          # qualifying gap (register 84 convention)
NULL_SHUFFLES = 100
NULL_SEEDS = tuple(range(NULL_SHUFFLES))
THESIS_SEEDS = tuple(range(60, 80))    # 20 members (B-RANDOM lineage)
BASE_VARIANT = "R-NOTRAIL"   # the unmanaged full-hold base (declared)

# full-coverage family map — extends the registered cofire/trend
# groupings; implementer-proposed at prereg, FLAGGED. (Guarded
# single-digit identifiers built with f-strings per the register-31
# identifier guard — the trade-layer precedent.)
FAMILY_OF = {"S0-H1": "event", "S0-H2": "event", "S1-H1": "event",
             "S1-H2": "event", "S0-H4": "texture",
             f"S0-H{7}": "texture", "S0-H3": "structure",
             f"S0-H{9}": "structure", f"S1-H{9}": "structure",
             "S0-H10": "trend", "S0-H14": "trend", "S0-H11": "map",
             "S1-H11": "map", "S0-H13": "map", f"S0-H{6}": "retest",
             "S0-H5": "event-derived", "S0-H16": "event-derived",
             "S0-H17": "composite", "S0-H18": "composite",
             "S0-H19": "composite"}


# ----------------------------------------------------------- instrument

def build_instrument(instr):
    """One replay: arrays + undeduped fire stream + journal join keys."""
    cfg = make_cfg({"session_model.extended_hours": True,
                    "session_model.ladder": True,
                    "debug.structure": True})
    watch = SignalWatch()
    rec = _SurveyRecorder()

    def _hook(engine):
        watch.attach(engine)
        rec.attach(engine)
    engine, bars, _ = _replay(cfg, instr, engine_hook=_hook)
    env = build_env(instr, cfg, bars)
    ts = env.ts
    getm = rec.map.get
    loud = np.array([(getm(t, (None,) * 4)[1] or 0) >= LOUD_MULT
                     if t in rec.map else False for t in ts])
    eff_dir = np.array([{"EFFORTLESS_ADVANCE": 1,
                         "EFFORTLESS_DECLINE": -1}.get(
                            getm(t, (None,) * 4)[2], 0) for t in ts])
    t15_map = {}
    for e in engine.narrative.events:
        if e["type"] == "PHASE_EVAL" and e.get("tf") == "15min":
            t15_map[pd.Timestamp(e["ts"]).value] = e.get("trend", 0)
    keys = np.array(sorted(t15_map))
    vals = np.array([t15_map[k] for k in sorted(t15_map)] or [0])
    idx = np.searchsorted(keys, ts, side="right") - 1
    t15 = np.where(idx >= 0, vals[np.maximum(idx, 0)], 0)
    fires = watch.fires + event_derived_fires(engine.narrative.events,
                                              cfg, bars, instr=instr)
    undeduped = {}
    for f in fires:
        if f["name"] in AGNOSTIC_ROWS or is_sealed(f["ts"]):
            continue
        undeduped.setdefault(f["name"], []).append(
            (f["ts"].value, int(f["dir"])))
    for v in undeduped.values():
        v.sort()
    return {"env": env, "ts": ts, "o": env.o, "h": env.h, "l": env.l,
            "c": env.c, "eod": env.eod, "loud": loud,
            "eff_dir": eff_dir, "t15": np.sign(t15).astype(int),
            "undeduped": undeduped, "spread": _spread_median(instr),
            "engine_events": engine.narrative.events, "cfg": cfg}


# ---------------------------------------------------- pure path helpers

def trajectory(ei, xi, d, entry, atr0, h, l, c, loud):
    """Per-trade underwater profile over the hold [ei, xi]."""
    rel_c = (c[ei:xi + 1] - entry) * d
    adv = ((entry - l[ei:xi + 1]) if d == 1
           else (h[ei:xi + 1] - entry))
    pos = np.nonzero(rel_c > 0)[0]
    first_pos = int(pos[0]) + 1 if len(pos) else None    # 1-based bars
    mae_run = np.maximum.accumulate(np.maximum(adv, 0.0))
    mae_by_bar = [round(float(mae_run[k - 1]) / atr0, 3)
                  if atr0 and k <= len(mae_run) else None
                  for k in range(1, TRAJ_BARS + 1)]
    uw_end = (first_pos - 1) if first_pos else len(rel_c)
    loud_uw = loud[ei:ei + uw_end]
    neg_uw = rel_c[:uw_end] < 0
    loud_dip = np.nonzero(loud_uw & neg_uw)[0]
    return {"bars": len(rel_c), "first_pos": first_pos,
            "mae_by_bar": mae_by_bar, "rel_c": rel_c, "adv": adv,
            "first_loud_dip": (int(loud_dip[0]) if len(loud_dip)
                               else None)}


def path_class(pts, spread, first_pos):
    if abs(pts) < spread:
        return "scratch"
    if pts > 0:
        return "winner-clean" if first_pos == 1 else \
            "winner-after-underwater"
    return "loser-after-positive" if first_pos else \
        "loser-never-positive"


def underwater_at(traj, k):
    """Still open at bar k with no positive close among the first k."""
    return traj["bars"] >= k and (traj["first_pos"] is None
                                  or traj["first_pos"] > k)


def cut_counterfactuals(t, spread, atr0):
    """Rule -> counterfactual pts (None = rule never triggers; the
    actual outcome stands). Bar-count/loud cuts close-fill; MAE cuts
    touch-fill at threshold (OPTIMISTIC, declared)."""
    traj, pts = t["traj"], t["pts"]
    out = {}
    for k in CUT_KS:
        out[f"cut@{k}"] = (
            float(traj["rel_c"][k - 1] - spread)
            if underwater_at(traj, k) else None)
    j = traj["first_loud_dip"]
    out["cut-loud"] = (float(traj["rel_c"][j] - spread)
                       if j is not None else None)
    for m in MAE_CUTS_ATR:
        if atr0:
            w = traj["adv"][:TRAJ_BARS]
            hit = np.nonzero(w >= m * atr0)[0]
            out[f"cut-mae{m:g}"] = (float(-m * atr0 - spread)
                                    if len(hit) else None)
        else:
            out[f"cut-mae{m:g}"] = None
    return out


def survival_curve(trades):
    out = []
    for k in range(1, TRAJ_BARS + 1):
        uw = [t for t in trades if underwater_at(t["traj"], k)]
        wins = sum(1 for t in uw if t["pts"] > 0)
        out.append({"k": k, "n": len(uw),
                    "p_win": (round(wins / len(uw), 3) if uw
                              else None)})
    return out


# ------------------------------------------------------ probe simulator

def probe_sim(ei, d, entry, atr0, A, rung, end_idx):
    """Array-walk probe: stop STOP_ATR touch-fill; BE armed on settled
    favorable excursion (>= rung x ATR), fill at entry on a later
    touch; EOD close-fill; end_idx (thesis flip / window end)
    close-fill. Deterministic. Returns (exit_idx, pts, reason)."""
    h, l, c, eod = A["h"], A["l"], A["c"], A["eod"]
    stop_px = entry - d * STOP_ATR * (atr0 or 0)
    armed = False
    fav = 0.0
    j = ei
    last = min(end_idx, len(c) - 1)
    while j <= last:
        adv_ext = (entry - l[j]) if d == 1 else (h[j] - entry)
        if atr0 and adv_ext >= STOP_ATR * atr0:
            return j, float((stop_px - entry) * d - A["spread"]), "stop"
        if armed and adv_ext >= 0.0:
            return j, float(-A["spread"]), "scratch"
        if eod[j]:
            return j, float((c[j] - entry) * d - A["spread"]), "eod"
        fav = max(fav, (h[j] - entry) if d == 1 else (entry - l[j]))
        if rung is not None and atr0 and not armed \
                and fav >= rung * atr0:
            armed = True          # settled: touch active from next bar
        j += 1
    j = last
    return j, float((c[j] - entry) * d - A["spread"]), "flip"


# ------------------------------------------------------ thesis campaigns

def campaigns_of(t15):
    """Maximal constant-direction nonzero episodes: (start, end, dir);
    end exclusive."""
    out = []
    s = None
    for i in range(len(t15)):
        if s is None:
            if t15[i] != 0:
                s = i
        elif t15[i] != t15[s]:
            out.append((s, i, int(t15[s])))
            s = i if t15[i] != 0 else None
    if s is not None:
        out.append((s, len(t15), int(t15[s])))
    return out


def run_campaign(camp, fires, A, rung, reentry=True, backoff=None):
    """One thesis-campaign walk. fires: [(ei, d, entry, atr0)] sorted,
    agreeing direction only. backoff: None | (k, W) | (k, 'print').
    Returns per-campaign accounting incl the abstained counterfactual."""
    s, e, dth = camp
    probes = []
    suppressed = []
    consec = 0
    resume_idx = -1
    need_print = False
    cur_exit = -1
    for (ei, d, entry, atr0) in fires:
        if ei < s or ei >= e or ei <= cur_exit:
            continue
        if not probes and cur_exit == -1:
            pass                          # first probe always allowed
        elif not reentry:
            break
        blocked = ei < resume_idx
        if need_print:
            w = np.nonzero(A["eff_dir"][max(cur_exit, s):ei]
                           == dth)[0]
            blocked = not len(w)
        if blocked:
            xj, pts, reason = probe_sim(ei, d, entry, atr0, A, rung,
                                        e - 1)
            suppressed.append({"pts": pts, "reason": reason})
            continue
        need_print = False
        xj, pts, reason = probe_sim(ei, d, entry, atr0, A, rung, e - 1)
        probes.append({"pts": pts, "reason": reason,
                       "caught": reason == "flip" and pts > 0})
        cur_exit = xj
        if reason in ("scratch", "stop"):
            consec += 1
        else:
            consec = 0
        if backoff and consec >= backoff[0]:
            if backoff[1] == "print":
                need_print = True
            else:
                resume_idx = xj + backoff[1]
            consec = 0
    net = round(float(sum(p["pts"] for p in probes)), 2)
    run = np.cumsum([p["pts"] for p in probes]) if probes else [0.0]
    dd = round(float(np.max(np.maximum.accumulate(run) - run)), 2) \
        if probes else 0.0
    return {"probes": len(probes), "net": net, "max_dd": dd,
            "scratches": sum(1 for p in probes
                             if p["reason"] == "scratch"),
            "stops": sum(1 for p in probes if p["reason"] == "stop"),
            "caught": sum(1 for p in probes if p["caught"]),
            "caught_pts": round(float(sum(
                p["pts"] for p in probes if p["caught"])), 2),
            "suppressed": len(suppressed),
            "suppressed_losses_avoided": round(float(-sum(
                x["pts"] for x in suppressed if x["pts"] < 0)), 2),
            "suppressed_winners_missed": round(float(sum(
                x["pts"] for x in suppressed if x["pts"] > 0)), 2)}


# ---------------------------------------------------------------- main

def load_journal():
    rows = list(csv.DictReader(open(TRADES_CSV)))
    keep = [r for r in rows if not in_lockbox_span(r["open_ts"])
            and not is_sealed(pd.Timestamp(r["open_ts"]))]
    return rows, keep


def join_trades(rows, A):
    """Journal rows -> trade dicts with trajectories (ex-lockbox)."""
    ts = A["ts"]
    out = []
    for r in rows:
        open_ts = pd.Timestamp(r["open_ts"])
        ei = int(np.searchsorted(ts, open_ts.value, side="left"))
        if ei >= len(ts) or ts[ei] != open_ts.value:
            continue
        xi = int(np.searchsorted(
            ts, pd.Timestamp(r["close_ts"]).value, side="left"))
        xi = min(xi, len(ts) - 1)
        d = int(r["direction"])
        entry = float(r["open_price"])
        atr0 = (float(r["atr_entry"])
                if r["atr_entry"] not in ("", "None", None) else None)
        traj = trajectory(ei, xi, d, entry, atr0, A["h"], A["l"],
                          A["c"], A["loud"])
        fav = ((A["h"][ei:xi + 1] - entry) if d == 1
               else (entry - A["l"][ei:xi + 1]))
        out.append({"r": r, "ei": ei, "xi": xi, "d": d,
                    "entry": entry, "atr0": atr0,
                    "pts": float(r["points"]), "traj": traj,
                    "mfe_path": fav,
                    "family": FAMILY_OF.get(r["sentence_id"], "other"),
                    "cls": path_class(float(r["points"]), A["spread"],
                                      traj["first_pos"])})
    return out


def be_outcome(t, spread, rung):
    """Counterfactual outcome under BE rung on the actual hold: armed
    on settled favorable excursion, entry-touch fill on a LATER bar.
    Returns (pts, triggered, mfe_atr)."""
    atr0 = t["atr0"]
    fav = np.maximum.accumulate(np.maximum(t["mfe_path"], 0.0))
    mfe_atr = (round(float(fav[-1]) / atr0, 3)
               if atr0 and len(fav) else None)
    if not atr0:
        return t["pts"], False, mfe_atr
    armed = np.nonzero(fav >= rung * atr0)[0]
    if not len(armed):
        return t["pts"], False, mfe_atr
    a = int(armed[0])
    touch = np.nonzero(t["traj"]["adv"][a + 1:] >= 0.0)[0]
    if not len(touch):
        return t["pts"], False, mfe_atr
    return float(-spread), True, mfe_atr


def ladder_floors(A):
    """B-RANDOM members under the BASE_VARIANT recipe, ex-lockbox,
    with the identical rule/rung ladders applied — the mandatory
    baselines. Returns per-rule and per-rung member NET-DELTA bands."""
    recipe = RECIPE_SETS[RECIPE_SET_VERSION][BASE_VARIANT]
    members = baseline_fires(A["env"], A["engine_events"])["B-RANDOM"]
    ts = A["ts"]
    rule_nets, rung_nets = {}, {}
    for mf in members:
        trades = []
        for t in simulate(mf, A["env"], recipe, A["spread"]):
            if in_lockbox_span(t["entry_ts"]):
                continue
            ei = int(np.searchsorted(
                ts, pd.Timestamp(t["entry_ts"]).value, side="left"))
            xi = min(len(ts) - 1,
                     ei + int(t["duration_min"]))
            d = t["dir"]
            entry = t["entry"]
            atr0 = A["env"].atr_at(
                "15min", pd.Timestamp(t["entry_ts"]).value)
            traj = trajectory(ei, xi, d, entry, atr0, A["h"], A["l"],
                              A["c"], A["loud"])
            fav = ((A["h"][ei:xi + 1] - entry) if d == 1
                   else (entry - A["l"][ei:xi + 1]))
            trades.append({"pts": t["pts"], "traj": traj,
                           "atr0": atr0, "mfe_path": fav})
        m_rule = {}
        for t in trades:
            for rule, cf in cut_counterfactuals(
                    t, A["spread"], t["atr0"]).items():
                if cf is not None:
                    m_rule[rule] = m_rule.get(rule, 0.0) \
                        + (cf - t["pts"])
        for rule, v in m_rule.items():
            rule_nets.setdefault(rule, []).append(round(v, 1))
        for rung in BE_RUNGS_ATR:
            v = 0.0
            for t in trades:
                cf, _trig, _m = be_outcome(t, A["spread"], rung)
                v += cf - t["pts"]
            rung_nets.setdefault(f"{rung:g}", []).append(round(v, 1))

    def band(d_):
        return {k: {"members": len(v),
                    "median": round(float(np.median(v)), 1),
                    "min": round(float(min(v)), 1),
                    "max": round(float(max(v)), 1)}
                for k, v in sorted(d_.items())}
    return band(rule_nets), band(rung_nets)


def label_nulls(base, loud, fams):
    """Luck budget (declared at prereg): win/loss labels permuted
    within family x session strata (BASE_VARIANT slice), 100 pinned
    seeds. Field statistics at the reference bar k=REF_K: count of
    measurable family cells with separation >= SPLIT_MIN_PP, and with
    |quiet-loud gap| >= SPLIT_MIN_PP."""
    def stats(labels):
        n_sep = n_gap = 0
        for fam in fams:
            idx = [i for i, t in enumerate(base)
                   if t["family"] == fam]
            if not idx:
                continue
            uw = [i for i in idx if underwater_at(base[i]["traj"],
                                                  REF_K)]
            if len(uw) < MIN_CELL_N:
                continue
            p_loss = np.mean([not labels[i] for i in idx])
            pl_k = np.mean([not labels[i] for i in uw])
            if 100 * (pl_k - p_loss) >= SPLIT_MIN_PP:
                n_sep += 1
            lo = [i for i in uw if loud[base[i]["ei"] + REF_K - 1]]
            qt = [i for i in uw if not loud[base[i]["ei"] + REF_K - 1]]
            if len(lo) >= 10 and len(qt) >= 10:
                gap = 100 * (np.mean([labels[i] for i in qt])
                             - np.mean([labels[i] for i in lo]))
                if abs(gap) >= SPLIT_MIN_PP:
                    n_gap += 1
        return n_sep, n_gap
    obs = stats([t["pts"] > 0 for t in base])
    strata = {}
    for i, t in enumerate(base):
        strata.setdefault((t["family"], t["r"]["session"]),
                          []).append(i)
    null_sep, null_gap = [], []
    labels0 = [t["pts"] > 0 for t in base]
    for seed in NULL_SEEDS:
        rs = np.random.RandomState(seed)
        lab = list(labels0)
        for idxs in strata.values():
            perm = rs.permutation(len(idxs))
            vals = [labels0[idxs[j]] for j in perm]
            for j, i in enumerate(idxs):
                lab[i] = vals[j]
        s_, g_ = stats(lab)
        null_sep.append(s_)
        null_gap.append(g_)

    def budget(o, nd):
        return {"observed": o,
                "null_median": float(np.median(nd)),
                "null_p95": float(np.percentile(nd, 95)),
                "percentile_vs_null": round(
                    100 * float(np.mean([o > m for m in nd])), 1)}
    return {"separation_at_k": budget(obs[0], null_sep),
            "volume_gap_at_k": budget(obs[1], null_gap)}


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
    census = {}
    camp_art = {}
    for instr in a.instr:
        print(f"# underwater_census: {instr} ...", file=sys.stderr)
        A = build_instrument(instr)
        rows = [r for r in kept_rows if r["instrument"] == instr]
        trades = join_trades(rows, A)
        base = [t for t in trades if t["r"]["variant"] == BASE_VARIANT]
        res = {"n_journal": sum(1 for r in all_rows
                                if r["instrument"] == instr),
               "n_used": len(trades), "spread": A["spread"]}
        # (a) four-class loss decomposition + (b)/(c)/(d) per family
        fam_grid = {}
        for fam in sorted({t["family"] for t in base}):
            ft = [t for t in base if t["family"] == fam]
            losses = [t for t in ft if t["cls"].startswith("loser")]
            tot_loss = -sum(t["pts"] for t in losses)
            cls_loss = {}
            for c_ in ("loser-never-positive", "loser-after-positive"):
                cl = -sum(t["pts"] for t in ft if t["cls"] == c_)
                cls_loss[c_] = {"loss_pts": round(cl, 1),
                                "share": (round(cl / tot_loss, 3)
                                          if tot_loss else None),
                                "n": sum(1 for t in ft
                                         if t["cls"] == c_)}
            wins = [t for t in ft if t["pts"] > 0]
            within2 = (round(sum(
                1 for t in wins if t["traj"]["first_pos"] is not None
                and t["traj"]["first_pos"] <= 2) / len(wins), 3)
                if wins else None)
            curve = survival_curve(ft)
            p_loss = (sum(1 for t in ft if t["pts"] < 0) / len(ft)
                      if ft else None)
            frontier = []
            for k in range(1, TRAJ_BARS + 1):
                uw = [t for t in ft if underwater_at(t["traj"], k)]
                if not uw or p_loss is None:
                    frontier.append({"k": k, "n": 0})
                    continue
                pl_k = sum(1 for t in uw if t["pts"] < 0) / len(uw)
                avoid = -sum(
                    float(t["pts"] - (t["traj"]["rel_c"][k - 1]
                                      - A["spread"]))
                    for t in uw if t["pts"] < 0)
                frontier.append({
                    "k": k, "n": len(uw),
                    "separation_pp": round(100 * (pl_k - p_loss), 1),
                    "residual_avoidable_pts": round(avoid, 1)})
            vol_split = []
            for k in range(1, TRAJ_BARS + 1):
                uw = [t for t in ft if underwater_at(t["traj"], k)
                      and t["traj"]["bars"] >= k]
                lo = [t for t in uw if A["loud"][t["ei"] + k - 1]]
                qt = [t for t in uw if not A["loud"][t["ei"] + k - 1]]
                vol_split.append({
                    "k": k, "n_loud": len(lo), "n_quiet": len(qt),
                    "p_win_loud": (round(sum(
                        1 for t in lo if t["pts"] > 0) / len(lo), 3)
                        if lo else None),
                    "p_win_quiet": (round(sum(
                        1 for t in qt if t["pts"] > 0) / len(qt), 3)
                        if qt else None)})
            # (e) rule ladder
            ladder = {}
            for t in ft:
                cfs = cut_counterfactuals(t, A["spread"], t["atr0"])
                for rule, cf in cfs.items():
                    d_ = ladder.setdefault(rule, {
                        "n_trig": 0, "saved_on_losers": 0.0,
                        "amputated_from_winners": 0.0, "net": 0.0})
                    if cf is None:
                        continue
                    delta = cf - t["pts"]
                    d_["n_trig"] += 1
                    d_["net"] += delta
                    if t["pts"] < 0:
                        d_["saved_on_losers"] += delta
                    elif t["pts"] > 0:
                        d_["amputated_from_winners"] += delta
            for d_ in ladder.values():
                for k_ in ("saved_on_losers", "amputated_from_winners",
                           "net"):
                    d_[k_] = round(d_[k_], 1)
            fam_grid[fam] = {
                "n": len(ft), "loss_decomposition": cls_loss,
                "winners_positive_within_2_bars": within2,
                "survival": curve, "frontier": frontier,
                "volume_split": vol_split, "rule_ladder": ladder}
        # (f) BE ladder + never-again, on the base variant
        be = {}
        for rung in BE_RUNGS_ATR:
            agg = {"scratches_created": 0, "winners_amputated": 0,
                   "amputated_pts": 0.0, "losses_capped": 0,
                   "capped_pts_saved": 0.0, "net_delta": 0.0,
                   "max_mfe_of_losers_atr": 0.0,
                   "max_mfe_of_losers_pts": 0.0}
            for t in base:
                cf, trig, mfe_atr = be_outcome(t, A["spread"], rung)
                delta = cf - t["pts"]
                agg["net_delta"] += delta
                if trig:
                    agg["scratches_created"] += 1
                    if t["pts"] > 0:
                        agg["winners_amputated"] += 1
                        agg["amputated_pts"] += -delta
                    elif t["pts"] < 0:
                        agg["losses_capped"] += 1
                        agg["capped_pts_saved"] += delta
                elif cf < 0 and mfe_atr is not None:
                    if mfe_atr > agg["max_mfe_of_losers_atr"]:
                        agg["max_mfe_of_losers_atr"] = mfe_atr
                        agg["max_mfe_of_losers_pts"] = round(
                            mfe_atr * (t["atr0"] or 0), 1)
            for k_ in ("amputated_pts", "capped_pts_saved",
                       "net_delta"):
                agg[k_] = round(agg[k_], 1)
            be[f"{rung:g}"] = agg
        # (g) re-entry on the undeduped stream, BE@LOOP_RUNG
        reent = {"windows": {}, "policy": {}}
        scr = []
        for t in base:
            cf, trig, _m = be_outcome(t, A["spread"], LOOP_RUNG_ATR)
            if trig:
                scr.append(t)
        for w in REENTRY_WINDOWS_MIN:
            hit = 0
            for t in scr:
                exit_ns = A["ts"][t["xi"]]
                nxt = [x for x, _d in A["undeduped"].get(
                    t["r"]["sentence_id"], [])
                    if exit_ns < x <= exit_ns + w * 60_000_000_000]
                hit += bool(nxt)
            reent["windows"][w] = {
                "n_scratched": len(scr), "n_refire": hit,
                "refire_rate": (round(hit / len(scr), 3)
                                if scr else None)}
        census.setdefault(instr, {}).update(res)
        census[instr]["families"] = fam_grid
        census[instr]["be_ladder"] = be
        census[instr]["reentry"] = reent
        census[instr]["n_scratched_loop_rung"] = len(scr)
        rule_floors, rung_floors = ladder_floors(A)
        census[instr]["ladder_floors"] = {"rules": rule_floors,
                                          "rungs": rung_floors}
        census[instr]["luck_budget"] = label_nulls(
            base, A["loud"], sorted({t["family"] for t in base}))
        # ---- Part 3: thesis campaigns
        camps_all = campaigns_of(A["t15"])
        lb_lo = np.searchsorted(A["ts"], lockbox_boundary().value)
        lb_hi = np.searchsorted(A["ts"], zones()["go_live"].value)
        camps = [c_ for c_ in camps_all
                 if c_[1] <= lb_lo or c_[0] >= lb_hi]
        n_dropped = len(camps_all) - len(camps)
        fires = sorted(
            (t["ei"], t["d"], t["entry"], t["atr0"]) for t in base)
        pol = {}
        for rung in BE_RUNGS_ATR:
            per = [run_campaign(c_, [f for f in fires
                                     if f[1] == c_[2]], A, rung)
                   for c_ in camps]
            pol[f"loop_be{rung:g}"] = per
        pol["oneshot_nobe"] = [run_campaign(
            c_, [f for f in fires if f[1] == c_[2]], A, None,
            reentry=False) for c_ in camps]
        pol["oneshot_be"] = [run_campaign(
            c_, [f for f in fires if f[1] == c_[2]], A,
            LOOP_RUNG_ATR, reentry=False) for c_ in camps]
        for bk in BACKOFF_KS:
            for bw in list(BACKOFF_WS) + ["print"]:
                pol[f"backoff_k{bk}_" + (f"w{bw}"
                                         if bw != "print"
                                         else "print")] = [
                    run_campaign(c_, [f for f in fires
                                      if f[1] == c_[2]], A,
                                 LOOP_RUNG_ATR, backoff=(bk, bw))
                    for c_ in camps]
        # random-thesis controls (same windows, member directions)
        rand_nets = {}
        for seed in THESIS_SEEDS:
            rs = np.random.RandomState(seed)
            dirs = rs.choice([-1, 1], size=len(camps))
            per = [run_campaign((c_[0], c_[1], int(dirs[i])),
                                [f for f in fires
                                 if f[1] == int(dirs[i])], A,
                                LOOP_RUNG_ATR)
                   for i, c_ in enumerate(camps)]
            rand_nets[seed] = round(float(sum(p["net"] for p in per)),
                                    1)
        def _agg(per):
            return {"campaigns": len(per),
                    "probes": int(sum(p["probes"] for p in per)),
                    "net": round(float(sum(p["net"] for p in per)), 1),
                    "scratches": int(sum(p["scratches"]
                                         for p in per)),
                    "stops": int(sum(p["stops"] for p in per)),
                    "caught": int(sum(p["caught"] for p in per)),
                    "caught_pts": round(float(sum(
                        p["caught_pts"] for p in per)), 1),
                    "max_campaign_dd": (round(float(max(
                        p["max_dd"] for p in per)), 1) if per
                        else None),
                    "suppressed": int(sum(p["suppressed"]
                                          for p in per)),
                    "supp_losses_avoided": round(float(sum(
                        p["suppressed_losses_avoided"]
                        for p in per)), 1),
                    "supp_winners_missed": round(float(sum(
                        p["suppressed_winners_missed"]
                        for p in per)), 1)}
        band = sorted(rand_nets.values())
        camp_art[instr] = {
            "n_campaigns_total": len(camps_all),
            "n_campaigns_lockbox_dropped": n_dropped,
            "n_campaigns_used": len(camps),
            "policies": {k: _agg(v) for k, v in pol.items()},
            "random_thesis_net_band": {
                "members": len(band),
                "median": (round(float(np.median(band)), 1)
                           if band else None),
                "min": band[0] if band else None,
                "max": band[-1] if band else None}}
    art = {"STAMP": ("OBSERVATIONAL underwater census — measurement "
                     "before machinery (flip-cut precedent, register "
                     "44); no cut/BE/re-entry/backoff rule registers "
                     "without its own Q-number and forward grade; "
                     "never validation"),
           "engine_commit": head,
           "conventions": {
               "base_variant": BASE_VARIANT, "stop_atr": STOP_ATR,
               "loud_mult": LOUD_MULT, "traj_bars": TRAJ_BARS,
               "fills": ("bar-close for bar-count cuts; touch=fill "
                         "for MAE cuts (OPTIMISTIC, in-ladder only); "
                         "BE armed settled, entry-touch fill")},
           "per_instrument": census}
    with open(os.path.join(OUT, "underwater_census.json"), "w") as f:
        json.dump(art, f, indent=2, default=str)
    art2 = {"STAMP": ("OBSERVATIONAL thesis-campaign study — the "
                      "operator's loop measured, never adopted; "
                      "random-thesis controls mandatory; per-campaign "
                      "risk accounting mandatory; never validation"),
            "engine_commit": head, "loop_rung_atr": LOOP_RUNG_ATR,
            "thesis_v1": "15M phase-tracker trend state",
            "v2_candidates_recorded_not_built":
                "sentence-family states",
            "per_instrument": camp_art}
    with open(os.path.join(OUT, "thesis_campaign.json"), "w") as f:
        json.dump(art2, f, indent=2, default=str)
    _emit_md(census, camp_art, head, all_rows, kept_rows)
    print(f"OBSERVATIONAL underwater census -> "
          f"{OUT}/underwater_census.md + thesis_campaign.md")


def _emit_md(census, camp_art, head, all_rows, kept_rows):
    n_lb = len(all_rows) - len(kept_rows)
    common = (f"Engine `{head[:9]}` — OBSERVATIONAL, pre-registered "
              "(prereg_underwater_census + prereg_thesis_campaign, "
              "register 87). MEASUREMENT BEFORE MACHINERY (flip-cut "
              "precedent, register 44): nothing here changes any live "
              "recipe, label, or signal; every candidate rule needs "
              "its own Q-number and forward grade. EX-LOCKBOX "
              f"(register 85): {len(kept_rows)} of {len(all_rows)} "
              f"journal rows used, {n_lb} lockbox-span opens "
              "excluded; sealed rows 0. FILL MODEL: journal points "
              "PESSIMISTIC; counterfactuals on the census array-walk "
              "simulator (stop touch-fill, BE armed settled with "
              "entry-touch fill, EOD/flip close-fill; bar-count cuts "
              "close-fill; MAE cuts touch-fill — OPTIMISTIC, "
              "in-ladder comparisons only). ° = n<"
              f"{MIN_CELL_N}. The operator's manual practice (fast "
              "BE, re-enter on the next setup) is the RECORDED "
              "MOTIVATING POLICY; R-BE's scratch-machine record and "
              "the register-42d literature caution stand as opposing "
              "evidence; this census arbitrates.")
    L = ["# Underwater Census (GENERATED by "
         "backtest.underwater_census)", "",
         "Terms: [docs/GLOSSARY.md](../../docs/GLOSSARY.md).", "",
         common, "",
         "STATISTIC SHAPES (74-B): loss decomposition = per-cell "
         "class fractions (descriptive); survival = conditional "
         "P(win | underwater at k) with n at every k; frontier = "
         "conditional-minus-marginal loss rate beside residual "
         "avoidable points; volume split = conditional win rates "
         "quiet vs loud; ladders = mechanical re-pricing on "
         "identical paths (saved / amputated / net). The operator "
         "hypothesis ('winners become positive within 2 bars') is "
         "graded by the curve below, per family. Base variant for "
         f"paths and ladders: {BASE_VARIANT} (unmanaged full hold, "
         "declared; per-variant grids in the JSON follow-up flag).",
         ""]
    for instr, res in sorted(census.items()):
        lb = res["luck_budget"]
        L += [f"## {instr} (spread {res['spread']}; "
              f"{res['n_used']} rows used)", "",
              f"**Luck budget ({instr}, k={REF_K}, {BASE_VARIANT} "
              "slice, labels permuted within family x session "
              f"strata, {NULL_SHUFFLES} pinned seeds):** separation "
              f"cells >= {SPLIT_MIN_PP:g}pp: "
              f"{lb['separation_at_k']['observed']} vs null median "
              f"{lb['separation_at_k']['null_median']:g} / p95 "
              f"{lb['separation_at_k']['null_p95']:g} (pctl "
              f"{lb['separation_at_k']['percentile_vs_null']}); "
              "volume-gap cells: "
              f"{lb['volume_gap_at_k']['observed']} vs null median "
              f"{lb['volume_gap_at_k']['null_median']:g} / p95 "
              f"{lb['volume_gap_at_k']['null_p95']:g} (pctl "
              f"{lb['volume_gap_at_k']['percentile_vs_null']}).", ""]
        L += ["### Loss decomposition + the operator hypothesis "
              "(per family)", "",
              "| family | n | never-positive loss share | "
              "after-positive loss share | winners positive <=2 bars "
              "|", "|---|---|---|---|---|"]
        for fam, g in sorted(res["families"].items()):
            lp = g["loss_decomposition"]
            dim = "°" if g["n"] < MIN_CELL_N else ""
            L.append(
                f"| {fam} | {dim}{g['n']} "
                f"| {lp['loser-never-positive']['share']} "
                f"({lp['loser-never-positive']['loss_pts']} pts) "
                f"| {lp['loser-after-positive']['share']} "
                f"| {g['winners_positive_within_2_bars']} |")
        L += ["", "### Survival, frontier, volume split at the "
              f"reference bar k={REF_K} (full curves in the JSON)",
              "",
              "| family | n@k | P(win given underwater) | separation "
              "| avoidable pts | P(win given quiet dip) | P(win "
              "given loud dip) |", "|---|---|---|---|---|---|---|"]
        for fam, g in sorted(res["families"].items()):
            sv = g["survival"][REF_K - 1]
            fr = g["frontier"][REF_K - 1]
            vs = g["volume_split"][REF_K - 1]
            dim = "°" if (sv["n"] or 0) < MIN_CELL_N else ""
            L.append(f"| {fam} | {dim}{sv['n']} | {sv['p_win']} "
                     f"| {fr.get('separation_pp')}pp "
                     f"| {fr.get('residual_avoidable_pts')} "
                     f"| {vs['p_win_quiet']} | {vs['p_win_loud']} |")
        rf = res["ladder_floors"]["rules"]
        L += ["", "### Rule ladder (per family; saved on losers / "
              "amputated from winners / net, pts; floor = B-RANDOM "
              f"member NET-DELTA band under {BASE_VARIANT} with the "
              "identical rule)", "",
              "| family | rule | n trig | saved | amputated | net | "
              "floor med (min..max) |", "|---|---|---|---|---|---|---|"]
        for fam, g in sorted(res["families"].items()):
            for rule, d_ in sorted(g["rule_ladder"].items()):
                if not d_["n_trig"]:
                    continue
                fb = rf.get(rule)
                fs = (f"{fb['median']} ({fb['min']}..{fb['max']})"
                      if fb else "—")
                L.append(f"| {fam} | {rule} | {d_['n_trig']} "
                         f"| {d_['saved_on_losers']} "
                         f"| {d_['amputated_from_winners']} "
                         f"| {d_['net']} | {fs} |")
        L += ["", "### BE ladder + NEVER-AGAIN table "
              f"({BASE_VARIANT} base)", "",
              "| rung xATR | scratches | winners amputated (pts) | "
              "losses capped (pts saved) | net delta | floor med "
              "(min..max) | max MFE of eventual losers (xATR / pts) "
              "|", "|---|---|---|---|---|---|---|"]
        gf = res["ladder_floors"]["rungs"]
        for rung, agg in sorted(res["be_ladder"].items(),
                                key=lambda x: float(x[0])):
            fb = gf.get(rung)
            fs = (f"{fb['median']} ({fb['min']}..{fb['max']})"
                  if fb else "—")
            L.append(f"| {rung} | {agg['scratches_created']} "
                     f"| {agg['winners_amputated']} "
                     f"({agg['amputated_pts']}) "
                     f"| {agg['losses_capped']} "
                     f"({agg['capped_pts_saved']}) "
                     f"| {agg['net_delta']} | {fs} "
                     f"| {agg['max_mfe_of_losers_atr']} / "
                     f"{agg['max_mfe_of_losers_pts']} |")
        re_ = res["reentry"]["windows"]
        L += ["", f"### Re-entry (BE@{LOOP_RUNG_ATR:g} scratches, "
              "UNDEDUPED stream; the 5-bar dedup hides near "
              "re-fires — stated)", "",
              "| window min | scratched | re-fired | rate |",
              "|---|---|---|---|"]
        for w, d_ in sorted(re_.items()):
            L.append(f"| {w} | {d_['n_scratched']} | {d_['n_refire']} "
                     f"| {d_['refire_rate']} |")
        L.append("")
    with open(os.path.join(OUT, "underwater_census.md"), "w") as f:
        f.write("\n".join(L))
    L2 = ["# Thesis-Campaign Study (GENERATED by "
          "backtest.underwater_census)", "",
          "Terms: [docs/GLOSSARY.md](../../docs/GLOSSARY.md).", "",
          common, "",
          "STATISTIC SHAPES (74-B): per-campaign accounting "
          "distributions vs the RANDOM-THESIS member band (20 pinned "
          "members on the SAME campaign windows — sticky random "
          "theses in a trending month are the stated confound); the "
          "attribution ladder one-shot -> +BE -> +re-entry is a "
          "POLICY LADDER, not a causal claim; backoff rows carry the "
          "abstained counterfactual (backoff's price) MANDATORY. "
          "PER-CAMPAIGN RISK ACCOUNTING IN EVERY TABLE — the "
          "per-trade view is the known flattery. Thesis v1 = the 15M "
          "phase-tracker trend state; v2 candidate states "
          "(sentence-family states) RECORDED, NOT BUILT. Campaigns "
          "intersecting the lockbox span are DROPPED and counted. "
          "Consecutive scratches are recorded as a candidate "
          "narrative event ('repeated refusal') — if "
          "resume-on-print dominates the timers, that routes to the "
          "front door as its own question.", ""]
    for instr, res in sorted(camp_art.items()):
        band = res["random_thesis_net_band"]
        L2 += [f"## {instr} — {res['n_campaigns_used']} campaigns "
               f"used ({res['n_campaigns_lockbox_dropped']} "
               "lockbox-intersecting dropped of "
               f"{res['n_campaigns_total']})", "",
               f"Random-thesis net band ({band['members']} members, "
               f"loop BE@{LOOP_RUNG_ATR:g}): median {band['median']} "
               f"/ min {band['min']} / max {band['max']}.", "",
               "| policy | probes | net | scratches | stops | caught "
               "(pts) | max campaign DD | suppressed | losses "
               "avoided | winners missed |",
               "|---|---|---|---|---|---|---|---|---|---|"]
        order = (["oneshot_nobe", "oneshot_be"]
                 + [f"loop_be{r:g}" for r in BE_RUNGS_ATR]
                 + [k for k in sorted(res["policies"])
                    if k.startswith("backoff")])
        for k in order:
            p = res["policies"][k]
            L2.append(f"| {k} | {p['probes']} | {p['net']} "
                      f"| {p['scratches']} | {p['stops']} "
                      f"| {p['caught']} ({p['caught_pts']}) "
                      f"| {p['max_campaign_dd']} | {p['suppressed']} "
                      f"| {p['supp_losses_avoided']} "
                      f"| {p['supp_winners_missed']} |")
        L2.append("")
    with open(os.path.join(OUT, "thesis_campaign.md"), "w") as f:
        f.write("\n".join(L2))


if __name__ == "__main__":
    main()
