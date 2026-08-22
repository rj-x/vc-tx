"""The excursion-profiles incident (2026-08-19): a table emitted 9 data
cells under a 5-column separator — broken rendering. Pin: every table in
every generated scoreboard markdown has matching column counts across
header, separator, and rows."""
import glob
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def test_generated_tables_are_well_formed():
    bad = []
    pages = [os.path.join(ROOT, "reports", "SIGNAL_POINTS.md"),
             os.path.join(ROOT, "reports", "DASHBOARD.md")]
    for path in sorted(glob.glob(os.path.join(
            ROOT, "reports", "scoreboard", "*.md"))) \
            + [p for p in pages if os.path.exists(p)]:
        lines = open(path).read().splitlines()
        for i, ln in enumerate(lines):
            if re.match(r"^\|(---\|)+$", ln.replace(" ", "")):
                ncols = ln.count("---")
                if i and lines[i - 1].startswith("|") \
                        and lines[i - 1].count("|") - 1 != ncols:
                    bad.append(f"{path}:{i}: header")
                j = i + 1
                while j < len(lines) and lines[j].startswith("|"):
                    if lines[j].count("|") - 1 != ncols:
                        bad.append(f"{path}:{j + 1}: row")
                    j += 1
    assert not bad, "malformed markdown tables:\n" + "\n".join(bad[:10])
