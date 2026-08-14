"""Register item 11 guard: candidate hypotheses (H6/H7) are pre-registered
walk-forward-only (H6-H9) — no identifier may appear in engine/ or backtest/."""
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PATTERN = re.compile(r"\bH[6-9]\b")


def test_no_candidate_identifiers_in_code():
    hits = []
    for d in ("engine", "backtest"):
        for base, _, files in os.walk(os.path.join(ROOT, d)):
            for f in files:
                if f.endswith(".py"):
                    p = os.path.join(base, f)
                    for i, line in enumerate(open(p), 1):
                        if PATTERN.search(line):
                            hits.append(f"{p}:{i}: {line.strip()}")
    assert not hits, ("candidate hypotheses are walk-forward-only "
                      "(audit/candidate_hypotheses.md):\n" + "\n".join(hits))
