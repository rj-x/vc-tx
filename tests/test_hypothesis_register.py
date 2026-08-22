"""Register 35: the canonical hypothesis register governs the scoreboard —
a row whose ID isn't in the register (or isn't signal-live) is refused."""
import pytest

from backtest.scoreboard import register_status, validate_rows
from engine.signal_watch import FIRING_CONDITIONS


def test_register_has_ten_entries_with_statuses():
    reg = register_status()
    assert sorted(reg) == list(range(1, 17))
    assert all(v in ("signal-live", "definition-pending", "disabled")
               for v in reg.values())
    # ratification sitting part 1 (2026-08-20): all twelve signal-live
    assert all(v == "signal-live" for v in reg.values())


def test_current_rows_validate():
    validate_rows()


def test_unknown_id_refused():
    # schema v2 (register 49): S<k>-H<n> only; lab serials, the old S-H<n>
    # form, -ctx suffixes, and free names are all refused
    for bad in ("S-T3B", "S-H1", "LEGACY-NAME", "S1-H1-ctx"):
        FIRING_CONDITIONS[bad] = lambda *a: None
        try:
            with pytest.raises(ValueError, match=r"S<k>-H<n>"):
                validate_rows()
        finally:
            del FIRING_CONDITIONS[bad]
    FIRING_CONDITIONS["S0-H99"] = lambda *a: None
    try:
        with pytest.raises(ValueError, match="not in the canonical"):
            validate_rows()
    finally:
        del FIRING_CONDITIONS["S0-H99"]
    # the not-signal-live branch: no live fixture remains (all twelve are
    # live) — exercise it against a patched register
    import backtest.scoreboard as sb
    orig = sb.register_status
    sb.register_status = lambda: {n: ("definition-pending" if n == 1
                                      else "signal-live")
                                  for n in range(1, 17)}
    try:
        with pytest.raises(ValueError, match="not signal-live"):
            validate_rows()
    finally:
        sb.register_status = orig


def test_question_family_closure():
    """Register 54: Q<k>-H<n> is the third and FINAL identifier family —
    parsed from the register, bound to its hypothesis, malformed refused."""
    from backtest.scoreboard import parse_questions, validate_question_ids
    qs = parse_questions()
    assert qs.get(1) == ["Q1-H1"] and qs.get(7) == ["Q1-H7"]
    assert qs.get(11) == ["Q1-H11"] and qs.get(9) == ["Q2-H9"]
    assert qs.get(6) == ["Q1-H6"]
    validate_question_ids()                    # current doc passes
    import backtest.scoreboard as sb
    orig = sb.parse_questions
    for bad, n in ((["Q-H1-GEN"], 1), (["Q1-H2"], 1), (["QX-H1"], 1)):
        sb.parse_questions = lambda b=bad, m=n: {m: b}
        try:
            with pytest.raises(ValueError, match=r"Q<k>-H<n>"):
                validate_question_ids()
        finally:
            sb.parse_questions = orig
