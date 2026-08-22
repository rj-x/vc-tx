"""Dedicated signal module — THE ONE place hypothesis firing conditions
may live (registers 31/34/35; SCHEMA v2, register 49): a hypothesis H<n>
is a claim; a SIGNAL S<k>-H<n> is one mechanical configuration testing it.
S-numbers are per-hypothesis, never reused; a signal's parameters are
never edited in place — any change is a NEW S-number (append-only
configuration history by construction). H<n> and S<k>-H<n> are the ONLY
identifier forms; the scoreboard refuses anything else (test-enforced).

Import direction is enforced by test: NO decision path imports this module.
A firing condition PERCEIVES AND REPORTS.

A firing condition is a callable
    (bar, ectx, sctx, feats, cores, structural, qualified, prev_structural)
      -> dir (+1/-1) or None
evaluated per 1M exec bar. A CLASS registered here is instantiated fresh at
attach (per-run state; nothing leaks between runs).
"""

import numpy as np

ESTABLISHED_TREND_AGE = 10   # registry: T1d establishment cell (prereg_T3_build)
SEQUENCE_N = 2               # registry: sequence clause (prereg_signal_rows_v1)
H9_CHAIN_DEPTH_MIN = 2       # registry: operator pre-registration 2026-08-19
# ratified 2026-08-20 (register 46):
H5_EXTENSION_ATR = 2.0       # founding h5.extension_atr, cited
H5_MA_PERIOD = 20            # founding h5.ma_period, cited
H6_PROX_ATR_FRAC = 0.25      # ratified (founding level-identity, reused)
H6_SPREAD_PCTILE = 0.90      # ratified (measured day-relative p90)
H6_CLOSE_POS = 0.25          # ratified (founding close_pos_lo neighborhood)
H6_WICK_FRAC = 0.33          # ratified (founding wick_frac_min, cited)
H6_DAY_WINDOW = 480          # implementer constant: trailing 1M bars for the
                             # day-relative baseline (H6's registered free
                             # parameter; operator-adjustable, flagged)
H11_BUCKET_PTS = 4.0         # ratified (home-derived; MIS-SCALE caveat on
                             # other instruments until per-instrument values)
H11_LOOKBACK_SESS = 5        # ratified (best-of-weak-field, flag standing)
H12_MIN_VISITS = 3           # ratified
H12_WINDOW_MIN = 90          # ratified
H12_DRY_RV = 0.7             # ratified (founding low_volume_mult, cited)
H13_VALUE_AREA_PCT = 0.70    # operator-specified at S0-H13 registration
                             # 2026-08-20 (value-area convention, register 50)
H15_SPEED_LIMIT_MIN = 30     # PROPOSED (register 56): opposite-boundary
                             # break within 30 min of the sweep — derived
                             # from measured t-MFE medians (~25-33 min,
                             # excursion study); ratification pending
H16_WINDOW_MIN = 30          # opening/closing window (GHLZ JFE 2018
                             # construction; operator order register 56)

# row-declaration tables (this module is the one permitted home for
# hypothesis identifiers; the scoreboard imports these):
ROW_MIGRATION_CHAIN = "S0-H9"     # event-derived, RECRUITMENT-AGNOSTIC —
                                  # does not test the claim's core (F3 label)
ROW_MIGRATION_RECRUITED = "S1-H9"  # event-derived, recruited-only chains
                                  # (register 49; the claim's core; expected
                                  # starved at current n — stated)
ROW_CLIMAX_EXTENSION = "S0-H5"    # event-derived (15M read, register 46)
ROW_INTRADAY_MOMENTUM = "S0-H16"  # event-derived (native-calendar windows,
                                  # GHLZ JFE 2018 construction; register 56)
EVENT_DERIVED_ROWS = {ROW_MIGRATION_CHAIN, ROW_MIGRATION_RECRUITED,
                      ROW_CLIMAX_EXTENSION, ROW_INTRADAY_MOMENTUM}
AGNOSTIC_ROWS = {"S0-H8"}          # graded either-direction (register 36)
DUAL_GRADED = {"S0-H7"}            # graded in BOTH modes (register 36)
# ONE firing condition, TWO gradings (register 37): the value row's fires
# ARE the key row's fires, copied — never independently computed, never
# double-counted as two signals
DERIVED_FIRES = {"S0-H8": "S0-H2"}
# narrative-condition primitives a recipe stage may reference (register 42e;
# the one-home rule: primitives are DECLARED here, grammar validates against
# this set). CAPABILITY ONLY until the excursion study's conditional cut
# reports — no narrative recipe may be registered before then.
NARRATIVE_EXIT_PRIMITIVES = ("opposing_structural_core", "trend_flip",
                             "phase_transition", "opposing_signal_fire")
