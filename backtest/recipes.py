"""Recipe layer — grammar v1 (register 41/42). OBSERVATIONAL ONLY:
nothing here touches paper, the ledger, frozen_v1, labels, or criteria.

GRAMMAR v1 (register 42; supersedes v0's single-stop form — v0 recipes
normalize into it unchanged):
  A recipe is ORDERED STAGES. Each stage:
    stop components (>=0, COMPOSED: effective stop = tightest, RATCHET-ONLY,
    evaluated on settled bars):
      ("fixed_pts", v)
      ("atr", k, tf)              # k x ATR(tf), tf DECLARED per component —
                                  # any ladder rung 1M/3M/5M/15M/30M/1H,
                                  # no implicit default
      ("trail_nth", N, (off_kind, off[, off_tf]), bar_tf)
                                  # beyond the Nth previous SETTLED bar of
                                  # bar_tf (the management TF); offset in
                                  # pts or k x ATR(off_tf)
      ("breakeven", off_pts)      # entry +/- offset; literature-adverse
                                  # caution registered (register 42d)
    target: ("fixed_pts", v) | ("atr", k, tf) | ("atr_haircut", k, tf, hc) | None
      atr_haircut (register 94, the scalp arms): resting order at entry + d*k*ATR(tf);
      FILL only when the favorable extreme EXCEEDS the level by hc points (the
      register-65(d) queue-risk haircut; one home tick); exit at the level;
      gap-opens past level+hc fill at the open (price improvement) — an
      OPTIMISTIC-class fill, declared in every consuming header
    exit_on / tighten_to: narrative-condition primitives (signal_watch
      NARRATIVE_EXIT_PRIMITIVES — the one-home rule). The excursion cut
      and flip-cut gates reported 2026-08-19 (registers 42-43); the gate
      was ruled NOT PASSED for universal flip-exits (net points is the
      deciding currency) — R-FLIPGUARD is the ONE registered staged
      candidate; per-hypothesis cherry-picks are a FORBIDDEN MOVE
      (register 44).
    until: ("progress_atr", k, tf) | ("progress_or_age", k, tf, minutes)
    reverse_on_exit: bool — CAPABILITY ONLY (register 78): a narrative
      exit may chain the opposite entry as a LINKED journal row (two
      rows, shared fire timestamp, separable stats). No
      narrative-management recipe registers until the in-trade
      narrative census reports — the flip-gate precedent.
  Stop evaluation cadence is ALWAYS 1M, regardless of any component's TF.

HONEST-FILL RULES (operator-ruled 2026-08-19; rule 5 added 2026-08-24,
register 77; each pinned):
  1. Intrabar stop+target both reachable -> STOP fills, always.
  2. Gap through a level -> filled at the gapped (worse) price (the open).
  3. Trailing/composed stops RATCHET ONLY, evaluated on settled bars.
  4. EOD flat at each instrument's NATIVE session close.
  5. If the effective stop AT FILL would be at-or-beyond the entry
     price, the trade DOES NOT OPEN (fill-logic correction, register 77:
     the instant-kill class — a trail already beyond entry closed the
     trade at the entry instant and donated the spread).

Sets are versioned registry objects; a run's artifact states its set
version; additions/changes only by re-registration, counted in the trial
log. PROVENANCE per recipe (register 42 item 4): v0's R-FIX/R-ATR/R-TRAIL
values originated as operator examples in the design discussion, never
ratified; R-TRAIL-ATR's 0.5x offset was a reviewer invention with no
basis. R-OP1 is the FIRST RATIFIED-PROVENANCE recipe (operator-specified
2026-08-19; its ATR TF was unstated and 15M is an ASSUMPTION, flagged).
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

from engine.signal_watch import AGNOSTIC_ROWS, NARRATIVE_EXIT_PRIMITIVES
from engine.store_loader import is_sealed, lockbox_boundary, zones
from backtest.sessions import session_of
from backtest.scoreboard import (PAIR_OF, PROVISIONAL_INSTRS,
                                 PROVISIONAL_STAMP, _replay, _series,
                                 _atr15, event_derived_fires, make_cfg)
from engine.signal_watch import SignalWatch

OUT = os.path.join(ROOT, "reports", "scoreboard")

RECIPE_SET_VERSION = "recipe_set_v0.8"   # register 128 (prior: 94)
RECIPE_SETS = {
    "recipe_set_v0.6": {
        # R-NEXIT-SENT (register 82; counted): EXITS ARE SENTENCES, NOT
        # ATOMS — ARM15 base mechanics; exit ONLY on a minted composite
        # sentence firing against the position (COMPOSITE_SENTENCES —
        # future graded sentences join automatically); FULL-HOLD scope
        # (the census's post-arming texture). The atoms-vs-sentences
        # head-to-head (vs R-NEXIT-FULL) is the narrative doctrine's
        # exit-layer test.
        "R-NEXIT-SENT": {
            "provenance": "register 82 (counted; operator diagnosis: "
                          "exits are sentences)",
            "stages": [{"stop": [("atr", 2.5, "15min")], "target": None,
                        "exit_on": [("opposing_sentence_fire",)],
                        "until": ("progress_atr", 1.0, "15min")},
                       {"stop": [("atr", 2.5, "15min"),
                                 ("trail_nth", 1, ("atr", 1.0, "15min"),
                                  "15min")], "target": None,
                        "exit_on": [("opposing_sentence_fire",)]}]},
        # --- narrative-exit variants (register 81; front door, counted,
        # forward-graded). Base mechanics = R-ARM15 (the register-80
        # concentration observation). Exit trigger = any opposing
        # sentence-class event (survey vocabulary): opposing-effort,
        # absorption-against, opposing sentence-fire. THE RECORDED
        # DISAGREEMENT: the flip-gate lesson says exits pay PRE-ARMING
        # only; the in-trade census texture says exits pay ANY TIME —
        # this head-to-head is that disagreement's test. The census
        # remains the deeper instrument; its maturity read supersedes
        # on conflict.
        "R-NEXIT-EARLY": {
            "provenance": "register 81 (counted); RE-LABELED register "
                          "82: the ATOMIC-TRIGGER control, pre-arming "
                          "scope — atoms saturate (21,076 narrative "
                          "exits in the first 6-variant journal)",
            "stages": [{"stop": [("atr", 2.5, "15min")], "target": None,
                        "exit_on": [("opposing_effort",),
                                    ("absorption_event",),
                                    ("opposing_signal_fire",)],
                        "until": ("progress_atr", 1.0, "15min")},
                       {"stop": [("atr", 2.5, "15min"),
                                 ("trail_nth", 1, ("atr", 1.0, "15min"),
                                  "15min")], "target": None}]},
        "R-NEXIT-FULL": {
            "provenance": "register 81 (counted); RE-LABELED register "
                          "82: the ATOMIC-TRIGGER control, full-hold "
                          "scope — R-NEXIT-SENT vs this row is the "
                          "atoms-vs-sentences head-to-head",
            "stages": [{"stop": [("atr", 2.5, "15min")], "target": None,
                        "exit_on": [("opposing_effort",),
                                    ("absorption_event",),
                                    ("opposing_signal_fire",)],
                        "until": ("progress_atr", 1.0, "15min")},
                       {"stop": [("atr", 2.5, "15min"),
                                 ("trail_nth", 1, ("atr", 1.0, "15min"),
                                  "15min")], "target": None,
                        "exit_on": [("opposing_effort",),
                                    ("absorption_event",),
                                    ("opposing_signal_fire",)]}]},
        # --- management ladder v2 (register 77; external review
        # registered as design-input evidence, in-sample, 7 tickets
        # counted; findings verified where they overlap our artifacts).
        # All three graded beside the v0.3 incumbent on the doctrine
        # axes; forward accrual decides.
        # R-BE — the review's best risk-adjusted: BE at +1.5xATR MFE,
        # else ride to EOD. The grammar's breakeven literature-caution
        # (register 42d) is CITED and the tension RECORDED: this BE is
        # thesis-scale (1.5xATR), not noise-scale — the data decides.
        "R-BE": {"provenance": "operator-registered 2026-08-24 "
                               "(register 77; review design-input)",
                 "stages": [{"stop": [("atr", 2.5, "15min")],
                             "target": None,
                             "until": ("progress_atr", 1.5, "15min")},
                            {"stop": [("atr", 2.5, "15min"),
                                      ("breakeven", 0.0)],
                             "target": None}]},
        # R-ARM15 — trail armed only at +1.0xATR MFE, anchored to
        # settled 15M bars with a 1.0xATR buffer. N=1 (the previous
        # settled 15M bar) ASSUMED — unstated in the order, flagged.
        "R-ARM15": {"provenance": "operator-registered 2026-08-24 "
                                  "(register 77; N=1 RATIFIED, 2026-08-28 sitting, register 88)",
                    "stages": [{"stop": [("atr", 2.5, "15min")],
                                "target": None,
                                "until": ("progress_atr", 1.0, "15min")},
                               {"stop": [("atr", 2.5, "15min"),
                                         ("trail_nth", 1,
                                          ("atr", 1.0, "15min"),
                                          "15min")], "target": None}]},
        # R-NOTRAIL — 2.5xATR SL only, hold to EOD (the review's
        # largest net; SUSPECTED TREND-EXPOSURE until the baseline
        # column prints — register 77 clause 3).
        "R-NOTRAIL": {"provenance": "operator-registered 2026-08-24 "
                                    "(register 77)",
                      "stages": [{"stop": [("atr", 2.5, "15min")],
                                  "target": None}]},
        # R-OP2 — operator-specified 2026-08-24 (register 76): initial
        # 2.5xATR(15M) composed tighter-of with a 0.25xATR(15M) trail
        # beyond the 2nd-previous settled 1M bar's extreme; ratchet-only,
        # no target, EOD flat native; honest fills. The narrative trade
        # layer's recipe. UNREFINED entries (register 70: refinement is
        # per-family; the layer states its choice).
        "R-OP2": {"provenance": "operator-specified 2026-08-24 "
                                "(register 76)",
                  "stages": [{"stop": [("atr", 2.5, "15min"),
                                       ("trail_nth", 2,
                                        ("atr", 0.25, "15min"),
                                        "1min")], "target": None}]},
        # v0.2 members carried forward unchanged below.
        # v0 four — ILLUSTRATIVE, unratified (provenance: operator design
        # examples; R-TRAIL-ATR offset a reviewer invention). ATR TFs
        # retro-annotated 15min (register 42b).
        "R-FIX": {"provenance": "illustrative-unratified",
                  "stages": [{"stop": [("fixed_pts", 10.0)],
                              "target": ("fixed_pts", 20.0)}]},
        "R-ATR": {"provenance": "illustrative-unratified",
                  "stages": [{"stop": [("atr", 1.5, "15min")],
                              "target": ("atr", 3.0, "15min")}]},
        "R-TRAIL": {"provenance": "illustrative-unratified",
                    "stages": [{"stop": [("trail_nth", 6, ("pts", 0.0),
                                          "1min")], "target": None}]},
        "R-TRAIL-ATR": {"provenance": "illustrative-unratified "
                                      "(offset: reviewer invention)",
                        "stages": [{"stop": [("trail_nth", 6,
                                              ("atr", 0.5, "15min"),
                                              "1min")], "target": None}]},
        # R-OP1 — operator-specified 2026-08-19 (register 42 item 6):
        # initial 1.5xATR (TF ASSUMED 15min — unstated, flagged) composed
        # with a 5.0pt trail beyond the 2nd-previous settled 1M bar;
        # tighter-of, ratchet-only, no target, trail live from entry.
        # FLAG: the 5.0pt offset is instrument-absolute; cross-instrument
        # v1 may want it ATR-relative — operator's later call.
        "R-OP1": {"provenance": "operator-ratified 2026-08-19; ATR TF "
                                "15M CONFIRMED 2026-08-20 (register 46)",
                  "stages": [{"stop": [("atr", 1.5, "15min"),
                                       ("trail_nth", 2, ("pts", 5.0),
                                        "1min")], "target": None}]},
        # R-FLIPGUARD — the ONE staged narrative candidate (register 44,
        # counted): flip-exit ACTIVE ONLY BEFORE the progress-arming
        # transition. Derivation cited to the early-flip adversity (7/8
        # contexts) and t-MFE 13-45 min findings — NOT the counterfactual
        # cells (the per-hypothesis cherry-pick is a registered forbidden
        # move). Arming values DERIVED-STATED (1.0xATR(15M) progress OR
        # 45 min age), ratification pending; graded on forward accrual
        # alongside R-OP1; ratification before any status.
        "R-FLIPGUARD": {"provenance": "arming values RATIFIED "
                                      "2026-08-20 (register 46); staged "
                                      "per register 44",
                        "stages": [
                            {"stop": [("atr", 1.5, "15min"),
                                      ("trail_nth", 2, ("pts", 5.0),
                                       "1min")], "target": None,
                             "exit_on": [("trend_flip",)],
                             "until": ("progress_or_age", 1.0, "15min",
                                       45)},
                            {"stop": [("atr", 1.5, "15min"),
                                      ("trail_nth", 2, ("pts", 5.0),
                                       "1min")], "target": None}]},
    },
}


# register 94 (operator-ratified 2026-08-27; register 92 chain): the scalp,
# two counted arms. Target = resting order at entry+0.5xATR(15M)
# with the 0.5pt one-tick haircut (config tick_size cited; per-
# instrument tick at any away registration); stop = the registered
# 2.5xATR reuse, DISASTER CAP ONLY (a tighter scalp stop is a v1
# variant whose value must DERIVE from the forward non-reach EOD
# distribution once accrued — derivation-required, no invented
# numbers); EOD-flat on non-reach; OPTIMISTIC target fill declared
# (register 65). The -REF arm enters via the founding refinement
# micro-loop (R2 per-family verdict cited: refinement helps the
# rejection family; the entry transform lives in the trade layer).
# EVIDENCE BASE: FOUR-INSTRUMENT since register 99 (the away-reach
# question graded YES on every leg); away journal rows
# carry claim status on their own instruments' floors; per-instrument
# tick governs the haircut away from home.
_SCALP_STAGES = [{"stop": [("atr", 2.5, "15min")],
                  "target": ("atr_haircut", 0.5, "15min", 0.5)}]
RECIPE_SETS["recipe_set_v0.7"] = {
    **RECIPE_SETS["recipe_set_v0.6"],
    f"R-SCALP-H{6}": {"provenance": "operator-ratified 2026-08-27 "
                                 "(register 94; Q-chain register 92)",
                   "stages": _SCALP_STAGES},
    f"R-SCALP-H{6}-REF": {"provenance": "operator-ratified 2026-08-27 "
                                     "(register 94; refined-entry arm, "
                                     "R2 verdict cited)",
                       "stages": _SCALP_STAGES},
}

# register 128 (the register-60 H1 harvest tickets, restated against the
# grammar built since; operator disposition (a), 2026-08-31): the arms
# run on the founding climax sentence's fires only (the scalp scoping
# precedent) as counted journal variants. The ladder incumbent's
# mechanics (R-ARM15's stages) are the shared base where stated.
# S0-H1's own adverse curve, resolved from the excursion artifact AT
# BUILD and frozen (the register-60 ticket's own words: "values
# resolved from the excursion artifacts at build and cited, never
# re-tuned"): backtest-window whole-scope mae60 p90 in ATR(15M) units
# (excursion_geometry.json, engine 78bd8f52b emission; backtest =
# design input, forward accrual decides).
H1_MAE60_P90_ATR = {"uk100fut": 2.06, "ger40fut": 2.96,
                    "nas100fut": 3.13, "us30fut": 2.23}
_ARM15_STAGES = RECIPE_SETS["recipe_set_v0.7"]["R-ARM15"]["stages"]
RECIPE_SETS["recipe_set_v0.8"] = {
    **RECIPE_SETS["recipe_set_v0.7"],
    "R-H1-DELAY3": {
        "provenance": "register 128 (register-60 harvest ticket "
                      "restated): entry deferred 3 settled 1M bars, "
                      "then the ladder incumbent's mechanics",
        "entry_offset_bars": 3, "stages": _ARM15_STAGES},
    "R-H1-DELAY10": {
        "provenance": "register 128 (register-60 harvest ticket "
                      "restated): entry deferred 10 settled 1M bars, "
                      "then the ladder incumbent's mechanics",
        "entry_offset_bars": 10, "stages": _ARM15_STAGES},
    "R-H1-CONFIRM": {
        "provenance": "register 128 (register-60 harvest ticket "
                      "restated): entry on the FIRST CONFIRMING PRINT "
                      "— the founding sequence's TEST / direction-"
                      "matched no-supply-class vocabulary — within "
                      "config execution.window exec bars (the -REF "
                      "transform precedent); NO-ENTRY on expiry; the "
                      "fire transform lives in the trade layer; NOT "
                      "the R2 refinement micro-loop (that verdict "
                      "stands, register 70)",
        "stages": _ARM15_STAGES},
    "R-H1-OWNCURVE": {
        "provenance": "register 128 (register-60 harvest ticket "
                      "restated): initial stop = S0-H1's OWN measured "
                      "adverse curve — mae60 p90 per instrument, ATR "
                      "units, frozen from the excursion artifact at "
                      "build (H1_MAE60_P90_ATR; derivation printed in "
                      "VARIANTS.md); plain hold to EOD (the ticket's "
                      "time-exit half DROPPED per register 64's "
                      "expectancy ruling — stated, register 128)",
        "stages": [{"stop": [("atr_by_instr", H1_MAE60_P90_ATR,
                              "15min")], "target": None}]},
    "R-H1-KNIFE": {
        "provenance": "register 128 (register-60 falling-knife ticket "
                      "restated): the flip-guard family's early-exit "
                      "stage — trend-flip exit ACTIVE ONLY PRE-ARMING "
                      "(R-FLIPGUARD's ratified arming, register 46: "
                      "1.0xATR(15M) progress OR 45 min) — composed "
                      "onto the ladder incumbent's mechanics",
        "stages": [{"stop": [("atr", 2.5, "15min")], "target": None,
                    "exit_on": [("trend_flip",)],
                    "until": ("progress_or_age", 1.0, "15min", 45)},
                   {"stop": [("atr", 2.5, "15min"),
                             ("trail_nth", 1, ("atr", 1.0, "15min"),
                              "15min")], "target": None}]},
}


def specialize(recipe, instr):
    """Register 128: materialize per-instrument derived components —
    ('atr_by_instr', {slug: k}, tf) becomes ('atr', k, tf) for the
    instrument at hand. Everything else passes through unchanged; a
    recipe with no such component returns itself."""
    if not any(c[0] == "atr_by_instr" for st in recipe["stages"]
               for c in st.get("stop", [])):
        return recipe
    out = dict(recipe)
    out["stages"] = []
    for st in recipe["stages"]:
        st2 = dict(st)
        st2["stop"] = [("atr", c[1][instr], c[2])
                       if c[0] == "atr_by_instr" else c
                       for c in st.get("stop", [])]
        out["stages"].append(st2)
    return out


def _norm_component(c):
    kind = c[0]
    if kind == "atr_by_instr":
        # register 128: per-instrument derived value — must be
        # specialize()d before simulation; normalized here so the
        # VARIANTS renderer can read the un-specialized structure
        if len(c) < 3:
            raise ValueError("atr_by_instr requires (map, tf)")
        return {"kind": "atr_by_instr", "map": dict(c[1]), "tf": c[2]}
    if kind == "fixed_pts":
        return {"kind": "fixed_pts", "v": float(c[1])}
    if kind == "atr":
        if len(c) < 3:
            raise ValueError("ATR component requires a declared TF "
                             "(register 42b: no implicit default)")
        return {"kind": "atr", "k": float(c[1]), "tf": c[2]}
    if kind == "trail_nth":
        off = c[2]
        if off[0] == "atr" and len(off) < 3:
            raise ValueError("ATR offset requires a declared TF")
        return {"kind": "trail_nth", "n": int(c[1]),
                "off_kind": off[0], "off": float(off[1]),
                "off_tf": off[2] if off[0] == "atr" else None,
                "bar_tf": c[3]}
    if kind == "breakeven":
        return {"kind": "breakeven", "off": float(c[1])}
    raise ValueError(c)


def normalize(recipe):
    off = recipe.get("entry_offset_bars", 0)
    if not isinstance(off, int) or off < 0:
        raise ValueError("entry_offset_bars must be a non-negative int "
                         "(register 128 grammar component)")
    stages = []
    for st in recipe["stages"]:
        for cond in st.get("exit_on", []) + st.get("tighten_to", []):
            if cond[0] not in NARRATIVE_EXIT_PRIMITIVES:
                raise ValueError(f"unregistered narrative primitive {cond}")
        stages.append({
            "stop": [_norm_component(c) for c in st.get("stop", [])],
            "target": st.get("target"),
            "until": st.get("until"),
            "exit_on": st.get("exit_on", []),
            "reverse_on_exit": bool(st.get("reverse_on_exit", False)),
        })
    return stages


class Env:
    """Per-instrument simulation environment: 1M arrays, per-rung settled
    bars, per-rung ATR (trailing mean TR over context.atr_period of that
    rung's bars), EOD flags, narrative event streams (optional)."""

    def __init__(self, arrs1m, atr_by_tf, rung_bars, eod_flag, narr=None):
        self.ts, self.o, self.h, self.l, self.c = arrs1m
        self.atr_by_tf = atr_by_tf          # tf -> sorted {close_ts: atr}
        self.rung = rung_bars               # tf -> (ts_close_ns, high, low)
        self.eod = eod_flag
        self.narr = narr or {}              # key -> sorted [(ts_ns, dir)]

    def atr_at(self, tf, t_ns):
        d = self.atr_by_tf[tf]
        keys = d["keys"]
        i = np.searchsorted(keys, t_ns, side="right") - 1
        return d["vals"][i] if i >= 0 else None

    def trail_ref(self, tf, n, j):
        """Extreme of the Nth previous SETTLED bar of `tf` at 1M bar j.
        Settled = rung close <= this 1M bar's open."""
        rts, rh, rl = self.rung[tf]
        open_ns = self.ts[j] - 60_000_000_000
        s = np.searchsorted(rts, open_ns, side="right") - 1
        ref = s - (n - 1)
        if ref < 0:
            return None, None
        return rh[ref], rl[ref]


def _target_level(spec, entry, d, env, t0):
    if spec is None:
        return None
    if spec[0] == "fixed_pts":
        return entry + d * spec[1]
    if spec[0] == "atr":
        a = env.atr_at(spec[2], t0)
        return None if a is None else entry + d * spec[1] * a
    if spec[0] == "atr_haircut":                       # register 94
        a = env.atr_at(spec[2], t0)
        return None if a is None else entry + d * spec[1] * a
    raise ValueError(spec)


def simulate(fires, env, recipe, spread):
    """v1 engine. Deterministic (twin-run bit-identity pinned)."""
    stages = normalize(recipe)
    ts, o, h, l, c = env.ts, env.o, env.h, env.l, env.c
    n = len(ts)
    trades = []
    open_until = -1
    # register 128: entry-offset grammar component — entry at the open
    # AFTER entry_offset_bars further settled 1M bars (0 = the standard
    # next-open entry)
    entry_off = int(recipe.get("entry_offset_bars", 0))
    fires_iter = sorted(fires, key=lambda x: x["ts"].value)
    for f in fires_iter:
        fi = np.searchsorted(ts, f["ts"].value, side="right") - 1
        ei = fi + 1 + entry_off
        if fi < 0 or ei >= n or ei <= open_until:
            continue
        d = f["dir"]
        entry = o[ei]
        t0 = ts[ei]
        # static component levels resolved at entry
        stage_i = 0
        eff_stop = None
        exit_px = exit_ts = reason = None
        fav_ext = -np.inf                   # settled favorable excursion
        j = ei
        while j < n:
            st = stages[stage_i]
            # stage transition (settled evaluation, before this bar)
            if st["until"] is not None and stage_i + 1 < len(stages):
                u = st["until"]
                armed = False
                if u[0] == "progress_atr":
                    a0 = env.atr_at(u[2], t0)
                    armed = a0 is not None and fav_ext >= u[1] * a0
                elif u[0] == "progress_or_age":
                    a0 = env.atr_at(u[2], t0)
                    armed = ((a0 is not None and fav_ext >= u[1] * a0)
                             or (ts[j] - t0) >= u[3] * 60_000_000_000)
                else:
                    raise ValueError(u)
                if armed:
                    stage_i += 1
                    st = stages[stage_i]
            # compose candidate stop = tightest of components (settled)
            cands = []
            for comp in st["stop"]:
                if comp["kind"] == "atr_by_instr":
                    raise ValueError(
                        "atr_by_instr reached simulate() un-specialized "
                        "— call recipes.specialize(recipe, instr) first "
                        "(register 128)")
                if comp["kind"] == "fixed_pts":
                    cands.append(entry - d * comp["v"])
                elif comp["kind"] == "atr":
                    a = env.atr_at(comp["tf"], t0)
                    if a is not None:
                        cands.append(entry - d * comp["k"] * a)
                elif comp["kind"] == "breakeven":
                    cands.append(entry + d * comp["off"])
                elif comp["kind"] == "trail_nth":
                    rh, rl = env.trail_ref(comp["bar_tf"], comp["n"], j)
                    if rh is not None:
                        off = comp["off"]
                        if comp["off_kind"] == "atr":
                            a = env.atr_at(comp["off_tf"], t0)
                            off = 0.0 if a is None else off * a
                        cands.append((rl - off) if d == 1 else (rh + off))
            if cands:
                tight = max(cands) if d == 1 else min(cands)
                # rule 3: the EFFECTIVE stop ratchets only
                eff_stop = tight if eff_stop is None else (
                    max(eff_stop, tight) if d == 1 else min(eff_stop, tight))
            target = _target_level(st["target"], entry, d, env, t0)
            tgt_hc = (st["target"][3]
                      if st["target"] is not None
                      and st["target"][0] == "atr_haircut" else 0.0)
            # narrative exits: settled events inside the PREVIOUS bar
            narr_hit = False
            for cond in st["exit_on"]:
                key = cond[0] if isinstance(cond, (list, tuple)) else cond
                evs = env.narr.get(key, [])
                lo_ns, hi_ns = ts[j] - 60_000_000_000, ts[j]
                a = np.searchsorted([e[0] for e in evs], lo_ns, side="right")
                for e in evs[a:]:
                    if e[0] > hi_ns:
                        break
                    if e[1] == 0 or e[1] == -d:
                        narr_hit = True
                        break
            if j == ei and eff_stop is not None and (
                    (d == 1 and eff_stop >= entry)
                    or (d == -1 and eff_stop <= entry)):
                exit_px, reason = None, "no_open"           # rule 5
                break
            if eff_stop is not None:
                if (d == 1 and o[j] <= eff_stop) or (d == -1
                                                     and o[j] >= eff_stop):
                    exit_px, reason = o[j], "stop_gap"      # rule 2
                    break
            if target is not None:
                if (d == 1 and o[j] >= target + tgt_hc) \
                        or (d == -1 and o[j] <= target - tgt_hc):
                    exit_px, reason = o[j], "target_gap"    # rule 2
                    break
            stop_hit = eff_stop is not None and (
                l[j] <= eff_stop if d == 1 else h[j] >= eff_stop)
            tgt_hit = target is not None and (
                h[j] >= target + tgt_hc if d == 1
                else l[j] <= target - tgt_hc)
            if stop_hit:                                    # rule 1
                exit_px, reason = eff_stop, "stop"
                break
            if tgt_hit:
                exit_px, reason = target, "target"
                break
            if narr_hit:                    # settled-bar close exit
                exit_px, reason = c[j], "narrative"
                if st.get("reverse_on_exit"):
                    reason = "narrative_reversed"
                break
            if env.eod[j]:                                  # rule 4
                exit_px, reason = c[j], "eod"
                break
            fav_ext = max(fav_ext, (h[j] - entry) if d == 1
                          else (entry - l[j]))
            j += 1
        if reason == "no_open":
            continue                        # rule 5: never opened
        if exit_px is None:
            j = n - 1
            exit_px, reason = c[j], "end_of_data"
        pts = (exit_px - entry) * d - spread
        trades.append({"fire_ts": str(f["ts"]), "entry_ts": str(
            pd.Timestamp(ts[ei], tz="UTC")), "dir": d,
            "entry": float(entry), "exit": float(exit_px), "reason": reason,
            "pts": round(float(pts), 2),
            "duration_min": round((ts[j] - ts[ei]) / 60e9, 1),
            "session": session_of(pd.Timestamp(ts[ei], tz="UTC")),
            "linked_reverse": f.get("_linked_reverse", False)})
        open_until = j
        if reason == "narrative_reversed" and j + 1 < n:
            # register 78 capability: chain the opposite entry as a
            # LINKED row (shared fire ts, separable stats). CAVEAT
            # (capability-only): chained rows process after the original
            # stream — one-position semantics across a chained row and a
            # later original fire are finalized when a narrative-
            # management recipe registers (flip-gate precedent).
            fires_iter.append({"ts": pd.Timestamp(ts[j], tz="UTC"),
                               "dir": -d, "name": f["name"],
                               "_linked_reverse": True})
    return trades


def _eod_flags(bars, slug):
    import store as store_mod
    a, b = store_mod.SESSIONS[slug]
    tz = store_mod.SESSION_TZ.get(slug, "Europe/London")
    idx = pd.DatetimeIndex([x.ts for x in bars]).tz_convert(tz)
    lt = idx.hour + idx.minute / 60.0
    dates = idx.date
    n = len(bars)
    flags = np.zeros(n, bool)
    for j in range(n):
        if lt[j] >= b:
            continue
        if j + 1 == n or lt[j + 1] >= b or dates[j + 1] != dates[j]:
            flags[j] = True
    return flags


def _spread_median(slug):
    df = pd.read_csv(os.path.join(ROOT, "clean_finsa", f"{slug}_1min.csv"))
    s = df[df["in_cash"]]["spread"].dropna()
    return round(float(s.median()), 2) if len(s) else 0.0


def _rung_data(bars_dict, atr_period):
    """Per-rung settled arrays + ATR maps for every available TF."""
    atr_by_tf, rung = {}, {}
    for key, blist in bars_dict.items():
        tf = key.split(":")[-1]
        live = [b for b in blist if not b.is_stub]
        if not live:
            continue
        rung[tf] = (np.array([b.ts.value for b in live]),
                    np.array([b.high for b in live]),
                    np.array([b.low for b in live]))
        amap = _atr15(live, atr_period)
        keys = np.array([k.value for k in sorted(amap)])
        vals = [amap[k] for k in sorted(amap)]
        atr_by_tf[tf] = {"keys": keys, "vals": vals}
    return atr_by_tf, rung


def build_env(instr, cfg, bars, narr=None):
    b1m_all = bars[cfg.mtf.execution_tf]
    b1m = [x for x in b1m_all if not x.is_stub]
    ts, cl, hi, lo, _segs, _b = _series(b1m_all)
    op = np.array([x.open for x in b1m])
    atr_by_tf, rung = _rung_data(bars, cfg.context.atr_period)
    eod = _eod_flags(b1m, instr)
    return Env((ts, op, hi, lo, cl), atr_by_tf, rung, eod, narr)


def run_instrument(instr):
    cfg = make_cfg({"session_model.extended_hours": True,
                    "session_model.ladder": True,
                    "debug.structure": True})   # trend flips for R-FLIPGUARD
    watch = SignalWatch()
    engine, bars, _ = _replay(cfg, instr, engine_hook=watch.attach)
    flips, prev = [], 0
    for e in engine.narrative.events:
        if e["type"] == "PHASE_EVAL" and e.get("tf") == "1min":
            t = e.get("trend", 0)
            if t != prev and t != 0:
                flips.append((pd.Timestamp(e["ts"]).value, t))
            prev = t
    env = build_env(instr, cfg, bars, narr={"trend_flip": sorted(flips)})
    fires = watch.fires + event_derived_fires(engine.narrative.events, cfg, bars, instr=instr)
    fires = [f for f in fires
             if f["name"] not in AGNOSTIC_ROWS and not is_sealed(f["ts"])]
    spread = _spread_median(instr)
    boundary, gl = lockbox_boundary(), zones()["go_live"]
    rset = RECIPE_SETS[RECIPE_SET_VERSION]
    out = {"instrument": instr, "pair": PAIR_OF.get(instr, instr),
           "status": ("provisional" if instr in PROVISIONAL_INSTRS
                      else "canonical"),
           "spread_charged_pts": spread, "recipes": {}}
    names = sorted({f["name"] for f in fires})
    for rname, recipe in rset.items():
        rows = {"_provenance": recipe["provenance"]}
        for hname in names:
            hf = [f for f in fires if f["name"] == hname]
            trades = simulate(hf, env, recipe, spread)
            for wname, sel in (
                    ("backtest", lambda t: pd.Timestamp(t["entry_ts"])
                     < boundary),
                    ("forward", lambda t: pd.Timestamp(t["entry_ts"]) >= gl)):
                tw = [t for t in trades if sel(t)]
                if not tw:
                    continue
                p = np.array([t["pts"] for t in tw])
                by_sess = {}
                for t in tw:
                    by_sess[t["session"]] = round(
                        by_sess.get(t["session"], 0.0) + t["pts"], 1)
                rows.setdefault(hname, {})[wname] = {
                    "n": len(tw),
                    "win_rate_pct": round(100 * float((p > 0).mean()), 1),
                    "net_pts": round(float(p.sum()), 1),
                    "median_pts": round(float(np.median(p)), 2),
                    "biggest_win": round(float(p.max()), 1),
                    "biggest_loss": round(float(p.min()), 1),
                    "avg_duration_min": round(
                        float(np.mean([t["duration_min"] for t in tw])), 1),
                    "net_by_session": by_sess}
        out["recipes"][rname] = rows
    return out


def _emit(results, head):
    L = ["# Recipe Performance — points rollup (GENERATED by "
         "backtest.recipes)", "",
         "Terms: [docs/GLOSSARY.md](../../docs/GLOSSARY.md).", "",
         f"Engine `{head[:9]}` · recipe set **{RECIPE_SET_VERSION}** "
         "(grammar v1, register 42). Per-recipe PROVENANCE printed in every "
         "table; illustrative values remain unratified; R-OP1 is "
         "operator-ratified (ATR TF assumed 15M, flagged).",
         "",
         "**OBSERVATIONAL ONLY** — touches nothing: not paper, not the "
         "ledger, not frozen_v1, not labels, not criteria. Directional "
         "fires only; same fires as the signal scoreboard. Sealed windows "
         "and the lockbox span excluded. Points are mid-price minus each "
         "instrument's measured median cash spread per trade — idealized.",
         "",
         "**Honest-fill rules (operator-ruled, part of every recipe's "
         "definition):** (1) both reachable -> stop always; (2) gap -> "
         "gapped (worse) price; (3) composed/trailing stops ratchet only, "
         "settled bars; (4) EOD flat at native session close. **FILL "
         "MODEL: PESSIMISTIC (register 65) — stops always fill against "
         "you; not comparable with touch=fill (optimistic) artifacts.**",
         ""]
    for res in results:
        inst = res["instrument"]
        L += [f"## {inst} ({res['status'].upper()}; spread charged "
              f"{res['spread_charged_pts']} pts/trade)"]
        if res["status"] == "provisional":
            L += [f"> {PROVISIONAL_STAMP}"]
        L.append("")
        for wname in ("backtest", "forward"):
            for rname, rows in res["recipes"].items():
                have = {h: w[wname] for h, w in rows.items()
                        if h != "_provenance" and wname in w}
                if not have:
                    continue
                sessions = sorted({s for v in have.values()
                                   for s in v["net_by_session"]})
                L += [f"### {inst} / {wname} / {rname} "
                      f"[{rows['_provenance']}] — net points",
                      "", "| H | " + " | ".join(sessions)
                      + " | TOTAL | n | win% | median |",
                      "|---|" + "---|" * (len(sessions) + 4)]
                for hname in sorted(have):
                    v = have[hname]
                    cells = [str(v["net_by_session"].get(s, "—"))
                             for s in sessions]
                    L.append(f"| {hname} | "
                             + " | ".join(cells)
                             + f" | **{v['net_pts']}** | {v['n']} "
                             f"| {v['win_rate_pct']}% | {v['median_pts']} |")
                L.append("")
            names = sorted({h for r in res["recipes"].values() for h in r
                            if h != "_provenance" and wname in r.get(h, {})})
            if names:
                rnames = list(res["recipes"])
                L += [f"### {inst} / {wname} — recipe comparison "
                      f"(net pts (n); same fires)", "",
                      "| H | " + " | ".join(rnames) + " |",
                      "|---|" + "---|" * len(rnames)]
                for hname in names:
                    cells = []
                    for rname in rnames:
                        v = res["recipes"][rname].get(hname, {}).get(wname)
                        cells.append(f"{v['net_pts']:+.0f} ({v['n']})"
                                     if v else "—")
                    L.append(f"| {hname} | "
                             + " | ".join(cells) + " |")
                L.append("")
    L += ["---", "", "Cards detail in recipe_performance.json (same run)."]
    with open(os.path.join(OUT, "recipe_performance.md"), "w") as f:
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
        print(f"# recipes: {instr} ...", file=sys.stderr)
        results.append(run_instrument(instr))
    art = {"STAMP": ("OBSERVATIONAL recipe layer (grammar v1) — never "
                     "validation; idealized fills per the honest-fill "
                     "rules"),
           "engine_commit": head, "recipe_set": RECIPE_SET_VERSION,
           "set_definition": {k: str(v) for k, v in
                              RECIPE_SETS[RECIPE_SET_VERSION].items()},
           "results": results}
    with open(os.path.join(OUT, "recipe_performance.json"), "w") as f:
        json.dump(art, f, indent=2, default=str)
    _emit(results, head)
    print(f"OBSERVATIONAL recipes -> {OUT}/recipe_performance.md")


if __name__ == "__main__":
    main()
