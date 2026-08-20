# Standing Operations

The build phase is complete. The system is in **accumulation mode**: it observes and
measures daily, trades nothing, and touches no thresholds until walk-forward. Everything
below is routine operation. If a step produces something unexpected, see **When something
looks wrong** at the bottom — do not improvise fixes.

---

## Daily — data sync (manual, unforgiving)

```
scripts/sync_daily.sh
```

**When:** once per trading day, any time after the session you want captured. This is the
only task in the system with a hard penalty for lapses: the provider's 1M feed has a
**~30-day rolling retention floor** — unsynced minute data is permanently destroyed.
One run per trading day is ideal; **3 weeks without a run is the point of no return.**

**What it does:** pulls all instruments (incl. futures legs) → status → validate →
rebuilds the clean store → verifies. Logs to `logs/sync/YYYY-MM-DD.log`.

**Expected outcome:** the final `=== done ... ===` line shows `sync=0 build=0 verify=0`
and no `!!! FAILURE` line. The script tails the outcome when run interactively.

**Failure signals:**
- `!!! FAILURE` line → open the day's log; identify which stage failed; re-run once.
  Persistent failure = raise it, don't patch it.
- `validate` now fails only on **new or worsening** issues (known-issues ratchet in
  `data/_known_issues.json`). A validate failure means the data itself changed character —
  investigate before accepting; never add to the known-issues baseline casually.

---

## Weekly — campaign run (one command, everything else is automatic)

```
venv/bin/python -m backtest.campaign
```

