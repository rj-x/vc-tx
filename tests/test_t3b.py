"""Register 121 pins (T3b half): the T1d-exact gate (no phase gate, no
REACTION requirement) and the pre-registered signature fallback — the
signature bar's own rel_volume reads against h4.pullback_vol_max when
no pullback exists; the pullback path still reads the pullback mean.
The stop fallback is the engine's own h4_stop signature branch (cited,
not re-pinned here)."""
import types

from backtest.t3b import T3bManager


def _mgr():
    m = object.__new__(T3bManager)                # gate logic only
    m.spawn_diag = None
    m._hyp_seq = 0
    m.active = []
    m.calls = []
    m._try_add = lambda name, d, e, setup: m.calls.append((name, d))
    return m


def _e(structural="NO_SUPPLY", trend=1, age=12, rel_volume=0.5,
       reaction=None, pullback=None):
    ctx = types.SimpleNamespace(
        trend=trend, trend_age=age, impulse_reaction=reaction,
        pullback=pullback, idx=50,
        last_swing_low_before=lambda i: 99.0,
        last_swing_high_before=lambda i: 101.0)
    return types.SimpleNamespace(
        structural=structural, qualified=None,
        feats=types.SimpleNamespace(valid=True, rel_volume=rel_volume),
        bar=types.SimpleNamespace(is_stub=False), ctx=ctx,
        cfg=types.SimpleNamespace(hypotheses=types.SimpleNamespace(
            h4=types.SimpleNamespace(pullback_vol_max=0.8))))


def test_t1d_exact_gate_with_signature_fallback():
    m = _mgr()
    m._spawn(_e())                                # quiet signature bar
    assert m.calls == [("H4", 1)]
    g = m.spawn_diag
    assert g["confirm_via_signature"] == 1 and g["confirm_quiet"] == 1
    m._spawn(_e(rel_volume=1.2))                  # loud signature: no spawn
    assert len(m.calls) == 1
    m._spawn(_e(age=9))                           # below T1d age: gate holds
    assert m.spawn_diag["established"] == 2
    assert len(m.calls) == 1
    m._spawn(_e(structural="NO_DEMAND", trend=-1))   # mirror
    assert m.calls[-1] == ("H4", -1)
    m._spawn(_e(trend=-1))                        # trend-mismatched ND/NS
    assert len(m.calls) == 2


def test_pullback_path_still_reads_pullback_mean(monkeypatch):
    import backtest.t3b as t3b
    m = _mgr()
    seen = {}

    def fake_stats(pb, idx, d):
        seen["pb"] = pb
        return 0.5, None
    monkeypatch.setattr(t3b, "_pullback_stats", fake_stats)
    pb = {"start_idx": 40, "lows": [99.5], "highs": [100.5]}
    m._spawn(_e(reaction="REACTION", pullback=pb, rel_volume=9.9))
    assert seen["pb"] is pb                       # the pullback read
    assert m.calls == [("H4", 1)]                 # loud BAR is irrelevant
    assert m.spawn_diag["confirm_via_pullback"] == 1
