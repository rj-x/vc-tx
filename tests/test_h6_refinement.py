"""Register 100 pins: the co-fire tagger (+/-5 bars, same instrument,
other signals only), the split/measurability rule, the discriminator's
>= 3-of-4 same-sign rule, the scalp economics per fire, the time-cap
curve, and twin-run determinism of the luck budget."""
import json

import pandas as pd

from backtest.h6_refinement import (CAND_MIN_LEGS, cofire_tags,
                                    discriminate, fire_net, luck,
                                    split_cells, time_cap)


def _bp(instr, ts, touch, bar=None, atr=4.0, spread=1.0, c5=-1.0):
    return {"instrument": instr, "fire_ts": ts, "signal": "S0-H" + "6",
            "zone": "forward", "session": "london",
            "touched_0p5atr_5b": "True" if touch else "False",
            "touched_0p5atr_5b_net_of_spread": "True" if touch else "False",
            "bar_of_first_touch": str(bar) if bar else "",
            "spread_pts": str(spread), "atr15_at_fire": str(atr),
            "cum_pts_bar3": str(c5), "cum_pts_bar5": str(c5),
            "cum_pts_bar8": str(c5), "cum_pts_bar10": str(c5 - 1)}


def test_cofire_tags_window_and_exclusions():
    bp = [_bp("uk100fut", "2026-08-20 10:00:00+00:00", True)]
    fires = [{"instrument": "uk100fut", "fire_ts": "2026-08-20 10:04:00+00:00",
              "signal": "S0-H1"},
             {"instrument": "uk100fut", "fire_ts": "2026-08-20 10:06:00+00:00",
              "signal": "S0-H2"},                          # outside +/-5
             {"instrument": "ger40fut", "fire_ts": "2026-08-20 10:00:00+00:00",
              "signal": "S0-H1"}]                          # other instrument
    assert cofire_tags(bp, fires) == [["S0-H1"]]


def test_fire_net_scalp_economics():
    assert fire_net(_bp("x", "t", True, atr=4.0, spread=1.0)) == 1.0
    assert fire_net(_bp("x", "t", False, c5=-2.0, spread=1.0)) == -3.0


def _synthetic():
    # a separating co-fire on three legs, none on the fourth
    bp, fires = [], []
    for instr, separates in (("uk100fut", True), ("ger40fut", True),
                             ("nas100fut", True), ("us30fut", False)):
        for i in range(40):
            # 15-minute spacing: a co-fire must sit within +/-5 minutes
            # of ITS fire only, never a neighbour's
            ts = str(pd.Timestamp("2026-08-20 08:00:00+00:00")
                     + pd.Timedelta(minutes=15 * i))
            with_s = i % 2 == 0
            touch = (with_s if separates else (i % 3 == 0))
            bp.append(_bp(instr, ts, touch))
            if with_s:
                fires.append({"instrument": instr, "fire_ts": ts,
                              "signal": "S0-H1"})
    return bp, fires


def test_discriminator_three_of_four_and_twin_run():
    bp, fires = _synthetic()
    tags = cofire_tags(bp, fires)
    cells = split_cells(bp, tags, {})
    p95, budget = luck(bp, tags, {}, cells)
    disc = discriminate(cells, p95)
    d = disc["cofire:S0-H1"]
    assert d["grade"] == "candidate" and d["sign"] == "+"
    assert len(d["clearing_legs"]) >= CAND_MIN_LEGS
    assert "us30fut" not in d["clearing_legs"]
    def _ser(x):
        p, budget = x
        return json.dumps([{str(k): v for k, v in p.items()}, budget],
                          sort_keys=True)
    assert _ser(luck(bp, tags, {}, cells)) == _ser(luck(bp, tags, {}, cells))


def test_time_cap_curve():
    bp = [_bp("uk100fut", "t", True, bar=2), _bp("uk100fut", "t", True, bar=4),
          _bp("uk100fut", "t", False), _bp("uk100fut", "t", False)]
    tc = time_cap(bp)["uk100fut"]
    k1 = tc["conditional_reach"][0]
    assert k1["n_dry"] == 4 and k1["p_touch_by_5"] == 0.5
    k3 = tc["conditional_reach"][2]
    assert k3["n_dry"] == 3 and k3["p_touch_by_5"] == round(1 / 3, 3)
    assert tc["caps"]["5"]["n_nonreach"] == 2


def test_real_basis_dry_at_k_decomposition():
    from backtest.h6_refinement import real_basis
    fire = "2026-08-20 10:00:00+00:00"
    open_ts = "2026-08-20 10:01:00+00:00"
    fire_ns = pd.Timestamp(fire).value

    def _row(reason, dur, pts):
        return {"instrument": "uk100fut", "_window": "forward",
                "_fire_ns": fire_ns, "exit_reason": reason,
                "duration_min": str(dur), "points": str(pts),
                "open_ts": open_ts}
    rows = [_row("target", 0.0, 5.0),      # reached by bar 3: excluded
            _row("target", 10.0, 5.0),     # late reach: amputated
            _row("eod", 300.0, -4.0),      # drift: saved
            _row("stop", 20.0, -12.0),     # stop after cap: dodged
            _row("stop", 1.0, -12.0)]      # stop before cap: not dodgeable
    bp = [_bp("uk100fut", fire, True, c5=-1.0)]
    bp[0]["cum_pts_bar3"] = "-1.0"        # cap@3 = -1 - spread(1) = -2
    rb = real_basis(rows, bp)["uk100fut|forward"]
    c3 = rb["caps"]["3"]
    assert c3["n_dry"] == 3 and c3["n_stop_before_cap"] == 1
    assert c3["n_late_reach"] == 1 and c3["delta_late_reach"] == -7.0
    assert c3["n_eod"] == 1 and c3["delta_eod"] == 2.0
    assert c3["n_stop_dodged"] == 1 and c3["delta_stop"] == 10.0
    assert c3["delta_total"] == 5.0 and not c3["holds"]   # n_dry < 10
