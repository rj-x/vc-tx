# Data Layer Notes

Findings from the step-zero audit (2026-08-10) of the Finsa pipeline, plus standing
operational rules. The engine reads only from `clean_finsa/` (built by
`scripts/store.py build` from the raw store in `data/`). Path constants live in
`scripts/paths.py` and resolve to the project root, so the commands work from any
working directory.

## Feed semantics (verified empirically)

- **Endpoint:** `https://charts.finsatechnology.com/data/{tf}/{instr}/{side}?l={n}`
  with `tf ∈ minute|quarter|hour|day` (`quarter` = 15 min, confirmed),
  `side ∈ mid|bid|ask`. Cap is **10,000 bars per response** (not 5,000);
  pagination exists via an undocumented `m` end-anchor parameter, which
  `collect.py` uses to walk history backwards.
- **Timestamps:** true UTC, **open-time labeled** (1M bars rebuild 15M bars exactly
  under `label='left'`). DST verified correct: the FTSE cash-open volume surge sits
  at 08:00 London in both GMT and BST months.
- **Bid/ask/mid:** ask ≥ bid always; mid is exactly (bid+ask)/2.
- **Retention floors (rolling):** minute ~30 days · quarter ~12 months ·
  hour ~24 months · day = full history (2012+; EURUSD 1999).
  **Data older than a floor is gone for good — see sync cadence below.**
- **Provider trading day:** ~22:00 → ~21:00 UTC; native `day` bars use that
  boundary (labeled midnight of the close's calendar day), **not** the cash close.
  Hybrid D1 context seeding must account for this.

## Volume: real futures volume (the step-zero hard gate — answered)

- The futures feed (`uk100fut`) reports **raw traded contract counts**: quantum 1,
  median ~46/min, daily totals ≈ ICE FTSE 100 future ADV (~55–70k), day feed ≈ sum
  of minute volume, 0% zero-volume bars intraday.
- The cash-CFD feed (`uk100`) carries **the same series scaled ×4** (all values
  divisible by 4; per-day ratio ≈ 4.0–4.14). So even the older cash history is
  futures-volume-grade, not tick volume.
- **Daily-feed volume starts late:** `uk100` daily volume is zero before
  **2020-08-24**; `uk100fut` daily volume is zero before **2024-01-17**. D1
  volume features must respect these start dates (cash has the deeper D1 volume).

## Instrument registry

| Slug | Finsa ID | What it is | Role |
|---|---|---|---|
| `uk100fut` | 70152 | UK 100 Rolling Future | **Primary development instrument** |
| `uk100` | 16645 | UK 100 cash CFD | Cross-check; deeper D1 volume (2020+) |
| `uk100sep26` | 72516 | UK 100 Future, Sep-2026 outright | Roll verification (see below) |
| `ger40` | 17068 | DAX cash CFD | Portability stage 1 |
| `ustech100` | 20190 | NASDAQ 100 cash CFD | Portability stage 2 |
| `us30` / `us500` | 17322 / 67995 | Dow / S&P cash CFDs | Collected, unused by strategy |
| `gold` / `goldvar` | 68924 / 72302 | Gold (fixed / variable spread) | Collected, unused by strategy |
| `eurusd` | 16635 | EURUSD | Collected, unused by strategy |

History depth for `uk100fut` (as of 2026-08-11): 1d from 2021-07-05 · 1h from
2024-08-11 · 15m from 2025-08-10 · 1M from 2026-07-12 (~26 sessions). The
backtestable Signal/Execution window equals accumulated 1M history.

## The rolling future is a RAW SPLICE — no back-adjustment

Verified against cash: at each quarterly roll (~17th–18th of Mar/Jun/Sep/Dec,
landing ~20:00–22:00 UTC, i.e. overnight) the rolling series steps **20–50 pts**
in a single hour unexplained by cash moves (e.g. 2024-09-18 22:00: 59.1 pt jump
vs 5.3 pt cash move). Consequences for the engine:

- Roll gaps must **never** register as price/volume signatures.
- Levels, baselines, and context spanning a roll need back-adjustment at load
  time (or roll-window masking) — config choice per the spec.
- Roll dates are detectable mechanically: basis-step vs the cash series.

Spread costs: `uk100fut` ≈ 1.3 pts in cash hours vs 0.8 on the cash CFD (the
outright `uk100sep26` is quoted wider, ≈ 4.0). Cost model uses measured
per-bar spreads either way.

## Dated-contract lifecycle — WATCH ITEM for ~2026-09-18

`uk100sep26` (ID 72516) appears to be a **contract-specific ID**: its history
starts exactly 2026-06-11 (its platform listing) on every timeframe, even where
retention would allow more. It expires ~**Fri 2026-09-18** (third Friday).
Two scenarios:

- **A (expected):** the feed goes quiet after expiry. The store becomes a clean
  archive of one contract. A new market (e.g. "UK 100 - Future (Oct)" or "(Dec)")
  appears with a **new ID** → add it as a new slug (`uk100dec26`, …) and start
  syncing before the roll so both outrights straddle it.
- **B (dangerous):** the provider recycles ID 72516 for the next contract. Tell:
  **72516 keeps producing new bars after ~Sep 18.** If so, freeze the Sep archive
  at expiry and treat post-expiry bars as a separate series — the collector's
  union-merge would otherwise silently splice two contracts into one file.

In the week after expiry: check which scenario occurred, and grab the next
contract's ID from the platform (the number in the chart data URL). Having old
and new outrights live across the roll lets us measure exactly when and how the
rolling series (70152) hops contracts.

## Operational rules

1. **Sync at least every ~3 weeks** (ideally daily/weekly) or 1M history is
   permanently lost to the ~30-day retention floor:
   `venv/bin/python scripts/collect.py sync --instr all`
   then `scripts/store.py build --instr all && scripts/store.py verify`.
2. Naming: contract-dated slugs carry month+year (`uk100sep26`), so future
   contracts stay unambiguous.
3. `store.py build --instr <subset>` merges into `_report.json` (fixed
   2026-08-11; it previously clobbered other instruments' entries).
4. Known data quirks: 2 malformed `uk100` daily bid/ask bars (clamped and counted
   by the store); US/gold cash sessions are hardcoded in London hours and are off
   by one hour during the ~2–3 week US/UK DST misalignment windows — fix in
   `store.py` (compute in `America/New_York`) before the NASDAQ portability
   stage; `data/rates_*.csv` are daily interest rates from other work, not part
   of this pipeline.
5. Every report must state the volume type used (real futures volume vs ×4-scaled
   futures volume vs unknown) and the usable 1M date range per instrument.
