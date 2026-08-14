# Candidate Hypotheses — pre-registered, walk-forward entry only

**Status: CANDIDATE.** Not implemented. Not consuming data. Entry via
walk-forward only (standing ruling 1 pathway). **Append-only**; amendments
logged inline, never silent. Guard: no identifier below may appear in
`engine/` or `backtest/` before walk-forward (`tests/test_candidate_guard.py`).

Provenance: register items 8-10, ruling 5, ruling 1.

Two-layer form (adjudicated 2026-08-13, see amendment log): **FROZEN
ANATOMY** is fixed now and is what walk-forward tests — it cannot be
adjusted to fit results without a logged amendment. **FREE PARAMETERS** are
set at walk-forward under the same tuning protocol as H1-H5 thresholds,
never hand-picked against the candidates' own motivating window.

---

## H6 — Session-extreme rejection (registered 2026-08-13)

Motivation: 2026-08-13 06:56Z Asia-high rejection (v2 parking lot) +
item 9 (the rejection bar: 98th-pctile spread day-relative, 15th vs its
session-time bin).

### Frozen anatomy
- **Class:** REVERSAL · **Direction:** SHORT at a session-high rejection ·
  **Mirror:** LONG at a session-low rejection (exact sign-flip).
- **Spawn:** a rejection bar AT a session extreme (prior-session high/low or
  current-session extreme, within proximity of it): wide spread measured
  **day-relative** (trailing-window percentile, NOT session-time bins),
  adverse close (close_pos in the lower region for the short), large upper
  wick. **No volume condition anywhere** (volume-agnostic).
- **Confirm:** within the window, a bar that fails to re-approach the
  rejected extreme AND closes beyond the rejection bar's midpoint in the
  trade direction. Structural only — no volume condition.
- **Refute:** close beyond the rejected extreme.
- **Stop:** beyond the rejection bar's extreme (buffered, H1-H5 convention).
- **Gate:** standard reversal-class gate (RULES Sec 8), no exemptions.
- **Deliberate deviations from H1-H5 conventions:** (a) day-relative
  baselines instead of session-time bins — this IS the item-9 experiment;
  (b) volume-agnostic spawn and confirm — decouples the signature from the
  thin-session volume-rescaling question; (c) OPEN VARIANT QUESTION, to be
  A/B'd at walk-forward, not decided now: extended-hours spawns permitted
  (observational lineage) vs cash-only.

### Free parameters (schema; set at walk-forward)
day-relative spread percentile threshold · trailing window length for the
day-relative baseline · session-extreme proximity (k x ATR) · spawn
close_pos threshold · wick_frac minimum · confirm window (bars) · confirm
midpoint-reclaim margin · "fails to re-approach" distance (k x ATR) ·
stop buffer.

## H7 — Quiet-decline reversal at session extremes (registered 2026-08-13)

**The formal walk-forward entry for the tracked EFFORTLESS_DECLINE signal
(standing ruling 1).** Evidence to date (non-evidential): drift-adjusted
excess -19 bps at +20 bars, n=16, wrong-way vs label sign. **Identity with
the tracked signal is frozen:** the spawn signature IS the signal ruling 1
tracks; H7 enters walk-forward only if that signal survives to powered n,
and dies unregretted otherwise.

### Frozen anatomy
- **Class:** REVERSAL · **Direction:** LONG off quiet declines ·
  **Mirror:** SHORT off quiet advances (exact sign-flip).
- **Spawn:** an EFFORTLESS_DECLINE-class print (structural core: wide down
  bar, weak close, volume at/below normal — NOT high) at/near a session
  extreme (low side), segment recorded at spawn.
- **Confirm:** within the window, an up bar reclaiming the decline bar's
  midpoint. Structural; volume may be reported but is not a condition.
