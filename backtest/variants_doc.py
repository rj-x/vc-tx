"""The VARIANTS reference — docs/VARIANTS.md (register 116 item 2).
GENERATED each Part C run from the recipe/variant one-home: every
number renders from backtest/recipes.py RECIPE_SETS (the SAME
structures the trade layer executes, via the same normalize()),
config.yaml (the refinement micro-loop values) and the trade layer's
scope constants — NO HAND-WRITTEN NUMBERS ANYWHERE. Curated text is
limited to status labels and plain-English glosses of registered
primitive NAMES; provenance strings render from the recipe structures
themselves.

One section per registered variant: mechanics (entry, initial stop,
trail/BE/arm logic with values, target + fill model with haircut,
exit conditions, EOD behavior), scope, fill-model class (register 65,
DERIVED from the structure: an atr_haircut target = OPTIMISTIC, else
PESSIMISTIC), provenance, status. Authority trails cite
docs/parameter_registry.md's curated map.

ENFORCEMENT (the glossary pattern applied to strategies, register 60
precedent): every variant name appearing in the journal must have a
rendered section — a journal variant absent from this page fails the
suite (tests/test_variants_doc.py); the page is also pinned
regeneration-clean against the working tree (the param-registry
pattern). Linked from the dashboard map, the glossary's R- entry, the
journal's header comment, and the reading order after the glossary.
"""

import os
import sys

import yaml

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "scripts"))

from backtest.recipes import (RECIPE_SET_VERSION, RECIPE_SETS,
                              normalize)
from backtest.trade_layer import (H1_SENTENCE, H1_VARIANTS,
                                  SCALP_SENTENCE, SCALP_VARIANTS,
                                  VARIANTS as JOURNAL_VARIANTS)
from param_registry import AUTHORITY

DOC = os.path.join(ROOT, "docs", "VARIANTS.md")

# status labels (the order's vocabulary: incumbent / experiment /
# counted-arm) — curated PROSE, no numbers; provenance numbers render
# from the recipe structures
STATUS = {
    "R-NOTRAIL": "counted-arm — the unmanaged full-hold base "
                 "(BASE_VARIANT for the counterfactual studies; "
                 "suspected trend-exposure, register 77 clause 3)",
    "R-BE": "counted-arm (management ladder v2)",
    "R-ARM15": "counted-arm (management ladder v2; the register-80 "
               "concentration observation's variant)",
    "R-OP2": "counted-arm — the narrative trade layer's operator "
             "recipe",
    "R-NEXIT-EARLY": "counted-arm — atomic-trigger control, "
                     "pre-arming scope",
    "R-NEXIT-FULL": "counted-arm — atomic-trigger control, full-hold "
                    "scope",
    "R-NEXIT-SENT": "counted-arm — sentence exits (the "
                    "atoms-vs-sentences head-to-head)",
    "R-SCALP-H" + str(6): "counted-arm + INCUMBENT scalp geometry "
                          "(v0; the refinement sweep found zero "
                          "survivors — the incumbent stands)",
    "R-SCALP-H" + str(6) + "-REF": "counted-arm + INCUMBENT scalp "
                                   "geometry (refined-entry arm)",
    "R-H1-DELAY3": "counted-arm — H1 harvest program (register 128; "
                   "the register-60 entry-delay ticket)",
    "R-H1-DELAY10": "counted-arm — H1 harvest program (register 128; "
                    "the register-60 entry-delay ticket)",
    "R-H1-CONFIRM": "counted-arm — H1 harvest program (register 128; "
                    "the founding-sequence confirming print; NOT the "
                    "R2 refinement micro-loop)",
    "R-H1-OWNCURVE": "counted-arm — H1 harvest program (register 128; "
                     "own-curve stop, derivation frozen at build; the "
                     "ticket's time-exit half dropped per register 64)",
    "R-H1-KNIFE": "counted-arm — H1 harvest program (register 128; "
                  "the falling-knife guard, flip-guard family)",
    "R-OP1": "experiment — registered recipe, forward-graded outside "
             "the journal ladder",
    "R-FLIPGUARD": "experiment — the one staged narrative candidate, "
                   "forward-graded outside the journal ladder",
    "R-FIX": "experiment — illustrative-unratified (historical spec)",
    "R-ATR": "experiment — illustrative-unratified (historical spec)",
    "R-TRAIL": "experiment — illustrative-unratified (historical "
               "spec)",
    "R-TRAIL-ATR": "experiment — illustrative-unratified (historical "
                   "spec)",
}

