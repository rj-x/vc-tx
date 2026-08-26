"""Account-mode simulation — the bankroll lens (register 83;
pre-registered prereg_account_mode). Activated through the campaign by
--pot; runnable standalone: venv/bin/python -m backtest.account_mode.

FENCES (register 83 clause 6): ACCOUNT MODE IS A BANKROLL LENS, NEVER
EVIDENCE — no signal, recipe, or label decision cites account curves;
points physics remains the evidence layer.

MECHANICS: UK spread betting — P&L is TAX-FREE (no haircut anywhere in
the arithmetic); costs are all-in-spread (PROVIDER-MARKUP CAVEAT: the
measured feed spread may understate live bet spreads — operator to
eyeball live quotes once; --spread-markup adds pts for sensitivity
runs); EOD-flat everywhere makes overnight funding ignorable. SIZING =
FIXED STAKE with a RISK GATE (operator practice — pass on the trade,
never shrink it): stop_points x stake <= balance x risk% else
SKIPPED_RISK; margin refusals SKIPPED_MARGIN (deposit = stake x price /
leverage; concurrent deposits sum). PROVIDER_CLOSEOUT: if a position's
adverse excursion drags equity below the maintenance level (default
50% of its deposit requirement), it closes THERE, before the stop —
the true small-account ruin mechanism. LIMITATION, stated: equity
marking is per-position (concurrent positions' simultaneous marks are
not netted bar-by-bar). RUIN = balance <= 0, or balance below the
minimum deposit for a minimum-stake position after a closeout —
simulation ends at the blowing trade, timestamped.

--exec-tf selects the ATR/MANAGEMENT scale only (stops and trails);
SIGNALS REMAIN THE REGISTERED STACK — re-deriving signals on another
timeframe would be a NEW REGISTRATION. Available scales: the ladder
rungs (1M/3M/5M/15M/30M/1H); 4H/D1 are not in the current ladder and
are refused with a message, flagged.

Honest fills (rule 5 included), spread, re-fire dedup, sealed/lockbox
exclusions all inherited unchanged from the journal machinery.
Defaults FLAGGED OPERATOR-UNVERIFIED: leverage 200:1 (calibrating fact
recorded: operator-observed GBP 1/pt on GBP 25 deposit), maintenance
50%, per-instrument minimum stake GBP 0.5 (operator to verify minis).
"""

import argparse
import csv
import json
import os
import subprocess
import sys

import numpy as np
import pandas as pd

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "scripts"))

from engine.signal_watch import AGNOSTIC_ROWS, SignalWatch
from engine.store_loader import is_sealed
from backtest.recipes import (RECIPE_SET_VERSION, RECIPE_SETS,
                              _spread_median, build_env, simulate)
from backtest.scoreboard import (_replay, event_derived_fires, make_cfg)
from backtest.signal_points import baseline_fires
from backtest.trade_layer import VARIANTS, dedup_fires

OUT = os.path.join(ROOT, "reports", "scoreboard")
CURVE_CSV = os.path.join(ROOT, "reports", "account_curve.csv")

TF_ALIAS = {"1M": "1min", "3M": "3min", "5M": "5min", "15M": "15min",
            "30M": "30min", "1H": "1h", "4H": "4h", "D1": "1d"}
LADDER_AVAILABLE = ("1min", "3min", "5min", "15min", "30min", "1h")
STAKE_DEFAULT = 0.5          # GBP/pt, spread-bet native
LEVERAGE_DEFAULT = 200       # FLAGGED operator-unverified (calibrating
                             # fact: GBP1/pt on GBP25 observed)
MAINTENANCE_PCT = 0.5        # of deposit requirement; FLAGGED
MIN_STAKE_DEFAULT = 0.5      # per instrument; operator to verify minis
INITIAL_STOP_ATR = 2.5       # the registered ladder-v2 initial stop


def transform_recipe(recipe, tf):
    """Re-scale a recipe's ATR/trail components to the exec TF. Signals
    are untouched — this is management scale only (register 83)."""
    out = {"provenance": recipe.get("provenance", "")
           + f" [account-lens exec-tf {tf}]", "stages": []}
    for st in recipe["stages"]:
        ns = dict(st)
        stop = []
        for comp in st.get("stop", []):
            if comp[0] == "atr":
                stop.append(("atr", comp[1], tf))
            elif comp[0] == "trail_nth":
                off = comp[2]
                off2 = (("atr", off[1], tf) if off[0] == "atr" else off)
                stop.append(("trail_nth", comp[1], off2, tf))
            else:
                stop.append(comp)
        ns["stop"] = stop
        out["stages"].append(ns)
    return out


