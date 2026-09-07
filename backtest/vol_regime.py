"""Volatility-regime cut (register 130; pre-registered
prereg_vol_regime, counted 2026-08-31; operator question: identify
violent conditions and handle them with caution). OBSERVATIONAL.

MOTIVATION, cited at registration: the operator's worst-27
scalp-REF forensic (2026-08-31) — every disaster fired at
elevated ATR-at-entry; the event-census clock inversion recorded as
EXPLAINED (the clock was a proxy for volatility; the clock stayed, the
volatility moved). MECHANISM STATED EX-ANTE: the asymmetric scalp
bracket (0.5xATR target vs 2.5xATR stop) x violence = outsized stops
at elevated stop-rates.

THE FIELD: every journal trade gains atr_pctl — the percentile of
ATR(15M)-at-entry against the instrument's OWN trailing-20-session
ATR(15M) distribution (strictly-prior 15M bars within the last
TRAIL_SESSIONS native sessions; existing data, no new thresholds —
the 20-session window and the bucket edges are the order's own).
BUCKETS: <50 / 50-80 / 80-95 / >=95.

CELLS per bucket x variant x leg x window (scalp arms headlined; both
windows; ex-lockbox; distinct paths per register 113): n (distinct),
stop-rate, net, median, win rate. LUCK: per (variant, leg, window),
the TOP-BUCKET DEGRADATION — median(other buckets pooled) minus
median(>=95) and the stop-rate gap the other way — vs bucket labels
permuted within the stratum (pinned seeds), ONE-SIDED (the degradation
direction is the ex-ante mechanism); a leg clears when the median gap
exceeds its null p95 with the top bucket measurable. CANDIDATE = >= 3
of 4 forward legs clearing; single-leg findings -> the per-market
WATCH page with the same selection discipline (grafted rows).

IF a candidate survives: an ENTRY-PAUSE rule (no new scalp entries
when atr_pctl > X) proposes through the FRONT DOOR — explicitly
distinguished from the failed clock rule (register 104: window
proxies) and the failed reactive cooldowns (register 103: after-the-
fact triggers): this rule is EX-ANTE STATE, not clock and not
reaction. Nothing registers from this page. Twin-run pinned
(tests/test_vol_regime.py). Weekly under Part C before the WATCH page.
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
from backtest.per_market_watch import NULL_SEEDS, distinct_paths
from backtest.zone_census import atr_series, session_ordinals

OUT = os.path.join(ROOT, "reports", "scoreboard")
TRADES_CSV = os.path.join(ROOT, "reports", "trades.csv")

INSTRUMENTS = ("uk100fut", "ger40fut", "nas100fut", "us30fut")
SCALP_ARMS = ("R-SCALP-H" + str(6), "R-SCALP-H" + str(6) + "-REF")
TRAIL_SESSIONS = 20      # the order's trailing window (native sessions)
VOL_BUCKETS = (50, 80, 95)   # the order's bucket edges: <50/50-80/80-95/>=95
MIN_TOP_N = 10           # top-bucket measurability (the matrix convention)
TOD_SLOT_MIN = 30        # register 134: time-of-day slot width (minutes)
MIN_TOD_N = 20           # register 134: minimum same-slot prior values
                         # (a slot holds two 15M bars/session -> 40 max
                         # in the trailing window, so the pooled
                         # 50-value floor is unreachable; 20 = ten full
                         # sessions of the slot)


def _slot_of(ns):
    return int((ns // 60_000_000_000) % 1440) // TOD_SLOT_MIN


def bucket_of(pct):
    if pct is None or np.isnan(pct):
        return None
    if pct < VOL_BUCKETS[0]:
        return "<50"
    if pct < VOL_BUCKETS[1]:
        return "50-80"
    if pct < VOL_BUCKETS[2]:
        return "80-95"
    return ">=95"


def frame15(instr):
    """The 15M store frame both percentile fns and the truncation
    harness (register 136) share."""
    return pd.read_csv(os.path.join(ROOT, "clean_finsa",
                                    f"{instr}_15min.csv"),
                       usecols=["time", "high", "low", "close",
                                "ldate"],
                       parse_dates=["time"])


def atr_pctl_fn(instr, frame=None):
    """entry_ts_ns, atr_entry -> percentile vs the instrument's own
    strictly-prior 15M ATR values within the trailing TRAIL_SESSIONS
    native sessions (the store's ldate). No lookahead: only bars whose
    CLOSE precedes the entry count. frame: injected (possibly
    truncated) 15M store for the register-136 behavioral pin."""
    df = frame if frame is not None else frame15(instr)
    atr = atr_series(df["high"].to_numpy(), df["low"].to_numpy(),
                     df["close"].to_numpy(), 14)
    # close stamps: the store is open-stamped; a 15M bar closes 15 min on
    close_ns = df["time"].dt.as_unit("ns").astype("int64").to_numpy() \
        + 15 * 60_000_000_000
    sess = session_ordinals(df["ldate"].astype(str).tolist())

    def f(entry_ns, atr_entry):
        j = int(np.searchsorted(close_ns, entry_ns, side="right"))
        if j == 0 or atr_entry is None:
            return None
        lo_ord = sess[j - 1] - TRAIL_SESSIONS + 1
        sel = (np.arange(len(atr)) < j) & (sess >= lo_ord)
        vals = atr[sel]
        vals = vals[~np.isnan(vals)]
        if len(vals) < 50:
            return None
        return round(100 * float(np.mean(vals <= atr_entry)), 1)
    return f


def atr_pctl_tod_fn(instr, frame=None):
    """entry_ts_ns, atr_entry -> percentile vs the SAME time-of-day
    slot's strictly-prior 15M ATR values within the trailing
    TRAIL_SESSIONS native sessions (register 134: the register-73
    time-matched-base method applied to volatility). Slot membership by
    close stamp on both sides — the atr_pctl anchor, verbatim. None =
    warmup or fewer than MIN_TOD_N prior same-slot values. frame: see
    atr_pctl_fn."""
    df = frame if frame is not None else frame15(instr)
    atr = atr_series(df["high"].to_numpy(), df["low"].to_numpy(),
                     df["close"].to_numpy(), 14)
    close_ns = df["time"].dt.as_unit("ns").astype("int64").to_numpy() \
        + 15 * 60_000_000_000
    sess = session_ordinals(df["ldate"].astype(str).tolist())
    slot = (close_ns // 60_000_000_000) % 1440 // TOD_SLOT_MIN

    def f(entry_ns, atr_entry):
        j = int(np.searchsorted(close_ns, entry_ns, side="right"))
        if j == 0 or atr_entry is None:
            return None
        lo_ord = sess[j - 1] - TRAIL_SESSIONS + 1
        sel = ((np.arange(len(atr)) < j) & (sess >= lo_ord)
               & (slot == _slot_of(entry_ns)))
        vals = atr[sel]
        vals = vals[~np.isnan(vals)]
        if len(vals) < MIN_TOD_N:
            return None
        return round(100 * float(np.mean(vals <= atr_entry)), 1)
    return f


def journal_rows():
    boundary, gl = lockbox_boundary(), zones()["go_live"]
    fns = {}
    out = []
    for r in csv.DictReader(l for l in open(TRADES_CSV)
                            if not l.startswith("#")):
        if r["instrument"] not in INSTRUMENTS \
                or in_lockbox_span(r["open_ts"]):
            continue
        t = pd.Timestamp(r["open_ts"])
        w = "backtest" if t < boundary else "forward" if t >= gl else None
        if w is None or r["atr_entry"] in ("", "None"):
            continue
        if r["instrument"] not in fns:
            fns[r["instrument"]] = (atr_pctl_fn(r["instrument"]),
                                    atr_pctl_tod_fn(r["instrument"]))
        f_p, f_t = fns[r["instrument"]]
        pct = f_p(t.value, float(r["atr_entry"]))
        pct_tod = f_t(t.value, float(r["atr_entry"]))
        out.append({"instrument": r["instrument"],
                    "variant": r["variant"], "window": w,
                    "pts": float(r["points"]),
                    "stopped": r["exit_reason"].startswith("stop"),
                    "atr_pctl": pct, "atr_pctl_tod": pct_tod,
                    "bucket": bucket_of(pct),
                    "path": f"{r['open_ts']}|{r['direction']}"
                            f"|{r['points']}"})
    return out


def cell(rows):
    """Distinct-path cell statistics (register 113) + stop rate."""
    ded = distinct_paths(rows)
    pts = np.array([r["pts"] for r in ded], float)
    return {"n": len(rows), "n_distinct": len(ded),
            "stop_rate": (round(float(np.mean([r["stopped"]
                                               for r in ded])), 3)
                          if ded else None),
            "net": round(float(pts.sum()), 1) if len(pts) else None,
            "median": round(float(np.median(pts)), 2) if len(pts)
            else None,
            "win_rate": (round(float((pts > 0).mean()), 3)
                         if len(pts) else None)}


def degradation(rows):
    """(median gap, stop-rate gap) = rest-vs-top-bucket; the ex-ante
    degradation direction (positive = the top bucket is worse)."""
    top = [r for r in rows if r["bucket"] == ">=95"]
    rest = [r for r in rows if r["bucket"] not in (None, ">=95")]
    ct, cr = cell(top), cell(rest)
    if ct["n_distinct"] < MIN_TOP_N or cr["n_distinct"] < MIN_TOP_N:
        return None, None, ct, cr
    return (round(cr["median"] - ct["median"], 2),
            round(ct["stop_rate"] - cr["stop_rate"], 3), ct, cr)


def stratum_null(rows):
    """Bucket labels permuted within the stratum (pinned seeds); the
    null distribution of the MEDIAN degradation (one-sided)."""
    labs = [r["bucket"] for r in rows]
    out = []
    for seed in NULL_SEEDS:
        rs = np.random.RandomState(seed)
        perm = rs.permutation(len(labs))
        fake = [dict(r, bucket=labs[j])
                for r, j in zip(rows, perm)]
        g, _sg, _t, _r = degradation(fake)
        out.append(np.nan if g is None else g)
    return np.array(out, float)


def run():
    rows = journal_rows()
    strata = {}
    for r in rows:
        if r["bucket"] is None:
            continue
        strata.setdefault((r["variant"], r["instrument"],
                           r["window"]), []).append(r)
    cells = {}
    gates = {}
    for key, rr in sorted(strata.items()):
        var, instr, w = key
        for b in ("<50", "50-80", "80-95", ">=95"):
            sel = [x for x in rr if x["bucket"] == b]
            if sel:
                cells["|".join((instr, var, w, b))] = cell(sel)
        gap, sgap, ct, cr = degradation(rr)
        entry = {"median_gap": gap, "stop_rate_gap": sgap,
                 "top_n_distinct": ct["n_distinct"],
                 "rest_n_distinct": cr["n_distinct"],
                 "measurable": gap is not None}
        if gap is not None:
            null = stratum_null(rr)
            valid = null[~np.isnan(null)]
            p95 = (float(np.percentile(valid, 95)) if len(valid)
                   else None)
            entry.update({
                "null_p95": None if p95 is None else round(p95, 2),
                "null_valid_seeds": int(len(valid)),
                "pct_vs_null": (round(100 * float(np.mean(valid < gap)),
                                      1) if len(valid) else None),
                "clears": bool(p95 is not None and gap > p95)})
        else:
            entry.update({"null_p95": None, "null_valid_seeds": 0,
                          "pct_vs_null": None, "clears": False})
        gates["|".join(key)] = entry
    # candidates per variant (forward legs; the event-clock shape)
    candidates = {}
    variants = sorted({k.split("|")[0] for k in gates})
    for var in variants:
        legs = {}
        for instr in INSTRUMENTS:
            g = gates.get("|".join((var, instr, "forward")))
            if g and g["measurable"]:
                legs[instr] = {"gap_pp": g["median_gap"],
                               "null_p95": g["null_p95"],
                               "clears": g["clears"]}
        cl = sorted(i for i, v in legs.items() if v["clears"])
        grade = ("candidate" if len(cl) >= 3
                 else "glint" if cl else "none")
        candidates[f"{var}|vol>=95"] = {
            "legs": legs, "clearing": cl, "grade": grade,
            "mechanism": "volatility pause (ex-ante state — not clock, "
                         "not reaction)"}
    watch_rows = []
    for key, g in gates.items():
        var, instr, w = key.split("|")
        if w == "forward" and g["clears"]:
            watch_rows.append({"instrument": instr, "variant": var,
                               "window": w,
                               "median_gap": g["median_gap"],
                               "stop_rate_gap": g["stop_rate_gap"],
                               "top_n_distinct": g["top_n_distinct"],
                               "pct_vs_null": g["pct_vs_null"]})
    return {"rows_ex_lockbox": len(rows),
            "rows_unmeasured_pctl": sum(1 for r in rows
                                        if r["bucket"] is None),
            "trail_sessions": TRAIL_SESSIONS,
            "buckets": list(VOL_BUCKETS),
            "cells": cells, "gates": gates,
            "candidates": candidates, "watch_rows": watch_rows}


def _emit(art, head):
    L = ["# Volatility-Regime Cut (GENERATED by backtest.vol_regime)",
         "", "Terms: [docs/GLOSSARY.md](../../docs/GLOSSARY.md).", "",
         f"Engine `{head[:9]}` — OBSERVATIONAL, pre-registered "
         "(prereg_vol_regime, register 130). atr_pctl = ATR(15M)-at-"
         "entry vs the instrument's OWN trailing-"
         f"{TRAIL_SESSIONS}-session 15M ATR distribution (strictly "
         "prior, no lookahead); buckets <50 / 50-80 / 80-95 / >=95 "
         "(the order's edges). MOTIVATION CITED: the worst-27 scalp-"
         "REF forensic — every disaster at elevated ATR-at-entry; the "
         "event-clock inversion EXPLAINED as a volatility proxy "
         "(register 130). MECHANISM EX-ANTE: the asymmetric bracket x "
         "violence = outsized stops at elevated stop-rates. STATISTIC "
         "SHAPES (74-B): per-stratum TOP-BUCKET DEGRADATION (rest-"
         "median minus top-median, one-sided) vs bucket labels "
         f"permuted within the stratum ({len(NULL_SEEDS)} pinned "
         "seeds); distinct paths throughout (register 113); top bucket "
         f"measurable at n_distinct >= {MIN_TOP_N}; CANDIDATE = >= 3 "
         "of 4 forward legs clearing; single-leg clears -> the WATCH "
         "page. A surviving candidate proposes an ENTRY-PAUSE rule "
         "through the front door — distinguished from the failed clock "
         "rule (register 104) and the failed reactive cooldowns "
         "(register 103). Ex-lockbox; nothing registers here. "
         f"({art['rows_unmeasured_pctl']} rows carry no percentile — "
         "warmup; counted.)", "",
         "## Scalp arms — top-bucket degradation (headline)", "",
         "| arm | leg | window | rest med (n) | >=95 med (n) | median "
         "gap | stop-rate gap | null p95 | pct | clears |",
         "|---|---|---|---|---|---|---|---|---|---|"]
    for key, g in art["gates"].items():
        var, instr, w = key.split("|")
        if var not in SCALP_ARMS:
            continue
        ct = art["cells"].get("|".join((instr, var, w, ">=95")), {})
        cr_med = None
        if g["measurable"]:
            cr_med = round(ct.get("median", 0) + g["median_gap"], 2) \
                if ct.get("median") is not None else None
        L.append(f"| {var} | {instr} | {w} "
                 f"| {cr_med if cr_med is not None else '—'} "
                 f"({g['rest_n_distinct']}) "
                 f"| {ct.get('median', '—')} ({g['top_n_distinct']}) "
                 f"| {g['median_gap'] if g['median_gap'] is not None else '—'} "
                 f"| {g['stop_rate_gap'] if g['stop_rate_gap'] is not None else '—'} "
                 f"| {g['null_p95'] if g['null_p95'] is not None else '—'} "
                 f"| {g['pct_vs_null'] if g['pct_vs_null'] is not None else '—'} "
                 f"| {'YES' if g['clears'] else 'no'} |")
    L += ["", "## Candidates and glints (forward legs clearing; "
          "candidate = >= 3 of 4, one mechanism)", "",
          "| variant | cut | mechanism | grade | clearing legs |",
          "|---|---|---|---|---|"]
    any_ = False
    for k, d in sorted(art["candidates"].items(),
                       key=lambda x: (x[1]["grade"] != "candidate",
                                      x[1]["grade"] != "glint", x[0])):
        if d["grade"] == "none":
            continue
        any_ = True
        var, cut = k.split("|")
        L.append(f"| {var} | {cut} | {d['mechanism']} | {d['grade']} "
                 f"| {', '.join(d['clearing'])} |")
    if not any_:
        L.append("| (no stratum clears its null on any forward leg) "
                 "| | | | |")
    L += ["", "## All buckets (every variant; full grid in the JSON; "
          "n as rows (distinct))", "",
          "| leg | variant | window | bucket | n (distinct) | stop% "
          "| median | win | net |", "|---|---|---|---|---|---|---|---|---|"]
    for key, c in art["cells"].items():
        instr, var, w, b = key.split("|")
        if var not in SCALP_ARMS or c["n_distinct"] < MIN_TOP_N:
            continue
        L.append(f"| {instr} | {var} | {w} | {b} "
                 f"| {c['n']} ({c['n_distinct']}) "
                 f"| {100 * c['stop_rate']:.0f} | {c['median']:+.2f} "
                 f"| {100 * c['win_rate']:.0f}% | {c['net']} |")
    L.append("")
    with open(os.path.join(OUT, "vol_regime.md"), "w") as f:
        f.write("\n".join(L))


def main():
    ap = argparse.ArgumentParser()
    ap.parse_args()
    head = subprocess.run(["git", "rev-parse", "HEAD"], cwd=ROOT,
                          capture_output=True, text=True).stdout.strip()
    art = {"STAMP": ("OBSERVATIONAL volatility-regime cut — ex-ante "
                     "state conditioning; any pause rule via the front "
                     "door only; never validation"),
           "engine_commit": head, **run()}
    with open(os.path.join(OUT, "vol_regime.json"), "w") as f:
        json.dump(art, f, indent=2, default=str)
    _emit(art, head)
    n_c = sum(1 for d in art["candidates"].values()
              if d["grade"] == "candidate")
    n_g = sum(1 for d in art["candidates"].values()
              if d["grade"] == "glint")
    print(f"OBSERVATIONAL vol regime -> {OUT}/vol_regime.md "
          f"({n_c} candidates, {n_g} glints)")


if __name__ == "__main__":
    main()
