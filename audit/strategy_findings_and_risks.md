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

---

## RULES.md v2 review rulings (2026-08-11)

**All six reviewer findings verified and ratified:** R1 CPG pending window (`pending_gate_max_bars`, default 2× Context/Signal ratio, replaces confirm-window expiry once confirmed — prompt patched); R2 CPG skips strength machinery entirely, floor kill never applies in CPG (prompt patched); R3 two-phase step (evaluate all → resolve conflicts by strength → act once); R4 in-position guard on all entry paths + direct-entry restatement when refinement disabled; R5 evidence semantics — general definition added to prompt, per-hypothesis enumeration required in RULES.md v3; R6 H5 extension gate signed in the fade direction (spec bug, prompt patched). All implementation traps accepted: H3 age re-anchors on each qualifying cluster bar; "outermost in trade direction" wording; H4 pullback boundaries pinned (start = REACTION transition, mean excludes evaluation bar, low at graduation); `zone_level` = the key level Lv; refinement window bar 1 = first exec bar closing strictly after graduation; triggered entry whose fill would land inside the embargo → abandon.

**The three referred rulings:** (1) opposite-direction graduation during pending refinement → **cancel the pending entry** (`REFINEMENT_CANCELLED_OPPOSED`); the opposing hypothesis may begin its own refinement — no position was open, so this is not reverse-and-flip; oscillation bounded by expiry, logged for diagnostics. (2) Confirm-while-understrength → **log-and-lose** for v1 with a `CONFIRM_UNDERSTRENGTH` counter in diagnostics; revisit if the counter is material once thresholds are tuned; no third pending state in v1. (3) `pending_gate_max_bars` default **2× Context/Signal ratio** ratified.

**Spec-bug tally:** two critical defects have now originated in the spec itself (unsigned H5 gate; missing reversal phase-agreement branch) — the spec is not privileged over the restatement; both documents are subject to the same adversarial process.

## Step-zero data findings (from DATA.md — headline implications)

- **Volume is real futures contract counts** (`uk100fut`, ID 70152), not tick volume — the hard gate cleared in the best possible way; absorption hypotheses run undegraded. Cash CFD volume = same series ×4: use ONE series (futures) as canonical; never mix.
- **URGENT operational requirement: rolling ~30-day provider retention.** Data older than the window is unrecoverable. Scheduled sync (daily; hard ceiling every 3 weeks) is now infrastructure-critical — every missed window is permanently lost backtest data.
- `uk100fut` is a RAW SPLICE at quarterly rolls — roll-gap handling (prompt Part 6) applies; signature exclusion around roll transitions; Sep-26 expiry watch item.
- DST session-label bug on US/gold instruments: must be fixed before the NASDAQ portability stage; does not affect FTSE development.

---

## Backtest campaign log

**2026-08-12 — Backtest v1 (first real-data run; report: `reports/backtest_v1.md`).**
Outcome: **sample starvation** — 16 working-set sessions (exactly 5 consumed by warmup), 2 spawns / 1 confirmation / 0 gated trades on uk100fut (uk100 secondary consistent: 6/2/0). No tuning performed; lockbox untouched. **Compromise in force: `baseline_sessions` 8 / `min_baseline_obs` 5 vs spec defaults 20/20** — all results conditional on this until data allows spec values. The single gate-veto observation (ablated no-gating trade lost 1.04R with negative forward returns at all horizons) is **explicitly non-evidential (n=1)** and is recorded only because the ablation table requires it. New standing diagnostics: per-TF label denominators with conservation-checked spawn fates; label-level event study (primary powered readout for the accumulation window); spread-vs-stop (first reading ≈31% of stop on the one ablated trade — above the 10–15% alarm line in finding 6, thin-sample flagged). Cost-model gap found and fixed during amendment: slippage now applies to entry fills, not just exits. DST session fix (finding: US/gold in_cash now computed in America/New_York) shipped; macro-release calendar scaffolded (`data/macro_releases.csv`, empty — owner to populate). Next checkpoint: first powered label-level readout or walk-forward feasibility, whichever first.

## Standing rulings (2026-08-12 sign-off)