**When:** once a week (e.g. weekend, after Friday's sync).

**What it does:** re-runs the full evidential pipeline over the working set (lockbox
excluded structurally) and **regenerates `reports/backtest_v1.md`** — every number
programmatically derived from logged artifacts (hand-edited numbers are banned by ruling).
Also emits/updates: the funnel with macro-release tags, the drift-adjusted label event
study (per-TF, per-instrument), the extended-hours segment-split study (observational),
spread-by-bin, graduation-stop distributions by stop basis, and the basis-at-entry guard.

**What to actually look at (5 minutes):**
1. Funnel trend — labels → spawns → confirmations → gate outcomes. Trend, not levels;
   numbers are trend-indicative while baselines grow toward spec.
2. Drift-adjusted label study — **excess** columns only; raw columns are tape-contaminated.
3. Any flagged rows: basis deviation flags, `SKIPPED_SIZE`, `CONFIRM_UNDERSTRENGTH`,
   staleness warnings.
4. `pre_open` rows in the extended study carry a standing small-n note — do not over-read.

**Not required:** any action. The expected weekly outcome during accumulation is
"numbers accrued, nothing notable." That is success, not stagnation.

---

## Weekly — macro calendar merge (~1 minute, human gate is deliberate)

```
venv/bin/python scripts/macro_fetch.py     # runs alongside daily sync too
```

The fetcher writes **staging only** (`data/macro_releases_staging.csv`) from the
FairEconomy `thisweek` feed (High impact, GBP/USD, UTC-normalized). It never touches the
live file — that merge is yours:

1. Eyeball staged rows against the validation output (schema, UTC `Z` suffix, and the
   NFP anchor: any "Non-Farm" row must sit at 12:30/13:30 UTC).
2. Append accepted rows to `data/macro_releases.csv`. Keep it red-impact GBP/USD only.

**Failure signals:** fetcher exits nonzero on rate-limit/HTML poisoning (it never writes
bad data — just re-run later; it makes one request + one mirror retry, nothing aggressive).
The loader warns if the live file's newest event is >10 days old → a week went uncaptured;
backfill manually from a UTC-mode ForexFactory printout (see register for the procedure).

---

## Ad hoc — narrative inspection (optional, safe by construction)

```
venv/bin/python -m engine.narrate --instr uk100fut --start <ISO> --end <ISO>   # replay
venv/bin/python -m engine.narrate --instr uk100fut --live                      # live watch
```

Replay any window or watch bars narrate live (bar-close driven; feed settles ~10s after
close, so with 1-min polling expect 9–69s). Post-lockbox-boundary windows **refuse**
without `--narrative-only`, which runs the engine in a structurally no-act, no-aggregate
mode (access is logged). Live mode is always narrative-only. Nothing you do here can
contaminate the evidential path — but narrate output feeds **no** thresholds, rulings, or
tracked signals, ever. Setups seen outside cash hours are tagged observational and are
not covered by any validation this system will ever produce.

---

## Standing prohibitions (until walk-forward opens)

- **Do not touch thresholds or config** to "get more trades." The config's value is that
  it has never been fitted. Sample starvation is the expected state; the lever is data.
- **Do not look at lockbox data** outside `--narrative-only` narrate. Every metric seen
  from post-boundary data spends the final exam.
- **Do not act on tracked signals** (e.g. EFFORTLESS_DECLINE excess) — they enter, if
  ever, through walk-forward as candidate hypotheses.
- **Do not hand-edit generated reports or the macro live file** (staging → review → merge
  only).

## Checkpoints (what ends accumulation mode)

Next formal checkpoint, whichever arrives first (~40–60 working sessions on FTSE alone):
1. **First powered drift-adjusted label readout** — the first real verdict on whether the
   bar-level psychology carries information at all.
2. **Walk-forward feasibility** — enough working-set history to support train/validation
   folds; opens threshold tuning under the pre-registered protocol.

(The formerly parked multi-instrument-acceleration decision was RETIRED
2026-08-20 — overtaken by the register-40 expansion; register 49(6).)

## When something looks wrong

The system is designed to fail loudly and specifically. Match the signal, don't guess:

| Signal | Meaning | Response |
|---|---|---|
| `!!! FAILURE` in sync log | a pipeline stage broke | read log, re-run once, then raise |
| `validate` nonzero | **new** data-quality issue vs baseline | investigate before accepting |
| store staleness warning (build) | newest 1M bar >5 days old | sync immediately; check cron/habit |
| macro staleness warning (loader) | calendar >10 days stale | manual backfill procedure |
| basis deviation flag | cash/fut quote anomaly at an entry | inspect that entry's quotes |
| `SKIPPED_SIZE` entries | stake rounded to zero | equity/stop-distance assumptions unrealistic |
| beautiful results | presumed leakage (tripwire) | perturbation test on that exact config first |

The last row is not a joke. Suspicion scales with beauty; that ruling has already caught
real bugs.

## Canonical parameter registry (standing rule, adopted 2026-08-18)

**`docs/parameter_registry.md` is canonical** for every yardstick,
threshold, default, and assumption in force — value, source, date set,
authority. It is GENERATED (`scripts/param_registry.py`; regeneration rides
the weekly campaign; a test pins it clean against HEAD). **No test,
analysis, census, or simulation may use an unregistered yardstick.**
Pre-registrations cite their yardsticks by registry reference (mandatory
field; the trial log refuses entries without it). This README deliberately
duplicates **no values** — the registry is the single source (drift
precedents: the stores-excluded policy, the US/gold session note).

## Version control (standing discipline, adopted 2026-08-14)

- Tracked: code, config, RULES/prompt/docs, register & candidate files, and
  GENERATED report artifacts (`reports/`) — the JSONs and md reports are
  evidence, not build products; their history is the point.
- Tracked (policy AMENDED 2026-08-18, register finding 23): raw/clean data
  stores and logs ARE tracked. The original 2026-08-14 text excluded them,
  but the exclusion was never enacted (`.gitignore` rules stayed commented
  out; stores/logs have been committed throughout) and the enacted practice
  is the correct one: the minute feed has a ~30-day rolling retention floor,
  so committed stores are the ONLY durable history — an untracked store
  loses everything beyond retention on the first mishap (see DATA.md).
  Policy follows the safer practice; the README was wrong, not the repo.
  **Caveat:** store commits made while a build is running were a truncation
  hazard until atomic writes (store.py `_atomic_to_csv`, finding 23);
  observed instance: empty `uk100fut_1h.csv` blob in commit `9bcf9ec`,
  restored in `c3e806b`.
- Rules: every campaign run's artifact changes are committed (the
  week-over-week diff of generated artifacts is itself a diagnostic); every
  register/candidate-file amendment is its own commit (append-only
  discipline gains cryptographic dates); code changes commit per completed
  order with the order's one-line summary.

