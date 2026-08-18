"""Signal-hypothesis scoreboard (register 31 revision, build approved
2026-08-18). Measures MOVE-DETECTION, not trading — no fills, no ledger.

Yardsticks (docs/parameter_registry.md, cited not defined):
  - qualifying_move: >= 1.5 x 15M ATR, one-directional, within 60 minutes,
    drift-adjusted (operator ratification 2026-08-18)
  - major_move: >= 3 x, same clause
  - ATR = trailing mean TR over context.atr_period (14) 15M bars
  - standard outcome horizons for any bar-mark reporting: STANDARD_HORIZONS

Operationalization (pre-registered, trial log
prereg_scoreboard_operationalization — the yardstick's 60-minute clause is
used for BOTH the forward window and the coverage lookback; nothing else is
introduced):
  - A bar QUALIFIES (dir d) if the drift-adjusted d-favorable excursion
    within the next 60 min reaches 1.5 x ATR15(t). Drift = same-segment
    mean net 60-min change, signed by d.
  - MOVE EPISODES: qualifying bars of one direction whose 60-min windows
    overlap merge into one episode; episode peak = the extreme reached in
    the merged windows; total move = |peak - close at episode start|.
  - FIRE = a Signal-TF CONFIRM event (H1-H5) or a signal_watch fire (candidate
    conditions; none defined yet — rows begin the day one is defined).
  - PRECISION: fire's own bar qualifies in the predicted direction.
  - COVERAGE: episode has a matching-direction fire in the 60 min BEFORE
    its start (the yardstick's window clause, applied as lookback).
  - EARLINESS: per covered episode, at its earliest covering fire:
    points-of-move remaining = (peak - close at fire) x d; and minutes
    from fire to the next 15M trend flip INTO d, where one occurs.

Sources: ONE full-store live-equivalent replay (Part B config), TWO
readout windows — backtest (working set, < lockbox boundary) and forward
(>= go_live, sealed windows auto-skipped per register 30). The lockbox
span is excluded from both. Counts adjacent to every number; fills do not
exist here by construction. OBSERVATIONAL — never validation.
"""

import argparse
import json
import os
import subprocess

import numpy as np
import pandas as pd

from engine.signal_watch import FIRING_CONDITIONS, SignalWatch
from engine.store_loader import is_sealed, lockbox_boundary, zones
from backtest.forward_migration import _replay
from backtest.campaign import make_cfg

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "reports", "scoreboard")

QUALIFYING_ATR_MULT = 1.5      # registry: qualifying_move
MAJOR_ATR_MULT = 3.0           # registry: major_move
MOVE_WINDOW_MIN = 60           # registry: qualifying_move window clause


def _atr15(bars15, period):
    """Trailing ATR keyed by 15M close ts (registry: context.atr_period)."""
    out, trs, prev_close = {}, [], None
    for b in bars15:
        tr = (b.high - b.low if prev_close is None else
              max(b.high - b.low, abs(b.high - prev_close),
                  abs(b.low - prev_close)))
        trs.append(tr)
        prev_close = b.close
        if len(trs) >= period:
            out[b.ts] = sum(trs[-period:]) / period
    return out


def _series(bars1m):
    b = [x for x in bars1m if not x.is_stub]
    return (np.array([x.ts.value for x in b]),
            np.array([x.close for x in b]),
            np.array([x.high for x in b]),
            np.array([x.low for x in b]),
            np.array([x.segment for x in b]), b)


