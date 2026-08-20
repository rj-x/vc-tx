# Canonical Hypothesis Register

**The single authoritative list (register 35; SCHEMA v2, register 49,
2026-08-21).** A hypothesis H\<n\> = falsifiable claim (one plain
sentence) + origin + status. A SIGNAL S\<k\>-H\<n\> = one mechanical
configuration testing that claim: exact condition, parameters, provenance,
registration date, status. One hypothesis may have many signals; every
signal belongs to exactly one hypothesis. Global yardsticks stay shared
and outside both — signals define what fires, never how fires are marked.
NAMESPACE: H\<n\> and S\<k\>-H\<n\> are the ONLY identifier forms;
S-numbers are per-hypothesis, never reused; parameters are never edited in
place — any change is a NEW S-number. STANDING GUARDS: every signal
pre-registered with rationale before first computation; configuration
counts printed on every card and in the matrix; review labels and
promote-candidate eligibility attach to SIGNALS, never hypotheses; no
best-of-configurations display anywhere — all of a hypothesis's signals
print or none do; when claim and implementation diverge, the resolution is
a NEW signal under the honest claim — never a silent rewrite of either.
Every entry has the same five fields. The trial log, scoreboard, and lab cite
H-numbers from here — **nothing runs that isn't in this register**
(scoreboard refuses unknown IDs; test-enforced). Signal rows are named
S-H\<n\>, nothing else; lab serials and descriptive names survive only as
cross-references inside entries. Doctrine: a hypothesis is a firing
condition (register 34, pure signals); recipes live at the bottom as
historical spec.

Companion queue page: **docs/sense_organ_queue.md** — every
authorized-but-unbuilt instrument, with its hypothesis mappings, for
operator prioritization.

Audit test applied to every entry (register 35 item 3): *is the claim one
falsifiable sentence, and is the firing condition mechanical enough that
two people would agree on every fire?*

**Review governance (register 36, 2026-08-19):** reviews emit
RECOMMENDATIONS, never actions — a **Latest review** label per entry
(keep-watching / deprioritize / retire / promote-candidate), per the fixed
criteria in register 36. **Status changes only via explicit dated operator
decision entries.** Unactioned recommendations persist visibly (the
performance table shows label and status side by side). *Retire* requires
a stated reason to stop free evidence accrual. *Promote-candidate* is the
only gate-opening label and grants walk-forward ELIGIBILITY only — round
entry is a separate decision.

---

## H1
- **Claim:** A climactic bar — extreme volume on a wide spread late in an
  extended move — marks exhaustion, and price then reverses against the
  climax direction.
- **Firing condition:** structural `SELLING_CLIMAX` → +1,
  `BUYING_CLIMAX` → −1, per 1M bar
  ([signal_watch.py `_s_h1`](../engine/signal_watch.py)); climax anatomy =
  the founding structural core (config `labels.climax_*`).
- **Origin:** founding spec (prompt.md Part 2/4; RULES v3.1, 2026-08-11).
- **Signals:**
  - **S0-H1** (migrated from S-H1, all history attached): bare structural
    climax anatomy — **labeled "anatomy-only — context clause untested by
    this signal"** (audit F1). Signal-live since 2026-08-18.
  - **S1-H1** (registered 2026-08-21, register 49; resolves F1): the
    FOUNDING context-qualified climax (qualified POTENTIAL_* labels — the
    "late in an extended move" clause lives in the qualification).
    Signal-live now; record opens at the next run.
- **Status:** **signal-live** (2 signals).
- **Latest review:** keep-watching (labels attach to signals; both open).
- AUDIT: F1 RESOLVED by the S0/S1 split (claim unchanged). Trade logic
  stripped to the recipes section.

## H2
- **Claim:** A failed probe beyond a prior extreme — an upthrust above or
  spring below that closes back inside — reverses against the probe.
- **Firing condition:** structural `UPTHRUST` → −1, `SPRING` → +1, per 1M
  bar (`_s_h2`).
