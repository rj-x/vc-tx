#!/usr/bin/env python3
"""
Finsa FTSE 100 collector — banks the maximum history the feed will release.
===========================================================================
The charts backend caps a single response at 10,000 BARS (not 10,000 minutes),
and the `m` parameter anchors the END of the returned window. Walking `m`
backwards therefore pages through history until the feed's per-timeframe
retention floor is hit:

    feed              cap/page   retention floor      practical depth
    minute            10,000     ~30 days             ~27 sessions
    quarter (15m)     10,000     ~12 months           ~302 sessions
    hour              10,000     ~24 months           ~604 sessions
    day               all        2012-03-26           ~3,745 sessions

Those floors are ROLLING. Minute data older than ~30 days and 15m data older
than ~12 months are gone for good, so the store only ever gets deeper by
syncing regularly and appending. Re-runs are safe: the store is a union,
deduplicated on timestamp.

Every timeframe is collected for mid, bid AND ask, which gives a measured
spread series rather than a flat cost assumption.

Usage:
  python3 collect.py sync                       # all feeds, full depth
  python3 collect.py sync --tf hour quarter     # subset
  python3 collect.py sync --sides mid           # mid only (faster)
  python3 collect.py status                     # what's in the store
  python3 collect.py validate                   # integrity checks

Notes:
  - The most recent bar of each feed is still forming, so it is dropped on
    collection and picked up by a later sync once settled.
  - Timestamps are UTC throughout. No resampling, no cleaning: this writes
    exactly what the feed returned. Hygiene is a separate, later step.
"""

import argparse
import json
import os
import sys
import time
import urllib.error
import urllib.request
from datetime import datetime, timezone

import pandas as pd

BASE = "https://charts.finsatechnology.com/data/{tf}/{instr}/{side}?l={n}"
# slug -> Finsa instrument id. Slug is used in filenames.
INSTRUMENTS = {
    "uk100":     "16645",   # FTSE 100
    "ger40":     "17068",   # DAX
    "us30":      "17322",   # Wall Street 30 (Dow)
    "ustech100": "20190",   # NASDAQ 100
    "us500":     "67995",   # S&P 500, per 0.1
    "gold":      "68924",   # Gold per 0.1, fixed spread
    "goldvar":   "72302",   # Gold per 0.1, VARIABLE spread
    "eurusd":    "16635",
    "uk100fut":  "70152",   # UK 100 Rolling Future — futures volume, roll handled by provider
    "uk100sep26": "72516",  # UK 100 Future (Sep 2026) — outright contract, for roll verification.
                            # Contract-specific ID (history starts at its 2026-06-11 listing);
                            # expected to go quiet after expiry ~2026-09-18. See DATA.md.
}
INSTRUMENT = "16645"          # default: FTSE 100
MAX_L = 10000                 # server-side cap per response
COLS = ["time", "open", "high", "low", "close", "volume"]
TFS = ["minute", "quarter", "hour", "day"]
SIDES = ["mid", "bid", "ask"]

from paths import DATA_DIR

MANIFEST = os.path.join(DATA_DIR, "_manifest.json")

# how far back to step `m` between pages; also used to sanity-check spacing
TF_STEP = {"minute": pd.Timedelta(minutes=1), "quarter": pd.Timedelta(minutes=15),
           "hour": pd.Timedelta(hours=1), "day": pd.Timedelta(days=1)}


# ---------------------------------------------------------------------------
# Fetch
# ---------------------------------------------------------------------------

def fetch_page(tf, side, n=MAX_L, m=None, retries=3, timeout=60, instr=None):
    """One response. Returns a DataFrame, or None when the feed has nothing
    left (which is how the retention floor announces itself)."""
    url = BASE.format(tf=tf, instr=instr or INSTRUMENT, side=side, n=n)
    if m is not None:
        url += "&m=" + pd.Timestamp(m).tz_convert("UTC").strftime("%Y-%m-%dT%H:%M:%S")
    last_err = None
    for attempt in range(retries):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(req, timeout=timeout) as r:
                payload = json.loads(r.read().decode())
            break
        except Exception as e:                       # transient network/5xx
            last_err = e
            if attempt == retries - 1:
                raise
            time.sleep(2 ** attempt)
    rows = [line.split(",") for line in payload.get("data", [])]
    if not rows:
        return None
    df = pd.DataFrame(rows, columns=COLS)
    df["time"] = pd.to_datetime(df["time"], utc=True)
    for c in COLS[1:]:
        df[c] = pd.to_numeric(df[c], errors="coerce")
    return df.sort_values("time").reset_index(drop=True)


