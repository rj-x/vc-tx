# Runbook — Post-Close Thin-Tape Probe (uk100fut)

**What this retires:** the finding-24-era caveat — the measured feed
contract (index 0 = forming bar; index ≥1 immutable; drop-last-post-sort
correct) was measured at Monday's **cash open only**; its validity on thin
tape is unverified. This probe is also the named instrument for the
Asia-session interpretability question (register 37: the 03:40–04:04Z
best-call cluster — regime edge vs thin-tape artifact vs unverified feed
regime).

**Total supervised time, honestly: ~50 minutes across one evening**
(two ~18-minute captures with a ~15-minute gap; you must be present to
start each capture on time — the capture itself needs no interaction).
Analysis is offline, unsupervised, any time after.

## The harness

The original measured-contract probe, reused as-is:
`scripts/feed_probe.py` — polls the raw minute endpoint every ~10s,
logs full raw pages UNTOUCHED to `logs/feed_probe/<date>_<HHMM>.jsonl`.
No store writes, no engine feed — capture only. It takes `--minutes` and
`--instr`.

## Steps (times UTC; a normal Mon–Thu evening)

1. **Capture A — pre-pause thin tape (start 20:35Z):**
   ```
   venv/bin/python scripts/feed_probe.py --minutes 18 --instr uk100fut
   ```
   Covers 20:35→20:53Z: post-close evening tape, sparse prints, ending
   near the measured pause onset (tape runs to 21:00Z exactly;
   register finding 24).
2. **Wait through the pause.** Bars cease at 21:00Z; nothing to capture.
3. **Capture B — reopen (start 22:02Z):**
   ```
   venv/bin/python scripts/feed_probe.py --minutes 18 --instr uk100fut
   ```
   Covers 22:02→22:20Z: the 22:05Z reopen (store-measured; Sunday reopen
   corroborates) plus the first thin minutes after.

## What each check verifies (run offline on both captures)

The analysis mirrors the original adjudication (register: measured feed
contract, six findings; second opinion procedure available):

- **Forming-bar semantics:** across polls inside one minute, the
  newest-stamped bar (served index 0) accrues volume/OHLC. THIN-TAPE
  QUESTION: when no trade prints for a minute, does index 0 hold a
  zero-volume forming bar, a stale bar, or nothing?
- **Settled-bar immutability:** every bar at index ≥1, once seen, is
  byte-identical in all later polls. THIN-TAPE QUESTION: do late prints
  ever REVISE an apparently settled thin bar (the class the cash-open
  capture could not exhibit)?
- **Settle timing:** delay from minute boundary to the settled bar's
  first appearance (cash-open measurement: ~10s; the live latency floor
  n=407 median 38s single-poll). THIN-TAPE QUESTION: does settle lag
  grow on empty minutes?
- **Fill density:** minutes with no bar at all vs zero-volume bars —
  which representation the feed uses for empty minutes, and whether the
  pause boundary (21:00Z) and reopen (22:05Z) are sharp or ragged.

## Expected vs anomalous

- EXPECTED: contract holds unchanged (0 = forming, ≥1 immutable); empty
  minutes simply absent from pages; sharp pause/reopen edges within a
  minute of 21:00Z/22:05Z; settle delay similar to cash-open.
- ANOMALOUS (each becomes a register finding, not a workaround): any
  settled-bar mutation; forming-bar index shifting on empty tape;
  reopen bars appearing with backdated timestamps; settle delays beyond
  the two-poll confirmation's protection (>~2 min).

## Archive + the register amendment this enables

Captures stay at `logs/feed_probe/` (committed — the probe capture is
evidence, same as 2026-08-17_0756.jsonl). Then amend the register's
measured-feed-contract entry:

> **Thin-tape amendment (date, capture files):** contract
> verified/violated in the post-close regime — [findings]. The
> finding-24-era "measured at cash open only" caveat is RETIRED /
> BOUNDED to [scope]. Asia-session scoreboard cells gain the note:
> "feed regime verified [date]" — or the measured anomaly, verbatim.

Also: the two-poll confirmation's latency reclaim decision (register:
retained pending this probe) becomes discussable either way.
