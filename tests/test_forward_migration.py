"""Zone fence for the forward-migration readout (mandatory per the
authorization): a readout span touching the lockbox or working set is
refused before any data is loaded."""
import pandas as pd
import pytest

from backtest.forward_migration import zone_fence, grade_1146
from engine.store_loader import zones


def test_fence_refuses_lockbox_span():
    gl = zones()["go_live"]
    assert gl is not None
    with pytest.raises(SystemExit, match="ZONE FENCE"):
        zone_fence(gl - pd.Timedelta(minutes=1))
    with pytest.raises(SystemExit, match="ZONE FENCE"):
        zone_fence("2026-08-04 00:00:00+00:00")     # lockbox open
    with pytest.raises(SystemExit, match="ZONE FENCE"):
        zone_fence("2026-07-20 00:00:00+00:00")     # working set


def test_fence_passes_forward_span():
    gl = zones()["go_live"]
    assert zone_fence(None) == gl                    # default = go_live
    later = gl + pd.Timedelta(days=1)
    assert zone_fence(later) == later


def test_grade_mechanics():
    t = pd.Timestamp("2026-08-17 12:00:00+00:00")
    deep_unrec = [{"ts": t, "dir": -1, "chain_rungs": 3, "recruited": False,
                   "recruitment_margin": -0.4},
                  {"ts": t, "dir": -1, "chain_rungs": 1, "recruited": False,
                   "recruitment_margin": -0.5}]
    g = grade_1146(deep_unrec)
    assert g["matched"] and g["max_chain_rungs"] == 3
    shallow = [{"ts": t, "dir": -1, "chain_rungs": 2, "recruited": True,
                "recruitment_margin": 0.3}]
    assert not grade_1146(shallow)["matched"]
    assert not grade_1146([])["matched"]
