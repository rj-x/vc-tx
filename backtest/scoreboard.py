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

Per-instrument mode (register 40 fence as AMENDED 2026-08-19, operator):
the scoreboard runs per instrument — episodes, ATR, base rates, and
session slices computed from each instrument's OWN store; output as
per-instrument sections (uk100 canonical; ger40/nas100/us30 stamped
PROVISIONAL pending their validation evenings), same matrix+cards format.
NO POOLING across instruments — cross-instrument aggregation is a future
registration.
"""

import argparse
import json
import os
import re
import subprocess

import numpy as np
import pandas as pd

from engine.signal_watch import (AGNOSTIC_ROWS, CONDITIONED_ROWS,
                                 DERIVED_FIRES, DUAL_GRADED,
                                 EVENT_DERIVED_ROWS, FIRING_CONDITIONS,
                                 H9_CHAIN_DEPTH_MIN, SignalWatch)
from backtest.sessions import SESSIONS, session_of, sessions_of_index
from engine.store_loader import is_sealed, lockbox_boundary, zones
from backtest.forward_migration import _replay
from backtest.campaign import make_cfg
from backtest.horizons import STANDARD_HORIZONS as _STD_HORIZONS

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
        m = _re.fullmatch(r"S(\d+)-H(\d+)", key)
        if not m:
            raise ValueError(f"signal row {key!r}: IDs are S<k>-H<n>, "
                             f"nothing else (schema v2, register 49)")
        n = int(m.group(2))
        if n not in reg:
            raise ValueError(f"signal row {key!r}: H{n} is not in the "
                             f"canonical hypothesis register")
        if reg[n] != "signal-live":
            raise ValueError(f"signal row {key!r}: H{n} status is "
                             f"{reg[n]!r}, not signal-live")

QUALIFYING_ATR_MULT = 1.5      # registry: qualifying_move
MAJOR_ATR_MULT = 3.0           # registry: major_move
MOVE_WINDOW_MIN = 60           # registry: qualifying_move window clause

# ---- per-instrument roster (register 40 fence as amended 2026-08-19).
# The future leg carries each pair's scoreboard (the uk100->uk100fut
# convention: the leg with real futures volume).
CANONICAL_INSTR = "uk100fut"
PROVISIONAL_INSTRS = ("ger40fut", "nas100fut", "us30fut")
PAIR_OF = {"uk100fut": "uk100", "ger40fut": "ger40",
           "nas100fut": "nas100", "us30fut": "us30"}
_R40_VOL = ("real futures volume (register 40 first-sync sanity; canonical "
            "verdict at this instrument's validation evening)")
VOLUME_TYPE = {"uk100fut": "real futures volume (step-zero audit)",
               "ger40fut": _R40_VOL, "nas100fut": _R40_VOL,
               "us30fut": _R40_VOL}  # DATA.md rule 5: stated per report
PROVISIONAL_STAMP = (
    "PROVISIONAL — validation pending (register 40 fence as amended "
    "2026-08-19): replay-only study over the synced store; canonical "
    "status, live attachment, and Asia/pause-sensitive cell "
    "interpretation await this instrument's validation evening. "
    "EXPLORATORY first cross-instrument look — expectations deliberately "
    "unregistered; anything interesting becomes a pre-registered question "
    "before it becomes a claim. NO POOLING across instruments.")
PROVISIONAL_CAVEATS = [
    ("drift-adjustment segments and engine tod baselines run on the "
     "provider/London trading-day structure; native cash-hour "
     "segmentation is part of this instrument's validation evening"),
    ("sessions = the registered register-37 world-clock partition "
     "(native-tz, DST-proof) applied to this instrument's own bars; "
     "'london' is not the home session of the US pairs"),
    ("the forward window (>= go_live) is also a replay over the synced "
     "store — this instrument has NO live attachment yet"),
]
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


def h5_fires(events, bars15, cfg):
    """Event-derived row (ratified 2026-08-20, register 46): the drafted
    condition READ ON THE SIGNAL TF per its founding origin — 15M
    structural BUYING_CLIMAX with close - SMA(H5_MA_PERIOD)(15M closes)
    >= H5_EXTENSION_ATR x ATR(15M), fire short at that 15M close. A 1M
    variant, if ever, is a separate hypothesis."""
    from engine.signal_watch import H5_EXTENSION_ATR, H5_MA_PERIOD
    live = [b for b in bars15 if not b.is_stub]
    atr = _atr15(live, cfg.context.atr_period)
    closes, sma = {}, {}
    hist = []
    for b in live:
        hist.append(b.close)
        closes[b.ts] = b.close
        if len(hist) >= H5_MA_PERIOD:
            sma[b.ts] = sum(hist[-H5_MA_PERIOD:]) / H5_MA_PERIOD
    from engine.signal_watch import ROW_CLIMAX_EXTENSION as name
    out = []
    for e in events:
        if (e["type"] == "LABEL" and e.get("tf") == cfg.mtf.signal_tf
                and e.get("structural") == "BUYING_CLIMAX"):
            t = pd.Timestamp(e["ts"])
            c, m, a = closes.get(t), sma.get(t), atr.get(t)
            if None not in (c, m, a) and c - m >= H5_EXTENSION_ATR * a:
                out.append({"ts": t, "name": name, "dir": -1})
    return out


def event_derived_fires(events, cfg, bars):
    """All event-derived rows in one place (migration chains + the
    15M-read extension row); every reader consumes this."""
    return (h9_fires(events, cfg)
            + h5_fires(events, bars[cfg.mtf.signal_tf], cfg))


def h9_fires(events, cfg):
    """Event-derived row (pre-registered 2026-08-19, changeable only by
    re-registration): fire = a migration chain reaching depth >=
    H9_CHAIN_DEPTH_MIN, stamped at the completing event's close, in the
    chain's direction."""
    from backtest.migration import migration_events
    from engine.signal_watch import (ROW_MIGRATION_CHAIN,
                                     ROW_MIGRATION_RECRUITED)
    out = []
    for e in migration_events(events, cfg):
        if e["chain_rungs"] < H9_CHAIN_DEPTH_MIN:
            continue
        out.append({"ts": e["ts"], "name": ROW_MIGRATION_CHAIN,
                    "dir": e["dir"]})
        if e["recruited"]:
            out.append({"ts": e["ts"], "name": ROW_MIGRATION_RECRUITED,
                        "dir": e["dir"]})
    return out


