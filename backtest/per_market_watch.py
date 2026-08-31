"""Per-market config WATCH page (register 105 item 5; pre-registered
prereg_per_market_watch, counted 2026-08-29). A MAP of where per-market
specialization would go — NEVER a settings page: cells graduate only by
walking the register-105 per-market track (mechanism sentence in the
operator's pen; selection-aware luck budget; own forward clock at
elevated n). Measurement only; nothing registers from this page.

THE DOCTRINE (register 105): markets are distinct populations with
distinct participant psychology; the register specializes claims, never
defaults. The >= 3-of-4-leg replication bar stays the luck filter for
FIELD screens; this page is the per-market complement, and it prices
its own selection.

THE IN-MARKET CONFIG FIELD, per instrument x zone: management variant x
session x slot (slot = the event-clock tags open15 / close15 / news15,
precedence in that order, else none — register 104's windows reused;
the stop-rung axis is NOT re-simulated here: each variant carries its
registered stop, and the risk grid (register 103) remains the stop
ladder's home — a stated coverage limitation, not a hidden default).

DISTINCT PATHS (register 113): co-fired identical price paths — the
same open timestamp, direction and points reached through different
sentences — count ONCE for evidence purposes: every cell statistic
(median, win rate, weekly counts, tail-carry, net) computes on
distinct paths; n prints as rows (distinct); measurability and the
track floor read on the distinct count; the selection-null is
unchanged in method and recomputes on the corrected counts.

CONSISTENCY RULING (register 105 item 3, operator: consistency over
magnitude): cells rank and print on consistency statistics only —
median-per-trade, win rate, weekly-consistency count (positive ISO weeks
/ measurable weeks, a week measurable at >= WEEK_MIN_N rows — RATIFIED
2026-08-29 with the slot precedence and the 45-row track floor) — with a
TAIL-CARRY CAP (register 105 follow-through, amended 2026-08-29 —
the drafted |net| denominator was degenerate near zero): any cell whose
single largest WINNING trade exceeds TAIL_CARRY_SHARE of GROSS WINNING
points is tail-carried and non-candidate at any n (register 62's
demotion extended). A cell with no winning trade has no gross to carry
and is tail-carried by convention. Net points print as context only.

SELECTION-AWARE NULL (item 2b): the cell's competitor is the BEST FAKE
its own market's field can manufacture — per instrument x zone, the
config labels are permuted across the market's rows (cell sizes kept),
the best win rate and best median across all cells at n >= MIN_CELL_N
are recorded per seed (NULL_SEEDS pinned), and every observed cell wears
its percentile against that best-of-field distribution on the SAME
statistic it is ranked by. "Most consistent in-market" must beat the
most consistent fake the field produces. Caveat declared: the journal's
variants share fires (rows are correlated across variants), so the
permutation is a label shuffle over correlated rows — conservative for
variant-axis cells only in the sense that it preserves cell sizes; the
elevated forward floor (item 2c) is the second guard.

CANDIDATE POOL (item 4): seeded from existing structure with EMPTY
mechanism-sentence slots — nothing advances without the operator's pen.
Ex-lockbox; sealed untouched; twin-run pinned
(tests/test_per_market_watch.py); weekly under Part C.

CENSUS CLEARS (register 108): the bar-persistence census's headline
cells (net reach 0.5xATR@5) that clear their matched floor's FULL
member range at n >= CENSUS_MIN_N route here programmatically (the
register-99 ger40fut S0-H19 cell was hand-seeded; this is the general
route), each wearing a SELECTION-NULL of the same shape as the config
field's: per instrument x window, the signal labels are permuted across
the census fires (n per signal kept), the best net reach among
measurable signals recorded per seed, and every clearing cell wears its
percentile against that best-of-field distribution. Listed, never
rules; a mechanism sentence is still the operator's pen.
"""

import argparse
import csv
import json
import os
import subprocess
import sys

import numpy as np
import pandas as pd

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "scripts"))

from engine.store_loader import in_lockbox_span, lockbox_boundary, zones
from backtest.event_clock import load_calendar, tag_row

