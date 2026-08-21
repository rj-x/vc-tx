"""Canonical parameter registry generator (register 32, Part A order
2026-08-18). Emits docs/parameter_registry.md — every yardstick/threshold/
default/assumption in force: value, source, date set (git blame), authority.

Rules of the sweep:
  - config.yaml leaves, frozen_v1 config_overrides, and module-level
    UPPERCASE literal constants in engine/ + backtest/ are swept
    mechanically.
  - Authority comes ONLY from the curated AUTHORITY map below. A swept
    value with no authority trail is FLAGGED (pending-ruling batch), never
    given an invented one.
  - RATIFIED_YARDSTICKS holds operator-ratified yardsticks that have no
    code site yet (registry-first entries).
  - Output is DETERMINISTIC (no generation timestamp); a test pins that
    regeneration is clean against HEAD; regeneration rides the weekly
    campaign.
"""

import ast
import os
import re
import subprocess

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOC = os.path.join(ROOT, "docs", "parameter_registry.md")

FOUNDING = ("founding config — RULES v3.1 contract era (owner rulings "
            "A1–A17 / R1–R6)")

# Curated authority trails. Keys: dotted config path, or "file.py:CONST".
AUTHORITY = {
    # -- config.yaml with specific post-founding history
    "features.baseline_sessions": "frozen compromise vs spec 20 (data poverty; backtest_v1 standing flag 1) — value here is the SPEC default; the operative 8 lives in frozen_v1 overrides",
    "features.min_baseline_obs": "frozen compromise vs spec 20 (data poverty; backtest_v1 standing flag 1) — operative 5 in frozen_v1 overrides",
    "hypotheses.test_proximity_atr": "RULES Sec 0 TEST criteria (i) — founding",
    "hypotheses.test_vol_vs_signature": "RULES Sec 0 TEST criteria (v) — founding",
    "migration.min_child_labels": "H9 candidate registration (persistence clause) + migration build 2026-08-15",
    "migration.recruitment_floor": "H9 candidate registration (falsifiable recruitment clause) + migration build 2026-08-15",
    # -- code constants
    "paper.py:SUSPENSION_THRESHOLD": "register finding 26 (machine-suspension detection; 5 min aligned with COVERAGE_GAP convention)",
    "store_loader.py:SEALED_SCHEDULE_START": "register 30 — standing sealed-window schedule, calendar-declared 2026-08-18",
    "store_loader.py:SEALED_MONTHS": "register 30 — quarterly anchor months (Sep/Dec/Mar/Jun)",
    "store_loader.py:SEALED_DAYS": "register 30 — first two weeks (days 1–14 inclusive, UTC)",
    "forward_migration.py:ESTABLISHED_TREND_AGE": "T1d establishment cell (age>=10) via prereg_T3_build; reused by forward readout",
    "forward_migration.py:EXPECT_WINDOW": "pre-registered 11:46Z expectation window (trial log 2026-08-18)",
    "forward_migration.py:EXPECT_DIR": "pre-registered 11:46Z expectation (decline)",
    "forward_migration.py:EXPECT_MIN_DEPTH": "pre-registered grading criterion ('deep' >= 3 rungs); graded MISS with semantics finding (register 28/29)",
    "forward_migration.py:EXPECT_UNRECRUITED_FRAC": "pre-registered grading criterion ('predominantly unrecruited')",
    "migration.py:LADDER": "six-rung doctrine (cascade analysis, register; ladder build 2026-08-14)",
    "horizons.py:STANDARD_HORIZONS": "operator ratification 2026-08-18 (batch R1) — ONE project-wide set of outcome marks; supersedes eventstudy (5,10,20) and expansion (5,15,30); different marks require re-registration with stated reason",
    "expansion.py:NOMINAL_BUFFER_PTS": "operator ratification 2026-08-18 (batch R1) — revisit if level-touch analysis becomes load-bearing",
    "macro.py:NFP_ANCHORS": "external fact, verified 2026-08-18 (BLS Employment Situation: 8:30 a.m. ET first Friday; 12:30Z in EDT / 13:30Z in EST — the DST-spanning UTC pair)",
    "scoreboard.py:QUALIFYING_ATR_MULT": "cites registry qualifying_move (operator ratification 2026-08-18) — code mirror of the ratified 1.5x",
    "scoreboard.py:MAJOR_ATR_MULT": "cites registry major_move (operator ratification 2026-08-18) — code mirror of the ratified 3x",
    "scoreboard.py:MOVE_WINDOW_MIN": "cites registry qualifying_move 60-minute clause; reused as coverage lookback per prereg_scoreboard_operationalization",
    "signal_watch.py:H9_CHAIN_DEPTH_MIN": "operator pre-registration 2026-08-19 (register 36 item 4): H9 fire = migration chain depth >= 2, stamped at completing event close; changeable only by re-registration",
    "scoreboard.py:SMALL_N_FIRES": "operator order 2026-08-19 (register 38): fires<20 dimmed + excluded from label arithmetic",
    "scoreboard.py:SMALL_N_EPISODES": "operator order 2026-08-19 (register 38): episodes<10 dimmed + excluded from label arithmetic",
    "scoreboard.py:MARKER_BAND_PP": "register 38 presentation convention (±2pp at-chance band for the ▲/▼/· markers) — implementer-proposed, operator ratification pending",
    "recipes.py:RECIPE_SETS": "register 44 — recipe_set_v0.2 adds R-FLIPGUARD (staged narrative candidate: flip-exit active ONLY before progress-arming; arming 1.0xATR(15M) OR 45 min, DERIVED-STATED from early-flip adversity + t-MFE 13-45min, ratification pending; graded on forward accrual alongside R-OP1). Prior: recipe_set_v0.1 (grammar v1): v0 four ILLUSTRATIVE-UNRATIFIED (provenance: operator design examples; R-TRAIL-ATR 0.5x offset a reviewer invention with no basis; ATR TFs retro-annotated 15M) + R-OP1 OPERATOR-RATIFIED 2026-08-19 (1.5xATR initial [TF ASSUMED 15M — unstated, flagged] composed tighter-of with 5.0pt trail beyond 2nd-previous settled 1M bar; 5.0pt offset is instrument-absolute — cross-instrument v1 may want ATR-relative, operator's later call); changes only by re-registration, trial-log counted",
    "recipes.py:RECIPE_SET_VERSION": "register 41/42/44 — the set version every recipe artifact must state",
    "vwap_census.py:BANDS": "band edges stated at pre-registration (prereg_vwap_census, register 51): at<=0.5 / 1s(0.5,1.5] / 2s(1.5,2.5] / beyond>2.5 sigma",
    "cofire.py:WINDOWS_MIN": "operator-set co-fire windows {5,15} min (activation order 2026-08-20; prereg_cofire_census)",
    "cofire.py:FAMILIES": "operator-set family partition (event/texture/structure; within-family excluded, H2/H8 pair excluded outright)",
    "volume_profile.py:LOOKBACK_CANDIDATES": "organ #2 lookback candidate grid (register 45 build; the DERIVED value is in the H11 proposal, ratification pending)",
    "excursions.py:WINDOW_NS": "cites registry qualifying_move 60-min window (excursion study, register 42 item 7)",
    "signal_watch.py:H5_EXTENSION_ATR": "founding h5.extension_atr, cited; H5 ratified as drawn 2026-08-20 (register 46), 15M read",
    "signal_watch.py:H5_MA_PERIOD": "founding h5.ma_period, cited (register 46)",
    "signal_watch.py:H6_PROX_ATR_FRAC": "ratified 2026-08-20 (register 46; founding level-identity tolerance reused)",
    "signal_watch.py:H6_SPREAD_PCTILE": "ratified 2026-08-20 (measured day-relative p90)",
    "signal_watch.py:H6_CLOSE_POS": "ratified 2026-08-20 (founding close_pos_lo neighborhood)",
    "signal_watch.py:H6_WICK_FRAC": "ratified 2026-08-20 (founding wick_frac_min, cited)",
    "signal_watch.py:H6_DAY_WINDOW": "IMPLEMENTER CONSTANT (trailing day-relative baseline, 480 x 1M bars) — H6's registered free parameter; operator-adjustable, flagged",
    "signal_watch.py:H11_BUCKET_PTS": "ratified 2026-08-20 (home-derived median 1M true range; MIS-SCALE caveat on other instruments)",
    "signal_watch.py:H11_LOOKBACK_SESS": "ratified 2026-08-20 (best-of-weak-field; weak-persistence flag stands in the register entry)",
    "signal_watch.py:H12_MIN_VISITS": "ratified 2026-08-20 (proposal derivation: exceed the founding H3 cluster's 2)",
    "signal_watch.py:H12_WINDOW_MIN": "ratified 2026-08-20 (1.5x the registered move window)",
    "signal_watch.py:H12_DRY_RV": "ratified 2026-08-20 (founding low_volume_mult, cited)",
    "signal_watch.py:H13_VALUE_AREA_PCT": "operator-specified at S0-H13 registration 2026-08-20 (register 50; standard value-area convention); H13's other parameters cite H11's ratified config + founding baseline machinery",
    "signal_watch.py:ESTABLISHED_TREND_AGE": "T1d establishment cell (age>=10) — S-T3B row fires on T1d's measured conditions exactly (prereg_signal_rows_v1)",
    "signal_watch.py:SEQUENCE_N": "S-EFFORTLESS-SEQ sequence clause: 2 consecutive same-direction effortless prints (prereg_signal_rows_v1; operator-reviewable)",
    "lab.py:TRIAL_LOG": "lab discipline — immutable multiple-comparisons record (execution-layer build order)",
    "t3.py:ESTABLISHED_TREND_AGE": "T1d establishment cell (age>=10), pinned in prereg_T3_build",
}