# registered narrative-exit primitives -> plain-English glosses of the
# NAMES (the definitions live in the survey vocabulary, registers
# 73/78/81/82; the engine's exit-primitive registry is the one-home —
# normalize() rejects anything outside it)
EXIT_EN = {
    "opposing_structural_core": "an opposing structural core prints",
    "trend_flip": "the 1M trend flips against the position",
    "phase_transition": "a phase transition against the position",
    "opposing_signal_fire": "any other registered signal fires against "
                            "the position",
    "opposing_effort": "an opposing-effort event (survey vocabulary)",
    "absorption_event": "an absorption-class event against the "
                        "position (survey vocabulary)",
    "opposing_sentence_fire": "a minted composite sentence fires "
                              "against the position",
}

AUTH_KEYS_SCALP = ("recipes.py:_SCALP_STAGES",
                   "trade_layer.py:SCALP_VARIANTS",
                   "trade_layer.py:SCALP_SENTENCE")
AUTH_KEYS_ALL = ("recipes.py:RECIPE_SETS", "recipes.py:RECIPE_SET_VERSION")


def _ordinal(n):
    return {1: "previous", 2: "2nd-previous", 3: "3rd-previous"}.get(
        n, f"{n}th-previous")


def _off_en(c):
    if c["off_kind"] == "atr":
        return f"{c['off']:g}×ATR({c['off_tf']})"
    return f"{c['off']:g} pts"


def _stop_en(c):
    if c["kind"] == "atr_by_instr":
        per = "; ".join(f"{k} {v:g}" for k, v in sorted(c["map"].items()))
        return (f"k×ATR({c['tf']}) protective stop with k PER INSTRUMENT "
                f"— {per} (derived and frozen at build, register 128: "
                "the signal's own backtest mae60 p90 from "
                "excursion_geometry.json; never re-tuned)")
    if c["kind"] == "fixed_pts":
        return f"fixed stop {c['v']:g} pts from entry"
    if c["kind"] == "atr":
        return f"{c['k']:g}×ATR({c['tf']}) protective stop"
    if c["kind"] == "trail_nth":
        return (f"ratchet trail {_off_en(c)} beyond the extreme of the "
                f"{_ordinal(c['n'])} settled {c['bar_tf']} bar")
    if c["kind"] == "breakeven":
        off = f" +{c['off']:g}" if c["off"] else ""
        return f"stop to entry{off} (breakeven)"
    raise ValueError(c)


def _until_en(u):
    if u is None:
        return None
    if u[0] == "progress_atr":
        return (f"until MFE reaches +{u[1]:g}×ATR({u[2]}) "
                "(settled arming)")
    if u[0] == "progress_or_age":
        return (f"until MFE reaches +{u[1]:g}×ATR({u[2]}) or trade age "
                f"{u[3]:g} min (settled arming)")
    raise ValueError(u)


def _target_en(t, cfg_yaml):
    if t is None:
        return "no target — ride until an exit condition, the stop or "\
               "EOD"
    if t[0] == "fixed_pts":
        return f"target at entry +{t[1]:g} pts (touch = fill)"
    if t[0] == "atr":
        return f"target at entry +{t[1]:g}×ATR({t[2]}) (touch = fill)"
    if t[0] == "atr_haircut":
        return (f"resting target at entry +{t[1]:g}×ATR({t[2]}); FILL "
                f"only on a touch beyond the level by the {t[3]:g}-pt "
                "haircut (one home tick; per-instrument tick away — "
                "register 94); exit at the level; gap-opens past "
                "level+haircut fill at the open")
    raise ValueError(t)