def build_moves(bars1m, bars15, atr_period):
    """Qualifying-move episodes per direction + per-bar qualify flags."""
    ts, cl, hi, lo, segs, blist = _series(bars1m)
    atr = _atr15(bars15, atr_period)
    atr_ts = sorted(atr)
    win = pd.Timedelta(minutes=MOVE_WINDOW_MIN).value

    # same-segment mean net 60-min change (drift)
    drift = {}
    for seg in sorted(set(segs)):
        idx = np.nonzero(segs == seg)[0]
        ends = np.searchsorted(ts, ts[idx] + win, side="right") - 1
        ok = ends > idx
        drift[seg] = float(np.mean(cl[ends[ok]] - cl[idx[ok]])) if ok.any() else 0.0

    def atr_at(t):
        i = np.searchsorted(atr_ts, t, side="right") - 1
        return atr[atr_ts[i]] if i >= 0 else None

    qual = {1: np.zeros(len(ts), bool), -1: np.zeros(len(ts), bool)}
    ends_all = np.searchsorted(ts, ts + win, side="right")
    for i in range(len(ts)):
        a = atr_at(pd.Timestamp(ts[i], tz="UTC"))
        if a is None or ends_all[i] <= i + 1:
            continue
        sl = slice(i + 1, ends_all[i])
        d_up = (hi[sl].max() - cl[i]) - drift[segs[i]]
        d_dn = (cl[i] - lo[sl].min()) + drift[segs[i]]
        if d_up >= QUALIFYING_ATR_MULT * a:
            qual[1][i] = True
        if d_dn >= QUALIFYING_ATR_MULT * a:
            qual[-1][i] = True

    episodes = []
    for d in (1, -1):
        i = 0
        while i < len(ts):
            if not qual[d][i]:
                i += 1
                continue
            j = i                      # merge overlapping qualifying windows
            while True:
                nxt = j + 1
                while nxt < len(ts) and not qual[d][nxt]:
                    nxt += 1
                if nxt < len(ts) and ts[nxt] <= ts[j] + win:
                    j = nxt
                else:
                    break
            end = min(ends_all[j], len(ts))
            sl = slice(i, end)
            peak = hi[sl].max() if d == 1 else lo[sl].min()
            a0 = atr_at(pd.Timestamp(ts[i], tz="UTC")) or float("nan")
            total = (peak - cl[i]) * d
            episodes.append({"start": pd.Timestamp(ts[i], tz="UTC"),
                             "dir": d, "peak": float(peak),
                             "start_close": float(cl[i]),
                             "total_pts": float(round(total, 1)),
                             "major": bool(total >= MAJOR_ATR_MULT * a0)})
            i = end
    episodes.sort(key=lambda e: e["start"])
    return qual, episodes, (ts, cl, segs), drift


def fires_from_events(events):
    out = []
    for e in events:
        if e["type"] == "CONFIRM" and "h" in e:
            out.append({"ts": pd.Timestamp(e["ts"]), "name": e["h"]["spec"],
                        "dir": int(e["h"]["dir"])})
    return out


def trend_flips(events):
    """15M trend series from debug PHASE_EVAL events -> flip timestamps."""
    flips, prev = [], 0
    for e in events:
        if e["type"] == "PHASE_EVAL" and e.get("tf") == "15min":
            t = e.get("trend", 0)
            if t != prev and t != 0:
                flips.append((pd.Timestamp(e["ts"]), t))
            prev = t
    return flips