OUT = os.path.join(ROOT, "reports", "scoreboard")
TRADES_CSV = os.path.join(ROOT, "reports", "trades.csv")
CENSUS_FIRES_CSV = os.path.join(OUT, "bar_persistence_fires.csv")
CENSUS_JSON = os.path.join(OUT, "bar_persistence.json")
CENSUS_MIN_N = 25               # register 108: a census clear is
                                # measurable at n >= 25 (the census's
                                # own CENSUS_MIN_N, mirrored)

INSTRUMENTS = ("uk100fut", "ger40fut", "nas100fut", "us30fut")
SLOT_ORDER = ("open15", "close15", "news15")   # precedence; else "none"
MIN_CELL_N = 10                 # the matrix convention
WEEK_MIN_N = 3                  # a week measurable at >= 3 rows (RATIFIED 08-29)
TAIL_CARRY_SHARE = 0.25         # one WIN > 25% of gross winning points
NULL_SHUFFLES = 100
NULL_SEEDS = tuple(range(NULL_SHUFFLES))
TOP_K = 5                       # rows printed per statistic per market
POOLED_Q_MIN_N = 30             # the pooled-question forward floor
TRACK_N_MULT = 1.5              # item 2c: >= 1.5x the pooled minimum
TRACK_MIN_N = int(POOLED_Q_MIN_N * TRACK_N_MULT)   # 45, RATIFIED 08-29; proposed at any mint

# item 4 — the seeded pool; mechanism slots EMPTY until the operator's pen
CANDIDATE_POOL = (
    {"cell": "R-NEXIT-EARLY x open-window",
     "legs": "ger40fut, nas100fut",
     "source": "event_clock.md glint list (register 104 first emission: "
               "open15 glint on ger40fut + nas100fut, recurring)",
     "mechanism": ""},
    {"cell": "us30fut x open-window strength",
     "legs": "us30fut",
     "source": "the ISO-week-32 refutation cell (operator + reviewer "
               "sitting 2026-08-29, chat-side; NOT located in a repo "
               "artifact under that name — nearest artifact: "
               "event_clock.md us30fut open15/open30 cells)",
     "mechanism": ""},
    {"cell": "ger40fut S0-H" + str(19) + " reach",
     "legs": "ger40fut",
     "source": "register 99: forward net reach 21.4% vs floor max 18.7 "
               "(n=126), the standing WATCH cell",
     "mechanism": ""},
)


def journal_rows():
    """Ex-lockbox journal rows with zone, session, and the event-clock
    slot tag (register 104's tagger reused; news = native or cross)."""
    boundary, gl = lockbox_boundary(), zones()["go_live"]
    rel, span = load_calendar()
    out = []
    for r in csv.DictReader(l for l in open(TRADES_CSV) if not l.startswith("#")):
        if in_lockbox_span(r["open_ts"]):
            continue
        t = pd.Timestamp(r["open_ts"])
        w = "backtest" if t < boundary else "forward" if t >= gl else None
        if w is None or r["instrument"] not in INSTRUMENTS:
            continue
        tags, _cov = tag_row(r, rel, span)
        out.append({"instrument": r["instrument"], "variant": r["variant"],
                    "session": r["session"], "window": w,
                    "slot": slot_of(tags), "pts": float(r["points"]),
                    "week": "%d-W%02d" % t.isocalendar()[:2],
                    # register 113: co-fired identical price paths count
                    # once for evidence — the path key
                    "path": f"{r['open_ts']}|{r['direction']}|{r['points']}"})
    return out


def slot_of(tags):
    for s in SLOT_ORDER:
        if s.startswith("news"):
            if tags.get(s + ":native") or tags.get(s + ":cross"):
                return s
        elif tags.get(s):
            return s
    return "none"


def distinct_paths(rows):
    """Register 113: co-fired identical price paths count once for
    evidence purposes — first occurrence kept per path key; rows
    without a path key (per-fire simulations, e.g. the TP ladder's)
    are all distinct by construction."""
    seen = set()
    out = []
    for r in rows:
        p = r.get("path")
        if p is not None:
            if p in seen:
                continue
            seen.add(p)
        out.append(r)
    return out


