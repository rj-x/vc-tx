"""Location-conditioned confirmation census (register 48; pre-registered
prereg_location_conditioned_census BEFORE computation). OBSERVATIONAL.

THE QUESTION (operator's seller-exhaustion-at-high-volume question, shaped
to avoid co-fire starvation): does exhaustion-family precision differ by
volume-at-price location? Split (not intersect) each exhaustion-family
fire by the H11-map class of its bar: node (>=p90 of the trailing
profile) / gap (<=p10) / neither. Full fire counts preserved. Any lift ->
composite candidate through the front door (operator yes/no), never
auto-minted.
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

from engine.signal_watch import (EXHAUSTION_FAMILY, H11_BUCKET_PTS,
                                 H11_LOOKBACK_SESS, SignalWatch)
from engine.store_loader import is_sealed, lockbox_boundary, zones
from backtest.scoreboard import (PROVISIONAL_INSTRS, PROVISIONAL_STAMP,
                                 _replay, _payoff, build_moves,
                                 event_derived_fires, make_cfg)

OUT = os.path.join(ROOT, "reports", "scoreboard")


class _Profile:
    """Trailing H11-map per the ratified parameters; classify a bar's
    bucket as node/gap/neither. Trailing sessions only — no lookahead."""

    def __init__(self):
        self._profiles, self._order = {}, []
        self._node = self._gap = None
        self._sid = None

    def _rebuild(self):
        agg = {}
        for sid in self._order[-H11_LOOKBACK_SESS:]:
            for b, v in self._profiles.get(sid, {}).items():
                agg[b] = agg.get(b, 0) + v
        if len(agg) < 10:
            self._node = self._gap = None
            return
        vols = sorted(agg.values())
        self._gap = {b for b, v in agg.items()
                     if v <= vols[int(0.1 * (len(vols) - 1))]}
        self._node = {b for b, v in agg.items()
                      if v >= vols[int(0.9 * (len(vols) - 1))]}

    def feed(self, bar):
        b = round(bar.close / H11_BUCKET_PTS) * H11_BUCKET_PTS
        if self._sid != bar.session_id:
            if self._sid is not None:
                self._order.append(self._sid)
                self._rebuild()
            self._sid = bar.session_id
            self._profiles[bar.session_id] = {}
        p = self._profiles[bar.session_id]
        p[b] = p.get(b, 0) + bar.volume
        if self._node is None:
            return None
        return ("node" if b in self._node
                else "gap" if b in self._gap else "neither")


def run_instrument(instr):
    cfg = make_cfg({"session_model.extended_hours": True,
                    "session_model.ladder": True})
    watch = SignalWatch()
    engine, bars, _ = _replay(cfg, instr, engine_hook=watch.attach)
    qual, _eps, series, _d = build_moves(
        bars[cfg.mtf.execution_tf], bars[cfg.mtf.signal_tf],
        cfg.context.atr_period)
    ts, cl, _segs = series
    # location class per 1M bar (trailing profile; no lookahead)
    prof = _Profile()
    b1m = [x for x in bars[cfg.mtf.execution_tf] if not x.is_stub]
    loc = {}
    for x in b1m:
        loc[x.ts.value] = prof.feed(x)
    fires = [f for f in watch.fires
             if f["name"] in EXHAUSTION_FAMILY and not is_sealed(f["ts"])]
    boundary, gl = lockbox_boundary(), zones()["go_live"]
    win = pd.Timedelta(minutes=60)
    out = {"instrument": instr,
           "status": ("provisional" if instr in PROVISIONAL_INSTRS
                      else "canonical"),
           "cells": {}}
    for name in EXHAUSTION_FAMILY:
        nf = [f for f in fires if f["name"] == name]
        for wname, sel in (("backtest", lambda f: f["ts"] < boundary),
                           ("forward", lambda f: f["ts"] >= gl)):
            sub = [f for f in nf if sel(f)]
            for cls in ("node", "gap", "neither", "unclassified"):
                cf = [f for f in sub
                      if (loc.get(f["ts"].value) or "unclassified") == cls]
                if not cf:
                    continue
                hits = tot = 0
                for f in cf:
                    i = np.searchsorted(ts, f["ts"].value, side="right") - 1
                    if i < 0:
                        continue
                    tot += 1
                    hits += bool(qual[f["dir"]][i])
                pay = _payoff(cf, ts, cl, win)
                out["cells"].setdefault(name, {}).setdefault(
                    wname, {})[cls] = {
                    "n": tot, "hits": hits,
                    "pct": round(100 * hits / tot, 1) if tot else None,
                    "unmeasurable": tot < 10,
                    "payoff_net": pay["net_pts"] if pay else None,
                    "payoff_median": pay["median_per_fire"] if pay else None}
    return out


def _emit(results, head):
    L = ["# Location-Conditioned Confirmation Census (GENERATED)", "",
         "Terms: [docs/GLOSSARY.md](../../docs/GLOSSARY.md).", "",
         f"Engine `{head[:9]}` — OBSERVATIONAL, pre-registered "
         "(prereg_location_conditioned_census). Exhaustion-family fires "
         "split by H11-map class at the fire bar (node/gap/neither; "
         "trailing profile, ratified parameters, home-derived bucket — "
         "MIS-SCALE caveat off-home). Full fire counts preserved (a "
         "split, not an intersection). n<10 UNMEASURABLE. Any lift -> "
         "composite candidate via operator yes/no, never auto-minted.",
         ""]
    for res in results:
        inst = res["instrument"]
        L += [f"## {inst} ({res['status'].upper()})"]
        if res["status"] == "provisional":
            L += [f"> {PROVISIONAL_STAMP}"]
        L += ["", "| H | window | class | n | precision | payoff net "
              "| payoff med |", "|---|---|---|---|---|---|---|"]
        for name, per_w in sorted(res["cells"].items()):
            for wname, per_c in per_w.items():
                for cls, v in per_c.items():
                    p = (f"UNMEASURABLE {v['pct']}%" if v["unmeasurable"]
                         else f"{v['pct']}%")
                    L.append(f"| {name} | {wname} "
                             f"| {cls} | {v['n']} | {p} ({v['hits']}"
                             f"/{v['n']}) | {v['payoff_net']} "
                             f"| {v['payoff_median']} |")
        L.append("")
    with open(os.path.join(OUT, "location_census.md"), "w") as f:
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
        print(f"# location_census: {instr} ...", file=sys.stderr)
        results.append(run_instrument(instr))
    art = {"STAMP": "OBSERVATIONAL location census — pre-registered; "
                    "never validation",
           "engine_commit": head, "results": results}
    with open(os.path.join(OUT, "location_census.json"), "w") as f:
        json.dump(art, f, indent=2, default=str)
    _emit(results, head)
    print(f"OBSERVATIONAL location census -> {OUT}/location_census.md")


if __name__ == "__main__":
    main()