def account_pass(trades, pot, risk_pct, stake, leverage, maintenance_pct,
                 min_stake):
    """Strict fill-order bankroll pass. Deterministic (pinned).
    trades: sorted by entry ts; each needs entry_ts, exit_ts, pts,
    stop_pts, mae_pts, entry price. Returns (curve_rows, summary)."""
    balance = float(pot)
    open_pos = []            # (exit_ts, deposit)
    rows = []
    skipped_risk = skipped_margin = closeouts = 0
    ruin = None
    for t in trades:
        # settle positions closed before this entry
        open_pos = [p for p in open_pos if p[0] > t["entry_ts"]]
        margin_used = sum(p[1] for p in open_pos)
        deposit = stake * t["entry"] / leverage
        reason = t["reason"]
        pnl = None
        if t["stop_pts"] * stake > balance * risk_pct / 100.0:
            gate = "SKIPPED_RISK"
            skipped_risk += 1
        elif margin_used + deposit > balance:
            gate = "SKIPPED_MARGIN"
            skipped_margin += 1
        else:
            gate = "TAKEN"
            maint = maintenance_pct * deposit
            worst_equity = balance - stake * t["mae_pts"]
            if worst_equity < maint:
                closeouts += 1
                reason = "PROVIDER_CLOSEOUT"
                pnl = (maint - balance)      # closes at maintenance
            else:
                pnl = stake * t["pts"]
            balance = balance + pnl
            open_pos.append((t["exit_ts"], deposit))
        rows.append({"entry_ts": str(t["entry_ts"]),
                     "exit_ts": str(t["exit_ts"]),
                     "instrument": t["instrument"],
                     "sentence_id": t["name"], "gate": gate,
                     "stake": stake, "stop_pts": round(t["stop_pts"], 1),
                     "risk_gbp": round(t["stop_pts"] * stake, 2),
                     "risk_budget_gbp": round(balance * risk_pct / 100.0,
                                              2),
                     "pnl_gbp": (round(pnl, 2) if pnl is not None
                                 else None),
                     "exit_reason": reason,
                     "balance": round(balance, 2)})
        if balance <= 0 or (reason == "PROVIDER_CLOSEOUT"
                            and balance < min_stake * t["entry"]
                            / leverage):
            ruin = str(t["exit_ts"])
            break
    peak = float(pot)
    max_dd = 0.0
    for r in rows:
        peak = max(peak, r["balance"])
        max_dd = max(max_dd, peak - r["balance"])
    return rows, {"end_balance": round(balance, 2),
                  "max_drawdown_gbp": round(max_dd, 2),
                  "max_drawdown_pct": (round(100 * max_dd / peak, 1)
                                       if peak else None),
                  "ruin": ruin, "skipped_risk": skipped_risk,
                  "skipped_margin": skipped_margin,
                  "provider_closeouts": closeouts,
                  "taken": sum(1 for r in rows if r["gate"] == "TAKEN")}


