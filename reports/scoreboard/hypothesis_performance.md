# Hypothesis Performance — Summary Matrix (page 1)

Engine `e458da339` — OBSERVATIONAL signal scoreboard - move-detection, not trading; no fills exist here by construction; never validation (docs/hypothesis_lifecycle.md stage 4)

**Review labels are RECOMMENDATIONS — none actioned, review pending operator familiarity.** Cells: marker + precision LIFT vs that context's OWN chance rate, (hits/fires), payoff net/median points (directional rows; either-direction rows have no payoff by construction). ▲/▼ = beyond ±2pp of chance, · = within. (°…) = small-n (fires<20 or episodes<10): dimmed, excluded from any future label arithmetic. Read READING_GUIDE.md first; full detail in signal_scoreboard.json.

| H | label | backtest whole | backtest london | forward whole | forward london |
|---|---|---|---|---|---|
| *context* | | 180 ep; chance 23.6%dir/44.3%either | 53 ep; chance 24.9%dir/47.1%either | 28 ep; chance 26.6%dir/47.2%either | 6 ep; chance 23.3%dir/42.4%either |
| H1 | keep-watching | ·-0.4pp (16/69) net+194/med+2.8 | ▲+6.9pp (7/22) net+133/med+3.0 | (°▲+2.8pp (5/17) net-18/med-1.0) | (°·+1.7pp (1/4) net-17/med-7.0) |
| H2 | promote-candidate | ·+1.2pp (86/347) net+781/med+1.5 | ▲+6.3pp (25/80) net+521/med+9.2 | ▲+10.0pp (26/71) net-60/med-0.8 | (°▼-9.0pp (2/14) net-14/med-1.8) |
| H3 | keep-watching | — | — | (°▲+23.4pp (2/4) net+8/med+0.3) | (°▲+26.7pp (1/2) net+8/med+3.8) |
| H4 | keep-watching | (°▼-23.6pp (0/7) net+14/med+0.5) | (°▼-24.9pp (0/1) net+6/med+5.5) | — | — |
| H7 | keep-watching | ▲+7.6pp (35/112) net+7/med+2.8 | ▲+4.4pp (12/41) net-217/med+2.7 | ▼-12.3pp (3/21) net-32/med+0.0 | (°▼-5.1pp (2/11) net-60/med-8.5) |
| H7 (either-dir) | keep-watching | ▲+9.3pp (60/112) | ▲+4.1pp (21/41) | ▼-9.1pp (8/21) | (°▲+12.1pp (6/11)) |
| H8 | keep-watching | ▲+2.1pp (161/347) | ▲+6.7pp (43/80) | ▲+2.1pp (35/71) | (°▼-21.0pp (3/14)) |
| H9 | keep-watching | ▲+3.7pp (15/55) net+319/med+3.5 | (°▲+20.6pp (5/11) net+108/med+12.5) | (°▼-18.3pp (1/12) net-18/med-3.1) | — |
| H10 | deprioritize | ▼-4.8pp (55/293) net-240/med-1.4 | ▲+2.4pp (18/66) net-62/med+1.9 | ▼-18.7pp (6/76) net-220/med-3.5 | (°▼-13.3pp (1/10) net+27/med+4.8) |
| **union coverage** | | 52.2% (94/180) | 47.2% (25/53) | 78.6% (22/28) | 83.3% (5/6) |

Not graded: H5 disabled; H6 definition-pending — see register entries.

---

# Hypothesis Cards (page 2)

## H1
*A climactic bar — extreme volume on a wide spread late in an extended move — marks exhaustion, and price then reverses against the climax direction.*
Grading: directional. Latest review: keep-watching (recommendation).

**H1** — session × window grid (cells as in the matrix):

| session | backtest | forward |
|---|---|---|
| whole | ·-0.4pp (16/69) net+194/med+2.8 | (°▲+2.8pp (5/17) net-18/med-1.0) |
| london | ▲+6.9pp (7/22) net+133/med+3.0 | (°·+1.7pp (1/4) net-17/med-7.0) |
| overlap | (°▲+23.9pp (1/2) net+35/med+17.7) | (°▼-33.8pp (0/1) net-0/med-0.3) |
| ny_only | ▲+8.0pp (4/22) net+17/med+1.6 | (°▼-11.0pp (0/1) net-1/med-0.8) |
| dead | (°▲+7.4pp (3/12) net+30/med+1.1) | (°▲+33.5pp (1/2) net+3/med+1.7) |
| asia | (°▼-23.4pp (1/11) net-22/med-2.6) | (°▼-8.2pp (3/9) net-3/med-1.0) |

