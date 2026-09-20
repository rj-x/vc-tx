# Hypothesis Performance — Per-Instrument

Terms: [docs/GLOSSARY.md](../../docs/GLOSSARY.md).

Engine `8effbb323` — register 40 fence as amended 2026-08-19 (operator): one section per instrument, each computed only from that instrument's own store and native calendar; uk100 canonical, ger40/nas100/us30 PROVISIONAL (validation pending). Numbers are NEVER pooled across instruments — cross-instrument aggregation is a future registration. This first cross-instrument read is EXPLORATORY: expectations deliberately unregistered; anything interesting becomes a pre-registered question before it becomes a claim.

---

# uk100 (uk100fut) — CANONICAL

Store span (1M, close ts): 2026-07-12 22:06:00+00:00 → 2026-09-16 16:06:00+00:00. Volume type: real futures volume (step-zero audit).

## Summary Matrix (page 1)

Engine `8effbb323` — OBSERVATIONAL signal scoreboard - move-detection, not trading; no fills exist here by construction; never validation (docs/hypothesis_lifecycle.md stage 4)

**Review labels are RECOMMENDATIONS — none actioned, review pending operator familiarity.** Cells: marker + precision LIFT vs that context's OWN chance rate, (hits/fires), payoff net/median points (directional rows; either-direction rows have no payoff by construction). ▲/▼ = beyond ±2pp of chance, · = within. (°…) = small-n (fires<20 or episodes<10): dimmed, excluded from any future label arithmetic. Read READING_GUIDE.md first; full detail in hypothesis_performance.json.

| H | label | backtest whole | backtest london | forward whole | forward london |
|---|---|---|---|---|---|
| *context* | | 178 ep; chance 23.6%dir/44.3%either | 52 ep; chance 24.8%dir/47.1%either | 220 ep; chance 25.5%dir/46.0%either | 59 ep; chance 28.9%dir/53.6%either |
| S0-H1 | keep-watching | ▲i+8.0pp (22/69) · p-0.4pp cap39.0 net+194/med+2.8 | ▲i+5.5pp (7/22) · p+7.0pp cap38.8 net+133/med+3.0 | ▲i+2.8pp (49/203) · p-1.4pp cap18.5 net+52/med+0.2 | ▲i+7.4pp (18/62) · p-3.1pp cap24.9 net-52/med-0.8 |
| S1-H1 | keep-watching | (°▼i-3.9pp (1/5) · p-3.6pp cap59.3 net+9/med+3.0) | — | (°▲i+7.3pp (4/14) · p-11.2pp cap25.8 net-39/med-2.3) | (°▲i+15.9pp (3/8) · p-3.9pp cap25.8 net-26/med-7.2) |
| S0-H2 | promote-candidate | ·i-0.3pp (82/347) · p+1.2pp cap34.8 net+781/med+1.5 | ▼i-3.8pp (18/80) · p+6.4pp cap40.0 net+521/med+9.2 | ▼i-2.1pp (141/733) · p-2.3pp cap21.4 net+427/med-0.1 | ▼i-5.8pp (32/203) · p+3.6pp cap30.3 net+758/med+4.5 |
| S1-H2 | promote-candidate | ·i+0.3pp (61/252) · p+0.6pp cap34.2 net+540/med+0.9 | ·i+0.8pp (16/59) · p+5.7pp cap39.0 net+559/med+12.0 | ·i-1.0pp (112/553) · p+0.0pp cap20.8 net+493/med+0.4 | ·i-1.7pp (29/146) · p+6.0pp cap30.7 net+628/med+5.2 |
| S0-H3 | keep-watching | — | — | ▲i+7.3pp (6/21) · p+7.8pp cap10.2 net-15/med+0.8 | (°▲i+28.4pp (3/6) · p+4.4pp cap23.4 net-16/med+2.2) |
| S0-H4 | keep-watching | (°▲i+19.0pp (3/7) · p-23.6pp cap— net+14/med+0.5) | (°▼i-26.3pp (0/1) · p-24.8pp cap— net+6/med+5.5) | — | — |
| S0-H5 | keep-watching | — | — | — | — |
| S0-H6 | keep-watching | ·i-1.0pp (8/59) · p+8.2pp cap33.8 [cls 37.6%/14.6%i] net+391/med+5.7 | ·i+0.0pp (4/31) · p+20.7pp cap32.9 [cls 37.4%/12.9%i] net+282/med+16.0 | ▲i+4.3pp (19/134) · p+9.6pp cap27.0 [cls 44.9%/9.9%i] net+534/med+5.8 | ▲i+4.8pp (12/78) · p+11.2pp cap24.4 [cls 42.6%/10.6%i] net+124/med+5.2 |
| S0-H7 | keep-watching | ▲i+5.6pp (33/112) · p+7.6pp cap30.8 net+7/med+2.8 | ▲i+7.8pp (14/41) · p+4.5pp cap29.7 net-217/med+2.7 | ·i+0.9pp (39/176) · p+2.9pp cap20.0 net+278/med+1.8 | ▼i-8.3pp (8/60) · p+7.8pp cap22.8 net+25/med+1.1 |
| S0-H7 (either-dir) | keep-watching | ▼i-2.8pp (45/112) · p+9.3pp cap17.5 | ·i-0.8pp (19/41) · p+4.1pp cap21.5 | ·i-1.9pp (65/176) · p+0.6pp cap14.6 | ▼i-6.9pp (19/60) · p+6.4pp cap18.5 |
| S0-H8 | keep-watching | ▼i-3.2pp (138/347) · p+2.4pp cap16.2 | ▼i-15.9pp (25/80) · p+6.7pp cap34.5 | ▼i-4.3pp (253/733) · p-1.3pp cap9.1 | ▼i-6.1pp (66/203) · p+5.0pp cap21.0 |
| S0-H9 | keep-watching | ▲i+5.2pp (16/55) · p+5.5pp cap31.9 net+319/med+3.5 | (°▼i-17.2pp (1/11) · p+20.7pp cap45.0 net+108/med+12.5) | ▼i-2.3pp (15/79) · p-7.8pp cap22.1 net-181/med-3.1 | (°▲i+3.4pp (4/16) · p-22.7pp cap22.2 net-300/med-16.1) |
| S1-H9 | keep-watching | (°▼i-13.4pp (2/19) · p+23.8pp cap45.0 net+263/med+12.8) | (°▼i-26.3pp (0/8) · p+25.2pp cap57.1 net+148/med+17.8) | ▼i-13.6pp (3/39) · p-12.7pp cap14.1 net-253/med-3.5 | (°▼i-9.1pp (1/8) · p-16.4pp cap22.2 net-224/med-27.8) |
| S0-H10 | deprioritize | ▼i-8.9pp (44/293) · p-4.5pp cap27.1 net-240/med-1.4 | ▼i-12.7pp (9/66) · p+2.5pp cap33.2 net-62/med+1.9 | ▲i+5.1pp (108/409) · p-11.1pp cap14.8 net-926/med-1.9 | ▲i+10.4pp (31/97) · p-2.1pp cap23.2 net+113/med-0.3 |
| S0-H11 | keep-watching | ·i+0.8pp (78/316) · p+2.7pp cap32.2 net-647/med-2.4 | ▲i+2.1pp (42/148) · p-1.2pp cap35.0 net+250/med-0.6 | ▼i-8.6pp (41/323) · p+4.2pp cap20.5 net+216/med+1.5 | ▼i-7.9pp (22/161) · p-3.4pp cap27.8 net-135/med-1.0 |
| S1-H11 | keep-watching | ▼i-5.2pp (29/155) · p-1.0pp cap33.0 net-617/med-0.7 | ▼i-2.0pp (9/37) · p-8.6pp cap34.0 net-466/med-15.7 | ▼i-6.3pp (62/412) · p+2.4pp cap21.2 net-188/med-0.1 | ▼i-7.1pp (24/165) · p+8.1pp cap22.2 net-69/med-1.5 |
| S0-H12 | keep-watching | — | — | — | — |
| S0-H13 | keep-watching | (°▲i+26.1pp (1/2) · p+26.4pp cap37.0 net+28/med+13.8) | (°▲i+23.7pp (1/2) · p+25.2pp cap37.0 net+28/med+13.8) | (°▼i-4.6pp (3/18) · p-8.8pp cap39.0 net-70/med-0.8) | (°▲i+28.4pp (3/6) · p+4.4pp cap39.2 net-32/med-5.4) |
| S0-H14 | keep-watching | ▼i-8.6pp (45/294) · p-9.0pp cap24.8 net-695/med-1.9 | ▼i-10.2pp (10/62) · p-5.4pp cap28.1 net-81/med+3.1 | ▲i+6.7pp (118/421) · p-11.0pp cap15.1 net-938/med-2.2 | ▲i+16.9pp (35/91) · p-4.7pp cap23.2 net+86/med-1.7 |
| S0-H15 | keep-watching | — | — | — | — |
| S0-H16 | keep-watching | (°▼i-3.9pp (3/15) · p+3.1pp cap33.4 net+5/med+6.0) | — | ▼i-7.7pp (3/22) · p-16.4pp cap36.6 net+39/med+2.4 | — |
| S0-H17 | rows | ▲i+10.2pp (14/41) · p-6.5pp cap41.5 net+76/med+2.5 | (°▲i+9.4pp (5/14) · p+3.8pp cap40.0 net+32/med+4.4) | ▲i+2.2pp (28/119) · p+1.4pp cap23.4 net+151/med-0.2 | ▲i+9.0pp (11/36) · p+7.2pp cap29.0 net+94/med+3.2 |
| S0-H18 | rows | ▼i-4.2pp (12/61) · p+4.3pp cap34.0 net+169/med-1.0 | ▼i-14.3pp (3/25) · p+11.2pp cap45.5 net+266/med+1.3 | ▼i-11.6pp (7/72) · p+6.4pp cap17.1 net+50/med+1.4 | ▼i-7.7pp (5/36) · p-6.7pp cap22.2 net-54/med-1.8 |
| S0-H19 | rows | ▼i-5.1pp (40/213) · p-2.0pp cap34.1 net-631/med-1.5 | ▼i-12.7pp (6/44) · p-13.4pp cap55.5 net-334/med-11.0 | ▼i-4.0pp (67/388) · p-0.5pp cap17.0 net-428/med-0.1 | ▼i-3.5pp (21/116) · p-5.6pp cap32.0 net-743/med-5.5 |
| S0-H20 | rows | ▼i-10.6pp (2/50) · p-7.6pp cap62.0 [cls 37.6%/14.6%i] net-221/med-9.7 | ▼i-12.9pp (0/28) · p+1.9pp cap75.5 [cls 37.4%/12.9%i] net+241/med-5.2 | ▼i-6.0pp (4/102) · p-6.7pp cap18.5 [cls 44.9%/9.9%i] net-741/med-6.8 | ▼i-4.6pp (4/67) · p-6.8pp cap24.0 [cls 42.6%/10.6%i] net-395/med-9.5 |
| **union coverage** | | 60.7% (108/178) | 59.6% (31/52) | 82.3% (181/220) | 83.1% (49/59) |

### Dual-convention side-by-side — load-bearing patterns

| pattern | context | initiation | participation (cap) |
|---|---|---|---|
| Q1-H1 away cells (S0-H1) | uk100fut/forward | 24.1% (49/203) | 24.1% (cap 18.5) |
| Q1-H1 away cells (S0-H1) | ger40fut/forward | 22.2% (48/216) | 25.9% (cap 44.9) |
| Q1-H1 away cells (S0-H1) | nas100fut/forward | 26.8% (38/142) | 33.1% (cap 82.1) |
| Q1-H1 away cells (S0-H1) | us30fut/forward | 25.7% (79/307) | 27.0% (cap 68.5) |
| H2 forward (S0-H2) | uk100fut/forward | 19.2% (141/733) | 23.2% (cap 21.4) |
| H2 forward (S0-H2) | ger40fut/forward | 20.1% (158/787) | 22.6% (cap 44.4) |
| H2 forward (S0-H2) | nas100fut/forward | 17.2% (112/650) | 30.9% (cap 83.2) |
| H2 forward (S0-H2) | us30fut/forward | 16.3% (146/896) | 28.3% (cap 80.5) |
| H2 forward (S1-H2) | uk100fut/forward | 20.3% (112/553) | 25.5% (cap 20.8) |
| H2 forward (S1-H2) | ger40fut/forward | 23.0% (129/561) | 21.4% (cap 43.4) |
| H2 forward (S1-H2) | nas100fut/forward | 19.5% (89/457) | 30.0% (cap 85.5) |
| H2 forward (S1-H2) | us30fut/forward | 18.8% (117/624) | 26.6% (cap 77.8) |
| S0-H8 (either-dir) | uk100fut/backtest | 39.8% (138/347) | 46.7% (cap 16.2) |
| S0-H8 (either-dir) | ger40fut/backtest | 28.6% (67/234) | 53.4% (cap 36.4) |
| S0-H8 (either-dir) | nas100fut/backtest | 36.6% (117/320) | 43.4% (cap 64.9) |
| S0-H8 (either-dir) | us30fut/backtest | 26.7% (75/281) | 52.7% (cap 75.2) |
| S0-H6 (conditioned) | uk100fut/backtest | 13.6% (8/59) | 45.8% (cap 33.8) |
| S0-H6 (conditioned) | ger40fut/backtest | 2.8% (1/36) | 41.7% (cap 56.7) |
| S0-H6 (conditioned) | nas100fut/backtest | 17.2% (5/29) | 31.0% (cap 260.8) |
| S0-H6 (conditioned) | us30fut/backtest | 5.8% (3/52) | 19.2% (cap 175.0) |
| S0-H8 (either-dir) | uk100fut/forward | 34.5% (253/733) | 44.7% (cap 9.1) |
| S0-H8 (either-dir) | ger40fut/forward | 42.8% (337/787) | 41.8% (cap 23.5) |
| S0-H8 (either-dir) | nas100fut/forward | 39.4% (256/650) | 52.0% (cap 58.5) |
| S0-H8 (either-dir) | us30fut/forward | 35.6% (319/896) | 50.4% (cap 46.2) |
| S0-H6 (conditioned) | uk100fut/forward | 14.2% (19/134) | 54.5% (cap 27.0) |
| S0-H6 (conditioned) | ger40fut/forward | 18.2% (35/192) | 41.7% (cap 55.1) |
| S0-H6 (conditioned) | nas100fut/forward | 20.1% (31/154) | 43.5% (cap 103.0) |
| S0-H6 (conditioned) | us30fut/forward | 24.9% (46/185) | 36.2% (cap 95.0) |


Not graded:  — see register entries.

## Hypothesis Cards (page 2)

### H1 — 2 signals
*A climactic bar — extreme volume on a wide spread late in an extended move — marks exhaustion, and price then reverses against the climax direction.*
Grading: directional. Latest review: keep-watching (recommendation).

- Question **Q1-H1**: see the register entry (status there is authoritative).
**S0-H1** — session × window grid (cells as in the matrix):

| session | backtest | forward |
|---|---|---|
| whole | ▲i+8.0pp (22/69) · p-0.4pp cap39.0 net+194/med+2.8 | ▲i+2.8pp (49/203) · p-1.4pp cap18.5 net+52/med+0.2 |
| london | ▲i+5.5pp (7/22) · p+7.0pp cap38.8 net+133/med+3.0 | ▲i+7.4pp (18/62) · p-3.1pp cap24.9 net-52/med-0.8 |
| overlap | (°▼i-16.4pp (0/2) · p+23.9pp cap27.5 net+35/med+17.7) | (°▼i-12.8pp (0/12) · p-14.8pp cap34.5 net-94/med-9.3) |
| ny_only | ▲i+19.6pp (9/22) · p+8.0pp cap46.9 net+17/med+1.6 | ▼i-2.8pp (9/50) · p-1.6pp cap11.0 net+12/med+0.2 |
| dead | (°▲i+2.6pp (4/12) · p+7.4pp cap15.3 net+30/med+1.1) | ▲i+17.8pp (14/28) · p+18.9pp cap11.9 net+76/med+2.2 |
| asia | (°▼i-4.6pp (2/11) · p-23.6pp cap59.3 net-22/med-2.6) | ▼i-4.8pp (8/51) · p+0.0pp cap18.0 net+109/med-0.6 |

- backtest payoff: right +639 / wrong -445 / net +194 pts; median per fire +2.75 (n=68)
- backtest best call: 2026-07-29 04:04 +105.2pts remaining (episode 102.8pts, major)
- backtest worst false alarm: 2026-07-23 12:17 -70.7pts adverse
- forward payoff: right +1106 / wrong -1054 / net +52 pts; median per fire +0.20 (n=203)
- forward best call: 2026-08-21 09:11 +74.0pts remaining (episode 95.0pts, major)
- forward worst false alarm: 2026-09-01 08:06 -91.5pts adverse
- earliness (backtest): median 35.3 pts of move remaining at fire (n=21)

**S1-H1** — session × window grid (cells as in the matrix):

| session | backtest | forward |
|---|---|---|
| whole | (°▼i-3.9pp (1/5) · p-3.6pp cap59.3 net+9/med+3.0) | (°▲i+7.3pp (4/14) · p-11.2pp cap25.8 net-39/med-2.3) |
| london | — | (°▲i+15.9pp (3/8) · p-3.9pp cap25.8 net-26/med-7.2) |
| overlap | — | (°▼i-12.8pp (0/2) · p-23.1pp cap— net-6/med-3.1) |
| ny_only | (°▼i-21.3pp (0/1) · p-10.2pp cap— net-13/med-13.3) | — |
| dead | (°▼i-30.7pp (0/1) · p-17.6pp cap— net+3/med+3.0) | (°▼i-32.2pp (0/3) · p-16.8pp cap— net-6/med-4.0) |
| asia | (°▲i+10.5pp (1/3) · p+0.6pp cap59.3 net+19/med+5.5) | (°▲i+79.5pp (1/1) · p-37.3pp cap— net-1/med-0.6) |

- backtest payoff: right +59 / wrong -50 / net +9 pts; median per fire +3.00 (n=5)
- backtest best call: 2026-07-29 04:04 +105.2pts remaining (episode 102.8pts, major)
- backtest worst false alarm: 2026-07-30 05:53 -37.6pts adverse
- forward payoff: right +68 / wrong -107 / net -39 pts; median per fire -2.30 (n=14)
- forward best call: 2026-09-01 08:42 +51.7pts remaining (episode 76.2pts)
- forward worst false alarm: 2026-08-20 15:03 -30.7pts adverse
- earliness (backtest): median 105.2 pts of move remaining at fire (n=1)

### H2 — 2 signals
*A failed probe beyond a prior extreme — an upthrust above or spring below that closes back inside — reverses against the probe.*
Grading: directional. Latest review: promote-candidate (recommendation).

**S0-H2** — session × window grid (cells as in the matrix):

| session | backtest | forward |
|---|---|---|
| whole | ·i-0.3pp (82/347) · p+1.2pp cap34.8 net+781/med+1.5 | ▼i-2.1pp (141/733) · p-2.3pp cap21.4 net+427/med-0.1 |
| london | ▼i-3.8pp (18/80) · p+6.4pp cap40.0 net+521/med+9.2 | ▼i-5.8pp (32/203) · p+3.6pp cap30.3 net+758/med+4.5 |
| overlap | (°▼i-7.3pp (1/11) · p+1.2pp cap39.0 net+21/med+3.5) | ▲i+9.1pp (7/32) · p-13.7pp cap30.2 net-88/med-0.3 |
| ny_only | ▼i-3.1pp (10/55) · p+4.3pp cap40.8 net-487/med-2.5 | ·i-0.6pp (33/163) · p-2.7pp cap21.5 net-37/med-0.7 |
| dead | ▼i-2.9pp (25/90) · p+1.3pp cap23.2 net+180/med+0.8 | ▼i-8.5pp (22/93) · p+3.6pp cap10.0 net-5/med-0.4 |
| asia | ▲i+2.4pp (28/111) · p-3.0pp cap29.8 net+546/med+2.7 | ·i-1.1pp (47/242) · p-6.7pp cap13.5 net-201/med-0.3 |

- backtest payoff: right +3270 / wrong -2490 / net +781 pts; median per fire +1.50 (n=347)
- backtest best call: 2026-07-30 04:03 +155.1pts remaining (episode 178.3pts, major)
- backtest worst false alarm: 2026-07-24 06:52 -98.0pts adverse
- forward payoff: right +4002 / wrong -3576 / net +427 pts; median per fire -0.05 (n=732)
- forward best call: 2026-09-09 02:43 +116.5pts remaining (episode 119.3pts, major)
- forward worst false alarm: 2026-09-01 08:00 -94.5pts adverse
- earliness (backtest): median 28.4 pts of move remaining at fire (n=38)

**S1-H2** — session × window grid (cells as in the matrix):

| session | backtest | forward |
|---|---|---|
| whole | ·i+0.3pp (61/252) · p+0.6pp cap34.2 net+540/med+0.9 | ·i-1.0pp (112/553) · p+0.0pp cap20.8 net+493/med+0.4 |
| london | ·i+0.8pp (16/59) · p+5.7pp cap39.0 net+559/med+12.0 | ·i-1.7pp (29/146) · p+6.0pp cap30.7 net+628/med+5.2 |
| overlap | (°▼i-7.3pp (1/11) · p+1.2pp cap39.0 net+21/med+3.5) | ▲i+3.2pp (4/25) · p-11.1pp cap30.2 net-80/med+1.0 |
| ny_only | ·i-1.3pp (8/40) · p+4.8pp cap38.6 net-304/med-2.1 | ·i+0.1pp (24/115) · p-1.5pp cap18.8 net+38/med-0.5 |
| dead | ▼i-6.1pp (15/61) · p+5.4pp cap23.0 net+201/med+0.8 | ▼i-15.3pp (12/71) · p+8.6pp cap10.7 net+55/med+0.2 |
| asia | ▲i+3.1pp (21/81) · p-8.0pp cap28.4 net+62/med-1.2 | ·i+1.4pp (43/196) · p-5.7pp cap13.1 net-148/med-0.3 |

- backtest payoff: right +2121 / wrong -1581 / net +540 pts; median per fire +0.95 (n=252)
- backtest best call: 2026-07-30 04:03 +155.1pts remaining (episode 178.3pts, major)
- backtest worst false alarm: 2026-07-29 19:00 -94.0pts adverse
- forward payoff: right +3072 / wrong -2579 / net +493 pts; median per fire +0.40 (n=553)
- forward best call: 2026-09-09 02:43 +116.5pts remaining (episode 119.3pts, major)
- forward worst false alarm: 2026-09-01 08:00 -94.5pts adverse
- earliness (backtest): median 31.3 pts of move remaining at fire (n=35)

### H3 — 1 signal
*Repeated absorption — high effort with no result — at a price level precedes a breakout through that level.*
Grading: directional. Latest review: keep-watching (recommendation).

**S0-H3** — session × window grid (cells as in the matrix):

| session | backtest | forward |
|---|---|---|
| whole | — | ▲i+7.3pp (6/21) · p+7.8pp cap10.2 net-15/med+0.8 |
| london | — | (°▲i+28.4pp (3/6) · p+4.4pp cap23.4 net-16/med+2.2) |
| overlap | — | — |
| ny_only | — | (°▼i-4.1pp (1/6) · p-7.6pp cap— net+11/med+2.2) |
| dead | — | (°▲i+17.8pp (1/2) · p+33.2pp cap7.1 net-5/med-2.5) |
| asia | — | (°▼i-6.2pp (1/7) · p+19.8pp cap8.6 net-6/med-2.2) |

- forward payoff: right +66 / wrong -81 / net -15 pts; median per fire +0.80 (n=21)
- forward best call: 2026-08-20 11:13 +45.0pts remaining (episode 70.0pts, major)
- forward worst false alarm: 2026-08-20 11:13 -39.0pts adverse

### H4 — 1 signal
*In an established trend, a quiet (low-volume) pullback resolves with trend resumption.*
Grading: directional. Latest review: keep-watching (recommendation).

**S0-H4** — session × window grid (cells as in the matrix):

| session | backtest | forward |
|---|---|---|
| whole | (°▲i+19.0pp (3/7) · p-23.6pp cap— net+14/med+0.5) | — |
| london | (°▼i-26.3pp (0/1) · p-24.8pp cap— net+6/med+5.5) | — |
| overlap | — | — |
| ny_only | (°▲i+28.7pp (3/6) · p-10.2pp cap— net+8/med-0.1) | — |
| dead | — | — |
| asia | — | — |

- backtest payoff: right +27 / wrong -13 / net +14 pts; median per fire +0.50 (n=7)
- backtest best call: 2026-07-28 16:11 +11.3pts remaining (episode 28.8pts)
- backtest worst false alarm: 2026-07-28 16:11 -17.5pts adverse
- earliness (backtest): median 11.3 pts of move remaining at fire (n=1)

### H5 — 1 signal
*A buying climax that extends far above its trend mean mean-reverts (climax-extension fade; registered short-side only).*
Grading: directional. Latest review: keep-watching (recommendation).

**S0-H5** — session × window grid (cells as in the matrix):

| session | backtest | forward |
|---|---|---|
| whole | — | — |
| london | — | — |
| overlap | — | — |
| ny_only | — | — |
| dead | — | — |
| asia | — | — |


### H6 — 1 signal
*A wide-spread rejection bar at a session extreme (measured day-relative, volume-agnostic) reverses away from the extreme.*
Grading: directional. Latest review: keep-watching (recommendation).

- Question **Q1-H6**: see the register entry (status there is authoritative).
- Question **Q2-H6**: see the register entry (status there is authoritative).
- Question **Q3-H6**: see the register entry (status there is authoritative).
**S0-H6** — session × window grid (cells as in the matrix):

| session | backtest | forward |
|---|---|---|
| whole | ·i-1.0pp (8/59) · p+8.2pp cap33.8 [cls 37.6%/14.6%i] net+391/med+5.7 | ▲i+4.3pp (19/134) · p+9.6pp cap27.0 [cls 44.9%/9.9%i] net+534/med+5.8 |
| london | ·i+0.0pp (4/31) · p+20.7pp cap32.9 [cls 37.4%/12.9%i] net+282/med+16.0 | ▲i+4.8pp (12/78) · p+11.2pp cap24.4 [cls 42.6%/10.6%i] net+124/med+5.2 |
| overlap | (°▲i+32.5pp (3/6) · p-30.8pp cap— [cls 30.8%/17.5%i] net-87/med-15.4) | (°▲i+4.4pp (3/18) · p-4.0pp cap30.7 [cls 31.8%/12.3%i] net+8/med+4.5) |
| ny_only | (°▲i+10.6pp (1/4) · p-20.5pp cap— [cls 20.5%/14.4%i] net+0/med+6.5) | (°▲i+26.7pp (1/3) · p-7.3pp cap— [cls 7.3%/6.6%i] net-1/med-1.0) |
| dead | (°▼i-9.6pp (0/5) · p-19.1pp cap— [cls 19.1%/9.6%i] net-25/med-6.4) | — |
| asia | (°▼i-16.2pp (0/13) · p+24.5pp cap44.8 [cls 44.7%/16.2%i] net+220/med+5.7) | ·i+0.0pp (3/35) · p+16.7pp cap29.0 [cls 57.6%/8.6%i] net+403/med+7.8 |

- backtest payoff: right +818 / wrong -428 / net +391 pts; median per fire +5.70 (n=59)
- backtest best call: 2026-07-31 08:00 +72.8pts remaining (episode 70.3pts, major)
- backtest worst false alarm: 2026-07-22 08:07 -80.3pts adverse
- forward payoff: right +1498 / wrong -964 / net +534 pts; median per fire +5.75 (n=134)
- forward best call: 2026-08-26 13:22 +40.8pts remaining (episode 52.0pts, major)
- forward worst false alarm: 2026-09-01 08:00 -94.5pts adverse
- earliness (backtest): median 21.6 pts of move remaining at fire (n=8)

### H7 — 1 signal
*Quiet decline at a session extreme is disguised accumulation: effortless (low-volume) weakness reverses UP once selling fails to attract participation (mirror: quiet advance at a high reverses down).*
Grading: directional + either-direction (dual). Latest review: keep-watching (recommendation).

- Question **Q1-H7**: see the register entry (status there is authoritative).
**S0-H7** — session × window grid (cells as in the matrix):

