# Trade management review: is the exit engine starving the trades?

*Replay of all 12,783 trades in `reports/trades.csv` against `clean_finsa/` 1M data, 2026-08-24.
Rule under test: initial SL 2.5×ATR(15M); trail 0.25×ATR(15M) beyond the 2nd-previous settled 1M bar's extreme; tighter-of, ratchet-only, no target, EOD flat native; honest fills.*

**Replay fidelity:** entry convention verified (trades are close-stamped; `open_price` = open of the bar at `open_ts − 1min`; per-instrument cost ger40 1.5 / nas100 1.8 / uk100 1.3 / us30 2.6 pts). The reconstructed baseline reproduces recorded points with corr 0.945, mean −1.88 vs −2.03 recorded, 65% of trades within 1 pt.

## Verdict: yes — the trail is starving the trades, and the book's loss is almost entirely spread

1. **90% of the net loss is transaction cost.** Recorded net −25,899 pts; total spread paid 23,226 pts; gross (pre-cost) P&L −2,672 pts (−0.21 pts/trade, −0.007 ATR/trade). The current management scratches nearly every trade to ~zero gross and pays the spread 12,783 times.
2. **The initial 2.5×ATR stop is decorative.** The average stop exit realizes −0.087 ATR — 3.5% of the stated risk budget. The "tighter-of" clause means the 1M trail governs from the first bar.
3. **Starvation, quantified.** Median stopped trade achieved a max favorable excursion of just **0.27×ATR(15M)** before dying; only 11.7% ever saw +1 ATR; 51.5% were dead within 5 minutes. **48% of stopped trades would have closed profitable at EOD**; average post-exit favorable move was 145 pts.
4. **Timeframe mismatch is the root cause.** Entries are 15M theses; the trail anchors to a 1M bar two bars back plus 0.25 ATR — total room ≈ 0.3–0.4×ATR(15M). A 15M-scale idea is being managed with 1M-noise-scale tolerance.
5. **1,411 trades (11%) died at the entry instant** (`stop_gap`, duration 0): the trail level was already beyond the entry price at fill, closing the trade immediately at entry and donating the spread — ~2,900 pts of pure structural bleed.

## Counterfactual replays (same signals, same costs, honest fills, EOD flat)

| Variant | Net pts | Gross/ATR per trade | Win% | Pos. weeks | Ex-top-50 net |
|---|---|---|---|---|---|
| BASE (current rule, reconstructed) | −23,987 | −0.007 | 27% | 0/7 | −33,572 |
| Trail buffer 0.25→1.5×ATR (1M anchor) | +13,555 | +0.028 | 36% | 2/7 | −20,511 |
| Trail on settled 15M bars (0.25 buf) | −5,313 | — | 22% | — | — |
| Trail armed only after +1 ATR MFE (15M anchor) | +8,217 | +0.011 | 50% | 1/7 | −24,051 |
| Fixed target 2×ATR, no trail | −2,400 | — | 55% | 3/7 | −14,899 |
| **No trail: 2.5 ATR SL only, hold to EOD** | **+82,632** | +0.057 | 33% | 5/7 | +26,106 |
| **Breakeven-only: BE at +1.5 ATR, else hold to EOD** | **+76,483** | **+0.095** | 21% | 4/7 | **+27,890 (PF 1.21)** |

Every loosening of the trail improves the book; removing it entirely swings the outcome by ~107k pts. The best *risk-adjusted* scheme tested is breakeven-only management: initial 2.5 ATR stop, move to entry at +1.5 ATR MFE, otherwise ride to EOD — the only variant with positive gross per ATR (+0.095) and still positive after stripping its 50 best trades.

## Honest caveats

- **No scheme achieves weekly consistency** (best: 5/7 positive weeks; all schemes lost in W33's chop and feasted in W31's trend). Management determines how much noise and spread you pay — it cannot manufacture directional edge the signals don't have. The ATR-normalized edge of the signal book remains ≈ 0; the signal-selection findings in `backtest_read.md` still have to carry alpha.
- Hold-to-EOD variants are **us30/nas100-driven and negative on ger40/uk100**; results are tail-heavy (though BE-only survives ex-top-50) and in-sample — validate forward before adopting.
- Long holds (~11h avg to session end) mean overlapping positions and 2.5 ATR per-trade risk vs ~0.09 realized today: size down accordingly; portfolio heat needs its own cap.
- "EOD flat native" was approximated by the data's session break; ATR = Wilder-14 on 15M.

## Recommendations, in order of conviction

1. **Never arm the 1M trail at entry.** The tighter-of clause makes the trail the binding stop from bar one and creates the instant-kill class. Minimum fix: trail activates only after the trade reaches +1×ATR(15M) MFE. Preferred fix: drop the 1M trail entirely.
2. **Adopt breakeven-only management as the new default candidate:** 2.5×ATR(15M) initial stop → stop to entry at +1.5×ATR MFE → EOD flat. Best gross-per-ATR of everything tested (+0.095 vs −0.007 now), left tail capped, right tail kept.
3. **If a trail is kept, match it to the signal timeframe:** anchor to settled **15M** bars (not 1M) and/or widen the buffer to ≥0.75–1.5×ATR(15M). Every step from 0.25×ATR/1M toward 1.5×ATR/15M monotonically recovers P&L.
4. **Refuse entries whose trail/stop is already beyond the fill price** (the 1,411 instant `stop_gap` kills, ~2,900 pts): if the management scheme would close the trade at entry, the trade should not open.
5. **Attack the spread bleed directly:** 23,226 pts of the 25,899 loss is cost. Dedup rapid re-fires of the same sentence (many entries 1 min apart each re-pay spread), and reconsider uk100fut, where the spread is 0.115×ATR — ~2× the cost of the other instruments in volatility terms and negative under every management scheme tested.
6. **Validate forward, per regime.** All variants share W31 (trend) as the profit engine and W33 (chop) as the failure mode; a simple regime overlay (e.g., only hold-to-EOD when the day is trending by some pre-registered measure) is the natural next pre-registered question, and any adopted change should run as a NEW S-number per register doctrine, not a silent rewrite.
