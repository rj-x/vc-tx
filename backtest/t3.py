"""T3 — EXPLORATORY, NOT VALIDATION (prereg_T3_build, hash c1d826a919050364).

H4-mirror on the 1M execution TF: the engine's own H4 lifecycle (spawn from
trend-consistent NO_SUPPLY/NO_DEMAND prints, TREND_RESUMPTION confirm,
structural-break refute) driven one rung down the ladder, with establishment
anchored to the 1M trend per T1d's cell (trend-matched, trend_age >= 10).

Construction discipline (lab-harness/engine-guard boundary, the prereg's
first implementation step):
  - engine/ files are NOT modified; boundary_check() refuses to run if the
    engine tree differs from HEAD.
  - Every engine class is used as-is: HypothesisManager (one subclass
    overriding ONLY _spawn), SignalRouter, Broker, Narrative, the gate.
  - The one engine runs the standard system untouched; T3 attaches by
    wrapping MTFEngine.process and reading the exec pipe's classification
    output. T3 keeps its own narrative/router/broker (parallel exploratory
    book) so the standard system's events and trades are uncontaminated.

Mirror mapping (documented deviations from the 15M system, all structural):
  signal TF -> 1min, context TF -> 15min (signal ctx), ctx_ratio = 15.
  Everything else — confirm window, pending-gate window multiple, strength
  ledger, gate branches, refinement micro-loop, stops, exits, EOD/embargo,
  cash-CFD fills — is the frozen config verbatim.

Read criteria (fixed in advance): funnel progression + per-trade R
distribution; trend-indicative only; expected n single digits.
"""

import argparse
import json
import os
import subprocess

import pandas as pd

from engine.broker import Broker
from engine.config import load
from engine.gating import mtf_gate_permits
from engine.hypotheses import HypothesisManager
from engine.narrative import Narrative
from engine.pipeline import MTFEngine
from engine.router import SignalRouter
from backtest.loop import run_backtest, session_fns
from backtest.metrics import breakdowns

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "reports", "lab")
TRIAL_LOG = os.path.join(OUT, "trial_log.jsonl")

ESTABLISHED_TREND_AGE = 10      # T1d establishment cell (age>=10), pinned

FUNNEL_EVENTS = [
    "SPAWNED", "BLOCKED_SPAWN", "CONFIRM", "CONFIRM_UNDERSTRENGTH",
    "GATE", "CONFIRMED_PENDING_GATE", "GATE_RECHECK", "GRADUATED",
    "GRADUATION_CONFLICT", "SIGNAL_UNACTED_CONFLICT",
    "SIGNAL_UNACTED_IN_POSITION", "REFINEMENT_STARTED",
    "REFINEMENT_TRIGGERED", "REFINEMENT_FALLBACK",
    "REFINEMENT_CANCELLED_REFUTED", "REFINEMENT_CANCELLED_OPPOSED",
    "REFINEMENT_ABANDONED_NO_TRIGGER", "REFINEMENT_ABANDONED_EMBARGO",
    "ENTRY_REFINED", "ENTRY_FALLBACK", "ENTRY_DIRECT",
    "REFUTED", "EXPIRED", "KILLED_WEAK",
]


def boundary_check():
    """Engine-guard: refuse to run unless engine/ is byte-identical to HEAD
    (no unstaged, staged, or untracked engine changes)."""
    diff = subprocess.run(["git", "diff", "HEAD", "--stat", "--", "engine/"],
                          cwd=ROOT, capture_output=True, text=True)
    untracked = subprocess.run(
        ["git", "ls-files", "--others", "--exclude-standard", "engine/"],
        cwd=ROOT, capture_output=True, text=True)
    dirty = diff.stdout.strip() or untracked.stdout.strip()
    if dirty:
        raise SystemExit(f"BOUNDARY CHECK FAILED - engine/ differs from "
                         f"HEAD:\n{dirty}")
    head = subprocess.run(["git", "rev-parse", "HEAD"], cwd=ROOT,
                          capture_output=True, text=True).stdout.strip()
    return {"engine_tree": "clean vs HEAD", "head": head,
            "runtime_attachments": [
                "wrap MTFEngine.process (read-only tap + T3 post-step)",
                "wrap engine.exec_pipe.on_close (stash classification "
                "return value; behavior unchanged)",
                "subclass HypothesisManager overriding _spawn only",
            ]}


