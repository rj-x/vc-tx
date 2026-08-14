"""Migration event log + study — OBSERVATIONAL (working set only).

Migration event on adjacent TF pair (i -> i+1): (a) PERSISTENCE — >= N
same-direction structural labels on TF(i) accruing within a single
not-yet-closed TF(i+1) bar (a single lower-TF label never counts);
(b) the TF(i+1) bar closes with a same-direction structural label;
(c) RECRUITMENT — the TF(i+1) bar closes with rel_volume >= floor vs its
session-time bin (participation must expand at the parent).

No look-ahead: (a) uses only closed TF(i) bars; the chain timestamp is the
TF(i+1) close. Chains span consecutive rungs with matching direction.
Study: drift-adjusted forward returns after k-rung chains vs same-segment
baselines; recruitment-passing vs recruitment-failing chains reported
SEPARATELY (the falsifiable second clause of the candidate register's
timeframe-pressure-migration entry must be able to die as-written).
Non-evidential; feeds no thresholds or rules before walk-forward.
"""

import numpy as np
import pandas as pd

from backtest.eventstudy import LABEL_DIR

LADDER = ["1min", "3min", "5min", "15min", "30min", "1h"]
_MIN = {"1min": 1, "3min": 3, "5min": 5, "15min": 15, "30min": 30, "1h": 60}
HORIZONS = (5, 10, 20)


def _labels_by_tf(events):
    out = {tf: [] for tf in LADDER}
    for e in events:
        tf = e.get("tf")
        if e["type"] == "LABEL" and tf in out and e.get("structural"):
            d = LABEL_DIR.get(e["structural"], 0)
            if d:
                out[tf].append({"ts": pd.Timestamp(e["ts"]), "dir": d,
                                "seg": e.get("segment", "cash"),
                                "rv": e.get("rel_volume")})
    return out


def migration_events(events, cfg):
    lbl = _labels_by_tf(events)
    n_req = cfg.migration.min_child_labels
    floor = cfg.migration.recruitment_floor
    evs = []
    for i in range(len(LADDER) - 1):
        child, parent = LADDER[i], LADDER[i + 1]
        pm = pd.Timedelta(minutes=_MIN[parent])
        for p in lbl[parent]:
            window_lo = p["ts"] - pm
            kids = [c for c in lbl[child]
                    if window_lo < c["ts"] <= p["ts"] and c["dir"] == p["dir"]]
            if len(kids) >= n_req:                      # (a) + (b)
                evs.append({"pair": f"{child}->{parent}", "rung": i + 1,
                            "ts": p["ts"], "dir": p["dir"], "seg": p["seg"],
                            "n_child": len(kids),
                            "recruited": bool(p["rv"] and p["rv"] >= floor),
                            "recruitment_margin": (round(p["rv"] - floor, 2)
                                                   if p["rv"] else None)})
    # chains: consecutive rungs, matching direction, child event inside the
    # next parent's window
    evs.sort(key=lambda e: (e["rung"], e["ts"]))
    for e in evs:
        e["chain_rungs"] = 1
        prev = [x for x in evs
                if x["rung"] == e["rung"] - 1 and x["dir"] == e["dir"]
                and e["ts"] - pd.Timedelta(minutes=_MIN[e["pair"].split("->")[1]])
                < x["ts"] <= e["ts"]]
        if prev:
            e["chain_rungs"] = max(x["chain_rungs"] for x in prev) + 1
    return evs


def migration_study(evs, signal_bars):
    bars = [b for b in signal_bars if not b.is_stub]
    cl = np.array([b.close for b in bars])
    ts_ix = {b.ts: i for i, b in enumerate(bars)}
    segs = np.array([b.segment for b in bars])
    drift = {}
    for seg in set(segs):
        for k in HORIZONS:
            rs = [(cl[i + k] - cl[i]) / cl[i]
                  for i in np.nonzero(segs == seg)[0] if i + k < len(cl)]
            drift[(seg, k)] = float(np.mean(rs)) if rs else 0.0
    rows = []
    for e in evs:
        i = ts_ix.get(e["ts"])
        if i is None:                      # chain top not on Signal TF grid
            continue
        r = dict(e)
        for k in HORIZONS:
            if i + k < len(cl):
                raw = (cl[i + k] - cl[i]) / cl[i] * e["dir"]
                r[f"exc_{k}_bps"] = round(
                    (raw - drift[(e["seg"], k)] * e["dir"]) * 1e4, 1)
        rows.append(r)
    out = {"note": "OBSERVATIONAL migration study - non-evidential; "
                   "recruitment-passing vs -failing reported separately",
           "n_events": len(evs), "n_on_signal_grid": len(rows), "groups": {}}
    df = pd.DataFrame(rows)
    if df.empty:
        return out
    for (rc, rec, seg), g in df.groupby(["chain_rungs", "recruited", "seg"]):
        key = f"rungs{rc}_{'recruited' if rec else 'unrecruited'}_{seg}"
        entry = {"n": len(g)}
        for k in HORIZONS:
            col = g.get(f"exc_{k}_bps")
            if col is not None and col.dropna().size:
                entry[f"exc_{k}_bps_mean"] = round(float(col.dropna().mean()), 1)
        out["groups"][key] = entry
    return out
