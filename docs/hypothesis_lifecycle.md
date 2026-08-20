# Hypothesis Lifecycle — idea to paper, one page

**Adopted 2026-08-18. Each stage states its verdict-power — what a result
there is allowed to decide. Nothing skips stages; nothing borrows a later
stage's authority.**

```
idea → register → lab → shadow-live → weekly reads → walk-forward → lockbox → paper
```

## 1. Idea
Anything: operator observation, session exhibit, census surprise, reviewer
prior. **Verdict-power: none.** An idea decides nothing, including its own
priority.

## 2. Register
`audit/candidate_hypotheses.md`, two-layer form: **frozen anatomy**
(mechanism, falsifiable as written) / **free parameters** (fit later, in
walk-forward only). Priors and citations recorded (trial log). Candidate
guard: identifiers of unbuilt hypotheses (H6–H9…) may not appear in
`engine/` or `backtest/` (`tests/test_candidate_guard.py`).
**Verdict-power: none — registration is memory, not evidence.**

## 3. Lab
Exploratory censuses over the **working set only**, pre-registered in the
trial log before compute, EXPLORATORY-stamped, engine hash embedded
(rule 25a). **Verdict-power: negative only** — a census can KILL a
candidate or gate the next census/build; it can never validate, tune, or
touch the engine. Multiple-comparisons record: the trial log, consulted at
round 1.

## 4. Signal-live
(Pure-signals doctrine, register 34 — supersedes the original shadow-trade
framing; register 31's trade layer is deferred-not-deleted.) The
hypothesis is a bare firing condition in the signal module; the scoreboard
grades precision/coverage/earliness/payoff against each context's own
chance rate (class-conditioned where the condition selects a volatility
class, register 47). The recipe layer harvests the same fires separately,
observationally. New registrations go signal-live on ratification of a
mechanical condition. **Verdict-power: none — texture and prioritization
input, never promotion evidence.**

## 5. Weekly reads
Campaign + forward dossiers (Part C when adopted): scoreboard tables,
migration/expansion/label studies, all counts-adjacent-to-points, all
stamped observational. **Verdict-power: none.** A beautiful weekly read
changes what gets *worked on*, never what gets *believed*.

## 6. Walk-forward
The only tuning venue. Training on the working set; free parameters fitted
inside the walk; recipe + thresholds pre-registered before evaluation.
**Verdict-power: THE verdict machinery** — crowns a round champion, kills
the rest. Consumes neither sealed windows nor the forward zone.

## 7. Lockbox
One pre-registered evaluation of the champion on a sealed window
(docs/lockbox_policy.md); the window is spent whatever the result says.
**Verdict-power: confirm/refute the champion — the only stage that can.**

## 8. Paper
The survivor trades on paper in the forward zone; the ledger is the honest
record (holes and all). **Verdict-power: deployment evidence** — live
frictions, latency, coverage; feeds the go/no-go on real capital, never a
retroactive re-tune.
