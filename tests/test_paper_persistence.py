"""2026-08-14 finding: steady-state polls must persist through the standard
raw->clean collector path so warm-from-store == last-processed."""
import json
import os
import sys

import pandas as pd

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "scripts"))
import collect as collector          # noqa: E402
import store as store_mod            # noqa: E402


def test_steady_state_polls_advance_both_stores(tmp_path, monkeypatch):
    monkeypatch.setattr(collector, "DATA_DIR", str(tmp_path / "data"))
    monkeypatch.setattr(store_mod, "RAW", str(tmp_path / "data"))
    monkeypatch.setattr(store_mod, "CLEAN", str(tmp_path / "clean"))
    os.makedirs(tmp_path / "data", exist_ok=True)
    base = pd.Timestamp("2026-08-14 09:00", tz="UTC")

    def page(n_new):
        idx = pd.date_range(base, periods=n_new, freq="1min")
        return pd.DataFrame({"time": idx, "open": 100.0, "high": 101.0,
                             "low": 99.0, "close": 100.5, "volume": 50})

    # N steady-state "polls": persist-then-feed path (same collector code)
    for n in (5, 8, 12):
        pg = page(n)
        collector.merge_store("minute", "mid", pg.iloc[:-1], "uk100fut")
        store_mod.build_one("uk100fut", verbose=False)
    raw = pd.read_csv(tmp_path / "data" / "uk100fut_minute_mid.csv",
                      parse_dates=["time"])
    clean = pd.read_csv(tmp_path / "clean" / "uk100fut_1min.csv",
                        index_col=0, parse_dates=[0])
    last_polled_open = page(12)["time"].iloc[-2]     # last SETTLED bar
    assert raw["time"].max() == last_polled_open, "raw store lags polls"
    assert clean.index.max() == last_polled_open, "clean store lags polls"
    assert len(raw) == 11, "dedup failed across overlapping polls"
    # restart contract: warm point == last polled settled bar
    assert clean.index.max() == last_polled_open
