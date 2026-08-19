# Reading Guide — Hypothesis Performance

**Read this before the table. Labels are recommendations only — none
actioned; status changes need a dated operator decision.**

## The two views
Page 1 (matrix): every live hypothesis x four contexts (backtest/forward,
whole-window and London). One cell = how far precision sits above or below
THAT CONTEXT'S OWN chance rate. Page 2 (cards): one card per hypothesis —
claim, full session x window grid, payoff, dated exhibits. Everything else
(other sessions' exhibits, horizon-mark payoffs) is in
signal_scoreboard.json.

## How to read a cell
`▲+9.4pp (26/80) net+123/med+1.2` means: precision 9.4 percentage points
ABOVE this context's chance rate (▲ = beyond +2pp; ▼ = beyond -2pp; · =
within the band), on 26 hits of 80 fires; summed signed excursion across
all fires +123 points with a median fire worth +1.2. `(°...)` = small-n
(fires<20 or episodes<10): dimmed, excluded from any future label
arithmetic — read as anecdote.

## The base-rate logic
The tape moves: in a typical context ~40-50% of bars are followed by a
qualifying move (>=1.5x 15M ATR within 60 min, drift-adjusted) in SOME
direction — so directional rows are chance-compared at roughly half that,
either-direction rows at the full rate, and EVERY context (each session,
each window) displays its own rates because they differ by session. A row
at chance has measured nothing.

## Payoff (directional rows only)
Per fire: the signed price change 60 minutes later (the registered
move-definition window), signed by the predicted direction. Total right =
sum of positive fires, wrong = sum of negative, net = the difference;
median per fire is the robust companion because CLUSTERED FIRES
DOUBLE-COUNT SHARED PRICE TRAVEL — a burst of 20 fires into one move books
that move 20 times in the totals, once in the median. Mid-price, no
spread, idealized — points here are not tradeable points.
Either-direction rows: n/a by construction (no predicted direction to
sign by).

## Session character (register 37 partition; native-tz, DST-proof)
- **asia** (Tokyo open -> London open): thin tape; the Asia best-call
  cluster is an OPEN QUESTION (regime edge vs thin-tape artifact vs
  unverified feed regime; thin-tape probe pending).
- **london** (London open -> NY open): the instrument's home session.
- **overlap** (NY open -> London close): highest participation; macro
  releases land here.
- **ny_only** (London close -> NY close): FTSE tape without its home
  market.
- **dead** (NY close -> Tokyo open): includes the daily feed pause.
London+overlap as the label-bearing window is a REGISTERED PROPOSAL,
unratified — criteria compute on whole windows.

## Small-n caveats
Forward is days old; several cells are single-digit. The small-n dimming
is registered convention (operator, 2026-08-19), not styling. Nothing in
these pages is validation — walk-forward and the lockbox remain the only
verdict machinery.
