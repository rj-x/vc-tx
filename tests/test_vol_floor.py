"""Register 137 pins: the inverted predicate (a LOW percentile gates,
None never does, the joint form needs both), the five-point grid, and
twin-run bit-identity of the cell accounting."""
import json

from backtest.vol_floor import (FLOOR_X, JOINT_X, gate_cell, gate_grid,
                                gated)


def test_grid_is_the_preregistered_five():
    assert (FLOOR_X, JOINT_X) == ((30, 50), 50)
    assert gate_grid() == (("pooled", 30), ("pooled", 50),
                           ("tod", 30), ("tod", 50), ("joint", 50))


def test_predicate_inversion_and_none_handling():
    # low volatility gates; high does not — the register-132 predicate
    # inverted
    assert gated(20.0, 90.0, "pooled", 30)
    assert not gated(80.0, 20.0, "pooled", 30)
    assert gated(90.0, 20.0, "tod", 30)
    assert not gated(20.0, 80.0, "tod", 30)
    # joint needs BOTH below
    assert gated(40.0, 45.0, "joint", 50)
    assert not gated(40.0, 55.0, "joint", 50)
    assert not gated(55.0, 40.0, "joint", 50)
    # a None percentile never gates, any form
    assert not gated(None, 10.0, "pooled", 50)
    assert not gated(10.0, None, "tod", 50)
    assert not gated(None, 10.0, "joint", 50)
    assert not gated(10.0, None, "joint", 50)


def _rows():
    out = []
    for i in range(40):
        pc = float(i * 2.5)            # 0 .. 97.5
        out.append({"atr_pctl": pc, "atr_pctl_tod": 100.0 - pc,
                    "pts": 10.0 if i % 2 else -8.0,
                    "stopped": i % 2 == 0, "path": f"p{i}"})
    return out


def test_cell_accounting_twin_run_and_direction():
    a = json.dumps(gate_cell(_rows(), "pooled", 50))
    b = json.dumps(gate_cell(_rows(), "pooled", 50))
    assert a == b
    c = gate_cell(_rows(), "pooled", 50)
    # rows 0..19 gate (pctl < 50): 10 winners of +10, 10 losers of -8
    assert c["skipped"] == 20
    assert c["foregone_win_pts"] == 100.0
    assert c["avoided_loss_pts"] == 80.0
    assert c["net_delta"] == -20.0
    # the joint form gates only the overlap (both < 50): pooled<50 is
    # i<20, tod<50 is i>20 — empty overlap here
    assert gate_cell(_rows(), "joint", 50)["skipped"] == 0
