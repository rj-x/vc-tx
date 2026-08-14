#!/usr/bin/env python3
"""Feed-contract probe (2026-08-14 amendment): MEASURE, don't recall.

Polls the RAW minute endpoint every ~10s for a 15-20 min window (run during
Monday's cash open), logging full raw pages UNTOUCHED (pre-sort, exactly as
served) to logs/feed_probe/<date>.jsonl. Answers absolutely:
  (a) which index holds the forming bar vs last closed, across boundaries;
  (b) whether that bar's volume accrues between same-minute polls (forming);
  (c) whether deeper-index bars ever change after appearing settled
      (true post-close revision — distinct from forming).
No store writes, no engine feed — capture only. ~90-120 requests in the
window; well within the collector's observed tolerance, single endpoint.

Usage: venv/bin/python scripts/feed_probe.py [--minutes 18] [--instr uk100fut]
"""
import argparse, json, os, sys, time, urllib.request
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from collect import BASE, INSTRUMENTS
from paths import ROOT

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--minutes", type=int, default=18)
    ap.add_argument("--instr", default="uk100fut")
    ap.add_argument("--rows", type=int, default=6)
    a = ap.parse_args()
    out_dir = os.path.join(ROOT, "logs", "feed_probe")
    os.makedirs(out_dir, exist_ok=True)
    out = os.path.join(out_dir, time.strftime("%Y-%m-%d_%H%M") + ".jsonl")
    url = BASE.format(tf="minute", instr=INSTRUMENTS[a.instr], side="mid",
                      n=a.rows)
    end = time.time() + a.minutes * 60
    n = 0
    with open(out, "a") as f:
        while time.time() < end:
            try:
                req = urllib.request.Request(url,
                                             headers={"User-Agent": "Mozilla/5.0"})
                with urllib.request.urlopen(req, timeout=30) as r:
                    payload = json.loads(r.read().decode())
                # UNTOUCHED: raw row strings in served order, no sort/parse
                f.write(json.dumps({"poll_utc": time.time(),
                                    "raw_rows": payload.get("data", [])}) + "\n")
                f.flush()
                n += 1
            except Exception as e:
                f.write(json.dumps({"poll_utc": time.time(),
                                    "error": str(e)}) + "\n")
            time.sleep(10)
    print(f"{n} polls captured -> {out}\nAnalyze: index position of newest "
          f"row, same-minute volume accrual, deeper-row mutations.")

if __name__ == "__main__":
    main()
