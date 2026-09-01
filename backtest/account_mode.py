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

RESTRUCTURE (register 86, operator + reviewer 2026-08-27): the blended
everything-at-once single stream is RETIRED (reason recorded: it
interleaved mutually exclusive management schemes and all sentences
into one balance — an account nobody would run; the final blended
artifact is archived). Each (variant x sentence) pair now simulates as
its OWN ISOLATED ACCOUNT — one pot, one balance, hunting across the
operator-scoped instrument set (--instruments comma-list, default the
four canonical; scope abbreviated in filenames: all4 / ex-<mkt> /
joined shorts). CROSS-INSTRUMENT COLLISION RULE: strict fill-order
first-come — a subsequent entry is refused (SKIPPED_RISK) when
combined open risk would breach the gate. Outputs:
reports/account_curves/<variant>_<sentence>__<scope>.csv (leading '#'
header line; footer line = quick read, tail -n 1) plus
reports/account_curves/_LEADERBOARD.csv (field-honesty header;
summary pair account_mode.md|.json emits in the SAME directory —
the scoreboard pair was archived by operator order 2026-08-28,
ARCHIVE_LOG; one home for the lens;
B-RANDOM member curves per variant as the luck reference;
leaderboard-top is best-of-field by construction). ALL CURVES BORN
EX-LOCKBOX (register 85): lockbox-span entries excluded, counts
reconciled in every header. --exec-tf takes ONE scale per run (the
filename layout); default 1M — the only scale register 83's read found
accessible at small pots (implementer choice, stated).
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
from engine.store_loader import in_lockbox_span, is_sealed
from backtest.recipes import (RECIPE_SET_VERSION, RECIPE_SETS,
                              _spread_median, build_env, simulate)
from backtest.scoreboard import (_replay, event_derived_fires, make_cfg)
from backtest.signal_points import baseline_fires
from backtest.trade_layer import VARIANTS, dedup_fires

OUT = os.path.join(ROOT, "reports", "scoreboard")
CURVES_DIR = os.path.join(ROOT, "reports", "account_curves")
LEADERBOARD_CSV = os.path.join(CURVES_DIR, "_LEADERBOARD.csv")

CANONICAL_INSTRUMENTS = ("uk100fut", "ger40fut", "nas100fut",
                         "us30fut")
SCOPE_SHORT = {"uk100fut": "uk100", "ger40fut": "ger40",
               "nas100fut": "nas", "us30fut": "us30"}
