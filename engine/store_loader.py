"""Clock-gated store access + programmatic lockbox (prompt Part 8, RULES
scope: the ONLY path from the clean store into the engine).

Two layers:

1. `load_frame()` — reads clean_finsa/{slug}_{tf}.csv and enforces the
   frozen lockbox boundary (lockbox.json at project root). By default rows
   at/after the boundary DO NOT EXIST as far as any caller is concerned.
   `lockbox_evaluation=True` is the single, logged, explicit override for
   the one final evaluation.

2. `ClockGatedFeed` — the event loop's only view of market data. It is
   parameterized by the simulation clock and physically cannot return bars
   whose CLOSE lies beyond it: there is no method that accepts an arbitrary
   timestamp, and the clock only moves forward.
"""

import json
import os

import pandas as pd

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CLEAN_DIR = os.path.join(ROOT, "clean_finsa")
LOCKBOX_PATH = os.path.join(ROOT, "lockbox.json")

TF_MINUTES = {"1min": 1, "3min": 3, "5min": 5, "10min": 10, "15min": 15,
              "30min": 30, "1h": 60, "4h": 240, "1d": 1440}  # "ladder:<tf>" keys resolve via split


def lockbox_boundary(root=None):
    path = os.path.join(root, "lockbox.json") if root else LOCKBOX_PATH
    with open(path) as f:
        return pd.Timestamp(json.load(f)["boundary_utc"])


def zones(root=None):
    """Three-zone model (register item 14): working set (-> boundary,
    freely simulatable) | lockbox (boundary -> go-live: sealed, finite,
    exactly one walk-forward evaluation) | forward (go-live ->:
    paper-visible live only, NEVER tunable; walk-forward training may not
    consume it). go_live_utc is stamped by the paper executor's first
    start and is terminal for the lockbox."""
    path = os.path.join(root, "lockbox.json") if root else LOCKBOX_PATH
    j = json.load(open(path))
    return {"working_end": pd.Timestamp(j["boundary_utc"]),
            "go_live": (pd.Timestamp(j["go_live_utc"])
                        if j.get("go_live_utc") else None)}


def stamp_go_live(ts, root=None):
    """One-shot terminal boundary: first paper go-live. Never overwrites."""
    path = os.path.join(root, "lockbox.json") if root else LOCKBOX_PATH
    j = json.load(open(path))
    if j.get("go_live_utc"):
        return j["go_live_utc"]
    j["go_live_utc"] = str(pd.Timestamp(ts))
    j.setdefault("rules", []).append(
        "go_live_utc = paper executor first start; lockbox terminal "
        "boundary; forward period (go-live ->) is paper-visible live only, "
        "never tunable, excluded from walk-forward training like the lockbox.")
    with open(path, "w") as f:
        json.dump(j, f, indent=2)
    return j["go_live_utc"]


# ---- standing sealed-window schedule (register 30, docs/lockbox_policy.md)
# Declared 2026-08-18, FORWARD ONLY, chosen by calendar never by content:
# the first two weeks of each quarter (anchored 2026-09-01; months
# Sep/Dec/Mar/Jun, days 1-14 inclusive, UTC) are born sealed. Forward
# readers (Part C, scoreboards, censuses) skip sealed spans automatically;
# explicitly targeting one is refused. The Aug 4-14 legacy lockbox is
# separate and unchanged — first to be spent.
SEALED_SCHEDULE_START = pd.Timestamp("2026-09-01", tz="UTC")
SEALED_MONTHS = (3, 6, 9, 12)
SEALED_DAYS = 14


def is_sealed(ts):
    """True iff ts falls inside a standing sealed window."""
    t = pd.Timestamp(ts)
    t = t.tz_localize("UTC") if t.tzinfo is None else t.tz_convert("UTC")
    return bool(t >= SEALED_SCHEDULE_START and t.month in SEALED_MONTHS
                and t.day <= SEALED_DAYS)