# rows whose firing condition CONDITIONS on a bar-size/volatility class
# (register 47 fairness amendment): the scoreboard computes the named
# class's own chance rate and grades lift against it — unconditioned lift
# on a conditioned signal is a known confound class and is refused as
# headline lift. Class-mask implementations live in the scoreboard,
# keyed by these names.
CONDITIONED_ROWS = {"S0-H6": "wide_bar_p90_trailing_day"}
# exhaustion-family rows for the location-conditioned census (register 48)
EXHAUSTION_FAMILY = ("S0-H3", "S0-H4", "S0-H12")
# co-fire census family partition (register 45, operator-set; the one-home
# rule keeps hypothesis identifiers out of the census reader)
COFIRE_FAMILIES = {"event": ("S0-H1", "S0-H2"), "texture": ("S0-H4", "S0-H7"),
                   "structure": ("S0-H3", "S0-H9")}


def _s_h1(bar, ectx, sctx, feats, cores, structural, qualified, prev):
    """H1 bare pattern: climax print -> reversal against the climax."""
    return {"SELLING_CLIMAX": 1, "BUYING_CLIMAX": -1}.get(structural)


def _s_h2(bar, ectx, sctx, feats, cores, structural, qualified, prev):
    """H2 bare pattern: failed probe beyond an extreme -> reversal."""
    return {"UPTHRUST": -1, "SPRING": 1}.get(structural)


class _SH3:
    """H3 bare pattern: absorption cluster at a swing level -> breakout
    THROUGH the level. Founding cluster params cited from config
    (h3.min_absorption_bars, h3.cluster_window, context.level_atr_mult,
    context.level_identity_atr_frac); spawn layer only, no zone/recipe."""

    def __init__(self):
        self._recs = []          # (idx, level)

    def __call__(self, bar, ectx, sctx, feats, cores, structural, qualified,
                 prev):
        cfg = ectx.cfg
        w = cfg.hypotheses.h3.cluster_window
        self._recs = [r for r in self._recs if ectx.idx - r[0] < w]
        if ectx.atr is None or not cores.get("ABSORPTION"):
            return None
        mid = (bar.high + bar.low) / 2
        lv, dist = ectx.nearest_level(mid)
        if lv is None or dist > cfg.context.level_atr_mult * ectx.atr:
            return None
        self._recs.append((ectx.idx, lv))
        tol = cfg.context.level_identity_atr_frac * ectx.atr
        group = [r for r in self._recs if abs(r[1] - lv) <= tol]
        if len(group) < cfg.hypotheses.h3.min_absorption_bars:
            return None
        return 1 if lv >= ectx.close else -1


def _s_h4(bar, ectx, sctx, feats, cores, structural, qualified, prev):
    """H4 bare pattern: QUALIFIED no-supply/no-demand — the classifier's
    qualification (trending phase + pullback) IS the founding trend-pullback
    context, computed mechanically. Direction = trend resumption."""
    return {"NO_SUPPLY": 1, "NO_DEMAND": -1}.get(qualified)


def _s_h7(bar, ectx, sctx, feats, cores, structural, qualified, prev):
    """H7 claim direction (REVERSAL — quiet weakness as disguised
    accumulation, candidate register verbatim): SEQUENCE_N consecutive
    effortless prints -> fire AGAINST the drift. BARE VARIANT: the
    registered anatomy's session-extreme proximity is a walk-forward free
    parameter and is NOT applied here (audit flag in the register)."""
    if structural == "EFFORTLESS_DECLINE" and prev == "EFFORTLESS_DECLINE":
        return 1
    if structural == "EFFORTLESS_ADVANCE" and prev == "EFFORTLESS_ADVANCE":
        return -1
    return None


def _s1_h1(bar, ectx, sctx, feats, cores, structural, qualified, prev):
    """S1-H1 (register 49): the FOUNDING CONTEXT-QUALIFIED climax — the
    qualified layer carries the claim's "late in an extended move" clause
    (after-decline/after-rally + new-extreme/level context, classifier
    founding rules). Registered to resolve audit finding F1."""
    return {"POTENTIAL_SELLING_CLIMAX": 1,
            "POTENTIAL_BUYING_CLIMAX": -1}.get(qualified)


