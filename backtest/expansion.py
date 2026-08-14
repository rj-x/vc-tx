"""Expansion event study — OBSERVATIONAL instrumentation (working set only).

For every exec-TF signature moment (1min SPRING/UPTHRUST print): forward
realized range and max up/down excursions at +5/+15/+30 1min bars, vs
matched same-segment baseline bars. Direction-agnostic by construction
(drift-irrelevant). Location splits use the ledger's columns
(dist_signal_atr / location_ref) — no parallel location logic. Measured
spread is stated in the same point units alongside. Cross-ref: candidate
register, signature-moment expansion bracket entry (walk-forward evidence).
"""

import numpy as np

HORIZONS = (5, 15, 30)
NOMINAL_BUFFER_PTS = 0.5    # chop-rate nominal bracket buffer (1 tick), stated


def _bucket(d):
    if d is None or d == "":
        return "unknown"
    d = abs(float(d))
    return "at_extreme" if d <= 0.25 else ("near" if d <= 1.0 else "far")


def expansion_study(events, exec_bars, exec_tf, median_spread_pts):
    bars = [b for b in exec_bars if not b.is_stub]
    hi = np.array([b.high for b in bars])
    lo = np.array([b.low for b in bars])
    cl = np.array([b.close for b in bars])
    segs = np.array([b.segment for b in bars])
    ts_ix = {b.ts: i for i, b in enumerate(bars)}
    n = len(bars)

    def stats(i, k):
        j = min(i + k, n - 1)
        if j <= i:
            return None
        w_hi, w_lo = hi[i + 1:j + 1].max(), lo[i + 1:j + 1].min()
        return {"range": w_hi - w_lo, "up": w_hi - cl[i], "dn": cl[i] - w_lo}

    # (1) matched-volatility pools: trailing-5-bar realized range quintiles
    # per segment, signature-labeled bars excluded from pools
    vol = np.full(n, np.nan)
    for i in range(5, n):
        vol[i] = hi[i - 4:i + 1].max() - lo[i - 4:i + 1].min()
    sig_ix = {ts_ix[e["ts"]] for e in events
              if e["type"] == "LABEL" and e.get("tf") == exec_tf
              and e.get("label") in ("SPRING", "UPTHRUST")
              and e["ts"] in ts_ix}
    quint = {}
    matched_base = {}
    for seg in set(segs):
        pool = [i for i in np.nonzero(segs == seg)[0]
                if i >= 5 and i not in sig_ix]
        if len(pool) < 50:
            continue
        vals = vol[pool]
        edges = np.quantile(vals, [0.2, 0.4, 0.6, 0.8])
        quint[seg] = edges
        # assign quintiles vectorized
        qs = np.searchsorted(edges, vals)
        for q in range(5):
            qi = [pool[j] for j in np.nonzero(qs == q)[0]]
            if len(qi) > 1500:
                qi = list(np.random.default_rng(1).choice(qi, 1500,
                                                          replace=False))
            for k in HORIZONS:
                v2 = [stats(i, k)["range"] for i in qi if stats(i, k)]
                matched_base[(seg, q, k)] = (float(np.mean(v2)) if v2
                                             else None)

    groups = {}
    for e in events:
        if (e["type"] != "LABEL" or e.get("tf") != exec_tf
                or e.get("label") not in ("SPRING", "UPTHRUST")):
            continue
        i = ts_ix.get(e["ts"])
        if i is None:
            continue
        key = (e.get("segment", "cash"), _bucket(e.get("dist_signal_atr")))
        seg = e.get("segment", "cash")
        q = (int(np.searchsorted(quint[seg], vol[i]))
             if seg in quint and vol[i] == vol[i] else None)
        sig_hi, sig_lo = e.get("high"), e.get("low")
        for k in HORIZONS:
            st = stats(i, k)
            if st:
                st["matched"] = matched_base.get((seg, q, k))
                # (2) chop: both bracket legs (sig extreme +/- nominal
                # buffer) exceeded within the horizon = double-trigger
                j = min(i + k, n - 1)
                if sig_hi is not None and j > i:
                    buf = NOMINAL_BUFFER_PTS
                    st["chop"] = bool(hi[i + 1:j + 1].max() >= sig_hi + buf
                                      and lo[i + 1:j + 1].min() <= sig_lo - buf)
                groups.setdefault(key, {}).setdefault(k, []).append(st)

    # same-segment baselines over ALL bars (direction-agnostic magnitudes)
    base = {}
    rng = np.random.default_rng(0)
    for seg in set(segs):
        idxs = np.nonzero(segs == seg)[0]
        if len(idxs) > 3000:
            idxs = rng.choice(idxs, 3000, replace=False)
        for k in HORIZONS:
            vals = [stats(i, k)["range"] for i in idxs if stats(i, k)]
            base[f"{seg}_{k}"] = {"mean_range": round(float(np.mean(vals)), 2),
                                  "n": len(vals)} if vals else None

    out = {"note": "OBSERVATIONAL - working set only; direction-agnostic; "
                   "location splits from ledger columns; matched baseline = "
                   "same-segment trailing-5-bar realized-range quintile, "
                   "signature bars excluded; chop = both bracket legs "
                   f"(sig extreme +/- {NOMINAL_BUFFER_PTS} pt nominal buffer) "
                   "hit within horizon (double-trigger, the -2R failure mode)",
           "median_spread_pts": median_spread_pts,
           "baseline_same_segment": base, "by_segment_and_location": {}}
    for (seg, buck), ks in sorted(groups.items()):
        entry = {}
        for k, vals in ks.items():
            mr = float(np.mean([v["range"] for v in vals]))
            mm = [v["matched"] for v in vals if v.get("matched")]
            chops = [v["chop"] for v in vals if "chop" in v]
            entry[f"h{k}"] = {
                "n": len(vals),
                "mean_range": round(mr, 2),
                "median_range": round(float(np.median([v["range"] for v in vals])), 2),
                "mean_up_excursion": round(float(np.mean([v["up"] for v in vals])), 2),
                "mean_dn_excursion": round(float(np.mean([v["dn"] for v in vals])), 2),
                "matched_vol_baseline_range": (round(float(np.mean(mm)), 2)
                                               if mm else None),
                "delta_vs_matched_pct": (round(100 * (mr / np.mean(mm) - 1), 1)
                                         if mm else None),
                "chop_rate": (round(float(np.mean(chops)), 3)
                              if chops else None),
            }
        out["by_segment_and_location"][f"{seg} [{buck}]"] = entry
    return out
