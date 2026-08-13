# Engine Rules — Pseudocode Restatement v3.1

v2 was adversarially reviewed (findings R1–R6 + implementation traps, all
ratified); prompt.md Parts 4–5 were patched for the spec-level items. v3
applied every fix and added the per-hypothesis evidence enumeration (Sec 2b).
v3.1 (confirmation-pass rulings): route_signal guard split so
`REFINEMENT_CANCELLED_OPPOSED` is reachable; evidence precedence pinned;
H2 rally-attempt clause pinned; `ENTRY_FALLBACK` tag; all four v3 open items
ratified. **This is the final pre-code contract — engine code follows.**

**Scope:** this document covers the hypothesis lifecycle, H1–H5 + mirrors,
MTF gating, and execution refinement (prompt Parts 3–5). **Deferred, not
covered here:** Part 7 trade mechanics beyond entry (exits, sizing, EOD,
intrabar resolution) and the alignment-score formula (Part 5 coordinator
duty) — each gets its own section when the coordinator is designed. Where an
entry-path rule is needed for correctness (in-position guard, direct entry)
it is restated inline.

Conventions: `cfg.*` = config knob; **all knobs and defaults are in Sec 11**.
"bar" = the just-closed Signal-TF bar unless stated. Every hypothesis has an
exact mirror; predicates are dir-symmetric ("beyond X in the trade direction"
means above for LONG, below for SHORT). Mirror strength boosters sign-flip
with the hypothesis.

## 0. Labels: structural core vs. context qualifier

Every label decomposes into a **structural core** (bar anatomy only:
direction, rel_spread, rel_volume, close_pos, wicks) and a **context
qualifier** (phase, location, prior move), applied at point of use:

- **Spawn conditions** use the fully qualified label.
- **Confirmation and evidence events** reference the **structural core**,
  plus geometry relative to the hypothesis's own signature/zone (never
  phase/location qualifiers — those make confirmations unreachable, e.g.
  NO_DEMAND's "in a downtrend" during post-climax `MARKUP`).

Label set includes mirrors `EFFORTLESS_DECLINE` / `VALIDATED_DECLINE`.

**TEST — authoritative criteria wherever used** (written for a long test of a
low; mirror flips): low-volume probe of a prior signature extreme that
(i) reaches within `cfg.test_proximity_atr` × ATR of the extreme,
(ii) holds it (low > signature low), (iii) recovers (close_pos > 0.5),
(iv) rel_volume below baseline, and (v) rel_volume <
`cfg.test_vol_vs_signature` × the signature bar's rel_volume.
The classifier's registry-based `TEST` label (diagnostics/event-study) and
the hypothesis-internal test-of-signature check use these same criteria,
anchored to the registry entry and the hypothesis's own signature
respectively — one predicate, two anchors, kept in one function.

**Signature ownership rule:** climax labels → H1/H1-mirror;
`UPTHRUST`/`SPRING` → H2/H2-mirror; no label spawns two specs.
(`POTENTIAL_BUYING_CLIMAX` additionally spawns H5 when `cfg.h5.enabled` —
the sanctioned exception; the two are distinguished by confirm paths.)

## 1. Per-bar processing order (per timeframe, on bar N close)

```
1. label, feats = classify(bar_N, context_as_of_bar_N-1)
2. context.update(bar_N, label)
3. hypotheses.step(...)                      # Sec 2
4. signal routing / entry                    # broker acts >= bar N+1 open
```

**Simultaneous multi-TF closes:** process timeframes in **descending order**
(the just-closed HTF bar becomes "last closed HTF state" for lower TFs at the
same timestamp). Deterministic; unit-tested. At any LTF bar, visible HTF
context = last **closed** HTF bar.

## 2. Hypothesis lifecycle