def _s1_h2(bar, ectx, sctx, feats, cores, structural, qualified, prev):
    """S1-H2 (register 49): the FOUNDING QUALIFIED upthrust/spring — the
    qualification carries the claim's "beyond a prior extreme" clause
    (range-extreme/resistance context). Resolves audit finding F2."""
    return {"UPTHRUST": -1, "SPRING": 1}.get(qualified)


def _s_h10(bar, ectx, sctx, feats, cores, structural, qualified, prev):
    """H10 (T1d's measured conditions exactly): trend-matched structural
    ND/NS in an established 1M trend -> continuation. H4 variant
    re-anchored to 1M; no phase gate."""
    d = {"NO_SUPPLY": 1, "NO_DEMAND": -1}.get(structural)
    if d and ectx.trend == d and ectx.trend_age >= ESTABLISHED_TREND_AGE:
        return d
    return None


class _SH6:
    """H6 (ratified 2026-08-20): wide rejection bar AT a session extreme —
    day-relative spread (trailing-window percentile, NOT session-time
    bins), adverse close, large wick, volume-agnostic. Short at highs,
    mirrored long at lows. Session extremes tracked internally (current +
    prior session); proximity band H6_PROX_ATR_FRAC x ATR(15M)."""

    def __init__(self):
        from collections import deque
        self._ranges = deque(maxlen=H6_DAY_WINDOW)
        self._sess = None

    def __call__(self, bar, ectx, sctx, feats, cores, structural, qualified,
                 prev):
        st = self._sess
        if st is None or st["sid"] != bar.session_id:
            self._sess = {"sid": bar.session_id, "hi": bar.high,
                          "lo": bar.low,
                          "prior_hi": st["hi"] if st else None,
                          "prior_lo": st["lo"] if st else None}
            st = self._sess
        else:
            st["hi"] = max(st["hi"], bar.high)
            st["lo"] = min(st["lo"], bar.low)
        rng = bar.high - bar.low
        self._ranges.append(rng)
        if (sctx is None or sctx.atr is None or rng <= 0
                or len(self._ranges) < 100 or feats.close_pos is None):
            return None
        srt = sorted(self._ranges)
        if rng < srt[int(H6_SPREAD_PCTILE * (len(srt) - 1))]:
            return None
        tol = H6_PROX_ATR_FRAC * sctx.atr
        up_wick = (bar.high - max(bar.open, bar.close)) / rng
        dn_wick = (min(bar.open, bar.close) - bar.low) / rng
        highs = [x for x in (st["hi"], st["prior_hi"]) if x is not None]
        lows = [x for x in (st["lo"], st["prior_lo"]) if x is not None]
        if (feats.close_pos <= H6_CLOSE_POS and up_wick >= H6_WICK_FRAC
                and any(bar.high >= hx - tol for hx in highs)):
            return -1
        if (feats.close_pos >= 1 - H6_CLOSE_POS and dn_wick >= H6_WICK_FRAC
                and any(bar.low <= lx + tol for lx in lows)):
            return 1
        return None


class _SH11:
    """H11 traversal clause (ratified 2026-08-20): fire in the direction
    of travel when price crosses INTO a low-volume gap bucket (trailing
    H11_LOOKBACK_SESS-session profile, bucket H11_BUCKET_PTS, gap = <=p10).
    The NODE-STALL clause needs its own grading mode — registered pending
    sub-question, not this row. Home-derived bucket: MIS-SCALE caveat on
    other instruments."""

    def __init__(self):
        self._profiles = {}
        self._order = []
        self._gaps = None
        self._sid = None
        self._prev_b = None

    def _rebuild(self):
        agg = {}
        for sid in self._order[-H11_LOOKBACK_SESS:]:
            for b, v in self._profiles.get(sid, {}).items():
                agg[b] = agg.get(b, 0) + v
        if len(agg) < 10:
            self._gaps = None
            return
        vols = sorted(agg.values())
        p10 = vols[int(0.1 * (len(vols) - 1))]
        self._gaps = {b for b, v in agg.items() if v <= p10}

    def __call__(self, bar, ectx, sctx, feats, cores, structural, qualified,
                 prev):
        b = round(bar.close / H11_BUCKET_PTS) * H11_BUCKET_PTS
        if self._sid != bar.session_id:
            if self._sid is not None:
                self._order.append(self._sid)
                self._rebuild()
            self._sid = bar.session_id
            self._profiles[bar.session_id] = {}
        p = self._profiles[bar.session_id]
        p[b] = p.get(b, 0) + bar.volume
        fire = None
        if (self._gaps and self._prev_b is not None and b != self._prev_b
                and b in self._gaps and self._prev_b not in self._gaps):
            fire = 1 if b > self._prev_b else -1
        self._prev_b = b
        return fire


