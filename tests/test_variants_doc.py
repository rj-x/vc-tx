"""Register 116 pins: every variant name appearing in the journal has
a rendered VARIANTS.md section (the glossary-enforcement pattern
applied to strategies); the trade layer's counted tuple is documented
even before it reaches the journal; and the page regenerates clean
against the working tree (the param-registry pattern — a recipe change
without a regenerated page fails the suite)."""
import csv
import os
import re

from backtest.variants_doc import DOC, generate
from backtest.trade_layer import TRADES_CSV, VARIANTS


def _sections(text):
    return set(re.findall(r"^## (R-[A-Z0-9-]+)$", text, re.M))


def test_every_journal_variant_documented():
    assert os.path.exists(DOC), "docs/VARIANTS.md missing"
    secs = _sections(open(DOC).read())
    journal = {r["variant"] for r in csv.DictReader(
        l for l in open(TRADES_CSV) if not l.startswith("#"))}
    missing = journal - secs
    assert not missing, ("journal variants without a VARIANTS.md "
                         f"section: {sorted(missing)} — regenerate "
                         "(python -m backtest.variants_doc) or register "
                         "the variant properly")
    assert set(VARIANTS) <= secs, "counted tuple not fully documented"


def test_regeneration_clean_against_tree():
    assert generate() == open(DOC).read(), (
        "docs/VARIANTS.md is stale against the recipe structures — "
        "regenerate: python -m backtest.variants_doc")


def test_dashboard_generates_with_commented_journal():
    # the register-116 incident pin: the journal's '#' header line
    # crashed the dashboard's Q2-H11 clock reader at the post-commit
    # regeneration (an eleventh call site the sweep missed — it opened
    # the path through a local variable); every journal reader must
    # survive the header line
    assert open(TRADES_CSV).readline().startswith("#"), \
        "the journal header line is the fixture — it must exist"
    from backtest.dashboard import generate as dash_generate
    assert "DASHBOARD" in dash_generate()