Active states: `OPEN`, `CONFIRMED_PENDING_GATE` (CPG).
Terminal states: `GRADUATED`, `REFUTED`, `EXPIRED`, `KILLED_WEAK`.
Legal transitions: `OPEN → {CPG, GRADUATED, REFUTED, EXPIRED, KILLED_WEAK}`;
`CPG → {GRADUATED, REFUTED, EXPIRED}` (no strength changes in CPG, so no
`KILLED_WEAK` from CPG).

The step is **two-phase**: evaluate everything first, then act once —
same-bar conflicts are resolved by strength, never by iteration order.

```
hypotheses.step(bar, label_struct, label_qualified, feats, ctx):

    # ---- PHASE A: evaluate every active hypothesis; no actions yet ----
    candidates = []
    for h in active:                        # 'active' is the collection;
                                            # OPEN is a state — distinct names
        if h.refuted(bar, ctx):             # refutation first, both states;
            close(h, REFUTED); continue     # an old bar meeting refute+expiry
                                            # reports REFUTED (note in stats)
        if h.state == CPG:
            h.pending_age += 1
            if h.pending_age > cfg.pending_gate_max_bars:
                close(h, EXPIRED); continue          # logged as pending-window expiry
            if mtf_gate_permits(h, ctxTF):
                candidates.append(h)                 # gate only — no re-confirm,
            continue                                 # no delta, no floor (prompt P5)

        # state == OPEN
        h.age += 1                          # H3: age measured from window_anchor
                                            # (re-anchoring, Sec 5)
        if h.age > h.spec.expiry_bars:      # default: top of confirm window
            close(h, EXPIRED); continue
        h.strength += evidence_delta(h, bar, label_struct, feats)   # Sec 2b;
                                            # confirming bar's own delta applies
                                            # before its confirm check (deliberate)
        if cfg.strength_floor.enabled and h.strength < cfg.strength_floor.value:
            close(h, KILLED_WEAK); continue          # default OFF
        if h.age in h.spec.confirm_window and h.confirm_event(bar, label_struct, feats):
            if h.strength < h.spec.min_strength_to_confirm:
                diagnostics.CONFIRM_UNDERSTRENGTH += 1; log(h)   # log-and-lose (v1
                continue                                          # ruling; revisit w/ data)
            if mtf_gate_permits(h, ctxTF): candidates.append(h)
            else: h.state = CPG; h.pending_age = 0; log(h)

    # ---- PHASE B: resolve same-bar graduation conflicts by strength ----
    for h in candidates: graduate(h)        # all graduate; each emits a signal
    if candidates:
        acted = argmax_strength(candidates) # tie -> act on NONE; conflict logged
        route_signal(acted)                 # PHASE C
        for h in candidates - {acted}: log(h, SIGNAL_UNACTED_CONFLICT)
    # INTERPRETATION (for confirmation pass): conflict losers still GRADUATE —
    # their signals are emitted-but-unacted, reusing Part 7's signals-while-
    # in-position machinery — rather than being deferred to a later bar.

    # ---- PHASE C: act once ----
    route_signal(h):
        if position_open:                               # any direction
            log(h, SIGNAL_UNACTED_IN_POSITION); return
        if entry_pending:                               # refinement or scheduled entry
            if h.dir opposes pending.dir:
                cancel_pending(REFINEMENT_CANCELLED_OPPOSED)
                # guard split (v3.1): v3 returned on entry_pending before the
                # opposed path could fire — it was unreachable. Now the
                # opposing signal falls through and acts below.
            else:
                log(h, SIGNAL_UNACTED_PENDING); return  # same direction
        if cfg.exec.enabled: start_refinement(h)        # Sec 9
        else: schedule_entry(next Signal-TF bar open,
                             stop = signature extreme -+ cfg.stop_buffer_ticks,
                             tag = ENTRY_DIRECT)        # direct path, prompt P7;
                                                        # EOD embargo applies

    maybe_spawn(label_qualified, feats, ctx)
        # dedupe: one active hypothesis per spec+direction; blocked spawns
        # logged. Opposite directions coexist.
```

## 2b. Evidence semantics (per prompt Part 4 general definition)

