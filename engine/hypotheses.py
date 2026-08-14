"""Hypothesis specs and lifecycle manager — RULES.md Secs 2, 2b, 3-7.

Directions: +1 LONG, -1 SHORT. Each listed spec is written direction-neutral
via `d = h.dir`; the mirror is the same spec instantiated with the opposite
direction (RULES: exact mirrors, sign-flipped predicates and boosters).
"""

from .testcrit import test_criteria
from .classifier import structural_cores

LONG, SHORT = 1, -1
OPEN, CPG = "OPEN", "CONFIRMED_PENDING_GATE"
TERMINAL = ("GRADUATED", "REFUTED", "EXPIRED", "KILLED_WEAK")


class Hypothesis:
    def __init__(self, spec, direction, bar, feats, ctx, cfg):
        self.id = None                    # assigned by the manager at spawn
                                          # (per-manager sequence: two engine
                                          # instances must be fully independent
                                          # — perturbation-test determinism)
        self.spec = spec                  # 'H1'..'H5'
        self.dir = direction
        self.state = OPEN
        self.age = 0
        self.pending_age = 0
        self.strength = cfg.hypotheses.base_strength
        self.tag = None
        self.spawn_idx = ctx.idx
        self.sig_idx = ctx.idx
        self.sig_low = bar.low
        self.sig_high = bar.high
        self.sig_close = bar.close
        self.sig_mid = (bar.high + bar.low) / 2
        self.sig_rel_volume = feats.rel_volume
        self.boosters_applied = set()
        self.prev_ctx_tf_phase = None     # for H1 transition booster
        self.refute_count = 0             # H5
        self.confirm_branch = None        # which confirm branch fired
        # spec-specific, set by spawners:
        self.spawn_level = None           # H1
        self.zone_lo = self.zone_hi = None  # H3
        self.level = None                 # H3 Lv
        self.window_anchor = ctx.idx      # H3 re-anchoring
        self.pullback = None              # H4 (ref to ctx.pullback dict)
        self.prior_structural_level = None  # H4 last confirmed HL/LH before pullback

    @property
    def sig_extreme(self):
        """The signature extreme the trade is anchored to (stop side)."""
        return self.sig_low if self.dir == LONG else self.sig_high

    def describe(self):
        return {"id": self.id, "spec": self.spec, "dir": self.dir,
                "state": self.state, "age": self.age, "strength": self.strength,
                "tag": self.tag, "confirm_branch": self.confirm_branch,
                "sig_idx": self.sig_idx, "sig_extreme": self.sig_extreme,
                "spawn_segment": getattr(self, "spawn_segment", "cash")}


# --------------------------------------------------------------------------
# helpers

def _pullback_stats(pb, ctx_idx, direction=LONG):
    """(mean rel_volume, pullback extreme) over pullback bars EXCLUDING the
    current evaluation bar (RULES Sec 6 pin). Extreme is the min low for the
    long spec / max high for the short mirror."""
    if pb is None:
        return None, None
    rel = list(pb["rel_vols"])
    exts = list(pb["lows"] if direction == LONG else pb["highs"])
    if pb.get("last_idx") == ctx_idx:
        rel = rel[:-1] if rel else rel
        exts = exts[:-1] if exts else exts
    mean = sum(rel) / len(rel) if rel else None
    if not exts:
        return mean, None
    return mean, (min(exts) if direction == LONG else max(exts))


def _rally_attempt(bar, prev_bar, d):
    """RULES Sec 4 pin (direction-neutral): move against hypothesis dir.
    d=SHORT -> rally attempt (up); d=LONG (spring mirror) -> dip attempt."""
    if prev_bar is None:
        return False
    if d == SHORT:
        return (bar.close > prev_bar.close
                or (bar.close > bar.open and prev_bar.close > prev_bar.open))
    return (bar.close < prev_bar.close
            or (bar.close < bar.open and prev_bar.close < prev_bar.open))


