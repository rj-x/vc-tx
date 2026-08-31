"""The weekly INSIGHTS ledger (register 109; pre-registered
prereg_insights_ledger, counted 2026-08-30). AN INDEX, NEVER EVIDENCE:
nothing gains evidential status by appearing here — every line points
at a stamped artifact and carries that artifact's own statistic, n and
null. Emitted by every Part C run after the WATCH page, before the
dashboard; dashboard-linked; reading-order item 2.

FIVE SECTIONS, each generated from the artifacts' JSON: (A) every cell
currently clearing any null (statistic, n, percentile, source); (B)
WATCH / glint entries with AGE-IN-WEEKS since first appearance; (C)
benched candidates with their gate status; (D) parked threads' standing
-null state; (E) DELTA — cells that CROSSED (new this emission), AGED
(present last emission and this), DIED (present last emission, absent
now) since the last emission. Field-level readings (a leg's whole-field
consistency percentile) are ledger entries too — register 110's
doctrine-stress note is the founding example of a field-level DIED.

STATE: reports/lab/insights_ledger.jsonl — one line per emission date
(re-emitting on the same date replaces that date's line, so twin runs
are idempotent); first-seen dates ride forward in the line. Absolute
dates only. Twin-run pinned (tests/test_insights.py).
"""

import argparse
import csv
import datetime as dt
import json
import os
import subprocess

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SB = os.path.join(ROOT, "reports", "scoreboard")
LEDGER = os.path.join(ROOT, "reports", "lab", "insights_ledger.jsonl")
OUT_MD = os.path.join(ROOT, "reports", "INSIGHTS.md")
OUT_JSON = os.path.join(SB, "insights.json")

# (C) the bench — candidates pre-registered or docketed but gated; the
# register cites are the authority, the gate status is read live where
# an artifact carries it
BENCH = (
    {"candidate": "R-SCOPED-BE (contingent variant)", "register": "92 / 107",
     "gate": "capture_study regime gate (ranging BE@0.25 clears its member "
             "band AND the ranging-minus-trending gap beyond luck)",
     "live": "capture_gate"},
    {"candidate": "v1 scalp geometry package (stop derivation + target rung)",
     "register": "101 / 106",
     "gate": "a target rung clearing on >= 3 of 4 forward legs beside the "
             "register-101 stop derivation; one ratification",
     "live": "tp_candidates"},
    {"candidate": "H" + str(6) + "-not-in-London suppression composite",
     "register": "93",
     "gate": "HOLD — re-proposes only if below-chance suppression reappears "
             "on fresh accrual", "live": None},
    {"candidate": "per-market candidate pool (3 seeded cells)",
     "register": "105 item 4",
     "gate": "operator's mechanism sentence, then the track's selection-null "
             "and a >= 45-row forward clock", "live": "pool_slots"},
    {"candidate": "HELD sentences: nas100fut R-NEXIT-FULL x overlap; "
                  "us30fut R-ARM15 x dead", "register": "105 follow-through",
     "gate": "condition (b): selection-percentile > 95 on a future emission",
     "live": "held"},
    {"candidate": "pyramiding counterfactual", "register": "79",
     "gate": "build slot behind the census reads (measurement, no grammar)",
     "live": None},
    {"candidate": "H15 sweep-zone entry variant", "register": "79",
     "gate": "PARKED until H15's record justifies", "live": None},
    {"candidate": "zone census v3 (departure bases, D1/H4)", "register": "111",
     "gate": "mint-on-lift only; scarcity check first (D1 5-15 active zones "
             "per leg expected)", "live": "zone_v3"},
)

HELD = (("nas100fut", "forward", "R-NEXIT-FULL", "overlap", "none"),
        ("us30fut", "forward", "R-ARM15", "dead", "none"))

# (D) parked threads whose standing null lives in prose (no live JSON)
PARKED_STATIC = (
    {"thread": "VWAP conditioner", "register": "51",
     "standing_null": "nothing survives the re-cut (-0.9pp)",
     "expiry": "re-read when forward fires double from the verdict date, "
               "or at the first monthly review"},
    {"thread": "ORB, EMA levels", "register": "51",
     "standing_null": "examined-and-parked, no artifact",
     "expiry": "revisitable by re-registration"},
    {"thread": "drift census", "register": "51",
     "standing_null": "no base-rate change", "expiry": "self-expiring on change"},
    {"thread": "flip gate", "register": "44",
     "standing_null": "NOT PASSED (procedural)",
     "expiry": "re-openable only by re-registration"},
)


