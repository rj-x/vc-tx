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

from engine.signal_watch import (AGNOSTIC_ROWS, DERIVED_FIRES, DUAL_GRADED,
                                 EVENT_DERIVED_ROWS, FIRING_CONDITIONS,
                                 H9_CHAIN_DEPTH_MIN, SignalWatch)
from backtest.sessions import SESSIONS, session_of
from engine.store_loader import is_sealed, lockbox_boundary, zones
from backtest.forward_migration import _replay
from backtest.campaign import make_cfg

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "reports", "scoreboard")
REGISTER = os.path.join(ROOT, "docs", "hypothesis_register.md")


def register_status():
    """H-number -> status from the canonical hypothesis register."""
    import re as _re
    out, cur = {}, None
    for line in open(REGISTER):
        m = _re.match(r"^## H(\d+)\s*$", line)
        if m:
            cur = int(m.group(1))
            continue
        m = _re.match(r"^- \*\*Status:\*\* \*\*([a-z-]+)\*\*", line)
        if m and cur is not None:
            out[cur] = m.group(1)
            cur = None
    return out


def validate_rows():
    """Register 35 item 4: the scoreboard refuses a row whose ID isn't in
    the canonical register (S-H<n>, status signal-live)."""
    import re as _re
    reg = register_status()
    for key in set(FIRING_CONDITIONS) | EVENT_DERIVED_ROWS | set(DERIVED_FIRES):
        m = _re.fullmatch(r"S-H(\d+)", key)
        if not m:
            raise ValueError(f"signal row {key!r}: IDs are S-H<n>, nothing "
                             f"else (docs/hypothesis_register.md)")
        n = int(m.group(1))
        if n not in reg:
            raise ValueError(f"signal row {key!r}: H{n} is not in the "
                             f"canonical hypothesis register")
        if reg[n] != "signal-live":
            raise ValueError(f"signal row {key!r}: H{n} status is "
                             f"{reg[n]!r}, not signal-live")

QUALIFYING_ATR_MULT = 1.5      # registry: qualifying_move
MAJOR_ATR_MULT = 3.0           # registry: major_move
MOVE_WINDOW_MIN = 60           # registry: qualifying_move window clause
# row declarations + event-row depth live in the signal module (the
# guard's one permitted home for hypothesis identifiers); imported read-only


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


def h9_fires(events, cfg):
    """Event-derived row (pre-registered 2026-08-19, changeable only by
    re-registration): fire = a migration chain reaching depth >=
    H9_CHAIN_DEPTH_MIN, stamped at the completing event's close, in the
    chain's direction."""
    from backtest.migration import migration_events
    name = next(iter(EVENT_DERIVED_ROWS))
    return [{"ts": e["ts"], "name": name, "dir": e["dir"]}
            for e in migration_events(events, cfg)
            if e["chain_rungs"] >= H9_CHAIN_DEPTH_MIN]


def register_labels():
    """H-number -> latest review label from the canonical register (the
    governance rule: reviews emit recommendations, never actions — label
    and status shown side by side, unactioned recommendations persist)."""
    import re as _re
    out, cur = {}, None
    for line in open(REGISTER):
        m = _re.match(r"^## H(\d+)\s*$", line)
        if m:
            cur = int(m.group(1))
            continue
        m = _re.match(r"^- \*\*Latest review:\*\* ([a-z-]+)", line)
        if m and cur is not None:
            out[cur] = m.group(1)
    return out


def fires_from_events(events):
    out = []
    for e in events:
        if e["type"] == "CONFIRM" and "h" in e:
            out.append({"ts": pd.Timestamp(e["ts"]), "name": e["h"]["spec"],
                        "dir": int(e["h"]["dir"])})
    return out


