# Claude Code Prompt: Volume-Narrative Trading Strategy — Build & Backtest

## Objective

Build a backtestable **intraday** trading system based on volume/price-action analysis (Wyckoff/VSA-inspired). The system does **not** pattern-match single candles. It maintains an **evolving narrative** of buyer/seller psychology as a state machine, updated bar-by-bar, across multiple timeframes. Trades are taken only when a Signal-timeframe hypothesis matures in a direction permitted by higher-timeframe context. All positions are closed before the cash session ends — no overnight exposure.

Implement in Python. Prioritize correctness (zero look-ahead bias), auditability (the system must be able to explain *why* it believed what it believed at every bar), and clean separation of concerns so the hypothesis set can be extended later.

---

## Non-Negotiable: Zero Look-Ahead

**Prior backtesting projects built with AI assistance failed because future information bled into decisions — the strategies only appeared to work because they read the future. This must not happen here.** Treat leakage as the default failure mode to be actively disproven, not an edge case. In addition to the specific rules throughout this spec:

1. **Clock-gated data access:** engine components never touch raw arrays directly. All market data flows through a single access layer parameterized by the current simulation timestamp, physically incapable of returning bars beyond it. If a component can even *request* future data, the architecture is wrong.
2. **Bar timestamp convention:** define once whether bars are indexed by open time or close time, assert it in tests, and use it everywhere. A decision "at bar N" means at bar N's **close**, using data up to and including that close; fills occur no earlier than bar N+1's open.
3. **Precomputed features are a known leak vector:** the vectorized feature precomputation (Part 6) must be leak-checked — centered rolling windows, full-sample normalization, and percentiles ranked over the whole dataset are classic silent leaks. Test: recompute a random sample of bars' features using data truncated at each bar, and assert equality with the precomputed values.
4. **Future-perturbation test (mandatory, automated):** run the backtest to a cutoff T and record every decision (labels, hypothesis transitions, signals, fills). Truncate or randomly mutate all data after T. Re-run. Every decision at or before T must be bit-identical. Automate over multiple random cutoffs and keep it in the test suite.
5. **Subtle leaks to check explicitly:** session-normalization bins computed over the full dataset instead of trailing sessions; threshold percentiles computed over full history; swing points used before their k-bar confirmation lag; HTF bar state visible before that HTF bar closes; range boundaries or key levels defined using later data; any train/validation contamination in walk-forward.
6. **Leakage tripwire:** exceptional results are presumed leakage until proven otherwise. Any configuration producing (for example) profit factor > 2.5, win rate > 65% at ≥ 2R targets, or a near-monotonic equity curve must trigger a leakage investigation — rerun the perturbation test on that exact configuration — before being reported as a result. Suspicion scales with beauty.

---

## Part 1: Core Concepts

Every bar is described by four variables:

1. **Spread (result):** high − low. The size of the battle.
2. **Volume (effort):** participation. The size of the armies.
3. **Close position (victor):** `(close − low) / (high − low)`, a 0–1 score. 1.0 = buyers won the bar outright; 0.0 = sellers won. For zero-spread bars, define close_pos = 0.5.
4. **Context:** where the bar occurs — trend direction/age, proximity to support/resistance, background volume trend, current market phase.

**Everything is relative, never absolute.** "High volume" = volume vs. a trailing baseline (e.g., > 1.5× trailing mean, or > 80th percentile of the trailing distribution; thresholds in config). Same for spread. Baselines use trailing data only.

**Session-time normalization:** on all intraday timeframes (everything below D1), both **volume and spread** baselines must be session-time normalized — compare a bar to the same time-of-day bin over the prior N sessions (N configurable, default 20). Intraday volume/volatility seasonality (open surge, lunch lull, US-open shift) is schedule, not psychology.

### Interpretive principles (encode these as the logic foundation)

- **Effort vs. result:** Wide spread on modest volume = ease of movement (low friction). Narrow spread on high volume = absorption (a two-sided battle; someone is soaking up the other side).
- **Absorption metric:** `vol_per_point` = raw volume ÷ raw spread, then normalized against its *own* trailing (session-time normalized) baseline, like every other feature. Do not divide relative measures by relative measures.
- **Close position converts effort+result into direction.** Same spread and volume with close at high vs. close at low are opposite events. A wide-range bar that closes back at its low after rallying is a failed move that trapped buyers (upthrust).
- **Symmetry:** Nearly every signature has a mirror. Absorption at resistance = distribution (bearish); the identical signature at support = accumulation (bullish). Implement one detector, sign-flipped by context.
- **Volume trend across a move:** Rising volume on the impulse leg validates a young trend but warns of climax when parabolic late in an extended trend. Falling volume on the impulse leg = demand thinning (bearish divergence). Falling volume on a *pullback* = no supply (bullish). The impulse-vs-reaction distinction must be explicit in code.
- **Signatures are hypotheses, not signals.** Climax, absorption, no-supply are hypotheses that the next 1–5 bars confirm or refute. Entries live on the confirmation bar, not the signature bar.
- **Evidence accumulates.** One narrow-spread high-volume bar at resistance is a whisper; three is absorption. Hypotheses carry strength scores that bars increment or decrement.

---

## Part 2: Bar Classification

Implement a `BarClassifier` that, for each bar, emits a feature vector and a categorical label. Features (all trailing-relative, session-time normalized on intraday TFs):

