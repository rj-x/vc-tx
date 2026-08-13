"""Synthetic-scenario verification — RULES.md Sec 10.

Each scenario builds hand-crafted bar sequences through the REAL pipeline
(features -> classifier -> context -> hypotheses -> gating -> routing) and
asserts the ruled behavior. Narrative logs are written to
reports/scenarios/ for joint review before any backtest.
"""

import os

from helpers import Rig, sig_zigzag, zigzag_gen

OUTDIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                      "reports", "scenarios")
os.makedirs(OUTDIR, exist_ok=True)


def _dump(rig, name):
    rig.dump(os.path.join(OUTDIR, f"{name}.txt"))
    rig.engine.narrative.write_jsonl(os.path.join(OUTDIR, f"{name}.jsonl"))


# --------------------------------------------------------------- setups

def upthrust_setup(execution=False, extra=None):
    """Signal-TF rally into an upthrust while Context TF is in MARKDOWN.
    Leaves an H2 SHORT hypothesis active (spawned, unconfirmed)."""
    over = dict(extra or {})
    if execution:
        over["execution.enabled"] = True
    rig = Rig(over)
    rig.ctx_gen = zigzag_gen(300, up=False)
    rig.flat(48)                       # long preamble: Context trend forms + ages
    px = 100.0
    for _ in range(6):                 # signal-TF rally (reaction rally)
        o, c = px, px + 1.2
        rig.sig(o, c + 0.4, o - 0.4, c, 105)
        px = c
    # upthrust: wide, high vol, big upper wick, weak close
    rig.sig(px, px + 6.0, px - 0.5, px + 0.1, 210)
    return rig


def climax_and_test_setup(extra=None):
    """Signal-TF selling climax + TEST while Context TF is MARKDOWN and the
    gate is closed (strict mode) -> H1 LONG in CONFIRMED_PENDING_GATE.
    The TEST bar is placed directly after a Context close so the 2nd
    Context close lands within the pending window."""
    over = {"gating.strict_mode": True}
    over.update(extra or {})
    rig = Rig(over)
    rig.ctx_gen = zigzag_gen(300, up=False)
    rig.flat(48)                       # long preamble: Context TF trend forms + ages
    px = sig_zigzag(rig, 100.0, 5)     # signal-TF downtrend, trend age grows
    # align so the NEXT bar lands right after a context close
    while rig.nsig % 4 != 0:
        rig.sig(px, px + 0.4, px - 0.6, px - 0.1, 95)
        px -= 0.1
    # selling climax: huge spread + volume, trailing max, closes near low
    lo = px - 6.5
    rig.sig(px, px + 0.3, lo, lo + 0.8, 330)
    # TEST: quiet probe toward the climax low that holds and recovers
    rig.sig(lo + 0.8, lo + 1.9, lo + 0.5, lo + 1.7, 60)
    return rig


# ------------------------------------------------------------- scenarios

def test_s1_upthrust_in_ctx_markdown_graduates_rev_with_trend():
    rig = upthrust_setup()
    assert rig.cctx.phase == "MARKDOWN", f"context phase: {rig.cctx.phase}"
    hs = [h for h in rig.engine.manager.active if h.spec == "H2"]
    assert hs and hs[0].dir == -1, "H2 SHORT must spawn from the upthrust"
    ut_high = hs[0].sig_high
    px = rig.sctx.close
    # confirm: down bar closing below the upthrust midpoint, volume expanding
    rig.sig(px, px + 0.3, px - 2.7, px - 2.4, 230)
    grads = rig.of("GRADUATED")
    assert grads, "H2 must graduate"
    assert grads[0]["h"]["tag"] == "REV_WITH_TREND", grads[0]["h"]
    # direct entry path: entry at the NEXT signal bar's open
    rig.sig(px - 2.4, px - 2.2, px - 3.0, px - 2.8, 120)
    entries = rig.of("ENTRY")
    assert entries and entries[0]["tag"] == "ENTRY_DIRECT"
    assert entries[0]["dir"] == -1
    assert entries[0]["stop"] > ut_high        # stop above upthrust high + buffer
    _dump(rig, "s1_rev_with_trend")


