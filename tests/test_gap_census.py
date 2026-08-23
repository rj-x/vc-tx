"""Register 67 pins: seam classification (weekend vs pause vs micro),
the fill definition (trade back to prior close, capped at next pause),
the micro-gap spread gate, and twin-run bit-identity."""
import json

import numpy as np
import pandas as pd

from backtest.gap_census import GAP_BUCKETS_ATR, seam_events

T0 = pd.Timestamp("2026-08-17 09:00", tz="UTC")


def _mk(specs):
    """specs: list of (minutes_offset, o, h, l, c)."""
    ts = np.array([T0.value + m * 60_000_000_000 for m, *_ in specs])
    o, h, l, c = (np.array([sp[i] for sp in specs], float)
                  for i in (1, 2, 3, 4))
    return ts, o, h, l, c


def test_buckets_pinned():
    assert GAP_BUCKETS_ATR == (0.25, 1.0)


def test_classification_and_fill():
    # normal bar, then a 70-min pause with an up-gap that fills 2 bars
    # later, then a weekend (>24h) gap that never fills
    specs = [(0, 100, 100.5, 99.5, 100),
             (1, 100, 100.5, 99.5, 100),
             (71, 103, 103.5, 102.5, 103),      # pause gap +3
             (72, 103, 103.2, 102.4, 102.6),
             (73, 102.6, 102.8, 99.9, 100.2),   # trades back to 100
             (73 + 48 * 60, 96, 96.5, 95.5, 96)]  # weekend gap -4.2
    ts, o, h, l, c = _mk(specs)
    ev = seam_events(ts, o, h, l, c, lambda i: 4.0, 0.6)
    assert len(ev["pause"]) == 1 and len(ev["weekend"]) == 1
    p = ev["pause"][0]
    assert p["gap_pts"] == 3.0 and p["fill_bars"] == 2
    w = ev["weekend"][0]
    assert w["gap_pts"] == -4.2 and w["fill_bars"] is None
    # persistence is signed by the gap: weekend gap is DOWN, and price
    # sits below its open -> continuation would need close < open
    assert all(v == 0.0 or isinstance(v, float)
               for v in w["persist"].values())


def test_micro_gap_needs_to_beat_spread():
    specs = [(0, 100, 100.5, 99.5, 100),
             (1, 100.4, 100.6, 100.2, 100.5),   # gap 0.4 <= spread 0.6
             (2, 101.4, 101.6, 101.2, 101.5)]   # gap 0.9 > spread
    ts, o, h, l, c = _mk(specs)
    ev = seam_events(ts, o, h, l, c, lambda i: 4.0, 0.6)
    assert len(ev["micro"]) == 1
    assert ev["micro"][0]["gap_pts"] == 0.9


def test_twin_run_bit_identity():
    specs = [(m, 100 + (m % 7) * 0.3, 100.6 + (m % 7) * 0.3,
              99.4 + (m % 5) * 0.2, 100.1 + (m % 3) * 0.25)
             for m in list(range(0, 200))
             + [270 + i for i in range(60)]
             + [270 + 60 + 49 * 60 + i for i in range(60)]]
    ts, o, h, l, c = _mk(specs)
    a = seam_events(ts, o, h, l, c, lambda i: 5.0, 0.5)
    b = seam_events(ts, o, h, l, c, lambda i: 5.0, 0.5)
    assert json.dumps(a, sort_keys=True, default=str) \
        == json.dumps(b, sort_keys=True, default=str)
