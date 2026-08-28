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
