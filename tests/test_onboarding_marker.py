"""Register 98 pin: ONBOARDING.md §4 is marker-driven — its stated
Register-current-through may lag the register by at most 3 entries
(the campaign warns at the same bound); the backlog marker must match
the register exactly (register 55)."""
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def _latest_register():
    txt = open(os.path.join(ROOT, "audit",
                            "strategy_findings_and_risks.md")).read()
    return max(int(x) for x in re.findall(r"^(\d+)\.\s\*\*", txt, re.M))


def test_onboarding_marker_within_three_of_register():
    ob = open(os.path.join(ROOT, "ONBOARDING.md")).read()
    m = re.search(r"Register-current-through:\s*(\d+)", ob)
    assert m, "ONBOARDING.md must carry a Register-current-through marker"
    assert _latest_register() - int(m.group(1)) <= 3


def test_backlog_marker_matches_register():
    bl = open(os.path.join(ROOT, "docs", "backlog_status.md")).read()
    m = re.search(r"Register-current-through:\s*(\d+)", bl)
    assert m and int(m.group(1)) == _latest_register()