- backtest payoff: right +639 / wrong -445 / net +194 pts; median per fire +2.75 (n=68)
- backtest best call: 2026-07-29 04:04 +105.2pts remaining (episode 102.8pts, major)
- backtest worst false alarm: 2026-07-23 12:17 -70.7pts adverse
- forward payoff: right +28 / wrong -46 / net -18 pts; median per fire -1.00 (n=17)
- forward best call: 2026-08-17 10:30 +46.5pts remaining (episode 42.7pts, major)
- forward worst false alarm: 2026-08-18 12:05 -20.7pts adverse
- earliness (backtest): median 29.0 pts of move remaining at fire (n=23)

## H2
*A failed probe beyond a prior extreme — an upthrust above or spring below that closes back inside — reverses against the probe.*
Grading: directional. Latest review: promote-candidate (recommendation).

**H2** — session × window grid (cells as in the matrix):

| session | backtest | forward |
|---|---|---|
| whole | ·+1.2pp (86/347) net+781/med+1.5 | ▲+10.0pp (26/71) net-60/med-0.8 |
| london | ▲+6.3pp (25/80) net+521/med+9.2 | (°▼-9.0pp (2/14) net-14/med-1.8) |
| overlap | (°·+1.2pp (3/11) net+21/med+3.5) | (°▼-33.8pp (0/1) net+1/med+1.0) |
| ny_only | ▲+4.3pp (8/55) net-487/med-2.5 | (°▼-11.0pp (0/8) net-5/med-1.0) |
| dead | ·+1.3pp (17/90) net+180/med+0.8 | (°▲+33.5pp (4/8) net+16/med+3.1) |
| asia | ▼-2.8pp (33/111) net+546/med+2.7 | ▲+8.5pp (20/40) net-59/med-1.4 |

- backtest payoff: right +3270 / wrong -2490 / net +781 pts; median per fire +1.50 (n=347)
- backtest best call: 2026-07-30 04:03 +155.1pts remaining (episode 178.3pts, major)
- backtest worst false alarm: 2026-07-24 06:52 -98.0pts adverse
- forward payoff: right +203 / wrong -263 / net -60 pts; median per fire -0.80 (n=71)
- forward best call: 2026-08-17 10:33 +37.0pts remaining (episode 42.7pts, major)
- forward worst false alarm: 2026-08-18 12:00 -25.5pts adverse
- earliness (backtest): median 27.5 pts of move remaining at fire (n=39)

## H3
*Repeated absorption — high effort with no result — at a price level precedes a breakout through that level.*
Grading: directional. Latest review: keep-watching (recommendation).

**H3** — session × window grid (cells as in the matrix):

| session | backtest | forward |
|---|---|---|
| whole | — | (°▲+23.4pp (2/4) net+8/med+0.3) |
| london | — | (°▲+26.7pp (1/2) net+8/med+3.8) |
| overlap | — | — |
| ny_only | — | (°▼-11.0pp (0/1) net+1/med+0.8) |
| dead | — | (°▲+83.5pp (1/1) net-0/med-0.2) |
| asia | — | — |

- forward payoff: right +13 / wrong -5 / net +8 pts; median per fire +0.30 (n=4)
- forward best call: 2026-08-18 18:23 +13.0pts remaining (episode 10.0pts)
- forward worst false alarm: 2026-08-18 08:40 -12.5pts adverse

## H4
*In an established trend, a quiet (low-volume) pullback resolves with trend resumption.*
Grading: directional. Latest review: keep-watching (recommendation).

**H4** — session × window grid (cells as in the matrix):

| session | backtest | forward |
|---|---|---|
| whole | (°▼-23.6pp (0/7) net+14/med+0.5) | — |
| london | (°▼-24.9pp (0/1) net+6/med+5.5) | — |
| overlap | — | — |
| ny_only | (°▼-10.2pp (0/6) net+8/med-0.1) | — |
| dead | — | — |
| asia | — | — |