def _fill_class(stages):
    if any(st["target"] and st["target"][0] == "atr_haircut"
           for st in stages):
        return ("OPTIMISTIC (register 65): the resting-target fill "
                "beyond the haircut — never compared to pessimistic "
                "rows without the class stated")
    return ("PESSIMISTIC (register 65): stop-fill conventions; the "
            "journal/ladder family")


def _entry_en(name, cfg_yaml, recipe=None):
    base = ("entry at the next 1M open after the fire (register 93 "
            "design shape); entries UNREFINED (register 70: refinement "
            "is per-family — the layer's choice, stated)")
    off = (recipe or {}).get("entry_offset_bars", 0)
    if off:
        return (f"entry DEFERRED {off} settled 1M bars past the fire — "
                f"the open of bar fire+{off + 1} (the register-128 "
                "entry-offset grammar component; 0 = the standard "
                "next-open entry)")
    if name == "R-H1-CONFIRM":
        ex = cfg_yaml["execution"]
        return ("entry on the FIRST CONFIRMING PRINT within "
                f"window={ex['window']:g} exec bars after the fire — a "
                "qualified TEST, or a structural no-supply-class print "
                "matching the fire direction (the founding two-chapter "
                "sequence, registry-cited); NO-ENTRY if the window "
                "expires (the -REF precedent; the transform lives in "
                "the trade layer). NOT the R2 refinement micro-loop — "
                "that verdict stands (register 70)")
    if name.endswith("-REF") and name in SCALP_VARIANTS:
        ex = cfg_yaml["execution"]
        return ("entry via the founding refinement micro-loop (config "
                f"execution, RULES Sec 9): within window={ex['window']:g} "
                "exec bars after the fire, enter on a 1M close "
                f"positioned beyond close_pos_trigger={ex['close_pos_trigger']:g} "
                "of its bar's range in the fire direction (mirrored for "
                f"shorts); fallback={ex['fallback']}")
    return base


def _scope_en(name):
    if name in H1_VARIANTS:
        return (f"the founding climax sentence only ({H1_SENTENCE} — "
                "register 128, the scalp scoping precedent); all four "
                "canonical instruments; re-fires deduped")
    if name in SCALP_VARIANTS:
        return (f"the scalp's own sentence only ({SCALP_SENTENCE}, the "
                "Q-chain's signal — register 94); all four canonical "
                "instruments; per-instrument spread and tick")
    if name in JOURNAL_VARIANTS:
        return ("every registered signal sentence (composites tagged "
                "is_composite); all four canonical instruments; "
                "re-fires deduped (register 77 clause 4)")
    return ("registered recipe outside the journal ladder — graded in "
            "recipe_performance.md on forward accrual")


def _section(name, recipe, cfg_yaml):
    stages = normalize(recipe)
    L = [f"## {name}", "",
         f"- **Status:** {STATUS.get(name, 'registered variant')}",
         f"- **Provenance:** {recipe.get('provenance', '(none stated)')} "
         f"— rendered from `RECIPE_SETS['{RECIPE_SET_VERSION}']`",
         f"- **Entry:** {_entry_en(name, cfg_yaml, recipe)}",
         f"- **Scope:** {_scope_en(name)}",
         f"- **Fill model:** {_fill_class(stages)}"]
    multi = len(stages) > 1
    for i, st in enumerate(stages, 1):
        head = (f"- **Stage {i}"
                + (f" ({_until_en(st['until'])})" if st["until"]
                   else (" (from arming, to exit)" if multi and i > 1
                         else ""))
                + ":**") if multi else "- **Mechanics:**"
        L.append(head)
        stops = [_stop_en(c) for c in st["stop"]]
        if len(stops) > 1:
            L.append("  - stop: tighter-of, ratchet-only — "
                     + "; ".join(stops))
        elif stops:
            L.append(f"  - stop: {stops[0]}")
        L.append(f"  - target: {_target_en(st['target'], cfg_yaml)}")
        if st["exit_on"]:
            L.append("  - exit when "
                     + "; or ".join(EXIT_EN[c[0]] for c in st["exit_on"])
                     + " (registered primitives — the one-home rule)")
        if st.get("reverse_on_exit"):
            L.append("  - reverses on exit (capability gated, "
                     "register 78)")
    L.append("- **EOD:** flat at end of day if still open (native to "
             "the simulate engine; every variant)")
    keys = AUTH_KEYS_ALL + (AUTH_KEYS_SCALP if name in SCALP_VARIANTS
                            else ())
    L.append("- **Authority:** " + ", ".join(f"`{k}`" for k in keys)
             + " (trails in the appendix)")
    L.append("")
    return L


