"""Trade forensics — the journal deep review (register 84;
pre-registered prereg_trade_forensics; operator-ordered 2026-08-26).

(1) ENRICHMENT — reports/trades_enriched.csv, one row per journal
    trade, every field mechanical: entry context (day-of-week, UTC
    hour; quadrant / MTF / H11 / phase at the FIRE BAR — open_ts minus
    one 1M bar, the trade layer's tag convention — via the
    conditioning-matrix instruments, registers 66/79, and the H11
    profile with its standing MIS-SCALE caveat off-home; VWAP band +
    signed per the vwap-census convention, register 51; sequel class
    for composites = the composite's defining class, registers 76/82);
    path context on the *fut 1M leg (MAE/MFE in pts and xATR(15M at
    entry), time-to-MFE, bars-to-resolution, post-exit continuation at
    +30/+60 min and post-exit favorable excursion within 60 min);
    outcome (R-multiple vs the shared 2.5xATR(15M) initial stop;
    win/loss/scratch with scratch = |points| < the instrument's
    measured median in-cash spread).
(2) COMPARISON ENGINE — winners-vs-losers categorical splits per
    instrument x sentence x variant x session, each against (a) its
    class-conditioned base, (b) a permutation null (win/loss labels
    shuffled within instrument x sentence x variant strata, 100 pinned
    seeds; cell set fixed at observed measurability; luck budget
    printed), (c) counts and dimming everywhere. Exit-efficiency and
    winner-MAE tables are DESCRIPTIVE design inputs (no null, stated).
(3) DELIVERABLE — reports/forensics/: one md per market + a
    cross-market synthesis (family-repeats vs single-market glints;
    comparison only, NEVER pooling — register 40e) + forensics.json.

STATISTIC SHAPES (74-B): grids = per-cell medians, descriptive;
separators = field count vs permutation null + per-cell extremity vs
the same null's p95; exit-efficiency / winner-MAE = descriptive
medians and quantiles. FENCE: forensics is CANDIDATE-GENERATION ONLY —
no pattern becomes a gate, filter, or recipe change without its own
Q-number and forward grade; candidates are read at an operator +
reviewer sitting on the emitted mds; questions minted through the
front door only. Lockbox-span opens EXCLUDED from every aggregate —
now the PROJECT-WIDE RULING (register 85, 2026-08-27: the span is its
own zone, neither backtest nor forward; this module's stance at first
build generalized). The enriched CSV carries in_lockbox_span as the
audit trail; sealed opens excluded and counted. FILL MODEL:
PESSIMISTIC (inherited from the journal, register 65). Twin-run
pinned (tests/test_trade_forensics.py). Weekly under Part C after the
journal survey.
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

from engine.store_loader import (in_lockbox_span, is_sealed,
                                 lockbox_boundary, zones)
from backtest.conditioning_matrix import _FeatRecorder, quadrant_of
from backtest.location_census import _Profile
from backtest.recipes import _spread_median, build_env
from backtest.scoreboard import _replay, make_cfg
from backtest.signal_points import DRIFT_SKEW_SHARE, TREND_FAMILY
from backtest.vwap_census import _band, _vwap_frame

OUT = os.path.join(ROOT, "reports", "forensics")
TRADES_CSV = os.path.join(ROOT, "reports", "trades.csv")
ENRICHED_CSV = os.path.join(ROOT, "reports", "trades_enriched.csv")
BASE_JSON = os.path.join(ROOT, "reports", "scoreboard",
                         "journal_baselines.json")

MIN_CELL_N = 25          # journal-survey measurability convention
TOP_LEDGER = 25          # NET LEDGER rows per market (cap stated,
                         # drop count printed; full ledger in JSON)
MIN_SIDE_N = 10          # both labels must carry at least this
SPLIT_MIN_PP = 10.0      # separator qualifying |split|
NULL_SHUFFLES = 100
NULL_SEEDS = tuple(range(NULL_SHUFFLES))
CONT_WINDOWS_MIN = (30, 60)
INITIAL_STOP_ATR = 2.5   # shared by all seven journal variants
WATCH_MIN_N = 12
WATCH_CAP = 20
MAE_VARIANT = "R-NOTRAIL"   # unmanaged full-hold path (stop-floor input)

MARKET_OF = {"uk100fut": "uk100", "ger40fut": "ger40",
             "nas100fut": "nas100", "us30fut": "us30"}
FAMILIES = {"EU": ("uk100fut", "ger40fut"),
            "CME": ("nas100fut", "us30fut")}
# the composite's defining sequel class (the one-home module's
# composite definitions, registers 76/82)
SEQUEL_OF = {"S0-H17": "absorption", "S0-H18": "effortless-same",
             "S0-H19": "opposing"}
FEATURES = ("quadrant", "mtf", "h11", "phase", "vwap_band",
            "vwap_signed", "dow", "with_trend", "retest_level",
            "new_hh", "new_hl", "new_lh", "new_ll")
DOW = ("Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun")

FENCE = ("FENCE: forensics is CANDIDATE-GENERATION ONLY — no pattern "
         "becomes a gate, filter, or recipe change without its own "
         "Q-number and forward grade; candidates are read at an "
         "operator+reviewer sitting on these files; questions minted "
         "through the front door only (closed namespace, register 54; "
         "counted trial log).")


def mtf_of(d, t1, t15):
    """register 79 (copied from the conditioning matrix, cited):
    fire-relative MTF alignment; 'pullback' = counter-1M + with-15M."""
    if d == 0 or t15 == 0:
        return "no-15M-trend"
    with15 = (d * t15) > 0
    if t1 == 0:
        return "with-15M-flat-1M" if with15 else "against-15M"
    with1 = (d * t1) > 0
    if with15 and with1:
        return "with-both"
    if with15 and not with1:
        return "pullback"
    if not with15 and with1:
        return "counter-15M"
    return "against-both"


def _context_arrays(instr):
    """One engine replay per instrument (house pattern): per-bar
    quadrant / H11 / 1M+15M trend / VWAP-z on the env's 1M axis."""
    cfg = make_cfg({"session_model.extended_hours": True,
                    "session_model.ladder": True,
                    "debug.structure": True})
    rec = _FeatRecorder()
    engine, bars, _ = _replay(cfg, instr, engine_hook=rec.attach)
    env = build_env(instr, cfg, bars)
    ts = env.ts
    b1m = [x for x in bars[cfg.mtf.execution_tf] if not x.is_stub]
    prof = _Profile()
    h11 = np.array([prof.feed(x) or "unclassified" for x in b1m],
                   dtype=object)
    quad = np.array([quadrant_of(*rec.map.get(t, (None, None)),
                                 cfg.labels.wide_spread_pctile,
                                 cfg.labels.high_volume_mult)
                     for t in ts], dtype=object)
    trend_map, trend15_map = {}, {}
    for e in engine.narrative.events:
        if e["type"] == "PHASE_EVAL" and e.get("tf") == "1min":
            trend_map[pd.Timestamp(e["ts"]).value] = e.get("trend", 0)
        elif e["type"] == "PHASE_EVAL" and e.get("tf") == "15min":
            trend15_map[pd.Timestamp(e["ts"]).value] = e.get("trend", 0)
    t1 = np.array([trend_map.get(t, 0) for t in ts])
    t15_keys = np.array(sorted(trend15_map))
    t15_vals = np.array([trend15_map[k] for k in sorted(trend15_map)]
                        or [0])
    vf = _vwap_frame(instr)
    # settled fire bar: vwap row is open-stamped store time + 1min
    # (the vwap-census lookup convention, cited)
    vmap = {(t + pd.Timedelta(minutes=1)).value: float(r.z)
            for t, r in vf.iterrows() if r.sigma == r.sigma}
    return {"ts": ts, "o": env.o, "h": env.h, "l": env.l, "c": env.c,
            "quad": quad, "h11": h11, "t1": t1,
            "t15_keys": t15_keys, "t15_vals": t15_vals, "vmap": vmap}


