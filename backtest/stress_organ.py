"""Cross-asset stress organ (register 123; pre-registered
prereg_stress_organ, counted 2026-08-31; session order item 7 —
external block 1, translated). OBSERVATIONAL. CONDITIONING DIMENSION
ONLY: the state splits matrix and scalp cells; no signal, question,
recipe or SIZING machinery (the practitioner's de-risking response is
PARKED — we have no sizing layer, first recorded in register 125).

RE-REGISTRATION NOTE (register 40 park acknowledged): gold / eurusd /
us500 were examined-and-PARKED as EVIDENCE feeds for their volume
semantics (no rolling-future volume; synthetic spot-FX volume). This
organ reads PRICES ONLY — returns, realized vol, correlation — the
park's stated defect is untouched; volume columns are never read.

THE FIELDS, per UTC day (trailing store only, no lookahead):
- gold momentum sign  = sign(close_d - close_{d-5 trading days});
- dollar direction    = the OPPOSITE of the same 5-day sign on eurusd
  (the dollar proxy); MOM_SESSIONS = 5, one trading week —
  implementer-proposed, FLAGGED;
- realized-vol level  = mean over the three feeds of the day's 1h
  log-return std, each read as a PERCENTILE of that feed's own PRIOR
  days (expanding, >= WARMUP_DAYS history);
- cross correlation   = mean pairwise |corr| of the day's aligned 1h
  returns, as a percentile of its own prior days.

THE STATE (registered, small): alarms = {rvol percentile >=
STRESS_PCTILE, |corr| percentile >= STRESS_PCTILE, safe-haven co-fire
(gold momentum UP and dollar UP)}; stressed = >= 2 alarms, mixed = 1,
calm = 0; days without data = uncovered (excluded, never calm).
STRESS_PCTILE from the store's own percentiles — implementer-proposed,
FLAGGED. Origin recorded: the practitioner's stacking claim —
uncorrelated alarms co-firing marks a regime shift.

CONSUMERS: the conditioning matrix gains a 'stress' dimension (field
size restated there); THE SCALP SPLIT here: the scalp arms' journal
rows per leg x window x state (register-105 consistency statistics,
distinct paths per register 113) with a DAY-STATE PERMUTATION luck
budget (states shuffled across days, pinned seeds; the qualifying
statistic = best-minus-worst state median gap beyond the null p95).
MINT-ON-LIFT ONLY. Per-session field slices print in the JSON; the
DAY state is the authoritative conditioning unit (sessions are thin
for within-day correlation — stated). Twin-run pinned
(tests/test_stress_organ.py). Weekly under Part C before the matrix.
"""

import argparse
import csv
import functools
import json
import os
import subprocess
import sys

import numpy as np
import pandas as pd

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "scripts"))

from backtest.per_market_watch import (MIN_CELL_N, NULL_SEEDS,
                                       cell_stats)

OUT = os.path.join(ROOT, "reports", "scoreboard")
TRADES_CSV = os.path.join(ROOT, "reports", "trades.csv")

FEEDS = ("gold", "eurusd", "us500")   # the named non-traded feeds
MOM_SESSIONS = 5          # one trading week — implementer-proposed, FLAGGED
STRESS_PCTILE = 0.80      # alarm bar on the store's own percentile —
                          # implementer-proposed, FLAGGED
WARMUP_DAYS = 60          # minimum prior days before a percentile reads
STATES = ("calm", "mixed", "stressed")
SCALP_ARMS = ("R-SCALP-H" + str(6), "R-SCALP-H" + str(6) + "-REF")


def _feed_frame(slug):
    df = pd.read_csv(os.path.join(ROOT, "clean_finsa", f"{slug}_1h.csv"),
                     usecols=["time", "close"], parse_dates=["time"])
    df["date"] = df["time"].dt.strftime("%Y-%m-%d")
    df["lr"] = np.log(df["close"]).diff()
    return df


def _expanding_pctile(vals):
    """Percentile of each value vs STRICTLY PRIOR values (NaN until
    WARMUP_DAYS prior points exist). No lookahead."""
    out = np.full(len(vals), np.nan)
    for i in range(len(vals)):
        prior = vals[:i]
        prior = prior[~np.isnan(prior)]
        if len(prior) >= WARMUP_DAYS and not np.isnan(vals[i]):
            out[i] = float(np.mean(prior <= vals[i]))
    return out