- **Origin:** founding spec (as H1).
- **SHARED CONDITION (register 37):** H2 and H8 are ONE firing condition
  (these prints) graded two ways — H8's fires are copied from H2's
  (`DERIVED_FIRES`, signal module), never independently computed. A reader
  must never count them as two signals.
- **Signals:**
  - **S0-H2** (migrated from S-H2, ALL history attached — including the
    2026-08-19 forward two-layer observation, whose register entry cites
    S0-H2 specifically): bare upthrust/spring anatomy — "anatomy-only —
    prior-extreme clause untested by this signal" (audit F2).
  - **S1-H2** (registered 2026-08-21, register 49; resolves F2): the
    FOUNDING qualified upthrust/spring (range-extreme context in the
    qualification). Signal-live now; record opens at the next run.
- **Status:** **signal-live** (2 signals).
- **Latest review:** promote-candidate ATTACHES TO S0-H2 (2026-08-19,
  review R1; note amended same day under the corrected PER-CONTEXT chance
  rates of register 38 — backtest lift is only +1.2pp (86/347 vs 23.6% directional
  chance), inside the ±2pp at-chance band, while forward is +10.0pp
  (26/71) and London backtest +6.3pp; the criterion ("above chance both
  windows, n≥30") is still met LITERALLY but the backtest leg is
  materially weaker than the original note stated. Payoff adds texture:
  backtest net +781 pts / forward net −60 despite the precision lift.
  RECOMMENDATION ONLY — walk-forward eligibility awaits the operator
  decision entry).
- AUDIT: PASS. Recipe stripped as H1.

## H3
- **Claim:** Repeated absorption — high effort with no result — at a price
  level precedes a breakout through that level.
- **Firing condition:** ≥ `h3.min_absorption_bars` structural `ABSORPTION`
  prints within `h3.cluster_window` bars, level-identity within
  `context.level_identity_atr_frac`×ATR, each within
  `context.level_atr_mult`×ATR of a 1M swing level; fire toward the level
  (`_SH3`). All parameters founding config, registry-cited.
- **Origin:** founding spec (as H1).
- **Status:** **signal-live** (S0-H3).
- **Latest review:** keep-watching (2026-08-19, review R1 — 0 backtest
  fires, 3 forward; the level list needs confirmed 1M swings to exist).
- AUDIT: PASS with note — the founding spawn also directioned by
  phase/range context; the bare row directions purely *through the level*
  (the claim as written). Zone growth, breakout confirmation, and the OCO
  logic are recipe layer.

## H4
- **Claim:** In an established trend, a quiet (low-volume) pullback
  resolves with trend resumption.
- **Firing condition:** *qualified* `NO_SUPPLY` → +1 / `NO_DEMAND` → −1
  per 1M bar (`_s_h4`) — the classifier's qualification (trending phase +
  active pullback, classifier.py:103-108) is exactly the founding context,
  computed mechanically.
- **Origin:** founding spec (as H1).
- **Status:** **signal-live** (S0-H4). Known property: extremely sparse on
  1M under frozen thresholds (T3 finding — the phase gate rarely opens;
  n≈1/month; see H10 for the re-anchored variant).
- **Latest review:** keep-watching (2026-08-19, review R1 — 7 fires, 0
  hits; too sparse for any criterion to bite).
- AUDIT: PASS. Pullback-mean confirm, structural-break refute, pullback
  stop = recipe layer.

## H5
- **Claim:** A buying climax that extends far above its trend mean
  mean-reverts (climax-extension fade; registered short-side only).
- **Firing condition (DRAFTED 2026-08-20, ratification pending):**
  structural `BUYING_CLIMAX` with extension — `close − SMA20(1M closes)
  ≥ 2.0 × ATR(1M)` → fire −1 (short-side only, per the founding
  registration; no mirror). Values cited to founding `h5.extension_atr`
  (2.0) and `h5.ma_period` (20); INTERPRETATION FLAG: the founding spec
  was signal-TF-flavored — the bare row reads both on the 1M pipe like
  every other row; operator may re-anchor at ratification.
