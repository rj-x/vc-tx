"""Register 60: the glossary is ENFORCEABLE — same pattern as the
identifier validator. The sweep extracts uppercase terms from the
generated reports, the register, and docs; every term must either be a
plain-English dictionary word (caps-for-emphasis) or be defined in
docs/GLOSSARY.md. An undefined term fails the suite: new terms enter the
glossary in the same commit that first uses them, or the commit doesn't
pass."""
import glob
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GLOSSARY = os.path.join(ROOT, "docs", "GLOSSARY.md")

# this week's offenders — must be defined regardless of any exemption
# (MAE is a dictionary word; the operator named it anyway)
REQUIRED_SEEDS = ["MAE", "MFE", "ND", "NS", "PoC",
                  "S-numbers", "Q-numbers", "R- prefix", "B- prefix"]

# register/serial shapes are covered by the glossary's family entries,
# not per-instance lines
SERIAL = re.compile(r"^(?:H|S|Q|R|A|F|P|T|B)\d+[A-Z]?$")

WORDS_FILE = "/usr/share/dict/words"


def _sweep_targets():
    return (sorted(glob.glob(os.path.join(ROOT, "reports", "scoreboard",
                                          "*.md")))
            + sorted(glob.glob(os.path.join(ROOT, "docs", "*.md")))
            + [os.path.join(ROOT, "reports", p) for p in
               ("DASHBOARD.md", "SIGNAL_POINTS.md", "backtest_v1.md")]
            + [os.path.join(ROOT, "audit",
                            "strategy_findings_and_risks.md")])


# plain-English words the system dictionary (web2, 1934) happens to
# lack — emphasis exemptions, NOT domain terms; domain terms go in the
# glossary
EMPHASIS_EXTRA = {"held", "checklist", "intraday", "readout", "readouts",
                  "standalone", "retro"}


def _tokens(text):
    """Maximal uppercase runs (underscores/hyphens included). Tokens cut
    off by a truncation ellipsis ("ILLUSTRATI...") are skipped — they are
    display artifacts, not terms."""
    out = []
    for m in re.finditer(r"\b[A-Z][A-Z0-9]+(?:[-_][A-Z0-9]+)*\b", text):
        if text[m.end():m.end() + 3] == "..." \
                or text[m.end():m.end() + 1] == "…":
            continue
        out.append(m.group(0))
    return out


def test_glossary_defines_every_swept_term():
    assert os.path.exists(GLOSSARY), "docs/GLOSSARY.md missing"
    gloss = open(GLOSSARY).read()
    for seed in REQUIRED_SEEDS:
        assert seed in gloss, f"seed offender undefined: {seed}"
    words = set()
    if os.path.exists(WORDS_FILE):
        words = {w.strip().lower() for w in open(WORDS_FILE,
                                                 errors="ignore")}
    assert words, "dictionary unavailable — the emphasis exemption " \
                  "cannot run; define terms or restore the word list"
    gloss_low = gloss.lower()

    def english(low):
        """The dictionary plus simple inflections (web2 lacks plurals,
        past tense, -ing forms)."""
        if low in words:
            return True
        for suf, reps in (("ies", ["y"]), ("ied", ["y"]), ("es", ["", "e"]),
                          ("s", [""]), ("ed", ["", "e"]),
                          ("ing", ["", "e"]), ("d", [""]),
                          ("ly", [""]), ("er", ["", "e"]),
                          ("est", ["", "e"])):
            if low.endswith(suf) and len(low) > len(suf) + 2:
                stem = low[:-len(suf)]
                if any(stem + r in words for r in reps):
                    return True
                if stem[-1] == stem[-2:-1] and stem[:-1] in words:
                    return True             # doubled consonant (REGRETTED)
        return False

    def defined(tok):
        if tok in gloss or tok.lower() in gloss_low:
            return True
        if SERIAL.fullmatch(tok):
            return True                     # family entries cover serials
        if "_" in tok:
            return True                     # code identifier, not prose —
                                            # the identifier validators
                                            # govern those
        if english(tok.lower()) or tok.lower() in EMPHASIS_EXTRA:
            return True                     # caps-for-emphasis English
        if re.fullmatch(r"\d+[A-Z]?", tok):
            return True
        parts = tok.split("-")
        if len(parts) > 1:
            return all(defined(p) for p in parts if p)
        return False

    offenders = {}
    for path in _sweep_targets():
        if not os.path.exists(path):
            continue
        if os.path.abspath(path) == os.path.abspath(GLOSSARY):
            continue
        for tok in set(_tokens(open(path).read())):
            if not defined(tok):
                offenders.setdefault(tok, []).append(
                    os.path.relpath(path, ROOT))
    assert not offenders, (
        "undefined terms — add them to docs/GLOSSARY.md in this commit:\n"
        + "\n".join(f"  {t}: {sorted(set(ps))}"
                    for t, ps in sorted(offenders.items())))