def test_s2_and_s7_cpg_graduates_on_second_ctx_close_shared_ts():
    rig = climax_and_test_setup()
    m = rig.engine.manager
    assert m.active and m.active[0].state == "CONFIRMED_PENDING_GATE", \
        [h.describe() for h in m.active]
    assert rig.of("CONFIRMED_PENDING_GATE")
    h = m.active[0]
    px = rig.sctx.close

    # quiet bars through the FIRST context close after CPG (normal zigzag bar)
    while rig.nsig % 4 != 0:
        rig.sig(px, px + 0.6, px - 0.4, px + 0.1, 95)
    assert m.active and m.active[0].state == "CONFIRMED_PENDING_GATE"
    # approach the SECOND context close
    while rig.nsig % 4 != 3:
        rig.sig(px, px + 0.6, px - 0.4, px + 0.1, 95)
    assert m.active and m.active[0].state == "CONFIRMED_PENDING_GATE"

    # 2nd context close: the CONTEXT TF prints its own selling climax ->
    # POST_CLIMAX(selling). Shared timestamp: context processes first
    # (descending order), so the SAME signal close re-evaluates the gate
    # against the new phase and graduates (scenario 7's ordering proof).
    cpx = rig.cctx.close
    ctx_climax = (cpx, cpx + 0.5, cpx - 24.0, cpx - 21.0, 400)
    rig.sig(px, px + 0.6, px - 0.4, px + 0.1, 95, ctx=ctx_climax)

    assert rig.cctx.phase == "POST_CLIMAX" and rig.cctx.post_climax_dir == 1, \
        (rig.cctx.phase, rig.cctx.post_climax_dir)
    grads = rig.of("GRADUATED")
    assert grads, "CPG hypothesis must graduate when the gate opens"
    assert grads[0]["h"]["id"] == h.id
    assert h.pending_age <= rig.engine.manager.pending_gate_max
    # scenario 7: graduation happened AT the shared timestamp
    assert grads[0]["ts"] == rig.t, "graduation must land on the shared-ts close"
    _dump(rig, "s2_s7_cpg_second_ctx_close")


def test_s3_h3_growing_zone_false_break_inside_then_confirm():
    rig = Rig()
    rig.ctx_gen = zigzag_gen(300, up=True)     # Context MARKUP (gate)
    rig.flat(12)
    px = sig_zigzag(rig, 100.0, 4, up=True)    # signal MARKUP; resistance forms
    m = rig.engine.manager
    lv_area = px + 1.7                          # last swing high ~ px + 1.7

    # two absorption bars near the level -> spawn
    for _ in range(2):
        rig.sig(lv_area - 0.5, lv_area - 0.1, lv_area - 0.6, lv_area - 0.2, 170)
    hs = [h for h in m.active if h.spec == "H3"]
    assert hs and hs[0].dir == 1, [h.describe() for h in m.active]
    h = hs[0]
    spawn_idx, anchor0 = h.spawn_idx, h.window_anchor
    boundary = max(h.level, h.zone_hi)

    # false breakout INSIDE the zone: wide, strong close, volume — but the
    # close is not beyond outermost(level, zone edge) -> must NOT confirm
    rig.sig(boundary - 3.1, boundary - 0.1, boundary - 3.2, boundary - 0.2, 200)
    assert h.state == "OPEN" and not rig.of("GRADUATED"), \
        "breakout inside the zone must not confirm"

    # quiet drift, then a third absorption bar late enough that the OLD
    # spawn-anchored expiry would have killed the hypothesis
    for _ in range(5):
        rig.sig(lv_area - 0.7, lv_area - 0.4, lv_area - 0.9, lv_area - 0.55, 95)
    rig.sig(lv_area - 0.4, lv_area + 0.1, lv_area - 0.5, lv_area - 0.05, 175)
    assert rig.of("H3_ZONE_EXTENDED"), "third absorption bar must extend the zone"
    assert h.window_anchor > anchor0

    # two more quiet bars, then the true breakout beyond outermost(level,
    # zone edge) — at an age where the OLD spawn-anchored expiry would
    # already have killed the hypothesis (re-anchor proof)
    for _ in range(2):
        rig.sig(lv_area - 0.6, lv_area - 0.3, lv_area - 0.8, lv_area - 0.45, 95)
    boundary = max(h.level, h.zone_hi)
    rig.sig(boundary - 0.4, boundary + 2.9, boundary - 0.5, boundary + 2.7, 185)
    grads = rig.of("GRADUATED")
    assert grads and grads[0]["h"]["spec"] == "H3", \
        rig.dump()[-2000:]
    assert rig.sctx.idx - spawn_idx > rig.cfg.hypotheses.h3.confirm_window, \
        "confirmation landed beyond the old spawn-anchored window (re-anchor proof)"
    _dump(rig, "s3_h3_growing_zone")