| session | backtest | forward |
|---|---|---|
| whole | ▲i+5.6pp (33/112) · p+7.6pp cap30.8 net+7/med+2.8 | ·i+0.9pp (39/176) · p+2.9pp cap20.0 net+278/med+1.8 |
| london | ▲i+7.8pp (14/41) · p+4.5pp cap29.7 net-217/med+2.7 | ▼i-8.3pp (8/60) · p+7.8pp cap22.8 net+25/med+1.1 |
| overlap | ▼i-3.4pp (3/23) · p+13.0pp cap38.8 net+227/med+8.7 | ▲i+4.6pp (4/23) · p-1.4pp cap29.0 net+69/med+5.3 |
| ny_only | (°·i+0.1pp (3/14) · p+4.1pp cap27.6 net-24/med+0.0) | ▲i+8.8pp (8/27) · p-7.6pp cap— net-16/med+0.7 |
| dead | (°▲i+49.3pp (4/5) · p+2.4pp cap51.1 net+60/med+3.5) | (°▲i+17.8pp (4/8) · p-4.3pp cap13.6 net-11/med-2.2) |
| asia | ▲i+8.2pp (9/29) · p+5.2pp cap20.7 net-38/med+0.7 | ▲i+5.4pp (15/58) · p+0.6pp cap16.1 net+211/med+2.8 |

- backtest payoff: right +1097 / wrong -1090 / net +7 pts; median per fire +2.80 (n=112)
- backtest best call: 2026-07-22 04:18 +132.7pts remaining (episode 138.3pts, major)
- backtest worst false alarm: 2026-07-30 06:55 -94.0pts adverse
- forward payoff: right +1059 / wrong -781 / net +278 pts; median per fire +1.75 (n=176)
- forward best call: 2026-09-01 03:37 +95.3pts remaining (episode 92.3pts, major)
- forward worst false alarm: 2026-09-03 10:40 -47.5pts adverse
- earliness (backtest): median 29.8 pts of move remaining at fire (n=29)

**S0-H7 (either-dir)** — session × window grid (cells as in the matrix):

| session | backtest | forward |
|---|---|---|
| whole | ▼i-2.8pp (45/112) · p+9.3pp cap17.5 | ·i-1.9pp (65/176) · p+0.6pp cap14.6 |
| london | ·i-0.8pp (19/41) · p+4.1pp cap21.5 | ▼i-6.9pp (19/60) · p+6.4pp cap18.5 |
| overlap | ·i+0.0pp (7/23) · p+9.7pp cap31.2 | ·i+0.5pp (6/23) · p-2.4pp cap20.9 |
| ny_only | (°▼i-16.4pp (3/14) · p+8.5pp cap13.4) | ▲i+10.7pp (13/27) · p-4.0pp cap0.8 |
| dead | (°▲i+27.3pp (4/5) · p-12.9pp cap51.1) | (°▲i+17.8pp (6/8) · p+4.6pp cap5.3) |
| asia | ·i-1.1pp (12/29) · p+9.3pp cap10.1 | ·i-1.6pp (21/58) · p-11.3pp cap12.6 |

- backtest payoff: n/a by construction (either-direction)
- backtest best call: 2026-07-22 04:18 +132.7pts remaining (episode 138.3pts, major)
- backtest worst false alarm: 2026-07-23 16:44 -25.7pts adverse
- forward payoff: n/a by construction (either-direction)
- forward best call: 2026-09-01 03:37 +95.3pts remaining (episode 92.3pts, major)
- forward worst false alarm: 2026-09-08 11:05 -26.2pts adverse
- earliness (backtest): median 16.8 pts of move remaining at fire (n=40)

### H8 — 1 signal
*Reversal-signature bar anatomy (upthrust/spring) predicts imminent range expansion irrespective of direction.*
Grading: either-direction. Latest review: keep-watching (recommendation).

**S0-H8** — session × window grid (cells as in the matrix):

| session | backtest | forward |
|---|---|---|
| whole | ▼i-3.2pp (138/347) · p+2.4pp cap16.2 | ▼i-4.3pp (253/733) · p-1.3pp cap9.1 |
| london | ▼i-15.9pp (25/80) · p+6.7pp cap34.5 | ▼i-6.1pp (66/203) · p+5.0pp cap21.0 |
| overlap | (°▼i-12.2pp (2/11) · p+12.4pp cap18.3) | ▲i+15.0pp (13/32) · p-17.8pp cap0.3 |
| ny_only | ▼i-5.1pp (18/55) · p+23.5pp cap6.9 | ▼i-3.0pp (56/163) · p-5.3pp cap7.4 |
| dead | ▼i-3.8pp (44/90) · p+1.5pp cap13.9 | ▼i-18.5pp (36/93) · p+8.0pp cap6.3 |
| asia | ·i+1.6pp (49/111) · p-8.3pp cap19.0 | ▼i-3.9pp (82/242) · p-2.7pp cap5.7 |

- backtest payoff: n/a by construction (either-direction)
- backtest best call: 2026-07-30 04:03 +155.1pts remaining (episode 178.3pts, major)
- backtest worst false alarm: 2026-07-30 11:13 -30.5pts adverse
- forward payoff: n/a by construction (either-direction)
- forward best call: 2026-09-09 02:43 +116.5pts remaining (episode 119.3pts, major)
- forward worst false alarm: 2026-09-01 11:17 -34.2pts adverse
- earliness (backtest): median 26.9 pts of move remaining at fire (n=58)

### H9 — 2 signals
*Persistent lower-TF directional pressure that recruits expanding participation at the parent timeframe precedes continuation beyond what the parent label alone predicts; pressure without participation expansion does not.*
Grading: directional. Latest review: keep-watching (recommendation).

- Question **Q2-H9**: see the register entry (status there is authoritative).
**S0-H9** — session × window grid (cells as in the matrix):

| session | backtest | forward |
|---|---|---|
| whole | ▲i+5.2pp (16/55) · p+5.5pp cap31.9 net+319/med+3.5 | ▼i-2.3pp (15/79) · p-7.8pp cap22.1 net-181/med-3.1 |
| london | (°▼i-17.2pp (1/11) · p+20.7pp cap45.0 net+108/med+12.5) | (°▲i+3.4pp (4/16) · p-22.7pp cap22.2 net-300/med-16.1) |
| overlap | — | (°▼i-12.8pp (0/8) · p+64.4pp cap31.7 net+193/med+27.2) |
| ny_only | (°▲i+20.4pp (5/12) · p+14.8pp cap69.9 net+115/med+2.8) | (°▼i-9.7pp (2/18) · p+9.1pp cap14.1 net-25/med-1.3) |
| dead | (°▼i-3.4pp (3/11) · p-8.5pp cap26.6 net+11/med+1.0) | (°▼i-3.6pp (2/7) · p-16.8pp cap— net+16/med+1.5) |
| asia | ▲i+10.5pp (7/21) · p+0.6pp cap13.5 net+86/med+6.8 | ▲i+2.8pp (7/30) · p-27.3pp cap15.4 net-66/med-3.4 |

- backtest payoff: right +558 / wrong -239 / net +319 pts; median per fire +3.50 (n=53)
- backtest best call: 2026-08-03 03:40 +73.2pts remaining (episode 81.3pts, major)
- backtest worst false alarm: 2026-07-30 09:15 -59.3pts adverse
- forward payoff: right +350 / wrong -531 / net -181 pts; median per fire -3.10 (n=77)
- forward best call: 2026-09-04 04:40 +46.6pts remaining (episode 47.0pts, major)
- forward worst false alarm: 2026-09-01 08:00 -94.5pts adverse
- earliness (backtest): median 15.6 pts of move remaining at fire (n=10)

**S1-H9** — session × window grid (cells as in the matrix):

| session | backtest | forward |
|---|---|---|
| whole | (°▼i-13.4pp (2/19) · p+23.8pp cap45.0 net+263/med+12.8) | ▼i-13.6pp (3/39) · p-12.7pp cap14.1 net-253/med-3.5 |
| london | (°▼i-26.3pp (0/8) · p+25.2pp cap57.1 net+148/med+17.8) | (°▼i-9.1pp (1/8) · p-16.4pp cap22.2 net-224/med-27.8) |
| overlap | — | (°▼i-12.8pp (0/1) · p-23.1pp cap— net-1/med-1.0) |
| ny_only | (°▼i-21.3pp (0/4) · p+64.8pp cap69.9 net+105/med+31.6) | (°▼i-20.8pp (0/10) · p+12.4pp cap14.1 net-26/med-4.7) |
| dead | (°▼i-10.7pp (1/5) · p+2.4pp cap26.6 net+6/med+2.3) | (°▼i-15.5pp (1/6) · p-16.8pp cap— net+22/med+5.5) |
| asia | (°▲i+27.2pp (1/2) · p+17.3pp cap20.2 net+4/med+2.1) | (°▼i-13.4pp (1/14) · p-23.0pp cap13.1 net-24/med-3.4) |

- backtest payoff: right +377 / wrong -114 / net +263 pts; median per fire +12.75 (n=18)
- backtest best call: 2026-07-19 23:10 +9.2pts remaining (episode 30.7pts)
- backtest worst false alarm: 2026-07-30 09:15 -59.3pts adverse
- forward payoff: right +86 / wrong -339 / net -253 pts; median per fire -3.50 (n=37)
- forward best call: 2026-09-09 11:45 +28.0pts remaining (episode 38.0pts)
- forward worst false alarm: 2026-09-01 08:00 -94.5pts adverse
- earliness (backtest): median 9.2 pts of move remaining at fire (n=1)

### H10 — 1 signal
*In an established 1-minute trend, no-demand/no-supply prints in the trend's direction signal continuation.*
Grading: directional. Latest review: deprioritize (recommendation).

**S0-H10** — session × window grid (cells as in the matrix):

| session | backtest | forward |
|---|---|---|
| whole | ▼i-8.9pp (44/293) · p-4.5pp cap27.1 net-240/med-1.4 | ▲i+5.1pp (108/409) · p-11.1pp cap14.8 net-926/med-1.9 |
| london | ▼i-12.7pp (9/66) · p+2.5pp cap33.2 net-62/med+1.9 | ▲i+10.4pp (31/97) · p-2.1pp cap23.2 net+113/med-0.3 |
| overlap | (°▼i-16.4pp (0/7) · p-26.1pp cap— net+27/med+6.8) | ▼i-8.6pp (1/24) · p-18.9pp cap19.5 net-268/med-12.6 |
| ny_only | ▼i-2.0pp (16/83) · p-0.6pp cap25.3 net+51/med-1.5 | ▲i+7.8pp (24/84) · p-2.8pp cap18.8 net-52/med-0.8 |
| dead | ·i-0.1pp (11/36) · p-3.7pp cap11.5 net-110/med-2.5 | ▼i-5.6pp (17/64) · p-13.7pp cap14.2 net-114/med-0.9 |
| asia | ▼i-14.9pp (8/101) · p-7.9pp cap27.0 net-147/med-1.5 | ▲i+4.5pp (35/140) · p-18.7pp cap9.8 net-605/med-3.0 |

- backtest payoff: right +1533 / wrong -1773 / net -240 pts; median per fire -1.40 (n=293)
- backtest best call: 2026-07-23 10:20 +90.0pts remaining (episode 104.8pts, major)
- backtest worst false alarm: 2026-07-28 13:10 -62.5pts adverse
- forward payoff: right +1144 / wrong -2070 / net -926 pts; median per fire -1.90 (n=407)
- forward best call: 2026-09-01 03:06 +83.9pts remaining (episode 92.3pts, major)
- forward worst false alarm: 2026-09-10 11:50 -47.5pts adverse
- earliness (backtest): median 21.6 pts of move remaining at fire (n=24)

### H11 — 2 signals
*Price entering a low-volume price zone traverses it faster than baseline; entering a high-volume node it stalls or reverses at above-baseline rates.*
Grading: directional. Latest review: keep-watching (recommendation).

- Question **Q1-H11**: see the register entry (status there is authoritative).
- Question **Q2-H11**: see the register entry (status there is authoritative).
**S0-H11** — session × window grid (cells as in the matrix):

| session | backtest | forward |
|---|---|---|
| whole | ·i+0.8pp (78/316) · p+2.7pp cap32.2 net-647/med-2.4 | ▼i-8.6pp (41/323) · p+4.2pp cap20.5 net+216/med+1.5 |
| london | ▲i+2.1pp (42/148) · p-1.2pp cap35.0 net+250/med-0.6 | ▼i-7.9pp (22/161) · p-3.4pp cap27.8 net-135/med-1.0 |
| overlap | ▲i+8.6pp (10/40) · p-18.6pp cap33.5 net-403/med-11.8 | ·i-1.9pp (5/46) · p+11.7pp cap21.8 net+198/med+9.4 |
| ny_only | ▼i-5.5pp (6/38) · p+18.7pp cap34.0 net-267/med-1.6 | ▼i-6.5pp (6/42) · p+9.1pp cap13.2 net+67/med+3.6 |
| dead | ▼i-15.7pp (3/20) · p+37.4pp cap18.5 net+59/med+0.7 | (°▼i-32.2pp (0/8) · p+8.2pp cap12.6 net+27/med+3.5) |
| asia | ·i+1.5pp (17/70) · p+0.2pp cap18.0 net-286/med-4.5 | ▼i-8.4pp (8/66) · p+8.2pp cap14.1 net+59/med+1.6 |

- backtest payoff: right +2555 / wrong -3203 / net -647 pts; median per fire -2.35 (n=316)
- backtest best call: 2026-07-22 04:01 +129.4pts remaining (episode 138.3pts, major)
- backtest worst false alarm: 2026-07-22 07:36 -96.5pts adverse
- forward payoff: right +2152 / wrong -1936 / net +216 pts; median per fire +1.50 (n=323)
- forward best call: 2026-09-01 03:56 +91.7pts remaining (episode 92.3pts, major)
- forward worst false alarm: 2026-09-01 08:00 -94.5pts adverse
- earliness (backtest): median 25.5 pts of move remaining at fire (n=25)

**S1-H11** — session × window grid (cells as in the matrix):

| session | backtest | forward |
|---|---|---|
| whole | ▼i-5.2pp (29/155) · p-1.0pp cap33.0 net-617/med-0.7 | ▼i-6.3pp (62/412) · p+2.4pp cap21.2 net-188/med-0.1 |
| london | ▼i-2.0pp (9/37) · p-8.6pp cap34.0 net-466/med-15.7 | ▼i-7.1pp (24/165) · p+8.1pp cap22.2 net-69/med-1.5 |
| overlap | ▼i-16.4pp (0/30) · p+3.9pp cap34.5 net+73/med-1.6 | ▼i-5.2pp (6/79) · p-9.2pp cap23.5 net+41/med+1.0 |
| ny_only | ▼i-7.0pp (6/42) · p+4.1pp cap20.6 net+75/med+0.7 | ▼i-3.8pp (9/53) · p-3.8pp cap15.2 net-111/med-3.5 |
| dead | (°▲i+44.3pp (3/4) · p-17.6pp cap— net-21/med-4.5) | (°▼i-16.4pp (3/19) · p+4.3pp cap14.6 net+28/med+1.2) |
| asia | ▲i+3.4pp (11/42) · p+0.6pp cap34.3 net-277/med-0.9 | ·i+0.3pp (20/96) · p+1.2pp cap11.7 net-77/med-0.6 |

- backtest payoff: right +1033 / wrong -1650 / net -617 pts; median per fire -0.70 (n=155)
- backtest best call: 2026-07-24 03:18 +96.3pts remaining (episode 104.3pts, major)
- backtest worst false alarm: 2026-07-31 07:01 -103.0pts adverse
- forward payoff: right +2495 / wrong -2683 / net -188 pts; median per fire -0.10 (n=412)
- forward best call: 2026-08-20 11:09 +45.0pts remaining (episode 70.0pts, major)
- forward worst false alarm: 2026-09-15 06:58 -73.3pts adverse
- earliness (backtest): median 18.4 pts of move remaining at fire (n=10)

### H12 — 1 signal
*A zone showing repeated visits with elevated volume, diminishing range-per-unit-volume, and drying pullback volume precedes a directional move away from the zone in the absorber's direction.*
Grading: directional. Latest review: keep-watching (recommendation).

**S0-H12** — session × window grid (cells as in the matrix):

| session | backtest | forward |
|---|---|---|
| whole | — | — |
| london | — | — |
| overlap | — | — |
| ny_only | — | — |
| dead | — | — |
| asia | — | — |


### H13 — 1 signal
*After price breaks out of the session value area on declining volume and reclaims it on expanding volume, it continues toward the far side of the value area.*
Grading: directional. Latest review: keep-watching (recommendation).

**S0-H13** — session × window grid (cells as in the matrix):

| session | backtest | forward |
|---|---|---|
| whole | (°▲i+26.1pp (1/2) · p+26.4pp cap37.0 net+28/med+13.8) | (°▼i-4.6pp (3/18) · p-8.8pp cap39.0 net-70/med-0.8) |
| london | (°▲i+23.7pp (1/2) · p+25.2pp cap37.0 net+28/med+13.8) | (°▲i+28.4pp (3/6) · p+4.4pp cap39.2 net-32/med-5.4) |
| overlap | — | (°▼i-12.8pp (0/2) · p-23.1pp cap— net-17/med-8.6) |
| ny_only | — | (°▼i-20.8pp (0/2) · p-7.6pp cap— net+1/med+0.7) |
| dead | — | — |
| asia | — | (°▼i-20.5pp (0/8) · p-24.8pp cap6.7 net-22/med+0.4) |

- backtest payoff: right +28 / wrong +0 / net +28 pts; median per fire +13.75 (n=2)
- backtest best call: 2026-07-24 09:09 +43.2pts remaining (episode 42.7pts)
- backtest worst false alarm: 2026-07-24 09:09 -5.8pts adverse
- forward payoff: right +11 / wrong -82 / net -70 pts; median per fire -0.75 (n=18)
- forward best call: 2026-09-04 11:02 +32.7pts remaining (episode 29.7pts)
- forward worst false alarm: 2026-08-28 15:27 -20.5pts adverse
- earliness (backtest): median 43.2 pts of move remaining at fire (n=1)

### H14 — 1 signal
*Counter-trend No Demand / No Supply prints in an established trend mark absorption and precede trend continuation.*
Grading: directional. Latest review: keep-watching (recommendation).

**S0-H14** — session × window grid (cells as in the matrix):

| session | backtest | forward |
|---|---|---|
| whole | ▼i-8.6pp (45/294) · p-9.0pp cap24.8 net-695/med-1.9 | ▲i+6.7pp (118/421) · p-11.0pp cap15.1 net-938/med-2.2 |
| london | ▼i-10.2pp (10/62) · p-5.4pp cap28.1 net-81/med+3.1 | ▲i+16.9pp (35/91) · p-4.7pp cap23.2 net+86/med-1.7 |
| overlap | (°▼i-16.4pp (0/4) · p-1.1pp cap24.0 net+20/med+5.6) | (°▲i+3.9pp (3/18) · p-17.5pp cap23.0 net-194/med-15.0) |
| ny_only | ▼i-5.1pp (16/99) · p-1.1pp cap24.5 net-174/med-3.1 | ▲i+6.3pp (29/107) · p-2.9pp cap14.5 net-14/med+0.8 |
| dead | ▲i+8.7pp (13/33) · p-11.5pp cap17.2 net-105/med-2.4 | ▲i+5.5pp (23/61) · p-15.2pp cap11.3 net-212/med-2.6 |
| asia | ▼i-16.6pp (6/96) · p-12.9pp cap30.8 net-355/med-3.6 | ·i-1.1pp (28/144) · p-15.1pp cap9.5 net-603/med-3.5 |

- backtest payoff: right +1293 / wrong -1989 / net -695 pts; median per fire -1.95 (n=294)
- backtest best call: 2026-07-31 11:45 +89.0pts remaining (episode 93.7pts, major)
- backtest worst false alarm: 2026-07-28 05:56 -59.0pts adverse
- forward payoff: right +1275 / wrong -2212 / net -938 pts; median per fire -2.20 (n=421)
- forward best call: 2026-09-01 03:44 +95.0pts remaining (episode 92.3pts, major)
- forward worst false alarm: 2026-08-27 08:05 -54.2pts adverse
- earliness (backtest): median 23.2 pts of move remaining at fire (n=23)

### H15 — 1 signal
*A range sweep followed by aggressive traversal to the opposite boundary continues toward the range's volume center.*
Grading: directional. Latest review: keep-watching (recommendation).

**S0-H15** — session × window grid (cells as in the matrix):

| session | backtest | forward |
|---|---|---|
| whole | — | — |
| london | — | — |
| overlap | — | — |
| ny_only | — | — |
| dead | — | — |
| asia | — | — |


### H16 — 1 signal
*The opening session's direction predicts the closing session's direction.*
Grading: directional. Latest review: keep-watching (recommendation).

**S0-H16** — session × window grid (cells as in the matrix):

| session | backtest | forward |
|---|---|---|
| whole | (°▼i-3.9pp (3/15) · p+3.1pp cap33.4 net+5/med+6.0) | ▼i-7.7pp (3/22) · p-16.4pp cap36.6 net+39/med+2.4 |
| london | — | — |
| overlap | (°▲i+3.6pp (3/15) · p+0.6pp cap33.4 net+5/med+6.0) | ·i+0.8pp (3/22) · p-14.0pp cap36.6 net+39/med+2.4 |
| ny_only | — | — |
| dead | — | — |
| asia | — | — |

- backtest payoff: right +173 / wrong -169 / net +5 pts; median per fire +6.00 (n=15)
- backtest best call: 2026-08-03 15:00 +4.5pts remaining (episode 28.5pts)
- backtest worst false alarm: 2026-07-16 15:00 -61.7pts adverse
- forward payoff: right +176 / wrong -136 / net +39 pts; median per fire +2.40 (n=22)
- forward best call: 2026-08-20 15:00 +25.5pts remaining (episode 25.5pts)
- forward worst false alarm: 2026-09-08 15:00 -37.8pts adverse
- earliness (backtest): median 1.2 pts of move remaining at fire (n=3)

### H17 — 1 signal
*A climax reversal signal followed by absorption within five bars — effort meeting a quiet counter-party — marks a genuine exhaustion turn: the two-chapter story (exhaustion needs absorption to become reversal).*
Grading: directional. Latest review: rows (recommendation).

**S0-H17** — session × window grid (cells as in the matrix):

| session | backtest | forward |
|---|---|---|
| whole | ▲i+10.2pp (14/41) · p-6.5pp cap41.5 net+76/med+2.5 | ▲i+2.2pp (28/119) · p+1.4pp cap23.4 net+151/med-0.2 |
| london | (°▲i+9.4pp (5/14) · p+3.8pp cap40.0 net+32/med+4.4) | ▲i+9.0pp (11/36) · p+7.2pp cap29.0 net+94/med+3.2 |
| overlap | (°▼i-16.4pp (0/1) · p-26.1pp cap— net+12/med+12.0) | (°▼i-12.8pp (0/9) · p-0.9pp cap25.7 net-57/med-6.0) |
| ny_only | (°▲i+18.7pp (6/15) · p+3.1pp cap53.0 net+34/med+2.5) | ·i+1.8pp (7/31) · p-4.4pp cap29.2 net-22/med-0.7 |
| dead | (°▲i+29.3pp (3/5) · p-17.6pp cap— net-5/med-1.3) | (°▲i+21.6pp (7/13) · p+21.7pp cap9.8 net+10/med+0.0) |
| asia | (°▼i-22.8pp (0/6) · p-16.0pp cap60.8 net+3/med-2.3) | ▼i-10.5pp (3/30) · p-0.6pp cap22.0 net+127/med+1.1 |

- backtest payoff: right +396 / wrong -320 / net +76 pts; median per fire +2.50 (n=41)
- backtest best call: 2026-07-30 12:44 +66.8pts remaining (episode 77.3pts, major)
- backtest worst false alarm: 2026-07-23 12:18 -71.0pts adverse
- forward payoff: right +685 / wrong -534 / net +151 pts; median per fire -0.20 (n=119)
- forward best call: 2026-08-21 09:16 +70.5pts remaining (episode 95.0pts, major)
- forward worst false alarm: 2026-09-03 12:32 -38.0pts adverse
- earliness (backtest): median 26.1 pts of move remaining at fire (n=12)

### H18 — 1 signal
*A gap-traversal signal followed by a same-direction effortless print within five bars — travel meeting no opposition — continues: the map says vacuum, the tape confirms no resistance.*
Grading: directional. Latest review: rows (recommendation).

**S0-H18** — session × window grid (cells as in the matrix):

| session | backtest | forward |
|---|---|---|
| whole | ▼i-4.2pp (12/61) · p+4.3pp cap34.0 net+169/med-1.0 | ▼i-11.6pp (7/72) · p+6.4pp cap17.1 net+50/med+1.4 |
| london | ▼i-14.3pp (3/25) · p+11.2pp cap45.5 net+266/med+1.3 | ▼i-7.7pp (5/36) · p-6.7pp cap22.2 net-54/med-1.8 |
| overlap | (°▲i+10.9pp (3/11) · p-7.9pp cap36.4 net-81/med-6.8) | (°▼i-12.8pp (0/16) · p+1.9pp cap23.1 net+80/med+11.8) |
| ny_only | (°▲i+12.0pp (2/6) · p-10.2pp cap— net+11/med+0.1) | (°▲i+12.5pp (2/6) · p+9.1pp cap8.0 net-0/med+2.9) |
| dead | (°▼i-30.7pp (0/1) · p+82.4pp cap19.2 net+18/med+17.6) | — |
| asia | (°·i-0.6pp (4/18) · p-4.9pp cap22.3 net-44/med-1.9) | (°▼i-20.5pp (0/14) · p+34.1pp cap12.7 net+25/med+4.8) |

- backtest payoff: right +650 / wrong -482 / net +169 pts; median per fire -1.00 (n=61)
- backtest best call: 2026-07-27 03:05 +77.3pts remaining (episode 83.2pts, major)
- backtest worst false alarm: 2026-07-30 14:37 -50.0pts adverse
- forward payoff: right +504 / wrong -453 / net +50 pts; median per fire +1.40 (n=72)
- forward best call: 2026-08-25 12:27 +34.0pts remaining (episode 56.5pts, major)
- forward worst false alarm: 2026-09-03 14:06 -49.5pts adverse
- earliness (backtest): median 15.2 pts of move remaining at fire (n=10)

### H19 — 1 signal
*A probe-failure reversal signal followed by continued wide-loud effort in the anchor bar's own close direction within five bars is NOT the start of the claimed reversal — a SUPPRESSION/FADE configuration, and it says so.*
Grading: directional. Latest review: rows (recommendation).

- Question **Q1-H19**: see the register entry (status there is authoritative).
**S0-H19** — session × window grid (cells as in the matrix):

| session | backtest | forward |
|---|---|---|
| whole | ▼i-5.1pp (40/213) · p-2.0pp cap34.1 net-631/med-1.5 | ▼i-4.0pp (67/388) · p-0.5pp cap17.0 net-428/med-0.1 |
| london | ▼i-12.7pp (6/44) · p-13.4pp cap55.5 net-334/med-11.0 | ▼i-3.5pp (21/116) · p-5.6pp cap32.0 net-743/med-5.5 |
| overlap | (°▼i-16.4pp (0/4) · p+23.9pp cap37.6 net+8/med+5.3) | (°▲i+8.6pp (3/14) · p-8.8pp cap28.8 net+42/med+7.2) |
| ny_only | ▼i-12.2pp (3/33) · p+35.3pp cap41.7 net+263/med+0.7 | ·i-0.1pp (17/82) · p-1.5pp cap17.5 net+97/med+0.2 |
| dead | ·i+1.2pp (23/72) · p-3.7pp cap21.2 net-100/med-0.8 | ▼i-11.4pp (10/48) · p+2.0pp cap12.5 net+27/med+1.1 |
| asia | ▼i-9.5pp (8/60) · p-9.4pp cap26.8 net-469/med-2.0 | ▼i-8.0pp (16/128) · p+4.9pp cap13.7 net+148/med+1.2 |

- backtest payoff: right +1487 / wrong -2118 / net -631 pts; median per fire -1.50 (n=213)
- backtest best call: 2026-07-27 03:04 +78.6pts remaining (episode 83.2pts, major)
- backtest worst false alarm: 2026-07-29 18:44 -83.2pts adverse
- forward payoff: right +1953 / wrong -2381 / net -428 pts; median per fire -0.05 (n=388)
- forward best call: 2026-08-21 09:17 +70.5pts remaining (episode 95.0pts, major)
- forward worst false alarm: 2026-09-01 07:54 -87.7pts adverse
- earliness (backtest): median 25.8 pts of move remaining at fire (n=22)

