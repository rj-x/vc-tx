"""T3b — EXPLORATORY, NOT VALIDATION (register 121; pre-registered
prereg_T3b_build, counted 2026-08-31; the register-33/35 pre-sketch
executed: "identical to T3 — engine untouched, boundary check, frozen
config, funnel + per-trade R read criteria; gate EXACTLY T1d's
pre-registered conditions").

THE LAYER QUESTION SETTLED AT PRE-REGISTRATION (the 08-17 pre-sketch
said "identical to T3"; register 35 said "RECIPE-layer build" — the
two agree once the layers are named): the SIGNAL-layer read of the
T1d-exact gate is S0-H10 (register 35 consolidation); T3b is the
RECIPE-layer question — does H4's confirmation/stop machinery harvest
those bare fires? — which is exactly the T3 mould with the gate
loosened to T1d-exact. Built as the T3 scaffold with a new manager;
t3.py itself is untouched (a frozen lab instrument).

GATE (T1d-exact): trend-matched structural ND/NS print, 1M
trend_age >= ESTABLISHED_TREND_AGE. NO phase gate, NO REACTION
requirement (T3's verdict: the phase gate was an untested extra
condition, structurally unsatisfiable at 1M under frozen thresholds).

THE PRE-REGISTERED SIGNATURE FALLBACKS (the register_T3b design point:
without the phase gate, ctx.pullback may be None at spawn):
- CONFIRM (H4's pullback-mean rel_vol < h4.pullback_vol_max): when a
  quiet pullback exists (REACTION + pullback), the pullback mean reads
  as in H4; otherwise the SIGNATURE BAR'S OWN rel_volume reads against
  the same threshold — the print itself is the quiet-participation
  signature. Both paths counted separately in spawn_diag.
- STOP (pullback extreme): the engine's h4_stop ALREADY falls back to
  the signature bar's extremes when no pullback exists — the fallback
  is the engine's own, cited, not invented here.
- prior_structural_level: the last opposite swing before the pullback
  start when a pullback exists, else before the signature bar.

READ CRITERIA (T3's, verbatim): the spawn funnel and per-trade R;
home instrument, frozen_v1 config, boundary check (engine/ must be
byte-identical to HEAD). H10's deprioritize label (register 88) is on
record as this build's input — the label attaches to the SIGNAL row;
this run answers the recipe-layer half. EXPLORATORY: reports/lab/, not
evidence; twin-run pinned (tests/test_t3b.py on the manager's gate).
"""

import argparse
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "scripts"))

from engine.hypotheses import _pullback_stats
from backtest.t3 import (ESTABLISHED_TREND_AGE, T3Driver, T3Manager,
                         boundary_check, funnel)

OUT = os.path.join(ROOT, "reports", "lab")


class T3bManager(T3Manager):
    """T1d-exact gate + the pre-registered signature fallbacks."""

    def _spawn(self, e):
        if self.spawn_diag is None:
            self.spawn_diag = {k: 0 for k in (
                "calls", "valid", "structural_nd_ns", "trend_matched",
                "established", "confirm_via_pullback",
                "confirm_via_signature", "confirm_quiet", "spawned")}
        g = self.spawn_diag
        g["calls"] += 1
        if not e.feats.valid or e.bar.is_stub:
            return []
        g["valid"] += 1
        n0 = self._hyp_seq
        d = {"NO_SUPPLY": 1, "NO_DEMAND": -1}.get(e.structural)
        if d is not None:
            ctx, hc = e.ctx, e.cfg.hypotheses.h4
            g["structural_nd_ns"] += 1
            if ctx.trend == d:
                g["trend_matched"] += 1
                if ctx.trend_age >= ESTABLISHED_TREND_AGE:
                    g["established"] += 1
                    if (ctx.impulse_reaction == "REACTION"
                            and ctx.pullback is not None):
                        mean, _ = _pullback_stats(ctx.pullback, ctx.idx,
                                                  d)
                        pb = ctx.pullback
                        g["confirm_via_pullback"] += 1
                    else:
                        mean = e.feats.rel_volume   # the signature bar
                        pb = None
                        g["confirm_via_signature"] += 1
                    if mean is not None and mean < hc.pullback_vol_max:
                        g["confirm_quiet"] += 1
                        pb_start = (pb["start_idx"] if pb is not None
                                    else ctx.idx)
                        prior = (ctx.last_swing_low_before(pb_start)
                                 if d == 1 else
                                 ctx.last_swing_high_before(pb_start))

                        def setup(h):
                            h.pullback = pb
                            h.prior_structural_level = prior
                        self._try_add("H4", d, e, setup)
        out = [h for h in self.active if h.id is not None and h.id > n0]
        g["spawned"] += len(out)
        return out


class T3bDriver(T3Driver):
    def __init__(self, engine, cfg, embargo_fn, eod_fn, tick_size,
                 point_value):
        super().__init__(engine, cfg, embargo_fn, eod_fn, tick_size,
                         point_value)
        # swap the manager before any bar processes; the gate closure
        # mirrors the parent's construction
        from backtest.t3 import mtf_gate_permits
        gate = (mtf_gate_permits if not cfg.ablation.no_gating
                else (lambda h, c, s, cf: (True, "ABLATION_NO_GATE")))
        self.manager = T3bManager(cfg, 15, self.narrative, self.router,
                                  gate)


def run(instr="uk100fut", seed_note=""):
    bc = boundary_check()
    from engine.strategy import load_definition, apply_definition
    from engine.config import load
    from backtest.t3 import session_fns
    from backtest.loop import run_backtest
    from backtest.metrics import breakdowns
    fdef = load_definition(os.path.join(ROOT, "definitions",
                                        "frozen_v1.yaml"))
    cfg = apply_definition(load(), fdef)
    bc["definition"] = {"name": fdef["name"], "hash": fdef["_hash"]}
    inst = cfg.instruments[instr]
    embargo_fn, eod_fn = session_fns(cfg, instr)
    driver_box = {}
    import backtest.loop as L
    orig = L.MTFEngine

    def make(cfg2, **kw):
        e = orig(cfg2, **kw)
        driver_box["d"] = T3bDriver(e, cfg2, embargo_fn, eod_fn,
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
        "prereg": "prereg_T3b_build (register 121)",
        "boundary_check": bc,
        "mechanism": ("H4-mirror on 1M, T1d-EXACT gate: trend-matched "
                      f"structural ND/NS, trend_age>={ESTABLISHED_TREND_AGE}; "
                      "NO phase gate; confirm via pullback-mean rel_vol "
                      "with the SIGNATURE-BAR rel_volume fallback; stop "
                      "via h4_stop (its signature-extreme fallback is "
                      "the engine's own); confirm/refute/gate/refine/"
                      "exits frozen"),
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
    ap.add_argument("--tag", default="T3b")
    a = ap.parse_args()
    os.makedirs(OUT, exist_ok=True)
    res, d, _ = run(a.instr)
    out_path = os.path.join(OUT, f"{a.tag}_h4mirror_1m.json")
    with open(out_path, "w") as f:
        json.dump(res, f, indent=2, default=str)
    print(json.dumps({k: res[k] for k in
                      ("spawn_diag", "funnel", "n_trades",
                       "per_trade_R")}, indent=1))
    print(f"EXPLORATORY run -> {out_path}")


if __name__ == "__main__":
    main()
