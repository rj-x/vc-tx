"""Register 102 pins: strict-order halting (the tripping row is taken,
the remainder foregone), the two rule families, the dodged/forfeited
decomposition priced from the foregone rows, and twin-run."""
import json

import pandas as pd

from backtest.circuit_breaker import apply_rule, replay, rules


def test_rules_and_apply():
    names = [r[0] for r in rules()]
    assert names == ["halt@1stops", "halt@2stops", "halt@3losers",
                     "halt@5losers"]
    day = [(2.0, "target"), (-9.0, "stop"), (2.0, "target"),
           (-9.0, "stop"), (2.0, "target")]
    assert apply_rule(day, "stops", 1) == 2      # after the first stop
    assert apply_rule(day, "stops", 2) == 4      # after the second
    assert apply_rule(day, "stops", 3) is None
    losers = [(-1.0, "eod"), (-1.0, "eod"), (-1.0, "eod"), (5.0, "target")]
    assert apply_rule(losers, "losers", 3) == 3
    assert apply_rule([(-1.0, "eod"), (5.0, "target"), (-1.0, "eod")],
                      "losers", 3) is None       # the streak resets


def _rows():
    t0 = pd.Timestamp("2026-08-20 08:00:00+00:00")
    seq = [(2.0, "target"), (-9.0, "stop"), (3.0, "target"),
           (-9.0, "stop"), (-2.0, "eod")]
    return [(t0 + pd.Timedelta(minutes=10 * i), p, r)
            for i, (p, r) in enumerate(seq)]


def test_replay_decomposition_and_twin_run():
    rep = replay(_rows(), "Europe/London")
    r1 = rep["halt@1stops"]
    # halt after row 1 (the first stop): foregone = target +3, stop -9,
    # eod -2 -> net delta = -(3 - 9 - 2) = +8
    assert r1["halt_days"] == 1 and r1["halt_dates"] == ["2026-08-20"]
    assert r1["stops_dodged"] == 1 and r1["stops_dodged_pts"] == 9.0
    assert r1["targets_forfeited"] == 1 and r1["targets_forfeited_pts"] == 3.0
    assert r1["eod_forfeited"] == 1 and r1["eod_forfeited_pts"] == -2.0
    assert r1["net_delta"] == 8.0
    r2 = rep["halt@2stops"]                     # after row 3: only the eod
    assert r2["rows_foregone"] == 1 and r2["net_delta"] == 2.0
    a = json.dumps(replay(_rows(), "Europe/London"), sort_keys=True)
    b = json.dumps(replay(_rows(), "Europe/London"), sort_keys=True)
    assert a == b
