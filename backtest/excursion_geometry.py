"""Excursion-geometry extension (register 52; pre-registered
prereg_excursion_geometry). MEASUREMENT ONLY — both halves are
RECIPE-DESIGN INPUTS, not strategies.

(a) Adverse side: per fire, MAE at 60 min, 120 min, and to-EOD (native
    calendars); median/p90/p95 per signal x instrument x session — the
    stop-width design input for the v1 recipe-values discussion.
(b) Favorable side (the TP ladder): per fire, P(reach +k x ATR(15M)
    before -6 x ATR(15M) or EOD-flat) for k in {0.5, 1.0, 1.5, 2.0} —
    the target-reach curve. EOD and -6 both count as not-reached.
    A point-denominated ladder (5/10/15/20) is reported for uk100 ONLY,
    labeled NON-COMPARABLE across instruments.

WARNINGS carried in the artifact header: the high-win-rate shapes the TP
ladder produces are TAIL-RISK PURCHASES — each -6xATR loss ~= 12-24 small
wins; spread ~= a quarter of a 0.5xATR win at home. Honest-fill rules and
EOD-flat apply; twin-run determinism pinned; sealed/lockbox excluded.
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
from backtest.recipes import _eod_flags
from backtest.sessions import session_of
from backtest.scoreboard import (PROVISIONAL_INSTRS, PROVISIONAL_STAMP,
                                 _atr15, _replay, _series,
                                 event_derived_fires, make_cfg)

OUT = os.path.join(ROOT, "reports", "scoreboard")

TP_LADDER_ATR = (0.5, 1.0, 1.5, 2.0)
UNSTOPPED_ATR = 6.0
PTS_LADDER_HOME = (5.0, 10.0, 15.0, 20.0)


def _pcts(a):
    if not a:
        return None
    a = np.array(a, float)
    return {"n": len(a), "median": round(float(np.median(a)), 2),
            "p90": round(float(np.percentile(a, 90)), 2),
            "p95": round(float(np.percentile(a, 95)), 2)}


def geometry(fires, ts, o, h, l, c, atr_at, eod, home=False):
    """Per-fire MAE windows + TP-ladder race. Deterministic."""
    rows = []
    n = len(ts)
    for f in sorted(fires, key=lambda x: x["ts"].value):
        i = np.searchsorted(ts, f["ts"].value, side="right") - 1
        if i < 0 or i + 1 >= n:
            continue
        d = f["dir"]
        ref = c[i]
        a0 = atr_at(pd.Timestamp(ts[i], tz="UTC"))
        if a0 is None:
            continue
        # find EOD index (first flagged bar at/after i+1)
        j_eod = i + 1
        while j_eod < n - 1 and not eod[j_eod]:
            j_eod += 1
        def mae_to(j_hi):
            sl = slice(i + 1, min(j_hi, n))
            if sl.start >= sl.stop:
                return 0.0
            return float(max(0.0, (ref - l[sl].min()) if d == 1
                             else (h[sl].max() - ref)))
        j60 = np.searchsorted(ts, ts[i] + 3_600_000_000_000, side="right")
        j120 = np.searchsorted(ts, ts[i] + 7_200_000_000_000, side="right")
        row = {"name": f["name"], "ts": f["ts"],
               "session": session_of(f["ts"]),
               "atr": a0,
               "mae60": mae_to(j60), "mae120": mae_to(j120),
               "mae_eod": mae_to(j_eod + 1)}
        # TP ladder race: +k*ATR vs -6*ATR vs EOD (settled-bar walk)
        stop_px = ref - d * UNSTOPPED_ATR * a0
        ladders = ([(f"atr_{k}", ref + d * k * a0) for k in TP_LADDER_ATR]
                   + ([(f"pts_{p:g}", ref + d * p)
                       for p in PTS_LADDER_HOME] if home else []))
        reached = {}
        for name_, tgt in ladders:
            hit = False
            for j in range(i + 1, min(j_eod + 1, n)):
                stop_hit = (l[j] <= stop_px if d == 1 else h[j] >= stop_px)
                tgt_hit = (h[j] >= tgt if d == 1 else l[j] <= tgt)
                if stop_hit:            # rule 1: stop wins ties
                    break
                if tgt_hit:
                    hit = True
                    break
            reached[name_] = hit
        row["reached"] = reached
        rows.append(row)
    return rows


def run_instrument(instr):
    cfg = make_cfg({"session_model.extended_hours": True,
                    "session_model.ladder": True})
    watch = SignalWatch()
    engine, bars, _ = _replay(cfg, instr, engine_hook=watch.attach)
    b1m = [x for x in bars[cfg.mtf.execution_tf] if not x.is_stub]
    ts, cl, hi, lo, _s, _b = _series(bars[cfg.mtf.execution_tf])
    op = np.array([x.open for x in b1m])
    amap = _atr15(bars[cfg.mtf.signal_tf], cfg.context.atr_period)
    atr_ts = sorted(amap)

    def atr_at(t):
        i = np.searchsorted([k.value for k in atr_ts], t.value,
                            side="right") - 1
        return amap[atr_ts[i]] if i >= 0 else None
    eod = _eod_flags(b1m, instr)
    fires = watch.fires + event_derived_fires(engine.narrative.events, cfg,
                                              bars)
    fires = [f for f in fires
             if f["name"] not in AGNOSTIC_ROWS and not is_sealed(f["ts"])]
    home = instr == "uk100fut"
    rows = geometry(fires, ts, op, hi, lo, cl, atr_at, eod, home=home)
    boundary, gl = lockbox_boundary(), zones()["go_live"]
    out = {"instrument": instr,
           "status": ("provisional" if instr in PROVISIONAL_INSTRS
                      else "canonical"),
           "adverse": {}, "tp_ladder": {}}
    for w, sel in (("backtest", lambda r: r["ts"] < boundary),
                   ("forward", lambda r: r["ts"] >= gl)):
        ws = [r for r in rows if sel(r)]
        for name in sorted({r["name"] for r in ws}):
            sub = [r for r in ws if r["name"] == name]
            adv = {"whole": {k: _pcts([r[k] / r["atr"] for r in sub])
                             for k in ("mae60", "mae120", "mae_eod")}}
            for s in sorted({r["session"] for r in sub}):
                ss = [r for r in sub if r["session"] == s]
                adv[s] = {k: _pcts([r[k] / r["atr"] for r in ss])
                          for k in ("mae60", "mae120", "mae_eod")}
            out["adverse"].setdefault(w, {})[name] = adv
            keys = sub[0]["reached"].keys() if sub else []
            out["tp_ladder"].setdefault(w, {})[name] = {
                k: {"n": len(sub),
                    "reach_pct": round(100 * float(np.mean(
                        [r["reached"][k] for r in sub])), 1)}
                for k in keys}
    return out


def _emit(results, head):
    L = ["# Excursion Geometry — stop-width + target-reach "
         "(GENERATED)", "",
         f"Engine `{head[:9]}` — OBSERVATIONAL, pre-registered "
         "(prereg_excursion_geometry). BOTH HALVES ARE RECIPE-DESIGN "
         "INPUTS, NOT STRATEGIES. MAE in ATR(15M) units. **WARNING: the "
         "high-win-rate shapes the TP ladder produces are tail-risk "
         "purchases — each -6xATR loss ≈ 12-24 small wins; spread ≈ a "
         "quarter of a 0.5xATR win at home. The points ladder is uk100 "
         "HOME-SCALE ONLY, non-comparable across instruments.**", ""]
    for res in results:
        inst = res["instrument"]
        L += [f"## {inst} ({res['status'].upper()})"]
        if res["status"] == "provisional":
            L += [f"> {PROVISIONAL_STAMP}"]
        for w in ("backtest", "forward"):
            adv = res["adverse"].get(w, {})
            if adv:
                L += ["", f"### {inst} / {w} — MAE (xATR): "
                      f"median | p90 | p95 (whole-window)",
                      "", "| signal | n | 60min | 120min | to-EOD |",
                      "|---|---|---|---|---|"]
                for name, per in sorted(adv.items()):
                    p = per["whole"]
                    if not p["mae60"]:
                        continue
                    def fmt(d):
                        return (f"{d['median']} · {d['p90']} · {d['p95']}"
                                if d else "—")
                    L.append(f"| {name} | {p['mae60']['n']} "
                             f"| {fmt(p['mae60'])} | {fmt(p['mae120'])} "
                             f"| {fmt(p['mae_eod'])} |")
            lad = res["tp_ladder"].get(w, {})
            if lad:
                keys = sorted({k for per in lad.values() for k in per})
                L += ["", f"### {inst} / {w} — TP ladder "
                      f"(reach % before -6xATR/EOD)",
                      "", "| signal | n | " + " | ".join(keys) + " |",
                      "|---|---|" + "---|" * len(keys)]
                for name, per in sorted(lad.items()):
                    n0 = next(iter(per.values()))["n"] if per else 0
                    cells = [f"{per[k]['reach_pct']}%" if k in per else "—"
                             for k in keys]
                    L.append(f"| {name} | {n0} | " + " | ".join(cells)
                             + " |")
        L.append("")
    with open(os.path.join(OUT, "excursion_geometry.md"), "w") as f:
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
        print(f"# excursion_geometry: {instr} ...", file=sys.stderr)
        results.append(run_instrument(instr))
    art = {"STAMP": ("OBSERVATIONAL excursion geometry — recipe-design "
                     "inputs, not strategies; never validation"),
           "engine_commit": head, "results": results}
    with open(os.path.join(OUT, "excursion_geometry.json"), "w") as f:
        json.dump(art, f, indent=2, default=str)
    _emit(results, head)
    print(f"OBSERVATIONAL geometry -> {OUT}/excursion_geometry.md")


if __name__ == "__main__":
    main()