def cell_stats(rows):
    """Consistency statistics + the tail-carry check for one cell.
    Register 113: ALL statistics compute on distinct price paths
    (median, win rate, weekly counts, tail-carry, net); n keeps the
    raw row count, n_distinct the evidence count."""
    ded = distinct_paths(rows)
    pts = np.array([r["pts"] for r in ded], dtype=float)
    net = float(pts.sum())
    weeks = {}
    for r in ded:
        weeks.setdefault(r["week"], []).append(r["pts"])
    meas = {w: v for w, v in weeks.items() if len(v) >= WEEK_MIN_N}
    pos = sum(1 for v in meas.values() if sum(v) > 0)
    wins = pts[pts > 0]
    gross_win = float(wins.sum())
    share = (float(wins.max()) / gross_win) if gross_win else None
    return {"n": int(len(rows)), "n_distinct": int(len(ded)),
            "median": round(float(np.median(pts)), 2) if len(pts) else None,
            "win_rate": round(float((pts > 0).mean()), 3) if len(pts) else None,
            "weeks_pos": pos, "weeks_meas": len(meas),
            "net_pts": round(net, 1),
            "max_win_share": (round(share, 3) if share is not None
                                else None),
            "tail_carried": bool(share is None or share > TAIL_CARRY_SHARE)}


def build_field(rows):
    """(instr, window) -> {(variant, session, slot): stats}."""
    grouped = {}
    for r in rows:
        grouped.setdefault((r["instrument"], r["window"]), {}) \
               .setdefault((r["variant"], r["session"], r["slot"]), []) \
               .append(r)
    return {k: {c: cell_stats(v) for c, v in cells.items()}
            for k, cells in grouped.items()}


def best_of_field(cells):
    """The best win rate and best median across measurable, non-tail-
    carried cells (the ranking population)."""
    ok = [s for s in cells.values()
          if s["n_distinct"] >= MIN_CELL_N and not s["tail_carried"]]
    if not ok:
        return None, None
    return (max(s["win_rate"] for s in ok), max(s["median"] for s in ok))


def selection_null(rows_market):
    """Label permutation over one market x zone: the config label of
    every row is shuffled (cell sizes kept, week stamps travel with the
    row), the best-of-field win rate and median recorded per seed."""
    labels = [(r["variant"], r["session"], r["slot"]) for r in rows_market]
    best_wr, best_md = [], []
    for seed in NULL_SEEDS:
        rs = np.random.RandomState(seed)
        perm = rs.permutation(len(labels))
        cells = {}
        for i, j in enumerate(perm):
            cells.setdefault(labels[j], []).append(rows_market[i])
        wr, md = best_of_field({c: cell_stats(v) for c, v in cells.items()})
        # a seed with no rankable cell is MISSING, never a low value
        best_wr.append(wr if wr is not None else np.nan)
        best_md.append(md if md is not None else np.nan)
    return np.array(best_wr, dtype=float), np.array(best_md, dtype=float)


def percentile_vs(null, value):
    """Share of the VALID best-of-field null strictly below the value
    (None when no seed produced a rankable cell)."""
    valid = null[~np.isnan(null)]
    if not len(valid):
        return None
    return round(100 * float(np.mean(valid < value)), 1)


def null_p95(null):
    valid = null[~np.isnan(null)]
    return float(np.percentile(valid, 95)) if len(valid) else np.inf