`evidence_delta` per bar ∈ {`+cfg.support_delta`, `-cfg.contra_delta`, 0}.
Evidence predicates use structural cores + hypothesis-relative geometry only
(Sec 0). No accrual in CPG. **Precedence (v3.1 pin):** supporting and
contradicting are evaluated independently (a supporting event is
label-based, contradicting is close_pos-based — one bar can qualify as
both); when both fire, **supporting wins** — apply `+support_delta` only,
and log both flags on the bar.

**Contradicting (uniform across hypotheses, from the prompt):** the bar's
close_pos is beyond `cfg.evidence_contra_close_pos` **against** the
hypothesis direction (LONG: close_pos < 0.3; SHORT: > 0.7) and the bar does
not meet the refutation condition. Delta `-cfg.contra_delta`.

**Supporting (enumerated per hypothesis; canonical events from the prompt,
proposed additions flagged):**

| Spec | Supporting events (+cfg.support_delta each) |
|---|---|
| H1 | A bar meeting the full TEST criteria against the signature extreme (an additional probe that holds); an ABSORPTION core whose extreme sits within `cfg.test_proximity_atr` × ATR of the signature extreme (accumulation at the low — ratified v3.1). |
| H2 | NO_DEMAND core arriving on a rally attempt (same predicate as confirm branch 1 — inside the confirm window this event confirms rather than merely supports; as a supporting event it matters only pre-window edge cases and diagnostics). |
| H3 | Each further qualifying ABSORPTION bar (the same event that extends the zone — "refreshes evidence" is exactly this +delta). |
| H4 | Each further NO_SUPPLY core bar during the pullback; a TEST-criteria probe of the pullback low (ratified v3.1). |
| H5 | No distinct supporting events — its natural evidence bars (UPTHRUST / NO_DEMAND cores) are its confirm events; base strength alone meets the default threshold. Flagged: if H5 is ever enabled with a raised threshold, a supporting set must be defined first. |

**Boosters (H1 + mirror only, per spec):** edge-triggered — applied **once**
per condition per hypothesis, on the first bar the condition becomes true:
Context TF at major support (major = a Context-TF key level: Context swing
or range boundary), `+cfg.booster_increment`; Context-TF phase transition
MARKDOWN → RANGING or → POST_CLIMAX(selling) while the hypothesis is active,
`+cfg.booster_increment`. Sign-flipped in the mirror. Boosters apply in
state OPEN only.

## 3. H1 — Selling-Climax-and-Test (long, reversal)

Mirror: Buying-Climax-and-Test (short) from `POTENTIAL_BUYING_CLIMAX`.

```
spawn on:
    label_qualified == POTENTIAL_SELLING_CLIMAX
    and ctx.after_marked_decline                 # >= cfg.move_atr_mult x ATR
    and (ctx.near_support                        # within cfg.level_atr_mult x ATR
         or bar.low == lowest_low(trailing cfg.new_low_lookback bars, inclusive))
    spawn_level = the support level if ctx.near_support holds,
                  else signature.low             # precedence: level first

confirm (window 1..5):
    TEST of signature (Sec 0, all five criteria)
    or ( VALIDATED_ADVANCE structural core
         and bar.low within cfg.level_atr_mult x ATR of spawn_level )

refute:  bar.close < signature.low               # any volume; volume logged
stop:    signature.low - cfg.stop_buffer_ticks
boosters: Sec 2b
```

## 4. H2 — Upthrust Reversal (short, reversal)

Mirror: Spring Reversal (long), spawned by `SPRING` (sole owner).

```
spawn on:  label_qualified == UPTHRUST
confirm (window 1..4):
    ( NO_DEMAND structural core on a rally attempt.
      Rally attempt (v3.1 pin; up-close means close > open):
          bar.close > prev.close
          OR (bar is an up-close AND prev bar is an up-close) )
    or ( direction == DOWN
         and bar.close < signature.midpoint              # (high+low)/2
         and feats.rel_volume > prev.rel_volume )
refute:  bar.close > signature.high
stop:    signature.high + cfg.stop_buffer_ticks
```

