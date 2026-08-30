"""Register 105 pins: the tail-carry cap, the weekly-consistency count,
the slot precedence, the best-of-field selection null (twin-run and the
percentile's direction), and the candidate pool's empty mechanism slots
(nothing advances without the operator's pen)."""
import json

import numpy as np

from backtest.per_market_watch import (CANDIDATE_POOL, TAIL_CARRY_SHARE,
                                       best_of_field, cell_stats,
                                       percentile_vs, selection_null,
                                       slot_of)


def _rows(pts, week="2026-W33", **kw):
    base = {"instrument": "uk100fut", "variant": "R-NOTRAIL",
            "session": "london", "slot": "none", "window": "forward"}
    return [{**base, **kw, "pts": p, "week": week} for p in pts]


def test_tail_carry_cap_and_weekly_count():
    s = cell_stats(_rows([1.0, 1.0, 1.0, 20.0]))   # 20/23 gross > 25%
    assert s["tail_carried"] and s["max_win_share"] > TAIL_CARRY_SHARE
    s2 = cell_stats(_rows([2.0, 2.0, 2.0, 2.0, 2.0]))  # 2/10 = 20%
    assert not s2["tail_carried"] and s2["win_rate"] == 1.0
    # the amendment's pin: a near-zero-NET cell is no longer tail-carried
    # when its wins are spread (the |net| denominator was the defect)
    s3 = cell_stats(_rows([2.0] * 5 + [-2.0] * 5))     # net 0, gross 10
    assert not s3["tail_carried"] and s3["max_win_share"] == 0.2
    assert cell_stats(_rows([-1.0, -2.0]))["tail_carried"]   # no gross
    rows = (_rows([1, 1, 1], week="2026-W31") + _rows([-1, -1, -1], week="2026-W32")
            + _rows([5], week="2026-W33"))            # W33 not measurable
    s3 = cell_stats(rows)
    assert (s3["weeks_pos"], s3["weeks_meas"]) == (1, 2)


def test_slot_precedence():
    assert slot_of({"open15": True, "close15": True}) == "open15"
    assert slot_of({"news15:cross": True, "close15": False}) == "news15"
    assert slot_of({"news15:native": None, "news15:cross": None}) == "none"


def test_selection_null_twin_run_and_direction():
    rs = np.random.RandomState(0)
    rows = []
    for var in ("A", "B", "C"):
        for sess in ("london", "asia"):
            # drifted rows: cells net clearly, so the tail-carry cap does
            # not swallow the field (the zero-drift degeneracy is the
            # rule as written, recorded at register 105)
            rows += _rows(list(rs.normal(1, 1, 15)), variant=var, session=sess)
    wr1, md1 = selection_null(rows)
    wr2, md2 = selection_null(rows)
    assert json.dumps(wr1.tolist()) == json.dumps(wr2.tolist())
    assert json.dumps(md1.tolist()) == json.dumps(md2.tolist())
    assert not np.isnan(wr1).all()
    # the best-of-field null sits ABOVE a typical cell: a chance-level
    # cell cannot beat the field's best fake
    assert percentile_vs(wr1, 0.5) < 50.0
    assert percentile_vs(wr1, 1.01) == 100.0
    assert percentile_vs(np.array([np.nan, np.nan]), 0.5) is None
    cells = {("A", "london", "none"): cell_stats(_rows([1.0] * 12)),
             ("B", "asia", "none"): cell_stats(_rows([1.0] * 3 + [-1.0] * 9))}
    assert best_of_field(cells) == (1.0, 1.0)


def test_distinct_paths_count_once_register_113():
    # co-fired identical price paths count ONCE for evidence: all
    # statistics compute on distinct paths; n keeps rows, n_distinct
    # the evidence count; rows without a path key never dedup
    rows = _rows([1.0, -1.0])
    rows += [dict(rows[0]), dict(rows[0])]
    assert cell_stats(rows)["n_distinct"] == 4        # no path key
    for i, r in enumerate(rows):
        r["path"] = f"p{i}"
    rows[2]["path"] = rows[3]["path"] = rows[0]["path"]
    s = cell_stats(rows)
    assert (s["n"], s["n_distinct"]) == (4, 2)
    assert s["win_rate"] == 0.5 and s["median"] == 0.0
    assert s["net_pts"] == 0.0
    # tail-carry recomputes on distinct gross: one path duplicated 11x
    # diluted the raw share below the cap; the distinct share trips it
    pts = [3.0] + [1.0] * 11 + [-1.0]
    rows2 = _rows(pts)
    for i, r in enumerate(rows2):
        r["path"] = "dup" if 0 < i < 12 else f"p{i}"
    s2 = cell_stats(rows2)
    assert (s2["n"], s2["n_distinct"]) == (13, 3)
    assert s2["max_win_share"] == 0.75 and s2["tail_carried"]
    raw = cell_stats(_rows(pts))                      # no dedup
    assert raw["max_win_share"] < TAIL_CARRY_SHARE and not raw["tail_carried"]


def test_census_selection_null_twin_run_and_direction():
    # register 108: signal labels permuted across census fires, n kept;
    # a chance-level signal cannot beat the field's best fake
    from backtest.per_market_watch import (census_selection_null,
                                           null_p95)
    rs = np.random.RandomState(3)
    fires = [(s, float(rs.rand() < 0.2)) for s in ("A", "B", "C", "D")
             for _ in range(40)]
    n1, n2 = census_selection_null(fires), census_selection_null(fires)
    assert json.dumps(n1.tolist()) == json.dumps(n2.tolist())
    assert not np.isnan(n1).any()
    assert percentile_vs(n1, 20.0) < 50.0
    assert percentile_vs(n1, 100.0) == 100.0
    assert null_p95(n1) > 20.0
    # nothing measurable -> every seed missing, never a low value
    assert np.isnan(census_selection_null(fires[:10])).all()


def test_candidate_pool_mechanism_slots_empty():
    assert len(CANDIDATE_POOL) == 3
    assert all(c["mechanism"] == "" for c in CANDIDATE_POOL)
