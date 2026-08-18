"""Register 32: the parameter registry is canonical and GENERATED.
(1) Regeneration must be clean against HEAD — a parameter change without a
regenerated registry fails here (the drift pin; regeneration also rides the
weekly campaign). (2) Pre-registrations after the adoption date must cite
their yardsticks by registry reference — the trial log refuses entries
without the field going forward."""
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "scripts"))

YARDSTICKS_REQUIRED_FROM = "2026-08-19"       # adoption: register 32


def test_registry_regeneration_clean_against_head():
    import param_registry
    generated = param_registry.generate()
    committed = open(os.path.join(ROOT, "docs", "parameter_registry.md")).read()
    assert generated == committed, (
        "docs/parameter_registry.md is stale — a swept parameter changed "
        "without regenerating the registry (scripts/param_registry.py)")


def test_preregistrations_cite_yardsticks():
    path = os.path.join(ROOT, "reports", "lab", "trial_log.jsonl")
    offenders = []
    for line in open(path):
        e = json.loads(line)
        if (e.get("name", "").startswith("prereg")
                and e.get("ts", "") >= YARDSTICKS_REQUIRED_FROM
                and "yardsticks" not in e):
            offenders.append(e["name"])
    assert not offenders, (
        f"pre-registrations without a yardsticks field (registry citations "
        f"mandatory from {YARDSTICKS_REQUIRED_FROM}): {offenders}")