def score(fires, qual, episodes, series, lo_ts, hi_ts, label,
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
        agnostic = name in AGNOSTIC_ROWS or name.endswith("(either-dir)")
        hits, misses = [], []
        for f in nf:
            i = np.searchsorted(ts, f["ts"].value, side="right") - 1
            if i < 0:
                continue
            ok = bool(qual[1][i] or qual[-1][i]) if agnostic \
                else bool(qual[f["dir"]][i])
            adverse = 0.0
            j = np.searchsorted(ts, (f["ts"] + win).value, side="right")
            if j > i + 1:
                seg = cl[i + 1:j]
                adverse = float((cl[i] - seg.min()) if f["dir"] == 1
                                else (seg.max() - cl[i]))
            (hits if ok else misses).append(
                {**f, "close_at_fire": float(cl[i]), "adverse_pts": adverse})
        covered, remaining = [], []
        for e in E:
            pre = [f for f in nf if (agnostic or f["dir"] == e["dir"])
                   and e["start"] - win <= f["ts"] <= e["start"]]
            if not pre:
                continue
            first = min(pre, key=lambda f: f["ts"])
            i = np.searchsorted(ts, first["ts"].value, side="right") - 1
            rem = (e["peak"] - cl[i]) * e["dir"]
            covered.append((e, first, float(rem)))
            remaining.append(float(rem))
        best = max(covered, key=lambda c: c[2], default=None)
        worst = max(misses, key=lambda m: m["adverse_pts"], default=None)
        rows[name] = {
            "source": label,
            "grading": "either-direction" if agnostic else "directional",
            "n_fires": len(nf),
            "precision": {"hits": len(hits), "of": len(hits) + len(misses),
                          "pct": round(100 * len(hits) / (len(hits) + len(misses)), 1)
                          if (hits or misses) else None},
            "coverage": {"covered": len(covered), "of": len(E),
                         "pct": round(100 * len(covered) / len(E), 1) if E else None},
            "earliness": {
                "median_pts_remaining_at_fire": (round(float(np.median(remaining)), 1)
                                                 if remaining else None),
                "n": len(remaining)},
            "best_call": ({"ts": str(best[1]["ts"]), "dir": best[1]["dir"],
                           "episode_start": str(best[0]["start"]),
                           "pts_remaining_at_fire": round(best[2], 1),
                           "episode_total_pts": best[0]["total_pts"],
                           "major": best[0]["major"]} if best else None),
            "worst_false_alarm": ({"ts": str(worst["ts"]), "dir": worst["dir"],
                                   "adverse_pts": round(worst["adverse_pts"], 1)}
                                  if worst else None),
        }
    union_cov = 0
    for e in E:
        pre = [f for f in F if (f["name"].split(" ")[0] in AGNOSTIC_ROWS
                                or f["dir"] == e["dir"])
               and e["start"] - win <= f["ts"] <= e["start"]]
        if pre:
            union_cov += 1
    rows["_union"] = {"source": label,
                      "episodes_covered_by_any_row": union_cov,
                      "of": len(E),
                      "pct": round(100 * union_cov / len(E), 1) if E else None}
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
    validate_rows()
    cfg = make_cfg({"session_model.extended_hours": True,
                    "session_model.ladder": True})
    watch = SignalWatch()
    engine, bars, _ = _replay(cfg, instr, engine_hook=watch.attach)
    events = engine.narrative.events
    b1m = bars[cfg.mtf.execution_tf]
    qual, episodes, series, drift = build_moves(
        b1m, bars[cfg.mtf.signal_tf], cfg.context.atr_period)
    recipe_fires = fires_from_events(events)          # CONFIRM = recipe stage
    signal_fires = watch.fires + h9_fires(events, cfg)  # bare conditions
    # derived rows (register 37): ONE condition, two gradings — copied fires
    for derived, src_row in DERIVED_FIRES.items():
        signal_fires += [{**f, "name": derived}
                         for f in watch.fires if f["name"] == src_row]
    # dual grading (register 36): same fire timestamps, either-direction
    # mode — the movement-not-direction question graded explicitly
    signal_fires += [{**f, "name": f["name"] + " (either-dir)"}
                     for f in signal_fires if f["name"] in DUAL_GRADED]
    # sealed spans excluded before scoring (register 30 pattern)
    recipe_fires = [f for f in recipe_fires if not is_sealed(f["ts"])]
    signal_fires = [f for f in signal_fires if not is_sealed(f["ts"])]
    episodes = [e for e in episodes if not is_sealed(e["start"])]
    boundary = lockbox_boundary()
    gl = zones()["go_live"]
    far = pd.Timestamp("2100-01-01", tz="UTC")
    head = subprocess.run(["git", "rev-parse", "HEAD"], cwd=ROOT,
                          capture_output=True, text=True).stdout.strip()
    _RES = {
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
        "signals": {},
        "signals_by_session": {},
        "founding_recipes_at_confirmation": {
            "note": ("graded pattern+wrapper stacks (confirmation = recipe "
                     "stage under the pure-signals doctrine) - historically "
                     "interesting, kept distinct, NOT signal rows; frozen_v1 "
                     "in paper is the untouched baseline record")},
    } | {}
    all_names = frozenset(FIRING_CONDITIONS) | EVENT_DERIVED_ROWS \
        | frozenset(DERIVED_FIRES)
    out = _RES
    windows = {"backtest": (pd.Timestamp("1970-01-01", tz="UTC"), boundary,
                            "backtest_replay"),
               "forward": (gl, far, "forward_feed_replay")}
    for wname, (lo, hi, lbl) in windows.items():
        out["signals"][wname] = score(signal_fires, qual, episodes, series,
                                      lo, hi, lbl, names=all_names)
        out["founding_recipes_at_confirmation"][wname] = score(
            recipe_fires, qual, episodes, series, lo, hi, lbl,
            names=frozenset({"H1", "H2", "H3", "H4", "H5"}))
        # session splits (register 37): reporting slices only — the
        # machinery stays 24/5; fires and episodes assigned by session_of
        out["signals_by_session"][wname] = {}
        for sess in SESSIONS:
            sf = [f for f in signal_fires if session_of(f["ts"]) == sess]
            se = [e for e in episodes if session_of(e["start"]) == sess]
            out["signals_by_session"][wname][sess] = score(
                sf, qual, se, series, lo, hi, f"{lbl}/{sess}",
                names=all_names)
    return out


def _fmt_row(disp, st, lab, r):
    if st != "signal-live" or r is None:
        return f"| {disp} | {st} | {lab} | - | - | - | - | - | - | - |"
    if r.get("n_fires") == 0:
        return (f"| {disp} | signal-live | {lab} | "
                f"{r.get('grading', 'directional')} | 0 | - | - | - | - "
                f"| - |")
    p, c, e = r["precision"], r["coverage"], r["earliness"]
    bc, wf = r["best_call"], r["worst_false_alarm"]
    return (f"| {disp} | signal-live | {lab} | {r['grading']} "
            f"| {r['n_fires']} "
            f"| {p['pct']}% ({p['hits']}/{p['of']}) "
            f"| {c['pct']}% ({c['covered']}/{c['of']}) "
            f"| {e['median_pts_remaining_at_fire']} (n={e['n']}) "
            f"| {bc['ts'][:16] + ' +' + str(bc['pts_remaining_at_fire']) + 'pts' if bc else '-'} "
            f"| {wf['ts'][:16] + ' -' + str(wf['adverse_pts']) + 'pts' if wf else '-'} |")


_HDR = ("| H | status | review label | grading | fires | precision | "
        "coverage | median pts remaining | best call | worst false alarm |\n"
        "|---|---|---|---|---|---|---|---|---|---|")


def _block_rows(blk, reg, labels):
    rows = []
    for n in sorted(reg):
        st, lab = reg[n], labels.get(n, "-")
        rows.append(_fmt_row(f"H{n}", st, lab, blk.get(f"S-H{n}")))
        supp = blk.get(f"S-H{n} (either-dir)")
        if supp:
            rows.append(_fmt_row(f"H{n} (either-dir)", st, lab, supp))
    return rows


def _emit_performance_md(res):
    """Register 35/37 deliverable: every H-number x window x session x the
    standard metrics; gaps visible; labels shown as recommendations."""
    reg = register_status()
    labels = register_labels()
    L = ["# Hypothesis Performance Table (GENERATED by backtest.scoreboard)",
         "",
         f"Engine `{res['engine_commit'][:9]}` - {res['STAMP']}",
         "",
         "**Review labels are RECOMMENDATIONS — none actioned, review "
         "pending operator familiarity (register 37: no status decisions "
         "this cycle).** Read reports/scoreboard/READING_GUIDE.md first. "
         "The derived-fires pair (signal module DERIVED_FIRES) is ONE "
         "firing condition graded two ways — never double-count. Criteria "
         "on whole windows only (session scoping is a registered "
         "proposal, unratified).", ""]
    for wname in ("backtest", "forward"):
        mv = res["signals"][wname]["_moves"]
        un = res["signals"][wname]["_union"]
        L += [f"## {wname} — whole window: "
              f"{mv['n_qualifying_episodes']} episodes "
              f"({mv['n_major']} major), either-direction base rate "
              f"{mv['bar_qualify_base_rate_pct']}%",
              "", _HDR]
        L += _block_rows(res["signals"][wname], reg, labels)
        L += ["",
              f"**Union coverage:** {un['pct']}% "
              f"({un['episodes_covered_by_any_row']}/{un['of']}) of "
              f"episodes preceded by ANY signal-live fire.", ""]
        for sess, blk in res["signals_by_session"][wname].items():
            mv = blk["_moves"]
            un = blk["_union"]
            if mv["n_qualifying_episodes"] == 0 and not any(
                    (blk.get(f"S-H{n}") or {}).get("n_fires") for n in reg):
                L.append(f"### {wname} / {sess} — no episodes, no fires")
                L.append("")
                continue
            L += [f"### {wname} / {sess} — {mv['n_qualifying_episodes']} "
                  f"episodes ({mv['n_major']} major); union coverage "
                  f"{un['pct']}% ({un['episodes_covered_by_any_row']}"
                  f"/{un['of']})", "", _HDR]
            L += _block_rows(blk, reg, labels)
            L.append("")
    L += ["## founding recipes at confirmation (kept distinct — not "
          "signal rows)", ""]
    for wname in ("backtest", "forward"):
        blk = res["founding_recipes_at_confirmation"][wname]
        rows = [f"{k}: {v['n_fires']} fires"
                + (f", precision {v['precision']['pct']}%"
                   if v.get("precision") else "")
                for k, v in sorted(blk.items()) if not k.startswith("_")]
        L.append(f"- {wname}: " + "; ".join(rows))
    L.append("")
    with open(os.path.join(OUT, "hypothesis_performance.md"), "w") as f:
        f.write("\n".join(L))
    _emit_reading_guide()


_GUIDE = """# Reading Guide — Hypothesis Performance Table

**One page. Read before the table. Labels are recommendations only —
none actioned; status changes need a dated operator decision.**

## What each column means
- **fires** — times the bare firing condition triggered. A hypothesis is
  only its firing condition (pure-signals doctrine); no trade logic exists
  here.
- **precision** — of those fires, how many were followed within 60 minutes
  by a qualifying move (>= 1.5x the 15-minute ATR, drift-adjusted) in the
  predicted direction. *Either-direction* rows count a move either way.
- **coverage** — of all qualifying moves in the window, how many had this
  signal fire in the 60 minutes before the move began. Precision asks "when
  it speaks, is it right?"; coverage asks "how much does it see?".
- **median pts remaining** — at the earliest covering fire, how many points
  of the move were still ahead. The earliness metric. (A
  minutes-before-trend-flip column existed briefly and was retired — it
  measured time to the next unrelated flip, not earliness.)
- **best call / worst false alarm** — dated single exhibits: the covered
  move with most points remaining, and the miss with the worst adverse
  drift. Anecdotes by construction; never generalize from them.
- **union coverage** — episodes preceded by ANY live signal vs none: how
  much of the tape the whole board sees at all.

## The base-rate logic
Roughly 44-48% of bars are followed by a qualifying move in SOME direction
within the hour — the tape moves a lot. So: directional precision only
means something against ~half that (~22-24%); either-direction precision
only against the full base rate. A row AT its base rate has measured
nothing. The base rate is printed per window and the table's numbers mean
nothing without it.

## Session character (register 37 partition; boundaries in native
exchange timezones, DST-proof)
- **asia** (Tokyo open -> London open): thin tape; the Asia best-call
  cluster (03:40-04:04Z) is an OPEN QUESTION — regime edge vs thin-tape
  artifact vs unverified feed regime (thin-tape probe pending).
- **london** (London open -> NY open): the instrument's home session.
- **overlap** (NY open -> London close): highest participation; macro
  releases (12:30/13:30Z class) land here.
- **ny_only** (London close -> NY close): FTSE tape without its home
  market.
- **dead** (NY close -> Tokyo open): includes the daily feed pause;
  expect near-empty rows.
London+overlap as the label-bearing (tradeable) window is a REGISTERED
PROPOSAL, unratified — criteria compute on whole windows until the
operator ratifies session scoping.

## Small-n caveats
Forward is a few sessions old; single-digit fire counts dominate several
cells. n sits beside every number deliberately: a 50% precision on 4 fires
is two lucky bars, not a signal. Backtest n>=100 rows are the only ones
where the chance comparison has teeth yet. Nothing in this table is
validation — the walk-forward and the lockbox remain the only verdict
machinery.
"""


def _emit_reading_guide():
    with open(os.path.join(OUT, "READING_GUIDE.md"), "w") as f:
        f.write(_GUIDE)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--instr", default="uk100fut")
    a = ap.parse_args()
    os.makedirs(OUT, exist_ok=True)
    res = run(a.instr)
    path = os.path.join(OUT, "signal_scoreboard.json")
    with open(path, "w") as f:
        json.dump(res, f, indent=2, default=str)
    _emit_performance_md(res)
    for block in ("signals", "founding_recipes_at_confirmation"):
      for src in ("backtest", "forward"):
        print(f"\n== {block} / {src} ==")
        for name, r in res[block][src].items():
            if name == "_moves":
                print(f"  qualifying episodes: {r['n_qualifying_episodes']} "
                      f"(major {r['n_major']})")
                continue
            if name == "_union":
                print(f"  union coverage: {r['pct']}% "
                      f"({r['episodes_covered_by_any_row']}/{r['of']})")
                continue
            if r.get("n_fires") == 0:
                print(f"  {name}: fires 0")
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