def _t15_at(A, t_ns):
    j = np.searchsorted(A["t15_keys"], t_ns, side="right") - 1
    return int(A["t15_vals"][j]) if j >= 0 else 0


def outcome_of(points, spread):
    if abs(points) < spread:
        return "scratch"
    return "win" if points > 0 else "loss"


def enrich_rows(rows, A, spread, boundary, go_live, calendar=None,
                pctl=None, pctl_tod=None):
    """Mechanical enrichment of one instrument's journal rows against
    its per-bar context arrays. Pure given (rows, A, spread, zones,
    calendar, pctl); calendar = (rel, span) from
    event_clock.load_calendar for the register-124 spans_high_event
    flag; pctl = vol_regime.atr_pctl_fn(instr) for the register-130
    atr_pctl column (None -> column None)."""
    from backtest.event_clock import spans_high
    ts = A["ts"]
    n = len(ts)
    out = []
    for r in rows:
        e = dict(r)
        open_ts = pd.Timestamp(r["open_ts"])
        close_ts = pd.Timestamp(r["close_ts"])
        e["spans_high_event"] = (
            spans_high(r["open_ts"], r["close_ts"], *calendar)
            if calendar else None)
        _a = (float(r["atr_entry"])
              if r["atr_entry"] not in (None, "", "None") else None)
        e["atr_pctl"] = (pctl(open_ts.value, _a)
                         if pctl and _a is not None else None)
        e["atr_pctl_tod"] = (pctl_tod(open_ts.value, _a)
                             if pctl_tod and _a is not None else None)
        d = int(r["direction"])
        pts = float(r["points"])
        entry = float(r["open_price"])
        exit_px = float(r["close_price"])
        atr0 = (float(r["atr_entry"])
                if r["atr_entry"] not in (None, "", "None") else None)
        e["dow"] = DOW[open_ts.dayofweek]
        e["hour_utc"] = int(open_ts.hour)
        e["sequel_class"] = SEQUEL_OF.get(r["sentence_id"], "")
        e["in_lockbox_span"] = bool(boundary <= open_ts < go_live)
        e["outcome"] = outcome_of(pts, spread)
        e["r_multiple"] = (round(pts / (INITIAL_STOP_ATR * atr0), 3)
                           if atr0 else None)
        ei = int(np.searchsorted(ts, open_ts.value, side="left"))
        aligned = ei < n and ts[ei] == open_ts.value
        fi = ei - 1
        if aligned and fi >= 0:
            e["quadrant"] = str(A["quad"][fi])
            e["h11"] = str(A["h11"][fi])
            t1 = int(A["t1"][fi])
            e["phase"] = "trending" if t1 != 0 else "ranging"
            e["mtf"] = mtf_of(d, t1, _t15_at(A, ts[fi]))
            z = A["vmap"].get(ts[fi] + 60_000_000_000)
            if z is None:
                e["vwap_band"] = e["vwap_signed"] = "no-vwap"
            else:
                e["vwap_band"] = _band(z)
                e["vwap_signed"] = "away" if z * d > 0 else "toward"
        else:
            for k in ("quadrant", "h11", "phase", "mtf", "vwap_band",
                      "vwap_signed"):
                e[k] = "unclassified"
        if aligned:
            xi = int(np.searchsorted(ts, close_ts.value, side="left"))
            xi = min(xi, n - 1)
            hh, ll = A["h"][ei:xi + 1], A["l"][ei:xi + 1]
            fav = (hh - entry) if d == 1 else (entry - ll)
            adv = (entry - ll) if d == 1 else (hh - entry)
            mfe = float(max(0.0, fav.max())) if len(fav) else 0.0
            mae = float(max(0.0, adv.max())) if len(adv) else 0.0
            e["mfe_pts"] = round(mfe, 2)
            e["mae_pts"] = round(mae, 2)
            e["mfe_atr"] = round(mfe / atr0, 3) if atr0 else None
            e["mae_atr"] = round(mae / atr0, 3) if atr0 else None
            if len(fav) and mfe > 0:
                j = int(np.argmax(fav >= fav.max()))
                e["time_to_mfe_min"] = round(
                    (ts[ei + j] - ts[ei]) / 60e9, 1)
            else:
                e["time_to_mfe_min"] = 0.0
            e["bars_to_resolution"] = int(xi - ei)
            for w in CONT_WINDOWS_MIN:
                k = int(np.searchsorted(
                    ts, close_ts.value + w * 60_000_000_000,
                    side="right")) - 1
                e[f"cont_{w}m_pts"] = (
                    round(d * (float(A["c"][k]) - exit_px), 2)
                    if k > xi else None)
            k60 = int(np.searchsorted(
                ts, close_ts.value + 60 * 60_000_000_000,
                side="right")) - 1
            if k60 > xi:
                hh2, ll2 = A["h"][xi + 1:k60 + 1], A["l"][xi + 1:k60 + 1]
                fav2 = (hh2 - exit_px) if d == 1 else (exit_px - ll2)
                e["postexit_mfe_60m_pts"] = round(
                    float(max(0.0, fav2.max())), 2)
            else:
                e["postexit_mfe_60m_pts"] = None
        else:
            for k in ("mfe_pts", "mae_pts", "mfe_atr", "mae_atr",
                      "time_to_mfe_min", "bars_to_resolution",
                      "cont_30m_pts", "cont_60m_pts",
                      "postexit_mfe_60m_pts"):
                e[k] = None
        out.append(e)
    return out