def run():
    rows = journal_rows()
    field = build_field(rows)
    by_market = {}
    for r in rows:
        by_market.setdefault((r["instrument"], r["window"]), []).append(r)
    markets = {}
    for key in sorted(field):
        instr, w = key
        cells = field[key]
        nb_wr, nb_md = selection_null(by_market[key])
        table = []
        for (var, sess, slot), s in cells.items():
            if s["n_distinct"] < MIN_CELL_N:
                continue
            table.append({"variant": var, "session": sess, "slot": slot,
                          **s,
                          "sel_pct_win": percentile_vs(nb_wr, s["win_rate"]),
                          "sel_pct_median": percentile_vs(nb_md, s["median"]),
                          "beats_field_null_win": bool(
                              s["win_rate"] > null_p95(nb_wr)),
                          "beats_field_null_median": bool(
                              s["median"] > null_p95(nb_md))})
        rankable = [c for c in table if not c["tail_carried"]]
        axes = {}
        for axis in ("variant", "session", "slot"):
            best = {}
            for c in rankable:
                lv = c[axis]
                if lv not in best or (c["win_rate"], c["median"]) > \
                        (best[lv]["win_rate"], best[lv]["median"]):
                    best[lv] = c
            axes[axis] = (max(best.values(),
                              key=lambda c: (c["win_rate"], c["median"]))
                          if best else None)
        markets["|".join(key)] = {
            "rows": len(by_market[key]),
            "field_cells": len(cells),
            "measurable_cells": len(table),
            "tail_carried_cells": sum(1 for c in table if c["tail_carried"]),
            "null_valid_seeds": int((~np.isnan(nb_wr)).sum()),
            "null_best_win_p95": round(null_p95(nb_wr), 3),
            "null_best_median_p95": round(null_p95(nb_md), 2),
            "top_by_win": sorted(rankable, key=lambda c: (-c["win_rate"],
                                                          -c["median"]))
            [:TOP_K],
            "top_by_median": sorted(rankable, key=lambda c: (-c["median"],
                                                             -c["win_rate"]))
            [:TOP_K],
            "top_by_weeks": sorted(rankable,
                                   key=lambda c: (-c["weeks_pos"],
                                                  -c["win_rate"]))[:TOP_K],
            "best_by_axis": axes,
            "cells": table}
    return {"journal_rows_ex_lockbox": len(rows),
            "field_dims": "variant x session x slot (stop axis: the "
                          "variant's registered stop; not re-simulated)",
            "track": {"min_forward_n": TRACK_MIN_N,
                      "pooled_min": POOLED_Q_MIN_N, "mult": TRACK_N_MULT,
                      "tail_carry_share": TAIL_CARRY_SHARE,
                      "week_min_n": WEEK_MIN_N},
            "candidate_pool": [dict(c) for c in CANDIDATE_POOL],
            "markets": markets}


def census_fires(path=CENSUS_FIRES_CSV):
    """(instrument, window) -> list of (signal, net_touch) from the
    census's row-level ledger (register 91); lockbox rows excluded by
    their zone tag."""
    out = {}
    if not os.path.exists(path):
        return out
    for r in csv.DictReader(open(path)):
        if r["zone"] not in ("backtest", "forward"):
            continue
        v = r["touched_0p5atr_5b_net_of_spread"]
        if v in ("", "None"):
            continue
        out.setdefault((r["instrument"], r["zone"]), []).append(
            (r["signal"], 1.0 if v in ("True", "1", "1.0") else 0.0))
    return out


def census_selection_null(fires, min_n=CENSUS_MIN_N):
    """Best-of-field net reach % per seed under signal-label
    permutation across one instrument x window's census fires (n per
    signal kept). NaN = no measurable signal that seed."""
    labels = [f[0] for f in fires]
    vals = np.array([f[1] for f in fires], dtype=float)
    out = []
    for seed in NULL_SEEDS:
        rs = np.random.RandomState(seed)
        perm = rs.permutation(len(labels))
        cells = {}
        for i, j in enumerate(perm):
            cells.setdefault(labels[j], []).append(vals[i])
        best = [100 * float(np.mean(v)) for v in cells.values()
                if len(v) >= min_n]
        out.append(max(best) if best else np.nan)
    return np.array(out, dtype=float)


def census_watch(census_json=CENSUS_JSON, fires_csv=CENSUS_FIRES_CSV):
    """Register 108: every census clear (full floor range) at n >=
    CENSUS_MIN_N, wearing its selection-null percentile; unmeasurable
    clears listed with their n-to-measurable and no null."""
    if not os.path.exists(census_json):
        return []
    bp = json.load(open(census_json))
    fires = census_fires(fires_csv)
    nulls = {}
    out = []
    for res in bp.get("results", []):
        instr = res["instrument"]
        for c in res.get("census_clears", []):
            key = (instr, c["window"])
            row = {"instrument": instr, **c,
                   "sel_pct": None, "null_p95": None,
                   "beats_field_null": False,
                   "null_valid_seeds": 0,
                   "n_to_measurable": max(0, CENSUS_MIN_N - c["n"])}
            if c["measurable"] and key in fires:
                if key not in nulls:
                    nulls[key] = census_selection_null(fires[key])
                nb = nulls[key]
                row["sel_pct"] = percentile_vs(nb, c["net_reach_pct"])
                p95 = null_p95(nb)
                row["null_p95"] = (round(p95, 1) if np.isfinite(p95)
                                   else None)
                row["beats_field_null"] = bool(c["net_reach_pct"] > p95)
                row["null_valid_seeds"] = int((~np.isnan(nb)).sum())
            out.append(row)
    return out