def _load(name, base=SB):
    p = os.path.join(base, name)
    return json.load(open(p)) if os.path.exists(p) else {}


def clearing_cells(pmw, survey, jsurvey, events, srg, tp, h6, capture,
                   anatomy=None, stress=None):
    """(A) every cell clearing a null on the current emission."""
    out = []
    for key, c in (stress or {}).get("scalp_split", {}).items():
        if c.get("clears"):
            instr, arm, w = key.split("|")
            out.append({"key": f"stress:{key}",
                        "source": "stress_state.md",
                        "instrument": instr, "window": w,
                        "cell": f"{arm} by stress state",
                        "statistic": "best-worst state median gap",
                        "value": f"{c['gap']} ({c['best_state']})",
                        "n": sum(v["n"] for v in c["states"].values()),
                        "percentile": None,
                        "null": "day-state permutation p95"})
    for c in (anatomy or {}).get("claims", []):
        out.append({"key": f"anatomy:{c['tf']}|{c['side']}|{c['window']}"
                           f"|{c['metric']}",
                    "source": "zone_anatomy.md",
                    "instrument": ", ".join(c["legs"]),
                    "window": c["window"],
                    "cell": f"{c['metric']} in-zone ({c['tf']}/{c['side']})",
                    "statistic": "anatomy shift (>=3-of-4 legs)",
                    "value": "; ".join(f"{s:+g}" for s in c["shifts"]),
                    "n": len(c["legs"]), "percentile": None,
                    "null": "two-sided in/out permutation p95, per leg"})
    for mkey, m in (pmw.get("markets") or {}).items():
        instr, win = mkey.split("|")
        for c in m.get("cells", []):
            if c.get("tail_carried"):
                continue
            for stat, flag, pct in (("win_rate", "beats_field_null_win",
                                     "sel_pct_win"),
                                    ("median", "beats_field_null_median",
                                     "sel_pct_median")):
                if c.get(flag):
                    cell = f"{c['variant']} x {c['session']} x {c['slot']}"
                    out.append({
                        "key": f"pmw:{instr}|{win}|{c['variant']}|"
                               f"{c['session']}|{c['slot']}:{stat}",
                        "source": "per_market_watch.md",
                        "instrument": instr, "window": win, "cell": cell,
                        "statistic": stat, "value": c[stat], "n": c["n"],
                        "n_distinct": c.get("n_distinct"),
                        "percentile": c[pct],
                        "null": "field best-of selection null p95"})
    for h in pmw.get("ladder_handoffs", []):
        if h.get("beats_field_null"):
            out.append({"key": f"handoff:{h['instrument']}|{h['arm']}|"
                               f"{h['statistic']}",
                        "source": "scalp_tp_ladder.md (via WATCH hand-offs)",
                        "instrument": h["instrument"], "window": "forward",
                        "cell": f"{h['arm']} @ {h['rung']:g}xATR",
                        "statistic": h["statistic"], "value": h["value"],
                        "n": h["n"], "percentile": h["sel_pct"],
                        "null": h["null_kind"]})
    for c in pmw.get("census_watch", []):
        if c.get("beats_field_null"):
            out.append({"key": f"census:{c['instrument']}|{c['window']}|"
                               f"{c['signal']}",
                        "source": "bar_persistence.md (via WATCH census clears)",
                        "instrument": c["instrument"], "window": c["window"],
                        "cell": f"{c['signal']} net reach 0.5xATR@5",
                        "statistic": "net_reach_pct",
                        "value": c["net_reach_pct"], "n": c["n"],
                        "percentile": c["sel_pct"],
                        "null": "census signal-label selection null p95"})
    for res in survey.get("results", []):
        instr = res["instrument"]
        cons = (res.get("null") or {}).get("consistency") or {}
        if cons.get("field_significant"):
            out.append({"key": f"survey-field:{instr}:consistency",
                        "source": "narrative_survey.md",
                        "instrument": instr, "window": "both",
                        "cell": "consistency field count",
                        "statistic": "qualifying pairs",
                        "value": cons.get("actual_qualifying_pairs"),
                        "n": cons.get("candidate_pairs"),
                        "percentile": cons.get("percentile_vs_null"),
                        "null": "pair-count permutation null p95"})
        for ck, c in (res.get("cells") or {}).items():
            if c.get("survey_notable") or c.get("consistency_notable"):
                route = "+".join(r for r, f in (("EXT", "survey_notable"),
                                                ("CONS", "consistency_notable"))
                                 if c.get(f))
                out.append({"key": f"survey:{instr}|{ck}",
                            "source": "narrative_survey.md",
                            "instrument": instr,
                            "window": ck.split("|")[2], "cell": ck,
                            "statistic": f"lift_pp ({route})",
                            "value": c.get("lift_pp"), "n": c.get("n"),
                            "percentile": None,
                            "null": "survey extremity / consistency null"})
    conc = jsurvey.get("concentration") or {}
    if conc.get("percentile_vs_null") is not None \
            and conc["percentile_vs_null"] > 95:
        out.append({"key": "jsurvey:concentration",
                    "source": "journal_survey.md", "instrument": "pooled",
                    "window": "both", "cell": "max positive cells in one variant",
                    "statistic": "concentration",
                    "value": conc.get("observed_max"),
                    "n": conc.get("measurable_cells"),
                    "percentile": conc["percentile_vs_null"],
                    "null": "variant-label permutation p95"})
    for i, q in enumerate(jsurvey.get("question_candidates") or []):
        out.append({"key": "jsurvey:candidate:" + "|".join(
                        str(q.get(k)) for k in sorted(q) if k != "n"),
                    "source": "journal_survey.md", "instrument": "pooled",
                    "window": "both", "cell": json.dumps(q, default=str)[:80],
                    "statistic": "question candidate", "value": None,
                    "n": q.get("n"), "percentile": None,
                    "null": "session floors + concentration"})
    for src, art, label in (("event", events, "event_clock.md"),
                            ("srg", srg, "scalp_risk_grid.md"),
                            ("tp", tp, "scalp_tp_ladder.md")):
        for cell, c in (art.get("candidates") or {}).items():
            for leg in c.get("clearing", []):
                lg = (c.get("legs") or {}).get(leg, {})
                out.append({"key": f"{src}:{cell}|{leg}", "source": label,
                            "instrument": leg, "window": "forward",
                            "cell": cell, "statistic": c.get("grade", "cell"),
                            "value": lg.get("gap_pp", lg.get("net_delta",
                                                             lg.get("median"))),
                            "n": lg.get("n"), "percentile": None,
                            "null": "per-leg null p95 / member band"})
    for c in h6.get("candidates") or []:
        out.append({"key": f"h6:candidate:{c}", "source": "h6_refinement.md",
                    "instrument": "scalp", "window": "forward",
                    "cell": str(c), "statistic": "candidate", "value": None,
                    "n": None, "percentile": None, "null": "cell budget"})
    lb = h6.get("luck_budget") or {}
    if (lb.get("percentile_vs_null") or 0) > 95:
        out.append({"key": "h6:luck_budget", "source": "h6_refinement.md",
                    "instrument": "scalp", "window": "forward",
                    "cell": "field count of qualifying splits",
                    "statistic": "field count",
                    "value": lb.get("observed_qualifying"),
                    "n": lb.get("measurable_cells"),
                    "percentile": lb["percentile_vs_null"],
                    "null": "label permutation p95"})
    elb = events.get("luck_budget") or {}
    if (elb.get("percentile_vs_null") or 0) > 95:
        out.append({"key": "event:luck_budget", "source": "event_clock.md",
                    "instrument": "all", "window": "both",
                    "cell": "field count of qualifying window splits",
                    "statistic": "field count",
                    "value": elb.get("observed_qualifying"),
                    "n": elb.get("measurable_cells"),
                    "percentile": elb["percentile_vs_null"],
                    "null": "label permutation p95"})
    for instr, v in (capture.get("per_instrument") or {}).items():
        lb = v.get("luck_budget") or {}
        if (lb.get("percentile_vs_null") or 0) > 95:
            out.append({"key": f"capture:{instr}:luck", "source": "capture_study.md",
                        "instrument": instr, "window": "both",
                        "cell": "quiet/loud differentiating pairs",
                        "statistic": "field count", "value": lb.get("observed"),
                        "n": v.get("n_base"),
                        "percentile": lb["percentile_vs_null"],
                        "null": "tape-label permutation p95"})
        g = (v.get("regime_gate") or {}).get("gate") or {}
        if g.get("PASS"):
            out.append({"key": f"capture:{instr}:regime_gate",
                        "source": "capture_study.md", "instrument": instr,
                        "window": "both", "cell": "R-SCOPED-BE gate",
                        "statistic": "ranging BE@0.25 per-trade delta",
                        "value": g.get("ranging_per_trade_delta"),
                        "n": g.get("ranging_n"),
                        "percentile": g.get("percentile_vs_null"),
                        "null": "member band + regime-label permutation"})
    return out