ENRICH_COLS = ("dow", "hour_utc", "quadrant", "mtf", "h11", "phase",
               "vwap_band", "vwap_signed", "sequel_class", "mae_pts",
               "mfe_pts", "mae_atr", "mfe_atr", "time_to_mfe_min",
               "bars_to_resolution", "cont_30m_pts", "cont_60m_pts",
               "postexit_mfe_60m_pts", "r_multiple", "outcome",
               "in_lockbox_span",
               "spans_high_event",   # register 124: the hold window
                                     # contains a High release (None =
                                     # outside calendar coverage)
               "atr_pctl",           # register 130: ATR-at-entry as a
                                     # percentile of the instrument's
                                     # trailing-20-session distribution
                                     # (the vol_regime field, verbatim;
                                     # None = warmup)
               "atr_pctl_tod")       # register 134: same, vs the SAME
                                     # 30-min time-of-day slot only
                                     # (None = warmup or thin slot)


# ---------------------------------------------------------------- report

def usable(rows):
    """Aggregate-eligible rows + exclusion counts (lockbox / sealed).
    Lockbox test = the shared choke-point helper (register 85)."""
    keep, n_lock, n_seal = [], 0, 0
    for r in rows:
        t = pd.Timestamp(r["open_ts"])
        if in_lockbox_span(t):
            n_lock += 1
        elif is_sealed(t):
            n_seal += 1
        else:
            keep.append(r)
    return keep, n_lock, n_seal


def grid(rows):
    """sentence x variant x session -> {n, median_pts} (scratches
    included in the points grid; descriptive)."""
    cells = {}
    for r in rows:
        k = (r["sentence_id"], r["variant"], r["session"])
        cells.setdefault(k, []).append(float(r["points"]))
    return {k: {"n": len(v),
                "median_pts": round(float(np.median(v)), 2)}
            for k, v in sorted(cells.items())}


def zone_of(ts):
    """working | lockbox | forward (register 85 three-zone model)."""
    t = pd.Timestamp(ts)
    if in_lockbox_span(t):
        return "lockbox"
    return "working" if t < lockbox_boundary() else "forward"


