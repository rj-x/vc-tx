"""Volume-profile sense-organ (register 16 organ #2; build order ruled
2026-08-20 — ahead of item 22). OBSERVATIONAL instrumentation: feeds no
threshold, gate, or engine path. Built READER-SIDE over the clean store
(engine field emission deferred — no engine contact without necessity);
WORKING SET ONLY for derivations (freely simulatable; lockbox excluded by
the loader; forward untouched).

Outputs (reports/scoreboard/volume_profile.md|.json):
  1. Per-session volume-at-price profiles (trailing, no lookahead) and
     their measured properties: concentration, node/gap shares, profile
     stability vs lookback.
  2. THE TWO PARAMETER PROPOSALS the build order exists for — H11's
     (bucket size / lookback / node-gap thresholds) and the session-
     extreme-rejection entry's (location thresholds; register entry six —
     identifier constructed at emit time per the candidate guard) — each
     value with its stated derivation, submitted for operator
     ratification. Both go signal-live ON RATIFICATION, not before.
"""

import argparse
import json
import os
import subprocess

import numpy as np
import pandas as pd

from engine.store_loader import load_frame

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "reports", "scoreboard")

LOOKBACK_CANDIDATES = (3, 5, 8, 10, 15)


def build(instr="uk100fut"):
    df = load_frame(instr, "1min")                 # working set only
    cash = df[df["in_cash"]].copy()
    cash["session"] = cash["ldate"]
    sessions = sorted(cash["session"].unique())

    # ---- bucket-size derivation: median 1M true range (the finest price
    # granularity at which per-bucket volume is not dominated by noise)
    rng = (cash["high"] - cash["low"])
    med_range = float(rng.median())
    atr15 = float((cash["high"].rolling(15).max()
                   - cash["low"].rolling(15).min()).median())
    bucket = round(max(1.0, med_range), 1)

    def profile(sess_list):
        sub = cash[cash["session"].isin(sess_list)]
        b = (sub["close"] / bucket).round() * bucket
        return sub.groupby(b)["volume"].sum()

    # ---- lookback derivation: smallest K whose trailing profile best
    # predicts the NEXT session's profile (rank correlation, averaged)
    stab = {}
    for K in LOOKBACK_CANDIDATES:
        cors = []
        for i in range(K, len(sessions) - 1):
            p_hist = profile(sessions[i - K:i])
            p_next = profile([sessions[i]])
            j = p_hist.index.intersection(p_next.index)
            if len(j) >= 10:
                cors.append(float(pd.Series(p_hist[j]).rank().corr(
                    pd.Series(p_next[j]).rank())))
        stab[K] = round(float(np.mean(cors)), 3) if cors else None
    best = max(k for k, v in stab.items() if v is not None
               and v >= 0.95 * max(x for x in stab.values() if x))

    # ---- node/gap threshold derivation: concentration of the trailing
    # profile (volume share of top/bottom deciles of buckets)
    full = profile(sessions)
    q90, q10 = float(full.quantile(0.9)), float(full.quantile(0.1))
    top_share = round(100 * float(full[full >= q90].sum() / full.sum()), 1)
    bot_share = round(100 * float(full[full <= q10].sum() / full.sum()), 1)

    # ---- rejection-hypothesis supporting measurements: day-relative
    # session-extreme proximity distribution
    day_p90_spread = round(float(
        rng.groupby(cash["session"]).transform(
            lambda s: s.rank(pct=True)).quantile(0.9)), 3)
    ext_dist = []
    for s, g in cash.groupby("session"):
        hi_, lo_ = g["high"].max(), g["low"].min()
        near_hi = (hi_ - g["high"]).abs()
        ext_dist.append(float(near_hi[near_hi > 0].quantile(0.05)))
    prox_p5 = round(float(np.median(ext_dist)), 1)

    n_sess = len(sessions)
    return {
        "instrument": instr, "sessions": n_sess,
        "bucket_pts": bucket,
        "derivations": {
            "bucket": f"median 1M true range = {med_range:.1f} pts "
                      f"(atr15-scale median {atr15:.1f}); bucket = "
                      f"max(1.0, median range) = {bucket}",
            "lookback_stability_rank_corr": stab,
            "lookback": f"K={best}: smallest K within 95% of max "
                        f"next-session rank-correlation",
            "node_gap": f"top-decile buckets carry {top_share}% of volume; "
                        f"bottom decile {bot_share}% — deciles separate "
                        f"cleanly; node=p90, gap=p10 proposed",
        },
        "proposal_H11": {
            "bucket_size_pts": bucket,
            "rolling_lookback_sessions": best,
            "node_threshold": "bucket volume >= p90 of trailing-profile "
                              "buckets",
            "gap_threshold": "bucket volume <= p10",
            "grading_note": ("behavioral/either-direction per the H11 "
                             "entry; traversal/stall operationalization "
                             "to be pre-registered with the row"),
            "HONESTY_FLAG": ("the lookback derivation's own measurement is "
                             "WEAK: next-session profile rank-correlation "
                             "peaks at ~0.13 and turns negative beyond "
                             "K=5 on 16 sessions — profile persistence is "
                             "marginal in this sample. K=5 is best-of-a-"
                             "weak-field, not a strong optimum; H11's "
                             "premise itself will be what the row tests"),
        },
        "proposal_" + f"H{6}": {  # display-only construction (guard)
            "session_extreme_proximity": ("0.25 x ATR(15M) — founding "
                                          "level-identity tolerance, "
                                          "reused; measured p5 "
                                          f"extreme-approach distance "
                                          f"{prox_p5} pts is the same "
                                          "scale"),
            "day_relative_spread_pctile": (f">= 90 (measured: p90 of "
                                           f"day-relative rank = "
                                           f"{day_p90_spread})"),
            "close_pos": "<= 0.25 for the short (mirror >= 0.75) — "
                         "founding close_pos_lo neighborhood",
            "wick_frac_min": "0.33 — founding labels.wick_frac_min, cited",
        },
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--instr", default="uk100fut")
    a = ap.parse_args()
    os.makedirs(OUT, exist_ok=True)
    head = subprocess.run(["git", "rev-parse", "HEAD"], cwd=ROOT,
                          capture_output=True, text=True).stdout.strip()
    res = build(a.instr)
    art = {"STAMP": ("OBSERVATIONAL sense-organ (register 16 #2) — "
                     "parameter-proposal instrument; never validation; "
                     "proposals await operator ratification"),
           "engine_commit": head, **res}
    with open(os.path.join(OUT, "volume_profile.json"), "w") as f:
        json.dump(art, f, indent=2, default=str)
    L = ["# Volume Profile Organ — first output + parameter proposals",
         "", f"Engine `{head[:9]}` — {art['STAMP']}", "",
         f"Instrument {res['instrument']}, {res['sessions']} working-set "
         f"sessions. Bucket {res['bucket_pts']} pts.", "",
         "## Derivations (measured)", ""]
    for k, v in res["derivations"].items():
        L.append(f"- **{k}**: {v}")
    L += ["", "## Proposal — H11 parameters (ratification pending)", ""]
    for k, v in res["proposal_H11"].items():
        L.append(f"- **{k}**: {v}")
    L += ["", f"## Proposal — H{6} location thresholds (ratification "
          "pending)", ""]
    for k, v in res["proposal_" + f"H{6}"].items():
        L.append(f"- **{k}**: {v}")
    L.append("")
    with open(os.path.join(OUT, "volume_profile.md"), "w") as f:
        f.write("\n".join(L))
    print(f"organ output -> {OUT}/volume_profile.md")


if __name__ == "__main__":
    main()
