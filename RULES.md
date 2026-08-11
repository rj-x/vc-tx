# Engine Rules — Pseudocode Restatement (pre-code deliverable)

Restates Part 3–5 of `prompt.md` as executable logic, per Part 9 step 5.
Ambiguities are tagged `[A#]` inline and collected at the end with proposed
resolutions. Nothing here is code yet; this is the contract to agree on.

Conventions: `cfg.*` = config knob (all land in `config.yaml`). "bar" = the
just-closed Signal-TF bar unless stated. All features are trailing-relative and
session-time normalized per Part 2. Every hypothesis has an exact mirror;
pseudocode is written for the listed direction with `dir`-symmetric predicates.

---

## 1. Per-bar processing order (per timeframe, on bar N close)

```
1. label, feats = classify(bar_N, context_as_of_bar_N-1)   # never current-bar context
2. context.update(bar_N, label)          # swings (k-bar confirmation lag), phase,
                                         # levels, signature registry, volume trend,
                                         # impulse/reaction flag
3. hypotheses.step(bar_N, label, feats, context)   # test open, then spawn new
4. if any hypothesis graduated: emit signal        # broker acts >= bar N+1 open
```

HTF state visible to any LTF decision = last **closed** HTF bar, always.

## 2. Generic hypothesis lifecycle

```
class Hypothesis:
    spec            # H1..H5 or mirror
    dir             # LONG | SHORT
    signature_bar   # spawning bar (index, high, low, close, features)
    strength        # starts spec.base_strength
    age             # bars since signature bar

hypotheses.step(bar, label, feats, ctx):
    for h in open:                          # oldest first
        h.age += 1
        if h.refuted(bar, ctx):             # refute checked BEFORE confirm:
            close(h, REFUTED); continue     #   a bar satisfying both kills [conservative]
        if h.age > h.spec.expiry_bars:
            close(h, EXPIRED); continue
        h.strength += h.evidence_delta(bar, label, feats, ctx)      # [A10]
        if h.age in h.spec.confirm_window and h.confirm_event(bar, label, feats, ctx):
            if h.strength >= h.spec.min_strength_to_confirm:
                if mtf_gate_permits(h, context_tf.last_closed_state):
                    graduate(h)             # -> signal; exec refinement (Sec 9)
                else:
                    log(h, CONFIRMED_BUT_GATED)   # stays open, may re-confirm [A2]
    maybe_spawn(label, feats, ctx)          # dedupe: no second open hypothesis of
                                            # same spec+dir while one is open [A5]
    # every transition (spawn/confirm/refute/expire/gate-block/strength change) logged
```

## 3. H1 — Selling-Climax-and-Test (long, reversal). Mirror: [A1]

```
spawn on:
    label in {POTENTIAL_SELLING_CLIMAX, SPRING}
    and ctx.after_marked_decline            # >= cfg.move_atr_mult (2.0) x ATR, Part 3
    and (ctx.near_support                   # within cfg.level_atr_mult (0.5) x ATR
         or bar.low == lowest_low(trailing cfg.new_low_lookback bars))   # [A6]

confirm (window 1..5 bars):
    ( label == TEST
      and bar.low > signature.low                          # held
      and bar.low <= signature.low + cfg.test_proximity_atr x ATR   # actually probed [A4]
      and feats.close_pos > 0.5 )                          # recovered [A4]
    or ( label == VALIDATED_ADVANCE
         and bar.low within cfg.level_atr_mult x ATR of spawn level )   # "off the level" [A7]

refute:  bar.close < signature.low          # volume logged; refutes at ANY volume [A8]
stop:    signature.low - cfg.stop_buffer_ticks
strength boosters (+cfg.booster_increment each):
    context_tf at major support; context_tf phase transition
    MARKDOWN -> RANGING or -> POST_CLIMAX(selling) while open
```

## 4. H2 — Upthrust Reversal (short, reversal). Mirror: Spring Reversal (long)

```
spawn on:
    label == UPTHRUST
    and (ctx.after_rally or ctx.near_resistance or at_range_high(ctx))

confirm (window 1..4 bars):
    ( label == NO_DEMAND and bar arrives on a rally attempt:
          bar.close > prev_bar.close or bar within a >=2-bar up-move )   # [A9]
    or ( feats.direction == DOWN
         and bar.close < signature.midpoint          # (high+low)/2
         and feats.rel_volume > prev_bar.rel_volume )        # "expanding" [A9]

refute:  bar.close > signature.high
stop:    signature.high + cfg.stop_buffer_ticks
```