def net_ledger(rows_all, floors, long_share):
    """NET LEDGER (register 84 amendment, operator order 2026-08-27):
    cells ranked by POOLED net points — the discovery lens. Pooled =
    working + lockbox + forward: the ONE table where the lockbox span
    appears inside a printed aggregate, sanctioned by the dated order
    for decomposition display only (register 85 stands everywhere
    else); the mandatory per-zone columns are why the pooled number is
    unquotable. Floor clearance reads the EX-LOCKBOX cell median vs
    the session-scoped baseline floor max. Verdict: forward-thin at
    forward n < MIN_CELL_N, else the FORWARD MEDIAN's sign."""
    cells = {}
    fwd_weeks = {}
    for r in rows_all:
        k = (r["sentence_id"], r["variant"], r["session"])
        z = zone_of(r["open_ts"])
        cells.setdefault(k, {}).setdefault(z, []).append(
            float(r["points"]))
        if z == "forward":
            iso = pd.Timestamp(r["open_ts"]).isocalendar()
            wk = fwd_weeks.setdefault(k, {})
            kk = f"{iso.year}-W{iso.week:02d}"
            wk[kk] = wk.get(kk, 0.0) + float(r["points"])
    out = []
    for (sent, var, sess), zones_ in sorted(cells.items()):
        row = {"sentence": sent, "variant": var, "session": sess}
        pooled = []
        for z in ("working", "lockbox", "forward"):
            pts = zones_.get(z, [])
            pooled.extend(pts)
            row[f"{z}_net"] = round(float(np.sum(pts)), 1)
            row[f"{z}_median"] = (round(float(np.median(pts)), 2)
                                  if pts else None)
            row[f"{z}_n"] = len(pts)
        row["pooled_net"] = round(float(np.sum(pooled)), 1)
        # register 88 item 3: week columns — forward ISO weeks with
        # positive net, so accrual reads without re-runs
        fwd_wk = fwd_weeks.get((sent, var, sess), {})
        row["fwd_weeks_pos"] = sum(1 for v in fwd_wk.values()
                                   if v > 0)
        row["fwd_weeks_total"] = len(fwd_wk)
        ex_lb = zones_.get("working", []) + zones_.get("forward", [])
        med_ex = float(np.median(ex_lb)) if ex_lb else None
        bname = ("B-TREND" if sent in TREND_FAMILY else
                 "B-ALWAYS-LONG"
                 if long_share.get(sent, 0.0) >= DRIFT_SKEW_SHARE
                 else "B-RANDOM")
        fl = floors.get("|".join((var, bname, sess)), [])
        row["floor_baseline"] = bname
        row["clears_floor"] = (None if not fl or med_ex is None
                               else bool(med_ex > max(fl)))
        nf, mf = row["forward_n"], row["forward_median"]
        row["verdict"] = ("forward-thin" if nf < MIN_CELL_N else
                          "forward-positive" if mf > 0 else
                          "forward-negative")
        out.append(row)
    out.sort(key=lambda r: (-r["pooled_net"], r["sentence"],
                            r["variant"], r["session"]))
    return out


def separators(rows):
    """Winners-vs-losers feature splits vs the permutation null.
    Strata = sentence x variant (labels shuffled within; sessions
    inherit). Cell set FIXED at observed measurability. Deterministic."""
    strata = {}
    for r in rows:
        if r["outcome"] == "scratch":
            continue
        strata.setdefault((r["sentence_id"], r["variant"]),
                          []).append(r)
    cells = []          # observed, measurable
    stat_data = []      # per stratum: arrays for the null loop
    for sk in sorted(strata):
        rs_ = strata[sk]
        w = np.array([r["outcome"] == "win" for r in rs_])
        sess = np.array([r["session"] for r in rs_], dtype=object)
        sess_vals = sorted(set(sess))
        sidx = np.array([sess_vals.index(s) for s in sess])
        ns = len(sess_vals)
        win_tot = np.bincount(sidx[w], minlength=ns)
        los_tot = np.bincount(sidx[~w], minlength=ns)
        feats = {}
        for f in FEATURES:
            vals = np.array([str(r[f]) for r in rs_], dtype=object)
            fvals = sorted(set(vals))
            vidx = np.array([fvals.index(v) for v in vals])
            codes = vidx * ns + sidx
            feats[f] = (fvals, codes)
            nb = len(fvals) * ns
            cw = np.bincount(codes[w], minlength=nb)
            cl = np.bincount(codes[~w], minlength=nb)
            for vi, val in enumerate(fvals):
                for si, sv in enumerate(sess_vals):
                    nw, nl = int(win_tot[si]), int(los_tot[si])
                    if nw + nl < MIN_CELL_N or min(nw, nl) < MIN_SIDE_N:
                        continue
                    code = vi * ns + si
                    p_w = cw[code] / nw
                    p_l = cl[code] / nl
                    base = (cw[code] + cl[code]) / (nw + nl)
                    cells.append({
                        "sentence": sk[0], "variant": sk[1],
                        "session": sv, "feature": f, "value": val,
                        "n_win": nw, "n_loss": nl,
                        "n_value": int(cw[code] + cl[code]),
                        "win_share_pct": round(100 * p_w, 1),
                        "loss_share_pct": round(100 * p_l, 1),
                        "base_share_pct": round(100 * base, 1),
                        "split_pp": round(100 * (p_w - p_l), 1),
                        "_stratum": sk, "_code": code, "_feat": f})
        stat_data.append((sk, w, sidx, ns, feats))
    # the null: within-stratum label shuffles, pinned seeds
    null_abs = {i: [] for i in range(len(cells))}
    by_stratum = {}
    for i, c in enumerate(cells):
        by_stratum.setdefault(c["_stratum"], []).append(i)
    field_counts = []
    for seed in NULL_SEEDS:
        rng = np.random.RandomState(seed)
        count = 0
        for sk, w, sidx, ns, feats in stat_data:
            idxs = by_stratum.get(sk)
            if not idxs:
                continue
            wp = w[rng.permutation(len(w))]
            win_tot = np.bincount(sidx[wp], minlength=ns)
            los_tot = np.bincount(sidx[~wp], minlength=ns)
            per_feat = {}
            for i in idxs:
                c = cells[i]
                f = c["_feat"]
                if f not in per_feat:
                    fvals, codes = feats[f]
                    nb = len(fvals) * ns
                    per_feat[f] = (
                        np.bincount(codes[wp], minlength=nb),
                        np.bincount(codes[~wp], minlength=nb))
                cw, cl = per_feat[f]
                si = c["_code"] % ns
                nw, nl = int(win_tot[si]), int(los_tot[si])
                if nw == 0 or nl == 0:
                    sp = 0.0
                else:
                    sp = 100 * (cw[c["_code"]] / nw
                                - cl[c["_code"]] / nl)
                null_abs[i].append(abs(sp))
                if abs(sp) >= SPLIT_MIN_PP:
                    count += 1
        field_counts.append(count)
    observed_count = sum(1 for c in cells
                         if abs(c["split_pp"]) >= SPLIT_MIN_PP)
    for i, c in enumerate(cells):
        na = null_abs[i]
        c["null_p95_abs_pp"] = (round(float(np.percentile(na, 95)), 1)
                                if na else None)
        c["survivor"] = bool(
            abs(c["split_pp"]) >= SPLIT_MIN_PP
            and c["null_p95_abs_pp"] is not None
            and abs(c["split_pp"]) > c["null_p95_abs_pp"])
        c.pop("_stratum")
        c.pop("_code")
        c.pop("_feat")
    luck = {"measurable_cells": len(cells),
            "observed_qualifying": observed_count,
            "null_median": (float(np.median(field_counts))
                            if field_counts else None),
            "null_p95": (float(np.percentile(field_counts, 95))
                         if field_counts else None),
            "percentile_vs_null": (round(100 * float(np.mean(
                [observed_count > m for m in field_counts])), 1)
                if field_counts else None)}
    return cells, luck


