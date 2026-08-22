"""Artifact currency pin (register 25 family; added 2026-08-21 with the
scoreboard name alignment): every module's .md/.json pair must come from
the SAME run — the md's printed engine hash equals the json's
engine_commit. A stale half-pair is the incident class this prevents."""
import json
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "reports", "scoreboard")

PAIRS = [("hypothesis_performance.md", "hypothesis_performance.json"),
         ("recipe_performance.md", "recipe_performance.json"),
         ("excursion_profiles.md", "excursion_profiles.json"),
         ("flip_cut.md", "flip_cut.json"),
         ("cofire.md", "cofire.json"),
         ("location_census.md", "location_census.json"),
         (os.path.join("..", "SIGNAL_POINTS.md"), "signal_points.json")]


def test_md_json_pairs_are_from_the_same_run():
    stale = []
    for md_name, js_name in PAIRS:
        md_p, js_p = os.path.join(OUT, md_name), os.path.join(OUT, js_name)
        if not (os.path.exists(md_p) and os.path.exists(js_p)):
            continue
        m = re.search(r"Engine `([0-9a-f]{9})", open(md_p).read())
        js = json.load(open(js_p))
        commit = js.get("engine_commit", "")
        if not m or not commit.startswith(m.group(1)):
            stale.append(f"{md_name} ({m.group(1) if m else '?'}) vs "
                         f"{js_name} ({commit[:9]})")
    assert not stale, "md/json pairs from different runs:\n" + "\n".join(stale)