def watch_entries(pmw, events, srg, h6, forensics, anatomy=None):
    """(B) WATCH / glint entries — listed, never rules."""
    out = []
    for r in (anatomy or {}).get("watch_rows", []):
        out.append({"key": f"anatomy-watch:{r['instrument']}|{r['tf']}"
                           f"|{r['side']}|{r['window']}|{r['metric']}",
                    "kind": "anatomy finding",
                    "source": "zone_anatomy.md",
                    "entry": f"{r['instrument']} {r['metric']} in-zone "
                             f"({r['tf']}/{r['side']}, {r['window']})",
                    "legs": r["instrument"],
                    "status": f"shift {r['shift']:+g} (pct {r['pct_vs_null']}); "
                              f"sel-pct {r['sel_pct']} — "
                              f"{'beats' if r['beats_selection'] else 'inside'} "
                              "the field's best fake"})
    for c in pmw.get("candidate_pool", []):
        out.append({"key": f"pool:{c['cell']}", "kind": "candidate pool",
                    "source": "per_market_watch.md", "entry": c["cell"],
                    "legs": c["legs"],
                    "status": ("mechanism EMPTY" if not c.get("mechanism")
                               else "mechanism written")})
    cells = {}
    for mkey, m in (pmw.get("markets") or {}).items():
        instr, win = mkey.split("|")
        for c in m.get("cells", []):
            cells[(instr, win, c["variant"], c["session"], c["slot"])] = c
    for hk in HELD:
        c = cells.get(hk)
        st = ("not on the page this emission" if not c else
              f"n={c['n']} ({c.get('n_distinct', c['n'])} distinct) "
              f"sel-pct win {c['sel_pct_win']} / median "
              f"{c['sel_pct_median']}; condition (b) "
              f"{'MET' if (c['beats_field_null_win'] or c['beats_field_null_median']) and not c['tail_carried'] else 'unmet'}")
        out.append({"key": "held:" + "|".join(hk), "kind": "HELD sentence",
                    "source": "per_market_watch.md",
                    "entry": f"{hk[0]} {hk[2]} x {hk[3]}", "legs": hk[0],
                    "status": st})
    for h in pmw.get("ladder_handoffs", []):
        out.append({"key": f"handoff:{h['instrument']}|{h['arm']}|{h['statistic']}",
                    "kind": "ladder hand-off", "source": "scalp_tp_ladder.md",
                    "entry": f"{h['instrument']} {h['arm']} best {h['statistic']} "
                             f"@ {h['rung']:g}x", "legs": h["instrument"],
                    "status": f"n={h['n']} sel-pct {h['sel_pct']} "
                              f"{'beats null' if h['beats_field_null'] else 'inside null'}"})
    for c in pmw.get("census_watch", []):
        out.append({"key": f"census:{c['instrument']}|{c['window']}|{c['signal']}",
                    "kind": "census clear", "source": "bar_persistence.md",
                    "entry": f"{c['instrument']} {c['signal']} {c['window']} "
                             "net reach 0.5xATR@5", "legs": c["instrument"],
                    "status": (f"n={c['n']} sel-pct {c['sel_pct']} "
                               f"{'beats null' if c['beats_field_null'] else 'inside null'}"
                               if c["measurable"] else
                               f"unmeasurable n={c['n']} "
                               f"({c['n_to_measurable']} to go)")})
    for src, art, label in (("event", events, "event_clock.md"),
                            ("srg", srg, "scalp_risk_grid.md")):
        for cell, c in (art.get("candidates") or {}).items():
            if c.get("grade") == "glint":
                out.append({"key": f"{src}-glint:{cell}", "kind": "glint",
                            "source": label, "entry": cell,
                            "legs": ", ".join(c.get("clearing", [])),
                            "status": f"glint ({len(c.get('clearing', []))} of "
                                      f"{len(c.get('legs') or {})} legs)"})
    for g in h6.get("glints") or []:
        out.append({"key": f"h6-glint:{g}", "kind": "glint",
                    "source": "h6_refinement.md", "entry": str(g),
                    "legs": "scalp", "status": "glint"})
    fw = {}
    for instr, v in (forensics.get("per_instrument") or {}).items():
        w = v.get("watch") or []
        if w:
            near = sorted(w, key=lambda r: r.get("n_to_measurable", 999))[:3]
            fw[instr] = {"count": len(w),
                         "nearest": [f"{r['sentence']} {r['variant']} "
                                     f"{r['session']} {r['feature']}={r['value']} "
                                     f"({r['n_to_measurable']} to go)"
                                     for r in near]}
    return out, fw


