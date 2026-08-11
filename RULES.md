# Engine Rules — Pseudocode Restatement v2

v1 ambiguities [A1]–[A17] were ruled on in `audit/engine_rulings.md`, which also
added second-pass and forensic-pass findings; all are folded in here and the
prompt has been amended to match. This document is the implementation contract.

Conventions: `cfg.*` = config knob (all land in `config.yaml`). "bar" = the
just-closed Signal-TF bar unless stated. All features trailing-relative and
session-time normalized. Every hypothesis has an exact mirror; pseudocode is
written for the listed direction with dir-symmetric predicates. **Mirror
strength boosters sign-flip with the hypothesis** (H1-mirror boosts on major
resistance and MARKUP → RANGING/POST_CLIMAX(buying) transitions).

## 0. Labels: structural core vs. context qualifier

Every label decomposes into a **structural core** (bar anatomy only: direction,
rel_spread, rel_volume, close_pos, wicks) and a **context qualifier** (phase,
location, prior move), applied at point of use:

- **Spawn conditions** use the fully qualified label.
- **Confirmation events** reference the **structural core only** (otherwise
  e.g. NO_DEMAND's "in a downtrend" qualifier is unsatisfiable during `MARKUP`,
  silently disabling H5's and part of H2's confirmations).

Label set includes the mirrors `EFFORTLESS_DECLINE` / `VALIDATED_DECLINE`
(exact sign-flips of their advance counterparts).

**TEST — authoritative criteria wherever used:** low-volume probe of a prior
signature extreme that (i) reaches within `cfg.test_proximity_atr` (1.0) × ATR
of the extreme, (ii) holds it (long case: low > signature low), (iii) recovers
(close_pos > 0.5), (iv) rel_volume below baseline, **and (v) rel_volume <
`cfg.test_vol_vs_signature` (0.5) × the signature bar's rel_volume** — a test
on climax-comparable volume is the battle resuming, not a test.

**Signature ownership rule:** each signature label spawns exactly one
hypothesis type — climax labels → H1/H1-mirror; `UPTHRUST`/`SPRING` →
H2/H2-mirror; no label spawns two specs. (H5 spawns from
`POTENTIAL_BUYING_CLIMAX` but is disabled by default and gate-exempt; when
enabled it is the sanctioned exception to single-ownership — H1-mirror and H5
share the spawn label, distinguished by their confirm paths.)

## 1. Per-bar processing order

On each bar close, per timeframe, strictly:

```
1. label, feats = classify(bar_N, context_as_of_bar_N-1)   # never current-bar context
2. context.update(bar_N, label)     # swings (k-lag), phase, levels,
                                    # signature registry, volume trend, impulse/reaction
3. hypotheses.step(...)             # Sec 2
4. graduation -> signal             # broker acts >= bar N+1 open
```

**Simultaneous multi-TF closes** (e.g. 1M/10M/H1 all closing at 10:00): process
timeframes in **descending order**, so the just-closed HTF bar is part of "last
closed HTF state" for the lower TFs at the same timestamp. Deterministic,
unit-tested — unspecified ordering makes the future-perturbation test flaky.
At any LTF bar, visible HTF context = the last **closed** HTF bar.

## 2. Hypothesis lifecycle

States: `OPEN → {CONFIRMED_PENDING_GATE, GRADUATED, REFUTED, EXPIRED}`;
`CONFIRMED_PENDING_GATE → {GRADUATED, REFUTED, EXPIRED}`.

```
hypotheses.step(bar, label_struct, label_qualified, feats, ctx):
    for h in open (oldest first):
        h.age += 1
        if h.refuted(bar, ctx):  close(h, REFUTED); continue
            # refute checked BEFORE confirm and BEFORE expiry (conservative);
            # consequence: an old bar meeting both reports REFUTED, not EXPIRED —
            # note in outcome stats
        if h.age > h.spec.expiry_bars:  close(h, EXPIRED); continue
            # expiry_bars DEFAULTS to top of confirm window; a separate config
            # value may widen it — the coupling is explicit so knobs can't
            # silently disagree
        h.strength += h.evidence_delta(bar, feats, ctx)
            # deliberate: the confirming bar's own delta applies BEFORE its
            # confirm check below
        if cfg.strength_floor_kill.enabled and h.strength < cfg.strength_floor:
            close(h, KILLED_WEAK)                          # default OFF

        if h.state == CONFIRMED_PENDING_GATE:
            if mtf_gate_permits(h, ctxTF): graduate(h)     # gate only; no re-confirm
            continue
        if h.age in h.spec.confirm_window and h.confirm_event(bar, label_struct, feats):
            if h.strength >= h.spec.min_strength_to_confirm:   # base 1.0, +1/-0.5,
                                                               # threshold 1.0 —
                                                               # near-no-op is deliberate
                if mtf_gate_permits(h, ctxTF): graduate(h)
                else: h.state = CONFIRMED_PENDING_GATE; log(h)

    maybe_spawn(label_qualified, feats, ctx)
        # dedupe: one open hypothesis per spec+direction; blocked spawns LOGGED
        # (measures stronger-signature-suppressed-by-weaker-open frequency);
        # opposite directions coexist; same-bar double graduation -> higher
        # strength wins, conflict logged, tie -> no trade
    # every transition logged: spawn / blocked-spawn / strength delta / confirm /
    # pending-gate / gate-block / graduate / refute / expire
```

