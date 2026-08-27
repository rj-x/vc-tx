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
    "scoreboard.py:MARKER_BAND_PP": "register 38 presentation convention (±2pp at-chance band for the ▲/▼/· markers) — RATIFIED at the 2026-08-28 sitting (register 88)",
    "recipes.py:RECIPE_SETS": "register 94 — recipe_set_v0.7 adds the scalp arms (operator-ratified 2026-08-27, all four register-93 gates: entry next 1M open at the scalp sentence, resting target entry+0.5xATR(15M) with the 0.5pt one-tick haircut, 2.5xATR disaster-cap stop reuse, EOD-flat; plain + refined-entry arms, both counted; OPTIMISTIC target fill declared; v1 tighter stop derivation-required). Prior: register 82 — recipe_set_v0.6 adds R-NEXIT-SENT (sentence-only exits; the atoms-vs-sentences head-to-head vs R-NEXIT-FULL); EARLY/FULL relabeled atomic controls. Prior: register 81 — recipe_set_v0.5 adds R-NEXIT-EARLY/R-NEXIT-FULL (counted narrative-exit variants on R-ARM15 mechanics; the flip-gate-vs-census disagreement head-to-head). Prior: register 77 — recipe_set_v0.4 adds the management ladder v2 (R-BE / R-ARM15 [N=1 assumed, flagged] / R-NOTRAIL) beside R-OP2; honest-fills RULE 5 added (no-open when the stop at fill is at-or-beyond entry). Prior: register 76 — recipe_set_v0.3 adds R-OP2 (operator-specified 2026-08-24: 2.5xATR(15M) initial composed tighter-of with 0.25xATR(15M) trail beyond 2nd-previous settled 1M bar; ratchet-only, no target, EOD flat; the narrative trade layer recipe, UNREFINED per register 70). Prior: register 44 — recipe_set_v0.2 adds R-FLIPGUARD (staged narrative candidate: flip-exit active ONLY before progress-arming; arming 1.0xATR(15M) OR 45 min, DERIVED-STATED from early-flip adversity + t-MFE 13-45min, ratification pending; graded on forward accrual alongside R-OP1). Prior: recipe_set_v0.1 (grammar v1): v0 four ILLUSTRATIVE-UNRATIFIED (provenance: operator design examples; R-TRAIL-ATR 0.5x offset a reviewer invention with no basis; ATR TFs retro-annotated 15M) + R-OP1 OPERATOR-RATIFIED 2026-08-19 (1.5xATR initial [TF ASSUMED 15M — unstated, flagged] composed tighter-of with 5.0pt trail beyond 2nd-previous settled 1M bar; 5.0pt offset is instrument-absolute — cross-instrument v1 may want ATR-relative, operator's later call); changes only by re-registration, trial-log counted",
    "recipes.py:RECIPE_SET_VERSION": "register 41/42/44/76/77/81/82/94 — the set version every recipe artifact must state",
    "recipes.py:_SCALP_STAGES": "register 94: the scalp arms' shared stages — 2.5xATR(15M) disaster-cap stop reuse + atr_haircut target (0.5xATR, 0.5pt one-tick haircut, config tick_size cited) — operator-ratified 2026-08-27",
    "trade_layer.py:SCALP_VARIANTS": "register 94: the two counted scalp arms (plain + refined-entry) — run on the scalp's own sentence only",
    "trade_layer.py:SCALP_SENTENCE": "register 94: the scalp's sentence = the Q-chain's signal (register 92) — identifier built per the register-31 guard convention",
    "conditioning_matrix.py:COIL_WINDOW": "coil proxy RATIFIED as flagged at the 2026-08-28 sitting (register 88); proxy status stands — organ #3 is the eventual instrument",
    "conditioning_matrix.py:COIL_PCTILE": "coil proxy threshold RATIFIED as flagged at the 2026-08-28 sitting (register 88); proxy status stands",
    "excursion_geometry.py:TP_LADDER_ATR": "operator-set (register 52 order): TP ladder {0.5,1,1.5,2}xATR(15M)",
    "excursion_geometry.py:UNSTOPPED_ATR": "operator-set (register 52 order): -6xATR effectively-unstopped bound",
    "excursion_geometry.py:PTS_LADDER_HOME": "operator-set (register 52 order): uk100 home-scale reference ladder, labeled non-comparable",
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
    "signal_watch.py:H15_SPEED_LIMIT_MIN": "RATIFIED 2026-08-22 (register 57; derivation: measured t-MFE medians 25-33 min). Range definition = the phase tracker's own ranging object — no new free parameter, ratified as the best possible derivation",
    "signal_watch.py:H16_WINDOW_MIN": "GHLZ JFE 2018 window construction; operator order register 56",
    "account_mode.py:STAKE_DEFAULT": "register 83: fixed stake GBP0.5/pt, spread-bet native (operator-stated default)",
    "account_mode.py:LEVERAGE_DEFAULT": "register 83: 200:1 — LOOSE, FLAGGED OPERATOR-UNVERIFIED (calibrating fact recorded: GBP1/pt on GBP25 observed)",
    "account_mode.py:MAINTENANCE_PCT": "register 83: provider closeout at 50% of deposit requirement — FLAGGED operator-unverified default",
    "account_mode.py:MIN_STAKE_DEFAULT": "register 83: per-instrument minimum stake GBP0.5 — OPERATOR TO VERIFY minis",
    "account_mode.py:INITIAL_STOP_ATR": "register 83: risk-gate stop distance = the registered ladder-v2 initial stop (2.5xATR at the exec TF), cited",
    "journal_survey.py:MIN_CELL_N": "register 80: journal-survey cell measurability n>=25 — operator-stated in the order",
    "journal_survey.py:NULL_SHUFFLES": "register 80: concentration permutation null, pinned seeds (>=100 per the order)",
    "trade_forensics.py:MIN_CELL_N": "register 84: separator-cell measurability (wins+losses) — the journal-survey convention reused; also the NET LEDGER's forward-thin bar (84 amendment 2026-08-27)",
    "trade_forensics.py:TOP_LEDGER": "register 84 amendment (2026-08-27): NET LEDGER rows per market, drop count printed, full ledger in the JSON — implementer-proposed at the counted amendment, flagged",
    "underwater_census.py:TRAJ_BARS": "register 87: underwater trajectory window (MAE at bars 1..10) — operator-stated in the order",
    "underwater_census.py:CUT_KS": "register 87: bars-underwater cut grid {2,3,5} — operator-stated in the order",
    "underwater_census.py:MAE_CUTS_ATR": "register 87: MAE cut grid {0.5,1.0}xATR — operator-stated in the order",
    "underwater_census.py:BE_RUNGS_ATR": "register 87: BE ladder {0.25,0.5,1.0,1.5}xATR MFE — operator-stated in the order",
    "underwater_census.py:REENTRY_WINDOWS_MIN": "register 87: same-sentence re-fire windows {15,30,60} min — operator-stated in the order",
    "underwater_census.py:BACKOFF_KS": "register 87: consecutive-failure grid {2,3} — operator-stated in the order",
    "underwater_census.py:BACKOFF_WS": "register 87: suppression windows {5,15,30} bars — operator-stated in the order",
    "underwater_census.py:LOOP_RUNG_ATR": "register 87: the operator's fast-BE rung for the loop and backoff grids — implementer choice of 0.25 (the aggressive rung), flagged; other rungs' grids are a flagged follow-up",
    "underwater_census.py:STOP_ATR": "register 87: probe initial stop = the registered ladder-v2 2.5xATR(15M) (registers 76/77)",
    "underwater_census.py:LOUD_MULT": "register 66 founding volume cut (1.5 on time-matched rel_volume), reused",
    "underwater_census.py:MIN_CELL_N": "register 87: measurability n>=25 — the standing convention reused",
    "underwater_census.py:REF_K": "register 87: declared reference bar (k=3, middle of the cut grid) for the luck-budget field statistics — implementer-proposed at prereg, flagged",
    "underwater_census.py:SPLIT_MIN_PP": "register 87: qualifying gap 10pp — the register-84 convention reused",
    "underwater_census.py:NULL_SHUFFLES": "register 87: label-permutation null, 100 pinned seeds — the survey convention (register 73 clause 3 lineage)",
    "underwater_census.py:THESIS_SEEDS": "register 87: 20 random-thesis members, seeds range(60,80) — the B-RANDOM seed lineage, stated at prereg",
    "underwater_census.py:FAMILY_OF": "register 87: full-coverage signal-family map extending the registered cofire/trend groupings — implementer-proposed at prereg, FLAGGED for operator ratification",
    "h6_refinement.py:PROPOSAL_MIN_LEGS": "register 101: the joint v1 package emits only if cap@3 holds on the real basis on >= 3 forward legs — operator-stated in the order",
    "h6_refinement.py:STOP_PCTILE": "register 101: candidate stop = the p75 of forward non-reachers' MAE (xATR15) — implementer-proposed derivation at the counted amendment, FLAGGED; p50/p90 printed beside; nothing registers until the operator rules",
    "h6_refinement.py:SCALP_ARM": "register 101: the plain scalp arm's journal rows are the real basis (register 94 variant) — identifier built per the register-31 guard convention",
    "h6_refinement.py:SIGNAL": "register 100: the program's sentence = the scalp signal (the Q-chain's signal, register 92) — identifier built per the register-31 guard convention",
    "h6_refinement.py:COFIRE_BARS": "register 100: co-fire window +/-5 bars on the 1M axis — operator-stated in the order",
    "h6_refinement.py:SPLIT_MIN_PP": "register 100: qualifying split 10pp — the register-84 convention reused",
    "h6_refinement.py:MIN_SIDE_N": "register 100: both sides >= 10 — the matrix convention reused",
    "h6_refinement.py:CAND_MIN_LEGS": "register 100: candidate-grade needs >= 3 of 4 instruments — operator-stated in the order",
    "h6_refinement.py:CAP_KS": "register 100: time-cap grid {3,5,8} bars — operator-stated in the order",
    "h6_refinement.py:REACH_ATR": "register 100: the scalp target 0.5xATR (register 94), reused for the census economics",
    "h6_refinement.py:NULL_SHUFFLES": "register 100: label-permutation null, 100 pinned seeds — the survey convention",
    "zone_census.py:UNMEASURABLE_N": "register 95 item 2: cells n<10 unmeasurable — the conditioning-matrix convention reused",
    "zone_census.py:REVERSAL_MULTS": "register 96: the ladder's reversal multiples — the registered qualifying multiple (1.5) and its double; no invented number",
    "zone_census.py:SIG_SESSIONS": "register 96: extreme-significance filter {none,1,3,5}-session high/low — the source's own session structure",
    "zone_census.py:AGE_BINS": "register 96: freshness REPORTING bins from the same session ladder (<=1/<=3/<=5/>5 sessions) — bins, not thresholds",
    "zone_census.py:TOUCH_BINS": "register 96: touch-number reporting bins (1st/2nd/3rd/4+ visit) — bins, not thresholds",
    "zone_census.py:LOCATION_FAMILY": "register 95 item 2: the location family cross-reference (S0-H6 / S0-H11 / S1-H11 / S0-H13) — the zone census is its first higher-TF member",
    "capture_study.py:POLICIES": "register 88 item 4: the pre-registered protection ladder (4 BE rungs + 4 TRAIL arm x distance + 2 RATCHET schedules) — prereg_capture_study, counted",
    "capture_study.py:GAP_MIN_PTS": "register 88 item 4: tape-differentiation threshold 5 pts/trade — implementer-proposed at prereg, FLAGGED",
    "capture_study.py:NEVER_AGAIN_BOUND_ATR": "register 89 item 1: the operator's never-again bound (+1.0xATR MFE unprotected) — operator-stated in the order; a risk-rule pricing input, enactable by operator fiat once priced",
    "cofire_reread.py:CONS_MIN_CELLS": "register 73 consistency yardsticks reused (register 88 item 7, one emission)",
    "cofire_reread.py:CONS_MIN_N": "register 73 consistency yardsticks reused (register 88 item 7)",
    "cofire_reread.py:CONS_MIN_LIFT_PP": "register 73 consistency yardsticks reused (register 88 item 7)",
    "cofire_reread.py:CONS_PCTL": "register 73 consistency yardsticks reused (register 88 item 7)",
    "cofire_reread.py:NULL_SHUFFLES": "register 88 item 7: pinned sign-randomization null, 100 seeds — the survey-null lineage",
    "trade_forensics.py:MIN_SIDE_N": "register 84: each label side >=10 in a measurable cell — implementer-proposed at prereg, flagged",
    "trade_forensics.py:SPLIT_MIN_PP": "register 84: qualifying winner-loser split >=10pp — implementer-proposed at prereg, flagged",
    "trade_forensics.py:NULL_SHUFFLES": "register 84: win/loss label-permutation null, pinned seeds — the survey convention (register 73 clause 3 lineage)",
    "trade_forensics.py:CONT_WINDOWS_MIN": "register 84: post-exit continuation marks +30/+60 min — operator-stated in the order",
    "trade_forensics.py:INITIAL_STOP_ATR": "register 84: R-multiple denominator = the 2.5xATR(15M) initial stop shared by all seven journal variants (recipes v0.6, registers 76/77)",
    "trade_forensics.py:WATCH_MIN_N": "register 84: WATCH-list floor n>=12 — implementer-proposed at prereg, flagged",
    "trade_forensics.py:WATCH_CAP": "register 84: WATCH list top-20 per instrument, drop count printed — implementer-proposed at prereg, flagged",
    "trade_forensics.py:MAE_VARIANT": "register 84: winner-MAE reads R-NOTRAIL only (the unmanaged full-hold path isolates path pain from management) — stated in the prereg",
    "trade_layer.py:REFIRE_DEDUP_BARS": "register 77 clause 4: re-fire dedup, derivation = the sequel window (register 71/73 W=5); operator-ratification PENDING",
    "trade_layer.py:VARIANTS": "register 77: the management ladder v2 — the incumbent + three counted recipes; graded on the doctrine axes",
    "intra_trade_census.py:ARM_PROGRESS_ATR": "register 78: arming split CITES the ratified R-FLIPGUARD transition (register 46)",
    "intra_trade_census.py:ARM_AGE_MIN": "register 78: same cite",
    "intra_trade_census.py:EVENT_CLASSES": "register 78: in-trade event classes from the survey vocabulary — analysis splits, not a partition",
    "trade_layer.py:SENTENCES": "register 76: the three composite sentences the trade layer reports as is_composite — the minted S0 rows, not a tunable",
    "signal_watch.py:COMPOSITE_SENTENCES": "register 82: the minted composite sentences — the one home; future mints append here and every sentence-scoped consumer (R-NEXIT-SENT, the census's opposing-sentence class) follows automatically",
    "signal_watch.py:H17_SEQUEL_WINDOW": "register 76: composite sequel window, cited from the survey (register 71/73 W=5)",
    "signal_watch.py:QUAD_WIDE_PCTILE": "register 76: MIRROR of founding labels.wide_spread_pctile=80 (scoreboard-mirror precedent)",
    "signal_watch.py:QUAD_LOUD_MULT": "register 76: MIRROR of founding labels.high_volume_mult=1.5 (scoreboard-mirror precedent)",
    "signal_watch.py:H13_VALUE_AREA_PCT": "operator-specified at S0-H13 registration 2026-08-20 (register 50; standard value-area convention); H13's other parameters cite H11's ratified config + founding baseline machinery",
    "signal_watch.py:ESTABLISHED_TREND_AGE": "T1d establishment cell (age>=10) — S-T3B row fires on T1d's measured conditions exactly (prereg_signal_rows_v1)",
    "signal_watch.py:SEQUENCE_N": "S-EFFORTLESS-SEQ sequence clause: 2 consecutive same-direction effortless prints (prereg_signal_rows_v1; operator-reviewable)",
    "signal_points.py:LADDER_WIDTHS": "INSTRUMENTATION registered once (register 59; prereg_stopwidth_ladder): the stop-width ladder IS the measurement — values are not strategy parameters awaiting ratification; changes only by re-registration",
    "gap_census.py:GAP_BUCKETS_ATR": "IMPLEMENTER-PROPOSED abs-gap/ATR bucket edges (register 67), FLAGGED pending ratification",
    "gap_census.py:WEEKEND_MIN_H": "definitional seam-classification cutoff (register 67): a pause longer than 24h is a weekend",
    "gap_census.py:PAUSE_MIN_MIN": "definitional seam-classification cutoff (register 67): >5 min and <=24h is the instrument's daily pause (register-40 measured pauses all exceed it)",
    "narrative_survey.py:SEQUEL_WINDOWS": "register 73 (survey; inherits the register-71 pilot's operator-stated windows)",
    "narrative_survey.py:CONS_MIN_CELLS": "register 73 amendment (consistency statistic): >=3 measurable cells per qualifying pair — operator-stated",
    "narrative_survey.py:CONS_MIN_N": "register 73 amendment: cell measurability n>=15 for the consistency statistic — operator-stated",
    "narrative_survey.py:CONS_MIN_LIFT_PP": "register 73 amendment: |lift|>3pp in every cell of a qualifying pair — operator-stated",
    "narrative_survey.py:CONS_PCTL": "register 73 amendment: field percentile must exceed 95 for consistency-notable marking — operator-stated",
    "narrative_survey.py:NULL_SHUFFLES": "register 73 clause 3: 100 label-permutation shuffles, pinned seed set — the field's luck budget",
    "sequel_census.py:SEQUEL_WINDOWS": "register 71 (prereg_sequel_census): sequel windows {5,15} bars — operator-stated in the order",
    "bar_persistence.py:QUAD_KS": "register 68 (prereg_bar_persistence_quadrant): quadrant rows report k in {1,3,5} — subset of the register-63 horizons, operator order",
    "bar_persistence.py:HORIZONS": "register 63 (prereg_bar_persistence): the census horizons — instrumentation stated in the operator order, registered once",
    "bar_persistence.py:PTS_LADDER": "register 63: reach thresholds +{2,5,10} points, HOME-REFERENCE ONLY (operator order)",
    "bar_persistence.py:ATR_LADDER": "register 63: reach thresholds +{0.25,0.5,1.0}xATR(15M), cross-instrument (operator order)",
    "signal_points.py:BASELINE_SEEDS": "register 61 (prereg_baselines_v2_ensemble): B-RANDOM's 20-seed ensemble, pinned — the floor is a distribution, not a draw; single-seed history superseded",
    "signal_points.py:TREND_OFFSETS": "register 61: B-TREND's 20 cadence phase-offsets (same interval, shifted starts), pinned",
    "signal_points.py:BASELINE_INTERVAL_BARS": "IMPLEMENTER-PROPOSED baseline fire cadence (register 60), FLAGGED pending ratification",
    "signal_points.py:DRIFT_SKEW_SHARE": "IMPLEMENTER-PROPOSED drift-sensitive match rule (register 60), FLAGGED pending ratification",
    "signal_points.py:TREND_FAMILY": "DERIVED (register 60): the signals whose firing condition requires an established 1M trend — matched to B-TREND",
    "signal_points.py:BASELINE_NAMES": "register 60: the three controls; fenced, never candidates",
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
    ("label_bearing_sessions_PROPOSAL", "london + overlap as the tradeable window for criteria scoping — RATIFIED as proposed at the 2026-08-28 sitting (register 88)",
     "register 37", "2026-08-19",
     "RATIFIED at the 2026-08-28 sitting (register 88)"),
    ("either_direction_chance_baseline", "the either-direction bar-qualify base rate, computed per window and shown beside every either-direction precision",
     "backtest/scoreboard.py:score (agnostic mode)", "2026-08-19",
     "register 36 (direction-agnostic grading mode, operator order 2026-08-19)"),
    ("review_promote_min_fires", "30 per window — REDRAFTED ON THE DOCTRINE AXES (register 62, edge = consistency): promote-candidate requires, at this n in BOTH windows, (i) positive INITIATION lift vs conditioned chance, (ii) positive median-per-trade at a width <= 3xATR(15M) on the stop-width ladder, AND (iii) that median clearing the matched baseline ensemble's FULL member range (above the floor's luck, not just its median). Tail-carried cells (positive net, negative median) are non-evidence at any n",
     "register 36 criteria; register 62 redraft", "2026-08-22",
     "register 62 doctrine; numbers RATIFIED at the 2026-08-28 sitting (register 88: n>=30 both windows promote / n>=100 deprioritize)"),
    ("review_deprioritize_min_fires", "100 in the larger window — REDRAFTED ON THE DOCTRINE AXES (register 62): deprioritize requires, at this n, (i) at/below-chance initiation lift AND (ii) no positive median-per-trade at any width <= 3xATR(15M) AND (iii) no cell clearing its matched baseline ensemble range — with no redeeming metric",
     "register 36 criteria; register 62 redraft", "2026-08-22",
     "register 62 doctrine; numbers RATIFIED at the 2026-08-28 sitting (register 88: n>=30 both windows promote / n>=100 deprioritize)"),
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