def score(fires, qual, episodes, series, flips, lo_ts, hi_ts, label,
          names=frozenset()):
    """One source window [lo_ts, hi_ts); sealed spans already excluded
    from `fires`/`episodes` by the caller."""
    ts, cl, _ = series
    win = pd.Timedelta(minutes=MOVE_WINDOW_MIN)
    F = [f for f in fires if lo_ts <= f["ts"] < hi_ts]
    E = [e for e in episodes if lo_ts <= e["start"] < hi_ts]
    rows = {}
    for name in sorted(names | {f["name"] for f in F}):
        nf = [f for f in F if f["name"] == name]
        if not nf:
            rows[name] = {"source": label, "n_fires": 0,
                          "note": "no confirmations in window"}
            continue
        hits, misses = [], []
        for f in nf:
            i = np.searchsorted(ts, f["ts"].value, side="right") - 1
            if i < 0:
                continue
            ok = bool(qual[f["dir"]][i])
            adverse = 0.0
            j = np.searchsorted(ts, (f["ts"] + win).value, side="right")
            if j > i + 1:
                seg = cl[i + 1:j]
                adverse = float((cl[i] - seg.min()) if f["dir"] == 1
                                else (seg.max() - cl[i]))
            (hits if ok else misses).append(
                {**f, "close_at_fire": float(cl[i]), "adverse_pts": adverse})
        covered, remaining, flip_mins = [], [], []
        for e in E:
            pre = [f for f in nf if f["dir"] == e["dir"]
                   and e["start"] - win <= f["ts"] <= e["start"]]
            if not pre:
                continue
            first = min(pre, key=lambda f: f["ts"])
            i = np.searchsorted(ts, first["ts"].value, side="right") - 1
            rem = (e["peak"] - cl[i]) * e["dir"]
            covered.append((e, first, float(rem)))
            remaining.append(float(rem))
            fl = [t for t, d in flips if d == e["dir"] and t >= first["ts"]]
            if fl:
                flip_mins.append((min(fl) - first["ts"]).total_seconds() / 60)
        best = max(covered, key=lambda c: c[2], default=None)
        worst = max(misses, key=lambda m: m["adverse_pts"], default=None)
        rows[name] = {
            "source": label,
            "n_fires": len(nf),
            "precision": {"hits": len(hits), "of": len(hits) + len(misses),
                          "pct": round(100 * len(hits) / (len(hits) + len(misses)), 1)
                          if (hits or misses) else None},
            "coverage": {"covered": len(covered), "of": len(E),
                         "pct": round(100 * len(covered) / len(E), 1) if E else None},
            "earliness": {
                "median_pts_remaining_at_fire": (round(float(np.median(remaining)), 1)
                                                 if remaining else None),
                "n": len(remaining),
                "median_min_before_15m_flip": (round(float(np.median(flip_mins)), 1)
                                               if flip_mins else None),
                "n_flips": len(flip_mins)},
            "best_call": ({"ts": str(best[1]["ts"]), "dir": best[1]["dir"],
                           "episode_start": str(best[0]["start"]),
                           "pts_remaining_at_fire": round(best[2], 1),
                           "episode_total_pts": best[0]["total_pts"],
                           "major": best[0]["major"]} if best else None),
            "worst_false_alarm": ({"ts": str(worst["ts"]), "dir": worst["dir"],
                                   "adverse_pts": round(worst["adverse_pts"], 1)}
                                  if worst else None),
        }
    w = (ts >= lo_ts.value) & (ts < hi_ts.value)
    base = (round(100 * float(np.mean(qual[1][w] | qual[-1][w])), 1)
            if w.any() else None)
    rows["_moves"] = {"source": label, "n_qualifying_episodes": len(E),
                      "n_major": sum(1 for e in E if e["major"]),
                      "bar_qualify_base_rate_pct": base,
                      "base_rate_note": ("precision reads against this: the "
                                         "share of bars that qualify in "
                                         "EITHER direction by clock alone")}
    return rows


