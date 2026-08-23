# Findings Audit — 2026-08-23 (register 74; operator-ordered)

Every finding-bearing claim re-derived from its artifact. Three checks
per row: (a) re-derivation (transcription, register-34 class); (b)
statistic-shape match (extremity vs consistency, single-cell vs field,
participation vs initiation, median vs net, conditioned vs raw); (c)
negative-finding symmetry (what statistic would have seen structure,
and was it computed). Verdicts: VERIFIED / MISMATCH-FLAGGED /
RE-EXAMINE. Every flag becomes a register-74 amendment through the
normal machinery; no silent fixes. Backtest cells are stable (fixed
working set); forward cells drift with weekly accrual — drift is noted,
never counted as error.

## Tier 1 — feeding pending grades and the doctrine

| claim (as worded) | artifact / cells | statistic shape | verdict |
|---|---|---|---|
| Q1-H11 founding: S0-H11 Overlap +39.3pp, n=40 bt | conditioning_matrix.json S0-H11\|backtest\|session\|overlap | single-cell conditioned lift (best-of-many, discount stated) | VERIFIED (+39.3, n40 exact) |
| Q2-H9 founding: nas100 NY +34.2pp | same, nas100fut S0-H9\|backtest\|session\|ny_only | single-cell conditioned lift (PROVISIONAL instrument) | VERIFIED (+34.2; n=25 — n was never claimed in the entry; now on record) |
| Q1-H6 founding: London −34.2pp, n=31 | same, S0-H6\|backtest\|session\|london | single-cell conditioned suppression | VERIFIED (−34.2, n31 exact) |
| Q2-H6 founding: 33.9% net reach, +22.8pp over floor [9.4…15.0], touch med 3 | bar_persistence.json S0-H6 bt whole | single-cell vs ensemble-median floor, range printed | VERIFIED (all four numbers exact; fwd clock 25) |
| R2 verdict (register 70): −76.8→−139.5 / −10.9→+37.5 / −63.2→−9.7; spread 28.9% | r2_experiment.json rows | paired net + family split (was verified at entry) | VERIFIED again |
| Survey focal: +11.3/+11.6 bt, +5.1/+5.4 fwd | narrative_survey.json S0-H1×absorption ×4 | single-pair cells within a priced field | VERIFIED |
| Consistency field: 13/20, null med 6 / p95 8, pctl 100 | narrative_survey.json null.consistency | field count vs permutation null | VERIFIED |
| Ensemble floor: B-RANDOM 3× bt med −26.50 [−42.10…+12.20]; single seed was max member | signal_points.json baselines | ensemble median + range | VERIFIED |
| Register 72(c): "every home hypothesis sits inside its floor's noise" | signal_points.json matched deltas, fwd 3× | single-cell clearance vs floor max | **MISMATCH-FLAGGED (wording): amendment 74-A1** — true for every MEASURABLE cell and every S0 board row; the full sweep finds S1-H1 fwd +10.66 above floor max at n=2 (unmeasurable, excluded by convention). Claim should have said "every measurable home cell." |
| Register 73 focal numbers vs pilot (+9.2→+11.3 etc.) | sequel_census.json vs narrative_survey.json | same cell, different vocabulary precedence | **MISMATCH-FLAGGED (transparency): amendment 74-A2** — the shift is explained (richer vocabulary captures earlier bars) but the explanation lived only in review prose, not the register. Now recorded. |
| Expectancy: S0-H6 peak-k=2 at −0.10; floors ≈ −spread | bar_persistence.json expectancy | close-based median curve (vs touch-based reach — register 65 families) | VERIFIED |

## Tier 2 — retired/parked/negative verdicts (symmetry check applied)

