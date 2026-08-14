"""Standing backtest campaign (weekly cadence) — the backtest_v1.md report
template with the sign-off amendments:
  (1) per-TF label denominators (classified = feature-valid non-stub bars);
  (2) spawn-fate conservation accounting;
  (3) explicit zero-count categories;
  (4) cost columns + cost-model statement;
  (5) self-describing artifact names.
Plus: label-level event study (primary powered readout while trade samples
are thin), spread-vs-stop diagnostic, macro-release tagging (±15 min, from
data/macro_releases.csv when populated).

Working set only — lockbox enforced at the loader. Frozen config = untuned
defaults. Usage: venv/bin/python -m backtest.campaign
"""

import json
import os
from collections import Counter

import pandas as pd

from engine.config import load
from engine.resample import cash_sessions, resample_bars
from engine.store_loader import load_frame
from backtest.loop import run_backtest
from backtest.metrics import breakdowns, tripwire
from backtest.eventstudy import (event_study, label_event_study,
                                 summarize_event_study)

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "reports", "backtest_v1")
MACRO_CSV = os.path.join(ROOT, "data", "macro_releases.csv")

SLUG = "uk100fut"

from engine.strategy import load_definition as _loaddef
_FROZEN = _loaddef(os.path.join(ROOT, "definitions", "frozen_v1.yaml"))
BASE_OVERRIDES = dict(_FROZEN["config_overrides"])   # pure refactor; pinned

VARIANTS = {
    "full_1r": {"trade.exit_mode": "fixed_r", "trade.r_target": 1.0},
    "full_2r": {"trade.exit_mode": "fixed_r", "trade.r_target": 2.0},
    "full_3r": {"trade.exit_mode": "fixed_r", "trade.r_target": 3.0},
    "full_opposing": {"trade.exit_mode": "opposing"},
    "full_context_flip": {"trade.exit_mode": "context_flip"},
    "norefine_2r": {"trade.exit_mode": "fixed_r", "trade.r_target": 2.0,
                    "execution.enabled": False},
    "strict_2r": {"trade.exit_mode": "fixed_r", "trade.r_target": 2.0,
                  "gating.strict_mode": True},
    "zerocost_2r": {"trade.exit_mode": "fixed_r", "trade.r_target": 2.0,
                    "trade.commission_per_contract": 0.0,
                    "trade.slippage_ticks": 0},
    "abl_no_location_2r": {"trade.exit_mode": "fixed_r", "trade.r_target": 2.0,
                           "ablation.no_location": True},
    "abl_no_gating_2r": {"trade.exit_mode": "fixed_r", "trade.r_target": 2.0,
                         "ablation.no_gating": True},
    "abl_no_confirmation_2r": {"trade.exit_mode": "fixed_r",
                               "trade.r_target": 2.0,
                               "ablation.no_confirmation": True},
}

TERMINALS = ("GRADUATED", "REFUTED", "EXPIRED", "KILLED_WEAK")


def make_cfg(extra):
    cfg = load()
    for k, v in {**BASE_OVERRIDES, **extra}.items():
        cfg = cfg.override(k, v)
    return cfg


def spawn_fates(events):
    """(2) Conservation: every spawn's terminal state, per spec+dir."""
    spawns = {}
    for e in events:
        if e["type"] == "SPAWNED":
            h = e["h"]
            spawns[h["id"]] = {"key": f"{h['spec']} "
                               f"{'LONG' if h['dir'] == 1 else 'SHORT'}",
                               "fate": "active_at_end"}
    for e in events:
        if e["type"] in TERMINALS and e.get("h", {}).get("id") in spawns:
            spawns[e["h"]["id"]]["fate"] = e["type"]
    out = {}
    for s in spawns.values():
        out.setdefault(s["key"], Counter())[s["fate"]] += 1
    fates = {k: dict(v) for k, v in out.items()}
    total = sum(sum(v.values()) for v in out.values())
    assert total == len(spawns), "spawn-fate accounting must conserve"
    return {"per_spec": fates, "total_spawns": len(spawns)}


