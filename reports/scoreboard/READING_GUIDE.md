# Reading Guide — Hypothesis Performance Table

**One page. Read before the table. Labels are recommendations only —
none actioned; status changes need a dated operator decision.**

## What each column means
- **fires** — times the bare firing condition triggered. A hypothesis is
  only its firing condition (pure-signals doctrine); no trade logic exists
  here.
- **precision** — of those fires, how many were followed within 60 minutes
  by a qualifying move (>= 1.5x the 15-minute ATR, drift-adjusted) in the
  predicted direction. *Either-direction* rows count a move either way.
- **coverage** — of all qualifying moves in the window, how many had this
  signal fire in the 60 minutes before the move began. Precision asks "when
  it speaks, is it right?"; coverage asks "how much does it see?".
- **median pts remaining** — at the earliest covering fire, how many points
  of the move were still ahead. The earliness metric. (A
  minutes-before-trend-flip column existed briefly and was retired — it
  measured time to the next unrelated flip, not earliness.)
- **best call / worst false alarm** — dated single exhibits: the covered
  move with most points remaining, and the miss with the worst adverse
  drift. Anecdotes by construction; never generalize from them.
- **union coverage** — episodes preceded by ANY live signal vs none: how
  much of the tape the whole board sees at all.

## The base-rate logic
Roughly 44-48% of bars are followed by a qualifying move in SOME direction
within the hour — the tape moves a lot. So: directional precision only
means something against ~half that (~22-24%); either-direction precision
only against the full base rate. A row AT its base rate has measured
nothing. The base rate is printed per window and the table's numbers mean
nothing without it.

## Session character (register 37 partition; boundaries in native
exchange timezones, DST-proof)
- **asia** (Tokyo open -> London open): thin tape; the Asia best-call
  cluster (03:40-04:04Z) is an OPEN QUESTION — regime edge vs thin-tape
  artifact vs unverified feed regime (thin-tape probe pending).
- **london** (London open -> NY open): the instrument's home session.
- **overlap** (NY open -> London close): highest participation; macro
  releases (12:30/13:30Z class) land here.
- **ny_only** (London close -> NY close): FTSE tape without its home
  market.
- **dead** (NY close -> Tokyo open): includes the daily feed pause;
  expect near-empty rows.
London+overlap as the label-bearing (tradeable) window is a REGISTERED
PROPOSAL, unratified — criteria compute on whole windows until the
operator ratifies session scoping.

## Small-n caveats
Forward is a few sessions old; single-digit fire counts dominate several
cells. n sits beside every number deliberately: a 50% precision on 4 fires
is two lucky bars, not a signal. Backtest n>=100 rows are the only ones
where the chance comparison has teeth yet. Nothing in this table is
validation — the walk-forward and the lockbox remain the only verdict
machinery.