## 3. H1 — Selling-Climax-and-Test (long, reversal)

Mirror: Buying-Climax-and-Test (short), from `POTENTIAL_BUYING_CLIMAX`.
`SPRING` no longer spawns H1 (ownership rule: it spawns H2-mirror).

```
spawn on:
    label_qualified == POTENTIAL_SELLING_CLIMAX
    and ctx.after_marked_decline                 # >= cfg.move_atr_mult (2.0) x ATR
    and (ctx.near_support                        # within cfg.level_atr_mult (0.5) x ATR
         or bar.low == lowest_low(trailing cfg.new_low_lookback (50) bars,
                                  INCLUSIVE of current bar))
    spawn_level = nearest support level, or signature.low when spawned
                  via the new-low condition

confirm (window 1..5 bars):
    TEST of signature (Sec 0 criteria, all five)
    or ( VALIDATED_ADVANCE (structural core)
         and bar.low within cfg.level_atr_mult x ATR of spawn_level )

refute:  bar.close < signature.low               # any volume; volume logged
stop:    signature.low - cfg.stop_buffer_ticks   # (2 ticks)
boosters (+cfg.booster_increment, sign-flipped in mirror):
    context_tf at major support; context_tf phase transition
    MARKDOWN -> RANGING or -> POST_CLIMAX(selling) while open
```

## 4. H2 — Upthrust Reversal (short, reversal)

Mirror: Spring Reversal (long), spawned by `SPRING` (sole owner of that label).

```
spawn on:
    label_qualified == UPTHRUST                  # qualifier: after rally / at
                                                 # resistance or range high
confirm (window 1..4 bars):
    ( NO_DEMAND (structural core: up bar, narrow spread, low volume)
      arriving on a rally attempt:
          bar.close > prev.close or bar is in a >=2-bar up-move )
    or ( direction == DOWN
         and bar.close < signature.midpoint
         and feats.rel_volume > prev.rel_volume )

refute:  bar.close > signature.high
stop:    signature.high + cfg.stop_buffer_ticks
```

## 5. H3 — Absorption Breakout (with-trend). Mirror: sign-flipped

```
spawn on (checked each bar close):
    >= cfg.h3.min_absorption_bars (2) ABSORPTION bars within last
       cfg.h3.cluster_window (10) bars, each within cfg.level_atr_mult x ATR
       of the SAME key level Lv
       # level identity carries cfg.level_identity_atr_frac tolerance —
       # swing levels drift; "same level" means within that fraction of ATR
    direction:
        signal_tf trending: Lv resistance + trend UP -> LONG;
                            Lv support + trend DOWN -> SHORT
        signal_tf RANGING:  direction = OUT of the range from the boundary
                            where the absorption sits (range high -> LONG,
                            range low -> SHORT)
    zone = [min(low), max(high)] over clustered absorption bars
    # ZONE GROWS: each further qualifying absorption bar before confirmation
    # extends the zone (and refreshes evidence); stop is computed at
    # GRADUATION on the final zone

confirm (window 1..cfg.h3.confirm_window (8) bars from latest cluster bar):
    breakout bar:
        rel_spread >= cfg.wide_spread_pctile
        and close beyond max(Lv, zone edge in trade direction)   # a "breakout"
                                                                 # inside the zone
                                                                 # never confirms
        and close_pos extreme (LONG > 0.7 / SHORT < 0.3)
        and rel_volume >= cfg.h3.breakout_vol_mult

refute:  wide-range bar closing beyond the FAR side of the zone on high volume
stop:    far side of final zone -+ cfg.stop_buffer_ticks (at graduation)
gate:    trend rule + RANGE_BREAK exception (Sec 8); tag H3_RANGE_BREAK
```

## 6. H4 — No-Supply Continuation (long, trend). Mirror: No-Demand (short)

```
spawn on:
    signal_tf phase == MARKUP, age >= cfg.h4.established_min_bars (10)
    and ctx.impulse_reaction == REACTION
    and pullback quiet: mean rel_volume over pullback bars
        < cfg.h4.pullback_vol_max (1.0)
        # pullback volume SLOPE logged for later evaluation of a stricter
        # bar-on-bar declining definition
    and label_qualified == NO_SUPPLY

confirm (window 1..cfg.h4.confirm_window (5) bars):
    direction == UP and close_pos > 0.7
    and rel_volume > pullback mean rel_volume

refute (state + trigger — NOT same-bar AND):
    expansion is pullback-level STATE: any pullback bar with
        rel_volume >= cfg.h4.expand_mult sets pullback.expanded = true
    trigger: bar.close < last CONFIRMED (k-lag) higher-low swing before
        pullback start, while pullback.expanded
    # the volume expansion and the structural break may arrive on
    # different bars — the realistic sequence

stop:    min(low) of pullback - cfg.stop_buffer_ticks (computed at GRADUATION —
         the pullback can deepen after spawn)
```

