"""Register item 11 guard, AMENDED per register 31 revision (approved
2026-08-18): candidate-hypothesis (H6+) firing conditions are permitted in
ONE dedicated signal module (engine/signal_watch.py); everywhere else in
engine//backtest/ the identifiers stay banned. The guard's purpose —
candidates cannot influence decisions — is preserved by IMPORT-DIRECTION
enforcement: no decision path may import the signal module."""
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PATTERN = re.compile(r"\bH[6-9]\b")
SIGNAL_MODULE = os.path.join("engine", "signal_watch.py")
# the only permitted importers of the signal module (reader + attach points)
IMPORT_ALLOWED = {os.path.join("backtest", "scoreboard.py"),
                  os.path.join("backtest", "recipes.py"),   # register 41 reader
                  os.path.join("backtest", "excursions.py"),  # register 42 reader
                  os.path.join("backtest", "flip_cut.py"),    # register 43 reader
                  os.path.join("backtest", "cofire.py"),      # register 45 reader
                  os.path.join("backtest", "location_census.py"),  # register 48
                  os.path.join("engine", "paper.py"),
                  os.path.join("engine", "narrate.py")}


def test_no_candidate_identifiers_in_code():
    hits = []
    for d in ("engine", "backtest"):
        for base, _, files in os.walk(os.path.join(ROOT, d)):
            for f in files:
                if f.endswith(".py"):
                    p = os.path.join(base, f)
                    if os.path.relpath(p, ROOT) == SIGNAL_MODULE:
                        continue          # the one permitted home
                    for i, line in enumerate(open(p), 1):
                        if PATTERN.search(line):
                            hits.append(f"{p}:{i}: {line.strip()}")
    assert not hits, ("candidate hypotheses are walk-forward-only "
                      "(audit/candidate_hypotheses.md):\n" + "\n".join(hits))


def test_signal_module_import_direction():
    """No decision path imports the signal module — only the scoreboard
    reader and the live-loop attachment points may."""
    offenders = []
    for d in ("engine", "backtest"):
        for base, _, files in os.walk(os.path.join(ROOT, d)):
            for f in files:
                if not f.endswith(".py"):
                    continue
                p = os.path.join(base, f)
                rel = os.path.relpath(p, ROOT)
                if rel == SIGNAL_MODULE or rel in IMPORT_ALLOWED:
                    continue
                if "signal_watch" in open(p).read():
                    offenders.append(rel)
    assert not offenders, (
        f"signal module imported outside the permitted attach/read points "
        f"(guard: candidates cannot influence decisions): {offenders}")