## Paper executor — long-running invocation (recommended)

```bash
mkdir -p logs/paper
caffeinate -is nohup venv/bin/python -m engine.paper --instr uk100fut \
    >> logs/paper/$(date +%F).log 2>&1 &
echo $! > logs/paper/paper.pid
```

- `caffeinate -is` keeps the Mac awake (sleep = coverage gap; gaps are
  honest holes, never backfilled — but avoidable ones are still downtime).
- `nohup ... &` detaches from the terminal; stdout/stderr append to a
  dated log in `logs/paper/` (gitignored with the rest of logs/).
- Stop cleanly with `kill -INT $(cat logs/paper/paper.pid)` — SIGINT writes
  the ledger STOP record. A crash/kill without STOP is handled at next
  start by reconcile (RECONCILE_CLOSE + COVERAGE_GAP, per register 15).
- Check liveness: `tail -f logs/paper/$(date +%F).log` (one poll/min) or
  `ps -p $(cat logs/paper/paper.pid)`.
- After each session: commit the ledger delta
  (`git add reports/paper/ledger.jsonl && git commit -m "paper: session YYYY-MM-DD"`).
- Ledger and go-live semantics: reports/paper/ledger.jsonl is append-only;
  the first-ever start stamped go_live_utc (done 2026-08-14) — restarts
  never restamp.

**Crash-coverage honesty (2026-08-17, supersedes the positions-only note):**
restart handles positions (RECONCILE_CLOSE) AND coverage: UNCLEAN_PREDECESSOR
is emitted when the ledger's last lifecycle event is a START without STOP;
`reports/paper/checkpoint.json` (overwritten per poll) dates crash deaths to
the minute; decision-coverage gaps anchor on the predecessor's last activity
(STOP.last_processed, else checkpoint, else predecessor warm_through) — never
this run's warm_through, since a post-crash sync can erase downtime.

## Component map (one line per module; artifacts in reports/scoreboard/ unless noted)

- `engine/signal_watch.py` — THE one home for hypothesis firing conditions + narrative primitives; passive observer, invariance-pinned; no artifact (fires feed the readers).
- `backtest/scoreboard.py` — signal scoreboard (precision/coverage/earliness/payoff vs per-context chance) → `hypothesis_performance.md` + `signal_scoreboard.json` + `READING_GUIDE.md`.
- `backtest/recipes.py` — recipe layer, grammar v1 (composed/staged stops, honest fills) → `recipe_performance.md|.json`.
- `backtest/excursions.py` — MFE/MAE/time-to-MFE profiles + narrative-conditional cut → `excursion_profiles.md|.json`.
- `backtest/sessions.py` — register-37 session partition (native-tz, DST-proof); no artifact.
- `backtest/forward_migration.py` — forward-zone migration readout → `reports/forward/`.
- `backtest/volume_profile.py` — volume-at-price organ (register 16 #2) → `volume_profile.md|.json`.
- `backtest/cofire.py` — cross-family co-fire census → `cofire.md|.json`.
- `backtest/flip_cut.py` — post-flip counterfactual (ARCHIVED standing reference, register 44) → `flip_cut.md|.json`.
- `backtest/location_census.py` — exhaustion-family × H11-map census → `location_census.md|.json`.
- `docs/backlog_status.md` — one-status-per-idea glance table (register 45).
- `backtest/campaign.py` — the weekly evidential pipeline → `reports/backtest_v1/` + `backtest_v1.md`.
- `scripts/param_registry.py` — canonical parameter registry generator → `docs/parameter_registry.md` (regen rides the campaign; pinned vs HEAD).
- `docs/hypothesis_register.md` — THE hypothesis list (H1–H12) · `docs/sense_organ_queue.md` — build queue · `docs/lockbox_policy.md` + `docs/hypothesis_lifecycle.md` — zone + stage doctrine · `docs/location_apparatus.md` — location mechanics.