1. **EFFORTLESS_DECLINE excess signal — tracked, not acted.** The −19 bps drift-adjusted wrong-way reading at n=16 is a tracked observation only. If it survives to powered n, it enters the system **only through walk-forward as a candidate hypothesis** — no mid-accumulation rule or threshold changes on its account. (Ruled 2026-08-12; guards the quiet-overfitting defense in finding 3.)

2. **OPEN QUESTION — refinement stop-tightening vs spread burden.** Does execution refinement's R-geometry gain pay for its proportionally larger spread cost? Current evidence (corrected 2026-08-12 — the initially quoted 31% was a hand-derivation error; programmatic figures from logged fill-to-stop): spread ≈ 2.6% of the signature-stop distance (~50 pts) vs ≈ 10.8% of the exec-local tightened stop (12.0 pts) — a ~4× spread-burden ratio, both below the 15% alarm line, single observation each. Weekly campaign reports carry the graduation-stop distribution **split by stop basis** (signature at every graduation, all variants; exec-local at every refined entry) so both populations accrue; resolved by the spec-mandated with/without-refinement comparison once trade samples are powered.

3. **Reports are generated, not written** (effective 2026-08-12, extracted from the 31%-figure correction). Every quantitative claim in any report must be programmatically derived from logged artifacts; hand arithmetic is banned. Implemented: `backtest/report.py` renders `reports/backtest_v1.md` entirely from `reports/backtest_v1/*.json` (trade records now persisted per variant for this purpose); the campaign regenerates the report on every run; the file carries a GENERATED banner. Interpretive prose may carry no hand-computed numbers.


4. **Macro calendar scope contract** (2026-08-12). `data/macro_releases.csv`: timestamps/currency only, red-impact only by construction; used for ex-post tagging (±15 min) and the macro-spike volume check exclusively; **never engine-facing without clock-gating** (actuals are post-release information). Validation-on-load is mandatory for every consumer (`engine/macro.py`: schema, Z-suffix UTC, monotonic, NFP 12:30/13:30 anchor — hard fail). Forward population: `scripts/macro_fetch.py` (FairEconomy JSON feed; HTML scraping banned) writes `data/macro_releases_staging.csv` only; the human merge gate into the live file is deliberate and stays. Deferral: **surprise-conditioned release analysis (actual vs. forecast) — v2 candidate, backfillable from official archives, no capture urgency.**

5. **narrate is diagnostic/non-evidential** (2026-08-13). `engine/narrate.py` (replay + live) is the human front door to the narrative engine: labels/phases/hypotheses/dump only, always narrative-only past the lockbox boundary (scoped loader access, logged on every use; refused without the explicit flag). **No thresholds, rulings, or tracked signals may be touched off any narrate output.** Live mode is v2 machinery arriving early: polling watcher on the collector's rate discipline, always narrative-only, and must not displace the weekly cadence. First replay exercised 2026-08-13 05:00-09:40Z uk100fut (reports/narrate/). Note: that replay printed an EFFORTLESS_DECLINE at the session low preceding the rally - consistent with the tracked signal (ruling 1), explicitly non-evidential, n=1.


## v2 parking lot (additions)

- **Extended-hours signature detection** (2026-08-13): the 2026-08-13 06:56Z Asia-high rejection occurred 4 minutes pre-cash-open and is structurally invisible under cash-only detection; session-model implications unscoped.

- **Basis mechanics note** (2026-08-13, diagnostic): uk100fut-vs-uk100 close basis is intraday-stable (2026-08-13 morning: mean +32.2 pts, std 0.19 over 278 min) and steps on FTSE ex-dividend Thursdays (+~20 pts 2026-08-06, +~30 pts 2026-08-13; cash drops the dividend, the future does not), drifting with rates-minus-remaining-dividends between. Narrate snapshots confirmed faithful. Relevant to any future cross-series logic (basis-step days must never read as price signatures on a fut/cash spread).

6. **Execution vehicle pre-registered (Part A, 2026-08-13, BEFORE any powered results).** Deployment reality modeled exactly: signals/levels/stops/R on uk100fut; execution on the uk100 cash CFD — fills at measured bid/ask (long entry@ask exit@bid, mirrored), intrabar resolution on uk100 1M, GBP-per-point sizing with configurable minimum stake (SKIPPED_SIZE retained), no commission, no roll on the execution leg. Stop/target levels mapped fut->cash by basis-at-entry; justification on record: intraday basis stability (std 0.19 pts, 2026-08-13) + EOD-flat asserted as a config precondition (broker refuses cash_cfd without an EOD hook). Spread reported per session-time bin from real quotes; open question R2 now tracks measured uk100 spread. Old-cost-model report snapshotted once (reports/backtest_v1_futures-direct_final.md) for continuity; thresholds and lockbox untouched.