- **Origin:** **founding-anatomy / fresh-start** (operator decision
  2026-08-20: REVIVE-AS-NEW — data-innocent birth, revived without its
  lost rationale; the pre-crash disable rationale stays lost, register
  finding H5-audit).
- **Status:** **signal-live** (S0-H5, event-derived, ratified 2026-08-20 —
  read on the SIGNAL TF (15M) per its founding origin; a 1M variant, if
  ever, is a separate hypothesis).
- **Latest review:** keep-watching (rows begin at the next run).

## H6
- **Claim:** A wide-spread rejection bar at a session extreme (measured
  day-relative, volume-agnostic) reverses away from the extreme.
- **Firing condition:** **not written** — definition-pending. Missing
  pieces, named: day-relative spread percentile threshold; session-extreme
  proximity band (k×ATR); close_pos and wick_frac thresholds. All are
  registered free parameters (two-layer form, candidate register
  2026-08-13) reserved for walk-forward — a bare variant would need an
  operator ruling picking provisional values or a parameter-free
  formulation.
- **Origin:** data-born 2026-08-13 (06:56Z Asia-high rejection; register
  items 8–9). Cross-ref: audit/candidate_hypotheses.md H6.
- **Status:** **signal-live** (S0-H6, ratified 2026-08-20): proximity
  0.25×ATR(15M); day-relative spread ≥ p90 over a trailing 480-bar
  window (the window length is an implementer constant, registry-flagged
  operator-adjustable); close_pos ≤ 0.25 / ≥ 0.75; wick ≥ 0.33;
  volume-agnostic. Walk-forward may still re-tune (two-layer form
  preserved).
- **Latest review:** keep-watching (rows begin at the next run).
- AUDIT: PASS (parameters ratified; the anatomy's confirm/refute/stop
  stay recipe layer in the candidate register).

## H7
- **Claim:** Quiet decline at a session extreme is disguised accumulation:
  effortless (low-volume) weakness reverses UP once selling fails to
  attract participation (mirror: quiet advance at a high reverses down).
- **Firing condition (bare variant, signal-live):** `SEQUENCE_N` (=2)
  consecutive same-direction `EFFORTLESS_*` structural prints → fire
  AGAINST the drift (`_s_h7`). AUDIT FLAG: the registered anatomy's
  **session-extreme proximity is a walk-forward free parameter and is NOT
  applied** — the bare row grades the claim direction without the location
  condition; treat readouts as the unconditioned variant.
