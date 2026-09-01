"""Conditional open-pause cut (register 133; pre-registered
prereg_open_pause, counted 2026-09-01; operator hypothesis 2026-08-31:
volatility-gated open avoidance). OBSERVATIONAL.

THE HONESTY FENCE, first (the order's own words): this cell was
SELECTED POST-HOC from the worst-27 forensic — all three conditions
(the open window, the elevated ATR, the scalp arms) were read off the
losses. THE BACKTEST RESULT IS THEREFORE MOTIVATING, NOT EVIDENTIAL.
Enactment requires the FORWARD / SEALED-WINDOW cells clearing their
floors at measurable n, PER-MARKET SCOPED — ger40/nas100's open
weakness vs us30's open strength already diverge (register 104), so a
surviving rule likely wears two legs, not four.

(a) THE MEASUREMENT: journal outcomes INSIDE the open window (the
event-clock open±30 tag, register 104) split by the DAY'S open-window
ATR percentile — atr_pctl at the window's FIRST BAR (open − 30 min),
the register-130 percentile machinery verbatim — strata {<80, 80-95,
>=95} (the registered edges; no new thresholds anywhere in this cut).
Per variant × leg × window, distinct paths (register 113): n, median,
win, stop-rate, net. LUCK: per stratum-pair, gap = median(<80) −
median(>=95), one-sided (does open degradation CONCENTRATE in the
stretched strata?), vs the day→bucket map permuted across the leg's
days (pinned seeds); both strata measurable at n_distinct >= 10.

(b) THE COUNTERFACTUAL (register-132 conventions verbatim): entries
skipped ONLY inside the open window ONLY when the day's open-ATR pctl
> X ∈ {80, 95} — implemented by mapping each row's pctl to None unless
in-window, then the register-132 pause_cell applies unchanged (skipped
= foregone, no resurrection; distinct paths; skipped counts, foregone
winners, avoided losers, net delta, stop changes). FLOORS: B-RANDOM
members under the IDENTICAL conditional rule, scalp arms (the evidence
rows); context ladder floor-less, stated.

Weekly under Part C beside the register-132 counterfactual; ex-lockbox;
sealed untouched; twin-run pinned (tests/test_open_pause.py); shapes
per 74-B (stratum gap vs day-permutation null; counterfactual delta vs
member band).
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
from backtest.event_clock import AUCTION_UTC, auction_tag
from backtest.per_market_watch import NULL_SEEDS, distinct_paths
from backtest.vol_pause import PAUSE_X, pause_cell
from backtest.vol_regime import SCALP_ARMS
from backtest.zone_census import atr_series, session_ordinals

OUT = os.path.join(ROOT, "reports", "scoreboard")
TRADES_CSV = os.path.join(ROOT, "reports", "trades.csv")

INSTRUMENTS = ("uk100fut", "ger40fut", "nas100fut", "us30fut")
OPEN_W_MIN = 30          # the event-clock open±30 tag, reused
TRAIL_SESSIONS = 20      # the register-130 window, reused
STRATA = ("<80", "80-95", ">=95")
MIN_STRATUM_N = 10       # the matrix convention


def stratum_of(pct):
    if pct is None:
        return None
    if pct < 80:
        return "<80"
    if pct < 95:
        return "80-95"
    return ">=95"


def day_open_pctl(instr, frame=None, days=None):
    """UTC-date -> the atr_pctl at the open window's FIRST bar (the
    auction open − 30 min): the ATR of the last 15M bar CLOSED at or
    before that moment, as a percentile of the instrument's own
    strictly-prior 15M ATR values within the trailing TRAIL_SESSIONS
    native sessions (the register-130 machinery, re-anchored to the
    window's first bar; no lookahead). frame: injected (possibly
    truncated) 15M store for the register-136 behavioral pin."""
    from backtest.vol_regime import frame15
    df = frame if frame is not None else frame15(instr)
    atr = atr_series(df["high"].to_numpy(), df["low"].to_numpy(),
                     df["close"].to_numpy(), 14)
    close_ns = df["time"].dt.as_unit("ns").astype("int64").to_numpy() \
        + 15 * 60_000_000_000
    sess = session_ordinals(df["ldate"].astype(str).tolist())
    hh, mm = map(int, AUCTION_UTC[instr][0].split(":"))
    out = {}
    if days is None:
        days = sorted(set(df["time"].dt.strftime("%Y-%m-%d")))
    for d in days:
        t0 = (pd.Timestamp(d, tz="UTC")
              + pd.Timedelta(hours=hh, minutes=mm)
              - pd.Timedelta(minutes=OPEN_W_MIN))
        j = int(np.searchsorted(close_ns, t0.value, side="right"))
        if j == 0 or np.isnan(atr[j - 1]):
            continue
        lo_ord = sess[j - 1] - TRAIL_SESSIONS + 1
        sel = (np.arange(len(atr)) < j - 1) & (sess >= lo_ord)
        vals = atr[sel]
        vals = vals[~np.isnan(vals)]
        if len(vals) < 50:
            continue
        out[d] = round(100 * float(np.mean(vals <= atr[j - 1])), 1)
    return out


def journal_rows():
    boundary, gl = lockbox_boundary(), zones()["go_live"]
    pctls = {i: day_open_pctl(i) for i in INSTRUMENTS}
    out = []
    for r in csv.DictReader(l for l in open(TRADES_CSV)
                            if not l.startswith("#")):
        if r["instrument"] not in INSTRUMENTS \
                or in_lockbox_span(r["open_ts"]):
            continue
        t = pd.Timestamp(r["open_ts"])
        w = "backtest" if t < boundary else "forward" if t >= gl else None
        if w is None:
            continue
        instr = r["instrument"]
        in_open = auction_tag(t, instr, "open", OPEN_W_MIN)
        day = t.strftime("%Y-%m-%d")
        pct = pctls[instr].get(day)
        out.append({"instrument": instr, "variant": r["variant"],
                    "window": w, "pts": float(r["points"]),
                    "stopped": r["exit_reason"].startswith("stop"),
                    "in_open": bool(in_open), "day": day,
                    "open_pctl": pct,
                    "stratum": stratum_of(pct) if in_open else None,
                    # the register-132 reuse: a pctl only in-window,
                    # so pause_cell's predicate becomes the
                    # CONDITIONAL gate verbatim
                    "atr_pctl": (pct if in_open else None),
                    "path": f"{r['open_ts']}|{r['direction']}"
                            f"|{r['points']}"})
    return out


def _cellstats(rows):
    ded = distinct_paths(rows)
    pts = np.array([r["pts"] for r in ded], float)
    return {"n": len(rows), "n_distinct": len(ded),
            "median": round(float(np.median(pts)), 2) if len(pts)
            else None,
            "win_rate": (round(float((pts > 0).mean()), 3)
                         if len(pts) else None),
            "stop_rate": (round(float(np.mean([r["stopped"]
                                               for r in ded])), 3)
                          if ded else None),
            "net": round(float(pts.sum()), 1) if len(pts) else None}


def stratum_gap(rows):
    """gap = median(<80) − median(>=95) among IN-OPEN rows; one-sided
    (positive = open degradation concentrates in stretched ATR)."""
    lo = [r for r in rows if r["stratum"] == "<80"]
    hi = [r for r in rows if r["stratum"] == ">=95"]
    cl, ch = _cellstats(lo), _cellstats(hi)
    if cl["n_distinct"] < MIN_STRATUM_N \
            or ch["n_distinct"] < MIN_STRATUM_N:
        return None, cl, ch
    return round(cl["median"] - ch["median"], 2), cl, ch


def day_perm_null(rows, pctls_by_day):
    """The day→bucket map permuted across the leg's covered days
    (pinned seeds); the null of the stratum gap."""
    days = sorted(pctls_by_day)
    vals = [pctls_by_day[d] for d in days]
    out = []
    for seed in NULL_SEEDS:
        rs = np.random.RandomState(seed)
        perm = rs.permutation(len(days))
        fake_map = {d: vals[j] for d, j in zip(days, perm)}
        fake = []
        for r in rows:
            p = fake_map.get(r["day"])
            fake.append(dict(r, stratum=(stratum_of(p) if r["in_open"]
                                         else None)))
        g, _a, _b = stratum_gap(fake)
        out.append(np.nan if g is None else g)
    return np.array(out, float)


def open_floor_bands(instr, day_pctl):
    """B-RANDOM members under the scalp arms + the IDENTICAL
    conditional rule (skip iff in-open AND day open-pctl > X)."""
    from backtest.underwater_census import build_instrument
    from backtest.recipes import (RECIPE_SET_VERSION, RECIPE_SETS,
                                  simulate, specialize)
    from backtest.signal_points import baseline_fires
    A = build_instrument(instr)
    env = A["env"]
    members = baseline_fires(env, A["engine_events"])["B-RANDOM"]
    boundary, gl = lockbox_boundary(), zones()["go_live"]
    bands = {}
    for arm in SCALP_ARMS:
        recipe = specialize(RECIPE_SETS[RECIPE_SET_VERSION][arm], instr)
        deltas = {}
        for mf in members:
            agg = {}
            for t in simulate(mf, env, recipe, A["spread"]):
                if in_lockbox_span(t["entry_ts"]):
                    continue
                ts = pd.Timestamp(t["entry_ts"])
                w = ("backtest" if ts < boundary
                     else "forward" if ts >= gl else None)
                if w is None:
                    continue
                if not auction_tag(ts, instr, "open", OPEN_W_MIN):
                    continue
                pc = day_pctl.get(ts.strftime("%Y-%m-%d"))
                for x in PAUSE_X:
                    if pc is not None and pc > x:
                        agg[(w, x)] = agg.get((w, x), 0.0) \
                            - float(t["pts"])
            for w in ("backtest", "forward"):
                for x in PAUSE_X:
                    deltas.setdefault((w, x), []).append(
                        round(agg.get((w, x), 0.0), 1))
        bands[arm] = {f"{w}|{x}": {
            "members": len(v),
            "median": round(float(np.median(v)), 1),
            "min": round(float(min(v)), 1),
            "max": round(float(max(v)), 1)}
            for (w, x), v in sorted(deltas.items())}
    return bands


def run():
    rows = journal_rows()
    pctls = {i: day_open_pctl(i) for i in INSTRUMENTS}
    strata_cells = {}
    gaps = {}
    cf = {}
    by = {}
    for r in rows:
        by.setdefault((r["instrument"], r["variant"], r["window"]),
                      []).append(r)
    for key, rr in sorted(by.items()):
        instr, var, w = key
        for s in STRATA:
            sel = [x for x in rr if x["stratum"] == s]
            if sel:
                strata_cells["|".join(key) + f"|{s}"] = _cellstats(sel)
        g, cl, ch = stratum_gap(rr)
        entry = {"gap": g, "lo": cl, "hi": ch, "measurable": g is not None}
        if g is not None:
            null = day_perm_null(rr, pctls[instr])
            valid = null[~np.isnan(null)]
            p95 = (float(np.percentile(valid, 95)) if len(valid)
                   else None)
            entry.update({"null_p95": None if p95 is None
                          else round(p95, 2),
                          "null_valid_seeds": int(len(valid)),
                          "pct_vs_null": (round(100 * float(
                              np.mean(valid < g)), 1) if len(valid)
                              else None),
                          "clears": bool(p95 is not None and g > p95)})
        else:
            entry.update({"null_p95": None, "null_valid_seeds": 0,
                          "pct_vs_null": None, "clears": False})
        gaps["|".join(key)] = entry
        for x in PAUSE_X:
            cf["|".join(key) + f"|{x}"] = pause_cell(rr, x)
    floors = {}
    for instr in INSTRUMENTS:
        print(f"# open_pause floors: {instr} ...", file=sys.stderr)
        floors[instr] = open_floor_bands(instr, pctls[instr])
    return {"rows_ex_lockbox": len(rows),
            "open_days_covered": {i: len(p) for i, p in pctls.items()},
            "strata_cells": strata_cells, "gaps": gaps,
            "counterfactual": cf, "scalp_floors": floors}


def _emit(art, head):
    L = ["# Conditional Open-Pause Cut (GENERATED by "
         "backtest.open_pause)", "",
         "Terms: [docs/GLOSSARY.md](../../docs/GLOSSARY.md).", "",
         f"Engine `{head[:9]}` — OBSERVATIONAL, pre-registered "
         "(prereg_open_pause, register 133). **THE HONESTY FENCE "
         "FIRST: this cell was SELECTED POST-HOC from the worst-27 "
         "forensic — all three conditions were read off the losses; "
         "the backtest result is MOTIVATING, NOT EVIDENTIAL. Enactment "
         "requires the forward / sealed-window cells clearing their "
         "floors at measurable n, PER-MARKET SCOPED (ger40/nas100's "
         "open weakness vs us30's open strength already diverge — a "
         "surviving rule likely wears two legs, not four).** (a) "
         "in-open outcomes split by the DAY'S open-window ATR "
         "percentile (the window's first bar, register-130 machinery; "
         "strata <80 / 80-95 / >=95); gap = median(<80) − "
         "median(>=95), one-sided, vs the day→bucket map permuted "
         f"across days ({len(NULL_SEEDS)} pinned seeds); distinct "
         "paths (register 113). (b) the register-132 counterfactual "
         "with the CONDITIONAL predicate (skip only in-open, only at "
         "day open-pctl > X ∈ {80, 95}); B-RANDOM floors under the "
         "identical rule, scalp arms only (context floor-less, "
         "stated). Weekly under Part C beside register 132; "
         "ex-lockbox; nothing registers here.", "",
         "## (a) Open-window strata — scalp arms headlined (gap = "
         "<80 median minus >=95 median; positive = degradation "
         "concentrates in stretched ATR)", "",
         "| arm | leg | window | <80 med (n) | 80-95 med (n) | >=95 "
         "med (n) | gap | null p95 | pct | clears |",
         "|---|---|---|---|---|---|---|---|---|---|"]
    for key, g in art["gaps"].items():
        instr, var, w = key.split("|")
        if var not in SCALP_ARMS:
            continue
        mid = art["strata_cells"].get(f"{key}|80-95", {})
        L.append(
            f"| {var} | {instr} | {w} "
            f"| {g['lo']['median']} ({g['lo']['n_distinct']}) "
            f"| {mid.get('median', '—')} ({mid.get('n_distinct', 0)}) "
            f"| {g['hi']['median']} ({g['hi']['n_distinct']}) "
            f"| {g['gap'] if g['gap'] is not None else '—'} "
            f"| {g['null_p95'] if g['null_p95'] is not None else '—'} "
            f"| {g['pct_vs_null'] if g['pct_vs_null'] is not None else '—'} "
            f"| {'YES' if g['clears'] else 'no'} |")
    L += ["", "## (a) Context ladder — measurable gaps only", "",
          "| leg | variant | window | gap | pct vs null | clears |",
          "|---|---|---|---|---|---|"]
    for key, g in art["gaps"].items():
        instr, var, w = key.split("|")
        if var in SCALP_ARMS or not g["measurable"]:
            continue
        L.append(f"| {instr} | {var} | {w} | {g['gap']} "
                 f"| {g['pct_vs_null']} | {'YES' if g['clears'] else 'no'} |")
    L += ["", "## (b) The conditional counterfactual — scalp arms vs "
          "the member band (positive Δ = the rule helped)", "",
          "| arm | leg | window | X | skipped (of distinct) | net Δ | "
          "stops dodged (pts) | member band med [min..max] | beats "
          "band max |", "|---|---|---|---|---|---|---|---|---|"]
    for key, c in art["counterfactual"].items():
        instr, var, w, x = key.split("|")
        if var not in SCALP_ARMS or c["skipped"] == 0:
            continue
        fb = art["scalp_floors"].get(instr, {}).get(var, {}) \
            .get(f"{w}|{x}")
        band = (f"{fb['median']} [{fb['min']}..{fb['max']}]" if fb
                else "—")
        beats = ("YES" if fb and c["net_delta"] > fb["max"] else "no"
                 if fb else "—")
        L.append(f"| {var} | {instr} | {w} | {x} "
                 f"| {c['skipped']} (of {c['n_distinct']}) "
                 f"| {c['net_delta']:+.1f} "
                 f"| {c['stops_dodged']} ({c['stops_dodged_pts']}) "
                 f"| {band} | {beats} |")
    L += ["", "## (b) Context ladder counterfactual (no floors — "
          "stated; full grid in the JSON)", "",
          "| leg | variant | window | X | skipped | net Δ |",
          "|---|---|---|---|---|---|"]
    for key, c in art["counterfactual"].items():
        instr, var, w, x = key.split("|")
        if var in SCALP_ARMS or c["skipped"] == 0:
            continue
        L.append(f"| {instr} | {var} | {w} | {x} | {c['skipped']} "
                 f"| {c['net_delta']:+.1f} |")
    L.append("")
    with open(os.path.join(OUT, "open_pause.md"), "w") as f:
        f.write("\n".join(L))


def main():
    ap = argparse.ArgumentParser()
    ap.parse_args()
    head = subprocess.run(["git", "rev-parse", "HEAD"], cwd=ROOT,
                          capture_output=True, text=True).stdout.strip()
    art = {"STAMP": ("OBSERVATIONAL conditional open-pause cut — "
                     "post-hoc-selected cell, backtest motivating not "
                     "evidential; enactment reads forward/sealed at "
                     "measurable n, per-market scoped; never "
                     "validation"),
           "engine_commit": head, **run()}
    with open(os.path.join(OUT, "open_pause.json"), "w") as f:
        json.dump(art, f, indent=2, default=str)
    _emit(art, head)
    n_cl = sum(1 for g in art["gaps"].values() if g["clears"])
    print(f"OBSERVATIONAL open pause -> {OUT}/open_pause.md "
          f"({n_cl} strata gaps clear)")


if __name__ == "__main__":
    main()