class _SH12:
    """H12 (ratified 2026-08-20): absorption-sequence zone. Zone = nearest
    1M swing level +/- H6_PROX_ATR_FRAC x ATR(15M) band. VISIT = band entry
    after having left by > band width. Fire at the close of the visit
    completing: >= H12_MIN_VISITS visits inside H12_WINDOW_MIN minutes,
    strictly diminishing per-visit median range-per-unit-volume, pullbacks
    drying (mean rel_volume < H12_DRY_RV and each quieter than the last).
    Direction = the side whose approach bars carry the higher volume."""

    def __init__(self):
        self._z = {}          # level key -> state

    def __call__(self, bar, ectx, sctx, feats, cores, structural, qualified,
                 prev):
        if (ectx.atr is None or sctx is None or sctx.atr is None
                or not ectx.levels):
            return None
        band = H6_PROX_ATR_FRAC * sctx.atr
        mid = (bar.high + bar.low) / 2
        lv, dist = ectx.nearest_level(mid)
        key = round(lv, 1)
        z = self._z.setdefault(key, {
            "in": False, "visit": None, "visits": [], "out_rv": [],
            "pulls": [], "out_far": True, "approach_from": None})
        inside = dist <= band
        fire = None
        if inside and not z["in"]:
            if z["out_far"]:              # a NEW visit begins
                if z["visits"]:
                    rvs = [r for r in z["out_rv"] if r is not None]
                    z["pulls"].append(float(np.mean(rvs)) if rvs else None)
                z["visit"] = {"r": [], "v": [],
                              "appr": 1 if bar.close > lv else -1,
                              "appr_vol": float(bar.volume)}
            z["in"], z["out_rv"], z["out_far"] = True, [], False
        elif not inside and z["in"]:      # visit ends
            v = z["visit"]
            if v and v["v"]:
                med_rpv = float(np.median(
                    [r / x for r, x in zip(v["r"], v["v"]) if x > 0]))
                z["visits"].append({"rpv": med_rpv,
                                    "t_end": bar.ts,
                                    "appr": v["appr"],
                                    "appr_vol": v["appr_vol"]})
                fire = self._check(z, bar)
            z["in"], z["visit"] = False, None
        if z["in"] and z["visit"] is not None:
            z["visit"]["r"].append(bar.high - bar.low)
            z["visit"]["v"].append(float(bar.volume))
        if not z["in"]:
            if feats.rel_volume is not None:
                z["out_rv"].append(feats.rel_volume)
            if dist > 2 * band:
                z["out_far"] = True
        return fire

    def _check(self, z, bar):
        vs = z["visits"]
        if len(vs) < H12_MIN_VISITS:
            return None
        seq = vs[-H12_MIN_VISITS:]
        span_min = (seq[-1]["t_end"] - seq[0]["t_end"]).total_seconds() / 60
        if span_min > H12_WINDOW_MIN:
            return None
        if not all(seq[i + 1]["rpv"] < seq[i]["rpv"]
                   for i in range(len(seq) - 1)):
            return None
        pulls = [p for p in z["pulls"][-(H12_MIN_VISITS - 1):]
                 if p is not None]
        if len(pulls) < H12_MIN_VISITS - 1:
            return None
        if not all(p < H12_DRY_RV for p in pulls):
            return None
        if not all(pulls[i + 1] < pulls[i] for i in range(len(pulls) - 1)):
            return None
        below = sum(v["appr_vol"] for v in seq if v["appr"] == -1)
        above = sum(v["appr_vol"] for v in seq if v["appr"] == 1)
        z["visits"], z["pulls"] = [], []          # one fire per sequence
        return 1 if below >= above else -1