- backtest payoff: right +27 / wrong -13 / net +14 pts; median per fire +0.50 (n=7)
- backtest best call: 2026-07-28 16:11 +11.3pts remaining (episode 28.8pts)
- backtest worst false alarm: 2026-07-28 16:11 -17.5pts adverse
- earliness (backtest): median 11.3 pts of move remaining at fire (n=1)

## H5 — disabled
*A buying climax that extends far above its trend mean mean-reverts (climax-extension fade; registered short-side only).*
Latest review: pending-on-operator. See the register entry for what is missing.

## H6 — definition-pending
*A wide-spread rejection bar at a session extreme (measured day-relative, volume-agnostic) reverses away from the extreme.*
Latest review: pending-on-operator. See the register entry for what is missing.

## H7
*Quiet decline at a session extreme is disguised accumulation: effortless (low-volume) weakness reverses UP once selling fails to attract participation (mirror: quiet advance at a high reverses down).*
Grading: directional + either-direction (dual). Latest review: keep-watching (recommendation).

**H7** — session × window grid (cells as in the matrix):

| session | backtest | forward |
|---|---|---|
| whole | ▲+7.6pp (35/112) net+7/med+2.8 | ▼-12.3pp (3/21) net-32/med+0.0 |
| london | ▲+4.4pp (12/41) net-217/med+2.7 | (°▼-5.1pp (2/11) net-60/med-8.5) |
| overlap | ▲+13.0pp (9/23) net+227/med+8.7 | (°▼-33.8pp (0/1) net+5/med+5.3) |
| ny_only | (°▲+4.1pp (2/14) net-24/med+0.0) | (°▼-11.0pp (0/6) net+17/med+3.9) |
| dead | (°▲+2.4pp (1/5) net+60/med+3.5) | (°▼-16.5pp (0/1) net+0/med+0.0) |
| asia | ▲+5.4pp (11/29) net-38/med+0.7 | (°▲+8.5pp (1/2) net+6/med+3.0) |

- backtest payoff: right +1097 / wrong -1090 / net +7 pts; median per fire +2.80 (n=112)
- backtest best call: 2026-07-24 11:09 +98.2pts remaining (episode 98.2pts, major)
- backtest worst false alarm: 2026-07-30 06:55 -94.0pts adverse
- forward payoff: right +74 / wrong -106 / net -32 pts; median per fire +0.00 (n=21)
- forward best call: 2026-08-18 19:09 +7.5pts remaining (episode 10.0pts)
- forward worst false alarm: 2026-08-17 11:49 -29.5pts adverse
- earliness (backtest): median 22.6 pts of move remaining at fire (n=30)

**H7 (either-dir)** — session × window grid (cells as in the matrix):

| session | backtest | forward |
|---|---|---|
| whole | ▲+9.3pp (60/112) | ▼-9.1pp (8/21) |
| london | ▲+4.1pp (21/41) | (°▲+12.1pp (6/11)) |
| overlap | ▲+9.7pp (14/23) | (°▼-67.5pp (0/1)) |
| ny_only | (°▲+8.6pp (4/14)) | (°▼-22.0pp (0/6)) |
| dead | (°▼-12.8pp (1/5)) | (°▼-33.1pp (0/1)) |
| asia | ▲+9.4pp (20/29) | (°▲+31.8pp (2/2)) |

- backtest payoff: n/a by construction (either-direction)
- backtest best call: 2026-07-24 11:09 +98.2pts remaining (episode 98.2pts, major)
- backtest worst false alarm: 2026-07-23 16:44 -25.7pts adverse
- forward payoff: n/a by construction (either-direction)
- forward best call: 2026-08-18 12:26 +29.5pts remaining (episode 43.5pts, major)
- forward worst false alarm: 2026-08-19 08:28 -12.7pts adverse
- earliness (backtest): median 15.3 pts of move remaining at fire (n=41)

## H8
*Reversal-signature bar anatomy (upthrust/spring) predicts imminent range expansion irrespective of direction.*
Grading: either-direction. Latest review: keep-watching (recommendation).

**H8** — session × window grid (cells as in the matrix):

| session | backtest | forward |
|---|---|---|
| whole | ▲+2.1pp (161/347) | ▲+2.1pp (35/71) |
| london | ▲+6.7pp (43/80) | (°▼-21.0pp (3/14)) |
| overlap | (°▲+12.4pp (7/11)) | (°▼-67.5pp (0/1)) |
| ny_only | ▲+23.6pp (24/55) | (°▼-9.5pp (1/8)) |
| dead | ·+1.6pp (31/90) | (°▲+29.4pp (5/8)) |
| asia | ▼-9.1pp (56/111) | ▼-3.2pp (26/40) |

