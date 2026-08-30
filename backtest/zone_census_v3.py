"""Zone census v3 — DEPARTURE BASES (register 111; pre-registered
prereg_zone_census_v3, counted 2026-08-30). OBSERVATIONAL. A NEW
DEFINITION AND A NEW SOURCE — not a rerun of the parked v2 (register
97 stands: extreme-based zones measured-and-unsupported; departure-
based zones are a different object). ORIGIN: operator D1/H4 chart
observation, uk100fut, 2026-08-30 — consolidations that break
impulsively leave a base price returns to.

THE DEFINITION, every constant from existing conventions or the unit
(one flagged choice): a BASE is >= BASE_MIN_BARS consecutive source-TF
bars (BASE_MIN_BARS = the registered swing_k — no new count) whose
collective range (max high - min low) <= BASE_RANGE_ATR x ATR(source
TF at the base's last bar); BASE_RANGE_ATR = 1.0 is the UNIT multiple,
implementer-chosen where a choice was unavoidable, FLAGGED. The
DEPARTURE: within the next BASE_MIN_BARS bars a close >= mult x
ATR beyond the base's edge, mult in DEPART_MULTS — the registered
qualifying multiple and its double (the v2 ladder's multiples, reused).
The ZONE IS THE BASE'S RANGE [low, high] — demand if the departure
went up, supply if down. ACTIVE from the OPEN OF THE BAR AFTER the
departure close (no lookahead — v2's active-at-confirmation-bar-open
convention would leak up to one source bar on D1, stated and
tightened). INVALIDATED on FULL TRADE-THROUGH: the first source-TF
close beyond the FAR edge. SOURCE TF: D1 primary, H4 secondary
(SOURCE_TFS) — the store's native products.

EXPECTED SCARCITY, STATED AT REGISTRATION: D1 should carry roughly
5-15 active zones per leg; HUNDREDS = THE DEFINITION FAILED, and the
census says so (the SCARCITY CHECK prints WITHIN / BELOW / ABOVE per
rung and FAILED at >= 100 active at once). H4 carries no stated band
(secondary; printed, not judged).

MEASUREMENT (the v2 conditioner machinery, range-tagged): 1M closes
tagged in/out of the nearest active zone's RANGE (no band — the zone
is the range); per rung x window: in/out fire splits vs the
ZONE-CONDITIONED directional base (the conditioning-matrix method,
per-direction average — never init_any); journal splits per variant
with the register-105 CONSISTENCY STATISTICS (per_market_watch.
cell_stats: median, win rate, weekly count, tail-carry) and a
SELECTION-NULL — per instrument x window x rung, the in/out label is
permuted across the journal rows (cell sizes kept), the best in-zone
median and win rate across variants recorded per seed; an in-zone
cell reads against that best-of-field. Both windows; all four legs; no
pooling; journal ex-lockbox; MINT-ON-LIFT ONLY, front door. Twin-run
pinned (tests/test_zone_census_v3.py). Weekly under Part C after v2.
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
from backtest.recipes import build_env
from backtest.scoreboard import (QUALIFYING_ATR_MULT, _replay, build_init,
                                 build_moves, event_derived_fires,
                                 make_cfg)
from backtest.zone_census import atr_series, session_ordinals
from backtest.per_market_watch import (MIN_CELL_N, NULL_SEEDS, cell_stats,
                                       null_p95, percentile_vs)

OUT = os.path.join(ROOT, "reports", "scoreboard")
TRADES_CSV = os.path.join(ROOT, "reports", "trades.csv")

SOURCE_TFS = ("1d", "4h")            # D1 primary, H4 secondary
DEPART_MULTS = (QUALIFYING_ATR_MULT, 2 * QUALIFYING_ATR_MULT)
BASE_RANGE_ATR = 1.0     # the UNIT multiple — implementer-chosen where a
                         # choice was unavoidable, FLAGGED at prereg
EXPECTED_ACTIVE_D1 = (5, 15)   # stated scarcity band, D1 (register 111)
SCARCITY_FAIL_AT = 100         # "hundreds = the definition failed"
UNMEASURABLE_N = 10            # the conditioning-matrix convention


def rung_name(tf, mult):
    return f"{tf}/x{mult:g}"


def source_frame(instr, tf):
    df = pd.read_csv(os.path.join(ROOT, "clean_finsa",
                                  f"{instr}_{tf}.csv"),
                     parse_dates=["time"])
    if "ldate" not in df.columns:
        df["ldate"] = df["time"].dt.date.astype(str)
    return df[["time", "open", "high", "low", "close",
               "ldate"]].reset_index(drop=True)


def departure_bases(df, k, period, mult, base_range_atr=BASE_RANGE_ATR):
    """Zones from consolidation-then-impulsive-departure at one rung.
    Base = >= k bars, collective range <= base_range_atr x ATR at the
    base's last bar; departure = within the next k bars a close >=
    mult x that ATR beyond the base's edge. Zone = the base's range;
    active from the NEXT bar's open after the departure close;
    invalidated at the first close beyond the FAR edge. Greedy
    left-to-right: a base extends while the range condition holds;
    after a confirmed zone the scan resumes past the departure bar.
    Deterministic."""
    h = df["high"].to_numpy()
    l = df["low"].to_numpy()
    c = df["close"].to_numpy()
    ts = df["time"].astype("int64").to_numpy()
    sess = session_ordinals(df["ldate"].astype(str).tolist())
    atr = atr_series(h, l, c, period)
    n = len(df)
    out = []
    i = 0
    while i < n - k:
        j = i
        hi, lo = h[i], l[i]
        while j + 1 < n:
            nh, nl = max(hi, h[j + 1]), min(lo, l[j + 1])
            if np.isnan(atr[j + 1]) or \
                    (nh - nl) > base_range_atr * atr[j + 1]:
                break
            j += 1
            hi, lo = nh, nl
        if j - i + 1 < k or np.isnan(atr[j]):
            i += 1
            continue
        thr = mult * atr[j]
        zone = None
        for m in range(j + 1, min(j + k, n - 1)):
            if c[m] >= hi + thr:
                zone = ("D", m)               # departed up: demand base
                break
            if c[m] <= lo - thr:
                zone = ("S", m)               # departed down: supply base
                break
        if zone is None:
            i += 1
            continue
        typ, m = zone
        inval = None
        for q in range(m + 1, n):
            if (typ == "D" and c[q] < lo) or (typ == "S" and c[q] > hi):
                inval = int(ts[q])            # full trade-through
                break
        out.append({"lo": float(lo), "hi": float(hi), "type": typ,
                    "base_idx": int(i), "base_bars": int(j - i + 1),
                    "depart_idx": int(m),
                    "active_from": int(ts[m + 1]),
                    "invalidated_at": inval,
                    "active_sess": int(sess[min(m + 1, n - 1)])})
        i = m + 1
    return out


def in_zone_v3(price, t_ns, zones_):
    """Scalar tagging (tests + spot checks): nearest ACTIVE zone whose
    RANGE contains the price -> (in, zone_index)."""
    best = None
    for zi, z in enumerate(zones_):
        if z["active_from"] > t_ns:
            continue
        if z["invalidated_at"] is not None and z["invalidated_at"] <= t_ns:
            continue
        if z["lo"] <= price <= z["hi"]:
            d = abs(price - 0.5 * (z["lo"] + z["hi"]))
            if best is None or d < best[0]:
                best = (d, zi)
    return (best is not None), (best[1] if best else None)


def tag_bars_v3(ts, cl, zones_):
    """Vectorized per-bar tagging: nearest active zone whose range
    contains the close (-1 if none). Chunked broadcast."""
    n = len(ts)
    zid = np.full(n, -1)
    if not zones_:
        return zid
    lo = np.array([z["lo"] for z in zones_])
    hi = np.array([z["hi"] for z in zones_])
    act = np.array([z["active_from"] for z in zones_])
    inv = np.array([z["invalidated_at"] if z["invalidated_at"] is not None
                    else np.iinfo(np.int64).max for z in zones_])
    mid = 0.5 * (lo + hi)
    step = 4000
    for s in range(0, n, step):
        e = min(n, s + step)
        t = ts[s:e, None]
        p = cl[s:e, None]
        ok = (act[None, :] <= t) & (inv[None, :] > t) \
            & (p >= lo[None, :]) & (p <= hi[None, :])
        d = np.where(ok, np.abs(p - mid[None, :]), np.inf)
        j = d.argmin(axis=1)
        zid[s:e] = np.where(np.isfinite(d[np.arange(e - s), j]), j, -1)
    return zid


def active_over_span(zones_, t0, t1):
    """(alive at any point in [t0, t1], max simultaneously active) —
    seeded with zones already active at t0."""
    if not zones_:
        return 0, 0
    alive = sum(1 for z in zones_ if z["active_from"] <= t1
                and (z["invalidated_at"] is None
                     or z["invalidated_at"] > t0))
    marks = sorted([(z["active_from"], 1) for z in zones_]
                   + [(z["invalidated_at"], -1) for z in zones_
                      if z["invalidated_at"] is not None])
    cur = sum(d for t_, d in marks if t_ <= t0)
    peak = cur
    for t_, d in marks:
        if t_ <= t0:
            continue
        if t_ > t1:
            break
        cur += d
        peak = max(peak, cur)
    return int(alive), int(peak)


def scarcity(tf, peak):
    """The stated check: D1 expects EXPECTED_ACTIVE_D1 active at once;
    hundreds = the definition failed; H4 is printed, not judged."""
    if peak >= SCARCITY_FAIL_AT:
        return "FAILED (hundreds — the definition failed; the census says so)"
    if tf != "1d":
        return f"(H4 secondary — no stated band; {peak} at once)"
    lo, hi = EXPECTED_ACTIVE_D1
    if peak < lo:
        return f"BELOW the stated band [{lo}-{hi}]"
    if peak > hi:
        return f"ABOVE the stated band [{lo}-{hi}]"
    return f"WITHIN the stated band [{lo}-{hi}]"


def journal_null(rows, seed_labels):
    """Selection-null over one instrument x window x rung: the in/out
    label permuted across the journal rows (cell sizes kept); best
    in-zone median and win rate across variant cells at n >=
    MIN_CELL_N, non-tail-carried, per seed. NaN = no rankable cell."""
    best_md, best_wr = [], []
    for seed in NULL_SEEDS:
        rs = np.random.RandomState(seed)
        perm = rs.permutation(len(seed_labels))
        cells = {}
        for i, j in enumerate(perm):
            if seed_labels[j] != "in":
                continue
            cells.setdefault(rows[i]["variant"], []).append(rows[i])
        ok = [cell_stats(v) for v in cells.values()]
        ok = [s for s in ok if s["n"] >= MIN_CELL_N
              and not s["tail_carried"]]
        best_md.append(max(s["median"] for s in ok) if ok else np.nan)
        best_wr.append(max(s["win_rate"] for s in ok) if ok else np.nan)
    return np.array(best_md, float), np.array(best_wr, float)


def run_instrument(instr, journal):
    cfg = make_cfg({"session_model.extended_hours": True,
                    "session_model.ladder": True,
                    "debug.structure": True})
    watch = SignalWatch()
    engine, bars, _ = _replay(cfg, instr, engine_hook=watch.attach)
    env = build_env(instr, cfg, bars)
    qual, episodes, series, _d = build_moves(
        bars[cfg.mtf.execution_tf], bars[cfg.mtf.signal_tf],
        cfg.context.atr_period)
    ts, cl = series[0], series[1]
    episodes = [e for e in episodes if not is_sealed(e["start"])]
    init = build_init(episodes, series)
    k = int(cfg.context.swing_k)
    period = int(cfg.context.atr_period)
    boundary, gl = lockbox_boundary(), zones()["go_live"]
    win_of = (lambda t: "backtest" if t < boundary else
              "forward" if t >= gl else None)
    wmask = {"backtest": ts < boundary.value, "forward": ts >= gl.value}
    fires = watch.fires + event_derived_fires(engine.narrative.events,
                                              cfg, bars, instr=instr)
    fires = [f for f in fires if f["name"] not in AGNOSTIC_ROWS
             and not is_sealed(f["ts"])]
    fire_idx = [(f, int(np.searchsorted(ts, f["ts"].value, side="right")
                        - 1)) for f in fires]
    fire_idx = [(f, i) for f, i in fire_idx if i >= 0
                and win_of(f["ts"]) is not None]
    jrows = []
    for r in journal:
        if r["instrument"] != instr or in_lockbox_span(r["open_ts"]):
            continue
        t = pd.Timestamp(r["open_ts"])
        w = win_of(t)
        if w is None:
            continue
        i = int(np.searchsorted(ts, t.value, side="left"))
        if i < len(ts) and ts[i] == t.value:
            jrows.append((r, i, w,
                          "%d-W%02d" % t.isocalendar()[:2]))
    frames = {tf: source_frame(instr, tf) for tf in SOURCE_TFS}
    ladder = {}
    for tf in SOURCE_TFS:
        for mult in DEPART_MULTS:
            rn = rung_name(tf, mult)
            zs = departure_bases(frames[tf], k, period, mult)
            zid = tag_bars_v3(ts, cl, zs)
            state = zid >= 0
            alive, peak = active_over_span(zs, int(ts[0]), int(ts[-1]))
            bases = {}
            for w, m in wmask.items():
                for st_name, st_val in (("in", True), ("out", False)):
                    sel = m & (state == st_val)
                    # per-direction average (the conditioning-matrix
                    # convention) — never init_any
                    bases[(w, st_name)] = (
                        round(50 * float(np.mean(init[1][sel])
                                         + np.mean(init[-1][sel])), 1)
                        if sel.any() else None)
            pooled, sig_cells = {}, {}
            for f, i in fire_idx:
                w = win_of(f["ts"])
                st = "in" if state[i] else "out"
                hit = int(init[int(f["dir"])][i])
                for d_, key in ((pooled, (w, st)),
                                (sig_cells, (f["name"], w, st))):
                    cbin = d_.setdefault(key, {"n": 0, "hits": 0})
                    cbin["n"] += 1
                    cbin["hits"] += hit

            def _cells(d):
                out = {}
                for key, cb in sorted(d.items()):
                    w, st = key[-2], key[-1]
                    base = bases.get((w, st))
                    pct = (round(100 * cb["hits"] / cb["n"], 1)
                           if cb["n"] else None)
                    out["|".join(map(str, key))] = {
                        "n": cb["n"], "hits": cb["hits"], "pct": pct,
                        "zone_base_pct": base,
                        "lift_pp": (round(pct - base, 1)
                                    if pct is not None and base is not None
                                    else None),
                        "unmeasurable": cb["n"] < UNMEASURABLE_N}
                return out
            # journal: register-105 consistency statistics + selection null
            jw = {}
            for r, i, w, week in jrows:
                jw.setdefault(w, []).append(
                    {"variant": r["variant"], "pts": float(r["points"]),
                     "week": week, "st": "in" if state[i] else "out"})
            jcells = {}
            for w, rows in sorted(jw.items()):
                labels = [r["st"] for r in rows]
                nb_md, nb_wr = journal_null(rows, labels)
                per_var = {}
                for r in rows:
                    per_var.setdefault((r["variant"], r["st"]),
                                       []).append(r)
                for (var, st), rr in sorted(per_var.items()):
                    s = cell_stats(rr)
                    entry = {**s, "window": w, "variant": var, "zone": st}
                    if st == "in" and s["n"] >= MIN_CELL_N:
                        entry["sel_pct_median"] = percentile_vs(
                            nb_md, s["median"])
                        entry["sel_pct_win"] = percentile_vs(
                            nb_wr, s["win_rate"])
                        entry["beats_field_null_median"] = bool(
                            s["median"] > null_p95(nb_md))
                        entry["beats_field_null_win"] = bool(
                            s["win_rate"] > null_p95(nb_wr))
                    jcells["|".join((var, w, st))] = entry
            ladder[rn] = {
                "tf": tf, "depart_mult": mult,
                "zones_total": len(zs),
                "zones_alive_over_1m_span": alive,
                "active_at_once_max": peak,
                "scarcity": {"verdict": scarcity(tf, peak),
                             "expected_d1": list(EXPECTED_ACTIVE_D1),
                             "fail_at": SCARCITY_FAIL_AT},
                "in_zone_bar_fraction": round(float(state.mean()), 4),
                "zone_bases_init_pct": {"|".join(kk): v
                                        for kk, v in bases.items()},
                "pooled": _cells(pooled),
                "signal_cells": _cells(sig_cells),
                "journal_cells": jcells}
    return {"instrument": instr,
            "source_bars": {tf: int(len(frames[tf]))
                            for tf in SOURCE_TFS},
            "swing_k": k, "base_range_atr_FLAGGED": BASE_RANGE_ATR,
            "ladder": ladder}


def _emit(results, head):
    L = ["# Zone Census v3 — departure bases (GENERATED by "
         "backtest.zone_census_v3)", "",
         "Terms: [docs/GLOSSARY.md](../../docs/GLOSSARY.md).", "",
         f"Engine `{head[:9]}` — OBSERVATIONAL, pre-registered "
         "(prereg_zone_census_v3, register 111). A NEW DEFINITION AND "
         "SOURCE — not a rerun of the parked v2 (register 97 stands; "
         "extreme-based ≠ departure-based). Zones = DEPARTURE BASES: "
         f"a consolidation of >= swing_k source-TF bars (range <= "
         f"{BASE_RANGE_ATR:g}xATR — the unit multiple, FLAGGED) that "
         "breaks impulsively (close >= {1.5, 3}xATR beyond the edge "
         "within swing_k bars); the zone IS the base's range; active "
         "from the next bar's open; dead on a close through the far "
         "edge. Source TF: D1 primary / H4 secondary. EXPECTED "
         f"SCARCITY (stated at registration): D1 ~{EXPECTED_ACTIVE_D1[0]}"
         f"-{EXPECTED_ACTIVE_D1[1]} active zones per leg; hundreds = "
         "the definition FAILED, and this page says so. STATISTIC "
         "SHAPES (74-B): pooled in-zone initiation vs the "
         "zone-conditioned directional base (conditioned lift); journal "
         "in-zone cells on the register-105 CONSISTENCY statistics with "
         "a SELECTION-NULL (in/out labels permuted, best-of-variants "
         f"per seed, {len(NULL_SEEDS)} pinned seeds). Cells "
         f"n<{UNMEASURABLE_N} unmeasurable; journal measurable at "
         f"n>={MIN_CELL_N}. MINT-ON-LIFT ONLY, front door; no pooling "
         "across instruments; ex-lockbox.", ""]
    for res in results:
        L += [f"## {res['instrument']} — D1 {res['source_bars']['1d']} "
              f"bars, H4 {res['source_bars']['4h']} bars", "",
              "### Scarcity and density (the stated check)", "",
              "| rung | zones total | alive over 1M span | max active "
              "at once | scarcity | in-zone bars % |",
              "|---|---|---|---|---|---|"]
        for rn, r in res["ladder"].items():
            L.append(f"| {rn} | {r['zones_total']} "
                     f"| {r['zones_alive_over_1m_span']} "
                     f"| {r['active_at_once_max']} "
                     f"| {r['scarcity']['verdict']} "
                     f"| {100 * r['in_zone_bar_fraction']:.1f} |")
        L += ["", "### Pooled in-zone initiation vs the zone-conditioned "
              "base", "",
              "| rung | window | zone | n | init % | base % | lift |",
              "|---|---|---|---|---|---|---|"]
        for rn, r in res["ladder"].items():
            for key, cb in r["pooled"].items():
                w, st = key.split("|")
                dim = "°" if cb["unmeasurable"] else ""
                lift = (f"{cb['lift_pp']:+.1f}pp"
                        if cb["lift_pp"] is not None else "—")
                L.append(f"| {rn} | {w} | {st} | {dim}{cb['n']} "
                         f"| {cb['pct']} | {cb['zone_base_pct']} "
                         f"| {lift} |")
        L += ["", "### Journal in-zone cells (register-105 consistency "
              "statistics; selection-null in-zone only; measurable "
              f"n>={MIN_CELL_N})", "",
              "| rung | variant | window | zone | n | median | win | "
              "+weeks/meas | sel-pct win / median | beats null win / "
              "median | tail |", "|---|---|---|---|---|---|---|---|---|---|---|"]
        printed = 0
        for rn, r in res["ladder"].items():
            for key, s in r["journal_cells"].items():
                if s["zone"] != "in" or s["n"] < MIN_CELL_N:
                    continue
                printed += 1
                sp = (f"{s.get('sel_pct_win')} / {s.get('sel_pct_median')}"
                      if "sel_pct_win" in s else "— / —")
                bn = (f"{'YES' if s.get('beats_field_null_win') else 'no'} / "
                      f"{'YES' if s.get('beats_field_null_median') else 'no'}"
                      if "beats_field_null_win" in s else "— / —")
                L.append(f"| {rn} | {s['variant']} | {s['window']} | in "
                         f"| {s['n']} | {s['median']:+.2f} "
                         f"| {100 * s['win_rate']:.0f}% "
                         f"| {s['weeks_pos']}/{s['weeks_meas']} | {sp} "
                         f"| {bn} "
                         f"| {'TAIL' if s['tail_carried'] else ''} |")
        if not printed:
            L.append("| (no measurable in-zone journal cell) "
                     "| | | | | | | | | | |")
        L.append("")
    with open(os.path.join(OUT, "zone_census_v3.md"), "w") as f:
        f.write("\n".join(L))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--instr", nargs="*",
                    default=["uk100fut", "ger40fut", "nas100fut",
                             "us30fut"])
    a = ap.parse_args()
    os.makedirs(OUT, exist_ok=True)
    head = subprocess.run(["git", "rev-parse", "HEAD"], cwd=ROOT,
                          capture_output=True, text=True).stdout.strip()
    journal = list(csv.DictReader(
        (l for l in open(TRADES_CSV) if not l.startswith("#"))))
    results = []
    for instr in a.instr:
        print(f"# zone_census_v3: {instr} ...", file=sys.stderr)
        results.append(run_instrument(instr, journal))
    art = {"STAMP": ("OBSERVATIONAL zone census v3 — departure bases; "
                     "a new definition, not a v2 rerun; scarcity check "
                     "stated at registration; mint-on-lift only; never "
                     "validation"),
           "engine_commit": head,
           "ladder": {"source_tfs": list(SOURCE_TFS),
                      "depart_mults": list(DEPART_MULTS),
                      "base_range_atr_FLAGGED": BASE_RANGE_ATR,
                      "expected_active_d1": list(EXPECTED_ACTIVE_D1),
                      "scarcity_fail_at": SCARCITY_FAIL_AT},
           "results": results}
    with open(os.path.join(OUT, "zone_census_v3.json"), "w") as f:
        json.dump(art, f, indent=2, default=str)
    _emit(results, head)
    print(f"OBSERVATIONAL zone census v3 -> {OUT}/zone_census_v3.md")


if __name__ == "__main__":
    main()