## 5. H3 — Absorption Breakout (with-trend). Mirror: sign-flipped

```
spawn on (checked each bar close):
    >= cfg.h3.min_absorption_bars ABSORPTION bars within last
       cfg.h3.cluster_window bars, each within cfg.level_atr_mult x ATR of the
       SAME key level Lv (each bar tested with the trailing ATR as of that
       bar's close; level identity tolerance cfg.level_identity_atr_frac)
    direction:
        signal_tf trending: Lv resistance + trend UP -> LONG;
                            Lv support + trend DOWN -> SHORT
        signal_tf RANGING:  OUT of the range from the boundary where the
                            absorption sits (range high -> LONG, low -> SHORT)
    zone = [min(low), max(high)] over clustered absorption bars
    window_anchor = latest qualifying cluster bar

RE-ANCHORING: each further qualifying ABSORPTION bar (before confirmation)
    extends the zone, adds evidence (Sec 2b), and RESETS window_anchor to
    itself; h.age is measured from window_anchor, so confirm window AND
    expiry re-anchor together. Total lifetime capped at
    cfg.h3.max_total_bars from spawn (prevents immortality via repeated
    extension).

confirm (window 1..cfg.h3.confirm_window from window_anchor):
    breakout bar:
        rel_spread >= cfg.wide_spread_pctile
        and close beyond the OUTERMOST of (Lv, zone edge) in the trade
            direction (LONG: above max(Lv, zone high); SHORT: below
            min(Lv, zone low)) — a "breakout" inside the zone never confirms
        and close_pos extreme in the trade direction (LONG > 0.7 / SHORT < 0.3)
        and rel_volume >= cfg.h3.breakout_vol_mult

refute:  wide-range bar closing beyond the FAR side of the zone (opposite
         the trade direction) on high volume
stop:    far side of final zone -+ cfg.stop_buffer_ticks, computed at GRADUATION
gate:    trend rule + RANGE_BREAK exception (Sec 8; gate's zone reference =
         the key level Lv, not a zone edge); tag H3_RANGE_BREAK
```

## 6. H4 — No-Supply Continuation (long, trend). Mirror: No-Demand (short)

Pullback boundaries (pinned): the pullback **starts** at the bar where the
impulse/reaction flag transitions to REACTION; it is ongoing at every
evaluation below. "Pullback bars" at bar N = bars from pullback start through
N−1 — **the evaluation bar is always excluded** from pullback aggregates.

```
spawn on:
    signal_tf phase == MARKUP, age >= cfg.h4.established_min_bars
    and ctx.impulse_reaction == REACTION
    and pullback quiet: mean rel_volume over pullback bars < cfg.h4.pullback_vol_max
        # pullback volume SLOPE logged for later evaluation
    and label_qualified == NO_SUPPLY

confirm (window 1..cfg.h4.confirm_window):
    direction == UP and close_pos > 0.7
    and rel_volume > mean rel_volume over pullback bars   # excludes this bar

refute (state + trigger, may arrive on different bars):
    state:   any pullback bar with rel_volume >= cfg.h4.expand_mult
             sets pullback.expanded (sticky)
    trigger: bar.close < last CONFIRMED (k-lag) higher-low swing before
             pullback start, while pullback.expanded

stop:  min(low) over pullback start..graduation bar, - cfg.stop_buffer_ticks
       (computed at GRADUATION — the pullback can deepen after spawn)
```

## 7. H5 — Buying-Climax Fade (short; cfg.h5.enabled = false)

```
spawn on:   label_qualified == POTENTIAL_BUYING_CLIMAX
confirm (1..5): UPTHRUST or NO_DEMAND structural core
refute:     cfg.h5.refute_bars consecutive Signal-TF closes strictly above
            signature.close, EACH with rel_volume >= 1.0; any non-qualifying
            bar resets the count
gate (replaces Sec 8; SIGNED in the fade direction):
    ctxTF.close - trend_mean > cfg.h5.extension_atr x ctxTF_ATR
        # buying-climax fade: extension must be ABOVE the mean;
        # sign-flips in the mirror (selling-climax fade: below)
    trend_mean = cfg.h5.ma_period MA on Context TF
```