def label_denominators(events, sig_tf, ctx_tf):
    """(1) Per-TF: classified bars (denominator) and non-null labels."""
    out = {}
    for tf in (sig_tf, ctx_tf):
        evs = [e for e in events if e["type"] == "LABEL" and e.get("tf") == tf]
        nonnull = [e for e in evs if e.get("label")]
        out[tf] = {"classified_bars": len(evs), "non_null": len(nonnull),
                   "frequencies": dict(Counter(e["label"] for e in nonnull))}
    return out


def explicit_zeros(events, engine):
    """(3) Every zero-capable category, reported even when zero."""
    c = Counter(e["type"] for e in events)
    return {
        "EOD_EXIT_trades": sum(1 for t in engine.broker.trades
                               if t["reason"] == "EOD_EXIT"),
        "SKIPPED_SIZE": engine.broker.skipped_size,
        "CONFIRM_UNDERSTRENGTH": engine.manager.diagnostics["CONFIRM_UNDERSTRENGTH"],
        "BLOCKED_SPAWNS": engine.manager.diagnostics["BLOCKED_SPAWNS"],
        "REFINEMENT_CANCELLED_REFUTED": c.get("REFINEMENT_CANCELLED_REFUTED", 0),
        "REFINEMENT_CANCELLED_OPPOSED": c.get("REFINEMENT_CANCELLED_OPPOSED", 0),
        "REFINEMENT_ABANDONED_EMBARGO": c.get("REFINEMENT_ABANDONED_EMBARGO", 0),
        "ENTRY_ABANDONED_EMBARGO": c.get("ENTRY_ABANDONED_EMBARGO", 0),
        "SIGNAL_UNACTED_IN_POSITION": c.get("SIGNAL_UNACTED_IN_POSITION", 0),
        "SIGNAL_UNACTED_CONFLICT": c.get("SIGNAL_UNACTED_CONFLICT", 0),
    }


def cost_model(cfg, slug):
    """(4) The cost model, stated."""
    v = cfg.execution_vehicle
    if v.mode == "cash_cfd":
        return (f"CASH-CFD VEHICLE (pre-registered 2026-08-13): signals/"
                f"levels/stops/R on {slug}; fills on {v.quote_slug} measured "
                f"bid/ask (long entry@ask exit@bid, mirrored), basis-at-entry "
                f"level mapping, GBP-per-point sizing (min stake "
                f"{v.min_stake_per_point}), NO commission; EOD-flat asserted")
    t = cfg.trade
    tick = cfg.instruments[slug].tick_size
    return (f"commission {t.commission_per_contract}/contract/side + "
            f"slippage {t.slippage_ticks} tick ({t.slippage_ticks * tick} pts) "
            f"on EVERY fill (entries and exits); "
            f"point value {cfg.instruments[slug].point_value}")


def spread_vs_stop(df1, records):
    """Risk-register item 6, promoted open question (2026-08-12): measured
    spread as % of stop distance, SPLIT BY STOP BASIS so both populations
    accrue — 'signature' (every graduation, all variants; the stop is
    defined at graduation) and 'exec_local' (actual refined entries whose
    tighter-of stop came from the execution window)."""
    cash = df1[df1["in_cash"]]
    med_spread = (float(cash["spread"].median())
                  if "spread" in cash and cash["spread"].notna().any() else None)
    out = {"median_cash_spread_pts": med_spread, "per_spec_and_basis": {}}
    if med_spread is None:
        return out
    groups = {}
    for r in records:
        if r["stop_dist"] and r["stop_dist"] > 0:
            groups.setdefault(f"{r['key']} [{r['basis']}]", []).append(
                100 * med_spread / r["stop_dist"])
    for key, vals in groups.items():
        s = pd.Series(vals)
        out["per_spec_and_basis"][key] = {
            "n": len(s),
            "spread_pct_of_stop": {"median": round(float(s.median()), 1),
                                   "p25": round(float(s.quantile(.25)), 1),
                                   "p75": round(float(s.quantile(.75)), 1),
                                   "max": round(float(s.max()), 1)},
            "above_15pct_alarm": int((s > 15).sum()),
        }
    return out


def _key(h):
    return f"{h['spec']} {'LONG' if h['dir'] == 1 else 'SHORT'}"


