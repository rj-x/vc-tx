# Engine Rulings — Response to Pseudocode Restatement v1

For Claude Code. `prompt.md` has been amended with everything below and remains the
single source of truth; this document maps each ruling to your `[A#]` tags and adds
findings from two further review passes. **Deliverable: pseudocode restatement v2 of
the affected sections only** (lifecycle, H1–H5, gating, refinement), reflecting these
rulings, before any engine code.

## Rulings on your ambiguities

- **[A1] Accepted, extended symmetrically — you missed the same collision on the long
  side.** Your Sec 4 gives H2's mirror as "Spring Reversal (long)", but H1 also spawned
  from `SPRING`. New signature ownership rule (now in prompt): **climax labels spawn
  H1/H1-mirror; `UPTHRUST`/`SPRING` spawn H2/H2-mirror; H5 unchanged (disabled).**
  `SPRING` is removed from H1's spawn set. Every label owns exactly one spec.
- **[A2] Accepted, strengthened into a state:** `CONFIRMED_PENDING_GATE`. Once
  confirmed while gated, the hypothesis does NOT need to re-confirm; each subsequent
  Signal-TF close re-evaluates the gate only (refutation stays active, expiry applies);
  graduate on gate-open. Your version required a second confirm event, which for
  one-shot events like `TEST` almost never recurs — the pathway was dead.
- **[A3] Accepted:** add `EFFORTLESS_DECLINE` / `VALIDATED_DECLINE` as exact sign-flips.
- **[A4] Accepted plus one condition:** test volume must ALSO be < `cfg.test_vol_vs_signature`
  (default 0.5) × the signature bar's rel_volume. A test on climax-comparable volume is
  the battle resuming. These inline criteria are authoritative wherever TEST is used.
- **[A5] Accepted in full**, plus: log blocked spawns (measure how often a stronger
  signature is suppressed by a weaker open hypothesis).
- **[A6]–[A17] Accepted as proposed**, with: [A10] the base-1.0/threshold-1.0 near-no-op
  is deliberate — document it; the confirming bar's evidence delta applying before its
  own confirm check is deliberate — document it; optional strength floor kill, default
  off. [A15] accepted as a "quiet pullback" test; log the pullback volume slope so the
  stricter bar-on-bar definition can be evaluated later. Typo: `ctxATF` (Sec 8).
  `expiry_bars` = top of the confirm window unless separately configured — make the
  coupling explicit so the knobs can't silently disagree.

## Second-pass findings (fix in v2)

1. **Label-context entanglement (general rule, now in prompt Part 2):** every label
   splits into a *structural core* (bar anatomy only) and a *context qualifier* applied
   at point of use. Spawns use the qualified form; **confirmation events reference the
   structural core only.** Otherwise `NO_DEMAND`'s "in a downtrend" qualifier is
   unsatisfiable during `MARKUP`, silently disabling H5's and part of H2's confirmations.
2. **Refinement invalidation:** if the parent hypothesis's refutation fires on any
   Signal-TF close during a pending refinement window → cancel
   (`REFINEMENT_CANCELLED_REFUTED`). One pending refinement at a time; further
   graduations logged, not acted on.
3. **H3 direction when Signal TF is `RANGING`** (your Sec 5 rule referenced a trend that
   doesn't exist there): direction = out of the range from the boundary where the
   absorption sits (range high → LONG, range low → SHORT).
4. Minor: H1 `VALIDATED_ADVANCE` spawn level = signature bar low when spawned via the
   new-low condition; H4 stop computed at graduation (pullback can deepen);
   `lowest_low(trailing N)` must include the current bar.

## Forensic-pass findings (fix in v2)

1. **CRITICAL — gating bug (ours, in the spec you faithfully restated):** the reversal
   gate had no phase-AGREEMENT branch, so an upthrust during Context `MARKDOWN` — the
   framework's canonical with-trend reversal — returned False through every branch.
   Fixed in prompt: reversal class graduates first on Context-phase agreement
   (`MARKUP`→LONG, `MARKDOWN`→SHORT), tagged `REV_WITH_TREND`, then the existing
   `RANGING` / `POST_CLIMAX` / strict-off branches.
2. **Simultaneous multi-TF closes:** at a shared timestamp (1M/10M/H1 all closing at
   10:00), process TFs in **descending order** so the just-closed HTF bar is part of
   "last closed HTF state" for lower TFs. Add a unit test; unspecified ordering makes
   the future-perturbation test flaky.
3. **H3 zone must grow:** the zone extends with each further qualifying absorption bar
   until confirmation; breakout requires close beyond **max(level, zone edge in trade
   direction)**; stop computed at graduation on the final zone.
4. **H4 refutation timing:** volume expansion is pullback-level *state* (any pullback
   bar ≥ expand_mult); the structural-break close is the *trigger*. Same-bar AND misses
   the realistic sequence.
5. Minor: H1 boosters sign-flip in the mirror; level identity needs an ATR-fraction
   tolerance (swing levels drift); exec-TF "local extreme" lookback = bars observed in
   the refinement window (default); refute-before-expiry precedence means old bars
   report REFUTED not EXPIRED — fine, note it in outcome stats.

## New pre-backtest deliverable

**Synthetic-scenario verification** (prompt Part 9): hand-built bar sequences
exercising every gate branch and lifecycle path — minimum set: upthrust in Context
`MARKDOWN` (must graduate `REV_WITH_TREND`); climax + TEST while gated, phase flips
after (must graduate via `CONFIRMED_PENDING_GATE`); H3 growing zone with a false
breakout inside the zone (must not confirm); H4 expansion and break on different bars
(must refute); refutation during pending refinement (must cancel). Produce narrative
logs for each; they will be reviewed before real data is touched.