def watch_list(rows):
    """Sub-measurable bright splits: |split|>=10pp, n>=WATCH_MIN_N,
    failing measurability; n-to-measurable printed. Deterministic."""
    strata = {}
    for r in rows:
        if r["outcome"] == "scratch":
            continue
        strata.setdefault((r["sentence_id"], r["variant"],
                           r["session"]), []).append(r)
    out = []
    for (sent, var, sess), rs_ in sorted(strata.items()):
        nw = sum(1 for r in rs_ if r["outcome"] == "win")
        nl = len(rs_) - nw
        measurable = (nw + nl >= MIN_CELL_N
                      and min(nw, nl) >= MIN_SIDE_N)
        if measurable or nw + nl < WATCH_MIN_N or not nw or not nl:
            continue
        for f in FEATURES:
            shares = {}
            for r in rs_:
                v = str(r[f])
                c = shares.setdefault(v, [0, 0])
                c[0 if r["outcome"] == "win" else 1] += 1
            for v, (cw, cl) in sorted(shares.items()):
                sp = 100 * (cw / nw - cl / nl)
                if abs(sp) < SPLIT_MIN_PP:
                    continue
                out.append({
                    "sentence": sent, "variant": var, "session": sess,
                    "feature": f, "value": v, "n_win": nw,
                    "n_loss": nl, "split_pp": round(sp, 1),
                    "n_to_measurable": max(
                        MIN_CELL_N - (nw + nl),
                        MIN_SIDE_N - min(nw, nl))})
    out.sort(key=lambda c: (-abs(c["split_pp"]), c["sentence"],
                            c["variant"], c["session"], c["feature"],
                            c["value"]))
    return out


def exit_efficiency(rows):
    """Captured vs available per sentence x exit_reason (variants
    POOLED — pseudo-replication caveat stated in the header).
    Descriptive medians, no null."""
    cells = {}
    for r in rows:
        cells.setdefault((r["sentence_id"], r["exit_reason"]),
                         []).append(r)
    out = {}
    for k, rs_ in sorted(cells.items()):
        pts = [float(r["points"]) for r in rs_]
        post = [(float(r["points"]), float(r["postexit_mfe_60m_pts"]),
                 (float(r["cont_60m_pts"])
                  if r["cont_60m_pts"] is not None else None))
                for r in rs_ if r["postexit_mfe_60m_pts"] is not None]
        avail = [p + m for p, m, _c in post]
        cont = [c for _p, _m, c in post if c is not None]
        out["|".join(k)] = {
            "n": len(rs_), "n_with_postexit": len(post),
            "median_captured_pts": round(float(np.median(pts)), 2),
            "median_available_pts": (round(float(np.median(avail)), 2)
                                     if avail else None),
            "median_left_on_table_pts": (round(float(np.median(
                [m for _p, m, _c in post])), 2) if post else None),
            "median_cont_60m_pts": (round(float(np.median(cont)), 2)
                                    if cont else None)}
    return out


def winner_mae(rows):
    """MAE-of-eventual-winners per sentence, MAE_VARIANT only (the
    unmanaged full-hold path). Descriptive quantiles — a stop-floor
    DESIGN INPUT, not a stop."""
    cells = {}
    for r in rows:
        if (r["variant"] != MAE_VARIANT or r["outcome"] != "win"
                or r["mae_atr"] is None):
            continue
        cells.setdefault(r["sentence_id"], []).append(
            float(r["mae_atr"]))
    out = {}
    for k, v in sorted(cells.items()):
        a = np.array(v)
        out[k] = {"n": len(a),
                  "mae_atr_p50": round(float(np.percentile(a, 50)), 3),
                  "mae_atr_p75": round(float(np.percentile(a, 75)), 3),
                  "mae_atr_p90": round(float(np.percentile(a, 90)), 3)}
    return out