def stop_records(events, variant):
    """Signature-basis records from every GRADUATED event; exec-local (and
    fallback signature) records from every actual ENTRY."""
    out = [{"variant": variant, "key": _key(e["h"]), "basis": "signature",
            "stop_dist": e.get("stop_dist_at_grad")}
           for e in events if e["type"] == "GRADUATED"]
    for e in events:
        if e["type"] == "ENTRY":
            fill = e.get("fill", e["price"])
            out.append({"variant": variant, "key": _key(e["h"]),
                        "basis": f"entered_{e.get('stop_basis', '?')}",
                        "stop_dist": abs(fill - e["stop"])})
    return out


def macro_tags(events, sig_tf, relevance=None):
    """News dimension of the funnel: SPAWNED and non-null Signal-TF LABEL
    events within ±15 min of a release vs outside, split by release
    currency. Loads the calendar through validation-on-load (engine.macro);
    a corrupt calendar hard-fails the campaign — deliberately loud."""
    from engine.macro import load_and_validate
    if not os.path.exists(MACRO_CSV):
        return {"calendar": "absent"}
    cal = load_and_validate(MACRO_CSV)          # raises on any violation
    if relevance is not None:                   # capture-all, consume-filtered
        cal = cal[cal["currency"].isin(list(relevance.currencies))
                  & cal["impact"].isin(list(relevance.impacts))]
    if cal.empty:
        return {"calendar": "empty (validated)"}
    rel = list(zip(cal["ts"], cal["currency"], cal["name"]))

    def near(ts):
        return [(c, n, str(t)) for t, c, n in rel
                if abs((ts - t).total_seconds()) <= 900]

    funnel = {"SPAWNED": Counter(), "LABEL": Counter()}
    per_release = Counter()
    detail = []
    for e in events:
        if e["ts"] is None:
            continue
        if e["type"] == "SPAWNED":
            kind = "SPAWNED"
        elif (e["type"] == "LABEL" and e.get("tf") == sig_tf
                and e.get("label")):
            kind = "LABEL"
        else:
            continue
        hits = near(pd.Timestamp(e["ts"]))
        if hits:
            for c, n, t in {(c, n, t) for c, n, t in hits}:
                funnel[kind][f"near_{c}"] += 1
                per_release[f"{t} {n}"] += 1
            detail.append({"type": kind, "ts": str(e["ts"]),
                           "near": hits,
                           "payload": e.get("label") or e.get("h", {}).get("spec")})
        else:
            funnel[kind]["outside"] += 1
    return {"calendar": f"{len(cal)} releases (validated)",
            "funnel": {k: dict(v) for k, v in funnel.items()},
            "per_release_tag_counts": dict(per_release),
            "tagged_detail": detail}


def macro_volume_check(df1, sessions_col="session_id", window_min=15,
                       relevance=None):
    """Risk-register finding 2(b): does volume spike at known release
    timestamps? For each in-cash release inside the working set, the
    [release, release+15min) 1M volume vs the same minutes-of-day averaged
    over all OTHER sessions. Real volume should spike hard."""
    from engine.macro import load_and_validate
    if not os.path.exists(MACRO_CSV):
        return {"calendar": "absent"}
    cal = load_and_validate(MACRO_CSV)
    if relevance is not None:
        cal = cal[cal["currency"].isin(list(relevance.currencies))
                  & cal["impact"].isin(list(relevance.impacts))]
    cash = df1[df1["in_cash"]].copy()
    if cal.empty or cash.empty:
        return {"n": 0}
    cash["mod"] = cash.index.hour * 60 + cash.index.minute
    cash["date"] = cash.index.date
    per_mod = cash.groupby(["date", "mod"])["volume"].sum().unstack()
    rows = []
    for t, cur, name in zip(cal["ts"], cal["currency"], cal["name"]):
        day = t.date()
        mods = [t.hour * 60 + t.minute + i for i in range(window_min)]
        if day not in per_mod.index:
            continue
        mods = [m for m in mods if m in per_mod.columns]
        if not mods:
            continue                        # release outside cash hours
        ev_vol = per_mod.loc[day, mods].sum()
        others = per_mod.drop(index=day)[mods]
        base = others.sum(axis=1).mean()
        if pd.isna(ev_vol) or pd.isna(base) or base <= 0:
            continue
        rows.append({"release": f"{t} {cur} {name}",
                     "vol_ratio_vs_same_time_other_sessions":
                     round(float(ev_vol / base), 2)})
    ratios = [r["vol_ratio_vs_same_time_other_sessions"] for r in rows]
    return {"n": len(rows),
            "median_ratio": round(float(pd.Series(ratios).median()), 2)
            if ratios else None,
            "per_release": rows}