# --------------------------------------------------------------------------
# spec predicate table. Each entry: functions(h, env) -> bool / delta.
# env carries: bar, feats, cores, structural, qualified, ctx, cfg,
#              prev_bar, prev_feats

def _h1_confirm(h, e):
    """Returns the confirm branch name, or None (all confirm fns do)."""
    d = h.dir
    if test_criteria(e.bar, e.feats, h.sig_extreme, h.sig_rel_volume, d,
                     e.ctx.atr, e.cfg):
        return "TEST_OF_SIGNATURE"
    core = "VALIDATED_ADVANCE" if d == LONG else "VALIDATED_DECLINE"
    if e.cores.get(core) and e.ctx.atr and h.spawn_level is not None:
        tol = e.cfg.context.level_atr_mult * e.ctx.atr
        edge = e.bar.low if d == LONG else e.bar.high
        if abs(edge - h.spawn_level) <= tol:
            return f"{core}_OFF_LEVEL"
    return None


def _h1_refute(h, e):
    return (e.bar.close < h.sig_low if h.dir == LONG
            else e.bar.close > h.sig_high)


def _h1_support(h, e):
    d = h.dir
    if test_criteria(e.bar, e.feats, h.sig_extreme, h.sig_rel_volume, d,
                     e.ctx.atr, e.cfg):
        return True
    if e.cores.get("ABSORPTION") and e.ctx.atr:
        prox = e.cfg.hypotheses.test_proximity_atr * e.ctx.atr
        if d == LONG:
            return e.bar.low <= h.sig_low + prox
        return e.bar.high >= h.sig_high - prox
    return False


def _h2_confirm(h, e):
    d = h.dir
    core = "NO_DEMAND" if d == SHORT else "NO_SUPPLY"
    if e.cores.get(core) and _rally_attempt(e.bar, e.prev_bar, d):
        return f"{core}_ON_COUNTER_ATTEMPT"
    if (e.prev_feats is not None and e.prev_feats.rel_volume is not None
            and e.feats.rel_volume is not None
            and e.feats.rel_volume > e.prev_feats.rel_volume):
        if d == SHORT and e.feats.direction < 0 and e.bar.close < h.sig_mid:
            return "MIDPOINT_BREAK_VOL_EXPANDING"
        if d == LONG and e.feats.direction > 0 and e.bar.close > h.sig_mid:
            return "MIDPOINT_BREAK_VOL_EXPANDING"
    return None


def _h2_refute(h, e):
    return (e.bar.close > h.sig_high if h.dir == SHORT
            else e.bar.close < h.sig_low)


def _h2_support(h, e):
    core = "NO_DEMAND" if h.dir == SHORT else "NO_SUPPLY"
    return e.cores.get(core) and _rally_attempt(e.bar, e.prev_bar, h.dir)


def _h3_confirm(h, e):
    d = h.dir
    lc, hc = e.cfg.labels, e.cfg.hypotheses
    if e.feats.rel_spread_pct is None or e.feats.rel_volume is None:
        return None
    wide = e.feats.rel_spread_pct >= lc.wide_spread_pctile
    vol = e.feats.rel_volume >= hc.h3.breakout_vol_mult
    if d == LONG:
        boundary = max(h.level, h.zone_hi)     # outermost in trade direction
        beyond = e.bar.close > boundary
        cp = e.feats.close_pos > 0.7
    else:
        boundary = min(h.level, h.zone_lo)
        beyond = e.bar.close < boundary
        cp = e.feats.close_pos < 0.3
    return "ZONE_BREAKOUT" if (wide and beyond and cp and vol) else None


def _h3_refute(h, e):
    lc = e.cfg.labels
    if e.feats.rel_spread_pct is None or e.feats.rel_volume is None:
        return False
    wide = e.feats.rel_spread_pct >= lc.wide_spread_pctile
    high_vol = e.feats.rel_volume >= lc.high_volume_mult
    far = (e.bar.close < h.zone_lo if h.dir == LONG
           else e.bar.close > h.zone_hi)
    return wide and high_vol and far