def cross_market(per_instr):
    """Survivor patterns repeated across instruments; families compared,
    NEVER pooled (register 40e)."""
    pat = {}
    for instr, res in per_instr.items():
        for c in res["separators"]:
            if not c["survivor"]:
                continue
            key = (c["sentence"], c["variant"], c["session"],
                   c["feature"], c["value"],
                   "+" if c["split_pp"] > 0 else "-")
            pat.setdefault(key, {})[instr] = c["split_pp"]
    out = []
    for key, hits in sorted(pat.items()):
        instrs = sorted(hits)
        fam = []
        for fname, members in FAMILIES.items():
            if all(m in hits for m in members):
                fam.append(fname)
        cls = ("cross-family" if len(fam) == 2 else
               f"family-repeat ({fam[0]})" if fam else
               "multi-market" if len(instrs) > 1 else "glint")
        out.append({"sentence": key[0], "variant": key[1],
                    "session": key[2], "feature": key[3],
                    "value": key[4], "sign": key[5],
                    "instruments": instrs, "splits_pp": hits,
                    "class": cls})
    return out


# -------------------------------------------------------------- emission

def _hdr(title, head, extra=""):
    return [f"# {title} (GENERATED by backtest.trade_forensics)", "",
            "Terms: [docs/GLOSSARY.md](../../docs/GLOSSARY.md).", "",
            f"Engine `{head[:9]}` — OBSERVATIONAL, pre-registered "
            "(prereg_trade_forensics, register 84). " + FENCE, "",
            "STATISTIC SHAPES (74-B): grids = per-cell medians "
            "(descriptive); separators = field count vs permutation "
            "null (win/loss labels shuffled within sentence x variant "
            f"strata, {NULL_SHUFFLES} pinned shuffles; cell set fixed "
            "at observed measurability) plus per-cell extremity vs "
            "that null's p95; exit-efficiency and winner-MAE = "
            "descriptive medians/quantiles, DESIGN INPUTS with no "
            "null. Measurable separator cell: wins+losses >= "
            f"{MIN_CELL_N} and each side >= {MIN_SIDE_N}; scratch = "
            "|points| < instrument median spread, excluded from "
            "labels. Exit-efficiency pools variants — the same fire "
            "appears under each management, so rows are "
            "management-outcomes, not independent fires (stated). "
            "Prices are the FUTURES leg (the journal's basis). "
            "FILL MODEL: PESSIMISTIC (inherited). ° = dimmed (below "
            "measurability), excluded from the arithmetic. NET LEDGER "
            "= per-cell pooled net with MANDATORY zone decomposition "
            "(descriptive, no null; ranking is best-of-field by "
            "construction): pooled INCLUDES the lockbox span under "
            "the dated operator order of 2026-08-27 — the one "
            "sanctioned decomposition display; register 85 stands for "
            "every evidential aggregate, and the decomposition "
            "columns are why the pooled number is candidate-"
            "generation only. NO CELL IS QUOTABLE FROM THE LEDGER "
            "WITHOUT ITS FORWARD COLUMN." + extra,
            ""]