class _SH13:
    """S0-H13 (register 50, pre-registered): value-area reclaim. Value
    area = central H13_VALUE_AREA_PCT volume band of the trailing profile
    (POC expansion; H11's ratified bucket/lookback). Break = 1M close
    beyond the band edge; fade = excursion mean rel_volume < 1.0 vs the
    session-time baseline AND last excursion rv <= first (the registered
    implementation reading of "declining"); reclaim = close back inside
    with rel_volume > 1.0; fire at the reclaim close toward the far edge.
    The source's absorption clause and stop/target geometry are OUT OF
    SCOPE by registration (organs #4/#5 / recipe layer)."""

    def __init__(self):
        self._profiles, self._order = {}, []
        self._sid = None
        self._va = None
        self._out = None

    def _rebuild(self):
        agg = {}
        for sid in self._order[-H11_LOOKBACK_SESS:]:
            for b, v in self._profiles.get(sid, {}).items():
                agg[b] = agg.get(b, 0) + v
        if len(agg) < 10:
            self._va = None
            return
        total = sum(agg.values())
        poc = max(agg, key=agg.get)
        lo = hi = poc
        vol = agg[poc]
        while vol < H13_VALUE_AREA_PCT * total:
            up, dn = hi + H11_BUCKET_PTS, lo - H11_BUCKET_PTS
            uv, dv = agg.get(up, 0.0), agg.get(dn, 0.0)
            if uv <= 0 and dv <= 0:
                break
            if uv >= dv:
                hi, vol = up, vol + uv
            else:
                lo, vol = dn, vol + dv
        self._va = (lo - H11_BUCKET_PTS / 2, hi + H11_BUCKET_PTS / 2)

    def __call__(self, bar, ectx, sctx, feats, cores, structural, qualified,
                 prev):
        b = round(bar.close / H11_BUCKET_PTS) * H11_BUCKET_PTS
        if self._sid != bar.session_id:
            if self._sid is not None:
                self._order.append(self._sid)
                self._rebuild()
            self._sid = bar.session_id
            self._profiles[bar.session_id] = {}
            self._out = None
        p = self._profiles[bar.session_id]
        p[b] = p.get(b, 0) + bar.volume
        if self._va is None:
            return None
        val, vah = self._va
        inside = val <= bar.close <= vah
        fire = None
        if not inside:
            side = 1 if bar.close > vah else -1
            if self._out is None or self._out["side"] != side:
                self._out = {"side": side, "rvs": []}
            if feats.rel_volume is not None:
                self._out["rvs"].append(feats.rel_volume)
        elif self._out is not None:
            rvs = self._out["rvs"]
            fade = (bool(rvs) and sum(rvs) / len(rvs) < 1.0
                    and (len(rvs) < 2 or rvs[-1] <= rvs[0]))
            if fade and feats.rel_volume is not None                     and feats.rel_volume > 1.0:
                fire = -self._out["side"]     # toward the far edge
            self._out = None
        return fire


def _ts_ns(ts):
    """Nanosecond value for either pandas Timestamps or the synthetic
    integer-minute stamps the scenario rig uses."""
    return ts.value if hasattr(ts, "value") else int(ts) * 60_000_000_000


def _s_h14(bar, ectx, sctx, feats, cores, structural, qualified, prev):
    """S0-H14 (register 56): COUNTER-trend structural ND/NS in an
    established 1M trend (trend_age >= ESTABLISHED_TREND_AGE) — the mirror
    of H10's trend-matched configuration; absorption reading: fire WITH
    the trend (continuation). Origin: the parked T1d contra-direction
    curiosity (2026-08-17)."""
    d = {"NO_SUPPLY": 1, "NO_DEMAND": -1}.get(structural)
    if d and ectx.trend == -d and ectx.trend_age >= ESTABLISHED_TREND_AGE:
        return ectx.trend
    return None