def collect_feed(tf, side, max_pages=40, sleep=0.25, verbose=True, instr=None):
    """Walk `m` backwards to the retention floor. Returns the union of pages.

    `m` is set to the earliest timestamp already seen rather than one step
    before it, so an off-by-one in the server's inclusivity cannot open a
    silent gap — any overlap is removed by the dedupe instead.
    """
    pages, m, earliest = [], None, None
    for page in range(max_pages):
        d = fetch_page(tf, side, MAX_L, m, instr=instr)
        if d is None or d.empty:
            if verbose:
                print(f"      page {page + 1}: retention floor reached")
            break
        if earliest is not None and d["time"].min() >= earliest:
            if verbose:
                print(f"      page {page + 1}: no further progress, stopping")
            break
        pages.append(d)
        earliest = d["time"].min()
        if verbose:
            print(f"      page {page + 1}: {len(d):>6,} bars  "
                  f"{d['time'].min()} -> {d['time'].max()}")
        if len(d) < MAX_L:                 # short page == start of available history
            break
        m = earliest
        time.sleep(sleep)
    if not pages:
        return None
    out = (pd.concat(pages, ignore_index=True)
             .drop_duplicates(subset="time", keep="first")
             .sort_values("time").reset_index(drop=True))
    # the newest bar is still forming — drop it, a later sync will settle it
    if len(out) > 1:
        out = out.iloc[:-1].reset_index(drop=True)
    return out


# ---------------------------------------------------------------------------
# Store
# ---------------------------------------------------------------------------

def store_path(tf, side, slug="uk100"):
    return os.path.join(DATA_DIR, f"{slug}_{tf}_{side}.csv")


def load_store(tf, side, slug="uk100"):
    p = store_path(tf, side, slug)
    if not os.path.exists(p):
        return None
    df = pd.read_csv(p)
    df["time"] = pd.to_datetime(df["time"], utc=True)
    return df.sort_values("time").reset_index(drop=True)


def merge_store(tf, side, new, slug="uk100"):
    """Union of stored and freshly fetched bars. Newly fetched values win on
    a timestamp collision (the feed may revise a bar); nothing is discarded."""
    old = load_store(tf, side, slug)
    before = 0 if old is None else len(old)
    merged = new if old is None else pd.concat([old, new], ignore_index=True)
    merged = (merged.drop_duplicates(subset="time", keep="last")
                    .sort_values("time").reset_index(drop=True))
    os.makedirs(DATA_DIR, exist_ok=True)
    merged.to_csv(store_path(tf, side, slug), index=False)
    return merged, len(merged) - before


def read_manifest():
    if os.path.exists(MANIFEST):
        with open(MANIFEST) as f:
            return json.load(f)
    return {}


def write_manifest(man):
    os.makedirs(DATA_DIR, exist_ok=True)
    with open(MANIFEST, "w") as f:
        json.dump(man, f, indent=2, sort_keys=True)


# ---------------------------------------------------------------------------
# Integrity
# ---------------------------------------------------------------------------

def check(df, tf):
    """Structural checks only — nothing is repaired or removed here."""
    o, h, l, c = df["open"], df["high"], df["low"], df["close"]
    issues = {
        "duplicate_timestamps": int(df["time"].duplicated().sum()),
        "not_sorted": int(not df["time"].is_monotonic_increasing),
        "nan_rows": int(df[COLS].isna().any(axis=1).sum()),
        "high_lt_low": int((h < l).sum()),
        "close_outside_hl": int(((c > h) | (c < l)).sum()),
        "open_outside_hl": int(((o > h) | (o < l)).sum()),
        "non_positive_price": int((df[["open", "high", "low", "close"]] <= 0).any(axis=1).sum()),
        "negative_volume": int((df["volume"] < 0).sum()),
        "zero_volume_pct": round(100.0 * (df["volume"] == 0).mean(), 2),
    }
    return issues


# ---------------------------------------------------------------------------
# Commands
# ---------------------------------------------------------------------------

def cmd_sync(a):
    man = read_manifest()
    slugs = list(INSTRUMENTS) if a.instr == ["all"] else a.instr
    for slug in slugs:
        iid = INSTRUMENTS[slug]
        print(f"\n=== {slug} (id {iid}) -> {DATA_DIR} ===")
        _sync_one(slug, iid, a, man)
    print("\nDone. `python3 collect.py status` for a summary.")