def emit_market(instr, res, head):
    mk = MARKET_OF[instr]
    lk = res["excluded_lockbox"]
    sl = res["excluded_sealed"]
    luck = res["luck"]
    L = _hdr(f"Trade forensics — {mk} ({instr})", head,
             f" EXCLUDED FROM AGGREGATES: {lk} lockbox-span rows, "
             f"{sl} sealed rows (of {res['n_journal']} journal rows; "
             f"{res['n_used']} used).")
    L += [f"**Luck budget ({instr}):** {luck['observed_qualifying']} "
          f"of {luck['measurable_cells']} measurable separator cells "
          f"reach |split| >= {SPLIT_MIN_PP:g}pp vs null median "
          f"{luck['null_median']:g} / p95 {luck['null_p95']:g}; "
          f"percentile {luck['percentile_vs_null']}. Survivors also "
          "clear their own cell's null p95.", ""]
    L += ["## Session x variant x sentence grid (median pts; "
          "rows with a measurable session cell; full grid in the "
          "JSON)", ""]
    sessions = ("asia", "london", "overlap", "ny_only", "dead")
    by_sv = {}
    for (sent, var, sess), c in res["grid"].items():
        by_sv.setdefault((sent, var), {})[sess] = c
    L += ["| sentence | variant | " + " | ".join(sessions) + " |",
          "|---|---|" + "---|" * len(sessions)]
    for (sent, var), per in sorted(by_sv.items()):
        if not any(c["n"] >= MIN_CELL_N for c in per.values()):
            continue
        row = [sent, var]
        for s in sessions:
            c = per.get(s)
            if c is None:
                row.append("—")
            else:
                dim = "°" if c["n"] < MIN_CELL_N else ""
                row.append(f"{c['median_pts']} ({dim}{c['n']})")
        L.append("| " + " | ".join(row) + " |")
    nl = res["net_ledger"]
    L += ["", f"## NET LEDGER — top {min(TOP_LEDGER, len(nl))} of "
          f"{len(nl)} cells by pooled net points (the discovery lens; "
          "full ledger in the JSON)", "",
          "> Pooled net is CANDIDATE-GENERATION ONLY — the "
          "decomposition columns are why. Verdict: forward-thin at "
          f"forward n < {MIN_CELL_N}, else the forward median's sign. "
          "Floor clearance = ex-lockbox cell median vs the "
          "session-scoped baseline floor max. No cell quotable "
          "without its forward column.", "",
          "| sentence | variant | session | pooled net | working "
          "net / med (n) | lockbox net / med (n) | forward net / med "
          "(n) | fwd wks +/tot | floor (base) | clears | verdict |",
          "|---|---|---|---|---|---|---|---|---|---|---|"]
    for r in nl[:TOP_LEDGER]:
        zc = {z: (f"{r[f'{z}_net']} / {r[f'{z}_median']} "
                  f"({r[f'{z}_n']})")
              for z in ("working", "lockbox", "forward")}
        cl = {True: "YES", False: "no", None: "—"}[r["clears_floor"]]
        L.append(f"| {r['sentence']} | {r['variant']} "
                 f"| {r['session']} | {r['pooled_net']} "
                 f"| {zc['working']} | {zc['lockbox']} "
                 f"| {zc['forward']} "
                 f"| {r['fwd_weeks_pos']}/{r['fwd_weeks_total']} "
                 f"| {r['floor_baseline']} | {cl} "
                 f"| {r['verdict']} |")
    if len(nl) > TOP_LEDGER:
        L.append(f"| … | | | ({len(nl) - TOP_LEDGER} more cells in "
                 "the JSON) | | | | | | | |")
    L += ["", "## Winner/loser separators clearing their null", ""]
    surv = [c for c in res["separators"] if c["survivor"]]
    if surv:
        L += ["| sentence | variant | session | feature | value "
              "| win% | loss% | base% | split | null p95 | n w/l |",
              "|---|---|---|---|---|---|---|---|---|---|---|"]
        for c in sorted(surv, key=lambda c: -abs(c["split_pp"])):
            L.append(f"| {c['sentence']} | {c['variant']} "
                     f"| {c['session']} | {c['feature']} "
                     f"| {c['value']} | {c['win_share_pct']} "
                     f"| {c['loss_share_pct']} | {c['base_share_pct']} "
                     f"| {c['split_pp']:+.1f}pp "
                     f"| {c['null_p95_abs_pp']}pp "
                     f"| {c['n_win']}/{c['n_loss']} |")
    else:
        L.append("No separator clears its null at current depth "
                 "(measurable cells: "
                 f"{luck['measurable_cells']}).")
    L += ["", "## Exit efficiency (captured vs available per exit "
          "reason per sentence; variants pooled, caveat above; rows "
          f"n >= {MIN_CELL_N})", "",
          "| sentence | exit | n | captured med | available med "
          "| left-on-table med | cont 60m med |",
          "|---|---|---|---|---|---|---|"]
    for key, c in res["exit_efficiency"].items():
        if c["n"] < MIN_CELL_N:
            continue
        sent, reason = key.split("|")
        L.append(f"| {sent} | {reason} | {c['n']} "
                 f"| {c['median_captured_pts']} "
                 f"| {c['median_available_pts']} "
                 f"| {c['median_left_on_table_pts']} "
                 f"| {c['median_cont_60m_pts']} |")
    L += ["", f"## MAE of eventual winners ({MAE_VARIANT} only — the "
          "unmanaged full-hold path; xATR at entry; stop-floor "
          "DESIGN INPUT, not a stop)", "",
          "| sentence | n | p50 | p75 | p90 |", "|---|---|---|---|---|"]
    for sent, c in res["winner_mae"].items():
        dim = "°" if c["n"] < MIN_CELL_N else ""
        L.append(f"| {sent} | {dim}{c['n']} | {c['mae_atr_p50']} "
                 f"| {c['mae_atr_p75']} | {c['mae_atr_p90']} |")
    wl = res["watch"]
    L += ["", f"## WATCH list (bright but sub-measurable: |split| >= "
          f"{SPLIT_MIN_PP:g}pp, n >= {WATCH_MIN_N}, failing "
          f"measurability; top {WATCH_CAP} of {len(wl)}; "
          "n-to-measurable = rows still needed)", ""]
    if wl:
        L += ["| sentence | variant | session | feature | value "
              "| split | n w/l | n-to-measurable |",
              "|---|---|---|---|---|---|---|---|"]
        for c in wl[:WATCH_CAP]:
            L.append(f"| {c['sentence']} | {c['variant']} "
                     f"| {c['session']} | {c['feature']} "
                     f"| {c['value']} | {c['split_pp']:+.1f}pp "
                     f"| {c['n_win']}/{c['n_loss']} "
                     f"| {c['n_to_measurable']} |")
    else:
        L.append("Empty.")
    L.append("")
    with open(os.path.join(OUT, f"{mk}.md"), "w") as f:
        f.write("\n".join(L))


