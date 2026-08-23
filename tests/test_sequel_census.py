"""Register 71 pins: sequel classification (first qualifying bar
decides; absorption outranks opposing within a bar; opposing requires
the ORIGINAL move's direction), windows, and twin-run determinism."""
import json

import numpy as np

from backtest.sequel_census import (ANCHORS, SEQUEL_WINDOWS,
                                    classify_sequel)


def test_instrumentation():
    assert ANCHORS == ("S0-H1", "S0-H2")
    assert SEQUEL_WINDOWS == (5, 15)


def _arrs(n, quad=None, closedir=None, test=None):
    return (np.array(quad if quad else ["narrow-quiet"] * n,
                     dtype=object),
            np.array(closedir if closedir else [1] * n),
            np.array(test if test else [False] * n))


def test_first_bar_decides_and_precedence():
    n = 8
    # bar 2 is wide-loud AGAINST the fire (original direction), bar 3
    # is narrow-loud: opposing comes first -> opposing
    quad, cd, tm = _arrs(n, quad=["narrow-quiet", "narrow-quiet",
                                  "wide-loud", "narrow-loud"]
                         + ["narrow-quiet"] * 4,
                         closedir=[1, 1, -1, 1, 1, 1, 1, 1])
    assert classify_sequel(0, 1, 5, quad, cd, tm, set(), n) == "opposing"
    # same bar carries BOTH signatures: absorption outranks opposing
    quad2, cd2, tm2 = _arrs(n, quad=["narrow-quiet", "narrow-quiet",
                                     "wide-loud"] + ["narrow-quiet"] * 5,
                            closedir=[1, 1, -1, 1, 1, 1, 1, 1],
                            test=[False, False, True] + [False] * 5)
    assert classify_sequel(0, 1, 5, quad2, cd2, tm2, set(), n) \
        == "absorption"
    # wide-loud WITH the fire's direction is not opposing-effort
    quad3, cd3, tm3 = _arrs(n, quad=["narrow-quiet", "narrow-quiet",
                                     "wide-loud"] + ["narrow-quiet"] * 5,
                            closedir=[1, 1, 1, 1, 1, 1, 1, 1])
    assert classify_sequel(0, 1, 5, quad3, cd3, tm3, set(), n) == "none"
    # H3 fire bar inside the window -> absorption
    quad4, cd4, tm4 = _arrs(n)
    assert classify_sequel(0, 1, 5, quad4, cd4, tm4, {3}, n) \
        == "absorption"
    # outside the window -> none
    assert classify_sequel(0, 1, 2, quad4, cd4, tm4, {4}, n) == "none"


def test_twin_run_bit_identity():
    rsq = [["narrow-quiet", "wide-loud", "narrow-loud",
            "wide-quiet"][i % 4] for i in range(300)]
    quad, cd, tm = _arrs(300, quad=rsq,
                         closedir=[(-1) ** i for i in range(300)],
                         test=[i % 17 == 0 for i in range(300)])
    h3 = {i for i in range(0, 300, 23)}
    a = [classify_sequel(i, (-1) ** i, 15, quad, cd, tm, h3, 300)
         for i in range(280)]
    b = [classify_sequel(i, (-1) ** i, 15, quad, cd, tm, h3, 300)
         for i in range(280)]
    assert json.dumps(a) == json.dumps(b)
