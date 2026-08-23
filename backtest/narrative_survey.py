"""Narrative survey census (register 73; pre-registered
prereg_narrative_survey) — the narrative doctrine's THOROUGHNESS
instrument (register 69): the systematic survey of the sentence space,
with its own luck fully priced. The two-anchor sequel census (register
71) is this survey's PILOT; its machinery generalizes here.

REGISTERED SEQUEL VOCABULARY (v1 — from the existing event stream only;
definitions cited, no new thresholds):
  absorption     — S0-H3 signature fire, narrow-loud quadrant bar
                   (register-66 conventions), or qualifying TEST print;
  opposing       — continued wide-loud effort in the ANCHOR BAR's own
                   close direction (against the predicted move; doji
                   anchor bars fall back to the anti-fire direction);
  effortless-same— EFFORTLESS_ADVANCE/_DECLINE structural print in the
                   fire's predicted direction;
  trend-flip     — a 1M phase-tracker trend flip, either direction
                   (TF STATED: 1M);
  map-arrival    — the bar's H11 location class becomes node or gap,
                   differing from the anchor bar's class (H11's
                   ratified map);
  none.
PRECEDENCE (stated): first qualifying bar in the window decides; within
one bar: absorption > opposing > effortless-same > trend-flip >
map-arrival.

SCOPE DISCIPLINE (register 73 clause 6): TWO-CLAUSE sentences only in
v1 (anchor + one sequel); three-clause sentences gate behind two-clause
survivors — the H12/H15 starvation precedent cited.

FIELD-SIZE HONESTY (clause 3, mandatory): the header states the total
cell count; every emission computes the expected-maximum-under-null by
permuting sequel labels WITHIN anchor (100 shuffles, pinned seed set —
label permutation preserves each cell's n; class-conditioned bases are
bar-population properties and do not reshuffle). A cell is
SURVEY-NOTABLE only if its |lift| exceeds the null's expected max among
measurable cells (n >= 20; dimmed cells excluded from the arithmetic,
as everywhere). The page prints how many cells the null predicts would
glow versus how many actually do. The null prices PRECISION lift only;
payoff medians are reported as texture.

FOCAL CELL (clause 4): S0-H1 x absorption — the survey's ONE
pre-registered focal cell (mechanism and prediction stated before the
survey existed: register 71's first emission; the founding two-chapter
story). Its head start is real and stays cited; it grades WITHIN the
field, against the same null, no special treatment in the arithmetic.

Q-MINTING RULE (clause 5): a cell becomes a question only if it is
survey-notable AND carries a written mechanism sentence — no mechanism,
no clock, however bright.

PURPOSE: the thesis is to be investigated, not anecdotally confirmed.
If the field glows only at null-expected rates at current data depth,
that reading stresses the doctrine itself (register 69 clause 3).
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
from backtest.conditioning_matrix import quadrant_of
from backtest.location_census import _Profile
from backtest.scoreboard import (PROVISIONAL_INSTRS, PROVISIONAL_STAMP,
                                 _payoff, _replay, build_moves,
                                 event_derived_fires, make_cfg)
from backtest.signal_points import all_signals

OUT = os.path.join(ROOT, "reports", "scoreboard")

SEQUEL_WINDOWS = (5, 15)                  # bars (register 71 pilot)
CLASSES = ("absorption", "opposing", "effortless-same", "trend-flip",
           "map-arrival", "none")
NULL_SHUFFLES = 100                       # clause 3; pinned
NULL_SEEDS = tuple(range(NULL_SHUFFLES))  # pinned seed set
FOCAL = ("S0-H1", "absorption")           # clause 4
# consistency statistic (register 73 amendment — the doctrine's actual
# prediction shape): a PAIR (anchor x sequel) qualifies when >=3 of its
# measurable cells (n >= 15) carry same-signed lifts, each |lift| > 3pp
CONS_MIN_CELLS = 3
CONS_MIN_N = 15
CONS_MIN_LIFT_PP = 3.0
CONS_PCTL = 95.0


class _SurveyRecorder:
    """Per-1M-bar (rel_spread_pct, rel_volume, structural, qualified)."""

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
                                              feats.rel_volume,
                                              structural, qualified)
            return out
        engine.exec_pipe.on_close = observed


def classify(i, d, anchor_dir_close, W, arrs, n):
    """First qualifying bar in (i, i+W] decides; precedence within a
    bar as documented. Deterministic (pinned).
    arrs: dict with quad, closedir, test, eff_dir, flip, h11, h3 (set).
    anchor_dir_close: the anchor bar's own close direction (opposing =
    continued effort that way); 0 falls back to -d."""
    ad = anchor_dir_close if anchor_dir_close != 0 else -d
    for j in range(i + 1, min(i + W + 1, n)):
        if (j in arrs["h3"] or arrs["quad"][j] == "narrow-loud"
                or arrs["test"][j]):
            return "absorption"
        if arrs["quad"][j] == "wide-loud" and arrs["closedir"][j] == ad:
            return "opposing"
        if arrs["eff_dir"][j] == d:
            return "effortless-same"
        if arrs["flip"][j]:
            return "trend-flip"
        if arrs["h11"][j] in ("node", "gap") \
                and arrs["h11"][j] != arrs["h11"][i]:
            return "map-arrival"
    return "none"


def _pair_qualifies(cells):
    """cells: list of (window, n, lift). Returns (qualifies,
    n_measurable, spans_both_windows_same_signed)."""
    meas = [(w, n_, l) for w, n_, l in cells
            if n_ >= CONS_MIN_N and l is not None]
    if len(meas) < CONS_MIN_CELLS:
        return False, len(meas), False
    signs = {1 if l > 0 else -1 if l < 0 else 0 for _w, _n, l in meas}
    same = len(signs) == 1 and 0 not in signs
    strong = all(abs(l) > CONS_MIN_LIFT_PP for _w, _n, l in meas)
    wins = {w for w, _n, _l in meas}
    return (same and strong), len(meas), \
        (same and len(wins) >= 2)


def survey_nulls(cells_by_anchor, bases):
    """Both permutation statistics over the SAME pinned shuffles
    (register 73 + amendment): EXTREMITY — expected max |lift| among
    measurable (n>=20) cells; CONSISTENCY — the null distribution of
    the count of qualifying pairs (>=3 cells n>=15, same-signed,
    |lift|>3pp). Labels permute within (anchor, W, window); each cell's
    n is preserved; bases do not reshuffle. Deterministic (pinned)."""
    keys = list(cells_by_anchor)
    maxima, cons_counts = [], []
    for seed in NULL_SEEDS:
        rs = np.random.RandomState(seed)
        lifts = []
        pair_cells = {}
        for key in keys:
            anchor, W, win = key
            pairs = cells_by_anchor[key]
            labels = [p[0] for p in pairs]
            hits = np.array([p[1] for p in pairs])
            perm = rs.permutation(len(labels))
            shuffled = [labels[k] for k in perm]
            for cls in CLASSES:
                m = np.array([sh == cls for sh in shuffled])
                nc = int(m.sum())
                base = bases.get((W, win, cls))
                if base is None or nc == 0:
                    continue
                lift = 100 * float(hits[m].mean()) - base
                if nc >= 20:
                    lifts.append(abs(lift))
                pair_cells.setdefault((anchor, cls), []).append(
                    (win, nc, lift))
        maxima.append(max(lifts) if lifts else 0.0)
        cons_counts.append(sum(
            1 for cells in pair_cells.values()
            if _pair_qualifies(cells)[0]))
    exp_max = float(np.mean(maxima))
    glows = []
    for k, seed in enumerate(NULL_SEEDS):
        rs = np.random.RandomState(seed)
        cnt = 0
        for key in keys:
            anchor, W, win = key
            pairs = cells_by_anchor[key]
            labels = [p[0] for p in pairs]
            hits = np.array([p[1] for p in pairs])
            perm = rs.permutation(len(labels))
            shuffled = [labels[k2] for k2 in perm]
            for cls in CLASSES:
                m = np.array([sh == cls for sh in shuffled])
                if m.sum() < 20:
                    continue
                base = bases.get((W, win, cls))
                if base is None:
                    continue
                if abs(100 * float(hits[m].mean()) - base) > exp_max:
                    cnt += 1
        glows.append(cnt)
    return {"shuffles": NULL_SHUFFLES,
            "expected_max_abs_lift_pp": round(exp_max, 1),
            "null_expected_glow_cells": round(float(np.mean(glows)), 2),
            "null_consistent_pairs": {
                "median": float(np.median(cons_counts)),
                "p95": float(np.percentile(cons_counts, 95)),
                "mean": round(float(np.mean(cons_counts)), 2)},
            "_cons_counts": cons_counts}


def run_instrument(instr):
    cfg = make_cfg({"session_model.extended_hours": True,
                    "session_model.ladder": True,
                    "debug.structure": True})
    watch = SignalWatch()
    rec = _SurveyRecorder()

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
    getm = rec.map.get
    quad = np.array([quadrant_of(*getm(t, (None,) * 4)[:2],
                                 cfg.labels.wide_spread_pctile,
                                 cfg.labels.high_volume_mult)
                     if t in rec.map else "unclassified"
                     for t in ts], dtype=object)
    test_mask = np.array([getm(t, (None,) * 4)[3] == "TEST" for t in ts])
    eff_dir = np.array([{"EFFORTLESS_ADVANCE": 1,
                         "EFFORTLESS_DECLINE": -1}.get(
                            getm(t, (None,) * 4)[2], 0) for t in ts])
    closedir = np.sign(cl - op).astype(int)
    flips = np.zeros(n, bool)
    prev = 0
    for e in engine.narrative.events:
        if e["type"] == "PHASE_EVAL" and e.get("tf") == "1min":
            t = e.get("trend", 0)
            if t != prev and t != 0:
                j = np.searchsorted(ts, pd.Timestamp(e["ts"]).value,
                                    side="right") - 1
                if 0 <= j < n:
                    flips[j] = True
            prev = t
    prof = _Profile()
    h11 = np.array([prof.feed(x) or "unclassified" for x in b1m],
                   dtype=object)
    h3_bars = {int(np.searchsorted(ts, f["ts"].value, side="right") - 1)
               for f in watch.fires if f["name"] == "S0-H3"}
    arrs = {"quad": quad, "closedir": closedir, "test": test_mask,
            "eff_dir": eff_dir, "flip": flips, "h11": h11, "h3": h3_bars}
    fires = watch.fires + event_derived_fires(engine.narrative.events,
                                              cfg, bars, instr=instr)
    fires = [f for f in fires
             if f["name"] not in AGNOSTIC_ROWS and not is_sealed(f["ts"])]
    anchors = sorted({name for _h, _s, name in all_signals()
                      if name not in AGNOSTIC_ROWS})
    boundary, gl = lockbox_boundary(), zones()["go_live"]
    win60 = pd.Timedelta(minutes=60)
    out = {"instrument": instr,
           "status": ("provisional" if instr in PROVISIONAL_INSTRS
                      else "canonical"),
           "cells": {}, "class_bases": {}, "null": None,
           "total_cells": 0}
    bases = {}
    for W in SEQUEL_WINDOWS:
        bar_class = np.array([
            classify(i, closedir[i] if closedir[i] != 0 else 1,
                     closedir[i], W, arrs, n) for i in range(n)],
            dtype=object)
        for w_lo, w_hi, wname in (
                (pd.Timestamp.min.tz_localize("UTC"), boundary,
                 "backtest"),
                (gl, pd.Timestamp.max.tz_localize("UTC"), "forward")):
            wmask = (ts >= w_lo.value) & (ts < w_hi.value)
            for cls in CLASSES:
                m = wmask & (bar_class == cls)
                b = (round(100 * float(hits_all[m].mean()), 1)
                     if m.any() else None)
                bases[(W, wname, cls)] = b
                out["class_bases"][f"{W}|{wname}|{cls}"] = b
    cells_by_anchor = {}
    for anchor in anchors:
        af = [f for f in fires if f["name"] == anchor]
        for W in SEQUEL_WINDOWS:
            for w_lo, w_hi, wname in (
                    (pd.Timestamp.min.tz_localize("UTC"), boundary,
                     "backtest"),
                    (gl, pd.Timestamp.max.tz_localize("UTC"),
                     "forward")):
                pairs, per_cls = [], {}
                for f in af:
                    if not (w_lo <= f["ts"] < w_hi):
                        continue
                    i = int(np.searchsorted(ts, f["ts"].value,
                                            side="right") - 1)
                    if i < 0:
                        continue
                    cls = classify(i, f["dir"], closedir[i], W, arrs, n)
                    hit = bool(hits_all[i])
                    pairs.append((cls, hit))
                    per_cls.setdefault(cls, []).append((f, hit))
                if pairs:
                    cells_by_anchor[(anchor, W, wname)] = pairs
                for cls, grp in per_cls.items():
                    base = bases[(W, wname, cls)]
                    pct = round(100 * sum(h for _f, h in grp)
                                / len(grp), 1)
                    pay = _payoff([f for f, _h in grp], ts, cl, win60)
                    out["cells"]["|".join((anchor, str(W), wname,
                                           cls))] = {
                        "n": len(grp), "init_pct": pct,
                        "class_base_pct": base,
                        "lift_pp": (round(pct - base, 1)
                                    if base is not None else None),
                        "payoff_net": pay["net_pts"] if pay else None,
                        "payoff_median": (pay["median_per_fire"]
                                          if pay else None)}
    out["total_cells"] = len(out["cells"])
    out["null"] = survey_nulls(cells_by_anchor, bases)
    if out["null"]:
        # EXTREMITY marking (clause 3): measurable cells beyond the
        # null's expected max
        thr = out["null"]["expected_max_abs_lift_pp"]
        glow = 0
        for c in out["cells"].values():
            c["survey_notable"] = bool(
                c["n"] >= 20 and c["lift_pp"] is not None
                and abs(c["lift_pp"]) > thr)
            glow += int(c["survey_notable"])
        out["null"]["actual_glow_cells"] = glow
        # CONSISTENCY statistic (register 73 amendment): observed
        # qualifying pairs vs the null count distribution
        pair_obs = {}
        for key, v in out["cells"].items():
            anchor, _W, wname, cls = key.split("|")
            pair_obs.setdefault((anchor, cls), []).append(
                (wname, v["n"], v["lift_pp"]))
        actual, candidates, marked = 0, 0, []
        for pk, cells in pair_obs.items():
            q, nm, spans = _pair_qualifies(cells)
            if nm >= CONS_MIN_CELLS:
                candidates += 1
            if q:
                actual += 1
                if spans:
                    marked.append(pk)
        counts = out["null"].pop("_cons_counts")
        pct = round(100 * float(np.mean(
            [actual > c for c in counts])), 1)
        significant = pct > CONS_PCTL
        out["null"]["consistency"] = {
            "actual_qualifying_pairs": actual,
            "candidate_pairs": candidates,
            "percentile_vs_null": pct,
            "field_significant": significant}
        for key, v in out["cells"].items():
            anchor, _W, wname, cls = key.split("|")
            v["consistency_notable"] = bool(
                significant and (anchor, cls) in marked)
    return out


def _emit(results, head):
    total = sum(r["total_cells"] for r in results)
    L = ["# Narrative Survey — the sentence space, luck priced "
         "(GENERATED by backtest.narrative_survey)", "",
         "Terms: [docs/GLOSSARY.md](../../docs/GLOSSARY.md).", "",
         f"Engine `{head[:9]}` — OBSERVATIONAL, pre-registered "
         "(prereg_narrative_survey, register 73). The narrative "
         "doctrine's THOROUGHNESS instrument (register 69): every "
         "signal-live anchor × the registered sequel vocabulary × "
         "W ∈ {5,15} bars, two-clause sentences only (v1; three-clause "
         "gates behind survivors — the H12/H15 starvation precedent). "
         f"**FIELD SIZE: {total} cells this emission.** Lifts read "
         "against class-conditioned floors (register-47 method). "
         "NULL CALIBRATION: sequel labels permuted within anchor "
         f"({NULL_SHUFFLES} shuffles, pinned seeds); a cell is "
         "SURVEY-NOTABLE only if its |lift| exceeds the null's expected "
         "max among measurable (n≥20) cells. CONSISTENCY STATISTIC "
         "(register 73 amendment — the doctrine's actual prediction "
         "shape): same pinned shuffles; a pair qualifies on ≥3 "
         "measurable cells (n≥15) same-signed at |lift|>3pp; "
         "consistency-notable requires the field percentile > 95 AND "
         "the pair same-signed across windows. Q-MINTING RULE: notable "
         "BY EITHER ROUTE (extremity or consistency) AND a written "
         "mechanism sentence — no mechanism, no clock, however bright. "
         "FOCAL CELL: "
         f"{FOCAL[0]} × {FOCAL[1]} (pre-registered, register 71 pilot; "
         "head start cited; grades within the field, same null, no "
         "special arithmetic). If the field glows only at null-expected "
         "rates, that reading stresses the doctrine itself (register 69 "
         "clause 3). The pilot (sequel_census, register 71) is "
         "superseded by this survey. ° = n<20; full grid in the JSON.",
         ""]
    for res in results:
        inst = res["instrument"]
        L += [f"## {inst} ({res['status'].upper()})"]
        if res["status"] == "provisional":
            L += [f"> {PROVISIONAL_STAMP}"]
        nu = res.get("null")
        if nu:
            co = nu.get("consistency", {})
            np_ = nu.get("null_consistent_pairs", {})
            L += ["", f"**Luck budget ({inst}) — both statistics side "
                  f"by side.** EXTREMITY: {res['total_cells']} cells; "
                  f"null expected max |lift| "
                  f"{nu['expected_max_abs_lift_pp']}pp; null predicts "
                  f"{nu['null_expected_glow_cells']} glowing; actually "
                  f"glowing: {nu['actual_glow_cells']}. CONSISTENCY "
                  "(the doctrine's actual prediction shape): "
                  f"**{co.get('actual_qualifying_pairs', '—')} of "
                  f"{co.get('candidate_pairs', '—')} candidate pairs "
                  "qualify** (≥3 cells n≥15, same-signed, |lift|>3pp) "
                  f"vs null median {np_.get('median', '—')} / p95 "
                  f"{np_.get('p95', '—')}; percentile "
                  f"{co.get('percentile_vs_null', '—')} — "
                  + ("**FIELD-SIGNIFICANT**"
                     if co.get("field_significant")
                     else "not field-significant") + ".",
                  ""]
        L += ["| anchor | W | window | sequel | n | init % | base % "
              "| lift | notable | payoff net/med |",
              "|---|---|---|---|---|---|---|---|---|---|"]
        rows = [(k.split("|"), v) for k, v in res["cells"].items()
                if v["n"] >= 20 and v["lift_pp"] is not None]
        rows.sort(key=lambda r: -abs(r[1]["lift_pp"]))
        focal_key = None
        for (anchor, W, wname, cls), v in rows:
            if (anchor, cls) == FOCAL:
                focal_key = True
            routes = ([r for r, k in (("EXT", "survey_notable"),
                                      ("CONS", "consistency_notable"))
                       if v.get(k)])
            mark = "**" + "+".join(routes) + "**" if routes else "—"
            foc = " ← FOCAL" if (anchor, cls) == FOCAL else ""
            L.append(f"| {anchor} | {W} | {wname} | {cls}{foc} "
                     f"| {v['n']} | {v['init_pct']} "
                     f"| {v['class_base_pct']} | {v['lift_pp']:+.1f}pp "
                     f"| {mark} | {v['payoff_net']}/"
                     f"{v['payoff_median']} |")
        omitted = res["total_cells"] - len(rows)
        L += [f"", f"({omitted} dimmed/unmeasurable cells omitted — "
              "full grid in the JSON.)", ""]
        if not focal_key:
            L += [f"(Focal cell {FOCAL[0]}×{FOCAL[1]} currently "
                  "dimmed/unmeasurable on this instrument — printed in "
                  "the JSON.)", ""]
    with open(os.path.join(OUT, "narrative_survey.md"), "w") as f:
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
        print(f"# narrative_survey: {instr} ...", file=sys.stderr)
        results.append(run_instrument(instr))
    art = {"STAMP": ("OBSERVATIONAL narrative survey — the sentence "
                     "space with luck priced; never validation; "
                     "Q-minting: notable + mechanism only"),
           "engine_commit": head, "classes": list(CLASSES),
           "windows_bars": list(SEQUEL_WINDOWS),
           "null_shuffles": NULL_SHUFFLES,
           "focal_cell": list(FOCAL), "results": results}
    with open(os.path.join(OUT, "narrative_survey.json"), "w") as f:
        json.dump(art, f, indent=2, default=str)
    _emit(results, head)
    print(f"OBSERVATIONAL survey -> {OUT}/narrative_survey.md")


if __name__ == "__main__":
    main()
