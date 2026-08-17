"""tod-anchor defect fix (2026-08-17): live-loop bin keys == resampler's."""
import pandas as pd
from engine.resample import canonical_tod


def test_canonical_anchor_matches_resampler():
    tod, _ = canonical_tod(pd.Timestamp("2026-08-14 15:17:00+00:00"))
    assert tod == 1127            # the Friday 15:18Z-close bar's replay bin
    tod2, d2 = canonical_tod(pd.Timestamp("2026-08-14 20:35:00+00:00"))
    assert tod2 == 5              # 21:35 London = 5 min into NEXT trading day
    _, d1 = canonical_tod(pd.Timestamp("2026-08-14 19:25:00+00:00"))
    assert d2 == d1 + pd.Timedelta(days=1)