def collect_trades(instr, exec_tfs, variants, spread_markup):
    """One replay; per exec-TF x variant simulate with the transformed
    recipe; annotate stop_pts (INITIAL_STOP_ATR x ATR(tf)) and MAE."""
    cfg = make_cfg({"session_model.extended_hours": True,
                    "session_model.ladder": True,
                    "debug.structure": True})
    watch = SignalWatch()
    engine, bars, _ = _replay(cfg, instr, engine_hook=watch.attach)
    env = build_env(instr, cfg, bars)
    fires = watch.fires + event_derived_fires(engine.narrative.events,
                                              cfg, bars, instr=instr)
    fires = dedup_fires([f for f in fires
                         if f["name"] not in AGNOSTIC_ROWS
                         and not is_sealed(f["ts"])])
    spread = _spread_median(instr) + spread_markup
    ts, o, h, l, c = env.ts, env.o, env.h, env.l, env.c
    rset = RECIPE_SETS[RECIPE_SET_VERSION]
    out = {}
    floors = {}
    members = baseline_fires(env, engine.narrative.events)["B-RANDOM"]
    names = sorted({f["name"] for f in fires})
    for tf in exec_tfs:
        for variant in variants:
            recipe = transform_recipe(rset[variant], tf)
            key = (tf, variant)
            tl = []
            for name in names:
                nf = [f for f in fires if f["name"] == name]
                for t in simulate(nf, env, recipe, spread):
                    ei = int(np.searchsorted(
                        ts, pd.Timestamp(t["entry_ts"]).value,
                        side="left"))
                    xi = min(len(ts) - 1, ei + int(t["duration_min"]))
                    d = t["dir"]
                    a0 = env.atr_at(tf, ts[ei])
                    if not a0:
                        continue
                    mae = max([0.0] + [
                        (t["entry"] - l[j]) if d == 1
                        else (h[j] - t["entry"])
                        for j in range(ei, xi + 1)])
                    tl.append({"instrument": instr, "name": name,
                               "entry_ts": pd.Timestamp(t["entry_ts"]),
                               "exit_ts": pd.Timestamp(t["entry_ts"])
                               + pd.Timedelta(minutes=t["duration_min"]),
                               "entry": t["entry"], "pts": t["pts"],
                               "session": t["session"],
                               "stop_pts": INITIAL_STOP_ATR * a0,
                               "mae_pts": mae})
            out[key] = tl
            fl = []
            for mf in members:
                bt = simulate(mf, env, recipe, spread)
                if bt:
                    fl.append(float(np.median([x["pts"] for x in bt])))
            floors[key] = fl
    return out, floors


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--pot", type=float, required=True)
    ap.add_argument("--risk-pct", type=float, default=2.0)
    ap.add_argument("--stake", type=float, default=STAKE_DEFAULT)
    ap.add_argument("--exec-tf", nargs="+", default=["15M"],
                    choices=list(TF_ALIAS))
    ap.add_argument("--leverage", type=float, default=LEVERAGE_DEFAULT)
    ap.add_argument("--maintenance-pct", type=float,
                    default=MAINTENANCE_PCT)
    ap.add_argument("--min-stake", type=float, default=MIN_STAKE_DEFAULT)
    ap.add_argument("--spread-markup", type=float, default=0.0)
    ap.add_argument("--variants", nargs="+", default=list(VARIANTS))
    ap.add_argument("--from", dest="dfrom", default=None)
    ap.add_argument("--to", dest="dto", default=None)
    ap.add_argument("--instr", nargs="*",
                    default=["uk100fut", "ger40fut", "nas100fut", "us30fut"])
    a = ap.parse_args(argv)
    if a.dfrom:
        os.environ["VC_PERIOD_FROM"] = a.dfrom
    if a.dto:
        os.environ["VC_PERIOD_TO"] = a.dto
    tfs = []
    for t in a.exec_tf:
        tf = TF_ALIAS[t]
        if tf not in LADDER_AVAILABLE:
            print(f"!! exec-tf {t} not in the current ladder "
                  f"({'/'.join(LADDER_AVAILABLE)}) — refused, flagged")
            continue
        tfs.append(tf)
    head = subprocess.run(["git", "rev-parse", "HEAD"], cwd=ROOT,
                          capture_output=True, text=True).stdout.strip()
    all_trades = {}
    all_floors = {}
    for instr in a.instr:
        print(f"# account_mode: {instr} ...", file=sys.stderr)
        tr, fl = collect_trades(instr, tfs, a.variants, a.spread_markup)
        for k, v in tr.items():
            all_trades.setdefault(k, []).extend(v)
        for k, v in fl.items():
            all_floors.setdefault(k, []).extend(v)
    curves = {}
    census = []
    curve_rows_all = []
    for (tf, variant), tl in sorted(all_trades.items()):
        tl.sort(key=lambda t: t["entry_ts"].value)
        tl2 = [dict(t, reason="close") for t in tl]
        rows, summary = account_pass(tl2, a.pot, a.risk_pct, a.stake,
                                     a.leverage, a.maintenance_pct,
                                     a.min_stake)
        curves[f"{tf}|{variant}"] = summary
        for r in rows:
            r["exec_tf"], r["variant"] = tf, variant
            curve_rows_all.append(r)
        # accessibility census per signal
        for name in sorted({t["name"] for t in tl}):
            sub = [t for t in tl if t["name"] == name]
            acc = [t for t in sub if t["stop_pts"] * a.stake
                   <= a.pot * a.risk_pct / 100.0]
            fl = all_floors.get((tf, variant), [])
            row = {"exec_tf": tf, "variant": variant, "sentence": name,
                   "n_total": len(sub), "n_accessible": len(acc),
                   "pass_frac": round(len(acc) / len(sub), 3)
                   if sub else None}
            if acc:
                med = round(float(np.median([t["pts"] for t in acc])), 2)
                row.update({
                    "accessible_median_pts": med,
                    "floor_median": (round(float(np.median(fl)), 2)
                                     if fl else None),
                    "floor_max": (round(float(max(fl)), 2)
                                  if fl else None),
                    "clears_floor": (fl and med > max(fl)) or False,
                    "session_mix": {
                        s: sum(1 for t in acc if t["session"] == s)
                        for s in sorted({t["session"] for t in acc})}})
            census.append(row)
    with open(CURVE_CSV, "w", newline="") as f:
        cols = ["exec_tf", "variant", "entry_ts", "exit_ts",
                "instrument", "sentence_id", "gate", "stake",
                "stop_pts", "risk_gbp", "risk_budget_gbp", "pnl_gbp",
                "exit_reason", "balance"]
        w = csv.DictWriter(f, fieldnames=cols)
        w.writeheader()
        w.writerows({k: r.get(k) for k in cols} for r in curve_rows_all)
    params = {"pot": a.pot, "risk_pct": a.risk_pct, "stake": a.stake,
              "exec_tf": tfs, "leverage_FLAGGED": a.leverage,
              "maintenance_pct_FLAGGED": a.maintenance_pct,
              "min_stake_OPERATOR_TO_VERIFY": a.min_stake,
              "spread_markup": a.spread_markup,
              "variants": a.variants,
              "period": [a.dfrom, a.dto]}
    art = {"STAMP": ("ACCOUNT-MODE BANKROLL LENS — NEVER EVIDENCE "
                     "(register 83): no signal, recipe, or label "
                     "decision cites account curves; points physics is "
                     "the evidence layer. Tax-free spread-bet "
                     "arithmetic; provider-markup caveat flagged."),
           "engine_commit": head, "parameters": params,
           "curves": curves, "accessibility_census": census}
    with open(os.path.join(OUT, "account_mode.json"), "w") as f:
        json.dump(art, f, indent=2, default=str)
    L = ["# Account Mode — the bankroll lens (GENERATED by "
         "backtest.account_mode)", "",
         "Terms: [docs/GLOSSARY.md](../../docs/GLOSSARY.md).", "",
         f"Engine `{head[:9]}` — **BANKROLL LENS, NEVER EVIDENCE "
         "(register 83).** THE OPERATOR'S REAL QUESTION: what fraction "
         "of the book can this bankroll touch, and does the accessible "
         "fraction carry edge? UK spread betting: P&L tax-free (no "
         "haircut anywhere); all-in-spread costs (provider-markup "
         "caveat: measured feed spreads may understate live bet "
         "spreads); EOD-flat makes overnight funding ignorable. Sizing "
         "= fixed stake + risk gate (pass, never shrink). Equity "
         "marking is per-position (limitation stated). Defaults "
         "FLAGGED operator-unverified: leverage "
         f"{a.leverage:g}:1, maintenance {a.maintenance_pct:g}, min "
         f"stake {a.min_stake:g}.", "",
         f"**Parameters:** pot £{a.pot:g}, risk {a.risk_pct:g}%, stake "
         f"£{a.stake:g}/pt, exec-TF {tfs}, spread markup "
         f"{a.spread_markup:g} pts, period {a.dfrom}..{a.dto}.", "",
         "| exec-TF | variant | end £ | maxDD £ (%) | ruin | taken | "
         "skip-risk | skip-margin | closeouts |",
         "|---|---|---|---|---|---|---|---|---|"]
    for key, s2 in sorted(curves.items()):
        tf, variant = key.split("|")
        L.append(f"| {tf} | {variant} | {s2['end_balance']} "
                 f"| {s2['max_drawdown_gbp']} "
                 f"({s2['max_drawdown_pct']}%) "
                 f"| {s2['ruin'] or 'survived'} | {s2['taken']} "
                 f"| {s2['skipped_risk']} | {s2['skipped_margin']} "
                 f"| {s2['provider_closeouts']} |")
    L += ["", "## Accessibility census (headline): pass fraction + the "
          "points-physics of the ACCESSIBLE subset only", "",
          "| exec-TF | variant | sentence | n | accessible | pass % | "
          "acc median pts | floor med/max | clears |",
          "|---|---|---|---|---|---|---|---|---|"]
    for r in census:
        pf = (f"{100 * r['pass_frac']:.0f}%"
              if r["pass_frac"] is not None else "—")
        L.append(f"| {r['exec_tf']} | {r['variant']} | {r['sentence']} "
                 f"| {r['n_total']} | {r['n_accessible']} | {pf} "
                 f"| {r.get('accessible_median_pts', '—')} "
                 f"| {r.get('floor_median', '—')}/"
                 f"{r.get('floor_max', '—')} "
                 f"| {'YES' if r.get('clears_floor') else '—'} |")
    L.append("")
    with open(os.path.join(OUT, "account_mode.md"), "w") as f:
        f.write("\n".join(L))
    print(f"BANKROLL LENS -> {OUT}/account_mode.md + {CURVE_CSV}")


if __name__ == "__main__":
    main()
