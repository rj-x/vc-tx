"""Register 135 pin: the microsecond/nanosecond timebase incident.
pandas 3 parses the store's time column to datetime64[us]; a raw
astype("int64") yields microseconds, and a nanosecond probe
(Timestamp.value) searchsorted against a microsecond axis lands past
the end of the array — trailing-prior windows silently become
file-tail windows (lookahead) and zone masks go all-backtest. Every
time axis must convert explicitly via .dt.as_unit("ns"). Pin the
class (the banned pattern) and the instance (the register-130 fn's
window is prior, not file-tail)."""
import glob
import os

import pandas as pd

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def test_no_raw_int64_time_axis():
    bad = []
    for p in (glob.glob(os.path.join(ROOT, "backtest", "*.py"))
              + glob.glob(os.path.join(ROOT, "engine", "*.py"))
              + glob.glob(os.path.join(ROOT, "scripts", "*.py"))):
        if '["time"].astype("int64")' in open(p).read():
            bad.append(os.path.basename(p))
    assert not bad, f"raw microsecond time axes: {bad}"


def test_trailing_window_is_prior_not_file_tail():
    from backtest.vol_regime import atr_pctl_fn
    f = atr_pctl_fn("us30fut")
    t = pd.read_csv(os.path.join(ROOT, "clean_finsa",
                                 "us30fut_15min.csv"),
                    usecols=["time"], parse_dates=["time"])["time"] \
        .dt.as_unit("ns").astype("int64")
    early = int(t.iloc[2]) + 15 * 60_000_000_000
    late = int(t.iloc[-1]) + 15 * 60_000_000_000
    # broken axis returned a value for EVERY entry (file-tail window
    # always holds >= 50 values); a prior window must warm up ...
    assert f(early, 100.0) is None
    # ... and a late entry with an absurd ATR tops a NON-EMPTY window
    assert f(late, 1e12) == 100.0
