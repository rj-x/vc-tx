"""H4 key-zone conditioner census — v2, the STRICTNESS LADDER (register
95 item 2 built; register 96 re-registered as a ladder; pre-registered
prereg_zone_census + AMENDMENT_zone_census_v2_ladder, counted).
OBSERVATIONAL. The docketed source, verbatim in the trial log: "Use
H4; look for price reversals; flag zones where price has reversed;
look for opportunities in those zones on lower timeframes" — and the
operator's instinct: significant reversals, relatively recent, "not
last year". The LOCATION FAMILY's first higher-timeframe member
(cross-referenced: the retest, map and value-area signals —
LOCATION_FAMILY); the founding TF-ladder doctrine's first location
application (define high, trade low). MINT-ON-LIFT ONLY, front door.

THE LADDER, every rung from existing conventions or the source's own
structure — NO INVENTED THRESHOLDS: (a) reversal multiple in
REVERSAL_MULTS x ATR(H4) — the registered qualifying multiple and its
double; (b) extreme-significance: the swing was the S-session
high/low when formed, S in SIG_SESSIONS (sessions = the store's
native ldate field; None = no filter). v1 (1.5x, no filter) is the
loosest rung and the NULL ANCHOR. Zones: H4 fractal swing extremes by
the registered convention (config context.swing_k), reversal leg to
the next opposite swing >= the rung's multiple, ACTIVE from the
reversal's confirmation (no lookahead), INVALIDATED at the first H4
close beyond the level by the same multiple.

FRESHNESS is MEASURED, never assumed: zone age in sessions at the
fire (bins from the same session ladder — reporting bins, not
thresholds) and touch number (a visit = a contiguous run of in-band
1M closes on that zone); reaction quality by age bin and by touch
number, signals POOLED per instrument for the decay curve (a property
of the zone, not a signal claim — stated). PER RUNG: zones, active-
at-once, in-zone bar fraction, in-zone fires, pooled in-zone
initiation vs the ZONE-CONDITIONED base (episode-begin rate of all
bars in that zone state — the conditioning-matrix method): the
DENSITY-vs-LIFT CURVE, so "significant and recent" gets its
mechanical values from the table rather than by fiat.

TAGGING band = the ratified retest band, H6_PROX_ATR_FRAC x ATR(15M).
Per-signal cells per rung in the JSON (n<UNMEASURABLE_N unmeasurable);
journal ex-lockbox (register 85); both windows; all four instruments,
no pooling. Twin-run pinned (tests/test_zone_census.py). Weekly under
Part C.
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
REVERSAL_MULTS = (QUALIFYING_ATR_MULT, 2 * QUALIFYING_ATR_MULT)
SIG_SESSIONS = (None, 1, 3, 5)      # the source's session structure
AGE_BINS = (1, 3, 5)                # reporting bins from the same ladder
TOUCH_BINS = (1, 2, 3)              # 1st / 2nd / 3rd / 4+


def rung_name(mult, sig):
    return f"x{mult:g}/{'any' if sig is None else f'{sig}s'}"


def h4_frame(instr):
    df = pd.read_csv(os.path.join(ROOT, "clean_finsa", f"{instr}_4h.csv"),
                     parse_dates=["time"])
    keep = ["time", "open", "high", "low", "close"]
    if "ldate" in df.columns:
        keep.append("ldate")
    else:
        df["ldate"] = df["time"].dt.date.astype(str)
        keep.append("ldate")
    return df[keep].reset_index(drop=True)


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
    """Registered fractal convention mirrored on H4 (strict both sides,
    confirmed at bar i+k). [(idx, type, price, conf_idx)] in
    confirmation order."""
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


def session_ordinals(ldates):
    """Distinct-session ordinal per H4 bar from the native ldate."""
    ords, cur, last = [], -1, None
    for d in ldates:
        if d != last:
            cur += 1
            last = d
        ords.append(cur)
    return np.array(ords)


def significant(idx, typ, h, l, sess_ord, s_sessions):
    """The swing was the S-session high/low when formed: its price is
    the extreme over all bars whose session ordinal lies within the
    last S sessions up to and including its own."""
    if s_sessions is None:
        return True
    lo_ord = sess_ord[idx] - s_sessions + 1
    m = (sess_ord <= sess_ord[idx]) & (sess_ord >= lo_ord)
    m[idx + 1:] = False
    return bool(h[idx] >= h[m].max()) if typ == "H" \
        else bool(l[idx] <= l[m].min())


def build_zones(df, k, period, mult, sig_sessions=None):
    """Zones from qualifying H4 reversals at one rung. Each: level,
    type, h4_idx, active_from (ns), invalidated_at (ns|None),
    active_sess (session ordinal at activation). Deterministic."""
    h, l, c = df["high"].to_numpy(), df["low"].to_numpy(), \
        df["close"].to_numpy()
    ts = df["time"].astype("int64").to_numpy()
    sess = session_ordinals(df["ldate"].astype(str).tolist())
    atr = atr_series(h, l, c, period)
    sw = fractal_swings(h, l, k)
    out = []
    for a, s in enumerate(sw):
        idx, typ, price, conf = s
        if np.isnan(atr[idx]):
            continue
        if not significant(idx, typ, h, l, sess, sig_sessions):
            continue
        nxt = next((x for x in sw[a + 1:] if x[1] != typ
                    and x[0] > idx), None)
        if nxt is None:
            continue
        leg = (price - nxt[2]) if typ == "H" else (nxt[2] - price)
        thr = mult * atr[idx]
        if leg < thr:
            continue
        act = nxt[3]
        if act >= len(ts):
            continue
        inval = None
        for j in range(act + 1, len(c)):
            if (typ == "H" and c[j] >= price + thr) or \
                    (typ == "L" and c[j] <= price - thr):
                inval = int(ts[j])
                break
        out.append({"level": price, "type": typ, "h4_idx": int(idx),
                    "active_from": int(ts[act]),
                    "invalidated_at": inval,
                    "active_sess": int(sess[act])})
    return out


def in_zone(price, t_ns, atr15, zones_):
    """Scalar tagging (tests + journal rows): nearest ACTIVE zone
    within the ratified band -> (in, dist_atr, zone_index)."""
    if not atr15:
        return None, None, None
    band = H6_PROX_ATR_FRAC * atr15
    best = None
    for zi, z in enumerate(zones_):
        if z["active_from"] > t_ns:
            continue
        if z["invalidated_at"] is not None and z["invalidated_at"] <= t_ns:
            continue
        d = abs(price - z["level"])
        if best is None or d < best[0]:
            best = (d, zi)
    if best is None:
        return False, None, None
    return bool(best[0] <= band), round(best[0] / atr15, 3), best[1]


def tag_bars(ts, cl, atr15, zones_):
    """Vectorized per-bar tagging: nearest active zone index (-1 if
    none within band). Chunked broadcast over bars x zones."""
    n = len(ts)
    zid = np.full(n, -1)
    if not zones_:
        return zid
    lvl = np.array([z["level"] for z in zones_])
    act = np.array([z["active_from"] for z in zones_])
    inv = np.array([z["invalidated_at"] if z["invalidated_at"] is not None
                    else np.iinfo(np.int64).max for z in zones_])
    band = H6_PROX_ATR_FRAC * atr15
    step = 4000
    for s in range(0, n, step):
        e = min(n, s + step)
        t = ts[s:e, None]
        alive = (act[None, :] <= t) & (inv[None, :] > t)
        d = np.abs(cl[s:e, None] - lvl[None, :])
        d = np.where(alive, d, np.inf)
        j = d.argmin(axis=1)
        dm = d[np.arange(e - s), j]
        ok = (dm <= band[s:e]) & np.isfinite(dm)
        zid[s:e] = np.where(ok, j, -1)
    return zid


def visit_numbers(zid):
    """Touch number per bar: the ordinal of the contiguous in-band
    visit on that zone (1 = first visit), -1 off-zone."""
    n = len(zid)
    out = np.full(n, -1)
    count = {}
    prev = -1
    for i in range(n):
        z = zid[i]
        if z >= 0:
            if z != prev:
                count[z] = count.get(z, 0) + 1
            out[i] = count[z]
        prev = z
    return out


def active_at_once(zones_, t0, t1):
    """Max number of zones simultaneously active over [t0, t1] —
    seeded with those already active at t0 (zones can activate years
    before the 1M span). Deterministic."""
    if not zones_:
        return 0
    big = np.iinfo(np.int64).max
    marks = sorted([(z["active_from"], 1) for z in zones_]
                   + [(z["invalidated_at"], -1) for z in zones_
                      if z["invalidated_at"] is not None])
    cur = 0
    for t_, d in marks:
        if t_ <= t0:
            cur += d
    peak = cur
    for t_, d in marks:
        if t_ <= t0:
            continue
        if t_ > t1:
            break
        cur += d
        peak = max(peak, cur)
    return int(peak)


def _bin(v, edges):
    for k, edge in enumerate(edges):
        if v <= edge:
            return f"<={edge}"
    return f">{edges[-1]}"


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
    atr15 = np.array([env.atr_at("15min", t) or np.nan for t in ts])
    df4 = h4_frame(instr)
    k = int(cfg.context.swing_k)
    period = int(cfg.context.atr_period)
    h4_ts = df4["time"].astype("int64").to_numpy()
    h4_sess = session_ordinals(df4["ldate"].astype(str).tolist())
    bar_sess = h4_sess[np.clip(np.searchsorted(h4_ts, ts, side="right")
                               - 1, 0, len(h4_sess) - 1)]
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
        if win_of(t) is None:
            continue
        i = int(np.searchsorted(ts, t.value, side="left"))
        if i < len(ts) and ts[i] == t.value:
            jrows.append((r, i, win_of(t)))
    ladder = {}
    for mult in REVERSAL_MULTS:
        for sig in SIG_SESSIONS:
            rn = rung_name(mult, sig)
            zs = build_zones(df4, k, period, mult, sig)
            zid = tag_bars(ts, cl, atr15, zs)
            state = zid >= 0
            vnum = visit_numbers(zid)
            z_act = np.array([z["active_sess"] for z in zs]) if zs \
                else np.zeros(0, int)
            peak = active_at_once(zs, int(ts[0]), int(ts[-1]))
            bases = {}
            for w, m in wmask.items():
                for st_name, st_val in (("in", True), ("out", False)):
                    sel = m & (state == st_val)
                    # per-direction average (the conditioning-matrix
                    # convention): fires grade in THEIR direction, so
                    # the base must be directional too — never init_any
                    bases[(w, st_name)] = (
                        round(50 * float(np.mean(init[1][sel])
                                         + np.mean(init[-1][sel])), 1)
                        if sel.any() else None)
            sig_cells, pooled, age_c, touch_c = {}, {}, {}, {}
            for f, i in fire_idx:
                w = win_of(f["ts"])
                st = "in" if state[i] else "out"
                hit = int(init[int(f["dir"])][i])
                c = sig_cells.setdefault((f["name"], w, st),
                                         {"n": 0, "hits": 0})
                c["n"] += 1
                c["hits"] += hit
                p = pooled.setdefault((w, st), {"n": 0, "hits": 0})
                p["n"] += 1
                p["hits"] += hit
                if st == "in":
                    age = int(bar_sess[i] - z_act[zid[i]])
                    ab = _bin(age, AGE_BINS)
                    a_ = age_c.setdefault((w, ab), {"n": 0, "hits": 0})
                    a_["n"] += 1
                    a_["hits"] += hit
                    tb = _bin(int(vnum[i]), TOUCH_BINS)
                    t_ = touch_c.setdefault((w, tb), {"n": 0, "hits": 0})
                    t_["n"] += 1
                    t_["hits"] += hit
            jcells, jage, jtouch = {}, {}, {}
            for r, i, w in jrows:
                st = "in" if state[i] else "out"
                pts = float(r["points"])
                jcells.setdefault((r["variant"], w, st), []).append(pts)
                if st == "in":
                    age = int(bar_sess[i] - z_act[zid[i]])
                    jage.setdefault((w, _bin(age, AGE_BINS)),
                                    []).append(pts)
                    jtouch.setdefault((w, _bin(int(vnum[i]), TOUCH_BINS)),
                                      []).append(pts)

            def _pct(c):
                return round(100 * c["hits"] / c["n"], 1) if c["n"] else None

            def _cells(d, with_base=True):
                out = {}
                for key, c in sorted(d.items()):
                    w, st = key[-2], key[-1]
                    base = bases.get((w, st))
                    pct = _pct(c)
                    out["|".join(map(str, key))] = {
                        "n": c["n"], "hits": c["hits"], "pct": pct,
                        "zone_base_pct": base if with_base else None,
                        "lift_pp": (round(pct - base, 1)
                                    if pct is not None and base is not None
                                    and with_base else None),
                        "unmeasurable": c["n"] < UNMEASURABLE_N}
                return out

            def _fresh(d, w_base_key):
                out = {}
                for key, c in sorted(d.items()):
                    w = key[0]
                    base = bases.get((w, "in"))
                    pct = _pct(c)
                    out["|".join(key)] = {
                        "n": c["n"], "pct": pct, "zone_base_pct": base,
                        "lift_pp": (round(pct - base, 1)
                                    if pct is not None and base is not None
                                    else None),
                        "unmeasurable": c["n"] < UNMEASURABLE_N}
                return out

            def _jc(d):
                return {"|".join(k): {
                    "n": len(v),
                    "median_pts": round(float(np.median(v)), 2),
                    "net_pts": round(float(np.sum(v)), 1),
                    "unmeasurable": len(v) < UNMEASURABLE_N}
                    for k, v in sorted(d.items())}
            sc = _cells(sig_cells)
            for key in sc:
                sc[key]["location_family"] = key.split("|")[0] \
                    in LOCATION_FAMILY
            ladder[rn] = {
                "reversal_mult": mult, "sig_sessions": sig,
                "zones_total": len(zs), "active_at_once_max": int(peak),
                "in_zone_bar_fraction": round(float(state.mean()), 4),
                "zone_bases_init_pct": {"|".join(k): v
                                        for k, v in bases.items()},
                "pooled": _cells(pooled),
                "freshness_age": _fresh(age_c, "in"),
                "freshness_touch": _fresh(touch_c, "in"),
                "signal_cells": sc, "journal_cells": _jc(jcells),
                "journal_age": _jc(jage), "journal_touch": _jc(jtouch)}
    return {"instrument": instr, "h4_store_bars": int(len(df4)),
            "h4_span": [str(df4["time"].iloc[0]),
                        str(df4["time"].iloc[-1])],
            "swing_k": k, "band_atr_frac": H6_PROX_ATR_FRAC,
            "null_anchor_rung": rung_name(REVERSAL_MULTS[0], None),
            "ladder": ladder}


def _emit(results, head):
    L = ["# H4 Key-Zone Conditioner Census — the strictness ladder "
         "(GENERATED by backtest.zone_census)", "",
         "Terms: [docs/GLOSSARY.md](../../docs/GLOSSARY.md).", "",
         f"Engine `{head[:9]}` — OBSERVATIONAL, pre-registered "
         "(prereg_zone_census + AMENDMENT_zone_census_v2_ladder, "
         "registers 95/96). The operator's instinct — significant "
         "reversals, relatively recent, 'not last year' — gets its "
         "mechanical values FROM THE TABLE: every rung is an existing "
         "convention or the source's own structure (reversal "
         f"multiple in {[f'{m:g}' for m in REVERSAL_MULTS]}xATR(H4) — "
         "the registered multiple and its double; extreme = the "
         f"{[s for s in SIG_SESSIONS if s]}-session high/low when "
         "formed; freshness bins from the same session ladder). v1 "
         "(x1.5, any) is the loosest rung and the NULL ANCHOR. "
         "STATISTIC SHAPE (74-B): per-rung pooled in-zone initiation "
         "vs the ZONE-CONDITIONED base (density-vs-lift curve); "
         "freshness = the same lift by age bin and touch number, "
         "signals pooled per instrument (a zone property, not a "
         "signal claim); per-signal cells per rung in the JSON. "
         f"Cells n<{UNMEASURABLE_N} unmeasurable. Band = the ratified "
         f"retest band ({H6_PROX_ATR_FRAC:g}xATR15). MINT-ON-LIFT "
         "ONLY, front door; no pooling across instruments.", ""]
    for res in results:
        L += [f"## {res['instrument']} — H4 store {res['h4_store_bars']} "
              f"bars ({res['h4_span'][0][:10]} → "
              f"{res['h4_span'][1][:10]})", "",
              "### Density vs lift (the ladder; pooled in-zone "
              "initiation vs zone-conditioned base, per window)", "",
              "| rung | zones | active-at-once | in-zone bars % | "
              "bt in n | bt in % | bt base % | bt lift | fwd in n | "
              "fwd in % | fwd base % | fwd lift |",
              "|---|---|---|---|---|---|---|---|---|---|---|---|"]
        for rn, r in res["ladder"].items():
            def _p(w):
                c = r["pooled"].get(f"{w}|in") or {}
                dim = "°" if c.get("unmeasurable", True) else ""
                lift = c.get("lift_pp")
                return (f"{dim}{c.get('n', 0)} | {c.get('pct', '—')} "
                        f"| {c.get('zone_base_pct', '—')} "
                        f"| {lift:+.1f}pp" if lift is not None else
                        f"{dim}{c.get('n', 0)} | — | — | —")
            L.append(f"| {rn} | {r['zones_total']} "
                     f"| {r['active_at_once_max']} "
                     f"| {100 * r['in_zone_bar_fraction']:.1f} "
                     f"| {_p('backtest')} | {_p('forward')} |")
        anchor = res["null_anchor_rung"]
        strict = list(res["ladder"])[-1]
        for rn in (anchor, strict):
            r = res["ladder"][rn]
            L += ["", f"### Freshness at rung {rn} (in-zone fires; "
                  "signals pooled; lift vs the in-zone base)", "",
                  "| split | window | bin | n | init % | base % | lift |",
                  "|---|---|---|---|---|---|---|"]
            for label, d in (("age (sessions)", r["freshness_age"]),
                             ("touch #", r["freshness_touch"])):
                for key, c in d.items():
                    w, b = key.split("|")
                    dim = "°" if c["unmeasurable"] else ""
                    lift = (f"{c['lift_pp']:+.1f}pp"
                            if c["lift_pp"] is not None else "—")
                    L.append(f"| {label} | {w} | {b} | {dim}{c['n']} "
                             f"| {c['pct']} | {c['zone_base_pct']} "
                             f"| {lift} |")
        L += ["", f"### Location family at the null anchor {anchor} "
              "(measurable cells; all rungs in the JSON)", "",
              "| signal | window | zone | n | init % | base % | lift |",
              "|---|---|---|---|---|---|---|"]
        for key, v in res["ladder"][anchor]["signal_cells"].items():
            if v["unmeasurable"] or not v["location_family"]:
                continue
            name, w, st = key.split("|")
            lift = (f"{v['lift_pp']:+.1f}pp" if v["lift_pp"] is not None
                    else "—")
            L.append(f"| {name} | {w} | {st} | {v['n']} | {v['pct']} "
                     f"| {v['zone_base_pct']} | {lift} |")
        L.append("")
    with open(os.path.join(OUT, "zone_census.md"), "w") as f:
        f.write("\n".join(L))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--instr", nargs="*",
                    default=["uk100fut", "ger40fut", "nas100fut",
                             "us30fut"])
    ap.add_argument("--from-json", action="store_true",
                    help="re-emit the md from the stored JSON (header/"
                         "layout refresh; no replay)")
    a = ap.parse_args()
    os.makedirs(OUT, exist_ok=True)
    head = subprocess.run(["git", "rev-parse", "HEAD"], cwd=ROOT,
                          capture_output=True, text=True).stdout.strip()
    if a.from_json:
        art = json.load(open(os.path.join(OUT, "zone_census.json")))
        for res in art["results"]:
            res["ladder"] = {k.replace("|", "/"): v
                             for k, v in res["ladder"].items()}
            res["null_anchor_rung"] = res["null_anchor_rung"].replace(
                "|", "/")
        with open(os.path.join(OUT, "zone_census.json"), "w") as f:
            json.dump(art, f, indent=2, default=str)
        _emit(art["results"], art["engine_commit"])
        print(f"zone census md re-emitted from JSON -> {OUT}")
        return
    journal = list(csv.DictReader(l for l in open(TRADES_CSV) if not l.startswith("#")))
    results = []
    for instr in a.instr:
        print(f"# zone_census: {instr} ...", file=sys.stderr)
        results.append(run_instrument(instr, journal))
    art = {"STAMP": ("OBSERVATIONAL H4 key-zone conditioner census, "
                     "strictness ladder — the location family's first "
                     "higher-TF member; freshness measured, never "
                     "assumed; mint-on-lift only; never validation"),
           "engine_commit": head,
           "ladder": {"reversal_mults": list(REVERSAL_MULTS),
                      "sig_sessions": list(SIG_SESSIONS),
                      "age_bins": list(AGE_BINS),
                      "touch_bins": list(TOUCH_BINS)},
           "results": results}
    with open(os.path.join(OUT, "zone_census.json"), "w") as f:
        json.dump(art, f, indent=2, default=str)
    _emit(results, head)
    print(f"OBSERVATIONAL zone census (ladder) -> {OUT}/zone_census.md")


if __name__ == "__main__":
    main()