## 8. MTF gating (ctxTF = last closed Context-TF bar; "price" = the current
Signal-TF bar's close)

```
mtf_gate_permits(h, ctxTF):
    if h.spec == H5: return h5_gate(ctxTF)                # Sec 7, signed

    if h.klass == TREND:                                  # H3, H4 + mirrors
        if ctxTF.phase == MARKUP   and h.dir == LONG:  return True
        if ctxTF.phase == MARKDOWN and h.dir == SHORT: return True
        if h.spec == H3 and ctxTF.phase == RANGING
           and h.Lv within cfg.level_atr_mult x ctxTF_ATR of a ctxTF range boundary
           and h.dir points OUT of the ctxTF range:
               h.tag = H3_RANGE_BREAK; return True
        return False

    if h.klass == REVERSAL:                               # H1, H2 + mirrors
        if ctxTF.phase == MARKUP   and h.dir == LONG:
            h.tag = REV_WITH_TREND; return True           # agreement branch
        if ctxTF.phase == MARKDOWN and h.dir == SHORT:
            h.tag = REV_WITH_TREND; return True
        if ctxTF.phase == RANGING
           and price within cfg.level_atr_mult x ctxTF_ATR of the range
               extreme opposing h.dir (LONG: range low):  return True
        if ctxTF.phase == POST_CLIMAX
           and matches(ctxTF.post_climax_dir, h.dir):     return True
        if not cfg.strict_mode
           and ctxTF.phase == opposing_trend(h.dir)
           and h.strength >= cfg.relaxed_min_strength:    return True
        return False
```

Context-structure distances use the Context TF's ATR. Report strict on AND
off; `REV_WITH_TREND` and `H3_RANGE_BREAK` broken out separately.

## 9. Execution-TF refinement (cfg.exec.enabled; report with AND without)

```
start_refinement(h):
    # precondition: reached only via route_signal (Sec 2 Phase C), which has
    # already resolved position/pending state — including cancelling an
    # opposed pending entry (REFINEMENT_CANCELLED_OPPOSED) so this signal
    # can act. No guard here; opposed-cancellation lives in route_signal.
    # No position is open, no-reverse-and-flip is not violated; all
    # cancellations logged (oscillation frequency is measurable).

    window = the next cfg.exec.window execution bars, where window bar 1 is
             the FIRST exec bar closing STRICTLY AFTER the graduation
             timestamp (the exec bar closing AT that timestamp — already
             processed under Sec 1 descending order — is NOT in the window)

    on each Signal-TF close during the window:
        if h.refuted: cancel (REFINEMENT_CANCELLED_REFUTED)

    trigger: with-direction exec bar, close_pos beyond threshold
             (LONG > 0.7 / SHORT < 0.3)
    on trigger: enter at the NEXT exec bar's open
        if that open falls at/inside the EOD entry embargo: abandon + log
        stop = tighter_of(exec-TF local extreme over bars observed in the
                          window (default lookback), signature extreme)   # cfg
    no trigger in window:
        cfg.exec.fallback = enter (next exec open, Signal-TF stop,
                                   tag ENTRY_FALLBACK — reported separately)
                            | abandon
    window reaches the embargo without trigger: abandon + log
```

## 10. Synthetic-scenario verification (before any backtest)

Hand-built bar sequences, narrative logs reviewed against the psychology
appendix before real data. Minimum set:

1. Upthrust during Context `MARKDOWN` → graduates tagged `REV_WITH_TREND`.
2. Selling climax + TEST while gated; Context phase flips **on the second
   Context-TF close afterward** → graduates via `CONFIRMED_PENDING_GATE`,
   exercising the pending window beyond the old confirm-window expiry.