- **Refute — the falsifiable core, FROZEN VERBATIM: quiet ages,
  participation kills.** Further quiet declines (volume at/below normal)
  only AGE the hypothesis toward expiry — they never refute, however far
  price drifts, until the stop-side structural break. A decline on HIGH
  volume — participation confirming the down move — REFUTES immediately.
  This asymmetry is the hypothesis: if quiet weakness at an extreme is
  disguised accumulation, only participative selling falsifies it.
- **Additional refutation (structural):** close below the quiet-decline
  sequence low on any volume.
- **Stop:** below the quiet-decline sequence low (buffered).
- **Gate:** standard reversal-class gate, no exemptions.
- **Deviation from H1-H5 conventions:** none beyond the refutation
  asymmetry above; otherwise a conventional reversal spec.

### Free parameters (schema; set at walk-forward)
"quiet" volume ceiling (rel_volume) · "participative" volume floor
(rel_volume) · session-extreme proximity (k x ATR) · spawn close_pos and
spread thresholds · confirm window (bars) · midpoint-reclaim margin ·
sequence-low definition window · stop buffer · segment conditioning
(which segments spawn).

## H8 — Signature-Moment Expansion Bracket (registered 2026-08-13)

Motivating cases (observation-only; **no outcome computation on
post-boundary data**): the 2026-08-11 10:27Z and 15:47Z register
annotations — one failed directionally, one worked; both preceded movement.

### Frozen anatomy
- **Class: DIRECTION-AGNOSTIC (new class).** No mirror needed — the bracket
  is its own mirror.
- **Spawn:** an exec-TF (1min) reversal-signature print — UPTHRUST or
  SPRING **structural core**.
- **Entry:** OCO bracket — buy stop above the signature bar high + buffer,
  sell stop below the signature bar low − buffer. On fill, stop at the
  opposite bracket leg. The un-filled leg **cancels or reverses — variant
  question, A/B at walk-forward**, not decided now.
- **Refute/expiry:** neither leg fills within N bars.
- **Core falsifiable claim, FROZEN VERBATIM: signature-bar anatomy predicts
  imminent range expansion irrespective of direction.**
- **Cost warning (embedded at registration):** 1min-scale stops vs the
  measured spread — bracket width is small multiples of spread; the
  expansion study states spread in the same point units alongside every
  readout. H8 dies at walk-forward if expansion does not clear spread.
- **Evidence instrument:** the expansion event study
  (`uk100fut_expansion_study.json`) — forward realized range and
  excursions vs matched same-segment baselines, split by the ledger's
  location columns — is the evidence this candidate faces at walk-forward.

### Free parameters (schema; set at walk-forward)
bracket buffer · N (fill window, 1min bars) · R-targets · location
conditioning (none / within k x ATR of extreme — uses the ledger's
dist_signal_atr, no parallel location logic) · segment conditioning ·
double-fill handling.

## Amendment log

- 2026-08-13: file created; H6, H7 registered (intent-only sketches).
- 2026-08-13: H8 registered directly in two-layer form (post-amendment-1 convention); direction-agnostic class introduced; cost warning embedded at registration.
- 2026-08-13 — **AMENDMENT 1 (two-layer form).** Original registration was
  intent-only, on the implementer's rationale that pre-specifying detailed
  rules with the motivating window fresh would fit the design to the data
  that motivated it. Owner adjudication: the concern is valid but the
  remedy overcorrects — "a registration too vague to die isn't
  pre-registered." Resolution: FROZEN ANATOMY (structure, falsifiable
  cores, deviations) fixed now; FREE PARAMETERS (all numbers) deferred to
  walk-forward under the H1-H5 tuning protocol, never tuned against the
  motivating window. This log entry existing and being used is itself the
  mechanism working.
- 2026-08-13 — **META-HISTORY (recorded per owner instruction, alongside
  amendment 1):** first instance of implementer methodological pushback
  changing a ruling — the candidate-file design adjudication of 2026-08-13;
  dissent (intent-only, anecdote-fitting concern) -> counter ("too vague to
  die isn't pre-registered") -> synthesis (frozen anatomy / free
  parameters), outcome stronger than either original position.