7. **Extended-hours observational instrumentation (Part B, 2026-08-13; evidential path untouched).** 24h session-time bins on futures trading-day boundaries (~21:30 London anchor) with per-bin observation counts reported (undercooked bins visible); structural labels/phase/levels run all hours, every emission segment-tagged (overnight_asia / pre_open 07:00-08:00 London / cash / post_close); hypothesis machinery outside cash is STRUCTURALLY narrative-only (SIGNAL_EXTENDED_OBSERVATIONAL — hypotheses spawned outside cash can never trade even if confirming in cash). Trading pipeline unchanged: spawning-for-trading, gating, and campaign trade metrics remain cash-session-only under the frozen config. Weekly readout gains the drift-adjusted label event study split by session segment — the experiment on whether volume signatures rescale in thin sessions. narrate/live show extended hours by default with segments visible. **Extended-hours results feed no thresholds or rules before walk-forward.** Motivating case: 2026-08-13 06:56Z Asia-high rejection.

8. **Late-session swing confirmability** (2026-08-13, spec gap; ruling to follow). Code today: swing confirmation carries ACROSS the session boundary — the 2k+1 fractal window is a rolling deque that never resets, so a swing in the final k bars confirms only when the NEXT session's opening bars arrive, with fractal neighbors spanning the overnight gap. Worked example: 2026-08-13 14:45-15:15Z range-break lows (10801.8->10785.8) — the only range break of the day — sit inside the final k bars and were unconfirmable at the close; RANGING verdict stood on the confirmed sequence (11:00Z higher high included).

9. **Day-relative vs time-of-day-relative signature detection** (2026-08-13, named question; no changes now). The 06:45Z rejection bar: 98th-percentile spread vs trailing-50 bars, 15th vs its session-time bin — the two normalizations disagree by construction in quiet segments. Adjudicated by the segment-split event study; feeds no thresholds before walk-forward.

10. **Execution-TF classification gap** (open). v1 runs the classifier/context pipeline on Context+Signal TFs only; 1min feeds refinement/broker but is never classified, so narrate --show-tf 1M shows no labels. Spec Part 5 says identical pipeline per TF — known v1 deviation, prioritization pending.

**Rulings closing items 8 and 10 (2026-08-13):** Item 8 RATIFIED as spec — cross-boundary k-window confirmation stands (formalized in prompt Part 3); swings tagged confirmed_across_gap with a weekly diagnostic count; **EOD-provisional confirmation registered as the named v2 alternative** if tagged swings prove pathological. Item 10 CLOSED — classification extended to the 1min TF as OBSERVATIONAL instrumentation: separate drift-adjusted segment-split 1min label event study (uk100fut_exec_label_study.json, autocorrelation caveat embedded, never pooled with 15min), narrate --show-tf 1M live, no threshold or rule consumes 1min labels before walk-forward, formal checkpoint remains Signal-TF. Compute impact measured: full campaign 29s wall (was ~20s), primary narrative artifact 3-4MB — immaterial to the sync-to-report cadence; no sampling scheme needed at current scale.

11. **Candidate-hypothesis register** (2026-08-13): `audit/candidate_hypotheses.md` pre-registers H6 (session-extreme rejection, day-relative baselines, volume-agnostic) and H7 (quiet-decline reversal at session extremes — the formal walk-forward entry for the tracked EFFORTLESS_DECLINE signal per standing ruling 1). Status CANDIDATE: not implemented, not consuming data, walk-forward entry only; the file is append-only with a logged amendment trail. Provenance: items 8-10 and ruling 5. Guard: `tests/test_candidate_guard.py` greps engine/ and backtest/ for the identifiers and fails the suite on any reference before walk-forward.

**Meta-history note (2026-08-13, cross-ref item 11 / candidate-file amendment 1):** first instance of implementer methodological pushback changing a ruling — the candidate-file design adjudication: dissent -> counter -> synthesis, outcome (frozen anatomy / free parameters) stronger than either original position.