# Structural/definitional constants — not yardsticks; listed, not flagged.
DEFINITIONAL = {
    "pipeline.py:_TF_MINUTES", "loop.py:_TFMIN", "migration.py:_MIN",
    "forward_migration.py:_TFMIN", "resample.py:_TFMIN",
    "classifier.py:CLIMAX_LABELS", "context.py:CLIMAX_LABELS",
    "context.py:_REGISTRY_SPECS", "hypotheses.py:SPECS",
    "hypotheses.py:OPEN", "hypotheses.py:CPG", "hypotheses.py:LONG",
    "hypotheses.py:SHORT", "eventstudy.py:LABEL_DIR",
    "t3.py:FUNNEL_EVENTS", "campaign.py:VARIANTS",
    "campaign.py:BASE_OVERRIDES", "ledger.py:_TFMIN",
    "narrate.py:TF_MINUTES", "store_loader.py:TF_MINUTES",
}

# Operator-ratified yardsticks with no code site yet (registry-first).
RATIFIED_YARDSTICKS = [
    ("qualifying_move", ">= 1.5 x 15M ATR, one-directional, within 60 min, drift-adjusted",
     "registry seed (no code site yet)", "2026-08-18",
     "operator ratification 2026-08-18 (register 31 revision) — changed only by re-registration"),
    ("major_move", ">= 3 x 15M ATR, same clause",
     "registry seed (no code site yet)", "2026-08-18",
     "operator ratification 2026-08-18 (register 31 revision) — changed only by re-registration"),
    ("signal_payoff_window", "+60 min from fire (the registered move-definition window); signed excursion by predicted direction; mid-price, no spread, idealized; standard-horizon marks additionally in the JSON artifact",
     "backtest/scoreboard.py:_payoff", "2026-08-19",
     "register 38 (operator order 2026-08-19) — changeable only by re-registration"),
    ("session_partition", "london [08:00 Europe/London -> 09:30 America/New_York) | overlap [-> 16:30 Europe/London) | ny_only [-> 16:00 America/New_York) | dead [-> 09:00 Asia/Tokyo) | asia [-> 08:00 Europe/London); native-tz boundaries, DST-proof; finer cuts only by re-registration with a stated question",
     "backtest/sessions.py:session_of", "2026-08-19",
     "register 37 (operator order 2026-08-19); TWO INTERPRETATION FLAGS operator-correctable: London-only end taken as NY open per the Overlap clause (the order's '(08:00-13:30 local)' parenthetical matches neither tz); Asia open taken as Tokyo cash 09:00 JST (unspecified in the order)"),
    ("label_bearing_sessions_PROPOSAL", "london + overlap as the tradeable window for criteria scoping — PROPOSAL ONLY, UNRATIFIED; criteria compute on whole windows until operator ratification",
     "register 37", "2026-08-19",
     "registered proposal, awaiting operator ratification"),
    ("either_direction_chance_baseline", "the either-direction bar-qualify base rate, computed per window and shown beside every either-direction precision",
     "backtest/scoreboard.py:score (agnostic mode)", "2026-08-19",
     "register 36 (direction-agnostic grading mode, operator order 2026-08-19)"),
    ("review_promote_min_fires", "30 per window (promote-candidate requires above-chance precision in BOTH windows at this n)",
     "register 36 criteria", "2026-08-19",
     "register 36 governance; number implementer-proposed, operator ratification pending"),
    ("review_deprioritize_min_fires", "100 in the larger window (deprioritize requires at/below-chance precision at this n with no redeeming metric)",
     "register 36 criteria", "2026-08-19",
     "register 36 governance; number implementer-proposed, operator ratification pending"),
    ("move_episode_dedup", "overlapping qualifying windows of one direction merge into MAXIMAL episodes (never counted separately)",
     "backtest/scoreboard.py:build_moves", "2026-08-18",
     "operator ratification 2026-08-18 (episode-counting ruling) — the shipped artifact already counted merged; no re-emit needed"),
    ("watchdog_feed_pause_utc", "[21:00, 22:10) UTC + weekend Fri 21:00Z -> Sun 22:10Z",
     "engine/paper.py:expect_prints (inline)", "2026-08-18",
     "measured constant — register finding 24 (store-measured pause 21:00Z/22:05Z + 5 min margin)"),
]