def bench_status(capture, tp, pmw, zone3):
    """(C) benched candidates, gate status read live where it exists."""
    out = []
    gates = {}
    for instr, v in (capture.get("per_instrument") or {}).items():
        g = (v.get("regime_gate") or {}).get("gate") or {}
        gates[instr] = ("PASS" if g.get("PASS") else
                        f"not passed (pct {g.get('percentile_vs_null')})")
    tpc = sum(1 for c in (tp.get("candidates") or {}).values()
              if c.get("grade") == "candidate")
    slots = sum(1 for c in pmw.get("candidate_pool", [])
                if not c.get("mechanism"))
    held = [w for w in pmw.get("_held", [])]
    z3 = zone3.get("results") or []
    for b in BENCH:
        live = b["live"]
        if live == "capture_gate":
            st = "; ".join(f"{k} {v}" for k, v in sorted(gates.items())) \
                or "no emission"
        elif live == "tp_candidates":
            st = f"{tpc} target rung(s) clearing >= 3 of 4 legs"
        elif live == "pool_slots":
            st = f"{slots} of {len(pmw.get('candidate_pool', []))} slots EMPTY"
        elif live == "held":
            st = "; ".join(held) or "see WATCH section"
        elif live == "zone_v3":
            st = ("; ".join(f"{r['instrument']} {r.get('scarcity', {}).get('verdict', '?')}"
                            for r in z3) if z3 else "not yet emitted")
        else:
            st = "gated (no live artifact)"
        out.append({**{k: v for k, v in b.items() if k != "live"},
                    "status": st})
    return out


