"""MTF gating — RULES.md Sec 8. ctx_tf = the Context TF's ContextTracker,
whose state reflects its last CLOSED bar. `signal_close` = current Signal-TF
bar close.

Returns (permitted: bool, branch: str) so every gate decision is auditable;
the taken branch and any tag applied are logged by the caller.
"""

from .hypotheses import LONG, SHORT


def mtf_gate_permits(h, ctx_tf, signal_close, cfg):
    if ctx_tf is None:
        return False, "NO_CONTEXT"
    if h.spec == "H5":
        ok = _h5_gate(h, ctx_tf, cfg)
        return ok, ("H5_EXTENSION" if ok else "H5_BLOCKED")

    klass = "TREND" if h.spec in ("H3", "H4") else "REVERSAL"
    phase = ctx_tf.phase
    tol = (cfg.context.level_atr_mult * ctx_tf.atr) if ctx_tf.atr else None

    if klass == "TREND":
        if phase == "MARKUP" and h.dir == LONG:
            return True, "TREND_AGREEMENT"
        if phase == "MARKDOWN" and h.dir == SHORT:
            return True, "TREND_AGREEMENT"
        if h.spec == "H3" and phase == "RANGING" and tol is not None:
            boundary = ctx_tf.range_hi if h.dir == LONG else ctx_tf.range_lo
            if (boundary is not None and h.level is not None
                    and abs(h.level - boundary) <= tol):
                h.tag = "H3_RANGE_BREAK"
                return True, "H3_RANGE_BREAK"
        return False, "TREND_BLOCKED"

    # REVERSAL: (a) phase agreement first — REV_WITH_TREND
    if phase == "MARKUP" and h.dir == LONG:
        h.tag = "REV_WITH_TREND"
        return True, "REV_WITH_TREND"
    if phase == "MARKDOWN" and h.dir == SHORT:
        h.tag = "REV_WITH_TREND"
        return True, "REV_WITH_TREND"
    # (b) ranging at the opposing range extreme
    if phase == "RANGING" and tol is not None:
        extreme = ctx_tf.range_lo if h.dir == LONG else ctx_tf.range_hi
        if extreme is not None and abs(signal_close - extreme) <= tol:
            return True, "RANGING_EXTREME"
    # (c) post-climax with matching direction
    if phase == "POST_CLIMAX" and ctx_tf.post_climax_dir == h.dir:
        return True, "POST_CLIMAX_MATCH"
    # (d) strict mode off: opposing phase, higher strength bar
    if not cfg.gating.strict_mode:
        opposing = "MARKDOWN" if h.dir == LONG else "MARKUP"
        if phase == opposing and h.strength >= cfg.gating.relaxed_min_strength:
            return True, "RELAXED_OPPOSING"
    return False, "REVERSAL_BLOCKED"


def _h5_gate(h, ctx_tf, cfg):
    """Signed extension in the fade direction (v3.1 / prompt P4)."""
    hc = cfg.hypotheses.h5
    mean = ctx_tf.trend_mean(hc.ma_period)
    if mean is None or ctx_tf.atr is None or ctx_tf.close is None:
        return False
    ext = hc.extension_atr * ctx_tf.atr
    if h.dir == SHORT:                       # buying-climax fade
        return ctx_tf.close - mean > ext
    return mean - ctx_tf.close > ext         # mirror: selling-climax fade
