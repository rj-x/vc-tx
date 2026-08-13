"""Part A cash-CFD vehicle: ask/bid fills, basis level mapping, min stake."""
import pytest
from helpers import scenario_cfg
from engine.broker import Broker
from engine.bars import Bar
from engine.narrative import Narrative


def _mk(extra=None):
    cfg = scenario_cfg({"execution_vehicle.mode": "cash_cfd",
                        "trade.exit_mode": "fixed_r", **(extra or {})})
    return Broker(cfg, Narrative(), eod_fn=lambda ts: False), cfg


def _entry(price, stop):
    return {"entry_ts": 1, "dir": -1, "price": price, "stop": stop,
            "tag": "T", "gate_tag": None, "h": {"spec": "H2", "dir": -1}}


def test_eod_flat_precondition_asserted():
    cfg = scenario_cfg({"execution_vehicle.mode": "cash_cfd"})
    with pytest.raises(ValueError):
        Broker(cfg, Narrative(), eod_fn=None)


def test_short_fills_at_bid_with_basis_mapped_stop():
    b, cfg = _mk()
    b.set_quote({"open": 100.0, "high": 101, "low": 99, "close": 100.5,
                 "spread": 1.0})
    assert b.open_position(_entry(price=132.0, stop=140.0))  # fut prices
    p = b.position
    assert p["entry"] == 99.5            # bid = mid - spread/2 (short entry)
    assert p["basis_at_entry"] == 32.0   # fut 132 - cash open 100
    assert p["stop"] == 108.0            # fut stop 140 - basis
    assert p["stop_dist"] == 8.0         # R stays in futures points
    # short stop exits at ASK: hit when ask_high >= stop
    b.set_quote({"open": 106.0, "high": 107.8, "low": 105.5, "close": 107.5,
                 "spread": 1.0})
    b.on_exec_bar(Bar(2, 138, 140.2, 137.5, 139.9, 10, tf="1min"))
    tr = b.trades[-1]
    assert tr["reason"] == "STOP" and tr["exit"] == 108.0
    assert tr["costs"] == 0.0            # spread is the only cost


def test_min_stake_skips():
    b, cfg = _mk({"execution_vehicle.min_stake_per_point": 99999})
    b.set_quote({"open": 100.0, "high": 101, "low": 99, "close": 100.5,
                 "spread": 1.0})
    assert not b.open_position(_entry(price=132.0, stop=140.0))
    assert b.skipped_size == 1 and b.position is None
