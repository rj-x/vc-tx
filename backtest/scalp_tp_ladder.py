"""Scalp TP ladder (register 106; pre-registered prereg_scalp_tp_ladder,
counted 2026-08-30). REFINEMENT PROGRAM EXTENSION — measurement only;
v0 (the registered scalp arms) UNTOUCHED.

The scalp arms' journal fires (reconstructed as in register 103: fire =
open_ts - 1M; the refined arm's rows carry the transformed entry;
ex-lockbox) RE-SIMULATED with the identical recipe engine under target
in TP_RUNGS x ATR(15M) — the SAME haircut convention (register 94's
one-tick atr_haircut), the SAME disaster stop, the SAME EOD-flat;
INCUMBENT_TP is the reference and its re-simulation reconciles to the
journal (printed per leg). Per rung x instrument x arm x window: reach
rate, net (context), median-per-trade, win rate, spread-as-share-of-win,
weekly consistency, the tail-carry check — the consistency statistics
of the register-105 ruling, computed by the WATCH page's own cell_stats
so the ratified cap and week rule apply verbatim. Baselines: B-RANDOM
members under the identical rungs (member bands per statistic). THE
REACH-DECAY CURVE — P(touch) by rung — prints per leg per arm.

RANKING per register 105: consistency statistics only. A leg CLEARS a
rung when its forward win rate AND median both sit above the member
band's max at that rung, both at or above the incumbent's, and the cell
is not tail-carried; a candidate needs >= CAND_MIN_LEGS of 4 forward
legs. SINGLE-LEG OPTIMA never go straight to rules: they are handed to
the per-market WATCH page (watch_handoff in the JSON) wearing a
SELECTION-AWARE null — each member's best-over-rungs statistic is the
best fake the ladder field can manufacture; the optimum's percentile
against that distribution prints beside it. Any surviving rung proposes
through the front door BESIDE the register-101 v1 stop derivation — one
geometry package, one ratification; nothing registers here. Twin-run
pinned (tests/test_scalp_tp_ladder.py). Weekly under Part C.
"""

import argparse
import copy
import json
import os
import subprocess
import sys

import numpy as np
import pandas as pd

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "scripts"))

from engine.store_loader import in_lockbox_span, lockbox_boundary, zones
from backtest.recipes import (RECIPE_SET_VERSION, RECIPE_SETS,
                              _spread_median, build_env, simulate)
from backtest.scoreboard import _replay, make_cfg
from backtest.signal_points import baseline_fires
from backtest.scalp_risk_grid import (ARMS, INSTRUMENTS, REACH_REASONS,
                                      fires_from_rows, journal_rows)
from backtest.per_market_watch import cell_stats

OUT = os.path.join(ROOT, "reports", "scoreboard")

TP_RUNGS = (0.75, 1.0, 1.5)            # order-stated
INCUMBENT_TP = 0.5                     # register 94's target
CAND_MIN_LEGS = 3                      # the >= 3-of-4 rule
WINDOWS = ("backtest", "forward")


def with_target(recipe, k):
    """The scalp recipe with its target multiple re-rung; haircut, stop,
    and everything else untouched."""
    r = copy.deepcopy(recipe)
    for st in r["stages"]:
        t = st.get("target")
        if t and t[0] == "atr_haircut":
            st["target"] = (t[0], k, t[2], t[3])
    return r


def ladder_rows(trades, win):
    """simulate() trades -> the WATCH page's row shape, per window."""
    out = {w: [] for w in WINDOWS}
    for t in trades:
        w = win(t["entry_ts"])
        if w is None:
            continue
        ts = pd.Timestamp(t["entry_ts"])
        out[w].append({"pts": float(t["pts"]), "reason": t["reason"],
                       "week": "%d-W%02d" % ts.isocalendar()[:2]})
    return out


def ladder_cell(rows, spread):
    """Consistency statistics (register 105, via cell_stats) + reach
    rate + spread-as-share-of-win for one rung x arm x window."""
    if not rows:
        return {"n": 0}
    s = cell_stats(rows)
    reach = float(np.mean([r["reason"] in REACH_REASONS for r in rows]))
    wins = np.array([r["pts"] for r in rows if r["pts"] > 0])
    # spread share of the median winner's GROSS move (pts + spread):
    # the cost the rung has to clear — implementer-proposed, FLAGGED
    share = (round(float(spread / (np.median(wins) + spread)), 3)
             if len(wins) and spread is not None else None)
    return {**s, "reach_rate": round(reach, 3),
            "spread_share_of_win": share}


def band(values):
    v = [x for x in values if x is not None]
    if not v:
        return None
    return {"members": len(v), "median": round(float(np.median(v)), 3),
            "min": round(float(min(v)), 3), "max": round(float(max(v)), 3)}