def run_variant(name, overrides, slug=SLUG):
    cfg = make_cfg(overrides)
    engine, info = run_backtest(cfg, slug)
    ev = engine.narrative.events
    trades = engine.broker.trades
    res = {
        "variant": name, "slug": slug,
        "data": {"sessions": info["sessions"],
                 "span": [str(info["span"][0]), str(info["span"][1])],
                 "rows_1m": info["rows_1m"]},
        "cost_model": cost_model(cfg, slug),
        "metrics": breakdowns(trades, cfg.trade.starting_equity),
        "tripwire": tripwire(breakdowns(trades, cfg.trade.starting_equity)["overall"]),
        "label_denominators": label_denominators(ev, cfg.mtf.signal_tf,
                                                 cfg.mtf.context_tf),
        "spawn_fates": spawn_fates(ev),
        "explicit_zeros": explicit_zeros(ev, engine),
        "macro_tags": macro_tags(ev, cfg.mtf.signal_tf,
                                 cfg.instruments[slug].get("macro_relevance")),
        # full trade records: every quantitative report claim must be
        # derivable from logged artifacts (standing rule: reports are
        # generated, not written)
        "trades": [{k: (str(v) if isinstance(v, pd.Timestamp) else v)
                    for k, v in t.items()} for t in trades],
        "cross_gap_swings": {           # register ruling 8 diagnostic
            "signal_tf": getattr(engine.signal_pipe.ctx, "cross_gap_swings", 0),
            "context_tf": getattr(engine.context_pipe.ctx, "cross_gap_swings", 0),
        },
    }
    return res, engine, cfg


def annotate_trades(engine, n=10, window_min=90):
    out = []
    for tr in engine.broker.trades[:n]:
        lo = tr["entry_ts"] - pd.Timedelta(minutes=window_min)
        hi = tr["exit_ts"] + pd.Timedelta(minutes=30)
        evs = [e for e in engine.narrative.events
               if e["ts"] is not None and lo <= e["ts"] <= hi
               and not (e["type"] == "LABEL" and e.get("label") is None)]
        out.append({"trade": {k: str(v) for k, v in tr.items()},
                    "narrative": evs})
    return out


