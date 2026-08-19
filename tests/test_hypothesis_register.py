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
    # ratification sitting part 1 (2026-08-20): all twelve signal-live
    assert all(v == "signal-live" for v in reg.values())


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
    # the not-signal-live branch: no live fixture remains (all twelve are
    # live) — exercise it against a patched register
    import backtest.scoreboard as sb
    orig = sb.register_status
    sb.register_status = lambda: {n: ("definition-pending" if n == 1
                                      else "signal-live")
                                  for n in range(1, 13)}
    try:
        with pytest.raises(ValueError, match="not signal-live"):
            validate_rows()
    finally:
        sb.register_status = orig
    FIRING_CONDITIONS["LEGACY-NAME"] = lambda *a: None
    try:
        with pytest.raises(ValueError, match="S-H<n>"):
            validate_rows()
    finally:
        del FIRING_CONDITIONS["LEGACY-NAME"]