**Field-review annotations, 2026-08-11 ledger session (review-surface, non-evidential):**
- 10:27/10:29Z 1min UPTHRUST prints @ ~10865: anatomy-correct, LOCATION-ABSENT (14 pts below session high), failed forward (rallied to 10880) — concrete instance of anatomy-without-location noise; supports the hypothesis layer's location requirement (cf. ablation (i)).
- 15:47Z 1min UPTHRUST: anatomy-correct, worked (7-pt risk, 37-pt run, stop untouched), post_close segment — **extended-hours exhibit #2** alongside 2026-08-13 06:56Z (v2 parking lot, extended-hours signature detection).

**Item 11 addendum (2026-08-13):** H8 (Signature-Moment Expansion Bracket, direction-agnostic class) registered in two-layer form; guard extended to H6/H7/H8. Evidence instrument built: expansion event study (uk100fut_expansion_study.json — forward realized range + up/dn excursions at +5/+15/+30 1min bars vs same-segment baselines, location splits from the ledger's dist_signal_atr/location_ref, measured spread stated alongside; observational, working set only). Motivating cases = the two 2026-08-11 field annotations, observation-only, no outcome computation on post-boundary data.

**Item 11 / H8 addendum — standing evidence status (2026-08-14, matched-baseline first reading):** "early evidence adverse: anatomy residue +8% at extremes net of volatility matching; double-trigger 0.57-0.66 at minimal buffer; spread 0.8 — bracket viability doubtful, directional variants unaffected by this result." Non-evidential; verdict at walk-forward. Cross-reference: the overnight_asia at_extreme cell (−4.2% net of matching) is logged as **item 9's first data point** — signature prints under thin-session volatility matching underperform their matched baseline, bearing directly on day-relative vs time-of-day-relative signature detection. Guard-circumlocution note: `backtest/expansion.py`'s prose reference to "the candidate register's signature-moment expansion bracket entry" (rather than the identifier) is **deliberate and load-bearing** — the H6/H7/H8 guard (`tests/test_candidate_guard.py`) scans that file; do not add candidate identifiers to engine/ or backtest/ before walk-forward.

12. **TF-ladder + migration instrumentation and H9** (2026-08-14). Scope contract: observational throughout — ladder TFs (1min/3min/5min/15min/30min/1h) run classifier+context only, no hypothesis manager, structurally (item-10 scoping); only the configured stack holds hypothesis/gating roles; every emission segment-tagged; per-TF label studies never pooled (nesting caveat embedded: higher-TF labels are compositions of lower-TF bars, not independent confirmations); migration events (persistence >= N same-direction child labels in one parent bar + same-direction parent close + RECRUITMENT: parent rel_volume >= floor) logged with chains, timing, recruitment margins; weekly migration study reports recruitment-passing vs -failing separately. **Standing rule: ladder/migration outputs feed no thresholds or rules before walk-forward.** Evidential path untouched (ladder off in all trading variants). H9 (Timeframe-Pressure Migration, direction-follows-pressure class) registered two-layer in the candidate file; guard extended to \bH[6-9]\b; migration code references the candidate by prose per the load-bearing-omission convention. **Recruitment-condition design lineage (logged as design rationale): implementer tautology objection -> owner participant-depth reframe -> recruitment synthesis** — the falsifiable second clause of H9's frozen claim exists because of this exchange. Compute impact: campaign 35.6s (+12s with ladder on the observational run only), migration artifact 125K, ladder studies 58K — immaterial; per-TF toggles exist (session_model.ladder) if scale changes.

**Item 12 addendum (2026-08-14, verification + first readout):** Evidential-path invariance across the ladder build is now a TESTED FACT: (a) one-off diff — post-ladder evidential outputs (trade record to the penny, 374/58 label denominators, 2-spawn fate table) match the pre-ladder documented values (pre-ladder JSONs were overwritten in place; the generated-report values served as baseline — noted as a reason to start committing artifact baselines); (b) standing regression `tests/test_ladder_invariance.py` — ladder-on vs ladder-off runs on the same store must produce identical evidential event streams and trade records (covers the ClockGatedFeed modification). Migration first readout logged: **direction-consistent with the candidate's frozen claim (cash rungs-1 recruited +3.5 bps @5 vs unrecruited −3.1), magnitudes non-evidential at current n.** Cross-file: the post_close recruited cell (−12.8 bps @5) is **item 9's data point #2** — thin-session behavior diverging from cash again, now on the migration surface.

13. **Version control adopted as standing discipline** (2026-08-14). Provenance / motivating gap: the ladder-build invariance one-off had to diff against values that survived only in report prose — pre-ladder artifact JSONs were overwritten in place with no baseline. Tracked: code, config, docs, registers, and generated report artifacts (evidence, not build products); excluded: raw/clean stores and logs (large; reproducible via sync only within the ~30-day minute-feed retention — caveat in README). Rules (README operations): campaign artifact changes committed per run (week-over-week artifact diff = diagnostic); each register/candidate amendment is its own commit (append-only gains cryptographic dates); code commits per completed order. Initial commit 8cc9443 records: post-ladder, 37 green, config frozen-never-fitted, lockbox 2026-08-04.

**Item 13 — LOGGED AMENDMENT (2026-08-14, git archaeology; not a silent edit):** the original provenance ("no VCS baseline existed") was WRONG. Prior owner history existed (c85d068..b8e1095, 2026-08-10 -> 2026-08-14, including data snapshots and report artifacts) but was unverified by both reviewer and implementer. The gap was discipline-around-artifacts, not absence of VCS. Archaeology results: (1) DATA INVENTORY — all committed data snapshots are strict subsets of the current store (identical 1M start dates: uk100 2026-07-03, uk100fut 2026-07-12; the live store's union merge already contains every committed row): zero recoverable sessions beyond retention, no lockbox implications, no recovery plan needed. (2) BASELINE UPGRADE — pre-ladder artifacts exist in b8e1095 (2026-08-14 09:07); the invariance one-off is UPGRADED to a bit-level diff: all evidential variant JSONs (full_2r, abl_no_gating_2r, full_1r, strict_2r, uk100_full_2r) are byte-identical pre-ladder -> post-ladder.

**Meta-history addition (2026-08-14): repository-state claims join market-data claims under compute-don't-assert.** The premise of item 13 went unverified by both reviewer and implementer — "no commits exist" was asserted from a stale session snapshot and accepted without a `git log`. Same rule as everywhere else in this project: verify against the artifact, not the recollection.

**Ruling 4 amendment — capture-all, consume-filtered (2026-08-14, design rule).** Staging captures EVERY feed event (all currencies/impacts, + forecast/previous staging-only); the live file stays lean (utc_time,currency,impact,name); consumption filters through per-instrument `macro_relevance` config (uk100fut = {GBP,USD} x {High} — tagging behavior pinned bit-identical by test). Loader validates impact in {High,Medium,Low,Holiday}; NFP anchors unchanged; merge-gate view renders staged rows grouped by currency/impact. Notes: pre-change weeks hold GBP/USD-High only (backfill from official archives if another instrument's history ever needs more); **relevance filters are per-instrument config — a named walk-forward-adjacent question, not a constant.**

**2026-08-11 field annotation — LOGGED AMENDMENT (2026-08-14, not a silent edit):** the 10:27/10:29Z pair was "location-absent" only by the session-extreme reference (14 pts below session high); by the swing-registry reference it was location-PRESENT (−0.03 ATR from a registered level). The original annotation used the only reference then measured. **Reference-class discrimination (session extremes vs prior-session extremes vs swing-registry levels) is registered as an open question feeding H6's parameter schema**; the expansion study now splits by reference class, so the question is computable weekly.

**Week field-review scoreboard (w/e 2026-08-14; review annotations, non-evidential):** five verified events — 14.5R post_close winner; 2.2R-then-stopped at session high; three failures. Method note on the record: **discretionary recall surfaced the two winners; the ledger surfaced all five** — the review surface exists precisely to keep the failures in view.

**Week-of-08-10 register annotations (2026-08-14; non-evidential, narrative-only provenance):**
1. **H9 canonical worked example — 2026-08-12 12:29-13:30Z:** simultaneous multi-TF quiet-advance at the session high (EFFORTLESS_ADVANCE printing 1min/3min/5min/15min at 12:30, VALIDATED_ADVANCE 1min at the session high 10866), then a RECRUITED decline (VALIDATED_DECLINE at 1min/3min 12:36-12:38) propagating 1min -> 3min -> 5min -> 15min -> 30min -> 1h within one hour, ~43 pts to 13:30. Cross-reference: the recruitment condition's design lineage (item 12) — this is the pattern the participant-depth reframe predicted the definition would capture.
2. **First observed climax-and-test anatomy — 2026-08-11 11:02Z POTENTIAL_BUYING_CLIMAX** (first climax label in project history, 1min, at the weekly high 10878.6/swing 10879.1) **+ 11:24Z 3min TEST**, preceding a ~100-pt decline over the following sessions. Filed to the exec-TF/ladder studies as motivating texture (H1-anatomy at 1min scale; the Signal-TF has yet to print one).
3. **Scoreboard amendment (logged) — the 2026-08-12 12:31Z SPRING failure now explained as COUNTER-CASCADE:** it printed against the forming multi-TF decline of annotation 1 (long signature into a recruiting downward migration). Mechanistic support for MTF-alignment gating, n=1.

14. **Execution layer** (2026-08-14). **One engine, multiple feeds** — a strategy definition executes through the identical code path (classifier/context/hypotheses/gating/broker/exits) in lab, paper, and narrate; no mode-specific strategy logic anywhere; enforced by `tests/test_one_engine_invariance.py` (lab bulk path vs simulated-clock incremental path: bit-identical decisions and fills). **Exit universe pre-declared** for walk-forward: fixed_points, r_multiple, atr_k, beyond_swing_n, beyond_signature_n, trail_atr, trail_swing, breakeven_at_r (`engine/exits.py`; trailing tightens-only, same intrabar rules as stops). **Strategy schema** (`engine/strategy.py`, definitions/): engine mode + signal_rules composition (labels incl. ladder rungs, location by reference class, segment, phase, migration conditions); frozen config refactored to `definitions/frozen_v1.yaml` — campaign pin passed BIT-IDENTICAL; candidates referenced by prose per guard. **Zone model**: working (-> 2026-08-04, freely simulatable) | lockbox (-> go-live: sealed, one evaluation) | forward (go-live ->: paper-visible live only, never tunable, excluded from training like the lockbox); go_live_utc stamped one-shot into lockbox.json at first paper start (terminal boundary). **Lab** (`backtest.lab`): working-set-only, EXPLORATORY-stamped, physically separate artifacts, immutable trial log (hash/ts/metrics) = the multiple-comparisons record walk-forward MUST consult; graduation = candidate-backlog registration only. **Paper** (`engine.paper`): frozen_v1 only, zero strategy knobs, cash-CFD fills on live uk100 bid/ask, EOD/embargo enforced, FORWARD_PAPER append-only ledger, restart = warm+reconcile-close+logged coverage gaps (honest holes, never backfilled). **Deferred (named v2 option): lab strategies as live shadow ledgers.** Compute: suite 42 tests ~8s; campaign unchanged; paper smoke pending first supervised session.

**Drill-deviation note + rationale correction (2026-08-14, logged amendment style):** Outcome ACCEPTED AND PREFERRED — the standing synthetic drill test with shared-helper extraction beats the ordered one-off. **Rationale CORRECTED for the record: the implementer's stated justification ("real-data drills leak frozen-config behavior onto sealed data") is WRONG** — working-set data is not sealed; it is the freely-simulatable zone, and the weekly campaign already publishes frozen_v1's complete P&L over it by design. A real-data drill on July would have contaminated nothing. **The live-rehearsal ban applies to the lockbox and forward zones only.** Logged so no over-broad caution enters doctrine — false cautions metastasize like false permissions. (Meta-history: this register now holds both pushback that improved a ruling AND pushback whose outcome was accepted despite its reasoning.)

**Untested surface, accepted by design (2026-08-14):** real-feed latency under the live polling loop is the one surface the simulated-clock drill could not exercise; it receives its test at supervised go-live, where the failure mode is logged coverage gaps.

**GO-LIVE AUTHORIZED (2026-08-14):** owner starts the paper executor at a supervised moment, verifies the go_live_utc stamp, watches first polls, exercises one natural kill-and-restart, commits the stamped state. Standing expectation: first-session silence is the likely and correct outcome.
