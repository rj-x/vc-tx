# GLOSSARY (register 60 — enforceable)

One line of plain English per term. Every generated report links here; the
enforcement test (tests/test_glossary.py) sweeps the generated reports,
the register, and docs for uppercase terms and fails the suite on any
term not defined below. New terms enter this file in the same commit that
first uses them, or the commit doesn't pass.

## Measurement terms

- **MAE** — maximum adverse excursion: the worst the price moved against a position before it exited.
- **MFE** — maximum favorable excursion: the best the price moved in a position's favor before it exited.
- **time-to-MFE** — minutes from entry until the favorable extreme was reached.
- **initiation** — strict grading convention: a qualifying episode must BEGIN in the hour after the fire (the signal called the start).
- **participation** — lenient grading convention: the forward window overlapped a move that may already have been underway (the signal was merely aboard).
- **capture** — participation's honesty companion: the median favorable points actually available after the fire.
- **precision** — of all fires, the share followed by the predicted outcome.
- **coverage** — of all outcomes that happened, the share the signal fired before.
- **earliness** — how many points of the eventual move remained available at fire time.
- **lift** — a signal's hit rate minus what chance would give (in percentage points, pp).
- **base rate / chance rate** — how often the outcome happens with no signal at all (the "pp" backdrop lift is measured against).
- **conditioned baseline** — the chance rate computed only over bars in the same state the signal fires in (its class, its session, its volatility) — the fair comparison.
- **episode** — a qualifying directional move, the unit the grading conventions count.
- **qualifying move / major move** — a price move big enough (by the registered thresholds) to count as an episode; "major" is the larger registered tier.
- **drift adjustment** — subtracting the tape's own average drift from an event study so a rising market doesn't flatter long signals.
- **pp** — percentage points (a difference of two percentages, never a ratio).
- **p90 / p95 / p25 / p75 / p10 / p20** — percentiles: the value 90% (95%, …) of observations sit below.
- **n** — sample size; the count behind any number. Small n = weak evidence.
- **Δmed** — delta-median: a median-per-trade difference (signal minus its matched baseline).

## Structure terms

- **working set** — history up to 2026-08-04: freely simulatable, tunable, re-runnable.
- **forward zone** — everything after go-live (2026-08-14): visible to paper trading and grading, never used for tuning.
- **lockbox** — the sealed span between working set and go-live: served for narrative replay only, no metrics or aggregates permitted. Register 85 (2026-08-27): the span is its OWN ZONE — neither backtest nor forward; trades opening inside it are excluded from every evidential aggregate project-wide; spendable only by a future dated ruling, never by default.
- **sealed window** — quarterly futures-roll windows (from 2026-09-01: Sep/Dec/Mar/Jun days 1–14 UTC) excluded from every study.
- **backtest window / forward window** — the two reporting spans: before the lockbox boundary, and after go-live.
- **session names** — asia (Tokyo hours), london (LSE open to NY open), overlap (London and NY both open), ny_only (NY after London close), dead (none of the above); NY = New York.
- **go-live** — the moment the paper deployment started (2026-08-14T15:04:09Z); the forward zone's left edge.

## Object families

- **H-numbers (H1…H16)** — hypotheses: falsifiable claims about the tape. Example: H2 "a failed probe beyond an extreme reverses."
- **S-numbers (S0-H2, S1-H11, …)** — signal configurations: a hypothesis's concrete firing condition; S0 is the founding configuration, S1+ are registered variants. Example: S1-H11 is H11's suppression variant.
- **Q-numbers (Q1-H6, Q2-H9, …)** — pre-registered questions: a prediction with grading conditions attached to a hypothesis, graded on forward accrual. Example: Q1-H6 "the London suppression persists."
- **serial letters (A1, F3, P5, R1–R6, T1, T3, T3B, …)** — register-internal serials: audit findings (F), audit approvals/pins (P/A), open questions of the founding review (R), and the T-series lab experiments; meanings live in the register entries that coined them.

## Label anatomy