def parked_state(zone, cofire_reread):
    """(D) parked threads — the standing null as the artifact states it."""
    out = []
    for res in zone.get("results") or []:
        a = res["ladder"].get(res["null_anchor_rung"], {})
        p = a.get("pooled") or {}
        cells = []
        for w in ("backtest", "forward"):
            c = p.get(f"{w}|in") or {}
            if c.get("lift_pp") is not None:
                cells.append(f"{w} in-zone {c['lift_pp']:+.1f}pp (n{c['n']})")
        out.append({"thread": f"H4 key-zone census v2 — {res['instrument']}",
                    "register": "97",
                    "standing_null": "; ".join(cells) or "no measurable cell",
                    "expiry": "revisitable only by re-registration on new "
                              "evidence (v3 is a new definition, register 111)"})
    if cofire_reread:
        out.append({"thread": "co-fire census", "register": "88 item 7",
                    "standing_null": f"{len(cofire_reread.get('qualifying_pairs') or [])} "
                                     f"qualifying pairs of "
                                     f"{len(cofire_reread.get('measurable_pairs') or [])} "
                                     "measurable (dated re-read)",
                    "expiry": "accrual decides; archive-bound after the sitting"})
    out.extend(dict(p) for p in PARKED_STATIC)
    return out


def load_ledger(path=LEDGER):
    if not os.path.exists(path):
        return []
    return [json.loads(l) for l in open(path) if l.strip()]