def _sync_one(slug, iid, a, man):
    for tf in a.tf:
        for side in a.sides:
            print(f"  {tf}/{side}:")
            try:
                new = collect_feed(tf, side, sleep=a.sleep, instr=iid)
            except Exception as e:
                print(f"      FAILED — {e}\n")
                continue
            if new is None:
                print("      nothing returned\n")
                continue
            merged, added = merge_store(tf, side, new, slug)
            bad = {k: v for k, v in check(merged, tf).items()
                   if k != "zero_volume_pct" and v}
            man[f"{slug}_{tf}_{side}"] = {
                "bars": int(len(merged)),
                "first": str(merged["time"].min()),
                "last": str(merged["time"].max()),
                "sessions": int(merged["time"].dt.date.nunique()),
                "last_sync_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
            }
            flag = f"  !! {bad}" if bad else ""
            print(f"      fetched {len(new):,} | +{added:,} new | store {len(merged):,} bars  "
                  f"{merged['time'].min().date()} -> {merged['time'].max().date()}{flag}\n")
            write_manifest(man)


def cmd_status(a):
    man = read_manifest()
    rows = []
    for slug in INSTRUMENTS:
      for tf in TFS:
        for side in SIDES:
            df = load_store(tf, side, slug)
            if df is None:
                continue
            meta = man.get(f"{slug}_{tf}_{side}", {})
            rows.append([slug, tf, side, len(df), df["time"].min().date(), df["time"].max().date(),
                         df["time"].dt.date.nunique(),
                         round(100.0 * (df["volume"] == 0).mean(), 1),
                         meta.get("last_sync_utc", "—")[:16]])
    if not rows:
        sys.exit("Store is empty — run `sync` first.")
    t = pd.DataFrame(rows, columns=["instr", "feed", "side", "bars", "from", "to",
                                    "sessions", "vol=0 %", "last sync"])
    pd.set_option("display.width", 200)
    print(t.to_string(index=False))

    for tf in TFS:
        b, ask = load_store(tf, "bid", "uk100"), load_store(tf, "ask", "uk100")
        if b is None or ask is None:
            continue
        j = b[["time", "close"]].merge(ask[["time", "close"]], on="time",
                                       suffixes=("_b", "_a"))
        if j.empty:
            continue
        sp = j["close_a"] - j["close_b"]
        hrs = j["time"].dt.hour
        core = sp[(hrs >= 7) & (hrs < 16)]
        print(f"\nspread ({tf}, n={len(sp):,}): median {sp.median():.2f} pts | "
              f"p90 {sp.quantile(0.9):.2f} | core 07:00-15:59 UTC median "
              f"{core.median():.2f} pts (n={len(core):,})")


def cmd_validate(a):
    ok = True
    for slug in INSTRUMENTS:
      for tf in TFS:
        for side in SIDES:
            df = load_store(tf, side, slug)
            if df is None:
                continue
            iss = check(df, tf)
            bad = {k: v for k, v in iss.items() if k != "zero_volume_pct" and v}
            step = TF_STEP[tf]
            gaps = df["time"].diff().dropna()
            over = int((gaps > step).sum())
            print(f"{slug}/{tf}/{side}: {len(df):,} bars | "
                  f"{'OK' if not bad else 'ISSUES ' + str(bad)} | "
                  f"zero-volume {iss['zero_volume_pct']}% | "
                  f"{over:,} gaps > one bar (weekends/closures expected)")
            ok = ok and not bad
    print("\nAll structural checks passed." if ok else "\nSee issues above.")


def main():
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("sync", help="page each feed back to its retention floor")
    p.add_argument("--instr", nargs="*", default=["uk100"],
                   choices=list(INSTRUMENTS) + ["all"])
    p.add_argument("--tf", nargs="*", default=TFS, choices=TFS)
    p.add_argument("--sides", nargs="*", default=SIDES, choices=SIDES)
    p.add_argument("--sleep", type=float, default=0.25, help="delay between requests")
    p.set_defaults(func=cmd_sync)

    p = sub.add_parser("status", help="summarise the store")
    p.set_defaults(func=cmd_status)

    p = sub.add_parser("validate", help="structural integrity checks")
    p.set_defaults(func=cmd_validate)

    a = ap.parse_args()
    a.func(a)


if __name__ == "__main__":
    main()