def main(slugs=(SLUG, "uk100")):
    os.makedirs(OUT, exist_ok=True)
    from backtest.ledger import (hypothesis_rows, signature_moment_rows,
                                 write_ledger)
    led_h, led_s = [], []
    summary = {}
    for slug in slugs:
        variants = (VARIANTS if slug == SLUG
                    else {k: VARIANTS[k] for k in ("full_2r", "abl_no_gating_2r")})
        grads = []                     # every graduation across ALL variants
        for name, over in variants.items():
            key = f"{slug}_{name}"
            res, engine, cfg = run_variant(name, over, slug)
            summary[key] = res
            grads.extend(stop_records(engine.narrative.events, name))
            led_h.extend(hypothesis_rows(engine.narrative.events,
                                         engine.broker.trades,
                                         cfg.mtf.signal_tf, key))
            if name == "full_2r":
                led_s.extend(signature_moment_rows(
                    engine.narrative.events, cfg.mtf.execution_tf, key))
            with open(os.path.join(OUT, f"{key}.json"), "w") as f:
                json.dump(res, f, indent=2, default=str)
            if name == "full_2r":
                df1 = load_frame(slug, "1min")
                from engine.resample import exec_bars as _ebars
                ex_study = label_event_study(engine.narrative.events,
                                             _ebars(cash_sessions(df1)),
                                             cfg.mtf.execution_tf)
                with open(os.path.join(OUT, f"{slug}_exec_label_study.json"),
                          "w") as f:
                    json.dump({"note": "1min OBSERVATIONAL label study "
                               "(register ruling 10) - drift-adjusted, "
                               "segment-split, NEVER pooled with 15min; no "
                               "threshold or rule may consume 1min labels "
                               "before walk-forward; checkpoint remains "
                               "Signal-TF",
                               "autocorrelation_caveat": "adjacent 1min "
                               "labels share forward windows - rows are NOT "
                               "independent observations; treat n as "
                               "overstated",
                               "study": ex_study}, f, indent=2, default=str)
                sig_bars = resample_bars(cash_sessions(df1), 15, "15min")
                evh, base = event_study(engine.narrative.events, sig_bars)
                les = label_event_study(engine.narrative.events, sig_bars,
                                        cfg.mtf.signal_tf)
                with open(os.path.join(OUT, f"{slug}_event_study.json"), "w") as f:
                    json.dump({"hypothesis_level":
                               summarize_event_study(evh, base),
                               "label_level_drift_adjusted": les},
                              f, indent=2, default=str)
                engine.narrative.write_jsonl(os.path.join(
                    OUT, f"{slug}_full-system_2R_narrative.jsonl"))
                ann = annotate_trades(engine)
                with open(os.path.join(OUT, f"{slug}_annotated_trades.json"), "w") as f:
                    json.dump(ann, f, indent=2, default=str)
            print(f"{key:32s} n={res['metrics']['overall'].get('n', 0):>3} "
                  f"spawns={res['spawn_fates']['total_spawns']:>2} "
                  f"tripwire={res['tripwire'] or 'clear'}")
        cfg0 = make_cfg({})
        spread_slug = (cfg0.execution_vehicle.quote_slug
                       if cfg0.execution_vehicle.mode == "cash_cfd" else slug)
        dfq = load_frame(spread_slug, "1min")
        with open(os.path.join(OUT, f"{slug}_spread_vs_stop.json"), "w") as f:
            json.dump({"spread_source": spread_slug,
                       **spread_vs_stop(dfq, grads)}, f, indent=2, default=str)
        # spread per session-time bin from real quotes (Part A)
        q = dfq[dfq["in_cash"]]
        if "spread" in q.columns:
            lon = q.index.tz_convert("Europe/London")
            b = ((lon.hour * 60 + lon.minute) // 30)
            g = q.groupby(b)["spread"]
            bins = {f"{int(k)//2:02d}:{(int(k)%2)*30:02d}London":
                    {"median": round(float(v.median()), 2),
                     "p75": round(float(v.quantile(.75)), 2)}
                    for k, v in g}
            with open(os.path.join(OUT, f"{spread_slug}_spread_by_bin.json"),
                      "w") as f:
                json.dump(bins, f, indent=2)
        if slug == SLUG and cfg0.execution_vehicle.mode == "cash_cfd":
            # Part A addition: basis_at_entry distribution + per-session-
            # median deviation flag (single-point-dependency guard)
            ff = load_frame(slug, "1min")
            j = pd.DataFrame({"fut": ff["close"], "cash": dfq["close"]}).dropna()
            j["ldate"] = j.index.tz_convert("Europe/London").date
            sess_med = (j["fut"] - j["cash"]).groupby(j["ldate"]).median()
            thr = cfg0.execution_vehicle.basis_deviation_flag_pts
            rows, flags = [], 0
            for key, r in summary.items():
                if not key.startswith(slug):
                    continue
                for t in r.get("trades", []):
                    if t.get("basis_at_entry") is None:
                        continue
                    d0 = pd.Timestamp(t["entry_ts"]).tz_convert(
                        "Europe/London").date()
                    med = float(sess_med.get(d0, float("nan")))
                    dev = (t["basis_at_entry"] - med
                           if med == med else None)
                    fl = dev is not None and abs(dev) > thr
                    flags += bool(fl)
                    rows.append({"variant": key, "entry_ts": t["entry_ts"],
                                 "basis_at_entry": t["basis_at_entry"],
                                 "session_median": med,
                                 "deviation": dev, "flagged": fl})
            with open(os.path.join(OUT, f"{slug}_basis_check.json"), "w") as f:
                json.dump({"flag_threshold_pts": thr, "n_entries": len(rows),
                           "n_flagged": flags, "entries": rows},
                          f, indent=2, default=str)
        if slug == SLUG:
            # Part B: observational extended-hours run (structurally
            # narrative-only outside cash; evidential path above untouched)
            cfge = make_cfg({"session_model.extended_hours": True,
                             "session_model.ladder": True})
            engx, infox = run_backtest(cfge, slug)
            from engine.resample import trading_sessions as _tsess
            dfx = load_frame(slug, "1min")
            bx = resample_bars(_tsess(dfx,
                 cfge.session_model.trading_day_anchor_london), 15, "15min")
            lesx = label_event_study(engx.narrative.events, bx,
                                     cfge.mtf.signal_tf)
            fe = engx.signal_pipe.fe
            bins_n = ({k: len(v.volumes) for k, v in fe._bins.items()}
                      if hasattr(fe, "_bins") else {})
            under = sum(1 for n in bins_n.values()
                        if n < cfge.features.min_baseline_obs)
            from backtest.expansion import expansion_study
            from engine.resample import exec_bars as _xbars
            spr = dfq[dfq["in_cash"]]["spread"].median() if "spread" in dfq else None
            xb = _xbars(_tsess(dfx, cfge.session_model.trading_day_anchor_london))
            with open(os.path.join(OUT, f"{slug}_expansion_study.json"), "w") as f:
                json.dump(expansion_study(engx.narrative.events, xb,
                                          cfge.mtf.execution_tf,
                                          round(float(spr), 2) if spr == spr else None),
                          f, indent=2, default=str)
            from backtest.migration import migration_events, migration_study, LADDER
            mev = migration_events(engx.narrative.events, cfge)
            bx15 = bx
            with open(os.path.join(OUT, f"{slug}_migration.json"), "w") as f:
                json.dump({"log": [{k: str(v) if isinstance(v, pd.Timestamp)
                                    else v for k, v in e.items()}
                                   for e in mev],
                           "study": migration_study(mev, bx15)},
                          f, indent=2, default=str)
            ladder_out = {"nesting_caveat": "higher-TF labels are "
                          "compositions of lower-TF bars, not independent "
                          "confirmations; NEVER pool across TFs"}
            xcash = _tsess(dfx, cfge.session_model.trading_day_anchor_london)
            from engine.resample import exec_bars as _eb2
            for tf in LADDER:
                m = {"1min": 1, "3min": 3, "5min": 5, "15min": 15,
                     "30min": 30, "1h": 60}[tf]
                btf = _eb2(xcash, tf) if m == 1 else resample_bars(xcash, m, tf)
                ladder_out[tf] = {
                    "study": label_event_study(engx.narrative.events, btf, tf),
                    "bins": {"n_bins": len(getattr(
                        engx.ladder_pipes.get(tf, engx.signal_pipe).fe,
                        "_bins", {}))}}
            with open(os.path.join(OUT, f"{slug}_ladder_label_studies.json"),
                      "w") as f:
                json.dump(ladder_out, f, indent=2, default=str)
            led_h.extend(hypothesis_rows(engx.narrative.events, [],
                                         cfge.mtf.signal_tf,
                                         f"{slug}_extended_observational"))
            led_s.extend(signature_moment_rows(engx.narrative.events,
                                               cfge.mtf.execution_tf,
                                               f"{slug}_extended_observational"))
            with open(os.path.join(OUT, f"{slug}_extended_label_study.json"),
                      "w") as f:
                json.dump({"note": "OBSERVATIONAL (Part B) - feeds no "
                           "thresholds or rules before walk-forward",
                           "standing_note_pre_open": "pre_open accrues only "
                           "~1h/day - small-n applies to every pre_open row "
                           "until stated otherwise",
                           "trades_possible": False,
                           "bin_coverage": {"bins": len(bins_n),
                                            "undercooked": under},
                           "label_study_by_segment": lesx},
                          f, indent=2, default=str)
        if slug == SLUG:
            with open(os.path.join(OUT, f"{slug}_macro_volume_check.json"),
                      "w") as f:
                json.dump(macro_volume_check(
                    df1, relevance=cfg0.instruments[slug].get("macro_relevance")),
                    f, indent=2, default=str)
    write_ledger(led_h, led_s,
                 os.path.join(ROOT, "reports", "opportunity_ledger.md"),
                 os.path.join(ROOT, "reports", "opportunity_ledger.csv"))
    with open(os.path.join(OUT, "summary.json"), "w") as f:
        json.dump(summary, f, indent=2, default=str)
    from backtest.report import generate_report
    generate_report()
    print(f"\nWrote {OUT}/ and reports/backtest_v1.md (generated)")
    return summary


if __name__ == "__main__":
    main()