def run(instr="uk100fut"):
    cfg = make_cfg({"session_model.extended_hours": True,
                    "session_model.ladder": True,
                    "debug.structure": True})       # PHASE_EVAL for flips
    watch = SignalWatch()
    engine, bars, _ = _replay(cfg, instr, engine_hook=watch.attach)
    events = engine.narrative.events
    b1m = bars[cfg.mtf.execution_tf]
    qual, episodes, series, drift = build_moves(
        b1m, bars[cfg.mtf.signal_tf], cfg.context.atr_period)
    recipe_fires = fires_from_events(events)          # CONFIRM = recipe stage
    signal_fires = watch.fires                         # bare firing conditions
    flips = trend_flips(events)
    # sealed spans excluded before scoring (register 30 pattern)
    recipe_fires = [f for f in recipe_fires if not is_sealed(f["ts"])]
    signal_fires = [f for f in signal_fires if not is_sealed(f["ts"])]
    episodes = [e for e in episodes if not is_sealed(e["start"])]
    boundary = lockbox_boundary()
    gl = zones()["go_live"]
    far = pd.Timestamp("2100-01-01", tz="UTC")
    head = subprocess.run(["git", "rev-parse", "HEAD"], cwd=ROOT,
                          capture_output=True, text=True).stdout.strip()
    return {
        "STAMP": ("OBSERVATIONAL signal scoreboard - move-detection, not "
                  "trading; no fills exist here by construction; never "
                  "validation (docs/hypothesis_lifecycle.md stage 4)"),
        "engine_commit": head,
        "yardsticks": ["qualifying_move (registry: operator ratification "
                       "2026-08-18)", "major_move (same)",
                       "context.atr_period (founding config)",
                       "60-min clause reused as coverage lookback "
                       "(prereg_scoreboard_operationalization)"],
        "zone_statement": ("one full-store live-equivalent replay; backtest "
                           "window < lockbox boundary; forward window >= "
                           "go_live; lockbox span excluded from both; "
                           "sealed windows auto-skipped"),
        "doctrine": ("PURE SIGNALS (operator-ratified 2026-08-18): a "
                     "hypothesis = a firing condition, nothing else; graded "
                     "only on whether a qualifying move follows, how "
                     "reliably, how early. Trade logic is a separate later "
                     "layer for signals that earn one."),
        "signals": {
            "backtest": score(signal_fires, qual, episodes, series, flips,
                              pd.Timestamp("1970-01-01", tz="UTC"), boundary,
                              "backtest_replay",
                              names=frozenset(FIRING_CONDITIONS)),
            "forward": score(signal_fires, qual, episodes, series, flips,
                             gl, far, "forward_feed_replay",
                             names=frozenset(FIRING_CONDITIONS))},
        "founding_recipes_at_confirmation": {
            "note": ("graded pattern+wrapper stacks (confirmation = recipe "
                     "stage under the pure-signals doctrine) - historically "
                     "interesting, kept distinct, NOT signal rows; frozen_v1 "
                     "in paper is the untouched baseline record"),
            "backtest": score(recipe_fires, qual, episodes, series, flips,
                              pd.Timestamp("1970-01-01", tz="UTC"), boundary,
                              "backtest_replay",
                              names=frozenset({"H1", "H2", "H3", "H4", "H5"})),
            "forward": score(recipe_fires, qual, episodes, series, flips,
                             gl, far, "forward_feed_replay",
                             names=frozenset({"H1", "H2", "H3", "H4", "H5"}))},
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--instr", default="uk100fut")
    a = ap.parse_args()
    os.makedirs(OUT, exist_ok=True)
    res = run(a.instr)
    path = os.path.join(OUT, "signal_scoreboard.json")
    with open(path, "w") as f:
        json.dump(res, f, indent=2, default=str)
    for block in ("signals", "founding_recipes_at_confirmation"):
      for src in ("backtest", "forward"):
        print(f"\n== {block} / {src} ==")
        for name, r in res[block][src].items():
            if r.get("n_fires") == 0:
                print(f"  {name}: fires 0")
                continue
            if name == "_moves":
                print(f"  qualifying episodes: {r['n_qualifying_episodes']} "
                      f"(major {r['n_major']})")
                continue
            p, c, e = r["precision"], r["coverage"], r["earliness"]
            print(f"  {name}: fires {r['n_fires']} | precision "
                  f"{p['pct']}% ({p['hits']}/{p['of']}) | coverage "
                  f"{c['pct']}% ({c['covered']}/{c['of']}) | median pts "
                  f"remaining {e['median_pts_remaining_at_fire']} "
                  f"(n={e['n']})")
    print(f"\nOBSERVATIONAL scoreboard -> {path}")


if __name__ == "__main__":
    main()