class _SH15:
    """S0-H15 (register 56): sweep-and-reclaim, deliberately LOOSENED
    three-clause skeleton (the H12/H13 starvation lesson): RANGING phase +
    a sweep print beyond the phase tracker's own range boundary (the
    range-definition PROPOSAL: ectx.range_hi/range_lo — the founding
    ranging criteria's existing object, no new window) + a close beyond
    the OPPOSITE boundary within H15_SPEED_LIMIT_MIN -> fire toward the
    session's volume center (trailing-profile PoC). Both parameter
    choices derivation-stated, ratification pending. The six-clause
    original schematic is preserved verbatim in the register entry as
    future S<k> material."""

    def __init__(self):
        self._prof = None
        self._sweep = None            # (side, ts_value)

    def __call__(self, bar, ectx, sctx, feats, cores, structural, qualified,
                 prev):
        from backtest.location_census import _Profile  # lazy; reader-side
        if self._prof is None:
            self._prof = _Profile()
        self._prof.feed(bar)
        if ectx.phase != "RANGING" or ectx.range_hi is None                 or ectx.range_lo is None:
            self._sweep = None
            return None
        if bar.high > ectx.range_hi:
            self._sweep = ("high", _ts_ns(bar.ts))
        elif bar.low < ectx.range_lo:
            self._sweep = ("low", _ts_ns(bar.ts))
        if self._sweep is None:
            return None
        side, t0 = self._sweep
        if (_ts_ns(bar.ts) - t0) > H15_SPEED_LIMIT_MIN * 60_000_000_000:
            self._sweep = None
            return None
        broke = (bar.close < ectx.range_lo if side == "high"
                 else bar.close > ectx.range_hi)
        if not broke:
            return None
        self._sweep = None
        # PoC = max-volume bucket of the trailing profile
        agg = {}
        for sid in self._prof._order[-5:]:
            for b, v in self._prof._profiles.get(sid, {}).items():
                agg[b] = agg.get(b, 0) + v
        if len(agg) < 10:
            return None
        poc = max(agg, key=agg.get)
        if poc == bar.close:
            return None
        return 1 if poc > bar.close else -1


class _S1H11:
    """S1-H11 (register 56; the node-stall clause, grading mode RATIFIED
    as SUPPRESSION): fires on entry INTO a high-volume node bucket, in the
    travel direction. THE CLAIM SUCCEEDS WHEN INITIATION LIFT IS NEGATIVE
    — node entries suppress episode-begins below their conditioned base.
    Read the sign accordingly; a positive lift REFUTES the stall clause."""

    def __init__(self):
        from backtest.location_census import _Profile
        self._p = _Profile()
        self._prev_cls = None

    def __call__(self, bar, ectx, sctx, feats, cores, structural, qualified,
                 prev):
        cls = self._p.feed(bar)
        fire = None
        if cls == "node" and self._prev_cls not in (None, "node"):
            b = round(bar.close / H11_BUCKET_PTS) * H11_BUCKET_PTS
            prev_b = getattr(self, "_prev_b", None)
            if prev_b is not None and b != prev_b:
                fire = 1 if b > prev_b else -1
        self._prev_cls = cls
        self._prev_b = round(bar.close / H11_BUCKET_PTS) * H11_BUCKET_PTS
        return fire


FIRING_CONDITIONS = {
    "S0-H1": _s_h1,
    "S0-H2": _s_h2,
    "S0-H3": _SH3,                # class: fresh instance per attach
    "S0-H4": _s_h4,
    "S0-H7": _s_h7,
    "S0-H10": _s_h10,
    "S0-H6": _SH6,                # ratified 2026-08-20 (register 46)
    "S0-H11": _SH11,              # ratified 2026-08-20; traversal clause
    "S0-H12": _SH12,              # ratified 2026-08-20
    "S1-H1": _s1_h1,              # register 49 (audit F1 resolution)
    "S1-H2": _s1_h2,              # register 49 (audit F2 resolution)
    "S0-H13": _SH13,              # register 50 (value-area reclaim)
    "S0-H14": _s_h14,             # register 56 (counter-trend absorption)
    "S0-H15": _SH15,              # register 56 (sweep-and-reclaim skeleton)
    "S1-H11": _S1H11,             # register 56 (node-stall, SUPPRESSION)
}


class SignalWatch:
    """Passive observer. attach() wraps the exec pipe's on_close to record
    fires; the wrapped call's inputs and outputs are untouched (invariance
    test: decisions AND narration bit-identical with tracking on/off)."""

    def __init__(self):
        self.fires = []          # {"ts", "name", "dir"}
        self._prev_structural = None

    def attach(self, engine):
        conds = {n: (f() if isinstance(f, type) else f)
                 for n, f in FIRING_CONDITIONS.items()}
        orig = engine.exec_pipe.on_close

        def observed(bar, ctx_tf=None, signal_ctx=None):
            out = orig(bar, ctx_tf=ctx_tf, signal_ctx=signal_ctx)
            if out is not None and not bar.is_stub:
                feats, cores, structural, qualified = out
                if feats.valid:
                    for name, fn in conds.items():
                        d = fn(bar, engine.exec_pipe.ctx, signal_ctx, feats,
                               cores, structural, qualified,
                               self._prev_structural)
                        if d:
                            self.fires.append({"ts": bar.ts, "name": name,
                                               "dir": int(d)})
                    self._prev_structural = structural
            return out
        engine.exec_pipe.on_close = observed
        return self
