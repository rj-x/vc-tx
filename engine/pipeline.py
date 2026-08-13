"""Per-TF pipeline (steps 1-4 of the per-bar processing order) and the MTF
engine that enforces descending-TF processing at shared timestamps."""

from .broker import Broker
from .classifier import classify
from .context import ContextTracker
from .features import FeatureEngine
from .gating import mtf_gate_permits
from .hypotheses import HypothesisManager
from .narrative import Narrative
from .router import SignalRouter

_TF_MINUTES = {"1min": 1, "3min": 3, "5min": 5, "10min": 10, "15min": 15,
               "30min": 30, "1h": 60, "4h": 240, "1d": 1440}


class TFPipeline:
    def __init__(self, cfg, tf, narrative, manager=None):
        self.cfg = cfg
        self.tf = tf
        self.narrative = narrative
        self.fe = FeatureEngine(cfg)
        self.ctx = ContextTracker(cfg, tf)
        self.manager = manager            # Signal TF only

    def on_close(self, bar, ctx_tf=None):
        # 1. classify with context AS OF THE PREVIOUS bar's close
        feats = self.fe.update(bar)
        cores, structural, qualified = classify(bar, feats, self.ctx, self.cfg)
        if feats.valid and not bar.is_stub:
            # EVERY classified bar emits a LABEL event (audit completeness);
            # label/structural are null for bars matching no core
            self.narrative.log("LABEL", ts=bar.ts, tf=self.tf,
                               label=qualified, structural=structural,
                               segment=bar.segment)
        # 2. update context (stub bars update context but nothing else)
        n_phase = len(self.ctx.phase_log)
        n_swings = getattr(self.ctx, 'swing_count', 0)
        self.ctx.update(bar, feats, qualified)
        if self.cfg._d.get("debug", {}).get("structure"):
            new_n = getattr(self.ctx, 'swing_count', 0) - n_swings
            for s in (self.ctx.swings[-new_n:] if new_n else []):
                self.narrative.log("SWING_CONFIRMED", ts=bar.ts, tf=self.tf,
                                   swing=s["type"], price=s["price"],
                                   occurred_idx=s["idx"],
                                   confirmed_idx=self.ctx.idx,
                                   lag_bars=self.ctx.idx - s["idx"],
                                   across_gap=s.get("confirmed_across_gap",
                                                    False))
            c = self.ctx
            self.narrative.log("PHASE_EVAL", ts=bar.ts, tf=self.tf,
                               trend=c.trend, trend_age=c.trend_age,
                               swings_wo_extreme=c._swings_wo_extreme,
                               bars_since_extreme=c.idx - c._last_extreme_idx,
                               ranging_if=f">={self.cfg.context.ranging_swings}sw|"
                                          f">={self.cfg.context.ranging_bars}b",
                               post_climax=bool(c.post_climax),
                               verdict=c.phase)
        for entry in self.ctx.phase_log[n_phase:]:
            _idx, phase, trigger = entry[0], entry[1], entry[2]
            payload = {"phase": phase, "trigger": trigger}
            if phase == "POST_CLIMAX":
                payload["direction"] = self.ctx.post_climax_dir
            payload["segment"] = bar.segment
            self.narrative.log("PHASE", ts=bar.ts, tf=self.tf, **payload)
        pb = self.ctx.pullback
        if (pb and not pb.get("expanded_logged")
                and pb["max_rel_vol"] >= self.cfg.hypotheses.h4.expand_mult):
            pb["expanded_logged"] = True
            self.narrative.log("PULLBACK_EXPANDED", ts=bar.ts, tf=self.tf,
                               max_rel_vol=round(pb["max_rel_vol"], 2))
        # 3./4. hypotheses + signals (skipped entirely for stub bars)
        if self.manager is not None and not bar.is_stub:
            self.manager.step(bar, feats, cores, structural, qualified,
                              self.ctx, ctx_tf)
        return feats, cores, structural, qualified


class MTFEngine:
    """Wires Context/Signal/Execution TFs. Callers feed closed bars via
    process(); bars sharing a timestamp are processed in descending TF
    order (RULES Sec 1)."""

    def __init__(self, cfg, embargo_fn=None, eod_fn=None, tick_size=1.0,
                 point_value=1.0, narrative_only=False):
        self.cfg = cfg
        self.narrative = Narrative()
        self.broker = Broker(cfg, self.narrative, eod_fn=eod_fn,
                             point_value=point_value, tick_size=tick_size,
                             inert=narrative_only)
        self.router = SignalRouter(cfg, self.narrative,
                                   embargo_fn=embargo_fn, tick_size=tick_size,
                                   broker=self.broker,
                                   narrative_only=narrative_only)
        ctx_tf = cfg.mtf.context_tf
        sig_tf = cfg.mtf.signal_tf
        self.ctx_ratio = max(1, _TF_MINUTES[ctx_tf] // _TF_MINUTES[sig_tf])
        self.context_pipe = TFPipeline(cfg, ctx_tf, self.narrative)
        gate = (mtf_gate_permits if not cfg.ablation.no_gating
                else (lambda h, c, s, cf: (True, "ABLATION_NO_GATE")))
        manager = HypothesisManager(cfg, self.ctx_ratio, self.narrative,
                                    self.router, gate)
        self.signal_pipe = TFPipeline(cfg, sig_tf, self.narrative,
                                      manager=manager)
        # ruling 2026-08-13 (register 10): exec-TF classification as
        # OBSERVATIONAL instrumentation — labels emitted, nothing consumes
        # them (no manager); closes the Part 5 identical-pipeline deviation
        self.exec_pipe = TFPipeline(cfg, cfg.mtf.execution_tf, self.narrative)
        self.manager = manager

    def process(self, ts, context_bar=None, signal_bar=None, exec_bar=None,
                exec_quote=None):
        """All bars passed must close at `ts`. Descending TF order:
        context -> signal -> execution."""
        if context_bar is not None:
            self.context_pipe.on_close(context_bar)
        if signal_bar is not None:
            # scheduled direct entries execute at the NEXT signal bar's open,
            # i.e. when that bar arrives — before its close is processed
            self.router.on_signal_open(signal_bar)
            self.signal_pipe.on_close(signal_bar, ctx_tf=self.context_pipe.ctx)
            if self.broker.position is not None:
                opposing = any(d != self.broker.position["dir"]
                               for d in self.manager.last_confirm_dirs)
                self.broker.on_signal_close(signal_bar, self.context_pipe.ctx,
                                            opposing)
        if exec_bar is not None:
            self.exec_pipe.on_close(exec_bar)     # observational labels only
            self.broker.set_quote(exec_quote)     # cash leg (cash_cfd mode)
            self.broker.on_exec_bar(exec_bar)     # exits before new entries
            self.router.on_exec_bar(exec_bar)