def delta(prev, clearing_keys, watch_keys, today):
    """(E) crossed / aged / died vs the previous emission; first-seen
    dates ride forward."""
    p_clear = set(prev.get("clearing", [])) if prev else set()
    p_watch = set(prev.get("watch", [])) if prev else set()
    first = dict((prev or {}).get("first_seen", {}))
    for k in set(clearing_keys) | set(watch_keys):
        first.setdefault(k, today)
    return {"crossed": sorted(set(clearing_keys) - p_clear),
            "aged": sorted(set(clearing_keys) & p_clear),
            "died": sorted(p_clear - set(clearing_keys)),
            "watch_new": sorted(set(watch_keys) - p_watch),
            "watch_died": sorted(p_watch - set(watch_keys)),
            "first_seen": first,
            "previous_date": (prev or {}).get("date")}


def age_weeks(first_seen, key, today):
    d0 = dt.date.fromisoformat(first_seen.get(key, today))
    return (dt.date.fromisoformat(today) - d0).days // 7


def build(today, prev=None):
    pmw = _load("per_market_watch.json")
    survey = _load("narrative_survey.json")
    jsurvey = _load("journal_survey.json")
    events = _load("event_clock.json")
    srg = _load("scalp_risk_grid.json")
    tp = _load("scalp_tp_ladder.json")
    h6 = _load("h6_refinement.json")
    capture = _load("capture_study.json")
    zone = _load("zone_census.json")
    zone3 = _load("zone_census_v3.json")
    anatomy = _load("zone_anatomy.json")
    stress = _load("stress_state.json")
    cofr = _load("cofire_reread_2026-08-28.json")
    forensics = _load("forensics.json",
                      os.path.join(ROOT, "reports", "forensics"))
    clearing = clearing_cells(pmw, survey, jsurvey, events, srg, tp, h6,
                              capture, anatomy, stress)
    watch, fwatch = watch_entries(pmw, events, srg, h6, forensics,
                                  anatomy)
    pmw["_held"] = [w["status"] for w in watch if w["kind"] == "HELD sentence"]
    bench = bench_status(capture, tp, pmw, zone3)
    parked = parked_state(zone, cofr)
    d = delta(prev, [c["key"] for c in clearing], [w["key"] for w in watch],
              today)
    for c in clearing:
        c["age_weeks"] = age_weeks(d["first_seen"], c["key"], today)
    for w in watch:
        w["age_weeks"] = age_weeks(d["first_seen"], w["key"], today)
    return {"date": today, "clearing": clearing, "watch": watch,
            "forensics_watch": fwatch, "bench": bench, "parked": parked,
            "delta": d}