def emit_cross(cm, per_instr, head):
    L = _hdr("Trade forensics — cross-market synthesis", head,
             " COMPARISON ONLY, NEVER POOLING (register 40e): each "
             "column is its own instrument's statistic. H11 carries "
             "the standing MIS-SCALE caveat off-home (4.0pt bucket is "
             "a uk100fut value).")
    rep = [p for p in cm if p["class"] != "glint"]
    gl = [p for p in cm if p["class"] == "glint"]
    L += [f"Survivor patterns: {len(cm)} total — {len(rep)} repeated "
          f"across markets, {len(gl)} single-market glints (glints "
          "are counted, not listed; the per-market files carry "
          "them).", ""]
    if rep:
        L += ["| class | sentence | variant | session | feature "
              "| value | sign | splits (pp) |",
              "|---|---|---|---|---|---|---|---|"]
        order = {"cross-family": 0, "family-repeat (EU)": 1,
                 "family-repeat (CME)": 1, "multi-market": 2}
        for p in sorted(rep, key=lambda p: (order.get(p["class"], 3),
                                            p["sentence"])):
            sp = ", ".join(f"{i}:{v:+.1f}"
                           for i, v in sorted(p["splits_pp"].items()))
            L.append(f"| {p['class']} | {p['sentence']} "
                     f"| {p['variant']} | {p['session']} "
                     f"| {p['feature']} | {p['value']} | {p['sign']} "
                     f"| {sp} |")
    else:
        L.append("No survivor repeats across markets at current "
                 "depth.")
    L += ["", "Per-market luck budgets:", ""]
    for instr in sorted(per_instr):
        lk = per_instr[instr]["luck"]
        L.append(f"- {instr}: {lk['observed_qualifying']} of "
                 f"{lk['measurable_cells']} measurable qualify vs "
                 f"null median {lk['null_median']:g} / p95 "
                 f"{lk['null_p95']:g}; percentile "
                 f"{lk['percentile_vs_null']}.")
    L.append("")
    with open(os.path.join(OUT, "cross_market.md"), "w") as f:
        f.write("\n".join(L))


def report(enriched, head, baselines=None):
    """The comparison engine over enriched rows. Pure given inputs;
    twin-run pinned in tests. baselines: journal_baselines floors per
    instrument (loaded from disk when None and present)."""
    if baselines is None:
        baselines = (json.load(open(BASE_JSON))["floors"]
                     if os.path.exists(BASE_JSON) else {})
    per_instr = {}
    for instr in sorted({r["instrument"] for r in enriched}):
        rows = [r for r in enriched if r["instrument"] == instr]
        use, n_lock, n_seal = usable(rows)
        cells, luck = separators(use)
        share = {}
        for r in rows:
            if r.get("direction") is not None:
                share.setdefault(r["sentence_id"], []).append(
                    int(r["direction"]) == 1)
        share = {k: float(np.mean(v)) for k, v in share.items()}
        per_instr[instr] = {
            "n_journal": len(rows), "n_used": len(use),
            "excluded_lockbox": n_lock, "excluded_sealed": n_seal,
            "grid": grid(use), "separators": cells, "luck": luck,
            "watch": watch_list(use),
            "exit_efficiency": exit_efficiency(use),
            "winner_mae": winner_mae(use),
            "net_ledger": net_ledger(rows, baselines.get(instr, {}),
                                     share)}
    cm = cross_market(per_instr)
    art = {"STAMP": ("OBSERVATIONAL trade forensics — luck priced; "
                     "candidate-generation only, read at an "
                     "operator+reviewer sitting; questions through "
                     "the front door; never validation"),
           "engine_commit": head, "min_cell_n": MIN_CELL_N,
           "min_side_n": MIN_SIDE_N, "split_min_pp": SPLIT_MIN_PP,
           "null_shuffles": NULL_SHUFFLES,
           "per_instrument": {
               i: {k: (v if k != "grid" else
                       {"|".join(kk): vv for kk, vv in v.items()})
                   for k, v in res.items()}
               for i, res in per_instr.items()},
           "cross_market": cm}
    return per_instr, cm, art


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--instr", nargs="*",
                    default=["uk100fut", "ger40fut", "nas100fut",
                             "us30fut"])
    a = ap.parse_args()
    os.makedirs(OUT, exist_ok=True)
    head = subprocess.run(["git", "rev-parse", "HEAD"], cwd=ROOT,
                          capture_output=True, text=True).stdout.strip()
    journal = list(csv.DictReader(l for l in open(TRADES_CSV) if not l.startswith("#")))
    boundary, gl = lockbox_boundary(), zones()["go_live"]
    from backtest.event_clock import load_calendar
    calendar = load_calendar()          # register 124: spans_high_event
    enriched = []
    from backtest.vol_regime import atr_pctl_fn, atr_pctl_tod_fn
    for instr in a.instr:
        print(f"# trade_forensics: {instr} ...", file=sys.stderr)
        rows = [r for r in journal if r["instrument"] == instr]
        A = _context_arrays(instr)
        enriched.extend(enrich_rows(rows, A, _spread_median(instr),
                                    boundary, gl, calendar,
                                    atr_pctl_fn(instr),
                                    atr_pctl_tod_fn(instr)))
    cols = (list(journal[0].keys()) + list(ENRICH_COLS)
            if journal else [])
    with open(ENRICHED_CSV, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=cols)
        w.writeheader()
        w.writerows({k: r.get(k) for k in cols} for r in enriched)
    per_instr, cm, art = report(enriched, head)
    with open(os.path.join(OUT, "forensics.json"), "w") as f:
        json.dump(art, f, indent=2, default=str)
    for instr, res in per_instr.items():
        emit_market(instr, res, head)
    emit_cross(cm, per_instr, head)
    n_surv = sum(1 for res in per_instr.values()
                 for c in res["separators"] if c["survivor"])
    print(f"OBSERVATIONAL trade forensics -> {OUT}/ "
          f"({len(enriched)} rows enriched, {n_surv} separator "
          f"survivors) + {ENRICHED_CSV}")


if __name__ == "__main__":
    main()
