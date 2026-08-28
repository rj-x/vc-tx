"""Event-clock census v1 (register 104 part 2; pre-registered
prereg_event_clock_census, counted 2026-08-29). MEASUREMENT ONLY;
scalp arms headlined, every journal variant in the JSON. Two
dimensions with their mechanisms SEPARATED:

(a) SCHEDULED NEWS — windows +/-15 and +/-30 min around each
    data/macro_releases.csv timestamp, currency-tagged: USD releases
    vs the US legs, GBP vs uk100fut; CROSS-tagging reported, never
    assumed (ger40fut has no native currency in the file: it reads
    cross-tagged only). COVERAGE: the calendar's span is stated in the
    header; trades on days outside it are EXCLUDED from news cells
    (counted), never treated as no-news; VERIFIED_EMPTY spans (dated,
    attributed in data/macro_releases_log.md) count as no-news days.
(b) AUCTION SLOTS — native cash open and close +/-15/+/-30 per
    instrument (UTC values valid for the August store; DST stated):
    uk100fut 08:00Z / 16:30Z; ger40fut 07:00Z / 21:00Z (the register-40
    amendment's main pause cited as the close); US legs 13:30Z /
    20:00Z. Motivation: the week-32 re-identification — the killing
    zone was the US cash open (13:30-15:00Z), not the 12:30Z release
    slot (the reviewer's DST error recorded); Aug 3's ISM at 14:00Z the
    one confirmed news kill; Aug 4, the worst day, carried no release.

Per slot-type x leg x variant x window: stop-rate, net reach-rate
(target exits; meaningful for the scalp arms — the ladder variants
carry win-rate as their hit), net points, in-window vs out; the
conditioned base = the same cell's out-of-window rate; luck budget =
in-window labels shuffled within variant x leg x window strata, pinned
seeds, per-cell null p95 + field count vs null; measurable = both
sides >= MIN_SIDE_N; candidate = |gap| >= SPLIT_MIN_PP beyond its null
p95, same sign, on >= CAND_MIN_LEGS of 4 legs; glints listed, never
chained. Rule candidates on survival are mechanism-matched and
separate — a NEWS-WINDOW entry pause (scheduled avoidance) and/or an
OPEN-WINDOW entry pause (auction avoidance) — each distinguished from
the failed reactive cooldowns (register 103) by its EX-ANTE
mechanism; either proposes via the front door as a v1 arm component,
ratification required, nothing auto-built. Ex-lockbox; sealed
untouched; twin-run pinned (tests/test_event_clock.py); weekly under
Part C.
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

OUT = os.path.join(ROOT, "reports", "scoreboard")
TRADES_CSV = os.path.join(ROOT, "reports", "trades.csv")
CALENDAR = os.path.join(ROOT, "data", "macro_releases.csv")

WINDOWS_MIN = (15, 30)                 # order-stated
NATIVE_CCY = {"uk100fut": "GBP", "nas100fut": "USD", "us30fut": "USD",
              "ger40fut": None}         # ger40fut: cross-tagged only
AUCTION_UTC = {"uk100fut": ("08:00", "16:30"),
               "ger40fut": ("07:00", "21:00"),     # register 40: main pause
               "nas100fut": ("13:30", "20:00"),
               "us30fut": ("13:30", "20:00")}
VERIFIED_EMPTY = (("2026-08-20", "2026-08-22"),)   # calendar log, dated
SCALP_ARMS = ("R-SCALP-H" + str(6), "R-SCALP-H" + str(6) + "-REF")
REACH_REASONS = ("target", "target_gap")
STOP_REASONS = ("stop", "stop_gap")
MIN_SIDE_N = 10
SPLIT_MIN_PP = 10.0
CAND_MIN_LEGS = 3
NULL_SHUFFLES = 100
NULL_SEEDS = tuple(range(NULL_SHUFFLES))
INSTRUMENTS = ("uk100fut", "ger40fut", "nas100fut", "us30fut")


def load_calendar(path=CALENDAR):
    rows = [r for r in csv.DictReader(open(path))]
    rel = [(pd.Timestamp(r["utc_time"]).value, r["currency"],
            r["impact"], r["name"]) for r in rows]
    rel.sort()
    dates = sorted({str(pd.Timestamp(t, tz="UTC").date())
                    for t, _c, _i, _n in rel})
    return rel, (dates[0], dates[-1]) if dates else (None, None)


def in_coverage(day, span):
    lo, hi = span
    if lo is None:
        return False
    if lo <= day <= hi:
        return True
    return any(a <= day <= b for a, b in VERIFIED_EMPTY)


def news_tag(t_ns, ccy, rel, w_min):
    """Any release of currency ccy within +/-w_min of t."""
    w = w_min * 60_000_000_000
    for rt, rc, _i, _n in rel:
        if rc != ccy:
            continue
        if abs(rt - t_ns) <= w:
            return True
        if rt - t_ns > w:
            break
    return False


def auction_tag(t, instr, which, w_min):
    hh, mm = map(int, AUCTION_UTC[instr][0 if which == "open" else 1]
                 .split(":"))
    slot = t.normalize() + pd.Timedelta(hours=hh, minutes=mm)
    return abs((t - slot).total_seconds()) <= w_min * 60


def tag_row(r, rel, span):
    """All slot tags for one journal row; news tags None when the day
    is outside coverage (excluded, never no-news)."""
    t = pd.Timestamp(r["open_ts"])
    instr = r["instrument"]
    day = str(t.date())
    tags = {}
    covered = in_coverage(day, span)
    native = NATIVE_CCY[instr]
    cross = [c for c in ("USD", "GBP") if c != native]
    for w in WINDOWS_MIN:
        if covered:
            tags[f"news{w}:native"] = (news_tag(t.value, native, rel, w)
                                       if native else None)
            tags[f"news{w}:cross"] = any(news_tag(t.value, c, rel, w)
                                         for c in cross)
        else:
            tags[f"news{w}:native"] = None
            tags[f"news{w}:cross"] = None
        tags[f"open{w}"] = auction_tag(t, instr, "open", w)
        tags[f"close{w}"] = auction_tag(t, instr, "close", w)
    return tags, covered


def journal_rows():
    boundary, gl = lockbox_boundary(), zones()["go_live"]
    out = []
    for r in csv.DictReader(open(TRADES_CSV)):
        if in_lockbox_span(r["open_ts"]):
            continue
        t = pd.Timestamp(r["open_ts"])
        w = "backtest" if t < boundary else "forward" if t >= gl else None
        if w is None:
            continue
        out.append({"instrument": r["instrument"], "variant": r["variant"],
                    "open_ts": r["open_ts"], "window": w,
                    "pts": float(r["points"]), "reason": r["exit_reason"]})
    return out


def hit_of(r):
    """The variant's hit: reach (target) for the scalp arms, win for
    the ladder variants."""
    if r["variant"] in SCALP_ARMS:
        return r["reason"] in REACH_REASONS
    return r["pts"] > 0


def cells(rows, tags):
    """(instr, variant, window, tag) -> in/out stats."""
    out = {}
    for r, tg in zip(rows, tags):
        for tag, val in tg.items():
            if val is None:
                continue
            key = (r["instrument"], r["variant"], r["window"], tag)
            c = out.setdefault(key, {"in": [], "out": []})
            c["in" if val else "out"].append(r)

    def stats(rs):
        if not rs:
            return {"n": 0}
        return {"n": len(rs),
                "stop_rate": round(float(np.mean(
                    [x["reason"] in STOP_REASONS for x in rs])), 3),
                "hit_rate": round(float(np.mean([hit_of(x) for x in rs])),
                                  3),
                "net_pts": round(float(sum(x["pts"] for x in rs)), 1),
                "median_pts": round(float(np.median([x["pts"] for x in rs])),
                                    2)}
    res = {}
    for key, c in out.items():
        si, so = stats(c["in"]), stats(c["out"])
        meas = si["n"] >= MIN_SIDE_N and so["n"] >= MIN_SIDE_N
        res[key] = {"in": si, "out": so, "measurable": meas,
                    "hit_gap_pp": (round(100 * (si["hit_rate"]
                                                - so["hit_rate"]), 1)
                                   if meas else None),
                    "stop_gap_pp": (round(100 * (si["stop_rate"]
                                                 - so["stop_rate"]), 1)
                                    if meas else None)}
    return res


def luck(rows, tags, res):
    """In-window labels shuffled within (instr, variant, window) strata
    per tag; per-cell null |hit gap| p95; field count vs null."""
    keys = [k for k, v in res.items() if v["measurable"]]
    strata = {}
    for i, r in enumerate(rows):
        strata.setdefault((r["instrument"], r["variant"], r["window"]),
                          []).append(i)
    hits = np.array([hit_of(r) for r in rows])
    obs = sum(1 for k in keys if abs(res[k]["hit_gap_pp"]) >= SPLIT_MIN_PP)
    null_abs = {k: [] for k in keys}
    counts = []
    tag_names = sorted({k[3] for k in keys})
    # boolean membership per row per tag (None -> excluded)
    memb = {tag: np.array([tg.get(tag) for tg in tags], dtype=object)
            for tag in tag_names}
    for seed in NULL_SEEDS:
        rs = np.random.RandomState(seed)
        n_q = 0
        for k in keys:
            instr, var, w, tag = k
            idxs = np.array(strata[(instr, var, w)])
            m = memb[tag][idxs]
            valid = np.array([x is not None for x in m])
            idxs = idxs[valid]
            lab = np.array([bool(x) for x in m[valid]])
            perm = rs.permutation(len(lab))
            lab = lab[perm]
            h = hits[idxs]
            if lab.sum() and (~lab).sum():
                gap = 100 * (h[lab].mean() - h[~lab].mean())
            else:
                gap = 0.0
            null_abs[k].append(abs(gap))
            if abs(gap) >= SPLIT_MIN_PP:
                n_q += 1
        counts.append(n_q)
    for k in keys:
        res[k]["null_p95_pp"] = round(float(np.percentile(null_abs[k], 95)),
                                      1)
        res[k]["clears"] = bool(abs(res[k]["hit_gap_pp"]) >= SPLIT_MIN_PP
                                and abs(res[k]["hit_gap_pp"])
                                > res[k]["null_p95_pp"])
    return {"measurable_cells": len(keys), "observed_qualifying": obs,
            "null_median": float(np.median(counts)) if counts else None,
            "null_p95": (float(np.percentile(counts, 95))
                         if counts else None),
            "percentile_vs_null": (round(100 * float(np.mean(
                [obs > m for m in counts])), 1) if counts else None)}


def candidates(res):
    """Per (variant, tag): legs clearing (windows pooled by requiring
    the clear in either window is NOT allowed — a leg clears only if
    its forward cell clears; backtest printed beside)."""
    out = {}
    combos = sorted({(k[1], k[3]) for k in res})
    for var, tag in combos:
        legs = {}
        for instr in INSTRUMENTS:
            f = res.get((instr, var, "forward", tag))
            if f and f["measurable"]:
                legs[instr] = {"gap_pp": f["hit_gap_pp"],
                               "null_p95": f["null_p95_pp"],
                               "clears": f["clears"]}
        cl = {i: v for i, v in legs.items() if v["clears"]}
        signs = {np.sign(v["gap_pp"]) for v in cl.values()}
        grade = ("candidate" if len(cl) >= CAND_MIN_LEGS and len(signs) == 1
                 else "glint" if cl else "none")
        out[f"{var}|{tag}"] = {"legs": legs, "clearing": sorted(cl),
                               "grade": grade,
                               "mechanism": ("scheduled avoidance"
                                             if tag.startswith("news")
                                             else "auction avoidance")}
    return out


def run():
    rel, span = load_calendar()
    rows = journal_rows()
    tagged = [tag_row(r, rel, span) for r in rows]
    tags = [t for t, _c in tagged]
    excluded_news = sum(1 for _t, c in tagged if not c)
    res = cells(rows, tags)
    budget = luck(rows, tags, res)
    cand = candidates(res)
    return {"calendar_rows": len(rel), "coverage_span": list(span),
            "verified_empty": [list(x) for x in VERIFIED_EMPTY],
            "journal_rows_ex_lockbox": len(rows),
            "rows_outside_news_coverage": excluded_news,
            "luck_budget": budget,
            "cells": {"|".join(k): v for k, v in sorted(res.items())},
            "candidates": cand}


def _emit(art, head):
    lb = art["luck_budget"]
    L = ["# Event-Clock Census v1 (GENERATED by backtest.event_clock)", "",
         "Terms: [docs/GLOSSARY.md](../../docs/GLOSSARY.md).", "",
         f"Engine `{head[:9]}` — OBSERVATIONAL, pre-registered "
         "(prereg_event_clock_census, register 104). Two dimensions, "
         "mechanisms SEPARATED: scheduled news (+/-15/30 min around "
         "macro_releases.csv timestamps, currency-tagged; cross-tagging "
         "reported never assumed) and auction slots (native cash open/"
         "close +/-15/30; UTC values valid for the August store). "
         f"CALENDAR COVERAGE: {art['coverage_span'][0]} → "
         f"{art['coverage_span'][1]} ({art['calendar_rows']} High "
         "USD/GBP rows); VERIFIED-EMPTY (dated, attributed in "
         f"data/macro_releases_log.md): {art['verified_empty']} counts as "
         f"no-news; {art['rows_outside_news_coverage']} journal rows on "
         "uncovered days are EXCLUDED from news cells (never no-news); "
         "auction cells cover all days. STATISTIC SHAPES (74-B): "
         "in-window vs out-of-window hit-rate gap (reach for the scalp "
         "arms, win for the ladder variants) vs a label-permutation null "
         f"({NULL_SHUFFLES} pinned seeds) — per-cell p95 and the field "
         "count vs null; stop-rate and net points descriptive; measurable "
         f"= both sides >= {MIN_SIDE_N}; candidate = |gap| >= "
         f"{SPLIT_MIN_PP:g}pp beyond its null on >= {CAND_MIN_LEGS} of 4 "
         "forward legs, same sign. Fill models: the journal's PESSIMISTIC "
         "rows; the scalp arms' optimistic target fill declared (register "
         "94). Ex-lockbox. Rule candidates on survival are mechanism-"
         "matched and separate (news-window pause / open-window pause), "
         "distinguished from register 103's failed reactive cooldowns by "
         "their EX-ANTE mechanism; front door, ratification required.", "",
         f"**Luck budget:** {lb['observed_qualifying']} of "
         f"{lb['measurable_cells']} measurable cells reach |gap| >= "
         f"{SPLIT_MIN_PP:g}pp vs null median {lb['null_median']} / p95 "
         f"{lb['null_p95']}; percentile {lb['percentile_vs_null']}.", "",
         "## Scalp arms headline (in-window vs out; n in:out; forward "
         "and backtest)", "",
         "| arm | instrument | window | slot | n in:out | stop% in/out | "
         "hit% in/out | net in/out | hit gap | null p95 | clears |",
         "|---|---|---|---|---|---|---|---|---|---|---|"]
    for key, v in art["cells"].items():
        instr, var, w, tag = key.split("|")
        if var not in SCALP_ARMS or not v["measurable"]:
            continue
        si, so = v["in"], v["out"]
        L.append(f"| {var} | {instr} | {w} | {tag} | {si['n']}:{so['n']} "
                 f"| {100 * si['stop_rate']:.0f}/{100 * so['stop_rate']:.0f} "
                 f"| {100 * si['hit_rate']:.0f}/{100 * so['hit_rate']:.0f} "
                 f"| {si['net_pts']}/{so['net_pts']} "
                 f"| {v['hit_gap_pp']:+.1f}pp | {v['null_p95_pp']} "
                 f"| {'YES' if v['clears'] else 'no'} |")
    L += ["", "## Candidates and glints (all variants; forward legs "
          "clearing their null, same sign)", "",
          "| variant | slot | mechanism | grade | clearing legs |",
          "|---|---|---|---|---|"]
    any_ = False
    for k, d in sorted(art["candidates"].items(),
                       key=lambda x: (x[1]["grade"] != "candidate",
                                      x[1]["grade"] != "glint", x[0])):
        if d["grade"] == "none":
            continue
        any_ = True
        var, tag = k.split("|")
        L.append(f"| {var} | {tag} | {d['mechanism']} | {d['grade']} "
                 f"| {', '.join(d['clearing'])} |")
    if not any_:
        L.append("| (no cell clears its null on any forward leg) | | | | |")
    L.append("")
    with open(os.path.join(OUT, "event_clock.md"), "w") as f:
        f.write("\n".join(L))


def main():
    ap = argparse.ArgumentParser()
    ap.parse_args()
    head = subprocess.run(["git", "rev-parse", "HEAD"], cwd=ROOT,
                          capture_output=True, text=True).stdout.strip()
    art = {"STAMP": ("OBSERVATIONAL event-clock census — scheduled news "
                     "and auction slots, mechanisms separated; survivors "
                     "propose as ex-ante entry pauses via the front door; "
                     "never validation"),
           "engine_commit": head, **run()}
    with open(os.path.join(OUT, "event_clock.json"), "w") as f:
        json.dump(art, f, indent=2, default=str)
    _emit(art, head)
    n_c = sum(1 for d in art["candidates"].values()
              if d["grade"] == "candidate")
    print(f"OBSERVATIONAL event clock -> {OUT}/event_clock.md "
          f"({n_c} candidates; {art['rows_outside_news_coverage']} rows "
          "outside news coverage excluded)")


if __name__ == "__main__":
    main()