def refuse_if_sealed(ts, what="read"):
    """Fence: explicitly targeting a sealed span is refused outright."""
    if is_sealed(ts):
        raise SystemExit(f"SEALED WINDOW: {what} targets {pd.Timestamp(ts)} "
                         f"inside a standing sealed window (first two weeks "
                         f"of each quarter from {SEALED_SCHEDULE_START.date()}"
                         f") - declared by calendar, spent only by "
                         f"walk-forward evaluation")


def load_frame(slug, tf, root=None, lockbox_evaluation=False,
               narrative_scope=False, log_fn=print):
    """Clean-store frame for slug/tf, lockbox-filtered by default.
    Bars are OPEN-time indexed (verified in the step-zero audit).

    narrative_scope: scoped post-boundary access for narrate replays —
    labels/phases/hypotheses/dump ONLY; no metrics, no event-study rows,
    no trade records, nothing aggregated. Logged on every access, like
    lockbox_evaluation."""
    clean = os.path.join(root, "clean_finsa") if root else CLEAN_DIR
    p = os.path.join(clean, f"{slug}_{tf}.csv")
    if not os.path.exists(p):
        raise FileNotFoundError(f"no clean store for {slug}/{tf} - run store.py build")
    df = pd.read_csv(p, index_col=0, parse_dates=[0])
    boundary = lockbox_boundary(root)
    if lockbox_evaluation:
        log_fn(f"!! LOCKBOX ACCESS: {slug}/{tf} served INCLUDING data at/after "
               f"{boundary} - this is the one-shot final evaluation path.")
        return df
    if narrative_scope:
        log_fn(f"!! LOCKBOX-SCOPE ACCESS (narrative-only): {slug}/{tf} served "
               f"past {boundary} for a narrate replay - labels/phases/"
               f"hypotheses/dump only; no metrics or aggregates permitted.")
        return df
    return df[df.index < boundary]


class ClockGatedFeed:
    """Single market-data access layer for the event loop.

    frames: {tf: DataFrame} open-time indexed. Each bar becomes visible only
    once the clock reaches its CLOSE (open + tf duration). The clock is
    monotonic; there is no API to peek past it."""

    def __init__(self, frames):
        self._frames = {}
        self._close_ts = {}
        self._cursor = {}
        for tf, df in frames.items():
            if not df.index.is_monotonic_increasing:
                raise ValueError(f"{tf}: frame must be sorted by time")
            self._frames[tf] = df
            self._close_ts[tf] = df.index + pd.Timedelta(
                minutes=TF_MINUTES[tf.split(":")[-1]])
            self._cursor[tf] = 0
        self._clock = None

    @property
    def clock(self):
        return self._clock

    def advance_to(self, ts):
        ts = pd.Timestamp(ts)
        if self._clock is not None and ts < self._clock:
            raise ValueError(f"clock cannot move backwards ({self._clock} -> {ts})")
        self._clock = ts
        for tf, closes in self._close_ts.items():
            c = self._cursor[tf]
            n = len(closes)
            while c < n and closes[c] <= ts:
                c += 1
            self._cursor[tf] = c

    def bars(self, tf):
        """All bars CLOSED at or before the current clock. A copy - mutating
        it cannot affect the feed."""
        if self._clock is None:
            raise RuntimeError("advance_to() must be called before reading")
        return self._frames[tf].iloc[:self._cursor[tf]].copy()

    def latest(self, tf):
        c = self._cursor[tf]
        if self._clock is None:
            raise RuntimeError("advance_to() must be called before reading")
        return None if c == 0 else self._frames[tf].iloc[c - 1]

    def newly_closed(self, tf, since_cursor):
        """Bars that closed since a caller-held cursor position; returns
        (bars, new_cursor). The event loop's incremental read."""
        c = self._cursor[tf]
        return self._frames[tf].iloc[since_cursor:c], c
