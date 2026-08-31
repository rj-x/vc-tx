"""Aggregation-decay census (register 121; pre-registered
prereg_aggregation_decay, counted 2026-08-31; the register-27/35
pre-sketch executed as originally scoped — trial log
presketch_cascade_decay_census + its amendment). OBSERVATIONAL.

VOCABULARY (register 27's split, named as ordered): CASCADE = label
arrival at successive rungs; MIGRATION CHAIN = the persistence object
(>= 2 children per parent window) — different objects; this page
reports CASCADE arrival and PER-EVENT rv survival, never chains.
NESTING CAVEAT (the campaign's standing line, inherited): higher-TF
labels are compositions of lower-TF bars, not independent
confirmations; NEVER pool across TFs.

TWO MEASUREMENTS on the six-rung ladder (the registered LADDER — the
dense-rung densification idea stays unbuilt, stated):
(a) TIME-TO-ARRIVAL per rung, for the 1M TREND-ONSET population
    (the T1d object: the 1M phase tracker turning nonzero), split
    true/false lead (a qualifying episode begins within the registered
    60-min window, the initiation convention): minutes from onset to
    the first same-direction STRUCTURAL label at that rung, within the
    same 60-min window; the k-lag arithmetic floor (minutes to that
    rung's first bar close) prints beside it as the REGISTERED NULL
    CONTROL — no permutation null; arrival tracking the floor = the
    expected null (the reviewer's split prior, on record).
(b) PER-EVENT EFFORT-DECAY, for the high-effort classes (structural
    climaxes; rv-anomalies = rel_volume >= LOUD_MULT, register 66):
    how many CONSECUTIVE rungs from 1M upward the event's parent bar
    carries rel_volume >= the same cut vs THAT RUNG'S OWN tod
    baseline — rv sourced from every rung pipe's FeatureEngine
    directly (the trial-log line-44 mandate: INDEPENDENT of label
    qualification; LABEL events only carry rv when a core matches),
    conditional on true/false lead and on outcome (median 60-min
    drift in the event direction, by survival depth).

Full rung grid (the amendment: the 15M-grid restriction was an
outcome-measurement artifact, not inherited here). Both windows, all
four legs, sealed excluded, no pooling; counts and distributions —
the priors are on record, the census decides. Prerequisite cited:
rv on structural-only labels (register 28). The chain hypothesis is
the customer (its recruited-chains clause; the ger40 structure-family
forward flicker, register 108, is uninterpretable without this
instrument). Twin-run pinned
(tests/test_aggregation_decay.py). Weekly under Part C.
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

from engine.store_loader import is_sealed, lockbox_boundary, zones
from backtest.migration import LADDER, _MIN
from backtest.scoreboard import (MOVE_WINDOW_MIN, _replay, build_init,
                                 build_moves, make_cfg)
from backtest.underwater_census import LOUD_MULT

OUT = os.path.join(ROOT, "reports", "scoreboard")
CLIMAXES = ("SELLING_CLIMAX", "BUYING_CLIMAX")
# the climax's directional grading = H1's registered convention (the
# reversal direction: selling climax -> +1), mirrored from _s_h1
CLIMAX_DIR = {"SELLING_CLIMAX": 1, "BUYING_CLIMAX": -1}


class _RungRVRecorder:
    """Per-rung rel_volume for EVERY measured bar, from each rung
    pipe's own FeatureEngine (tod-binned per rung) — independent of
    label qualification (the line-44 mandate)."""

    def __init__(self):
        self.map = {}     # tf -> {bar_open_ts_ns: rel_volume}

    def attach_pipe(self, tf, pipe):
        orig = pipe.on_close

        def observed(bar, *a, **kw):
            out = orig(bar, *a, **kw)
            if out is not None and not bar.is_stub:
                feats = out[0]
                if feats.valid and feats.rel_volume is not None:
                    self.map.setdefault(tf, {})[bar.ts.value] = \
                        float(feats.rel_volume)
            return out
        pipe.on_close = observed

    def attach(self, engine, cfg):
        stack = {cfg.mtf.execution_tf: engine.exec_pipe,
                 cfg.mtf.signal_tf: engine.signal_pipe,
                 cfg.mtf.context_tf: engine.context_pipe}
        for tf in LADDER:
            pipe = stack.get(tf) or engine.ladder_pipes.get(tf)
            if pipe is not None:
                self.attach_pipe(tf, pipe)


def parent_open(ts_ns, rung_min):
    """The open of the rung bar containing a 1M open timestamp —
    fixed-grid arithmetic (UTC-anchored rungs, the store convention)."""
    span = rung_min * 60_000_000_000
    return (ts_ns // span) * span


def klag_floor_min(ts_ns, rung_min):
    """Minutes from the 1M bar open to its rung parent's CLOSE — the
    arithmetic null control."""
    return (parent_open(ts_ns, rung_min) + rung_min * 60_000_000_000
            - ts_ns) / 60_000_000_000


def survival_depth(ts_ns, rv_maps, cut=LOUD_MULT):
    """Consecutive rungs from 1M upward whose parent bar carries
    rel_volume >= cut vs its own rung baseline; unmeasured parent bars
    break the run (counted separately by the caller)."""
    depth = 0
    for tf in LADDER:
        rv = rv_maps.get(tf, {}).get(parent_open(ts_ns, _MIN[tf]))
        if rv is None or rv < cut:
            break
        depth += 1
    return depth


def arrivals_by_rung(ts_ns, d, labels_by_tf, window_min=MOVE_WINDOW_MIN):
    """Per rung: minutes to the first same-direction structural label
    at/after the onset, within the registered window (None = none)."""
    out = {}
    w = window_min * 60_000_000_000
    for tf in LADDER[1:]:
        arr = None
        for lt, ld in labels_by_tf.get(tf, []):
            if lt < ts_ns:
                continue
            if lt > ts_ns + w:
                break
            if ld == d:
                arr = (lt - ts_ns) / 60_000_000_000
                break
        out[tf] = arr
    return out


def _labels(events):
    from backtest.eventstudy import LABEL_DIR
    out = {}
    for e in events:
        if e["type"] == "LABEL" and e.get("structural"):
            d = LABEL_DIR.get(e["structural"], 0)
            if d:
                out.setdefault(e["tf"], []).append(
                    (pd.Timestamp(e["ts"]).value, d))
    return {tf: sorted(v) for tf, v in out.items()}


def _dist(v):
    if not v:
        return None
    a = np.array(v, float)
    return {"n": int(len(a)), "median": round(float(np.median(a)), 1),
            "p90": round(float(np.percentile(a, 90)), 1)}


def run_instrument(instr):
    cfg = make_cfg({"session_model.extended_hours": True,
                    "session_model.ladder": True,
                    "debug.structure": True})
    rec = _RungRVRecorder()

    def _hook(engine):
        rec.attach(engine, cfg)
    engine, bars, _ = _replay(cfg, instr, engine_hook=_hook)
    qual, eps, series, _d = build_moves(
        bars[cfg.mtf.execution_tf], bars[cfg.mtf.signal_tf],
        cfg.context.atr_period)
    ts, cl = series[0], series[1]
    eps = [e for e in eps if not is_sealed(e["start"])]
    init = build_init(eps, series)
    n = len(ts)
    # 1M trend state (the T1d onset object)
    t1_map = {}
    for e in engine.narrative.events:
        if e["type"] == "PHASE_EVAL" and e.get("tf") == "1min":
            t1_map[pd.Timestamp(e["ts"]).value] = e.get("trend", 0)
    t1 = np.array([t1_map.get(t, 0) for t in ts])
    labels_by_tf = _labels(engine.narrative.events)
    # 60-min drift
    idx60 = np.searchsorted(ts, ts + MOVE_WINDOW_MIN * 60_000_000_000,
                            side="left")
    boundary, gl = lockbox_boundary(), zones()["go_live"]
    day_ts = pd.DatetimeIndex(pd.to_datetime(ts, utc=True))
    sealed_days = {d_: bool(is_sealed(pd.Timestamp(d_)))
                   for d_ in day_ts.normalize().unique()}
    unsealed = ~np.array([sealed_days[d_] for d_ in day_ts.normalize()])

    def win_of(i):
        if not unsealed[i]:
            return None
        if ts[i] < boundary.value:
            return "backtest"
        if ts[i] >= gl.value:
            return "forward"
        return None
    rv1 = rec.map.get("1min", {})
    # (a) onsets
    onsets = [(i, int(t1[i])) for i in range(1, n)
              if t1[i] != 0 and t1[i] != t1[i - 1]]
    arrival = {}
    for i, d in onsets:
        w = win_of(i)
        if w is None:
            continue
        lead = "true-lead" if init[d][i] else "false-lead"
        arr = arrivals_by_rung(ts[i], d, labels_by_tf)
        for tf in LADDER[1:]:
            c = arrival.setdefault((w, lead, tf), {
                "n": 0, "arrived": 0, "mins": [], "floor": []})
            c["n"] += 1
            c["floor"].append(klag_floor_min(ts[i], _MIN[tf]))
            if arr[tf] is not None:
                c["arrived"] += 1
                c["mins"].append(arr[tf])
    # (b) effort-decay events
    ev = []
    for e in engine.narrative.events:
        if e["type"] == "LABEL" and e.get("tf") == "1min" \
                and e.get("structural") in CLIMAXES:
            t_ns = pd.Timestamp(e["ts"]).value
            i = int(np.searchsorted(ts, t_ns, side="left"))
            if i < n and ts[i] == t_ns:
                ev.append((i, "climax", CLIMAX_DIR[e["structural"]]))
    for i in range(n):
        rv = rv1.get(ts[i])
        if rv is not None and rv >= LOUD_MULT:
            d = int(np.sign(cl[i] - (cl[i - 1] if i else cl[i])))
            if d:
                ev.append((i, "rv-anomaly", d))
    decay = {}
    unmeasured = 0
    for i, cls_, d in ev:
        w = win_of(i)
        if w is None:
            continue
        if ts[i] not in rv1:
            unmeasured += 1
            continue
        depth = survival_depth(ts[i], rec.map)
        lead = "true-lead" if init[d][i] else "false-lead"
        j = min(int(idx60[i]), n - 1)
        drift = float((cl[j] - cl[i]) * d)
        c = decay.setdefault((w, cls_, lead), {"depths": {}, "outcome": {}})
        c["depths"][depth] = c["depths"].get(depth, 0) + 1
        c["outcome"].setdefault("deep" if depth >= 3 else "shallow",
                                []).append(drift)
    out = {"instrument": instr,
           "onsets": len(onsets),
           "events_unmeasured_rv": unmeasured,
           "arrival": {"|".join(map(str, k)): {
               "n": c["n"], "arrived": c["arrived"],
               "arrival_min": _dist(c["mins"]),
               "klag_floor_min": _dist(c["floor"])}
               for k, c in sorted(arrival.items())},
           "effort_decay": {"|".join(k): {
               "survival_depths": dict(sorted(c["depths"].items())),
               "outcome_by_depth": {b: _dist(v) for b, v in
                                    sorted(c["outcome"].items())}}
               for k, c in sorted(decay.items())}}
    return out


def _emit(art, head):
    L = ["# Aggregation-Decay Census (GENERATED by "
         "backtest.aggregation_decay)", "",
         "Terms: [docs/GLOSSARY.md](../../docs/GLOSSARY.md).", "",
         f"Engine `{head[:9]}` — OBSERVATIONAL, pre-registered "
         "(prereg_aggregation_decay, register 121; the register-27/35 "
         "pre-sketch as scoped; prerequisite register 28 cited). "
         "VOCABULARY: CASCADE (label arrival at successive rungs), "
         "never migration chains — different objects (register 27). "
         "NESTING CAVEAT: higher-TF labels are compositions of "
         "lower-TF bars, not independent confirmations; NEVER pool "
         "across TFs. (a) onset time-to-arrival per rung vs the k-lag "
         "ARITHMETIC FLOOR (the registered null control — no "
         "permutation null; arrival tracking the floor = the expected "
         "null, the reviewer's split prior on record); (b) per-event "
         f"rv survival across rungs (cut = {LOUD_MULT:g}x the rung's "
         "OWN tod baseline; rv from every rung pipe's FeatureEngine, "
         "independent of label qualification — the line-44 mandate), "
         "by lead and outcome. Six-rung ladder (registered; the "
         "dense-rung idea stays unbuilt, stated). Counts and "
         "distributions; the census decides, not the priors. The chain hypothesis is "
         "the customer.", ""]
    for res in art["results"]:
        L += [f"## {res['instrument']} ({res['onsets']} 1M trend "
              f"onsets; {res['events_unmeasured_rv']} events with "
              "unmeasured 1M rv excluded — counted, per register 44's "
              "conflation lesson)", "",
              "### (a) Time-to-arrival per rung (same-direction "
              "structural label within 60 min; floor = the rung's "
              "first close)", "",
              "| window | lead | rung | n | arrived | arrival med/p90 "
              "(min) | k-lag floor med/p90 |",
              "|---|---|---|---|---|---|---|"]
        for key, c in res["arrival"].items():
            w, lead, tf = key.split("|")
            a, f = c["arrival_min"], c["klag_floor_min"]
            acell = f"{a['median']}/{a['p90']}" if a else "—"
            fcell = f"{f['median']}/{f['p90']}" if f else "—"
            L.append(f"| {w} | {lead} | {tf} | {c['n']} | {c['arrived']} "
                     f"| {acell} | {fcell} |")
        L += ["", "### (b) Per-event effort decay (consecutive rungs "
              "carrying rv >= the cut; outcome = 60-min drift in the "
              "event direction)", "",
              "| window | class | lead | survival depths {rungs: n} "
              "| shallow (<3) outcome | deep (>=3) outcome |",
              "|---|---|---|---|---|---|"]
        for key, c in res["effort_decay"].items():
            w, cls_, lead = key.split("|")
            sh = c["outcome_by_depth"].get("shallow")
            dp = c["outcome_by_depth"].get("deep")

            def _o(x):
                return (f"med {x['median']} (n{x['n']})" if x else "—")
            L.append(f"| {w} | {cls_} | {lead} | {c['survival_depths']} "
                     f"| {_o(sh)} | {_o(dp)} |")
        L.append("")
    with open(os.path.join(OUT, "aggregation_decay.md"), "w") as f:
        f.write("\n".join(L))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--instr", nargs="*",
                    default=["uk100fut", "ger40fut", "nas100fut",
                             "us30fut"])
    a = ap.parse_args()
    head = subprocess.run(["git", "rev-parse", "HEAD"], cwd=ROOT,
                          capture_output=True, text=True).stdout.strip()
    results = []
    for instr in a.instr:
        print(f"# aggregation_decay: {instr} ...", file=sys.stderr)
        results.append(run_instrument(instr))
    art = {"STAMP": ("OBSERVATIONAL aggregation-decay census — cascade "
                     "arrival + per-event rv survival; counts and "
                     "distributions; never validation"),
           "engine_commit": head, "ladder": list(LADDER),
           "rv_cut": LOUD_MULT, "window_min": MOVE_WINDOW_MIN,
           "results": results}
    with open(os.path.join(OUT, "aggregation_decay.json"), "w") as f:
        json.dump(art, f, indent=2, default=str)
    _emit(art, head)
    print(f"OBSERVATIONAL aggregation decay -> {OUT}/aggregation_decay.md")


if __name__ == "__main__":
    main()
