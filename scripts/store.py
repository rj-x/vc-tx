#!/usr/bin/env python3
"""
Finsa-native multi-instrument store. Single source of truth.
============================================================
Dukascopy is retired from the pipeline: its volume correlates only +0.37 with
real volume, its stores for DAX / NASDAQ / S&P stop in 2023-24, and it has no
bid/ask at all. Finsa gives real volume, a MEASURED spread on every bar, and
verified cash products (return correlation 0.977-0.999 against the independent
Dukascopy series, with stable sub-0.01% offsets and no basis drift).

The cost is history: 1m ~28 sessions, 15m ~305, 1h ~615, daily back to 2012
(EURUSD 1999). That is the trade being made deliberately — two clean years
across eight markets rather than ten patchy ones on one.

NATIVE FEEDS ARE USED DIRECTLY, never resampled down from 1m, because each
timeframe has its own retention floor and resampling from the shallowest one
would throw away most of the history:
    1min <- minute     15min <- quarter     1h <- hour     1d <- day
    4h   <- resampled from hour, anchored to that market's cash open

SESSIONS ARE PER INSTRUMENT. The FTSE pipeline hardcoded 08:00-16:30 London,
which is right for UK and German cash but wrong by six hours for US indices.
Getting this wrong would mislabel every session-anchored bar and every
session-derived level.

EVERY BAR CARRIES ITS OWN MEASURED SPREAD (ask close - bid close), so costs are
exact per trade rather than a constant. This is the main thing Dukascopy could
never provide.

Usage
  python3 store.py build --instr all
  python3 store.py verify --instr all
  python3 store.py report

  from store import load
  d = load("ger40", "1h", session="cash")
"""

import argparse
import json
import os
import sys

import numpy as np
import pandas as pd

from paths import DATA_DIR as RAW, CLEAN_DIR as CLEAN

LONDON = "Europe/London"

# cash session in INSTRUMENT-LOCAL hours (SESSION_TZ; default London).
# US/gold sessions are defined in America/New_York so the in_cash label is
# correct through the ~2-3 week windows each year when US and UK DST shifts
# diverge (the old hardcoded London hours were off by one hour there).
SESSIONS = {
    "uk100":     (8.0, 16.5),    # FTSE cash 08:00-16:30 London
    "ger40":     (8.0, 16.5),    # Frankfurt 09:00-17:30 CET == 08:00-16:30 London (EU DST aligned)
    "us500":     (9.5, 16.0),    # NYSE 09:30-16:00 ET
    "us30":      (9.5, 16.0),
    "ustech100": (9.5, 16.0),
    "gold":      (8.0, 16.0),    # COMEX active hours, ET
    "goldvar":   (8.0, 16.0),
    "eurusd":    (8.0, 21.0),    # London + NY overlap, the liquid window
    "uk100fut":  (8.0, 16.5),    # UK 100 rolling future — trade only in FTSE cash hours
    "uk100sep26": (8.0, 16.5),   # UK 100 Sep-26 outright — roll-verification series
}
SESSION_TZ = {
    "us500": "America/New_York", "us30": "America/New_York",
    "ustech100": "America/New_York",
    "gold": "America/New_York", "goldvar": "America/New_York",
}
# NOTE: 4h resampling stays anchored to London wall time (lwall); for US
# instruments its cash-open anchor can drift 1h in DST-divergence weeks —
# accepted for the 4h reference product, revisit if 4h becomes a traded TF.
FEED = {"1min": "minute", "15min": "quarter", "1h": "hour", "1d": "day"}
BAR_MIN = {"1min": 1, "15min": 15, "1h": 60, "4h": 240, "1d": 1440}
TFS = ["1min", "15min", "1h", "4h", "1d"]
OHLCV = ["open", "high", "low", "close", "volume"]


def _read(slug, feed, side):
    p = os.path.join(RAW, f"{slug}_{feed}_{side}.csv")
    if not os.path.exists(p):
        return None
    df = pd.read_csv(p)
    df["time"] = pd.to_datetime(df["time"], utc=True)
    return df.drop_duplicates("time").sort_values("time").set_index("time")


def _label(df, slug, is_daily=False):
    lon = df.index.tz_convert(LONDON)
    df["lwall"] = lon.tz_localize(None)
    df["ltime"] = lon.hour + lon.minute / 60.0
    df["ldate"] = lon.normalize().tz_localize(None)
    a, b = SESSIONS[slug]
    # in_cash is judged in the INSTRUMENT's own timezone (DST-correct);
    # lwall/ltime/ldate stay London for cross-instrument comparability
    tz = SESSION_TZ.get(slug, LONDON)
    loc = df.index.tz_convert(tz)
    ltime_local = loc.hour + loc.minute / 60.0
    df["in_cash"] = True if is_daily else (ltime_local >= a) & (ltime_local < b)
    return df