@functools.lru_cache(maxsize=1)
def fields_by_day():
    """Per-UTC-day stress fields across the three feeds. Cached —
    deterministic given the store."""
    frames = {s: _feed_frame(s) for s in FEEDS}
    daily_close = {s: f.groupby("date")["close"].last() for s, f in
                   frames.items()}
    days = sorted(set.intersection(*(set(dc.index)
                                     for dc in daily_close.values())))
    # momentum signs (5 trading days back on the shared day axis)
    mom = {}
    for s in ("gold", "eurusd"):
        c = daily_close[s].reindex(days).to_numpy()
        m = np.full(len(days), np.nan)
        m[MOM_SESSIONS:] = np.sign(c[MOM_SESSIONS:] - c[:-MOM_SESSIONS])
        mom[s] = m
    # per-day realized vol per feed
    rv = {s: frames[s].groupby("date")["lr"].std().reindex(days)
          .to_numpy() for s in FEEDS}
    rv_pct = {s: _expanding_pctile(rv[s]) for s in FEEDS}
    rvol_level = np.nanmean(np.vstack([rv_pct[s] for s in FEEDS]),
                            axis=0)
    # per-day mean pairwise |corr| of aligned 1h returns
    corr = np.full(len(days), np.nan)
    grouped = {s: dict(tuple(frames[s].groupby("date")))
               for s in FEEDS}
    for i, d in enumerate(days):
        rets = []
        for s in FEEDS:
            g = grouped[s].get(d)
            if g is None or len(g) < 4:
                rets = []
                break
            rets.append(g.set_index("time")["lr"])
        if not rets:
            continue
        j = pd.concat(rets, axis=1, join="inner").dropna()
        if len(j) < 4:
            continue
        cm = j.corr().to_numpy()
        corr[i] = float(np.mean(np.abs(
            cm[np.triu_indices_from(cm, k=1)])))
    corr_pct = _expanding_pctile(corr)
    out = {}
    for i, d in enumerate(days):
        if np.isnan(rvol_level[i]) or np.isnan(corr_pct[i]) \
                or np.isnan(mom["gold"][i]) or np.isnan(mom["eurusd"][i]):
            continue
        alarms = int(rvol_level[i] >= STRESS_PCTILE) \
            + int(corr_pct[i] >= STRESS_PCTILE) \
            + int(mom["gold"][i] > 0 and mom["eurusd"][i] < 0)
        out[d] = {"state": ("stressed" if alarms >= 2 else
                            "mixed" if alarms == 1 else "calm"),
                  "alarms": alarms,
                  "gold_mom": int(mom["gold"][i]),
                  "dollar_up": bool(mom["eurusd"][i] < 0),
                  "rvol_pctile": round(float(rvol_level[i]), 3),
                  "corr_pctile": round(float(corr_pct[i]), 3)}
    return out


def day_state():
    """UTC-date string -> calm/mixed/stressed (uncovered days absent).
    The matrix's dimension provider (import point)."""
    return {d: v["state"] for d, v in fields_by_day().items()}


def scalp_split(rows, states):
    """The scalp arms' journal rows per leg x window x arm x state:
    register-105 consistency statistics (distinct paths) + a day-state
    permutation luck budget (states shuffled across days, pinned
    seeds; qualifying statistic = best-minus-worst state median gap
    among states measurable at MIN_CELL_N distinct)."""
    cells = {}
    for r in rows:
        st = states.get(r["day"])
        if st is None:
            continue
        cells.setdefault((r["instrument"], r["variant"], r["window"]),
                         []).append({**r, "state": st})
    out = {}
    for key, rr in sorted(cells.items()):
        per_state = {}
        for s in STATES:
            sel = [x for x in rr if x["state"] == s]
            if sel:
                per_state[s] = cell_stats(sel)
        meas = {s: c for s, c in per_state.items()
                if c["n_distinct"] >= MIN_CELL_N}
        gap = best = None
        if len(meas) >= 2:
            meds = {s: c["median"] for s, c in meas.items()}
            best = max(meds, key=meds.get)
            gap = round(meds[best] - min(meds.values()), 2)
        # the null: permute the day->state map (states shuffled across
        # the covered days, counts preserved)
        days = sorted({x["day"] for x in rr})
        dstates = [states[d] for d in days]
        null = []
        for seed in NULL_SEEDS:
            rs = np.random.RandomState(seed)
            perm = rs.permutation(len(dstates))
            fake = {d: dstates[j] for d, j in zip(days, perm)}
            fs = {}
            for x in rr:
                fs.setdefault(fake[x["day"]], []).append(x)
            fmeas = {s: cell_stats(v) for s, v in fs.items()}
            fmeas = {s: c for s, c in fmeas.items()
                     if c["n_distinct"] >= MIN_CELL_N}
            if len(fmeas) >= 2:
                m = [c["median"] for c in fmeas.values()]
                null.append(max(m) - min(m))
            else:
                null.append(np.nan)
        null = np.array(null, dtype=float)
        valid = null[~np.isnan(null)]
        p95 = float(np.percentile(valid, 95)) if len(valid) else None
        out["|".join(key)] = {
            "states": per_state, "best_state": best, "gap": gap,
            "null_p95": None if p95 is None else round(p95, 2),
            "null_valid_seeds": int(len(valid)),
            "clears": bool(gap is not None and p95 is not None
                           and gap > p95)}
    return out


