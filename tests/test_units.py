"""Unit tests: swing confirmation lag, TEST criteria, trailing-only features,
processing order, CPG pending window, spawn dedupe."""

from helpers import Rig, scenario_cfg, sig_zigzag

from engine.bars import Bar
from engine.context import ContextTracker
from engine.features import FeatureEngine, Features
from engine.testcrit import test_criteria as check_test


def _bar(ts, o, h, l, c, v=100):
    return Bar(ts, o, h, l, c, v, tf="t")


def _feats(**kw):
    d = dict(valid=True, rel_volume=1.0, rel_spread_pct=50.0, close_pos=0.5,
             direction=0)
    d.update(kw)
    return Features(**d)


def test_swing_confirms_k_bars_late():
    cfg = scenario_cfg({"context.swing_k": 2})
    ctx = ContextTracker(cfg)
    highs = [1, 2, 5, 2, 1]      # peak at idx 2
    for i, hp in enumerate(highs):
        b = _bar(i, hp - 0.5, hp, hp - 1, hp - 0.2)
        ctx.update(b, _feats(), None)
        if i < 4:
            assert not any(s["idx"] == 2 for s in ctx.swings), \
                "swing must not be known before its k-bar confirmation"
    assert any(s["idx"] == 2 and s["type"] == "H" for s in ctx.swings)


def test_test_criteria_all_five():
    cfg = scenario_cfg()
    atr, sig_low, sig_rv = 2.0, 100.0, 3.0
    good = _bar(0, 102, 102.5, 100.5, 102.2)          # probes to 100.5, holds
    f = _feats(rel_volume=0.6, close_pos=0.85)
    assert check_test(good, f, sig_low, sig_rv, +1, atr, cfg)
    # (ii) fails: pierces the low
    assert not check_test(_bar(0, 102, 102.5, 99.9, 102.2), f,
                             sig_low, sig_rv, +1, atr, cfg)
    # (i) fails: never gets near the low (prox = 1.0 * atr = 2.0)
    assert not check_test(_bar(0, 105, 105.5, 103.5, 105.2), f,
                             sig_low, sig_rv, +1, atr, cfg)
    # (iii) fails: closes weak
    assert not check_test(good, _feats(rel_volume=0.6, close_pos=0.3),
                             sig_low, sig_rv, +1, atr, cfg)
    # (iv) fails: volume at baseline
    assert not check_test(good, _feats(rel_volume=1.1, close_pos=0.85),
                             sig_low, sig_rv, +1, atr, cfg)
    # (v) fails: volume not far enough below the signature bar's
    assert not check_test(good, _feats(rel_volume=0.9, close_pos=0.85),
                             sig_low, 1.5, +1, atr, cfg)


def test_features_are_trailing_only():
    """A bar must not be part of its own baseline: an outlier's features are
    computed against the pre-outlier distribution."""
    cfg = scenario_cfg()
    fe = FeatureEngine(cfg)
    for i in range(20):
        fe.update(_bar(i, 100, 101, 99, 100.5, v=100))
    monster = fe.update(_bar(20, 100, 110, 90, 109, v=1000))
    assert monster.rel_volume == 10.0          # vs mean 100, itself excluded
    assert monster.rel_spread_pct == 100.0


def test_classifier_sees_previous_bar_context():
    """Processing order: a climax bar's own context update (which flips phase
    to POST_CLIMAX) must not affect its own classification."""
    rig = Rig()
    from helpers import zigzag_gen
    rig.ctx_gen = zigzag_gen(300, up=False)
    # build a signal-TF downtrend, then a climax bar
    rig.flat(12)
    px = sig_zigzag(rig, 100.0, 5)
    assert rig.sctx.trend == -1
    pre_phase = rig.sctx.phase
    rig.sig(px, px + 0.3, px - 6.5, px - 5.7, 330)       # climax bar
    labels = [e for e in rig.of("LABEL") if e["tf"] == "15min"
              and e["label"] == "POTENTIAL_SELLING_CLIMAX"]
    assert labels, f"climax label expected (phase before: {pre_phase})"
    assert rig.sctx.phase == "POST_CLIMAX"             # updated AFTER classify


def test_cpg_expires_at_pending_window():
    """CPG lives pending_gate_max_bars (2 x ctx ratio = 8), not the confirm
    window."""
    from test_scenarios import climax_and_test_setup
    rig = climax_and_test_setup()                      # H1 now in CPG
    h = rig.engine.manager.active[0]
    assert h.state == "CONFIRMED_PENDING_GATE"
    px = rig.sctx.close
    for _ in range(9):                                 # 9 > pending window 8
        rig.sig(px, px + 1.0, px - 1.0, px + 0.1, 100)
    exp = rig.of("EXPIRED")
    assert any(e.get("note") == "pending_gate_window" for e in exp)


def test_duplicate_spawn_blocked_and_logged():
    from test_scenarios import upthrust_setup
    rig = upthrust_setup()                             # H2 SHORT active
    assert any(h.spec == "H2" for h in rig.engine.manager.active)
    px = rig.sctx.close
    # second upthrust bar while the first H2 is open
    rig.sig(px, px + 6.5, px - 0.5, px + 0.2, 210)
    assert rig.of("BLOCKED_SPAWN"), "second same-direction spawn must be blocked+logged"
