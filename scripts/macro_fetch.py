#!/usr/bin/env python3
"""Forward-population of the macro release calendar (takes over from the
manual backfill after 2026-08-19).

Source: ForexFactory's official machine-readable feed via FairEconomy —
ff_calendar_thisweek.json ONLY (the nextweek variant does not exist; 404
confirmed 2026-08-12), with cdn-nfs.faireconomy.media as fallback mirror.
Deliberately NOT the forexfactory.com HTML (ToS, Cloudflare, and
session-dependent timezone rendering — the silent-mistagging failure mode
this design avoids).

Operational contract:
- Run alongside the daily sync. Each fetch covers the full current week;
  staging UPSERTS on (utc_time, name), so repeated daily fetches are
  idempotent and any one successful run per week suffices.
- The feed is rate-limited (2 requests / 5 min) and returns a "Request
  Denied" HTML page WITH NO ERROR STATUS when exceeded: the response must
  parse as JSON before staging is touched; HTML/non-JSON = failed fetch
  (log, exit nonzero, never write). Exactly one request per run, one retry
  via the mirror on failure — nothing more aggressive.
- Writes data/macro_releases_staging.csv ONLY. The human merge gate into
  the live file is deliberate and stays. Staged output must pass the same
  validation as the live calendar (engine.macro, NFP anchor included).

Usage: venv/bin/python scripts/macro_fetch.py
"""

import json
import os
import sys
import urllib.request

import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from engine.macro import load_and_validate          # noqa: E402
from paths import ROOT                              # noqa: E402

PRIMARY = "https://nfs.faireconomy.media/ff_calendar_thisweek.json"
MIRROR = "https://cdn-nfs.faireconomy.media/ff_calendar_thisweek.json"
STAGING = os.path.join(ROOT, "data", "macro_releases_staging.csv")


def fetch_json(url):
    """One request. Returns parsed JSON list or raises — a rate-limit
    'Request Denied' HTML page arrives with 200, so JSON-parseability IS
    the success check."""
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=60) as r:
        raw = r.read().decode()
    data = json.loads(raw)                  # non-JSON (HTML) raises here
    if not isinstance(data, list):
        raise ValueError(f"unexpected payload shape: {type(data)}")
    return data


def main():
    data = None
    for url in (PRIMARY, MIRROR):           # one request + one mirror retry
        try:
            data = fetch_json(url)
            print(f"fetched {url}: {len(data)} events")
            break
        except Exception as e:
            print(f"WARN: fetch failed {url}: {e}")
    if data is None:
        sys.exit("FETCH FAILED on primary and mirror — staging untouched")

    rows = []
    for ev in data:                       # CAPTURE-ALL (2026-08-14): every
        ts = pd.Timestamp(ev["date"])     # currency and impact is staged;
        if ts.tzinfo is None:             # consumption filters per instrument
            sys.exit(f"REFUSING offset-less timestamp: {ev} — staging untouched")
        rows.append({"utc_time": ts.tz_convert("UTC").strftime("%Y-%m-%dT%H:%M:%SZ"),
                     "currency": ev["country"],
                     "impact": ev.get("impact", ""),
                     "name": ev.get("title", "").strip(),
                     "forecast": ev.get("forecast", ""),   # staging-only cols;
                     "previous": ev.get("previous", "")})  # live file stays lean
    new = pd.DataFrame(rows, columns=["utc_time", "currency", "impact",
                                      "name", "forecast", "previous"])
    print(f"captured {len(new)} (all currencies/impacts)")

    # upsert into staging on (utc_time, name): fresh rows win, prior weeks kept
    if os.path.exists(STAGING):
        old = pd.read_csv(STAGING)
        merged = pd.concat([old, new], ignore_index=True)
    else:
        merged = new
    merged = (merged.drop_duplicates(subset=["utc_time", "name"], keep="last")
                    .sort_values(["utc_time", "currency", "name"], kind="stable")
                    .reset_index(drop=True))
    merged.to_csv(STAGING, index=False)

    load_and_validate(STAGING)              # same bar as the live calendar
    print(f"\nStaging: {len(merged)} rows ({len(new)} upserted) -> {STAGING} "
          f"(validated).")
    print("\nStaged rows by currency/impact (merge-gate view):")
    for (cur, imp), g in merged.groupby(["currency", "impact"]):
        print(f"  {cur}/{imp}: {len(g)}")
        for _, r in g.iterrows():
            print(f"    {r['utc_time']} {r['name'][:60]}")
    print("\nReview and merge into data/macro_releases.csv by hand "
          "(live file schema: utc_time,currency,impact,name — drop "
          "forecast/previous at merge) — this script never touches the "
          "live file.")


if __name__ == "__main__":
    main()