def run_instrument(instr, jr):
    cfg = make_cfg({"session_model.extended_hours": True,
                    "session_model.ladder": True,
                    "debug.structure": True})
    engine, bars, _ = _replay(cfg, instr)
    env = build_env(instr, cfg, bars)
    spread = _spread_median(instr)
    members = baseline_fires(env, engine.narrative.events)["B-RANDOM"]
    boundary, gl = lockbox_boundary(), zones()["go_live"]

    def win(t):
        t = pd.Timestamp(t)
        return ("backtest" if t < boundary else
                "forward" if t >= gl else None)

    def sim(fires, recipe):
        return [t for t in simulate(fires, env, recipe, spread)
                if not in_lockbox_span(t["entry_ts"])]

    rungs = (INCUMBENT_TP,) + TP_RUNGS
    out = {"spread": spread, "ladder": {}, "floors": {},
           "member_best": {}, "reconciliation": {}, "reach_decay": {}}
    for arm in ARMS:
        rows = jr.get((instr, arm), [])
        if not rows:
            continue
        recipe = RECIPE_SETS[RECIPE_SET_VERSION][arm]
        fires = fires_from_rows(rows)
        per_rung = {}
        for k in rungs:
            trades = sim(fires, with_target(recipe, k))
            if k == INCUMBENT_TP:
                jmap = {r["open_ts"].value: r["pts"] for r in rows}
                smap = {pd.Timestamp(t["entry_ts"]).value: float(t["pts"])
                        for t in trades}
                diffs = [abs(smap[x] - jmap[x]) for x in jmap if x in smap]
                out["reconciliation"][arm] = {
                    "journal_rows": len(rows), "resimulated": len(diffs),
                    "max_abs_pts_diff": (round(max(diffs), 3) if diffs
                                         else None),
                    "exact_matches": sum(1 for d in diffs if d < 1e-6)}
            per_rung[k] = ladder_rows(trades, win)
            for w in WINDOWS:
                out["ladder"][f"{arm}|{w}|{k:g}"] = ladder_cell(
                    per_rung[k][w], spread)
        out["reach_decay"][arm] = {
            w: {f"{k:g}": out["ladder"][f"{arm}|{w}|{k:g}"].get("reach_rate")
                for k in rungs} for w in WINDOWS}
        # floors: members under the identical rungs; and each member's
        # best-over-rungs (the selection-aware null for single-leg optima)
        fl = {}
        best = {w: {"win_rate": [], "median": []} for w in WINDOWS}
        for mf in members:
            m_cells = {}
            for k in rungs:
                mt = ladder_rows(sim(mf, with_target(recipe, k)), win)
                for w in WINDOWS:
                    c = ladder_cell(mt[w], spread)
                    m_cells[(w, k)] = c
                    for stat in ("win_rate", "median", "reach_rate"):
                        fl.setdefault(f"{arm}|{w}|{k:g}|{stat}", []).append(
                            c.get(stat))
            for w in WINDOWS:
                for stat in ("win_rate", "median"):
                    vals = [m_cells[(w, k)].get(stat) for k in rungs
                            if m_cells[(w, k)].get("n", 0) >= 10
                            and not m_cells[(w, k)].get("tail_carried", True)]
                    best[w][stat].append(max(vals) if vals else None)
        out["floors"].update({k: band(v) for k, v in fl.items()})
        out["member_best"].update(
            {f"{arm}|{w}|{stat}": [x for x in best[w][stat] if x is not None]
             for w in WINDOWS for stat in ("win_rate", "median")})
    return out


def leg_clears(cell, inc, fl_win, fl_med):
    """Forward leg clears the rung: win rate AND median above the member
    band max at that rung, both >= the incumbent's, not tail-carried."""
    if cell.get("n", 0) < 10 or cell.get("tail_carried", True) \
            or not fl_win or not fl_med or inc.get("n", 0) < 10:
        return False
    return bool(cell["win_rate"] > fl_win["max"]
                and cell["median"] > fl_med["max"]
                and cell["win_rate"] >= inc["win_rate"]
                and cell["median"] >= inc["median"])


def candidates(results):
    out = {}
    for arm in ARMS:
        for k in TP_RUNGS:
            legs = {}
            for instr, res in results.items():
                key = f"{arm}|forward|{k:g}"
                c = res["ladder"].get(key)
                inc = res["ladder"].get(f"{arm}|forward|{INCUMBENT_TP:g}")
                if not c or c.get("n", 0) == 0 or not inc:
                    continue
                fw = res["floors"].get(f"{key}|win_rate")
                fm = res["floors"].get(f"{key}|median")
                legs[instr] = {"win_rate": c["win_rate"], "median": c["median"],
                               "band_win_max": fw["max"] if fw else None,
                               "band_median_max": fm["max"] if fm else None,
                               "tail_carried": c["tail_carried"],
                               "clears": leg_clears(c, inc, fw, fm)}
            cl = sorted(i for i, v in legs.items() if v["clears"])
            grade = ("candidate" if len(cl) >= CAND_MIN_LEGS
                     else "glint" if cl else "none")
            out[f"{arm}|{k:g}"] = {"legs": legs, "clearing": cl,
                                   "grade": grade}
    return out