def build_one(slug, verbose=True):
    a, b = SESSIONS[slug]
    if verbose:
        print(f"\n=== {slug}  (cash {a:.1f}-{b:.1f} London) ===")
    os.makedirs(CLEAN, exist_ok=True)
    stats = {"cash_session_london": [a, b]}

    for tf in TFS:
        if tf == "4h":
            src = _read(slug, "hour", "mid")
            hb, ha = _read(slug, "hour", "bid"), _read(slug, "hour", "ask")
            if src is None:
                continue
            src = _label(src, slug)
            if hb is not None and ha is not None:
                src["_sp"] = (ha["close"] - hb["close"]).reindex(src.index)
            else:
                src["_sp"] = np.nan
            off = pd.Timedelta(hours=a)
            src["_k"] = ((src["lwall"] - off).dt.floor("4h") + off).values
            g = src.groupby("_k")
            df = g.agg(open=("open", "first"), high=("high", "max"),
                       low=("low", "min"), close=("close", "last"),
                       volume=("volume", "sum"), n_bars=("close", "size"),
                       cash_frac=("in_cash", "mean"), spread=("_sp", "mean"))
            # keep the true UTC time of each block's first bar; .values on a
            # tz-aware series silently drops the timezone, so index the Series
            first_utc = src.reset_index().groupby("_k")["time"].first()
            df.index = pd.DatetimeIndex(first_utc.reindex(df.index))
            bid = ask = None
            has_spread = True
        else:
            feed = FEED[tf]
            mid = _read(slug, feed, "mid")
            if mid is None:
                continue
            df = mid[OHLCV].copy()
            bid, ask = _read(slug, feed, "bid"), _read(slug, feed, "ask")
            has_spread = False

        is_daily = tf == "1d"
        # clamp the handful of derived bid/ask bars that sit outside high/low
        lo, hi = df["low"], df["high"]
        clamped = int(((df["open"] > hi) | (df["open"] < lo) |
                       (df["close"] > hi) | (df["close"] < lo)).sum())
        df["open"] = df["open"].clip(lo, hi)
        df["close"] = df["close"].clip(lo, hi)

        if bid is not None and ask is not None:
            df["spread"] = (ask["close"] - bid["close"]).reindex(df.index)
        elif not has_spread:
            df["spread"] = np.nan
        df["vol_ok"] = df["volume"] > 0
        df = _label(df, slug, is_daily)

        r = np.log(df["close"]).diff()
        s = r.rolling(500, min_periods=100).std()
        with np.errstate(invalid="ignore", divide="ignore"):
            df["extreme"] = ((r / s).abs() > 12).fillna(False)

        df.index.name = "time"
        df.to_csv(os.path.join(CLEAN, f"{slug}_{tf}.csv"))
        cash = df[df["in_cash"]]
        stats[tf] = {
            "bars": int(len(df)), "cash_bars": int(len(cash)),
            "sessions": int(df["ldate"].nunique()),
            "first": str(df.index.min().date()), "last": str(df.index.max().date()),
            "zero_vol_pct": round(100.0 * float((~df["vol_ok"]).mean()), 2),
            "clamped": clamped,
            "median_spread_cash": (round(float(cash["spread"].median()), 4)
                                   if cash["spread"].notna().any() else None),
        }
        if tf == "1min":
            age_days = (pd.Timestamp.now(tz="UTC") - df.index.max()) / pd.Timedelta(days=1)
            stats["stale_1min_days"] = round(float(age_days), 1)
            if age_days > 5:
                print(f"  !! STALE: newest 1min bar is {age_days:.1f} days old — "
                      f"the ~30-day retention floor is eroding unsynced history. "
                      f"Run scripts/sync_daily.sh.")
        if verbose:
            sp = stats[tf]["median_spread_cash"]
            print(f"  {tf:>6}: {len(df):>7,} bars ({len(cash):>6,} cash) "
                  f"{stats[tf]['first']} -> {stats[tf]['last']}"
                  + (f"   spread {sp}" if sp is not None else ""))
    return stats


