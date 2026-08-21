"""Conditioning-matrix census (register 52; pre-registered
prereg_conditioning_matrix). OBSERVATIONAL. Confirmation testing done
STATE-CONDITIONED per the co-fire lesson: every live signal's fires split
by standing context-state dimensions; full fire counts preserved (never
time-coincidence).

Dimensions per fire bar: H11 position (node/gap/neither) · coil-state
preceding (FLAGGED proxy: trailing 30-bar 1M range-sum <= p20 of its
trailing-day distribution; parameters implementer-proposed pending
ratification — organ #3 is the eventual instrument) · H13 value-area
geometry (inside/edge/outside; edge = within one bucket of a band edge) ·
1M phase (trending/ranging) · session.

GRADING (mandatory, per register 47 + the VWAP re-cut): hits are
EPISODE-BEGINS-AFTER-FIRE; each cell's lift reads against its OWN
state-conditioned base (the episode-hit rate of ALL bars in that state).
Single-digit cells UNMEASURABLE. Any surviving lift -> composite proposal
via the front door; nothing auto-minted.
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

from engine.signal_watch import (AGNOSTIC_ROWS, H11_BUCKET_PTS,
                                 H13_VALUE_AREA_PCT, SignalWatch)
from engine.store_loader import is_sealed, lockbox_boundary, zones
from backtest.location_census import _Profile
from backtest.sessions import sessions_of_index
from backtest.scoreboard import (PROVISIONAL_INSTRS, PROVISIONAL_STAMP,
                                 _payoff, _replay, build_moves,
                                 event_derived_fires, make_cfg)

OUT = os.path.join(ROOT, "reports", "scoreboard")

COIL_WINDOW = 30      # flagged implementer proposal (prereg)
COIL_PCTILE = 0.20    # flagged implementer proposal (prereg)


class _VATracker:
    """H13 value-area geometry per bar: inside/edge/outside (trailing
    profile, ratified config; edge = within one bucket of a band edge)."""

    def __init__(self):
        self._p = _Profile()
        self._agg_order = self._p._order
        self._va = None

    def feed(self, bar):
        prof = self._p
        prev_sid = prof._sid
        prof.feed(bar)
        if prof._sid != prev_sid and prev_sid is not None:
            agg = {}
            for sid in prof._order[-5:]:
                for b, v in prof._profiles.get(sid, {}).items():
                    agg[b] = agg.get(b, 0) + v
            if len(agg) >= 10:
                total = sum(agg.values())
                poc = max(agg, key=agg.get)
                lo = hi = poc
                vol = agg[poc]
                while vol < H13_VALUE_AREA_PCT * total:
                    up, dn = hi + H11_BUCKET_PTS, lo - H11_BUCKET_PTS
                    uv, dv = agg.get(up, 0.0), agg.get(dn, 0.0)
                    if uv <= 0 and dv <= 0:
                        break
                    if uv >= dv:
                        hi, vol = up, vol + uv
                    else:
                        lo, vol = dn, vol + dv
                self._va = (lo - H11_BUCKET_PTS / 2, hi + H11_BUCKET_PTS / 2)
            else:
                self._va = None
        if self._va is None:
            return None
        val, vah = self._va
        c = bar.close
        if val <= c <= vah:
            return ("edge" if (c - val <= H11_BUCKET_PTS
                               or vah - c <= H11_BUCKET_PTS) else "inside")
        return "outside"


def run_instrument(instr):
    cfg = make_cfg({"session_model.extended_hours": True,
                    "session_model.ladder": True,
                    "debug.structure": True})
    watch = SignalWatch()
    engine, bars, _ = _replay(cfg, instr, engine_hook=watch.attach)
    qual, eps, series, _d = build_moves(
        bars[cfg.mtf.execution_tf], bars[cfg.mtf.signal_tf],
        cfg.context.atr_period)
    ts, cl, _segs = series
    b1m = [x for x in bars[cfg.mtf.execution_tf] if not x.is_stub]
    n = len(b1m)
    # episode-start-forward hit per bar
    ep_starts = np.array(sorted(e["start"].value for e in eps))

    def ep_hit(t_ns):
        j = np.searchsorted(ep_starts, t_ns, side="left")
        return bool(j < len(ep_starts)
                    and ep_starts[j] <= t_ns + 3_600_000_000_000)
    hits_all = np.array([ep_hit(t) for t in ts])
    # state arrays per bar
    prof, vat = _Profile(), _VATracker()
    h11 = np.array([prof.feed(x) or "unclassified" for x in b1m],
                   dtype=object)
    va = np.array([vat.feed(x) or "unclassified" for x in b1m],
                  dtype=object)
    rng = np.array([x.high - x.low for x in b1m])
    rsum = pd.Series(rng).rolling(COIL_WINDOW).sum()
    thr = rsum.rolling(480, min_periods=100).quantile(COIL_PCTILE).shift(1)
    coil = np.where((rsum <= thr).fillna(False).to_numpy(), "coil",
                    "no-coil")
    trend_map = {}
    prev = 0
    for e in engine.narrative.events:
        if e["type"] == "PHASE_EVAL" and e.get("tf") == "1min":
            trend_map[pd.Timestamp(e["ts"]).value] = e.get("trend", 0)
    phase = np.array(["trending" if trend_map.get(t, 0) != 0 else "ranging"
                      for t in ts], dtype=object)
    sess = sessions_of_index(pd.DatetimeIndex(ts, tz="UTC"))
    DIMS = {"h11": h11, "coil": coil, "va": va, "phase": phase,
            "session": sess}
    fires = watch.fires + event_derived_fires(engine.narrative.events, cfg,
                                              bars)
    fires = [f for f in fires
             if f["name"] not in AGNOSTIC_ROWS and not is_sealed(f["ts"])]
    boundary, gl = lockbox_boundary(), zones()["go_live"]
    win = pd.Timedelta(minutes=60)
    out = {"instrument": instr,
           "status": ("provisional" if instr in PROVISIONAL_INSTRS
                      else "canonical"),
           "coil_proxy_flag": ("trailing 30-bar range-sum <= p20 of "
                               "trailing day — implementer-proposed, "
                               "ratification pending"),
           "cells": {}}
    for w_lo, w_hi, w in ((pd.Timestamp.min.tz_localize("UTC"), boundary,
                           "backtest"),
                          (gl, pd.Timestamp.max.tz_localize("UTC"),
                           "forward")):
        wmask = (ts >= w_lo.value) & (ts < w_hi.value)
        # state-conditioned bases per dimension value
        bases = {}
        for dim, arr in DIMS.items():
            for val in np.unique(arr[wmask]):
                m = wmask & (arr == val)
                bases[(dim, val)] = (round(100 * float(hits_all[m].mean()),
                                           1) if m.any() else None)
        for f in fires:
            if not (w_lo <= f["ts"] < w_hi):
                continue
            i = np.searchsorted(ts, f["ts"].value, side="right") - 1
            if i < 0:
                continue
            h = ep_hit(ts[i])
            for dim, arr in DIMS.items():
                val = arr[i]
                key = (f["name"], w, dim, str(val))
                c = out["cells"].setdefault("|".join(key), {
                    "n": 0, "hits": 0, "fires": [],
                    "state_base_pct": bases.get((dim, val))})
                c["n"] += 1
                c["hits"] += int(h)
                c["fires"].append(f)
    # finalize: precision, lift, payoff
    final = {}
    for key, c in out["cells"].items():
        pay = _payoff(c["fires"], ts, cl, win)
        pct = round(100 * c["hits"] / c["n"], 1) if c["n"] else None
        final[key] = {
            "n": c["n"], "hits": c["hits"], "pct": pct,
            "state_base_pct": c["state_base_pct"],
            "lift_pp": (round(pct - c["state_base_pct"], 1)
                        if pct is not None
                        and c["state_base_pct"] is not None else None),
            "unmeasurable": c["n"] < 10,
            "payoff_net": pay["net_pts"] if pay else None,
            "payoff_median": pay["median_per_fire"] if pay else None}
    out["cells"] = final
    return out


def _emit(results, head):
    L = ["# Conditioning-Matrix Census (GENERATED)", "",
         f"Engine `{head[:9]}` — OBSERVATIONAL, pre-registered "
         "(prereg_conditioning_matrix). STATE-conditioned confirmation "
         "testing: hits are EPISODE-BEGINS-AFTER-FIRE; every cell's lift "
         "reads against its OWN state-conditioned base. Coil dimension is "
         "a FLAGGED proxy pending ratification. Cells n<10 UNMEASURABLE "
         "(omitted here; full grid in the JSON). Surviving lift -> "
         "composite proposal via front door only.", ""]
    for res in results:
        inst = res["instrument"]
        L += [f"## {inst} ({res['status'].upper()})"]
        if res["status"] == "provisional":
            L += [f"> {PROVISIONAL_STAMP}"]
        L += ["", "| signal | window | dim | state | n | precision "
              "| state base | lift | payoff net/med |",
              "|---|---|---|---|---|---|---|---|---|"]
        rows = [(k.split("|"), v) for k, v in res["cells"].items()
                if not v["unmeasurable"] and v["lift_pp"] is not None]
        rows.sort(key=lambda r: -abs(r[1]["lift_pp"]))
        for (name, w, dim, val), v in rows[:60]:
            L.append(f"| {name} | {w} | {dim} | {val} | {v['n']} "
                     f"| {v['pct']}% | {v['state_base_pct']}% "
                     f"| {v['lift_pp']:+.1f}pp "
                     f"| {v['payoff_net']}/{v['payoff_median']} |")
        if len(rows) > 60:
            L.append(f"| … | | | | | | | ({len(rows) - 60} more "
                     f"measurable cells in the JSON) | |")
        L.append("")
    with open(os.path.join(OUT, "conditioning_matrix.md"), "w") as f:
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
        print(f"# conditioning_matrix: {instr} ...", file=sys.stderr)
        res = run_instrument(instr)
        for c in res["cells"].values():
            c.pop("fires", None)
        results.append(res)
    art = {"STAMP": ("OBSERVATIONAL conditioning matrix — pre-registered; "
                     "state-conditioned; never validation"),
           "engine_commit": head, "results": results}
    with open(os.path.join(OUT, "conditioning_matrix.json"), "w") as f:
        json.dump(art, f, indent=2, default=str)
    _emit(results, head)
    print(f"OBSERVATIONAL matrix -> {OUT}/conditioning_matrix.md")


if __name__ == "__main__":
    main()
