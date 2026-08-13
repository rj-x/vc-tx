# Backtest v1 — Standing Report (GENERATED — do not hand-edit numbers)

**Generated from:** `reports/backtest_v1/*.json` · **Instrument:** `uk100fut` (secondary `uk100`) · **Volume type: real futures contract volume** · **Stack:** 1h / 15min / 1min
**Data:** 16 sessions, 2026-07-13 07:00:00+00:00 → 2026-08-03 15:29:00+00:00, 8,160 1M rows · **Lockbox:** 2026-08-04T00:00:00+00:00 (loader-enforced, untouched)
**Cost model:** CASH-CFD VEHICLE (pre-registered 2026-08-13): signals/levels/stops/R on uk100fut; fills on uk100 measured bid/ask (long entry@ask exit@bid, mirrored), basis-at-entry level mapping, GBP-per-point sizing (min stake 0.5), NO commission; EOD-flat asserted

## Headline

Full system: **2 spawns, 0 trades**; secondary uk100: 6 spawns, 0 trades. While samples remain below powered n, the informative outputs are the funnel, per-TF label frequencies, and the drift-adjusted label-level event study; all weekly numbers are trend-indicative while baselines grow toward spec.

## Label denominators (per TF; classified = feature-valid, non-stub)

| Slug | TF | Classified bars | Non-null | Frequencies |
|---|---|---|---|---|
| uk100fut | 15min | 374 | 58 | EFFORTLESS_ADVANCE 30 · EFFORTLESS_DECLINE 16 · VALIDATED_ADVANCE 4 · VALIDATED_DECLINE 4 · UPTHRUST 2 · ABSORPTION 1 · TEST 1 |
| uk100fut | 1h | 88 | 13 | EFFORTLESS_ADVANCE 7 · EFFORTLESS_DECLINE 3 · UPTHRUST 2 · VALIDATED_ADVANCE 1 |
| uk100 | 15min | 544 | 90 | EFFORTLESS_ADVANCE 41 · EFFORTLESS_DECLINE 31 · VALIDATED_ADVANCE 5 · VALIDATED_DECLINE 4 · SPRING 3 · UPTHRUST 3 · TEST 2 · ABSORPTION 1 |
| uk100 | 1h | 128 | 19 | EFFORTLESS_ADVANCE 12 · EFFORTLESS_DECLINE 4 · VALIDATED_DECLINE 1 · UPTHRUST 1 · VALIDATED_ADVANCE 1 |

## Spawn-fate conservation

| Slug | Spec | Spawned | GRAD | REFUTED | EXPIRED | KILLED | active |
|---|---|---|---|---|---|---|---|
| uk100fut | H2 SHORT | 2 | 0 | 0 | 2 | 0 | 0 |
| uk100 | H2 LONG | 3 | 0 | 2 | 1 | 0 | 0 |
| uk100 | H2 SHORT | 3 | 0 | 0 | 3 | 0 | 0 |

## Explicit zeros (primary variant)

EOD_EXIT_trades 0 · SKIPPED_SIZE 0 · CONFIRM_UNDERSTRENGTH 0 · BLOCKED_SPAWNS 0 · REFINEMENT_CANCELLED_REFUTED 0 · REFINEMENT_CANCELLED_OPPOSED 0 · REFINEMENT_ABANDONED_EMBARGO 0 · ENTRY_ABANDONED_EMBARGO 0 · SIGNAL_UNACTED_IN_POSITION 0 · SIGNAL_UNACTED_CONFLICT 0

Swings confirmed across the session boundary (ruling 8 diagnostic): signal-TF 16 · context-TF 25
1min observational label study (ruling 10): 10 label rows, autocorrelation caveat embedded - `uk100fut_exec_label_study.json` (never pooled with 15min).

## Variants & ablations (identical data; cost model above)

| Variant | Trades | Win rate | Avg R | PnL | Tripwire |
|---|---|---|---|---|---|
| uk100fut_full_1r | 0 | — | — | — | clear |
| uk100fut_full_2r | 0 | — | — | — | clear |
| uk100fut_full_3r | 0 | — | — | — | clear |
| uk100fut_full_opposing | 0 | — | — | — | clear |
| uk100fut_full_context_flip | 0 | — | — | — | clear |
| uk100fut_norefine_2r | 0 | — | — | — | clear |
| uk100fut_strict_2r | 0 | — | — | — | clear |
| uk100fut_zerocost_2r | 0 | — | — | — | clear |
| uk100fut_abl_no_location_2r | 0 | — | — | — | clear |
| uk100fut_abl_no_gating_2r | 1 | 0.0 | -1.035 | -1034.7 | clear |
| uk100fut_abl_no_confirmation_2r | 0 | — | — | — | clear |
| uk100_full_2r | 0 | — | — | — | clear |
| uk100_abl_no_gating_2r | 1 | 0.0 | -1.038 | -1037.63 | clear |