def watch_handoff(results):
    """Single-leg optima -> the per-market WATCH page: per leg x arm, the
    forward rung with the best (win rate, median) among rankable cells,
    wearing its percentile against the members' best-over-rungs."""
    out = []
    for instr, res in results.items():
        for arm in ARMS:
            cells = []
            for k in (INCUMBENT_TP,) + TP_RUNGS:
                c = res["ladder"].get(f"{arm}|forward|{k:g}")
                if c and c.get("n", 0) >= 10 and not c["tail_carried"]:
                    cells.append((k, c))
            if not cells:
                continue
            k, c = max(cells, key=lambda x: (x[1]["win_rate"], x[1]["median"]))
            nb_w = np.array(res["member_best"].get(f"{arm}|forward|win_rate",
                                                   []), dtype=float)
            nb_m = np.array(res["member_best"].get(f"{arm}|forward|median",
                                                   []), dtype=float)
            out.append({"instrument": instr, "arm": arm, "rung": k,
                        "n": c["n"], "win_rate": c["win_rate"],
                        "median": c["median"],
                        "weeks": f"{c['weeks_pos']}/{c['weeks_meas']}",
                        "sel_pct_win": (round(100 * float(np.mean(nb_w < c["win_rate"])), 1)
                                        if len(nb_w) else None),
                        "sel_pct_median": (round(100 * float(np.mean(nb_m < c["median"])), 1)
                                           if len(nb_m) else None),
                        "beats_field_null": bool(
                            len(nb_w) and len(nb_m)
                            and c["win_rate"] > np.percentile(nb_w, 95)
                            and c["median"] > np.percentile(nb_m, 95)),
                        "is_incumbent": k == INCUMBENT_TP})
    return out