def verify_one(slug):
    """Checks that matter for analysis, run per instrument."""
    out = []

    def ck(name, ok, detail=""):
        out.append((name, bool(ok), detail))

    frames = {}
    for tf in TFS:
        p = os.path.join(CLEAN, f"{slug}_{tf}.csv")
        if os.path.exists(p):
            frames[tf] = pd.read_csv(p, index_col=0, parse_dates=[0])

    for tf, df in frames.items():
        bad = int(((df["high"] < df["low"]) | (df["close"] > df["high"]) |
                   (df["close"] < df["low"]) | (df["open"] > df["high"]) |
                   (df["open"] < df["low"])).sum())
        ck(f"OHLC integrity {tf}", bad == 0, f"{bad} malformed")
        ck(f"unique timestamps {tf}", not df.index.duplicated().any())

    # the strongest internal check: the native 15m feed must rebuild the
    # native 1h feed exactly, across the period where both exist
    if "15min" in frames and "1h" in frames:
        q = frames["15min"]
        agg = q.resample("1h").agg(open=("open", "first"), high=("high", "max"),
                                   low=("low", "min"), close=("close", "last"),
                                   volume=("volume", "sum")).dropna()
        j = agg.join(frames["1h"], rsuffix="_h", how="inner")
        # drop the first and last hour: the 15m store's retention floor lands
        # mid-hour, so its opening hour is missing constituent bars by
        # construction. That is a boundary effect, not a data disagreement.
        if len(j) > 200:
            j = j.iloc[1:-1]
            dis = (((j["high"] - j["high_h"]).abs() > 1e-9) |
                   ((j["low"] - j["low_h"]).abs() > 1e-9))
            e = float(max((j["high"] - j["high_h"]).abs().max(),
                          (j["low"] - j["low_h"]).abs().max()))
            v = float((j["volume"] - j["volume_h"]).abs().median())
            ck("15m rebuilds 1h", dis.mean() < 0.001 and v == 0.0,
               f"{int(dis.sum())}/{len(j)} bars differ ({100*dis.mean():.3f}%), "
               f"max {e:.2f} pts, median vol err {v}")

    # cash session must contain the bulk of the day's activity
    if "1h" in frames:
        d = frames["1h"]
        share = d[d["in_cash"]]["volume"].sum() / max(d["volume"].sum(), 1e-9)
        ck("cash session holds most volume", share > 0.45,
           f"{100*share:.1f}% of volume inside the declared session")
        cs = d[d["in_cash"]].groupby("ldate").size()
        a, b = SESSIONS[slug]
        ck("cash bars/session ~ session length", abs(cs.median() - (b - a)) <= 1.5,
           f"median {cs.median():.0f}/session, session is {b-a:.1f}h")

    if "1min" in frames:
        d = frames["1min"]
        sp = d[d["in_cash"]]["spread"]
        ck("spread present in cash hours", sp.notna().mean() > 0.9,
           f"median {sp.median():.3f}, {sp.round(4).nunique()} distinct values")
    return out


def cmd_build(a):
    slugs = list(SESSIONS) if a.instr == ["all"] else a.instr
    # merge into the existing report so a partial build doesn't clobber
    # other instruments' entries
    rp = os.path.join(CLEAN, "_report.json")
    rep = {}
    if os.path.exists(rp):
        with open(rp) as f:
            rep = {k: v for k, v in json.load(f).items() if k in SESSIONS}
    for s in slugs:
        rep[s] = build_one(s)
    with open(rp, "w") as f:
        json.dump(rep, f, indent=2, default=str)
    stale = {s: v["stale_1min_days"] for s, v in rep.items()
             if v.get("stale_1min_days", 0) > 5}
    if stale:
        print(f"\n!! STALE 1min data (days since newest bar): {stale}")
    print(f"\nWrote {CLEAN}/")


def cmd_verify(a):
    slugs = list(SESSIONS) if a.instr == ["all"] else a.instr
    total = passed = 0
    for s in slugs:
        res = verify_one(s)
        if not res:
            print(f"{s}: nothing built"); continue
        bad = [r for r in res if not r[1]]
        total += len(res); passed += len(res) - len(bad)
        print(f"{s:10s} {len(res)-len(bad)}/{len(res)} passed"
              + ("" if not bad else "   FAIL: " +
                 "; ".join(f"{n} ({d})" for n, _, d in bad)))
    print(f"\n{passed}/{total} checks passed overall.")
    if passed != total:
        sys.exit(1)


def cmd_report(a):
    p = os.path.join(CLEAN, "_report.json")
    if not os.path.exists(p):
        sys.exit("run build first")
    rep = json.load(open(p))
    rows = []
    for slug, s in rep.items():
        for tf in TFS:
            if tf in s:
                v = s[tf]
                rows.append([slug, tf, v["bars"], v["cash_bars"], v["sessions"],
                             v["first"], v["last"], v["median_spread_cash"]])
    t = pd.DataFrame(rows, columns=["instr", "tf", "bars", "cash bars",
                                    "sessions", "from", "to", "spread (cash)"])
    pd.set_option("display.width", 200)
    print(t.to_string(index=False))


def load(slug, tf="1h", session=None, drop_partial=False):
    p = os.path.join(CLEAN, f"{slug}_{tf}.csv")
    if not os.path.exists(p):
        sys.exit(f"no clean store for {slug}/{tf} — run `store.py build`")
    df = pd.read_csv(p, index_col=0, parse_dates=[0])
    df["ldate"] = pd.to_datetime(df["ldate"])
    if session == "cash":
        df = df[df["in_cash"]]
    return df


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    for nm, fn in (("build", cmd_build), ("verify", cmd_verify)):
        p = sub.add_parser(nm)
        p.add_argument("--instr", nargs="*", default=["all"],
                       choices=list(SESSIONS) + ["all"])
        p.set_defaults(func=fn)
    sub.add_parser("report").set_defaults(func=cmd_report)
    a = ap.parse_args()
    a.func(a)


if __name__ == "__main__":
    main()