def parse_questions():
    """H-number -> [(Qk-Hn, status-line)] from the canonical register
    (register 54: questions render beneath signals on each card)."""
    import re as _re
    out, cur = {}, None
    for line in open(REGISTER):
        m = _re.match(r"^## H(\d+)\s*$", line)
        if m:
            cur = int(m.group(1))
            continue
        m = _re.match(r"^  - \*\*(Q\d+-H\d+)\*\*", line)
        if m and cur is not None:
            out.setdefault(cur, []).append(m.group(1))
    return out


def validate_question_ids():
    """Register 54 namespace closure: question IDs are Q<k>-H<n>, bound to
    their enclosing hypothesis; anything else is refused."""
    import re as _re
    for n, qs in parse_questions().items():
        for q in qs:
            m = _re.fullmatch(r"Q(\d+)-H(\d+)", q)
            if not m or int(m.group(2)) != n:
                raise ValueError(f"question id {q!r} under H{n}: IDs are "
                                 f"Q<k>-H<n> bound to their hypothesis "
                                 f"(register 54)")


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


def _payoff(nf, ts, cl, win):
    """Register 38 payoff (directional rows only): per fire, SIGNED price
    excursion at +window end (mid-price, no spread, idealized), signed by
    predicted direction. Clustered fires double-count shared travel —
    median is the robust companion. JSON also carries the standard-horizon
    marks."""
    exc, marks = [], {k: [] for k in _STD_HORIZONS}
    for f in nf:
        i = np.searchsorted(ts, f["ts"].value, side="right") - 1
        j = np.searchsorted(ts, (f["ts"] + win).value, side="right") - 1
        if i < 0 or j <= i:
            continue
        exc.append(float((cl[j] - cl[i]) * f["dir"]))
        for k in _STD_HORIZONS:
            if i + k < len(cl):
                marks[k].append(float((cl[i + k] - cl[i]) * f["dir"]))
    if not exc:
        return None
    a = np.array(exc)
    return {"n": len(exc),
            "total_pts_right": round(float(a[a > 0].sum()), 1),
            "total_pts_wrong": round(float(a[a < 0].sum()), 1),
            "net_pts": round(float(a.sum()), 1),
            "median_per_fire": round(float(np.median(a)), 2),
            "horizon_marks_net": {k: round(float(np.sum(v)), 1)
                                  for k, v in marks.items() if v}}


def class_masks(series, cfg):
    """Bar-class masks for CONDITIONED_ROWS (register 47). Implementations
    keyed by the class names declared in the signal module."""
    from engine.signal_watch import H6_DAY_WINDOW, H6_SPREAD_PCTILE
    ts, _cl, _segs = series
    return {}          # populated by run(), which holds hi/lo