def _emit(art, head):
    n_cells = sum(len(r["ladder"]) for r in art["results"].values())
    L = ["# Scalp TP Ladder (GENERATED by backtest.scalp_tp_ladder)", "",
         "Terms: [docs/GLOSSARY.md](../../docs/GLOSSARY.md).", "",
         f"Engine `{head[:9]}` — OBSERVATIONAL, pre-registered "
         "(prereg_scalp_tp_ladder, register 106). Refinement-program "
         "extension; v0 UNTOUCHED; measurement only. The arms' own fires "
         f"re-simulated under target {{{INCUMBENT_TP:g} (incumbent), "
         f"{', '.join(f'{k:g}' for k in TP_RUNGS)}}}xATR(15M) — same "
         "one-tick haircut (register 94), same disaster stop, same EOD-"
         "flat; the incumbent reconciles to the journal (printed per leg). "
         f"FIELD HONESTY: {n_cells} cells (rungs x legs x arms x windows). "
         "STATISTIC SHAPES (74-B): per cell the register-105 consistency "
         "statistics — median-per-trade, win rate, weekly consistency, the "
         "gross-profit tail-carry cap — against B-RANDOM member bands under "
         "the identical rungs; reach rate and net descriptive (net = "
         "context only); the reach-decay curve is descriptive. A leg "
         "clears a rung when win rate AND median exceed the member band's "
         "max, both >= the incumbent's, not tail-carried; a candidate needs "
         f">= {CAND_MIN_LEGS} of 4 forward legs. Single-leg optima go to "
         "per_market_watch.md wearing a selection-aware null (members' "
         "best-over-rungs), never straight to rules. Survivors propose "
         "BESIDE the register-101 v1 stop derivation — one geometry "
         "package, one ratification. Fill model: OPTIMISTIC target fill "
         "with the declared haircut (register 94); spread charged = the "
         "instrument's median cash spread; spread-as-share-of-win = spread "
         "/ the median winner's gross move (implementer-proposed, FLAGGED). "
         "Ex-lockbox.", ""]
    for instr, res in sorted(art["results"].items()):
        L += [f"## {instr} (spread charged {res['spread']} pts/trade)", "",
              "Reconciliation (incumbent re-simulation vs journal): "
              + "; ".join(f"{arm}: {v['exact_matches']}/{v['resimulated']} "
                          f"exact, max |Δ| {v['max_abs_pts_diff']}"
                          for arm, v in res["reconciliation"].items()), "",
              "### Ladder (consistency statistics; floors = member band "
              "max at the same rung)", "",
              "| arm | window | target xATR | n | reach | win | median "
              "| +weeks/meas | spread/win | max-win share | net (context) "
              "| member max win / median |",
              "|---|---|---|---|---|---|---|---|---|---|---|---|"]
        for k, c in res["ladder"].items():
            arm, w, rung = k.split("|")
            if c.get("n", 0) == 0:
                L.append(f"| {arm} | {w} | {rung} | 0 | — | — | — | — | — "
                         "| — | — | — |")
                continue
            fw = res["floors"].get(f"{k}|win_rate") or {}
            fm = res["floors"].get(f"{k}|median") or {}
            L.append(f"| {arm} | {w} | {rung} | {c['n']} "
                     f"| {100 * c['reach_rate']:.0f}% "
                     f"| {100 * c['win_rate']:.0f}% | {c['median']:+.2f} "
                     f"| {c['weeks_pos']}/{c['weeks_meas']} "
                     f"| {c['spread_share_of_win']} "
                     f"| {c['max_win_share'] if c['max_win_share'] is not None else '—'}"
                     f"{' TAIL' if c['tail_carried'] else ''} "
                     f"| {c['net_pts']} | {fw.get('max', '—')} / "
                     f"{fm.get('max', '—')} |")
        L += ["", "### Reach-decay curve — P(touch) by rung", "",
              "| arm | window | " + " | ".join(
                  f"{k:g}x" for k in (INCUMBENT_TP,) + TP_RUNGS) + " |",
              "|---|---|" + "---|" * (1 + len(TP_RUNGS))]
        for arm, per in res["reach_decay"].items():
            for w, d in per.items():
                L.append(f"| {arm} | {w} | " + " | ".join(
                    f"{100 * v:.0f}%" if v is not None else "—"
                    for v in d.values()) + " |")
        L.append("")
    L += ["## Candidates (>= 3-of-4 forward legs clearing) and glints", "",
          "| arm | target xATR | grade | clearing legs |", "|---|---|---|---|"]
    if any(d["grade"] != "none" for d in art["candidates"].values()):
        for k, d in sorted(art["candidates"].items()):
            if d["grade"] != "none":
                arm, rung = k.split("|")
                L.append(f"| {arm} | {rung} | {d['grade']} "
                         f"| {', '.join(d['clearing'])} |")
    else:
        L.append("| (no rung clears on any forward leg) | | | |")
    L += ["", "## WATCH hand-off — single-leg forward optima (selection-"
          "aware null = members' best-over-rungs; printed again on "
          "per_market_watch.md; never rules)", "",
          "| instrument | arm | best rung | n | win | median | +weeks/meas "
          "| sel-pct win / median | beats field null |",
          "|---|---|---|---|---|---|---|---|---|"]
    for h in art["watch_handoff"]:
        L.append(f"| {h['instrument']} | {h['arm']} | {h['rung']:g}x"
                 f"{' (incumbent)' if h['is_incumbent'] else ''} | {h['n']} "
                 f"| {100 * h['win_rate']:.0f}% | {h['median']:+.2f} "
                 f"| {h['weeks']} | {h['sel_pct_win']} / {h['sel_pct_median']} "
                 f"| {'YES' if h['beats_field_null'] else 'no'} |")
    if not art["watch_handoff"]:
        L.append("| (no rankable forward cell) | | | | | | | | |")
    L.append("")
    with open(os.path.join(OUT, "scalp_tp_ladder.md"), "w") as f:
        f.write("\n".join(L))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--instr", nargs="*", default=list(INSTRUMENTS))
    a = ap.parse_args()
    head = subprocess.run(["git", "rev-parse", "HEAD"], cwd=ROOT,
                          capture_output=True, text=True).stdout.strip()
    jr = journal_rows()
    results = {}
    for instr in a.instr:
        print(f"# scalp_tp_ladder: {instr} ...", file=sys.stderr)
        results[instr] = run_instrument(instr, jr)
    art = {"STAMP": ("OBSERVATIONAL scalp TP ladder — measurement only; "
                     "v0 untouched; survivors propose beside the "
                     "register-101 stop derivation as one geometry "
                     "package via the front door; never validation"),
           "engine_commit": head, "tp_rungs": list(TP_RUNGS),
           "incumbent_tp": INCUMBENT_TP, "results": results}
    art["candidates"] = candidates(results)
    art["watch_handoff"] = watch_handoff(results)
    with open(os.path.join(OUT, "scalp_tp_ladder.json"), "w") as f:
        json.dump(art, f, indent=2, default=str)
    _emit(art, head)
    n_c = sum(1 for d in art["candidates"].values()
              if d["grade"] == "candidate")
    print(f"OBSERVATIONAL scalp TP ladder -> {OUT}/scalp_tp_ladder.md "
          f"({n_c} candidates; {len(art['watch_handoff'])} WATCH hand-offs)")


if __name__ == "__main__":
    main()
