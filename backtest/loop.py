"""Backtest loop — reads market data EXCLUSIVELY through ClockGatedFeed
(lockbox-filtered by the store loader), replays bar closes chronologically
into the MTFEngine (descending-TF at shared timestamps inside process()),
and lets the broker resolve exits on 1M bars.

Session discipline (Part 7): EOD force-flat at session_end - eod_cutoff;
entry embargo from cutoff - embargo_min. Both derived from the instrument's
session calendar in config and evaluated in London wall time.
"""

import pandas as pd

from engine.pipeline import MTFEngine
from engine.resample import (cash_sessions, exec_bars, resample_bars,
                             trading_sessions)
from engine.store_loader import ClockGatedFeed, load_frame

_TFMIN = {"1min": 1, "3min": 3, "5min": 5, "15min": 15, "30min": 30, "1h": 60}


def session_fns(cfg, slug):
    inst = cfg.instruments[slug]
    end = inst.session_end_london
    cutoff_h = end - cfg.session.eod_cutoff_min_before_close / 60.0
    embargo_h = cutoff_h - cfg.session.entry_embargo_min / 60.0

    def _ltime(ts):
        lon = pd.Timestamp(ts).tz_convert("Europe/London")
        return lon.hour + lon.minute / 60.0 + lon.second / 3600.0

    return (lambda ts: _ltime(ts) >= embargo_h,      # embargo_fn
            lambda ts: _ltime(ts) >= cutoff_h)       # eod_fn


def build_bars(cfg, slug, root=None, lockbox_evaluation=False):
    """Load 1M working-set data and derive the configured TF stack."""
    df1 = load_frame(slug, "1min", root=root,
                     lockbox_evaluation=lockbox_evaluation)
    if cfg.session_model.extended_hours:
        cash = trading_sessions(df1,
                                cfg.session_model.trading_day_anchor_london)
    else:
        cash = cash_sessions(df1)
    sig_tf = cfg.mtf.signal_tf
    ctx_tf = cfg.mtf.context_tf
    bars = {
        cfg.mtf.execution_tf: exec_bars(cash, tf=cfg.mtf.execution_tf),
        sig_tf: resample_bars(cash, _TFMIN[sig_tf], sig_tf),
        ctx_tf: resample_bars(cash, _TFMIN[ctx_tf], ctx_tf),
    }
    if cfg.session_model.get("ladder"):
        for tf, m in (("3min", 3), ("5min", 5), ("30min", 30),
                      ("1min", 1), ("15min", 15), ("1h", 60)):
            if tf not in bars:
                bars["ladder:" + tf] = (exec_bars(cash, tf=tf) if m == 1
                                        else resample_bars(cash, m, tf))
    n_sessions = cash["session_id"].nunique()
    span = (cash.index.min(), cash.index.max())
    return bars, {"sessions": n_sessions, "span": span, "rows_1m": len(cash)}


def run_backtest(cfg, slug, root=None, lockbox_evaluation=False):
    """Returns (engine, info). All decisions flow through the standard
    pipeline; data visibility is enforced by ClockGatedFeed."""
    bars, info = build_bars(cfg, slug, root, lockbox_evaluation)
    inst = cfg.instruments[slug]
    embargo_fn, eod_fn = session_fns(cfg, slug)
    engine = MTFEngine(cfg, embargo_fn=embargo_fn, eod_fn=eod_fn,
                       tick_size=inst.tick_size, point_value=inst.point_value)

    # cash-CFD execution leg (Part A): quotes from the quote slug's clean
    # store (mid OHLC + measured spread, ffilled over quote gaps)
    qmap = {}
    if cfg.execution_vehicle.mode == "cash_cfd":
        qdf = load_frame(cfg.execution_vehicle.quote_slug, "1min", root=root,
                         lockbox_evaluation=lockbox_evaluation)
        qdf = qdf.copy()
        qdf["spread"] = qdf["spread"].ffill()
        for ts, r in qdf.iterrows():
            if pd.notna(r["spread"]):
                qmap[ts + pd.Timedelta(minutes=1)] = {
                    "open": r["open"], "high": r["high"], "low": r["low"],
                    "close": r["close"], "spread": r["spread"]}

    # index bars by close-ts through a ClockGatedFeed: frames are open-time
    # indexed, visibility = close time
    frames = {}
    barmap = {}
    for tf, blist in bars.items():
        # ClockGatedFeed makes a bar visible at index + tf_minutes, so index
        # each bar at close - tf_minutes: visibility lands EXACTLY at the
        # bar's true close, stub bars included (their nominal slot may be
        # longer than their true duration; the close is what matters).
        delta = pd.Timedelta(minutes=_TFMIN[tf.split(":")[-1]])
        idx = pd.DatetimeIndex([b.ts - delta for b in blist])
        frames[tf] = pd.DataFrame({"i": range(len(blist))}, index=idx)
        barmap[tf] = {b.ts: b for b in blist}
    feed = ClockGatedFeed(frames)

    cursors = {tf: 0 for tf in frames}
    exec_tf = cfg.mtf.execution_tf
    clock_steps = sorted({b.ts for b in bars[exec_tf]})
    order = ([cfg.mtf.context_tf]
             + [k for k in frames if k.startswith("ladder:")]
             + [cfg.mtf.signal_tf, exec_tf])
    for ts in clock_steps:
        feed.advance_to(ts)
        closed = {}
        for tf in order:
            rows, cursors[tf] = feed.newly_closed(tf, cursors[tf])
            if len(rows):
                delta = pd.Timedelta(minutes=_TFMIN[tf.split(":")[-1]])
                closed[tf] = [barmap[tf][i + delta] for i in rows.index]
        # feed every newly closed bar; same-ts bars go in one process() call
        kw = {}
        if closed.get(cfg.mtf.context_tf):
            kw["context_bar"] = closed[cfg.mtf.context_tf][-1]
        if closed.get(cfg.mtf.signal_tf):
            kw["signal_bar"] = closed[cfg.mtf.signal_tf][-1]
        if closed.get(exec_tf):
            kw["exec_bar"] = closed[exec_tf][-1]
        lb = {k.split(":")[1]: v[-1] for k, v in closed.items()
              if k.startswith("ladder:")}
        if lb:
            kw["ladder_bars"] = lb
        if kw:
            if "exec_bar" in kw:
                kw["exec_quote"] = qmap.get(ts)
            engine.process(ts, **kw)
    return engine, info