CENSUS_HDR = ("| instrument | signal | window | n | net reach % | floor "
              "[range] (members) | Δ vs range max | sel-pct | field null "
              "p95 | beats field null | status |",
              "|---|---|---|---|---|---|---|---|---|---|---|")


def census_row(c):
    lo, hi = c["floor_range"]
    st = ("WATCH" if c["measurable"] else
          f"unmeasurable (n<{CENSUS_MIN_N}; {c['n_to_measurable']} to go)")
    return (f"| {c['instrument']} | {c['signal']} | {c['window']} | {c['n']} "
            f"| {c['net_reach_pct']} | {c['floor']} [{lo}…{hi}] "
            f"({c['floor_members']}) | {c['delta_vs_range_max_pp']:+.1f}pp "
            f"| {c['sel_pct'] if c['sel_pct'] is not None else '—'} "
            f"| {c['null_p95'] if c['null_p95'] is not None else '—'} "
            f"| {'YES' if c['beats_field_null'] else 'no'} | {st} |")


def _row(c):
    return (f"| {c['variant']} | {c['session']} | {c['slot']} "
            f"| {c['n']} ({c['n_distinct']}) "
            f"| {c['median']:+.2f} | {100 * c['win_rate']:.0f}% "
            f"| {c['weeks_pos']}/{c['weeks_meas']} "
            f"| {c['sel_pct_win']} / {c['sel_pct_median']} "
            f"| {'YES' if c['beats_field_null_win'] else 'no'} / "
            f"{'YES' if c['beats_field_null_median'] else 'no'} "
            f"| {c['max_win_share']:.2f}"
            f"{' TAIL' if c['tail_carried'] else ''} | {c['net_pts']} |")


HDR = ("| variant | session | slot | n (distinct) | median | win | +weeks/meas "
       "| sel-pct win / median | beats field null win / median "
       "| max-win share of gross | net (context) |",
       "|---|---|---|---|---|---|---|---|---|---|---|")