## 5. H3 — Absorption Breakout (with-trend). Mirror: sign-flipped

```
spawn on (checked each bar close):
    count of ABSORPTION bars within last cfg.h3.cluster_window (10) bars
        that sit within cfg.level_atr_mult x ATR of the SAME key level Lv
        >= cfg.h3.min_absorption_bars (2)
    and direction from context:
        Lv is resistance and signal_tf trend UP  -> LONG    # "after basing" [A11]
        Lv is support    and signal_tf trend DOWN -> SHORT
    zone = [min(low), max(high)] over the clustered absorption bars

confirm (window 1..cfg.h3.confirm_window (8) bars):        # window unspecified in spec [A12]
    breakout bar through Lv:
        feats.rel_spread >= cfg.wide_spread_pctile
        and close beyond Lv (LONG: close > Lv)
        and close_pos extreme (LONG: > 0.7)
        and feats.rel_volume >= cfg.h3.breakout_vol_mult

refute:
    wide-range bar (rel_spread wide) closing back through the FAR side of zone
    on rel_volume high                                      # [A13: far side vs re-entry]

stop:    far side of zone -+ cfg.stop_buffer_ticks
gate:    trend rule + RANGE_BREAK exception (Sec 8); tag H3_RANGE_BREAK
```

## 6. H4 — No-Supply Continuation (long, trend). Mirror: No-Demand (short)

```
spawn on:
    signal_tf phase == MARKUP with age >= cfg.h4.established_min_bars   # "established" [A14]
    and ctx.impulse_reaction == REACTION            # we are in a pullback
    and pullback volume declining:
        mean rel_volume over pullback bars < cfg.h4.pullback_vol_max (1.0)   # [A15]
    and label == NO_SUPPLY

confirm (window 1..cfg.h4.confirm_window (5) bars):        # unspecified in spec [A12]
    feats.direction == UP and feats.close_pos > 0.7
    and feats.rel_volume > pullback mean rel_volume        # "re-expanding" [A15]

refute:
    pullback volume expanding (rel_volume >= cfg.h4.expand_mult over >=1 bar)
    AND bar.close < last CONFIRMED higher-low swing before pullback start   # k-bar lag [A16]

stop:    min(low) of the pullback - cfg.stop_buffer_ticks
```

## 7. H5 — Buying-Climax Fade (short, reversal; cfg.h5.enabled = false)

```
spawn on:   label == POTENTIAL_BUYING_CLIMAX
confirm (1..5): label in {UPTHRUST, NO_DEMAND}
refute:     cfg.h5.refute_bars (3) consecutive closes above signature.close
            with rel_volume >= 1.0                          # "sustained" [A17]
gate (replaces Sec 8 entirely):
    |context_tf.close - context_tf.trend_mean| > cfg.h5.extension_atr x context_ATR
    where trend_mean = cfg.h5.ma_period (20) MA on Context TF   # [A17]
```

## 8. MTF gating (evaluated at graduation time, Context-TF = last closed bar)

```
mtf_gate_permits(h, ctxTF):
    if h.spec == H5: return h5_gate(ctxTF)                 # exempt, Sec 7

    if h.klass == TREND:                                   # H3, H4 + mirrors
        if ctxTF.phase == MARKUP    and h.dir == LONG:  return True
        if ctxTF.phase == MARKDOWN  and h.dir == SHORT: return True
        if h.spec == H3 and ctxTF.phase == RANGING
           and h.zone_level within cfg.level_atr_mult x ctxATR of a ctxTF range boundary
           and h.dir points OUT of the ctxTF range:
               h.tag = H3_RANGE_BREAK; return True
        return False

    if h.klass == REVERSAL:                                # H1, H2 + mirrors
        if ctxTF.phase == RANGING
           and price within cfg.level_atr_mult x ctxATF of the range extreme
               opposing h.dir (LONG: range low):  return True
        if ctxTF.phase == POST_CLIMAX
           and matches(ctxTF.post_climax_dir, h.dir):      # selling-climax -> LONG
               return True
        if not cfg.strict_mode
           and ctxTF.phase == opposing_trend(h.dir)        # e.g. MARKDOWN vs LONG
           and h.strength >= cfg.relaxed_min_strength:     # separate, higher bar
               return True
        return False
```

