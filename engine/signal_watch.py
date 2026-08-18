"""Dedicated signal module — THE ONE place candidate-hypothesis (H6+)
firing conditions may live (register 31 revision, candidate-guard
amendment). Import direction is enforced by test: NO decision path imports
this module — only the scoreboard reader and the live-loop attachment
points may. A firing condition PERCEIVES AND REPORTS; it can never touch
gating, spawning, routing, or the broker.

A firing condition is a pure function (bar, ectx, sctx, feats, cores,
structural, qualified) -> dir (+1/-1) or None, keyed by hypothesis name.
Signal rows begin the day a firing condition is defined here — none are
defined yet; the registry below is intentionally empty.
"""

# name -> callable; empty until a candidate's firing condition is defined
# alongside its registration (docs/hypothesis_lifecycle.md stage 4)
FIRING_CONDITIONS = {}


class SignalWatch:
    """Passive observer. attach() wraps the exec pipe's on_close to record
    fires; the wrapped call's inputs and outputs are untouched (invariance
    test: decisions AND narration bit-identical with tracking on/off)."""

    def __init__(self):
        self.fires = []          # {"ts", "name", "dir"}

    def attach(self, engine):
        orig = engine.exec_pipe.on_close

        def observed(bar, ctx_tf=None, signal_ctx=None):
            out = orig(bar, ctx_tf=ctx_tf, signal_ctx=signal_ctx)
            if out is not None and not bar.is_stub:
                feats, cores, structural, qualified = out
                for name, fn in FIRING_CONDITIONS.items():
                    d = fn(bar, engine.exec_pipe.ctx, signal_ctx,
                           feats, cores, structural, qualified)
                    if d:
                        self.fires.append({"ts": bar.ts, "name": name,
                                           "dir": int(d)})
            return out
        engine.exec_pipe.on_close = observed
        return self
