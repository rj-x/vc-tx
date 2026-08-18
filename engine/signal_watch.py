"""Dedicated signal module — THE ONE place candidate-hypothesis firing
conditions may live (register 31 revision + PURE-SIGNALS doctrine,
operator-ratified 2026-08-18: a hypothesis = a firing condition, nothing
else — no confirmation windows, no gates, no entries, no stops, no
management. Its only graded property: does a qualifying move follow, how
reliably, how early. Trade logic is a separate later layer, registered
separately for signals that earn one).

Import direction is enforced by test: NO decision path imports this module
— only the scoreboard reader and the live-loop attachment points may. A
firing condition PERCEIVES AND REPORTS.

A firing condition is a function
    (bar, ectx, sctx, feats, cores, structural, qualified, prev_structural)
      -> dir (+1/-1) or None
evaluated per 1M exec bar; prev_structural = the previous non-stub bar's
structural label (for sequence conditions). All six rows pre-registered
(trial log prereg_signal_rows_v1) with registry citations.
"""

ESTABLISHED_TREND_AGE = 10   # registry: T1d establishment cell (prereg_T3_build)
SEQUENCE_N = 2               # registry: S-sequence clause (prereg_signal_rows_v1)


def _s_h1(bar, ectx, sctx, feats, cores, structural, qualified, prev):
    """Climax prints, structural, bare (founding H1's pattern layer)."""
    return {"SELLING_CLIMAX": 1, "BUYING_CLIMAX": -1}.get(structural)


def _s_h2(bar, ectx, sctx, feats, cores, structural, qualified, prev):
    """Upthrust/spring prints, bare (founding H2's pattern layer)."""
    return {"UPTHRUST": -1, "SPRING": 1}.get(structural)


def _s_h3(bar, ectx, sctx, feats, cores, structural, qualified, prev):
    """Test prints (registry-evaluated TEST label; perception-layer state,
    no recipe). Direction = the recovery side (testcrit clause iii)."""
    if qualified != "TEST" or feats.close_pos is None:
        return None
    return 1 if feats.close_pos > 0.5 else -1


def _s_h4(bar, ectx, sctx, feats, cores, structural, qualified, prev):
    """No-supply / no-demand prints, structural, bare."""
    return {"NO_SUPPLY": 1, "NO_DEMAND": -1}.get(structural)


def _s_h7(bar, ectx, sctx, feats, cores, structural, qualified, prev):
    """Effortless sequence (dossier texture): SEQUENCE_N consecutive
    same-direction effortless prints; direction = continuation (the
    tracked-not-acted event-study sign)."""
    if structural == "EFFORTLESS_DECLINE" and prev == "EFFORTLESS_DECLINE":
        return -1
    if structural == "EFFORTLESS_ADVANCE" and prev == "EFFORTLESS_ADVANCE":
        return 1
    return None


def _s_t3b(bar, ectx, sctx, feats, cores, structural, qualified, prev):
    """T1d's measured conditions exactly (the signal-layer read of next
    cycle's question): trend-matched structural ND/NS in an established
    1M trend (trend_age >= ESTABLISHED_TREND_AGE). No phase gate."""
    d = {"NO_SUPPLY": 1, "NO_DEMAND": -1}.get(structural)
    if d and ectx.trend == d and ectx.trend_age >= ESTABLISHED_TREND_AGE:
        return d
    return None


FIRING_CONDITIONS = {
    "S-CLIMAX": _s_h1,
    "S-UPTHRUST-SPRING": _s_h2,
    "S-TEST": _s_h3,
    "S-ND-NS": _s_h4,
    "S-EFFORTLESS-SEQ": _s_h7,
    "S-T3B-ESTABLISHED": _s_t3b,
}


class SignalWatch:
    """Passive observer. attach() wraps the exec pipe's on_close to record
    fires; the wrapped call's inputs and outputs are untouched (invariance
    test: decisions AND narration bit-identical with tracking on/off)."""

    def __init__(self):
        self.fires = []          # {"ts", "name", "dir"}
        self._prev_structural = None

    def attach(self, engine):
        orig = engine.exec_pipe.on_close

        def observed(bar, ctx_tf=None, signal_ctx=None):
            out = orig(bar, ctx_tf=ctx_tf, signal_ctx=signal_ctx)
            if out is not None and not bar.is_stub:
                feats, cores, structural, qualified = out
                if feats.valid:
                    for name, fn in FIRING_CONDITIONS.items():
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
