"""Sequel census (register 71; pre-registered prereg_sequel_census) —
the narrative doctrine's first phase-two instrument (register 69): the
operator's climax-into-absorption question, ASYMMETRIC BY DESIGN.

For each anchor signal's fires (start: S0-H1, S0-H2 — the exhaustion
family), classify what follows within {5, 15} bars from the existing
event stream:
  ABSORPTION-flavored sequel — H3 cluster signature (an S0-H3 fire),
    a narrow-loud quadrant bar (register-66 conventions, cited), or a
    qualifying TEST print;
  OPPOSING-EFFORT sequel — continued wide-loud in the ORIGINAL move's
    direction (against the anchor's predicted reversal);
  NONE.
PRECEDENCE: the FIRST qualifying sequel bar in the window decides;
within one bar, absorption outranks opposing-effort (stated rule).
Denominators stay whole — every anchor fire lands in exactly one class
(no co-fire starvation). Class-conditioned baselines per the register-47
method: each class's base = the episode-begin rate of ALL bars whose own
forward window carries that sequel class (anchor-direction proxy for
generic bars = the bar's close direction — implementer detail, stated).

PURPOSE: tests the founding two-chapter story (exhaustion needs
absorption to become reversal) and directly addresses H1's
sight-without-harvest gap. Mint-on-lift, front door. Counts, dimming,
both windows, all instruments, sealed/lockbox excluded, twin-run pinned.
Weekly under Part C.
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

from engine.signal_watch import SignalWatch
from engine.store_loader import is_sealed, lockbox_boundary, zones
from backtest.conditioning_matrix import quadrant_of
from backtest.scoreboard import (PROVISIONAL_INSTRS, PROVISIONAL_STAMP,
                                 _payoff, _replay, build_moves, make_cfg)

OUT = os.path.join(ROOT, "reports", "scoreboard")

ANCHORS = ("S0-H1", "S0-H2")           # the exhaustion family, per order
SEQUEL_WINDOWS = (5, 15)               # bars; operator-stated
CLASSES = ("absorption", "opposing", "none")


class _SeqRecorder:
    """Per-1M-bar (rel_spread_pct, rel_volume, qualified) capture."""

    def __init__(self):
        self.map = {}

    def attach(self, engine):
        orig = engine.exec_pipe.on_close

        def observed(bar, ctx_tf=None, signal_ctx=None):
            out = orig(bar, ctx_tf=ctx_tf, signal_ctx=signal_ctx)
            if out is not None and not bar.is_stub:
                feats, cores, structural, qualified = out
                if feats.valid:
                    self.map[bar.ts.value] = (feats.rel_spread_pct,
                                              feats.rel_volume, qualified)
            return out
        engine.exec_pipe.on_close = observed


def classify_sequel(i, d, W, quad, closedir, test_mask, h3_bars, n):
    """First qualifying sequel bar in (i, i+W] decides; absorption
    outranks opposing within one bar. Deterministic (pinned)."""
    for j in range(i + 1, min(i + W + 1, n)):
        if (j in h3_bars or quad[j] == "narrow-loud" or test_mask[j]):
            return "absorption"
        if quad[j] == "wide-loud" and closedir[j] == -d:
            return "opposing"
    return "none"


def run_instrument(instr):
    cfg = make_cfg({"session_model.extended_hours": True,
                    "session_model.ladder": True,
                    "debug.structure": True})
    watch = SignalWatch()
    rec = _SeqRecorder()

    def _hook(engine):
        watch.attach(engine)
        rec.attach(engine)
    engine, bars, _ = _replay(cfg, instr, engine_hook=_hook)
    qual, eps, series, _d = build_moves(
        bars[cfg.mtf.execution_tf], bars[cfg.mtf.signal_tf],
        cfg.context.atr_period)
    ts, cl, _segs = series
    b1m = [x for x in bars[cfg.mtf.execution_tf] if not x.is_stub]
    op = np.array([x.open for x in b1m])
    n = len(ts)
    ep_starts = np.array(sorted(e["start"].value for e in eps))

    def ep_hit(t_ns):
        j = np.searchsorted(ep_starts, t_ns, side="left")
        return bool(j < len(ep_starts)
                    and ep_starts[j] <= t_ns + 3_600_000_000_000)
    hits_all = np.array([ep_hit(t) for t in ts])
    quad = np.array([quadrant_of(*rec.map.get(t, (None, None))[:2],
                                 cfg.labels.wide_spread_pctile,
                                 cfg.labels.high_volume_mult)
                     if t in rec.map else "unclassified"
                     for t in ts], dtype=object)
    test_mask = np.array([rec.map.get(t, (None, None, None))[2] == "TEST"
                          for t in ts])
    closedir = np.sign(cl - op).astype(int)
    h3_ts = {f["ts"].value for f in watch.fires if f["name"] == "S0-H3"}
    h3_bars = {int(np.searchsorted(ts, t, side="right") - 1)
               for t in h3_ts}
    anchors = [f for f in watch.fires
               if f["name"] in ANCHORS and not is_sealed(f["ts"])]
    boundary, gl = lockbox_boundary(), zones()["go_live"]
    win60 = pd.Timedelta(minutes=60)
    out = {"instrument": instr,
           "status": ("provisional" if instr in PROVISIONAL_INSTRS
                      else "canonical"),
           "cells": {}, "class_bases": {}}
    for W in SEQUEL_WINDOWS:
        # class-conditioned bases: every bar classified by its own
        # forward window (anchor-dir proxy = the bar's close direction)
        bar_class = np.array([
            classify_sequel(i, closedir[i] if closedir[i] != 0 else 1,
                            W, quad, closedir, test_mask, h3_bars, n)
            for i in range(n)], dtype=object)
        for w_lo, w_hi, wname in (
                (pd.Timestamp.min.tz_localize("UTC"), boundary,
                 "backtest"),
                (gl, pd.Timestamp.max.tz_localize("UTC"), "forward")):
            wmask = (ts >= w_lo.value) & (ts < w_hi.value)
            for cls in CLASSES:
                m = wmask & (bar_class == cls)
                out["class_bases"][f"{W}|{wname}|{cls}"] = (
                    round(100 * float(hits_all[m].mean()), 1)
                    if m.any() else None)
            for anchor in ANCHORS:
                for cls in CLASSES:
                    grp = []
                    for f in anchors:
                        if f["name"] != anchor \
                                or not (w_lo <= f["ts"] < w_hi):
                            continue
                        i = int(np.searchsorted(ts, f["ts"].value,
                                                side="right") - 1)
                        if i < 0:
                            continue
                        c = classify_sequel(i, f["dir"], W, quad,
                                            closedir, test_mask,
                                            h3_bars, n)
                        if c == cls:
                            grp.append((f, i))
                    if not grp:
                        continue
                    hits = sum(int(hits_all[i]) for _f, i in grp)
                    pay = _payoff([f for f, _i in grp], ts, cl, win60)
                    base = out["class_bases"][f"{W}|{wname}|{cls}"]
                    pct = round(100 * hits / len(grp), 1)
                    out["cells"]["|".join((anchor, str(W), wname,
                                           cls))] = {
                        "n": len(grp), "init_pct": pct,
                        "class_base_pct": base,
                        "lift_pp": (round(pct - base, 1)
                                    if base is not None else None),
                        "payoff_net": pay["net_pts"] if pay else None,
                        "payoff_median": (pay["median_per_fire"]
                                          if pay else None)}
    return out


def _emit(results, head):
    L = ["# Sequel Census — the two-chapter story (GENERATED by "
         "backtest.sequel_census)", "",
         "Terms: [docs/GLOSSARY.md](../../docs/GLOSSARY.md).", "",
         f"Engine `{head[:9]}` — OBSERVATIONAL, pre-registered "
         "(prereg_sequel_census, register 71; the narrative doctrine's "
         "first phase-two instrument, register 69). ASYMMETRIC BY "
         "DESIGN: anchors are the exhaustion family (S0-H1, S0-H2); "
         "sequels within {5,15} bars — ABSORPTION (S0-H3 signature, "
         "narrow-loud bar, or TEST print), OPPOSING-EFFORT (continued "
         "wide-loud in the original move's direction), or NONE. First "
         "qualifying bar decides; absorption outranks opposing within a "
         "bar. Every anchor fire lands in exactly one class — "
         "denominators stay whole. Lifts read against CLASS-CONDITIONED "
         "bases (each class's own episode-begin rate over all bars; "
         "anchor-dir proxy for generic bars = close direction, stated). "
         "PURPOSE: does exhaustion need absorption to become reversal "
         "(H1's sight-without-harvest gap)? Mint-on-lift, front door. "
         "° = n<20.", ""]
    for res in results:
        inst = res["instrument"]
        L += [f"## {inst} ({res['status'].upper()})"]
        if res["status"] == "provisional":
            L += [f"> {PROVISIONAL_STAMP}"]
        L += ["", "| anchor | W | window | sequel | n | init % | class "
              "base % | lift | payoff net/med |",
              "|---|---|---|---|---|---|---|---|---|"]
        for anchor in ANCHORS:
            for W in SEQUEL_WINDOWS:
                for wname in ("backtest", "forward"):
                    for cls in CLASSES:
                        c = res["cells"].get("|".join(
                            (anchor, str(W), wname, cls)))
                        if not c:
                            continue
                        dim = "°" if c["n"] < 20 else ""
                        lift = (f"{c['lift_pp']:+.1f}pp"
                                if c["lift_pp"] is not None else "—")
                        L.append(
                            f"| {anchor} | {W} | {wname} | {cls} "
                            f"| {dim}{c['n']} | {c['init_pct']} "
                            f"| {c['class_base_pct']} | {lift} "
                            f"| {c['payoff_net']}/{c['payoff_median']} |")
        L.append("")
    with open(os.path.join(OUT, "sequel_census.md"), "w") as f:
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
        print(f"# sequel_census: {instr} ...", file=sys.stderr)
        results.append(run_instrument(instr))
    art = {"STAMP": ("OBSERVATIONAL sequel census — narrative phase-two "
                     "instrument; never validation; mint-on-lift only"),
           "engine_commit": head, "anchors": list(ANCHORS),
           "windows_bars": list(SEQUEL_WINDOWS), "results": results}
    with open(os.path.join(OUT, "sequel_census.json"), "w") as f:
        json.dump(art, f, indent=2, default=str)
    _emit(results, head)
    print(f"OBSERVATIONAL sequels -> {OUT}/sequel_census.md")


if __name__ == "__main__":
    main()
