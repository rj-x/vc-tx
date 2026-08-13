# Candidate Hypotheses — Pre-Registered Backlog

**Status: CANDIDATE — not implemented, not consuming data, walk-forward entry only.**

These specs are pre-registered: written and dated BEFORE any evidence on them exists,
so they cannot be unconsciously sculpted to fit data seen later. They were motivated by
discretionary reads of the 2026-08-13 session (see register items 8–10 and ruling 5's
diagnostic scope). They enter the system, if ever, through the same pipeline as H1–H5:
pseudocode restatement, adversarial review, synthetic scenarios, walk-forward evaluation,
ablation, per-hypothesis reporting. Until then the engine must not reference them.

Registered: 2026-08-13.

---

## H6 (candidate) — Session-Extreme Rejection — reversal class

**Motivating case:** uk100fut 2026-08-13 06:45Z bar — probe of the Asia high (10870.6),
13.0-pt spread, close_pos 0.25, upper wick 60%, close back through the bar midpoint.
Structurally an upthrust; invisible to the current system because (a) it printed pre-cash
and (b) its spread is 98th percentile day-relative but 15th percentile vs its own
session-time bin (register item 9).

**Deliberate deviations from the H1–H5 conventions (this is what makes it a new
hypothesis, not a re-tune):**
- **Day-relative baselines:** spread/volume thresholds measured against the current
  session's trailing bars, not session-time bins. (Adjudication of day-relative vs
  time-of-day-relative detection is register item 9; H6 is the day-relative playbook
  given trade anatomy.)
- **Volume-agnostic spawn:** no minimum volume condition. Location + rejection anatomy
  carry the hypothesis; volume features are logged for later analysis, not gated on.
- **Extended-hours spawn permitted (observational question):** the motivating case is
  pre-open. Whether H6 may spawn outside cash (with confirmation/entry inside cash only)
  is a walk-forward design variant to be tested both ways, not assumed.

**Spawn:** a bar that (a) trades within k × ATR of a registered session extreme
(prior-day high/low, overnight/Asia high/low, current-session high/low once established),
(b) probes beyond or to it (bar extreme beyond/at the level), (c) closes back through its
own midpoint against the probe direction (probe up → close_pos < 0.5; mirror for probes
down), (d) with day-relative spread ≥ a configurable percentile of the current session's
trailing bars. The spawning bar is the signature bar. Direction: against the probe.

**Confirm:** within 1–4 bars, a close beyond the signature bar's midpoint in the trade
direction on any bar that does not violate the refutation; OR a structural
EFFORTLESS/VALIDATED bar in the trade direction.

**Refute:** close beyond the probed extreme in the probe direction (the "rejection" was
absorbed and the level broke).

**Stop:** beyond the signature bar's probe extreme ± tick buffer.

**Gate relationship:** reversal class, standard reversal gating (phase agreement /
RANGING at extremes / POST_CLIMAX match / strict-off branch), REV_WITH_TREND tagging
applies. Mirror is exact (probe of session low → long).

---

## H7 (candidate) — Quiet-Decline Reversal at a Session Extreme — reversal class (long)

**Motivating case:** uk100fut 2026-08-13 07:15Z bar — EFFORTLESS_DECLINE printed into the
session low (10808.6) on below-baseline volume, immediately preceding a ~40-pt recovery.
Also consistent with the tracked EFFORTLESS_DECLINE excess signal (−19 bps at n=16,
non-evidential) and with three qualitative observations to date (register ruling 5 notes).

**Relationship to the tracked signal:** H7 IS the tracked EFFORTLESS_DECLINE signal given
location and trade anatomy. Standing ruling 1 already requires that signal to enter only
through walk-forward as a candidate hypothesis — H7 is that entry, specified in advance.

**Spawn:** one or more EFFORTLESS_DECLINE-class bars (structural core: wide spread down,
close_pos ≤ 0.2, volume BELOW baseline — the defining quiet-ness condition) whose lows
sit within k × ATR of a registered session extreme (session low, prior-day low,
overnight low). Signature bar = the bar making the lowest low of the cluster. Direction:
long. (Baseline convention — session-time vs day-relative — to be tested as a variant
under item 9; default session-time for consistency with the tracked signal's definition.)

**Confirm:** within 1–5 bars, an up bar with close_pos > 0.7 closing above the signature
bar's midpoint; volume re-expansion strengthens but is not required (deliberate: the
motivating phenomenon is demand absence, not demand climax).

**Refute:** close below the signature bar low on EXPANDING volume (quiet continuation
lower ages the hypothesis; participative continuation kills it — this asymmetry is the
hypothesis's core claim and must be tested as-written before being "fixed").

**Stop:** below signature bar low ± tick buffer.

**Gate relationship:** reversal class, standard reversal gating, REV_WITH_TREND tagging
applies. Mirror: Quiet-Rally Fade at a session high (EFFORTLESS_ADVANCE into a session
extreme on below-baseline volume, short) — exact sign-flip.

---

## Rules of the backlog

1. Candidates are append-only and dated. Amendments before evaluation are permitted but
   must be logged as amendments, never silent edits — the point is receipts.
2. Nothing here may influence thresholds, gating, tracked-signal handling, or any
   evidential artifact before walk-forward.
3. New discretionary observations that survive a week's reflection get drafted into this
   file in full anatomy, same rules. Impressions without anatomy don't enter.
4. At walk-forward, candidates compete identically with H1–H5 revisions: pseudocode →
   adversarial review → synthetic scenarios → evaluation → ablation → per-hypothesis
   reporting. Dying on paper here is a success mode.
