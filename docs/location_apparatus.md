# Location Apparatus — documented mechanics

**Status:** verified against code 2026-08-17 (every claim re-read from source, not carried from memory).
**Purpose:** the scalp location census (trial-log amendment, cycle d98d6f9) must design its cells against DOCUMENTED mechanics, not inferred ones — the presence-study comparator incident is the standing precedent for what inference costs.
**Scope:** what produces `location_ref` / `location_level` / `dist_pts` / `dist_signal_atr` on LABEL events; what the signature registry is and is not; TEST-label evaluation in full; swing/level mechanics; session-extreme rules.

---

## 1. `location_ref` — the emitting apparatus

`engine/pipeline.py:36-59` (`TFPipeline._location`). Candidates are exactly **three families** (up to five refs):

| Family | Refs | Source |
|---|---|---|
| Current-session extremes | `session_high`, `session_low` | `_track_session_extremes`, `pipeline.py:26-34` |
| Prior-session extremes | `prior_session_high`, `prior_session_low` | same tracker: the outgoing session's finals roll over at `session_id` change (`pipeline.py:28-31`) |
| Signal-TF swing level | `signal_swing_level` | `signal_ctx.nearest_level(px)` — the **Signal-TF** ContextTracker's `levels` list (`pipeline.py:46-48`, `context.py:262-267`) |

- **Winner:** nearest by absolute distance, `min |px − cand|` (`pipeline.py:52`). **No band, no tolerance** — some ref always wins if any candidate exists. `dist_pts = px − ref` (signed) and `dist_signal_atr = dist / Signal-TF ATR` are *reported*, never thresholded (`pipeline.py:53-59`). Any "within ATR-band" location class is census-defined arithmetic on these columns, not an apparatus concept.
- **When emitted:** only for **qualified** labels, only on the **exec pipe** (`signal_ctx is not None`, `pipeline.py:76-79`); session extremes are likewise tracked only on the exec pipe (`pipeline.py:65-66`).
- **Measurement anchor `px`** (`pipeline.py:77-78`): `UPTHRUST → bar.high`, `SPRING → bar.low`, **every other label (climaxes included) → bar.close**. (The registry stores climax wick extremes — §3 — but the *location measurement* for a climax print is taken from its close.)
- **Signal-only authority:** ladder rungs' own swing levels are never consulted; `_location` receives the Signal-TF context only.

## 2. Swing-level registry (the `signal_swing_level` source)

`engine/context.py`:

- **Confirmation:** fractal with `k = swing_k = 3` (config.yaml:27) bars each side; a swing at bar *i* confirms at bar *i+k* (`_confirm_swings`, `context.py:70-84`). Confirmation carries across the session boundary — ratified as spec, tagged `confirmed_across_gap` (register ruling 8; `context.py:78-84`).
- **Level entry:** every confirmed swing price enters `levels` after dedupe: existing levels within `level_identity_atr_frac (0.25) × ATR` are **removed and replaced** — most recent wins (`context.py:97-101`).
- **Retention:** `levels = levels[-12:]` (`context.py:102`) — lifetime is **displacement-based**, not bar-, age-, or session-based. A level persists across sessions until pushed out by the 13th newer level or absorbed by a near-identical newer swing. (The `swings` list itself is separately capped at 40, `context.py:94-95`, but `location_ref` reads only `levels`.)
- **Repeated tests:** touching a level neither strengthens, refreshes, nor ages it. An equal-price re-swing re-registers it (dedupe-replace), which resets its displacement position to newest.
- **`nearest_level(px)`** (`context.py:262-267`): unconditioned nearest — no side, no tolerance. (Contrast `_near_level`/`near_support`/`near_resistance`, `context.py:234-260`, which ARE side-conditioned and banded by `level_atr_mult × ATR` — those feed classifier/hypothesis location conditions, **not** `location_ref`.)

## 3. Signature registry — a SEPARATE apparatus (divergence flag)

`engine/context.py`:

- **Registration triggers** (`_REGISTRY_SPECS`, `context.py:16-21`; applied in `_update_registry`, `context.py:202-213`): exactly four qualified labels — `POTENTIAL_SELLING_CLIMAX` and `SPRING` register `bar.low` with dir +1; `POTENTIAL_BUYING_CLIMAX` and `UPTHRUST` register `bar.high` with dir −1. Entry = `{label, idx, extreme (wick), rel_volume, dir}`.
- **Expiry:** age-based — entries dropped once `idx − entry.idx > signature_registry_max_age = 30` bars (config.yaml:37; `context.py:211-213`). No price-displacement expiry; no cap on count within the age window.
- **Consumers:** TEST-label classification and each hypothesis's test-of-signature check — one predicate, two anchors (`engine/testcrit.py:1-4`; `hypotheses.py:124`). **Nothing else.**

> **Naming trap:** the lab's own snapshot code (`backtest/lab.py:47`) maps
> `signal_swing_level` to a ref-class it calls **"swing_registry"** — a
> plausible source for any "registry" component in a secondhand account.
> The swing-level list (§2) and the signature registry (this section) are
> different structures with different contents, lifetimes, and consumers.
>
> **⚑ KEY DIVERGENCE — `location_ref` never consults the signature registry.** `_location()` draws only from the three families in §1. If the reviewer's three-component account (given to the operator 2026-08-18) presented signature-registry levels as a `location_ref` component, that diverges from code. The account was not available in-session for verbatim comparison — if it instead named {session extremes, prior-session extremes, swing levels}, it matches the code exactly. Corrections welcome; this doc states what the code does.
>
> **Census consequence:** a "within ATR-band of a registered signature-registry level" cell has **no existing column**. It requires census-side plumbing joining each LABEL event to registry state as of that bar — replayable from logs/store with zero look-ahead, but it is *new derivation*, not a read-off.

## 4. TEST label — evaluation conditions in full

`engine/testcrit.py:7-26` (authoritative wherever used; RULES.md Sec 0). Written long-side (dir +1, testing a registered LOW), mirrored for short:

0. **Preconditions:** `feats.valid` and ATR available and > 0 — else no TEST regardless of geometry (`testcrit.py:11-12`).
1. **Reaches:** `bar.low ≤ extreme + test_proximity_atr (1.0) × ATR` — the bar actually probed the level (config.yaml:51).
2. **Holds:** `bar.low > extreme` — strict; touching or breaching the extreme fails.
3. **Recovers:** `close_pos > 0.5` (short side: < 0.5).
4. **Low volume (absolute):** `rel_volume < 1.0`.
5. **Low volume (relative):** `rel_volume < test_vol_vs_signature (0.5) × signature rel_volume` (config.yaml:52); requires the signature's rel_volume to be recorded and non-zero.

All five must hold. Two call sites, same predicate: classifier TEST vs any live registry entry; hypothesis test-of-signature vs the owning hypothesis's signature.

## 5. Session-extreme reference rules

`engine/pipeline.py:26-34`:

- Extremes are **running** (bar-by-bar max/min of high/low), not end-of-session finals — so `location_ref = session_high` at 10:00 refers to the high *so far*.
- On `session_id` change the tracker resets; the outgoing session's running extremes become `prior_session_high/low`. First session of a run has `prior_* = None` (candidates silently absent, `pipeline.py:49`).
- A print that *sets* a new session extreme can measure distance ≈ 0 to itself (e.g. an UPTHRUST whose `px = bar.high` just became `session_high` — tracker updates before `_location` is called, `pipeline.py:65-66` then `76-79`, so dist = 0.0 exactly).

## 6. Downstream columns

`backtest/ledger.py:21,100-127,161-162`: `signature_moment_rows` copies `location_ref`/`location_level`/`dist_pts`/`dist_signal_atr` verbatim off LABEL events; blank when absent. No re-derivation downstream — the pipeline emission (§1) is the single source.
