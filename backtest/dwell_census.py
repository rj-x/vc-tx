"""Organ #5 — dwell-time at levels (register 120; pre-registered
prereg_organ_dwell, counted 2026-08-31; register-16 organ, session
order item 4; dispositions register 115). OBSERVATIONAL VOCABULARY —
auction acceptance vs touch: how long price DWELLS at a level once it
arrives, per level-touch episode. No signal, question or recipe
changes; distributions are the vocabulary's range, not findings.

LEVEL CLASSES (every definition an existing registered convention):
- session-extreme — the running session extreme BEFORE the bar (and
  the prior session's), in-band at |close - level| <= the ratified
  retest band (H6_PROX_ATR_FRAC x ATR(15M)); the retest-anchor level object (the H20 companion shares it);
- h11-node — the volume-profile node state (the conditioning matrix's
  h11 dimension, same _Profile machinery);
- v3-zone-4h / v3-zone-1d — inside a zone-census-v3 anchor-rung zone's
  range (register 111 objects).

EPISODE = a maximal run of consecutive in-band 1M closes, broken at
UTC-day changes (a dwell across the overnight gap is not an auction);
DWELL = the run's length in bars. Per class x leg x window: episode
counts, dwell median / p75 / p90 / max, in-band bar share.

CUSTOMERS (named at registration): H12's clauses (visit definition —
its vocabulary was never built, register 115), arrival-anatomy (e)
(reversal-print clustering needs the visit unit), the location family.
H12's re-registration stays a FUTURE OPERATOR PROPOSAL. Twin-run
pinned (tests/test_organs.py). Weekly under Part C.
"""

import argparse
import json
import os
import subprocess
import sys

import numpy as np
import pandas as pd

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "scripts"))

from engine.signal_watch import H6_PROX_ATR_FRAC, SignalWatch
from engine.store_loader import is_sealed, lockbox_boundary, zones
from backtest.recipes import build_env
from backtest.scoreboard import _replay, make_cfg
from backtest.location_census import _Profile
from backtest.zone_census_v3 import (DEPART_MULTS, SOURCE_TFS,
                                     departure_bases, source_frame,
                                     tag_bars_v3)

OUT = os.path.join(ROOT, "reports", "scoreboard")


def dwell_episodes(state, days, wmask):
    """Maximal runs of consecutive True, broken at day changes;
    returns run lengths keyed by the window of the run's FIRST bar."""
    out = {w: [] for w in wmask}
    n = len(state)
    i = 0
    while i < n:
        if not state[i]:
            i += 1
            continue
        j = i
        while j + 1 < n and state[j + 1] and days[j + 1] == days[i]:
            j += 1
        for w, m in wmask.items():
            if m[i]:
                out[w].append(j - i + 1)
        i = j + 1
    return out


def session_extreme_band(b1m, atr15):
    """In-band at the PRE-BAR session extremes (running + prior
    session) within the ratified retest band — the retest-anchor level
    object, close-tested."""
    n = len(b1m)
    out = np.zeros(n, dtype=bool)
    st = None
    for i, bar in enumerate(b1m):
        if st is None or st["sid"] != bar.session_id:
            st = {"sid": bar.session_id, "hi": bar.high, "lo": bar.low,
                  "prior_hi": st["hi"] if st else None,
                  "prior_lo": st["lo"] if st else None}
            pre_hi = pre_lo = None
            new = st
        else:
            pre_hi, pre_lo = st["hi"], st["lo"]
            st["hi"] = max(st["hi"], bar.high)
            st["lo"] = min(st["lo"], bar.low)
            new = st
        st = new
        a = atr15[i]
        if not a or np.isnan(a):
            continue
        band = H6_PROX_ATR_FRAC * a
        levels = [x for x in (pre_hi, st["prior_hi"], pre_lo,
                              st["prior_lo"]) if x is not None]
        out[i] = any(abs(bar.close - lv) <= band for lv in levels)
    return out


def _dist(runs):
    if not runs:
        return None
    v = np.array(runs, float)
    return {"episodes": int(len(v)),
            "dwell_median": round(float(np.median(v)), 1),
            "dwell_p75": round(float(np.percentile(v, 75)), 1),
            "dwell_p90": round(float(np.percentile(v, 90)), 1),
            "dwell_max": int(v.max()),
            "bars_in_band": int(v.sum())}


