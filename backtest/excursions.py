"""Excursion-profile study (register 42 item 7; pre-registered,
OBSERVATIONAL). Purpose, stated: the PRINCIPLED INPUT to the v1
recipe-values discussion — management style derived per hypothesis from
MEASURED excursion shape, not guessed. No recipe changes flow from this
without operator ratification.

(a) For every directional hypothesis fire, every instrument, both windows:
    MFE and MAE over the following 60 minutes (the registered move window)
    from the fire bar's close, plus time-to-MFE; distributions
    (median/p75/p90) per hypothesis x instrument x session; counts
    everywhere; sealed/lockbox excluded; PROVISIONAL stamps carried.
(b) Narrative-conditional cut — THE GATE ON ALL NARRATIVE-EXIT RECIPES.
    The question, stated: do opposing narrative events during a hold
    predict adverse resolution? Each fire's window is split by whether an
    opposing event occurred (per class: opposing 1M structural core /
    1M trend flip against / opposing S-H fire) and by its timing
    (first occurrence; early = first half of the window).
    Adverse resolution = signed net excursion at window end < 0.
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
from backtest.sessions import session_of
from backtest.eventstudy import LABEL_DIR
from backtest.scoreboard import (PROVISIONAL_INSTRS, PROVISIONAL_STAMP,
                                 _replay, _series, event_derived_fires,
                                 make_cfg)

OUT = os.path.join(ROOT, "reports", "scoreboard")
WINDOW_NS = 60 * 60_000_000_000            # registry: qualifying_move window


def _dist(a):
    if not len(a):
        return None
    a = np.array(a, float)
    return {"n": len(a), "median": round(float(np.median(a)), 2),
            "p75": round(float(np.percentile(a, 75)), 2),
            "p90": round(float(np.percentile(a, 90)), 2)}


def _narr_streams(events, fires):
    """Opposing-event streams: (ts_ns, dir) per class."""
    core = []
    for e in events:
        if (e["type"] == "LABEL" and e.get("tf") == "1min"
                and e.get("structural")):
            d = LABEL_DIR.get(e["structural"], 0)
            if d:
                core.append((pd.Timestamp(e["ts"]).value, d))
    flips, prev = [], 0
    for e in events:
        if e["type"] == "PHASE_EVAL" and e.get("tf") == "1min":
            t = e.get("trend", 0)
            if t != prev and t != 0:
                flips.append((pd.Timestamp(e["ts"]).value, t))
            prev = t
    sf = sorted((f["ts"].value, f["dir"]) for f in fires)
    return {"opposing_structural_core": sorted(core),
            "trend_flip": sorted(flips),
            "opposing_signal_fire": sf}


def _first_opposing(stream, lo, hi, d):
    ks = [e[0] for e in stream]
    i = np.searchsorted(ks, lo, side="right")
    for e in stream[i:]:
        if e[0] > hi:
            return None
        if e[1] == -d:
            return e[0]
    return None


def run_instrument(instr):
    cfg = make_cfg({"session_model.extended_hours": True,
                    "session_model.ladder": True,
                    "debug.structure": True})       # 1M trend flips
    watch = SignalWatch()
    engine, bars, _ = _replay(cfg, instr, engine_hook=watch.attach)
    ts, cl, hi, lo, _s, _b = _series(bars[cfg.mtf.execution_tf])
    fires = watch.fires + event_derived_fires(engine.narrative.events, cfg, bars, instr=instr)
    fires = [f for f in fires
             if f["name"] not in AGNOSTIC_ROWS and not is_sealed(f["ts"])]
    narr = _narr_streams(engine.narrative.events, fires)
    boundary, gl = lockbox_boundary(), zones()["go_live"]
    rows = []
    for f in fires:
        i = np.searchsorted(ts, f["ts"].value, side="right") - 1
        if i < 0:
            continue
        j = np.searchsorted(ts, ts[i] + WINDOW_NS, side="right")
        if j <= i + 1:
            continue
        d = f["dir"]
        sl = slice(i + 1, j)
        ref = cl[i]
        mfe = float((hi[sl].max() - ref) if d == 1 else (ref - lo[sl].min()))
        mae = float((ref - lo[sl].min()) if d == 1 else (hi[sl].max() - ref))
        k_mfe = (int(np.argmax(hi[sl])) if d == 1
                 else int(np.argmin(lo[sl]))) + 1
        net = float((cl[j - 1] - ref) * d)
        row = {"name": f["name"], "dir": d, "ts": f["ts"].value,
               "window": ("backtest" if f["ts"] < boundary else
                          "forward" if f["ts"] >= gl else None),
               "session": session_of(f["ts"]),
               "mfe": mfe, "mae": mae, "t_mfe_min": k_mfe, "net": net}
        for cls, stream in narr.items():
            t = _first_opposing(stream, ts[i], ts[i] + WINDOW_NS, d)
            row[cls] = None if t is None else round((t - ts[i]) / 60e9, 1)
        rows.append(row)
    rows = [r for r in rows if r["window"]]
    out = {"instrument": instr,
           "status": ("provisional" if instr in PROVISIONAL_INSTRS
                      else "canonical"),
           "profiles": {}, "narrative_cut": {}}
    names = sorted({r["name"] for r in rows})
    for w in ("backtest", "forward"):
        for name in names:
            sel = [r for r in rows if r["window"] == w and r["name"] == name]
            if not sel:
                continue
            prof = {"whole": {
                "mfe": _dist([r["mfe"] for r in sel]),
                "mae": _dist([r["mae"] for r in sel]),
                "t_mfe_min": _dist([r["t_mfe_min"] for r in sel])}}
            for sess in sorted({r["session"] for r in sel}):
                ss = [r for r in sel if r["session"] == sess]
                prof[sess] = {"mfe": _dist([r["mfe"] for r in ss]),
                              "mae": _dist([r["mae"] for r in ss]),
                              "t_mfe_min": _dist([r["t_mfe_min"]
                                                  for r in ss])}
            out["profiles"].setdefault(w, {})[name] = prof
        # (b) the conditional cut, per class, pooled across hypotheses
        cut = {}
        selw = [r for r in rows if r["window"] == w]
        for cls in ("opposing_structural_core", "trend_flip",
                    "opposing_signal_fire"):
            with_ = [r for r in selw if r[cls] is not None]
            without = [r for r in selw if r[cls] is None]
            early = [r for r in with_ if r[cls] <= 30.0]
            late = [r for r in with_ if r[cls] > 30.0]

            def adverse(g):
                return (round(100 * sum(1 for r in g if r["net"] < 0)
                              / len(g), 1) if g else None)
            cut[cls] = {
                "with": {"n": len(with_), "adverse_pct": adverse(with_),
                         "mfe_median": _dist([r["mfe"] for r in with_]),
                         "first_occurrence_min_median": (round(float(
                             np.median([r[cls] for r in with_])), 1)
                             if with_ else None)},
                "without": {"n": len(without),
                            "adverse_pct": adverse(without),
                            "mfe_median": _dist([r["mfe"]
                                                 for r in without])},
                "early_le30min": {"n": len(early),
                                  "adverse_pct": adverse(early)},
                "late_gt30min": {"n": len(late),
                                 "adverse_pct": adverse(late)},
            }
        out["narrative_cut"][w] = cut
    return out


def _emit(results, head):
    L = ["# Excursion Profiles (GENERATED by backtest.excursions)", "",
         f"Engine `{head[:9]}` — OBSERVATIONAL, pre-registered (register "
         "42 item 7). PURPOSE: the principled input to the v1 "
         "recipe-values discussion — management style derived per "
         "hypothesis from measured excursion shape, not guessed; no "
         "recipe changes flow from this without operator ratification. "
         "MFE/MAE measured over the registered 60-min move window from "
         "the fire bar's close; counts everywhere; sealed/lockbox "
         "excluded.", ""]
    for res in results:
        inst = res["instrument"]
        L += [f"## {inst} ({res['status'].upper()})"]
        if res["status"] == "provisional":
            L += [f"> {PROVISIONAL_STAMP}"]
        L.append("")
        for w in ("backtest", "forward"):
            profs = res["profiles"].get(w, {})
            if profs:
                L += [f"### {inst} / {w} — MFE / MAE / time-to-MFE "
                      f"(whole-window)",
                      "",
                      "| H | n | MFE med | MFE p75 | MFE p90 "
                      "| MAE med | MAE p75 | MAE p90 | t-MFE med (min) |",
                      "|---|---|---|---|---|---|---|---|---|"]
                for name, prof in sorted(profs.items()):
                    p = prof["whole"]
                    if not p["mfe"]:
                        continue
                    L.append(
                        f"| {name} | {p['mfe']['n']} "
                        f"| {p['mfe']['median']} | {p['mfe']['p75']} "
                        f"| {p['mfe']['p90']} "
                        f"| {p['mae']['median']} | {p['mae']['p75']} "
                        f"| {p['mae']['p90']} "
                        f"| {p['t_mfe_min']['median']} |")
                L.append("")
            cut = res["narrative_cut"].get(w)
            if cut:
                L += [f"### {inst} / {w} — narrative-conditional cut "
                      f"(THE QUESTION: do opposing events during a hold "
                      f"predict adverse resolution?)", "",
                      "| class | with: n / adverse% / MFE med / first-min "
                      "| without: n / adverse% / MFE med | early<=30: "
                      "n/adv% | late>30: n/adv% |",
                      "|---|---|---|---|---|"]
                for cls, v in cut.items():
                    wi, wo = v["with"], v["without"]
                    L.append(
                        f"| {cls} | {wi['n']} / {wi['adverse_pct']}% / "
                        f"{wi['mfe_median']['median'] if wi['mfe_median'] else '—'} / "
                        f"{wi['first_occurrence_min_median']} "
                        f"| {wo['n']} / {wo['adverse_pct']}% / "
                        f"{wo['mfe_median']['median'] if wo['mfe_median'] else '—'} "
                        f"| {v['early_le30min']['n']}/"
                        f"{v['early_le30min']['adverse_pct']}% "
                        f"| {v['late_gt30min']['n']}/"
                        f"{v['late_gt30min']['adverse_pct']}% |")
                L.append("")
    L += ["---", "", "Per-session distributions in "
          "excursion_profiles.json (same run)."]
    with open(os.path.join(OUT, "excursion_profiles.md"), "w") as f:
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
        print(f"# excursions: {instr} ...", file=sys.stderr)
        results.append(run_instrument(instr))
    art = {"STAMP": ("OBSERVATIONAL excursion-profile study — "
                     "pre-registered; never validation"),
           "engine_commit": head, "results": results}
    with open(os.path.join(OUT, "excursion_profiles.json"), "w") as f:
        json.dump(art, f, indent=2, default=str)
    _emit(results, head)
    print(f"OBSERVATIONAL excursions -> {OUT}/excursion_profiles.md")


if __name__ == "__main__":
    main()
