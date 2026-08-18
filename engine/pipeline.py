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

    def _track_session_extremes(self, bar):
        st = getattr(self, "_sess", None)
        if st is None or st["sid"] != bar.session_id:
            self._sess = {"sid": bar.session_id, "hi": bar.high, "lo": bar.low,
                          "prior_hi": st["hi"] if st else None,
                          "prior_lo": st["lo"] if st else None}
        else:
            st["hi"] = max(st["hi"], bar.high)
            st["lo"] = min(st["lo"], bar.low)

    def _location(self, px, signal_ctx):
        """Nearest of session/prior-session extremes and Signal-TF swing
        levels; signed distance (px - ref) in pts and Signal-TF ATR.
        Review-surface enrichment only (opportunity ledger)."""
        st = getattr(self, "_sess", None)
        cands = {}
        if st:
            cands = {"session_high": st["hi"], "session_low": st["lo"],
                     "prior_session_high": st["prior_hi"],
                     "prior_session_low": st["prior_lo"]}
        if signal_ctx is not None and signal_ctx.levels:
            lv, _ = signal_ctx.nearest_level(px)
            cands["signal_swing_level"] = lv
        cands = {k: v for k, v in cands.items() if v is not None}
        if not cands:
            return {}
        ref = min(cands, key=lambda k: abs(px - cands[k]))
        d = px - cands[ref]
        atr = signal_ctx.atr if signal_ctx is not None else None
        return {"location_ref": ref,
                "location_level": float(round(cands[ref], 1)),
                "dist_pts": float(round(d, 1)),
                "dist_signal_atr": (float(round(d / atr, 2))
                                    if atr else None)}

    def on_close(self, bar, ctx_tf=None, signal_ctx=None):
        # 1. classify with context AS OF THE PREVIOUS bar's close
        feats = self.fe.update(bar)
        cores, structural, qualified = classify(bar, feats, self.ctx, self.cfg)
        if signal_ctx is not None:          # exec pipe: session extremes
            self._track_session_extremes(bar)
        if feats.valid and not bar.is_stub:
            # EVERY classified bar emits a LABEL event (audit completeness);
            # label/structural are null for bars matching no core
            # rv on structural-only labels too (ruling 2026-08-18, register
            # 28): additive/observational — no decision path consumes a
            # label's rv post-emission (verified); cures the migration
            # instrument's measured-quiet/unmeasured conflation
            extra = ({"open": float(bar.open), "high": float(bar.high),
                      "low": float(bar.low), "close": float(bar.close),
                      "volume": float(bar.volume),
                      "rel_volume": (float(round(feats.rel_volume, 2))
                                     if feats.rel_volume else None)}
                     if (qualified or structural) else {})
            if qualified and signal_ctx is not None:
                px = bar.high if qualified == "UPTHRUST" else (
                    bar.low if qualified == "SPRING" else bar.close)
                extra.update(self._location(px, signal_ctx))
            self.narrative.log("LABEL", ts=bar.ts, tf=self.tf,
                               label=qualified, structural=structural,
                               segment=bar.segment, **extra)
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
        # TF-ladder observational classification (2026-08-14): classifier +
        # context only, no hypothesis manager, structurally (item-10 scoping)
        self.ladder_pipes = {}
        if cfg.session_model.get("ladder"):
            stack = {ctx_tf, sig_tf, cfg.mtf.execution_tf}
            for tf in ("1h", "30min", "15min", "5min", "3min", "1min"):
                if tf not in stack:
                    self.ladder_pipes[tf] = TFPipeline(cfg, tf, self.narrative)
        self.manager = manager

    def process(self, ts, context_bar=None, signal_bar=None, exec_bar=None,
                exec_quote=None, ladder_bars=None):
        """All bars passed must close at `ts`. Descending TF order:
        context -> ladder (descending, observational) -> signal -> execution."""
        if context_bar is not None:
            self.context_pipe.on_close(context_bar)
        if ladder_bars:
            for tf in ("1h", "30min", "15min", "5min", "3min", "1min"):
                b = ladder_bars.get(tf)
                if b is not None and tf in self.ladder_pipes:
                    self.ladder_pipes[tf].on_close(b)
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
            sc = self.signal_pipe.ctx
            lows = [x for x in sc.swings if x["type"] == "L"]
            highs = [x for x in sc.swings if x["type"] == "H"]
            self.broker.signal_state = {
                "atr": sc.atr,
                "swings": {"low": lows[-1]["price"] if lows else None,
                           "high": highs[-1]["price"] if highs else None}}
        if exec_bar is not None:
            self.exec_pipe.on_close(exec_bar,     # observational labels only
                                    signal_ctx=self.signal_pipe.ctx)
            self.broker.set_quote(exec_quote)     # cash leg (cash_cfd mode)
            self.broker.on_exec_bar(exec_bar)     # exits before new entries
            self.router.on_exec_bar(exec_bar)