def generate():
    cfg_yaml = yaml.safe_load(open(os.path.join(ROOT, "config.yaml")))
    rset = RECIPE_SETS[RECIPE_SET_VERSION]
    L = ["# VARIANTS — every registered recipe, from the structures "
         "the trade layer executes (GENERATED by backtest.variants_doc)",
         "",
         "Terms: [GLOSSARY.md](GLOSSARY.md). Regenerated every Part C "
         "run (register 116). **No hand-written numbers**: every value "
         f"renders from `RECIPE_SETS['{RECIPE_SET_VERSION}']` "
         "(backtest/recipes.py — the same structures, through the same "
         "normalize(), that simulate() executes), config.yaml, and the "
         "trade layer's scope constants; provenance strings are the "
         "recipe structures' own; authority trails cite "
         "[parameter_registry.md](parameter_registry.md). "
         "**TIMESTAMP CONVENTION (register 131, verified with a worked "
         "example): the journal's open_ts/close_ts are bar-CLOSE "
         "stamps — the simulate() time axis stamps each 1M bar by its "
         "close (Env.trail_ref derives a bar's open as ts − 1M), so "
         "the FILL is the OPEN of the bar that CLOSES at open_ts (the "
         "fire/trigger bar closes at open_ts − 1M). Enrichment MAE/MFE "
         "join on the same axis and are FILL-ANCHORED. Reading open_ts "
         "against the store's open-stamped bars mislocates the fill by "
         "one minute — the register-131 flag's anatomy.** ENFORCED: "
         "every variant in the journal has a section here or the suite "
         "fails (tests/test_variants_doc.py — the glossary pattern "
         "applied to strategies). Fill classes per register 65; "
         "nothing here re-grades anything.", "",
         "## The journal set (the trade layer's counted arms, in "
         "execution order)", "",
         " · ".join(f"[{v}](#{v.lower().replace('.', '')})"
                    for v in JOURNAL_VARIANTS), ""]
    for name in JOURNAL_VARIANTS:
        L += _section(name, rset[name], cfg_yaml)
    L += ["## Registered recipes outside the journal ladder "
          "(experiments and historical spec)", ""]
    for name in sorted(rset):
        if name in JOURNAL_VARIANTS:
            continue
        L += _section(name, rset[name], cfg_yaml)
    L += ["## Authority trails (docs/parameter_registry.md, curated "
          "map — verbatim)", ""]
    for k in AUTH_KEYS_ALL + AUTH_KEYS_SCALP:
        L.append(f"- `{k}` — {AUTHORITY.get(k, '(no trail; FLAGGED)')}")
    L.append("")
    return "\n".join(L)


def main():
    doc = generate()
    with open(DOC, "w") as f:
        f.write(doc)
    rset = RECIPE_SETS[RECIPE_SET_VERSION]
    print(f"VARIANTS reference -> docs/VARIANTS.md ({len(rset)} "
          f"variants; {len(JOURNAL_VARIANTS)} journal arms)")


if __name__ == "__main__":
    main()
