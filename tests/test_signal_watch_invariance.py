"""Register 31 revision, approved structural requirement: engine decisions
AND narration bit-identical with signal-tracking on/off. The SignalWatch
attach point is a pure observer — this pins it."""
import json

from engine.bars import Bar
from engine.pipeline import MTFEngine
from engine.signal_watch import SignalWatch, FIRING_CONDITIONS
from helpers import scenario_cfg


def _run(attach, fire_everything=False):
    cfg = scenario_cfg()
    eng = MTFEngine(cfg)
    watch = None
    if attach:
        if fire_everything:
            # register BEFORE attach — attach snapshots the condition table
            FIRING_CONDITIONS["TEST_ALWAYS"] = (
                lambda bar, ectx, sctx, feats, cores, structural, qualified,
                prev: 1)
        watch = SignalWatch().attach(eng)
    try:
        t = 0
        for i in range(120):
            t += 1
            px = 100.0 + (i % 7) * 0.3 - (i % 3) * 0.2
            eb = Bar(t, px, px + 0.5, px - 0.5, px + 0.1, 100 + (i % 5) * 10,
                     tf="1min")
            kw = {"exec_bar": eb}
            if t % 15 == 0:
                kw["signal_bar"] = Bar(t, px - 1, px + 1, px - 1.2, px + 0.4,
                                       500, tf="15min")
            if t % 60 == 0:
                kw["context_bar"] = Bar(t, px - 2, px + 2, px - 2.2, px + 0.8,
                                        2000, tf="1h")
            eng.process(t, **kw)
    finally:
        FIRING_CONDITIONS.pop("TEST_ALWAYS", None)
    events = json.dumps(eng.narrative.events, default=str, sort_keys=True)
    trades = json.dumps(eng.broker.trades, default=str, sort_keys=True)
    return events, trades, watch


def test_narration_and_decisions_identical_on_off():
    ev_off, tr_off, _ = _run(attach=False)
    ev_on, tr_on, watch = _run(attach=True)
    assert ev_on == ev_off          # narration bit-identical
    assert tr_on == tr_off          # decisions bit-identical
    # six pre-registered conditions are defined; fires are OBSERVATIONS —
    # the assertion above already proved they perturb nothing

    # even an ACTIVELY FIRING condition must not perturb engine output
    ev_fire, tr_fire, watch2 = _run(attach=True, fire_everything=True)
    assert ev_fire == ev_off and tr_fire == tr_off
    assert len(watch2.fires) > 0    # it observed, and only observed