### H20 — 1 signal
*A wide-bar close-through of a session extreme (the same conditioned wide-bar class the retest anchor fires on; resolution = the close beyond the level, not a rejection back inside) initiates continuation in the break direction.*
Grading: directional. Latest review: rows (recommendation).

**S0-H20** — session × window grid (cells as in the matrix):

| session | backtest | forward |
|---|---|---|
| whole | ▼i-10.6pp (2/50) · p-7.6pp cap62.0 [cls 37.6%/14.6%i] net-221/med-9.7 | ▼i-6.0pp (4/102) · p-6.7pp cap18.5 [cls 44.9%/9.9%i] net-741/med-6.8 |
| london | ▼i-12.9pp (0/28) · p+1.9pp cap75.5 [cls 37.4%/12.9%i] net+241/med-5.2 | ▼i-4.6pp (4/67) · p-6.8pp cap24.0 [cls 42.6%/10.6%i] net-395/med-9.5 |
| overlap | (°▼i-17.5pp (0/4) · p-30.8pp cap— [cls 30.8%/17.5%i] net-47/med-11.6) | (°▼i-12.3pp (0/9) · p+1.5pp cap25.0 [cls 31.8%/12.3%i] net+53/med+4.0) |
| ny_only | (°▲i+10.6pp (1/4) · p-20.5pp cap— [cls 20.5%/14.4%i] net+29/med+7.3) | (°▼i-6.6pp (0/3) · p-7.3pp cap— [cls 7.3%/6.6%i] net-23/med-2.5) |
| dead | (°▲i+23.7pp (1/3) · p-19.1pp cap— [cls 19.1%/9.6%i] net-41/med-14.3) | — |
| asia | (°▼i-16.2pp (0/11) · p-8.3pp cap27.8 [cls 44.7%/16.2%i] net-404/med-29.8) | ▼i-8.6pp (0/23) · p-5.4pp cap10.7 [cls 57.6%/8.6%i] net-375/med-7.3 |

- backtest payoff: right +648 / wrong -869 / net -221 pts; median per fire -9.65 (n=50)
- backtest best call: 2026-07-20 16:42 +48.5pts remaining (episode 41.7pts)
- backtest worst false alarm: 2026-07-24 06:50 -96.0pts adverse
- forward payoff: right +412 / wrong -1153 / net -741 pts; median per fire -6.85 (n=102)
- forward best call: 2026-09-16 11:01 +10.5pts remaining (episode 19.0pts)
- forward worst false alarm: 2026-09-09 06:33 -66.7pts adverse
- earliness (backtest): median 31.9 pts of move remaining at fire (n=2)


---

# ger40 (ger40fut) — CANONICAL