def _blame_dates(relpath):
    """line -> YYYY-MM-DD from git blame (uncommitted lines -> 'uncommitted')."""
    out = subprocess.run(["git", "blame", "--line-porcelain", relpath],
                         cwd=ROOT, capture_output=True, text=True).stdout
    dates, line_no, cur = {}, 0, None
    for ln in out.splitlines():
        if re.match(r"^[0-9a-f]{40} ", ln):
            line_no = int(ln.split()[2])
            cur = None
        elif ln.startswith("author-time "):
            import datetime as dt
            cur = dt.datetime.fromtimestamp(int(ln.split()[1]),
                                            dt.timezone.utc).strftime("%Y-%m-%d")
        elif ln.startswith("\t"):
            dates[line_no] = cur or "uncommitted"
    return dates


def sweep_config():
    rows = []
    path = os.path.join(ROOT, "config.yaml")
    dates = _blame_dates("config.yaml")
    stack = []
    for i, raw in enumerate(open(path), 1):
        line = raw.rstrip("\n")
        m = re.match(r"^( *)([A-Za-z_][A-Za-z0-9_]*):\s*(.*)$", line)
        if not m:
            continue
        indent, key, rest = len(m.group(1)) // 2, m.group(2), m.group(3)
        stack = stack[:indent] + [key]
        val = rest.split("#")[0].strip()
        comment = rest.split("#", 1)[1].strip() if "#" in rest else ""
        if not val:
            continue                      # section header
        dotted = ".".join(stack)
        auth = AUTHORITY.get(dotted, FOUNDING)
        rows.append((dotted, val, f"config.yaml:{i}",
                     dates.get(i, "?"), auth, comment))
    return rows