ATR in Context-level distance checks is the **Context TF's** ATR (the rule is
evaluated against Context-TF structure). Results reported strict on AND off.

## 9. Execution-TF refinement (after graduation; cfg.exec.enabled compared both ways)

```
watch up to cfg.exec.window (10) execution bars:
    trigger = with-direction exec bar with close_pos beyond threshold
              (LONG > 0.7, SHORT < 0.3)
    on trigger: enter at NEXT exec bar open
                stop = tighter_of(exec-TF local extreme, signature extreme)  # cfg choice
if no trigger in window:
    cfg.exec.fallback: enter at next exec bar open with Signal-TF stop | abandon
EOD entry embargo overrides: window reaches embargo -> abandon + log
```

---

## Ambiguities & proposed resolutions

**Needs your call (psychology / design):**

- **[A1] H1's mirror collides with H2 and H5.** A literal mirror of H1 spawns
  from `POTENTIAL_BUYING_CLIMAX` or `UPTHRUST` — but UPTHRUST already spawns H2,
  and the climax-fade short is H5 (disabled, special gate). Proposal: H1-mirror
  spawns from `POTENTIAL_BUYING_CLIMAX` **only** (climax-and-test short, normal
  reversal gating); UPTHRUST spawns only H2; H5 stays as specified (a faster
  fade without the test requirement, off by default). Alternative: drop
  H1-mirror entirely and let H2 + H5 cover the short side.
- **[A2] Gate-blocked confirmation.** When a hypothesis confirms but the
  Context-TF gate says no: kill it, or keep it open (it may re-confirm on a
  later bar after the Context phase flips, within its expiry)? Proposal: keep
  open, log `CONFIRMED_BUT_GATED` each time — the event-study layer records
  gated confirmations anyway, so both choices stay measurable.
- **[A3] Missing mirror labels.** Part 2 has `EFFORTLESS_ADVANCE` /
  `VALIDATED_ADVANCE` but no down-bar equivalents, which the mirrored
  hypotheses need. Proposal: add `EFFORTLESS_DECLINE` / `VALIDATED_DECLINE`
  (exact sign-flips).
- **[A4] What makes a TEST a test.** Proposal: the probe must come within
  `test_proximity_atr` (default 1.0) × ATR of the signature extreme, hold it
  (low > signature low), and recover (close_pos > 0.5) on rel_volume below
  baseline. Too strict / too loose?
- **[A5] Concurrency & ties.** Proposal: max one open hypothesis per
  spec+direction; opposite-direction hypotheses may coexist (they're competing
  narratives); if two graduate on the same bar, take the higher strength and
  log the conflict; ties → no trade.

**Proposed defaults (config-tunable; will adopt unless you object):**

- **[A6]** "near new lows" = lowest low of trailing `new_low_lookback` (50) bars.
- **[A7]** "off the level" = confirming bar's low within 0.5 × ATR of spawn level.
- **[A8]** H1 refutes on any close below signature low (volume logged, not required).
- **[A9]** "rally attempt" = up-close vs prior bar or ≥2-bar up-move; "expanding
  volume" = rel_volume above the previous bar's.
- **[A10]** Strength: base 1.0; +1 per supporting bar (additional signature-
  consistent label), −0.5 per contradicting bar (strong close against hypothesis
  direction w/o meeting refutation); confirm requires ≥ 1.0; relaxed-mode
  reversal gate requires ≥ 3.0.
- **[A11]** H3 "after basing": the cluster window itself is the base — no extra
  condition beyond ≥N absorption bars near the level (KISS for v1).
- **[A12]** Unspecified confirm windows: H3 = 8 bars from cluster completion,
  H4 = 5 bars from NO_SUPPLY bar.
- **[A13]** H3 refutation = wide high-volume bar closing beyond the far side of
  the absorption zone (not mere re-entry into it).
- **[A14]** "Established MARKUP" = phase age ≥ 10 Signal-TF bars.
- **[A15]** Pullback volume declining/re-expanding measured vs the pullback's own
  mean rel_volume (impulse/reaction flag delimits the pullback).
- **[A16]** H4 refutation uses the last *confirmed* (k-lag) higher-low swing;
  the confirmation lag is accepted — no peeking at unconfirmed swings.
- **[A17]** H5 "sustained advance" = 3 consecutive up closes at rel_volume ≥ 1.0;
  trend mean = 20-period MA on Context TF.
