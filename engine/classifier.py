"""BarClassifier — structural cores and qualified labels (Part 2 + RULES Sec 0).

Structural cores are bar-anatomy-only predicates. The primary structural
label is categorical (priority-ordered). Context qualifiers are applied at
point of use: `classify()` returns (cores, primary_structural,
primary_qualified) where the qualified label requires context state AS OF
THE PREVIOUS BAR'S CLOSE (the caller passes context before updating it).
"""

from .testcrit import test_criteria

# structural core names
CORES = [
    "SELLING_CLIMAX", "BUYING_CLIMAX", "UPTHRUST", "SPRING", "ABSORPTION",
    "NO_SUPPLY", "NO_DEMAND", "VALIDATED_ADVANCE", "EFFORTLESS_ADVANCE",
    "VALIDATED_DECLINE", "EFFORTLESS_DECLINE", "APATHY",
]

# priority for the categorical primary label (first match wins)
_PRIORITY = [
    "SELLING_CLIMAX", "BUYING_CLIMAX", "UPTHRUST", "SPRING", "ABSORPTION",
    "NO_SUPPLY", "NO_DEMAND", "VALIDATED_ADVANCE", "VALIDATED_DECLINE",
    "EFFORTLESS_ADVANCE", "EFFORTLESS_DECLINE", "APATHY",
]


def structural_cores(feats, lcfg):
    """All structural-core booleans for a bar. feats must be valid."""
    f = feats
    wide = f.rel_spread_pct is not None and f.rel_spread_pct >= lcfg.wide_spread_pctile
    narrow = f.rel_spread_pct is not None and f.rel_spread_pct <= lcfg.narrow_spread_pctile
    high_vol = f.rel_volume is not None and f.rel_volume >= lcfg.high_volume_mult
    low_vol = f.rel_volume is not None and f.rel_volume <= lcfg.low_volume_mult
    climactic = (f.rel_volume is not None
                 and f.rel_volume >= lcfg.climax_vol_mult
                 and f.rel_spread_pct is not None
                 and f.rel_spread_pct >= lcfg.climax_spread_pctile
                 and f.vol_is_trailing_max)
    up, down = f.direction > 0, f.direction < 0
    return {
        "SELLING_CLIMAX": climactic and down,
        "BUYING_CLIMAX": climactic and up,
        "UPTHRUST": (wide and high_vol and f.upper_wick_frac >= lcfg.wick_frac_min
                     and f.close_pos < lcfg.upthrust_close_pos),
        "SPRING": (wide and high_vol and f.lower_wick_frac >= lcfg.wick_frac_min
                   and f.close_pos > 1 - lcfg.upthrust_close_pos),
        "ABSORPTION": narrow and high_vol,
        "NO_SUPPLY": down and narrow and low_vol,
        "NO_DEMAND": up and narrow and low_vol,
        "VALIDATED_ADVANCE": (up and wide and f.close_pos > lcfg.close_pos_hi
                              and high_vol),
        "EFFORTLESS_ADVANCE": (up and wide and f.close_pos > lcfg.close_pos_hi
                               and not high_vol),
        "VALIDATED_DECLINE": (down and wide and f.close_pos < lcfg.close_pos_lo
                              and high_vol),
        "EFFORTLESS_DECLINE": (down and wide and f.close_pos < lcfg.close_pos_lo
                               and not high_vol),
        "APATHY": narrow and low_vol and 0.35 <= f.close_pos <= 0.65,
    }


def classify(bar, feats, ctx_prev, cfg):
    """Returns (cores: dict, structural: str|None, qualified: str|None).

    `ctx_prev` = ContextTracker state as of the PREVIOUS bar's close
    (per-bar processing order step 1 — the classifier never sees context
    updated with the current bar). Stub bars and warmup bars yield no labels.
    """
    if not feats.valid or bar.is_stub:
        return {}, None, None
    lcfg = cfg.labels
    cores = structural_cores(feats, lcfg)

    structural = next((n for n in _PRIORITY if cores.get(n)), None)

    # TEST label: registry-based — a probe of a prior climax/spring extreme
    # (diagnostics/event-study; hypothesis confirms use the same criteria
    # anchored to their own signature via engine.testcrit).
    is_test = False
    for sig in ctx_prev.signature_registry:
        if test_criteria(bar, feats, sig["extreme"], sig["rel_volume"],
                         sig["dir"], ctx_prev.atr, cfg):
            is_test = True
            break

    qualified = None
    if structural == "SELLING_CLIMAX":
        if ctx_prev.trend == -1 and ctx_prev.trend_age >= lcfg.extended_trend_bars:
            qualified = "POTENTIAL_SELLING_CLIMAX"
    elif structural == "BUYING_CLIMAX":
        if ctx_prev.trend == 1 and ctx_prev.trend_age >= lcfg.extended_trend_bars:
            qualified = "POTENTIAL_BUYING_CLIMAX"
    elif structural == "UPTHRUST":
        if (cfg.ablation.no_location or ctx_prev.after_rally
                or ctx_prev.near_resistance or ctx_prev.at_range_high):
            qualified = "UPTHRUST"
    elif structural == "SPRING":
        if (cfg.ablation.no_location or ctx_prev.after_decline
                or ctx_prev.near_support or ctx_prev.at_range_low):
            qualified = "SPRING"
    elif structural == "ABSORPTION":
        qualified = "ABSORPTION"        # level proximity applied by H3 spawn
    elif structural == "NO_SUPPLY":
        if ctx_prev.phase == "MARKUP" and ctx_prev.impulse_reaction == "REACTION":
            qualified = "NO_SUPPLY"
    elif structural == "NO_DEMAND":
        if ctx_prev.phase == "MARKDOWN" and ctx_prev.impulse_reaction == "REACTION":
            qualified = "NO_DEMAND"
    elif structural is not None:
        qualified = structural           # advance/decline/apathy: no qualifier

    if is_test and qualified is None:
        qualified = "TEST"

    return cores, structural, qualified