- **ND / NS** — no-demand / no-supply: a narrow, low-volume bar closing against the effort direction — the crowd isn't there.
- **upthrust** — a probe above resistance that closes back below — a failed breakout, bearish.
- **spring** — the mirror: a probe below support that closes back above — a failed breakdown, bullish.
- **climax** — an extreme-volume, wide-range bar after a run (SELLING_CLIMAX / BUYING_CLIMAX): potential exhaustion.
- **test** — a low-volume revisit of a prior high-volume area, checking whether supply/demand is still there.
- **effortless move** — price travel on shrinking volume: no opposition (the EFFORTLESS / S-EFFORTLESS-SEQ family).
- **absorption** — heavy volume without price progress: someone is quietly taking the other side.
- **structural label** — any of the above when produced by the classifier on settled bars (UPTHRUST, SPRING, NO_SUPPLY, NO_DEMAND, SELLING_CLIMAX, BUYING_CLIMAX).

## Machinery

- **ATR / ATR15 / k×ATR(15M)** — average true range: the typical bar-to-bar movement, here computed on 15-minute bars; "3×ATR" = a stop three of those units away.
- **stop-width ladder** — the register-59 instrument: the same fires harvested at stops of 1.5/2/3/4/5×ATR(15M) plus NOSTOP.
- **NOSTOP** — the ladder's endpoint: no stop-loss at all, exit at end of day — what looseness ultimately buys or costs.
- **R- prefix (R-OP1, R-FLIPGUARD, R-LADDER, …)** — recipes: exit/stop harvest rules applied to fires; the signal layer never changes.
- **R-BE / R-ARM15 / R-NOTRAIL** — the management ladder v2 (register 77): breakeven-at-thesis-scale, trail-armed-at-progress (15M anchor), and stop-only-hold-to-EOD — graded beside the R-OP2 incumbent.
- **R-NEXIT-EARLY / R-NEXIT-FULL / R-NEXIT-SENT** — the narrative-exit family (registers 81/82): ARM15 mechanics plus opposing-event exits. EARLY/FULL are the atomic-trigger controls (pre-arming vs any-time); SENT exits only on a minted composite sentence firing against the position — SENT vs FULL is the atoms-vs-sentences exit-layer test.
- **B- prefix (B-TREND, B-RANDOM, B-ALWAYS-LONG)** — baseline pseudo-signals: controls run through the identical harvest machinery, never candidates; they print in the fenced BASELINES section only.
- **PoC / POC** — point of control: the price with the most traded volume in a profile.
- **value area** — the price band around the PoC holding the registered share (70%) of traded volume; VA / VAL / VAH = the area and its low/high edges.
- **VWAP** — volume-weighted average price: the session's average price weighted by volume.
- **one-position rule** — while a signal's position is open, its further fires are not taken.
- **honest fills** — the register-41 rules: stop wins ties, gaps fill at the worse price, trails ratchet on settled bars only, flat at end of day.
- **fill model (pessimistic / optimistic)** — a standing fact of each artifact family (register 65): the harvest-ladder family prices stops PESSIMISTICALLY (always fill against you); any touch=fill family prices targets OPTIMISTICALLY (always fill for you). Every artifact header states its family; numbers across families are not comparable; a real scalp recipe's optimism carries a stated, operator-ratified haircut.
- **dimming (°)** — the small-n convention: n<20 rows print dimmed and are excluded from label arithmetic; single-digit cells are unmeasurable.
- **EOD** — end of day: each instrument's native session close, where every simulated position goes flat.
- **spread** — the buy/sell price gap; charged once per simulated trade at the instrument's measured median.
- **TF / MTF / HTF** — timeframe / multi-timeframe / higher timeframe (1M, 15M = 1-minute, 15-minute bars).
- **OHLC / OHLCV** — a bar's open, high, low, close (and volume).
- **SL / TP** — stop-loss / take-profit levels.
- **fire** — the moment a signal's condition is met on a settled bar.
- **stub** — a placeholder bar carrying no trade data, excluded from studies.
- **coil** — a volatility squeeze: unusually small trailing range (the flagged proxy pending the real instrument).
- **node / gap (volume profile)** — a high-volume price shelf vs a low-volume vacuum between shelves.
- **ratchet** — a trailing stop that only ever tightens, never loosens.
- **arming** — a staged recipe's transition condition (progress or age) that switches its exit behavior on/off.