def test_s4_h4_expansion_and_break_on_different_bars_refutes():
    rig = Rig()
    rig.ctx_gen = zigzag_gen(300, up=True)
    rig.flat(12)
    px = sig_zigzag(rig, 100.0, 5, up=True)    # established MARKUP
    m = rig.engine.manager

    # pullback: quiet, SHALLOW down bars flip impulse/reaction to REACTION
    # (must stay above the last confirmed higher-low)
    for _ in range(2):
        o, c = px, px - 0.6
        rig.sig(o, o + 0.3, c - 0.2, c, 80)
        px = c
    assert rig.sctx.impulse_reaction == "REACTION", rig.sctx.impulse_reaction
    # NO_SUPPLY bar -> spawn
    rig.sig(px, px + 0.2, px - 0.3, px - 0.25, 65)
    px -= 0.25
    hs = [h for h in m.active if h.spec == "H4"]
    assert hs, [h.describe() for h in m.active]
    h = hs[0]
    prior = h.prior_structural_level
    assert prior is not None and prior < px

    # bar A: volume EXPANSION (state), close still above the structural level
    mid = prior + (px - prior) * 0.5
    rig.sig(px, px + 0.2, mid - 0.2, mid, 160)
    assert h.state == "OPEN", "expansion alone must not refute"
    assert h.pullback["max_rel_vol"] >= rig.cfg.hypotheses.h4.expand_mult

    # bar B: structural BREAK (trigger) on a later, quieter bar
    rig.sig(mid, mid + 0.2, prior - 1.2, prior - 1.0, 110)
    refs = rig.of("REFUTED")
    assert refs and refs[-1]["h"]["spec"] == "H4", \
        "state+trigger on different bars must refute"
    _dump(rig, "s4_h4_state_trigger_refute")


def test_s5_refutation_during_pending_refinement_cancels():
    rig = upthrust_setup(execution=True)
    hs = [h for h in rig.engine.manager.active if h.spec == "H2"]
    ut_high = hs[0].sig_high
    px = rig.sctx.close
    rig.sig(px, px + 0.3, px - 2.7, px - 2.4, 230)      # confirm -> graduate
    assert rig.of("REFINEMENT_STARTED")
    # exec bars WITHOUT a with-direction trigger (up bars vs SHORT)
    e = px - 2.4
    rig.execs([(e, e + 0.3, e - 0.05, e + 0.25, 50),
               (e + 0.25, e + 0.5, e + 0.2, e + 0.45, 50)])
    assert rig.router.pending is not None
    # next signal close refutes the parent (close above upthrust high)
    rig.sig(e, ut_high + 1.4, e - 0.2, ut_high + 1.2, 150)
    assert rig.of("REFINEMENT_CANCELLED_REFUTED"), "pending refinement must cancel"
    assert rig.router.pending is None and not rig.of("ENTRY")
    _dump(rig, "s5_refinement_cancelled_refuted")