- **Origin:** data-born 2026-08-13 (tracked EFFORTLESS_DECLINE signal,
  standing ruling 1; candidate register H7 — the falsifiable core "quiet
  ages, participation kills" is recipe/refutation layer, preserved there).
- **Status:** **signal-live** (S0-H7, bare variant). **Grading: BOTH
  modes** (register 36) — directional (the claim) and either-direction
  (movement), reported side by side.
- **Movement-not-direction finding (2026-08-18/19, recorded per operator
  order):** both directions of the effortless sequence read above chance
  in the July window (claim direction 29.5%, retired continuation
  direction 30.4%, vs ~22% per-direction chance) — the print localizes
  VOLATILITY, not direction; the either-direction grading now measures
  that property explicitly, and the directional edge question stays open.
- **Latest review:** keep-watching (2026-08-19, review R1).
- **Standing adverse evidence, on the record:** the event study reads
  effortless declines as continuing (−19bps excess at +20, n=16), and the
  retired continuation-direction row measured 30.4% (34/112) continuation
  precision vs ~23% chance in July. H7 bets against this; the scoreboard
  now grades that bet directly.

## H8
- **Claim:** Reversal-signature bar anatomy (upthrust/spring) predicts
  imminent range expansion irrespective of direction.
- **Firing condition:** structural `UPTHRUST` or `SPRING` per 1M bar
  (`_s_h8` — same prints as S0-H2, DIFFERENT claim and grading).
  **Grading: either-direction** (register 36 mode): precision = a
  qualifying move follows in EITHER direction; chance baseline = the
  either-direction base rate (own registered baseline, shown per window).
  Free parameters (bracket buffer, fill window) remain walk-forward
  recipe layer. **SHARED CONDITION (register 37):** these are H2's fires,
  copied (`DERIVED_FIRES`) — one condition, two gradings; never
  double-count.
- **Origin:** data-born 2026-08-13 (2026-08-11 10:27Z/15:47Z annotations).
  Cross-ref: candidate register H8; expansion study = its evidence
  instrument. **Standing adverse evidence:** expansion-vs-spread readouts
  (register: "evidence adverse").
- **Status:** **signal-live** (S0-H8, either-direction mode; operator
  order 2026-08-19 resolved the grading-model mismatch by defining the
  mode).
- **Latest review:** keep-watching (2026-08-19, review R1 — first
  readout).
- AUDIT: PASS under the either-direction mode.

## H9
- **Claim:** Persistent lower-TF directional pressure that recruits
  expanding participation at the parent timeframe precedes continuation
  beyond what the parent label alone predicts; pressure without
  participation expansion does not.
- **Firing condition (pre-registered 2026-08-19, changeable only by
  re-registration):** a migration chain reaching **depth ≥ 2**, fire
  stamped at the completing event's close, in the chain's direction
  (event-derived row: `scoreboard.h9_fires`, `H9_CHAIN_DEPTH_MIN`
  registry-cited). Recruitment measurement unbiased since register 28;
  the recruited/unrecruited split stays the falsifiable second clause at
  walk-forward.
- **Origin:** data-born 2026-08-14 (week-review; candidate register H9).
  Cross-refs: migration study; forward readout; cascade analysis 3a0988b.
- **Signals:**
  - **S0-H9** (migrated, history attached): pooled depth-≥2 chains —
    **labeled "recruitment-agnostic — does not test the claim's core"**
    (audit F3). [Flagged for the next sitting: operator may retire S0-H9
    if the pooled configuration isn't worth continued measurement;
    default = keep running.]
  - **S1-H9** (registered 2026-08-21, register 49; resolves F3):
    RECRUITED-ONLY depth-≥2 chains — the claim's falsifiable core.
    Signal-live now; EXPECTED STARVED at current n (July: 16/89 forward
    chains recruited), stated at registration.
- **Status:** **signal-live** (2 signals).
- **Latest review:** keep-watching (per signal).
- AUDIT: F3 RESOLVED by the S0/S1 split (claim kept).

## H10
- **Claim:** In an established 1-minute trend, no-demand/no-supply prints
  in the trend's direction signal continuation.
- **Firing condition:** structural `NO_SUPPLY`/`NO_DEMAND` with 1M
  `trend == dir` and `trend_age ≥ 10` (T1d's measured conditions exactly,
  no phase gate) → fire in trend direction (`_s_h10`;
  `ESTABLISHED_TREND_AGE` registry-cited).
- **Origin:** data-born 2026-08-17/18 — the timeframe question via the
  T1/T1d censuses; an **H4 variant re-anchored to 1M**. Cross-refs: lab
  serials T1d, T3 (transplant-null), T3b (pre-sketch — superseded by this
  entry as the signal-layer read; the recipe-layer T3b build remains
  next lab cycle's first candidate).
- **Status:** **signal-live** (S0-H10).
- **Latest review:** deprioritize (2026-08-19, review R1 — at/below
  chance in both windows, n=293 backtest, per the register-36 criterion;
  evidence keeps accruing free; the T3b recipe-layer question and any
  status change are the operator's queue decision).
- AUDIT: PASS. First readouts at/below chance (18.8% backtest, 7.1%
  forward vs ~23%) — evidence, not verdict.

## H11
- **Claim:** Price entering a low-volume price zone traverses it faster
  than baseline; entering a high-volume node it stalls or reverses at
  above-baseline rates.
- **Firing condition:** **not written** — definition-pending. Parameters
  to pre-register BEFORE any computation: price bucket size, rolling
  lookback, node/gap thresholds. Grading is behavioral/either-direction
  (traversal speed and stall/reversal rates need their own grading model —
  to be defined with the parameters). Also noted as a candidate
  CONDITIONER for existing signals (location machinery, the H6 thread) —
  the session volume profile sense-organ (register 16, backlog #2) is the
  natural instrument.
- **Origin:** data-born 2026-08-19 — operator volume-profile question +
  institutional-execution thought experiment. **Causal story (recorded per
  the origin note):** institutions execute size where they found liquidity
  before — high-volume nodes mark standing interest that absorbs or repels
  price; low-volume gaps mark prices where no business was done and none
  defends them, so price traverses fast because nobody trades there.
- **Status:** **signal-live** (S0-H11, ratified 2026-08-20): bucket 4.0
  pts, lookback 5 sessions, node = p90 / gap = p10 of the trailing
  profile. THE ROW GRADES THE TRAVERSAL CLAUSE (directional fire into a
  gap bucket, direction of travel); the NODE-STALL clause needs its own
  grading mode — registered pending sub-question. TWO STANDING FLAGS:
  (a) the weak-persistence measurement (next-session profile corr ~0.13,
  K=5 best-of-weak-field) stands as the premise's own first stress — the
  row tests exactly this; (b) the bucket is HOME-DERIVED — other
  instruments' cells carry a mis-scale caveat until per-instrument
  values are ratified.
- **Latest review:** keep-watching (rows begin at the next run).
- AUDIT: PASS for the traversal clause; stall clause pending its grading
  mode.

## H12
- **Claim:** A zone showing repeated visits with elevated volume,
  diminishing range-per-unit-volume, and drying pullback volume precedes a
  directional move away from the zone in the absorber's direction.
- **Firing condition:** **not written** — definition-pending. Sequence
  parameters to pre-register: minimum visits, visit window, and the
  mechanical definitions of "diminishing range-per-unit-volume" and
  "drying pullback volume". Directional grading (the absorber's direction
  signs the fire).
- **Origin:** data-born 2026-08-19 — same operator thought experiment as
  H11. **Causal story:** a large buyer (seller) absorbing supply (demand)
  at a level caps the range produced per unit of volume while refilling;
  when opposing pullback volume dries up, the absorber's inventory is
  complete and price moves away in their direction. **Cross-reference:**
  the multi-visit COMPOSITE of H3's single-cluster claim — H3 fires on one
  absorption cluster; H12 requires the repeated-visit sequence with the
  exhaustion signature.
- **Status:** **signal-live** (S0-H12, ratified 2026-08-20): zone = 1M
  swing level ± 0.25×ATR(15M); visit = band entry after leaving by > band
  width; ≥3 visits within 90 min; strictly diminishing per-visit median
  range-per-unit-volume; pullbacks drying (mean rel_volume < 0.7 and
  each quieter); fire at the completing visit's close, direction = the
  higher-volume approach side.
- **Latest review:** keep-watching (rows begin at the next run).
- AUDIT: PASS (mechanical conjunction; every threshold ratified or
  founding-cited).

## H13
- **Claim:** After price breaks out of the session value area on declining
  volume and reclaims it on expanding volume, it continues toward the far
  side of the value area.
- **Origin:** external trader advice via the operator, 2026-08-21 —
  **source description, verbatim:** *"I wait for the market to show it's
  hand first, and it always does. Draw the volume profile over the
  session. Shows you where the most money traded. That's the value area.
  Now the trade. Price drops below the value area low. The second it
  does, your eyes go on the volume bars. If they are declining, nobody is
  really selling and the money isn't following price lower. Then the
  buyers step in and form a wall the sellers can't push through. There's
  the bubble, sellers getting absorbed. So price gets pulled back towards
  the money. When it closes back inside the value area, and the volume
  bars grow again, that's your long. Stop below the low. Target the value
  area high, right back into the money."*
- **Lineage:** the composition of the operator's H11/H12 origination
  questions (2026-08-19) with the externally-sourced reclaim trigger —
  the register's FIRST COMPOSITE born from its own prior entries.
- **Cross-references:** H11 (geography — the value area is its map), H4
  (the fade anatomy), H2 (the spring shape at a level), H12 (the
  mechanism's causal story).
- **Signals:**
  - **S0-H13** (pre-registered then implemented 2026-08-21, register 50):
    value area = central 70% volume band of the trailing profile (POC
    expansion; H11's ratified bucket 4.0 / lookback 5); break = 1M close
    beyond the band edge; fade = excursion mean rel_volume < 1.0 vs the
    session-time baseline AND last excursion rv ≤ first (the registered
    reading of "declining" — a stricter monotone variant would be a new
    S-number); reclaim = close back inside with rel_volume > 1.0; fire at
    the reclaim close toward the far edge. Expected fire rate LOW
    (multi-clause conjunction) — stated at registration.
- **SCOPE NOTE:** the absorption clause (the buyers'-wall mechanism —
  "the bubble, sellers getting absorbed") is DELIBERATELY OMITTED from
  S0 — unmeasurable at our resolution without the dwell-time and
  cumulative-signed-volume organs (#4/#5); a richer S<k> may add it when
  those exist. S0 tests the tradeable skeleton: break, fade, reclaim,
  continuation. The source's stop/target geometry (stop below the low,
  target the far edge) is NOT part of the signal — recipe-layer material,
  noted for the future level-based grammar extension.
- **Status:** **signal-live** (1 signal). Grading: directional, standard
  yardsticks, standard sessions; conditioned-baseline check n/a.
- **Latest review:** keep-watching (record opens at the next run).
- AUDIT: PASS (every parameter cites the registry or H11's ratified
  config; the one new value — the 70% band — was operator-specified at
  registration).

---

## Retired signal rows (register 35 sweep — no third category)

- **S-TEST** (bare test prints): RETIRED. TEST is the founding
  *confirmation* pattern (RULES Sec 0) — recipe layer under the
  pure-signals doctrine, preserved in the recipes section. Bare readout
  at/below chance (21.2% backtest, 3.6% forward).
- **S-ND-NS** (bare no-demand/no-supply, unconditioned): RETIRED. An
  unconditioned fragment of H4/H10 — measured at chance (24.2% vs ~23%,
  n=2046); the conditioned versions are the registered hypotheses; a
  duplicate row adds noise, not information. Its one distinctive readout
  (49% coverage, high-noise early warning) is recorded here for the
  future recall question.
- **S-EFFORTLESS-SEQ (continuation direction)**: RETIRED as mis-mapped —
  it graded the OPPOSITE of H7's registered claim. Its readout survives
  as H7's standing adverse evidence (above). Replaced by S0-H7 (claim
  direction).

## Recipes (historical spec — NOT hypotheses; frozen_v1 baseline record)

The founding H1–H5 machinery — confirmation windows, TEST-of-signature and
midpoint confirms, strength ledger, MTF gates, refinement micro-loop,
signature/pullback/zone stops, 2R exits, EOD discipline — is the
**recipe layer** (RULES v3.1; engine/hypotheses.py SPECS). It runs
untouched in frozen_v1 on paper as the null-baseline record. Under the
pure-signals doctrine it is graded as `founding_recipes_at_confirmation`
in the scoreboard, kept distinct from signal rows. Candidate recipe
layers (H6–H9 confirm/refute/stop anatomy; H7's "quiet ages,
participation kills" core) stay frozen in audit/candidate_hypotheses.md
for walk-forward.