def _emit(art, head):
    tr = art["track"]
    L = ["# Per-Market Config WATCH (GENERATED by backtest.per_market_watch)",
         "", "Terms: [docs/GLOSSARY.md](../../docs/GLOSSARY.md).", "",
         f"Engine `{head[:9]}` — OBSERVATIONAL, pre-registered "
         "(prereg_per_market_watch, register 105). A MAP of where "
         "per-market specialization would go — NEVER a settings page: "
         "cells graduate only by walking the per-market track (register "
         "105 item 2): (a) a written mechanism sentence, operator's pen; "
         "(b) a selection-aware luck budget against the market's whole "
         "config field; (c) its own forward clock at >= "
         f"{tr['min_forward_n']} forward rows ({tr['mult']}x the pooled "
         f"minimum {tr['pooled_min']}, proposed at mint). CONSISTENCY "
         "RULING: ranked and printed on consistency statistics only — "
         "median-per-trade, win rate, weekly-consistency count (positive "
         f"ISO weeks / weeks with >= {tr['week_min_n']} rows); TAIL-CARRY "
         f"CAP (amended, register 105 follow-through): one winning trade > "
         f"{100 * tr['tail_carry_share']:.0f}% of gross winning points = "
         "tail-carried, non-candidate at any n (register 62 extended); net "
         "points context only. STATISTIC SHAPES (74-B): every cell wears "
         "its SELECTION-NULL percentile — the share of "
         f"{NULL_SHUFFLES} label-permutation best-of-field values (pinned "
         "seeds) it beats, on the same statistic it is ranked by — and a "
         "YES only above the field's null p95 (the most consistent fake "
         f"the field manufactures). FIELD: {art['field_dims']}; measurable "
         f"= n >= {MIN_CELL_N}. Fill model: the journal's PESSIMISTIC rows "
         "(the scalp arms' optimistic target fill declared, register 94). "
         "Ex-lockbox. Nothing registers from this page.", ""]
    L += ["## Candidate pool (register 105 item 4) — mechanism slots "
          "await the operator's pen; nothing advances without it", "",
          "| cell | legs | source | mechanism sentence |",
          "|---|---|---|---|"]
    for c in art["candidate_pool"]:
        L.append(f"| {c['cell']} | {c['legs']} | {c['source']} "
                 f"| {c['mechanism'] or '(EMPTY — awaiting operator)'} |")
    for key, m in art["markets"].items():
        instr, w = key.split("|")
        L += ["", f"## {instr} — {w} ({m['rows']} rows; {m['field_cells']} "
              f"field cells, {m['measurable_cells']} measurable, "
              f"{m['tail_carried_cells']} tail-carried; field null p95 over "
              f"{m['null_valid_seeds']} valid seeds: best win "
              f"{100 * m['null_best_win_p95']:.0f}%, best median "
              f"{m['null_best_median_p95']:+.2f})", ""]
        for title, lst in (("Top by win rate", m["top_by_win"]),
                           ("Top by median-per-trade", m["top_by_median"]),
                           ("Top by weekly consistency", m["top_by_weeks"])):
            L += [f"### {title}", "", *HDR]
            L += [_row(c) for c in lst] or [
                "| (no measurable, non-tail-carried cell) | | | | | | | | | | |"]
            L.append("")
        L += ["### Best level per axis (by win rate, then median)", "",
              "| axis | level | session | slot | n | win | median "
              "| sel-pct win | beats field null |", "|---|---|---|---|---|---|---|---|---|"]
        for axis, c in m["best_by_axis"].items():
            if c is None:
                L.append(f"| {axis} | (none) | | | | | | | |")
                continue
            L.append(f"| {axis} | {c[axis]} | {c['session']} | {c['slot']} "
                     f"| {c['n']} ({c['n_distinct']}) "
                     f"| {100 * c['win_rate']:.0f}% "
                     f"| {c['median']:+.2f} | {c['sel_pct_win']} "
                     f"| {'YES' if c['beats_field_null_win'] else 'no'} |")
    from backtest.scalp_tp_ladder import HANDOFF_HDR, handoff_row
    hand = art.get("ladder_handoffs", [])
    L += ["", "## Ladder hand-offs (register 106) — single-leg forward "
          "optima from scalp_tp_ladder.md PER STATISTIC (no composite); "
          "win rate / weekly count vs the members' best-over-rungs, median "
          "vs members at the same rung; listed, never rules", "",
          *HANDOFF_HDR]
    L += [handoff_row(h) for h in hand] or [
        "| (no ladder hand-off on this emission) | | | | | | | | | |"]
    cw = art.get("census_watch", [])
    L += ["", "## Census clears (register 108) — bar-persistence headline "
          "cells (net reach 0.5xATR@5) above their matched floor's FULL "
          f"member range; measurable at n >= {CENSUS_MIN_N}; selection-null "
          "= the best net reach among measurable signals under signal-label "
          f"permutation across the leg's census fires ({NULL_SHUFFLES} pinned "
          "seeds); listed, never rules — the mechanism sentence is the "
          "operator's pen", "", *CENSUS_HDR]
    L += [census_row(c) for c in cw] or [
        "| (no census cell clears its full floor range) | | | | | | | | | | |"]
    aw = art.get("anatomy_watch", [])
    L += ["", "## Arrival-anatomy findings (register 114) — single-leg "
          "significant anatomy shifts from zone_anatomy.md, wearing the "
          "leg's whole-field selection-null (best fake |shift|/p95 per "
          "seed); listed, never rules", "",
          "| instrument | tf | side | window | metric | in n (zones/days) "
          "| in | base | shift | pct vs null | sel-pct | beats selection |",
          "|---|---|---|---|---|---|---|---|---|---|---|---|"]
    L += [f"| {r['instrument']} | {r['tf']} | {r['side']} | {r['window']} "
          f"| {r['metric']} "
          f"| {r['in_n']} ({r.get('in_zones', '?')}z/{r.get('in_days', '?')}d) "
          f"| {r['in_value']} "
          f"| {r['base_value']} | {r['shift']:+g} | {r['pct_vs_null']} "
          f"| {r['sel_pct']} | {'YES' if r['beats_selection'] else 'no'} |"
          for r in aw] or [
        "| (no single-leg anatomy finding this emission) | | | | | | | | | | | |"]
    vw = art.get("vol_watch", [])
    L += ["", "## Volatility-regime findings (register 130) — forward "
          "strata whose top-bucket (atr_pctl >= 95) degradation clears "
          "its within-stratum permutation null; listed, never rules — "
          "the entry-pause proposal needs >= 3 legs and the front door",
          "",
          "| instrument | variant | median gap (rest − top) | stop-rate "
          "gap | top n (distinct) | pct vs null |",
          "|---|---|---|---|---|---|"]
    L += [f"| {r['instrument']} | {r['variant']} | {r['median_gap']:+.2f} "
          f"| {r['stop_rate_gap']:+.3f} | {r['top_n_distinct']} "
          f"| {r['pct_vs_null']} |" for r in vw] or [
        "| (no forward stratum clears this emission) | | | | | |"]
    burden = art.get("spread_burden", [])
    L += ["", "## Standing per-instrument facts — spread burden at the "
          "scalp incumbent (register 106 follow-through (3); from "
          "scalp_tp_ladder.md)", "",
          "| instrument | arm | spread pts | n | spread / median winner's "
          "gross |", "|---|---|---|---|---|"]
    L += [f"| {b['instrument']} | {b['arm']} | {b['spread_pts']} | {b['n']} "
          f"| {100 * b['spread_share_of_win']:.0f}% |" for b in burden] or [
        "| (no ladder emission) | | | | |"]
    L.append("")
    with open(os.path.join(OUT, "per_market_watch.md"), "w") as f:
        f.write("\n".join(L))


