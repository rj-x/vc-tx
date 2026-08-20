"""Register 48(c) proposed pins P1-P6, approved register 49 — the
previously assumed-unpinned properties, each pinned."""
import types

import numpy as np
import pandas as pd

from engine.bars import Bar
from helpers import scenario_cfg


def _bar(ts, o=100.0, h=101.0, l=99.0, c=100.5, v=100, sid=0):
    return Bar(ts, o, h, l, c, v, tf="1min", session_id=sid)


def _feats(close_pos=0.5, rel_volume=1.0, valid=True):
    return types.SimpleNamespace(close_pos=close_pos, rel_volume=rel_volume,
                                 valid=valid, flags={})


# ---- P1: recipes EOD flags across BOTH DST regimes (native closes)
def test_p1_eod_flags_native_close_both_dst_regimes():
    from backtest.recipes import _eod_flags
    for day, last_utc in (("2026-08-17", "15:29"),   # BST: 16:29 London
                          ("2026-01-12", "16:29")):  # GMT: 16:29 London
        ts0 = pd.Timestamp(f"{day} 07:05", tz="UTC")
        bars = [_bar(ts0 + pd.Timedelta(minutes=i)) for i in range(700)]
        flags = _eod_flags(bars, "uk100fut")
        flagged = [b.ts.strftime("%H:%M") for b, f in zip(bars, flags) if f]
        assert flagged == [last_utc], (day, flagged)


# ---- P2: _atr15 equivalence to the engine's ContextTracker ATR
def test_p2_atr_equivalence_to_engine():
    from engine.context import ContextTracker
    from backtest.scoreboard import _atr15
    cfg = scenario_cfg()                    # atr_period 5
    ctx = ContextTracker(cfg, "15min")
    bars = []
    px = 100.0
    for i in range(12):
        px += (-1) ** i * (1.5 + 0.3 * i)   # gaps between closes
        b = Bar(i + 1, px, px + 2 + 0.1 * i, px - 1, px + 0.5, 100,
                tf="15min")
        bars.append(b)
        ctx.update(b, _feats(), None)
    amap = _atr15(bars, cfg.context.atr_period)
    assert ctx.atr is not None
    assert abs(amap[bars[-1].ts] - ctx.atr) < 1e-9


# ---- P3: unit fixtures for the ratified condition classes
def test_p3_s0h6_rejection_fires_and_narrow_does_not():
    from engine.signal_watch import FIRING_CONDITIONS
    cond = FIRING_CONDITIONS["S0-H6"]()
    sctx = types.SimpleNamespace(atr=10.0)
    t0 = pd.Timestamp("2026-08-17 08:00", tz="UTC")
    d = None
    for i in range(120):                    # narrow baseline bars
        d = cond(_bar(t0 + pd.Timedelta(minutes=i), 100, 100.6, 99.9,
                      100.2, sid=1), None, sctx, _feats(0.5), {}, None,
                 None, None)
    assert d is None
    # wide rejection AT the session high: close weak, big upper wick
    b = _bar(t0 + pd.Timedelta(minutes=121), 100, 106, 99.5, 100.2, sid=1)
    d = cond(b, None, sctx, _feats(close_pos=0.1), {}, None, None, None)
    assert d == -1
    # same-width bar far below the extreme: silent
    b2 = _bar(t0 + pd.Timedelta(minutes=122), 90, 96, 89.5, 90.2, sid=1)
    assert cond(b2, None, sctx, _feats(0.1), {}, None, None, None) is None


def test_p3_s0h11_gap_entry_fires_in_travel_direction():
    from engine.signal_watch import FIRING_CONDITIONS, H11_BUCKET_PTS
    cond = FIRING_CONDITIONS["S0-H11"]()
    t0 = pd.Timestamp("2026-08-17 08:00", tz="UTC")
    k = 0
    # six sessions: heavy volume across 12 buckets, thin at 160 (the gap)
    for sid in range(6):
        for i in range(36):
            px = 100 + 4 * (i % 12)
            cond(_bar(t0 + pd.Timedelta(minutes=k), px, px + .5, px - .5,
                      px, v=1000 + 50 * (i % 12), sid=sid), None, None,
                 _feats(), {}, None, None, None)
            k += 1
        cond(_bar(t0 + pd.Timedelta(minutes=k), 160, 160.5, 159.5, 160,
                  v=1, sid=sid), None, None, _feats(), {}, None, None, None)
        k += 1
    # new session: step from the heavy bucket INTO the thin bucket
    cond(_bar(t0 + pd.Timedelta(minutes=k), 144, 144.5, 143.5, 144,
              v=500, sid=9), None, None, _feats(), {}, None, None, None)
    d = cond(_bar(t0 + pd.Timedelta(minutes=k + 1), 160, 160.5, 159.5,
                  160, v=5, sid=9), None, None, _feats(), {}, None, None,
             None)
    assert d == 1                           # upward travel into the gap