Trade detail (uk100fut_abl_no_gating_2r, cash_cfd): -1 fill 10682.4 stop 10694.3 (11.9 pts) × £86.95/pt, basis@entry +5.0 → exit 10694.3 (STOP), -11.9 pts, R -1.03, costs 0, PnL -1035.
Trade detail (uk100_abl_no_gating_2r, cash_cfd): -1 fill 10682.4 stop 10693.4 (11.0 pts) × £94.33/pt, basis@entry +0.0 → exit 10693.4 (STOP), -11.0 pts, R -1.04, costs 0, PnL -1038.

## Event study — drift-adjusted label level (primary powered readout)

Window drift (bps): post_US_10 +13.2 · post_US_20 +16.3 · post_US_5 +3.8 · pre_US_10 +3.3 · pre_US_20 +11.1 · pre_US_5 +2.5

| Label | n | signed | raw+20 (bps) | excess+20 (bps) | excess hit+20 |
|---|---|---|---|---|---|
| ABSORPTION | 1 | False | 90.77 | 79.64 | — |
| EFFORTLESS_ADVANCE | 30 | True | 18.05 | 4.69 | 0.536 |
| EFFORTLESS_DECLINE | 16 | True | -33.01 | -19.1 | 0.333 |
| TEST | 1 | False | 47.12 | 35.99 | — |
| UPTHRUST | 2 | True | -54.62 | -43.48 | 0.0 |
| VALIDATED_ADVANCE | 4 | True | 11.16 | 0.02 | 0.75 |
| VALIDATED_DECLINE | 4 | True | -26.25 | -15.12 | 0.25 |

## Spread vs stop (split by stop basis; open question, register R2)

Median cash spread: **0.8 pts**

| Population | n | median % | p25–p75 | max | >15% alarm |
|---|---|---|---|---|---|
| H2 SHORT [signature] | 1 | 1.6 | 1.6–1.6 | 1.6 | 0 |
| H2 SHORT [entered_exec_local] | 1 | 4.7 | 4.7–4.7 | 4.7 | 0 |

Tracked quantity (register ruling 2, recalibrated): the spread-burden ratio between stop bases vs refinement's R-geometry gain, resolved by the with/without-refinement comparison at powered n.

## Basis-at-entry check (single-point-dependency guard)

Entries: 1 · flagged (|deviation from session median| > 3.0 pts): **0**
- uk100fut_abl_no_gating_2r: basis +5.0 vs session median +5.0 -> deviation +0.0 (ok)

## Extended-hours observational readout (Part B; non-evidential)

Bin coverage: 91 bins, 0 undercooked · segment-split label rows: 20
**Standing note:** pre_open accrues only ~1h/day - small-n applies to every pre_open row until stated otherwise
Feeds no thresholds or rules before walk-forward; full table in `uk100fut_extended_label_study.json`.

## Macro tagging (±15 min; calendar validated on load)

Calendar: 21 releases (validated).

| Event type | outside | near_GBP |
|---|---|---|
| SPAWNED | 2 | 0 |
| LABEL | 56 | 2 |

Per-release tagged events: 2026-07-30 11:00:00+00:00 BoE rate decision (Bank Rate; MPC votes; Monetary Policy Report & Summary): 2

**2026-07-30 BoE decision (11:00 UTC, mid-FTSE-session — most contaminating single event in the window):** 2 tagged event(s).

## Macro-spike volume check (register finding 2b)

In-cash releases inside the working set: **8** · median volume ratio in [release, +15 min) vs same-time other sessions: **1.02×**

| Release | vol ratio |
|---|---|
| 2026-07-14 12:30:00+00:00 USD US CPI (CPI & Core CPI m/m & y/y) | 2.8 |
| 2026-07-14 14:00:00+00:00 USD Fed Chair Warsh testifies (day 1) | 0.89 |
| 2026-07-15 12:30:00+00:00 USD US PPI (PPI & Core PPI m/m) | 0.9 |
| 2026-07-15 14:00:00+00:00 USD Fed Chair Warsh testifies (day 2) | 0.79 |
| 2026-07-30 11:00:00+00:00 GBP BoE rate decision (Bank Rate; MPC votes; Monetary Policy Report & Summary) | 1.46 |
| 2026-07-30 12:00:00+00:00 GBP BoE Gov Bailey speaks | 1.05 |
| 2026-07-30 12:30:00+00:00 USD US Advance GDP q/q & Core PCE Price Index m/m | 1.43 |
| 2026-08-03 14:00:00+00:00 USD ISM Manufacturing PMI | 1.0 |

## Standing flags

1. `baseline_sessions` 8 / `min_baseline_obs` 5 (spec: 20/20) — data poverty; warmup = exactly `min_baseline_obs` sessions.
2. Frozen config = untuned defaults; no walk-forward has occurred.
3. Open-auction bars not excluded at the signal TF (v1 decision).
4. Context-TF stub bar is context-only per spec.
5. EFFORTLESS_DECLINE excess signal: tracked-not-acted (register ruling 1); enters only via walk-forward if it survives to powered n.

## Cadence

Daily manual sync (`scripts/sync_daily.sh`); weekly campaign (`venv/bin/python -m backtest.campaign` — regenerates this report); lockbox and thresholds untouched. Next formal checkpoint: first powered drift-adjusted label readout or walk-forward feasibility, whichever first.

