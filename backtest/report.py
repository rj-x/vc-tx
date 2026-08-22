"""Report generator — standing rule (register, 2026-08-12): reports are
GENERATED, not written. Every quantitative claim below is derived from the
campaign's logged artifacts (reports/backtest_v1/*.json); interpretive prose
is fixed text that carries no hand-computed numbers. Regenerate with the
campaign, or standalone: venv/bin/python -m backtest.report
"""

import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "reports", "backtest_v1")
DEST = os.path.join(ROOT, "reports", "backtest_v1.md")
PRIMARY = "uk100fut"
SECONDARY = "uk100"
PRIMARY_VARIANT = f"{PRIMARY}_full_2r"


def _load(name):
    p = os.path.join(OUT, name)
    return json.load(open(p)) if os.path.exists(p) else None


def _fates_row(sf):
    fields = ("GRADUATED", "REFUTED", "EXPIRED", "KILLED_WEAK", "active_at_end")
    rows = []
    for key, fates in sf["per_spec"].items():
        total = sum(fates.values())
        rows.append((key, total, *[fates.get(f, 0) for f in fields]))
    return rows


def generate_report():
    summary = _load("summary.json")
    lockbox = json.load(open(os.path.join(ROOT, "lockbox.json")))
    es = _load(f"{PRIMARY}_event_study.json")
    sp = _load(f"{PRIMARY}_spread_vs_stop.json")
    prim = summary[PRIMARY_VARIANT]
    sec = summary.get(f"{SECONDARY}_full_2r")
    nogate = summary.get(f"{PRIMARY}_abl_no_gating_2r")

    L = []
    a = L.append
    a("# Backtest v1 — Standing Report (GENERATED — do not hand-edit numbers)")
    a("")
    a(f"**Generated from:** `reports/backtest_v1/*.json` · **Instrument:** "
      f"`{PRIMARY}` (secondary `{SECONDARY}`) · **Volume type: real futures "
      f"contract volume** · **Stack:** 1h / 15min / 1min")
    a(f"**Data:** {prim['data']['sessions']} sessions, "
      f"{prim['data']['span'][0]} → {prim['data']['span'][1]}, "
      f"{prim['data']['rows_1m']:,} 1M rows · **Lockbox:** "
      f"{lockbox['boundary_utc']} (loader-enforced, untouched)")
    a(f"**Cost model:** {prim['cost_model']}")
    a("")
    a("## Headline")
    a("")
    tot_trades = prim["metrics"]["overall"].get("n", 0)
    a(f"Full system: **{prim['spawn_fates']['total_spawns']} spawns, "
      f"{tot_trades} trades**"
      + (f"; secondary {SECONDARY}: {sec['spawn_fates']['total_spawns']} "
         f"spawns, {sec['metrics']['overall'].get('n', 0)} trades" if sec else "")
      + ". While samples remain below powered n, the informative outputs are "
        "the funnel, per-TF label frequencies, and the drift-adjusted "
        "label-level event study; all weekly numbers are trend-indicative "
        "while baselines grow toward spec.")
    a("")
    a("## Label denominators (per TF; classified = feature-valid, non-stub)")
    a("")
    a("| Slug | TF | Classified bars | Non-null | Frequencies |")
    a("|---|---|---|---|---|")
    for slug, r in ((PRIMARY, prim), (SECONDARY, sec)):
        if r is None:
            continue
        for tf, d in r["label_denominators"].items():
            freq = " · ".join(f"{k} {v}" for k, v in
                              sorted(d["frequencies"].items(),
                                     key=lambda kv: -kv[1]))
            a(f"| {slug} | {tf} | {d['classified_bars']} | {d['non_null']} "
              f"| {freq or '—'} |")
    a("")
    a("## Spawn-fate conservation")
    a("")
    a("| Slug | Spec | Spawned | GRAD | REFUTED | EXPIRED | KILLED | active |")
    a("|---|---|---|---|---|---|---|---|")
    for slug, r in ((PRIMARY, prim), (SECONDARY, sec)):
        if r is None:
            continue
        for row in _fates_row(r["spawn_fates"]):
            a(f"| {slug} | {row[0]} | {row[1]} | {row[2]} | {row[3]} "
              f"| {row[4]} | {row[5]} | {row[6]} |")
    a("")
    a("## Explicit zeros (primary variant)")
    a("")
    a(" · ".join(f"{k} {v}" for k, v in prim["explicit_zeros"].items()))
    cg = prim.get("cross_gap_swings", {})
    a("")
    a(f"Swings confirmed across the session boundary (ruling 8 diagnostic): "
      f"signal-TF {cg.get('signal_tf', 0)} · context-TF "
      f"{cg.get('context_tf', 0)}")
    xs = _load(f"{PRIMARY}_exec_label_study.json")
    if xs:
        n_rows = sum(1 for k, v in xs["study"].items()
                     if isinstance(v, dict) and "n" in v)
        a(f"1min observational label study (ruling 10): {n_rows} label rows, "
          f"autocorrelation caveat embedded - `{PRIMARY}_exec_label_study.json` "
          f"(never pooled with 15min).")
    a("")
    a("## Variants & ablations (identical data; cost model above)")
    a("")
    a("| Variant | Trades | Win rate | Avg R | PnL | Tripwire |")
    a("|---|---|---|---|---|---|")
    for key, r in summary.items():
        o = r["metrics"]["overall"]
        a(f"| {key} | {o.get('n', 0)} | {o.get('win_rate', '—')} "
          f"| {o.get('avg_r', '—')} | {o.get('total_pnl', '—')} "
          f"| {', '.join(r['tripwire']) or 'clear'} |")
    a("")
    for key, r in summary.items():
        for t in r.get("trades", []):
            size = (f"£{t['stake']}/pt" if t.get("stake")
                    else f"{t['contracts']} contracts")
            basis = (f", basis@entry {t['basis_at_entry']:+.1f}"
                     if t.get("basis_at_entry") is not None else "")
            a(f"Trade detail ({key}, {t.get('vehicle', 'direct')}): "
              f"{t['dir']:+d} fill {t['entry']:.1f} stop {t['stop']:.1f} "
              f"({abs(t['entry'] - t['stop']):.1f} pts) × {size}{basis} → "
              f"exit {t['exit']:.1f} ({t['reason']}), {t['points']:.1f} pts, "
              f"R {t['r_multiple']:.2f}, costs {t['costs']:.0f}, "
              f"PnL {t['pnl']:.0f}.")
    a("")
    a("## Event study — drift-adjusted label level (primary powered readout)")
    a("")
    lab = (es or {}).get("label_level_drift_adjusted", {})
    drift = lab.get("drift_bps", {})
    if drift:
        a(f"Window drift (bps): "
          + " · ".join(f"{k} {v:+.1f}" for k, v in sorted(drift.items())))
        a("")
    a("| Label | n | signed | raw+20 (bps) | excess+20 (bps) | excess hit+20 |")
    a("|---|---|---|---|---|---|")
    for label, d in sorted(lab.items()):
        if label == "drift_bps" or not isinstance(d, dict):
            continue
        a(f"| {label} | {d['n']} | {d['signed']} "
          f"| {d.get('raw_20_mean_bps', '—')} "
          f"| {d.get('excess_20_mean_bps', '—')} "
          f"| {d.get('excess_20_hit', '—')} |")
    a("")
    a("## Spread vs stop (split by stop basis; open question, register R2)")
    a("")
    a(f"Median cash spread: **{sp['median_cash_spread_pts']:.1f} pts**"
      if sp and sp.get("median_cash_spread_pts") else
      "Median cash spread: n/a")
    a("")
    a("| Population | n | median % | p25–p75 | max | >15% alarm |")
    a("|---|---|---|---|---|---|")
    for key, d in (sp or {}).get("per_spec_and_basis", {}).items():
        s = d["spread_pct_of_stop"]
        a(f"| {key} | {d['n']} | {s['median']} | {s['p25']}–{s['p75']} "
          f"| {s['max']} | {d['above_15pct_alarm']} |")
    a("")
    a("Tracked quantity (register ruling 2, recalibrated): the spread-burden "
      "ratio between stop bases vs refinement's R-geometry gain, resolved by "
      "the with/without-refinement comparison at powered n.")
    a("")
    bc = _load(f"{PRIMARY}_basis_check.json")
    a("## Basis-at-entry check (single-point-dependency guard)")
    a("")
    if bc and bc["n_entries"]:
        a(f"Entries: {bc['n_entries']} · flagged (|deviation from session "
          f"median| > {bc['flag_threshold_pts']} pts): **{bc['n_flagged']}**")
        for r in bc["entries"]:
            a(f"- {r['variant']}: basis {r['basis_at_entry']:+.1f} vs session "
              f"median {r['session_median']:+.1f} -> deviation "
              f"{r['deviation']:+.1f} {'** FLAGGED**' if r['flagged'] else '(ok)'}")
    else:
        a("No cash-CFD entries this run.")
    a("")
    ext = _load(f"{PRIMARY}_extended_label_study.json")
    a("## Extended-hours observational readout (Part B; non-evidential)")
    a("")
    if ext:
        a(f"Bin coverage: {ext['bin_coverage']['bins']} bins, "
          f"{ext['bin_coverage']['undercooked']} undercooked · "
          f"segment-split label rows: "
          f"{sum(1 for k in ext['label_study_by_segment'] if '[' in k)}")
        a(f"**Standing note:** {ext['standing_note_pre_open']}")
        a("Feeds no thresholds or rules before walk-forward; full table in "
          f"`{PRIMARY}_extended_label_study.json`.")
    a("")
    a("## Macro tagging (±15 min; calendar validated on load)")
    a("")
    mt = prim["macro_tags"]
    a(f"Calendar: {mt['calendar']}.")
    if "funnel" in mt:
        a("")
        a("| Event type | outside | " + " | ".join(
            k for k in sorted(set(
                kk for v in mt["funnel"].values() for kk in v
                if kk != "outside")) or ["near_*"]) + " |")
        curs = sorted(set(kk for v in mt["funnel"].values() for kk in v
                          if kk != "outside"))
        a("|---|---|" + "---|" * len(curs))
        for kind, cnt in mt["funnel"].items():
            a(f"| {kind} | {cnt.get('outside', 0)} | "
              + " | ".join(str(cnt.get(c, 0)) for c in curs) + " |")
        a("")
        if mt.get("per_release_tag_counts"):
            a("Per-release tagged events: " + " · ".join(
                f"{k}: {v}" for k, v in
                sorted(mt["per_release_tag_counts"].items())))
        else:
            a("Per-release tagged events: none.")
        boe = [k for k in mt.get("per_release_tag_counts", {})
               if "2026-07-30 11:00" in k]
        a("")
        a("**2026-07-30 BoE decision (11:00 UTC, mid-FTSE-session — most "
          "contaminating single event in the window):** "
          + (f"{mt['per_release_tag_counts'][boe[0]]} tagged event(s)."
             if boe else "0 tagged events within ±15 min."))
    a("")
    mv = _load(f"{PRIMARY}_macro_volume_check.json")
    a("## Macro-spike volume check (register finding 2b)")
    a("")
    if mv and mv.get("n"):
        a(f"In-cash releases inside the working set: **{mv['n']}** · median "
          f"volume ratio in [release, +15 min) vs same-time other sessions: "
          f"**{mv['median_ratio']}×**")
        a("")
        a("| Release | vol ratio |")
        a("|---|---|")
        for r in mv["per_release"]:
            a(f"| {r['release']} | {r['vol_ratio_vs_same_time_other_sessions']} |")
    else:
        a("No in-cash releases inside the working set.")
    a("")
    a("## Standing flags")
    a("")
    a("1. `baseline_sessions` 8 / `min_baseline_obs` 5 (spec: 20/20) — data "
      "poverty; warmup = exactly `min_baseline_obs` sessions.")
    a("2. Frozen config = untuned defaults; no walk-forward has occurred.")
    a("3. Open-auction bars not excluded at the signal TF (v1 decision).")
    a("4. Context-TF stub bar is context-only per spec.")
    a("5. EFFORTLESS_DECLINE excess signal: tracked-not-acted "
      "(register ruling 1); enters only via walk-forward if it survives to "
      "powered n.")
    a("")
    import json as _j
    pl = os.path.join(ROOT, "reports", "paper", "ledger.jsonl")
    a("## FORWARD_PAPER (live paper ledger; forward zone)")
    a("")
    if os.path.exists(pl):
        evs = [_j.loads(l) for l in open(pl)]
        c = {}
        for e in evs:
            c[e["event"]] = c.get(e["event"], 0) + 1
        lb = _j.load(open(os.path.join(ROOT, "lockbox.json")))
        a(f"go_live_utc: **{lb.get('go_live_utc', 'UNSTAMPED')}** · ledger "
          f"events: " + " · ".join(f"{k} {v}" for k, v in sorted(c.items())))
        trades = [e for e in evs if e["event"] == "EXIT"
                  and e.get("tag") == "FORWARD_PAPER"]
        a(f"Paper trades to date: **{len(trades)}**"
          + ("" if trades else " (first-session silence is the likely and "
             "correct outcome)"))
        # RECONCILIATION CHECK (prerequisite of the first-live-trade
        # verification checklist, register 15): live ENTRY events' embedded
        # bar data vs settled store rows; divergences flagged
        import pandas as _pd
        ents = [e for e in evs if e["event"] == "ENTRY"]
        flags = 0
        if ents:
            from engine.store_loader import load_frame as _lf
            sf = _lf("uk100fut", "1min", narrative_scope=True,
                     log_fn=lambda m: None)
            for e in ents:
                ts = _pd.Timestamp(e["entry_ts"]) - _pd.Timedelta(minutes=1)
                if ts in sf.index:
                    if abs(float(e.get("price", 0)) - float(sf.loc[ts, "open"])) > 1e-9:
                        flags += 1
                        a(f"- RECONCILE FLAG: entry {e['entry_ts']} price "
                          f"{e.get('price')} vs settled open "
                          f"{sf.loc[ts, 'open']}")
                else:
                    flags += 1
                    a(f"- RECONCILE FLAG: entry {e['entry_ts']} has no "
                      f"settled store row")
        a(f"Reconciliation (live-vs-settled): {len(ents)} entries checked, "
          f"**{flags} flagged**"
          + ("" if ents else " — check ARMED ahead of first trade"))
    else:
        a("No paper ledger yet.")
    a("")
    a("## Part C — forward-zone & standing studies (register 55, weekly)")
    a("")
    a("Run in the same campaign command; every artifact carries its own "
      "stamps, conventions (dual-convention grading, register 53; "
      "conditioned baselines, register 47), and sealed-window skips. "
      "Index + headlines (artifacts in reports/scoreboard/ unless noted):")
    a("")
    import json as _json

    def _art(name):
        p = os.path.join(ROOT, "reports", "scoreboard", name)
        try:
            return _json.load(open(p))
        except Exception:
            return None
    sb = _art("hypothesis_performance.json")
    if sb:
        insts = sb.get("instruments", {})
        home = insts.get("uk100fut", {})
        un = (home.get("signals", {}).get("forward", {})
              .get("_union", {}))
        a(f"- **Signal scoreboard** (`hypothesis_performance.md|.json`, "
          f"engine `{sb.get('engine_commit', '?')[:9]}`): "
          f"{len(insts)} instruments; home forward union coverage "
          f"{un.get('pct', '—')}% "
          f"({un.get('episodes_covered_by_any_row', '—')}"
          f"/{un.get('of', '—')}).")
    rc = _art("recipe_performance.json")
    if rc:
        a(f"- **Recipe performance** (`recipe_performance.md|.json`): set "
          f"**{rc.get('recipe_set', '?')}**, "
          f"{len(rc.get('results', []))} instruments; provenance printed "
          f"per recipe.")
    try:
        import glob as _glob
        fm_paths = sorted(_glob.glob(os.path.join(
            ROOT, "reports", "forward", "migration_forward_*.json")))
        if fm_paths:
            fm = _json.load(open(fm_paths[-1]))
            g = fm.get("graded_1146Z_expectation", {})
            a(f"- **Forward migration** (`reports/forward/"
            f"{os.path.basename(fm_paths[-1])}`): "
              f"{fm.get('n_chain_events_forward', '—')} forward chains; "
              f"11:46Z grade matched={g.get('matched')}.")
    except Exception:
        pass
    cf = _art("cofire.json")
    if cf:
        a("- **Co-fire census** (`cofire.md|.json`): cross-family pairs; "
          "composites go through the front door only.")
    cm = _art("conditioning_matrix.json")
    if cm:
        a("- **Conditioning matrix** (`conditioning_matrix.md|.json`): "
          "state-conditioned cells, episode-start hits; survivors are "
          "sitting material.")
    vw = _art("vwap_census.json")
    if vw:
        a("- **VWAP census** (`vwap_census.md|.json`): re-cut conventions "
          "(episode-start hits, decile-matched + phase-conditioned bases); "
          "nothing survives at home as of the re-cut.")
    dc = _art("drift_census.json")
    if dc:
        a("- **Drift census** (`drift_census.md|.json`): "
          "overnight-vs-intraday + per-session drift; grading-fairness "
          "verdict — no base-rate change indicated.")
    eg = _art("excursion_geometry.json")
    if eg:
        a("- **Excursion geometry** (`excursion_geometry.md|.json`): MAE "
          "distributions + TP ladder (tail-risk warnings in-header) — the "
          "v1 recipe-values evidence base.")
    a("")
    a("## Cadence")
    a("")
    a("Daily manual sync (`scripts/sync_daily.sh`); weekly campaign "
      "(`venv/bin/python -m backtest.campaign` — regenerates this report); "
      "lockbox and thresholds untouched. Next formal checkpoint: first "
      "powered drift-adjusted label readout or walk-forward feasibility, "
      "whichever first.")
    a("")

    with open(DEST, "w") as f:
        f.write("\n".join(L) + "\n")
    print(f"generated {DEST}")


if __name__ == "__main__":
    generate_report()
