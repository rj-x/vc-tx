"""Register 136 pin: the lookahead PROPERTY, enforced behaviorally.

A trailing/prior field's value may depend only on store rows at or
before its anchor. Each run draws a weekly-rotating sample of
PIN_PAIRS (trade, field) pairs from the enriched journal, truncates
the input store at the pair's anchor — rows whose bar close exceeds
the anchor do not exist at all — recomputes, and requires the emitted
value to survive. The seed is the ISO year+week: deterministic within
a week (twin-run holds), rotating weekly, so any future lookahead —
whatever its mechanism — fails the suite within a week of its
introduction. Anchors per register 136: entry close-stamp for the
volatility percentiles; trade close for the hold-window descriptor
(its claim is the hold, not the prior)."""
import csv
import datetime
import os

import numpy as np
import pandas as pd
import pytest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ENRICHED = os.path.join(ROOT, "reports", "trades_enriched.csv")

PIN_PAIRS = 25           # register 136: pairs per run
PIN_FIELDS = ("atr_pctl", "atr_pctl_tod", "spans_high_event")


def _none(v):
    return None if v in ("", "None", None) else v


def truncated_frame(frame, anchor_ns):
    """Store as it existed at the anchor: bars CLOSED by then only."""
    close = frame["time"].dt.as_unit("ns").astype("int64").to_numpy() \
        + 15 * 60_000_000_000
    return frame[close <= anchor_ns].reset_index(drop=True)


def recompute(field, row, frames, calendar):
    from backtest.vol_regime import atr_pctl_fn, atr_pctl_tod_fn
    from backtest.event_clock import spans_high
    instr = row["instrument"]
    if field == "spans_high_event":
        if calendar is None:
            return None
        close_ns = pd.Timestamp(row["close_ts"]).value
        rel, span = calendar
        rel_t = [r for r in rel if r[0] <= close_ns]
        v = spans_high(row["open_ts"], row["close_ts"], rel_t, span)
        return None if v is None else str(v)
    anchor = pd.Timestamp(row["open_ts"]).value
    atr0 = _none(row["atr_entry"])
    if atr0 is None:
        return None
    fn = {"atr_pctl": atr_pctl_fn,
          "atr_pctl_tod": atr_pctl_tod_fn}[field]
    f = fn(instr, frame=truncated_frame(frames[instr], anchor))
    v = f(anchor, float(atr0))
    return None if v is None else str(v)


def test_rotating_truncation_sample():
    if not os.path.exists(ENRICHED):
        pytest.skip("no enriched journal artifact")
    from backtest.vol_regime import INSTRUMENTS, frame15
    rows = [r for r in csv.DictReader(
                l for l in open(ENRICHED) if not l.startswith("#"))
            if r["instrument"] in INSTRUMENTS
            and _none(r["atr_entry"]) is not None]
    assert rows, "enriched journal empty"
    y, w, _ = datetime.date.today().isocalendar()
    rng = np.random.RandomState(y * 100 + w)
    picks = [(rows[i], PIN_FIELDS[j]) for i, j in zip(
        rng.randint(0, len(rows), PIN_PAIRS),
        rng.randint(0, len(PIN_FIELDS), PIN_PAIRS))]
    frames = {i: frame15(i)
              for i in {r["instrument"] for r, _ in picks}}
    try:
        from backtest.event_clock import load_calendar
        calendar = load_calendar()
    except Exception:
        calendar = None
    bad = []
    for r, field in picks:
        emitted = _none(r[field])
        redone = recompute(field, r, frames, calendar)
        if field == "spans_high_event" and calendar is None:
            continue                     # no calendar to replay against
        if emitted != redone:
            bad.append((r["instrument"], r["variant"], r["open_ts"],
                        field, emitted, redone))
    assert not bad, (
        "lookahead: value changed when the store was truncated at its "
        f"anchor (emitted vs recomputed): {bad[:5]}")