def main():
    ap = argparse.ArgumentParser()
    ap.parse_args()
    head = subprocess.run(["git", "rev-parse", "HEAD"], cwd=ROOT,
                          capture_output=True, text=True).stdout.strip()
    art = {"STAMP": ("OBSERVATIONAL per-market config WATCH — a map of "
                     "where specialization would go, never a settings "
                     "page; cells graduate only via the register-105 "
                     "track; never validation"),
           "engine_commit": head, **run()}
    # register 106: the TP ladder's single-leg optima ride along (read
    # from its JSON when present; the ladder runs first under Part C)
    lad = os.path.join(OUT, "scalp_tp_ladder.json")
    lj = json.load(open(lad)) if os.path.exists(lad) else {}
    art["ladder_handoffs"] = lj.get("watch_handoff", [])
    art["spread_burden"] = lj.get("spread_burden", [])
    # register 108: census clears route here with their selection-null
    art["census_watch"] = census_watch()
    # register 114: single-leg anatomy findings ride along (the anatomy
    # runs with v3, before this page)
    an = os.path.join(OUT, "zone_anatomy.json")
    art["anatomy_watch"] = (json.load(open(an)).get("watch_rows", [])
                            if os.path.exists(an) else [])
    # register 130: single-leg volatility-regime clears ride along
    vr = os.path.join(OUT, "vol_regime.json")
    art["vol_watch"] = (json.load(open(vr)).get("watch_rows", [])
                        if os.path.exists(vr) else [])
    with open(os.path.join(OUT, "per_market_watch.json"), "w") as f:
        json.dump(art, f, indent=2, default=str)
    _emit(art, head)
    beats = sum(1 for m in art["markets"].values() for c in m["cells"]
                if c["beats_field_null_win"] and not c["tail_carried"])
    print(f"OBSERVATIONAL per-market watch -> {OUT}/per_market_watch.md "
          f"({beats} cells above their field's win-rate null p95; "
          "mechanism slots empty)")


if __name__ == "__main__":
    main()