def test_p3_s0h12_sequence_fires_on_diminishing_drying_visits():
    from engine.signal_watch import FIRING_CONDITIONS
    cond = FIRING_CONDITIONS["S0-H12"]()
    lv = 100.0
    ectx = types.SimpleNamespace(atr=2.0, levels=[lv],
                                 nearest_level=lambda px: (lv, abs(px - lv)))
    sctx = types.SimpleNamespace(atr=8.0)   # band = 2.0
    t0 = pd.Timestamp("2026-08-17 08:00", tz="UTC")
    k = 0
    fire = None

    def step(px, rng, vol, rv):
        nonlocal k, fire
        b = _bar(t0 + pd.Timedelta(minutes=k), px, px + rng / 2,
                 px - rng / 2, px, v=vol, sid=1)
        r = cond(b, ectx, sctx, _feats(rel_volume=rv), {}, None, None, None)
        k += 1
        if r:
            fire = r
    # three visits from below, r/v 0.02 -> 0.01 -> 0.005; pullbacks drying
    for rpv, pull_rv in ((0.02, None), (0.01, 0.6), (0.005, 0.4)):
        if pull_rv is not None:
            for _ in range(3):
                step(94.0, 1.0, 100, pull_rv)      # outside, > 2x band away
        for _ in range(4):
            step(100.0, rpv * 100, 100, 0.9)       # inside the band
        step(94.0, 1.0, 100, 0.5)                  # exit completes visit
    assert fire == 1                       # below-side approaches dominate


# ---- P4: S0-H5 event-derived arithmetic
def test_p4_s0h5_extension_arithmetic():
    from backtest.scoreboard import h5_fires
    cfg = scenario_cfg()
    bars, px = [], 100.0
    for i in range(30):
        bars.append(Bar(pd.Timestamp("2026-08-17", tz="UTC")
                        + pd.Timedelta(minutes=15 * (i + 1)),
                        px, px + 2, px - 2, px, 100, tf="15min"))
    far = bars[-1].close + 100              # force close - sma >= 2*atr
    bars.append(Bar(bars[-1].ts + pd.Timedelta(minutes=15),
                    far, far + 2, far - 2, far, 100, tf="15min"))
    ev_hit = [{"type": "LABEL", "tf": cfg.mtf.signal_tf,
               "structural": "BUYING_CLIMAX", "ts": str(bars[-1].ts)}]
    ev_miss = [{"type": "LABEL", "tf": cfg.mtf.signal_tf,
                "structural": "BUYING_CLIMAX", "ts": str(bars[5].ts)}]
    assert [f["dir"] for f in h5_fires(ev_hit, bars, cfg)] == [-1]
    assert h5_fires(ev_miss, bars, cfg) == []


# ---- P5: class-mask no-lookahead (trailing shift)
def test_p5_class_mask_no_lookahead():
    from backtest.scoreboard import _wide_bar_mask
    rng = np.random.default_rng(7)
    lo = rng.normal(100, 1, 400)
    hi = lo + rng.uniform(0.5, 3.0, 400)
    m1 = _wide_bar_mask(hi, lo)
    hi2 = hi.copy()
    hi2[250] = lo[250] + 500.0              # explode bar 250's range
    m2 = _wide_bar_mask(hi2, lo)
    # bar 250's OWN class may change (its own range is the subject); all
    # EARLIER bars' classes must be untouched (the threshold is trailing)
    assert (m1[:250] == m2[:250]).all()


# ---- P6: trailing-profile no-lookahead across session rebuilds
def test_p6_profile_classification_uses_completed_sessions_only():
    from backtest.location_census import _Profile
    t0 = pd.Timestamp("2026-08-17 08:00", tz="UTC")
    def feed(prof, sid, px, v, k):
        return prof.feed(_bar(t0 + pd.Timedelta(minutes=k), px, px + .5,
                              px - .5, px, v=v, sid=sid))
    def run(vol_late):
        p = _Profile()
        k = 0
        for sid in range(6):
            for i in range(36):
                feed(p, sid, 100 + 4 * (i % 12), 1000 + 50 * (i % 12),
                     k); k += 1
            feed(p, sid, 160, 1, k); k += 1
        first = feed(p, 9, 160, 5, k); k += 1        # classified bar
        feed(p, 9, 160, vol_late, k)                  # later same-session
        return first
    assert run(1) == run(10**9) == "gap"    # later volume can't reach back


# ---- S0-H13 unit fixture (registered with the signal, register 50)
def test_s0h13_break_fade_reclaim_fires_toward_far_edge():
    from engine.signal_watch import FIRING_CONDITIONS
    cond = FIRING_CONDITIONS["S0-H13"]()
    t0 = pd.Timestamp("2026-08-17 08:00", tz="UTC")
    k = 0

    def step(px, v, rv, sid):
        nonlocal k
        b = _bar(t0 + pd.Timedelta(minutes=k), px, px + .5, px - .5, px,
                 v=v, sid=sid)
        r = cond(b, None, None, _feats(rel_volume=rv), {}, None, None, None)
        k += 1
        return r
    # six sessions build a value area centred near 116 (12 buckets,
    # centre-weighted volume)
    for sid in range(6):
        for i in range(36):
            px = 100 + 4 * (i % 12)
            step(px, 1000 + 400 * (6 - abs((i % 12) - 6)), 1.0, sid)
    # new session: break BELOW the band on fading volume, reclaim on
    # expanding volume -> long
    step(116, 1000, 1.0, 9)
    assert step(84, 100, 0.8, 9) is None       # break below, quiet
    assert step(84, 80, 0.6, 9) is None        # still out, declining
    assert step(116, 2000, 1.5, 9) == 1        # reclaim on volume -> long
    # negative control: heavy-volume excursion never fires on reclaim
    step(84, 5000, 2.0, 9)
    assert step(116, 2000, 1.5, 9) is None
