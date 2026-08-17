# Location Apparatus — documented mechanics (2026-08-18)
Purpose: the location census designs its cells against DOCUMENTED mechanics
(comparator incident = standing precedent for what inference costs).

## 1. location_ref (ledger/label columns) — THREE candidate families
`engine/pipeline.py:_location` (L36-56): nearest of
- session_high/session_low — running extremes of the CURRENT trading
  session, tracked per exec pipeline (`_track_session_extremes`, L26);
  reset at session_id change; prior session's extremes become
  prior_session_high/low.
- prior_session_high/prior_session_low — previous session's finals.
- signal_swing_level — `signal_ctx.nearest_level(px)`: the SIGNAL-TF
  ContextTracker's swing-level list (signal-only authority; ladder rungs'
  own levels are NOT consulted for location_ref).
Geometry: NO band — nearest-by-absolute-distance wins (L52); signed
dist_pts = px − ref and dist_signal_atr = dist/Signal-TF ATR are REPORTED,
not thresholded. Any "within ATR-band" cell is census-defined, not
apparatus-defined.

## 2. Swing-level registry (the signal_swing_level source)
`engine/context.py:_add_swing` (L83-102): swings confirm k bars late
(fractal, cross-session per the ruled contract); each confirmed swing price
enters `levels` with dedupe tol = level_identity_atr_frac × ATR (L98,
most-recent wins); retention = LAST 12 LEVELS (L102) — level lifetime is
displacement-based, not bar- or session-based; levels persist across
sessions until displaced. Repeated tests neither age nor strengthen a
level; an equal-price re-swing REPLACES it (re-register).

## 3. Signature registry — SEPARATE from location_ref (KEY DIVERGENCE FLAG)
`engine/context.py` L16-21, 204-212: registers ONLY
POTENTIAL_SELLING_CLIMAX / SPRING (extreme=low, dir +1) and
POTENTIAL_BUYING_CLIMAX / UPTHRUST (extreme=high, dir −1), at the QUALIFIED
label's wick-extreme anchor, expiring after signature_registry_max_age bars
(config; scenario override 20, default 30). Consumers: TEST-label
evaluation and hypothesis confirm logic ONLY.
**FLAG: location_ref NEVER consults the signature registry.** If the
reviewer's 2026-08-18 three-component account included signature-registry
levels as a location_ref family, that diverges from code. Consequence for
the scalp census: its "within ATR-band of a registered signature-registry
level" cell requires NEW (census-side) plumbing joining LABEL events to
registry state — replayable, but not an existing column.

## 4. TEST label — full conditions (`engine/testcrit.py`)
All five, vs a registry (or hypothesis-signature) extreme: (i) probe
reaches within test_proximity_atr × ATR of the extreme; (ii) holds it
(long: low > extreme); (iii) recovers (close_pos > 0.5 long-side);
(iv) rel_volume < 1.0; (v) rel_volume < test_vol_vs_signature (0.5) × the
signature bar's rel_volume. Same predicate, two anchors (classifier
registry / hypothesis signature).

## 5. Session-extreme reference rules
Running (not final) extremes; a print AT a fresh extreme yields dist 0.0 to
its own bar's price anchor (e.g. UPTHRUST high == session_high). Anchor
price for reversal signatures = wick extreme; other labels = close
(`backtest/ledger.py` signature_moment_rows; `engine/pipeline.py` px
selection).