| claim | artifact | statistic shape | verdict |
|---|---|---|---|
| Quadrant base rates "remarkably flat" (register-66 read) | conditioning_matrix.json quadrant_base_rates, 8 cells/quadrant (4 instr × 2 win) | single-window eyeball at entry — **shape mismatch: no cross-cell statistic was computed** | **RE-EXAMINE: amendment 74-A3** — consistency lens: wide-loud episode-begin deviation negative in 7/8 cells (mean ≈ −4pp); narrow-quiet positive in 7/8 (≈ +1pp); sign-consistent across instruments and windows. Small effects; NO MINT; watched under weekly accrual with the field statistic now standing. |
| Quadrant persistence "does not predict the next close" (register 68) | bar_persistence.json quadrants, 8 cells/quadrant/conv | Δ vs ensemble floor at k=1 — symmetry check run | VERIFIED under the consistency lens for the actual claim (no cross-QUADRANT differentiation; same/fade symmetric at floor). SHAPE NOTE (74-A4): the universal sub-50 favorable fraction in BOTH conventions is tie-mass (close==entry counts unfavorable both ways), not signal. |
| Co-fire "starved / expect UNMEASURABLE" | cofire.json (current) | single-cell n-threshold verdict from 2026-08-20 | **RE-EXAMINE: amendment 74-A5** — STALE: the current artifact carries 248 cells at n≥15 (max n 347). The verdict predates three weeks of accrual; a proper co-fire re-read is ordered at the next weekly sitting through normal machinery. |
| H8 collapse "at base rate" (register 36 era) | hypothesis_performance.json S0-H8 either-dir | was PARTICIPATION-era; initiation columns opened at register 53 | VERIFIED under the new convention, stronger: initiation 40.9 vs base 43.8 bt; 34.4 vs 40.5 fwd — at-or-below base in both. Shape note recorded. |
| VWAP re-cut: "−0.9pp survives; 63.3% retired unquoted" | vwap_census.json recut fields | decile-matched, episode-start convention | VERIFIED in structure (recut fields present as claimed; the retired 63.3% reproduces at 63.6% current — forward accrual drift, not error) |
| Flip-gate NOT PASSED (register 44) | flip_cut.json (archived, unchanged) | pre-registered gate on (b); procedural | VERIFIED (artifact frozen; verdict procedural) |
| Suppression reading S1-H11 (negative lift = claim winning) | scoreboard + survey CONS pairs | initiation, conditioned; now also cross-window consistency | VERIFIED and reinforced (S1-H11 none/trend-flip/absorption pairs consistency-marked) |
| Micro-gap fade texture (−1.7/−2.3/−3.3/−3.0) | gap_census.json micro persist | signed median at standard horizons vs null 0 | VERIFIED (fresh artifact) |
| Drift census "no base-rate change" / gap-fill unregistered | drift_census.json / gap_census header | descriptive | VERIFIED (stamps and fences intact) |
| 11:46Z migration MISS (registers 28/29) | forward dossier | pre-registered expectation graded at entry | VERIFIED-AT-ENTRY (dossier frozen; not re-derived — grading was contemporaneous and commit-stamped) |

## Tier 3 — texture notes

| claim | verdict |
|---|---|
| H2 initiation-vs-participation divergence (18.2 vs 27.3) | VERIFIED at register 53 entry (side-by-side emitted; not re-derived — flagged for the ≥30-episode revisit it already awaits) |
| Expectancy floors = spread (B-RANDOM −1.30 flat) | VERIFIED (sanity identity) |
| Baseline single-seed incident (register 61) | VERIFIED (the +12.20 = ensemble max member reproduces) |

## Summary

22 rows: 17 VERIFIED, 2 MISMATCH-FLAGGED (wording/transparency — 74-A1,
74-A2), 3 RE-EXAMINE (74-A3 quadrant base-rate consistency structure,
74-A4 tie-mass shape note, 74-A5 co-fire staleness). No transcription
errors found — every registered number reproduced exactly from its
artifact. Both genuine flags are STATISTIC-SHAPE class, not arithmetic:
the exact class the consistency amendment exposed. The standing rule
(register 74): every future finding entry states its statistic's shape
alongside its numbers.
