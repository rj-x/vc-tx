"""Register finding 23 (2026-08-18): build_one truncate-rewrote clean
stores, exposing concurrent readers (live warm-from-store; git snapshot at
commit time — observed: an empty uk100fut_1h.csv blob in commit 9bcf9ec) to
truncated data. Store writes must be atomic: a reader opening at ANY moment
during a build sees the old file or the new file, never an empty or partial
one."""
import os
import sys

import pandas as pd
import pytest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "scripts"))
import store as store_mod            # noqa: E402


def _df(vals):
    return pd.DataFrame(
        {"close": vals},
        index=pd.date_range("2026-08-14 09:00", periods=len(vals),
                            freq="1min", tz="UTC", name="time"))


def test_reader_never_sees_empty_or_partial(tmp_path, monkeypatch):
    """Crash at any point during the new write leaves the old file intact;
    only a completed write changes what a reader sees."""
    path = str(tmp_path / "uk100fut_1min.csv")
    old, new = _df([1.0, 2.0]), _df([3.0, 4.0, 5.0])
    store_mod._atomic_to_csv(old, path)
    old_bytes = open(path, "rb").read()
    assert len(old_bytes) > 0

    # crash mid-write of the replacement (temp file half-written): the
    # visible file must still be the complete OLD content
    calls = {"n": 0}
    orig = pd.DataFrame.to_csv

    def crashing_to_csv(self, *a, **kw):
        calls["n"] += 1
        p = a[0] if a else kw.get("path_or_buf")
        with open(p, "w") as f:
            f.write("time,close\n")            # partial temp content
        raise OSError("simulated crash mid-write")

    monkeypatch.setattr(pd.DataFrame, "to_csv", crashing_to_csv)
    with pytest.raises(OSError):
        store_mod._atomic_to_csv(new, path)
    monkeypatch.setattr(pd.DataFrame, "to_csv", orig)
    assert calls["n"] == 1
    assert open(path, "rb").read() == old_bytes   # old, complete, unchanged

    # completed write: reader sees the complete NEW content
    store_mod._atomic_to_csv(new, path)
    seen = pd.read_csv(path)
    assert list(seen["close"]) == [3.0, 4.0, 5.0]


def test_temp_file_is_same_directory(tmp_path):
    """os.replace is atomic only within a filesystem — the temp file must
    live next to the target, never in a system temp dir."""
    path = str(tmp_path / "x.csv")
    store_mod._atomic_to_csv(_df([1.0]), path)
    assert not os.path.exists(path + ".tmp")
    # the helper writes <path>.tmp: prove it by intercepting os.replace
    seen = {}
    orig_replace = os.replace

    def spy(src, dst):
        seen["src"], seen["dst"] = src, dst
        return orig_replace(src, dst)

    os.replace, _ = spy, None
    try:
        store_mod._atomic_to_csv(_df([2.0]), path)
    finally:
        os.replace = orig_replace
    assert seen["src"] == path + ".tmp"
    assert os.path.dirname(seen["src"]) == os.path.dirname(seen["dst"])


def test_report_json_atomic(tmp_path):
    path = str(tmp_path / "_report.json")
    store_mod._atomic_json_dump({"a": 1}, path, indent=2)
    import json
    assert json.load(open(path)) == {"a": 1}
    assert not os.path.exists(path + ".tmp")