def journal_scalp_rows():
    out = []
    for r in csv.DictReader(l for l in open(TRADES_CSV)
                            if not l.startswith("#")):
        if r["variant"] not in SCALP_ARMS:
            continue
        t = pd.Timestamp(r["open_ts"])
        from engine.store_loader import (in_lockbox_span,
                                         lockbox_boundary, zones)
        if in_lockbox_span(r["open_ts"]):
            continue
        b, g = lockbox_boundary(), zones()["go_live"]
        w = "backtest" if t < b else "forward" if t >= g else None
        if w is None:
            continue
        out.append({"instrument": r["instrument"],
                    "variant": r["variant"], "window": w,
                    "pts": float(r["points"]),
                    "week": "%d-W%02d" % t.isocalendar()[:2],
                    "day": t.strftime("%Y-%m-%d"),
                    "path": f"{r['open_ts']}|{r['direction']}"
                            f"|{r['points']}"})
    return out


def _emit(art, head):
    f = art["fields_tail"]
    L = ["# Cross-Asset Stress Organ (GENERATED by backtest.stress_organ)",
         "", "Terms: [docs/GLOSSARY.md](../../docs/GLOSSARY.md).", "",
         f"Engine `{head[:9]}` — OBSERVATIONAL ORGAN (register 123; "
         "prereg_stress_organ). CONDITIONING DIMENSION ONLY — no "
         "sizing machinery (parked, register 125). PRICES ONLY from "
         "the register-40-parked feeds (the park concerned volume "
         "semantics — untouched, stated). State per UTC day: alarms = "
         f"{{rvol pctile >= {STRESS_PCTILE:g}, |corr| pctile >= "
         f"{STRESS_PCTILE:g}, safe-haven co-fire}} (both bars "
         "FLAGGED); stressed >= 2, mixed = 1, calm = 0; uncovered "
         "days excluded, never calm. Origin: the practitioner's "
         "stacking claim (uncorrelated alarms co-firing = regime "
         "shift), recorded. The matrix's stress dimension reads "
         "day_state(); the scalp split below wears a day-state "
         "permutation luck budget. MINT-ON-LIFT ONLY.", "",
         f"State days: {art['state_counts']} (of {art['days_covered']} "
         "covered).", "",
         "## Recent days (tail of the field table; full series in the "
         "JSON)", "",
         "| day | state | alarms | gold mom | dollar up | rvol pctile "
         "| corr pctile |", "|---|---|---|---|---|---|---|"]
    for d, v in f:
        L.append(f"| {d} | {v['state']} | {v['alarms']} "
                 f"| {v['gold_mom']:+d} | {'Y' if v['dollar_up'] else 'n'} "
                 f"| {v['rvol_pctile']} | {v['corr_pctile']} |")
    L += ["", "## Scalp cells by stress state (register-105 consistency "
          "statistics, distinct paths; gap = best-minus-worst state "
          "median among states measurable at n_distinct >= "
          f"{MIN_CELL_N}; luck = day-state permutation p95)", "",
          "| leg | arm | window | calm n(d)/med | mixed n(d)/med "
          "| stressed n(d)/med | gap (best) | null p95 | clears |",
          "|---|---|---|---|---|---|---|---|---|"]
    for key, c in art["scalp_split"].items():
        instr, arm, w = key.split("|")

        def _s(s):
            v = c["states"].get(s)
            if not v:
                return "—"
            return f"{v['n']}({v['n_distinct']})/{v['median']:+.2f}"
        gap = (f"{c['gap']:+.2f} ({c['best_state']})"
               if c["gap"] is not None else "—")
        L.append(f"| {instr} | {arm} | {w} | {_s('calm')} | {_s('mixed')} "
                 f"| {_s('stressed')} | {gap} "
                 f"| {c['null_p95'] if c['null_p95'] is not None else '—'} "
                 f"| {'YES' if c['clears'] else 'no'} |")
    L.append("")
    with open(os.path.join(OUT, "stress_state.md"), "w") as f_:
        f_.write("\n".join(L))


def main():
    ap = argparse.ArgumentParser()
    ap.parse_args()
    head = subprocess.run(["git", "rev-parse", "HEAD"], cwd=ROOT,
                          capture_output=True, text=True).stdout.strip()
    fields = fields_by_day()
    states = day_state()
    counts = {s: sum(1 for v in states.values() if v == s)
              for s in STATES}
    split = scalp_split(journal_scalp_rows(), states)
    art = {"STAMP": ("OBSERVATIONAL cross-asset stress organ — a "
                     "conditioning dimension, never sizing; prices "
                     "only; mint-on-lift; never validation"),
           "engine_commit": head,
           "feeds": list(FEEDS), "mom_sessions_FLAGGED": MOM_SESSIONS,
           "stress_pctile_FLAGGED": STRESS_PCTILE,
           "warmup_days": WARMUP_DAYS,
           "days_covered": len(states), "state_counts": counts,
           "fields": fields, "scalp_split": split,
           "fields_tail": sorted(fields.items())[-15:]}
    with open(os.path.join(OUT, "stress_state.json"), "w") as f:
        json.dump(art, f, indent=2, default=str)
    _emit(art, head)
    n_clear = sum(1 for c in split.values() if c["clears"])
    print(f"OBSERVATIONAL stress organ -> {OUT}/stress_state.md "
          f"({counts}; {n_clear} scalp cells clear the day-state null)")


if __name__ == "__main__":
    main()