## 7. H5 — Buying-Climax Fade (short; cfg.h5.enabled = false)

```
spawn on:   label_qualified == POTENTIAL_BUYING_CLIMAX
confirm (1..5): UPTHRUST or NO_DEMAND — structural cores
                (their trend/location qualifiers are unsatisfiable this early
                after a climax; see Sec 0)
refute:     cfg.h5.refute_bars (3) consecutive closes above signature.close
            with rel_volume >= 1.0
gate (replaces Sec 8):
    |ctxTF.close - ctxTF.trend_mean| > cfg.h5.extension_atr x ctxTF_ATR
    trend_mean = cfg.h5.ma_period (20) MA on Context TF
```

## 8. MTF gating (graduation time; ctxTF = last closed Context-TF bar)

```
mtf_gate_permits(h, ctxTF):
    if h.spec == H5: return h5_gate(ctxTF)

    if h.klass == TREND:                              # H3, H4 + mirrors
        if ctxTF.phase == MARKUP   and h.dir == LONG:  return True
        if ctxTF.phase == MARKDOWN and h.dir == SHORT: return True
        if h.spec == H3 and ctxTF.phase == RANGING
           and h.zone_level within cfg.level_atr_mult x ctxTF_ATR
               of a ctxTF range boundary
           and h.dir points OUT of the ctxTF range:
               h.tag = H3_RANGE_BREAK; return True
        return False

    if h.klass == REVERSAL:                           # H1, H2 + mirrors
        # (a) phase AGREEMENT first — Signal-TF reversal in the direction of
        # the Context trend is a with-trend entry (upthrust fading a reaction
        # rally in a Context downtrend), expected highest-conviction setup.
        # This branch was MISSING from the v1 spec (forensic finding #1).
        if ctxTF.phase == MARKUP   and h.dir == LONG:
            h.tag = REV_WITH_TREND; return True
        if ctxTF.phase == MARKDOWN and h.dir == SHORT:
            h.tag = REV_WITH_TREND; return True
        # (b) range extreme
        if ctxTF.phase == RANGING
           and price within cfg.level_atr_mult x ctxTF_ATR of the range
               extreme opposing h.dir (LONG: range low): return True
        # (c) post-climax with matching direction
        if ctxTF.phase == POST_CLIMAX
           and matches(ctxTF.post_climax_dir, h.dir):  return True
        # (d) strict mode off: opposing phase, higher strength bar
        if not cfg.strict_mode
           and ctxTF.phase == opposing_trend(h.dir)
           and h.strength >= cfg.relaxed_min_strength (3.0): return True
        return False
```

Distances against Context-TF structure use the **Context TF's ATR**. Results
reported strict on AND off; `REV_WITH_TREND` and `H3_RANGE_BREAK` broken out.

## 9. Execution-TF refinement (cfg.exec.enabled; report with AND without)

```
on graduation:
    if a refinement is already pending: log the graduation, do NOT act
                                        # one pending refinement at a time
    watch up to cfg.exec.window (10) execution bars:
        each SIGNAL-TF close during the window: re-check parent refutation;
            if refuted -> cancel (REFINEMENT_CANCELLED_REFUTED)
        trigger = with-direction exec bar, close_pos beyond threshold
                  (LONG > 0.7 / SHORT < 0.3)
        on trigger: enter at NEXT exec bar open
            stop = tighter_of(exec-TF local extreme over the bars observed
                              in the refinement window (default lookback),
                              Signal-TF signature extreme)     # cfg choice
    no trigger in window:
        cfg.exec.fallback: next exec bar open w/ Signal-TF stop | abandon
    EOD entry embargo overrides everything: window reaches embargo ->
        abandon + log
```

## 10. Synthetic-scenario verification (before any backtest)

Hand-built bar sequences exercising every gate branch and lifecycle path,
narrative logs produced and reviewed against the psychology appendix before
real data is touched. Minimum set:

1. Upthrust during Context `MARKDOWN` → must graduate tagged `REV_WITH_TREND`.
2. Selling climax + TEST while gated, Context phase flips afterward → must
   graduate via `CONFIRMED_PENDING_GATE` without re-confirming.
3. H3 growing zone with a false "breakout" inside the zone → must NOT confirm;
   later true breakout beyond max(level, zone edge) → confirms.
4. H4 with volume expansion and structural break on different bars → must refute.
5. Refutation arriving during a pending execution refinement → must cancel
   (`REFINEMENT_CANCELLED_REFUTED`).

Plus: simultaneous multi-TF close ordering test (descending-TF rule, Sec 1).
