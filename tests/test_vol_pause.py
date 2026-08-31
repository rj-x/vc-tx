"""Register 132 pins: the pause cell's accounting (skip set at the
edge, foregone vs avoided, net delta = minus the skipped sum, stop
dodging, distinct paths), the X edges, and the forensic table's
skip-set membership logic."""
import numpy as np

from backtest.vol_pause import PAUSE_X, WORST_N, pause_cell


def _r(pts, pctl, stopped=False, path=None):
    return {"pts": pts, "atr_pctl": pctl, "stopped": stopped,
            "path": path}


def test_pause_cell_accounting_and_edge():
    rows = [_r(10.0, 50, path="a"),       # kept
            _r(-20.0, 96, stopped=True, path="b"),   # skipped: stop dodged
            _r(5.0, 99, path="c"),        # skipped: winner foregone
            _r(-3.0, 95, path="d"),       # NOT skipped: > is strict
            _r(7.0, None, path="e")]      # unmeasured: never skipped
    c = pause_cell(rows, 95)
    assert (c["n"], c["n_distinct"], c["skipped"]) == (5, 5, 2)
    assert c["skip_share"] == 0.4
    assert c["foregone_win_pts"] == 5.0
    assert c["avoided_loss_pts"] == 20.0
    assert c["net_delta"] == 15.0          # -(−20 + 5)
    assert c["stops_dodged"] == 1 and c["stops_dodged_pts"] == -20.0
    assert c["worst_stop_dodged"] == -20.0
    assert PAUSE_X == (80, 95) and WORST_N == 27


def test_pause_cell_distinct_paths_and_empty():
    rows = [_r(-20.0, 99, stopped=True, path="dup")] * 3 \
        + [_r(4.0, 10, path="k")]
    c = pause_cell(rows, 95)
    assert (c["n"], c["n_distinct"]) == (4, 2)      # dup counts once
    assert c["net_delta"] == 20.0                    # one dodge, not three
    c0 = pause_cell([_r(4.0, 10, path="k")], 80)
    assert c0["skipped"] == 0 and c0["net_delta"] == 0.0
    assert c0["worst_stop_dodged"] is None
