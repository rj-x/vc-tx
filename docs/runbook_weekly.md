# Weekly Regeneration Runbook (register 81 — the operator's manual procedure)

Terms: [GLOSSARY.md](GLOSSARY.md). Every command below runs from the
repo root. Steps marked **[venv]** need the project venv (they all
invoke `venv/bin/python` directly, so no `activate` is required — the
path IS the activation).

## Step 1 — data sync (any time after the session you want captured)

```
scripts/sync_daily.sh
```

- **What it pulls:** all instruments (futures legs included) → status →
  validate → clean-store rebuild → verify. The provider's 1M feed has a
  ~30-day retention floor — this step is the one with a hard penalty
  for lapses.
- **Expected duration:** a few minutes.
- **Healthy output:** a final `=== done ... ===` line with
  `sync=0 build=0 verify=0` and no `!!! FAILURE` line. A validate
  failure means the data changed character — investigate, never extend
  the known-issues baseline casually.

## Step 2 — the campaign **[venv]**

```
venv/bin/python -m backtest.campaign
```

- **Expected wall time:** roughly 60–90 minutes at the current Part C
  module count (27 modules at register 112, several of which replay all four
  instruments; the trade layer alone simulates six management variants
  plus the baseline ensembles).
- **What regenerates:** `reports/backtest_v1/` + `backtest_v1.md`
  (the evidential pipeline), then Part C — the scoreboard, recipes,
  SIGNAL_POINTS (stop-width ladder + baselines), bar-persistence,
  forward migration, co-fire, conditioning matrix (quadrant + MTF
  dims), gap census, narrative survey, **trades.csv /
  weekly_summary.csv / management_grades.csv** (the trade layer),
  the in-trade census, the **journal field survey**, VWAP census,
  drift census, excursion geometry, **trade forensics**
  (trades_enriched.csv + reports/forensics/), the **underwater
  census + thesis-campaign study** — then the parameter registry
  and **reports/DASHBOARD.md**.
- **Header-only refreshes:** artifacts whose *templates* changed since
  their last emission print the new headers only when their module
  re-runs — everything in Part C refreshes weekly, so after this step
  all live artifacts are current. Archived artifacts
  (`reports/archive/`) never refresh — that is what the archive means.
- **Healthy output:** each Part C module prints its `-> artifact`
  line; the backlog freshness check is silent (it prints
  `!! BACKLOG STALENESS` only when the hand-maintained page lags the
  register); the archive check prints `!! ARCHIVE CANDIDATES` only
  when something stopped being regenerated — both lines are actions
  for the reviewer, not errors.

## Step 3 — the reading order

1. `reports/DASHBOARD.md` — state, the doctrine-ordered board,
   question clocks, decisions awaiting you, the artifact map.
2. `reports/INSIGHTS.md` — the weekly index (register 109): what
   clears any null, what is watched (with age), what is benched or
   parked, and the DELTA since last week. An index, never evidence.
3. `docs/GLOSSARY.md` — whenever a term is opaque.
4. `docs/VARIANTS.md` — whenever a variant name is opaque: every
   registered recipe's mechanics, rendered from the structures the
   trade layer executes (register 116; enforcement-tested).
5. `reports/SIGNAL_POINTS.md` — the assessment page (ladder,
   baselines, Δ vs floor).
6. **`reports/trades.csv` + `reports/weekly_summary.csv`** — your
   working files for operator cuts (`management_grades.csv` is the
   quotability gate: no variant's net without its floor line;
   `journal_survey.md` prices the cuts' luck).
7. **`reports/forensics/`** (+ `reports/trades_enriched.csv`) — the
   trade-forensics deliverable (register 84): per-market
   winner/loser separators with their luck budgets, exit-efficiency,
   winner-MAE, the WATCH list, cross-market synthesis. Candidates
   only — reserved for the operator+reviewer sitting.
8. Drill-downs on warrant: the conditioning matrix, the narrative
   survey, the in-trade census, gap census, bar persistence.

## Step 4 — freshness checks (30 seconds)

- `docs/backlog_status.md` header: `Register-current-through: N` must
  equal the register's latest entry number.
- Artifact timestamps: everything in `reports/scoreboard/` should be
  from today's run (the campaign warns about stragglers — the
  `!! ARCHIVE CANDIDATES` line).
- The verdict-expiry block in the backlog: any expired condition is a
  sitting item.

## Step 5 — what to paste to the reviewer

Paste `reports/DASHBOARD.md` in full, plus **any line that stops
you** — a `!!` warning, a tripwire, a flagged parameter, a question
clock that crossed its threshold, a number that contradicts what the
register says. The reviewer's job is the reconciliation; yours is the
noticing.