def sweep_frozen():
    rows = []
    path = os.path.join(ROOT, "definitions", "frozen_v1.yaml")
    dates = _blame_dates("definitions/frozen_v1.yaml")
    for i, raw in enumerate(open(path), 1):
        m = re.match(r"^  ([A-Za-z0-9_.]+):\s*([^#]+?)\s*(?:#\s*(.*))?$", raw.rstrip())
        if m and "." in m.group(1):
            rows.append((m.group(1), m.group(2),
                         f"definitions/frozen_v1.yaml:{i}",
                         dates.get(i, "?"),
                         "frozen_v1 pinned override (hash-pinned definition; "
                         "campaign bit-identical pin)", m.group(3) or ""))
    return rows


def _has_number(node):
    """True iff the AST value contains a numeric literal anywhere — the
    mechanical test for 'is this a yardstick candidate'. Path/plumbing and
    pure-name structures carry no numbers and are skipped."""
    for n in ast.walk(node):
        if isinstance(n, ast.Constant) and isinstance(n.value, (int, float)) \
                and not isinstance(n.value, bool):
            return True
    return False


def _is_plumbing(src_text):
    return any(tok in src_text for tok in
               ("__file__", "os.path", "open(", "ROOT"))


def sweep_constants():
    rows, flagged = [], []
    for d in ("engine", "backtest"):
        base = os.path.join(ROOT, d)
        for f in sorted(os.listdir(base)):
            if not f.endswith(".py"):
                continue
            rel = f"{d}/{f}"
            src = open(os.path.join(base, f)).read()
            tree = ast.parse(src)
            dates = None
            for node in tree.body:
                if not isinstance(node, ast.Assign) or len(node.targets) != 1:
                    continue
                t = node.targets[0]
                if not (isinstance(t, ast.Name) and t.id.isupper()):
                    continue
                key = f"{f}:{t.id}"
                val = ast.get_source_segment(src, node.value)
                if key in DEFINITIONAL or _is_plumbing(val):
                    continue
                if key not in AUTHORITY and not _has_number(node.value):
                    continue              # name enumerations: not yardsticks
                if val and len(val) > 60:
                    val = val[:57] + "..."
                if dates is None:
                    dates = _blame_dates(rel)
                row = (key, val, f"{rel}:{node.lineno}",
                       dates.get(node.lineno, "?"),
                       AUTHORITY.get(key), "")
                if row[4] is None:
                    flagged.append(row)
                else:
                    rows.append(row)
    return rows, flagged


