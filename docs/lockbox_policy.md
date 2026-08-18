# Lockbox Policy — minting, spending, schedule, fences

**Adopted 2026-08-18 (register 30). One page; the register holds history.**

## Principle

Sealed data is the only currency that buys a verdict. A window is sealed by
**calendar declaration, never by content** — nobody looks first. A window is
spent by **exactly one walk-forward evaluation** of a pre-registered
champion; spent is spent, there is no second read.

## Minting (the standing schedule)

- **The first two weeks of each quarter are born sealed**, anchored
  **2026-09-01**: months **Sep / Dec / Mar / Jun**, days **1–14 inclusive,
  UTC** (`engine/store_loader.py: is_sealed`).
- Windows are declared **forward only**. A window that has already begun
  or passed cannot be declared sealed retroactively — data that has been
  readable is spent as evidence the moment it was readable.
- The schedule is code (`SEALED_SCHEDULE_START`, `SEALED_MONTHS`,
  `SEALED_DAYS`) — changing it is a registered ruling, forward-only.

## The legacy lockbox

The **Aug 4 → go-live (2026-08-14T15:04:09Z)** lockbox predates this
schedule, is governed by `lockbox.json` + the loader boundary, is
**unchanged** by this policy, and is **first to be spent** when round 1
crowns a champion.

## Spending

1. A champion exists (walk-forward, pre-registered recipe + thresholds).
2. The evaluation is pre-registered: definition hash, read criteria,
   pass/fail stated **before** the seal is broken.
3. One run via the loader's single logged override
   (`lockbox_evaluation=True`). The access line in the log is part of the
   evidence.
4. The result is registered whatever it says. The window is then spent —
   it becomes ordinary history, never a tuning set.

## Fences (all loader-enforced, all test-pinned)

- Default reads exclude the legacy lockbox (`load_frame` boundary filter).
- Explicitly targeting a sealed span is **refused**
  (`refuse_if_sealed`, `tests/test_sealed_windows.py`).
- **All forward readers skip sealed spans automatically** — Part C
  readouts, scoreboards, censuses. Skipped rows are counted in artifacts
  (`sealed_windows_skipped_events`), never reported.
- Live processes (paper/narrate) are NOT fenced: they stream through
  sealed windows as live consumers — the seal governs *reads for
  research*, not perception. Their outputs over sealed spans are ledger
  history like any other and become readable evidence only when the
  window is spent.
- Walk-forward training may consume neither sealed windows nor the
  forward zone.
