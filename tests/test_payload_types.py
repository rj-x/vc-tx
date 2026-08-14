"""Item-1 pin: numeric payload fields are plain floats at event construction
for BOTH location_ref resolution paths (session-extreme AND swing-registry).
Bars flow through numpy (pandas rows in production), so feed np.float64."""
import numpy as np

from helpers import scenario_cfg
from engine.bars import Bar
from engine.context import ContextTracker
from engine.narrative import Narrative
from engine.pipeline import TFPipeline


def test_label_payload_types_both_paths():
    cfg = scenario_cfg({"features.min_baseline_obs": 4,
                        "features.simple_baseline_window": 10})
    narr = Narrative()
    pipe = TFPipeline(cfg, "1min", narr)
    sig_ctx = ContextTracker(cfg, "15min")
    sig_ctx.atr = 2.0
    sig_ctx.levels = [100.0]
    f = np.float64
    px = 100.0
    for i in range(14):                       # warmup + drift down
        b = Bar(i, f(px), f(px + 0.4), f(px - 0.6), f(px - 0.4), f(100),
                tf="1min", session_id=1, tod_bin=i)
        pipe.on_close(b, signal_ctx=sig_ctx)
        px -= 0.4
    # wide quiet decline at the running session LOW -> session-extreme path
    pipe.on_close(Bar(20, f(px), f(px + 0.1), f(px - 3.0), f(px - 2.8), f(60),
                      tf="1min", session_id=1, tod_bin=20),
                  signal_ctx=sig_ctx)
    # wide quiet advance closing AT the swing level 100 -> swing-registry path
    pipe.on_close(Bar(21, f(97.0), f(100.2), f(96.9), f(100.0), f(60),
                      tf="1min", session_id=1, tod_bin=21),
                  signal_ctx=sig_ctx)
    seen = set()
    for e in narr.events:
        if e["type"] == "LABEL" and e.get("location_ref"):
            seen.add("swing" if e["location_ref"] == "signal_swing_level"
                     else "extreme")
            for fld in ("location_level", "dist_pts", "dist_signal_atr",
                        "high", "low", "close"):
                v = e.get(fld)
                assert v is None or type(v) is float, (fld, type(v), e)
    assert seen == {"swing", "extreme"}, seen