def test_s6_opposed_graduation_cancels_pending_and_acts():
    rig = upthrust_setup(execution=True)
    m = rig.engine.manager
    px = rig.sctx.close
    rig.sig(px, px + 0.3, px - 2.7, px - 2.4, 230)      # H2 SHORT graduates
    px -= 2.4
    assert rig.of("REFINEMENT_STARTED")
    # exec bars, no trigger
    rig.execs([(px, px + 0.2, px - 0.05, px + 0.15, 50)])

    # decline toward support (keeps the SHORT premise alive: below ut high).
    # Exec bars are fed as UP-closes — NOT with-direction for the SHORT
    # window — so every TRIGGER_CHECK logs hit=False and the pending
    # refinement stays untriggered by construction (blocker-1 answer).
    for _ in range(4):
        o, c = px, px - 2.0
        rig.sig(o, o + 0.2, c - 0.3, c, 100)
        px = c
        rig.execs([(px, px + 0.3, px - 0.05, px + 0.25, 50)])
    # context prints a selling climax -> POST_CLIMAX(selling) permits LONGs
    cpx = rig.cctx.close
    while rig.nsig % 4 != 3:
        o, c = px, px - 0.8
        rig.sig(o, o + 0.2, c - 0.3, c, 100)
        px = c
    rig.sig(px, px + 0.2, px - 1.0, px - 0.8, 100,
            ctx=(cpx, cpx + 0.5, cpx - 24.0, cpx - 21.0, 400))
    px -= 0.8
    assert rig.cctx.phase == "POST_CLIMAX" and rig.cctx.post_climax_dir == 1

    # spring: wide, high vol, deep lower wick, strong close -> H2-mirror LONG
    rig.sig(px, px + 0.4, px - 6.0, px + 0.2, 210)
    hs = [h for h in m.active if h.spec == "H2" and h.dir == 1]
    assert hs, [h.describe() for h in m.active]
    mid = hs[0].sig_mid
    # confirm: UP bar (close > open) closing above the spring midpoint on
    # expanding volume
    rig.sig(mid + 0.2, mid + 2.0, mid - 0.1, mid + 1.8, 235)

    assert rig.of("REFINEMENT_CANCELLED_OPPOSED"), \
        "opposing graduation must cancel the pending SHORT refinement"
    started = rig.of("REFINEMENT_STARTED")
    assert started[-1]["h"]["dir"] == 1, \
        "the opposing LONG must then act (start its own refinement)"
    _dump(rig, "s6_opposed_cancel_then_act")


def test_s8_refinement_trigger_enters_with_tighter_stop():
    """Positive proof of the refined entry path: a with-direction exec bar
    beyond the close_pos threshold triggers; entry fills at the NEXT exec
    bar's open; stop = tighter of exec-local extreme vs signature extreme."""
    rig = upthrust_setup(execution=True)
    hs = [h for h in rig.engine.manager.active if h.spec == "H2"]
    ut_high = hs[0].sig_high
    px = rig.sctx.close
    rig.sig(px, px + 0.3, px - 2.7, px - 2.4, 230)      # confirm -> graduate
    assert rig.of("REFINEMENT_STARTED")
    e = px - 2.4
    # exec bar 1: up-close -> checked, no hit; exec bar 2: strong down close
    # (with-direction, close_pos < 0.3) -> trigger; exec bar 3: entry at open
    rig.execs([(e, e + 0.3, e - 0.05, e + 0.25, 50),
               (e + 0.25, e + 0.35, e - 0.9, e - 0.8, 60),
               (e - 0.8, e - 0.7, e - 1.2, e - 1.1, 60)])
    checks = rig.of("TRIGGER_CHECK")
    assert len(checks) == 2 and not checks[0]["hit"] and checks[1]["hit"], checks
    entries = rig.of("ENTRY")
    assert entries and entries[0]["tag"] == "ENTRY_REFINED"
    assert entries[0]["price"] == e - 0.8                # next exec bar's open
    assert entries[0]["gate_tag"] == "REV_WITH_TREND"
    # tighter-of: exec-local extreme (high of observed window bars + buffer)
    # must beat the signature stop for a SHORT
    buf = rig.cfg.hypotheses.stop_buffer_ticks * 1.0
    exec_high = max(e + 0.3, e + 0.35)
    assert entries[0]["stop"] == exec_high + buf < ut_high + buf
    assert rig.router.position is not None and rig.router.position["dir"] == -1
    _dump(rig, "s8_refined_entry_tighter_stop")
