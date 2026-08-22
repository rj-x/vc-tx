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
- **lockbox** — the sealed span between working set and go-live: served for narrative replay only, no metrics or aggregates permitted.
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
- **B- prefix (B-TREND, B-RANDOM, B-ALWAYS-LONG)** — baseline pseudo-signals: controls run through the identical harvest machinery, never candidates; they print in the fenced BASELINES section only.
- **PoC / POC** — point of control: the price with the most traded volume in a profile.
- **value area** — the price band around the PoC holding the registered share (70%) of traded volume; VA / VAL / VAH = the area and its low/high edges.
- **VWAP** — volume-weighted average price: the session's average price weighted by volume.
- **one-position rule** — while a signal's position is open, its further fires are not taken.
- **honest fills** — the register-41 rules: stop wins ties, gaps fill at the worse price, trails ratchet on settled bars only, flat at end of day.
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
- **docket** — the agenda of items awaiting an operator sitting.
- **sitting** — an operator decision session that disposes of the docket.
- **campaign / Part C** — the weekly one-command evidential pipeline; Part C is its forward-zone study block.
- **scoreboard** — the per-instrument signal grading artifact (hypothesis_performance.md).
- **census** — a pre-registered observational sweep over a dimension (VWAP, drift, location, co-fire, conditioning).
- **conditioning matrix** — the census splitting every signal's fires by market state; the grading instrument for the open questions.
- **co-fire** — two signals from different families firing in the same window.
- **organ / sense organ** — a planned market-structure instrument (volume profile, velocity/efficiency) feeding future signals.
- **backlog** — docs/backlog_status.md: one status line per idea so nothing silently stalls.
- **lockbox policy / zone fence** — the loader-enforced refusal to serve sealed or locked data to studies.
- **one-home rule** — hypothesis identifiers and firing conditions live in exactly one module (engine/signal_watch.py); everywhere else they are banned literals.
- **namespace closure** — only H/S/Q identifiers exist; lab serials and free names are refused by validators.
- **harvest** — everything downstream of a fire (entries, stops, exits); harvest experiments never touch the signal.
- **falling knife** — the adverse tail where price runs hard against a reversal signal immediately.

## Incidental abbreviations (context, formats, venues)

- **UTC / GMT / BST / CET / CEST / EST / EDT / ET / JST** — timezones; all storage is UTC, sessions are defined in native market timezones.
- **DST** — daylight saving time; session logic is tested against its transitions.
- **FTSE / DAX / NASDAQ** — the UK, German, and US indices behind uk100, ger40, nas100; US30 tracks the Dow.
- **UK / US / GB / NY** — United Kingdom / United States / Great Britain / New York.
- **GBP / USD / EURUSD** — pound sterling / US dollar / the euro-dollar currency pair.
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
- **WIP** — work in progress.
- **MB / GB** — megabytes / gigabytes.
- **HHMM** — a time printed as hours+minutes.
- **GHLZ / JFE** — the Gao-Han-Li-Zhou paper (Journal of Financial Economics, 2018) H16 cites.
- **OP1** — the numbering in R-OP1: operator-specified recipe #1.
- **SEQ** — sequence (S-EFFORTLESS-SEQ: consecutive effortless prints).
- **GEN / GEO** — the origin-lapse suffixes of the migrated question names (general / geometry), retired at namespace closure.
- **CPG** — CONFIRMED_PENDING_GATE: the hypothesis-lifecycle state between confirmation and the entry gate.
- **PF** — profit factor: gross wins divided by gross losses (a tripwire input).
- **AC** — mains power (the suspension/travel model: the machine sleeps when unplugged).
- **DNS** — network name lookup (an executor-error incident's cause).
- **MIS** — the MIS- prefix of MIS-SCALE: a home-derived value knowingly wrong-sized off-home.
- **RULES / RULES.md** — the founding per-hypothesis specification document.
