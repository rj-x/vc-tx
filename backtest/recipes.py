"""Recipe layer v0 — grammar + versioned sets (register 41, operator order
2026-08-19). OBSERVATIONAL ONLY: nothing here touches paper, the ledger,
frozen_v1, labels, or criteria. Harvests the signal scoreboard's directional
fires under explicit exit recipes and reports POINTS, spread-charged.

GRAMMAR (the engine capability — any stop x target composition):
  stops   : ("fixed_pts", v) | ("atr", k)            [k x ATR(15M) at entry]
          | ("trail_nth", N, ("pts"|"atr", off))     [beyond the Nth previous
                                                      settled 1M bar's extreme
                                                      +/- offset; RATCHET ONLY]
  targets : ("fixed_pts", v) | ("atr", k) | None     [None = trail-out only]
  entry   : next 1M bar open after a directional fire; ONE position per
            hypothesis per instrument (per recipe); spread charged per trade
            (median in-cash spread measured from the instrument's own store,
            per the uk100 spread-by-bin template).

HONEST-FILL RULES (operator-ruled 2026-08-19; part of every recipe's
definition; printed in the artifact header):
  1. Intrabar stop+target both reachable -> STOP fills, always.
  2. Gap through a level -> filled at the gapped (worse) price (the open).
  3. Trailing stops RATCHET ONLY and are evaluated on settled bars.
  4. EOD flat at each instrument's NATIVE session close.

Versioned sets: a run's artifact states its set version; additions or value
changes only by re-registration, counted in the trial log. recipe_set_v0's
VALUES ARE ILLUSTRATIVE — awaiting operator ratification (registry-flagged
like the criteria numbers); discuss on the working system before any v1.
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

from engine.signal_watch import AGNOSTIC_ROWS
from engine.store_loader import is_sealed, lockbox_boundary, zones
from backtest.sessions import session_of
from backtest.scoreboard import (PAIR_OF, PROVISIONAL_INSTRS,
                                 PROVISIONAL_STAMP, _replay, _series,
                                 _atr15, h9_fires, make_cfg)
from engine.signal_watch import (DERIVED_FIRES, DUAL_GRADED,
                                 FIRING_CONDITIONS, SignalWatch)

OUT = os.path.join(ROOT, "reports", "scoreboard")

RECIPE_SET_VERSION = "recipe_set_v0"
RECIPE_SETS = {
    "recipe_set_v0": {
        # ILLUSTRATIVE defaults — awaiting operator ratification
        "R-FIX": {"stop": ("fixed_pts", 10.0),
                  "target": ("fixed_pts", 20.0)},
        "R-ATR": {"stop": ("atr", 1.5), "target": ("atr", 3.0)},
        "R-TRAIL": {"stop": ("trail_nth", 6, ("pts", 0.0)), "target": None},
        "R-TRAIL-ATR": {"stop": ("trail_nth", 6, ("atr", 0.5)),
                        "target": None},
    },
}


def _stop_level(spec, entry, d, atr0):
    kind = spec[0]
    if kind == "fixed_pts":
        return entry - d * spec[1]
    if kind == "atr":
        return entry - d * spec[1] * atr0
    return None                            # trail_nth: set per bar


def _target_level(spec, entry, d, atr0):
    if spec is None:
        return None
    kind = spec[0]
    if kind == "fixed_pts":
        return entry + d * spec[1]
    if kind == "atr":
        return entry + d * spec[1] * atr0
    raise ValueError(spec)


def simulate(fires, arrs, atr_at, recipe, spread, eod_flag):
    """One recipe over one hypothesis's fires. arrs = (ts, o, h, l, c);
    eod_flag[j] True iff bar j is the last bar of its native cash session.
    Returns trade dicts. Deterministic (twin-run bit-identity pinned)."""
    ts, o, h, l, c = arrs
    n = len(ts)
    trades = []
    open_until = -1                        # one position per hypothesis
    for f in sorted(fires, key=lambda x: x["ts"].value):
        fi = np.searchsorted(ts, f["ts"].value, side="right") - 1
        ei = fi + 1                        # entry = next bar open
        if fi < 0 or ei >= n or ei <= open_until:
            continue
        d = f["dir"]
        entry = o[ei]
        atr0 = atr_at(pd.Timestamp(ts[ei], tz="UTC"))
        if atr0 is None:
            continue
        sspec, tspec = recipe["stop"], recipe["target"]
        trail = sspec[0] == "trail_nth"
        stop = _stop_level(sspec, entry, d, atr0)
        target = _target_level(tspec, entry, d, atr0)
        exit_px = exit_ts = reason = None
        j = ei
        while j < n:
            if trail:
                N, (okind, off) = sspec[1], sspec[2]
                ref = j - N
                if ref >= 0:
                    off_pts = off * atr0 if okind == "atr" else off
                    cand = (l[ref] - off_pts) if d == 1 else (h[ref] + off_pts)
                    # rule 3: ratchet only, settled bars only
                    stop = cand if stop is None else (
                        max(stop, cand) if d == 1 else min(stop, cand))
            if stop is not None:
                if (d == 1 and o[j] <= stop) or (d == -1 and o[j] >= stop):
                    exit_px, reason = o[j], "stop_gap"     # rule 2
                    break
            if target is not None:
                if (d == 1 and o[j] >= target) or (d == -1 and o[j] <= target):
                    exit_px, reason = o[j], "target_gap"   # rule 2
                    break
            stop_hit = stop is not None and (
                l[j] <= stop if d == 1 else h[j] >= stop)
            tgt_hit = target is not None and (
                h[j] >= target if d == 1 else l[j] <= target)
            if stop_hit:                                   # rule 1: stop wins
                exit_px, reason = stop, "stop"
                break
            if tgt_hit:
                exit_px, reason = target, "target"
                break
            if eod_flag[j]:                                # rule 4
                exit_px, reason = c[j], "eod"
                break
            j += 1
        if exit_px is None:                # data ran out: mark at last close
            j = n - 1
            exit_px, reason = c[j], "end_of_data"
        pts = (exit_px - entry) * d - spread
        trades.append({"fire_ts": str(f["ts"]), "entry_ts": str(
            pd.Timestamp(ts[ei], tz="UTC")), "dir": d,
            "entry": float(entry), "exit": float(exit_px), "reason": reason,
            "pts": round(float(pts), 2),
            "duration_min": round((ts[j] - ts[ei]) / 60e9, 1),
            "session": session_of(pd.Timestamp(ts[ei], tz="UTC"))})
        open_until = j
    return trades


def _eod_flags(bars, slug):
    """bar j is the last bar of its NATIVE cash session (rule 4)."""
    import store as store_mod
    a, b = store_mod.SESSIONS[slug]
    tz = store_mod.SESSION_TZ.get(slug, "Europe/London")
    idx = pd.DatetimeIndex([x.ts for x in bars]).tz_convert(tz)
    lt = idx.hour + idx.minute / 60.0
    dates = idx.date
    n = len(bars)
    flags = np.zeros(n, bool)
    for j in range(n):
        if lt[j] >= b:
            continue
        if j + 1 == n or lt[j + 1] >= b or dates[j + 1] != dates[j]:
            flags[j] = True
    return flags


def _spread_median(slug):
    df = pd.read_csv(os.path.join(ROOT, "clean_finsa", f"{slug}_1min.csv"))
    s = df[df["in_cash"]]["spread"].dropna()
    return round(float(s.median()), 2) if len(s) else 0.0


def run_instrument(instr):
    cfg = make_cfg({"session_model.extended_hours": True,
                    "session_model.ladder": True})
    watch = SignalWatch()
    engine, bars, _ = _replay(cfg, instr, engine_hook=watch.attach)
    b1m = [x for x in bars[cfg.mtf.execution_tf] if not x.is_stub]
    ts, cl, hi, lo, segs, _b = _series(bars[cfg.mtf.execution_tf])
    op = np.array([x.open for x in b1m])
    atr = _atr15(bars[cfg.mtf.signal_tf], cfg.context.atr_period)
    atr_ts = sorted(atr)

    def atr_at(t):
        i = np.searchsorted(atr_ts, t, side="right") - 1
        return atr[atr_ts[i]] if i >= 0 else None

    fires = watch.fires + h9_fires(engine.narrative.events, cfg)
    # directional rows only: no either-dir supplements, no agnostic rows
    fires = [f for f in fires
             if f["name"] not in AGNOSTIC_ROWS and not is_sealed(f["ts"])]
    eod = _eod_flags(b1m, instr)
    spread = _spread_median(instr)
    boundary, gl = lockbox_boundary(), zones()["go_live"]
    arrs = (ts, op, hi, lo, cl)
    rset = RECIPE_SETS[RECIPE_SET_VERSION]
    out = {"instrument": instr, "pair": PAIR_OF.get(instr, instr),
           "status": ("provisional" if instr in PROVISIONAL_INSTRS
                      else "canonical"),
           "spread_charged_pts": spread,
           "recipes": {}}
    names = sorted({f["name"] for f in fires})
    for rname, recipe in rset.items():
        rows = {}
        for hname in names:
            hf = [f for f in fires if f["name"] == hname]
            trades = simulate(hf, arrs, atr_at, recipe, spread, eod)
            for wname, sel in (
                    ("backtest", lambda t: pd.Timestamp(t["entry_ts"])
                     < boundary),
                    ("forward", lambda t: pd.Timestamp(t["entry_ts"]) >= gl)):
                tw = [t for t in trades if sel(t)]
                if not tw:
                    continue
                p = np.array([t["pts"] for t in tw])
                by_sess = {}
                for t in tw:
                    by_sess[t["session"]] = round(
                        by_sess.get(t["session"], 0.0) + t["pts"], 1)
                rows.setdefault(hname, {})[wname] = {
                    "n": len(tw),
                    "win_rate_pct": round(100 * float((p > 0).mean()), 1),
                    "net_pts": round(float(p.sum()), 1),
                    "median_pts": round(float(np.median(p)), 2),
                    "biggest_win": round(float(p.max()), 1),
                    "biggest_loss": round(float(p.min()), 1),
                    "avg_duration_min": round(
                        float(np.mean([t["duration_min"] for t in tw])), 1),
                    "net_by_session": by_sess}
        out["recipes"][rname] = rows
    return out


def _emit(results, head):
    hdr = ["# Recipe Performance — points rollup (GENERATED by "
           "backtest.recipes)", "",
           f"Engine `{head[:9]}` · recipe set **{RECIPE_SET_VERSION}** "
           "(values ILLUSTRATIVE — awaiting operator ratification; changes "
           "only by re-registration, counted in the trial log).",
           "",
           "**OBSERVATIONAL ONLY** — touches nothing: not paper, not the "
           "ledger, not frozen_v1, not labels, not criteria. Directional "
           "fires only; same fires as the signal scoreboard, four harvests. "
           "Sealed windows and the lockbox span excluded. Points are "
           "mid-price MINUS each instrument's measured median cash spread "
           "per trade — idealized, not tradeable.",
           "",
           "**Honest-fill rules (operator-ruled 2026-08-19, part of every "
           "recipe's definition):** (1) intrabar stop+target both reachable "
           "-> stop fills, always; (2) gap through a level -> filled at the "
           "gapped (worse) price; (3) trailing stops ratchet only, "
           "evaluated on settled bars; (4) EOD flat at each instrument's "
           "native session close.", ""]
    L = list(hdr)
    for res in results:
        inst = res["instrument"]
        L += [f"## {inst} ({res['status'].upper()}; spread charged "
              f"{res['spread_charged_pts']} pts/trade)"]
        if res["status"] == "provisional":
            L += [f"> {PROVISIONAL_STAMP}"]
        L.append("")
        for wname in ("backtest", "forward"):
            # page-0 rollup: per recipe, hypotheses x sessions (+total)
            for rname, rows in res["recipes"].items():
                have = {h: w[wname] for h, w in rows.items() if wname in w}
                if not have:
                    continue
                sessions = sorted({s for v in have.values()
                                   for s in v["net_by_session"]})
                L += [f"### {inst} / {wname} / {rname} — net points",
                      "", "| H | " + " | ".join(sessions)
                      + " | TOTAL | n | win% | median |",
                      "|---|" + "---|" * (len(sessions) + 4)]
                for hname in sorted(have):
                    v = have[hname]
                    cells = [str(v["net_by_session"].get(s, "—"))
                             for s in sessions]
                    disp = hname.replace("S-", "")
                    L.append(f"| {disp} | " + " | ".join(cells)
                             + f" | **{v['net_pts']}** | {v['n']} "
                             f"| {v['win_rate_pct']}% | {v['median_pts']} |")
                L.append("")
            # recipe-comparison line per hypothesis: same fires, harvests
            names = sorted({h for r in res["recipes"].values() for h in r
                            if wname in r.get(h, {})})
            if names:
                L += [f"### {inst} / {wname} — recipe comparison "
                      f"(net pts | n; same fires, four harvests)", ""]
                rnames = list(res["recipes"])
                L += ["| H | " + " | ".join(rnames) + " |",
                      "|---|" + "---|" * len(rnames)]
                for hname in names:
                    cells = []
                    for rname in rnames:
                        v = res["recipes"][rname].get(hname, {}).get(wname)
                        cells.append(f"{v['net_pts']:+.0f} | " if False else
                                     (f"{v['net_pts']:+.0f} ({v['n']})"
                                      if v else "—"))
                    L.append(f"| {hname.replace('S-', '')} | "
                             + " | ".join(cells) + " |")
                L.append("")
    L += ["---", "", "Cards detail (biggest win/loss, durations, full "
          "per-session splits) in recipe_performance.json (same run)."]
    with open(os.path.join(OUT, "recipe_performance.md"), "w") as f:
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
        print(f"# recipes: {instr} ...", file=sys.stderr)
        results.append(run_instrument(instr))
    art = {"STAMP": ("OBSERVATIONAL recipe layer v0 — never validation; "
                     "idealized fills per the honest-fill rules"),
           "engine_commit": head, "recipe_set": RECIPE_SET_VERSION,
           "set_definition": {k: str(v) for k, v in
                              RECIPE_SETS[RECIPE_SET_VERSION].items()},
           "results": results}
    with open(os.path.join(OUT, "recipe_performance.json"), "w") as f:
        json.dump(art, f, indent=2, default=str)
    _emit(results, head)
    print(f"OBSERVATIONAL recipes -> {OUT}/recipe_performance.md")


if __name__ == "__main__":
    main()