def _wide_bar_mask(hi, lo):
    from engine.signal_watch import H6_DAY_WINDOW, H6_SPREAD_PCTILE
    rng = pd.Series(hi - lo)
    thr = rng.rolling(H6_DAY_WINDOW, min_periods=100).quantile(
        H6_SPREAD_PCTILE).shift(1)
    return (rng >= thr).fillna(False).to_numpy()


CLASS_MASK_FNS = {"wide_bar_p90_trailing_day": _wide_bar_mask}


def build_init(episodes, series):
    """INITIATION arrays (register 53): init[d][i] = a qualifying episode
    of direction d BEGINS in (ts_i, ts_i + 60min] — the strict exam."""
    ts, _cl, _ = series
    win = 3_600_000_000_000
    out = {}
    for d in (1, -1):
        starts = np.array(sorted(e["start"].value for e in episodes
                                 if e["dir"] == d))
        arr = np.zeros(len(ts), bool)
        j = np.searchsorted(starts, ts, side="right")
        ok = j < len(starts)
        arr[ok] = starts[np.minimum(j[ok], len(starts) - 1)] <= ts[ok] + win
        out[d] = arr
    return out


def score(fires, qual, episodes, series, lo_ts, hi_ts, label,
          names=frozenset(), bar_mask=None, cls_masks=None, init=None):
    """One source window [lo_ts, hi_ts); sealed spans already excluded.
    DUAL-CONVENTION GRADING (register 53): every precision cell reports
    PARTICIPATION (the historic qual[] convention — fire lands before or
    inside a qualifying move; always printed with its capture companion,
    median forward-MFE points of participation hits) and INITIATION (an
    episode BEGINS after the fire — the strict exam). Baselines computed
    per convention."""
    ts, cl, hi_a, lo_a = series[0], series[1], None, None
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
        cls_mask = (cls_masks or {}).get(name)
        hits, misses = [], []
        init_hits = init_tot = 0
        for f in nf:
            i = np.searchsorted(ts, f["ts"].value, side="right") - 1
            if i < 0:
                continue
            if init is not None:
                init_tot += 1
                ih = (bool(init[1][i] or init[-1][i]) if agnostic
                      else bool(init[f["dir"]][i]))
                init_hits += int(ih)
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
        pay = None if agnostic else _payoff(nf, ts, cl, win)
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
        cond_chance = cond_chance_init = None
        if cls_mask is not None:
            wsel = (ts >= lo_ts.value) & (ts < hi_ts.value)
            if bar_mask is not None:
                wsel = wsel & bar_mask
            wsel = wsel & cls_mask
            if wsel.any():
                cond_chance = round(50 * float(np.mean(qual[1][wsel])
                                               + np.mean(qual[-1][wsel])), 1)
                if init is not None:
                    cond_chance_init = round(
                        50 * float(np.mean(init[1][wsel])
                                   + np.mean(init[-1][wsel])), 1)
        # participation capture companion (MANDATORY, never separable):
        # median forward-window MFE of participation-hit fires
        cap = None
        if hits:
            win_ns = 3_600_000_000_000
            vals = []
            for f in hits:
                i = np.searchsorted(ts, f["ts"].value, side="right") - 1
                j = np.searchsorted(ts, ts[i] + win_ns, side="right")
                if j > i + 1:
                    seg = cl[i + 1:j]
                    vals.append(float((seg.max() - cl[i]) if f["dir"] == 1
                                      else (cl[i] - seg.min())))
            if vals:
                cap = round(float(np.median(vals)), 1)
        rows[name] = {
            "source": label,
            "grading": "either-direction" if agnostic else "directional",
            "conditioned_chance_pct": cond_chance,
            "conditioned_chance_init_pct": cond_chance_init,
            "conditioned_class": (CONDITIONED_ROWS.get(name)
                                  if cls_mask is not None else None),
            "initiation": ({"hits": init_hits, "of": init_tot,
                            "pct": round(100 * init_hits / init_tot, 1)
                            if init_tot else None}
                           if init is not None else None),
            "participation_capture_median_pts": cap,
            "payoff": pay,        # None for either-direction (by construction)
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
    if bar_mask is not None:
        w = w & bar_mask
    either = (round(100 * float(np.mean(qual[1][w] | qual[-1][w])), 1)
              if w.any() else None)
    per_dir = (round(50 * float(np.mean(qual[1][w]) + np.mean(qual[-1][w])), 1)
               if w.any() else None)
    either_i = per_dir_i = None
    if init is not None and w.any():
        either_i = round(100 * float(np.mean(init[1][w] | init[-1][w])), 1)
        per_dir_i = round(50 * float(np.mean(init[1][w])
                                     + np.mean(init[-1][w])), 1)
    rows["_moves"] = {"source": label, "n_qualifying_episodes": len(E),
                      "n_major": sum(1 for e in E if e["major"]),
                      "bar_qualify_base_rate_pct": either,
                      "per_direction_base_rate_pct": per_dir,
                      "initiation_base_either_pct": either_i,
                      "initiation_base_per_direction_pct": per_dir_i,
                      "base_rate_note": ("directional precision reads "
                                         "against per_direction; "
                                         "either-direction rows against "
                                         "bar_qualify (this context's own "
                                         "rates)")}
    return rows


def run(instr="uk100fut", provisional=False):
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
    signal_fires = watch.fires + event_derived_fires(events, cfg, bars)
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
    live_1m = [x for x in b1m if not x.is_stub]
    _RES = {
        "STAMP": ("OBSERVATIONAL signal scoreboard - move-detection, not "
                  "trading; no fills exist here by construction; never "
                  "validation (docs/hypothesis_lifecycle.md stage 4)"),
        "engine_commit": head,
        "instrument": instr,
        "pair": PAIR_OF.get(instr, instr),
        "status": "provisional" if provisional else "canonical",
        "volume_type": VOLUME_TYPE.get(instr, "unknown"),
        "store_span_1min": [str(live_1m[0].ts), str(live_1m[-1].ts)]
                           if live_1m else None,
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
    if provisional:
        _RES = {"STAMP_PROVISIONAL": PROVISIONAL_STAMP,
                "provisional_caveats": PROVISIONAL_CAVEATS} | _RES
    all_names = frozenset(FIRING_CONDITIONS) | EVENT_DERIVED_ROWS \
        | frozenset(DERIVED_FIRES)
    init = build_init(episodes, series)
    bar_sessions = sessions_of_index(
        pd.DatetimeIndex(series[0], tz="UTC"))
    live_hi = np.array([x.high for x in b1m if not x.is_stub])
    live_lo = np.array([x.low for x in b1m if not x.is_stub])
    cmasks = {row: CLASS_MASK_FNS[cls](live_hi, live_lo)
              for row, cls in CONDITIONED_ROWS.items()
              if cls in CLASS_MASK_FNS}
    out = _RES
    fwd_lbl = "post_go_live_replay" if provisional else "forward_feed_replay"
    windows = {"backtest": (pd.Timestamp("1970-01-01", tz="UTC"), boundary,
                            "backtest_replay"),
               "forward": (gl, far, fwd_lbl)}
    for wname, (lo, hi, lbl) in windows.items():
        out["signals"][wname] = score(signal_fires, qual, episodes, series,
                                      lo, hi, lbl, names=all_names,
                                      cls_masks=cmasks, init=init)
        out["founding_recipes_at_confirmation"][wname] = score(
            recipe_fires, qual, episodes, series, lo, hi, lbl,
            names=frozenset({"H1", "H2", "H3", "H4", "H5"}), init=init)
        # session splits (register 37): reporting slices only — the
        # machinery stays 24/5; fires and episodes assigned by session_of
        out["signals_by_session"][wname] = {}
        for sess in SESSIONS:
            sf = [f for f in signal_fires if session_of(f["ts"]) == sess]
            se = [e for e in episodes if session_of(e["start"]) == sess]
            out["signals_by_session"][wname][sess] = score(
                sf, qual, se, series, lo, hi, f"{lbl}/{sess}",
                names=all_names, bar_mask=(bar_sessions == sess),
                cls_masks=cmasks, init=init)
    return out


SMALL_N_FIRES = 20      # registry: operator order 2026-08-19 (dimmed +
SMALL_N_EPISODES = 10   # excluded from any future label arithmetic)
MARKER_BAND_PP = 2.0    # registry: implementer-proposed, ratification pending


def parse_claims():
    """H-number -> the register entry's one-sentence claim."""
    import re as _re
    out, cur, buf = {}, None, None
    for line in open(REGISTER):
        m = _re.match(r"^## H(\d+)\s*$", line)
        if m:
            if cur and buf:
                out[cur] = " ".join(buf)
            cur, buf = int(m.group(1)), None
            continue
        if cur is None:
            continue
        if line.startswith("- **Claim:**"):
            buf = [line.replace("- **Claim:**", "").strip()]
            continue
        if buf is not None:
            if line.startswith("- **"):
                out[cur] = " ".join(buf)
                buf = None
            else:
                buf.append(line.strip())
    if cur and buf:
        out[cur] = " ".join(buf)
    return out


def _chance(mv, agnostic):
    return (mv["bar_qualify_base_rate_pct"] if agnostic
            else mv["per_direction_base_rate_pct"])


def _cell(blk, key):
    """One matrix/grid cell: lift vs the CONTEXT'S OWN chance — or, for
    class-conditioned rows (register 47), vs the CLASS'S OWN chance (the
    scoreboard refuses unconditioned lift as headline lift); marker,
    hits/fires, payoff; dimmed (°) when small-n."""
    r = blk.get(key)
    mv = blk["_moves"]
    if r is None or r.get("n_fires", 0) == 0:
        return "—"
    agnostic = r["grading"] == "either-direction"
    ch = _chance(mv, agnostic)
    ch_i = (mv.get("initiation_base_either_pct") if agnostic
            else mv.get("initiation_base_per_direction_pct"))
    cond = r.get("conditioned_chance_pct")
    cls_note = ""
    if cond is not None:
        cls_note = f" [cls {cond}%/{r.get('conditioned_chance_init_pct')}%i]"
        ch = cond
        if r.get("conditioned_chance_init_pct") is not None:
            ch_i = r["conditioned_chance_init_pct"]
    p = r["precision"]
    if ch is None or p["pct"] is None:
        return "—"
    lift = round(p["pct"] - ch, 1)          # participation lift
    ini = r.get("initiation")
    if ini and ini["pct"] is not None and ch_i is not None:
        lift_i = round(ini["pct"] - ch_i, 1)
        mark = ("▲" if lift_i >= MARKER_BAND_PP
                else "▼" if lift_i <= -MARKER_BAND_PP else "·")
        cap = r.get("participation_capture_median_pts")
        core = (f"{mark}i{lift_i:+.1f}pp ({ini['hits']}/{ini['of']}) · "
                f"p{lift:+.1f}pp cap{cap if cap is not None else '—'}")
    else:
        mark = ("▲" if lift >= MARKER_BAND_PP
                else "▼" if lift <= -MARKER_BAND_PP else "·")
        core = f"{mark}p{lift:+.1f}pp ({p['hits']}/{p['of']})"
    core += cls_note
    pay = r.get("payoff")
    if pay:
        core += f" net{pay['net_pts']:+.0f}/med{pay['median_per_fire']:+.1f}"
    small = (r["n_fires"] < SMALL_N_FIRES
             or mv["n_qualifying_episodes"] < SMALL_N_EPISODES)
    return f"(°{core})" if small else core


def _signals_of(blk, n):
    """Signal keys for hypothesis n present in a block, sorted by S-number
    (schema v2: grouped rendering, configuration count visible)."""
    out = []
    for key in blk:
        m = re.fullmatch(rf"S(\d+)-H{n}( \(either-dir\))?", key)
        if m:
            out.append((int(m.group(1)), key))
    return [k for _, k in sorted(out)]


def _row_keys(blk, reg):
    keys = []
    for n in sorted(reg):
        if reg[n] != "signal-live":
            continue
        for key in _signals_of(blk, n):
            keys.append((key, key))
    return keys


def _section_lines(res, reg, labels, claims):
    """Matrix + cards for ONE instrument (register 38 format, heading
    levels shifted down one so per-instrument sections are the top level;
    register 40 amendment 2026-08-19)."""
    CTX = [("backtest", "whole"), ("backtest", "london"),
           ("forward", "whole"), ("forward", "london")]

    def blk_of(w, c):
        return (res["signals"][w] if c == "whole"
                else res["signals_by_session"][w][c])

    provisional = res.get("status") == "provisional"
    span = res.get("store_span_1min") or ["?", "?"]
    L = [f"# {res.get('pair', '?')} ({res.get('instrument', '?')}) — "
         + ("PROVISIONAL" if provisional else "CANONICAL"),
         ""]
    if provisional:
        L += [f"> **{PROVISIONAL_STAMP}**", ">"]
        L += [f"> - {c}" for c in PROVISIONAL_CAVEATS]
        L.append("")
    L += [f"Store span (1M, close ts): {span[0]} → {span[1]}. "
          f"Volume type: {res.get('volume_type', 'unknown')}.",
          "",
          "## Summary Matrix (page 1)",
          "",
          f"Engine `{res['engine_commit'][:9]}` — {res['STAMP']}",
          "",
          "**Review labels are RECOMMENDATIONS — none actioned, review "
          "pending operator familiarity.** Cells: marker + precision LIFT "
          "vs that context's OWN chance rate, (hits/fires), payoff "
          "net/median points (directional rows; either-direction rows have "
          "no payoff by construction). ▲/▼ = beyond ±2pp of chance, · = "
          "within. (°…) = small-n (fires<20 or episodes<10): dimmed, "
          "excluded from any future label arithmetic. Read "
          "READING_GUIDE.md first; full detail in hypothesis_performance.json.",
          ""]
    hdr = ("| H | label | " + " | ".join(f"{w} {c}" for w, c in CTX) + " |")
    L += [hdr, "|---|---|" + "---|" * len(CTX)]
    # context header row: episodes + both base rates per context
    ctx_info = []
    for w, c in CTX:
        mv = blk_of(w, c)["_moves"]
        ctx_info.append(f"{mv['n_qualifying_episodes']} ep; chance "
                        f"{mv['per_direction_base_rate_pct']}%dir/"
                        f"{mv['bar_qualify_base_rate_pct']}%either")
    L.append("| *context* | | " + " | ".join(ctx_info) + " |")
    whole_bt = blk_of("backtest", "whole")
    for disp, key in _row_keys(whole_bt, reg):
        n = int(re.search(r"-H(\d+)", disp).group(1))
        cells = [_cell(blk_of(w, c), key) for w, c in CTX]
        L.append(f"| {disp} | {labels.get(n, '-')} | " + " | ".join(cells)
                 + " |")
    unions = []
    for w, c in CTX:
        u = blk_of(w, c)["_union"]
        unions.append(f"{u['pct']}% ({u['episodes_covered_by_any_row']}"
                      f"/{u['of']})")
    L.append("| **union coverage** | | " + " | ".join(unions) + " |")
    # side-by-side for the load-bearing patterns (register 53 item 3);
    # printed ONCE, in the first (canonical) instrument's section
    _is_first = (not _ALL_RESULTS
                 or res is next(iter(_ALL_RESULTS.values())))
    if _is_first:
      L += ["", "### Dual-convention side-by-side — load-bearing patterns",
            "", "| pattern | context | initiation | participation (cap) |",
            "|---|---|---|---|"]
      def _sbs(res_all, key, w, label_):
          for inst, r_ in res_all.items():
              blk = r_["signals"][w]
              r = blk.get(key)
              if not r or not r.get("n_fires"):
                  continue
              ini, p = r.get("initiation"), r["precision"]
              cap = r.get("participation_capture_median_pts")
              L.append(f"| {label_} | {inst}/{w} "
                       f"| {ini['pct'] if ini else '—'}% "
                       f"({ini['hits']}/{ini['of']}) "
                       f"| {p['pct']}% (cap {cap}) |")
      from engine.signal_watch import (AGNOSTIC_ROWS as _AGN,
                                       CONDITIONED_ROWS as _CND)
      _agn_key = next(iter(_AGN))
      _cnd_key = next(iter(_CND))
      _sbs(_ALL_RESULTS, "S0-H1", "forward", "Q1-H1 away cells (S0-H1)")
      for key in ("S0-H2", "S1-H2"):
          _sbs(_ALL_RESULTS, key, "forward", f"H2 forward ({key})")
      for w in ("backtest", "forward"):
          _sbs(_ALL_RESULTS, _agn_key, w, f"{_agn_key} (either-dir)")
          _sbs(_ALL_RESULTS, _cnd_key, w, f"{_cnd_key} (conditioned)")
      L.append("")
    pend = [f"H{n} {reg[n]}" for n in sorted(reg) if reg[n] != "signal-live"]
    L += ["", "Not graded: " + "; ".join(pend)
          + " — see register entries.", "",
          "## Hypothesis Cards (page 2)", ""]

    for n in sorted(reg):
        if reg[n] != "signal-live":
            L += [f"### H{n} — {reg[n]}",
                  f"*{claims.get(n, '')}*",
                  f"Latest review: {labels.get(n, '-')}. See the register "
                  f"entry for what is missing.", ""]
            continue
        sigs = _signals_of(whole_bt, n)
        n_configs = len({k.split("-")[0] for k in sigs
                         if "(either-dir)" not in k})
        base = (blk_of("backtest", "whole").get(sigs[0]) if sigs else None) \
            or {}
        grading = base.get("grading", "directional")
        both = any("(either-dir)" in k for k in sigs)
        L += [f"### H{n} — {n_configs} signal"
              + ("s" if n_configs != 1 else ""),
              f"*{claims.get(n, '')}*",
              f"Grading: {grading}"
              + (" + either-direction (dual)" if both else "")
              + f". Latest review: {labels.get(n, '-')} (recommendation).",
              ""]
        for q in (parse_questions().get(n) or []):
            L.append(f"- Question **{q}**: see the register entry "
                     f"(status there is authoritative).")
        variants = [(k, k) for k in sigs]
        for disp, key in variants:
            L += [f"**{disp}** — session × window grid "
                  f"(cells as in the matrix):", "",
                  "| session | backtest | forward |", "|---|---|---|"]
            for sess in ("whole",) + tuple(SESSIONS):
                row = [_cell(blk_of(w, sess), key)
                       for w in ("backtest", "forward")]
                L.append(f"| {sess} | {row[0]} | {row[1]} |")
            L.append("")
            for w in ("backtest", "forward"):
                r = blk_of(w, "whole").get(key)
                if not r or r.get("n_fires", 0) == 0:
                    continue
                pay = r.get("payoff")
                if pay:
                    L.append(f"- {w} payoff: right "
                             f"{pay['total_pts_right']:+.0f} / wrong "
                             f"{pay['total_pts_wrong']:+.0f} / net "
                             f"{pay['net_pts']:+.0f} pts; median per fire "
                             f"{pay['median_per_fire']:+.2f} (n={pay['n']})")
                elif r["grading"] == "either-direction":
                    L.append(f"- {w} payoff: n/a by construction "
                             f"(either-direction)")
                bc, wf = r.get("best_call"), r.get("worst_false_alarm")
                if bc:
                    L.append(f"- {w} best call: {bc['ts'][:16]} "
                             f"+{bc['pts_remaining_at_fire']}pts remaining"
                             f" (episode {bc['episode_total_pts']}pts"
                             f"{', major' if bc['major'] else ''})")
                if wf:
                    L.append(f"- {w} worst false alarm: {wf['ts'][:16]} "
                             f"{-wf['adverse_pts']:+.1f}pts adverse")
            e = (blk_of("backtest", "whole").get(key) or {}).get("earliness")
            if e and e.get("median_pts_remaining_at_fire") is not None:
                L.append(f"- earliness (backtest): median "
                         f"{e['median_pts_remaining_at_fire']} pts of move "
                         f"remaining at fire (n={e['n']})")
            L.append("")
    return L


_ALL_RESULTS = {}


def _emit_performance_md(results):
    global _ALL_RESULTS
    _ALL_RESULTS = results
    """Per-instrument sections (register 40 amendment, 2026-08-19), each
    the register-38 matrix+cards format computed ONLY from that
    instrument's own store. uk100 canonical, the rest PROVISIONAL. NO
    POOLING across instruments."""
    reg = register_status()
    labels = register_labels()
    claims = parse_claims()
    first = next(iter(results.values()))
    L = ["# Hypothesis Performance — Per-Instrument",
         "",
         f"Engine `{first['engine_commit'][:9]}` — register 40 fence as "
         "amended 2026-08-19 (operator): one section per instrument, each "
         "computed only from that instrument's own store and native "
         "calendar; uk100 canonical, ger40/nas100/us30 PROVISIONAL "
         "(validation pending). Numbers are NEVER pooled across "
         "instruments — cross-instrument aggregation is a future "
         "registration. This first cross-instrument read is EXPLORATORY: "
         "expectations deliberately unregistered; anything interesting "
         "becomes a pre-registered question before it becomes a claim.",
         ""]
    for res in results.values():
        L += ["---", ""] + _section_lines(res, reg, labels, claims) + [""]
    L += ["---", "", "Appendix: the per-session detail beyond London and "
          "every horizon-mark payoff live in hypothesis_performance.json "
          "(generated, same run)."]
    with open(os.path.join(OUT, "hypothesis_performance.md"), "w") as f:
        f.write("\n".join(L))
    _emit_reading_guide()


_GUIDE = """# Reading Guide — Hypothesis Performance

**Read this before the table. Labels are recommendations only — none
actioned; status changes need a dated operator decision.**

## The two views
Page 1 (matrix): every live hypothesis x four contexts (backtest/forward,
whole-window and London). One cell = how far precision sits above or below
THAT CONTEXT'S OWN chance rate. Page 2 (cards): one card per hypothesis —
claim, full session x window grid, payoff, dated exhibits. Everything else
(other sessions' exhibits, horizon-mark payoffs) is in
hypothesis_performance.json.

## How to read a cell
`▲+9.4pp (26/80) net+123/med+1.2` means: precision 9.4 percentage points
ABOVE this context's chance rate (▲ = beyond +2pp; ▼ = beyond -2pp; · =
within the band), on 26 hits of 80 fires; summed signed excursion across
all fires +123 points with a median fire worth +1.2. `(°...)` = small-n
(fires<20 or episodes<10): dimmed, excluded from any future label
arithmetic — read as anecdote.

## The base-rate logic
The tape moves: in a typical context ~40-50% of bars are followed by a
qualifying move (>=1.5x 15M ATR within 60 min, drift-adjusted) in SOME
direction — so directional rows are chance-compared at roughly half that,
either-direction rows at the full rate, and EVERY context (each session,
each window) displays its own rates because they differ by session. A row
at chance has measured nothing.

## Payoff (directional rows only)
Per fire: the signed price change 60 minutes later (the registered
move-definition window), signed by the predicted direction. Total right =
sum of positive fires, wrong = sum of negative, net = the difference;
median per fire is the robust companion because CLUSTERED FIRES
DOUBLE-COUNT SHARED PRICE TRAVEL — a burst of 20 fires into one move books
that move 20 times in the totals, once in the median. Mid-price, no
spread, idealized — points here are not tradeable points.
Either-direction rows: n/a by construction (no predicted direction to
sign by).

## Session character (register 37 partition; native-tz, DST-proof)
- **asia** (Tokyo open -> London open): thin tape; the Asia best-call
  cluster is an OPEN QUESTION (regime edge vs thin-tape artifact vs
  unverified feed regime; thin-tape probe pending).
- **london** (London open -> NY open): the instrument's home session.
- **overlap** (NY open -> London close): highest participation; macro
  releases land here.
- **ny_only** (London close -> NY close): FTSE tape without its home
  market.
- **dead** (NY close -> Tokyo open): includes the daily feed pause.
London+overlap as the label-bearing window is a REGISTERED PROPOSAL,
unratified — criteria compute on whole windows.

## Small-n caveats
Forward is days old; several cells are single-digit. The small-n dimming
is registered convention (operator, 2026-08-19), not styling. Nothing in
these pages is validation — walk-forward and the lockbox remain the only
verdict machinery.

## Per-instrument sections (register 40 fence as amended 2026-08-19)
One section per instrument, each computed ONLY from that instrument's own
store: its own episodes, ATR, base rates, and session slices. uk100 is
CANONICAL; ger40/nas100/us30 are PROVISIONAL (replay-only permission —
canonical status, live attachment, and Asia/pause-sensitive cell
interpretation await each instrument's validation evening) and this first
read is EXPLORATORY (expectations deliberately unregistered; anything
interesting becomes a pre-registered question before it becomes a claim).
Numbers are NEVER pooled across instruments — cross-instrument
aggregation is a future registration. Session labels are the registered
world-clock partition applied to each instrument's own bars: 'london' is
not the home session of the US pairs, and each section's chance rates are
its own. The session-character notes above are FTSE-specific; read other
instruments' session structure only after their validation evenings.
"""


def _emit_reading_guide():
    with open(os.path.join(OUT, "READING_GUIDE.md"), "w") as f:
        f.write(_GUIDE)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--instr", nargs="+",
                    default=[CANONICAL_INSTR, *PROVISIONAL_INSTRS],
                    help="instruments to run, canonical first (register 40 "
                         "amendment: per-instrument sections, no pooling)")
    a = ap.parse_args()
    os.makedirs(OUT, exist_ok=True)
    results = {}
    for instr in a.instr:
        provisional = instr != CANONICAL_INSTR
        print(f"\n#### {PAIR_OF.get(instr, instr)} ({instr}) — "
              + ("PROVISIONAL replay" if provisional else "canonical"))
        results[instr] = run(instr, provisional=provisional)
    path = os.path.join(OUT, "hypothesis_performance.json")
    doc = {"engine_commit": next(iter(results.values()))["engine_commit"],
           "REGISTER_40_AMENDMENT": (
               "per-instrument sections (operator, 2026-08-19): replay-only "
               "cross-instrument runs permitted; uk100 canonical; "
               "ger40/nas100/us30 PROVISIONAL pending validation evenings; "
               "NO POOLING across instruments"),
           "instruments": results}
    with open(path, "w") as f:
        json.dump(doc, f, indent=2, default=str)
    _emit_performance_md(results)
    for instr, res in results.items():
      print(f"\n==== {res['pair']} ({instr}) — {res['status'].upper()} ====")
      for block in ("signals", "founding_recipes_at_confirmation"):
        for src in ("backtest", "forward"):
            print(f"\n== {block} / {src} ==")
            for name, r in res[block][src].items():
                if name == "_moves":
                    print(f"  qualifying episodes: "
                          f"{r['n_qualifying_episodes']} "
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