def _emit(art, head):
    d = art["delta"]
    L = ["# INSIGHTS — the weekly index (GENERATED by backtest.insights)", "",
         "Terms: [docs/GLOSSARY.md](docs/GLOSSARY.md).", "",
         f"Engine `{head[:9]}` — emission {art['date']}; previous "
         f"{d['previous_date'] or 'none (founding emission)'}. AN INDEX, "
         "NEVER EVIDENCE (register 109): nothing gains evidential status by "
         "appearing here — every line points at a stamped artifact and "
         "carries that artifact's own statistic, n and null. Statistic "
         "shapes are the sources' (74-B). Ages are weeks since first "
         "appearance in this ledger (founding emission = 0). Ex-lockbox "
         "throughout (the sources are). Nothing advances from this page.",
         ""]
    L += ["## A. Cells clearing a null on this emission "
          f"({len(art['clearing'])})", "",
          "| source | instrument | window | cell | statistic | value | n "
          "| percentile | null | age (w) |",
          "|---|---|---|---|---|---|---|---|---|---|"]
    for c in art["clearing"]:
        nd = c.get("n_distinct")
        ncell = (f"{c['n']} ({nd})" if nd is not None and nd != c["n"]
                 else c["n"])
        L.append(f"| {c['source']} | {c['instrument']} | {c['window']} "
                 f"| {c['cell']} | {c['statistic']} | {c['value']} | {ncell} "
                 f"| {c['percentile'] if c['percentile'] is not None else '—'} "
                 f"| {c['null']} | {c['age_weeks']} |")
    if not art["clearing"]:
        L.append("| (no cell clears any null this emission) | | | | | | | | | |")
    L += ["", f"## B. WATCH / glint entries ({len(art['watch'])}) — listed, "
          "never rules; age = weeks since first appearance here", "",
          "| kind | source | entry | legs | status | age (w) |",
          "|---|---|---|---|---|---|"]
    for w in art["watch"]:
        L.append(f"| {w['kind']} | {w['source']} | {w['entry']} | {w['legs']} "
                 f"| {w['status']} | {w['age_weeks']} |")
    if art["forensics_watch"]:
        L += ["", "Forensics WATCH list (reports/forensics/; thin cells "
              "tracked to measurability):", ""]
        for instr, v in sorted(art["forensics_watch"].items()):
            L.append(f"- {instr}: {v['count']} rows; nearest to measurable — "
                     + "; ".join(v["nearest"]))
    L += ["", "## C. Benched candidates — gate status", "",
          "| candidate | register | gate | status this emission |",
          "|---|---|---|---|"]
    for b in art["bench"]:
        L.append(f"| {b['candidate']} | {b['register']} | {b['gate']} "
                 f"| {b['status']} |")
    L += ["", "## D. Parked threads — standing-null state", "",
          "| thread | register | standing null (current emission) | expiry / "
          "re-open condition |", "|---|---|---|---|"]
    for p in art["parked"]:
        L.append(f"| {p['thread']} | {p['register']} | {p['standing_null']} "
                 f"| {p['expiry']} |")
    def _keys(ks, cap=25):
        if not ks:
            return ""
        s = " — " + "; ".join(ks[:cap])
        return s + (f"; … (+{len(ks) - cap} more, in insights.json)"
                    if len(ks) > cap else "")
    founding = d["previous_date"] is None
    L += ["", f"## E. DELTA since {d['previous_date'] or 'the founding emission'}",
          "",
          f"- CROSSED (clearing now, not last emission): {len(d['crossed'])}"
          + (" — founding emission: every key is CROSSED by construction "
             "(keys in insights.json)" if founding else _keys(d["crossed"])),
          f"- AGED (clearing both emissions): {len(d['aged'])}"
          + _keys(d["aged"]),
          f"- DIED (cleared last emission, not now): {len(d['died'])}"
          + _keys(d["died"]),
          f"- WATCH entries new / gone: {len(d['watch_new'])} / "
          f"{len(d['watch_died'])}"
          + ((" — gone:" + _keys(d["watch_died"])[3:]) if d["watch_died"]
             and not founding else ""),
          "",
          "Founding example (register 110): the narrative survey's home "
          "consistency count read 13 of 20 pairs at percentile 100 on the "
          "2026-08-23 emission and 9 of 31 at percentile 89 on the "
          "2026-08-30 emission — a field-level DIED that predates this "
          "ledger; field-level readings are therefore ledger entries "
          "(survey-field keys), so the next such death is dated here.", ""]
    with open(OUT_MD, "w") as f:
        f.write("\n".join(L))


def write_ledger(art, head, path=LEDGER):
    lines = [l for l in load_ledger(path) if l.get("date") != art["date"]]
    lines.append({"date": art["date"], "engine_commit": head,
                  "clearing": [c["key"] for c in art["clearing"]],
                  "watch": [w["key"] for w in art["watch"]],
                  "first_seen": art["delta"]["first_seen"]})
    with open(path, "w") as f:
        for l in lines:
            f.write(json.dumps(l, default=str) + "\n")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--date", default=dt.date.today().isoformat(),
                    help="emission date (absolute; default today UTC-naive)")
    a = ap.parse_args()
    head = subprocess.run(["git", "rev-parse", "HEAD"], cwd=ROOT,
                          capture_output=True, text=True).stdout.strip()
    prior = [l for l in load_ledger() if l.get("date") != a.date]
    prev = prior[-1] if prior else None
    art = build(a.date, prev)
    art = {"STAMP": ("INSIGHTS ledger — an index of what clears, what is "
                     "watched, what is benched, what is parked, and what "
                     "changed; never evidence"),
           "engine_commit": head, **art}
    with open(OUT_JSON, "w") as f:
        json.dump(art, f, indent=2, default=str)
    _emit(art, head)
    write_ledger(art, head)
    d = art["delta"]
    print(f"INSIGHTS ledger -> reports/INSIGHTS.md ({len(art['clearing'])} "
          f"clearing, {len(art['watch'])} watched; delta +{len(d['crossed'])} "
          f"/ ={len(d['aged'])} / -{len(d['died'])})")


if __name__ == "__main__":
    main()