class T3Manager(HypothesisManager):
    """Spawn surface: ONLY the H4 spawner, only on trend-consistent ND/NS
    prints in an established 1M trend. No H1/H2/H3/H5, no absorption scan.
    _spawn_h4 itself (inherited, verbatim) still requires the H4 anatomy:
    MARKUP/MARKDOWN with phase_age >= established_min_bars, an active
    quiet pullback (REACTION, mean rel_volume < pullback_vol_max)."""

    spawn_diag = None

    def _spawn(self, e):
        if self.spawn_diag is None:
            self.spawn_diag = {k: 0 for k in (
                "calls", "valid", "structural_any",
                "structural_nd_ns", "trend_matched", "established",
                "phase_trending", "in_reaction", "pullback_quiet",
                "qualified_nd_ns", "spawned")}
        self.spawn_diag["calls"] += 1
        if not e.feats.valid or e.bar.is_stub:
            return []
        self.spawn_diag["valid"] += 1
        if e.structural is not None:
            self.spawn_diag["structural_any"] += 1
        n0 = self._hyp_seq
        # spawn keys on the STRUCTURAL print — T1d's measured object (its
        # census counted structural ND/NS; the engine's qualified layer
        # measured 0 on 1M in July, see T3 build notes)
        d = {"NO_SUPPLY": 1, "NO_DEMAND": -1}.get(e.structural)
        if d is not None:
            g = self.spawn_diag
            ctx, hc = e.ctx, e.cfg.hypotheses.h4
            g["structural_nd_ns"] += 1
            if e.qualified == e.structural:
                g["qualified_nd_ns"] += 1
            if ctx.trend == d:
                g["trend_matched"] += 1
                if ctx.trend_age >= ESTABLISHED_TREND_AGE:
                    g["established"] += 1
                    want = "MARKUP" if d == 1 else "MARKDOWN"
                    if ctx.phase == want:
                        g["phase_trending"] += 1
                    if (ctx.impulse_reaction == "REACTION"
                            and ctx.pullback is not None):
                        g["in_reaction"] += 1
                        from engine.hypotheses import _pullback_stats
                        mean, _ = _pullback_stats(ctx.pullback, ctx.idx, d)
                        if mean is not None and mean < hc.pullback_vol_max:
                            g["pullback_quiet"] += 1
                            self._spawn_h4(e, d)
        out = [h for h in self.active if h.id is not None and h.id > n0]
        self.spawn_diag["spawned"] += len(out)
        return out


class T3Driver:
    """Attaches the T3 stack to a running MTFEngine. Own narrative, router,
    broker; steps on every exec (1M) bar close after the engine's standard
    processing at the same timestamp."""

    def __init__(self, engine, cfg, embargo_fn, eod_fn, tick_size,
                 point_value):
        self.engine = engine
        self.cfg = cfg
        self.narrative = Narrative()
        self.broker = Broker(cfg, self.narrative, eod_fn=eod_fn,
                             point_value=point_value, tick_size=tick_size)
        self.router = SignalRouter(cfg, self.narrative, embargo_fn=embargo_fn,
                                   tick_size=tick_size, broker=self.broker)
        gate = (mtf_gate_permits if not cfg.ablation.no_gating
                else (lambda h, c, s, cf: (True, "ABLATION_NO_GATE")))
        # ctx_ratio mirror: context refresh = 15min ctx over 1min signal
        self.manager = T3Manager(cfg, 15, self.narrative, self.router, gate)

        # tap the exec pipe's classification (return value only)
        self._cls = None
        orig_on_close = engine.exec_pipe.on_close

        def tapped(bar, ctx_tf=None, signal_ctx=None):
            out = orig_on_close(bar, ctx_tf=ctx_tf, signal_ctx=signal_ctx)
            self._cls = out
            return out
        engine.exec_pipe.on_close = tapped

        orig_process = engine.process

        def process(ts, context_bar=None, signal_bar=None, exec_bar=None,
                    exec_quote=None, ladder_bars=None):
            orig_process(ts, context_bar=context_bar, signal_bar=signal_bar,
                         exec_bar=exec_bar, exec_quote=exec_quote,
                         ladder_bars=ladder_bars)
            if exec_bar is not None and self._cls is not None:
                self._step(exec_bar, exec_quote, *self._cls)
                self._cls = None
        engine.process = process

    def _step(self, bar, quote, feats, cores, structural, qualified):
        if bar.is_stub:
            return
        ectx = self.engine.exec_pipe.ctx          # 1M ("signal" of the mirror)
        sctx = self.engine.signal_pipe.ctx        # 15M ("context" of the mirror)
        # mirror of MTFEngine.process's signal-close block, one rung down
        self.router.on_signal_open(bar)           # scheduled direct entries
        self.manager.step(bar, feats, cores, structural, qualified,
                          ectx, sctx)
        if self.broker.position is not None:
            opposing = any(d != self.broker.position["dir"]
                           for d in self.manager.last_confirm_dirs)
            self.broker.on_signal_close(bar, sctx, opposing)
        lows = [x for x in ectx.swings if x["type"] == "L"]
        highs = [x for x in ectx.swings if x["type"] == "H"]
        self.broker.signal_state = {
            "atr": ectx.atr,
            "swings": {"low": lows[-1]["price"] if lows else None,
                       "high": highs[-1]["price"] if highs else None}}
        self.broker.set_quote(quote)
        self.broker.on_exec_bar(bar)              # exits
        self.router.on_exec_bar(bar)              # refinement micro-loop


