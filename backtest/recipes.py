"""Recipe layer — grammar v1 (register 41/42). OBSERVATIONAL ONLY:
nothing here touches paper, the ledger, frozen_v1, labels, or criteria.

GRAMMAR v1 (register 42; supersedes v0's single-stop form — v0 recipes
normalize into it unchanged):
  A recipe is ORDERED STAGES. Each stage:
    stop components (>=0, COMPOSED: effective stop = tightest, RATCHET-ONLY,
    evaluated on settled bars):
      ("fixed_pts", v)
      ("atr", k, tf)              # k x ATR(tf), tf DECLARED per component —
                                  # any ladder rung 1M/3M/5M/15M/30M/1H,
                                  # no implicit default
      ("trail_nth", N, (off_kind, off[, off_tf]), bar_tf)
                                  # beyond the Nth previous SETTLED bar of
                                  # bar_tf (the management TF); offset in
                                  # pts or k x ATR(off_tf)
      ("breakeven", off_pts)      # entry +/- offset; literature-adverse
                                  # caution registered (register 42d)
    target: ("fixed_pts", v) | ("atr", k, tf) | None
    exit_on / tighten_to: narrative-condition primitives (signal_watch
      NARRATIVE_EXIT_PRIMITIVES — the one-home rule). The excursion cut
      and flip-cut gates reported 2026-08-19 (registers 42-43); the gate
      was ruled NOT PASSED for universal flip-exits (net points is the
      deciding currency) — R-FLIPGUARD is the ONE registered staged
      candidate; per-hypothesis cherry-picks are a FORBIDDEN MOVE
      (register 44).
    until: ("progress_atr", k, tf) | ("progress_or_age", k, tf, minutes)
  Stop evaluation cadence is ALWAYS 1M, regardless of any component's TF.

HONEST-FILL RULES (operator-ruled 2026-08-19; unchanged; each pinned):
  1. Intrabar stop+target both reachable -> STOP fills, always.
  2. Gap through a level -> filled at the gapped (worse) price (the open).
  3. Trailing/composed stops RATCHET ONLY, evaluated on settled bars.
  4. EOD flat at each instrument's NATIVE session close.

Sets are versioned registry objects; a run's artifact states its set
version; additions/changes only by re-registration, counted in the trial
log. PROVENANCE per recipe (register 42 item 4): v0's R-FIX/R-ATR/R-TRAIL
values originated as operator examples in the design discussion, never
ratified; R-TRAIL-ATR's 0.5x offset was a reviewer invention with no
basis. R-OP1 is the FIRST RATIFIED-PROVENANCE recipe (operator-specified
2026-08-19; its ATR TF was unstated and 15M is an ASSUMPTION, flagged).
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

from engine.signal_watch import AGNOSTIC_ROWS, NARRATIVE_EXIT_PRIMITIVES
from engine.store_loader import is_sealed, lockbox_boundary, zones
from backtest.sessions import session_of
from backtest.scoreboard import (PAIR_OF, PROVISIONAL_INSTRS,
                                 PROVISIONAL_STAMP, _replay, _series,
                                 _atr15, h9_fires, make_cfg)
from engine.signal_watch import SignalWatch

OUT = os.path.join(ROOT, "reports", "scoreboard")

RECIPE_SET_VERSION = "recipe_set_v0.2"
RECIPE_SETS = {
    "recipe_set_v0.2": {
        # v0 four — ILLUSTRATIVE, unratified (provenance: operator design
        # examples; R-TRAIL-ATR offset a reviewer invention). ATR TFs
        # retro-annotated 15min (register 42b).
        "R-FIX": {"provenance": "illustrative-unratified",
                  "stages": [{"stop": [("fixed_pts", 10.0)],
                              "target": ("fixed_pts", 20.0)}]},
        "R-ATR": {"provenance": "illustrative-unratified",
                  "stages": [{"stop": [("atr", 1.5, "15min")],
                              "target": ("atr", 3.0, "15min")}]},
        "R-TRAIL": {"provenance": "illustrative-unratified",
                    "stages": [{"stop": [("trail_nth", 6, ("pts", 0.0),
                                          "1min")], "target": None}]},
        "R-TRAIL-ATR": {"provenance": "illustrative-unratified "
                                      "(offset: reviewer invention)",
                        "stages": [{"stop": [("trail_nth", 6,
                                              ("atr", 0.5, "15min"),
                                              "1min")], "target": None}]},
        # R-OP1 — operator-specified 2026-08-19 (register 42 item 6):
        # initial 1.5xATR (TF ASSUMED 15min — unstated, flagged) composed
        # with a 5.0pt trail beyond the 2nd-previous settled 1M bar;
        # tighter-of, ratchet-only, no target, trail live from entry.
        # FLAG: the 5.0pt offset is instrument-absolute; cross-instrument
        # v1 may want it ATR-relative — operator's later call.
        "R-OP1": {"provenance": "operator-ratified 2026-08-19 "
                                "(ATR TF assumed 15min, flagged)",
                  "stages": [{"stop": [("atr", 1.5, "15min"),
                                       ("trail_nth", 2, ("pts", 5.0),
                                        "1min")], "target": None}]},
        # R-FLIPGUARD — the ONE staged narrative candidate (register 44,
        # counted): flip-exit ACTIVE ONLY BEFORE the progress-arming
        # transition. Derivation cited to the early-flip adversity (7/8
        # contexts) and t-MFE 13-45 min findings — NOT the counterfactual
        # cells (the per-hypothesis cherry-pick is a registered forbidden
        # move). Arming values DERIVED-STATED (1.0xATR(15M) progress OR
        # 45 min age), ratification pending; graded on forward accrual
        # alongside R-OP1; ratification before any status.
        "R-FLIPGUARD": {"provenance": "staged candidate (register 44; "
                                      "arming values derived-stated, "
                                      "ratification pending)",
                        "stages": [
                            {"stop": [("atr", 1.5, "15min"),
                                      ("trail_nth", 2, ("pts", 5.0),
                                       "1min")], "target": None,
                             "exit_on": [("trend_flip",)],
                             "until": ("progress_or_age", 1.0, "15min",
                                       45)},
                            {"stop": [("atr", 1.5, "15min"),
                                      ("trail_nth", 2, ("pts", 5.0),
                                       "1min")], "target": None}]},
    },
}


def _norm_component(c):
    kind = c[0]
    if kind == "fixed_pts":
        return {"kind": "fixed_pts", "v": float(c[1])}
    if kind == "atr":
        if len(c) < 3:
            raise ValueError("ATR component requires a declared TF "
                             "(register 42b: no implicit default)")
        return {"kind": "atr", "k": float(c[1]), "tf": c[2]}
    if kind == "trail_nth":
        off = c[2]
        if off[0] == "atr" and len(off) < 3:
            raise ValueError("ATR offset requires a declared TF")
        return {"kind": "trail_nth", "n": int(c[1]),
                "off_kind": off[0], "off": float(off[1]),
                "off_tf": off[2] if off[0] == "atr" else None,
                "bar_tf": c[3]}
    if kind == "breakeven":
        return {"kind": "breakeven", "off": float(c[1])}
    raise ValueError(c)


def normalize(recipe):
    stages = []
    for st in recipe["stages"]:
        for cond in st.get("exit_on", []) + st.get("tighten_to", []):
            if cond[0] not in NARRATIVE_EXIT_PRIMITIVES:
                raise ValueError(f"unregistered narrative primitive {cond}")
        stages.append({
            "stop": [_norm_component(c) for c in st.get("stop", [])],
            "target": st.get("target"),
            "until": st.get("until"),
            "exit_on": st.get("exit_on", []),
        })
    return stages


class Env:
    """Per-instrument simulation environment: 1M arrays, per-rung settled
    bars, per-rung ATR (trailing mean TR over context.atr_period of that
    rung's bars), EOD flags, narrative event streams (optional)."""

    def __init__(self, arrs1m, atr_by_tf, rung_bars, eod_flag, narr=None):
        self.ts, self.o, self.h, self.l, self.c = arrs1m
        self.atr_by_tf = atr_by_tf          # tf -> sorted {close_ts: atr}
        self.rung = rung_bars               # tf -> (ts_close_ns, high, low)
        self.eod = eod_flag
        self.narr = narr or {}              # key -> sorted [(ts_ns, dir)]

    def atr_at(self, tf, t_ns):
        d = self.atr_by_tf[tf]
        keys = d["keys"]
        i = np.searchsorted(keys, t_ns, side="right") - 1
        return d["vals"][i] if i >= 0 else None

    def trail_ref(self, tf, n, j):
        """Extreme of the Nth previous SETTLED bar of `tf` at 1M bar j.
        Settled = rung close <= this 1M bar's open."""
        rts, rh, rl = self.rung[tf]
        open_ns = self.ts[j] - 60_000_000_000
        s = np.searchsorted(rts, open_ns, side="right") - 1
        ref = s - (n - 1)
        if ref < 0:
            return None, None
        return rh[ref], rl[ref]


def _target_level(spec, entry, d, env, t0):
    if spec is None:
        return None
    if spec[0] == "fixed_pts":
        return entry + d * spec[1]
    if spec[0] == "atr":
        a = env.atr_at(spec[2], t0)
        return None if a is None else entry + d * spec[1] * a
    raise ValueError(spec)


def simulate(fires, env, recipe, spread):
    """v1 engine. Deterministic (twin-run bit-identity pinned)."""
    stages = normalize(recipe)
    ts, o, h, l, c = env.ts, env.o, env.h, env.l, env.c
    n = len(ts)
    trades = []
    open_until = -1
    for f in sorted(fires, key=lambda x: x["ts"].value):
        fi = np.searchsorted(ts, f["ts"].value, side="right") - 1
        ei = fi + 1
        if fi < 0 or ei >= n or ei <= open_until:
            continue
        d = f["dir"]
        entry = o[ei]
        t0 = ts[ei]
        # static component levels resolved at entry
        stage_i = 0
        eff_stop = None
        exit_px = exit_ts = reason = None
        fav_ext = -np.inf                   # settled favorable excursion
        j = ei
        while j < n:
            st = stages[stage_i]
            # stage transition (settled evaluation, before this bar)
            if st["until"] is not None and stage_i + 1 < len(stages):
                u = st["until"]
                armed = False
                if u[0] == "progress_atr":
                    a0 = env.atr_at(u[2], t0)
                    armed = a0 is not None and fav_ext >= u[1] * a0
                elif u[0] == "progress_or_age":
                    a0 = env.atr_at(u[2], t0)
                    armed = ((a0 is not None and fav_ext >= u[1] * a0)
                             or (ts[j] - t0) >= u[3] * 60_000_000_000)
                else:
                    raise ValueError(u)
                if armed:
                    stage_i += 1
                    st = stages[stage_i]
            # compose candidate stop = tightest of components (settled)
            cands = []
            for comp in st["stop"]:
                if comp["kind"] == "fixed_pts":
                    cands.append(entry - d * comp["v"])
                elif comp["kind"] == "atr":
                    a = env.atr_at(comp["tf"], t0)
                    if a is not None:
                        cands.append(entry - d * comp["k"] * a)
                elif comp["kind"] == "breakeven":
                    cands.append(entry + d * comp["off"])
                elif comp["kind"] == "trail_nth":
                    rh, rl = env.trail_ref(comp["bar_tf"], comp["n"], j)
                    if rh is not None:
                        off = comp["off"]
                        if comp["off_kind"] == "atr":
                            a = env.atr_at(comp["off_tf"], t0)
                            off = 0.0 if a is None else off * a
                        cands.append((rl - off) if d == 1 else (rh + off))
            if cands:
                tight = max(cands) if d == 1 else min(cands)
                # rule 3: the EFFECTIVE stop ratchets only
                eff_stop = tight if eff_stop is None else (
                    max(eff_stop, tight) if d == 1 else min(eff_stop, tight))
            target = _target_level(st["target"], entry, d, env, t0)
            # narrative exits: settled events inside the PREVIOUS bar
            narr_hit = False
            for cond in st["exit_on"]:
                key = cond[0] if isinstance(cond, (list, tuple)) else cond
                evs = env.narr.get(key, [])
                lo_ns, hi_ns = ts[j] - 60_000_000_000, ts[j]
                a = np.searchsorted([e[0] for e in evs], lo_ns, side="right")
                for e in evs[a:]:
                    if e[0] > hi_ns:
                        break
                    if e[1] == 0 or e[1] == -d:
                        narr_hit = True
                        break
            if eff_stop is not None:
                if (d == 1 and o[j] <= eff_stop) or (d == -1
                                                     and o[j] >= eff_stop):
                    exit_px, reason = o[j], "stop_gap"      # rule 2
                    break
            if target is not None:
                if (d == 1 and o[j] >= target) or (d == -1
                                                   and o[j] <= target):
                    exit_px, reason = o[j], "target_gap"    # rule 2
                    break
            stop_hit = eff_stop is not None and (
                l[j] <= eff_stop if d == 1 else h[j] >= eff_stop)
            tgt_hit = target is not None and (
                h[j] >= target if d == 1 else l[j] <= target)
            if stop_hit:                                    # rule 1
                exit_px, reason = eff_stop, "stop"
                break
            if tgt_hit:
                exit_px, reason = target, "target"
                break
            if narr_hit:                    # settled-bar close exit
                exit_px, reason = c[j], "narrative"
                break
            if env.eod[j]:                                  # rule 4
                exit_px, reason = c[j], "eod"
                break
            fav_ext = max(fav_ext, (h[j] - entry) if d == 1
                          else (entry - l[j]))
            j += 1
        if exit_px is None:
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


def _rung_data(bars_dict, atr_period):
    """Per-rung settled arrays + ATR maps for every available TF."""
    atr_by_tf, rung = {}, {}
    for key, blist in bars_dict.items():
        tf = key.split(":")[-1]
        live = [b for b in blist if not b.is_stub]
        if not live:
            continue
        rung[tf] = (np.array([b.ts.value for b in live]),
                    np.array([b.high for b in live]),
                    np.array([b.low for b in live]))
        amap = _atr15(live, atr_period)
        keys = np.array([k.value for k in sorted(amap)])
        vals = [amap[k] for k in sorted(amap)]
        atr_by_tf[tf] = {"keys": keys, "vals": vals}
    return atr_by_tf, rung


def build_env(instr, cfg, bars, narr=None):
    b1m_all = bars[cfg.mtf.execution_tf]
    b1m = [x for x in b1m_all if not x.is_stub]
    ts, cl, hi, lo, _segs, _b = _series(b1m_all)
    op = np.array([x.open for x in b1m])
    atr_by_tf, rung = _rung_data(bars, cfg.context.atr_period)
    eod = _eod_flags(b1m, instr)
    return Env((ts, op, hi, lo, cl), atr_by_tf, rung, eod, narr)


def run_instrument(instr):
    cfg = make_cfg({"session_model.extended_hours": True,
                    "session_model.ladder": True,
                    "debug.structure": True})   # trend flips for R-FLIPGUARD
    watch = SignalWatch()
    engine, bars, _ = _replay(cfg, instr, engine_hook=watch.attach)
    flips, prev = [], 0
    for e in engine.narrative.events:
        if e["type"] == "PHASE_EVAL" and e.get("tf") == "1min":
            t = e.get("trend", 0)
            if t != prev and t != 0:
                flips.append((pd.Timestamp(e["ts"]).value, t))
            prev = t
    env = build_env(instr, cfg, bars, narr={"trend_flip": sorted(flips)})
    fires = watch.fires + h9_fires(engine.narrative.events, cfg)
    fires = [f for f in fires
             if f["name"] not in AGNOSTIC_ROWS and not is_sealed(f["ts"])]
    spread = _spread_median(instr)
    boundary, gl = lockbox_boundary(), zones()["go_live"]
    rset = RECIPE_SETS[RECIPE_SET_VERSION]
    out = {"instrument": instr, "pair": PAIR_OF.get(instr, instr),
           "status": ("provisional" if instr in PROVISIONAL_INSTRS
                      else "canonical"),
           "spread_charged_pts": spread, "recipes": {}}
    names = sorted({f["name"] for f in fires})
    for rname, recipe in rset.items():
        rows = {"_provenance": recipe["provenance"]}
        for hname in names:
            hf = [f for f in fires if f["name"] == hname]
            trades = simulate(hf, env, recipe, spread)
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
    L = ["# Recipe Performance — points rollup (GENERATED by "
         "backtest.recipes)", "",
         f"Engine `{head[:9]}` · recipe set **{RECIPE_SET_VERSION}** "
         "(grammar v1, register 42). Per-recipe PROVENANCE printed in every "
         "table; illustrative values remain unratified; R-OP1 is "
         "operator-ratified (ATR TF assumed 15M, flagged).",
         "",
         "**OBSERVATIONAL ONLY** — touches nothing: not paper, not the "
         "ledger, not frozen_v1, not labels, not criteria. Directional "
         "fires only; same fires as the signal scoreboard. Sealed windows "
         "and the lockbox span excluded. Points are mid-price minus each "
         "instrument's measured median cash spread per trade — idealized.",
         "",
         "**Honest-fill rules (operator-ruled, part of every recipe's "
         "definition):** (1) both reachable -> stop always; (2) gap -> "
         "gapped (worse) price; (3) composed/trailing stops ratchet only, "
         "settled bars; (4) EOD flat at native session close.", ""]
    for res in results:
        inst = res["instrument"]
        L += [f"## {inst} ({res['status'].upper()}; spread charged "
              f"{res['spread_charged_pts']} pts/trade)"]
        if res["status"] == "provisional":
            L += [f"> {PROVISIONAL_STAMP}"]
        L.append("")
        for wname in ("backtest", "forward"):
            for rname, rows in res["recipes"].items():
                have = {h: w[wname] for h, w in rows.items()
                        if h != "_provenance" and wname in w}
                if not have:
                    continue
                sessions = sorted({s for v in have.values()
                                   for s in v["net_by_session"]})
                L += [f"### {inst} / {wname} / {rname} "
                      f"[{rows['_provenance']}] — net points",
                      "", "| H | " + " | ".join(sessions)
                      + " | TOTAL | n | win% | median |",
                      "|---|" + "---|" * (len(sessions) + 4)]
                for hname in sorted(have):
                    v = have[hname]
                    cells = [str(v["net_by_session"].get(s, "—"))
                             for s in sessions]
                    L.append(f"| {hname.replace('S-', '')} | "
                             + " | ".join(cells)
                             + f" | **{v['net_pts']}** | {v['n']} "
                             f"| {v['win_rate_pct']}% | {v['median_pts']} |")
                L.append("")
            names = sorted({h for r in res["recipes"].values() for h in r
                            if h != "_provenance" and wname in r.get(h, {})})
            if names:
                rnames = list(res["recipes"])
                L += [f"### {inst} / {wname} — recipe comparison "
                      f"(net pts (n); same fires)", "",
                      "| H | " + " | ".join(rnames) + " |",
                      "|---|" + "---|" * len(rnames)]
                for hname in names:
                    cells = []
                    for rname in rnames:
                        v = res["recipes"][rname].get(hname, {}).get(wname)
                        cells.append(f"{v['net_pts']:+.0f} ({v['n']})"
                                     if v else "—")
                    L.append(f"| {hname.replace('S-', '')} | "
                             + " | ".join(cells) + " |")
                L.append("")
    L += ["---", "", "Cards detail in recipe_performance.json (same run)."]
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
    art = {"STAMP": ("OBSERVATIONAL recipe layer (grammar v1) — never "
                     "validation; idealized fills per the honest-fill "
                     "rules"),
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