EXEC_TF_DEFAULT = "1M"       # register 86: the one scale register 83's
                             # read found accessible at small pots
                             # (implementer choice, stated)

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
    stop_pts, mae_pts, entry price. Returns (curve_rows, summary).
    COLLISION RULE (register 86): first-come — a subsequent entry is
    refused (SKIPPED_RISK) when COMBINED open risk (this trade's plus
    all still-open positions') would breach the gate."""
    balance = float(pot)
    open_pos = []            # (exit_ts, deposit, risk_gbp)
    rows = []
    skipped_risk = skipped_margin = closeouts = 0
    ruin = None
    for t in trades:
        # settle positions closed before this entry
        open_pos = [p for p in open_pos if p[0] > t["entry_ts"]]
        margin_used = sum(p[1] for p in open_pos)
        open_risk = sum(p[2] for p in open_pos)
        deposit = stake * t["entry"] / leverage
        this_risk = t["stop_pts"] * stake
        reason = t["reason"]
        pnl = None
        if this_risk + open_risk > balance * risk_pct / 100.0:
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
            open_pos.append((t["exit_ts"], deposit, this_risk))
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


def scope_slug(instruments):
    """Filename abbreviation for an instrument scope (register 86):
    all4 | ex-<missing market> | joined shorts (canonical order)."""
    s = ([i for i in CANONICAL_INSTRUMENTS if i in instruments]
         + sorted(i for i in instruments
                  if i not in CANONICAL_INSTRUMENTS))
    if set(s) == set(CANONICAL_INSTRUMENTS):
        return "all4"
    if len(s) == 3 and all(i in CANONICAL_INSTRUMENTS for i in s):
        missing = next(i for i in CANONICAL_INSTRUMENTS if i not in s)
        return "ex-" + SCOPE_SHORT[missing]
    return "-".join(SCOPE_SHORT.get(i, i) for i in s)


def collect_trades(instr, tf, variants, spread_markup):
    """One replay; per variant simulate with the transformed recipe;
    annotate stop_pts (INITIAL_STOP_ATR x ATR(tf)) and MAE. Returns
    per-strategy trade lists, B-RANDOM member trade lists, and the
    lockbox-span exclusion count (register 85: curves born ex-lockbox)."""
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
    members = baseline_fires(env, engine.narrative.events)["B-RANDOM"]
    names = sorted({f["name"] for f in fires})
    strat, memb = {}, {}
    n_excl = 0

    def _annotate(t):
        ei = int(np.searchsorted(ts, pd.Timestamp(t["entry_ts"]).value,
                                 side="left"))
        xi = min(len(ts) - 1, ei + int(t["duration_min"]))
        d = t["dir"]
        a0 = env.atr_at(tf, ts[ei])
        if not a0:
            return None
        mae = max([0.0] + [(t["entry"] - l[j]) if d == 1
                           else (h[j] - t["entry"])
                           for j in range(ei, xi + 1)])
        return {"instrument": instr, "name": t.get("_name", "?"),
                "entry_ts": pd.Timestamp(t["entry_ts"]),
                "exit_ts": pd.Timestamp(t["entry_ts"])
                + pd.Timedelta(minutes=t["duration_min"]),
                "entry": t["entry"], "pts": t["pts"],
                "session": t["session"],
                "stop_pts": INITIAL_STOP_ATR * a0, "mae_pts": mae}

    for variant in variants:
        from backtest.recipes import specialize
        recipe = transform_recipe(specialize(rset[variant], instr), tf)
        for name in names:
            nf = [f for f in fires if f["name"] == name]
            tl = []
            for t in simulate(nf, env, recipe, spread):
                if in_lockbox_span(t["entry_ts"]):      # register 85
                    n_excl += 1
                    continue
                t["_name"] = name
                a = _annotate(t)
                if a:
                    tl.append(a)
            strat[(variant, name)] = tl
        for m, mf in enumerate(members):
            tl = []
            for t in simulate(mf, env, recipe, spread):
                if in_lockbox_span(t["entry_ts"]):      # register 85
                    n_excl += 1
                    continue
                t["_name"] = f"B-RANDOM#{m:02d}"
                a = _annotate(t)
                if a:
                    tl.append(a)
            memb[(variant, m)] = tl
    return strat, memb, n_excl


def attribution(rows):
    """Per-instrument footer: trades taken, net GBP contribution,
    refusals (register 86: scope questions read without re-runs)."""
    per = {}
    for r in rows:
        a = per.setdefault(r["instrument"],
                           {"taken": 0, "net_gbp": 0.0, "refused": 0})
        if r["gate"] == "TAKEN":
            a["taken"] += 1
            a["net_gbp"] = round(a["net_gbp"] + (r["pnl_gbp"] or 0.0), 2)
        else:
            a["refused"] += 1
    return dict(sorted(per.items()))


def _attr_str(per):
    return "; ".join(f"{i}: taken={a['taken']} net={a['net_gbp']:+.2f} "
                     f"refused={a['refused']}" for i, a in per.items())


CURVE_COLS = ["entry_ts", "exit_ts", "instrument", "sentence_id",
              "gate", "stake", "stop_pts", "risk_gbp",
              "risk_budget_gbp", "pnl_gbp", "exit_reason", "balance"]


def write_curve(path, rows, summary, per, hdr):
    with open(path, "w", newline="") as f:
        f.write(hdr + "\n")
        w = csv.DictWriter(f, fieldnames=CURVE_COLS)
        w.writeheader()
        w.writerows({k: r.get(k) for k in CURVE_COLS} for r in rows)
        f.write(f"# FOOTER end_balance={summary['end_balance']} "
                f"max_dd={summary['max_drawdown_gbp']} "
                f"({summary['max_drawdown_pct']}%) "
                f"ruin={summary['ruin'] or 'survived'} "
                f"taken={summary['taken']} "
                f"skipped_risk={summary['skipped_risk']} "
                f"skipped_margin={summary['skipped_margin']} "
                f"closeouts={summary['provider_closeouts']} | "
                + _attr_str(per) + "\n")


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--pot", type=float, required=True)
    ap.add_argument("--risk-pct", type=float, default=2.0)
    ap.add_argument("--stake", type=float, default=STAKE_DEFAULT)
    ap.add_argument("--exec-tf", default=EXEC_TF_DEFAULT,
                    choices=list(TF_ALIAS))
    ap.add_argument("--leverage", type=float, default=LEVERAGE_DEFAULT)
    ap.add_argument("--maintenance-pct", type=float,
                    default=MAINTENANCE_PCT)
    ap.add_argument("--min-stake", type=float, default=MIN_STAKE_DEFAULT)
    ap.add_argument("--spread-markup", type=float, default=0.0)
    ap.add_argument("--variants", nargs="+", default=list(VARIANTS))
    ap.add_argument("--from", dest="dfrom", default=None)
    ap.add_argument("--to", dest="dto", default=None)
    ap.add_argument("--instruments", default=",".join(
        CANONICAL_INSTRUMENTS),
        help="comma-list; scope abbreviated in filenames "
             "(all4 / ex-<mkt> / joined shorts)")
    a = ap.parse_args(argv)
    if a.dfrom:
        os.environ["VC_PERIOD_FROM"] = a.dfrom
    if a.dto:
        os.environ["VC_PERIOD_TO"] = a.dto
    tf = TF_ALIAS[a.exec_tf]
    if tf not in LADDER_AVAILABLE:
        print(f"!! exec-tf {a.exec_tf} not in the current ladder "
              f"({'/'.join(LADDER_AVAILABLE)}) — refused, flagged")
        return
    instruments = [i.strip() for i in a.instruments.split(",")
                   if i.strip()]
    scope = scope_slug(instruments)
    os.makedirs(CURVES_DIR, exist_ok=True)
    head = subprocess.run(["git", "rev-parse", "HEAD"], cwd=ROOT,
                          capture_output=True, text=True).stdout.strip()
    strat, memb = {}, {}
    n_excl = 0
    for instr in instruments:
        print(f"# account_mode: {instr} ...", file=sys.stderr)
        s_, m_, x_ = collect_trades(instr, tf, a.variants,
                                    a.spread_markup)
        n_excl += x_
        for k, v in s_.items():
            strat.setdefault(k, []).extend(v)
        for k, v in m_.items():
            memb.setdefault(k, []).extend(v)
    params = (f"pot={a.pot:g} risk={a.risk_pct:g}% "
              f"stake={a.stake:g}/pt exec-tf={a.exec_tf} "
              f"leverage={a.leverage:g}(FLAGGED) "
              f"maintenance={a.maintenance_pct:g}(FLAGGED) "
              f"spread-markup={a.spread_markup:g} "
              f"period={a.dfrom}..{a.dto}")
    hdr_common = (
        "— BANKROLL LENS, NEVER EVIDENCE (registers 83/86). "
        "EX-LOCKBOX (register 85): lockbox-span entries excluded "
        "before simulation. COLLISION RULE: strict fill-order "
        "first-come; a subsequent entry is refused (SKIPPED_RISK) if "
        "combined open risk would breach the gate. " + params
        + f" scope={scope}")

    def _run(tl):
        tl = sorted(tl, key=lambda t: (t["entry_ts"].value,
                                       t["instrument"]))
        tl2 = [dict(t, reason="close") for t in tl]
        for t in tl2:
            t["sentence_id"] = t["name"]
        rows, summary = account_pass(tl2, a.pot, a.risk_pct, a.stake,
                                     a.leverage, a.maintenance_pct,
                                     a.min_stake)
        return rows, summary, attribution(rows)

    board = []
    census = []
    for (variant, name), tl in sorted(strat.items()):
        rows, summary, per = _run(tl)
        write_curve(os.path.join(CURVES_DIR,
                                 f"{variant}_{name}__{scope}.csv"),
                    rows, summary, per,
                    f"# ACCOUNT CURVE {variant} x {name} " + hdr_common)
        board.append(dict(variant=variant, sentence=name,
                          is_baseline=False, summary=summary, per=per))
        acc = [t for t in tl if t["stop_pts"] * a.stake
               <= a.pot * a.risk_pct / 100.0]
        census.append({
            "variant": variant, "sentence": name, "n_total": len(tl),
            "n_accessible": len(acc),
            "pass_frac": (round(len(acc) / len(tl), 3) if tl
                          else None),
            "accessible_median_pts": (round(float(np.median(
                [t["pts"] for t in acc])), 2) if acc else None)})
    for (variant, m), tl in sorted(memb.items()):
        rows, summary, per = _run(tl)
        board.append(dict(variant=variant, sentence=f"B-RANDOM#{m:02d}",
                          is_baseline=True, summary=summary, per=per))
    board.sort(key=lambda b: (-b["summary"]["end_balance"],
                              b["variant"], b["sentence"]))
    n_strat = sum(1 for b in board if not b["is_baseline"])
    n_base = len(board) - n_strat
    with open(LEADERBOARD_CSV, "w", newline="") as f:
        f.write("# ACCOUNT-CURVE LEADERBOARD — BANKROLL LENS, NEVER "
                "EVIDENCE (registers 83/86): no signal, recipe, or "
                "label decision cites account curves.\n")
        f.write(f"# FIELD HONESTY: {n_strat} strategy curves (variant "
                f"x sentence) + {n_base} B-RANDOM member curves (the "
                "luck reference, is_baseline=True). LEADERBOARD-TOP IS "
                "BEST-OF-FIELD BY CONSTRUCTION — read every row "
                "against the B-RANDOM band, never alone. Member curve "
                "files are not emitted (rows only, stated).\n")
        f.write("# EX-LOCKBOX (register 85): "
                f"{n_excl} lockbox-span entries excluded across the "
                f"field before simulation. {params} scope={scope}. "
                "Sorted by end_balance desc. Readers: comment='#'.\n")
        w = csv.writer(f)
        w.writerow(["variant", "sentence", "scope", "is_baseline",
                    "end_balance", "max_drawdown_gbp",
                    "max_drawdown_pct", "ruin", "trades_taken",
                    "skipped_risk", "skipped_margin",
                    "provider_closeouts", "per_instrument"])
        for b in board:
            s2 = b["summary"]
            w.writerow([b["variant"], b["sentence"], scope,
                        b["is_baseline"], s2["end_balance"],
                        s2["max_drawdown_gbp"], s2["max_drawdown_pct"],
                        s2["ruin"] or "survived", s2["taken"],
                        s2["skipped_risk"], s2["skipped_margin"],
                        s2["provider_closeouts"],
                        _attr_str(b["per"])])
    bands = {}
    for b in board:
        if b["is_baseline"]:
            bands.setdefault(b["variant"], []).append(
                b["summary"]["end_balance"])
    bands = {v: {"median": round(float(np.median(e)), 2),
                 "min": round(float(min(e)), 2),
                 "max": round(float(max(e)), 2), "n": len(e)}
             for v, e in sorted(bands.items())}
    art = {"STAMP": ("ACCOUNT-MODE BANKROLL LENS — NEVER EVIDENCE "
                     "(registers 83/86): no signal, recipe, or label "
                     "decision cites account curves; points physics is "
                     "the evidence layer. Per-strategy isolated "
                     "accounts (register 86); curves born ex-lockbox "
                     "(register 85)."),
           "engine_commit": head, "parameters": params,
           "scope": scope, "instruments": instruments,
           "excluded_lockbox_span_entries": n_excl,
           "leaderboard": [
               {"variant": b["variant"], "sentence": b["sentence"],
                "is_baseline": b["is_baseline"], **b["summary"],
                "per_instrument": b["per"]} for b in board],
           "b_random_end_balance_bands": bands,
           "accessibility_census": census}
    with open(os.path.join(CURVES_DIR, "account_mode.json"), "w") as f:
        json.dump(art, f, indent=2, default=str)
    L = ["# Account Mode — the bankroll lens (GENERATED by "
         "backtest.account_mode)", "",
         "Terms: [docs/GLOSSARY.md](../../docs/GLOSSARY.md).", "",
         f"Engine `{head[:9]}` — **BANKROLL LENS, NEVER EVIDENCE "
         "(registers 83/86).** Per-strategy isolated accounts: each "
         "variant x sentence pair is its own pot hunting the scoped "
         "instrument set; the blended single stream is RETIRED "
         "(register 86; archived). Curves born EX-LOCKBOX (register "
         f"85): {n_excl} lockbox-span entries excluded. Collision "
         "rule: strict fill-order first-come; combined open risk "
         "gates. LEADERBOARD-TOP IS BEST-OF-FIELD BY CONSTRUCTION — "
         "read against the B-RANDOM bands below. Defaults FLAGGED "
         f"operator-unverified: leverage {a.leverage:g}:1, "
         f"maintenance {a.maintenance_pct:g}, min stake "
         f"{a.min_stake:g}.", "",
         f"**Parameters:** {params}; scope {scope} "
         f"({', '.join(instruments)}); field {n_strat} strategy + "
         f"{n_base} baseline curves.", "",
         "## Leaderboard head (top 20 of the field; full board in "
         "reports/account_curves/_LEADERBOARD.csv)", "",
         "| variant | sentence | end £ | maxDD £ (%) | ruin | taken | "
         "skip-risk | closeouts |", "|---|---|---|---|---|---|---|---|"]
    for b in board[:20]:
        s2 = b["summary"]
        mark = " (B-RANDOM)" if b["is_baseline"] else ""
        L.append(f"| {b['variant']} | {b['sentence']}{mark} "
                 f"| {s2['end_balance']} | {s2['max_drawdown_gbp']} "
                 f"({s2['max_drawdown_pct']}%) "
                 f"| {s2['ruin'] or 'survived'} | {s2['taken']} "
                 f"| {s2['skipped_risk']} "
                 f"| {s2['provider_closeouts']} |")
    L += ["", "## B-RANDOM end-balance bands per variant (the luck "
          "reference)", "",
          "| variant | members | median £ | min £ | max £ |",
          "|---|---|---|---|---|"]
    for v, e in bands.items():
        L.append(f"| {v} | {e['n']} | {e['median']} | {e['min']} "
                 f"| {e['max']} |")
    L += ["", "## Accessibility census (pass fraction + accessible "
          "medians; static single-trade gate, stated)", "",
          "| variant | sentence | n | accessible | pass % | acc "
          "median pts |", "|---|---|---|---|---|---|"]
    for r in census:
        pf = (f"{100 * r['pass_frac']:.0f}%"
              if r["pass_frac"] is not None else "—")
        L.append(f"| {r['variant']} | {r['sentence']} | {r['n_total']} "
                 f"| {r['n_accessible']} | {pf} "
                 f"| {r['accessible_median_pts']} |")
    L.append("")
    with open(os.path.join(CURVES_DIR, "account_mode.md"), "w") as f:
        f.write("\n".join(L))
    print(f"BANKROLL LENS -> {CURVES_DIR}/ ({n_strat} strategy + "
          f"{n_base} baseline curves, scope {scope}) + "
          f"{LEADERBOARD_CSV} + {CURVES_DIR}/account_mode.md")


if __name__ == "__main__":
    main()
