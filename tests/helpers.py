"""Scenario rig for synthetic verification (RULES.md Sec 10).

Bars are hand-built; timestamps are minutes. Signal TF = 15min, Context TF =
1h (ratio 4), Execution TF = 1min. Config overrides shrink warmup windows so
scenarios stay hand-traceable — thresholds are config, the LOGIC under test
is not changed by them.
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from engine.bars import Bar                              # noqa: E402
from engine.config import load                           # noqa: E402
from engine.pipeline import MTFEngine                    # noqa: E402

SCENARIO_OVERRIDES = {
    "features.baseline_mode": "simple",
    "features.simple_baseline_window": 30,
    "features.min_baseline_obs": 8,
    "context.swing_k": 1,
    "context.atr_period": 5,
    "context.ranging_swings": 4,
    "context.ranging_bars": 15,
    "context.post_climax_bars": 8,
    "context.move_lookback": 10,
    "context.st_window": 3,
    "context.new_low_lookback": 30,
    "context.signature_registry_max_age": 20,
    "labels.extended_trend_bars": 6,
    "labels.climax_lookback": 10,
    "hypotheses.h4.established_min_bars": 4,
    "execution.enabled": False,
    "execution_vehicle.mode": "direct",
}


def scenario_cfg(extra=None):
    cfg = load()
    for k, v in {**SCENARIO_OVERRIDES, **(extra or {})}.items():
        cfg = cfg.override(k, v)
    return cfg


class Rig:
    def __init__(self, extra_cfg=None):
        self.cfg = scenario_cfg(extra_cfg)
        self.embargo_after = None
        self.engine = MTFEngine(self.cfg, embargo_fn=self._embargo)
        self.t = 0
        self.nsig = 0
        self.ctx_gen = None            # callable -> (o,h,l,c,v) | None
        self.script = []               # every process() call, for replays

    def _embargo(self, ts):
        return self.embargo_after is not None and ts >= self.embargo_after

    # ------------------------------------------------------------- feeding

    def sig(self, o, h, l, c, v, ctx=None):
        """Feed one Signal-TF bar (auto ts += 15). Every 4th signal bar a
        Context-TF bar closes at the SAME timestamp — supplied explicitly
        via `ctx`, or drawn from self.ctx_gen."""
        self.t += 15
        self.nsig += 1
        cb = None
        vals = ctx
        if vals is None and self.ctx_gen is not None and self.nsig % 4 == 0:
            vals = self.ctx_gen()
        if vals is not None:
            cb = Bar(self.t, *vals, tf="1h")
        sb = Bar(self.t, o, h, l, c, v, tf="15min")
        self.script.append((self.t, cb, sb, None))
        self.engine.process(self.t, context_bar=cb, signal_bar=sb)

    def flat(self, n, px=100.0, v_lo=90, v_hi=110):
        """Baseline bars: alternating mild spreads/volumes around px."""
        for i in range(n):
            wide = i % 2
            s = 1.1 if wide else 0.9
            o = px - 0.2 if wide else px + 0.2
            c = px + 0.2 if wide else px - 0.2
            self.sig(o, max(o, c) + s / 2, min(o, c) - s / 2, c,
                     v_hi if wide else v_lo)

    def execs(self, bars):
        """Feed Execution-TF bars between signal closes (ts = t+1, t+2, ...)."""
        for i, (o, h, l, c, v) in enumerate(bars, 1):
            eb = Bar(self.t + i, o, h, l, c, v, tf="1min")
            self.script.append((self.t + i, None, None, eb))
            self.engine.process(self.t + i, exec_bar=eb)

    # ------------------------------------------------------------ inspection

    @property
    def events(self):
        return self.engine.narrative.events

    def of(self, *types):
        return [e for e in self.events if e["type"] in types]

    @property
    def sctx(self):
        return self.engine.signal_pipe.ctx

    @property
    def cctx(self):
        return self.engine.context_pipe.ctx

    @property
    def router(self):
        return self.engine.router

    def dump(self, path=None):
        text = self.engine.narrative.human()
        if path:
            with open(path, "w") as f:
                f.write(text + "\n")
        return text


def sig_zigzag(rig, px, cycles, up=False, vol=100):
    """Signal-TF trend with confirmable swings (k=1): swing highs at each
    cycle's first bar, swing lows at the second (mirrored for up)."""
    for _ in range(cycles):
        if not up:
            bars = [(px, px + 0.3, px - 2.2, px - 2.0),
                    (px - 2.0, px - 1.8, px - 4.2, px - 4.0),
                    (px - 4.0, px - 2.3, px - 4.1, px - 2.5)]
            px -= 2.5
        else:
            bars = [(px, px + 2.2, px - 0.3, px + 2.0),
                    (px + 2.0, px + 4.2, px + 1.8, px + 4.0),
                    (px + 4.0, px + 4.1, px + 2.3, px + 2.5)]
            px += 2.5
        for (o, h, l, c) in bars:
            rig.sig(o, h, l, c, vol)
    return px


def zigzag_gen(start, up=False, vol=100, scale=2.0):
    """Context-TF zigzag generator (same shape, scaled)."""
    state = {"px": start, "queue": []}

    def gen():
        if not state["queue"]:
            px = state["px"]
            s = scale
            if not up:
                state["queue"] = [
                    (px, px + 0.3 * s, px - 2.2 * s, px - 2.0 * s),
                    (px - 2.0 * s, px - 1.8 * s, px - 4.2 * s, px - 4.0 * s),
                    (px - 4.0 * s, px - 2.3 * s, px - 4.1 * s, px - 2.5 * s)]
                state["px"] = px - 2.5 * s
            else:
                state["queue"] = [
                    (px, px + 2.2 * s, px - 0.3 * s, px + 2.0 * s),
                    (px + 2.0 * s, px + 4.2 * s, px + 1.8 * s, px + 4.0 * s),
                    (px + 4.0 * s, px + 4.1 * s, px + 2.3 * s, px + 2.5 * s)]
                state["px"] = px + 2.5 * s
        o, h, l, c = state["queue"].pop(0)
        return (o, h, l, c, vol)

    return gen


def stair(start, deltas_cycle, spread=1.0, vol=100):
    """Generator factory: context-bar staircase. deltas_cycle e.g.
    (-2, -2, +1) for a zigzag downtrend with confirmable swings."""
    state = {"px": start, "i": 0}

    def gen():
        d = deltas_cycle[state["i"] % len(deltas_cycle)]
        state["i"] += 1
        o = state["px"]
        c = o + d
        state["px"] = c
        return (o, max(o, c) + spread / 2, min(o, c) - spread / 2, c, vol)

    return gen
