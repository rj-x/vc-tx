"""TEST criteria — RULES.md Sec 0, authoritative wherever used.
One predicate, two anchors: the classifier's registry-based TEST label and
each hypothesis's test-of-signature check both call this function.
"""


def test_criteria(bar, feats, sig_extreme, sig_rel_volume, direction, atr, cfg):
    """direction: +1 = long test of a LOW (probe down, holds above);
                  -1 = short test of a HIGH (probe up, fails below).
    All five criteria (i)-(v); written long-side, mirrored for short."""
    if not feats.valid or atr is None or atr <= 0:
        return False
    h = cfg.hypotheses
    prox = h.test_proximity_atr * atr
    if direction > 0:
        reaches = bar.low <= sig_extreme + prox        # (i) actually probed
        holds = bar.low > sig_extreme                  # (ii) held the low
        recovers = feats.close_pos > 0.5               # (iii)
    else:
        reaches = bar.high >= sig_extreme - prox
        holds = bar.high < sig_extreme
        recovers = feats.close_pos < 0.5
    low_vol = feats.rel_volume is not None and feats.rel_volume < 1.0        # (iv)
    vs_sig = (feats.rel_volume is not None and sig_rel_volume
              and feats.rel_volume < h.test_vol_vs_signature * sig_rel_volume)  # (v)
    return reaches and holds and recovers and low_vol and vs_sig