def run_instrument(instr):
    cfg = make_cfg({"session_model.extended_hours": True,
                    "session_model.ladder": True,
                    "debug.structure": True})
    watch = SignalWatch()
    engine, bars, _ = _replay(cfg, instr, engine_hook=watch.attach)
    env = build_env(instr, cfg, bars)
    b1m = [x for x in bars[cfg.mtf.execution_tf] if not x.is_stub]
    ts = np.array([x.ts.value for x in b1m])
    cl = np.array([x.close for x in b1m])
    atr15 = np.array([env.atr_at("15min", t) or np.nan for t in ts])
    days = ts // 86_400_000_000_000
    day_ts = pd.DatetimeIndex(pd.to_datetime(ts, utc=True))
    sealed_days = {d: bool(is_sealed(pd.Timestamp(d)))
                   for d in day_ts.normalize().unique()}
    unsealed = ~np.array([sealed_days[d] for d in day_ts.normalize()])
    boundary, gl = lockbox_boundary(), zones()["go_live"]
    wmask = {"backtest": (ts < boundary.value) & unsealed,
             "forward": (ts >= gl.value) & unsealed}
    k = int(cfg.context.swing_k)
    period = int(cfg.context.atr_period)
    classes = {}
    classes["session-extreme"] = session_extreme_band(b1m, atr15)
    prof = _Profile()
    classes["h11-node"] = np.array(
        [(prof.feed(x) or "unclassified") == "node" for x in b1m])
    for tf in SOURCE_TFS:
        zs = departure_bases(source_frame(instr, tf), k, period,
                             DEPART_MULTS[0])
        classes[f"v3-zone-{tf}"] = tag_bars_v3(ts, cl, zs) >= 0
    out = {"instrument": instr, "n_bars": int(len(ts)), "classes": {}}
    for cname, state in classes.items():
        runs = dwell_episodes(state, days, wmask)
        for w in wmask:
            d = _dist(runs[w])
            total = int(wmask[w].sum())
            out["classes"][f"{cname}|{w}"] = {
                **(d or {"episodes": 0}),
                "in_band_bar_share": (round(d["bars_in_band"] / total, 4)
                                      if d and total else 0.0)}
    return out


def _emit(art, head):
    L = ["# Organ #5 — Dwell-Time at Levels (GENERATED by "
         "backtest.dwell_census)", "",
         "Terms: [docs/GLOSSARY.md](../../docs/GLOSSARY.md).", "",
         f"Engine `{head[:9]}` — OBSERVATIONAL ORGAN (register 120; "
         "prereg_organ_dwell; register-16 family). VOCABULARY, not a "
         "signal: auction acceptance vs touch — dwell = consecutive "
         "in-band 1M closes per level-touch episode (day-broken). "
         "Level classes from existing conventions only: the pre-bar "
         "session extremes in the ratified retest band "
         f"({H6_PROX_ATR_FRAC:g}xATR15 — the retest-anchor object), the "
         "matrix's h11-node state, and the v3 anchor zones (register "
         "111). Customers: H12's visit definition (future operator "
         "proposal), arrival-anatomy (e), the location family. "
         "Consumers price their own fields; distributions are the "
         "vocabulary's range, not findings.", ""]
    for res in art["results"]:
        L += [f"## {res['instrument']} ({res['n_bars']} 1M bars)", "",
              "| class | window | episodes | dwell med | p75 | p90 "
              "| max | in-band bar share |",
              "|---|---|---|---|---|---|---|---|"]
        for key, c in res["classes"].items():
            cname, w = key.split("|")
            if not c["episodes"]:
                L.append(f"| {cname} | {w} | 0 | — | — | — | — | 0 |")
                continue
            L.append(f"| {cname} | {w} | {c['episodes']} "
                     f"| {c['dwell_median']:g} | {c['dwell_p75']:g} "
                     f"| {c['dwell_p90']:g} | {c['dwell_max']} "
                     f"| {100 * c['in_band_bar_share']:.1f}% |")
        L.append("")
    with open(os.path.join(OUT, "dwell_census.md"), "w") as f:
        f.write("\n".join(L))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--instr", nargs="*",
                    default=["uk100fut", "ger40fut", "nas100fut",
                             "us30fut"])
    a = ap.parse_args()
    head = subprocess.run(["git", "rev-parse", "HEAD"], cwd=ROOT,
                          capture_output=True, text=True).stdout.strip()
    results = []
    for instr in a.instr:
        print(f"# dwell_census: {instr} ...", file=sys.stderr)
        results.append(run_instrument(instr))
    art = {"STAMP": ("OBSERVATIONAL organ #5 — dwell-time vocabulary; "
                     "consumers price their own fields; never "
                     "validation"),
           "engine_commit": head, "results": results}
    with open(os.path.join(OUT, "dwell_census.json"), "w") as f:
        json.dump(art, f, indent=2, default=str)
    _emit(art, head)
    print(f"OBSERVATIONAL organ #5 -> {OUT}/dwell_census.md")


if __name__ == "__main__":
    main()
