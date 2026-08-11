# Strategy Findings & Risk Register

Companion to `vsa_strategy_prompt.md`. Captures known weaknesses, improvement ideas, and open questions so they survive across sessions and iterations. Update this document as items are resolved or new risks surface.

---

## 1. Critical risk: look-ahead leakage (ADDRESSED IN v1 SPEC — remain vigilant)

**History:** prior backtesting projects built with AI assistance produced strategies that only appeared to work because future information bled into decisions. This is the project's #1 failure mode.

**Defenses now in the spec** (Non-Negotiable section of the prompt): clock-gated data access layer; explicit bar timestamp convention; truncation-equivalence testing of precomputed features; automated future-perturbation test over random cutoffs; explicit checklist of subtle leaks (full-sample normalization bins/percentiles, unconfirmed swings, HTF state before close, levels defined with later data); leakage tripwire — exceptional results (PF > 2.5, win rate > 65% at ≥ 2R, near-monotonic equity) are presumed leakage until the perturbation test clears that exact configuration.

**Residual risk:** leakage via the *iteration process itself* (see finding 3) and via any manual data handling outside the engine. Never hand-inspect lockbox data.

## 2. Volume data quality (OPEN — first-iteration diagnostic)

Everything rests on Finsa tick volume being a faithful proxy for real participation. This is assumed, not tested.

**Action:** add a volume-quality study to the first iteration's diagnostics: (a) does tick volume show the expected intraday shape (open/close surges, lunch lull, 14:30 London jump on FTSE/DAX)? (b) does it spike on known macro release timestamps? (c) if a sample of real FTSE futures volume can be exported from any broker platform, correlate the two over the same period — this quantifies how degraded the absorption signal is.

**Status:** open. Depends on step-zero verification confirming a volume field exists at all (hard gate).

## 3. Iteration = quiet overfitting (ADDRESSED IN v1 SPEC)

Each review-refine-rerun cycle fits the rules a little more to the same history. Data snooping by another name.

**Defense adopted:** lockbox — most recent ~20% of 1M history (min 4 trading weeks once available), excluded programmatically at the store/loader level, evaluated exactly once when iteration is declared complete. New data accrues to the lockbox between formal iteration rounds.

**Discipline required from us:** the lockbox verdict is final for that iteration round. If it fails, the strategy failed — the answer is not to iterate against the lockbox.

## 4. Thin statistical power early on (ADDRESSED IN v1 SPEC)

Intraday-only + one instrument + gated hypotheses + short accumulated 1M window = possibly ~30 trades in the first backtests, which proves nothing either way.

**Defense adopted:** event-study layer — forward mid returns at +5/+10/+20 Signal-TF bars after every confirmed hypothesis, independent of gating/sizing/EOD/trade simulation, vs. matched baseline bars. ~10× the observations; answers "do the signatures predict anything?" while trade samples mature.

**Interpretation rule:** event-study significance without trade-level profitability means the edge exists but is being eaten by costs/EOD/spread — a fixable problem. Trade-level profit without event-study significance is suspicious (luck or leakage).

## 5. Cliff-edge thresholds (DEFERRED — v2)

