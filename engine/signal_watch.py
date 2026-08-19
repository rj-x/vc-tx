"""Dedicated signal module — THE ONE place hypothesis firing conditions
may live (register 31/34: PURE-SIGNALS doctrine; register 35: canonical
hypothesis register). Every row's ID is S-H<n> and must exist in
docs/hypothesis_register.md with status signal-live — the scoreboard
refuses anything else (test-enforced).

Import direction is enforced by test: NO decision path imports this module.
A firing condition PERCEIVES AND REPORTS.

A firing condition is a callable
    (bar, ectx, sctx, feats, cores, structural, qualified, prev_structural)
      -> dir (+1/-1) or None
evaluated per 1M exec bar. A CLASS registered here is instantiated fresh at
attach (per-run state; nothing leaks between runs).
"""

ESTABLISHED_TREND_AGE = 10   # registry: T1d establishment cell (prereg_T3_build)
SEQUENCE_N = 2               # registry: sequence clause (prereg_signal_rows_v1)
H9_CHAIN_DEPTH_MIN = 2       # registry: operator pre-registration 2026-08-19

# row-declaration tables (this module is the one permitted home for
# hypothesis identifiers; the scoreboard imports these):
EVENT_DERIVED_ROWS = {"S-H9"}     # produced from replay events, not per-bar
AGNOSTIC_ROWS = {"S-H8"}          # graded either-direction (register 36)
DUAL_GRADED = {"S-H7"}            # graded in BOTH modes (register 36)
# ONE firing condition, TWO gradings (register 37): the value row's fires
# ARE the key row's fires, copied — never independently computed, never
# double-counted as two signals
DERIVED_FIRES = {"S-H8": "S-H2"}
# narrative-condition primitives a recipe stage may reference (register 42e;
# the one-home rule: primitives are DECLARED here, grammar validates against
# this set). CAPABILITY ONLY until the excursion study's conditional cut
# reports — no narrative recipe may be registered before then.
NARRATIVE_EXIT_PRIMITIVES = ("opposing_structural_core", "trend_flip",
                             "phase_transition", "opposing_signal_fire")
# co-fire census family partition (register 45, operator-set; the one-home
# rule keeps hypothesis identifiers out of the census reader)
COFIRE_FAMILIES = {"event": ("S-H1", "S-H2"), "texture": ("S-H4", "S-H7"),
                   "structure": ("S-H3", "S-H9")}


def _s_h1(bar, ectx, sctx, feats, cores, structural, qualified, prev):
    """H1 bare pattern: climax print -> reversal against the climax."""
    return {"SELLING_CLIMAX": 1, "BUYING_CLIMAX": -1}.get(structural)


def _s_h2(bar, ectx, sctx, feats, cores, structural, qualified, prev):
    """H2 bare pattern: failed probe beyond an extreme -> reversal."""
    return {"UPTHRUST": -1, "SPRING": 1}.get(structural)


class _SH3:
    """H3 bare pattern: absorption cluster at a swing level -> breakout
    THROUGH the level. Founding cluster params cited from config
    (h3.min_absorption_bars, h3.cluster_window, context.level_atr_mult,
    context.level_identity_atr_frac); spawn layer only, no zone/recipe."""

    def __init__(self):
        self._recs = []          # (idx, level)

    def __call__(self, bar, ectx, sctx, feats, cores, structural, qualified,
                 prev):
        cfg = ectx.cfg
        w = cfg.hypotheses.h3.cluster_window
        self._recs = [r for r in self._recs if ectx.idx - r[0] < w]
        if ectx.atr is None or not cores.get("ABSORPTION"):
            return None
        mid = (bar.high + bar.low) / 2
        lv, dist = ectx.nearest_level(mid)
        if lv is None or dist > cfg.context.level_atr_mult * ectx.atr:
            return None
        self._recs.append((ectx.idx, lv))
        tol = cfg.context.level_identity_atr_frac * ectx.atr
        group = [r for r in self._recs if abs(r[1] - lv) <= tol]
        if len(group) < cfg.hypotheses.h3.min_absorption_bars:
            return None
        return 1 if lv >= ectx.close else -1


def _s_h4(bar, ectx, sctx, feats, cores, structural, qualified, prev):
    """H4 bare pattern: QUALIFIED no-supply/no-demand — the classifier's
    qualification (trending phase + pullback) IS the founding trend-pullback
    context, computed mechanically. Direction = trend resumption."""
    return {"NO_SUPPLY": 1, "NO_DEMAND": -1}.get(qualified)


def _s_h7(bar, ectx, sctx, feats, cores, structural, qualified, prev):
    """H7 claim direction (REVERSAL — quiet weakness as disguised
    accumulation, candidate register verbatim): SEQUENCE_N consecutive
    effortless prints -> fire AGAINST the drift. BARE VARIANT: the
    registered anatomy's session-extreme proximity is a walk-forward free
    parameter and is NOT applied here (audit flag in the register)."""
    if structural == "EFFORTLESS_DECLINE" and prev == "EFFORTLESS_DECLINE":
        return 1
    if structural == "EFFORTLESS_ADVANCE" and prev == "EFFORTLESS_ADVANCE":
        return -1
    return None


def _s_h10(bar, ectx, sctx, feats, cores, structural, qualified, prev):
    """H10 (T1d's measured conditions exactly): trend-matched structural
    ND/NS in an established 1M trend -> continuation. H4 variant
    re-anchored to 1M; no phase gate."""
    d = {"NO_SUPPLY": 1, "NO_DEMAND": -1}.get(structural)
    if d and ectx.trend == d and ectx.trend_age >= ESTABLISHED_TREND_AGE:
        return d
    return None


FIRING_CONDITIONS = {
    "S-H1": _s_h1,
    "S-H2": _s_h2,
    "S-H3": _SH3,                # class: fresh instance per attach
    "S-H4": _s_h4,
    "S-H7": _s_h7,
    "S-H10": _s_h10,
}


class SignalWatch:
    """Passive observer. attach() wraps the exec pipe's on_close to record
    fires; the wrapped call's inputs and outputs are untouched (invariance
    test: decisions AND narration bit-identical with tracking on/off)."""

    def __init__(self):
        self.fires = []          # {"ts", "name", "dir"}
        self._prev_structural = None

    def attach(self, engine):
        conds = {n: (f() if isinstance(f, type) else f)
                 for n, f in FIRING_CONDITIONS.items()}
        orig = engine.exec_pipe.on_close

        def observed(bar, ctx_tf=None, signal_ctx=None):
            out = orig(bar, ctx_tf=ctx_tf, signal_ctx=signal_ctx)
            if out is not None and not bar.is_stub:
                feats, cores, structural, qualified = out
                if feats.valid:
                    for name, fn in conds.items():
                        d = fn(bar, engine.exec_pipe.ctx, signal_ctx, feats,
                               cores, structural, qualified,
                               self._prev_structural)
                        if d:
                            self.fires.append({"ts": bar.ts, "name": name,
                                               "dir": int(d)})
                    self._prev_structural = structural
            return out
        engine.exec_pipe.on_close = observed
        return self