- backtest payoff: n/a by construction (either-direction)
- backtest best call: 2026-07-30 04:03 +155.1pts remaining (episode 178.3pts, major)
- backtest worst false alarm: 2026-07-30 11:13 -30.5pts adverse
- forward payoff: n/a by construction (either-direction)
- forward best call: 2026-08-18 10:57 +56.0pts remaining (episode 50.0pts, major)
- forward worst false alarm: 2026-08-19 07:26 -14.0pts adverse
- earliness (backtest): median 26.9 pts of move remaining at fire (n=58)

## H9
*Persistent lower-TF directional pressure that recruits expanding participation at the parent timeframe precedes continuation beyond what the parent label alone predicts; pressure without participation expansion does not.*
Grading: directional. Latest review: keep-watching (recommendation).

**H9** — session × window grid (cells as in the matrix):

| session | backtest | forward |
|---|---|---|
| whole | ▲+3.7pp (15/55) net+319/med+3.5 | (°▼-18.3pp (1/12) net-18/med-3.1) |
| london | (°▲+20.6pp (5/11) net+108/med+12.5) | — |
| overlap | — | (°▼-33.8pp (0/1) net-1/med-1.0) |
| ny_only | (°▲+14.8pp (3/12) net+115/med+2.8) | (°▲+22.3pp (1/3) net+11/med+6.8) |
| dead | (°▼-8.5pp (1/11) net+11/med+1.0) | — |
| asia | ▼-3.9pp (6/21) net+86/med+6.8 | (°▼-41.5pp (0/8) net-28/med-3.1) |

- backtest payoff: right +558 / wrong -239 / net +319 pts; median per fire +3.50 (n=53)
- backtest best call: 2026-08-03 03:40 +73.2pts remaining (episode 81.3pts, major)
- backtest worst false alarm: 2026-07-30 09:15 -59.3pts adverse
- forward payoff: right +24 / wrong -42 / net -18 pts; median per fire -3.10 (n=12)
- forward best call: 2026-08-17 15:40 +16.3pts remaining (episode 18.3pts)
- forward worst false alarm: 2026-08-14 16:30 -13.2pts adverse
- earliness (backtest): median 15.0 pts of move remaining at fire (n=11)

## H10
*In an established 1-minute trend, no-demand/no-supply prints in the trend's direction signal continuation.*
Grading: directional. Latest review: deprioritize (recommendation).

**H10** — session × window grid (cells as in the matrix):

| session | backtest | forward |
|---|---|---|
| whole | ▼-4.8pp (55/293) net-240/med-1.4 | ▼-18.7pp (6/76) net-220/med-3.5 |
| london | ▲+2.4pp (18/66) net-62/med+1.9 | (°▼-13.3pp (1/10) net+27/med+4.8) |
| overlap | (°▼-26.1pp (0/7) net+27/med+6.8) | (°▼-33.8pp (0/5) net-75/med-15.8) |
| ny_only | ·-0.6pp (8/83) net+51/med-1.5 | (°▼-5.7pp (1/19) net-14/med-1.0) |
| dead | ▼-3.7pp (5/36) net-110/med-2.5 | (°▼-16.5pp (0/15) net-24/med-2.0) |
| asia | ▼-8.7pp (24/101) net-147/med-1.5 | ▼-26.7pp (4/27) net-135/med-4.8 |

- backtest payoff: right +1533 / wrong -1773 / net -240 pts; median per fire -1.40 (n=293)
- backtest best call: 2026-07-23 10:20 +90.0pts remaining (episode 104.8pts, major)
- backtest worst false alarm: 2026-07-28 13:10 -62.5pts adverse
- forward payoff: right +115 / wrong -335 / net -220 pts; median per fire -3.45 (n=76)
- forward best call: 2026-08-14 16:54 +22.5pts remaining (episode 16.8pts)
- forward worst false alarm: 2026-08-17 14:08 -24.2pts adverse
- earliness (backtest): median 19.4 pts of move remaining at fire (n=26)

---

Appendix: the per-session detail beyond London and every horizon-mark payoff live in signal_scoreboard.json (generated, same run).