Labels are boolean (volume 1.49× baseline isn't "high", 1.51× is), but conviction is continuous. Binary labels waste information and make results threshold-sensitive.

**v1 mitigation:** ±30% sensitivity sweeps already in spec — edge must degrade gracefully.
**v2 candidate:** continuous signature scores (e.g., logistic transforms of rel_volume/rel_spread/close_pos) feeding hypothesis strength directly, replacing label counting.

## 6. Spread vs. stop distance on low TFs (OPEN — first-iteration diagnostic)

On 1M/3M executions, CFD spread may be a large fraction of a tight stop — an apparent 0.3R edge can vanish entirely into the spread.

**Action:** diagnostic reporting average spread as % of stop distance, per hypothesis and per session phase. If it exceeds ~10–15% for a hypothesis, that hypothesis needs wider stops or a higher execution TF.

## 7. Scheduled news contamination (PARTIAL — tag in v1, filter in v2)

A 13:30 London volume spike on CPI day is calendar, not psychology — it will generate false climax/absorption signatures. Session-time normalization cannot catch it (date-specific, not time-of-day-specific).

**v1:** tag all trades and hypothesis spawns within ±15 min of major scheduled releases (manually maintained list is fine initially) so contamination is visible in diagnostics.
**v2:** economic calendar integration as a spawn filter.

## 8. Other v2 candidates (parked)

- Volume profile / higher-quality supply-demand zones as the Layer-1 level source (upgrade path explicitly anticipated in spec).
- Overnight holding with gap-through-stop modeling.
- Trading divergence-migration across timeframes (log-only in v1).
- Reverse-and-flip on opposing confirmations.
- Live narrative mode: same engine fed by scheduled `collect.py` syncs, emitting per-TF phase, open hypotheses with scores, and alignment each minute (Part 10 / path-to-live discussion).
- Futures data with true volume, if Finsa instrument IDs for futures exist.

---

## Open questions (blocking or near-blocking)

1. **Does the Finsa feed / clean store contain a volume field, and what does it represent?** Hard gate — no engine work until answered. (Step zero.)
2. **How much 1M history is already accumulated per instrument?** Defines the initial backtest window and lockbox feasibility. (`collect.py status`.)
3. What interval is `quarter`, what timezone are timestamps, is there any pagination beyond `l`, and what is the true `l` limit? (Step zero.)
4. Do futures instrument IDs exist on Finsa? (Owner to ask provider.)
5. Do the existing scripts have any bugs affecting already-collected data (timezone drift, silent gaps)? If so, does historical data need re-validation? (Step-zero audit; report before fixing.)

## Decision log (headline design rulings)

- Intraday only; force-flat before cash close; entry embargo 30 min before cutoff. Overnight = v2.
- Intrabar stop/target ambiguity resolved by replaying constituent 1M bars; stop-first if a single 1M bar touches both.
- Execution TF fixed to 1M/3M; embargo overrides refinement.
- Gating is per hypothesis class; H3 range-boundary breakouts permitted in RANGING (`H3_RANGE_BREAK`); H5 exempt with ATR-extension gate.
- Ablation study (location / gating / confirmation independently disabled) mandatory, run on frozen config.
- Portability protocol: tune on FTSE, run frozen config on DAX and NASDAQ; per-instrument re-tuning reported separately.
- Engine reads only from the clean store (`store.py build`); scripts' output paths refactored to project root with equivalence proof; audit before refactor; report data-affecting bugs before fixing.

---

## Pseudocode review rulings (v1 restatement — logged so nothing lives only in chat)

**Rulings on Claude Code's [A1]–[A17]:** signature ownership rule (climax→H1, UPTHRUST/SPRING→H2, no label spawns two specs — resolves [A1] and its long-side twin); `CONFIRMED_PENDING_GATE` state replaces re-confirmation ([A2]); `EFFORTLESS_DECLINE`/`VALIDATED_DECLINE` added ([A3]); TEST additionally requires volume < 0.5× signature bar rel_volume ([A4]); concurrency rules accepted + blocked-spawn logging ([A5]); [A6]–[A17] accepted as proposed, with [A10]'s near-no-op base/threshold and confirm-bar-delta-before-check documented as deliberate, and [A15]'s pullback volume slope logged for later evaluation.

**Second pass:** structural-core vs. context-qualifier label rule (confirmations reference structural core only — fixes unreachable NO_DEMAND confirmations in H5/H2); refinement invalidation on parent refutation (`REFINEMENT_CANCELLED_REFUTED`), single pending refinement; H3 direction rule for RANGING Signal TF (out of range from the absorption boundary); H1 spawn-level definition under new-low spawns; H4/H3 stops computed at graduation; inclusive lowest-low lookback.

**Forensic pass:** **CRITICAL spec bug — reversal gate lacked a phase-agreement branch**, blocking the framework's canonical trade (upthrust in Context MARKDOWN; climax ending a pullback in Context MARKUP). Fixed: agreement branch first, tagged `REV_WITH_TREND` for separate reporting. Also: descending-TF processing order at simultaneous closes (determinism + perturbation-test stability, unit-tested); H3 zone grows until confirmation, breakout beyond max(level, zone edge); H4 refutation = expansion as pullback state + structural break as trigger; minor mirror/tolerance/lookback fixes.

**New requirement:** synthetic-scenario verification before any backtest (named cases including `REV_WITH_TREND` and `CONFIRMED_PENDING_GATE` paths), reviewed against the psychology appendix.

**Process lesson:** each review layer (document → instantiation → runtime trace) found bugs invisible to the previous one; the critical gating bug survived four document reviews and was only exposed by tracing runtime state. Next bug class lives in execution — hence the synthetic scenarios.
