"""H4 key-zone conditioner census (register 95 item 2; pre-registered
prereg_zone_census, counted 2026-08-28). OBSERVATIONAL. The docketed
source, verbatim in the trial log: "Use H4; look for price reversals;
flag zones where price has reversed; look for opportunities in those
zones on lower timeframes." This is the LOCATION FAMILY's first
higher-timeframe member (cross-referenced: the retest, map and
value-area signals — LOCATION_FAMILY) and the founding TF-ladder doctrine's first location
application (define high, trade low). MINT-ON-LIFT ONLY, front door.

ZONES, mechanically, on the H4 aggregation: swing extremes by the
registered fractal convention (config context.swing_k each side,
confirmed at the lag) whose reversal leg to the next opposite swing
reached >= QUALIFYING_ATR_MULT x ATR(H4 at the extreme) — the
registered qualifying-move multiplier reused; zone = the extreme's
price; ACTIVE from the reversal's confirmation (no lookahead);
INVALIDATED at the first H4 close beyond the level by the same
multiple on the far side. NO NEW NUMBERS. STORE DEPTH stated from the
file (the docket assumed ~180 bars; the store holds ~3,100 — the
thinness flag inverts to a DENSITY question, the counts print).

TAGGING: every signal fire and every journal fire in-zone/out-zone —
band = the ratified retest band, H6_PROX_ATR_FRAC x ATR(15M at fire),
against the nearest active zone. SPLITS: signal fires — initiation
hit rate in/out of zone per signal x window vs the ZONE-CONDITIONED
base (episode-begin rate of all bars in that zone state — the
conditioning-matrix method); journal fires — points per variant
in/out per window (ex-lockbox, register 85). Counts everywhere; cells
n<UNMEASURABLE_N unmeasurable; both windows; all four instruments, no
pooling. Twin-run pinned (tests/test_zone_census.py). Weekly under
Part C after first emission.
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

from engine.signal_watch import AGNOSTIC_ROWS, H6_PROX_ATR_FRAC, SignalWatch
from engine.store_loader import (in_lockbox_span, is_sealed,
                                 lockbox_boundary, zones)
from backtest.recipes import build_env
from backtest.scoreboard import (QUALIFYING_ATR_MULT, _replay, build_init,
                                 build_moves, event_derived_fires,
                                 make_cfg)

OUT = os.path.join(ROOT, "reports", "scoreboard")
TRADES_CSV = os.path.join(ROOT, "reports", "trades.csv")

UNMEASURABLE_N = 10      # the conditioning-matrix convention, reused
LOCATION_FAMILY = ("S0-H" + str(6), "S0-H11", "S1-H11", "S0-H13")


def h4_frame(instr):
    df = pd.read_csv(os.path.join(ROOT, "clean_finsa", f"{instr}_4h.csv"),
                     parse_dates=["time"])
    return df[["time", "open", "high", "low", "close"]].reset_index(
        drop=True)


def atr_series(h, l, c, period):
    tr = np.empty(len(h))
    tr[0] = h[0] - l[0]
    for i in range(1, len(h)):
        tr[i] = max(h[i] - l[i], abs(h[i] - c[i - 1]),
                    abs(l[i] - c[i - 1]))
    out = np.full(len(h), np.nan)
    for i in range(period - 1, len(h)):
        out[i] = tr[i - period + 1:i + 1].mean()
    return out


def fractal_swings(h, l, k):
    """Registered fractal convention mirrored on H4: bar i is a swing
    high if h[i] exceeds the k bars on each side (strict), a swing low
    symmetrically; confirmed at bar i+k. Returns [(idx, type, price,
    conf_idx)] in confirmation order."""
    out = []
    n = len(h)
    for i in range(k, n - k):
        if all(h[i] > h[i - m] for m in range(1, k + 1)) and \
                all(h[i] > h[i + m] for m in range(1, k + 1)):
            out.append((i, "H", float(h[i]), i + k))
        if all(l[i] < l[i - m] for m in range(1, k + 1)) and \
                all(l[i] < l[i + m] for m in range(1, k + 1)):
            out.append((i, "L", float(l[i]), i + k))
    out.sort(key=lambda s: (s[3], s[0]))
    return out


def build_zones(df, k, period, mult):
    """Zones from qualifying H4 reversals. Each: level, type,
    active_from (ns, the reversal's confirmation), invalidated_at (ns
    or None). Deterministic."""
    h, l, c = df["high"].to_numpy(), df["low"].to_numpy(), \
        df["close"].to_numpy()
    ts = df["time"].astype("int64").to_numpy()
    atr = atr_series(h, l, c, period)
    sw = fractal_swings(h, l, k)
    zones_ = []
    for a, s in enumerate(sw):
        idx, typ, price, conf = s
        if np.isnan(atr[idx]):
            continue
        nxt = next((x for x in sw[a + 1:] if x[1] != typ
                    and x[0] > idx), None)
        if nxt is None:
            continue
        leg = (price - nxt[2]) if typ == "H" else (nxt[2] - price)
        if leg < mult * atr[idx]:
            continue
        act = nxt[3]                       # reversal confirmed here
        if act >= len(ts):
            continue
        inval = None
        thr = mult * atr[idx]
        for j in range(act + 1, len(c)):
            if (typ == "H" and c[j] >= price + thr) or \
                    (typ == "L" and c[j] <= price - thr):
                inval = int(ts[j])
                break
        zones_.append({"level": price, "type": typ,
                       "h4_idx": int(idx), "active_from": int(ts[act]),
                       "invalidated_at": inval})
    return zones_


def in_zone(price, t_ns, atr15, zones_):
    """Nearest ACTIVE zone within the ratified retest band."""
    if not atr15:
        return None, None
    band = H6_PROX_ATR_FRAC * atr15
    best = None
    for z in zones_:
        if z["active_from"] > t_ns:
            continue
        if z["invalidated_at"] is not None and z["invalidated_at"] <= t_ns:
            continue
        d = abs(price - z["level"])
        if best is None or d < best[0]:
            best = (d, z)
    if best is None:
        return False, None
    return bool(best[0] <= band), round(best[0] / atr15, 3)


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
    df4 = h4_frame(instr)
    k = int(cfg.context.swing_k)
    zs = build_zones(df4, k, int(cfg.context.atr_period),
                     QUALIFYING_ATR_MULT)
    # per-bar zone state (close vs nearest active zone; bar ATR15)
    state = np.zeros(len(ts), bool)
    for i in range(len(ts)):
        a = env.atr_at("15min", ts[i])
        iz, _dist = in_zone(float(cl[i]), int(ts[i]), a, zs)
        state[i] = bool(iz)
    boundary, gl = lockbox_boundary(), zones()["go_live"]
    win_of = (lambda t: "backtest" if t < boundary else
              "forward" if t >= gl else None)
    wmask = {"backtest": ts < boundary.value, "forward": ts >= gl.value}
    bases = {}
    for w, m in wmask.items():
        for st_name, st_val in (("in", True), ("out", False)):
            sel = m & (state == st_val)
            bases[(w, st_name)] = (round(50 * float(
                np.mean(init[1][sel]) + np.mean(init[-1][sel])), 1)
                if sel.any() else None)
    fires = watch.fires + event_derived_fires(engine.narrative.events,
                                              cfg, bars, instr=instr)
    fires = [f for f in fires if f["name"] not in AGNOSTIC_ROWS
             and not is_sealed(f["ts"])]
    sig = {}
    for f in fires:
        w = win_of(f["ts"])
        if w is None:
            continue
        i = int(np.searchsorted(ts, f["ts"].value, side="right") - 1)
        if i < 0:
            continue
        st_name = "in" if state[i] else "out"
        c = sig.setdefault((f["name"], w, st_name),
                           {"n": 0, "hits": 0})
        c["n"] += 1
        c["hits"] += int(init[int(f["dir"])][i])
    sig_out = {}
    for (name, w, st_name), c in sorted(sig.items()):
        pct = round(100 * c["hits"] / c["n"], 1)
        base = bases[(w, st_name)]
        sig_out["|".join((name, w, st_name))] = {
            "n": c["n"], "hits": c["hits"], "pct": pct,
            "zone_base_pct": base,
            "lift_pp": (round(pct - base, 1) if base is not None
                        else None),
            "unmeasurable": c["n"] < UNMEASURABLE_N,
            "location_family": name in LOCATION_FAMILY}
    # journal fires (ex-lockbox)
    jr = {}
    for r in journal:
        if r["instrument"] != instr or in_lockbox_span(r["open_ts"]):
            continue
        t = pd.Timestamp(r["open_ts"])
        w = win_of(t)
        if w is None:
            continue
        a = (float(r["atr_entry"])
             if r["atr_entry"] not in ("", "None") else None)
        iz, _dist = in_zone(float(r["open_price"]), t.value, a, zs)
        if iz is None:
            continue
        jr.setdefault((r["variant"], w, "in" if iz else "out"),
                      []).append(float(r["points"]))
    jr_out = {"|".join(k): {"n": len(v),
                            "median_pts": round(float(np.median(v)), 2),
                            "net_pts": round(float(np.sum(v)), 1),
                            "unmeasurable": len(v) < UNMEASURABLE_N}
              for k, v in sorted(jr.items())}
    span_lo = ts[0] if len(ts) else 0
    active_at_span = sum(1 for z in zs if z["active_from"] <= ts[-1]
                         and (z["invalidated_at"] is None
                              or z["invalidated_at"] > span_lo))
    return {"instrument": instr, "h4_store_bars": int(len(df4)),
            "h4_span": [str(df4["time"].iloc[0]),
                        str(df4["time"].iloc[-1])],
            "swing_k": k, "reversal_atr_mult": QUALIFYING_ATR_MULT,
            "band_atr_frac": H6_PROX_ATR_FRAC,
            "zones_total": len(zs),
            "zones_active_over_1m_span": active_at_span,
            "in_zone_bar_fraction": round(float(state.mean()), 4),
            "zone_bases_init_pct": {"|".join(k): v
                                    for k, v in bases.items()},
            "signal_cells": sig_out, "journal_cells": jr_out}


def _emit(results, head):
    L = ["# H4 Key-Zone Conditioner Census (GENERATED by "
         "backtest.zone_census)", "",
         "Terms: [docs/GLOSSARY.md](../../docs/GLOSSARY.md).", "",
         f"Engine `{head[:9]}` — OBSERVATIONAL, pre-registered "
         "(prereg_zone_census, register 95 item 2). The docketed "
         "source measured mechanically: H4 fractal swing extremes "
         "(registered swing_k) whose reversal reached the registered "
         f"{QUALIFYING_ATR_MULT:g}xATR(H4), active from confirmation, "
         "invalidated at the same multiple beyond; fires tagged "
         f"in/out of the ratified retest band ({H6_PROX_ATR_FRAC:g}x"
         "ATR15). STATISTIC SHAPE (74-B): single-cell conditioned "
         "lift vs the ZONE-CONDITIONED base (episode-begin rate of "
         "bars in that zone state); journal cells descriptive. Cells "
         f"n<{UNMEASURABLE_N} UNMEASURABLE (omitted here, in the "
         "JSON). LOCATION FAMILY rows marked (*). Store depth stated "
         "per instrument — the docket's thinness assumption inverts "
         "to density, counts print. MINT-ON-LIFT ONLY, front door; "
         "no pooling across instruments.", ""]
    for res in results:
        L += [f"## {res['instrument']} — H4 store {res['h4_store_bars']} "
              f"bars ({res['h4_span'][0][:10]} → "
              f"{res['h4_span'][1][:10]}); zones {res['zones_total']} "
              f"total, {res['zones_active_over_1m_span']} active over "
              f"the 1M span; in-zone bar fraction "
              f"{100 * res['in_zone_bar_fraction']:.1f}%", "",
              "Zone-conditioned initiation bases: "
              + ", ".join(f"{k} {v}%" for k, v in
                          res["zone_bases_init_pct"].items()), "",
              "| signal | window | zone | n | init % | base % | lift |",
              "|---|---|---|---|---|---|---|"]
        rows = [(k.split("|"), v) for k, v in res["signal_cells"].items()
                if not v["unmeasurable"]]
        rows.sort(key=lambda r: (r[0][0], r[0][1], r[0][2]))
        for (name, w, st), v in rows:
            mark = "*" if v["location_family"] else ""
            L.append(f"| {name}{mark} | {w} | {st} | {v['n']} "
                     f"| {v['pct']} | {v['zone_base_pct']} "
                     f"| {v['lift_pp']:+.1f}pp |"
                     if v["lift_pp"] is not None else
                     f"| {name}{mark} | {w} | {st} | {v['n']} "
                     f"| {v['pct']} | — | — |")
        L += ["", "| variant | window | zone | n | median pts | net |",
              "|---|---|---|---|---|---|"]
        for k, v in res["journal_cells"].items():
            if v["unmeasurable"]:
                continue
            var, w, st = k.split("|")
            L.append(f"| {var} | {w} | {st} | {v['n']} "
                     f"| {v['median_pts']} | {v['net_pts']} |")
        L.append("")
    with open(os.path.join(OUT, "zone_census.md"), "w") as f:
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
    journal = list(csv.DictReader(open(TRADES_CSV)))
    results = []
    for instr in a.instr:
        print(f"# zone_census: {instr} ...", file=sys.stderr)
        results.append(run_instrument(instr, journal))
    art = {"STAMP": ("OBSERVATIONAL H4 key-zone conditioner census — "
                     "the location family's first higher-TF member; "
                     "mint-on-lift only; never validation"),
           "engine_commit": head, "results": results}
    with open(os.path.join(OUT, "zone_census.json"), "w") as f:
        json.dump(art, f, indent=2, default=str)
    _emit(results, head)
    print(f"OBSERVATIONAL zone census -> {OUT}/zone_census.md")


if __name__ == "__main__":
    main()
