"""Strategy laboratory — EXPLORATORY, NOT VALIDATION (every artifact says so).

  venv/bin/python -m backtest.lab --strategy definitions/foo.yaml

Runs any schema definition over the WORKING SET ONLY (zones loader-enforced)
through the one engine (identical code path as campaign/paper/narrate).
Outputs to reports/lab/ — physically separate from campaign artifacts; may
not feed the campaign, the register's evidential entries, or any threshold.
Every run appends to the immutable trial log (definition hash, timestamp,
headline metrics): the multiple-comparisons record that round-1 walk-forward
MUST consult when judging any surviving recipe. Promising definitions
graduate by candidate-backlog registration, nothing more.
"""

import argparse
import hashlib
import json
import os

import pandas as pd

from engine.config import load
from engine.strategy import load_definition, apply_definition, rule_matches
from engine.hypotheses import Hypothesis
from backtest.loop import run_backtest
from backtest.metrics import breakdowns

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "reports", "lab")
TRIAL_LOG = os.path.join(OUT, "trial_log.jsonl")


def _snapshot(engine, bar):
    ev = engine.narrative.events
    labels = set()
    loc = None
    for e in reversed(ev):
        if e.get("ts") != bar.ts:
            break
        if e["type"] == "LABEL" and e.get("label"):
            labels.add((e["tf"], e["label"]))
            if e.get("location_ref") and loc is None:
                loc = {"ref_class": {"session_high": "session_extreme",
                                     "session_low": "session_extreme",
                                     "prior_session_high": "prior_session_extreme",
                                     "prior_session_low": "prior_session_extreme",
                                     "signal_swing_level": "swing_registry"
                                     }.get(e["location_ref"], "unknown"),
                       "dist_atr": e.get("dist_signal_atr")}
    return {"labels": labels, "segment": bar.segment, "location": loc,
            "phases": {"context": engine.context_pipe.ctx.phase,
                       "signal": engine.signal_pipe.ctx.phase},
            "migration": {"max_rungs": 0, "any_recruited": False}}  # v1.1


class RuleDriver:
    """signal_rules mode: rule-matched entries through the SAME router/
    broker path (pseudo-hypothesis spec 'RULE'; direct entries)."""

    def __init__(self, engine, rules, cfg):
        self.engine, self.rules, self.cfg = engine, rules, cfg
        engine.cfg = cfg.override("execution.enabled", False)
        self._orig = engine.signal_pipe.on_close

        def wrapped(bar, ctx_tf=None):
            out = self._orig(bar, ctx_tf=ctx_tf)
            if not bar.is_stub and bar.segment == "cash":
                snap = _snapshot(engine, bar)
                for r in self.rules:
                    if rule_matches(r, snap):
                        h = Hypothesis("H1", r["direction"], bar,
                                       type("F", (), {"rel_volume": None})(),
                                       engine.signal_pipe.ctx, cfg)
                        h.spec, h.id = "RULE", 0
                        h.observational = False
                        h.spawn_segment = bar.segment
                        engine.router.route_signal(h, bar,
                                                   engine.signal_pipe.ctx,
                                                   engine.manager)
                        break
            return out
        engine.signal_pipe.on_close = wrapped


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--strategy", required=True)
    ap.add_argument("--instr", default="uk100fut")
    a = ap.parse_args()
    os.makedirs(OUT, exist_ok=True)
    d = load_definition(a.strategy)
    cfg = apply_definition(load(), d)

    if d["mode"] == "signal_rules":
        # one engine, wrapped entry driver; zones enforced by the loader
        from backtest import loop as L
        orig_engine = L.MTFEngine

        def make(cfg2, **kw):
            e = orig_engine(cfg2, **kw)
            RuleDriver(e, d["rules"], cfg2)
            return e
        L.MTFEngine = make
        try:
            engine, info = run_backtest(cfg, a.instr)
        finally:
            L.MTFEngine = orig_engine
    else:
        engine, info = run_backtest(cfg, a.instr)

    m = breakdowns(engine.broker.trades, cfg.trade.starting_equity)
    res = {"STAMP": "EXPLORATORY - not validation",
           "definition": d["name"], "hash": d["_hash"], "mode": d["mode"],
           "data": {"sessions": info["sessions"],
                    "span": [str(x) for x in info["span"]]},
           "metrics": m,
           "trades": [{k: str(v) for k, v in t.items()}
                      for t in engine.broker.trades]}
    out_path = os.path.join(OUT, f"{d['name']}_{d['_hash']}.json")
    with open(out_path, "w") as f:
        json.dump(res, f, indent=2, default=str)
    with open(TRIAL_LOG, "a") as f:
        f.write(json.dumps({
            "ts": str(pd.Timestamp.now(tz='UTC')), "name": d["name"],
            "hash": d["_hash"], "mode": d["mode"],
            "n_trades": m["overall"].get("n", 0),
            "total_pnl": m["overall"].get("total_pnl"),
            "win_rate": m["overall"].get("win_rate")}) + "\n")
    print(f"EXPLORATORY run -> {out_path}\n"
          f"trial log appended ({TRIAL_LOG})\n"
          f"n={m['overall'].get('n', 0)} pnl={m['overall'].get('total_pnl')}")


if __name__ == "__main__":
    main()