def funnel(narrative):
    counts = {}
    for e in narrative.events:
        t = e["type"]
        if t in FUNNEL_EVENTS:
            if t == "GATE":
                t = "GATE_PERMITTED" if e.get("permitted") else "GATE_BLOCKED"
            counts[t] = counts.get(t, 0) + 1
    return counts


def run(instr="uk100fut", seed_note=""):
    bc = boundary_check()
    from engine.strategy import load_definition, apply_definition
    fdef = load_definition(os.path.join(ROOT, "definitions",
                                        "frozen_v1.yaml"))
    cfg = apply_definition(load(), fdef)           # THE frozen config
    bc["definition"] = {"name": fdef["name"], "hash": fdef["_hash"]}
    inst = cfg.instruments[instr]
    embargo_fn, eod_fn = session_fns(cfg, instr)

    driver_box = {}
    import backtest.loop as L
    orig = L.MTFEngine

    def make(cfg2, **kw):
        e = orig(cfg2, **kw)
        driver_box["d"] = T3Driver(e, cfg2, embargo_fn, eod_fn,
                                   inst.tick_size, inst.point_value)
        return e
    L.MTFEngine = make
    try:
        engine, info = run_backtest(cfg, instr)
    finally:
        L.MTFEngine = orig
    d = driver_box["d"]

    trades = d.broker.trades
    m = breakdowns(trades, cfg.trade.starting_equity)
    res = {
        "STAMP": "EXPLORATORY - not validation",
        "prereg": "prereg_T3_build c1d826a919050364",
        "boundary_check": bc,
        "mechanism": ("H4-mirror on 1M: trend-consistent ND/NS spawn, "
                      f"1M trend_age>={ESTABLISHED_TREND_AGE} (T1d cell) "
                      "+ inherited H4 anatomy (phase_age>=10, quiet "
                      "pullback); confirm/refute/gate/refine/exits frozen"),
        "data": {"sessions": info["sessions"],
                 "span": [str(x) for x in info["span"]]},
        "spawn_diag": d.manager.spawn_diag,
        "funnel": funnel(d.narrative),
        "n_trades": len(trades),
        "per_trade_R": [round(t["r_multiple"], 3) for t in trades],
        "metrics": m,
        "trades": [{k: str(v) for k, v in t.items()} for t in trades],
        "note": seed_note,
    }
    return res, d, engine


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--instr", default="uk100fut")
    ap.add_argument("--tag", default="T3")
    a = ap.parse_args()
    os.makedirs(OUT, exist_ok=True)
    res, d, _ = run(a.instr)
    out_path = os.path.join(OUT, f"{a.tag}_h4mirror_1m.json")
    with open(out_path, "w") as f:
        json.dump(res, f, indent=2, default=str)
    print(json.dumps({k: res[k] for k in
                      ("funnel", "n_trades", "per_trade_R")}, indent=1))
    print(f"EXPLORATORY run -> {out_path}")


if __name__ == "__main__":
    main()
