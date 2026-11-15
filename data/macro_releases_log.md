# Macro-calendar log (register 104)

The dated, attributed record behind `data/macro_releases.csv`: every
hand merge from staging, and every MANUAL VERIFICATION of a calendar
gap. STANDING RULE (register 104): unverified gaps EXCLUDE their days
from news cells (never counted as no-news); verified-empty windows
COUNT as no-news days — verification dated and attributed here.

The fetcher (`scripts/macro_fetch.py`) reads the provider's
`thisweek` feed ONLY (no `nextweek` variant exists), so past-week gaps
are UNRECOVERABLE from the feed — manual verification per the rule
above is the only backfill. The human merge gate (validated review
before live) stays as designed; the daily sync's verify step now warns
loudly when it lapses (`UNMERGED BACKLOG`) or when the live file has
no future-dated entry.

## Merges

- **2026-08-29 (operator, by hand)** — four rows appended from staging
  to the live schema (forecast/previous dropped): 2026-08-26T12:30Z
  USD High Core PCE Price Index m/m · 2026-08-26T12:30Z USD High
  Prelim GDP q/q · 2026-08-28T14:00Z USD High Fed Chairman Warsh
  Speaks · 2026-08-28T14:00Z USD High Prelim Benchmark Payrolls
  Revision. Staging's AUD High rows stay unmerged per the live file's
  USD/GBP convention.

## Verified-empty windows

- **2026-08-20 → 2026-08-22 — VERIFIED-EMPTY (operator, eyeballed
  ForexFactory 2026-08-29):** no High USD/GBP events; AUD employment
  only, out of scope. These days COUNT as no-news days in the
  event-clock census.

## Coverage

- Live file span: 2026-07-14 → the file's max date (stated in every
  census header). Days outside the span are excluded from news cells.

## 2026-09-16 — hand backfill of the fetch-lapse gap (staging only)
- Span: Aug 30 00:00Z → Sep 12 24:00Z (the two feed weeks missed while
  the daily fetch lapsed; the feed serves the current week only, so the
  gap was unrecoverable from it — probed lastweek/nextweek: both 404).
- Source: operator's full-tier board screenshots (2026-09-16). Board
  clock verified as UTC+1 by cross-checking its FOMC row (7:00pm) vs
  the feed's staged row (2026-09-16T18:00:00Z); all times converted -1h.
- 184 rows added across all tiers. Forecast/previous left blank
  (not consumed by the live merge).
- EXCLUDED, untimed (no utc_time can be honest): G20 Meetings Day 2/3/4
  (Aug 30/31, Sep 1); German Prelim CPI m/m All Day (Aug 31, Medium);
  GBP Bank Holiday (Aug 31); Omdia Total Vehicle Sales All Day (Sep 1);
  CAD + USD Bank Holidays (Sep 7); BRICS Summit Day 1 (Sep 12).
- EXCLUDED, anomalous: a postponed "ADP Weekly Employment Change" row
  displayed under Sep 9 with an "Aug 15th" date label — a mis-timed
  makeup print is worse for news windows than an absent one.
- EXCLUDED, validator conflict: ADP Non-Farm Employment Change
  (Sep 2, 12:15Z — a REAL release at its real time). The engine.macro
  NFP anchor matches any name containing "Non-Farm" and would reject
  it. FLAG TO OPERATOR: this predicate is a latent false-positive —
  the next monthly ADP print that lands inside a normally fetched week
  will fail macro_fetch's validation the same way; narrowing the anchor
  to the BLS print is an operator call (register-104 machinery), not
  bent here.
- KNOWN SEAM: Tue Sep 8 after 20:00Z (post the Consumer Credit row) was
  cut off in the source screenshots — any late-evening Sep 8 rows are
  still missing pending one more screenshot.

## 2026-09-16 — High-tier merge into live (operator-directed)
- 46 staged High rows merged (operator instruction: "merge all High
  events"); live now 71 rows spanning 2026-07-14 → 2026-09-18T05:30Z;
  validated (engine.macro); the stale gate CLEARS.
- Composition note, disclosed: these are the FIRST non-USD/GBP rows the
  live file has carried (new: EUR 3, CAD 9, NZD 5, AUD 4, JPY 3,
  All 1). Every prior merge was USD/GBP-only — ger40's native-currency
  news tags were structurally empty until now; census readers should
  expect the EUR footprint to begin 2026-08-28 (Jackson Hole "All"
  row) / 2026-09-10 (ECB set), not at the file's start.
- Medium/Low tiers remain staged-only, per the live file's standing
  High-only convention (now explicit here; previously implicit).
- The 12 rows past the live max are the already-fetched Sep 18-19
  Low/Medium tail (post-BOJ Friday + Saturday) — normal backlog under
  the High-only convention, not a lapse.
