"""VWAP census (register 51; pre-registered prereg_vwap_census; NO
hypothesis minted). Session-anchored VWAP + sigma-bands from futures
volume, native cash sessions.

(a) Conditioner cut: every live signal's fires split by VWAP-relative
    position — band (|z|<=0.5 "at" / (0.5,1.5] "1s" / (1.5,2.5] "2s" /
    >2.5 "beyond") x SIGNED vs fire direction (away = fire points away
    from VWAP, toward = fire points back at it): precision + payoff per
    cell, counts everywhere.
(b) Direct: forward qualifying rate after +/-2-sigma touches vs the
    context's base rate; VWAP-touch reaction split by 1M trending/ranging.

Mechanism note: institutional execution benchmarking — VWAP algorithms
are the H12 order-slicing behavior industrialized; practitioner win-rate
claims explicitly NOT carried. Any lift -> hypothesis via front door.
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
from backtest.scoreboard import (PROVISIONAL_INSTRS, PROVISIONAL_STAMP,
                                 _payoff, _replay, build_moves,
                                 event_derived_fires, make_cfg)

OUT = os.path.join(ROOT, "reports", "scoreboard")

BANDS = (("at", 0.0, 0.5), ("1s", 0.5, 1.5), ("2s", 1.5, 2.5),
         ("beyond", 2.5, float("inf")))


def _vwap_frame(instr):
    """Per-minute session-anchored VWAP, sigma, z — native cash sessions."""
    import store as store_mod
    df = pd.read_csv(os.path.join(ROOT, "clean_finsa", f"{instr}_1min.csv"),
                     parse_dates=["time"]).set_index("time")
    tz = store_mod.SESSION_TZ.get(instr, "Europe/London")
    cash = df[df["in_cash"]].copy()
    cash["sess"] = pd.DatetimeIndex(cash.index).tz_convert(tz).date
    tp = (cash["high"] + cash["low"] + cash["close"]) / 3
    v = cash["volume"].clip(lower=0)
    g = cash.groupby("sess")
    cum_pv = (tp * v).groupby(cash["sess"]).cumsum()
    cum_v = v.groupby(cash["sess"]).cumsum().replace(0, np.nan)
    vwap = cum_pv / cum_v
    cum_p2v = (tp * tp * v).groupby(cash["sess"]).cumsum()
    var = (cum_p2v / cum_v - vwap * vwap).clip(lower=0)
    sigma = np.sqrt(var).replace(0, np.nan)
    z = (cash["close"] - vwap) / sigma
    return pd.DataFrame({"vwap": vwap, "sigma": sigma, "z": z,
                         "high": cash["high"], "low": cash["low"]})


def _band(z):
    az = abs(z)
    for name, lo, hi in BANDS:
        if lo <= az <= hi or (lo < az <= hi):
            return name
    return "beyond"


def run_instrument(instr):
    cfg = make_cfg({"session_model.extended_hours": True,
                    "session_model.ladder": True,
                    "debug.structure": True})       # 1M phase for (b)
    watch = SignalWatch()
    engine, bars, _ = _replay(cfg, instr, engine_hook=watch.attach)
    qual, _eps, series, _d = build_moves(
        bars[cfg.mtf.execution_tf], bars[cfg.mtf.signal_tf],
        cfg.context.atr_period)
    ts, cl, _segs = series
    vf = _vwap_frame(instr)
    # close-stamped bar ts -> vwap row is open-stamped store time + 1min
    vmap = {(t + pd.Timedelta(minutes=1)).value: (r.vwap, r.sigma, r.z)
            for t, r in vf.iterrows() if r.sigma == r.sigma}
    fires = watch.fires + event_derived_fires(engine.narrative.events, cfg,
                                              bars)
    fires = [f for f in fires
             if f["name"] not in AGNOSTIC_ROWS and not is_sealed(f["ts"])]
    boundary, gl = lockbox_boundary(), zones()["go_live"]
    win = pd.Timedelta(minutes=60)

    def wname(t):
        return ("backtest" if t < boundary else
                "forward" if t >= gl else None)

    # (a) conditioner cut
    cells = {}
    for f in fires:
        rec = vmap.get(f["ts"].value)
        w = wname(f["ts"])
        if rec is None or w is None:
            continue
        _vw, _sg, z = rec
        band = _band(z)
        signed = "away" if z * f["dir"] > 0 else "toward"
        cells.setdefault(f["name"], {}).setdefault(w, {}).setdefault(
            f"{band}/{signed}", []).append(f)
    cut = {}
    for name, per_w in cells.items():
        for w, per_c in per_w.items():
            for cell, fs in per_c.items():
                hits = tot = 0
                for f in fs:
                    i = np.searchsorted(ts, f["ts"].value, side="right") - 1
                    if i < 0:
                        continue
                    tot += 1
                    hits += bool(qual[f["dir"]][i])
                pay = _payoff(fs, ts, cl, win)
                cut.setdefault(name, {}).setdefault(w, {})[cell] = {
                    "n": tot, "hits": hits,
                    "pct": round(100 * hits / tot, 1) if tot else None,
                    "unmeasurable": tot < 10,
                    "payoff_net": pay["net_pts"] if pay else None,
                    "payoff_median": (pay["median_per_fire"]
                                      if pay else None)}

    # (b) direct: 2-sigma touches + vwap touches by phase
    phase_trend = {}
    prev = 0
    for e in engine.narrative.events:
        if e["type"] == "PHASE_EVAL" and e.get("tf") == "1min":
            phase_trend[pd.Timestamp(e["ts"]).value] = e.get("trend", 0)
    direct = {}
    either = {1: qual[1], -1: qual[-1]}
    for w_lo, w_hi, w in ((pd.Timestamp.min.tz_localize("UTC"), boundary,
                           "backtest"),
                          (gl, pd.Timestamp.max.tz_localize("UTC"),
                           "forward")):
        msk = (ts >= w_lo.value) & (ts < w_hi.value)
        base = (round(100 * float(np.mean(qual[1][msk] | qual[-1][msk])), 1)
                if msk.any() else None)
        ev = {"touch_2s": [], "touch_vwap_trending": [],
              "touch_vwap_ranging": []}
        for t_open, r in vf.iterrows():
            t = (t_open + pd.Timedelta(minutes=1)).value
            if not (w_lo.value <= t < w_hi.value) or r.sigma != r.sigma:
                continue
            i = np.searchsorted(ts, t, side="right") - 1
            if i < 0 or is_sealed(pd.Timestamp(t, tz="UTC")):
                continue
            hit = bool(qual[1][i] or qual[-1][i])
            if (r.high >= r.vwap + 2 * r.sigma
                    or r.low <= r.vwap - 2 * r.sigma):
                ev["touch_2s"].append(hit)
            if r.low <= r.vwap <= r.high:
                tr = phase_trend.get(t, 0)
                key = ("touch_vwap_trending" if tr != 0
                       else "touch_vwap_ranging")
                ev[key].append(hit)
        direct[w] = {"either_dir_base_pct": base}
        for k, v in ev.items():
            direct[w][k] = {"n": len(v),
                            "qualifying_pct": (round(100 * float(
                                np.mean(v)), 1) if v else None)}
    return {"instrument": instr,
            "status": ("provisional" if instr in PROVISIONAL_INSTRS
                       else "canonical"),
            "conditioner_cut": cut, "direct": direct}


def _emit(results, head):
    L = ["# VWAP Census (GENERATED by backtest.vwap_census)", "",
         f"Engine `{head[:9]}` — OBSERVATIONAL, pre-registered "
         "(prereg_vwap_census); NO hypothesis minted. Session-anchored "
         "VWAP + sigma-bands from futures volume, native cash sessions. "
         "Mechanism note: institutional execution benchmarking — VWAP "
         "algorithms are the H12 order-slicing behavior industrialized; "
         "practitioner win-rate claims NOT carried. Cells: band x signed "
         "(away/toward VWAP vs fire direction); n<10 UNMEASURABLE.", ""]
    for res in results:
        inst = res["instrument"]
        L += [f"## {inst} ({res['status'].upper()})"]
        if res["status"] == "provisional":
            L += [f"> {PROVISIONAL_STAMP}"]
        L += ["", "### direct measurements", "",
              "| window | event | n | qualifying% | either-dir base |",
              "|---|---|---|---|---|"]
        for w, d in res["direct"].items():
            for k in ("touch_2s", "touch_vwap_trending",
                      "touch_vwap_ranging"):
                v = d[k]
                L.append(f"| {w} | {k} | {v['n']} | {v['qualifying_pct']}% "
                         f"| {d['either_dir_base_pct']}% |")
        L += ["", "### conditioner cut (measurable cells only; full grid "
              "in the JSON)", "",
              "| signal | window | cell | n | precision | payoff net/med |",
              "|---|---|---|---|---|---|"]
        for name, per_w in sorted(res["conditioner_cut"].items()):
            for w, per_c in per_w.items():
                for cell, v in sorted(per_c.items()):
                    if v["unmeasurable"]:
                        continue
                    L.append(f"| {name} | {w} | {cell} | {v['n']} "
                             f"| {v['pct']}% ({v['hits']}/{v['n']}) "
                             f"| {v['payoff_net']}/{v['payoff_median']} |")
        L.append("")
    with open(os.path.join(OUT, "vwap_census.md"), "w") as f:
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
        print(f"# vwap_census: {instr} ...", file=sys.stderr)
        results.append(run_instrument(instr))
    art = {"STAMP": ("OBSERVATIONAL VWAP census — pre-registered; no "
                     "hypothesis minted; never validation"),
           "engine_commit": head, "results": results}
    with open(os.path.join(OUT, "vwap_census.json"), "w") as f:
        json.dump(art, f, indent=2, default=str)
    _emit(results, head)
    print(f"OBSERVATIONAL VWAP census -> {OUT}/vwap_census.md")


if __name__ == "__main__":
    main()
