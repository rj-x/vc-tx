# Volume Profile Organ — first output + parameter proposals

Engine `dc960c4c1` — OBSERVATIONAL sense-organ (register 16 #2) — parameter-proposal instrument; never validation; proposals await operator ratification

Instrument uk100fut, 16 working-set sessions. Bucket 4.0 pts.

## Derivations (measured)

- **bucket**: median 1M true range = 4.0 pts (atr15-scale median 17.5); bucket = max(1.0, median range) = 4.0
- **lookback_stability_rank_corr**: {3: 0.098, 5: 0.134, 8: -0.053, 10: -0.119, 15: None}
- **lookback**: K=5: smallest K within 95% of max next-session rank-correlation
- **node_gap**: top-decile buckets carry 20.5% of volume; bottom decile 2.4% — deciles separate cleanly; node=p90, gap=p10 proposed

## Proposal — H11 parameters (ratification pending)

- **bucket_size_pts**: 4.0
- **rolling_lookback_sessions**: 5
- **node_threshold**: bucket volume >= p90 of trailing-profile buckets
- **gap_threshold**: bucket volume <= p10
- **grading_note**: behavioral/either-direction per the H11 entry; traversal/stall operationalization to be pre-registered with the row
- **HONESTY_FLAG**: the lookback derivation's own measurement is WEAK: next-session profile rank-correlation peaks at ~0.13 and turns negative beyond K=5 on 16 sessions — profile persistence is marginal in this sample. K=5 is best-of-a-weak-field, not a strong optimum; H11's premise itself will be what the row tests

## Proposal — H6 location thresholds (ratification pending)

- **session_extreme_proximity**: 0.25 x ATR(15M) — founding level-identity tolerance, reused; measured p5 extreme-approach distance 12.6 pts is the same scale
- **day_relative_spread_pctile**: >= 90 (measured: p90 of day-relative rank = 0.902)
- **close_pos**: <= 0.25 for the short (mirror >= 0.75) — founding close_pos_lo neighborhood
- **wick_frac_min**: 0.33 — founding labels.wick_frac_min, cited