def _h4_confirm(h, e):
    mean, _ = _pullback_stats(h.pullback, e.ctx.idx, h.dir)
    if mean is None or e.feats.rel_volume is None:
        return None
    if h.dir == LONG:
        ok = (e.feats.direction > 0 and e.feats.close_pos > 0.7
              and e.feats.rel_volume > mean)
    else:
        ok = (e.feats.direction < 0 and e.feats.close_pos < 0.3
              and e.feats.rel_volume > mean)
    return "TREND_RESUMPTION" if ok else None


def _h4_refute(h, e):
    hc = e.cfg.hypotheses
    if h.pullback is None or h.prior_structural_level is None:
        return False
    expanded = h.pullback["max_rel_vol"] >= hc.h4.expand_mult   # sticky state
    if not expanded:
        return False
    if h.dir == LONG:                       # structural-break trigger
        return e.bar.close < h.prior_structural_level
    return e.bar.close > h.prior_structural_level


def _h4_support(h, e):
    core = "NO_SUPPLY" if h.dir == LONG else "NO_DEMAND"
    in_pullback = e.ctx.impulse_reaction == "REACTION"
    if e.cores.get(core) and in_pullback:
        return True
    _, pb_ext = _pullback_stats(h.pullback, e.ctx.idx, h.dir)
    if pb_ext is not None:
        # TEST-criteria probe of the pullback extreme (ratified v3.1)
        return test_criteria(e.bar, e.feats, pb_ext, h.sig_rel_volume, h.dir,
                             e.ctx.atr, e.cfg)
    return False


def _h5_confirm(h, e):
    if e.cores.get("UPTHRUST"):
        return "UPTHRUST"
    if e.cores.get("NO_DEMAND"):
        return "NO_DEMAND"
    return None


def _h5_refute(h, e):
    """3 consecutive qualifying closes; counter maintained here (v3.1 pin)."""
    hc = e.cfg.hypotheses
    qual = (e.bar.close > h.sig_close and e.feats.rel_volume is not None
            and e.feats.rel_volume >= 1.0)
    if h.dir == LONG:                       # mirror: selling-climax fade
        qual = (e.bar.close < h.sig_close and e.feats.rel_volume is not None
                and e.feats.rel_volume >= 1.0)
    h.refute_count = h.refute_count + 1 if qual else 0
    return h.refute_count >= hc.h5.refute_bars


SPECS = {
    "H1": {"klass": "REVERSAL", "confirm": _h1_confirm, "refute": _h1_refute,
           "support": _h1_support, "window": lambda c: c.hypotheses.h1.confirm_window},
    "H2": {"klass": "REVERSAL", "confirm": _h2_confirm, "refute": _h2_refute,
           "support": _h2_support, "window": lambda c: c.hypotheses.h2.confirm_window},
    "H3": {"klass": "TREND", "confirm": _h3_confirm, "refute": _h3_refute,
           "support": lambda h, e: False,   # handled via zone extension
           "window": lambda c: c.hypotheses.h3.confirm_window},
    "H4": {"klass": "TREND", "confirm": _h4_confirm, "refute": _h4_refute,
           "support": _h4_support, "window": lambda c: c.hypotheses.h4.confirm_window},
    "H5": {"klass": "REVERSAL", "confirm": _h5_confirm, "refute": _h5_refute,
           "support": lambda h, e: False,
           "window": lambda c: c.hypotheses.h5.confirm_window},
}


class _Env:
    def __init__(self, **kw):
        self.__dict__.update(kw)