Store span (1M, close ts): 2026-07-19 22:42:00+00:00 → 2026-09-16 16:07:00+00:00. Volume type: real futures volume (register 40 first-sync sanity; canonical verdict at this instrument's validation evening).

## Summary Matrix (page 1)

Engine `8effbb323` — OBSERVATIONAL signal scoreboard - move-detection, not trading; no fills exist here by construction; never validation (docs/hypothesis_lifecycle.md stage 4)

**Review labels are RECOMMENDATIONS — none actioned, review pending operator familiarity.** Cells: marker + precision LIFT vs that context's OWN chance rate, (hits/fires), payoff net/median points (directional rows; either-direction rows have no payoff by construction). ▲/▼ = beyond ±2pp of chance, · = within. (°…) = small-n (fires<20 or episodes<10): dimmed, excluded from any future label arithmetic. Read READING_GUIDE.md first; full detail in hypothesis_performance.json.

| H | label | backtest whole | backtest london | forward whole | forward london |
|---|---|---|---|---|---|
| *context* | | 110 ep; chance 23.6%dir/45.2%either | 28 ep; chance 26.3%dir/51.1%either | 227 ep; chance 24.5%dir/44.9%either | 63 ep; chance 25.6%dir/48.1%either |
| S0-H1 | keep-watching | ▼i-2.6pp (9/49) · p+11.1pp cap89.9 net-83/med+0.7 | (°▼i-21.1pp (0/5) · p+33.7pp cap89.9 net+198/med+39.9) | ·i+1.1pp (48/216) · p+1.4pp cap44.9 net-567/med+0.3 | ▲i+5.5pp (19/67) · p+2.8pp cap61.6 net-634/med-6.4 |
| S1-H1 | keep-watching | (°▼i-21.0pp (0/3) · p-23.6pp cap— net-72/med-34.2) | (°▼i-21.1pp (0/1) · p-26.3pp cap— net-54/med-53.5) | (°▼i-13.4pp (1/13) · p-9.1pp cap46.4 net-37/med+0.5) | (°▼i-22.9pp (0/6) · p-8.9pp cap57.0 net-55/med-11.1) |
| S0-H2 | promote-candidate | ▼i-9.5pp (27/234) · p+2.0pp cap76.6 net-661/med-5.2 | (°▼i-7.8pp (2/15) · p-13.0pp cap86.6 net+93/med+9.8) | ·i-1.0pp (158/787) · p-1.9pp cap44.4 net-1092/med-0.7 | ·i+0.3pp (47/203) · p-8.9pp cap76.5 net-710/med-3.8 |
| S1-H2 | promote-candidate | ▼i-9.1pp (21/176) · p+3.7pp cap76.6 net-760/med-8.3 | (°▼i-5.7pp (2/13) · p-10.9pp cap86.6 net+136/med+14.0) | ·i+1.9pp (129/561) · p-3.1pp cap43.4 net-1373/med-1.1 | ▲i+3.9pp (38/142) · p-8.7pp cap76.0 net-716/med-7.0 |
| S0-H3 | keep-watching | (°▲i+4.0pp (2/8) · p-11.1pp cap70.3 net-28/med+2.0) | — | ▼i-2.6pp (5/27) · p+1.4pp cap30.4 net-220/med-1.5 | (°▼i-22.9pp (0/3) · p-25.6pp cap— net-167/med-51.6) |
| S0-H4 | keep-watching | ▼i-9.2pp (4/34) · p+8.8pp cap50.2 net+72/med+10.0 | (°▲i+8.9pp (3/10) · p-16.3pp cap50.2 net-30/med-3.7) | — | — |
| S0-H5 | keep-watching | — | — | — | — |
| S0-H6 | keep-watching | ▼i-11.1pp (1/36) · p+7.4pp cap56.7 [cls 34.3%/13.9%i] net-192/med-10.4 | (°▼i-4.3pp (1/18) · p-7.3pp cap78.7 [cls 35.1%/9.9%i] net-56/med-10.3) | ▲i+5.3pp (35/192) · p+0.1pp cap55.1 [cls 41.6%/12.9%i] net-1115/med-4.5 | ·i+1.1pp (13/105) · p-1.9pp cap57.9 [cls 40.0%/11.3%i] net-1320/med-13.2 |
| S0-H7 | keep-watching | ·i-0.7pp (12/59) · p+12.0pp cap97.8 net+761/med+4.2 | ▼i-11.1pp (2/20) · p+23.7pp cap86.9 net+719/med+33.0 | ▲i+3.7pp (36/145) · p+3.1pp cap58.4 net-72/med+0.8 | ▲i+9.9pp (22/67) · p-0.2pp cap74.1 net-306/med-0.3 |
| S0-H7 (either-dir) | keep-watching | ▼i-5.6pp (20/59) · p+19.2pp cap50.2 | ▼i-10.2pp (6/20) · p+23.9pp cap57.4 | ▼i-6.1pp (48/145) · p+4.1pp cap23.8 | ·i-1.0pp (27/67) · p+2.6pp cap32.6 |
| S0-H8 | keep-watching | ▼i-10.9pp (67/234) · p+8.2pp cap36.4 | (°▼i-26.9pp (2/15) · p-31.1pp cap68.2) | ▲i+3.6pp (337/787) · p-3.1pp cap23.5 | ▲i+7.0pp (98/203) · p-9.7pp cap21.3 |
| S0-H9 | keep-watching | ▲i+2.1pp (12/52) · p-8.2pp cap55.5 net-426/med-4.1 | (°▼i-21.1pp (0/3) · p-26.3pp cap— net+17/med+22.6) | ▼i-11.5pp (8/83) · p-0.4pp cap40.6 net+136/med-1.9 | (°▼i-22.9pp (0/12) · p+16.1pp cap75.3 net+274/med+18.9) |
| S1-H9 | keep-watching | (°▼i-21.0pp (0/8) · p+26.4pp cap101.1 net-53/med+13.1) | — | ▼i-14.0pp (3/42) · p-3.1pp cap45.6 net+50/med-7.2 | (°▼i-22.9pp (0/8) · p+11.9pp cap120.0 net+280/med+41.9) |
| S0-H10 | deprioritize | ▲i+5.5pp (39/147) · p-5.2pp cap51.4 net-391/med+3.2 | ▲i+2.0pp (9/39) · p-16.0pp cap80.6 net-463/med-12.5 | ▼i-2.3pp (71/378) · p+2.0pp cap31.0 net+751/med+0.6 | ▲i+4.4pp (18/66) · p+0.2pp cap55.8 net-178/med-8.4 |
| S0-H11 | keep-watching | ·i-0.7pp (15/74) · p-3.3pp cap68.3 net-452/med-6.0 | (°▼i-21.1pp (0/14) · p-4.9pp cap73.1 net-472/med-58.8) | ▼i-2.7pp (127/691) · p+1.5pp cap42.1 net-998/med-2.3 | ·i+0.9pp (80/336) · p-2.7pp cap60.7 net-447/med-2.3 |
| S1-H11 | keep-watching | ·i+0.9pp (66/301) · p+6.6pp cap82.3 net+1221/med+5.2 | ▲i+10.1pp (35/112) · p+0.5pp cap84.4 net+267/med+1.2 | ▼i-3.6pp (139/794) · p+2.8pp cap48.2 net-758/med+0.2 | ▼i-6.5pp (45/274) · p+3.2pp cap57.9 net-123/med+0.9 |
| S0-H12 | keep-watching | — | — | — | — |
| S0-H13 | keep-watching | (°▼i-4.3pp (1/6) · p+59.7pp cap74.2 net+397/med+58.7) | (°▼i-21.1pp (0/2) · p+73.7pp cap116.8 net+181/med+90.7) | (°▼i-14.9pp (1/16) · p+6.7pp cap44.6 net+44/med+4.3) | (°▼i-8.6pp (1/7) · p-11.3pp cap66.9 net-42/med-9.9) |
| S0-H14 | keep-watching | ·i-0.6pp (23/113) · p+2.9pp cap53.9 net+312/med+0.5 | ▼i-2.6pp (5/27) · p-11.5pp cap80.6 net-256/med-4.2 | ·i-0.8pp (73/359) · p-0.3pp cap28.8 net-284/med-0.4 | ▲i+3.1pp (19/73) · p-0.9pp cap58.0 net-150/med-12.2 |
| S0-H15 | keep-watching | — | — | — | — |
| S0-H16 | keep-watching | (°▼i-21.0pp (0/10) · p-3.6pp cap126.3 net+8/med-16.3) | — | ▼i-8.1pp (3/23) · p-11.5pp cap69.9 net-217/med-4.9 | — |
| S0-H17 | rows | ·i+0.7pp (5/23) · p+6.8pp cap90.2 net+36/med+0.7 | (°▼i-21.1pp (0/3) · p+40.4pp cap96.2 net+198/med+78.9) | ▲i+3.7pp (34/137) · p+1.0pp cap45.2 net-130/med+0.3 | ▲i+13.5pp (16/44) · p-5.1pp cap64.5 net-444/med-9.1 |
| S0-H18 | rows | (°·i-1.0pp (3/15) · p-10.3pp cap102.0 net-232/med-14.3) | (°▼i-21.1pp (0/3) · p+7.0pp cap135.4 net-19/med-38.6) | ▼i-4.7pp (20/122) · p+3.4pp cap49.6 net-425/med-4.5 | ▼i-2.6pp (15/74) · p-2.6pp cap55.6 net-290/med-7.1 |
| S0-H19 | rows | ▼i-4.0pp (25/147) · p+5.0pp cap74.2 net+179/med+3.6 | (°▼i-10.0pp (1/9) · p-26.3pp cap— net-51/med-14.3) | ▲i+3.7pp (100/403) · p-4.6pp cap52.5 net+226/med-1.0 | ▲i+14.6pp (39/104) · p-8.3pp cap71.5 net-382/med-5.2 |
| S0-H20 | rows | ▼i-13.9pp (0/35) · p+2.8pp cap57.7 [cls 34.3%/13.9%i] net-450/med-4.3 | (°▼i-9.9pp (0/19) · p+7.0pp cap61.4 [cls 35.1%/9.9%i] net+20/med+11.4) | ▼i-7.5pp (8/148) · p+4.3pp cap55.8 [cls 41.6%/12.9%i] net+813/med+4.5 | ▼i-7.6pp (3/81) · p+9.4pp cap74.2 [cls 40.0%/11.3%i] net+1057/med+8.5 |
| **union coverage** | | 47.3% (52/110) | 35.7% (10/28) | 86.3% (196/227) | 93.7% (59/63) |

Not graded:  — see register entries.

## Hypothesis Cards (page 2)

### H1 — 2 signals
*A climactic bar — extreme volume on a wide spread late in an extended move — marks exhaustion, and price then reverses against the climax direction.*
Grading: directional. Latest review: keep-watching (recommendation).

- Question **Q1-H1**: see the register entry (status there is authoritative).
**S0-H1** — session × window grid (cells as in the matrix):

| session | backtest | forward |
|---|---|---|
| whole | ▼i-2.6pp (9/49) · p+11.1pp cap89.9 net-83/med+0.7 | ·i+1.1pp (48/216) · p+1.4pp cap44.9 net-567/med+0.3 |
| london | (°▼i-21.1pp (0/5) · p+33.7pp cap89.9 net+198/med+39.9) | ▲i+5.5pp (19/67) · p+2.8pp cap61.6 net-634/med-6.4 |
| overlap | — | (°·i-1.8pp (2/13) · p-2.2pp cap84.7 net-152/med-6.4) |
| ny_only | (°▼i-19.1pp (0/10) · p+18.5pp cap83.5 net-289/med-3.9) | ▼i-8.4pp (4/46) · p+1.5pp cap35.1 net+50/med+6.9 |
| dead | (°▲i+3.4pp (2/7) · p+40.7pp cap89.2 net+93/med+34.1) | ▲i+4.1pp (9/27) · p+8.9pp cap43.8 net+18/med+0.1 |
| asia | ▲i+3.0pp (7/27) · p-5.8pp cap94.2 net-85/med-12.0 | ·i+1.5pp (14/63) · p-0.8pp cap28.9 net+151/med+0.5 |

- backtest payoff: right +1327 / wrong -1411 / net -83 pts; median per fire +0.70 (n=49)
- backtest best call: 2026-07-29 03:13 +188.0pts remaining (episode 262.8pts, major)
- backtest worst false alarm: 2026-07-29 19:11 -164.0pts adverse
- forward payoff: right +2671 / wrong -3238 / net -567 pts; median per fire +0.30 (n=216)
- forward best call: 2026-09-11 02:06 +219.3pts remaining (episode 237.1pts, major)
- forward worst false alarm: 2026-09-01 08:06 -208.4pts adverse
- earliness (backtest): median 98.4 pts of move remaining at fire (n=8)

**S1-H1** — session × window grid (cells as in the matrix):

| session | backtest | forward |
|---|---|---|
| whole | (°▼i-21.0pp (0/3) · p-23.6pp cap— net-72/med-34.2) | (°▼i-13.4pp (1/13) · p-9.1pp cap46.4 net-37/med+0.5) |
| london | (°▼i-21.1pp (0/1) · p-26.3pp cap— net-54/med-53.5) | (°▼i-22.9pp (0/6) · p-8.9pp cap57.0 net-55/med-11.1) |
| overlap | — | — |
| ny_only | — | (°▼i-17.1pp (0/3) · p-7.2pp cap— net+11/med+5.0) |
| dead | — | (°▼i-29.2pp (0/1) · p+83.0pp cap35.8 net+32/med+31.5) |
| asia | (°▼i-22.9pp (0/2) · p-31.7pp cap— net-19/med-9.3) | (°▲i+12.6pp (1/3) · p-37.3pp cap— net-24/med-5.1) |

- backtest payoff: right +16 / wrong -88 / net -72 pts; median per fire -34.20 (n=3)
- backtest worst false alarm: 2026-07-28 10:36 -60.8pts adverse
- forward payoff: right +133 / wrong -169 / net -37 pts; median per fire +0.50 (n=13)
- forward best call: 2026-08-20 04:29 +162.0pts remaining (episode 176.7pts, major)
- forward worst false alarm: 2026-09-09 10:02 -93.4pts adverse

### H2 — 2 signals
*A failed probe beyond a prior extreme — an upthrust above or spring below that closes back inside — reverses against the probe.*
Grading: directional. Latest review: promote-candidate (recommendation).

**S0-H2** — session × window grid (cells as in the matrix):

| session | backtest | forward |
|---|---|---|
| whole | ▼i-9.5pp (27/234) · p+2.0pp cap76.6 net-661/med-5.2 | ·i-1.0pp (158/787) · p-1.9pp cap44.4 net-1092/med-0.7 |
| london | (°▼i-7.8pp (2/15) · p-13.0pp cap86.6 net+93/med+9.8) | ·i+0.3pp (47/203) · p-8.9pp cap76.5 net-710/med-3.8 |
| overlap | (°▼i-13.4pp (0/11) · p-14.6pp cap122.7 net-195/med-38.7) | ▼i-5.6pp (5/43) · p-2.0pp cap71.7 net-157/med-4.7 |
| ny_only | ▼i-7.6pp (7/61) · p+13.1pp cap77.0 net-1116/med-16.7 | ·i-1.8pp (29/190) · p-1.4pp cap51.0 net-720/med-3.5 |
| dead | ▼i-9.8pp (8/52) · p+6.7pp cap90.8 net+604/med+2.2 | ▼i-7.3pp (21/96) · p+16.3pp cap35.6 net+252/med+0.9 |
| asia | ▼i-12.4pp (10/95) · p-0.1pp cap75.9 net-47/med-10.6 | ·i+1.3pp (56/255) · p-1.6pp cap35.7 net+243/med+2.3 |

- backtest payoff: right +4896 / wrong -5557 / net -661 pts; median per fire -5.20 (n=234)
- backtest best call: 2026-07-27 03:23 +214.5pts remaining (episode 245.3pts, major)
- backtest worst false alarm: 2026-07-29 19:00 -192.8pts adverse
- forward payoff: right +9132 / wrong -10224 / net -1092 pts; median per fire -0.65 (n=786)
- forward best call: 2026-09-11 02:21 +211.3pts remaining (episode 237.1pts, major)
- forward worst false alarm: 2026-09-15 09:26 -152.3pts adverse
- earliness (backtest): median 97.8 pts of move remaining at fire (n=19)

**S1-H2** — session × window grid (cells as in the matrix):

| session | backtest | forward |
|---|---|---|
| whole | ▼i-9.1pp (21/176) · p+3.7pp cap76.6 net-760/med-8.3 | ·i+1.9pp (129/561) · p-3.1pp cap43.4 net-1373/med-1.1 |
| london | (°▼i-5.7pp (2/13) · p-10.9pp cap86.6 net+136/med+14.0) | ▲i+3.9pp (38/142) · p-8.7pp cap76.0 net-716/med-7.0 |
| overlap | (°▼i-13.4pp (0/7) · p-9.4pp cap122.7 net-89/med-38.1) | ▼i-3.9pp (4/30) · p+1.4pp cap72.2 net-86/med-1.3 |
| ny_only | ▼i-8.0pp (5/45) · p+17.4pp cap77.0 net-1094/med-25.7 | ·i-1.1pp (21/131) · p-4.9pp cap40.4 net-849/med-4.6 |
| dead | ▼i-10.2pp (6/40) · p+11.1pp cap74.9 net+699/med+7.8 | ·i+0.5pp (19/64) · p+15.8pp cap35.6 net+236/med+1.8 |
| asia | ▼i-11.6pp (8/71) · p-2.1pp cap76.2 net-413/med-26.4 | ▲i+3.5pp (47/194) · p-4.3pp cap35.8 net+42/med+1.6 |

- backtest payoff: right +3792 / wrong -4553 / net -760 pts; median per fire -8.35 (n=176)
- backtest best call: 2026-07-29 03:05 +193.7pts remaining (episode 262.8pts, major)
- backtest worst false alarm: 2026-07-29 19:00 -192.8pts adverse
- forward payoff: right +6101 / wrong -7474 / net -1373 pts; median per fire -1.10 (n=561)
- forward best call: 2026-09-11 02:21 +211.3pts remaining (episode 237.1pts, major)
- forward worst false alarm: 2026-09-15 09:26 -152.3pts adverse
- earliness (backtest): median 97.8 pts of move remaining at fire (n=17)

### H3 — 1 signal
*Repeated absorption — high effort with no result — at a price level precedes a breakout through that level.*
Grading: directional. Latest review: keep-watching (recommendation).

**S0-H3** — session × window grid (cells as in the matrix):

| session | backtest | forward |
|---|---|---|
| whole | (°▲i+4.0pp (2/8) · p-11.1pp cap70.3 net-28/med+2.0) | ▼i-2.6pp (5/27) · p+1.4pp cap30.4 net-220/med-1.5 |
| london | — | (°▼i-22.9pp (0/3) · p-25.6pp cap— net-167/med-51.6) |
| overlap | — | — |
| ny_only | (°▲i+20.9pp (2/5) · p+8.5pp cap70.3 net+132/med+41.2) | (°·i-0.4pp (1/6) · p-7.2pp cap— net+5/med-0.1) |
| dead | — | — |
| asia | (°▼i-22.9pp (0/3) · p-31.7pp cap— net-160/med-56.5) | (°·i+1.5pp (4/18) · p+1.6pp cap30.4 net-58/med-0.5) |

- backtest payoff: right +132 / wrong -160 / net -28 pts; median per fire +2.00 (n=8)
- backtest best call: 2026-07-27 18:10 +51.7pts remaining (episode 62.9pts)
- backtest worst false alarm: 2026-07-30 01:57 -65.7pts adverse
- forward payoff: right +215 / wrong -436 / net -220 pts; median per fire -1.50 (n=27)
- forward best call: 2026-08-27 04:28 +37.5pts remaining (episode 52.5pts, major)
- forward worst false alarm: 2026-09-09 09:25 -136.1pts adverse
- earliness (backtest): median 51.7 pts of move remaining at fire (n=1)

### H4 — 1 signal
*In an established trend, a quiet (low-volume) pullback resolves with trend resumption.*
Grading: directional. Latest review: keep-watching (recommendation).

**S0-H4** — session × window grid (cells as in the matrix):

| session | backtest | forward |
|---|---|---|
| whole | ▼i-9.2pp (4/34) · p+8.8pp cap50.2 net+72/med+10.0 | — |
| london | (°▲i+8.9pp (3/10) · p-16.3pp cap50.2 net-30/med-3.7) | — |
| overlap | (°▼i-13.4pp (0/6) · p+9.6pp cap59.3 net-4/med-8.4) | — |
| ny_only | (°▼i-19.1pp (0/6) · p+21.8pp cap25.4 net-9/med+10.8) | — |
| dead | (°·i-0.2pp (1/4) · p+8.6pp cap34.8 net-14/med+32.4) | — |
| asia | (°▼i-22.9pp (0/8) · p+30.8pp cap61.0 net+129/med+17.4) | — |

- backtest payoff: right +556 / wrong -484 / net +72 pts; median per fire +10.00 (n=33)
- backtest best call: 2026-08-03 11:48 +80.2pts remaining (episode 142.0pts, major)
- backtest worst false alarm: 2026-07-26 23:29 -102.8pts adverse
- earliness (backtest): median 75.7 pts of move remaining at fire (n=2)

### H5 — 1 signal
*A buying climax that extends far above its trend mean mean-reverts (climax-extension fade; registered short-side only).*
Grading: directional. Latest review: keep-watching (recommendation).

**S0-H5** — session × window grid (cells as in the matrix):

| session | backtest | forward |
|---|---|---|
| whole | — | — |
| london | — | — |
| overlap | — | — |
| ny_only | — | — |
| dead | — | — |
| asia | — | — |


### H6 — 1 signal
*A wide-spread rejection bar at a session extreme (measured day-relative, volume-agnostic) reverses away from the extreme.*
Grading: directional. Latest review: keep-watching (recommendation).

- Question **Q1-H6**: see the register entry (status there is authoritative).
- Question **Q2-H6**: see the register entry (status there is authoritative).
- Question **Q3-H6**: see the register entry (status there is authoritative).
**S0-H6** — session × window grid (cells as in the matrix):

| session | backtest | forward |
|---|---|---|
| whole | ▼i-11.1pp (1/36) · p+7.4pp cap56.7 [cls 34.3%/13.9%i] net-192/med-10.4 | ▲i+5.3pp (35/192) · p+0.1pp cap55.1 [cls 41.6%/12.9%i] net-1115/med-4.5 |
| london | (°▼i-4.3pp (1/18) · p-7.3pp cap78.7 [cls 35.1%/9.9%i] net-56/med-10.3) | ·i+1.1pp (13/105) · p-1.9pp cap57.9 [cls 40.0%/11.3%i] net-1320/med-13.2 |
| overlap | (°▼i-13.5pp (0/1) · p+72.1pp cap122.7 [cls 27.9%/13.5%i] net+108/med+108.3) | (°▲i+11.8pp (6/19) · p+8.7pp cap78.4 [cls 28.1%/19.8%i] net+228/med+0.8) |
| ny_only | — | (°▼i-8.7pp (0/3) · p-8.3pp cap— [cls 8.3%/8.7%i] net-57/med-2.8) |
| dead | (°▼i-12.5pp (0/3) · p-25.0pp cap— [cls 25.0%/12.5%i] net+29/med+13.4) | — |
| asia | (°▼i-20.4pp (0/14) · p+27.9pp cap40.0 [cls 36.4%/20.4%i] net-274/med-21.8) | ▲i+10.7pp (16/65) · p+1.0pp cap43.7 [cls 49.8%/13.9%i] net+34/med+2.0 |

- backtest payoff: right +682 / wrong -874 / net -192 pts; median per fire -10.40 (n=36)
- backtest best call: 2026-07-28 12:35 +146.2pts remaining (episode 195.2pts, major)
- backtest worst false alarm: 2026-08-03 07:10 -108.0pts adverse
- forward payoff: right +2856 / wrong -3970 / net -1115 pts; median per fire -4.55 (n=192)
- forward best call: 2026-08-26 12:31 +139.4pts remaining (episode 156.6pts, major)
- forward worst false alarm: 2026-09-15 07:24 -176.9pts adverse
- earliness (backtest): median 146.2 pts of move remaining at fire (n=1)

### H7 — 1 signal
*Quiet decline at a session extreme is disguised accumulation: effortless (low-volume) weakness reverses UP once selling fails to attract participation (mirror: quiet advance at a high reverses down).*
Grading: directional + either-direction (dual). Latest review: keep-watching (recommendation).

- Question **Q1-H7**: see the register entry (status there is authoritative).
**S0-H7** — session × window grid (cells as in the matrix):

| session | backtest | forward |
|---|---|---|
| whole | ·i-0.7pp (12/59) · p+12.0pp cap97.8 net+761/med+4.2 | ▲i+3.7pp (36/145) · p+3.1pp cap58.4 net-72/med+0.8 |
| london | ▼i-11.1pp (2/20) · p+23.7pp cap86.9 net+719/med+33.0 | ▲i+9.9pp (22/67) · p-0.2pp cap74.1 net-306/med-0.3 |
| overlap | (°▼i-6.7pp (1/15) · p+23.0pp cap91.3 net+56/med-29.0) | ▼i-7.7pp (2/21) · p+3.3pp cap72.7 net+125/med+2.8 |
| ny_only | (°▼i-2.4pp (1/6) · p+5.2pp cap101.1 net+59/med+7.7) | ▲i+2.1pp (5/26) · p+0.5pp cap50.5 net+38/med+6.2 |
| dead | (°▲i+24.8pp (2/4) · p+8.6pp cap128.8 net-15/med-28.8) | (°▼i-4.2pp (1/4) · p+33.0pp cap26.1 net+23/med-6.5) |
| asia | (°▲i+20.0pp (6/14) · p-17.4pp cap99.9 net-58/med-10.2) | ·i+1.5pp (6/27) · p+10.8pp cap25.8 net+48/med+0.9 |

- backtest payoff: right +1756 / wrong -995 / net +761 pts; median per fire +4.20 (n=59)
- backtest best call: 2026-07-27 03:04 +247.0pts remaining (episode 245.3pts, major)
- backtest worst false alarm: 2026-07-27 13:57 -91.8pts adverse
- forward payoff: right +2215 / wrong -2287 / net -72 pts; median per fire +0.80 (n=145)
- forward best call: 2026-08-27 11:41 +136.3pts remaining (episode 158.4pts, major)
- forward worst false alarm: 2026-09-10 11:52 -168.6pts adverse
- earliness (backtest): median 74.6 pts of move remaining at fire (n=11)

**S0-H7 (either-dir)** — session × window grid (cells as in the matrix):

| session | backtest | forward |
|---|---|---|
| whole | ▼i-5.6pp (20/59) · p+19.2pp cap50.2 | ▼i-6.1pp (48/145) · p+4.1pp cap23.8 |
| london | ▼i-10.2pp (6/20) · p+23.9pp cap57.4 | ·i-1.0pp (27/67) · p+2.6pp cap32.6 |
| overlap | (°▼i-19.9pp (1/15) · p+33.4pp cap65.0) | ▼i-10.1pp (5/21) · p+2.3pp cap64.6 |
| ny_only | (°▼i-2.4pp (2/6) · p+10.7pp cap52.5) | ▼i-6.2pp (7/26) · p+0.9pp cap25.5 |
| dead | (°▲i+4.0pp (2/4) · p+43.1pp cap-2.7) | (°·i-1.6pp (2/4) · p+17.8pp cap26.1) |
| asia | (°▲i+21.6pp (9/14) · p-16.5pp cap7.9) | ▼i-13.1pp (7/27) · p+9.2pp cap21.3 |

- backtest payoff: n/a by construction (either-direction)
- backtest best call: 2026-07-27 03:04 +247.0pts remaining (episode 245.3pts, major)
- backtest worst false alarm: 2026-07-29 11:19 -63.7pts adverse
- forward payoff: n/a by construction (either-direction)
- forward best call: 2026-08-27 11:41 +136.3pts remaining (episode 158.4pts, major)
- forward worst false alarm: 2026-09-04 14:35 -55.8pts adverse
- earliness (backtest): median 74.6 pts of move remaining at fire (n=17)

### H8 — 1 signal
*Reversal-signature bar anatomy (upthrust/spring) predicts imminent range expansion irrespective of direction.*
Grading: either-direction. Latest review: keep-watching (recommendation).

**S0-H8** — session × window grid (cells as in the matrix):

| session | backtest | forward |
|---|---|---|
| whole | ▼i-10.9pp (67/234) · p+8.2pp cap36.4 | ▲i+3.6pp (337/787) · p-3.1pp cap23.5 |
| london | (°▼i-26.9pp (2/15) · p-31.1pp cap68.2) | ▲i+7.0pp (98/203) · p-9.7pp cap21.3 |
| overlap | (°▼i-17.5pp (1/11) · p+17.0pp cap37.2) | ▼i-3.7pp (13/43) · p+1.1pp cap21.1 |
| ny_only | ▼i-7.8pp (17/61) · p+33.1pp cap32.1 | ·i+1.1pp (65/190) · p+1.8pp cap10.0 |
| dead | ▼i-13.3pp (17/52) · p+0.8pp cap53.2 | ·i+0.5pp (50/96) · p+19.9pp cap25.6 |
| asia | ▼i-11.1pp (30/95) · p+8.0pp cap29.9 | ▲i+4.5pp (111/255) · p-6.9pp cap24.9 |

- backtest payoff: n/a by construction (either-direction)
- backtest best call: 2026-07-27 03:23 +214.5pts remaining (episode 245.3pts, major)
- backtest worst false alarm: 2026-07-27 16:40 -76.3pts adverse
- forward payoff: n/a by construction (either-direction)
- forward best call: 2026-09-11 02:21 +211.3pts remaining (episode 237.1pts, major)
- forward worst false alarm: 2026-09-01 09:34 -73.8pts adverse
- earliness (backtest): median 80.1 pts of move remaining at fire (n=27)

### H9 — 2 signals
*Persistent lower-TF directional pressure that recruits expanding participation at the parent timeframe precedes continuation beyond what the parent label alone predicts; pressure without participation expansion does not.*
Grading: directional. Latest review: keep-watching (recommendation).

- Question **Q2-H9**: see the register entry (status there is authoritative).
**S0-H9** — session × window grid (cells as in the matrix):

| session | backtest | forward |
|---|---|---|
| whole | ▲i+2.1pp (12/52) · p-8.2pp cap55.5 net-426/med-4.1 | ▼i-11.5pp (8/83) · p-0.4pp cap40.6 net+136/med-1.9 |
| london | (°▼i-21.1pp (0/3) · p-26.3pp cap— net+17/med+22.6) | (°▼i-22.9pp (0/12) · p+16.1pp cap75.3 net+274/med+18.9) |
| overlap | (°▼i-13.4pp (0/2) · p-23.7pp cap— net+112/med+55.8) | (°▼i-17.2pp (0/5) · p-5.3pp cap42.5 net+49/med+13.3) |
| ny_only | ▲i+8.2pp (6/22) · p-7.0pp cap32.0 net-517/med-19.3 | ▼i-8.4pp (2/23) · p+10.2pp cap17.5 net-132/med-7.5 |
| dead | (°·i-0.2pp (3/12) · p+16.9pp cap101.1 net+200/med+3.0) | (°▼i-4.2pp (3/12) · p+8.0pp cap40.6 net+130/med+9.1) |
| asia | (°·i+0.2pp (3/13) · p-8.6pp cap49.0 net-238/med-8.5) | ▼i-11.0pp (3/31) · p-14.7pp cap25.0 net-186/med-5.5 |

- backtest payoff: right +725 / wrong -1151 / net -426 pts; median per fire -4.10 (n=51)
- backtest best call: 2026-07-31 05:00 +184.4pts remaining (episode 184.2pts, major)
- backtest worst false alarm: 2026-07-29 18:45 -160.1pts adverse
- forward payoff: right +927 / wrong -791 / net +136 pts; median per fire -1.90 (n=79)
- forward best call: 2026-09-14 23:30 +340.4pts remaining (episode 342.2pts, major)
- forward worst false alarm: 2026-08-18 07:00 -118.4pts adverse
- earliness (backtest): median 56.3 pts of move remaining at fire (n=6)

**S1-H9** — session × window grid (cells as in the matrix):

| session | backtest | forward |
|---|---|---|
| whole | (°▼i-21.0pp (0/8) · p+26.4pp cap101.1 net-53/med+13.1) | ▼i-14.0pp (3/42) · p-3.1pp cap45.6 net+50/med-7.2 |
| london | — | (°▼i-22.9pp (0/8) · p+11.9pp cap120.0 net+280/med+41.9) |
| overlap | (°▼i-13.4pp (0/1) · p-23.7pp cap— net+56/med+55.8) | — |
| ny_only | (°▼i-19.1pp (0/2) · p-11.5pp cap— net-320/med-160.1) | (°▼i-17.1pp (0/10) · p+12.8pp cap36.8 net-45/med-7.7) |
| dead | (°▼i-25.2pp (0/5) · p+63.6pp cap101.1 net+211/med+19.4) | (°▼i-4.2pp (2/8) · p+20.5pp cap40.6 net+116/med+21.3) |
| asia | — | (°▼i-14.5pp (1/16) · p-31.1pp cap40.2 net-300/med-13.8) |

- backtest payoff: right +294 / wrong -348 / net -53 pts; median per fire +13.05 (n=8)
- backtest worst false alarm: 2026-07-29 18:45 -160.1pts adverse
- forward payoff: right +592 / wrong -541 / net +50 pts; median per fire -7.20 (n=40)
- forward best call: 2026-08-25 03:30 +191.3pts remaining (episode 188.9pts, major)
- forward worst false alarm: 2026-08-18 07:00 -118.4pts adverse

### H10 — 1 signal
*In an established 1-minute trend, no-demand/no-supply prints in the trend's direction signal continuation.*
Grading: directional. Latest review: deprioritize (recommendation).

**S0-H10** — session × window grid (cells as in the matrix):

| session | backtest | forward |
|---|---|---|
| whole | ▲i+5.5pp (39/147) · p-5.2pp cap51.4 net-391/med+3.2 | ▼i-2.3pp (71/378) · p+2.0pp cap31.0 net+751/med+0.6 |
| london | ▲i+2.0pp (9/39) · p-16.0pp cap80.6 net-463/med-12.5 | ▲i+4.4pp (18/66) · p+0.2pp cap55.8 net-178/med-8.4 |
| overlap | (°▼i-13.4pp (0/9) · p-1.5pp cap59.5 net-114/med-21.0) | ·i-1.2pp (4/25) · p+2.7pp cap83.3 net+518/med+9.6 |
| ny_only | ·i-1.5pp (6/34) · p+6.1pp cap46.2 net+237/med+4.4 | ▲i+4.1pp (14/66) · p+3.4pp cap24.4 net-38/med+1.2 |
| dead | (°▲i+3.4pp (4/14) · p-16.4pp cap— net-275/med-13.8) | ▼i-11.0pp (10/55) · p-7.9pp cap22.7 net-188/med-2.6 |
| asia | ▲i+16.3pp (20/51) · p-2.3pp cap51.4 net+224/med+6.3 | ▼i-5.6pp (25/166) · p+1.3pp cap28.4 net+637/med+1.6 |

- backtest payoff: right +1730 / wrong -2121 / net -391 pts; median per fire +3.20 (n=147)
- backtest best call: 2026-07-27 03:28 +219.3pts remaining (episode 245.3pts, major)
- backtest worst false alarm: 2026-08-03 06:31 -111.9pts adverse
- forward payoff: right +3848 / wrong -3096 / net +751 pts; median per fire +0.60 (n=377)
- forward best call: 2026-09-08 23:46 +358.6pts remaining (episode 362.9pts, major)
- forward worst false alarm: 2026-09-04 09:34 -89.4pts adverse
- earliness (backtest): median 81.0 pts of move remaining at fire (n=11)

### H11 — 2 signals
*Price entering a low-volume price zone traverses it faster than baseline; entering a high-volume node it stalls or reverses at above-baseline rates.*
Grading: directional. Latest review: keep-watching (recommendation).

- Question **Q1-H11**: see the register entry (status there is authoritative).
- Question **Q2-H11**: see the register entry (status there is authoritative).
**S0-H11** — session × window grid (cells as in the matrix):

| session | backtest | forward |
|---|---|---|
| whole | ·i-0.7pp (15/74) · p-3.3pp cap68.3 net-452/med-6.0 | ▼i-2.7pp (127/691) · p+1.5pp cap42.1 net-998/med-2.3 |
| london | (°▼i-21.1pp (0/14) · p-4.9pp cap73.1 net-472/med-58.8) | ·i+0.9pp (80/336) · p-2.7pp cap60.7 net-447/med-2.3 |
| overlap | (°·i-0.9pp (2/16) · p-17.5pp cap68.3 net-166/med-13.2) | ▼i-17.2pp (0/52) · p-9.9pp cap70.9 net+286/med-0.1 |
| ny_only | (°▼i-19.1pp (0/4) · p-11.5pp cap— net-18/med-18.5) | ·i+1.4pp (12/65) · p-2.6pp cap27.0 net-320/med-5.3 |
| dead | (°▲i+17.7pp (3/7) · p-2.1pp cap52.6 net+1/med+4.1) | ▼i-17.2pp (3/25) · p+7.0pp cap21.8 net-43/med-2.6 |
| asia | ▲i+7.4pp (10/33) · p-1.4pp cap64.5 net+203/med-1.1 | ▼i-5.7pp (32/213) · p+3.1pp cap31.6 net-474/med-1.3 |

- backtest payoff: right +1359 / wrong -1811 / net -452 pts; median per fire -5.95 (n=74)
- backtest best call: 2026-07-29 04:03 +262.2pts remaining (episode 262.8pts, major)
- backtest worst false alarm: 2026-07-31 07:03 -171.6pts adverse
- forward payoff: right +9304 / wrong -10303 / net -998 pts; median per fire -2.30 (n=691)
- forward best call: 2026-08-26 10:01 +138.2pts remaining (episode 167.4pts, major)
- forward worst false alarm: 2026-09-01 08:03 -222.9pts adverse
- earliness (backtest): median 105.2 pts of move remaining at fire (n=8)

**S1-H11** — session × window grid (cells as in the matrix):

| session | backtest | forward |
|---|---|---|
| whole | ·i+0.9pp (66/301) · p+6.6pp cap82.3 net+1221/med+5.2 | ▼i-3.6pp (139/794) · p+2.8pp cap48.2 net-758/med+0.2 |
| london | ▲i+10.1pp (35/112) · p+0.5pp cap84.4 net+267/med+1.2 | ▼i-6.5pp (45/274) · p+3.2pp cap57.9 net-123/med+0.9 |
| overlap | ▼i-3.4pp (2/20) · p-13.7pp cap84.7 net+3/med+13.2 | ·i-1.9pp (18/118) · p-4.1pp cap59.7 net+111/med+0.7 |
| ny_only | ▼i-10.6pp (4/47) · p+9.8pp cap83.3 net+89/med+1.0 | ▼i-2.1pp (16/107) · p-6.3pp cap53.3 net+98/med-0.1 |
| dead | ▲i+10.1pp (12/34) · p+7.1pp cap86.7 net+169/med+5.3 | ▼i-6.8pp (11/49) · p-2.7pp cap20.2 net+99/med+3.5 |
| asia | ▼i-8.1pp (13/88) · p+14.9pp cap82.1 net+693/med+16.2 | ·i-0.8pp (49/246) · p+5.4pp cap38.0 net-943/med-2.7 |

- backtest payoff: right +7407 / wrong -6186 / net +1221 pts; median per fire +5.20 (n=301)
- backtest best call: 2026-07-30 00:35 +150.2pts remaining (episode 237.6pts, major)
- backtest worst false alarm: 2026-07-29 19:32 -168.0pts adverse
- forward payoff: right +10546 / wrong -11304 / net -758 pts; median per fire +0.25 (n=794)
- forward best call: 2026-09-08 23:27 +362.2pts remaining (episode 362.9pts, major)
- forward worst false alarm: 2026-09-15 06:57 -223.1pts adverse
- earliness (backtest): median 57.9 pts of move remaining at fire (n=22)

### H12 — 1 signal
*A zone showing repeated visits with elevated volume, diminishing range-per-unit-volume, and drying pullback volume precedes a directional move away from the zone in the absorber's direction.*
Grading: directional. Latest review: keep-watching (recommendation).

**S0-H12** — session × window grid (cells as in the matrix):

| session | backtest | forward |
|---|---|---|
| whole | — | — |
| london | — | — |
| overlap | — | — |
| ny_only | — | — |
| dead | — | — |
| asia | — | — |


### H13 — 1 signal
*After price breaks out of the session value area on declining volume and reclaims it on expanding volume, it continues toward the far side of the value area.*
Grading: directional. Latest review: keep-watching (recommendation).

**S0-H13** — session × window grid (cells as in the matrix):

| session | backtest | forward |
|---|---|---|
| whole | (°▼i-4.3pp (1/6) · p+59.7pp cap74.2 net+397/med+58.7) | (°▼i-14.9pp (1/16) · p+6.7pp cap44.6 net+44/med+4.3) |
| london | (°▼i-21.1pp (0/2) · p+73.7pp cap116.8 net+181/med+90.7) | (°▼i-8.6pp (1/7) · p-11.3pp cap66.9 net-42/med-9.9) |
| overlap | — | (°▼i-17.2pp (0/3) · p+8.0pp cap44.6 net-27/med-31.9) |
| ny_only | — | (°▼i-17.1pp (0/3) · p-7.2pp cap— net+18/med+7.8) |
| dead | (°▼i-25.2pp (0/1) · p+83.6pp cap74.2 net+51/med+51.0) | (°▼i-29.2pp (0/1) · p+83.0pp cap29.2 net+29/med+29.2) |
| asia | (°▲i+10.4pp (1/3) · p+35.0pp cap78.8 net+164/med+56.1) | (°▼i-20.7pp (0/2) · p+62.7pp cap59.1 net+66/med+32.8) |

- backtest payoff: right +397 / wrong +0 / net +397 pts; median per fire +58.70 (n=6)
- backtest best call: 2026-07-28 02:15 +115.9pts remaining (episode 109.7pts, major)
- backtest worst false alarm: 2026-07-28 02:15 -2.8pts adverse
- forward payoff: right +209 / wrong -165 / net +44 pts; median per fire +4.35 (n=16)
- forward best call: 2026-08-21 09:44 +113.7pts remaining (episode 144.6pts, major)
- forward worst false alarm: 2026-08-26 09:25 -50.0pts adverse
- earliness (backtest): median 115.9 pts of move remaining at fire (n=1)

### H14 — 1 signal
*Counter-trend No Demand / No Supply prints in an established trend mark absorption and precede trend continuation.*
Grading: directional. Latest review: keep-watching (recommendation).

**S0-H14** — session × window grid (cells as in the matrix):

| session | backtest | forward |
|---|---|---|
| whole | ·i-0.6pp (23/113) · p+2.9pp cap53.9 net+312/med+0.5 | ·i-0.8pp (73/359) · p-0.3pp cap28.8 net-284/med-0.4 |
| london | ▼i-2.6pp (5/27) · p-11.5pp cap80.6 net-256/med-4.2 | ▲i+3.1pp (19/73) · p-0.9pp cap58.0 net-150/med-12.2 |
| overlap | (°▼i-13.4pp (0/11) · p-23.7pp cap— net-138/med-20.3) | ▲i+18.8pp (9/25) · p-9.3pp cap57.0 net+50/med+0.0 |
| ny_only | ▼i-10.4pp (2/23) · p+27.6pp cap43.2 net+392/med+21.1 | ▲i+9.2pp (15/57) · p+3.3pp cap37.0 net+138/med+3.4 |
| dead | (°▲i+19.2pp (4/9) · p-16.4pp cap— net-178/med-20.1) | ▼i-14.4pp (9/61) · p-8.8pp cap25.1 net-470/med-1.9 |
| asia | ▲i+5.0pp (12/43) · p+7.8pp cap59.4 net+492/med+8.2 | ▼i-6.0pp (21/143) · p+0.5pp cap24.0 net+148/med+1.4 |

- backtest payoff: right +1733 / wrong -1421 / net +312 pts; median per fire +0.50 (n=113)
- backtest best call: 2026-07-31 04:56 +164.7pts remaining (episode 169.2pts, major)
- backtest worst false alarm: 2026-08-03 06:28 -123.0pts adverse
- forward payoff: right +3120 / wrong -3405 / net -284 pts; median per fire -0.40 (n=359)
- forward best call: 2026-09-08 23:58 +350.4pts remaining (episode 362.9pts, major)
- forward worst false alarm: 2026-09-04 09:35 -93.0pts adverse
- earliness (backtest): median 71.3 pts of move remaining at fire (n=7)

### H15 — 1 signal
*A range sweep followed by aggressive traversal to the opposite boundary continues toward the range's volume center.*
Grading: directional. Latest review: keep-watching (recommendation).

**S0-H15** — session × window grid (cells as in the matrix):

| session | backtest | forward |
|---|---|---|
| whole | — | — |
| london | — | — |
| overlap | — | — |
| ny_only | — | — |
| dead | — | — |
| asia | — | — |


### H16 — 1 signal
*The opening session's direction predicts the closing session's direction.*
Grading: directional. Latest review: keep-watching (recommendation).

**S0-H16** — session × window grid (cells as in the matrix):

| session | backtest | forward |
|---|---|---|
| whole | (°▼i-21.0pp (0/10) · p-3.6pp cap126.3 net+8/med-16.3) | ▼i-8.1pp (3/23) · p-11.5pp cap69.9 net-217/med-4.9 |
| london | — | — |
| overlap | (°▼i-13.4pp (0/10) · p-3.7pp cap126.3 net+8/med-16.3) | ▼i-4.2pp (3/23) · p-12.3pp cap69.9 net-217/med-4.9 |
| ny_only | — | — |
| dead | — | — |
| asia | — | — |

- backtest payoff: right +262 / wrong -254 / net +8 pts; median per fire -16.30 (n=10)
- backtest worst false alarm: 2026-07-27 15:00 -114.5pts adverse
- forward payoff: right +361 / wrong -579 / net -217 pts; median per fire -4.90 (n=23)
- forward best call: 2026-09-08 15:00 +59.3pts remaining (episode 78.8pts)
- forward worst false alarm: 2026-09-14 15:00 -160.8pts adverse

### H17 — 1 signal
*A climax reversal signal followed by absorption within five bars — effort meeting a quiet counter-party — marks a genuine exhaustion turn: the two-chapter story (exhaustion needs absorption to become reversal).*
Grading: directional. Latest review: rows (recommendation).

**S0-H17** — session × window grid (cells as in the matrix):

| session | backtest | forward |
|---|---|---|
| whole | ·i+0.7pp (5/23) · p+6.8pp cap90.2 net+36/med+0.7 | ▲i+3.7pp (34/137) · p+1.0pp cap45.2 net-130/med+0.3 |
| london | (°▼i-21.1pp (0/3) · p+40.4pp cap96.2 net+198/med+78.9) | ▲i+13.5pp (16/44) · p-5.1pp cap64.5 net-444/med-9.1 |
| overlap | — | (°▼i-17.2pp (0/9) · p+8.0pp cap64.5 net-33/med+7.2) |
| ny_only | (°▼i-19.1pp (0/2) · p-11.5pp cap— net-67/med-33.6) | ·i-1.7pp (4/26) · p+0.5pp cap35.6 net+168/med+7.8 |
| dead | (°▲i+14.8pp (2/5) · p+23.6pp cap109.2 net-58/med+0.7) | (°▲i+9.3pp (5/13) · p+6.1pp cap41.4 net-60/med-6.2) |
| asia | (°·i+0.2pp (3/13) · p-8.6pp cap75.2 net-37/med-9.0) | ·i-0.7pp (9/45) · p+2.7pp cap28.6 net+238/med-1.2 |

- backtest payoff: right +670 / wrong -634 / net +36 pts; median per fire +0.70 (n=23)
- backtest best call: 2026-07-28 23:06 +114.4pts remaining (episode 208.8pts, major)
- backtest worst false alarm: 2026-07-28 23:06 -138.5pts adverse
- forward payoff: right +1743 / wrong -1873 / net -130 pts; median per fire +0.30 (n=137)
- forward best call: 2026-09-11 02:50 +220.9pts remaining (episode 237.1pts, major)
- forward worst false alarm: 2026-09-10 11:58 -158.5pts adverse
- earliness (backtest): median 105.3 pts of move remaining at fire (n=4)

### H18 — 1 signal
*A gap-traversal signal followed by a same-direction effortless print within five bars — travel meeting no opposition — continues: the map says vacuum, the tape confirms no resistance.*
Grading: directional. Latest review: rows (recommendation).

**S0-H18** — session × window grid (cells as in the matrix):

| session | backtest | forward |
|---|---|---|
| whole | (°·i-1.0pp (3/15) · p-10.3pp cap102.0 net-232/med-14.3) | ▼i-4.7pp (20/122) · p+3.4pp cap49.6 net-425/med-4.5 |
| london | (°▼i-21.1pp (0/3) · p+7.0pp cap135.4 net-19/med-38.6) | ▼i-2.6pp (15/74) · p-2.6pp cap55.6 net-290/med-7.1 |
| overlap | (°▼i-13.4pp (0/6) · p-23.7pp cap— net-52/med-6.5) | (°▼i-17.2pp (0/10) · p-15.3pp cap88.8 net+74/med-5.8) |
| ny_only | — | (°▲i+11.5pp (2/7) · p-7.2pp cap— net-113/med-4.7) |
| dead | (°▲i+74.8pp (1/1) · p-16.4pp cap— net-14/med-14.3) | (°▼i-29.2pp (0/2) · p-17.0pp cap— net-2/med-0.8) |
| asia | (°▲i+17.1pp (2/5) · p-11.7pp cap68.5 net-146/med-6.4) | ▼i-10.4pp (3/29) · p+17.9pp cap33.0 net-95/med+0.0 |

- backtest payoff: right +233 / wrong -464 / net -232 pts; median per fire -14.30 (n=15)
- backtest best call: 2026-08-03 05:12 +128.8pts remaining (episode 144.6pts, major)
- backtest worst false alarm: 2026-07-31 06:36 -175.9pts adverse
- forward payoff: right +1599 / wrong -2023 / net -425 pts; median per fire -4.45 (n=122)
- forward best call: 2026-08-21 09:44 +113.7pts remaining (episode 144.6pts, major)
- forward worst false alarm: 2026-09-09 09:15 -142.4pts adverse
- earliness (backtest): median 70.1 pts of move remaining at fire (n=2)

### H19 — 1 signal
*A probe-failure reversal signal followed by continued wide-loud effort in the anchor bar's own close direction within five bars is NOT the start of the claimed reversal — a SUPPRESSION/FADE configuration, and it says so.*
Grading: directional. Latest review: rows (recommendation).

- Question **Q1-H19**: see the register entry (status there is authoritative).
**S0-H19** — session × window grid (cells as in the matrix):

| session | backtest | forward |
|---|---|---|
| whole | ▼i-4.0pp (25/147) · p+5.0pp cap74.2 net+179/med+3.6 | ▲i+3.7pp (100/403) · p-4.6pp cap52.5 net+226/med-1.0 |
| london | (°▼i-10.0pp (1/9) · p-26.3pp cap— net-51/med-14.3) | ▲i+14.6pp (39/104) · p-8.3pp cap71.5 net-382/med-5.2 |
| overlap | (°·i+0.9pp (1/7) · p+47.7pp cap75.9 net+81/med+40.1) | (°▲i+12.2pp (5/17) · p+4.1pp cap58.7 net+197/med+4.8) |
| ny_only | ▼i-12.0pp (3/42) · p+31.4pp cap80.8 net+903/med+21.6 | ▼i-3.6pp (14/104) · p+3.4pp cap47.7 net+487/med+3.4 |
| dead | ▼i-2.5pp (10/44) · p-5.0pp cap58.4 net-463/med-4.3 | ▲i+4.1pp (17/51) · p+4.6pp cap36.8 net+59/med+0.2 |
| asia | ·i-0.7pp (10/45) · p-0.6pp cap64.8 net-291/med+10.6 | ·i-1.0pp (25/127) · p-9.7pp cap38.6 net-135/med-3.8 |

- backtest payoff: right +3647 / wrong -3468 / net +179 pts; median per fire +3.60 (n=147)
- backtest best call: 2026-07-30 00:50 +147.0pts remaining (episode 237.6pts, major)
- backtest worst false alarm: 2026-07-29 18:59 -189.5pts adverse
- forward payoff: right +4831 / wrong -4605 / net +226 pts; median per fire -1.00 (n=403)
- forward best call: 2026-09-11 02:42 +227.5pts remaining (episode 237.1pts, major)
- forward worst false alarm: 2026-09-01 07:56 -215.0pts adverse
- earliness (backtest): median 93.6 pts of move remaining at fire (n=14)

### H20 — 1 signal
*A wide-bar close-through of a session extreme (the same conditioned wide-bar class the retest anchor fires on; resolution = the close beyond the level, not a rejection back inside) initiates continuation in the break direction.*
Grading: directional. Latest review: rows (recommendation).

**S0-H20** — session × window grid (cells as in the matrix):

| session | backtest | forward |
|---|---|---|
| whole | ▼i-13.9pp (0/35) · p+2.8pp cap57.7 [cls 34.3%/13.9%i] net-450/med-4.3 | ▼i-7.5pp (8/148) · p+4.3pp cap55.8 [cls 41.6%/12.9%i] net+813/med+4.5 |
| london | (°▼i-9.9pp (0/19) · p+7.0pp cap61.4 [cls 35.1%/9.9%i] net+20/med+11.4) | ▼i-7.6pp (3/81) · p+9.4pp cap74.2 [cls 40.0%/11.3%i] net+1057/med+8.5 |
| overlap | (°▼i-13.5pp (0/3) · p-27.9pp cap— [cls 27.9%/13.5%i] net-186/med-32.7) | ▼i-19.8pp (0/20) · p-3.1pp cap57.7 [cls 28.1%/19.8%i] net-225/med-6.2 |
| ny_only | — | (°▲i+35.7pp (4/9) · p-8.3pp cap— [cls 8.3%/8.7%i] net+91/med+7.3) |
| dead | (°▼i-12.5pp (0/3) · p+8.3pp cap44.1 [cls 25.0%/12.5%i] net-286/med-97.1) | — |
| asia | (°▼i-20.4pp (0/10) · p+3.6pp cap71.0 [cls 36.4%/20.4%i] net+2/med+8.8) | ▼i-11.3pp (1/38) · p+10.7pp cap31.7 [cls 49.8%/13.9%i] net-110/med-1.1 |

- backtest payoff: right +504 / wrong -954 / net -450 pts; median per fire -4.30 (n=35)
- backtest worst false alarm: 2026-07-27 13:49 -141.5pts adverse
- forward payoff: right +2943 / wrong -2130 / net +813 pts; median per fire +4.55 (n=148)
- forward best call: 2026-09-01 16:31 +103.9pts remaining (episode 85.5pts)
- forward worst false alarm: 2026-09-04 06:13 -116.2pts adverse


---

# nas100 (nas100fut) — CANONICAL

Store span (1M, close ts): 2026-07-19 22:02:00+00:00 → 2026-09-16 16:07:00+00:00. Volume type: real futures volume (register 40 first-sync sanity; canonical verdict at this instrument's validation evening).

## Summary Matrix (page 1)

Engine `8effbb323` — OBSERVATIONAL signal scoreboard - move-detection, not trading; no fills exist here by construction; never validation (docs/hypothesis_lifecycle.md stage 4)

**Review labels are RECOMMENDATIONS — none actioned, review pending operator familiarity.** Cells: marker + precision LIFT vs that context's OWN chance rate, (hits/fires), payoff net/median points (directional rows; either-direction rows have no payoff by construction). ▲/▼ = beyond ±2pp of chance, · = within. (°…) = small-n (fires<20 or episodes<10): dimmed, excluded from any future label arithmetic. Read READING_GUIDE.md first; full detail in hypothesis_performance.json.

| H | label | backtest whole | backtest london | forward whole | forward london |
|---|---|---|---|---|---|
| *context* | | 113 ep; chance 22.0%dir/41.6%either | 41 ep; chance 30.9%dir/55.9%either | 242 ep; chance 24.0%dir/45.7%either | 71 ep; chance 32.1%dir/59.6%either |
| S0-H1 | keep-watching | ·i-0.9pp (7/34) · p+19.2pp cap182.2 net+122/med-15.7 | (°▲i+11.7pp (3/8) · p-18.4pp cap153.6 net-257/med-46.2) | ▲i+4.8pp (38/142) · p+9.1pp cap82.1 net+355/med+4.8 | ▲i+9.5pp (24/71) · p+0.3pp cap96.5 net-304/med-1.8 |
| S1-H1 | keep-watching | (°▲i+11.8pp (1/3) · p+44.7pp cap279.0 net+465/med+128.4) | — | (°▲i+28.0pp (5/10) · p+16.0pp cap80.1 net+215/med+23.6) | (°▲i+50.7pp (3/4) · p-7.1pp cap74.3 net+89/med+8.1) |
| S0-H2 | promote-candidate | ▼i-3.1pp (59/320) · p-2.3pp cap157.6 net-3528/med-1.4 | ·i+1.3pp (16/59) · p-5.5pp cap106.7 net-313/med-30.0 | ▼i-4.8pp (112/650) · p+6.9pp cap83.2 net+2096/med+2.5 | ▼i-3.4pp (49/234) · p+6.4pp cap88.7 net+879/med+3.5 |
| S1-H2 | promote-candidate | ▼i-2.6pp (42/222) · p-1.3pp cap142.3 net-1379/med-4.2 | ▲i+4.4pp (13/43) · p-3.0pp cap101.9 net-382/med-31.5 | ▼i-2.5pp (89/457) · p+6.0pp cap85.5 net+1191/med+3.3 | ·i-1.4pp (36/157) · p+6.1pp cap90.1 net+263/med+6.4 |
| S0-H3 | keep-watching | (°▼i-21.5pp (0/1) · p+78.0pp cap105.8 net+106/med+105.8) | (°▼i-25.8pp (0/1) · p+69.1pp cap105.8 net+106/med+105.8) | (°▼i-22.0pp (0/3) · p+9.3pp cap61.8 net+42/med-1.1) | (°▼i-24.3pp (0/1) · p-32.1pp cap— net-10/med-9.6) |
| S0-H4 | keep-watching | — | — | (°▼i-22.0pp (0/10) · p+36.0pp cap38.4 net-18/med-7.4) | (°▼i-24.3pp (0/5) · p+7.9pp cap31.1 net+26/med+9.5) |
| S0-H5 | keep-watching | — | — | — | — |
| S0-H6 | keep-watching | ▲i+4.5pp (5/29) · p-8.2pp cap260.8 [cls 39.2%/12.7%i] net-232/med-11.8 | (°▲i+60.0pp (4/5) · p-38.6pp cap— [cls 38.6%/20.0%i] net-719/med-105.3) | ▲i+4.4pp (31/154) · p+6.8pp cap103.0 [cls 36.7%/15.7%i] net+2179/med+10.7 | ▲i+7.4pp (17/59) · p+6.7pp cap90.7 [cls 35.7%/21.4%i] net+548/med+15.1 |
| S0-H7 | keep-watching | ▼i-5.5pp (8/50) · p+0.0pp cap169.0 net+77/med-7.8 | (°·i-0.8pp (4/16) · p-5.9pp cap123.6 net-167/med-6.6) | ▼i-2.1pp (29/146) · p+4.8pp cap79.7 net+805/med+9.3 | ·i+0.7pp (10/40) · p+10.4pp cap90.7 net+828/med+10.1 |
| S0-H7 (either-dir) | keep-watching | ▼i-10.1pp (15/50) · p+4.4pp cap46.5 | (°▲i+2.6pp (8/16) · p+0.3pp cap23.3) | ▼i-5.9pp (51/146) · p+9.1pp cap43.3 | ·i+1.9pp (19/40) · p+12.9pp cap55.0 |
| S0-H8 | keep-watching | ▼i-3.5pp (117/320) · p+1.8pp cap64.9 | ▼i-6.7pp (24/59) · p+3.4pp cap48.5 | ·i-1.4pp (256/650) · p+6.3pp cap58.5 | ▼i-2.4pp (101/234) · p+4.9pp cap64.7 |
| S0-H9 | keep-watching | ▲i+2.4pp (21/88) · p+0.7pp cap129.2 net+593/med-4.3 | (°▼i-25.8pp (0/9) · p+2.4pp cap76.3 net+410/med+11.6) | ·i-0.4pp (48/222) · p-6.0pp cap53.9 net-601/med-6.5 | ▲i+3.8pp (9/32) · p+5.4pp cap76.0 net+131/med-14.4 |
| S1-H9 | keep-watching | ▼i-13.5pp (2/25) · p+6.0pp cap265.9 net-373/med+10.8 | (°▼i-25.8pp (0/5) · p-30.9pp cap— net-57/med+2.3) | ▼i-12.3pp (3/31) · p-11.1pp cap86.7 net-447/med+9.8 | (°·i+0.7pp (2/8) · p-7.1pp cap152.0 net-278/med-13.3) |
| S0-H10 | deprioritize | ·i-0.9pp (36/175) · p-6.6pp cap96.7 net+2743/med+15.3 | (°▼i-12.5pp (2/15) · p-17.6pp cap46.2 net-356/med-1.7) | ▼i-7.4pp (87/597) · p-2.9pp cap49.9 net-3578/med-4.8 | ▼i-3.2pp (28/133) · p+4.0pp cap48.5 net-815/med-5.0 |
| S0-H11 | keep-watching | ▼i-3.2pp (48/263) · p+2.0pp cap136.2 net+863/med+0.9 | ·i-1.6pp (22/91) · p-2.3pp cap113.7 net+264/med-3.9 | ▼i-5.0pp (120/706) · p+3.3pp cap82.0 net+2392/med+0.5 | ▼i-2.2pp (51/231) · p+6.4pp cap91.4 net+2031/med-0.7 |
| S1-H11 | keep-watching | ▼i-8.3pp (23/174) · p+5.0pp cap130.1 net+293/med-14.1 | ·i+0.6pp (14/53) · p-2.6pp cap109.7 net-436/med-14.7 | ·i+1.1pp (180/778) · p+2.0pp cap73.7 net-2241/med-3.3 | ·i+1.3pp (57/223) · p-2.1pp cap88.2 net+14/med-2.0 |
| S0-H12 | keep-watching | — | — | — | — |
| S0-H13 | keep-watching | (°▼i-21.5pp (0/1) · p+78.0pp cap95.7 net+93/med+93.0) | (°▼i-25.8pp (0/1) · p+69.1pp cap95.7 net+93/med+93.0) | (°·i+0.2pp (2/9) · p-12.9pp cap29.4 net-286/med-33.0) | (°▼i-24.3pp (0/1) · p-32.1pp cap— net-43/med-42.8) |
| S0-H14 | keep-watching | ·i+0.7pp (37/167) · p-13.6pp cap70.2 net-692/med+6.9 | ▼i-10.4pp (4/26) · p-19.4pp cap41.8 net-1762/med-17.1 | ▼i-5.4pp (100/602) · p-6.9pp cap53.5 net-4121/med-4.5 | ▼i-4.1pp (23/114) · p-3.2pp cap67.9 net-68/med-5.2 |
| S0-H15 | keep-watching | — | — | — | — |
| S0-H16 | keep-watching | (°▼i-11.5pp (1/10) · p+28.0pp cap121.0 net+274/med+0.1) | — | ▼i-13.7pp (2/24) · p+5.2pp cap74.5 net+277/med+10.0 | — |
| S0-H17 | rows | (°▼i-8.2pp (2/15) · p+18.0pp cap166.0 net+681/med+10.2) | (°▼i-5.8pp (1/5) · p+9.1pp cap125.1 net-18/med-23.3) | ·i-0.2pp (17/78) · p+6.8pp cap82.8 net-125/med+6.4 | ▲i+7.1pp (11/35) · p-3.5pp cap85.9 net-373/med-4.6 |
| S0-H18 | rows | ▼i-7.7pp (8/58) · p-8.2pp cap127.3 net-1784/med-23.8 | ▲i+3.4pp (7/24) · p-22.6pp cap111.1 net-559/med-16.3 | ▼i-4.2pp (23/129) · p+3.9pp cap103.5 net+540/med+1.5 | ·i+0.0pp (9/37) · p+8.4pp cap104.2 net+25/med-11.6 |
| S0-H19 | rows | ·i-1.9pp (40/204) · p+1.0pp cap180.0 net+1513/med+6.5 | ▼i-15.3pp (4/38) · p-2.0pp cap98.9 net-152/med+12.8 | ▲i+3.0pp (98/392) · p-0.3pp cap86.6 net-1100/med-2.2 | ▲i+2.0pp (36/137) · p-5.1pp cap99.6 net-1278/med-3.4 |
| S0-H20 | rows | ▼i-10.5pp (1/46) · p+8.6pp cap277.1 [cls 39.2%/12.7%i] net+1398/med+2.9 | (°▲i+13.3pp (1/3) · p-38.6pp cap— [cls 38.6%/20.0%i] net-182/med-90.2) | ▼i-11.0pp (6/127) · p+2.7pp cap84.0 [cls 36.7%/15.7%i] net+271/med-4.4 | ▼i-14.6pp (4/59) · p+1.6pp cap105.5 [cls 35.7%/21.4%i] net+1170/med-1.0 |
| **union coverage** | | 46.0% (52/113) | 39.0% (16/41) | 77.7% (188/242) | 81.7% (58/71) |

Not graded:  — see register entries.

## Hypothesis Cards (page 2)

### H1 — 2 signals
*A climactic bar — extreme volume on a wide spread late in an extended move — marks exhaustion, and price then reverses against the climax direction.*
Grading: directional. Latest review: keep-watching (recommendation).

- Question **Q1-H1**: see the register entry (status there is authoritative).
**S0-H1** — session × window grid (cells as in the matrix):

| session | backtest | forward |
|---|---|---|
| whole | ·i-0.9pp (7/34) · p+19.2pp cap182.2 net+122/med-15.7 | ▲i+4.8pp (38/142) · p+9.1pp cap82.1 net+355/med+4.8 |
| london | (°▲i+11.7pp (3/8) · p-18.4pp cap153.6 net-257/med-46.2) | ▲i+9.5pp (24/71) · p+0.3pp cap96.5 net-304/med-1.8 |
| overlap | — | (°▼i-9.8pp (0/3) · p-33.5pp cap— net-150/med-58.0) |
| ny_only | (°▼i-19.0pp (0/11) · p+50.5pp cap246.0 net-215/med-87.5) | (°▼i-5.8pp (2/15) · p-2.2pp cap93.8 net+150/med+14.9) |
| dead | (°▲i+31.5pp (4/8) · p+0.9pp cap406.7 net-181/med-23.6) | ▲i+2.1pp (9/33) · p+27.5pp cap78.0 net+462/med+20.1 |
| asia | (°▼i-24.3pp (0/7) · p+51.7pp cap178.9 net+776/med+154.4) | ▼i-8.7pp (3/20) · p+18.0pp cap75.3 net+196/med+11.8 |

- backtest payoff: right +2899 / wrong -2777 / net +122 pts; median per fire -15.65 (n=34)
- backtest best call: 2026-07-29 18:02 +663.1pts remaining (episode 663.1pts, major)
- backtest worst false alarm: 2026-07-29 19:01 -712.5pts adverse
- forward payoff: right +3722 / wrong -3368 / net +355 pts; median per fire +4.85 (n=142)
- forward best call: 2026-08-20 09:43 +293.2pts remaining (episode 306.7pts, major)
- forward worst false alarm: 2026-09-11 12:32 -191.9pts adverse
- earliness (backtest): median 183.0 pts of move remaining at fire (n=8)

**S1-H1** — session × window grid (cells as in the matrix):

| session | backtest | forward |
|---|---|---|
| whole | (°▲i+11.8pp (1/3) · p+44.7pp cap279.0 net+465/med+128.4) | (°▲i+28.0pp (5/10) · p+16.0pp cap80.1 net+215/med+23.6) |
| london | — | (°▲i+50.7pp (3/4) · p-7.1pp cap74.3 net+89/med+8.1) |
| overlap | — | — |
| ny_only | — | — |
| dead | (°▲i+31.5pp (1/2) · p+38.4pp cap406.7 net+337/med+168.5) | (°▼i-25.2pp (0/3) · p+85.1pp cap86.0 net+190/med+52.2) |
| asia | (°▼i-24.3pp (0/1) · p+80.3pp cap151.3 net+128/med+128.4) | (°▲i+43.0pp (2/3) · p-27.0pp cap— net-64/med-44.6) |

- backtest payoff: right +521 / wrong -56 / net +465 pts; median per fire +128.40 (n=3)
- backtest best call: 2026-07-28 23:45 +372.3pts remaining (episode 501.5pts, major)
- backtest worst false alarm: 2026-07-28 23:45 -141.6pts adverse
- forward payoff: right +313 / wrong -98 / net +215 pts; median per fire +23.65 (n=10)
- forward best call: 2026-09-09 09:56 +192.9pts remaining (episode 212.5pts, major)
- forward worst false alarm: 2026-09-11 04:52 -51.8pts adverse
- earliness (backtest): median 372.3 pts of move remaining at fire (n=1)

### H2 — 2 signals
*A failed probe beyond a prior extreme — an upthrust above or spring below that closes back inside — reverses against the probe.*
Grading: directional. Latest review: promote-candidate (recommendation).

**S0-H2** — session × window grid (cells as in the matrix):

| session | backtest | forward |
|---|---|---|
| whole | ▼i-3.1pp (59/320) · p-2.3pp cap157.6 net-3528/med-1.4 | ▼i-4.8pp (112/650) · p+6.9pp cap83.2 net+2096/med+2.5 |
| london | ·i+1.3pp (16/59) · p-5.5pp cap106.7 net-313/med-30.0 | ▼i-3.4pp (49/234) · p+6.4pp cap88.7 net+879/med+3.5 |
| overlap | (°▼i-4.8pp (1/32) · p-12.5pp cap193.4 net-742/med-38.1) | ▼i-9.8pp (0/30) · p-0.2pp cap154.9 net+490/med+12.9 |
| ny_only | ▼i-9.1pp (7/71) · p+2.4pp cap234.9 net-3199/med-7.4 | ▼i-8.6pp (8/76) · p+2.9pp cap111.7 net+101/med+0.7 |
| dead | ·i+0.3pp (9/48) · p+5.1pp cap284.2 net+874/med+2.4 | ▼i-5.6pp (18/92) · p+13.4pp cap81.7 net+218/med+0.3 |
| asia | ·i-0.7pp (26/110) · p-0.6pp cap116.8 net-147/med+10.2 | ▼i-6.7pp (37/218) · p+3.3pp cap67.4 net+408/med+3.5 |

- backtest payoff: right +13405 / wrong -16933 / net -3528 pts; median per fire -1.35 (n=320)
- backtest best call: 2026-07-30 07:00 +812.7pts remaining (episode 832.8pts, major)
- backtest worst false alarm: 2026-07-29 19:00 -719.1pts adverse
- forward payoff: right +16765 / wrong -14669 / net +2096 pts; median per fire +2.55 (n=650)
- forward best call: 2026-08-21 11:28 +288.7pts remaining (episode 309.6pts, major)
- forward worst false alarm: 2026-08-19 12:55 -322.0pts adverse
- earliness (backtest): median 111.3 pts of move remaining at fire (n=25)

**S1-H2** — session × window grid (cells as in the matrix):

| session | backtest | forward |
|---|---|---|
| whole | ▼i-2.6pp (42/222) · p-1.3pp cap142.3 net-1379/med-4.2 | ▼i-2.5pp (89/457) · p+6.0pp cap85.5 net+1191/med+3.3 |
| london | ▲i+4.4pp (13/43) · p-3.0pp cap101.9 net-382/med-31.5 | ·i-1.4pp (36/157) · p+6.1pp cap90.1 net+263/med+6.4 |
| overlap | (°▼i-7.9pp (0/20) · p-2.5pp cap185.1 net+164/med+49.0) | ▼i-9.8pp (0/25) · p+2.5pp cap153.4 net+441/med+17.4 |
| ny_only | ▼i-10.7pp (4/48) · p-0.6pp cap194.2 net-1585/med-19.9 | ▼i-6.8pp (7/57) · p+3.4pp cap91.3 net-22/med+0.5 |
| dead | ▲i+2.7pp (7/33) · p+0.5pp cap206.8 net+152/med-7.9 | ▼i-2.6pp (14/62) · p+7.7pp cap83.9 net-91/med-2.9 |
| asia | ·i-1.2pp (18/78) · p+2.1pp cap106.9 net+272/med+15.2 | ▼i-3.2pp (32/156) · p+3.1pp cap68.2 net+601/med+3.5 |

- backtest payoff: right +8973 / wrong -10352 / net -1379 pts; median per fire -4.15 (n=222)
- backtest best call: 2026-07-30 07:00 +812.7pts remaining (episode 832.8pts, major)
- backtest worst false alarm: 2026-07-29 19:16 -700.8pts adverse
- forward payoff: right +11804 / wrong -10613 / net +1191 pts; median per fire +3.30 (n=457)
- forward best call: 2026-08-21 11:28 +288.7pts remaining (episode 309.6pts, major)
- forward worst false alarm: 2026-08-19 13:09 -291.0pts adverse
- earliness (backtest): median 118.9 pts of move remaining at fire (n=23)

### H3 — 1 signal
*Repeated absorption — high effort with no result — at a price level precedes a breakout through that level.*
Grading: directional. Latest review: keep-watching (recommendation).

**S0-H3** — session × window grid (cells as in the matrix):

| session | backtest | forward |
|---|---|---|
| whole | (°▼i-21.5pp (0/1) · p+78.0pp cap105.8 net+106/med+105.8) | (°▼i-22.0pp (0/3) · p+9.3pp cap61.8 net+42/med-1.1) |
| london | (°▼i-25.8pp (0/1) · p+69.1pp cap105.8 net+106/med+105.8) | (°▼i-24.3pp (0/1) · p-32.1pp cap— net-10/med-9.6) |
| overlap | — | — |
| ny_only | — | — |
| dead | — | — |
| asia | — | (°▼i-23.7pp (0/2) · p+23.0pp cap61.8 net+51/med+25.7) |

- backtest payoff: right +106 / wrong +0 / net +106 pts; median per fire +105.80 (n=1)
- forward payoff: right +52 / wrong -11 / net +42 pts; median per fire -1.10 (n=3)
- forward worst false alarm: 2026-08-25 01:40 -42.8pts adverse

### H4 — 1 signal
*In an established trend, a quiet (low-volume) pullback resolves with trend resumption.*
Grading: directional. Latest review: keep-watching (recommendation).

**S0-H4** — session × window grid (cells as in the matrix):

| session | backtest | forward |
|---|---|---|
| whole | — | (°▼i-22.0pp (0/10) · p+36.0pp cap38.4 net-18/med-7.4) |
| london | — | (°▼i-24.3pp (0/5) · p+7.9pp cap31.1 net+26/med+9.5) |
| overlap | — | — |
| ny_only | — | — |
| dead | — | — |
| asia | — | (°▼i-23.7pp (0/5) · p+53.0pp cap44.3 net-44/med-8.1) |

- forward payoff: right +65 / wrong -83 / net -18 pts; median per fire -7.40 (n=10)
- forward worst false alarm: 2026-08-17 06:55 -54.5pts adverse

### H5 — 1 signal
*A buying climax that extends far above its trend mean mean-reverts (climax-extension fade; registered short-side only).*
Grading: directional. Latest review: keep-watching (recommendation).

**S0-H5** — session × window grid (cells as in the matrix):

| session | backtest | forward |
|---|---|---|
| whole | — | — |
| london | — | — |
| overlap | — | — |
| ny_only | — | — |
| dead | — | — |
| asia | — | — |


### H6 — 1 signal
*A wide-spread rejection bar at a session extreme (measured day-relative, volume-agnostic) reverses away from the extreme.*
Grading: directional. Latest review: keep-watching (recommendation).

- Question **Q1-H6**: see the register entry (status there is authoritative).
- Question **Q2-H6**: see the register entry (status there is authoritative).
- Question **Q3-H6**: see the register entry (status there is authoritative).
**S0-H6** — session × window grid (cells as in the matrix):

| session | backtest | forward |
|---|---|---|
| whole | ▲i+4.5pp (5/29) · p-8.2pp cap260.8 [cls 39.2%/12.7%i] net-232/med-11.8 | ▲i+4.4pp (31/154) · p+6.8pp cap103.0 [cls 36.7%/15.7%i] net+2179/med+10.7 |
| london | (°▲i+60.0pp (4/5) · p-38.6pp cap— [cls 38.6%/20.0%i] net-719/med-105.3) | ▲i+7.4pp (17/59) · p+6.7pp cap90.7 [cls 35.7%/21.4%i] net+548/med+15.1 |
| overlap | (°·i-1.8pp (1/20) · p-7.3pp cap263.9 [cls 47.3%/6.8%i] net+333/med+9.0) | ·i+0.9pp (5/59) · p+7.4pp cap112.7 [cls 45.1%/7.6%i] net+1532/med+35.6 |
| ny_only | — | (°▼i-10.8pp (0/3) · p-6.7pp cap— [cls 6.7%/10.8%i] net-55/med-30.7) |
| dead | (°▼i-13.5pp (0/3) · p-23.8pp cap— [cls 23.8%/13.5%i] net+42/med+18.9) | (°▲i+6.7pp (1/5) · p+5.4pp cap78.4 [cls 34.6%/13.3%i] net+27/med+15.9) |
| asia | (°▼i-17.7pp (0/1) · p+75.0pp cap129.0 [cls 25.0%/17.7%i] net+112/med+111.8) | ▲i+10.5pp (8/28) · p-0.2pp cap99.7 [cls 32.3%/18.1%i] net+126/med-4.6 |

- backtest payoff: right +1875 / wrong -2108 / net -232 pts; median per fire -11.80 (n=29)
- backtest best call: 2026-08-03 11:04 +303.5pts remaining (episode 396.3pts, major)
- backtest worst false alarm: 2026-07-27 13:46 -514.5pts adverse
- forward payoff: right +5795 / wrong -3616 / net +2179 pts; median per fire +10.65 (n=154)
- forward best call: 2026-09-09 10:08 +180.8pts remaining (episode 212.5pts, major)
- forward worst false alarm: 2026-09-03 14:34 -231.0pts adverse
- earliness (backtest): median 78.8 pts of move remaining at fire (n=2)

### H7 — 1 signal
*Quiet decline at a session extreme is disguised accumulation: effortless (low-volume) weakness reverses UP once selling fails to attract participation (mirror: quiet advance at a high reverses down).*
Grading: directional + either-direction (dual). Latest review: keep-watching (recommendation).

- Question **Q1-H7**: see the register entry (status there is authoritative).
**S0-H7** — session × window grid (cells as in the matrix):

| session | backtest | forward |
|---|---|---|
| whole | ▼i-5.5pp (8/50) · p+0.0pp cap169.0 net+77/med-7.8 | ▼i-2.1pp (29/146) · p+4.8pp cap79.7 net+805/med+9.3 |
| london | (°·i-0.8pp (4/16) · p-5.9pp cap123.6 net-167/med-6.6) | ·i+0.7pp (10/40) · p+10.4pp cap90.7 net+828/med+10.1 |
| overlap | (°▲i+4.6pp (1/8) · p+25.0pp cap183.1 net+464/med+8.3) | (°▼i-9.8pp (0/17) · p+7.7pp cap118.0 net+219/med+22.9) |
| ny_only | (°▲i+6.0pp (2/8) · p-13.1pp cap— net-76/med-18.5) | ▼i-3.1pp (4/25) · p-4.9pp cap107.5 net+37/med+10.0 |
| dead | (°·i+1.5pp (1/5) · p-11.6pp cap— net+53/med+23.0) | (°▼i-16.1pp (1/11) · p-5.8pp cap71.3 net-82/med+5.3) |
| asia | (°▼i-24.3pp (0/13) · p-4.3pp cap142.4 net-196/med-24.5) | ▲i+2.7pp (14/53) · p+3.2pp cap55.6 net-198/med+6.0 |

- backtest payoff: right +2351 / wrong -2274 / net +77 pts; median per fire -7.75 (n=50)
- backtest best call: 2026-07-29 09:26 +577.3pts remaining (episode 632.8pts, major)
- backtest worst false alarm: 2026-07-31 13:43 -365.8pts adverse
- forward payoff: right +4054 / wrong -3249 / net +805 pts; median per fire +9.35 (n=146)
- forward best call: 2026-09-14 04:40 +206.3pts remaining (episode 216.0pts, major)
- forward worst false alarm: 2026-09-14 13:12 -211.9pts adverse
- earliness (backtest): median 308.2 pts of move remaining at fire (n=7)

**S0-H7 (either-dir)** — session × window grid (cells as in the matrix):

| session | backtest | forward |
|---|---|---|
| whole | ▼i-10.1pp (15/50) · p+4.4pp cap46.5 | ▼i-5.9pp (51/146) · p+9.1pp cap43.3 |
| london | (°▲i+2.6pp (8/16) · p+0.3pp cap23.3) | ·i+1.9pp (19/40) · p+12.9pp cap55.0 |
| overlap | (°▼i-3.3pp (1/8) · p+30.1pp cap118.7) | (°▼i-18.7pp (0/17) · p-8.8pp cap113.3) |
| ny_only | (°·i+0.7pp (3/8) · p-13.1pp cap18.8) | ▼i-11.8pp (6/25) · p-5.8pp cap7.0 |
| dead | (°▼i-14.4pp (1/5) · p-22.3pp cap—) | (°▼i-33.9pp (1/11) · p+8.5pp cap21.8) |
| asia | (°▼i-29.4pp (2/13) · p-0.5pp cap35.7) | ▲i+2.1pp (25/53) · p+13.1pp cap27.3 |

- backtest payoff: n/a by construction (either-direction)
- backtest best call: 2026-07-29 09:26 +577.3pts remaining (episode 632.8pts, major)
- backtest worst false alarm: 2026-07-29 02:54 -123.2pts adverse
- forward payoff: n/a by construction (either-direction)
- forward best call: 2026-09-14 04:40 +206.3pts remaining (episode 216.0pts, major)
- forward worst false alarm: 2026-08-20 14:49 -108.6pts adverse
- earliness (backtest): median 170.9 pts of move remaining at fire (n=14)

### H8 — 1 signal
*Reversal-signature bar anatomy (upthrust/spring) predicts imminent range expansion irrespective of direction.*
Grading: either-direction. Latest review: keep-watching (recommendation).

**S0-H8** — session × window grid (cells as in the matrix):

| session | backtest | forward |
|---|---|---|
| whole | ▼i-3.5pp (117/320) · p+1.8pp cap64.9 | ·i-1.4pp (256/650) · p+6.3pp cap58.5 |
| london | ▼i-6.7pp (24/59) · p+3.4pp cap48.5 | ▼i-2.4pp (101/234) · p+4.9pp cap64.7 |
| overlap | (°▼i-9.6pp (2/32) · p-4.3pp cap69.4) | ▼i-18.7pp (0/30) · p-18.4pp cap128.2 |
| ny_only | ▼i-12.9pp (17/71) · p+18.1pp cap52.0 | ▼i-6.9pp (22/76) · p-0.7pp cap85.5 |
| dead | ▼i-3.2pp (15/48) · p+2.7pp cap133.9 | ▲i+3.7pp (43/92) · p+17.8pp cap60.4 |
| asia | ▲i+8.8pp (59/110) · p-2.6pp cap73.5 | ▼i-3.8pp (90/218) · p+1.7pp cap52.4 |

- backtest payoff: n/a by construction (either-direction)
- backtest best call: 2026-07-30 06:39 +793.0pts remaining (episode 832.8pts, major)
- backtest worst false alarm: 2026-07-29 19:48 -233.6pts adverse
- forward payoff: n/a by construction (either-direction)
- forward best call: 2026-09-03 10:13 +413.8pts remaining (episode 420.0pts, major)
- forward worst false alarm: 2026-08-28 16:07 -114.0pts adverse
- earliness (backtest): median 130.5 pts of move remaining at fire (n=32)

### H9 — 2 signals
*Persistent lower-TF directional pressure that recruits expanding participation at the parent timeframe precedes continuation beyond what the parent label alone predicts; pressure without participation expansion does not.*
Grading: directional. Latest review: keep-watching (recommendation).

- Question **Q2-H9**: see the register entry (status there is authoritative).
**S0-H9** — session × window grid (cells as in the matrix):

| session | backtest | forward |
|---|---|---|
| whole | ▲i+2.4pp (21/88) · p+0.7pp cap129.2 net+593/med-4.3 | ·i-0.4pp (48/222) · p-6.0pp cap53.9 net-601/med-6.5 |
| london | (°▼i-25.8pp (0/9) · p+2.4pp cap76.3 net+410/med+11.6) | ▲i+3.8pp (9/32) · p+5.4pp cap76.0 net+131/med-14.4 |
| overlap | (°▼i-7.9pp (0/10) · p+12.5pp cap306.3 net+540/med+51.3) | ▲i+18.8pp (8/28) · p-19.2pp cap74.4 net-104/med-10.2 |
| ny_only | ▲i+29.0pp (12/25) · p-5.1pp cap125.7 net-148/med-7.0 | ▼i-9.3pp (5/51) · p-5.0pp cap61.4 net-464/med-3.8 |
| dead | (°▲i+5.0pp (4/17) · p+17.8pp cap265.9 net+98/med-5.5) | ▼i-21.2pp (1/25) · p-10.9pp cap78.4 net+96/med-1.3 |
| asia | ▼i-5.8pp (5/27) · p-1.2pp cap78.6 net-307/med-10.2 | ▲i+5.4pp (25/86) · p-2.6pp cap47.1 net-261/med-12.3 |

- backtest payoff: right +3019 / wrong -2427 / net +593 pts; median per fire -4.35 (n=88)
- backtest best call: 2026-08-03 03:30 +174.2pts remaining (episode 209.2pts, major)
- backtest worst false alarm: 2026-07-29 18:45 -500.8pts adverse
- forward payoff: right +3012 / wrong -3613 / net -601 pts; median per fire -6.50 (n=216)
- forward best call: 2026-09-01 05:10 +289.8pts remaining (episode 376.3pts, major)
- forward worst false alarm: 2026-08-19 13:00 -321.5pts adverse
- earliness (backtest): median 116.8 pts of move remaining at fire (n=6)

**S1-H9** — session × window grid (cells as in the matrix):

| session | backtest | forward |
|---|---|---|
| whole | ▼i-13.5pp (2/25) · p+6.0pp cap265.9 net-373/med+10.8 | ▼i-12.3pp (3/31) · p-11.1pp cap86.7 net-447/med+9.8 |
| london | (°▼i-25.8pp (0/5) · p-30.9pp cap— net-57/med+2.3) | (°·i+0.7pp (2/8) · p-7.1pp cap152.0 net-278/med-13.3) |
| overlap | (°▼i-7.9pp (0/1) · p+62.5pp cap306.3 net+150/med+150.3) | — |
| ny_only | (°▼i-19.0pp (0/3) · p-13.1pp cap— net-373/med+63.9) | (°▼i-8.0pp (1/9) · p-8.9pp cap— net-310/med+4.5) |
| dead | (°▼i-18.5pp (0/8) · p+50.9pp cap265.9 net+174/med+55.5) | (°▼i-25.2pp (0/6) · p+1.8pp cap78.4 net+121/med+14.4) |
| asia | (°·i+0.7pp (2/8) · p-7.2pp cap78.6 net-267/med-8.6) | (°▼i-23.7pp (0/8) · p-14.5pp cap52.5 net+19/med+11.8) |

- backtest payoff: right +1181 / wrong -1554 / net -373 pts; median per fire +10.80 (n=25)
- backtest best call: 2026-07-30 03:00 +120.0pts remaining (episode 134.4pts)
- backtest worst false alarm: 2026-07-29 18:45 -500.8pts adverse
- forward payoff: right +672 / wrong -1119 / net -447 pts; median per fire +9.80 (n=29)
- forward best call: 2026-08-19 18:40 +56.7pts remaining (episode 74.5pts)
- forward worst false alarm: 2026-08-19 13:00 -321.5pts adverse
- earliness (backtest): median 120.0 pts of move remaining at fire (n=1)

### H10 — 1 signal
*In an established 1-minute trend, no-demand/no-supply prints in the trend's direction signal continuation.*
Grading: directional. Latest review: deprioritize (recommendation).

**S0-H10** — session × window grid (cells as in the matrix):

| session | backtest | forward |
|---|---|---|
| whole | ·i-0.9pp (36/175) · p-6.6pp cap96.7 net+2743/med+15.3 | ▼i-7.4pp (87/597) · p-2.9pp cap49.9 net-3578/med-4.8 |
| london | (°▼i-12.5pp (2/15) · p-17.6pp cap46.2 net-356/med-1.7) | ▼i-3.2pp (28/133) · p+4.0pp cap48.5 net-815/med-5.0 |
| overlap | (°▼i-7.9pp (0/18) · p-37.5pp cap— net+764/med+45.5) | ▼i-3.6pp (5/80) · p-21.0pp cap102.7 net-1415/med-19.8 |
| ny_only | ·i+1.8pp (10/48) · p-6.9pp cap88.9 net+398/med+12.5 | ·i-0.8pp (15/82) · p+3.3pp cap91.8 net-426/med-5.2 |
| dead | (°▼i-6.0pp (2/16) · p+0.9pp cap254.7 net+551/med+8.9) | ▼i-10.0pp (10/66) · p-10.4pp cap40.5 net-650/med-3.8 |
| asia | ▲i+3.9pp (22/78) · p+5.9pp cap99.4 net+1385/med+15.6 | ▼i-11.4pp (29/236) · p-3.7pp cap45.3 net-272/med-0.1 |

- backtest payoff: right +4792 / wrong -2049 / net +2743 pts; median per fire +15.30 (n=175)
- backtest best call: 2026-08-03 03:44 +199.5pts remaining (episode 209.2pts, major)
- backtest worst false alarm: 2026-07-27 12:56 -252.9pts adverse
- forward payoff: right +7064 / wrong -10642 / net -3578 pts; median per fire -4.80 (n=597)
- forward best call: 2026-09-01 05:05 +287.4pts remaining (episode 376.3pts, major)
- forward worst false alarm: 2026-09-04 11:59 -175.2pts adverse
- earliness (backtest): median 108.5 pts of move remaining at fire (n=7)

### H11 — 2 signals
*Price entering a low-volume price zone traverses it faster than baseline; entering a high-volume node it stalls or reverses at above-baseline rates.*
Grading: directional. Latest review: keep-watching (recommendation).

- Question **Q1-H11**: see the register entry (status there is authoritative).
- Question **Q2-H11**: see the register entry (status there is authoritative).
**S0-H11** — session × window grid (cells as in the matrix):

| session | backtest | forward |
|---|---|---|
| whole | ▼i-3.2pp (48/263) · p+2.0pp cap136.2 net+863/med+0.9 | ▼i-5.0pp (120/706) · p+3.3pp cap82.0 net+2392/med+0.5 |
| london | ·i-1.6pp (22/91) · p-2.3pp cap113.7 net+264/med-3.9 | ▼i-2.2pp (51/231) · p+6.4pp cap91.4 net+2031/med-0.7 |
| overlap | (°▼i-7.9pp (0/20) · p+2.5pp cap232.1 net-137/med-23.4) | ▼i-2.1pp (7/91) · p-4.9pp cap117.7 net-863/med-2.3 |
| ny_only | ▼i-12.1pp (2/29) · p+14.5pp cap229.4 net+826/med+77.1 | ▼i-3.0pp (31/192) · p+0.0pp cap110.0 net+426/med+1.1 |
| dead | ·i-1.3pp (10/58) · p+10.8pp cap98.2 net+874/med-3.1 | ▼i-12.7pp (4/32) · p+10.1pp cap77.2 net+258/med+6.8 |
| asia | ▼i-2.8pp (14/65) · p-7.4pp cap115.2 net-964/med+3.6 | ▼i-6.8pp (27/160) · p+6.1pp cap64.6 net+541/med+0.3 |

- backtest payoff: right +10765 / wrong -9902 / net +863 pts; median per fire +0.90 (n=262)
- backtest best call: 2026-07-30 07:02 +741.2pts remaining (episode 832.8pts, major)
- backtest worst false alarm: 2026-07-29 13:50 -332.3pts adverse
- forward payoff: right +16859 / wrong -14467 / net +2392 pts; median per fire +0.45 (n=706)
- forward best call: 2026-08-24 09:01 +259.2pts remaining (episode 284.5pts, major)
- forward worst false alarm: 2026-09-03 14:41 -264.9pts adverse
- earliness (backtest): median 176.0 pts of move remaining at fire (n=14)

**S1-H11** — session × window grid (cells as in the matrix):

| session | backtest | forward |
|---|---|---|
| whole | ▼i-8.3pp (23/174) · p+5.0pp cap130.1 net+293/med-14.1 | ·i+1.1pp (180/778) · p+2.0pp cap73.7 net-2241/med-3.3 |
| london | ·i+0.6pp (14/53) · p-2.6pp cap109.7 net-436/med-14.7 | ·i+1.3pp (57/223) · p-2.1pp cap88.2 net+14/med-2.0 |
| overlap | (°·i-1.2pp (1/15) · p-10.8pp cap192.0 net-139/med-40.7) | ▼i-6.7pp (2/65) · p+11.1pp cap95.4 net-661/med-5.9 |
| ny_only | ▼i-19.0pp (0/39) · p+10.0pp cap558.0 net+1758/med-19.4 | ▲i+7.3pp (29/110) · p+2.0pp cap80.9 net-220/med-0.7 |
| dead | (°·i-1.8pp (2/12) · p-3.3pp cap141.6 net-253/med+3.9) | ·i-0.7pp (26/106) · p+4.9pp cap78.5 net-215/med+1.9 |
| asia | ▼i-13.4pp (6/55) · p+13.0pp cap124.1 net-637/med-13.4 | ·i+0.4pp (66/274) · p-0.4pp cap55.5 net-1160/med-4.7 |

- backtest payoff: right +9792 / wrong -9499 / net +293 pts; median per fire -14.05 (n=174)
- backtest best call: 2026-07-29 09:17 +555.3pts remaining (episode 632.8pts, major)
- backtest worst false alarm: 2026-07-29 19:07 -730.3pts adverse
- forward payoff: right +15697 / wrong -17938 / net -2241 pts; median per fire -3.30 (n=778)
- forward best call: 2026-09-03 09:58 +396.3pts remaining (episode 420.0pts, major)
- forward worst false alarm: 2026-08-21 12:50 -221.2pts adverse
- earliness (backtest): median 113.5 pts of move remaining at fire (n=11)

### H12 — 1 signal
*A zone showing repeated visits with elevated volume, diminishing range-per-unit-volume, and drying pullback volume precedes a directional move away from the zone in the absorber's direction.*
Grading: directional. Latest review: keep-watching (recommendation).

**S0-H12** — session × window grid (cells as in the matrix):

| session | backtest | forward |
|---|---|---|
| whole | — | — |
| london | — | — |
| overlap | — | — |
| ny_only | — | — |
| dead | — | — |
| asia | — | — |


### H13 — 1 signal
*After price breaks out of the session value area on declining volume and reclaims it on expanding volume, it continues toward the far side of the value area.*
Grading: directional. Latest review: keep-watching (recommendation).

**S0-H13** — session × window grid (cells as in the matrix):

| session | backtest | forward |
|---|---|---|
| whole | (°▼i-21.5pp (0/1) · p+78.0pp cap95.7 net+93/med+93.0) | (°·i+0.2pp (2/9) · p-12.9pp cap29.4 net-286/med-33.0) |
| london | (°▼i-25.8pp (0/1) · p+69.1pp cap95.7 net+93/med+93.0) | (°▼i-24.3pp (0/1) · p-32.1pp cap— net-43/med-42.8) |
| overlap | — | — |
| ny_only | — | (°▼i-19.1pp (0/3) · p-8.9pp cap— net-100/med-37.2) |
| dead | — | (°▲i+8.1pp (1/3) · p+18.4pp cap29.4 net-97/med-33.0) |
| asia | — | (°▲i+26.3pp (1/2) · p-27.0pp cap— net-46/med-23.1) |

- backtest payoff: right +93 / wrong +0 / net +93 pts; median per fire +93.00 (n=1)
- forward payoff: right +0 / wrong -286 / net -286 pts; median per fire -33.00 (n=9)
- forward best call: 2026-09-02 22:24 +50.9pts remaining (episode 82.8pts, major)
- forward worst false alarm: 2026-09-02 23:46 -60.1pts adverse

### H14 — 1 signal
*Counter-trend No Demand / No Supply prints in an established trend mark absorption and precede trend continuation.*
Grading: directional. Latest review: keep-watching (recommendation).

**S0-H14** — session × window grid (cells as in the matrix):

| session | backtest | forward |
|---|---|---|
| whole | ·i+0.7pp (37/167) · p-13.6pp cap70.2 net-692/med+6.9 | ▼i-5.4pp (100/602) · p-6.9pp cap53.5 net-4121/med-4.5 |
| london | ▼i-10.4pp (4/26) · p-19.4pp cap41.8 net-1762/med-17.1 | ▼i-4.1pp (23/114) · p-3.2pp cap67.9 net-68/med-5.2 |
| overlap | (°▼i-7.9pp (0/17) · p-37.5pp cap— net+433/med+24.0) | ▼i-5.0pp (4/83) · p-20.2pp cap98.2 net-1992/med-26.5 |
| ny_only | ▲i+14.3pp (17/51) · p-13.1pp cap— net+410/med+13.6 | ▲i+4.1pp (22/95) · p-1.5pp cap85.1 net-614/med-5.1 |
| dead | (°▼i-7.4pp (2/18) · p-11.6pp cap— net-56/med+4.5) | ▼i-4.6pp (14/68) · p-9.0pp cap37.1 net-702/med-4.5 |
| asia | ·i+1.2pp (14/55) · p+0.3pp cap85.1 net+282/med+6.6 | ▼i-8.4pp (37/242) · p-7.2pp cap46.5 net-744/med-0.0 |

- backtest payoff: right +2905 / wrong -3598 / net -692 pts; median per fire +6.90 (n=167)
- backtest best call: 2026-08-03 03:48 +195.6pts remaining (episode 209.2pts, major)
- backtest worst false alarm: 2026-07-27 12:59 -334.6pts adverse
- forward payoff: right +6844 / wrong -10964 / net -4121 pts; median per fire -4.50 (n=602)
- forward best call: 2026-09-01 05:03 +286.9pts remaining (episode 376.3pts, major)
- forward worst false alarm: 2026-09-04 11:58 -177.6pts adverse
- earliness (backtest): median 106.9 pts of move remaining at fire (n=11)

### H15 — 1 signal
*A range sweep followed by aggressive traversal to the opposite boundary continues toward the range's volume center.*
Grading: directional. Latest review: keep-watching (recommendation).

**S0-H15** — session × window grid (cells as in the matrix):

| session | backtest | forward |
|---|---|---|
| whole | — | — |
| london | — | — |
| overlap | — | — |
| ny_only | — | — |
| dead | — | — |
| asia | — | — |


### H16 — 1 signal
*The opening session's direction predicts the closing session's direction.*
Grading: directional. Latest review: keep-watching (recommendation).

**S0-H16** — session × window grid (cells as in the matrix):

| session | backtest | forward |
|---|---|---|
| whole | (°▼i-11.5pp (1/10) · p+28.0pp cap121.0 net+274/med+0.1) | ▼i-13.7pp (2/24) · p+5.2pp cap74.5 net+277/med+10.0 |
| london | — | — |
| overlap | — | — |
| ny_only | (°▼i-9.0pp (1/10) · p+36.9pp cap121.0 net+274/med+0.1) | ▼i-10.8pp (2/24) · p+20.3pp cap74.5 net+277/med+10.0 |
| dead | — | — |
| asia | — | — |

- backtest payoff: right +666 / wrong -392 / net +274 pts; median per fire +0.05 (n=10)
- backtest best call: 2026-08-03 19:30 +30.1pts remaining (episode 61.6pts)
- backtest worst false alarm: 2026-07-23 19:30 -188.1pts adverse
- forward payoff: right +466 / wrong -189 / net +277 pts; median per fire +10.00 (n=24)
- forward best call: 2026-09-02 19:30 +28.1pts remaining (episode 54.9pts)
- forward worst false alarm: 2026-08-31 19:30 -82.7pts adverse
- earliness (backtest): median 30.1 pts of move remaining at fire (n=1)

### H17 — 1 signal
*A climax reversal signal followed by absorption within five bars — effort meeting a quiet counter-party — marks a genuine exhaustion turn: the two-chapter story (exhaustion needs absorption to become reversal).*
Grading: directional. Latest review: rows (recommendation).

**S0-H17** — session × window grid (cells as in the matrix):

| session | backtest | forward |
|---|---|---|
| whole | (°▼i-8.2pp (2/15) · p+18.0pp cap166.0 net+681/med+10.2) | ·i-0.2pp (17/78) · p+6.8pp cap82.8 net-125/med+6.4 |
| london | (°▼i-5.8pp (1/5) · p+9.1pp cap125.1 net-18/med-23.3) | ▲i+7.1pp (11/35) · p-3.5pp cap85.9 net-373/med-4.6 |
| overlap | — | (°▼i-9.8pp (0/3) · p-33.5pp cap— net-197/med-50.9) |
| ny_only | — | (°▼i-19.1pp (0/8) · p-8.9pp cap— net+140/med+23.1) |
| dead | (°·i+1.5pp (1/5) · p+8.4pp cap360.0 net+282/med+13.9) | (°▼i-3.8pp (3/14) · p+35.1pp cap68.3 net+161/med+15.2) |
| asia | (°▼i-24.3pp (0/5) · p+40.3pp cap172.4 net+417/med+120.1) | (°▼i-7.0pp (3/18) · p+11.9pp cap73.2 net+143/med+10.1) |

- backtest payoff: right +958 / wrong -277 / net +681 pts; median per fire +10.20 (n=15)
- backtest best call: 2026-07-29 23:42 +191.5pts remaining (episode 157.1pts)
- backtest worst false alarm: 2026-07-28 07:57 -96.5pts adverse
- forward payoff: right +1927 / wrong -2053 / net -125 pts; median per fire +6.40 (n=78)
- forward best call: 2026-08-20 09:44 +291.5pts remaining (episode 306.7pts, major)
- forward worst false alarm: 2026-08-20 11:26 -192.8pts adverse
- earliness (backtest): median 150.3 pts of move remaining at fire (n=2)

### H18 — 1 signal
*A gap-traversal signal followed by a same-direction effortless print within five bars — travel meeting no opposition — continues: the map says vacuum, the tape confirms no resistance.*
Grading: directional. Latest review: rows (recommendation).

**S0-H18** — session × window grid (cells as in the matrix):

| session | backtest | forward |
|---|---|---|
| whole | ▼i-7.7pp (8/58) · p-8.2pp cap127.3 net-1784/med-23.8 | ▼i-4.2pp (23/129) · p+3.9pp cap103.5 net+540/med+1.5 |
| london | ▲i+3.4pp (7/24) · p-22.6pp cap111.1 net-559/med-16.3 | ·i+0.0pp (9/37) · p+8.4pp cap104.2 net+25/med-11.6 |
| overlap | (°▼i-7.9pp (0/6) · p+29.2pp cap141.5 net-621/med-85.3) | (°·i+0.7pp (2/19) · p+8.6pp cap121.4 net+347/med+46.5) |
| ny_only | (°▼i-19.0pp (0/3) · p-13.1pp cap— net-88/med-59.0) | ·i+0.9pp (8/40) · p-3.9pp cap82.8 net-211/med-3.7 |
| dead | (°▼i-18.5pp (0/7) · p+2.7pp cap62.0 net-92/med-3.5) | (°▼i-25.2pp (0/4) · p-14.9pp cap— net+2/med-2.7) |
| asia | (°▼i-18.7pp (1/18) · p-14.1pp cap140.0 net-424/med-20.4) | ▼i-9.9pp (4/29) · p+10.9pp cap61.6 net+376/med+17.7 |

- backtest payoff: right +1006 / wrong -2790 / net -1784 pts; median per fire -23.75 (n=58)
- backtest best call: 2026-07-31 10:15 +476.0pts remaining (episode 521.8pts, major)
- backtest worst false alarm: 2026-07-29 13:54 -255.0pts adverse
- forward payoff: right +3413 / wrong -2873 / net +540 pts; median per fire +1.50 (n=129)
- forward best call: 2026-08-27 10:22 +159.0pts remaining (episode 172.9pts, major)
- forward worst false alarm: 2026-08-24 13:29 -277.8pts adverse
- earliness (backtest): median 155.6 pts of move remaining at fire (n=5)

### H19 — 1 signal
*A probe-failure reversal signal followed by continued wide-loud effort in the anchor bar's own close direction within five bars is NOT the start of the claimed reversal — a SUPPRESSION/FADE configuration, and it says so.*
Grading: directional. Latest review: rows (recommendation).

- Question **Q1-H19**: see the register entry (status there is authoritative).
**S0-H19** — session × window grid (cells as in the matrix):

| session | backtest | forward |
|---|---|---|
| whole | ·i-1.9pp (40/204) · p+1.0pp cap180.0 net+1513/med+6.5 | ▲i+3.0pp (98/392) · p-0.3pp cap86.6 net-1100/med-2.2 |
| london | ▼i-15.3pp (4/38) · p-2.0pp cap98.9 net-152/med+12.8 | ▲i+2.0pp (36/137) · p-5.1pp cap99.6 net-1278/med-3.4 |
| overlap | (°▼i-7.9pp (0/20) · p+2.5pp cap185.4 net+387/med+17.1) | (°▼i-9.8pp (0/19) · p-17.7pp cap160.1 net+233/med-2.1) |
| ny_only | ▼i-4.7pp (7/49) · p+25.7pp cap260.5 net+2978/med+38.3 | ▼i-2.8pp (8/49) · p-0.7pp cap128.4 net+254/med-2.4 |
| dead | ·i-1.4pp (6/35) · p-5.9pp cap263.2 net-1043/med+14.8 | ▲i+5.6pp (16/52) · p+13.9pp cap82.8 net-335/med-7.2 |
| asia | ▲i+12.8pp (23/62) · p-8.4pp cap147.6 net-656/med-11.6 | ▲i+4.4pp (38/135) · p-1.8pp cap76.4 net+26/med+0.3 |

- backtest payoff: right +10830 / wrong -9317 / net +1513 pts; median per fire +6.45 (n=204)
- backtest best call: 2026-07-30 06:41 +804.0pts remaining (episode 832.8pts, major)
- backtest worst false alarm: 2026-07-29 19:16 -700.8pts adverse
- forward payoff: right +9433 / wrong -10533 / net -1100 pts; median per fire -2.25 (n=392)
- forward best call: 2026-08-21 11:30 +297.2pts remaining (episode 309.6pts, major)
- forward worst false alarm: 2026-08-19 12:53 -316.2pts adverse
- earliness (backtest): median 103.0 pts of move remaining at fire (n=16)

### H20 — 1 signal
*A wide-bar close-through of a session extreme (the same conditioned wide-bar class the retest anchor fires on; resolution = the close beyond the level, not a rejection back inside) initiates continuation in the break direction.*
Grading: directional. Latest review: rows (recommendation).

**S0-H20** — session × window grid (cells as in the matrix):

| session | backtest | forward |
|---|---|---|
| whole | ▼i-10.5pp (1/46) · p+8.6pp cap277.1 [cls 39.2%/12.7%i] net+1398/med+2.9 | ▼i-11.0pp (6/127) · p+2.7pp cap84.0 [cls 36.7%/15.7%i] net+271/med-4.4 |
| london | (°▲i+13.3pp (1/3) · p-38.6pp cap— [cls 38.6%/20.0%i] net-182/med-90.2) | ▼i-14.6pp (4/59) · p+1.6pp cap105.5 [cls 35.7%/21.4%i] net+1170/med-1.0 |
| overlap | (°▼i-6.8pp (0/34) · p+17.4pp cap277.1 [cls 47.3%/6.8%i] net+1975/med+63.9) | ▼i-7.6pp (0/28) · p-16.5pp cap97.7 [cls 45.1%/7.6%i] net-1198/med-45.9 |
| ny_only | (°▼i-6.9pp (0/2) · p-32.6pp cap— [cls 32.6%/6.9%i] net+16/med+7.9) | — |
| dead | (°▼i-13.5pp (0/4) · p-23.8pp cap— [cls 23.8%/13.5%i] net-155/med-45.4) | (°▲i+3.4pp (1/6) · p+15.4pp cap76.2 [cls 34.6%/13.3%i] net-187/med-15.2) |
| asia | (°▼i-17.7pp (0/3) · p-25.0pp cap— [cls 25.0%/17.7%i] net-256/med-75.9) | ▼i-15.2pp (1/34) · p+17.7pp cap62.4 [cls 32.3%/18.1%i] net+486/med+15.4 |

- backtest payoff: right +3786 / wrong -2388 / net +1398 pts; median per fire +2.90 (n=46)
- backtest best call: 2026-07-31 09:07 +2.0pts remaining (episode 98.0pts)
- backtest worst false alarm: 2026-07-31 13:34 -574.3pts adverse
- forward payoff: right +3980 / wrong -3709 / net +271 pts; median per fire -4.40 (n=127)
- forward best call: 2026-08-26 22:01 +81.5pts remaining (episode 81.5pts)
- forward worst false alarm: 2026-08-19 14:12 -233.2pts adverse
- earliness (backtest): median 2.0 pts of move remaining at fire (n=1)


---

# us30 (us30fut) — CANONICAL

Store span (1M, close ts): 2026-07-19 22:02:00+00:00 → 2026-09-16 16:08:00+00:00. Volume type: real futures volume (register 40 first-sync sanity; canonical verdict at this instrument's validation evening).

## Summary Matrix (page 1)

Engine `8effbb323` — OBSERVATIONAL signal scoreboard - move-detection, not trading; no fills exist here by construction; never validation (docs/hypothesis_lifecycle.md stage 4)

**Review labels are RECOMMENDATIONS — none actioned, review pending operator familiarity.** Cells: marker + precision LIFT vs that context's OWN chance rate, (hits/fires), payoff net/median points (directional rows; either-direction rows have no payoff by construction). ▲/▼ = beyond ±2pp of chance, · = within. (°…) = small-n (fires<20 or episodes<10): dimmed, excluded from any future label arithmetic. Read READING_GUIDE.md first; full detail in hypothesis_performance.json.

| H | label | backtest whole | backtest london | forward whole | forward london |
|---|---|---|---|---|---|
| *context* | | 109 ep; chance 24.0%dir/44.7%either | 36 ep; chance 36.8%dir/66.5%either | 226 ep; chance 25.3%dir/47.2%either | 65 ep; chance 37.1%dir/68.0%either |
| S0-H1 | keep-watching | ·i+1.4pp (11/49) · p+10.7pp cap154.0 net-83/med-8.0 | (°▲i+11.3pp (6/17) · p-1.5pp cap104.0 net-113/med-17.5) | ▲i+4.7pp (79/307) · p+1.7pp cap68.5 net-3135/med-1.0 | ▲i+4.3pp (32/122) · p-10.9pp cap101.5 net-3862/med-17.8 |
| S1-H1 | keep-watching | (°▼i-21.0pp (0/2) · p-24.0pp cap— net-18/med-9.2) | (°▼i-24.0pp (0/1) · p-36.8pp cap— net-50/med-50.0) | ▲i+26.4pp (18/38) · p+1.0pp cap69.8 net-1072/med-31.5 | ▲i+38.1pp (12/20) · p-22.1pp cap130.1 net-1326/med-76.8 |
| S0-H2 | promote-candidate | ▼i-5.7pp (43/281) · p+3.0pp cap130.7 net-2432/med-4.0 | ·i+0.2pp (15/62) · p-1.3pp cap116.2 net-337/med-20.0 | ▼i-4.7pp (146/896) · p+3.0pp cap80.5 net+2597/med-0.5 | ▼i-11.0pp (29/266) · p+7.3pp cap103.8 net+3472/med+4.5 |
| S1-H2 | promote-candidate | ▼i-3.7pp (38/220) · p+4.6pp cap131.9 net-505/med-2.8 | ▲i+2.0pp (13/50) · p+1.2pp cap119.0 net-218/med-18.0 | ▼i-2.2pp (117/624) · p+1.3pp cap77.8 net+2/med-1.0 | ▼i-7.9pp (23/164) · p+2.5pp cap103.5 net+476/med-0.5 |
| S0-H3 | keep-watching | (°▲i+4.0pp (1/4) · p+1.0pp cap81.0 net+59/med+13.2) | (°▲i+26.0pp (1/2) · p-36.8pp cap— net-22/med-11.0) | (°▼i-10.5pp (2/19) · p+32.6pp cap107.5 net+608/med+39.0) | (°▲i+3.1pp (2/8) · p+12.9pp cap116.8 net-9/med-3.5) |
| S0-H4 | keep-watching | (°▲i+17.5pp (5/13) · p+14.5pp cap83.0 net+194/med+15.0) | (°▼i-24.0pp (0/7) · p+34.6pp cap83.0 net+392/med+71.0) | — | — |
| S0-H5 | keep-watching | (°▼i-21.0pp (0/1) · p-24.0pp cap— net-135/med-135.0) | (°▼i-24.0pp (0/1) · p-36.8pp cap— net-135/med-135.0) | (°▼i-21.0pp (0/1) · p+74.7pp cap215.0 net+24/med+24.0) | (°▼i-21.9pp (0/1) · p+62.9pp cap215.0 net+24/med+24.0) |
| S0-H6 | keep-watching | ▼i-9.4pp (3/52) · p-21.5pp cap175.0 [cls 40.7%/15.2%i] net-1151/med-25.2 | ▼i-6.6pp (3/24) · p-28.6pp cap164.5 [cls 41.1%/19.1%i] net-664/med-30.0 | ▲i+11.7pp (46/185) · p-6.1pp cap95.0 [cls 42.3%/13.2%i] net-3379/med-6.0 | ▲i+10.7pp (20/76) · p-4.3pp cap77.0 [cls 42.5%/15.6%i] net-2092/med-13.0 |
| S0-H7 | keep-watching | ▲i+8.3pp (12/41) · p-2.0pp cap111.0 net+205/med-9.0 | (°▲i+13.5pp (6/16) · p-5.6pp cap111.0 net-161/med-7.0) | ▲i+2.2pp (42/181) · p+2.9pp cap68.0 net+1370/med+6.5 | ▲i+3.6pp (12/47) · p-7.3pp cap108.5 net-376/med-21.5 |
| S0-H7 (either-dir) | keep-watching | ▲i+2.4pp (17/41) · p-3.2pp cap66.5 | (°▼i-6.8pp (6/16) · p+2.3pp cap60.5) | ▼i-7.8pp (56/181) · p+6.9pp cap38.5 | ▼i-7.4pp (16/47) · p+4.3pp cap26.5 |
| S0-H8 | keep-watching | ▼i-12.4pp (75/281) · p+8.0pp cap75.2 | ▼i-4.0pp (25/62) · p+7.7pp cap57.2 | ▼i-3.1pp (319/896) · p+3.2pp cap46.2 | ▼i-7.9pp (89/266) · p+1.9pp cap67.5 |
| S0-H9 | keep-watching | ▼i-13.5pp (3/40) · p-1.5pp cap66.0 net-353/med-14.7 | (°▼i-24.0pp (0/3) · p-3.5pp cap52.0 net-198/med-61.5) | ·i+0.6pp (22/102) · p-5.7pp cap84.5 net-834/med-7.5 | ·i+0.7pp (7/31) · p+1.6pp cap99.0 net+109/med+14.5 |
| S1-H9 | keep-watching | (°▼i-21.0pp (0/9) · p-1.8pp cap273.0 net+460/med+1.5) | (°▼i-24.0pp (0/1) · p-36.8pp cap— net-38/med-38.0) | ▼i-18.4pp (1/39) · p-7.4pp cap81.0 net-638/med-16.0 | (°▼i-21.9pp (0/12) · p-3.8pp cap97.2 net-303/med-42.5) |
| S0-H10 | deprioritize | ·i-1.5pp (30/154) · p+0.0pp cap71.0 net+1774/med+11.0 | ▼i-19.0pp (2/40) · p+3.2pp cap116.0 net+1480/med+27.5 | ▼i-5.6pp (92/597) · p-4.0pp cap68.1 net-1294/med-0.5 | ·i-1.9pp (30/150) · p-1.8pp cap80.5 net-341/med-8.0 |
| S0-H11 | keep-watching | ·i-0.7pp (84/413) · p+3.4pp cap98.0 net+1254/med+3.0 | ▼i-5.6pp (30/163) · p+0.6pp cap91.0 net-404/med+5.0 | ▼i-4.6pp (151/920) · p-0.1pp cap75.2 net+1117/med-2.5 | ▼i-9.7pp (36/294) · p+2.0pp cap82.0 net+1498/med+3.5 |
| S1-H11 | keep-watching | ▲i+6.0pp (51/189) · p+0.9pp cap167.0 net+1560/med+0.5 | (°▼i-14.9pp (1/11) · p+8.7pp cap194.5 net+136/med-24.5) | ▼i-4.9pp (147/914) · p+4.0pp cap80.5 net+1305/med+2.5 | ▼i-2.4pp (74/379) · p+0.6pp cap81.4 net+2542/med+5.5 |
| S0-H12 | keep-watching | — | — | (°▼i-21.0pp (0/1) · p-25.3pp cap— net+20/med+19.9) | (°▼i-21.9pp (0/1) · p-37.1pp cap— net+20/med+19.9) |
| S0-H13 | keep-watching | (°▲i+79.0pp (1/1) · p-24.0pp cap— net-206/med-206.0) | (°▲i+76.0pp (1/1) · p-36.8pp cap— net-206/med-206.0) | (°▼i-21.0pp (0/5) · p+34.7pp cap125.0 net+147/med+12.0) | (°▼i-21.9pp (0/1) · p-37.1pp cap— net-58/med-58.0) |
| S0-H14 | keep-watching | ▲i+4.0pp (37/148) · p+2.4pp cap76.0 net+2606/med+12.5 | ▼i-17.6pp (3/47) · p+12.1pp cap106.0 net+1414/med+12.5 | ▼i-6.7pp (80/558) · p+0.0pp cap67.0 net+618/med-1.3 | ·i-0.4pp (32/149) · p-0.2pp cap92.0 net+1222/med-3.4 |
| S0-H15 | keep-watching | — | — | — | — |
| S0-H16 | keep-watching | (°▼i-21.0pp (0/10) · p+36.0pp cap98.2 net+522/med+37.5) | — | ▼i-16.8pp (1/24) · p-0.3pp cap68.8 net+109/med+0.5 | — |
| S0-H17 | rows | ▲i+2.1pp (6/26) · p+2.9pp cap119.5 net-167/med-10.5 | (°▲i+16.0pp (4/10) · p-6.8pp cap157.5 net+113/med+12.2) | ▲i+6.8pp (47/169) · p-5.2pp cap64.8 net-2134/med-12.5 | ▲i+9.1pp (18/58) · p-18.1pp cap86.5 net-2013/med-38.5 |
| S0-H18 | rows | ▲i+2.9pp (16/67) · p+2.9pp cap102.5 net+355/med+2.5 | ·i+1.0pp (7/28) · p+2.5pp cap87.5 net+681/med+46.2 | ▼i-8.5pp (20/160) · p-2.8pp cap69.0 net-1434/med-6.8 | ▼i-9.4pp (6/48) · p+4.6pp cap66.0 net-46/med+9.5 |
| S0-H19 | rows | ▼i-11.1pp (17/172) · p+10.3pp cap130.0 net+2236/med+3.2 | ▼i-5.2pp (6/32) · p+7.0pp cap135.5 net+708/med+34.0 | ·i+0.5pp (120/559) · p+2.1pp cap81.5 net-231/med+2.0 | ▲i+2.2pp (40/166) · p-3.4pp cap91.5 net-1876/med+0.0 |
| S0-H20 | rows | ▼i-11.8pp (2/58) · p-11.4pp cap114.0 [cls 40.7%/15.2%i] net+27/med+18.2 | ▼i-13.7pp (2/37) · p-16.8pp cap87.5 [cls 41.1%/19.1%i] net-532/med+4.5 | ▼i-11.4pp (3/163) · p+4.3pp cap120.8 [cls 42.3%/13.2%i] net-162/med-8.0 | ▼i-13.7pp (2/104) · p+19.0pp cap124.2 [cls 42.5%/15.6%i] net+2815/med+36.0 |
| **union coverage** | | 41.3% (45/109) | 38.9% (14/36) | 91.6% (207/226) | 95.4% (62/65) |

Not graded:  — see register entries.

## Hypothesis Cards (page 2)

### H1 — 2 signals
*A climactic bar — extreme volume on a wide spread late in an extended move — marks exhaustion, and price then reverses against the climax direction.*
Grading: directional. Latest review: keep-watching (recommendation).

- Question **Q1-H1**: see the register entry (status there is authoritative).
**S0-H1** — session × window grid (cells as in the matrix):

| session | backtest | forward |
|---|---|---|
| whole | ·i+1.4pp (11/49) · p+10.7pp cap154.0 net-83/med-8.0 | ▲i+4.7pp (79/307) · p+1.7pp cap68.5 net-3135/med-1.0 |
| london | (°▲i+11.3pp (6/17) · p-1.5pp cap104.0 net-113/med-17.5) | ▲i+4.3pp (32/122) · p-10.9pp cap101.5 net-3862/med-17.8 |
| overlap | — | (°▼i-11.2pp (0/6) · p-16.3pp cap186.5 net-154/med-79.5) |
| ny_only | (°▼i-3.7pp (2/13) · p+40.3pp cap253.5 net-62/med-15.5) | ▲i+6.3pp (8/34) · p-3.1pp cap125.2 net+16/med+2.2 |
| dead | (°▲i+28.3pp (3/7) · p-7.2pp cap— net-157/med-8.0) | ▲i+8.1pp (15/48) · p+23.3pp cap81.0 net+850/med+13.2 |
| asia | (°▼i-24.8pp (0/12) · p+9.4pp cap91.2 net+248/med+27.0) | ·i+0.2pp (24/97) · p+4.5pp cap49.0 net+15/med+2.0 |

- backtest payoff: right +1958 / wrong -2041 / net -83 pts; median per fire -8.00 (n=49)
- backtest best call: 2026-07-29 16:24 +398.0pts remaining (episode 602.0pts, major)
- backtest worst false alarm: 2026-07-29 19:22 -450.0pts adverse
- forward payoff: right +6360 / wrong -9495 / net -3135 pts; median per fire -1.00 (n=307)
- forward best call: 2026-09-03 09:59 +663.5pts remaining (episode 664.0pts, major)
- forward worst false alarm: 2026-09-15 13:23 -406.0pts adverse
- earliness (backtest): median 128.0 pts of move remaining at fire (n=10)

**S1-H1** — session × window grid (cells as in the matrix):

| session | backtest | forward |
|---|---|---|
| whole | (°▼i-21.0pp (0/2) · p-24.0pp cap— net-18/med-9.2) | ▲i+26.4pp (18/38) · p+1.0pp cap69.8 net-1072/med-31.5 |
| london | (°▼i-24.0pp (0/1) · p-36.8pp cap— net-50/med-50.0) | ▲i+38.1pp (12/20) · p-22.1pp cap130.1 net-1326/med-76.8 |
| overlap | — | — |
| ny_only | — | (°▼i-17.2pp (0/2) · p+41.0pp cap107.0 net+26/med+13.0) |
| dead | — | (°▼i-6.4pp (1/6) · p+42.1pp cap59.5 net+185/med+42.2) |
| asia | (°▼i-24.8pp (0/1) · p-23.9pp cap— net+32/med+31.5) | (°▲i+25.5pp (5/10) · p+0.5pp cap67.5 net+43/med+8.2) |

- backtest payoff: right +32 / wrong -50 / net -18 pts; median per fire -9.25 (n=2)
- backtest worst false alarm: 2026-07-29 12:17 -67.0pts adverse
- forward payoff: right +636 / wrong -1708 / net -1072 pts; median per fire -31.50 (n=38)
- forward best call: 2026-09-03 09:59 +663.5pts remaining (episode 664.0pts, major)
- forward worst false alarm: 2026-08-20 11:47 -199.5pts adverse

### H2 — 2 signals
*A failed probe beyond a prior extreme — an upthrust above or spring below that closes back inside — reverses against the probe.*
Grading: directional. Latest review: promote-candidate (recommendation).

**S0-H2** — session × window grid (cells as in the matrix):

| session | backtest | forward |
|---|---|---|
| whole | ▼i-5.7pp (43/281) · p+3.0pp cap130.7 net-2432/med-4.0 | ▼i-4.7pp (146/896) · p+3.0pp cap80.5 net+2597/med-0.5 |
| london | ·i+0.2pp (15/62) · p-1.3pp cap116.2 net-337/med-20.0 | ▼i-11.0pp (29/266) · p+7.3pp cap103.8 net+3472/med+4.5 |
| overlap | (°▼i-11.6pp (0/22) · p+12.6pp cap150.2 net-1080/med-77.8) | (°▼i-3.9pp (3/41) · p+3.6pp cap179.5 net-36/med+4.0) |
| ny_only | ▼i-15.8pp (2/60) · p+23.2pp cap224.8 net-1257/med-11.1 | ▼i-5.1pp (15/124) · p-2.5pp cap112.0 net-418/med-4.2 |
| dead | ·i+0.0pp (6/41) · p+2.6pp cap100.8 net-18/med-2.6 | ▼i-5.0pp (27/149) · p+6.2pp cap70.0 net-275/med-3.0 |
| asia | ▼i-4.0pp (20/96) · p-5.1pp cap82.5 net+261/med+1.2 | ·i-1.7pp (72/316) · p-0.4pp cap55.0 net-146/med-0.5 |

- backtest payoff: right +10496 / wrong -12928 / net -2432 pts; median per fire -4.00 (n=281)
- backtest best call: 2026-07-29 10:42 +781.0pts remaining (episode 752.0pts, major)
- backtest worst false alarm: 2026-07-29 18:55 -695.0pts adverse
- forward payoff: right +21685 / wrong -19088 / net +2597 pts; median per fire -0.50 (n=896)
- forward best call: 2026-09-10 09:46 +469.5pts remaining (episode 522.5pts, major)
- forward worst false alarm: 2026-08-19 12:55 -270.0pts adverse
- earliness (backtest): median 105.2 pts of move remaining at fire (n=24)

**S1-H2** — session × window grid (cells as in the matrix):

| session | backtest | forward |
|---|---|---|
| whole | ▼i-3.7pp (38/220) · p+4.6pp cap131.9 net-505/med-2.8 | ▼i-2.2pp (117/624) · p+1.3pp cap77.8 net+2/med-1.0 |
| london | ▲i+2.0pp (13/50) · p+1.2pp cap119.0 net-218/med-18.0 | ▼i-7.9pp (23/164) · p+2.5pp cap103.5 net+476/med-0.5 |
| overlap | (°▼i-11.6pp (0/17) · p+8.3pp cap120.5 net-983/med-92.0) | (°▼i-2.1pp (3/33) · p+3.4pp cap180.8 net-26/med-18.5) |
| ny_only | ▼i-14.2pp (2/41) · p+32.8pp cap239.5 net+169/med-15.0 | ▼i-2.0pp (14/92) · p-3.6pp cap96.5 net-732/med-3.5 |
| dead | ▲i+4.8pp (6/31) · p+2.5pp cap99.5 net-162/med-5.0 | ▼i-4.4pp (20/107) · p+5.2pp cap71.3 net+266/med-1.5 |
| asia | ▼i-3.8pp (17/81) · p-5.4pp cap83.0 net+689/med+6.0 | ·i+0.5pp (57/228) · p+1.2pp cap54.5 net+18/med-0.2 |

- backtest payoff: right +8589 / wrong -9094 / net -505 pts; median per fire -2.80 (n=220)
- backtest best call: 2026-07-29 10:42 +781.0pts remaining (episode 752.0pts, major)
- backtest worst false alarm: 2026-07-29 18:55 -695.0pts adverse
- forward payoff: right +13440 / wrong -13438 / net +2 pts; median per fire -1.00 (n=624)
- forward best call: 2026-09-10 09:46 +469.5pts remaining (episode 522.5pts, major)
- forward worst false alarm: 2026-09-10 13:17 -270.0pts adverse
- earliness (backtest): median 106.0 pts of move remaining at fire (n=23)

### H3 — 1 signal
*Repeated absorption — high effort with no result — at a price level precedes a breakout through that level.*
Grading: directional. Latest review: keep-watching (recommendation).

**S0-H3** — session × window grid (cells as in the matrix):

| session | backtest | forward |
|---|---|---|
| whole | (°▲i+4.0pp (1/4) · p+1.0pp cap81.0 net+59/med+13.2) | (°▼i-10.5pp (2/19) · p+32.6pp cap107.5 net+608/med+39.0) |
| london | (°▲i+26.0pp (1/2) · p-36.8pp cap— net-22/med-11.0) | (°▲i+3.1pp (2/8) · p+12.9pp cap116.8 net-9/med-3.5) |
| overlap | — | (°▼i-11.2pp (0/3) · p+67.0pp cap186.0 net+490/med+155.5) |
| ny_only | — | (°▼i-17.2pp (0/2) · p+41.0pp cap59.5 net+88/med+44.2) |
| dead | — | — |
| asia | (°▼i-24.8pp (0/2) · p+26.1pp cap81.0 net+81/med+40.5) | (°▼i-24.5pp (0/6) · p+20.5pp cap57.0 net+38/med+10.8) |

- backtest payoff: right +99 / wrong -40 / net +59 pts; median per fire +13.25 (n=4)
- backtest best call: 2026-07-30 09:10 +122.0pts remaining (episode 205.5pts)
- backtest worst false alarm: 2026-07-30 09:10 -83.5pts adverse
- forward payoff: right +1028 / wrong -421 / net +608 pts; median per fire +39.00 (n=19)
- forward best call: 2026-09-14 12:10 +281.6pts remaining (episode 313.6pts, major)
- forward worst false alarm: 2026-09-10 12:22 -179.0pts adverse
- earliness (backtest): median 122.0 pts of move remaining at fire (n=1)

### H4 — 1 signal
*In an established trend, a quiet (low-volume) pullback resolves with trend resumption.*
Grading: directional. Latest review: keep-watching (recommendation).

**S0-H4** — session × window grid (cells as in the matrix):

| session | backtest | forward |
|---|---|---|
| whole | (°▲i+17.5pp (5/13) · p+14.5pp cap83.0 net+194/med+15.0) | — |
| london | (°▼i-24.0pp (0/7) · p+34.6pp cap83.0 net+392/med+71.0) | — |
| overlap | (°▼i-11.6pp (0/1) · p-32.9pp cap— net-166/med-165.5) | — |
| ny_only | — | — |
| dead | (°▲i+85.4pp (5/5) · p-7.2pp cap— net-33/med-6.9) | — |
| asia | — | — |

- backtest payoff: right +410 / wrong -216 / net +194 pts; median per fire +15.00 (n=13)
- backtest best call: 2026-08-03 22:58 +63.0pts remaining (episode 86.0pts)
- backtest worst false alarm: 2026-08-03 14:10 -174.0pts adverse
- earliness (backtest): median 63.0 pts of move remaining at fire (n=1)

### H5 — 1 signal
*A buying climax that extends far above its trend mean mean-reverts (climax-extension fade; registered short-side only).*
Grading: directional. Latest review: keep-watching (recommendation).

**S0-H5** — session × window grid (cells as in the matrix):

| session | backtest | forward |
|---|---|---|
| whole | (°▼i-21.0pp (0/1) · p-24.0pp cap— net-135/med-135.0) | (°▼i-21.0pp (0/1) · p+74.7pp cap215.0 net+24/med+24.0) |
| london | (°▼i-24.0pp (0/1) · p-36.8pp cap— net-135/med-135.0) | (°▼i-21.9pp (0/1) · p+62.9pp cap215.0 net+24/med+24.0) |
| overlap | — | — |
| ny_only | — | — |
| dead | — | — |
| asia | — | — |

- backtest payoff: right +0 / wrong -135 / net -135 pts; median per fire -135.00 (n=1)
- backtest worst false alarm: 2026-07-28 11:30 -135.0pts adverse
- forward payoff: right +24 / wrong +0 / net +24 pts; median per fire +24.00 (n=1)

### H6 — 1 signal
*A wide-spread rejection bar at a session extreme (measured day-relative, volume-agnostic) reverses away from the extreme.*
Grading: directional. Latest review: keep-watching (recommendation).

- Question **Q1-H6**: see the register entry (status there is authoritative).
- Question **Q2-H6**: see the register entry (status there is authoritative).
- Question **Q3-H6**: see the register entry (status there is authoritative).
**S0-H6** — session × window grid (cells as in the matrix):

| session | backtest | forward |
|---|---|---|
| whole | ▼i-9.4pp (3/52) · p-21.5pp cap175.0 [cls 40.7%/15.2%i] net-1151/med-25.2 | ▲i+11.7pp (46/185) · p-6.1pp cap95.0 [cls 42.3%/13.2%i] net-3379/med-6.0 |
| london | ▼i-6.6pp (3/24) · p-28.6pp cap164.5 [cls 41.1%/19.1%i] net-664/med-30.0 | ▲i+10.7pp (20/76) · p-4.3pp cap77.0 [cls 42.5%/15.6%i] net-2092/med-13.0 |
| overlap | (°▼i-9.2pp (0/18) · p-19.3pp cap195.5 [cls 41.5%/9.2%i] net+234/med+6.8) | (°▲i+15.0pp (19/84) · p-10.6pp cap140.5 [cls 45.1%/7.6%i] net-1251/med-5.5) |
| ny_only | (°▼i-5.4pp (0/6) · p+7.7pp cap329.0 [cls 42.3%/5.4%i] net-856/med-92.0) | (°▼i-12.2pp (0/4) · p+15.2pp cap87.5 [cls 9.8%/12.2%i] net+51/med+13.8) |
| dead | (°▼i-7.4pp (0/3) · p-11.8pp cap— [cls 11.8%/7.4%i] net+58/med+5.5) | (°▼i-10.4pp (0/1) · p+82.3pp cap81.5 [cls 17.7%/10.4%i] net+3/med+3.4) |
| asia | (°▼i-20.5pp (0/1) · p-39.6pp cap— [cls 39.6%/20.5%i] net+77/med+77.0) | ▲i+20.9pp (7/20) · p-10.9pp cap68.5 [cls 45.9%/14.1%i] net-90/med+5.2 |

- backtest payoff: right +1398 / wrong -2549 / net -1151 pts; median per fire -25.25 (n=52)
- backtest best call: 2026-07-28 12:23 +197.5pts remaining (episode 226.5pts, major)
- backtest worst false alarm: 2026-07-28 15:11 -288.5pts adverse
- forward payoff: right +4691 / wrong -8070 / net -3379 pts; median per fire -6.00 (n=185)
- forward best call: 2026-09-09 05:31 +480.0pts remaining (episode 489.0pts, major)
- forward worst false alarm: 2026-09-03 14:34 -402.0pts adverse
- earliness (backtest): median 27.5 pts of move remaining at fire (n=3)

### H7 — 1 signal
*Quiet decline at a session extreme is disguised accumulation: effortless (low-volume) weakness reverses UP once selling fails to attract participation (mirror: quiet advance at a high reverses down).*
Grading: directional + either-direction (dual). Latest review: keep-watching (recommendation).

- Question **Q1-H7**: see the register entry (status there is authoritative).
**S0-H7** — session × window grid (cells as in the matrix):

| session | backtest | forward |
|---|---|---|
| whole | ▲i+8.3pp (12/41) · p-2.0pp cap111.0 net+205/med-9.0 | ▲i+2.2pp (42/181) · p+2.9pp cap68.0 net+1370/med+6.5 |
| london | (°▲i+13.5pp (6/16) · p-5.6pp cap111.0 net-161/med-7.0) | ▲i+3.6pp (12/47) · p-7.3pp cap108.5 net-376/med-21.5 |
| overlap | (°▼i-11.6pp (0/3) · p+33.8pp cap287.0 net+471/med+272.0) | (°·i+1.8pp (3/23) · p+14.8pp cap143.5 net+748/med+24.5) |
| ny_only | (°▼i-19.1pp (0/4) · p-13.5pp cap— net-21/med-5.0) | ·i-0.1pp (6/35) · p-3.3pp cap130.5 net+1040/med+27.5 |
| dead | (°▲i+10.4pp (1/4) · p-7.2pp cap— net-1/med-2.0) | (°▲i+5.5pp (2/7) · p+6.4pp cap61.5 net+34/med-0.5) |
| asia | (°▲i+10.9pp (5/14) · p-9.6pp cap76.0 net-84/med-13.8) | ▲i+3.0pp (19/69) · p+3.8pp cap45.5 net-77/med+0.0 |

- backtest payoff: right +1609 / wrong -1404 / net +205 pts; median per fire -9.00 (n=41)
- backtest best call: 2026-07-31 09:51 +528.0pts remaining (episode 569.0pts, major)
- backtest worst false alarm: 2026-07-28 10:48 -242.0pts adverse
- forward payoff: right +5083 / wrong -3713 / net +1370 pts; median per fire +6.50 (n=181)
- forward best call: 2026-09-01 03:37 +402.0pts remaining (episode 398.0pts, major)
- forward worst false alarm: 2026-08-19 12:12 -262.0pts adverse
- earliness (backtest): median 97.8 pts of move remaining at fire (n=10)

**S0-H7 (either-dir)** — session × window grid (cells as in the matrix):

| session | backtest | forward |
|---|---|---|
| whole | ▲i+2.4pp (17/41) · p-3.2pp cap66.5 | ▼i-7.8pp (56/181) · p+6.9pp cap38.5 |
| london | (°▼i-6.8pp (6/16) · p+2.3pp cap60.5) | ▼i-7.4pp (16/47) · p+4.3pp cap26.5 |
| overlap | (°▼i-23.1pp (0/3) · p+6.1pp cap287.0) | (°▼i-9.5pp (3/23) · p+9.0pp cap107.2) |
| ny_only | (°▼i-10.2pp (1/4) · p-26.1pp cap—) | ▼i-3.3pp (10/35) · p-11.8pp cap130.5 |
| dead | (°▲i+21.4pp (2/4) · p-14.4pp cap—) | (°▲i+2.7pp (3/7) · p-1.1pp cap61.5) |
| asia | (°▲i+11.2pp (8/14) · p-16.6pp cap37.0) | ▼i-9.6pp (24/69) · p+9.6pp cap35.0 |

- backtest payoff: n/a by construction (either-direction)
- backtest best call: 2026-07-31 09:51 +528.0pts remaining (episode 569.0pts, major)
- backtest worst false alarm: 2026-07-30 16:13 -170.0pts adverse
- forward payoff: n/a by construction (either-direction)
- forward best call: 2026-09-01 03:37 +402.0pts remaining (episode 398.0pts, major)
- forward worst false alarm: 2026-09-14 16:41 -115.5pts adverse
- earliness (backtest): median 84.8 pts of move remaining at fire (n=12)

### H8 — 1 signal
*Reversal-signature bar anatomy (upthrust/spring) predicts imminent range expansion irrespective of direction.*
Grading: either-direction. Latest review: keep-watching (recommendation).

**S0-H8** — session × window grid (cells as in the matrix):

| session | backtest | forward |
|---|---|---|
| whole | ▼i-12.4pp (75/281) · p+8.0pp cap75.2 | ▼i-3.1pp (319/896) · p+3.2pp cap46.2 |
| london | ▼i-4.0pp (25/62) · p+7.7pp cap57.2 | ▼i-7.9pp (89/266) · p+1.9pp cap67.5 |
| overlap | (°▼i-23.1pp (0/22) · p+21.2pp cap114.2) | (°▼i-10.3pp (5/41) · p+10.1pp cap95.0) |
| ny_only | ▼i-26.9pp (5/60) · p+37.2pp cap154.5 | ▼i-4.5pp (34/124) · p-3.0pp cap24.5 |
| dead | ▼i-11.5pp (7/41) · p+10.0pp cap10.5 | ·i-1.3pp (58/149) · p+11.4pp cap40.0 |
| asia | ▼i-6.3pp (38/96) · p-7.7pp cap47.2 | ▼i-2.3pp (133/316) · p+1.0pp cap28.5 |

- backtest payoff: n/a by construction (either-direction)
- backtest best call: 2026-07-29 10:42 +781.0pts remaining (episode 752.0pts, major)
- backtest worst false alarm: 2026-07-27 16:47 -152.0pts adverse
- forward payoff: n/a by construction (either-direction)
- forward best call: 2026-09-03 10:01 +661.0pts remaining (episode 664.0pts, major)
- forward worst false alarm: 2026-08-19 16:19 -145.5pts adverse
- earliness (backtest): median 100.5 pts of move remaining at fire (n=27)

### H9 — 2 signals
*Persistent lower-TF directional pressure that recruits expanding participation at the parent timeframe precedes continuation beyond what the parent label alone predicts; pressure without participation expansion does not.*
Grading: directional. Latest review: keep-watching (recommendation).

- Question **Q2-H9**: see the register entry (status there is authoritative).
**S0-H9** — session × window grid (cells as in the matrix):

| session | backtest | forward |
|---|---|---|
| whole | ▼i-13.5pp (3/40) · p-1.5pp cap66.0 net-353/med-14.7 | ·i+0.6pp (22/102) · p-5.7pp cap84.5 net-834/med-7.5 |
| london | (°▼i-24.0pp (0/3) · p-3.5pp cap52.0 net-198/med-61.5) | ·i+0.7pp (7/31) · p+1.6pp cap99.0 net+109/med+14.5 |
| overlap | (°▼i-11.6pp (0/2) · p-32.9pp cap— net-19/med-9.5) | (°▲i+55.5pp (4/6) · p-16.3pp cap92.5 net-234/med-45.0) |
| ny_only | (°▼i-9.1pp (1/10) · p-3.5pp cap464.5 net-196/med-66.5) | ▼i-12.4pp (1/21) · p-9.0pp cap— net-196/med-8.5 |
| dead | (°▼i-14.6pp (0/7) · p-7.2pp cap— net+60/med+15.5) | (°▲i+6.9pp (3/10) · p+2.1pp cap88.0 net+66/med+8.0) |
| asia | (°▼i-13.7pp (2/18) · p+15.0pp cap66.0 net-1/med-11.2) | ▼i-3.9pp (7/34) · p-11.9pp cap39.5 net-578/med-16.0 |

- backtest payoff: right +876 / wrong -1229 / net -353 pts; median per fire -14.70 (n=38)
- backtest best call: 2026-08-03 05:40 +463.0pts remaining (episode 472.0pts, major)
- backtest worst false alarm: 2026-08-03 17:15 -176.0pts adverse
- forward payoff: right +1506 / wrong -2340 / net -834 pts; median per fire -7.50 (n=100)
- forward best call: 2026-09-11 11:15 +374.5pts remaining (episode 377.5pts, major)
- forward worst false alarm: 2026-09-09 14:30 -164.0pts adverse
- earliness (backtest): median 351.5 pts of move remaining at fire (n=2)

**S1-H9** — session × window grid (cells as in the matrix):

| session | backtest | forward |
|---|---|---|
| whole | (°▼i-21.0pp (0/9) · p-1.8pp cap273.0 net+460/med+1.5) | ▼i-18.4pp (1/39) · p-7.4pp cap81.0 net-638/med-16.0 |
| london | (°▼i-24.0pp (0/1) · p-36.8pp cap— net-38/med-38.0) | (°▼i-21.9pp (0/12) · p-3.8pp cap97.2 net-303/med-42.5) |
| overlap | — | (°▼i-11.2pp (0/1) · p-33.0pp cap— net-101/med-101.0) |
| ny_only | (°▼i-19.1pp (0/4) · p+11.5pp cap464.5 net+421/med+15.3) | (°▼i-8.1pp (1/11) · p-9.0pp cap— net-106/med-13.0) |
| dead | — | (°▼i-23.1pp (0/3) · p+25.4pp cap88.0 net+40/med+28.5) |
| asia | (°▼i-24.8pp (0/4) · p+1.1pp cap81.5 net+76/med+12.8) | (°▼i-24.5pp (0/12) · p-12.8pp cap64.8 net-168/med-16.0) |

- backtest payoff: right +601 / wrong -141 / net +460 pts; median per fire +1.50 (n=9)
- backtest worst false alarm: 2026-07-27 16:10 -84.0pts adverse
- forward payoff: right +585 / wrong -1223 / net -638 pts; median per fire -16.00 (n=39)
- forward best call: 2026-09-09 15:30 +145.5pts remaining (episode 192.5pts)
- forward worst false alarm: 2026-09-09 14:30 -164.0pts adverse

### H10 — 1 signal
*In an established 1-minute trend, no-demand/no-supply prints in the trend's direction signal continuation.*
Grading: directional. Latest review: deprioritize (recommendation).

**S0-H10** — session × window grid (cells as in the matrix):

| session | backtest | forward |
|---|---|---|
| whole | ·i-1.5pp (30/154) · p+0.0pp cap71.0 net+1774/med+11.0 | ▼i-5.6pp (92/597) · p-4.0pp cap68.1 net-1294/med-0.5 |
| london | ▼i-19.0pp (2/40) · p+3.2pp cap116.0 net+1480/med+27.5 | ·i-1.9pp (30/150) · p-1.8pp cap80.5 net-341/med-8.0 |
| overlap | (°▼i-11.6pp (0/5) · p-32.9pp cap— net+36/med+33.0) | (°▲i+3.1pp (6/42) · p+2.7pp cap85.0 net-288/med+6.5) |
| ny_only | ▼i-3.7pp (4/26) · p+1.9pp cap80.9 net-348/med+48.8 | ▼i-6.1pp (15/135) · p-6.0pp cap89.2 net-1262/med+2.0 |
| dead | ▲i+15.4pp (6/20) · p-7.2pp cap— net-74/med-5.7 | ▼i-9.1pp (12/86) · p-4.4pp cap41.5 net-365/med-4.0 |
| asia | ▲i+3.8pp (18/63) · p+3.1pp cap50.5 net+680/med+8.0 | ▼i-8.7pp (29/184) · p-1.2pp cap49.2 net+962/med+3.0 |

- backtest payoff: right +4228 / wrong -2454 / net +1774 pts; median per fire +11.00 (n=154)
- backtest best call: 2026-07-31 10:20 +555.5pts remaining (episode 569.0pts, major)
- backtest worst false alarm: 2026-08-03 17:10 -197.0pts adverse
- forward payoff: right +9324 / wrong -10618 / net -1294 pts; median per fire -0.50 (n=596)
- forward best call: 2026-08-31 09:59 +350.0pts remaining (episode 343.0pts, major)
- forward worst false alarm: 2026-09-01 15:56 -234.0pts adverse
- earliness (backtest): median 87.5 pts of move remaining at fire (n=11)

### H11 — 2 signals
*Price entering a low-volume price zone traverses it faster than baseline; entering a high-volume node it stalls or reverses at above-baseline rates.*
Grading: directional. Latest review: keep-watching (recommendation).

- Question **Q1-H11**: see the register entry (status there is authoritative).
- Question **Q2-H11**: see the register entry (status there is authoritative).
**S0-H11** — session × window grid (cells as in the matrix):

| session | backtest | forward |
|---|---|---|
| whole | ·i-0.7pp (84/413) · p+3.4pp cap98.0 net+1254/med+3.0 | ▼i-4.6pp (151/920) · p-0.1pp cap75.2 net+1117/med-2.5 |
| london | ▼i-5.6pp (30/163) · p+0.6pp cap91.0 net-404/med+5.0 | ▼i-9.7pp (36/294) · p+2.0pp cap82.0 net+1498/med+3.5 |
| overlap | (°▼i-7.8pp (1/26) · p+20.9pp cap261.2 net+491/med+4.0) | (°▼i-4.1pp (7/98) · p-5.4pp cap143.0 net+626/med+6.5) |
| ny_only | ▲i+7.1pp (11/42) · p-1.6pp cap239.5 net+1037/med+15.2 | ▲i+3.5pp (43/208) · p+1.1pp cap103.5 net-178/med-3.0 |
| dead | ▼i-6.6pp (4/50) · p+14.8pp cap99.5 net+478/med+1.2 | ▼i-5.5pp (16/91) · p+0.9pp cap72.3 net-766/med-4.8 |
| asia | ▲i+4.0pp (38/132) · p-7.2pp cap62.5 net-348/med+2.0 | ▼i-3.1pp (49/229) · p-2.9pp cap43.0 net-64/med-3.5 |

- backtest payoff: right +12694 / wrong -11440 / net +1254 pts; median per fire +3.00 (n=413)
- backtest best call: 2026-07-31 09:39 +496.0pts remaining (episode 569.0pts, major)
- backtest worst false alarm: 2026-07-31 13:24 -492.5pts adverse
- forward payoff: right +20924 / wrong -19807 / net +1117 pts; median per fire -2.50 (n=919)
- forward best call: 2026-09-03 09:58 +643.5pts remaining (episode 664.0pts, major)
- forward worst false alarm: 2026-09-11 12:31 -323.1pts adverse
- earliness (backtest): median 90.5 pts of move remaining at fire (n=23)

**S1-H11** — session × window grid (cells as in the matrix):

| session | backtest | forward |
|---|---|---|
| whole | ▲i+6.0pp (51/189) · p+0.9pp cap167.0 net+1560/med+0.5 | ▼i-4.9pp (147/914) · p+4.0pp cap80.5 net+1305/med+2.5 |
| london | (°▼i-14.9pp (1/11) · p+8.7pp cap194.5 net+136/med-24.5) | ▼i-2.4pp (74/379) · p+0.6pp cap81.4 net+2542/med+5.5 |
| overlap | (°▲i+22.9pp (10/29) · p+11.9pp cap250.5 net+278/med+23.0) | (°·i-0.5pp (11/103) · p+4.9pp cap156.5 net-948/med-11.0) |
| ny_only | ▼i-4.2pp (7/47) · p+14.2pp cap181.4 net+1460/med+17.0 | ▼i-2.3pp (20/134) · p-0.8pp cap112.0 net-532/med-0.2 |
| dead | ▲i+26.3pp (9/22) · p+11.0pp cap86.0 net+232/med+18.2 | ▼i-10.6pp (10/80) · p+3.3pp cap97.0 net+265/med-0.6 |
| asia | ▲i+5.2pp (24/80) · p-8.9pp cap66.2 net-546/med-6.2 | ▼i-9.8pp (32/218) · p+0.8pp cap52.5 net-24/med+2.5 |

- backtest payoff: right +9216 / wrong -7657 / net +1560 pts; median per fire +0.50 (n=189)
- backtest best call: 2026-07-28 04:46 +523.0pts remaining (episode 543.0pts, major)
- backtest worst false alarm: 2026-07-29 18:58 -665.0pts adverse
- forward payoff: right +24405 / wrong -23100 / net +1305 pts; median per fire +2.50 (n=913)
- forward best call: 2026-09-03 09:11 +587.0pts remaining (episode 664.0pts, major)
- forward worst false alarm: 2026-09-15 13:25 -457.5pts adverse
- earliness (backtest): median 97.5 pts of move remaining at fire (n=8)

### H12 — 1 signal
*A zone showing repeated visits with elevated volume, diminishing range-per-unit-volume, and drying pullback volume precedes a directional move away from the zone in the absorber's direction.*
Grading: directional. Latest review: keep-watching (recommendation).

**S0-H12** — session × window grid (cells as in the matrix):

| session | backtest | forward |
|---|---|---|
| whole | — | (°▼i-21.0pp (0/1) · p-25.3pp cap— net+20/med+19.9) |
| london | — | (°▼i-21.9pp (0/1) · p-37.1pp cap— net+20/med+19.9) |
| overlap | — | — |
| ny_only | — | — |
| dead | — | — |
| asia | — | — |

- forward payoff: right +20 / wrong +0 / net +20 pts; median per fire +19.90 (n=1)
- forward worst false alarm: 2026-09-16 08:34 -11.0pts adverse

### H13 — 1 signal
*After price breaks out of the session value area on declining volume and reclaims it on expanding volume, it continues toward the far side of the value area.*
Grading: directional. Latest review: keep-watching (recommendation).

**S0-H13** — session × window grid (cells as in the matrix):

| session | backtest | forward |
|---|---|---|
| whole | (°▲i+79.0pp (1/1) · p-24.0pp cap— net-206/med-206.0) | (°▼i-21.0pp (0/5) · p+34.7pp cap125.0 net+147/med+12.0) |
| london | (°▲i+76.0pp (1/1) · p-36.8pp cap— net-206/med-206.0) | (°▼i-21.9pp (0/1) · p-37.1pp cap— net-58/med-58.0) |
| overlap | — | (°▼i-11.2pp (0/1) · p+67.0pp cap177.5 net+70/med+70.5) |
| ny_only | — | (°▼i-17.2pp (0/1) · p+91.0pp cap125.0 net+125/med+125.0) |
| dead | — | — |
| asia | — | (°▼i-24.5pp (0/2) · p+20.5pp cap47.0 net+10/med+4.8) |

- backtest payoff: right +0 / wrong -206 / net -206 pts; median per fire -206.00 (n=1)
- backtest best call: 2026-07-28 10:27 +-158.5pts remaining (episode 93.5pts)
- backtest worst false alarm: 2026-07-28 10:27 -252.0pts adverse
- forward payoff: right +208 / wrong -60 / net +147 pts; median per fire +12.00 (n=5)
- forward worst false alarm: 2026-08-31 12:13 -129.5pts adverse
- earliness (backtest): median -158.5 pts of move remaining at fire (n=1)

### H14 — 1 signal
*Counter-trend No Demand / No Supply prints in an established trend mark absorption and precede trend continuation.*
Grading: directional. Latest review: keep-watching (recommendation).

**S0-H14** — session × window grid (cells as in the matrix):

| session | backtest | forward |
|---|---|---|
| whole | ▲i+4.0pp (37/148) · p+2.4pp cap76.0 net+2606/med+12.5 | ▼i-6.7pp (80/558) · p+0.0pp cap67.0 net+618/med-1.3 |
| london | ▼i-17.6pp (3/47) · p+12.1pp cap106.0 net+1414/med+12.5 | ·i-0.4pp (32/149) · p-0.2pp cap92.0 net+1222/med-3.4 |
| overlap | (°▼i-11.6pp (0/7) · p-32.9pp cap— net-40/med+17.0) | (°·i-1.8pp (3/32) · p-1.8pp cap77.2 net-600/med-2.5) |
| ny_only | ·i-1.9pp (5/29) · p-6.6pp cap85.7 net+804/med+53.0 | ▼i-6.4pp (12/111) · p-1.8pp cap118.2 net-1075/med-1.5 |
| dead | (°▲i+38.0pp (10/19) · p-1.9pp cap104.9 net-80/med-14.4) | ▼i-13.6pp (7/74) · p+5.6pp cap38.2 net-41/med-1.8 |
| asia | ▲i+16.5pp (19/46) · p+4.4pp cap46.5 net+508/med+7.5 | ▼i-11.0pp (26/192) · p+0.7pp cap48.5 net+1112/med+0.8 |

- backtest payoff: right +4618 / wrong -2012 / net +2606 pts; median per fire +12.50 (n=148)
- backtest best call: 2026-08-03 05:18 +451.0pts remaining (episode 472.0pts, major)
- backtest worst false alarm: 2026-07-28 13:00 -258.0pts adverse
- forward payoff: right +9974 / wrong -9357 / net +618 pts; median per fire -1.30 (n=558)
- forward best call: 2026-09-01 03:31 +400.0pts remaining (episode 398.0pts, major)
- forward worst false alarm: 2026-09-16 14:24 -229.5pts adverse
- earliness (backtest): median 71.0 pts of move remaining at fire (n=12)

### H15 — 1 signal
*A range sweep followed by aggressive traversal to the opposite boundary continues toward the range's volume center.*
Grading: directional. Latest review: keep-watching (recommendation).

**S0-H15** — session × window grid (cells as in the matrix):

| session | backtest | forward |
|---|---|---|
| whole | — | — |
| london | — | — |
| overlap | — | — |
| ny_only | — | — |
| dead | — | — |
| asia | — | — |


### H16 — 1 signal
*The opening session's direction predicts the closing session's direction.*
Grading: directional. Latest review: keep-watching (recommendation).

**S0-H16** — session × window grid (cells as in the matrix):

| session | backtest | forward |
|---|---|---|
| whole | (°▼i-21.0pp (0/10) · p+36.0pp cap98.2 net+522/med+37.5) | ▼i-16.8pp (1/24) · p-0.3pp cap68.8 net+109/med+0.5 |
| london | — | — |
| overlap | — | — |
| ny_only | (°▼i-19.1pp (0/10) · p+46.5pp cap98.2 net+522/med+37.5) | ▼i-13.0pp (1/24) · p+16.0pp cap68.8 net+109/med+0.5 |
| dead | — | — |
| asia | — | — |

- backtest payoff: right +588 / wrong -66 / net +522 pts; median per fire +37.50 (n=10)
- backtest worst false alarm: 2026-07-28 19:30 -58.0pts adverse
- forward payoff: right +544 / wrong -435 / net +109 pts; median per fire +0.50 (n=24)
- forward best call: 2026-08-31 19:30 +58.0pts remaining (episode 72.5pts)
- forward worst false alarm: 2026-09-10 19:30 -104.0pts adverse

### H17 — 1 signal
*A climax reversal signal followed by absorption within five bars — effort meeting a quiet counter-party — marks a genuine exhaustion turn: the two-chapter story (exhaustion needs absorption to become reversal).*
Grading: directional. Latest review: rows (recommendation).

**S0-H17** — session × window grid (cells as in the matrix):

| session | backtest | forward |
|---|---|---|
| whole | ▲i+2.1pp (6/26) · p+2.9pp cap119.5 net-167/med-10.5 | ▲i+6.8pp (47/169) · p-5.2pp cap64.8 net-2134/med-12.5 |
| london | (°▲i+16.0pp (4/10) · p-6.8pp cap157.5 net+113/med+12.2) | ▲i+9.1pp (18/58) · p-18.1pp cap86.5 net-2013/med-38.5 |
| overlap | — | (°▼i-11.2pp (0/5) · p-13.0pp cap196.0 net-176/med-83.0) |
| ny_only | (°▲i+30.9pp (1/2) · p-13.5pp cap— net-281/med-140.5) | ▼i-2.2pp (3/20) · p-4.0pp cap163.0 net+119/med+1.0 |
| dead | (°▲i+10.4pp (1/4) · p-7.2pp cap— net-211/med-48.2) | ▲i+10.2pp (8/24) · p+4.6pp cap76.6 net+177/med+3.5 |
| asia | (°▼i-24.8pp (0/10) · p+16.1pp cap75.8 net+212/med+33.2) | ▲i+4.5pp (18/62) · p-0.5pp cap47.0 net-240/med-7.0 |

- backtest payoff: right +792 / wrong -958 / net -167 pts; median per fire -10.50 (n=26)
- backtest best call: 2026-07-29 10:09 +794.0pts remaining (episode 752.0pts, major)
- backtest worst false alarm: 2026-07-29 16:25 -203.5pts adverse
- forward payoff: right +3161 / wrong -5295 / net -2134 pts; median per fire -12.50 (n=169)
- forward best call: 2026-08-20 09:21 +405.0pts remaining (episode 411.5pts, major)
- forward worst false alarm: 2026-08-20 11:26 -260.0pts adverse
- earliness (backtest): median 110.0 pts of move remaining at fire (n=6)

### H18 — 1 signal
*A gap-traversal signal followed by a same-direction effortless print within five bars — travel meeting no opposition — continues: the map says vacuum, the tape confirms no resistance.*
Grading: directional. Latest review: rows (recommendation).

**S0-H18** — session × window grid (cells as in the matrix):

| session | backtest | forward |
|---|---|---|
| whole | ▲i+2.9pp (16/67) · p+2.9pp cap102.5 net+355/med+2.5 | ▼i-8.5pp (20/160) · p-2.8pp cap69.0 net-1434/med-6.8 |
| london | ·i+1.0pp (7/28) · p+2.5pp cap87.5 net+681/med+46.2 | ▼i-9.4pp (6/48) · p+4.6pp cap66.0 net-46/med+9.5 |
| overlap | (°▼i-11.6pp (0/9) · p+11.5pp cap252.2 net-157/med-78.0) | (°▼i-6.9pp (1/23) · p-11.3pp cap137.0 net-896/med-49.0) |
| ny_only | (°▼i-2.4pp (1/6) · p+3.2pp cap147.5 net-94/med-19.0) | ·i+1.4pp (8/43) · p-2.0pp cap69.0 net-158/med+1.0 |
| dead | (°▼i-14.6pp (0/5) · p-7.2pp cap— net+32/med-6.6) | (°▼i-14.0pp (1/11) · p+1.2pp cap98.5 net-195/med-13.5) |
| asia | (°▲i+17.3pp (8/19) · p-13.4pp cap61.5 net-107/med+2.5) | ▼i-13.1pp (4/35) · p-9.5pp cap45.0 net-138/med-10.0 |

- backtest payoff: right +2707 / wrong -2352 / net +355 pts; median per fire +2.50 (n=67)
- backtest best call: 2026-08-03 05:12 +445.5pts remaining (episode 472.0pts, major)
- backtest worst false alarm: 2026-07-28 15:04 -332.5pts adverse
- forward payoff: right +2780 / wrong -4214 / net -1434 pts; median per fire -6.75 (n=160)
- forward best call: 2026-08-18 09:56 +194.0pts remaining (episode 240.0pts, major)
- forward worst false alarm: 2026-09-11 13:59 -233.0pts adverse
- earliness (backtest): median 120.0 pts of move remaining at fire (n=11)

### H19 — 1 signal
*A probe-failure reversal signal followed by continued wide-loud effort in the anchor bar's own close direction within five bars is NOT the start of the claimed reversal — a SUPPRESSION/FADE configuration, and it says so.*
Grading: directional. Latest review: rows (recommendation).

- Question **Q1-H19**: see the register entry (status there is authoritative).
**S0-H19** — session × window grid (cells as in the matrix):

| session | backtest | forward |
|---|---|---|
| whole | ▼i-11.1pp (17/172) · p+10.3pp cap130.0 net+2236/med+3.2 | ·i+0.5pp (120/559) · p+2.1pp cap81.5 net-231/med+2.0 |
| london | ▼i-5.2pp (6/32) · p+7.0pp cap135.5 net+708/med+34.0 | ▲i+2.2pp (40/166) · p-3.4pp cap91.5 net-1876/med+0.0 |
| overlap | (°▼i-11.6pp (0/12) · p+58.8pp cap144.0 net+894/med+109.5) | (°▼i-7.2pp (1/25) · p+27.0pp cap155.0 net+452/med+79.5) |
| ny_only | ▼i-14.3pp (2/42) · p+24.6pp cap317.8 net+879/med+3.2 | ▼i-6.8pp (8/77) · p-2.5pp cap143.5 net+359/med+13.0 |
| dead | ▼i-11.5pp (1/32) · p+8.4pp cap107.0 net-17/med-1.0 | ·i+1.6pp (22/89) · p+10.1pp cap87.0 net+542/med-1.5 |
| asia | ▼i-10.0pp (8/54) · p+0.2pp cap68.5 net-228/med-3.0 | ·i-0.2pp (49/202) · p+0.7pp cap61.5 net+292/med+1.0 |

- backtest payoff: right +9284 / wrong -7047 / net +2236 pts; median per fire +3.25 (n=172)
- backtest best call: 2026-07-28 04:49 +523.0pts remaining (episode 543.0pts, major)
- backtest worst false alarm: 2026-07-29 19:00 -643.0pts adverse
- forward payoff: right +12965 / wrong -13196 / net -231 pts; median per fire +2.00 (n=559)
- forward best call: 2026-09-03 10:03 +654.0pts remaining (episode 664.0pts, major)
- forward worst false alarm: 2026-08-28 14:30 -277.5pts adverse
- earliness (backtest): median 100.0 pts of move remaining at fire (n=12)

### H20 — 1 signal
*A wide-bar close-through of a session extreme (the same conditioned wide-bar class the retest anchor fires on; resolution = the close beyond the level, not a rejection back inside) initiates continuation in the break direction.*
Grading: directional. Latest review: rows (recommendation).

**S0-H20** — session × window grid (cells as in the matrix):

| session | backtest | forward |
|---|---|---|
| whole | ▼i-11.8pp (2/58) · p-11.4pp cap114.0 [cls 40.7%/15.2%i] net+27/med+18.2 | ▼i-11.4pp (3/163) · p+4.3pp cap120.8 [cls 42.3%/13.2%i] net-162/med-8.0 |
| london | ▼i-13.7pp (2/37) · p-16.8pp cap87.5 [cls 41.1%/19.1%i] net-532/med+4.5 | ▼i-13.7pp (2/104) · p+19.0pp cap124.2 [cls 42.5%/15.6%i] net+2815/med+36.0 |
| overlap | (°▼i-9.2pp (0/12) · p+8.5pp cap148.8 [cls 41.5%/9.2%i] net+728/med+69.0) | (°▼i-7.6pp (0/35) · p-25.1pp cap124.0 [cls 45.1%/7.6%i] net-2233/med-67.5) |
| ny_only | (°▼i-5.4pp (0/4) · p-17.3pp cap217.5 [cls 42.3%/5.4%i] net-81/med-9.4) | (°▲i+7.8pp (1/5) · p-9.8pp cap— [cls 9.8%/12.2%i] net-192/med-31.5) |
| dead | (°▼i-7.4pp (0/2) · p-11.8pp cap— [cls 11.8%/7.4%i] net-51/med-25.7) | (°▼i-10.4pp (0/1) · p-17.7pp cap— [cls 17.7%/10.4%i] net-45/med-44.6) |
| asia | (°▼i-20.5pp (0/3) · p-6.3pp cap40.5 [cls 39.6%/20.5%i] net-36/med+11.0) | (°▼i-14.1pp (0/18) · p-18.1pp cap66.0 [cls 45.9%/14.1%i] net-507/med-19.5) |

- backtest payoff: right +1911 / wrong -1883 / net +27 pts; median per fire +18.25 (n=58)
- backtest best call: 2026-07-28 12:44 +200.0pts remaining (episode 347.0pts, major)
- backtest worst false alarm: 2026-07-27 13:28 -308.4pts adverse
- forward payoff: right +6733 / wrong -6895 / net -162 pts; median per fire -8.00 (n=163)
- forward best call: 2026-09-01 17:26 +48.5pts remaining (episode 108.0pts)
- forward worst false alarm: 2026-08-19 12:51 -260.0pts adverse
- earliness (backtest): median 200.0 pts of move remaining at fire (n=1)


---

Appendix: the per-session detail beyond London and every horizon-mark payoff live in hypothesis_performance.json (generated, same run).