def generate():
    cfg = sweep_config()
    frz = sweep_frozen()
    consts, flagged = sweep_constants()
    L = ["# Canonical Parameter Registry (GENERATED — do not hand-edit)",
         "",
         "Generated by `scripts/param_registry.py`; regeneration rides the "
         "weekly campaign; `tests/test_param_registry.py` pins it clean "
         "against HEAD. **Rule (README): no test, analysis, census, or "
         "simulation may use an unregistered yardstick.** Values with no "
         "authority trail are flagged below — a flag is a finding, not a "
         "permission.",
         "",
         "## Operator-ratified yardsticks (registry-first)",
         "", "| yardstick | value | source | date set | authority |",
         "|---|---|---|---|---|"]
    for n, v, s, dt_, a in RATIFIED_YARDSTICKS:
        L.append(f"| {n} | {v} | {s} | {dt_} | {a} |")
    L += ["", "## config.yaml defaults", "",
          "| parameter | value | source | date set | authority | note |",
          "|---|---|---|---|---|---|"]
    for r in cfg:
        L.append("| " + " | ".join(str(x) for x in r) + " |")
    L += ["", "## frozen_v1 pinned overrides (operative values)", "",
          "| parameter | value | source | date set | authority | note |",
          "|---|---|---|---|---|---|"]
    for r in frz:
        L.append("| " + " | ".join(str(x) for x in r) + " |")
    L += ["", "## Code constants (engine/ + backtest/)", "",
          "| constant | value | source | date set | authority |",
          "|---|---|---|---|---|"]
    for r in sorted(consts):
        L.append("| " + " | ".join(str(x) for x in r[:5]) + " |")
    L += ["", "## FLAGGED — no authority trail (pending-ruling batch R1)",
          "",
          "Each needs one operator line: **ratify** (becomes authority) / "
          "**source** (cite the existing trail) / **fix** (wrong value). "
          "Batched for review, not dribbled.",
          "", "| constant | value | source | date set | disposition |",
          "|---|---|---|---|---|"]
    for r in sorted(flagged):
        L.append(f"| {r[0]} | {r[1]} | {r[2]} | {r[3]} | PENDING RULING |")
    L.append("")
    return "\n".join(L)


def main():
    doc = generate()
    with open(DOC, "w") as f:
        f.write(doc)
    n_flag = doc.count("PENDING RULING")
    print(f"wrote docs/parameter_registry.md ({n_flag} flagged for batch R1)")


if __name__ == "__main__":
    main()