class HypothesisManager:
    """RULES Sec 2 two-phase lifecycle. One instance per Signal TF."""

    def __init__(self, cfg, ctx_ratio, narrative, router, gate_fn):
        self.cfg = cfg
        self.ctx_ratio = ctx_ratio
        self.pending_gate_max = (cfg.hypotheses.pending_gate_ctx_ratio_mult
                                 * ctx_ratio)
        self.narrative = narrative
        self.router = router
        self.gate_fn = gate_fn            # (h, ctx_tf, signal_close, cfg) -> bool
        self.active = []                  # collection; OPEN is a state
        self._hyp_seq = 0
        self.diagnostics = {"CONFIRM_UNDERSTRENGTH": 0, "BLOCKED_SPAWNS": 0}
        self._absorption_recs = []        # H3 scan: {idx, low, high, level}
        self._prev_bar = None
        self._prev_feats = None

    # ------------------------------------------------------------------ step

    def step(self, bar, feats, cores, structural, qualified, ctx, ctx_tf):
        e = _Env(bar=bar, feats=feats, cores=cores, structural=structural,
                 qualified=qualified, ctx=ctx, cfg=self.cfg,
                 prev_bar=self._prev_bar, prev_feats=self._prev_feats)
        hcfg = self.cfg.hypotheses
        self.last_confirm_dirs = []       # confirms this bar (broker exit b)

        # ---- PHASE A: evaluate; no actions ----
        candidates = []
        for h in list(self.active):
            spec = SPECS[h.spec]
            if spec["refute"](h, e):                      # refute first, both states
                self._close(h, "REFUTED", bar)
                continue
            if h.state == CPG:
                h.pending_age += 1
                if h.pending_age > self.pending_gate_max:
                    self._close(h, "EXPIRED", bar, note="pending_gate_window")
                    continue
                ok, branch = self.gate_fn(h, ctx_tf, bar.close, self.cfg)
                self._log("GATE_RECHECK", bar, h=h.describe(),
                          permitted=ok, branch=branch)
                if ok:
                    candidates.append(h)                  # gate only in CPG
                continue

            # state OPEN
            h.age += 1
            if self._expired(h, ctx):
                self._close(h, "EXPIRED", bar)
                continue
            self._h3_extend(h, e)                         # zone growth (+delta inside)
            delta = self._evidence_delta(h, e)
            if delta:
                h.strength += delta
                self._log("STRENGTH", bar, h=h.describe(), delta=delta)
            self._boosters(h, ctx_tf, bar)
            if (hcfg.strength_floor.enabled
                    and h.strength < hcfg.strength_floor.value):
                self._close(h, "KILLED_WEAK", bar)
                continue
            branch = (spec["confirm"](h, e) if self._in_window(h, ctx)
                      else None)
            if branch:
                h.confirm_branch = branch
                self.last_confirm_dirs.append(h.dir)
                self._log("CONFIRM", bar, h=h.describe(), branch=branch)
                if h.strength < hcfg.min_strength_to_confirm:
                    self.diagnostics["CONFIRM_UNDERSTRENGTH"] += 1
                    self._log("CONFIRM_UNDERSTRENGTH", bar, h=h.describe())
                    continue
                ok, branch = self.gate_fn(h, ctx_tf, bar.close, self.cfg)
                self._log("GATE", bar, h=h.describe(),
                          permitted=ok, branch=branch)
                if ok:
                    candidates.append(h)
                else:
                    h.state = CPG
                    h.pending_age = 0
                    self._log("CONFIRMED_PENDING_GATE", bar, h=h.describe())

        # ---- PHASE B: all graduate; resolve act-once by strength ----
        acted = None
        if candidates:
            for h in candidates:
                h.state = "GRADUATED"
                self.active.remove(h)
                # stop is DEFINED at graduation — logged here so the
                # spread-vs-stop diagnostic covers every graduation in
                # every variant, traded or not
                stop_ref = self.router._signature_stop(h, self)
                self._log("GRADUATED", bar, h=h.describe(),
                          stop_ref=stop_ref,
                          stop_dist_at_grad=abs(bar.close - stop_ref))
            best = max(c.strength for c in candidates)
            top = [c for c in candidates if c.strength == best]
            if len(candidates) > 1:
                self._log("GRADUATION_CONFLICT", bar,
                          ids=[c.id for c in candidates], acted=(
                              top[0].id if len(top) == 1 else None))
            if len(top) == 1:
                acted = top[0]
            for h in candidates:
                if h is not acted:
                    self._log("SIGNAL_UNACTED_CONFLICT", bar, h=h.describe())

        # ---- PHASE C: act once ----
        if acted is not None:
            self.router.route_signal(acted, bar, ctx, self)

        # refutation check for a pending refinement (Sec 9, on Signal closes)
        self.router.on_signal_close(bar, feats, cores, ctx, self.cfg, e)

        spawned = self._spawn(e)
        if self.cfg.ablation.no_confirmation and spawned:
            # ablation (iii): entry on the signature bar itself — the freshly
            # spawned hypothesis graduates immediately (gate still applies
            # unless ablated separately); acted-once discipline unchanged
            grads = []
            for h in spawned:
                h.confirm_branch = "ABLATION_IMMEDIATE"
                ok, br = self.gate_fn(h, ctx_tf, bar.close, self.cfg)
                self._log("GATE", bar, h=h.describe(), permitted=ok, branch=br)
                if ok:
                    grads.append(h)
                else:
                    h.state = CPG
                    h.pending_age = 0
            for h in grads:
                h.state = "GRADUATED"
                self.active.remove(h)
                stop_ref = self.router._signature_stop(h, self)
                self._log("GRADUATED", bar, h=h.describe(),
                          stop_ref=stop_ref,
                          stop_dist_at_grad=abs(bar.close - stop_ref))
            if grads:
                best = max(g.strength for g in grads)
                top = [g for g in grads if g.strength == best]
                if len(top) == 1:
                    self.router.route_signal(top[0], bar, ctx, self)
        self._prev_bar, self._prev_feats = bar, feats

    # ------------------------------------------------------------- lifecycle

    def _expired(self, h, ctx):
        hc = self.cfg.hypotheses
        if h.spec == "H3":
            if ctx.idx - h.spawn_idx > hc.h3.max_total_bars:
                return True
            return ctx.idx - h.window_anchor > hc.h3.confirm_window
        return h.age > SPECS[h.spec]["window"](self.cfg)   # expiry = window top

    def _in_window(self, h, ctx):
        if h.spec == "H3":
            off = ctx.idx - h.window_anchor
            return 1 <= off <= self.cfg.hypotheses.h3.confirm_window
        return 1 <= h.age <= SPECS[h.spec]["window"](self.cfg)

    def _evidence_delta(self, h, e):
        """Sec 2b: supporting wins over contradicting; both logged."""
        hc = self.cfg.hypotheses
        sup = SPECS[h.spec]["support"](h, e)
        cp = e.feats.close_pos
        thr = hc.evidence_contra_close_pos
        contra = (cp < thr if h.dir == LONG else cp > 1 - thr)
        if sup and contra:
            e.feats.flags["evidence_both"] = True
            self._log("EVIDENCE_BOTH_FLAGS", e.bar, h=h.describe())
        if sup:
            return hc.support_delta
        if contra:
            return -hc.contra_delta
        return 0.0

    def _boosters(self, h, ctx_tf, bar):
        """H1 + mirror only; edge-triggered once per condition (Sec 2b)."""
        if h.spec != "H1" or ctx_tf is None:
            return
        inc = self.cfg.hypotheses.booster_increment
        at_level = (ctx_tf.near_support if h.dir == LONG
                    else ctx_tf.near_resistance)
        if at_level and "ctx_level" not in h.boosters_applied:
            h.boosters_applied.add("ctx_level")
            h.strength += inc
            self._log("BOOSTER", bar, h=h.describe(), which="ctx_level")
        prev = h.prev_ctx_tf_phase
        cur = ctx_tf.phase
        if prev is not None and cur != prev and "ctx_transition" not in h.boosters_applied:
            src = "MARKDOWN" if h.dir == LONG else "MARKUP"
            ok_post = (cur == "POST_CLIMAX"
                       and ctx_tf.post_climax_dir == h.dir)
            if prev == src and (cur == "RANGING" or ok_post):
                h.boosters_applied.add("ctx_transition")
                h.strength += inc
                self._log("BOOSTER", bar, h=h.describe(), which="ctx_transition")
        h.prev_ctx_tf_phase = cur

    def _h3_extend(self, h, e):
        """Growing zone: further qualifying absorption extends zone, adds
        evidence, and re-anchors the confirm window (RULES Sec 5)."""
        if h.spec != "H3" or not e.cores.get("ABSORPTION") or e.ctx.atr is None:
            return
        tol = self.cfg.context.level_atr_mult * e.ctx.atr
        near = abs(((e.bar.high + e.bar.low) / 2) - h.level) <= tol
        if not near:
            return
        h.zone_lo = min(h.zone_lo, e.bar.low)
        h.zone_hi = max(h.zone_hi, e.bar.high)
        h.window_anchor = e.ctx.idx
        h.strength += self.cfg.hypotheses.support_delta
        self._log("H3_ZONE_EXTENDED", e.bar, h=h.describe(),
                  zone=[h.zone_lo, h.zone_hi])

    def _close(self, h, state, bar, **kw):
        h.state = state
        self.active.remove(h)
        self._log(state, bar, h=h.describe(), **kw)

    # ---------------------------------------------------------------- spawns

    def _spawn(self, e):
        if not e.feats.valid or e.bar.is_stub:
            return []
        n0 = self._hyp_seq
        # H3 absorption scan happens every bar regardless of label ownership
        self._h3_scan(e)
        q = e.qualified
        if q == "POTENTIAL_SELLING_CLIMAX":
            self._spawn_h1(e, LONG)
        elif q == "POTENTIAL_BUYING_CLIMAX":
            self._spawn_h1(e, SHORT)
            if self.cfg.hypotheses.h5.enabled:
                self._try_add("H5", SHORT, e)
        elif q == "UPTHRUST":
            self._try_add("H2", SHORT, e)
        elif q == "SPRING":
            self._try_add("H2", LONG, e)
        elif q == "NO_SUPPLY":
            self._spawn_h4(e, LONG)
        elif q == "NO_DEMAND":
            self._spawn_h4(e, SHORT)
        return [h for h in self.active if h.id is not None and h.id > n0]

    def _dup(self, spec, direction):
        return any(h.spec == spec and h.dir == direction for h in self.active)

    def _try_add(self, spec, direction, e, setup=None):
        if self._dup(spec, direction):
            self.diagnostics["BLOCKED_SPAWNS"] += 1
            self._log("BLOCKED_SPAWN", e.bar, spec=spec, dir=direction)
            return None
        h = Hypothesis(spec, direction, e.bar, e.feats, e.ctx, self.cfg)
        self._hyp_seq += 1
        h.id = self._hyp_seq
        h.observational = e.bar.segment != "cash"    # Part B: never trades
        h.spawn_segment = e.bar.segment
        h.spawn_ts = e.bar.ts
        if setup:
            setup(h)
        self.active.append(h)
        self._log("SPAWNED", e.bar, h=h.describe())
        return h

    def _spawn_h1(self, e, d):
        ctx = e.ctx
        marked_move = ctx.after_decline if d == LONG else ctx.after_rally
        if not marked_move:
            return
        if d == LONG:
            near = ctx.near_support
            fresh = ctx.is_new_low(e.bar)
            level = ctx.nearest_support_level
        else:
            near = ctx.near_resistance
            fresh = ctx.is_new_high(e.bar)
            level = ctx.nearest_resistance_level
        if not (near or fresh) and not self.cfg.ablation.no_location:
            return          # ablation (i): drop the location requirement

        def setup(h):
            # precedence pin: level first, else signature extreme
            h.spawn_level = level if near else h.sig_extreme
        self._try_add("H1", d, e, setup)

    def _h3_scan(self, e):
        """Track absorption bars near key levels; spawn on cluster. Spawn is
        attempted only when THIS bar added a qualifying absorption record —
        a persisting cluster must not re-attempt (and re-log BLOCKED_SPAWN)
        every bar."""
        hc = self.cfg.hypotheses.h3
        ctx = e.ctx
        if ctx.atr is None:
            return
        # record this bar if qualifying (uses ATR as of this bar's close — pin)
        added = False
        if e.cores.get("ABSORPTION"):
            mid = (e.bar.high + e.bar.low) / 2
            lv, dist = ctx.nearest_level(mid)
            if self.cfg.ablation.no_location:
                # ablation (i): absorption anywhere clusters; the "level"
                # degenerates to the bar mid (breakout boundary then reduces
                # to the zone edge via outermost())
                self._absorption_recs.append(
                    {"idx": ctx.idx, "low": e.bar.low, "high": e.bar.high,
                     "level": mid})
                added = True
            elif lv is not None and dist <= self.cfg.context.level_atr_mult * ctx.atr:
                self._absorption_recs.append(
                    {"idx": ctx.idx, "low": e.bar.low, "high": e.bar.high,
                     "level": lv})
                added = True
        self._absorption_recs = [r for r in self._absorption_recs
                                 if ctx.idx - r["idx"] < hc.cluster_window]
        if not added or not self._absorption_recs:
            return
        # cluster by level identity
        tol = self.cfg.context.level_identity_atr_frac * ctx.atr
        latest = self._absorption_recs[-1]
        group = [r for r in self._absorption_recs
                 if abs(r["level"] - latest["level"]) <= tol]
        if len(group) < hc.min_absorption_bars:
            return
        lv = latest["level"]
        close = ctx.close
        if ctx.phase in ("MARKUP", "MARKDOWN") and ctx.trend != 0:
            if ctx.trend == 1 and lv >= close:
                d = LONG
            elif ctx.trend == -1 and lv <= close:
                d = SHORT
            else:
                return
        elif ctx.phase == "RANGING":
            # direction = out of the range from the boundary where the
            # absorption sits (second-pass ruling #3)
            if (ctx.range_hi is not None
                    and abs(lv - ctx.range_hi) <= self.cfg.context.level_atr_mult * ctx.atr):
                d = LONG
            elif (ctx.range_lo is not None
                    and abs(lv - ctx.range_lo) <= self.cfg.context.level_atr_mult * ctx.atr):
                d = SHORT
            else:
                return
        else:
            return

        def setup(h):
            h.level = lv
            h.zone_lo = min(r["low"] for r in group)
            h.zone_hi = max(r["high"] for r in group)
            h.window_anchor = latest["idx"]
        self._try_add("H3", d, e, setup)

    def _spawn_h4(self, e, d):
        ctx = e.ctx
        hc = self.cfg.hypotheses.h4
        want_phase = "MARKUP" if d == LONG else "MARKDOWN"
        if ctx.phase != want_phase or ctx.phase_age < hc.established_min_bars:
            return
        if ctx.impulse_reaction != "REACTION" or ctx.pullback is None:
            return
        mean, _ = _pullback_stats(ctx.pullback, ctx.idx, d)
        if mean is None or mean >= hc.pullback_vol_max:
            return
        pb_start = ctx.pullback["start_idx"]
        prior = (ctx.last_swing_low_before(pb_start) if d == LONG
                 else ctx.last_swing_high_before(pb_start))

        def setup(h):
            h.pullback = ctx.pullback
            h.prior_structural_level = prior
        self._try_add("H4", d, e, setup)

    # ---------------------------------------------------------------- misc

    def _log(self, typ, bar, **payload):
        self.narrative.log(typ, ts=bar.ts, **payload)

    def h4_stop(self, h):
        """H4 stop at graduation: pullback extreme through the graduation bar
        (INCLUDES the current bar — the stop is computed at graduation)."""
        if h.pullback:
            exts = h.pullback["lows"] if h.dir == LONG else h.pullback["highs"]
            if exts:
                return min(exts) if h.dir == LONG else max(exts)
        return h.sig_low if h.dir == LONG else h.sig_high
