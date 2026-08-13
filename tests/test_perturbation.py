"""Future-perturbation test (Non-Negotiable #4): run the engine to a cutoff
T and record every decision; replace all data after T with different data;
re-run from scratch. Every logged decision at or before T must be identical.
Automated over multiple seeds and cutoffs.

Data is synthetic (regime-shifting random walk) — no real-data runs before
backtest authorization. The generator injects trend legs and volume bursts
so the engine actually labels, spawns, and gates (a quiet tape would make
the test vacuous; a floor assertion guards that)."""

import numpy as np

from helpers import scenario_cfg

from engine.bars import Bar
from engine.pipeline import MTFEngine
from backtest.driver import replay

N_MIN = 4800          # 80 signal bars / 20 context bars per run segment


def _minute_bars(seed, n, start_ts=1, px0=100.0):
    rng = np.random.default_rng(seed)
    bars = []
    px = px0
    trend = 0.0
    for i in range(n):
        ts = start_ts + i
        if i % 240 == 0:
            trend = rng.choice([-0.05, 0.0, 0.05])
        burst = 6.0 if rng.random() < 0.01 else 1.0
        vol = float(np.abs(rng.normal(100, 25)) * burst + 1)
        rngw = np.abs(rng.normal(0.4, 0.25)) * (2.0 if burst > 1 else 1.0)
        o = px
        c = px + trend + rng.normal(0, 0.35)
        h = max(o, c) + rngw
        l = min(o, c) - rngw
        bars.append(Bar(ts, o, h, l, c, vol, tf="1min"))
        px = c
    return bars


def _agg(ts, bars, tf):
    return Bar(ts, bars[0].open, max(b.high for b in bars),
               min(b.low for b in bars), bars[-1].close,
               sum(b.volume for b in bars), tf=tf)


def _run(minute_bars):
    cfg = scenario_cfg()
    engine = MTFEngine(cfg)
    replay(engine, minute_bars, make_bar=_agg)
    return engine.narrative.events


def _events_upto(events, t):
    return [e for e in events if e["ts"] is not None and e["ts"] <= t]


def test_future_perturbation_multiple_seeds_and_cutoffs():
    for seed in (3, 17):
        base = _minute_bars(seed, N_MIN)
        for cutoff in (N_MIN // 2, (3 * N_MIN) // 4):
            prefix = base[:cutoff]
            # mutated future: entirely different data after the cutoff,
            # continuing from the prefix's last price
            mutated_tail = _minute_bars(seed + 1000 + cutoff, N_MIN - cutoff,
                                        start_ts=cutoff + 1,
                                        px0=prefix[-1].close)
            ev_a = _run(base)
            ev_b = _run(prefix + mutated_tail)
            a, b = _events_upto(ev_a, cutoff), _events_upto(ev_b, cutoff)
            assert len(a) >= 30, "tape too quiet — perturbation test is vacuous"
            assert a == b, (
                f"seed {seed} cutoff {cutoff}: decisions at/before the cutoff "
                f"changed when future data changed — LOOK-AHEAD LEAK "
                f"(first divergence: "
                f"{next((x, y) for x, y in zip(a, b) if x != y) if len(a) == len(b) else (len(a), len(b))})")


def _replay_script(cfg, script):
    from engine.pipeline import MTFEngine
    eng = MTFEngine(cfg)
    for ts, cb, sb, eb in script:
        eng.process(ts, context_bar=cb, signal_bar=sb, exec_bar=eb)
    return eng.narrative.events


def _random_tail(seed, start_ts, n_sig, px0):
    """Random continuation signal bars (15-min spaced) as script entries."""
    from engine.bars import Bar
    rng = np.random.default_rng(seed)
    out, px, ts = [], px0, start_ts
    for _ in range(n_sig):
        ts += 15
        o = px
        c = px + rng.normal(0, 1.2)
        h = max(o, c) + abs(rng.normal(0.5, 0.4))
        l = min(o, c) - abs(rng.normal(0.5, 0.4))
        v = float(abs(rng.normal(110, 50)) + 10)
        out.append((ts, None, Bar(ts, o, h, l, c, v, tf="15min"), None))
        px = c
    return out


def test_perturbation_through_graduation_refinement_entry():
    """Enriched tape: the pre-cutoff prefix contains a full graduation ->
    refinement -> entry chain (the deterministic s8 flow); the post-cutoff
    future is replaced wholesale. Every decision at/before the cutoff —
    including the ENTRY — must be identical."""
    import sys, os
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    from test_scenarios import upthrust_setup

    rig = upthrust_setup(execution=True)
    px = rig.sctx.close
    rig.sig(px, px + 0.3, px - 2.7, px - 2.4, 230)      # confirm -> graduate
    e = px - 2.4
    rig.execs([(e, e + 0.3, e - 0.05, e + 0.25, 50),
               (e + 0.25, e + 0.35, e - 0.9, e - 0.8, 60),
               (e - 0.8, e - 0.7, e - 1.2, e - 1.1, 60)])   # trigger + ENTRY
    prefix = list(rig.script)
    cutoff = prefix[-1][0]
    cfg = rig.cfg

    tail_a = _random_tail(101, cutoff, 40, e - 1.1)
    tail_b = _random_tail(202, cutoff, 40, e - 1.1)
    ev_a = _replay_script(cfg, prefix + tail_a)
    ev_b = _replay_script(cfg, prefix + tail_b)
    a = _events_upto(ev_a, cutoff)
    b = _events_upto(ev_b, cutoff)
    types = {x["type"] for x in a}
    assert {"GRADUATED", "REFINEMENT_TRIGGERED", "ENTRY"} <= types, types
    assert a == b, "pre-cutoff decisions changed under future mutation"