- `rel_volume`: volume vs. baseline
- `rel_spread`: spread vs. baseline (percentile)
- `close_pos`: (close − low) / (high − low); 0.5 for zero-spread bars
- `rel_vol_per_point`: (raw volume ÷ raw spread) vs. its own baseline; undefined (null) for zero-spread bars
- `direction`: sign(close − open)
- `upper_wick_frac`, `lower_wick_frac`: wick sizes as fraction of spread
- `gap`: open vs. prior close (where relevant)

**Context dependency:** several labels reference context ("after a rally," "at resistance," a prior climax for `TEST`). These always use context state **as of the previous bar's close** (see per-bar processing order, Part 3). The classifier never sees context updated with the current bar.

**Structural core vs. context qualifier (general rule):** every label decomposes into a *structural core* (bar anatomy only — direction, spread, volume, close_pos, wicks) and a *context qualifier* (phase, location, prior move). The classifier emits the structural core unconditionally; context qualifiers are applied **at the point of use**. Spawn conditions apply the full qualified label; **hypothesis confirmation events reference the structural core only** — otherwise confirmations become unreachable (e.g., `NO_DEMAND`'s "in a downtrend" qualifier can never be satisfied while the Signal TF is still in `MARKUP` after a buying climax, silently disabling H5's and H2's confirmations). The table below shows the qualified forms; mirrors `EFFORTLESS_DECLINE` and `VALIDATED_DECLINE` (exact sign-flips of their advance counterparts) also exist for the mirrored hypotheses.

Categorical labels (non-exhaustive; all thresholds in config):

| Label | Definition sketch |
|---|---|
| `EFFORTLESS_ADVANCE` | Up bar, wide spread, close_pos > 0.8, low/normal volume |
| `VALIDATED_ADVANCE` | Up bar, wide spread, close_pos > 0.8, high volume |
| `ABSORPTION` | Narrow spread, high volume, any direction — direction assigned by context |
| `UPTHRUST` | Wide spread, high volume, large upper wick, close_pos < 0.3, after a rally / at resistance |
| `SPRING` (mirror) | Wide spread, high volume, large lower wick, close_pos > 0.7, after a decline / at support |
| `POTENTIAL_BUYING_CLIMAX` | Widest spreads + highest volume of the move, late in an extended uptrend |
| `POTENTIAL_SELLING_CLIMAX` | Mirror of above in a downtrend |
| `NO_SUPPLY` | Down bar, narrow spread, volume well below baseline, during a pullback in an uptrend |
| `NO_DEMAND` | Mirror: up bar, narrow spread, low volume, during a rally in a downtrend |
| `TEST` | Low-volume probe of a prior climax/spring extreme that holds |
| `APATHY` | Narrow spread, low volume, mid close — no information |

---

## Part 3: Context Tracker & Per-Bar Processing Order

A `ContextTracker` per timeframe maintains slow-moving background state:

- **Trend direction and age** (swing structure of higher-highs/higher-lows, or configurable MA structure; record bars-since-trend-start)
- **Swing detection:** a swing high/low is a fractal — a bar whose high (low) exceeds the highs (lows) of the k bars on each side (k configurable, default 3). Swings are only confirmed k bars after the fact; the tracker must use them accordingly (a swing is not known at the bar where it occurs — no look-ahead here either).
- **Phase determination (default rules; thresholds in config):** `MARKUP` = intact sequence of higher highs and higher lows; `MARKDOWN` = mirror; `RANGING` = no new swing extreme beyond the established range for R consecutive swings or B bars (whichever first); `POST_CLIMAX` = a climax label occurred within the last N bars — it overrides the structural phase for its countdown, then resolves to whatever the swing structure then shows. Phase transitions must be logged with their trigger.
- **Phase:** one of `MARKUP`, `MARKDOWN`, `RANGING`, `POST_CLIMAX`. `POST_CLIMAX` carries a **direction attribute** (post-buying-climax vs. post-selling-climax) and a countdown (climactic event within the last N bars, resolution pending).
- **Key levels:** recent swing highs/lows, range boundaries; distance of current price to nearest level in units of ATR. "At a level" anywhere in this spec means within k × ATR of a key level (k configurable, default 0.5).
- **ATR definition:** wherever ATR appears in this spec, it means the trailing average true range computed **on the timeframe where the rule is evaluated** (period configurable, default 14). Because bars never span the overnight gap, the first bar of each session computes true range against the prior session's close (standard TR); a config flag optionally clips that gap component.
- **Background volume trend:** rising/falling/flat over the trailing window
- **Impulse vs. reaction flag:** is the current short-term move with or against the prevailing trend? **Null when phase = `RANGING`** (no prevailing trend to be with or against).
- **Signature registry:** recent signature bars (climax, spring, upthrust — extreme price, volume, age in bars), recorded at step 2 of the processing order. Required by the `TEST` label and by hypothesis confirmation logic; entries expire after a configurable age.
- **Move qualifiers:** "after a rally" / "after a marked decline" anywhere in this spec means a prior directional move of ≥ m × ATR (m configurable, default 2.0) or one completed swing leg, whichever is defined first in config.

### Per-bar processing order (resolves the classifier↔context circular dependency)

On each bar N close, per timeframe, strictly in this order:

1. **Classify** bar N using context state as of bar N−1's close.
2. **Update** `ContextTracker` with bar N (price structure, levels, phase — including any climax label from step 1).
3. **Test hypotheses:** evaluate open hypotheses against bar N; spawn new hypotheses from bar N's label.
4. **Emit signal** if a hypothesis graduates; the broker simulator acts no earlier than bar N+1's open.

---

## Part 4: Hypothesis Set

Implement a `HypothesisManager`. A hypothesis is spawned by a signature bar (or accumulating evidence), carries a strength score, an expiry (max age in bars), confirmation rules, and refutation rules. Each new bar is tested against all open hypotheses: confirm → graduate to signal; refute → kill; neither → age.

**All confirmation and refutation conditions are evaluated on Signal-TF bar closes** unless stated otherwise. Phase and context references *within* hypothesis definitions (e.g., "in an established `MARKUP` phase") refer to the **Signal TF's own** context; the Context TF's phase enters only through the gating rule (Part 5). Initial set (all parameters configurable; each has an exact mirror for the opposite direction):

### H1. Selling-Climax-and-Test (long) — reversal class
- **Signature ownership rule (applies to all hypotheses):** each signature label spawns exactly one hypothesis type — climax labels spawn H1/H1-mirror; `UPTHRUST`/`SPRING` spawn H2/H2-mirror; no label spawns two specs.
- **Spawn:** `POTENTIAL_SELLING_CLIMAX` after a marked decline, near support / new lows ("near new lows" = lowest low of the trailing lookback *including* the current bar, else the condition can never fire). The spawning bar is the **signature bar**.
- **Confirm:** within 1–5 bars, a `TEST` — authoritative criteria, checked inline: down-probe coming within a configurable ATR distance of the signature low, holding above it, recovering (close_pos > 0.5), on volume below baseline **and** below a configurable fraction (default 0.5×) of the signature bar's rel_volume — a "test" on climax-comparable volume is the battle resuming, not a test. Alternatively, a `VALIDATED_ADVANCE` off the spawn level (spawn level = the key support level, or the signature bar low when spawned via the new-low condition).
- **Refute:** close below the signature bar low (any volume; volume logged).
- **Stop:** below signature bar low. **Strength boosters:** Context TF at major support; Context TF phase turning from `MARKDOWN` to `RANGING` or `POST_CLIMAX` (selling) while open. Boosters sign-flip in the mirror (`MARKUP` → `RANGING`/`POST_CLIMAX` (buying)).

### H2. Upthrust Reversal (short) — reversal class
- **Spawn:** `UPTHRUST` after a rally / at resistance or range high.
- **Confirm:** within 1–4 bars, `NO_DEMAND` on a weak rally attempt, or a down bar closing below the upthrust bar's midpoint on expanding volume.
- **Refute:** close above the upthrust high.
- **Stop:** above upthrust high.

### H3. Absorption Breakout (with-trend) — trend class
- **Spawn:** ≥ 2–3 `ABSORPTION` bars clustered at the *same* key level (within k × ATR; level identity needs a tolerance since swing-derived levels drift — treat levels within a configurable ATR fraction as identical). Direction from Signal-TF context: at resistance in an uptrend → long breakout; mirror at support in a downtrend. **When Signal-TF phase is `RANGING`** (where "trend" is undefined and the impulse/reaction flag is null): direction = out of the range from the boundary where the absorption sits — absorption at the range high → long breakout, at the range low → short.
- **Zone:** [min(low), max(high)] over the clustered absorption bars — and the zone **extends with each further qualifying absorption bar until confirmation** (later absorption outside a frozen zone would otherwise leave the stop inside the cluster).
- **Confirm:** breakout bar: wide spread, close_pos extreme, volume expansion, and close beyond **max(level, zone edge in the trade direction)** — a close "through the level" that is still inside the absorption zone is not a breakout.
- **Refute:** wide-range, high-volume bar closing beyond the *far* side of the zone (not mere re-entry into it).
- **Stop:** far side of the zone, **computed at graduation time** on the final zone.

### H4. No-Supply Continuation (long) — trend class
- **Spawn:** pullback in an established `MARKUP` phase showing declining volume; ≥ 1 `NO_SUPPLY` bar.
- **Confirm:** up bar with close_pos > 0.7 and volume re-expanding, resuming trend direction.
- **Refute:** structural break is the trigger, volume expansion is pullback-level state: refute on the bar that closes below the last *confirmed* (k-bar lag) higher-low formed before the pullback began, provided **any** pullback bar showed expanded volume (rel_volume ≥ a configurable multiple). Requiring both on the same bar would miss the realistic sequence (expansion first, break bars later).
- **Stop:** below the pullback low, **computed at graduation time** (the pullback can deepen after spawn). Mirror: No-Demand Continuation (short).

### H5. Buying-Climax Fade (short) — reversal class; optional, gated behind a flag
- **Spawn:** `POTENTIAL_BUYING_CLIMAX` (parabolic volume late in extended uptrend).
- **Confirm:** `UPTHRUST` or `NO_DEMAND` within 1–5 bars.
- **Refute:** continued advance on sustained volume.
- **H5 is exempt from the standard MTF gating rule** (its setting is, by definition, Context `MARKUP`). Its sole gate: Context TF extended beyond a configurable ATR multiple from its trend mean. Disabled by default.

**Strength scoring:** start each hypothesis at a base score; increment for each supporting bar (further absorption, additional tests); decrement for bars that contradict the hypothesis without meeting the refutation condition; require score ≥ threshold at confirmation time. The confirming bar's own evidence delta is applied before its confirmation check (deliberate). An optional configurable strength floor kills deeply negative hypotheses early (default off — expiry handles them). Log every transition.

**Concurrency:** max one open hypothesis per spec+direction — but log blocked spawns so we can measure how often a stronger signature is suppressed by a weaker open one. Opposite-direction hypotheses may coexist (competing narratives). If two hypotheses graduate on the same bar, the higher strength wins and the conflict is logged; ties → no trade.

---

## Part 5: Multi-Timeframe Coordination

Run the identical pipeline (classifier → context → hypotheses) independently per timeframe. A `MTFCoordinator` sits above:

### Roles
- **Context TF:** defines phase/bias. — **Signal TF:** hypotheses form and mature here. — **Execution TF:** entry refinement, **fixed to 1M or 3M** (config).
- Context↔Signal ratio ~4–8× (measured in cash-session bars — a FTSE cash day is ~8.5 H1 bars, so D1/H1 sits at the upper bound). Candidate stacks to test: (D1 / H1 / 3M), (H4 / H1 / 3M), (H4 / 30M / 3M), (H1 / 15M / 3M), (H1 / 10M / 1M). The stack is a hyperparameter — but search it staged (see Part 8), not jointly with all thresholds.
- Do not use adjacent TFs (e.g., 10M+15M) as Context/Signal — they are ~80% redundant.

### Gating rule (per hypothesis class)
- **Trend class (H3, H4 + mirrors):** graduate only if direction agrees with Context-TF phase (`MARKUP` → longs, `MARKDOWN` → shorts). **Exception for H3:** it also graduates when Context-TF phase is `RANGING`, the absorption cluster sits at a Context-TF range boundary, and the breakout direction points *out of* the range — this is the classic accumulation/distribution-range breakout (the range resolving into a new trend), and without this clause it would be untradeable. Tag such trades `H3_RANGE_BREAK` in results so they can be evaluated separately from with-trend H3.
- **Reversal class (H1, H2 + mirrors):** graduate if Context-TF phase is (a) **in agreement with the trade direction** (`MARKUP` → longs, `MARKDOWN` → shorts) — a Signal-TF reversal in the direction of the Context trend is a with-trend entry (upthrust fading a reaction rally in a Context downtrend; selling climax ending a pullback in a Context uptrend) and is expected to be the highest-conviction setup in the framework; tag these `REV_WITH_TREND` for separate reporting; or (b) `RANGING` and price is at the corresponding range extreme, or (c) `POST_CLIMAX` with matching direction (post-selling-climax permits longs; post-buying-climax permits shorts). A configurable `strict_mode=false` additionally permits reversal trades while Context TF is still in the opposing phase, but only when the Signal-TF hypothesis strength meets a separate, higher threshold (config) — report results with strict mode on and off.
- **Gate-blocked confirmations (`CONFIRMED_PENDING_GATE`):** a hypothesis whose confirmation event fires while the gate is closed does not die and does not need to re-confirm. It enters `CONFIRMED_PENDING_GATE`: on each subsequent Signal-TF close, only the gate is re-evaluated (refutation conditions remain active; expiry still applies). If the gate opens before expiry, it graduates at that bar's close. All such transitions are logged.
- **H5:** exempt (see H5).

### Execution-TF refinement (defined mechanics)
After a Signal-TF hypothesis graduates: watch up to N execution bars (config, default 10) for a with-direction execution bar with close_pos beyond threshold (> 0.7 for longs, < 0.3 for shorts). Enter at the next execution bar's open. Stop: the tighter of the execution-TF local extreme (lookback configurable, default the bars observed during the refinement window) or the Signal-TF signature extreme (config choice). If no trigger within N execution bars, fall back to entry at the next Execution-TF bar open with the Signal-TF stop (or abandon — config). **Invalidation:** if the parent hypothesis's refutation condition fires on any Signal-TF close during the window, the pending refinement is cancelled (`REFINEMENT_CANCELLED_REFUTED`) — never enter a trade whose premise is already dead. Only one pending refinement may exist at a time; graduations arriving while one is pending are logged, not acted on (consistent with the one-position rule). **The EOD entry embargo (Part 7) overrides refinement:** if the refinement window reaches the embargo without a trigger, the entry is abandoned and logged. Backtest must report results **with and without** execution refinement.

### Other coordinator duties
- **Alignment score:** propose and document a formula compositing per-TF phase agreement and open-hypothesis direction agreement. Config flag selects its use: trade filter, sizing multiplier, both, or off.
- **Divergence tracking:** log reversal evidence migrating upward through the configured stack's timeframes (e.g., absorption appearing on the Execution TF, then the Signal TF, then the Context TF sequentially). **Log-only in v1** — no trading logic on it yet.
- **Timestamp discipline:** an HTF bar's state is only known at its close. At any LTF bar, the "current" HTF context is the last *closed* HTF bar. Never let a completed HTF bar's values leak into LTF decisions made before that HTF close. This is the most common MTF look-ahead bug — write a unit test for it.
- **Simultaneous closes:** multiple TFs frequently close at the same timestamp (e.g., 1M, 10M, and H1 all at 10:00). At any shared timestamp, process timeframes in **descending order (highest first)** so a bar that closes at that instant is legitimately part of "last closed HTF state" for the lower TFs processed after it. Unspecified ordering here produces either nondeterminism or an accidental one-bar context lag, and will make the future-perturbation test flaky. Write a unit test asserting the convention.

---

## Part 6: Target Instruments & Data

### Instruments (in this order)

1. **FTSE 100** — primary development instrument.
2. **DAX 40** — first portability test.
3. **NASDAQ 100** — second portability test.

**Use index futures data, not the cash index.** The cash index is a calculation with no native volume; futures carry real traded volume, which this strategy depends on:

- FTSE 100: ICE FTSE 100 Index Future ("Z")
- DAX: Eurex FDAX (or FDXM mini)
- NASDAQ 100: CME NQ (or MNQ micro)

Requirements and caveats:

- **Continuous contract:** build or ingest a back-adjusted continuous series; handle roll dates explicitly and never let a roll gap register as a price/volume signature. Volume around roll week shifts between contracts — either use volume summed across front+next contract or exclude roll-transition days from signature detection (configurable).
- **Liquidity differences:** FTSE futures are materially thinner than FDAX and NQ. Expect noisier signatures on the lowest TFs for FTSE; the relative-baseline approach should adapt, but report signature quality (e.g., label frequency stability) per instrument.
- **Fallback — tick volume:** if only CFD/spread-bet data is available, volume is tick count (number of price updates), not traded size. It correlates with real volume but weakens absorption detection, which depends on effort *magnitude*. Acceptable for prototyping; must be flagged in all reports.

### Sessions (per-instrument calendar, in config)

- **Cash session hours:** LSE 08:00–16:30 London (FTSE); Xetra 09:00–17:30 CET (DAX); US 09:30–16:00 ET (NASDAQ). This is an intraday strategy: **signature detection and trading occur within cash session hours only** (extended-hours data may still feed baselines if available, flagged in config).
- **Trading day boundary:** D1 bars resample using the cash session close as the day boundary (per-instrument config).
- **Partial (stub) bars:** cash sessions are not integer multiples of higher intraday TFs — e.g., LSE 08:00–16:30 resampled to H1/H4 leaves a 16:00–16:30 stub. Stub bars **update context but are excluded from signature detection and hypothesis confirmation** (their spread/volume are structurally incomparable to full bars, and session-time bins only partially mitigate this). Bars never span the overnight gap — each session's resampling starts fresh at the cash open. Write a resampling unit test for the stub-bar and session-boundary behavior.
- **Auctions:** opening/closing auction volume spikes (e.g., FTSE 16:20–16:30 closing surge) are schedule, not psychology. Session-time normalization must absorb them; additionally apply an exclusion window around open/close auctions for signature detection (configurable, e.g., first/last N minutes).
- **The US-open regime shift:** FTSE and DAX undergo a structural volume/volatility shift at the US cash open (14:30 London) and at US data releases (13:30 London). Session-time-relative baselines handle this statistically, but diagnostics must break down trades and hypothesis outcomes by session phase (pre-US vs. post-US-open) for European instruments — the edge may differ dramatically between phases.

### Data source: Finsa API

- **Endpoint:** `https://charts.finsatechnology.com/data/{tf}/{instr}/{side}?l={n}`
  - `tf` ∈ `["minute", "quarter", "hour", "day"]` (`quarter` presumed 15M — verify)
  - `instr`: numeric instrument ID, mapped in config. Known IDs: `uk100=16645` (FTSE 100), `ger40=17068` (DAX), `ustech100=20190` (NASDAQ 100), plus `us30=17322`, `us500=67995`, `gold=68924`, `goldvar=72302`, `eurusd=16635`. Futures instrument IDs to be confirmed by the project owner.
  - `side` ∈ `bid`, `ask`, `mid`
  - `l`: bar count; believed max 5,000 — verify empirically.
- **Step zero — feed verification (hard gate, before any engine work):** fetch samples across `tf`/`side` and produce a short report: (a) **does the payload include a volume field, and is it tick volume or traded volume?** If no volume exists at all, STOP and report back — this strategy cannot run on a volume-less feed and an alternative source is needed; (b) exact bar interval of `quarter`; (c) timestamp format and timezone (DST behavior); (d) whether any pagination/offset/"before" parameter exists beyond `l`; (e) the true `l` limit per timeframe; (f) bid/ask/mid relationship sanity check.
- **History depth & the collector:** at ~5,000 bars, `day` covers decades but `minute` covers only a handful of sessions. **Collection tooling already exists in this project** — do not build a new collector; audit and integrate with it (see Existing tooling below). The backtestable period for Signal/Execution TFs equals the accumulated 1M history — report the usable date range per instrument prominently in all results.

### Existing tooling (audit before use — Part 9, step zero)

The repo contains a two-stage data pipeline in `scripts/`, operated as:

```
# 1. pull new bars into data/ (all instruments, all timeframes, all sides)
venv/bin/python scripts/collect.py sync --instr uk100 ger40 us30 ustech100 us500 gold goldvar eurusd

# 2. check what landed
venv/bin/python scripts/collect.py status
venv/bin/python scripts/collect.py validate

# 3. rebuild the clean store from raw
venv/bin/python scripts/store.py build
venv/bin/python scripts/store.py verify
```

- **The engine reads exclusively from the clean store produced by `store.py build`** — never from the API and never from raw files. Backtests must be reproducible offline from the store alone.
- **Known defect — output paths:** the scripts currently write their outputs to `scripts/data/` and `scripts/clean_finsa/` instead of the project root. Refactor so the raw store lives at `<project root>/data/` and the clean store at `<project root>/clean_finsa/` (path constants in one place — `config.yaml` or a single module — not scattered relative paths; resolve relative to the project root, not the script's location, so the commands work from any working directory). Migrate any existing collected data to the new locations — **do not lose accumulated history**. After the refactor, prove equivalence: `store.py build` + `verify` must pass, and row counts / checksums per instrument-timeframe must match the pre-refactor store.
- The step-zero audit must establish: the clean store's schema and format (columns — **is volume present, and what does it represent?** — timezone handling, DST); what `sync` actually fetches ("all feeds, all sides" — confirm which timeframes and bid/ask/mid are covered); dedup and gap behavior on repeated syncs; what `validate` and `verify` actually check versus what this spec needs (session gaps, duplicate timestamps, monotonicity); and — critically — **how much 1M history per instrument is already accumulated** (from `status`), which defines the initial backtestable window.
- If the existing pipeline lacks something the spec requires (e.g., gap logging, a needed timeframe or side), extend it rather than working around it, and document the change.
- **Hybrid TF seeding (amends the resample-only rule):** Context TFs (D1, H1) may be seeded from the native `day`/`hour` endpoints, giving deep history for context warmup and phase structure. Signal/Execution TFs, and all 1M intrabar resolution (Part 7), use collected 1M data. Where native and 1M-resampled bars overlap, run a consistency check and report discrepancies. **Trades are only simulated where 1M data exists.**
- **Bid/ask usage:** build bars from `mid`; sample `bid`/`ask` to estimate spread per session-time bin, feeding the cost model — where spread data exists, model fills as long entries/short exits at ask and long exits/short entries at bid, replacing flat slippage (keep flat slippage as fallback config). Note which instruments have variable spread.
- **Volume-type caveat:** the listed IDs are cash-index CFDs — expect tick volume at best (see fallback note below). Every report must state which volume type was used.

### Data ingestion & engineering

- The collector emits OHLCV (timestamp, open, high, low, close, volume), timezone-normalized, to the local store; the engine reads only from the store, never the API directly — backtests must be reproducible offline. Resample collected **1M** into intermediate TFs internally (subject to hybrid seeding above). Architecture generic across instruments: same config schema, per-instrument session calendar and tick size.
- **Warmup:** no signature detection and no trading until *all* rolling baselines, session-time-normalization bins, and context structures are fully populated on every TF in the stack (first N sessions excluded; N derived from the largest configured window and logged).
- **Data quantity:** given Context TFs up to D1 and walk-forward requirements, several years of 1M history per instrument is expected. Flag if the provided data is insufficient for the configured windows/folds rather than silently shrinking them.
- **Gaps/holidays:** handle session gaps and holidays explicitly (no fake bars).
- **No look-ahead, anywhere:** all rolling stats trailing-only; decisions at bar N use data through bar N's close only; fills occur no earlier than bar N+1 open.
- **Event-driven backtest loop** (bar-by-bar), not vectorized signal generation — hypothesis state is path-dependent. **Performance note:** with years of 1M data across multiple TFs, precompute all per-bar *features* (baselines, rel_volume, ATR, session bins) vectorized upfront; keep only the *stateful* layers (context, hypotheses, broker) in the event loop.
- **Narrative log:** for every bar, log: bar label, feature vector, context state, open hypotheses with scores, transitions (spawn/confirm/refute/expire), and MTF alignment. Output as structured JSONL so any trade can be fully audited. **Log-volume control (config):** full per-bar detail on Signal TF and above by default; Execution/1M bars logged in full only within a window around trades and hypothesis lifecycles (years of 1M full-detail JSONL would be unmanageable). Also produce a human-readable narrative dump for a specified date range ("At 14:30, H1 context = MARKUP; 10M spawned ABSORPTION hypothesis at 4512, score 2...").

---

## Part 7: Trade & Risk Management

### Intraday discipline (core rule, not a simplification)
- **No overnight positions.** All open positions are force-closed at a configurable cutoff before the cash close — default: the start of the closing-auction exclusion window (e.g., 16:15 London for FTSE).
- **Entry embargo:** no new entries within a configurable window before the cutoff (default 30 minutes) — a trade needs room to work.
- Force-closed trades are tagged `EOD_EXIT` in results and reported as their own category.

### Entries, stops, fills
- **Entry:** on hypothesis graduation, at next Signal-TF bar open — or via Execution-TF refinement (Part 5). Configurable slippage on all fills.
- **Stop placement:** signature extreme ± a tick buffer (configurable, default 2 ticks beyond).
- **Stop fills:** if a bar gaps through the stop, fill at that bar's open (the worse price), never at the stop level.
- **Intrabar stop/target ambiguity:** when a Signal-TF bar's range touches both the stop and the target, replay that bar's constituent **1M bars** to determine which was hit first. If a single 1M bar touches both, assume **stop first** (conservative). This is why 1M is the mandatory base timeframe.

### Exits
- **The stop is always active in every exit mode.**
- Exit modes to implement and compare: (a) fixed R-multiple targets (test 1R/2R/3R), (b) opposing-hypothesis exit (an opposite-direction hypothesis confirming on the Signal TF closes the trade), (c) context-flip exit (Context-TF phase flips against the position).
- **Time stop:** maximum trade duration in Signal-TF bars (configurable) applies in all modes; and the EOD cutoff overrides everything.

### Sizing & costs
- Fixed fractional risk per trade (e.g., 0.5–1% of equity based on stop distance), optionally scaled by alignment score (per config flag).
- **Contract granularity:** starting equity, point value, and tick size per instrument in config (e.g., FTSE Z = £10/point). Position size = risk budget ÷ (stop distance × point value), **rounded down to whole contracts**. If that rounds to zero, skip the trade and log it as `SKIPPED_SIZE` — these must appear in diagnostics, since frequent skips mean the equity/stop-distance combination is unrealistic.
- Commission + slippage as configurable parameters; report results at zero cost and at realistic cost, side by side.
- One instrument, one position at a time. Signals arriving while in a position are logged, not traded as entries — **no reverse-and-flip** (an opposite-direction confirmation may still close the trade under exit mode (b), but never opens the reverse position).

---

## Part 8: Backtest Methodology & Evaluation

- **Lockbox (out-of-sample reserve):** before any analysis begins, carve off the most recent ~20% of accumulated 1M history (minimum 4 trading weeks once available) and exclude it **programmatically at the store/loader level**, not by convention. Every iteration cycle — reviewing results, refining rules, re-running — quietly fits the strategy to the data it's shown; the lockbox is the defense. It is evaluated against **exactly once**, when iteration is declared complete, as the final verdict. As new data accumulates, it joins the lockbox, not the working set, until the next formal iteration round.
- **Event-study layer (signature predictiveness, independent of trading):** for every *confirmed* hypothesis — regardless of gating, sizing, EOD rules, or whether a trade resulted — record forward mid-price returns at +5, +10, and +20 Signal-TF bars, and report their distributions against matched baseline bars (same session phase, same instrument). This yields roughly an order of magnitude more observations than the trade simulation and answers "do these signatures predict anything at all?" while the trade-level sample is still small. Report it per hypothesis, gated and ungated.
- **Walk-forward:** split data into sequential train/validation folds. Tune thresholds (volume/spread percentiles, hypothesis expiries, strength thresholds) on train, evaluate untouched on validation. No global in-sample optimization reported as results.
- **Staged hyperparameter search** (avoid combinatorial explosion): stage 1 — coarse sweep to select the TF stack with default thresholds; stage 2 — tune thresholds within the chosen stack via walk-forward. Document the search budget.
- **Frozen configuration** = the parameter set selected on the **final FTSE training fold**. Report median-across-folds parameters as a sensitivity note.
- **Metrics:** trade count, win rate, avg R, profit factor, max drawdown, Sharpe/Sortino (on daily equity), exposure, and per-hypothesis breakdown (H1–H5 and mirrors reported separately — this matters: I want to know *which* narratives carry the edge). Break out `EOD_EXIT` trades and pre-US vs. post-US session phases.
- **Baselines:** (a) buy-and-hold (intraday-adjusted: long from cash open to EOD cutoff daily); (b) naive volume breakout — long when close breaks the N-bar high with volume > 1.5× trailing baseline, mirror short; stop at 2 × ATR (config) since no signature extreme exists; same exit modes, EOD rules, and cost model as the main strategy (N in config, default 20). These establish whether the narrative machinery adds value.
- **Layer ablation (mandatory):** the strategy has three layers — location (signatures must occur at key levels), narrative gating (Context-TF phase/alignment permits or vetoes), and confirmation (the hypothesis lifecycle that triggers entry). Run the full system, then re-run with each layer independently disabled: (i) no location requirement (signatures anywhere spawn hypotheses); (ii) no gating (every matured hypothesis trades regardless of Context-TF state); (iii) location + gating but entry on the signature bar itself with no confirmation wait. Same folds, costs, and exit rules throughout. Report the full metrics table for each variant side by side, per hypothesis. This answers directly which layers carry the edge — if variant (i) matches the full system, the levels add nothing; if (ii) matches it, the MTF narrative adds nothing; if (iii) matches it, the confirmation wait only costs entry price. Run ablations with the *frozen* configuration — do not re-tune per variant, as that would flatter the ablated versions.
- **Cross-index portability (explicit evaluation stage):** develop and tune on FTSE only. Run the frozen configuration — only per-instrument session/roll calendars and tick size swapped — on DAX, then NASDAQ. If the narrative logic only works on FTSE, treat it as probable curve-fitting. Report the same full metrics per instrument and a comparison table. Per-instrument re-tuning is permitted only afterward, reported separately from frozen-config results.
- **Robustness:** parameter sensitivity sweeps (±30% on key thresholds — edge should degrade gracefully, not cliff); results by market regime (trending vs. ranging, classified ex-post for reporting only); Monte Carlo resampling of trade sequence for drawdown distribution.
- **Diagnostics:** distribution of hypothesis outcomes (spawned → confirmed/refuted/expired rates per type); MFE/MAE per trade; equity curve plots; a sample of 10 annotated trades with their full narrative logs for manual review.

---

## Part 9: Deliverables & Working Style

1. **Step zero — establish trust in the data layer before anything else, in this order:** (a) **Audit** `scripts/collect.py` and `scripts/store.py` read-only first: summarize what each does, trace the full data path (API → raw → clean store), verify correctness (timestamp handling, timezones/DST, dedup, gap behavior, error handling, partial-fetch behavior), and flag any issues found. (b) **Refactor** the output paths to project root per Part 6, with the equivalence proof (no history lost, row counts/checksums match). (c) **Verify the feed and store:** answer the feed-verification questions (Part 6) — preferring inspection of already-collected data over new API calls where possible — and deliver the verification report, including accumulated 1M history per instrument. **Do not begin engine work until all three are complete and the volume question is answered.** If the audit finds bugs affecting already-collected data (e.g., timezone drift, silent gaps), report them before fixing — we need to know whether historical data needs re-validation.
2. Project skeleton: extend the existing repo — `scripts/` (existing pipeline), `data/` (raw store), `clean_finsa/` (clean store), adding `engine/` (classifier, context, hypotheses, coordinator, broker sim), `backtest/`, `reports/`, `tests/`, `config.yaml` for all thresholds.
3. Unit tests: bar classifier edge cases (zero spread, missing volume), no-look-ahead tests (the HTF-close timing test, the **future-perturbation test**, and the **precomputed-feature truncation-equivalence test** — see Non-Negotiable section), per-bar processing-order test, hypothesis lifecycle tests, resampling correctness (trading-day boundary, stub bars, session-boundary behavior), collector tests (dedup, gap detection, idempotency), native-vs-resampled consistency test, intrabar 1M-resolution test, EOD force-close and entry-embargo tests, contract-rounding/`SKIPPED_SIZE` test, lockbox-exclusion test.
4. **Synthetic-scenario verification (before any backtest):** construct hand-built bar sequences exercising each hypothesis's full lifecycle and every gate branch — at minimum: upthrust during Context `MARKDOWN` (must graduate as `REV_WITH_TREND`), selling climax + TEST while gated with a Context phase flip afterward (must graduate via `CONFIRMED_PENDING_GATE`), H3 with a growing zone and a false "breakout" inside the zone (must not confirm), H4 with volume expansion and a structural break on different bars (must refute), and a refutation arriving during a pending execution refinement (must cancel). Produce the narrative logs for each; we review them together against the psychology appendix before real data is touched. Every pass so far has found bugs one layer deeper than the last (document → instantiation → runtime trace); this is the execution-layer defense.
5. Run on the collected data; produce the metrics report + narrative samples, stating the usable 1M date range and volume type.
6. **Before writing code:** restate the hypothesis confirmation/refutation rules and the gating rules as pseudocode and flag any remaining ambiguity or contradiction you find in this spec. Ask questions rather than guessing on ambiguous psychology rules.
7. Iterate: after the first backtest, we will review per-hypothesis performance and the annotated narrative samples together, then refine thresholds and rules. Expect the hypothesis set to change.

## Known simplifications (v1)

- OHLCV only — no tick data, order flow, or bid/ask (close_pos is a proxy for intrabar victory, not ground truth).
- Development on FTSE first; DAX and NASDAQ enter only at the portability stage. One instrument, one position at a time.
- Primary feed is Finsa cash-index CFD data: volume is expected to be tick volume, and the backtestable period for Signal/Execution TFs is bounded by accumulated 1M history. Futures data with true volume remains the preferred upgrade path.
- Strictly intraday; overnight holding with gap-through-stop modeling is a v2 consideration.
- Support/resistance from swing structure only (no volume profile levels yet — candidate for v2).
- Divergence-migration across timeframes is logged, not traded (v2 candidate).
- If tick-volume (CFD) data is used instead of futures volume, absorption-based hypotheses (H3 especially) are degraded — flag in all reports.

---

## Appendix: The Psychology Behind the Rules

This appendix is interpretive, not executable — use it to resolve judgment calls the spec doesn't cover, in the spirit intended. Every rule above derives from reading three variables (spread = size of the battle, volume = size of the armies, close position = the victor) against context:

| Signature | At/after highs, at resistance | At/after lows, at support |
|---|---|---|
| Wide up bar, close at high, high vol | Buyers confident — but if climactic, smart money is selling *to* them | Buyers seizing control; sellers overwhelmed |
| Wide up bar, close at high, low vol | Complacent drift; nobody opposing, nobody committing — fragile | Short-covering / absence of supply; demand unproven |
| Narrow bar, high vol | Buyers straining; sellers absorbing — distribution | Sellers straining; buyers absorbing — accumulation |
| Wide bar, close at low, high vol | Upthrust: buyers trapped, sellers seized control mid-bar | Failed rally; sellers still dominant |
| Wide down bar, close at high, high vol | Dip-buyers contesting the move | Spring/climax rejection: sellers exhausted, buyers absorbed the panic |
| Narrow bar, low vol, mid close | Apathy — vacuum before rotation | "No supply" if a pullback — quiet before demand returns |

Sequence principles: rising volume validates a young impulse and warns of climax when parabolic late; falling volume on an impulse = thinning demand; falling volume on a pullback = no supply (healthy). Signatures are hypotheses; the next 1–5 bars confirm or refute them; evidence accumulates — one bar is a whisper, three are a statement. Higher timeframes tell you which side the strong hands are on; lower timeframes tell you when they're active.
