# Canonical Hypothesis Register

**The single authoritative list (register 35, 2026-08-18).** Every entry
has the same five fields. The trial log, scoreboard, and lab cite
H-numbers from here — **nothing runs that isn't in this register**
(scoreboard refuses unknown IDs; test-enforced). Signal rows are named
S-H\<n\>, nothing else; lab serials and descriptive names survive only as
cross-references inside entries. Doctrine: a hypothesis is a firing
condition (register 34, pure signals); recipes live at the bottom as
historical spec.

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
- **Status:** **signal-live** (S-H1).
- **Latest review:** keep-watching (2026-08-19, review R1).
- AUDIT: PASS. Trade logic (confirmation window, spawn levels, boosters,
  2R stops) stripped to the recipes section.

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
- **Status:** **signal-live** (S-H2).
- **Latest review:** promote-candidate (2026-08-19, review R1; note
  amended same day under the corrected PER-CONTEXT chance rates of
  register 38 — backtest lift is only +1.2pp (86/347 vs 23.6% directional
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
- **Status:** **signal-live** (S-H3).
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
- **Status:** **signal-live** (S-H4). Known property: extremely sparse on
  1M under frozen thresholds (T3 finding — the phase gate rarely opens;
  n≈1/month; see H10 for the re-anchored variant).
- **Latest review:** keep-watching (2026-08-19, review R1 — 7 fires, 0
  hits; too sparse for any criterion to bite).
- AUDIT: PASS. Pullback-mean confirm, structural-break refute, pullback
  stop = recipe layer.

## H5
- **Claim:** A buying climax that extends far above its trend mean
  mean-reverts (climax-extension fade; registered short-side only).
- **Firing condition:** none running. The engine spec exists
  (spawn on `POTENTIAL_BUYING_CLIMAX` with `h5.extension_atr`/`ma_period`)
  but is recipe-shaped.
- **Origin:** founding spec (as H1).
- **Status:** **disabled** — operator ruling 2026-08-19: *"disable
  rationale lost to pre-crash era; preserved conservatively; revival =
  fresh review as new."*
- **Latest review:** pending-on-operator (revival is a fresh review, not
  a label).

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
- **Status:** **definition-pending**.
- **Latest review:** pending-on-operator (a bare variant needs an
  operator ruling on provisional thresholds or a parameter-free
  formulation).
- AUDIT: claim PASSES the one-sentence test; condition fails
  (unparameterized) — flagged as above.

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
- **Status:** **signal-live** (S-H7, bare variant). **Grading: BOTH
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
  (`_s_h8` — same prints as S-H2, DIFFERENT claim and grading).
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
- **Status:** **signal-live** (S-H8, either-direction mode; operator
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
- **Status:** **signal-live** (S-H9, event-derived).
- **Latest review:** keep-watching (2026-08-19, review R1 — first
  readout).
- AUDIT: PASS (depth and timestamp convention now pre-registered).

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
- **Status:** **signal-live** (S-H10).
- **Latest review:** deprioritize (2026-08-19, review R1 — at/below
  chance in both windows, n=293 backtest, per the register-36 criterion;
  evidence keeps accruing free; the T3b recipe-layer question and any
  status change are the operator's queue decision).
- AUDIT: PASS. First readouts at/below chance (18.8% backtest, 7.1%
  forward vs ~23%) — evidence, not verdict.

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
  as H7's standing adverse evidence (above). Replaced by S-H7 (claim
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
