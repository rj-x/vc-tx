# Backtest read: `sentence_id` performance and where the levers are

*Analysis of `reports/trades.csv` + `reports/weekly_summary.csv` against `docs/hypothesis_register.md` — 2026-08-24.*

## Headline

The book as a whole is deeply underwater: **−25,899 pts across 12,783 trades, 26.9% win rate, avg −2.03 pts/trade, and every single ISO week from W29 to W35 is net negative**. Only one sentence is net positive with meaningful sample size overall (S0-H16), and every green cell in the sentence × instrument matrix is tail-dependent — strip its 3 best trades and it goes red. That said, the data contains several large, ex-ante-usable conditioning effects, plus one structural bleed fixable at the engine level.

## Best performers by sentence × instrument

| Sentence | Instrument | Net pts | n | Avg/trade | Ex-top-3 |
|---|---|---|---|---|---|
| S0-H16 | us30fut | +275 | 24 | +11.5 | −63 |
| S0-H17 | nas100fut | +241 | 43 | +5.6 | −169 |
| S0-H19 | us30fut | +235 | 238 | +1.0 | −550 |
| S0-H4 | nas100fut | +120 | 31 | +3.9 | −117 |
| S1-H9 | nas100fut | +100 | 27 | +3.7 | −305 |

**S0-H16** (opening-session direction predicts closing-session direction, the GHLZ hypothesis) is the only sentence net-positive across the whole book (+238, n=103, PF 1.33). It works on **us30fut and ger40fut** and loses on nas100fut/uk100fut. The worst offenders in absolute terms are S0-H11/S1-H11 (−7,577 combined, worst on us30fut and nas100fut), S0-H14 (−3,250), and S0-H10 (−3,061) — the three highest-frequency rows are the three biggest bleeders, and S0-H10 already carries a *deprioritize* label in the register, which this data supports emphatically.

By instrument overall: **uk100fut (the canonical/home instrument) loses least per trade (−1.36); us30fut loses most (−2.81, −9,545 pts total)**. The provisional instruments are worse than home, not better.

## The honest caveat before the opportunities

The payoff shape is: ~88% of exits are stops, half of all trades die within 5 minutes (avg −9.8 pts; the 0–5 min bucket is −55k gross), and nearly all profit lives in trades that survive 15–60 min (+36,610 pts in that bucket) or to end-of-day (51 eod exits = **+2,366 pts, avg +46/trade**). Median trade is negative in *every* cell tested. So "best performer" here means "owns the right tail," not "wins consistently" — treat every green number above as fragile at these sample sizes.

## Opportunities in the data (ranked by robustness)

**1. Session filtering — London is the single biggest bleed.** London is −2.90/trade (−11,610 pts, 45% of all losses); ny_only is −0.63. Specific, actionable cells:

- **S0-H6 out of London**: −759 pts in London (n=233) vs +204 in asia+NY. This directly confirms the register's pre-registered **Q1-H6 London-suppression prediction** in payoff terms, not just precision — the strongest hypothesis-consistent finding in the file.
- **H2 family (S0-H2 + S1-H2) in ny_only**: +808 pts, n=368, +2.20/trade vs −2.25 unconditioned — driven by us30fut (+1,065) and nas100fut (+395); still negative on ger40/uk100.
- **S0-H19 in NY+overlap**: +760 pts, n=173, and it's the **only conditioned cell that stays positive ex-top-3** (+22) besides H16 shorts.

**2. S0-H16 short-side only — the most robust cell in the file.** Shorts: +462 pts, n=46, 43.5% win rate, **still +62 after removing the top 3 trades**; longs: −3.92/trade. Concentrated in us30fut (+309, median trade *positive* at +8.6) and ger40fut (+169). A down opening session carrying into the close is where H16's edge lives; the long side is noise or worse.

**3. with_trend gate.** Helps exactly the sentences you'd expect: S1-H2 (+0.67 with-trend vs −2.98 counter), S0-H1 (+0.13 vs −2.33), S1-H9 (+2.57 vs −3.90), S0-H9, S0-H19. Counter-trend fires on the reversal-family sentences are where they die.

**4. Structure flags at entry.** Trades entered on `new_hl`/`new_ll` bars lose materially less (−1.37/−1.50 per trade) than `new_hh`/`new_lh` (−2.57/−2.59); `retest_level=True` beats False (−1.76 vs −2.22). Chasing a fresh extreme is systematically worse than entering on a pullback structure or level retest.

**5. Fix the stop_gap bleed (engine-level, free money).** 1,411 trades (11%) have `duration_min=0` and exit `stop_gap` — the entry bar gaps straight through the stop for **−2,892 pts** of pure structural loss, worst on us30fut (−1,204). These trades never had a chance; entry-time gap/spread checks or stop placement outside the entry bar's gap range would remove most of it.

**6. Composite reality check.** S0-H18 minted on "+20.1pp backtest, positive payoff both windows" (register 76) but sits at **−1,524 pts, −4.03/trade** here — third worst per-trade in the book. S0-H17 is −330 overall (its nas100 pocket notwithstanding). The narrative-composite layer is not surviving contact with this window and deserves a hostile review before more mints.

## Bottom line

If allocating from this file alone: **S0-H16 short-only on us30fut/ger40fut** is the one configuration with a positive median and tail-independent net; **S0-H19 in NY/overlap on us30fut/nas100fut** is a credible second. The rest of the book's realistic path to improvement is subtractive — cut London (especially H6), cut counter-trend fires on the reversal family, cut H16 longs, retire the H10/H11/H14 volume rows, and fix the stop_gap leak — before any new signal is added. And given the every-week-negative equity curve, the stop geometry itself (half the book dead in ≤5 min while all profit accrues after 15) is a bigger lever than any signal selection.