3. H3 growing zone; false "breakout" inside the zone → must NOT confirm;
   later close beyond outermost(Lv, zone edge) → confirms. Include a zone
   extension late enough that the old spawn-anchored expiry would have
   killed the hypothesis (exercises re-anchoring).
4. H4 volume expansion and structural break on different bars → refutes.
5. Refutation during a pending refinement → `REFINEMENT_CANCELLED_REFUTED`.
6. Opposite-direction graduation during a pending refinement →
   `REFINEMENT_CANCELLED_OPPOSED`, and the opposing signal then acts,
   starting its own refinement — proving the cancel-then-act path end to
   end (v3.1: this path was unreachable in v3's guard).
7. Simultaneous multi-TF close → descending-order processing verified
   (HTF bar closing at timestamp T is visible to LTF decisions at T).

## 11. Config defaults (single source; config.yaml mirrors this table)

| Knob | Default | Used in |
|---|---|---|
| `test_proximity_atr` | 1.0 | Sec 0 TEST (i); H1 evidence proposal |
| `test_vol_vs_signature` | 0.5 | Sec 0 TEST (v) |
| `move_atr_mult` | 2.0 | H1 spawn ("marked decline") |
| `level_atr_mult` | 0.5 | all "at/near level" tests |
| `level_identity_atr_frac` | 0.25 | H3 same-level tolerance |
| `new_low_lookback` | 50 bars | H1 spawn |
| `stop_buffer_ticks` | 2 | all stops |
| `base_strength` | 1.0 | spawn |
| `support_delta` / `contra_delta` | +1.0 / 0.5 | Sec 2b |
| `evidence_contra_close_pos` | 0.3 / 0.7 | Sec 2b contradicting |
| `min_strength_to_confirm` | 1.0 | near-no-op w/ base 1.0 — deliberate |
| `booster_increment` | 1.0 | H1 boosters, edge-triggered |
| `strength_floor.enabled` / `.value` | false / −1.0 | Sec 2 (never in CPG) |
| `pending_gate_max_bars` | 2 × Context/Signal TF ratio | CPG window |
| `strict_mode` | false | Sec 8(d); report both |
| `relaxed_min_strength` | 3.0 | Sec 8(d) |
| `wide_spread_pctile` | 80th | H3 confirm; labels |
| `h1..h2 confirm windows` | 1..5 / 1..4 | fixed per spec |
| `expiry_bars` | top of confirm window | explicit coupling; H3 re-anchored |
| `h3.min_absorption_bars` | 2 | spawn |
| `h3.cluster_window` | 10 | spawn |
| `h3.confirm_window` | 8 (from window_anchor) | confirm |
| `h3.max_total_bars` | 24 from spawn | re-anchoring lifetime cap |
| `h3.breakout_vol_mult` | 1.5 | confirm |
| `h4.established_min_bars` | 10 | spawn |
| `h4.pullback_vol_max` | 1.0 | spawn |
| `h4.confirm_window` | 5 | confirm |
| `h4.expand_mult` | 1.5 | refute state |
| `h5.enabled` | false | Sec 7 |
| `h5.refute_bars` | 3 | refute |
| `h5.extension_atr` | 2.0 | gate (signed) |
| `h5.ma_period` | 20 | gate |
| `exec.enabled` | true (report both) | Sec 9 |
| `exec.window` | 10 exec bars | Sec 9 |
| `exec.fallback` | enter (tag `ENTRY_FALLBACK`) | Sec 9 |
| `exec.stop_choice` | tighter_of | Sec 9 |

**v3 open items — all ratified at the v3.1 confirmation pass:**
(1) conflict losers graduate-with-unacted-signal; (2) both evidence
additions accepted (H5 supporting-set placeholder stands: define before
enabling H5 with a raised threshold); (3) `h3.max_total_bars = 24`;
(4) `exec.fallback = enter` given the `ENTRY_FALLBACK` tag.
