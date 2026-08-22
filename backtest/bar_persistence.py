"""Bar-persistence census (register 63; pre-registered
prereg_bar_persistence). SCALP-VIABILITY MEASUREMENT, NOT A STRATEGY:
any scalp recipe is a separate counted registration, gated on cells that
clear spread AND baseline and survive forward accrual.

For every registered signal's fires, over the following N in {1,3,5,10}
settled 1M bars (entry = next 1M bar open after fire, the harvest
convention):
  (a) fraction of bars closing favorable (signed by fire direction,
      measured against the entry price);
  (b) reach probabilities at +{2,5,10} points (HOME-REFERENCE ONLY) and
      +{0.25,0.5,1.0} x ATR(15M) (cross-instrument);
  (c) time-to-first-touch distribution (within the 10-bar horizon);
  (d) the same reach probabilities NET of the instrument's measured
      spread — the scalp-economics column: reach counts only past
      entry + spread;
  (e) every cell against its matched baseline ensemble (register 60/61
      matching; B-RANDOM's own bar-persistence is the floor — random
      entries also see favorable bars).

Per signal x instrument x session, both windows; counts everywhere;
dimming and PROVISIONAL stamps standard; sealed/lockbox excluded;
twin-run pinned. Runs weekly under Part C.
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

from engine.signal_watch import AGNOSTIC_ROWS, SignalWatch
from engine.store_loader import is_sealed, lockbox_boundary, zones
from backtest.recipes import _spread_median
from backtest.sessions import session_of
from backtest.scoreboard import (PROVISIONAL_INSTRS, PROVISIONAL_STAMP,
                                 _atr15, _replay, _series,
                                 event_derived_fires, make_cfg)
from backtest.signal_points import (DRIFT_SKEW_SHARE, TREND_FAMILY,
                                    all_signals, baseline_fires)

OUT = os.path.join(ROOT, "reports", "scoreboard")

HORIZONS = (1, 3, 5, 10)               # settled 1M bars after entry
PTS_LADDER = (2.0, 5.0, 10.0)          # HOME-REFERENCE ONLY
ATR_LADDER = (0.25, 0.5, 1.0)          # cross-instrument
SESSIONS = ("asia", "london", "overlap", "ny_only", "dead")


def persistence(fires, ts, o, h, l, c, atr_at, spread, home=False):
    """Per-fire persistence record. Deterministic (twin-run pinned)."""
    n = len(ts)
    rows = []
    for f in sorted(fires, key=lambda x: x["ts"].value):
        i = np.searchsorted(ts, f["ts"].value, side="right") - 1
        ei = i + 1
        if i < 0 or ei >= n:
            continue
        d = f["dir"]
        entry = o[ei]
        a0 = atr_at(pd.Timestamp(ts[i], tz="UTC"))
        if a0 is None:
            continue
        thrs = [(f"atr_{k:g}", k * a0) for k in ATR_LADDER]
        if home:
            thrs += [(f"pts_{p:g}", p) for p in PTS_LADDER]
        hi_n = min(ei + max(HORIZONS), n)
        fav_ext = np.array([(h[j] - entry) if d == 1 else (entry - l[j])
                            for j in range(ei, hi_n)])
        fav_close = np.array([d * (c[j] - entry) > 0
                              for j in range(ei, hi_n)])
        row = {"name": f["name"], "ts": f["ts"],
               "session": session_of(pd.Timestamp(ts[ei], tz="UTC")),
               "fav_frac": {}, "reach": {}, "touch_min": {}}
        for N in HORIZONS:
            w = min(N, len(fav_close))
            if w == 0:
                continue
            row["fav_frac"][N] = float(fav_close[:w].mean())
            for lab, thr in thrs:
                ext = fav_ext[:w]
                row["reach"].setdefault(lab, {})[N] = {
                    "gross": bool((ext >= thr).any()),
                    "net": bool((ext >= thr + spread).any())}
        for lab, thr in thrs:
            idx = np.nonzero(fav_ext >= thr)[0]
            row["touch_min"][lab] = (int(idx[0]) + 1 if len(idx) else None)
        rows.append(row)
    return rows


def _agg(rows):
    """Aggregate a set of per-fire records into one cell."""
    if not rows:
        return None
    out = {"n_fires": len(rows), "fav_frac_pct": {}, "reach_pct": {},
           "touch_min": {}}
    for N in HORIZONS:
        v = [r["fav_frac"][N] for r in rows if N in r["fav_frac"]]
        if v:
            out["fav_frac_pct"][N] = round(100 * float(np.mean(v)), 1)
    labs = sorted({lab for r in rows for lab in r["reach"]})
    for lab in labs:
        for N in HORIZONS:
            sub = [r["reach"][lab][N] for r in rows
                   if lab in r["reach"] and N in r["reach"][lab]]
            if sub:
                out["reach_pct"].setdefault(lab, {})[N] = {
                    "gross": round(100 * float(np.mean(
                        [s["gross"] for s in sub])), 1),
                    "net": round(100 * float(np.mean(
                        [s["net"] for s in sub])), 1),
                    "n": len(sub)}
        touches = [r["touch_min"][lab] for r in rows
                   if r["touch_min"].get(lab) is not None]
        if touches:
            out["touch_min"][lab] = {
                "n_touch": len(touches),
                "median": round(float(np.median(touches)), 1),
                "p90": round(float(np.percentile(touches, 90)), 1)}
    return out


def _ens(cells, lab, N):
    """Ensemble median + range of a net-reach leaf across members."""
    vals = [c["reach_pct"][lab][N]["net"] for c in cells
            if c and c.get("reach_pct", {}).get(lab, {}).get(N)]
    if not vals:
        return None
    return {"members_measured": len(vals),
            "net_median": round(float(np.median(vals)), 1),
            "net_range": [round(float(min(vals)), 1),
                          round(float(max(vals)), 1)]}


def run_instrument(instr):
    cfg = make_cfg({"session_model.extended_hours": True,
                    "session_model.ladder": True,
                    "debug.structure": True})
    watch = SignalWatch()
    engine, bars, _ = _replay(cfg, instr, engine_hook=watch.attach)
    b1m_all = bars[cfg.mtf.execution_tf]
    b1m = [x for x in b1m_all if not x.is_stub]
    ts, cl, hi, lo, _s, _b = _series(b1m_all)
    op = np.array([x.open for x in b1m])
    amap = _atr15(bars[cfg.mtf.signal_tf], cfg.context.atr_period)
    atr_ts = sorted(amap)
    atr_keys = [k.value for k in atr_ts]

    def atr_at(t):
        j = np.searchsorted(atr_keys, t.value, side="right") - 1
        return amap[atr_ts[j]] if j >= 0 else None
    spread = _spread_median(instr)
    fires = watch.fires + event_derived_fires(engine.narrative.events, cfg,
                                              bars, instr=instr)
    fires = [f for f in fires if not is_sealed(f["ts"])]
    home = instr == "uk100fut"
    boundary, gl = lockbox_boundary(), zones()["go_live"]
    windows = (("backtest", lambda r: r["ts"] < boundary),
               ("forward", lambda r: r["ts"] >= gl))
    out = {"instrument": instr, "spread_pts": spread,
           "status": ("provisional" if instr in PROVISIONAL_INSTRS
                      else "canonical"),
           "signals": {}, "baselines": {}, "matched": {}}
    long_share = {}
    for hn, sn, name in all_signals():
        if name in AGNOSTIC_ROWS:
            out["signals"][name] = {"note": "direction-agnostic — "
                                    "persistence is signed (not "
                                    "measurable)"}
            continue
        rows = persistence([f for f in fires if f["name"] == name],
                           ts, op, hi, lo, cl, atr_at, spread, home=home)
        cell = {}
        for win, sel in windows:
            wr = [r for r in rows if sel(r)]
            cell[win] = {"whole": _agg(wr)}
            for s in SESSIONS:
                a = _agg([r for r in wr if r["session"] == s])
                if a:
                    cell[win][s] = a
            if wr:
                long_share[(name, win)] = float(np.mean(
                    [f["dir"] == 1 for f in fires
                     if f["name"] == name]))
        out["signals"][name] = cell
    # baselines through the identical measurement (ensembles); floors
    # computed for EVERY scope the signals report (whole + sessions)
    member_aggs = {}
    labs = ([f"atr_{k:g}" for k in ATR_LADDER]
            + ([f"pts_{p:g}" for p in PTS_LADDER] if home else []))
    for bname, members in baseline_fires(
            type("E", (), {"ts": ts})(), engine.narrative.events).items():
        member_rows = [persistence(mf, ts, op, hi, lo, cl, atr_at,
                                   spread, home=home) for mf in members]
        member_aggs[bname] = {}
        out["baselines"][bname] = {}
        for win, sel in windows:
            wrows = [[r for r in rows if sel(r)] for rows in member_rows]
            scopes = {"whole": [_agg(rs) for rs in wrows]}
            for s in SESSIONS:
                scopes[s] = [_agg([r for r in rs if r["session"] == s])
                             for rs in wrows]
            member_aggs[bname][win] = scopes["whole"]
            out["baselines"][bname][win] = {
                scope: {f"{lab}@{N}": _ens(cells, lab, N)
                        for lab in labs for N in HORIZONS}
                for scope, cells in scopes.items()}
    # matched-floor delta on the headline cell (net reach 0.5xATR @ N=5)
    for name, cell in out["signals"].items():
        if "note" in cell:
            continue
        for win in ("backtest", "forward"):
            whole = cell.get(win, {}).get("whole")
            if not whole:
                continue
            sig = whole.get("reach_pct", {}).get("atr_0.5", {}).get(5)
            if not sig:
                continue
            bname = ("B-TREND" if name in TREND_FAMILY else
                     "B-ALWAYS-LONG"
                     if long_share.get((name, win), 0) >= DRIFT_SKEW_SHARE
                     else "B-RANDOM")
            floor = _ens(member_aggs[bname][win], "atr_0.5", 5)
            if floor:
                out["matched"].setdefault(name, {})[win] = {
                    "name": bname,
                    "delta_net_pp": round(sig["net"]
                                          - floor["net_median"], 1),
                    "floor_net_median": floor["net_median"],
                    "floor_net_range": floor["net_range"]}
    return out


def _fmtcell(a, lab, N):
    r = (a or {}).get("reach_pct", {}).get(lab, {}).get(N)
    if not r:
        return "—"
    dim = "°" if r["n"] < 20 else ""
    return f"{dim}{r['gross']}/{r['net']}"


def _emit(results, head):
    L = ["# Bar-Persistence Census — scalp viability (GENERATED by "
         "backtest.bar_persistence)", "",
         "Terms: [docs/GLOSSARY.md](../../docs/GLOSSARY.md).", "",
         f"Engine `{head[:9]}` — OBSERVATIONAL, pre-registered "
         "(prereg_bar_persistence, register 63). **MEASUREMENT FOR "
         "SCALP-VIABILITY ASSESSMENT, NOT A STRATEGY: any scalp recipe "
         "is a separate counted registration, gated on cells that clear "
         "spread AND baseline and survive forward accrual.** Entry = "
         "next 1M open after fire; horizons N in {1,3,5,10} settled "
         "bars; reach cells print gross/NET-of-spread percentages (the "
         "net column is the scalp economics); the points ladder is "
         "HOME-REFERENCE ONLY, the ATR ladder cross-instrument. Floors: "
         "each signal's headline cell reads against its matched "
         "baseline ensemble median [range] — random entries also see "
         "favorable bars. ° = n<20. Full signal×session×horizon×"
         "threshold grid in the JSON.", ""]
    for res in results:
        inst = res["instrument"]
        home = inst == "uk100fut"
        L += [f"## {inst} ({res['status'].upper()}; spread "
              f"{res['spread_pts']} pts)"]
        if res["status"] == "provisional":
            L += [f"> {PROVISIONAL_STAMP}"]
        L.append("")
        for win in ("backtest", "forward"):
            hdr = ["H", "signal", "n", "fav-close% @1/3/5/10",
                   "reach 0.25×ATR@3 g/n", "reach 0.5×ATR@5 g/n",
                   "reach 1×ATR@10 g/n"]
            if home:
                hdr += ["reach +2pts@3 g/n", "reach +5pts@5 g/n"]
            hdr += ["touch 0.5×ATR med (bars)", "Δnet 0.5×ATR@5 vs "
                    "floor [range]"]
            L += [f"### {inst} / {win} — persistence (whole window)", "",
                  "| " + " | ".join(hdr) + " |",
                  "|" + "---|" * len(hdr)]
            for hn, sn, name in all_signals():
                cell = res["signals"].get(name, {})
                if "note" in cell:
                    row = [f"H{hn}", name, "—", cell["note"]] \
                        + ["—"] * (len(hdr) - 4)
                    L.append("| " + " | ".join(row) + " |")
                    continue
                a = cell.get(win, {}).get("whole")
                if not a:
                    L.append(f"| H{hn} | {name} | 0 | "
                             + " | ".join(["—"] * (len(hdr) - 3)) + " |")
                    continue
                fav = "/".join(
                    str(a["fav_frac_pct"].get(N, "—"))
                    for N in HORIZONS)
                row = [f"H{hn}", name, str(a["n_fires"]), fav,
                       _fmtcell(a, "atr_0.25", 3),
                       _fmtcell(a, "atr_0.5", 5),
                       _fmtcell(a, "atr_1", 10)]
                if home:
                    row += [_fmtcell(a, "pts_2", 3),
                            _fmtcell(a, "pts_5", 5)]
                t = a.get("touch_min", {}).get("atr_0.5")
                row.append(f"{t['median']:g} (n{t['n_touch']})"
                           if t else "—")
                m = res["matched"].get(name, {}).get(win)
                if m:
                    lo, hi = m["floor_net_range"]
                    row.append(f"{m['delta_net_pp']:+.1f}pp vs "
                               f"{m['name']} [{lo}…{hi}]")
                else:
                    row.append("—")
                L.append("| " + " | ".join(row) + " |")
            L.append("")
            # session split on the headline cell
            L += [f"### {inst} / {win} — sessions: net reach 0.5×ATR@5 "
                  "% (n)", "",
                  "| H | signal | " + " | ".join(SESSIONS) + " |",
                  "|---|---|" + "---|" * len(SESSIONS)]
            for hn, sn, name in all_signals():
                cell = res["signals"].get(name, {})
                cells = []
                for s in SESSIONS:
                    a = (cell.get(win, {}) or {}).get(s) \
                        if "note" not in cell else None
                    r = ((a or {}).get("reach_pct", {})
                         .get("atr_0.5", {}).get(5))
                    if not r:
                        cells.append("—")
                    else:
                        dim = "°" if r["n"] < 20 else ""
                        cells.append(f"{dim}{r['net']} (n{r['n']})")
                L.append(f"| H{hn} | {name} | " + " | ".join(cells)
                         + " |")
            L.append("")
        L += [f"### {inst} — BASELINE FLOORS (ensembles; net reach %, "
              "median [range])", "",
              "| baseline | window | 0.25×ATR@3 | 0.5×ATR@5 | 1×ATR@10 |",
              "|---|---|---|---|---|"]
        for bname in ("B-TREND", "B-RANDOM", "B-ALWAYS-LONG"):
            for win in ("backtest", "forward"):
                cells = []
                for key in ("atr_0.25@3", "atr_0.5@5", "atr_1@10"):
                    e = res["baselines"].get(bname, {}).get(win, {}) \
                        .get("whole", {}).get(key)
                    if not e:
                        cells.append("—")
                    else:
                        lo, hi = e["net_range"]
                        rng = "" if lo == hi else f" [{lo}…{hi}]"
                        cells.append(f"{e['net_median']}{rng} "
                                     f"(m{e['members_measured']})")
                L.append(f"| {bname} | {win} | " + " | ".join(cells)
                         + " |")
        L.append("")
    with open(os.path.join(OUT, "bar_persistence.md"), "w") as f:
        f.write("\n".join(L))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--instr", nargs="*",
                    default=["uk100fut", "ger40fut", "nas100fut", "us30fut"])
    a = ap.parse_args()
    os.makedirs(OUT, exist_ok=True)
    head = subprocess.run(["git", "rev-parse", "HEAD"], cwd=ROOT,
                          capture_output=True, text=True).stdout.strip()
    results = []
    for instr in a.instr:
        print(f"# bar_persistence: {instr} ...", file=sys.stderr)
        results.append(run_instrument(instr))
    art = {"STAMP": ("OBSERVATIONAL bar-persistence census — "
                     "scalp-viability measurement, not a strategy; "
                     "never validation"),
           "engine_commit": head,
           "horizons_bars": list(HORIZONS),
           "pts_ladder_home_reference_only": list(PTS_LADDER),
           "atr_ladder": list(ATR_LADDER),
           "results": results}
    with open(os.path.join(OUT, "bar_persistence.json"), "w") as f:
        json.dump(art, f, indent=2, default=str)
    _emit(results, head)
    print(f"OBSERVATIONAL persistence -> {OUT}/bar_persistence.md")


if __name__ == "__main__":
    main()
