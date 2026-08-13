"""Broker sim tests — Part 7: stop/target 1M resolution (stop-first),
gap-through-stop, EOD force-close, time stop, opposing-confirm exit,
contract sizing / SKIPPED_SIZE."""

from test_scenarios import upthrust_setup


def _short_position(extra=None):
    """s8 flow: H2 SHORT graduates, refinement triggers, position opens."""
    rig = upthrust_setup(execution=True, extra=extra)
    px = rig.sctx.close
    rig.sig(px, px + 0.3, px - 2.7, px - 2.4, 230)
    e = px - 2.4
    rig.execs([(e, e + 0.3, e - 0.05, e + 0.25, 50),
               (e + 0.25, e + 0.35, e - 0.9, e - 0.8, 60),
               (e - 0.8, e - 0.7, e - 1.2, e - 1.1, 60)])
    assert rig.engine.broker.position is not None
    return rig, rig.engine.broker.position


def test_sizing_fixed_fractional_whole_contracts():
    rig, p = _short_position()
    expected = int((100000.0 * 0.01) // p["stop_dist"])   # point_value 1.0
    assert p["contracts"] == expected >= 1


def test_skipped_size_logged():
    rig, _ = _short_position()          # position 1 opens fine
    rig2, _ = None, None
    rig3 = upthrust_setup(execution=True,
                          extra={"trade.risk_frac": 0.000001})
    px = rig3.sctx.close
    rig3.sig(px, px + 0.3, px - 2.7, px - 2.4, 230)
    e = px - 2.4
    rig3.execs([(e, e + 0.3, e - 0.05, e + 0.25, 50),
                (e + 0.25, e + 0.35, e - 0.9, e - 0.8, 60),
                (e - 0.8, e - 0.7, e - 1.2, e - 1.1, 60)])
    assert rig3.engine.broker.position is None
    assert rig3.of("SKIPPED_SIZE"), "sub-1-contract sizing must skip + log"


def test_stop_hit_on_exec_bar():
    rig, p = _short_position()
    stop = p["stop"]
    rig.execs([(stop - 1.0, stop + 0.5, stop - 1.1, stop - 0.9, 40)])
    assert rig.engine.broker.position is None
    tr = rig.engine.broker.trades[-1]
    assert tr["reason"] == "STOP"
    assert tr["exit"] == stop + 1.0     # slippage 1 tick AGAINST a short
    assert tr["pnl"] < 0


def test_gap_through_stop_fills_at_open():
    rig, p = _short_position()
    stop = p["stop"]
    gap_open = stop + 2.0               # opens beyond the stop
    rig.execs([(gap_open, gap_open + 0.4, gap_open - 0.2, gap_open + 0.2, 40)])
    tr = rig.engine.broker.trades[-1]
    assert tr["reason"] == "STOP_GAP"
    assert tr["exit"] == gap_open + 1.0  # the worse price, plus slippage


def test_target_and_stop_same_bar_is_stop_first():
    rig, p = _short_position()
    stop, tgt = p["stop"], p["target"]
    assert tgt is not None and tgt < p["entry"] < stop
    # one 1M bar touching BOTH -> conservative stop-first
    rig.execs([(p["entry"], stop + 0.2, tgt - 0.2, p["entry"], 80)])
    tr = rig.engine.broker.trades[-1]
    assert tr["reason"] == "STOP"


def test_target_exit_fixed_r():
    rig, p = _short_position()
    tgt = p["target"]
    rig.execs([(tgt + 1.0, tgt + 1.2, tgt - 0.3, tgt - 0.1, 40)])
    tr = rig.engine.broker.trades[-1]
    assert tr["reason"] == "TARGET" and tr["pnl"] > 0
    # exactly 2R minus 1 tick of slippage expressed in R (tick=1.0 here)
    expected_r = 2.0 - 1.0 / p["stop_dist"]
    assert abs(tr["r_multiple"] - expected_r) < 1e-9


def test_eod_force_close():
    rig, p = _short_position()
    rig.embargo_after = None
    rig.engine.broker.eod_fn = lambda ts: ts >= rig.t + 2
    e = p["entry"]
    rig.execs([(e, e + 0.1, e - 0.1, e, 30),        # before cutoff
               (e, e + 0.1, e - 0.1, e - 0.05, 30)])  # at cutoff -> force flat
    tr = rig.engine.broker.trades[-1]
    assert tr["reason"] == "EOD_EXIT"


def test_time_stop_via_signal_bars():
    rig, p = _short_position(extra={"trade.time_stop_bars": 2})
    e = p["entry"]
    rig.sig(e, e + 0.2, e - 0.4, e - 0.1, 90)
    rig.sig(e - 0.1, e + 0.1, e - 0.5, e - 0.2, 90)   # 2nd bar -> time stop
    assert rig.engine.broker.position["exit_pending"] == "TIME_STOP"
    rig.execs([(e - 0.2, e, e - 0.3, e - 0.1, 30)])   # fills at next exec open
    tr = rig.engine.broker.trades[-1]
    assert tr["reason"] == "TIME_STOP" and tr["exit"] == (e - 0.2) + 1.0


def test_opposing_confirm_exit_mode():
    rig, p = _short_position(extra={"trade.exit_mode": "opposing"})
    px = rig.sctx.close
    # build an opposing LONG confirm: spring then midpoint-break up bar
    for _ in range(3):
        o, c = px, px - 1.5
        rig.sig(o, o + 0.2, c - 0.3, c, 100)
        px = c
    rig.sig(px, px + 0.4, px - 6.0, px + 0.2, 210)          # SPRING -> H2 LONG
    hs = [h for h in rig.engine.manager.active
          if h.spec == "H2" and h.dir == 1]
    assert hs, [h.describe() for h in rig.engine.manager.active]
    mid = hs[0].sig_mid
    rig.sig(mid + 0.2, mid + 2.0, mid - 0.1, mid + 1.8, 235)  # LONG confirms
    assert rig.engine.broker.position["exit_pending"] == "OPPOSING_CONFIRM"
    rig.execs([(mid + 1.8, mid + 2.0, mid + 1.6, mid + 1.9, 40)])
    tr = rig.engine.broker.trades[-1]
    assert tr["reason"] == "OPPOSING_CONFIRM"
    # no reverse-and-flip: the position is closed, nothing new opened
    assert rig.engine.broker.position is None
