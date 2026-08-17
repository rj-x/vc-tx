"""Session-aware resampling (prompt Part 6): cash-session 1M bars into
intermediate TFs. Bars never span the overnight gap — each session's blocks
start fresh at the cash open; a trailing partial block is a STUB bar
(context-only downstream). Bars carry session_id and tod_bin for
session-time feature normalization. Bar.ts = the bar's CLOSE time.
"""

import pandas as pd

from .bars import Bar
from .segments import segment_of


def canonical_tod(ts_open, anchor_london=21.5):
    """Minutes since the canonical trading-day anchor (~21:30 London) for a
    bar OPEN timestamp — the live loops' bin key MUST match the resampler's
    (tod-misalignment defect, fixed 2026-08-17)."""
    lon = pd.Timestamp(ts_open).tz_convert("Europe/London")
    lt = lon.hour + lon.minute / 60.0
    tday = lon.normalize() + pd.Timedelta(days=1 if lt >= anchor_london else 0)
    anchor = (tday - pd.Timedelta(days=1)
              + pd.Timedelta(hours=int(anchor_london),
                             minutes=int((anchor_london % 1) * 60)))
    return int((lon - anchor).total_seconds() // 60), tday


def trading_sessions(df, anchor_london=21.5):
    """Part B: ALL rows (extended hours included), grouped into futures
    trading days anchored at ~21:30 London; tod_bin = minutes since anchor.
    Bars never span the anchor; segments tagged downstream."""
    out = df.copy()
    lon = out.index.tz_convert("Europe/London")
    lt = lon.hour + lon.minute / 60.0
    # bars at/after the anchor belong to the NEXT trading day
    tday = lon.normalize() + pd.to_timedelta((lt >= anchor_london) * 1, unit="D")
    days = sorted(pd.unique(tday))
    sid = {d: i for i, d in enumerate(days)}
    out["session_id"] = [sid[d] for d in tday]
    anchor = tday - pd.Timedelta(days=1) + pd.Timedelta(hours=int(anchor_london),
                                                        minutes=int((anchor_london % 1) * 60))
    out["_tod"] = ((out.index - anchor.tz_convert("UTC")).total_seconds() // 60).astype(int)
    return out


def cash_sessions(df):
    """Clean-store frame -> cash-session rows with a session ordinal.
    Relies on the clean store's in_cash/ldate columns (store.py build)."""
    cash = df[df["in_cash"]].copy()
    dates = sorted(cash["ldate"].unique())
    sid = {d: i for i, d in enumerate(dates)}
    cash["session_id"] = cash["ldate"].map(sid)
    return cash


def exec_bars(cash, tf="1min"):
    """1M bars as engine Bars. tod_bin = minute offset (from session start,
    or the trading-day anchor when frames come from trading_sessions)."""
    out = []
    has_tod = "_tod" in cash.columns
    for _sid, g in cash.groupby("session_id", sort=True):
        t0 = g.index[0]
        for ts, r in g.iterrows():
            tod = int(r["_tod"]) if has_tod else int((ts - t0).total_seconds() // 60)
            out.append(Bar(ts + pd.Timedelta(minutes=1),
                           r["open"], r["high"], r["low"], r["close"],
                           r["volume"], tf=tf, session_id=int(r["session_id"]),
                           tod_bin=tod, segment=segment_of(ts)))
    return out


def session_bars(cash, tf="1d"):
    """One bar per cash session (D1 at the cash-close boundary, Part 6).
    Never a stub — the session IS the bar."""
    out = []
    for sid, g in cash.groupby("session_id", sort=True):
        close_ts = g.index[-1] + pd.Timedelta(minutes=1)
        out.append(Bar(close_ts, g["open"].iloc[0], g["high"].max(),
                       g["low"].min(), g["close"].iloc[-1],
                       g["volume"].sum(), tf=tf,
                       session_id=int(sid), tod_bin=0, is_stub=False))
    return out


def resample_bars(cash, minutes, tf):
    """Aggregate 1M cash rows into `minutes`-blocks per session."""
    out = []
    has_tod = "_tod" in cash.columns
    for sid, g in cash.groupby("session_id", sort=True):
        t0 = g.index[0]
        if has_tod:
            offsets = g["_tod"].astype(int)
        else:
            offsets = ((g.index - t0).total_seconds() // 60).astype(int)
        blocks = offsets // minutes
        for blk, gg in g.groupby(blocks):
            n = len(gg)
            close_ts = gg.index[-1] + pd.Timedelta(minutes=1)
            out.append(Bar(close_ts, gg["open"].iloc[0], gg["high"].max(),
                           gg["low"].min(), gg["close"].iloc[-1],
                           gg["volume"].sum(), tf=tf,
                           session_id=int(sid), tod_bin=int(blk),
                           is_stub=(n < minutes),
                           segment=segment_of(gg.index[0])))
    return out