## Process vocabulary

- **pre-registration** — writing the prediction, grading conditions, and yardsticks into the counted trial log BEFORE looking at the answer.
- **yardsticks** — the mandatory trial-log field naming the conventions a study will be graded by.
- **Evidence Regression** — the register-25 standing rule: when a defect is found, everything computed downstream of it is suspect until rerun and diffed.
- **TAINTED-RERUNNABLE** — an artifact class: known to be contaminated by a fixed defect, and cheap to regenerate cleanly.
- **blast radius** — the set of artifacts, tests, and beliefs a given defect could have contaminated.
- **twin-run** — determinism check: run the same computation twice, require bit-identical output.
- **pin** — a test that freezes a ruling, an incident, or a value so it cannot silently drift; "pinned" = protected by one.
- **counted** — entered in the trial log so multiple-comparisons honesty is preserved.
- **minted** — a new hypothesis admitted through the front door (registered, counted, numbered).
- **ratified** — an operator decision that turned a flagged/proposed value into an authorized one.
- **FLAGGED / implementer-proposed** — a value chosen by the implementer to make a study runnable, awaiting operator ratification.
- **PROVISIONAL** — the stamp on unvalidated instruments (ger40fut, nas100fut, us30fut) until their validation evenings.
- **OBSERVATIONAL** — the stamp on studies that feed no thresholds, rules, or promotions — texture, never validation.
- **canonical** — the home, fully-validated instrument (uk100fut) whose readings carry evidential weight.
- **GENERATED** — the stamp on reports built entirely by code from logged artifacts; hand-editing them is banned.
- **register** — audit/strategy_findings_and_risks.md: the append-only numbered record of findings, rulings, and orders.
- **runbook** — a step-by-step operator procedure document (docs/runbook_*.md): what to run, what healthy output looks like, what to escalate.
- **docket** — the agenda of items awaiting an operator sitting.
- **sitting** — an operator decision session that disposes of the docket.
- **campaign / Part C** — the weekly one-command evidential pipeline; Part C is its forward-zone study block.
- **scoreboard** — the per-instrument signal grading artifact (hypothesis_performance.md).
- **census** — a pre-registered observational sweep over a dimension (VWAP, drift, location, co-fire, conditioning).
- **conditioning matrix** — the census splitting every signal's fires by market state; the grading instrument for the open questions.
- **trade forensics** — the journal deep-review layer (register 84): reports/trades_enriched.csv (mechanical per-trade entry/path/outcome context) + reports/forensics/ (winner/loser separators vs a permutation null, exit-efficiency and winner-MAE design inputs, WATCH list, cross-market synthesis). Candidate-generation only — no gate, filter, or recipe change without its own Q-number.
- **WATCH list** — forensics cells too thin to measure but bright enough to track; each carries its n-to-measurable (rows still needed before it can be read).
- **NET LEDGER** — the forensics discovery table (register 84 amendment): cells ranked by pooled net points with mandatory working/lockbox/forward decomposition columns and a one-word forward verdict. Pooled net is candidate-generation only; no cell quotable without its forward column.
- **leaderboard** — reports/account_curves/_LEADERBOARD.csv (register 86): one row per account curve sorted by end balance, B-RANDOM member curves as the luck reference. Leaderboard-top is best-of-field by construction — never quoted alone.
- **VSA** — volume-spread analysis: reading each bar's volume against its range and result. The in-trade VSA question (register 87): a quiet dip is the story breathing, a loud dip is the story changing — graded by conditional win rates, never assumed.
- **deceleration-against** — an in-trade census event class (register 95): the third successive new extreme in the position's direction whose leg velocity (points per bar, registered swing convention) declined strictly across three legs — the docketed RSI-divergence exit measured indicator-free.
- **key zone / zone census** — an H4-scale price level from a fractal swing extreme whose reversal reached the registered 1.5×ATR(H4); active from the reversal's confirmation, invalidated at the same multiple beyond (register 95). The zone census tags fires in/out of the ratified retest band and splits performance against zone-conditioned bases — the location family's first higher-timeframe member. v2 (register 96) is a STRICTNESS LADDER — reversal multiple {1.5, 3.0}×ATR(H4) × extreme-significance {none, 1, 3, 5}-session high/low — with freshness (zone age in sessions, touch number) carried as measured splits; v1 is the null anchor.
- **H6 refinement program** — a counted experiment family on the scalp thread (register 100): the co-fire context census with a ≥3-of-4-instrument discriminator, veto counterfactuals on identical fires, and the time-cap derivation; v0 untouched, every survivor a candidate v1 arm through the front door.
- **event clock** — the event-clock census (register 104): journal outcomes in vs out of scheduled-news windows (currency-tagged, calendar coverage stated, verified-empty gaps dated) and auction-slot windows (native cash open/close), mechanisms separated; candidate rules are ex-ante entry pauses, distinguished from reactive cooldowns.
- **verified-empty** — a calendar gap a human checked against the source on a stated date and found to hold no in-scope events (data/macro_releases_log.md); it counts as no-news. Unverified gaps exclude their days instead.
- **risk grid** — the scalp risk-grid v1 (register 103): the stop ladder (the arms' own fires re-simulated under tighter initial stops, reachers amputated vs stops saved, with the reacher-MAE curve) and the cooldown ladder (no new entries for T minutes after a full-stop exit, with the mechanism cut beside it); measurement only, member floors under identical rules, survivors propose jointly with the register-101 derivation.
- **circuit breaker** — a measured exposure-control counterfactual on the scalp arms (register 102): halt the rest of the native trading day after k full-stop exits or N consecutive losers, replayed in strict fill order; stops dodged vs targets/eod forfeited, priced from the actual foregone rows, against member floors under identical rules. Exposure control, not harvest timing.
- **veto counterfactual** — the filtered-vs-unfiltered book on identical fires for a candidate-grade class: reach, net, rows retained, amputation cost — the price of the filter, printed before any arm registers.
- **time cap** — a bar-count exit for non-reaching scalp fires only (the target retained), distinguished from register 64's ruled-out time-exit harvest; proposes jointly with the v1 price-stop.
- **fire ledger** — the row-level truth of the grading aggregates (register 91): reports/fires.csv (one row per signal fire — initiation/participation outcomes per the registered conventions) and bar_persistence_fires.csv (per-fire reach outcomes). Aggregates propose, rows confirm: no question's grade is enacted without row-level review.
- **capture study** — the protection measurement layer (register 88 item 4): when a trade has shown +X, which protection (BE rung / trail / ratchet schedule) maximizes kept-points per family × session × tape-character. Scoped policies expected, none adopted without a Q-number.
- **tape-character** — a trade's underwater volume class (register 88 item 4, from the underwater census machinery): clean (no underwater close) / quiet-dip / loud-dip (a loud underwater close before the first positive close).
- **underwater census** — the loser-cutting measurement layer (register 87): per-trade underwater trajectories, path classes, survival curves, the cut-rule and breakeven ladders with baseline floors, and the re-entry read on the undeduped fire stream. Measurement before machinery; no cut rule without its own Q-number.
- **thesis-campaign** — a maximal constant-direction narrative-state episode (register 87; v1 state = the 15M phase-tracker trend). Named to avoid colliding with the weekly campaign pipeline. The thesis-campaign study replays the journal under the operator's probe/BE/re-entry/backoff loop against mandatory random-thesis controls.
- **co-fire** — two signals from different families firing in the same window.
- **organ / sense organ** — a planned market-structure instrument (volume profile, velocity/efficiency) feeding future signals.
- **backlog** — docs/backlog_status.md: one status line per idea so nothing silently stalls.
- **ONBOARDING.md** — the collaborator handover file (repo root): stable method sections plus a marker-driven current-state section that points at generated artifacts and carries only the facts prose must (register 98).
- **staleness** — the class of defect where a hand-maintained page lags the register (register 55); the weekly campaign warns on the backlog's marker (`BACKLOG STALENESS`) and, from register 98, on ONBOARDING.md's marker lagging by more than three entries (`ONBOARDING STALENESS`); tests pin both bounds.
- **lockbox policy / zone fence** — the loader-enforced refusal to serve sealed or locked data to studies.
- **one-home rule** — hypothesis identifiers and firing conditions live in exactly one module (engine/signal_watch.py); everywhere else they are banned literals.
- **namespace closure** — only H/S/Q identifiers exist; lab serials and free names are refused by validators.
- **harvest** — everything downstream of a fire (entries, stops, exits); harvest experiments never touch the signal.
- **falling knife** — the adverse tail where price runs hard against a reversal signal immediately.

## Incidental abbreviations (context, formats, venues)

- **UTC / GMT / BST / CET / CEST / EST / EDT / ET / JST** — timezones; all storage is UTC, sessions are defined in native market timezones.
- **DST** — daylight saving time; session logic is tested against its transitions.
- **FTSE / DAX / NASDAQ / NQ** — the UK, German, and US indices behind uk100, ger40, nas100 (NQ = the CME NASDAQ-100 future, the volume-plausibility reference); US30 tracks the Dow.
- **UK / US / GB / NY** — United Kingdom / United States / Great Britain / New York.
- **GBP / USD / EURUSD** — pound sterling / US dollar / the euro-dollar currency pair (amounts like GBP0.5 / GBP1 / GBP25 read "£0.5" etc.).
- **bankroll** — the account balance the lens simulates; a bankroll lens reports affordability, never evidence (register 83).
- **D1** — the daily timeframe (one bar per day) — accepted by --exec-tf but refused until the ladder carries a daily rung.
- **maxDD** — maximum drawdown: the deepest peak-to-trough fall of the balance curve.
- **LSE** — London Stock Exchange.
- **CFD** — contract for difference: the cash execution vehicle quoted with bid/ask.
- **OTC** — over the counter (not exchange-traded).
- **FOMC / MPC** — the US and UK rate-setting committees.
- **NFP / CPI / PPI / PMI / GDP / ISM / PCE / BLS** — recurring macro releases (payrolls, inflation, purchasing managers, output) and the US statistics bureau.
- **EMA / SMA / SMA20 / MA** — moving averages (exponential, simple, 20-period).
- **ORB** — opening range breakout (a parked idea).
- **OCO** — one-cancels-other order pair.
- **RNG** — random number generator (seeded, pinned).
- **CSV / JSON / JSONL / YAML / HTML / MD** — file formats; JSONL is one JSON record per line.
- **README** — a repository's front-page instructions file.
- **CLI / IDE / TTY / UI** — command line / editor / terminal / user interface.
- **SHA / VCS** — commit hash / version control system (git).
- **API** — programming interface.
- **ID** — identifier.
- **TS** — timestamp.
- **NaN / NULL** — missing values.
- **EOF** — end of file.
- **TBD** — to be decided.
- **ISO** — the international standards body; ISO week = the Monday-anchored week numbering used in weekly_summary.csv.
- **WIP** — work in progress.
- **MB / GB** — megabytes / gigabytes.
- **HHMM** — a time printed as hours+minutes.
- **GHLZ / JFE** — the Gao-Han-Li-Zhou paper (Journal of Financial Economics, 2018) H16 cites.
- **OP1 / OP2** — the numbering in R-OP1/R-OP2: operator-specified recipes #1 and #2.
- **HH / HL / LH / LL** — higher high / higher low / lower high / lower low: the latest confirmed swing compared with the previous swing of its type (the trade journal's structure tags).
- **post-hoc** — after the fact: analysis done on results already seen — exploratory by definition, never a gate without the front door.
- **counterfactual** — what would have happened under a different rule on the same trades and fills — a ledger comparison, never a strategy by itself.
- **ATV** — "average time-of-day volume": the operator's 2026-08-22 shorthand; retired unneeded — rel_volume's time-matched baseline is the existing instrument (register 66).
- **SEQ** — sequence (S-EFFORTLESS-SEQ: consecutive effortless prints).
- **GEN / GEO** — the origin-lapse suffixes of the migrated question names (general / geometry), retired at namespace closure.
- **CPG** — CONFIRMED_PENDING_GATE: the hypothesis-lifecycle state between confirmation and the entry gate.
- **per-market specialization doctrine** — register 105: markets are distinct populations with distinct participant psychology; the register specializes claims, never defaults. Cross-market replication (≥3-of-4 legs) stays the luck filter for FIELD screens — it is not an assertion that markets match.
- **per-market track** — register 105 item 2: the route by which a single-market cell becomes a question candidate outside the ≥3-leg rule — ALL of (a) a written mechanism sentence in the operator's pen, (b) a selection-aware luck budget, (c) its own forward clock at elevated n (≥1.5× the pooled-question minimum; 45 proposed at mint).
- **mechanism sentence** — the per-market track's gate (a): one falsifiable sentence, operator's pen, stating why THIS market's participants would produce the cell's behavior; the candidate pool carries an EMPTY slot per cell until it is written.
- **selection-aware null / selection-null percentile** — register 105 item 2b: a cell's permutation null computed against the ENTIRE in-market config field it was selected from (the best-of-field win rate / median under label permutation, pinned seeds), on the same consistency statistic the cell is ranked by; the cell's percentile = the share of best-of-field null values it beats. The most consistent in-market cell must beat the most consistent fake the field can manufacture.
- **consistency ruling** — register 105 item 3 (operator: consistency over magnitude): per-market candidates rank and grade on median-per-trade, win rate, and the weekly-consistency count only; net points print as context (register 62's demotion extended).
- **weekly-consistency count** — positive ISO weeks / measurable weeks (a week measurable at ≥3 rows — ratified 2026-08-29, register 105 follow-through).
- **tail-carry cap** — register 105 item 3, AMENDED 2026-08-29 (follow-through, logged correction): any cell whose single largest winning trade exceeds 25% of its GROSS WINNING points is TAIL-CARRIED and non-candidate at any n. The drafted |net| denominator was degenerate for near-zero-net cells (293 of 454 cells at the first emission — the defect's evidence); a cell with no winning trade is tail-carried by convention.
- **config WATCH page** — reports/scoreboard/per_market_watch.md (register 105 item 5): per instrument × zone, the best window / management / session by consistency statistics, every cell wearing its selection-null percentile, n, and tail-carry check; explicitly a MAP of where specialization would go, never a settings page; cells graduate only via the per-market track.
- **candidate pool (per-market)** — register 105 item 4: cells seeded from existing structure (glints, WATCH cells, the ISO-week-32 refutation cell) each with an empty mechanism-sentence slot; nothing advances without the operator's pen.
- **W32 / W32-refutation cell** — reviewer conversation shorthand for ISO week 32 (2026-08-03..09) and the us30fut open-window cell discussed at the 2026-08-29 sitting; NOT a repo object (register 105 follow-through, resolved) — the nearest artifact is event_clock.md's us30fut open cells.
- **TP ladder** — the scalp target ladder (register 106): the arms' own fires re-simulated under target {0.5 (incumbent), 0.75, 1.0, 1.5}×ATR(15M) with haircut, stop and EOD-flat unchanged; consistency-ranked per register 105 against member bands at the same rung.
- **reach-decay curve** — P(touch) by target rung per leg per arm: how fast the touch rate falls as the target moves away — the TP ladder's descriptive read.
- **geometry package** — the scalp v1 proposal shape (register 106): the stop derivation (register 101) and any surviving target rung proposed TOGETHER through the front door — one package, one ratification; never one side alone.
- **OPTIMA / single-leg optima** — plain English (plural of optimum): the best cell per leg on a ladder or field — a candidate for the WATCH page, never a rule on its own.
- **ladder hand-off** — a single-leg forward optimum from a ladder study, carried to the per-market WATCH page wearing a selection-aware null (the members' best-over-rungs); listed, never a rule.
- **PF** — profit factor: gross wins divided by gross losses (a tripwire input).
- **AC** — mains power (the suspension/travel model: the machine sleeps when unplugged).
- **DNS** — network name lookup (an executor-error incident's cause).
- **MIS** — the MIS- prefix of MIS-SCALE: a home-derived value knowingly wrong-sized off-home.
- **RULES / RULES.md** — the founding per-hypothesis specification document.
