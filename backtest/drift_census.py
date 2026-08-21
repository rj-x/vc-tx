"""Overnight/intraday drift census (register 51; pre-registered
prereg_drift_census). DESCRIPTIVE, our own data. Purpose, ordered:
grading-fairness first (do per-direction base rates need session-drift
awareness beyond the current session split?), drift hypothesis second —
front door only. PROVISIONAL stamps off-home; counts everywhere."""

import argparse
import json
import os
import subprocess
import sys

import numpy as np
import pandas as pd

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "scripts"))

from engine.store_loader import lockbox_boundary, zones
from backtest.sessions import sessions_of_index
from backtest.scoreboard import PROVISIONAL_INSTRS, PROVISIONAL_STAMP

OUT = os.path.join(ROOT, "reports", "scoreboard")


def _dist(a):
    a = [x for x in a if x == x]
    if not a:
        return None
    a = np.array(a)
    return {"n": len(a), "mean_bps": round(float(a.mean()) * 1e4, 2),
            "median_bps": round(float(np.median(a)) * 1e4, 2)}


def run_instrument(instr):
    import store as store_mod
    df = pd.read_csv(os.path.join(ROOT, "clean_finsa", f"{instr}_1min.csv"),
                     parse_dates=["time"]).set_index("time")
    tz = store_mod.SESSION_TZ.get(instr, "Europe/London")
    loc_date = df.index.tz_convert(tz).date
    cash = df[df["in_cash"]]
    boundary, gl = lockbox_boundary(), zones()["go_live"]

    # per native session: first open, last close
    sess = {}
    for d, g in cash.groupby(pd.Series(loc_date, index=df.index)[
            df["in_cash"]]):
        sess[d] = {"open_ts": g.index[0], "open": g["open"].iloc[0],
                   "close": g["close"].iloc[-1]}
    days = sorted(sess)
    rows = {"backtest": {"overnight": [], "intraday": []},
            "forward": {"overnight": [], "intraday": []}}
    for i, d in enumerate(days):
        w = ("backtest" if sess[d]["open_ts"] < boundary else
             "forward" if sess[d]["open_ts"] >= gl else None)
        if w is None:
            continue
        rows[w]["intraday"].append(
            sess[d]["close"] / sess[d]["open"] - 1)
        if i > 0:
            rows[w]["overnight"].append(
                sess[d]["open"] / sess[days[i - 1]]["close"] - 1)

    # per-partition-session 1M drift
    idx = df.index
    ses = sessions_of_index(idx)
    ret = df["close"].pct_change().to_numpy()
    per_sess = {}
    for w, lo, hi in (("backtest", pd.Timestamp.min.tz_localize("UTC"),
                       boundary),
                      ("forward", gl, pd.Timestamp.max.tz_localize("UTC"))):
        m = (idx >= lo) & (idx < hi)
        per_sess[w] = {s: _dist(ret[m & (ses == s)])
                       for s in ("london", "overlap", "ny_only", "dead",
                                 "asia")}
    return {"instrument": instr,
            "status": ("provisional" if instr in PROVISIONAL_INSTRS
                       else "canonical"),
            "overnight_vs_intraday": {
                w: {k: _dist(v) for k, v in per.items()}
                for w, per in rows.items()},
            "per_session_1m_drift": per_sess}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--instr", nargs="*",
                    default=["uk100fut", "ger40fut", "nas100fut", "us30fut"])
    a = ap.parse_args()
    os.makedirs(OUT, exist_ok=True)
    head = subprocess.run(["git", "rev-parse", "HEAD"], cwd=ROOT,
                          capture_output=True, text=True).stdout.strip()
    results = [run_instrument(i) for i in a.instr]
    art = {"STAMP": "OBSERVATIONAL drift census — descriptive; "
                    "grading-fairness first; never validation",
           "engine_commit": head, "results": results}
    with open(os.path.join(OUT, "drift_census.json"), "w") as f:
        json.dump(art, f, indent=2, default=str)
    L = ["# Overnight/Intraday Drift Census (GENERATED)", "",
         f"Engine `{head[:9]}` — {art['STAMP']}", ""]
    for res in results:
        L += [f"## {res['instrument']} ({res['status'].upper()})"]
        if res["status"] == "provisional":
            L += [f"> {PROVISIONAL_STAMP}"]
        L += ["", "| window | leg | n | mean bps | median bps |",
              "|---|---|---|---|---|"]
        for w, per in res["overnight_vs_intraday"].items():
            for leg, d in per.items():
                if d:
                    L.append(f"| {w} | {leg} | {d['n']} | {d['mean_bps']} "
                             f"| {d['median_bps']} |")
        L += ["", "| window | session | n (1M bars) | mean bps/bar |",
              "|---|---|---|---|"]
        for w, per in res["per_session_1m_drift"].items():
            for s, d in per.items():
                if d:
                    L.append(f"| {w} | {s} | {d['n']} | {d['mean_bps']} |")
        L.append("")
    with open(os.path.join(OUT, "drift_census.md"), "w") as f:
        f.write("\n".join(L))
    print(f"OBSERVATIONAL drift census -> {OUT}/drift_census.md")


if __name__ == "__main__":
    main()
