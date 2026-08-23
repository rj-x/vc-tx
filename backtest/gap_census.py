"""Seam and gap census (register 67; pre-registered prereg_gap_census).
MEASUREMENT — the gap-fill folk strategy is explicitly NOT being
registered (ORB-adjacent family, parked precedent register 51);
mint-on-lift only, front door.

Per instrument, native calendars, both windows where applicable:
  (a) WEEKEND gaps (Friday close -> next open): ATR-normalized size,
      direction, fill rate + time-to-fill (fill = trade back to the
      prior close, capped at the next pause), directional persistence
      at the STANDARD horizons — against the open-context base row.
  (b) DAILY-PAUSE gaps (each instrument's own measured pause, register
      40): the same measurements.
  (c) CASH-OPEN seam (open print vs prior cash close): size, direction,
      and the following opening-window behavior (H16's registered
      window construction, shared, no duplication).
  (d) INTRASESSION 1M MICRO-GAPS (consecutive-bar gaps beyond the
      measured spread): frequency, size, session distribution, forward
      behavior vs base. INTERPRETATION CLAUSE: liquidity-vacuum
      fingerprint — the bar-scale cousin of H11's gap-traversal.

Counts everywhere; dimming; PROVISIONAL stamps; sealed/lockbox
excluded; twin-run pinned. Weekly under Part C.
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

from engine.signal_watch import H16_WINDOW_MIN
from engine.store_loader import is_sealed, lockbox_boundary, zones
from backtest.horizons import STANDARD_HORIZONS
from backtest.recipes import _spread_median
from backtest.sessions import session_of
from backtest.scoreboard import (PROVISIONAL_INSTRS, PROVISIONAL_STAMP,
                                 _atr15, _replay, _series, make_cfg)

OUT = os.path.join(ROOT, "reports", "scoreboard")

# |gap|/ATR bucket edges — IMPLEMENTER-PROPOSED, flagged for ratification
GAP_BUCKETS_ATR = (0.25, 1.0)
WEEKEND_MIN_H = 24.0        # pause classification: >24h = weekend
PAUSE_MIN_MIN = 5.0         # >5 min and <=24h = daily pause


def _bucket(x):
    a, b = GAP_BUCKETS_ATR
    return (f"<{a:g}" if x < a else f"{a:g}-{b:g}" if x < b else f">={b:g}")


def seam_events(ts, o, h, l, c, atr_of, spread):
    """Classify every consecutive-live-bar seam. Deterministic (pinned).
    Returns dict kind -> list of events; kinds: weekend, pause, micro.
    Each event: index i of the bar AFTER the seam, gap pts (signed,
    open[i] - close[i-1]), gap_atr, fill/persistence fields."""
    n = len(ts)
    out = {"weekend": [], "pause": [], "micro": []}
    # pause boundaries for the fill cap
    dt_min = np.diff(ts) / 60e9
    pause_idx = np.nonzero(dt_min > PAUSE_MIN_MIN)[0] + 1   # bar AFTER
    for i in range(1, n):
        dmin = (ts[i] - ts[i - 1]) / 60e9
        gap = float(o[i] - c[i - 1])
        atr = atr_of(i)
        if atr is None or atr <= 0:
            continue
        if dmin > WEEKEND_MIN_H * 60:
            kind = "weekend"
        elif dmin > PAUSE_MIN_MIN:
            kind = "pause"
        elif abs(gap) > spread:
            kind = "micro"
        else:
            continue
        ev = {"i": i, "ts": pd.Timestamp(ts[i], tz="UTC"),
              "session": session_of(pd.Timestamp(ts[i], tz="UTC")),
              "gap_pts": round(gap, 2),
              "gap_atr": round(gap / atr, 3)}
        if kind in ("weekend", "pause"):
            # fill = trade back to the prior close, capped at next pause
            j_next = pause_idx[np.searchsorted(pause_idx, i + 1)] \
                if np.searchsorted(pause_idx, i + 1) < len(pause_idx) \
                else n
            filled = None
            for j in range(i, min(j_next, n)):
                if (l[j] <= c[i - 1] <= h[j]):
                    filled = j - i
                    break
            ev["fill_bars"] = filled
        # directional persistence: sign(gap) * (close@+h - open[i])
        sgn = 1.0 if gap > 0 else -1.0 if gap < 0 else 0.0
        pers = {}
        for hz in STANDARD_HORIZONS:
            j = np.searchsorted(ts, ts[i] + hz * 60_000_000_000,
                                side="left")
            if j < n:
                pers[hz] = round(sgn * float(c[j] - o[i]), 2)
        ev["persist"] = pers
        out[kind].append(ev)
    return out


def cash_seams(ts, o, c, slug, atr_of):
    """(c) open print vs prior CASH close + H16-window continuation."""
    import store as store_mod
    a, b = store_mod.SESSIONS[slug]
    tz = store_mod.SESSION_TZ.get(slug, "Europe/London")
    idx = pd.DatetimeIndex(pd.to_datetime(ts, utc=True)).tz_convert(tz)
    lt = idx.hour + idx.minute / 60.0
    in_cash = (lt >= a) & (lt < b)
    dates = idx.date
    n = len(ts)
    events = []
    prev_close_i = None
    prev_date = None
    for i in range(n):
        if not in_cash[i]:
            continue
        if dates[i] != prev_date:
            if prev_close_i is not None:
                atr = atr_of(i)
                if atr and atr > 0:
                    seam = float(o[i] - c[prev_close_i])
                    sgn = (1.0 if seam > 0 else -1.0 if seam < 0
                           else 0.0)
                    j = np.searchsorted(
                        ts, ts[i] + H16_WINDOW_MIN * 60_000_000_000,
                        side="left")
                    cont = (round(sgn * float(c[j] - o[i]), 2)
                            if j < n else None)
                    events.append({
                        "ts": pd.Timestamp(ts[i], tz="UTC"),
                        "seam_pts": round(seam, 2),
                        "seam_atr": round(seam / atr, 3),
                        "window_min": H16_WINDOW_MIN,
                        "continuation_pts": cont})
            prev_date = dates[i]
        prev_close_i = i
    return events


def _pers_stats(evs):
    out = {}
    for hz in STANDARD_HORIZONS:
        v = [e["persist"][hz] for e in evs if hz in e["persist"]]
        if v:
            out[hz] = {"n": len(v), "mean": round(float(np.mean(v)), 2),
                       "median": round(float(np.median(v)), 2)}
    return out


def _gap_table(evs):
    """Bucketed (|gap|/ATR) + the all-events base row."""
    rows = {}
    groups = {"ALL (base row)": evs}
    for e in evs:
        groups.setdefault(_bucket(abs(e["gap_atr"])), []).append(e)
    for gname, g in groups.items():
        if not g:
            continue
        fills = [e.get("fill_bars") for e in g if "fill_bars" in e]
        done = [f for f in fills if f is not None]
        rows[gname] = {
            "n": len(g),
            "median_abs_atr": round(float(np.median(
                [abs(e["gap_atr"]) for e in g])), 3),
            "up_pct": round(100 * float(np.mean(
                [e["gap_pts"] > 0 for e in g])), 1),
            "fill_pct": (round(100 * len(done) / len(fills), 1)
                         if fills else None),
            "fill_bars_median": (round(float(np.median(done)), 1)
                                 if done else None),
            "persist": _pers_stats(g)}
    return rows


def run_instrument(instr):
    cfg = make_cfg({"session_model.extended_hours": True,
                    "session_model.ladder": True})
    engine, bars, _ = _replay(cfg, instr)
    b1m_all = bars[cfg.mtf.execution_tf]
    b1m = [x for x in b1m_all if not x.is_stub]
    ts, cl, hi, lo, _s, _b = _series(b1m_all)
    op = np.array([x.open for x in b1m])
    amap = _atr15(bars[cfg.mtf.signal_tf], cfg.context.atr_period)
    atr_ts = sorted(amap)
    atr_keys = [k.value for k in atr_ts]

    def atr_of(i):
        j = np.searchsorted(atr_keys, ts[i], side="right") - 1
        return amap[atr_ts[j]] if j >= 0 else None
    spread = _spread_median(instr)
    seams = seam_events(ts, op, hi, lo, cl, atr_of, spread)
    cash = cash_seams(ts, op, cl, instr, atr_of)
    boundary, gl = lockbox_boundary(), zones()["go_live"]

    def _win(evs):
        return {"backtest": [e for e in evs
                             if e["ts"] < boundary
                             and not is_sealed(e["ts"])],
                "forward": [e for e in evs
                            if e["ts"] >= gl and not is_sealed(e["ts"])]}
    out = {"instrument": instr, "spread_pts": spread,
           "status": ("provisional" if instr in PROVISIONAL_INSTRS
                      else "canonical"),
           "n_live_bars": len(b1m)}
    for kind in ("weekend", "pause"):
        out[kind] = {w: _gap_table(evs)
                     for w, evs in _win(seams[kind]).items() if evs}
    micro = _win(seams["micro"])
    out["micro"] = {}
    for w, evs in micro.items():
        if not evs:
            continue
        sess_share = {}
        for e in evs:
            sess_share[e["session"]] = sess_share.get(e["session"], 0) + 1
        out["micro"][w] = {
            "n": len(evs),
            "per_1000_bars": round(1000 * len(evs) / len(b1m), 2),
            "median_abs_atr": round(float(np.median(
                [abs(e["gap_atr"]) for e in evs])), 3),
            "session_share": {k: round(100 * v / len(evs), 1)
                              for k, v in sorted(sess_share.items())},
            "persist": _pers_stats(evs)}
    out["cash_seam"] = {}
    for w, evs in _win(cash).items():
        if not evs:
            continue
        conts = [e["continuation_pts"] for e in evs
                 if e["continuation_pts"] is not None]
        out["cash_seam"][w] = {
            "n": len(evs),
            "median_abs_atr": round(float(np.median(
                [abs(e["seam_atr"]) for e in evs])), 3),
            "up_pct": round(100 * float(np.mean(
                [e["seam_pts"] > 0 for e in evs])), 1),
            "window_min": H16_WINDOW_MIN,
            "continuation_mean_pts": (round(float(np.mean(conts)), 2)
                                      if conts else None),
            "continuation_median_pts": (round(float(np.median(conts)), 2)
                                        if conts else None)}
    return out


def _emit(results, head):
    hzs = "/".join(str(h) for h in STANDARD_HORIZONS)
    L = ["# Seam & Gap Census (GENERATED by backtest.gap_census)", "",
         "Terms: [docs/GLOSSARY.md](../../docs/GLOSSARY.md).", "",
         f"Engine `{head[:9]}` — OBSERVATIONAL, pre-registered "
         "(prereg_gap_census, register 67). **MEASUREMENT: the gap-fill "
         "folk strategy is explicitly NOT being registered "
         "(ORB-adjacent family, parked precedent register 51) — "
         "mint-on-lift only, front door.** Native calendars; fill = "
         "trade back to the prior close, capped at the next pause; "
         "persistence = sign(gap) × (close@+h − open), pts, at the "
         f"standard horizons {{{hzs}}} min (null 0); each bucketed row "
         "reads against the ALL base row of its own open-context. "
         f"Abs-gap/ATR buckets {GAP_BUCKETS_ATR} are "
         "IMPLEMENTER-PROPOSED, "
         "flagged for ratification. Micro-gaps: consecutive-bar gaps "
         "beyond the measured spread — INTERPRETATION CLAUSE: "
         "liquidity-vacuum fingerprint, the bar-scale cousin of H11's "
         "gap-traversal. ° = n<20.", ""]
    for res in results:
        inst = res["instrument"]
        L += [f"## {inst} ({res['status'].upper()}; spread "
              f"{res['spread_pts']} pts)"]
        if res["status"] == "provisional":
            L += [f"> {PROVISIONAL_STAMP}"]
        L.append("")
        for kind, title in (("weekend", "weekend gaps"),
                            ("pause", "daily-pause gaps (register-40 "
                                      "measured pauses)")):
            tabs = res.get(kind, {})
            if not tabs:
                continue
            L += [f"### {inst} — {title}", "",
                  "| window | bucket (abs gap/ATR) | n | med abs "
                  "gap/ATR | up % | fill % | t-fill med (bars) "
                  f"| persist @{hzs} (med pts) |",
                  "|---|---|---|---|---|---|---|---|"]
            for w, rows in tabs.items():
                order = ["ALL (base row)"] + sorted(
                    k for k in rows if k != "ALL (base row)")
                for gname in order:
                    r = rows[gname]
                    dim = "°" if r["n"] < 20 else ""
                    pers = "/".join(
                        (f"{r['persist'][hz]['median']:+.1f}"
                         if hz in r["persist"] else "—")
                        for hz in STANDARD_HORIZONS)
                    L.append(
                        f"| {w} | {gname} | {dim}{r['n']} "
                        f"| {r['median_abs_atr']} | {r['up_pct']} "
                        f"| {r['fill_pct']} | {r['fill_bars_median']} "
                        f"| {pers} |")
            L.append("")
        cs = res.get("cash_seam", {})
        if cs:
            L += [f"### {inst} — cash-open seam (H16's "
                  f"{H16_WINDOW_MIN}-min window construction, shared)",
                  "",
                  "| window | n | med abs seam/ATR | up % "
                  "| continuation mean/med (pts) |",
                  "|---|---|---|---|---|"]
            for w, r in cs.items():
                dim = "°" if r["n"] < 20 else ""
                L.append(f"| {w} | {dim}{r['n']} | {r['median_abs_atr']} "
                         f"| {r['up_pct']} "
                         f"| {r['continuation_mean_pts']}/"
                         f"{r['continuation_median_pts']} |")
            L.append("")
        mi = res.get("micro", {})
        if mi:
            L += [f"### {inst} — intrasession 1M micro-gaps (beyond "
                  "measured spread)", "",
                  "| window | n | per-1000 bars | med abs gap/ATR | "
                  f"session share % | persist @{hzs} (med pts) |",
                  "|---|---|---|---|---|---|"]
            for w, r in mi.items():
                dim = "°" if r["n"] < 20 else ""
                pers = "/".join(
                    (f"{r['persist'][hz]['median']:+.1f}"
                     if hz in r["persist"] else "—")
                    for hz in STANDARD_HORIZONS)
                share = ", ".join(f"{k} {v}"
                                  for k, v in r["session_share"].items())
                L.append(f"| {w} | {dim}{r['n']} | {r['per_1000_bars']} "
                         f"| {r['median_abs_atr']} | {share} | {pers} |")
            L.append("")
    with open(os.path.join(OUT, "gap_census.md"), "w") as f:
        f.write("\n".join(L))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--instr", nargs="*",
                    default=["uk100fut", "ger40fut", "nas100fut", "us30fut"])
    a = ap.parse_args()
    os.makedirs(OUT, exist_ok=True)
    head = subprocess.run(["git", "rev-parse", "HEAD"], cwd=ROOT,
                          capture_output=True, text=True).stdout.strip()
    results = []
    for instr in a.instr:
        print(f"# gap_census: {instr} ...", file=sys.stderr)
        results.append(run_instrument(instr))
    art = {"STAMP": ("OBSERVATIONAL seam & gap census — measurement, "
                     "never validation; gap-fill folk strategy NOT "
                     "registered (mint-on-lift only)"),
           "engine_commit": head,
           "buckets_atr_FLAGGED": list(GAP_BUCKETS_ATR),
           "results": results}
    with open(os.path.join(OUT, "gap_census.json"), "w") as f:
        json.dump(art, f, indent=2, default=str)
    _emit(results, head)
    print(f"OBSERVATIONAL gaps -> {OUT}/gap_census.md")


if __name__ == "__main__":
    main()
