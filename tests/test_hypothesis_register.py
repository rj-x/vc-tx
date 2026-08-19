"""Register 35: the canonical hypothesis register governs the scoreboard —
a row whose ID isn't in the register (or isn't signal-live) is refused."""
import pytest

from backtest.scoreboard import register_status, validate_rows
from engine.signal_watch import FIRING_CONDITIONS


def test_register_has_ten_entries_with_statuses():
    reg = register_status()
    assert sorted(reg) == list(range(1, 13))
    assert all(v in ("signal-live", "definition-pending", "disabled")
               for v in reg.values())
    assert reg[5] == "definition-pending"   # revive-as-new, drafted 08-20
    assert reg[6] == "definition-pending"          # H8/H9 went signal-live
    assert reg[11] == reg[12] == "definition-pending"
    assert reg[8] == reg[9] == "signal-live"       # by operator order 08-19


def test_current_rows_validate():
    validate_rows()


def test_unknown_id_refused():
    FIRING_CONDITIONS["S-T3B"] = lambda *a: None      # legacy lab serial
    try:
        with pytest.raises(ValueError, match="S-H<n>"):
            validate_rows()
    finally:
        del FIRING_CONDITIONS["S-T3B"]
    FIRING_CONDITIONS["S-H99"] = lambda *a: None
    try:
        with pytest.raises(ValueError, match="not in the canonical"):
            validate_rows()
    finally:
        del FIRING_CONDITIONS["S-H99"]
    FIRING_CONDITIONS["S-H6"] = lambda *a: None       # definition-pending
    try:
        with pytest.raises(ValueError, match="not signal-live"):
            validate_rows()
    finally:
        del FIRING_CONDITIONS["S-H6"]
    FIRING_CONDITIONS["LEGACY-NAME"] = lambda *a: None
    try:
        with pytest.raises(ValueError, match="S-H<n>"):
            validate_rows()
    finally:
        del FIRING_CONDITIONS["LEGACY-NAME"]
