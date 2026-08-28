"""Register 106 pins: the target re-rung leaves haircut, stop and EOD
untouched; the ladder cell carries the register-105 consistency
statistics (tail-carry cap on gross, week rule) plus reach and the
spread share; the leg-clears rule; candidates vs glints; the hand-off's
selection-null direction; twin-run."""
import json

from backtest.scalp_tp_ladder import (INCUMBENT_TP, TP_RUNGS, candidates,
                                      ladder_cell, leg_clears, with_target)


def _rows(spec, week="2026-W34"):
    return [{"pts": p, "reason": r, "week": week} for p, r in spec]


def test_with_target_rerungs_only_the_multiple():
    recipe = {"stages": [{"stop": [("atr", 2.5, "15min")],
                          "target": ("atr_haircut", 0.5, "15min", 0.5)}]}
    r = with_target(recipe, 1.0)
    assert r["stages"][0]["target"] == ("atr_haircut", 1.0, "15min", 0.5)
    assert r["stages"][0]["stop"] == [("atr", 2.5, "15min")]
    assert recipe["stages"][0]["target"][1] == INCUMBENT_TP   # intact
    assert INCUMBENT_TP not in TP_RUNGS


def test_ladder_cell_statistics():
    rows = _rows([(4.0, "target")] * 6 + [(-10.0, "stop"), (-1.0, "eod"),
                                          (2.0, "eod"), (-3.0, "eod")])
    c = ladder_cell(rows, spread=1.0)
    assert c["n"] == 10 and c["reach_rate"] == 0.6 and c["win_rate"] == 0.7
    assert c["spread_share_of_win"] == 0.2          # 1 / (4 + 1)
    assert not c["tail_carried"]                     # 4/26 gross
    assert (c["weeks_pos"], c["weeks_meas"]) == (1, 1)
    assert ladder_cell([], 1.0) == {"n": 0}
    tail = ladder_cell(_rows([(30.0, "target")] + [(1.0, "target")] * 9), 1.0)
    assert tail["tail_carried"]


def test_leg_clears_and_candidates():
    good = {"n": 20, "win_rate": 0.7, "median": 3.0, "tail_carried": False}
    inc = {"n": 20, "win_rate": 0.6, "median": 2.0, "tail_carried": False}
    fw, fm = {"max": 0.65}, {"max": 2.5}
    assert leg_clears(good, inc, fw, fm)
    assert not leg_clears({**good, "tail_carried": True}, inc, fw, fm)
    assert not leg_clears({**good, "median": 1.0}, inc, fw, fm)  # < incumbent
    assert not leg_clears(good, inc, None, fm)

    def res(clear):
        cell = good if clear else {**good, "win_rate": 0.5}
        return {"ladder": {f"{arm}|forward|{k:g}": (cell if k == 1.0 else inc)
                           for arm in ("R-SCALP-H" + "6", "R-SCALP-H" + "6-REF")
                           for k in (INCUMBENT_TP,) + TP_RUNGS},
                "floors": {f"{arm}|forward|{k:g}|{s}": (fw if s == "win_rate"
                                                          else fm)
                           for arm in ("R-SCALP-H" + "6", "R-SCALP-H" + "6-REF")
                           for k in (INCUMBENT_TP,) + TP_RUNGS
                           for s in ("win_rate", "median")}}
    results = {"a": res(True), "b": res(True), "c": res(True), "d": res(False)}
    cand = candidates(results)
    assert cand["R-SCALP-H" + "6|1"]["grade"] == "candidate"
    assert cand["R-SCALP-H" + "6|0.75"]["grade"] == "none"
    one = candidates({"a": res(True), "b": res(False)})
    assert one["R-SCALP-H" + "6|1"]["grade"] == "glint"
    assert json.dumps(cand, sort_keys=True) == json.dumps(candidates(results),
                                                          sort_keys=True)
