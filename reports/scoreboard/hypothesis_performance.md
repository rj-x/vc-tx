# Hypothesis Performance — Per-Instrument

Terms: [docs/GLOSSARY.md](../../docs/GLOSSARY.md).

Engine `79c2cdd41` — register 40 fence as amended 2026-08-19 (operator): one section per instrument, each computed only from that instrument's own store and native calendar; uk100 canonical, ger40/nas100/us30 PROVISIONAL (validation pending). Numbers are NEVER pooled across instruments — cross-instrument aggregation is a future registration. This first cross-instrument read is EXPLORATORY: expectations deliberately unregistered; anything interesting becomes a pre-registered question before it becomes a claim.

---

# uk100 (uk100fut) — CANONICAL

Store span (1M, close ts): 2026-07-12 22:06:00+00:00 → 2026-08-28 19:59:00+00:00. Volume type: real futures volume (step-zero audit).

## Summary Matrix (page 1)

Engine `79c2cdd41` — OBSERVATIONAL signal scoreboard - move-detection, not trading; no fills exist here by construction; never validation (docs/hypothesis_lifecycle.md stage 4)

**Review labels are RECOMMENDATIONS — none actioned, review pending operator familiarity.** Cells: marker + precision LIFT vs that context's OWN chance rate, (hits/fires), payoff net/median points (directional rows; either-direction rows have no payoff by construction). ▲/▼ = beyond ±2pp of chance, · = within. (°…) = small-n (fires<20 or episodes<10): dimmed, excluded from any future label arithmetic. Read READING_GUIDE.md first; full detail in hypothesis_performance.json.

| H | label | backtest whole | backtest london | forward whole | forward london |
|---|---|---|---|---|---|
| *context* | | 177 ep; chance 23.7%dir/44.4%either | 52 ep; chance 24.9%dir/47.2%either | 101 ep; chance 24.1%dir/43.9%either | 23 ep; chance 27.1%dir/50.5%either |
| S0-H1 | keep-watching | ▲i+6.7pp (21/69) · p+0.9pp cap38.8 net+194/med+2.8 | ·i+1.0pp (6/22) · p+11.5pp cap38.5 net+133/med+3.0 | ▲i+6.1pp (25/92) · p+0.9pp cap16.5 net+113/med+0.2 | ▲i+16.4pp (9/25) · p+8.9pp cap22.0 net+105/med+7.5 |
| S1-H1 | keep-watching | (°▼i-3.7pp (1/5) · p-3.7pp cap59.3 net+9/med+3.0) | — | (°▼i-4.4pp (1/6) · p+9.2pp cap25.8 net+18/med+5.7) | (°▲i+5.4pp (1/4) · p+22.9pp cap25.8 net+35/med+9.0) |
| S0-H2 | promote-candidate | ·i-0.4pp (81/347) · p+1.1pp cap34.8 net+781/med+1.5 | ▼i-3.8pp (18/80) · p+6.3pp cap40.0 net+521/med+9.2 | ·i-0.7pp (69/339) · p-0.2pp cap13.0 net+174/med-0.1 | ▼i-3.4pp (11/68) · p+3.8pp cap26.0 net+245/med+2.8 |
| S1-H2 | promote-candidate | ·i+0.1pp (60/252) · p+0.5pp cap34.2 net+540/med+0.9 | ·i+0.8pp (16/59) · p+5.6pp cap39.0 net+559/med+12.0 | ·i-0.5pp (56/272) · p+3.1pp cap13.0 net+273/med+0.3 | ·i+0.4pp (11/55) · p+5.6pp cap26.0 net+263/med+3.5 |
| S0-H3 | keep-watching | — | — | (°▲i+5.6pp (4/15) · p+15.9pp cap8.6 net-5/med+0.8) | (°▲i+30.4pp (2/4) · p-2.1pp cap19.5 net-14/med+2.2) |
| S0-H4 | keep-watching | (°▲i+19.2pp (3/7) · p-23.7pp cap— net+14/med+0.5) | (°▼i-26.3pp (0/1) · p-24.9pp cap— net+6/med+5.5) | — | — |
| S0-H5 | keep-watching | — | — | — | — |
| S0-H6 | keep-watching | ·i+0.8pp (9/59) · p+8.2pp cap33.8 [cls 37.6%/14.5%i] net+391/med+5.7 | ·i+0.1pp (4/31) · p+20.5pp cap32.9 [cls 37.6%/12.8%i] net+282/med+16.0 | ·i+0.5pp (7/66) · p+7.2pp cap20.2 [cls 42.8%/10.1%i] net+202/med+4.0 | ▼i-2.5pp (3/41) · p+10.3pp cap17.3 [cls 40.9%/9.8%i] net+40/med+2.7 |
| S0-H7 | keep-watching | ▲i+7.5pp (35/112) · p+5.8pp cap32.0 net+7/med+2.8 | ▲i+12.7pp (16/41) · p+1.9pp cap32.0 net-217/med+2.7 | ▼i-4.2pp (15/89) · p+2.9pp cap23.6 net+233/med+2.5 | ▼i-11.7pp (3/38) · p+9.7pp cap24.1 net+70/med+1.8 |
| S0-H7 (either-dir) | keep-watching | ·i-0.7pp (47/112) · p+7.4pp cap15.8 | ▲i+4.1pp (21/41) · p+1.6pp cap20.0 | ·i-1.6pp (33/89) · p-3.5pp cap19.4 | ▼i-4.0pp (13/38) · p+2.1pp cap20.0 |
| S0-H8 | keep-watching | ▼i-3.2pp (137/347) · p+2.0pp cap17.0 | ▼i-15.9pp (25/80) · p+5.3pp cap34.5 | ▼i-4.5pp (116/339) · p-0.8pp cap7.8 | ▼i-4.4pp (23/68) · p+1.0pp cap21.0 |
| S0-H9 | keep-watching | ▲i+5.4pp (16/55) · p+7.2pp cap26.6 net+319/med+3.5 | (°▼i-17.2pp (1/11) · p+20.6pp cap45.0 net+108/med+12.5) | ▲i+5.8pp (7/26) · p-20.3pp cap16.0 net-117/med-3.6 | (°▼i-19.6pp (0/3) · p-27.1pp cap— net-44/med-8.3) |
| S1-H9 | keep-watching | (°▼i-13.2pp (2/19) · p+23.7pp cap45.0 net+263/med+12.8) | (°▼i-26.3pp (0/8) · p+25.1pp cap57.1 net+148/med+17.8) | (°▼i-12.0pp (1/11) · p-24.1pp cap— net-67/med-7.0) | (°▼i-19.6pp (0/1) · p-27.1pp cap— net-34/med-33.5) |
| S0-H10 | deprioritize | ▼i-8.3pp (45/293) · p-4.2pp cap27.0 net-240/med-1.4 | ▼i-12.7pp (9/66) · p+2.4pp cap33.2 net-62/med+1.9 | ▲i+2.1pp (41/177) · p-12.8pp cap16.9 net-374/med-1.5 | ▼i-6.1pp (5/37) · p-5.5pp cap19.3 net+46/med-1.0 |
| S0-H11 | keep-watching | ·i-0.9pp (72/316) · p+2.6pp cap32.2 net-647/med-2.4 | ▲i+2.1pp (42/148) · p-1.3pp cap35.0 net+250/med-0.6 | ▼i-6.1pp (28/187) · p+3.7pp cap16.5 net+258/med+1.7 | ▼i-7.9pp (11/94) · p-4.8pp cap19.3 net+91/med+0.9 |
| S1-H11 | keep-watching | ▼i-5.6pp (28/155) · p-1.8pp cap33.2 net-617/med-0.7 | ▼i-2.0pp (9/37) · p-8.7pp cap34.0 net-466/med-15.7 | ▼i-4.4pp (30/180) · p+3.7pp cap20.8 net-269/med-0.5 | ▼i-3.1pp (13/79) · p+5.8pp cap21.3 net-165/med-4.0 |
| S0-H12 | keep-watching | — | — | — | — |
| S0-H13 | keep-watching | (°▲i+26.3pp (1/2) · p+26.3pp cap37.0 net+28/med+13.8) | (°▲i+23.7pp (1/2) · p+25.1pp cap37.0 net+28/med+13.8) | (°▼i-6.8pp (1/7) · p-9.8pp cap6.7 net-66/med-8.0) | (°▲i+30.4pp (1/2) · p-27.1pp cap— net-16/med-8.2) |
| S0-H14 | keep-watching | ▼i-8.4pp (45/294) · p-8.7pp cap24.8 net-695/med-1.9 | ▼i-10.2pp (10/62) · p-5.5pp cap28.1 net-81/med+3.1 | ▲i+3.1pp (45/186) · p-12.3pp cap15.8 net-495/med-2.2 | ·i+1.1pp (6/29) · p-3.0pp cap18.7 net-57/med-3.2 |
| S0-H15 | keep-watching | — | — | — | — |
| S0-H16 | keep-watching | (°▼i-3.7pp (3/15) · p+3.0pp cap33.4 net+5/med+6.0) | — | (°·i-1.1pp (2/10) · p-14.1pp cap24.7 net+41/med+6.8) | — |
| S0-H17 | rows | ▲i+10.4pp (14/41) · p-6.6pp cap41.5 net+76/med+2.5 | (°▲i+9.4pp (5/14) · p+3.7pp cap40.0 net+32/med+4.4) | ·i-0.8pp (12/59) · p+1.3pp cap16.5 net+14/med-0.5 | (°▲i+5.4pp (4/16) · p+10.4pp cap22.8 net+24/med-0.8) |
| S0-H18 | rows | ▼i-5.7pp (11/61) · p+4.2pp cap34.0 net+169/med-1.0 | ▼i-14.3pp (3/25) · p+11.1pp cap45.5 net+266/med+1.3 | ▼i-6.5pp (6/41) · p+12.5pp cap15.5 net+97/med+5.0 | ▼i-3.6pp (4/25) · p-7.1pp cap19.2 net+12/med-1.5 |
| S0-H19 | rows | ▼i-4.9pp (40/213) · p-2.1pp cap34.1 net-631/med-1.5 | ▼i-12.7pp (6/44) · p-13.5pp cap55.5 net-334/med-11.0 | ▼i-5.1pp (25/156) · p+0.9pp cap14.0 net-137/med-0.5 | ·i-1.4pp (6/33) · p-5.9pp cap29.3 net-140/med-1.5 |
| S0-H20 | rows | ▼i-10.5pp (2/50) · p-9.6pp cap67.0 [cls 37.6%/14.5%i] net-221/med-9.7 | ▼i-12.8pp (0/28) · p+1.7pp cap75.5 [cls 37.6%/12.8%i] net+241/med-5.2 | ▼i-10.1pp (0/45) · p-9.5pp cap18.5 [cls 42.8%/10.1%i] net-128/med-2.5 | ▼i-9.8pp (0/24) · p-7.6pp cap21.0 [cls 40.9%/9.8%i] net-141/med-6.7 |
| **union coverage** | | 59.9% (106/177) | 59.6% (31/52) | 86.1% (87/101) | 87.0% (20/23) |

### Dual-convention side-by-side — load-bearing patterns

| pattern | context | initiation | participation (cap) |
|---|---|---|---|
| Q1-H1 away cells (S0-H1) | uk100fut/forward | 27.2% (25/92) | 25.0% (cap 16.5) |
| Q1-H1 away cells (S0-H1) | ger40fut/forward | 25.5% (25/98) | 32.7% (cap 37.8) |
| Q1-H1 away cells (S0-H1) | nas100fut/forward | 30.4% (21/69) | 37.7% (cap 78.5) |
| Q1-H1 away cells (S0-H1) | us30fut/forward | 27.9% (39/140) | 27.9% (cap 60.5) |
| H2 forward (S0-H2) | uk100fut/forward | 20.4% (69/339) | 23.9% (cap 13.0) |
| H2 forward (S0-H2) | ger40fut/forward | 20.5% (74/361) | 23.8% (cap 35.5) |
| H2 forward (S0-H2) | nas100fut/forward | 18.6% (76/408) | 31.4% (cap 81.4) |
| H2 forward (S0-H2) | us30fut/forward | 17.0% (80/470) | 25.3% (cap 66.0) |
| H2 forward (S1-H2) | uk100fut/forward | 20.6% (56/272) | 27.2% (cap 13.0) |
| H2 forward (S1-H2) | ger40fut/forward | 24.7% (66/267) | 22.5% (cap 35.2) |
| H2 forward (S1-H2) | nas100fut/forward | 22.0% (64/291) | 29.9% (cap 82.8) |
| H2 forward (S1-H2) | us30fut/forward | 19.9% (67/337) | 23.1% (cap 66.5) |
| S0-H8 (either-dir) | uk100fut/backtest | 39.5% (137/347) | 46.4% (cap 17.0) |
| S0-H8 (either-dir) | ger40fut/backtest | 30.8% (72/234) | 53.4% (cap 36.4) |
| S0-H8 (either-dir) | nas100fut/backtest | 36.6% (117/320) | 44.1% (cap 65.1) |
| S0-H8 (either-dir) | us30fut/backtest | 25.6% (72/281) | 52.3% (cap 76.0) |
| S0-H6 (conditioned) | uk100fut/backtest | 15.3% (9/59) | 45.8% (cap 33.8) |
| S0-H6 (conditioned) | ger40fut/backtest | 2.8% (1/36) | 38.9% (cap 59.3) |
| S0-H6 (conditioned) | nas100fut/backtest | 17.2% (5/29) | 31.0% (cap 260.8) |
| S0-H6 (conditioned) | us30fut/backtest | 5.8% (3/52) | 19.2% (cap 175.0) |
| S0-H8 (either-dir) | uk100fut/forward | 34.2% (116/339) | 43.1% (cap 7.8) |
| S0-H8 (either-dir) | ger40fut/forward | 42.9% (155/361) | 39.1% (cap 23.0) |
| S0-H8 (either-dir) | nas100fut/forward | 41.7% (170/408) | 50.0% (cap 61.6) |
| S0-H8 (either-dir) | us30fut/forward | 34.0% (160/470) | 44.0% (cap 45.5) |
| S0-H6 (conditioned) | uk100fut/forward | 10.6% (7/66) | 50.0% (cap 20.2) |
| S0-H6 (conditioned) | ger40fut/forward | 34.0% (33/97) | 35.1% (cap 44.6) |
| S0-H6 (conditioned) | nas100fut/forward | 20.7% (17/82) | 43.9% (cap 92.4) |
| S0-H6 (conditioned) | us30fut/forward | 26.5% (22/83) | 36.1% (cap 100.5) |


Not graded:  — see register entries.

## Hypothesis Cards (page 2)

### H1 — 2 signals
*A climactic bar — extreme volume on a wide spread late in an extended move — marks exhaustion, and price then reverses against the climax direction.*
Grading: directional. Latest review: keep-watching (recommendation).

- Question **Q1-H1**: see the register entry (status there is authoritative).
**S0-H1** — session × window grid (cells as in the matrix):

| session | backtest | forward |
|---|---|---|
| whole | ▲i+6.7pp (21/69) · p+0.9pp cap38.8 net+194/med+2.8 | ▲i+6.1pp (25/92) · p+0.9pp cap16.5 net+113/med+0.2 |
| london | ·i+1.0pp (6/22) · p+11.5pp cap38.5 net+133/med+3.0 | ▲i+16.4pp (9/25) · p+8.9pp cap22.0 net+105/med+7.5 |
| overlap | (°▼i-16.3pp (0/2) · p+23.9pp cap27.5 net+35/med+17.7) | (°▼i-15.5pp (0/3) · p-25.2pp cap— net-26/med-4.7) |
| ny_only | ▲i+19.6pp (9/22) · p+7.9pp cap46.9 net+17/med+1.6 | ▼i-7.1pp (3/21) · p+3.8pp cap10.2 net+11/med+0.2 |
| dead | (°▲i+2.5pp (4/12) · p+7.3pp cap15.3 net+30/med+1.1) | (°▲i+17.0pp (7/15) · p+21.4pp cap10.0 net+35/med+2.7) |
| asia | (°▼i-4.2pp (2/11) · p-23.5pp cap59.3 net-22/med-2.6) | ·i+0.4pp (6/28) · p-14.7pp cap13.1 net-10/med-1.1 |

- backtest payoff: right +639 / wrong -445 / net +194 pts; median per fire +2.75 (n=68)
- backtest best call: 2026-07-29 04:04 +105.2pts remaining (episode 102.8pts, major)
- backtest worst false alarm: 2026-07-23 12:17 -70.7pts adverse
- forward payoff: right +386 / wrong -273 / net +113 pts; median per fire +0.20 (n=92)
- forward best call: 2026-08-21 09:11 +74.0pts remaining (episode 95.0pts, major)
- forward worst false alarm: 2026-08-20 15:03 -30.7pts adverse
- earliness (backtest): median 35.3 pts of move remaining at fire (n=21)

**S1-H1** — session × window grid (cells as in the matrix):

| session | backtest | forward |
|---|---|---|
| whole | (°▼i-3.7pp (1/5) · p-3.7pp cap59.3 net+9/med+3.0) | (°▼i-4.4pp (1/6) · p+9.2pp cap25.8 net+18/med+5.7) |
| london | — | (°▲i+5.4pp (1/4) · p+22.9pp cap25.8 net+35/med+9.0) |
| overlap | — | (°▼i-15.5pp (0/1) · p-25.2pp cap— net-21/med-21.2) |
| ny_only | (°▼i-21.3pp (0/1) · p-10.3pp cap— net-13/med-13.3) | — |
| dead | (°▼i-30.8pp (0/1) · p-17.7pp cap— net+3/med+3.0) | (°▼i-29.7pp (0/1) · p-18.6pp cap— net+4/med+3.9) |
| asia | (°▲i+10.9pp (1/3) · p+0.7pp cap59.3 net+19/med+5.5) | — |

- backtest payoff: right +59 / wrong -50 / net +9 pts; median per fire +3.00 (n=5)
- backtest best call: 2026-07-29 04:04 +105.2pts remaining (episode 102.8pts, major)
- backtest worst false alarm: 2026-07-30 05:53 -37.6pts adverse
- forward payoff: right +53 / wrong -35 / net +18 pts; median per fire +5.70 (n=6)
- forward best call: 2026-08-17 12:27 +5.7pts remaining (episode 19.5pts)
- forward worst false alarm: 2026-08-20 15:03 -30.7pts adverse
- earliness (backtest): median 105.2 pts of move remaining at fire (n=1)

### H2 — 2 signals
*A failed probe beyond a prior extreme — an upthrust above or spring below that closes back inside — reverses against the probe.*
Grading: directional. Latest review: promote-candidate (recommendation).

**S0-H2** — session × window grid (cells as in the matrix):

| session | backtest | forward |
|---|---|---|
| whole | ·i-0.4pp (81/347) · p+1.1pp cap34.8 net+781/med+1.5 | ·i-0.7pp (69/339) · p-0.2pp cap13.0 net+174/med-0.1 |
| london | ▼i-3.8pp (18/80) · p+6.3pp cap40.0 net+521/med+9.2 | ▼i-3.4pp (11/68) · p+3.8pp cap26.0 net+245/med+2.8 |
| overlap | (°▼i-7.2pp (1/11) · p+1.2pp cap39.0 net+21/med+3.5) | (°▲i+13.1pp (4/14) · p-3.8pp cap30.2 net+82/med+5.8) |
| ny_only | ▼i-4.9pp (9/55) · p+4.2pp cap40.8 net-487/med-2.5 | ▼i-2.7pp (14/75) · p-3.0pp cap18.2 net-22/med-0.7 |
| dead | ▼i-3.0pp (25/90) · p+1.2pp cap23.2 net+180/med+0.8 | ▼i-14.2pp (9/58) · p+9.0pp cap9.4 net+39/med+1.0 |
| asia | ▲i+2.8pp (28/111) · p-2.9pp cap29.8 net+546/med+2.7 | ▲i+4.0pp (31/124) · p-4.6pp cap10.4 net-169/med-0.7 |

- backtest payoff: right +3270 / wrong -2490 / net +781 pts; median per fire +1.50 (n=347)
- backtest best call: 2026-07-30 04:03 +155.1pts remaining (episode 178.3pts, major)
- backtest worst false alarm: 2026-07-24 06:52 -98.0pts adverse
- forward payoff: right +1374 / wrong -1200 / net +174 pts; median per fire -0.05 (n=338)
- forward best call: 2026-08-27 11:34 +68.8pts remaining (episode 60.8pts, major)
- forward worst false alarm: 2026-08-20 14:42 -45.3pts adverse
- earliness (backtest): median 28.4 pts of move remaining at fire (n=38)

**S1-H2** — session × window grid (cells as in the matrix):

| session | backtest | forward |
|---|---|---|
| whole | ·i+0.1pp (60/252) · p+0.5pp cap34.2 net+540/med+0.9 | ·i-0.5pp (56/272) · p+3.1pp cap13.0 net+273/med+0.3 |
| london | ·i+0.8pp (16/59) · p+5.6pp cap39.0 net+559/med+12.0 | ·i+0.4pp (11/55) · p+5.6pp cap26.0 net+263/med+3.5 |
| overlap | (°▼i-7.2pp (1/11) · p+1.2pp cap39.0 net+21/med+3.5) | (°▲i+7.6pp (3/13) · p-2.1pp cap30.2 net+94/med+7.5) |
| ny_only | ▼i-3.8pp (7/40) · p+4.7pp cap38.6 net-304/med-2.1 | ▼i-3.9pp (10/57) · p-2.2pp cap18.2 net-15/med-0.7 |
| dead | ▼i-6.2pp (15/61) · p+5.3pp cap23.0 net+201/med+0.8 | ▼i-18.6pp (5/45) · p+14.7pp cap9.6 net+63/med+2.7 |
| asia | ▲i+3.5pp (21/81) · p-7.9pp cap28.4 net+62/med-1.2 | ▲i+5.5pp (27/102) · p-0.8pp cap9.9 net-132/med-0.7 |

- backtest payoff: right +2121 / wrong -1581 / net +540 pts; median per fire +0.95 (n=252)
- backtest best call: 2026-07-30 04:03 +155.1pts remaining (episode 178.3pts, major)
- backtest worst false alarm: 2026-07-29 19:00 -94.0pts adverse
- forward payoff: right +1192 / wrong -919 / net +273 pts; median per fire +0.30 (n=272)
- forward best call: 2026-08-27 11:34 +68.8pts remaining (episode 60.8pts, major)
- forward worst false alarm: 2026-08-26 06:26 -45.0pts adverse
- earliness (backtest): median 31.3 pts of move remaining at fire (n=35)

### H3 — 1 signal
*Repeated absorption — high effort with no result — at a price level precedes a breakout through that level.*
Grading: directional. Latest review: keep-watching (recommendation).

**S0-H3** — session × window grid (cells as in the matrix):

| session | backtest | forward |
|---|---|---|
| whole | — | (°▲i+5.6pp (4/15) · p+15.9pp cap8.6 net-5/med+0.8) |
| london | — | (°▲i+30.4pp (2/4) · p-2.1pp cap19.5 net-14/med+2.2) |
| overlap | — | — |
| ny_only | — | (°▲i+3.6pp (1/4) · p-5.7pp cap— net+7/med+1.9) |
| dead | — | (°▼i-29.7pp (0/1) · p+81.4pp cap7.1 net-0/med-0.2) |
| asia | — | (°▼i-4.3pp (1/6) · p+30.6pp cap8.6 net+2/med+1.1) |

- forward payoff: right +47 / wrong -52 / net -5 pts; median per fire +0.80 (n=15)
- forward best call: 2026-08-20 11:13 +45.0pts remaining (episode 70.0pts, major)
- forward worst false alarm: 2026-08-20 11:13 -39.0pts adverse

### H4 — 1 signal
*In an established trend, a quiet (low-volume) pullback resolves with trend resumption.*
Grading: directional. Latest review: keep-watching (recommendation).

**S0-H4** — session × window grid (cells as in the matrix):

| session | backtest | forward |
|---|---|---|
| whole | (°▲i+19.2pp (3/7) · p-23.7pp cap— net+14/med+0.5) | — |
| london | (°▼i-26.3pp (0/1) · p-24.9pp cap— net+6/med+5.5) | — |
| overlap | — | — |
| ny_only | (°▲i+28.7pp (3/6) · p-10.3pp cap— net+8/med-0.1) | — |
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
| whole | ·i+0.8pp (9/59) · p+8.2pp cap33.8 [cls 37.6%/14.5%i] net+391/med+5.7 | ·i+0.5pp (7/66) · p+7.2pp cap20.2 [cls 42.8%/10.1%i] net+202/med+4.0 |
| london | ·i+0.1pp (4/31) · p+20.5pp cap32.9 [cls 37.6%/12.8%i] net+282/med+16.0 | ▼i-2.5pp (3/41) · p+10.3pp cap17.3 [cls 40.9%/9.8%i] net+40/med+2.7 |
| overlap | (°▲i+32.7pp (3/6) · p-30.0pp cap— [cls 30.0%/17.3%i] net-87/med-15.4) | (°▲i+20.3pp (3/8) · p-19.4pp cap30.7 [cls 31.9%/17.2%i] net-11/med+4.5) |
| ny_only | (°▲i+35.3pp (2/4) · p-20.5pp cap— [cls 20.5%/14.7%i] net+0/med+6.5) | (°▼i-6.1pp (0/2) · p-6.7pp cap— [cls 6.7%/6.1%i] net-7/med-3.4) |
| dead | (°▼i-9.6pp (0/5) · p-19.1pp cap— [cls 19.1%/9.6%i] net-25/med-6.4) | — |
| asia | (°▼i-15.9pp (0/13) · p+24.6pp cap44.8 [cls 44.6%/15.9%i] net+220/med+5.7) | (°·i-1.6pp (1/15) · p+18.2pp cap23.5 [cls 55.1%/8.3%i] net+180/med+7.3) |

- backtest payoff: right +818 / wrong -428 / net +391 pts; median per fire +5.70 (n=59)
- backtest best call: 2026-07-31 08:00 +72.8pts remaining (episode 68.5pts, major)
- backtest worst false alarm: 2026-07-22 08:07 -80.3pts adverse
- forward payoff: right +567 / wrong -365 / net +202 pts; median per fire +4.05 (n=66)
- forward best call: 2026-08-26 13:22 +40.8pts remaining (episode 52.3pts, major)
- forward worst false alarm: 2026-08-27 08:00 -52.0pts adverse
- earliness (backtest): median 21.6 pts of move remaining at fire (n=8)

### H7 — 1 signal
*Quiet decline at a session extreme is disguised accumulation: effortless (low-volume) weakness reverses UP once selling fails to attract participation (mirror: quiet advance at a high reverses down).*
Grading: directional + either-direction (dual). Latest review: keep-watching (recommendation).

- Question **Q1-H7**: see the register entry (status there is authoritative).
**S0-H7** — session × window grid (cells as in the matrix):

| session | backtest | forward |
|---|---|---|
| whole | ▲i+7.5pp (35/112) · p+5.8pp cap32.0 net+7/med+2.8 | ▼i-4.2pp (15/89) · p+2.9pp cap23.6 net+233/med+2.5 |
| london | ▲i+12.7pp (16/41) · p+1.9pp cap32.0 net-217/med+2.7 | ▼i-11.7pp (3/38) · p+9.7pp cap24.1 net+70/med+1.8 |
| overlap | ▼i-3.3pp (3/23) · p+8.7pp cap39.2 net+227/med+8.7 | (°▼i-5.5pp (1/10) · p-5.2pp cap37.2 net+34/med+2.6) |
| ny_only | (°·i+0.1pp (3/14) · p+4.0pp cap27.6 net-24/med+0.0) | (°▲i+11.9pp (5/15) · p-5.7pp cap— net+31/med+2.2) |
| dead | (°▲i+49.2pp (4/5) · p+2.3pp cap51.1 net+60/med+3.5) | (°▼i-4.7pp (1/4) · p+6.4pp cap13.6 net+7/med-1.4) |
| asia | ▲i+8.6pp (9/29) · p+5.3pp cap20.7 net-38/med+0.7 | ·i+1.7pp (5/22) · p-4.3pp cap19.8 net+90/med+3.8 |

- backtest payoff: right +1097 / wrong -1090 / net +7 pts; median per fire +2.80 (n=112)
- backtest best call: 2026-07-22 04:18 +132.7pts remaining (episode 139.7pts, major)
- backtest worst false alarm: 2026-07-30 06:55 -94.0pts adverse
- forward payoff: right +556 / wrong -323 / net +233 pts; median per fire +2.50 (n=89)
- forward best call: 2026-08-26 10:44 +53.5pts remaining (episode 58.0pts, major)
- forward worst false alarm: 2026-08-20 12:44 -43.0pts adverse
- earliness (backtest): median 29.8 pts of move remaining at fire (n=29)

**S0-H7 (either-dir)** — session × window grid (cells as in the matrix):

| session | backtest | forward |
|---|---|---|
| whole | ·i-0.7pp (47/112) · p+7.4pp cap15.8 | ·i-1.6pp (33/89) · p-3.5pp cap19.4 |
| london | ▲i+4.1pp (21/41) · p+1.6pp cap20.0 | ▼i-4.0pp (13/38) · p+2.1pp cap20.0 |
| overlap | ·i+0.2pp (7/23) · p+5.3pp cap32.5 | (°▼i-11.0pp (2/10) · p-9.6pp cap15.2) |
| ny_only | (°▼i-16.4pp (3/14) · p+8.4pp cap13.4) | (°▲i+30.7pp (10/15) · p-11.3pp cap—) |
| dead | (°▲i+26.6pp (4/5) · p-13.1pp cap51.1) | (°▼i-6.6pp (2/4) · p-11.8pp cap13.6) |
| asia | ·i-0.1pp (12/29) · p+9.4pp cap10.1 | ▼i-9.8pp (6/22) · p-11.8pp cap13.0 |

- backtest payoff: n/a by construction (either-direction)
- backtest best call: 2026-07-22 04:18 +132.7pts remaining (episode 139.7pts, major)
- backtest worst false alarm: 2026-07-23 16:44 -25.7pts adverse
- forward payoff: n/a by construction (either-direction)
- forward best call: 2026-08-27 11:56 +68.8pts remaining (episode 60.8pts, major)
- forward worst false alarm: 2026-08-17 10:09 -18.3pts adverse
- earliness (backtest): median 16.8 pts of move remaining at fire (n=40)

### H8 — 1 signal
*Reversal-signature bar anatomy (upthrust/spring) predicts imminent range expansion irrespective of direction.*
Grading: either-direction. Latest review: keep-watching (recommendation).

**S0-H8** — session × window grid (cells as in the matrix):

| session | backtest | forward |
|---|---|---|
| whole | ▼i-3.2pp (137/347) · p+2.0pp cap17.0 | ▼i-4.5pp (116/339) · p-0.8pp cap7.8 |
| london | ▼i-15.9pp (25/80) · p+5.3pp cap34.5 | ▼i-4.4pp (23/68) · p+1.0pp cap21.0 |
| overlap | (°▼i-12.0pp (2/11) · p+12.4pp cap18.3) | (°▲i+4.7pp (5/14) · p-21.0pp cap29.3) |
| ny_only | ▼i-6.9pp (17/55) · p+23.4pp cap6.9 | ▼i-10.7pp (19/75) · p-6.0pp cap5.4 |
| dead | ▼i-4.5pp (44/90) · p+1.3pp cap13.9 | ▼i-18.7pp (22/58) · p+11.5pp cap6.5 |
| asia | ▲i+2.6pp (49/111) · p-8.2pp cap19.0 | ·i+0.8pp (47/124) · p-1.3pp cap5.6 |

- backtest payoff: n/a by construction (either-direction)
- backtest best call: 2026-07-30 04:03 +155.1pts remaining (episode 178.3pts, major)
- backtest worst false alarm: 2026-07-22 10:02 -37.0pts adverse
- forward payoff: n/a by construction (either-direction)
- forward best call: 2026-08-27 11:34 +68.8pts remaining (episode 60.8pts, major)
- forward worst false alarm: 2026-08-28 15:49 -21.5pts adverse
- earliness (backtest): median 26.6 pts of move remaining at fire (n=57)

### H9 — 2 signals
*Persistent lower-TF directional pressure that recruits expanding participation at the parent timeframe precedes continuation beyond what the parent label alone predicts; pressure without participation expansion does not.*
Grading: directional. Latest review: keep-watching (recommendation).

- Question **Q2-H9**: see the register entry (status there is authoritative).
**S0-H9** — session × window grid (cells as in the matrix):

| session | backtest | forward |
|---|---|---|
| whole | ▲i+5.4pp (16/55) · p+7.2pp cap26.6 net+319/med+3.5 | ▲i+5.8pp (7/26) · p-20.3pp cap16.0 net-117/med-3.6 |
| london | (°▼i-17.2pp (1/11) · p+20.6pp cap45.0 net+108/med+12.5) | (°▼i-19.6pp (0/3) · p-27.1pp cap— net-44/med-8.3) |
| overlap | — | (°▼i-15.5pp (0/1) · p-25.2pp cap— net-1/med-1.0) |
| ny_only | (°▲i+20.4pp (5/12) · p+14.7pp cap69.9 net+115/med+2.8) | (°▲i+11.9pp (2/6) · p+11.0pp cap16.0 net-5/med-2.4) |
| dead | (°▼i-3.5pp (3/11) · p-8.6pp cap26.6 net+11/med+1.0) | (°▼i-29.7pp (0/2) · p-18.6pp cap—) |
| asia | ▲i+10.9pp (7/21) · p+5.5pp cap14.0 net+86/med+6.8 | (°▲i+14.7pp (5/14) · p-36.1pp cap— net-68/med-3.6) |

- backtest payoff: right +558 / wrong -239 / net +319 pts; median per fire +3.50 (n=53)
- backtest best call: 2026-08-03 03:40 +73.2pts remaining (episode 81.3pts, major)
- backtest worst false alarm: 2026-07-30 09:15 -59.3pts adverse
- forward payoff: right +27 / wrong -144 / net -117 pts; median per fire -3.60 (n=24)
- forward best call: 2026-08-21 15:30 +16.7pts remaining (episode 20.0pts)
- forward worst false alarm: 2026-08-27 09:00 -33.5pts adverse
- earliness (backtest): median 15.6 pts of move remaining at fire (n=10)

**S1-H9** — session × window grid (cells as in the matrix):

| session | backtest | forward |
|---|---|---|
| whole | (°▼i-13.2pp (2/19) · p+23.7pp cap45.0 net+263/med+12.8) | (°▼i-12.0pp (1/11) · p-24.1pp cap— net-67/med-7.0) |
| london | (°▼i-26.3pp (0/8) · p+25.1pp cap57.1 net+148/med+17.8) | (°▼i-19.6pp (0/1) · p-27.1pp cap— net-34/med-33.5) |
| overlap | — | (°▼i-15.5pp (0/1) · p-25.2pp cap— net-1/med-1.0) |
| ny_only | (°▼i-21.3pp (0/4) · p+64.7pp cap69.9 net+105/med+31.6) | (°▼i-21.4pp (0/1) · p-5.7pp cap— net-8/med-8.2) |
| dead | (°▼i-10.8pp (1/5) · p+2.3pp cap26.6 net+6/med+2.3) | (°▼i-29.7pp (0/2) · p-18.6pp cap—) |
| asia | (°▲i+27.6pp (1/2) · p+17.4pp cap20.2 net+4/med+2.1) | (°▼i-4.3pp (1/6) · p-36.1pp cap— net-24/med-5.2) |

- backtest payoff: right +377 / wrong -114 / net +263 pts; median per fire +12.75 (n=18)
- backtest best call: 2026-07-19 23:10 +9.2pts remaining (episode 30.7pts)
- backtest worst false alarm: 2026-07-30 09:15 -59.3pts adverse
- forward payoff: right +2 / wrong -69 / net -67 pts; median per fire -7.00 (n=9)
- forward best call: 2026-08-20 02:15 +-1.0pts remaining (episode 8.8pts)
- forward worst false alarm: 2026-08-27 09:00 -33.5pts adverse
- earliness (backtest): median 9.2 pts of move remaining at fire (n=1)

### H10 — 1 signal
*In an established 1-minute trend, no-demand/no-supply prints in the trend's direction signal continuation.*
Grading: directional. Latest review: deprioritize (recommendation).

**S0-H10** — session × window grid (cells as in the matrix):

| session | backtest | forward |
|---|---|---|
| whole | ▼i-8.3pp (45/293) · p-4.2pp cap27.0 net-240/med-1.4 | ▲i+2.1pp (41/177) · p-12.8pp cap16.9 net-374/med-1.5 |
| london | ▼i-12.7pp (9/66) · p+2.4pp cap33.2 net-62/med+1.9 | ▼i-6.1pp (5/37) · p-5.5pp cap19.3 net+46/med-1.0 |
| overlap | (°▼i-16.3pp (0/7) · p-26.1pp cap— net+27/med+6.8) | (°▼i-15.5pp (0/7) · p-25.2pp cap— net-73/med-12.2) |
| ny_only | ▼i-2.0pp (16/83) · p-0.7pp cap25.3 net+51/med-1.5 | ▲i+2.1pp (12/51) · p+0.2pp cap24.0 net+24/med-0.3 |
| dead | ·i-0.2pp (11/36) · p-3.8pp cap11.5 net-110/med-2.5 | ▲i+2.3pp (8/25) · p-14.6pp cap14.8 net-47/med-0.7 |
| asia | ▼i-13.5pp (9/101) · p-6.9pp cap25.8 net-147/med-1.5 | ▲i+7.1pp (16/57) · p-22.1pp cap11.2 net-325/med-4.2 |

- backtest payoff: right +1533 / wrong -1773 / net -240 pts; median per fire -1.40 (n=293)
- backtest best call: 2026-07-23 10:20 +90.0pts remaining (episode 104.8pts, major)
- backtest worst false alarm: 2026-07-28 13:10 -62.5pts adverse
- forward payoff: right +406 / wrong -780 / net -374 pts; median per fire -1.50 (n=177)
- forward best call: 2026-08-24 09:51 +37.0pts remaining (episode 47.8pts, major)
- forward worst false alarm: 2026-08-27 08:22 -42.0pts adverse
- earliness (backtest): median 21.6 pts of move remaining at fire (n=24)

### H11 — 2 signals
*Price entering a low-volume price zone traverses it faster than baseline; entering a high-volume node it stalls or reverses at above-baseline rates.*
Grading: directional. Latest review: keep-watching (recommendation).

- Question **Q1-H11**: see the register entry (status there is authoritative).
- Question **Q2-H11**: see the register entry (status there is authoritative).
**S0-H11** — session × window grid (cells as in the matrix):

| session | backtest | forward |
|---|---|---|
| whole | ·i-0.9pp (72/316) · p+2.6pp cap32.2 net-647/med-2.4 | ▼i-6.1pp (28/187) · p+3.7pp cap16.5 net+258/med+1.7 |
| london | ▲i+2.1pp (42/148) · p-1.3pp cap35.0 net+250/med-0.6 | ▼i-7.9pp (11/94) · p-4.8pp cap19.3 net+91/med+0.9 |
| overlap | ▲i+8.7pp (10/40) · p-18.6pp cap33.5 net-403/med-11.8 | (°·i+1.2pp (4/24) · p+24.8pp cap20.5 net+85/med+8.0) |
| ny_only | ▼i-5.5pp (6/38) · p+18.6pp cap34.0 net-267/med-1.6 | ·i-0.7pp (6/29) · p+8.1pp cap12.6 net+36/med+1.9 |
| dead | ▼i-15.8pp (3/20) · p+37.3pp cap18.5 net+59/med+0.7 | (°▼i-29.7pp (0/8) · p+6.4pp cap12.6 net+27/med+3.5) |
| asia | ▼i-6.7pp (11/70) · p+0.3pp cap18.0 net-286/med-4.5 | ·i+0.9pp (7/32) · p+4.5pp cap14.7 net+19/med+1.6 |

- backtest payoff: right +2555 / wrong -3203 / net -647 pts; median per fire -2.35 (n=316)
- backtest best call: 2026-07-22 04:16 +129.0pts remaining (episode 139.7pts, major)
- backtest worst false alarm: 2026-07-22 07:36 -96.5pts adverse
- forward payoff: right +1020 / wrong -761 / net +258 pts; median per fire +1.70 (n=187)
- forward best call: 2026-08-25 10:20 +43.0pts remaining (episode 60.0pts, major)
- forward worst false alarm: 2026-08-24 13:11 -50.8pts adverse
- earliness (backtest): median 25.6 pts of move remaining at fire (n=24)

**S1-H11** — session × window grid (cells as in the matrix):

| session | backtest | forward |
|---|---|---|
| whole | ▼i-5.6pp (28/155) · p-1.8pp cap33.2 net-617/med-0.7 | ▼i-4.4pp (30/180) · p+3.7pp cap20.8 net-269/med-0.5 |
| london | ▼i-2.0pp (9/37) · p-8.7pp cap34.0 net-466/med-15.7 | ▼i-3.1pp (13/79) · p+5.8pp cap21.3 net-165/med-4.0 |
| overlap | ▼i-16.3pp (0/30) · p+3.9pp cap34.5 net+73/med-1.6 | (°▼i-11.2pp (1/23) · p+5.2pp cap24.2 net-21/med-3.5) |
| ny_only | ▼i-7.0pp (6/42) · p+1.6pp cap20.8 net+75/med+0.7 | ▲i+4.4pp (8/31) · p-5.7pp cap— net-30/med-0.5 |
| dead | (°▲i+44.2pp (3/4) · p-17.7pp cap— net-21/med-4.5) | (°▼i-18.6pp (1/9) · p+25.8pp cap14.6 net+14/med+2.8) |
| asia | ·i+1.4pp (10/42) · p+0.7pp cap34.3 net-277/med-0.9 | ▼i-2.6pp (7/38) · p-1.9pp cap11.5 net-67/med+0.1 |

- backtest payoff: right +1033 / wrong -1650 / net -617 pts; median per fire -0.70 (n=155)
- backtest best call: 2026-07-24 03:18 +96.3pts remaining (episode 104.3pts, major)
- backtest worst false alarm: 2026-07-31 07:01 -103.0pts adverse
- forward payoff: right +746 / wrong -1015 / net -269 pts; median per fire -0.50 (n=180)
- forward best call: 2026-08-20 11:09 +45.0pts remaining (episode 70.0pts, major)
- forward worst false alarm: 2026-08-27 13:32 -45.3pts adverse
- earliness (backtest): median 22.8 pts of move remaining at fire (n=9)

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
| whole | (°▲i+26.3pp (1/2) · p+26.3pp cap37.0 net+28/med+13.8) | (°▼i-6.8pp (1/7) · p-9.8pp cap6.7 net-66/med-8.0) |
| london | (°▲i+23.7pp (1/2) · p+25.1pp cap37.0 net+28/med+13.8) | (°▲i+30.4pp (1/2) · p-27.1pp cap— net-16/med-8.2) |
| overlap | — | (°▼i-15.5pp (0/2) · p-25.2pp cap— net-17/med-8.6) |
| ny_only | — | (°▼i-21.4pp (0/1) · p-5.7pp cap— net-3/med-3.0) |
| dead | — | — |
| asia | — | (°▼i-21.0pp (0/2) · p+13.9pp cap6.7 net-30/med-14.8) |

- backtest payoff: right +28 / wrong +0 / net +28 pts; median per fire +13.75 (n=2)
- backtest best call: 2026-07-24 09:09 +43.2pts remaining (episode 42.7pts)
- backtest worst false alarm: 2026-07-24 09:09 -5.8pts adverse
- forward payoff: right +0 / wrong -66 / net -66 pts; median per fire -8.00 (n=7)
- forward best call: 2026-08-28 07:51 +3.5pts remaining (episode 14.5pts)
- forward worst false alarm: 2026-08-28 15:27 -20.5pts adverse
- earliness (backtest): median 43.2 pts of move remaining at fire (n=1)

### H14 — 1 signal
*Counter-trend No Demand / No Supply prints in an established trend mark absorption and precede trend continuation.*
Grading: directional. Latest review: keep-watching (recommendation).

**S0-H14** — session × window grid (cells as in the matrix):

| session | backtest | forward |
|---|---|---|
| whole | ▼i-8.4pp (45/294) · p-8.7pp cap24.8 net-695/med-1.9 | ▲i+3.1pp (45/186) · p-12.3pp cap15.8 net-495/med-2.2 |
| london | ▼i-10.2pp (10/62) · p-5.5pp cap28.1 net-81/med+3.1 | ·i+1.1pp (6/29) · p-3.0pp cap18.7 net-57/med-3.2 |
| overlap | (°▼i-16.3pp (0/4) · p-1.1pp cap24.0 net+20/med+5.6) | (°▼i-15.5pp (0/11) · p-16.1pp cap23.0 net-128/med-16.0) |
| ny_only | ▼i-5.1pp (16/99) · p-1.2pp cap24.5 net-174/med-3.1 | ▼i-2.8pp (11/59) · p-2.3pp cap17.9 net+49/med+1.0 |
| dead | ▲i+8.6pp (13/33) · p-11.6pp cap17.2 net-105/med-2.4 | ▲i+20.3pp (14/28) · p-18.6pp cap— net-117/med-2.4 |
| asia | ▼i-16.2pp (6/96) · p-11.8pp cap27.6 net-355/med-3.6 | ▲i+2.7pp (14/59) · p-15.8pp cap10.9 net-242/med-3.6 |

- backtest payoff: right +1293 / wrong -1989 / net -695 pts; median per fire -1.95 (n=294)
- backtest best call: 2026-07-31 11:45 +89.0pts remaining (episode 93.7pts, major)
- backtest worst false alarm: 2026-07-28 05:56 -59.0pts adverse
- forward payoff: right +416 / wrong -910 / net -495 pts; median per fire -2.25 (n=186)
- forward best call: 2026-08-27 03:22 +79.4pts remaining (episode 82.1pts, major)
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
| whole | (°▼i-3.7pp (3/15) · p+3.0pp cap33.4 net+5/med+6.0) | (°·i-1.1pp (2/10) · p-14.1pp cap24.7 net+41/med+6.8) |
| london | — | — |
| overlap | (°▲i+3.7pp (3/15) · p+0.6pp cap33.4 net+5/med+6.0) | (°▲i+4.5pp (2/10) · p-15.2pp cap24.7 net+41/med+6.8) |
| ny_only | — | — |
| dead | — | — |
| asia | — | — |

- backtest payoff: right +173 / wrong -169 / net +5 pts; median per fire +6.00 (n=15)
- backtest best call: 2026-08-03 15:00 +4.5pts remaining (episode 28.5pts)
- backtest worst false alarm: 2026-07-16 15:00 -61.7pts adverse
- forward payoff: right +72 / wrong -31 / net +41 pts; median per fire +6.75 (n=10)
- forward best call: 2026-08-21 15:00 +5.2pts remaining (episode 20.0pts)
- forward worst false alarm: 2026-08-17 15:00 -15.8pts adverse
- earliness (backtest): median -4.5 pts of move remaining at fire (n=3)

### H17 — 1 signal
*A climax reversal signal followed by absorption within five bars — effort meeting a quiet counter-party — marks a genuine exhaustion turn: the two-chapter story (exhaustion needs absorption to become reversal).*
Grading: directional. Latest review: rows (recommendation).

**S0-H17** — session × window grid (cells as in the matrix):

| session | backtest | forward |
|---|---|---|
| whole | ▲i+10.4pp (14/41) · p-6.6pp cap41.5 net+76/med+2.5 | ·i-0.8pp (12/59) · p+1.3pp cap16.5 net+14/med-0.5 |
| london | (°▲i+9.4pp (5/14) · p+3.7pp cap40.0 net+32/med+4.4) | (°▲i+5.4pp (4/16) · p+10.4pp cap22.8 net+24/med-0.8) |
| overlap | (°▼i-16.3pp (0/1) · p-26.1pp cap— net+12/med+12.0) | (°▼i-15.5pp (0/3) · p+8.1pp cap16.5 net-20/med-1.0) |
| ny_only | (°▲i+18.7pp (6/15) · p+3.0pp cap53.0 net+34/med+2.5) | (°·i+0.0pp (3/14) · p-5.7pp cap— net-17/med-0.8) |
| dead | (°▲i+29.2pp (3/5) · p-17.7pp cap— net-5/med-1.3) | (°▲i+7.8pp (3/8) · p+31.4pp cap9.8 net+10/med-0.1) |
| asia | (°▼i-22.4pp (0/6) · p-15.9pp cap60.8 net+3/med-2.3) | (°▼i-9.9pp (2/18) · p-13.9pp cap15.7 net+17/med+0.2) |

- backtest payoff: right +396 / wrong -320 / net +76 pts; median per fire +2.50 (n=41)
- backtest best call: 2026-07-30 12:44 +66.8pts remaining (episode 77.3pts, major)
- backtest worst false alarm: 2026-07-23 12:18 -71.0pts adverse
- forward payoff: right +226 / wrong -212 / net +14 pts; median per fire -0.50 (n=59)
- forward best call: 2026-08-21 09:16 +70.5pts remaining (episode 95.0pts, major)
- forward worst false alarm: 2026-08-20 15:06 -31.7pts adverse
- earliness (backtest): median 26.1 pts of move remaining at fire (n=12)

### H18 — 1 signal
*A gap-traversal signal followed by a same-direction effortless print within five bars — travel meeting no opposition — continues: the map says vacuum, the tape confirms no resistance.*
Grading: directional. Latest review: rows (recommendation).

**S0-H18** — session × window grid (cells as in the matrix):

| session | backtest | forward |
|---|---|---|
| whole | ▼i-5.7pp (11/61) · p+4.2pp cap34.0 net+169/med-1.0 | ▼i-6.5pp (6/41) · p+12.5pp cap15.5 net+97/med+5.0 |
| london | ▼i-14.3pp (3/25) · p+11.1pp cap45.5 net+266/med+1.3 | ▼i-3.6pp (4/25) · p-7.1pp cap19.2 net+12/med-1.5 |
| overlap | (°▲i+11.0pp (3/11) · p-7.9pp cap36.4 net-81/med-6.8) | (°▼i-15.5pp (0/5) · p+34.8pp cap20.2 net+53/med+19.2) |
| ny_only | (°▲i+12.0pp (2/6) · p-10.3pp cap— net+11/med+0.1) | (°▲i+18.6pp (2/5) · p+14.3pp cap8.0 net+11/med+4.7) |
| dead | (°▼i-30.8pp (0/1) · p+82.3pp cap19.2 net+18/med+17.6) | — |
| asia | (°▼i-5.7pp (3/18) · p-4.8pp cap22.3 net-44/med-1.9) | (°▼i-21.0pp (0/6) · p+63.9pp cap12.7 net+21/med+8.1) |

- backtest payoff: right +650 / wrong -482 / net +169 pts; median per fire -1.00 (n=61)
- backtest best call: 2026-07-27 03:05 +77.3pts remaining (episode 83.2pts, major)
- backtest worst false alarm: 2026-07-30 14:37 -50.0pts adverse
- forward payoff: right +294 / wrong -198 / net +97 pts; median per fire +5.00 (n=41)
- forward best call: 2026-08-25 12:27 +34.0pts remaining (episode 56.5pts, major)
- forward worst false alarm: 2026-08-25 12:27 -30.2pts adverse
- earliness (backtest): median 16.0 pts of move remaining at fire (n=9)

### H19 — 1 signal
*A probe-failure reversal signal followed by continued wide-loud effort in the anchor bar's own close direction within five bars is NOT the start of the claimed reversal — a SUPPRESSION/FADE configuration, and it says so.*
Grading: directional. Latest review: rows (recommendation).

- Question **Q1-H19**: see the register entry (status there is authoritative).
**S0-H19** — session × window grid (cells as in the matrix):

| session | backtest | forward |
|---|---|---|
| whole | ▼i-4.9pp (40/213) · p-2.1pp cap34.1 net-631/med-1.5 | ▼i-5.1pp (25/156) · p+0.9pp cap14.0 net-137/med-0.5 |
| london | ▼i-12.7pp (6/44) · p-13.5pp cap55.5 net-334/med-11.0 | ·i-1.4pp (6/33) · p-5.9pp cap29.3 net-140/med-1.5 |
| overlap | (°▼i-16.3pp (0/4) · p+23.9pp cap37.6 net+8/med+5.3) | (°▼i-15.5pp (0/6) · p-8.5pp cap16.0 net-54/med-14.5) |
| ny_only | ▼i-12.2pp (3/33) · p+35.2pp cap41.7 net+263/med+0.7 | ▼i-9.4pp (3/25) · p+2.3pp cap15.5 net+35/med-0.2 |
| dead | ·i+1.1pp (23/72) · p-3.8pp cap21.2 net-100/med-0.8 | ▼i-11.2pp (5/27) · p-0.1pp cap11.8 net-27/med-4.2 |
| asia | ▼i-9.1pp (8/60) · p-9.3pp cap26.8 net-469/med-2.0 | ▼i-4.1pp (11/65) · p+0.8pp cap13.5 net+49/med+0.7 |

- backtest payoff: right +1487 / wrong -2118 / net -631 pts; median per fire -1.50 (n=213)
- backtest best call: 2026-07-27 03:04 +78.6pts remaining (episode 83.2pts, major)
- backtest worst false alarm: 2026-07-29 18:44 -83.2pts adverse
- forward payoff: right +560 / wrong -698 / net -137 pts; median per fire -0.50 (n=156)
- forward best call: 2026-08-21 09:17 +70.5pts remaining (episode 95.0pts, major)
- forward worst false alarm: 2026-08-25 13:22 -38.2pts adverse
- earliness (backtest): median 25.8 pts of move remaining at fire (n=22)

### H20 — 1 signal
*A wide-bar close-through of a session extreme (the same conditioned wide-bar class the retest anchor fires on; resolution = the close beyond the level, not a rejection back inside) initiates continuation in the break direction.*
Grading: directional. Latest review: rows (recommendation).

**S0-H20** — session × window grid (cells as in the matrix):

| session | backtest | forward |
|---|---|---|
| whole | ▼i-10.5pp (2/50) · p-9.6pp cap67.0 [cls 37.6%/14.5%i] net-221/med-9.7 | ▼i-10.1pp (0/45) · p-9.5pp cap18.5 [cls 42.8%/10.1%i] net-128/med-2.5 |
| london | ▼i-12.8pp (0/28) · p+1.7pp cap75.5 [cls 37.6%/12.8%i] net+241/med-5.2 | ▼i-9.8pp (0/24) · p-7.6pp cap21.0 [cls 40.9%/9.8%i] net-141/med-6.7 |
| overlap | (°▼i-17.3pp (0/4) · p-30.0pp cap— [cls 30.0%/17.3%i] net-47/med-11.6) | (°▼i-17.2pp (0/9) · p+1.4pp cap25.0 [cls 31.9%/17.2%i] net+53/med+4.0) |
| ny_only | (°▲i+10.3pp (1/4) · p-20.5pp cap— [cls 20.5%/14.7%i] net+29/med+7.3) | (°▼i-6.1pp (0/1) · p-6.7pp cap— [cls 6.7%/6.1%i] net-2/med-2.5) |
| dead | (°▲i+23.7pp (1/3) · p-19.1pp cap— [cls 19.1%/9.6%i] net-41/med-14.3) | — |
| asia | (°▼i-15.9pp (0/11) · p-17.3pp cap30.5 [cls 44.6%/15.9%i] net-404/med-29.8) | (°▼i-8.3pp (0/11) · p-18.7pp cap9.8 [cls 55.1%/8.3%i] net-37/med-1.9) |

- backtest payoff: right +648 / wrong -869 / net -221 pts; median per fire -9.65 (n=50)
- backtest best call: 2026-07-20 16:42 +48.5pts remaining (episode 41.7pts)
- backtest worst false alarm: 2026-07-24 06:50 -96.0pts adverse
- forward payoff: right +151 / wrong -279 / net -128 pts; median per fire -2.50 (n=45)
- forward worst false alarm: 2026-08-20 12:06 -33.0pts adverse
- earliness (backtest): median 31.9 pts of move remaining at fire (n=2)


---

# ger40 (ger40fut) — CANONICAL

Store span (1M, close ts): 2026-07-19 22:42:00+00:00 → 2026-08-31 18:47:00+00:00. Volume type: real futures volume (register 40 first-sync sanity; canonical verdict at this instrument's validation evening).

## Summary Matrix (page 1)

Engine `79c2cdd41` — OBSERVATIONAL signal scoreboard - move-detection, not trading; no fills exist here by construction; never validation (docs/hypothesis_lifecycle.md stage 4)

**Review labels are RECOMMENDATIONS — none actioned, review pending operator familiarity.** Cells: marker + precision LIFT vs that context's OWN chance rate, (hits/fires), payoff net/median points (directional rows; either-direction rows have no payoff by construction). ▲/▼ = beyond ±2pp of chance, · = within. (°…) = small-n (fires<20 or episodes<10): dimmed, excluded from any future label arithmetic. Read READING_GUIDE.md first; full detail in hypothesis_performance.json.

| H | label | backtest whole | backtest london | forward whole | forward london |
|---|---|---|---|---|---|
| *context* | | 112 ep; chance 23.6%dir/45.1%either | 27 ep; chance 26.4%dir/51.3%either | 117 ep; chance 23.2%dir/43.1%either | 34 ep; chance 24.3%dir/45.9%either |
| S0-H1 | keep-watching | ▲i+5.1pp (13/49) · p+9.1pp cap90.7 net-83/med+0.7 | (°▼i-21.1pp (0/5) · p+33.6pp cap89.9 net+198/med+39.9) | ▲i+3.4pp (25/98) · p+9.5pp cap37.8 net+238/med-0.2 | ▲i+3.8pp (7/23) · p+23.5pp cap50.3 net+23/med-5.5 |
| S1-H1 | keep-watching | (°▲i+11.9pp (1/3) · p-23.6pp cap— net-72/med-34.2) | (°▼i-21.1pp (0/1) · p-26.4pp cap— net-54/med-53.5) | (°▲i+2.9pp (1/4) · p+1.8pp cap35.8 net-20/med-14.2) | (°▼i-26.6pp (0/1) · p-24.3pp cap— net-23/med-22.6) |
| S0-H2 | promote-candidate | ▼i-8.6pp (30/234) · p+1.2pp cap77.4 net-661/med-5.2 | (°▼i-7.8pp (2/15) · p-13.1pp cap86.6 net+93/med+9.8) | ·i-1.6pp (74/361) · p+0.6pp cap35.5 net-34/med+0.5 | ▲i+4.9pp (17/54) · p-9.5pp cap64.1 net-273/med-10.5 |
| S1-H2 | promote-candidate | ▼i-7.8pp (24/176) · p+2.5pp cap77.4 net-760/med-8.3 | (°▼i-5.7pp (2/13) · p-11.0pp cap86.6 net+136/med+14.0) | ▲i+2.6pp (66/267) · p-0.7pp cap35.2 net+11/med+0.7 | ▲i+7.5pp (14/41) · p-9.7pp cap72.5 net-202/med-11.4 |
| S0-H3 | keep-watching | (°▲i+3.6pp (2/8) · p-11.1pp cap70.3 net-28/med+2.0) | — | ▲i+2.9pp (5/20) · p-3.2pp cap30.6 net-17/med-0.5 | (°▼i-26.6pp (0/1) · p-24.3pp cap— net+19/med+18.8) |
| S0-H4 | keep-watching | ▼i-9.6pp (4/34) · p+8.8pp cap50.2 net+72/med+10.0 | (°▲i+8.9pp (3/10) · p-16.4pp cap50.2 net-30/med-3.7) | — | — |
| S0-H5 | keep-watching | — | — | — | — |
| S0-H6 | keep-watching | ▼i-11.4pp (1/36) · p+4.4pp cap59.3 [cls 34.5%/14.2%i] net-192/med-10.4 | (°▼i-4.3pp (1/18) · p-7.4pp cap78.7 [cls 35.2%/9.9%i] net-56/med-10.3) | ▲i+18.6pp (33/97) · p-3.5pp cap44.6 [cls 38.6%/15.4%i] net-1004/med-10.7 | ▲i+27.3pp (22/51) · p-10.1pp cap45.4 [cls 39.5%/15.8%i] net-873/med-21.9 |
| S0-H7 | keep-watching | ·i-1.1pp (12/59) · p+12.0pp cap97.8 net+761/med+4.2 | ▼i-11.1pp (2/20) · p+23.6pp cap86.9 net+719/med+33.0 | ▲i+7.3pp (20/68) · p-5.6pp cap56.5 net-182/med+0.1 | ▲i+12.1pp (12/31) · p-14.6pp cap88.2 net-191/med-0.3 |
| S0-H7 (either-dir) | keep-watching | ▼i-6.1pp (20/59) · p+19.3pp cap50.2 | ▼i-10.5pp (6/20) · p+23.7pp cap57.4 | ▼i-4.6pp (25/68) · p-0.5pp cap14.6 | ·i-0.4pp (15/31) · p-4.0pp cap8.5 |
| S0-H8 | keep-watching | ▼i-9.2pp (72/234) · p+8.3pp cap36.4 | (°▼i-20.5pp (3/15) · p-31.3pp cap68.2) | ·i+1.5pp (155/361) · p-4.0pp cap23.0 | ·i-0.7pp (26/54) · p-7.0pp cap14.4 |
| S0-H9 | keep-watching | ▲i+3.6pp (13/52) · p-8.2pp cap55.5 net-426/med-4.1 | (°▼i-21.1pp (0/3) · p-26.4pp cap— net+17/med+22.6) | ▼i-6.0pp (5/31) · p-10.3pp cap40.6 net-243/med-7.7 | (°▲i+6.7pp (1/3) · p-24.3pp cap— net-164/med-43.6) |
| S1-H9 | keep-watching | (°▼i-21.4pp (0/8) · p+26.4pp cap101.1 net-53/med+13.1) | — | ▼i-7.1pp (3/20) · p-3.2pp cap40.6 net-101/med-7.7 | (°▲i+73.4pp (1/1) · p-24.3pp cap— net-114/med-114.2) |
| S0-H10 | deprioritize | ▲i+4.5pp (38/147) · p-4.6pp cap50.5 net-391/med+3.2 | ▲i+2.0pp (9/39) · p-16.1pp cap80.6 net-463/med-12.5 | ▼i-2.7pp (33/170) · p+3.9pp cap33.0 net+618/med+1.8 | ·i+0.3pp (7/26) · p+10.3pp cap46.7 net-119/med-6.0 |
| S0-H11 | keep-watching | ·i-1.1pp (15/74) · p-2.0pp cap63.5 net-452/med-6.0 | (°▼i-21.1pp (0/14) · p-5.0pp cap73.1 net-472/med-58.8) | ·i-1.6pp (84/410) · p+1.7pp cap39.8 net-256/med-1.6 | ▲i+2.9pp (62/210) · p-6.2pp cap55.3 net-151/med-1.4 |
| S1-H11 | keep-watching | ·i-0.1pp (64/301) · p+6.6pp cap82.3 net+1221/med+5.2 | ▲i+8.4pp (33/112) · p+0.4pp cap84.4 net+267/med+1.2 | ▼i-2.0pp (44/219) · p+3.3pp cap39.9 net-933/med-0.8 | ▼i-7.1pp (15/77) · p+13.4pp cap46.2 net-385/med-7.0 |
| S0-H12 | keep-watching | — | — | — | — |
| S0-H13 | keep-watching | (°▼i-4.7pp (1/6) · p+59.7pp cap74.2 net+397/med+58.7) | (°▼i-21.1pp (0/2) · p+73.6pp cap116.8 net+181/med+90.7) | (°▼i-13.0pp (1/11) · p+4.1pp cap38.6 net+18/med+0.9) | (°▼i-9.9pp (1/6) · p-24.3pp cap— net-80/med-10.8) |
| S0-H14 | keep-watching | ·i-1.0pp (23/113) · p+3.8pp cap50.3 net+312/med+0.5 | ▼i-2.6pp (5/27) · p-11.6pp cap80.6 net-256/med-4.2 | ·i-1.6pp (35/171) · p+5.5pp cap28.8 net-388/med-0.1 | ▲i+4.0pp (11/36) · p+6.3pp cap59.7 net-120/med-14.2 |
| S0-H15 | keep-watching | — | — | — | — |
| S0-H16 | keep-watching | (°▼i-21.4pp (0/10) · p-3.6pp cap126.3 net+8/med-16.3) | — | (°▼i-13.0pp (1/11) · p+4.1pp cap69.9 net-11/med-15.9) | — |
| S0-H17 | rows | ▲i+9.0pp (7/23) · p+6.8pp cap90.2 net+36/med+0.7 | (°▼i-21.1pp (0/3) · p+40.3pp cap96.2 net+198/med+78.9) | ▲i+3.3pp (16/63) · p+7.0pp cap39.5 net+49/med-1.2 | (°▲i+19.6pp (6/13) · p+6.5pp cap51.8 net-101/med-15.7) |
| S0-H18 | rows | (°▼i-8.1pp (2/15) · p-10.3pp cap102.0 net-232/med-14.3) | (°▼i-21.1pp (0/3) · p+6.9pp cap135.4 net-19/med-38.6) | ▼i-5.4pp (12/72) · p+6.0pp cap41.8 net+88/med+0.9 | ▼i-3.9pp (10/44) · p-6.1pp cap54.1 net+39/med+3.2 |
| S0-H19 | rows | ▼i-3.0pp (27/147) · p+7.0pp cap74.2 net+179/med+3.6 | (°·i+1.1pp (2/9) · p-26.4pp cap— net-51/med-14.3) | ·i+0.8pp (38/166) · p-6.3pp cap38.7 net-39/med-1.0 | ▼i-9.2pp (4/23) · p+1.8pp cap61.0 net+52/med-2.6 |
| S0-H20 | rows | ▼i-14.2pp (0/35) · p+2.6pp cap57.7 [cls 34.5%/14.2%i] net-450/med-4.3 | (°▼i-9.9pp (0/19) · p+6.9pp cap61.4 [cls 35.2%/9.9%i] net+20/med+11.4) | ▼i-8.8pp (5/76) · p+6.1pp cap41.1 [cls 38.6%/15.4%i] net-68/med+0.4 | ▼i-9.7pp (2/33) · p+9.0pp cap48.5 [cls 39.5%/15.8%i] net+72/med-1.3 |
| **union coverage** | | 46.4% (52/112) | 33.3% (9/27) | 86.3% (101/117) | 91.2% (31/34) |

Not graded:  — see register entries.

## Hypothesis Cards (page 2)

### H1 — 2 signals
*A climactic bar — extreme volume on a wide spread late in an extended move — marks exhaustion, and price then reverses against the climax direction.*
Grading: directional. Latest review: keep-watching (recommendation).

- Question **Q1-H1**: see the register entry (status there is authoritative).
**S0-H1** — session × window grid (cells as in the matrix):

| session | backtest | forward |
|---|---|---|
| whole | ▲i+5.1pp (13/49) · p+9.1pp cap90.7 net-83/med+0.7 | ▲i+3.4pp (25/98) · p+9.5pp cap37.8 net+238/med-0.2 |
| london | (°▼i-21.1pp (0/5) · p+33.6pp cap89.9 net+198/med+39.9) | ▲i+3.8pp (7/23) · p+23.5pp cap50.3 net+23/med-5.5 |
| overlap | — | (°▲i+18.3pp (1/3) · p+5.5pp cap51.7 net+44/med+28.7) |
| ny_only | (°▼i-19.1pp (0/10) · p+18.8pp cap83.5 net-289/med-3.9) | (°▼i-10.9pp (1/17) · p+6.6pp cap34.1 net+77/med+11.5) |
| dead | (°▲i+3.2pp (2/7) · p+40.8pp cap89.2 net+93/med+34.1) | (°▲i+10.8pp (7/19) · p+4.9pp cap36.0 net-13/med-0.2) |
| asia | ▲i+16.5pp (11/27) · p-9.8pp cap95.6 net-85/med-12.0 | ▲i+2.6pp (9/36) · p+1.9pp cap26.1 net+107/med-0.2 |

- backtest payoff: right +1327 / wrong -1411 / net -83 pts; median per fire +0.70 (n=49)
- backtest best call: 2026-07-29 03:13 +188.0pts remaining (episode 262.8pts, major)
- backtest worst false alarm: 2026-07-29 19:11 -164.0pts adverse
- forward payoff: right +1031 / wrong -793 / net +238 pts; median per fire -0.20 (n=98)
- forward best call: 2026-08-20 04:29 +162.0pts remaining (episode 176.7pts, major)
- forward worst false alarm: 2026-08-20 11:25 -69.6pts adverse
- earliness (backtest): median 100.9 pts of move remaining at fire (n=9)

**S1-H1** — session × window grid (cells as in the matrix):

| session | backtest | forward |
|---|---|---|
| whole | (°▲i+11.9pp (1/3) · p-23.6pp cap— net-72/med-34.2) | (°▲i+2.9pp (1/4) · p+1.8pp cap35.8 net-20/med-14.2) |
| london | (°▼i-21.1pp (0/1) · p-26.4pp cap— net-54/med-53.5) | (°▼i-26.6pp (0/1) · p-24.3pp cap— net-23/med-22.6) |
| overlap | — | — |
| ny_only | — | (°▼i-16.8pp (0/1) · p-5.2pp cap— net-7/med-7.4) |
| dead | — | (°▼i-26.0pp (0/1) · p+78.6pp cap35.8 net+32/med+31.5) |
| asia | (°▲i+25.8pp (1/2) · p-32.0pp cap— net-19/med-9.3) | (°▲i+77.6pp (1/1) · p-34.2pp cap— net-21/med-21.0) |

- backtest payoff: right +16 / wrong -88 / net -72 pts; median per fire -34.20 (n=3)
- backtest best call: 2026-07-30 05:22 +120.0pts remaining (episode 162.9pts, major)
- backtest worst false alarm: 2026-07-28 10:36 -60.8pts adverse
- forward payoff: right +32 / wrong -51 / net -20 pts; median per fire -14.20 (n=4)
- forward best call: 2026-08-20 04:29 +162.0pts remaining (episode 176.7pts, major)
- forward worst false alarm: 2026-08-25 09:35 -25.4pts adverse
- earliness (backtest): median 120.0 pts of move remaining at fire (n=1)

### H2 — 2 signals
*A failed probe beyond a prior extreme — an upthrust above or spring below that closes back inside — reverses against the probe.*
Grading: directional. Latest review: promote-candidate (recommendation).

**S0-H2** — session × window grid (cells as in the matrix):

| session | backtest | forward |
|---|---|---|
| whole | ▼i-8.6pp (30/234) · p+1.2pp cap77.4 net-661/med-5.2 | ·i-1.6pp (74/361) · p+0.6pp cap35.5 net-34/med+0.5 |
| london | (°▼i-7.8pp (2/15) · p-13.1pp cap86.6 net+93/med+9.8) | ▲i+4.9pp (17/54) · p-9.5pp cap64.1 net-273/med-10.5 |
| overlap | (°▼i-13.3pp (0/11) · p-14.8pp cap122.7 net-195/med-38.7) | ▼i-5.5pp (2/21) · p-4.0pp cap94.5 net+128/med-3.4 |
| ny_only | ▼i-9.3pp (6/61) · p+13.4pp cap77.0 net-1116/med-16.7 | ▼i-4.0pp (11/86) · p-0.5pp cap41.0 net+9/med+0.2 |
| dead | ▼i-10.0pp (8/52) · p+6.8pp cap90.8 net+604/med+2.2 | ▼i-6.3pp (14/71) · p+16.6pp cap35.4 net+156/med+0.8 |
| asia | ▼i-9.5pp (14/95) · p-2.5pp cap80.0 net-47/med-10.6 | ·i+0.9pp (30/129) · p-1.6pp cap29.3 net-55/med+2.3 |

- backtest payoff: right +4896 / wrong -5557 / net -661 pts; median per fire -5.20 (n=234)
- backtest best call: 2026-07-27 03:23 +214.5pts remaining (episode 245.3pts, major)
- backtest worst false alarm: 2026-07-29 19:00 -192.8pts adverse
- forward payoff: right +3405 / wrong -3439 / net -34 pts; median per fire +0.50 (n=360)
- forward best call: 2026-08-25 03:19 +200.3pts remaining (episode 188.9pts, major)
- forward worst false alarm: 2026-08-31 06:44 -125.0pts adverse
- earliness (backtest): median 97.8 pts of move remaining at fire (n=19)

**S1-H2** — session × window grid (cells as in the matrix):

| session | backtest | forward |
|---|---|---|
| whole | ▼i-7.8pp (24/176) · p+2.5pp cap77.4 net-760/med-8.3 | ▲i+2.6pp (66/267) · p-0.7pp cap35.2 net+11/med+0.7 |
| london | (°▼i-5.7pp (2/13) · p-11.0pp cap86.6 net+136/med+14.0) | ▲i+7.5pp (14/41) · p-9.7pp cap72.5 net-202/med-11.4 |
| overlap | (°▼i-13.3pp (0/7) · p-9.6pp cap122.7 net-89/med-38.1) | (°·i-0.7pp (2/14) · p-6.4pp cap117.7 net+100/med-5.7) |
| ny_only | ▼i-10.2pp (4/45) · p+17.7pp cap77.0 net-1094/med-25.7 | ▼i-2.3pp (9/62) · p-2.0pp cap41.0 net+87/med+1.1 |
| dead | ▼i-10.4pp (6/40) · p+11.2pp cap74.9 net+699/med+7.8 | ·i+1.7pp (13/47) · p+16.9pp cap32.2 net+74/med-0.6 |
| asia | ▼i-7.3pp (12/71) · p-5.2pp cap83.8 net-413/med-26.4 | ▲i+4.8pp (28/103) · p-4.1pp cap29.6 net-48/med+2.3 |

- backtest payoff: right +3792 / wrong -4553 / net -760 pts; median per fire -8.35 (n=176)
- backtest best call: 2026-07-29 03:05 +193.7pts remaining (episode 262.8pts, major)
- backtest worst false alarm: 2026-07-29 19:00 -192.8pts adverse
- forward payoff: right +2593 / wrong -2582 / net +11 pts; median per fire +0.70 (n=267)
- forward best call: 2026-08-25 03:19 +200.3pts remaining (episode 188.9pts, major)
- forward worst false alarm: 2026-08-31 06:44 -125.0pts adverse
- earliness (backtest): median 97.8 pts of move remaining at fire (n=17)

### H3 — 1 signal
*Repeated absorption — high effort with no result — at a price level precedes a breakout through that level.*
Grading: directional. Latest review: keep-watching (recommendation).

**S0-H3** — session × window grid (cells as in the matrix):

| session | backtest | forward |
|---|---|---|
| whole | (°▲i+3.6pp (2/8) · p-11.1pp cap70.3 net-28/med+2.0) | ▲i+2.9pp (5/20) · p-3.2pp cap30.6 net-17/med-0.5 |
| london | — | (°▼i-26.6pp (0/1) · p-24.3pp cap— net+19/med+18.8) |
| overlap | — | — |
| ny_only | (°▲i+20.9pp (2/5) · p+8.8pp cap70.3 net+132/med+41.2) | (°·i-0.1pp (1/6) · p-5.2pp cap— net+5/med-0.1) |
| dead | — | — |
| asia | (°▼i-24.2pp (0/3) · p-32.0pp cap— net-160/med-56.5) | (°▲i+8.4pp (4/13) · p-3.4pp cap30.6 net-41/med-1.5) |

- backtest payoff: right +132 / wrong -160 / net -28 pts; median per fire +2.00 (n=8)
- backtest best call: 2026-07-27 18:10 +51.7pts remaining (episode 62.9pts)
- backtest worst false alarm: 2026-07-30 01:57 -65.7pts adverse
- forward payoff: right +162 / wrong -179 / net -17 pts; median per fire -0.50 (n=20)
- forward best call: 2026-08-27 04:28 +37.5pts remaining (episode 52.5pts, major)
- forward worst false alarm: 2026-08-26 01:44 -55.0pts adverse
- earliness (backtest): median 51.7 pts of move remaining at fire (n=1)

### H4 — 1 signal
*In an established trend, a quiet (low-volume) pullback resolves with trend resumption.*
Grading: directional. Latest review: keep-watching (recommendation).

**S0-H4** — session × window grid (cells as in the matrix):

| session | backtest | forward |
|---|---|---|
| whole | ▼i-9.6pp (4/34) · p+8.8pp cap50.2 net+72/med+10.0 | — |
| london | (°▲i+8.9pp (3/10) · p-16.4pp cap50.2 net-30/med-3.7) | — |
| overlap | (°▼i-13.3pp (0/6) · p+9.4pp cap59.3 net-4/med-8.4) | — |
| ny_only | (°▼i-19.1pp (0/6) · p+22.1pp cap25.4 net-9/med+10.8) | — |
| dead | (°·i-0.4pp (1/4) · p+8.7pp cap34.8 net-14/med+32.4) | — |
| asia | (°▼i-24.2pp (0/8) · p+30.5pp cap61.0 net+129/med+17.4) | — |

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
| whole | ▼i-11.4pp (1/36) · p+4.4pp cap59.3 [cls 34.5%/14.2%i] net-192/med-10.4 | ▲i+18.6pp (33/97) · p-3.5pp cap44.6 [cls 38.6%/15.4%i] net-1004/med-10.7 |
| london | (°▼i-4.3pp (1/18) · p-7.4pp cap78.7 [cls 35.2%/9.9%i] net-56/med-10.3) | ▲i+27.3pp (22/51) · p-10.1pp cap45.4 [cls 39.5%/15.8%i] net-873/med-21.9 |
| overlap | (°▼i-13.2pp (0/1) · p+71.3pp cap122.7 [cls 28.7%/13.2%i] net+108/med+108.3) | (°▲i+26.8pp (5/11) · p+5.9pp cap80.5 [cls 30.5%/18.7%i] net+168/med-8.0) |
| ny_only | — | — |
| dead | (°▼i-12.5pp (0/3) · p-25.0pp cap— [cls 25.0%/12.5%i] net+29/med+13.4) | — |
| asia | (°▼i-21.3pp (0/14) · p+20.4pp cap39.1 [cls 36.7%/21.3%i] net-274/med-21.8) | ▲i+2.2pp (6/35) · p+0.0pp cap35.8 [cls 42.9%/14.9%i] net-299/med-4.8 |

- backtest payoff: right +682 / wrong -874 / net -192 pts; median per fire -10.40 (n=36)
- backtest best call: 2026-07-28 12:35 +146.2pts remaining (episode 195.2pts, major)
- backtest worst false alarm: 2026-08-03 07:10 -108.0pts adverse
- forward payoff: right +982 / wrong -1986 / net -1004 pts; median per fire -10.70 (n=97)
- forward best call: 2026-08-26 12:31 +139.4pts remaining (episode 156.6pts, major)
- forward worst false alarm: 2026-08-18 07:07 -124.1pts adverse
- earliness (backtest): median 146.2 pts of move remaining at fire (n=1)

### H7 — 1 signal
*Quiet decline at a session extreme is disguised accumulation: effortless (low-volume) weakness reverses UP once selling fails to attract participation (mirror: quiet advance at a high reverses down).*
Grading: directional + either-direction (dual). Latest review: keep-watching (recommendation).

- Question **Q1-H7**: see the register entry (status there is authoritative).
**S0-H7** — session × window grid (cells as in the matrix):

| session | backtest | forward |
|---|---|---|
| whole | ·i-1.1pp (12/59) · p+12.0pp cap97.8 net+761/med+4.2 | ▲i+7.3pp (20/68) · p-5.6pp cap56.5 net-182/med+0.1 |
| london | ▼i-11.1pp (2/20) · p+23.6pp cap86.9 net+719/med+33.0 | ▲i+12.1pp (12/31) · p-14.6pp cap88.2 net-191/med-0.3 |
| overlap | (°▼i-6.6pp (1/15) · p+22.8pp cap91.3 net+56/med-29.0) | (°▼i-15.0pp (0/7) · p-13.5pp cap76.3 net-101/med-28.6) |
| ny_only | (°▼i-2.4pp (1/6) · p+5.5pp cap101.1 net+59/med+7.7) | (°▼i-8.5pp (1/12) · p+3.1pp cap56.6 net-11/med-0.7) |
| dead | (°▲i+24.6pp (2/4) · p+8.7pp cap128.8 net-15/med-28.8) | (°▲i+7.3pp (1/3) · p+11.9pp cap51.5 net+29/med-7.5) |
| asia | (°▲i+18.7pp (6/14) · p-17.7pp cap99.9 net-58/med-10.2) | (°▲i+17.6pp (6/15) · p+5.8pp cap37.8 net+92/med+0.9) |

- backtest payoff: right +1756 / wrong -995 / net +761 pts; median per fire +4.20 (n=59)
- backtest best call: 2026-07-27 03:04 +247.0pts remaining (episode 245.3pts, major)
- backtest worst false alarm: 2026-07-27 13:57 -91.8pts adverse
- forward payoff: right +834 / wrong -1016 / net -182 pts; median per fire +0.05 (n=68)
- forward best call: 2026-08-27 11:41 +136.3pts remaining (episode 158.4pts, major)
- forward worst false alarm: 2026-08-21 07:20 -80.9pts adverse
- earliness (backtest): median 74.6 pts of move remaining at fire (n=11)

**S0-H7 (either-dir)** — session × window grid (cells as in the matrix):

| session | backtest | forward |
|---|---|---|
| whole | ▼i-6.1pp (20/59) · p+19.3pp cap50.2 | ▼i-4.6pp (25/68) · p-0.5pp cap14.6 |
| london | ▼i-10.5pp (6/20) · p+23.7pp cap57.4 | ·i-0.4pp (15/31) · p-4.0pp cap8.5 |
| overlap | (°▼i-19.9pp (1/15) · p+33.1pp cap65.0) | (°▼i-29.8pp (0/7) · p+2.4pp cap8.1) |
| ny_only | (°·i-0.4pp (2/6) · p+11.2pp cap52.5) | (°▼i-16.3pp (2/12) · p-2.1pp cap56.6) |
| dead | (°▲i+3.7pp (2/4) · p+43.2pp cap-2.7) | (°▲i+19.5pp (2/3) · p-7.2pp cap51.5) |
| asia | (°▲i+18.9pp (9/14) · p-16.3pp cap7.9) | (°·i-1.8pp (6/15) · p+5.8pp cap24.1) |

- backtest payoff: n/a by construction (either-direction)
- backtest best call: 2026-07-27 03:04 +247.0pts remaining (episode 245.3pts, major)
- backtest worst false alarm: 2026-07-29 11:19 -63.7pts adverse
- forward payoff: n/a by construction (either-direction)
- forward best call: 2026-08-27 11:41 +136.3pts remaining (episode 158.4pts, major)
- forward worst false alarm: 2026-08-19 16:29 -39.5pts adverse
- earliness (backtest): median 74.6 pts of move remaining at fire (n=17)

### H8 — 1 signal
*Reversal-signature bar anatomy (upthrust/spring) predicts imminent range expansion irrespective of direction.*
Grading: either-direction. Latest review: keep-watching (recommendation).

**S0-H8** — session × window grid (cells as in the matrix):

| session | backtest | forward |
|---|---|---|
| whole | ▼i-9.2pp (72/234) · p+8.3pp cap36.4 | ·i+1.5pp (155/361) · p-4.0pp cap23.0 |
| london | (°▼i-20.5pp (3/15) · p-31.3pp cap68.2) | ·i-0.7pp (26/54) · p-7.0pp cap14.4 |
| overlap | (°▼i-17.5pp (1/11) · p+16.7pp cap37.2) | ▼i-6.0pp (5/21) · p+2.4pp cap17.1 |
| ny_only | ▼i-7.5pp (16/61) · p+33.6pp cap32.1 | ▼i-5.1pp (24/86) · p-5.7pp cap41.0 |
| dead | ▼i-13.6pp (17/52) · p+0.9pp cap53.2 | ▲i+9.1pp (40/71) · p+17.2pp cap22.2 |
| asia | ▼i-8.6pp (35/95) · p+8.2pp cap29.9 | ▲i+4.7pp (60/129) · p-12.1pp cap23.0 |

- backtest payoff: n/a by construction (either-direction)
- backtest best call: 2026-07-27 03:23 +214.5pts remaining (episode 245.3pts, major)
- backtest worst false alarm: 2026-07-27 16:30 -74.5pts adverse
- forward payoff: n/a by construction (either-direction)
- forward best call: 2026-08-25 03:18 +200.8pts remaining (episode 188.9pts, major)
- forward worst false alarm: 2026-08-18 09:32 -59.6pts adverse
- earliness (backtest): median 80.1 pts of move remaining at fire (n=27)

### H9 — 2 signals
*Persistent lower-TF directional pressure that recruits expanding participation at the parent timeframe precedes continuation beyond what the parent label alone predicts; pressure without participation expansion does not.*
Grading: directional. Latest review: keep-watching (recommendation).

- Question **Q2-H9**: see the register entry (status there is authoritative).
**S0-H9** — session × window grid (cells as in the matrix):

| session | backtest | forward |
|---|---|---|
| whole | ▲i+3.6pp (13/52) · p-8.2pp cap55.5 net-426/med-4.1 | ▼i-6.0pp (5/31) · p-10.3pp cap40.6 net-243/med-7.7 |
| london | (°▼i-21.1pp (0/3) · p-26.4pp cap— net+17/med+22.6) | (°▲i+6.7pp (1/3) · p-24.3pp cap— net-164/med-43.6) |
| overlap | (°▼i-13.3pp (0/2) · p-23.9pp cap— net+112/med+55.8) | (°▼i-15.0pp (0/1) · p-27.8pp cap— net-18/med-17.7) |
| ny_only | ▲i+12.7pp (7/22) · p-6.7pp cap32.0 net-517/med-19.3 | (°▲i+3.2pp (2/10) · p+4.8pp cap28.0 net-49/med-7.5) |
| dead | (°·i-0.4pp (3/12) · p+17.0pp cap101.1 net+200/med+3.0) | (°▼i-9.3pp (1/6) · p+28.6pp cap40.6 net+130/med+40.6) |
| asia | (°·i-1.1pp (3/13) · p-8.9pp cap49.0 net-238/med-8.5) | (°▼i-13.3pp (1/11) · p-34.2pp cap— net-141/med-13.8) |

- backtest payoff: right +725 / wrong -1151 / net -426 pts; median per fire -4.10 (n=51)
- backtest best call: 2026-07-31 05:00 +184.4pts remaining (episode 184.2pts, major)
- backtest worst false alarm: 2026-07-29 18:45 -160.1pts adverse
- forward payoff: right +184 / wrong -427 / net -243 pts; median per fire -7.70 (n=29)
- forward best call: 2026-08-25 03:30 +191.3pts remaining (episode 188.9pts, major)
- forward worst false alarm: 2026-08-18 07:00 -118.4pts adverse
- earliness (backtest): median 70.2 pts of move remaining at fire (n=7)

**S1-H9** — session × window grid (cells as in the matrix):

| session | backtest | forward |
|---|---|---|
| whole | (°▼i-21.4pp (0/8) · p+26.4pp cap101.1 net-53/med+13.1) | ▼i-7.1pp (3/20) · p-3.2pp cap40.6 net-101/med-7.7 |
| london | — | (°▲i+73.4pp (1/1) · p-24.3pp cap— net-114/med-114.2) |
| overlap | (°▼i-13.3pp (0/1) · p-23.9pp cap— net+56/med+55.8) | — |
| ny_only | (°▼i-19.1pp (0/2) · p-11.2pp cap— net-320/med-160.1) | (°▼i-16.8pp (0/4) · p+19.8pp cap28.0 net+5/med-7.5) |
| dead | (°▼i-25.4pp (0/5) · p+63.7pp cap101.1 net+211/med+19.4) | (°▼i-9.3pp (1/6) · p+28.6pp cap40.6 net+130/med+40.6) |
| asia | — | (°▼i-11.3pp (1/9) · p-34.2pp cap— net-122/med-13.8) |

- backtest payoff: right +294 / wrong -348 / net -53 pts; median per fire +13.05 (n=8)
- backtest worst false alarm: 2026-07-29 18:45 -160.1pts adverse
- forward payoff: right +163 / wrong -264 / net -101 pts; median per fire -7.70 (n=18)
- forward best call: 2026-08-25 03:30 +191.3pts remaining (episode 188.9pts, major)
- forward worst false alarm: 2026-08-18 07:00 -118.4pts adverse

### H10 — 1 signal
*In an established 1-minute trend, no-demand/no-supply prints in the trend's direction signal continuation.*
Grading: directional. Latest review: deprioritize (recommendation).

**S0-H10** — session × window grid (cells as in the matrix):

| session | backtest | forward |
|---|---|---|
| whole | ▲i+4.5pp (38/147) · p-4.6pp cap50.5 net-391/med+3.2 | ▼i-2.7pp (33/170) · p+3.9pp cap33.0 net+618/med+1.8 |
| london | ▲i+2.0pp (9/39) · p-16.1pp cap80.6 net-463/med-12.5 | ·i+0.3pp (7/26) · p+10.3pp cap46.7 net-119/med-6.0 |
| overlap | (°▼i-13.3pp (0/9) · p-1.7pp cap59.5 net-114/med-21.0) | (°·i+0.4pp (2/13) · p+3.0pp cap90.4 net+386/med+13.1) |
| ny_only | ·i-1.5pp (6/34) · p+3.5pp cap46.4 net+237/med+4.4 | ·i-1.4pp (6/39) · p+7.6pp cap21.8 net-110/med-1.6 |
| dead | (°▲i+3.2pp (4/14) · p-16.3pp cap— net-275/med-13.8) | (°▼i-7.2pp (3/16) · p-15.2pp cap25.7 net-65/med+1.2) |
| asia | ▲i+13.1pp (19/51) · p+1.3pp cap48.4 net+224/med+6.3 | ▼i-2.7pp (15/76) · p+1.3pp cap30.9 net+526/med+2.1 |

- backtest payoff: right +1730 / wrong -2121 / net -391 pts; median per fire +3.20 (n=147)
- backtest best call: 2026-07-27 03:28 +219.3pts remaining (episode 245.3pts, major)
- backtest worst false alarm: 2026-07-26 23:29 -102.8pts adverse
- forward payoff: right +2080 / wrong -1462 / net +618 pts; median per fire +1.80 (n=169)
- forward best call: 2026-08-25 03:44 +196.5pts remaining (episode 188.9pts, major)
- forward worst false alarm: 2026-08-26 11:10 -85.5pts adverse
- earliness (backtest): median 83.8 pts of move remaining at fire (n=10)

### H11 — 2 signals
*Price entering a low-volume price zone traverses it faster than baseline; entering a high-volume node it stalls or reverses at above-baseline rates.*
Grading: directional. Latest review: keep-watching (recommendation).

- Question **Q1-H11**: see the register entry (status there is authoritative).
- Question **Q2-H11**: see the register entry (status there is authoritative).
**S0-H11** — session × window grid (cells as in the matrix):

| session | backtest | forward |
|---|---|---|
| whole | ·i-1.1pp (15/74) · p-2.0pp cap63.5 net-452/med-6.0 | ·i-1.6pp (84/410) · p+1.7pp cap39.8 net-256/med-1.6 |
| london | (°▼i-21.1pp (0/14) · p-5.0pp cap73.1 net-472/med-58.8) | ▲i+2.9pp (62/210) · p-6.2pp cap55.3 net-151/med-1.4 |
| overlap | (°·i-0.8pp (2/16) · p-17.7pp cap68.3 net-166/med-13.2) | (°▼i-15.0pp (0/17) · p-16.0pp cap73.6 net+169/med+1.0) |
| ny_only | (°▼i-19.1pp (0/4) · p-11.2pp cap— net-18/med-18.5) | ·i-0.1pp (4/24) · p-5.2pp cap— net-68/med-1.2 |
| dead | (°▲i+17.5pp (3/7) · p-2.0pp cap52.6 net+1/med+4.1) | ▼i-11.0pp (3/20) · p+8.6pp cap21.8 net-8/med-0.1 |
| asia | ▲i+6.1pp (10/33) · p+1.3pp cap58.7 net+203/med-1.1 | ▼i-11.6pp (15/139) · p+6.1pp cap32.9 net-198/med-3.0 |

- backtest payoff: right +1359 / wrong -1811 / net -452 pts; median per fire -5.95 (n=74)
- backtest best call: 2026-07-29 04:03 +262.2pts remaining (episode 262.8pts, major)
- backtest worst false alarm: 2026-07-31 07:03 -171.6pts adverse
- forward payoff: right +4569 / wrong -4824 / net -256 pts; median per fire -1.65 (n=410)
- forward best call: 2026-08-26 10:01 +138.2pts remaining (episode 167.4pts, major)
- forward worst false alarm: 2026-08-27 13:29 -114.5pts adverse
- earliness (backtest): median 104.9 pts of move remaining at fire (n=8)

**S1-H11** — session × window grid (cells as in the matrix):

| session | backtest | forward |
|---|---|---|
| whole | ·i-0.1pp (64/301) · p+6.6pp cap82.3 net+1221/med+5.2 | ▼i-2.0pp (44/219) · p+3.3pp cap39.9 net-933/med-0.8 |
| london | ▲i+8.4pp (33/112) · p+0.4pp cap84.4 net+267/med+1.2 | ▼i-7.1pp (15/77) · p+13.4pp cap46.2 net-385/med-7.0 |
| overlap | ▼i-3.3pp (2/20) · p-13.9pp cap84.7 net+3/med+13.2 | ▼i-3.2pp (6/51) · p-4.3pp cap46.9 net-123/med-2.8 |
| ny_only | ▼i-10.6pp (4/47) · p+10.1pp cap83.3 net+89/med+1.0 | ▲i+9.5pp (10/38) · p-5.2pp cap— net+149/med+2.9 |
| dead | ▲i+9.9pp (12/34) · p+7.2pp cap86.7 net+169/med+5.3 | ▼i-16.5pp (2/21) · p-2.4pp cap25.5 net+81/med+6.7 |
| asia | ▼i-9.4pp (13/88) · p+14.6pp cap82.1 net+693/med+16.2 | ▲i+12.0pp (11/32) · p+6.4pp cap25.0 net-655/med-8.5 |

- backtest payoff: right +7407 / wrong -6186 / net +1221 pts; median per fire +5.20 (n=301)
- backtest best call: 2026-07-30 00:35 +150.2pts remaining (episode 237.6pts, major)
- backtest worst false alarm: 2026-07-29 19:32 -168.0pts adverse
- forward payoff: right +2509 / wrong -3442 / net -933 pts; median per fire -0.80 (n=219)
- forward best call: 2026-08-31 10:57 +142.7pts remaining (episode 169.9pts, major)
- forward worst false alarm: 2026-08-20 06:33 -145.0pts adverse
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
| whole | (°▼i-4.7pp (1/6) · p+59.7pp cap74.2 net+397/med+58.7) | (°▼i-13.0pp (1/11) · p+4.1pp cap38.6 net+18/med+0.9) |
| london | (°▼i-21.1pp (0/2) · p+73.6pp cap116.8 net+181/med+90.7) | (°▼i-9.9pp (1/6) · p-24.3pp cap— net-80/med-10.8) |
| overlap | — | — |
| ny_only | — | (°▼i-16.8pp (0/2) · p-5.2pp cap— net+3/med+1.4) |
| dead | (°▼i-25.4pp (0/1) · p+83.7pp cap74.2 net+51/med+51.0) | (°▼i-26.0pp (0/1) · p+78.6pp cap29.2 net+29/med+29.2) |
| asia | (°▲i+9.1pp (1/3) · p+34.7pp cap78.8 net+164/med+56.1) | (°▼i-22.4pp (0/2) · p+65.8pp cap59.1 net+66/med+32.8) |

- backtest payoff: right +397 / wrong +0 / net +397 pts; median per fire +58.70 (n=6)
- backtest best call: 2026-07-28 02:15 +115.9pts remaining (episode 109.7pts, major)
- backtest worst false alarm: 2026-07-28 02:15 -2.8pts adverse
- forward payoff: right +116 / wrong -98 / net +18 pts; median per fire +0.90 (n=11)
- forward best call: 2026-08-21 09:44 +113.7pts remaining (episode 144.6pts, major)
- forward worst false alarm: 2026-08-26 09:25 -50.0pts adverse
- earliness (backtest): median 115.9 pts of move remaining at fire (n=1)

### H14 — 1 signal
*Counter-trend No Demand / No Supply prints in an established trend mark absorption and precede trend continuation.*
Grading: directional. Latest review: keep-watching (recommendation).

**S0-H14** — session × window grid (cells as in the matrix):

| session | backtest | forward |
|---|---|---|
| whole | ·i-1.0pp (23/113) · p+3.8pp cap50.3 net+312/med+0.5 | ·i-1.6pp (35/171) · p+5.5pp cap28.8 net-388/med-0.1 |
| london | ▼i-2.6pp (5/27) · p-11.6pp cap80.6 net-256/med-4.2 | ▲i+4.0pp (11/36) · p+6.3pp cap59.7 net-120/med-14.2 |
| overlap | (°▼i-13.3pp (0/11) · p-23.9pp cap— net-138/med-20.3) | (°▲i+26.7pp (5/12) · p+5.5pp cap57.0 net+99/med+0.6) |
| ny_only | ▼i-10.4pp (2/23) · p+27.9pp cap43.2 net+392/med+21.1 | ▼i-3.5pp (4/30) · p+14.8pp cap26.2 net+156/med+4.6 |
| dead | (°▲i+19.0pp (4/9) · p-16.3pp cap— net-178/med-20.1) | ▼i-11.2pp (4/27) · p-10.3pp cap26.4 net-402/med-2.2 |
| asia | ▲i+3.7pp (12/43) · p+9.9pp cap59.0 net+492/med+8.2 | ▼i-5.7pp (11/66) · p+3.7pp cap24.0 net-122/med-0.4 |

- backtest payoff: right +1733 / wrong -1421 / net +312 pts; median per fire +0.50 (n=113)
- backtest best call: 2026-07-31 04:56 +164.7pts remaining (episode 169.2pts, major)
- backtest worst false alarm: 2026-08-03 06:28 -123.0pts adverse
- forward payoff: right +1728 / wrong -2116 / net -388 pts; median per fire -0.10 (n=171)
- forward best call: 2026-08-24 10:27 +121.4pts remaining (episode 126.9pts, major)
- forward worst false alarm: 2026-08-26 06:48 -90.4pts adverse
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
| whole | (°▼i-21.4pp (0/10) · p-3.6pp cap126.3 net+8/med-16.3) | (°▼i-13.0pp (1/11) · p+4.1pp cap69.9 net-11/med-15.9) |
| london | — | — |
| overlap | (°▼i-13.3pp (0/10) · p-3.9pp cap126.3 net+8/med-16.3) | (°▼i-5.9pp (1/11) · p-0.5pp cap69.9 net-11/med-15.9) |
| ny_only | — | — |
| dead | — | — |
| asia | — | — |

- backtest payoff: right +262 / wrong -254 / net +8 pts; median per fire -16.30 (n=10)
- backtest worst false alarm: 2026-07-27 15:00 -114.5pts adverse
- forward payoff: right +220 / wrong -231 / net -11 pts; median per fire -15.90 (n=11)
- forward best call: 2026-08-20 15:00 +43.7pts remaining (episode 52.1pts)
- forward worst false alarm: 2026-08-28 15:00 -60.4pts adverse

### H17 — 1 signal
*A climax reversal signal followed by absorption within five bars — effort meeting a quiet counter-party — marks a genuine exhaustion turn: the two-chapter story (exhaustion needs absorption to become reversal).*
Grading: directional. Latest review: rows (recommendation).

**S0-H17** — session × window grid (cells as in the matrix):

| session | backtest | forward |
|---|---|---|
| whole | ▲i+9.0pp (7/23) · p+6.8pp cap90.2 net+36/med+0.7 | ▲i+3.3pp (16/63) · p+7.0pp cap39.5 net+49/med-1.2 |
| london | (°▼i-21.1pp (0/3) · p+40.3pp cap96.2 net+198/med+78.9) | (°▲i+19.6pp (6/13) · p+6.5pp cap51.8 net-101/med-15.7) |
| overlap | — | (°▼i-15.0pp (0/2) · p+22.2pp cap48.1 net+64/med+31.9) |
| ny_only | (°▼i-19.1pp (0/2) · p-11.2pp cap— net-67/med-33.6) | (°▼i-7.7pp (1/11) · p+13.0pp cap35.6 net+89/med+14.6) |
| dead | (°▲i+14.6pp (2/5) · p+23.7pp cap109.2 net-58/med+0.7) | (°▲i+10.4pp (4/11) · p+5.9pp cap41.4 net-43/med-6.2) |
| asia | (°▲i+14.3pp (5/13) · p-8.9pp cap75.2 net-37/med-9.0) | ▼i-3.2pp (5/26) · p+0.4pp cap25.1 net+40/med+0.1 |

- backtest payoff: right +670 / wrong -634 / net +36 pts; median per fire +0.70 (n=23)
- backtest best call: 2026-07-30 05:24 +122.9pts remaining (episode 162.9pts, major)
- backtest worst false alarm: 2026-07-28 23:06 -138.5pts adverse
- forward payoff: right +630 / wrong -581 / net +49 pts; median per fire -1.20 (n=63)
- forward best call: 2026-08-20 04:30 +161.3pts remaining (episode 176.7pts, major)
- forward worst false alarm: 2026-08-20 11:26 -70.6pts adverse
- earliness (backtest): median 101.9 pts of move remaining at fire (n=5)

### H18 — 1 signal
*A gap-traversal signal followed by a same-direction effortless print within five bars — travel meeting no opposition — continues: the map says vacuum, the tape confirms no resistance.*
Grading: directional. Latest review: rows (recommendation).

**S0-H18** — session × window grid (cells as in the matrix):

| session | backtest | forward |
|---|---|---|
| whole | (°▼i-8.1pp (2/15) · p-10.3pp cap102.0 net-232/med-14.3) | ▼i-5.4pp (12/72) · p+6.0pp cap41.8 net+88/med+0.9 |
| london | (°▼i-21.1pp (0/3) · p+6.9pp cap135.4 net-19/med-38.6) | ▼i-3.9pp (10/44) · p-6.1pp cap54.1 net+39/med+3.2 |
| overlap | (°▼i-13.3pp (0/6) · p-23.9pp cap— net-52/med-6.5) | (°▼i-15.0pp (0/3) · p+5.5pp cap88.8 net+84/med+1.0) |
| ny_only | — | (°▼i-16.8pp (0/2) · p-5.2pp cap— net-40/med-20.1) |
| dead | (°▲i+74.6pp (1/1) · p-16.3pp cap— net-14/med-14.3) | (°▼i-26.0pp (0/2) · p-21.4pp cap— net-2/med-0.8) |
| asia | (°▼i-4.2pp (1/5) · p-12.0pp cap68.5 net-146/med-6.4) | ▼i-12.9pp (2/21) · p+22.9pp cap33.0 net+7/med+0.8 |

- backtest payoff: right +233 / wrong -464 / net -232 pts; median per fire -14.30 (n=15)
- backtest best call: 2026-08-03 05:26 +128.6pts remaining (episode 143.1pts, major)
- backtest worst false alarm: 2026-07-31 06:36 -175.9pts adverse
- forward payoff: right +945 / wrong -857 / net +88 pts; median per fire +0.90 (n=72)
- forward best call: 2026-08-21 09:44 +113.7pts remaining (episode 144.6pts, major)
- forward worst false alarm: 2026-08-18 07:07 -124.1pts adverse
- earliness (backtest): median 70.0 pts of move remaining at fire (n=2)

### H19 — 1 signal
*A probe-failure reversal signal followed by continued wide-loud effort in the anchor bar's own close direction within five bars is NOT the start of the claimed reversal — a SUPPRESSION/FADE configuration, and it says so.*
Grading: directional. Latest review: rows (recommendation).

- Question **Q1-H19**: see the register entry (status there is authoritative).
**S0-H19** — session × window grid (cells as in the matrix):

| session | backtest | forward |
|---|---|---|
| whole | ▼i-3.0pp (27/147) · p+7.0pp cap74.2 net+179/med+3.6 | ·i+0.8pp (38/166) · p-6.3pp cap38.7 net-39/med-1.0 |
| london | (°·i+1.1pp (2/9) · p-26.4pp cap— net-51/med-14.3) | ▼i-9.2pp (4/23) · p+1.8pp cap61.0 net+52/med-2.6 |
| overlap | (°·i+1.0pp (1/7) · p+47.5pp cap75.9 net+81/med+40.1) | (°▲i+5.0pp (1/5) · p-7.8pp cap50.7 net-30/med-8.4) |
| ny_only | ▼i-12.0pp (3/42) · p+36.4pp cap77.5 net+903/med+21.6 | ▼i-8.7pp (3/37) · p-2.5pp cap31.2 net+31/med+5.5 |
| dead | ▼i-2.7pp (10/44) · p-4.9pp cap58.4 net-463/med-4.3 | ▲i+11.2pp (16/43) · p-2.8pp cap35.6 net-95/med+0.2 |
| asia | ·i+0.2pp (11/45) · p+1.3pp cap64.2 net-291/med+10.6 | ·i+1.7pp (14/58) · p-13.5pp cap35.9 net+3/med-4.0 |

- backtest payoff: right +3647 / wrong -3468 / net +179 pts; median per fire +3.60 (n=147)
- backtest best call: 2026-07-30 00:50 +147.0pts remaining (episode 237.6pts, major)
- backtest worst false alarm: 2026-07-29 18:59 -189.5pts adverse
- forward payoff: right +1461 / wrong -1500 / net -39 pts; median per fire -1.00 (n=166)
- forward best call: 2026-08-20 04:29 +162.0pts remaining (episode 176.7pts, major)
- forward worst false alarm: 2026-08-28 14:12 -120.6pts adverse
- earliness (backtest): median 89.8 pts of move remaining at fire (n=15)

### H20 — 1 signal
*A wide-bar close-through of a session extreme (the same conditioned wide-bar class the retest anchor fires on; resolution = the close beyond the level, not a rejection back inside) initiates continuation in the break direction.*
Grading: directional. Latest review: rows (recommendation).

**S0-H20** — session × window grid (cells as in the matrix):

| session | backtest | forward |
|---|---|---|
| whole | ▼i-14.2pp (0/35) · p+2.6pp cap57.7 [cls 34.5%/14.2%i] net-450/med-4.3 | ▼i-8.8pp (5/76) · p+6.1pp cap41.1 [cls 38.6%/15.4%i] net-68/med+0.4 |
| london | (°▼i-9.9pp (0/19) · p+6.9pp cap61.4 [cls 35.2%/9.9%i] net+20/med+11.4) | ▼i-9.7pp (2/33) · p+9.0pp cap48.5 [cls 39.5%/15.8%i] net+72/med-1.3 |
| overlap | (°▼i-13.2pp (0/3) · p-28.7pp cap— [cls 28.7%/13.2%i] net-186/med-32.7) | (°▼i-18.7pp (0/14) · p-9.1pp cap57.7 [cls 30.5%/18.7%i] net-204/med-18.1) |
| ny_only | — | (°▲i+43.8pp (2/4) · p-4.5pp cap— [cls 4.5%/6.2%i] net+36/med+3.9) |
| dead | (°▼i-12.5pp (0/3) · p+8.3pp cap44.1 [cls 25.0%/12.5%i] net-286/med-97.1) | — |
| asia | (°▼i-21.3pp (0/10) · p+3.3pp cap71.0 [cls 36.7%/21.3%i] net+2/med+8.8) | ▼i-10.9pp (1/25) · p+17.1pp cap31.7 [cls 42.9%/14.9%i] net+28/med+5.8 |

- backtest payoff: right +504 / wrong -954 / net -450 pts; median per fire -4.30 (n=35)
- backtest worst false alarm: 2026-07-27 13:49 -141.5pts adverse
- forward payoff: right +1034 / wrong -1102 / net -68 pts; median per fire +0.40 (n=76)
- forward best call: 2026-08-18 05:31 +73.5pts remaining (episode 106.9pts, major)
- forward worst false alarm: 2026-08-18 08:06 -84.6pts adverse


---

# nas100 (nas100fut) — CANONICAL

Store span (1M, close ts): 2026-07-19 22:02:00+00:00 → 2026-08-31 18:48:00+00:00. Volume type: real futures volume (register 40 first-sync sanity; canonical verdict at this instrument's validation evening).

## Summary Matrix (page 1)

Engine `79c2cdd41` — OBSERVATIONAL signal scoreboard - move-detection, not trading; no fills exist here by construction; never validation (docs/hypothesis_lifecycle.md stage 4)

**Review labels are RECOMMENDATIONS — none actioned, review pending operator familiarity.** Cells: marker + precision LIFT vs that context's OWN chance rate, (hits/fires), payoff net/median points (directional rows; either-direction rows have no payoff by construction). ▲/▼ = beyond ±2pp of chance, · = within. (°…) = small-n (fires<20 or episodes<10): dimmed, excluded from any future label arithmetic. Read READING_GUIDE.md first; full detail in hypothesis_performance.json.

| H | label | backtest whole | backtest london | forward whole | forward london |
|---|---|---|---|---|---|
| *context* | | 113 ep; chance 22.1%dir/41.8%either | 41 ep; chance 30.9%dir/56.1%either | 121 ep; chance 23.3%dir/43.6%either | 39 ep; chance 31.6%dir/57.6%either |
| S0-H1 | keep-watching | ·i-0.9pp (7/34) · p+19.1pp cap182.2 net+122/med-15.7 | (°▲i+11.7pp (3/8) · p-18.4pp cap153.6 net-257/med-46.2) | ▲i+7.8pp (21/69) · p+14.4pp cap78.5 net+791/med+18.4 | ▲i+7.7pp (11/32) · p+5.9pp cap93.9 net+217/med+11.2 |
| S1-H1 | keep-watching | (°▲i+11.8pp (1/3) · p+44.6pp cap279.0 net+465/med+128.4) | — | (°▼i-22.6pp (0/2) · p+76.7pp cap90.8 net+170/med+85.0) | (°▼i-26.7pp (0/1) · p+68.4pp cap74.3 net+74/med+74.3) |
| S0-H2 | promote-candidate | ▼i-3.1pp (59/320) · p-2.1pp cap156.4 net-3528/med-1.4 | ·i+1.3pp (16/59) · p-5.5pp cap106.7 net-313/med-30.0 | ▼i-4.0pp (76/408) · p+8.1pp cap81.4 net+1812/med+3.5 | ▼i-2.3pp (30/123) · p+5.8pp cap84.6 net+458/med+5.7 |
| S1-H2 | promote-candidate | ▼i-2.6pp (42/222) · p-1.4pp cap142.3 net-1379/med-4.2 | ▲i+4.4pp (13/43) · p-3.0pp cap101.9 net-382/med-31.5 | ·i-0.6pp (64/291) · p+6.6pp cap82.8 net+1424/med+4.5 | ▲i+3.1pp (25/84) · p+2.9pp cap85.6 net+313/med+6.5 |
| S0-H3 | keep-watching | (°▼i-21.5pp (0/1) · p+77.9pp cap105.8 net+106/med+105.8) | (°▼i-25.8pp (0/1) · p+69.1pp cap105.8 net+106/med+105.8) | (°▼i-22.6pp (0/1) · p-23.3pp cap— net-1/med-1.1) | — |
| S0-H4 | keep-watching | — | — | (°▼i-22.6pp (0/10) · p+36.7pp cap38.4 net-18/med-7.4) | (°▼i-26.7pp (0/5) · p+8.4pp cap31.1 net+26/med+9.5) |
| S0-H5 | keep-watching | — | — | — | — |
| S0-H6 | keep-watching | ▲i+4.5pp (5/29) · p-8.3pp cap260.8 [cls 39.3%/12.7%i] net-232/med-11.8 | (°▲i+60.2pp (4/5) · p-38.7pp cap— [cls 38.7%/19.8%i] net-719/med-105.3) | ▲i+5.2pp (17/82) · p+6.3pp cap92.4 [cls 37.6%/15.5%i] net+1138/med+6.2 | ▲i+2.0pp (6/24) · p+22.6pp cap74.2 [cls 35.7%/23.0%i] net+723/med+28.0 |
| S0-H7 | keep-watching | ▼i-5.5pp (8/50) · p-0.1pp cap169.0 net+77/med-7.8 | (°·i-0.8pp (4/16) · p-5.9pp cap123.6 net-167/med-6.6) | ·i-1.9pp (17/82) · p+3.5pp cap80.7 net+96/med+8.9 | ▲i+5.1pp (7/22) · p+9.3pp cap82.9 net+404/med+10.0 |
| S0-H7 (either-dir) | keep-watching | ▼i-10.4pp (15/50) · p+4.2pp cap46.5 | (°▲i+2.2pp (8/16) · p+0.1pp cap23.3) | ▼i-9.1pp (27/82) · p+13.7pp cap44.5 | ·i-0.5pp (11/22) · p+15.1pp cap55.0 |
| S0-H8 | keep-watching | ▼i-3.8pp (117/320) · p+2.3pp cap65.1 | ▼i-7.1pp (24/59) · p+4.9pp cap53.7 | ·i-0.3pp (170/408) · p+6.4pp cap61.6 | ▲i+4.0pp (67/123) · p+4.2pp cap63.1 |
| S0-H9 | keep-watching | ▲i+2.4pp (21/88) · p+0.6pp cap129.2 net+593/med-4.3 | (°▼i-25.8pp (0/9) · p+2.4pp cap76.3 net+410/med+11.6) | ▼i-5.0pp (19/108) · p-7.6pp cap58.2 net-695/med-6.7 | (°·i+1.9pp (4/14) · p-3.0pp cap51.8 net-584/med-17.0) |
| S1-H9 | keep-watching | ▼i-13.5pp (2/25) · p+5.9pp cap265.9 net-373/med+10.8 | (°▼i-25.8pp (0/5) · p-30.9pp cap— net-57/med+2.3) | (°▼i-5.0pp (3/17) · p-11.5pp cap65.5 net-692/med-25.7) | (°▲i+23.3pp (2/4) · p-31.6pp cap— net-598/med-160.8) |
| S0-H10 | deprioritize | ·i-0.9pp (36/175) · p-5.5pp cap88.9 net+2743/med+15.3 | (°▼i-12.5pp (2/15) · p-17.6pp cap46.2 net-356/med-1.7) | ▼i-6.5pp (44/274) · p-3.6pp cap46.8 net-2610/med-9.9 | ▼i-3.2pp (19/81) · p+6.7pp cap42.9 net-566/med-10.5 |
| S0-H11 | keep-watching | ▼i-3.2pp (48/263) · p+2.6pp cap135.9 net+863/med+0.9 | ·i-1.6pp (22/91) · p-2.3pp cap113.7 net+264/med-3.9 | ▼i-4.6pp (69/384) · p+4.3pp cap78.7 net+2905/med+1.6 | ·i-1.7pp (26/104) · p+6.9pp cap85.5 net+1559/med+3.9 |
| S1-H11 | keep-watching | ▼i-8.3pp (23/174) · p+4.9pp cap130.1 net+293/med-14.1 | ·i+0.6pp (14/53) · p-2.6pp cap109.7 net-436/med-14.7 | ·i+1.5pp (90/373) · p+4.3pp cap78.2 net-1690/med-2.7 | ·i-0.6pp (29/111) · p-0.1pp cap80.5 net-441/med-1.9 |
| S0-H12 | keep-watching | — | — | — | — |
| S0-H13 | keep-watching | (°▼i-21.5pp (0/1) · p+77.9pp cap95.7 net+93/med+93.0) | (°▼i-25.8pp (0/1) · p+69.1pp cap95.7 net+93/med+93.0) | (°▼i-22.6pp (0/1) · p-23.3pp cap— net-37/med-37.2) | — |
| S0-H14 | keep-watching | ·i+0.1pp (36/167) · p-13.7pp cap70.2 net-692/med+6.9 | ▼i-10.4pp (4/26) · p-19.4pp cap41.8 net-1762/med-17.1 | ▼i-7.5pp (41/272) · p-6.8pp cap53.7 net-2082/med-7.0 | ▼i-4.7pp (13/59) · p+2.3pp cap55.7 net+90/med-7.0 |
| S0-H15 | keep-watching | — | — | — | — |
| S0-H16 | keep-watching | (°▼i-11.5pp (1/10) · p+27.9pp cap121.0 net+274/med+0.1) | — | (°▼i-14.3pp (1/12) · p+18.4pp cap76.1 net+365/med+26.8) | — |
| S0-H17 | rows | (°▼i-8.2pp (2/15) · p+17.9pp cap166.0 net+681/med+10.2) | (°▼i-5.8pp (1/5) · p+9.1pp cap125.1 net-18/med-23.3) | ▲i+2.4pp (9/36) · p+15.6pp cap80.3 net+249/med+18.8 | (°▲i+9.0pp (5/14) · p-3.0pp cap95.9 net-206/med-10.1) |
| S0-H18 | rows | ▼i-7.7pp (8/58) · p-8.3pp cap127.3 net-1784/med-23.8 | ▲i+3.4pp (7/24) · p-22.6pp cap111.1 net-559/med-16.3 | ·i+1.4pp (18/75) · p+4.7pp cap106.1 net+505/med-0.7 | (°▲i+6.6pp (6/18) · p+12.8pp cap112.0 net+48/med-10.9) |
| S0-H19 | rows | ·i-1.9pp (40/204) · p+0.9pp cap180.0 net+1513/med+6.5 | ▼i-15.3pp (4/38) · p-2.0pp cap98.9 net-152/med+12.8 | ▲i+2.0pp (64/260) · p-2.5pp cap85.8 net-340/med-0.2 | ▲i+4.3pp (22/71) · p-3.4pp cap102.5 net-248/med+5.3 |
| S0-H20 | rows | ▼i-10.5pp (1/46) · p+8.5pp cap277.1 [cls 39.3%/12.7%i] net+1398/med+2.9 | (°▲i+13.5pp (1/3) · p-38.7pp cap— [cls 38.7%/19.8%i] net-182/med-90.2) | ▼i-11.7pp (2/52) · p+10.5pp cap85.4 [cls 37.6%/15.5%i] net-652/med-11.3 | (°▼i-13.9pp (1/11) · p-8.4pp cap97.6 [cls 35.7%/23.0%i] net-424/med-23.1) |
| **union coverage** | | 45.1% (51/113) | 39.0% (16/41) | 86.0% (104/121) | 84.6% (33/39) |

Not graded:  — see register entries.

## Hypothesis Cards (page 2)

### H1 — 2 signals
*A climactic bar — extreme volume on a wide spread late in an extended move — marks exhaustion, and price then reverses against the climax direction.*
Grading: directional. Latest review: keep-watching (recommendation).

- Question **Q1-H1**: see the register entry (status there is authoritative).
**S0-H1** — session × window grid (cells as in the matrix):

| session | backtest | forward |
|---|---|---|
| whole | ·i-0.9pp (7/34) · p+19.1pp cap182.2 net+122/med-15.7 | ▲i+7.8pp (21/69) · p+14.4pp cap78.5 net+791/med+18.4 |
| london | (°▲i+11.7pp (3/8) · p-18.4pp cap153.6 net-257/med-46.2) | ▲i+7.7pp (11/32) · p+5.9pp cap93.9 net+217/med+11.2 |
| overlap | — | — |
| ny_only | (°▼i-19.0pp (0/11) · p+50.5pp cap246.0 net-215/med-87.5) | (°▲i+18.6pp (2/5) · p-9.1pp cap— net+40/med+22.6) |
| dead | (°▲i+31.6pp (4/8) · p+0.9pp cap406.7 net-181/med-23.6) | ▲i+8.8pp (7/22) · p+25.8pp cap78.0 net+273/med+19.8 |
| asia | (°▼i-24.3pp (0/7) · p+51.5pp cap178.9 net+776/med+154.4) | (°▼i-13.5pp (1/10) · p+16.6pp cap90.6 net+261/med+19.4) |

- backtest payoff: right +2899 / wrong -2777 / net +122 pts; median per fire -15.65 (n=34)
- backtest best call: 2026-07-29 18:02 +663.1pts remaining (episode 663.1pts, major)
- backtest worst false alarm: 2026-07-29 19:01 -712.5pts adverse
- forward payoff: right +2318 / wrong -1528 / net +791 pts; median per fire +18.40 (n=69)
- forward best call: 2026-08-20 09:43 +293.2pts remaining (episode 306.7pts, major)
- forward worst false alarm: 2026-08-20 11:25 -184.0pts adverse
- earliness (backtest): median 183.0 pts of move remaining at fire (n=8)

**S1-H1** — session × window grid (cells as in the matrix):

| session | backtest | forward |
|---|---|---|
| whole | (°▲i+11.8pp (1/3) · p+44.6pp cap279.0 net+465/med+128.4) | (°▼i-22.6pp (0/2) · p+76.7pp cap90.8 net+170/med+85.0) |
| london | — | (°▼i-26.7pp (0/1) · p+68.4pp cap74.3 net+74/med+74.3) |
| overlap | — | — |
| ny_only | — | — |
| dead | (°▲i+31.6pp (1/2) · p+38.4pp cap406.7 net+337/med+168.5) | (°▼i-23.0pp (0/1) · p+80.3pp cap107.3 net+96/med+95.6) |
| asia | (°▼i-24.3pp (0/1) · p+80.1pp cap151.3 net+128/med+128.4) | — |

- backtest payoff: right +521 / wrong -56 / net +465 pts; median per fire +128.40 (n=3)
- backtest best call: 2026-07-28 23:45 +372.3pts remaining (episode 501.5pts, major)
- backtest worst false alarm: 2026-07-28 23:45 -141.6pts adverse
- forward payoff: right +170 / wrong +0 / net +170 pts; median per fire +84.95 (n=2)
- earliness (backtest): median 372.3 pts of move remaining at fire (n=1)

### H2 — 2 signals
*A failed probe beyond a prior extreme — an upthrust above or spring below that closes back inside — reverses against the probe.*
Grading: directional. Latest review: promote-candidate (recommendation).

**S0-H2** — session × window grid (cells as in the matrix):

| session | backtest | forward |
|---|---|---|
| whole | ▼i-3.1pp (59/320) · p-2.1pp cap156.4 net-3528/med-1.4 | ▼i-4.0pp (76/408) · p+8.1pp cap81.4 net+1812/med+3.5 |
| london | ·i+1.3pp (16/59) · p-5.5pp cap106.7 net-313/med-30.0 | ▼i-2.3pp (30/123) · p+5.8pp cap84.6 net+458/med+5.7 |
| overlap | (°▼i-4.8pp (1/32) · p-12.6pp cap193.4 net-742/med-38.1) | (°▼i-8.8pp (0/15) · p-8.2pp cap192.4 net+312/med+3.8) |
| ny_only | ▼i-9.1pp (7/71) · p+2.4pp cap234.9 net-3199/med-7.4 | ▼i-7.4pp (8/57) · p+6.7pp cap111.7 net+49/med-0.1 |
| dead | ·i+0.4pp (9/48) · p+5.1pp cap284.2 net+874/med+2.4 | ▼i-3.0pp (12/60) · p+18.6pp cap82.5 net+438/med+3.2 |
| asia | ·i-0.7pp (26/110) · p+0.1pp cap113.5 net-147/med+10.2 | ▼i-6.5pp (26/153) · p+6.7pp cap71.5 net+555/med+3.4 |

- backtest payoff: right +13405 / wrong -16933 / net -3528 pts; median per fire -1.35 (n=320)
- backtest best call: 2026-07-30 07:00 +812.7pts remaining (episode 832.8pts, major)
- backtest worst false alarm: 2026-07-29 19:00 -719.1pts adverse
- forward payoff: right +10639 / wrong -8827 / net +1812 pts; median per fire +3.50 (n=408)
- forward best call: 2026-08-21 11:28 +288.7pts remaining (episode 309.6pts, major)
- forward worst false alarm: 2026-08-19 12:55 -322.0pts adverse
- earliness (backtest): median 111.3 pts of move remaining at fire (n=25)

**S1-H2** — session × window grid (cells as in the matrix):

| session | backtest | forward |
|---|---|---|
| whole | ▼i-2.6pp (42/222) · p-1.4pp cap142.3 net-1379/med-4.2 | ·i-0.6pp (64/291) · p+6.6pp cap82.8 net+1424/med+4.5 |
| london | ▲i+4.4pp (13/43) · p-3.0pp cap101.9 net-382/med-31.5 | ▲i+3.1pp (25/84) · p+2.9pp cap85.6 net+313/med+6.5 |
| overlap | (°▼i-7.9pp (0/20) · p-2.6pp cap185.1 net+164/med+49.0) | (°▼i-8.8pp (0/12) · p-9.9pp cap165.1 net+212/med+0.4) |
| ny_only | ▼i-10.7pp (4/48) · p-0.6pp cap194.2 net-1585/med-19.9 | ▼i-5.5pp (7/44) · p+6.8pp cap91.3 net-66/med+0.6 |
| dead | ▲i+2.8pp (7/33) · p+0.5pp cap206.8 net+152/med-7.9 | ▲i+2.6pp (10/39) · p+11.1pp cap83.9 net+195/med+4.0 |
| asia | ·i-1.2pp (18/78) · p+1.9pp cap106.9 net+272/med+15.2 | ▼i-3.9pp (22/112) · p+8.7pp cap68.9 net+770/med+5.0 |

- backtest payoff: right +8973 / wrong -10352 / net -1379 pts; median per fire -4.15 (n=222)
- backtest best call: 2026-07-30 07:00 +812.7pts remaining (episode 832.8pts, major)
- backtest worst false alarm: 2026-07-29 19:16 -700.8pts adverse
- forward payoff: right +7743 / wrong -6318 / net +1424 pts; median per fire +4.50 (n=291)
- forward best call: 2026-08-21 11:28 +288.7pts remaining (episode 309.6pts, major)
- forward worst false alarm: 2026-08-19 13:09 -291.0pts adverse
- earliness (backtest): median 118.9 pts of move remaining at fire (n=23)

### H3 — 1 signal
*Repeated absorption — high effort with no result — at a price level precedes a breakout through that level.*
Grading: directional. Latest review: keep-watching (recommendation).

**S0-H3** — session × window grid (cells as in the matrix):

| session | backtest | forward |
|---|---|---|
| whole | (°▼i-21.5pp (0/1) · p+77.9pp cap105.8 net+106/med+105.8) | (°▼i-22.6pp (0/1) · p-23.3pp cap— net-1/med-1.1) |
| london | (°▼i-25.8pp (0/1) · p+69.1pp cap105.8 net+106/med+105.8) | — |
| overlap | — | — |
| ny_only | — | — |
| dead | — | — |
| asia | — | (°▼i-23.5pp (0/1) · p-23.4pp cap— net-1/med-1.1) |

- backtest payoff: right +106 / wrong +0 / net +106 pts; median per fire +105.80 (n=1)
- forward payoff: right +0 / wrong -1 / net -1 pts; median per fire -1.10 (n=1)
- forward worst false alarm: 2026-08-25 01:40 -42.8pts adverse

### H4 — 1 signal
*In an established trend, a quiet (low-volume) pullback resolves with trend resumption.*
Grading: directional. Latest review: keep-watching (recommendation).

**S0-H4** — session × window grid (cells as in the matrix):

| session | backtest | forward |
|---|---|---|
| whole | — | (°▼i-22.6pp (0/10) · p+36.7pp cap38.4 net-18/med-7.4) |
| london | — | (°▼i-26.7pp (0/5) · p+8.4pp cap31.1 net+26/med+9.5) |
| overlap | — | — |
| ny_only | — | — |
| dead | — | — |
| asia | — | (°▼i-23.5pp (0/5) · p+56.6pp cap44.3 net-44/med-8.1) |

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
| whole | ▲i+4.5pp (5/29) · p-8.3pp cap260.8 [cls 39.3%/12.7%i] net-232/med-11.8 | ▲i+5.2pp (17/82) · p+6.3pp cap92.4 [cls 37.6%/15.5%i] net+1138/med+6.2 |
| london | (°▲i+60.2pp (4/5) · p-38.7pp cap— [cls 38.7%/19.8%i] net-719/med-105.3) | ▲i+2.0pp (6/24) · p+22.6pp cap74.2 [cls 35.7%/23.0%i] net+723/med+28.0 |
| overlap | (°·i-1.8pp (1/20) · p-7.4pp cap263.9 [cls 47.4%/6.8%i] net+333/med+9.0) | (°▲i+5.6pp (4/37) · p-0.2pp cap106.0 [cls 48.8%/5.2%i] net+563/med-3.3) |
| ny_only | — | (°▼i-8.8pp (0/2) · p-8.8pp cap— [cls 8.8%/8.8%i] net-72/med-36.0) |
| dead | (°▼i-13.5pp (0/3) · p-23.8pp cap— [cls 23.8%/13.5%i] net+42/med+18.9) | (°▲i+21.6pp (1/3) · p-5.0pp cap71.8 [cls 38.3%/11.7%i] net-1/med+15.9) |
| asia | (°▼i-18.0pp (0/1) · p+74.8pp cap129.0 [cls 25.2%/18.0%i] net+112/med+111.8) | (°▲i+16.3pp (6/16) · p-8.8pp cap87.4 [cls 27.6%/21.2%i] net-75/med+0.3) |

- backtest payoff: right +1875 / wrong -2108 / net -232 pts; median per fire -11.80 (n=29)
- backtest best call: 2026-08-03 11:04 +303.5pts remaining (episode 396.3pts, major)
- backtest worst false alarm: 2026-07-27 13:46 -514.5pts adverse
- forward payoff: right +3041 / wrong -1903 / net +1138 pts; median per fire +6.15 (n=82)
- forward best call: 2026-08-27 03:31 +150.7pts remaining (episode 141.2pts, major)
- forward worst false alarm: 2026-08-24 13:32 -193.9pts adverse
- earliness (backtest): median 78.8 pts of move remaining at fire (n=2)

### H7 — 1 signal
*Quiet decline at a session extreme is disguised accumulation: effortless (low-volume) weakness reverses UP once selling fails to attract participation (mirror: quiet advance at a high reverses down).*
Grading: directional + either-direction (dual). Latest review: keep-watching (recommendation).

- Question **Q1-H7**: see the register entry (status there is authoritative).
**S0-H7** — session × window grid (cells as in the matrix):

| session | backtest | forward |
|---|---|---|
| whole | ▼i-5.5pp (8/50) · p-0.1pp cap169.0 net+77/med-7.8 | ·i-1.9pp (17/82) · p+3.5pp cap80.7 net+96/med+8.9 |
| london | (°·i-0.8pp (4/16) · p-5.9pp cap123.6 net-167/med-6.6) | ▲i+5.1pp (7/22) · p+9.3pp cap82.9 net+404/med+10.0 |
| overlap | (°▲i+4.6pp (1/8) · p+24.9pp cap183.1 net+464/med+8.3) | (°▼i-8.8pp (0/8) · p+15.1pp cap115.7 net+99/med+26.9) |
| ny_only | (°▲i+6.0pp (2/8) · p-13.1pp cap— net-76/med-18.5) | (°▼i-2.6pp (3/16) · p-2.9pp cap107.5 net-36/med+9.3) |
| dead | (°·i+1.6pp (1/5) · p-11.6pp cap— net+53/med+23.0) | (°▼i-10.5pp (1/8) · p-7.2pp cap71.3 net-100/med-1.0) |
| asia | (°▼i-24.3pp (0/13) · p-4.5pp cap142.4 net-196/med-24.5) | ▼i-2.1pp (6/28) · p+1.6pp cap64.0 net-270/med+5.2 |

- backtest payoff: right +2351 / wrong -2274 / net +77 pts; median per fire -7.75 (n=50)
- backtest best call: 2026-07-29 09:26 +577.3pts remaining (episode 632.8pts, major)
- backtest worst false alarm: 2026-07-31 13:43 -365.8pts adverse
- forward payoff: right +2262 / wrong -2166 / net +96 pts; median per fire +8.95 (n=82)
- forward best call: 2026-08-19 13:50 +160.3pts remaining (episode 160.3pts)
- forward worst false alarm: 2026-08-20 12:41 -171.4pts adverse
- earliness (backtest): median 308.2 pts of move remaining at fire (n=7)

**S0-H7 (either-dir)** — session × window grid (cells as in the matrix):

| session | backtest | forward |
|---|---|---|
| whole | ▼i-10.4pp (15/50) · p+4.2pp cap46.5 | ▼i-9.1pp (27/82) · p+13.7pp cap44.5 |
| london | (°▲i+2.2pp (8/16) · p+0.1pp cap23.3) | ·i-0.5pp (11/22) · p+15.1pp cap55.0 |
| overlap | (°▼i-3.3pp (1/8) · p+30.0pp cap118.7) | (°▼i-15.8pp (0/8) · p+0.9pp cap113.3) |
| ny_only | (°·i+0.7pp (3/8) · p-13.1pp cap18.8) | (°▼i-14.2pp (4/16) · p+0.6pp cap7.0) |
| dead | (°▼i-14.4pp (1/5) · p-22.4pp cap—) | (°▼i-29.9pp (1/8) · p+13.4pp cap21.8) |
| asia | (°▼i-30.1pp (2/13) · p-1.0pp cap35.7) | ▼i-4.3pp (11/28) · p+22.1pp cap17.9 |

- backtest payoff: n/a by construction (either-direction)
- backtest best call: 2026-07-29 09:26 +577.3pts remaining (episode 632.8pts, major)
- backtest worst false alarm: 2026-07-29 02:54 -123.2pts adverse
- forward payoff: n/a by construction (either-direction)
- forward best call: 2026-08-27 04:47 +144.9pts remaining (episode 220.1pts, major)
- forward worst false alarm: 2026-08-20 14:49 -108.6pts adverse
- earliness (backtest): median 170.9 pts of move remaining at fire (n=14)

### H8 — 1 signal
*Reversal-signature bar anatomy (upthrust/spring) predicts imminent range expansion irrespective of direction.*
Grading: either-direction. Latest review: keep-watching (recommendation).

**S0-H8** — session × window grid (cells as in the matrix):

| session | backtest | forward |
|---|---|---|
| whole | ▼i-3.8pp (117/320) · p+2.3pp cap65.1 | ·i-0.3pp (170/408) · p+6.4pp cap61.6 |
| london | ▼i-7.1pp (24/59) · p+4.9pp cap53.7 | ▲i+4.0pp (67/123) · p+4.2pp cap63.1 |
| overlap | (°▼i-9.6pp (2/32) · p-4.4pp cap69.4) | (°▼i-15.8pp (0/15) · p-28.3pp cap165.1) |
| ny_only | ▼i-12.9pp (17/71) · p+18.1pp cap52.0 | ▼i-7.6pp (18/57) · p+4.6pp cap85.5 |
| dead | ▼i-3.2pp (15/48) · p+2.6pp cap133.9 | ▲i+7.6pp (30/60) · p+23.4pp cap63.4 |
| asia | ▲i+8.1pp (59/110) · p-2.2pp cap81.9 | ▼i-7.7pp (55/153) · p+2.6pp cap56.8 |

- backtest payoff: n/a by construction (either-direction)
- backtest best call: 2026-07-30 06:39 +793.0pts remaining (episode 832.8pts, major)
- backtest worst false alarm: 2026-07-29 19:48 -233.6pts adverse
- forward payoff: n/a by construction (either-direction)
- forward best call: 2026-08-21 11:26 +303.6pts remaining (episode 309.6pts, major)
- forward worst false alarm: 2026-08-28 16:07 -114.0pts adverse
- earliness (backtest): median 130.5 pts of move remaining at fire (n=32)

### H9 — 2 signals
*Persistent lower-TF directional pressure that recruits expanding participation at the parent timeframe precedes continuation beyond what the parent label alone predicts; pressure without participation expansion does not.*
Grading: directional. Latest review: keep-watching (recommendation).

- Question **Q2-H9**: see the register entry (status there is authoritative).
**S0-H9** — session × window grid (cells as in the matrix):

| session | backtest | forward |
|---|---|---|
| whole | ▲i+2.4pp (21/88) · p+0.6pp cap129.2 net+593/med-4.3 | ▼i-5.0pp (19/108) · p-7.6pp cap58.2 net-695/med-6.7 |
| london | (°▼i-25.8pp (0/9) · p+2.4pp cap76.3 net+410/med+11.6) | (°·i+1.9pp (4/14) · p-3.0pp cap51.8 net-584/med-17.0) |
| overlap | (°▼i-7.9pp (0/10) · p+12.4pp cap306.3 net+540/med+51.3) | (°▼i-8.8pp (0/11) · p-16.7pp cap120.8 net+79/med-10.2) |
| ny_only | ▲i+29.0pp (12/25) · p-5.1pp cap125.7 net-148/med-7.0 | ▼i-4.7pp (5/30) · p-2.4pp cap61.4 net-243/med-5.0 |
| dead | (°▲i+5.1pp (4/17) · p+17.8pp cap265.9 net+98/med-5.5) | (°▼i-15.3pp (1/13) · p-12.0pp cap78.4 net+87/med+6.3) |
| asia | ▼i-5.8pp (5/27) · p-1.4pp cap78.6 net-307/med-10.2 | ·i-1.0pp (9/40) · p-3.4pp cap53.9 net-34/med-9.6 |

- backtest payoff: right +3019 / wrong -2427 / net +593 pts; median per fire -4.35 (n=88)
- backtest best call: 2026-08-03 03:30 +174.2pts remaining (episode 209.2pts, major)
- backtest worst false alarm: 2026-07-29 18:45 -500.8pts adverse
- forward payoff: right +1402 / wrong -2097 / net -695 pts; median per fire -6.70 (n=103)
- forward best call: 2026-08-17 15:30 +189.7pts remaining (episode 134.5pts)
- forward worst false alarm: 2026-08-19 13:00 -321.5pts adverse
- earliness (backtest): median 116.8 pts of move remaining at fire (n=6)

**S1-H9** — session × window grid (cells as in the matrix):

| session | backtest | forward |
|---|---|---|
| whole | ▼i-13.5pp (2/25) · p+5.9pp cap265.9 net-373/med+10.8 | (°▼i-5.0pp (3/17) · p-11.5pp cap65.5 net-692/med-25.7) |
| london | (°▼i-25.8pp (0/5) · p-30.9pp cap— net-57/med+2.3) | (°▲i+23.3pp (2/4) · p-31.6pp cap— net-598/med-160.8) |
| overlap | (°▼i-7.9pp (0/1) · p+62.4pp cap306.3 net+150/med+150.3) | — |
| ny_only | (°▼i-19.0pp (0/3) · p-13.1pp cap— net-373/med+63.9) | (°▼i-4.7pp (1/6) · p-9.1pp cap— net-154/med+5.0) |
| dead | (°▼i-18.4pp (0/8) · p+50.9pp cap265.9 net+174/med+55.5) | (°▼i-23.0pp (0/3) · p+13.6pp cap78.4 net+78/med+78.4) |
| asia | (°·i+0.7pp (2/8) · p-7.4pp cap78.6 net-267/med-8.6) | (°▼i-23.5pp (0/4) · p+1.6pp cap52.5 net-18/med-5.7) |

- backtest payoff: right +1181 / wrong -1554 / net -373 pts; median per fire +10.80 (n=25)
- backtest best call: 2026-07-30 03:00 +120.0pts remaining (episode 134.4pts)
- backtest worst false alarm: 2026-07-29 18:45 -500.8pts adverse
- forward payoff: right +215 / wrong -906 / net -692 pts; median per fire -25.70 (n=15)
- forward best call: 2026-08-19 18:40 +56.7pts remaining (episode 74.5pts)
- forward worst false alarm: 2026-08-19 13:00 -321.5pts adverse
- earliness (backtest): median 120.0 pts of move remaining at fire (n=1)

### H10 — 1 signal
*In an established 1-minute trend, no-demand/no-supply prints in the trend's direction signal continuation.*
Grading: directional. Latest review: deprioritize (recommendation).

**S0-H10** — session × window grid (cells as in the matrix):

| session | backtest | forward |
|---|---|---|
| whole | ·i-0.9pp (36/175) · p-5.5pp cap88.9 net+2743/med+15.3 | ▼i-6.5pp (44/274) · p-3.6pp cap46.8 net-2610/med-9.9 |
| london | (°▼i-12.5pp (2/15) · p-17.6pp cap46.2 net-356/med-1.7) | ▼i-3.2pp (19/81) · p+6.7pp cap42.9 net-566/med-10.5 |
| overlap | (°▼i-7.9pp (0/18) · p-37.6pp cap— net+764/med+45.5) | (°▼i-6.6pp (1/45) · p-21.6pp cap124.9 net-1283/med-34.0) |
| ny_only | ·i+1.8pp (10/48) · p-6.9pp cap88.9 net+398/med+12.5 | ▲i+8.1pp (13/44) · p+0.0pp cap80.8 net+46/med+1.1 |
| dead | (°▼i-5.9pp (2/16) · p+0.9pp cap254.7 net+551/med+8.9) | (°▼i-5.4pp (3/17) · p-19.7pp cap— net-324/med-14.4) |
| asia | ▲i+3.9pp (22/78) · p+8.3pp cap84.4 net+1385/med+15.6 | ▼i-14.3pp (8/87) · p-8.5pp cap49.8 net-483/med-6.6 |

- backtest payoff: right +4792 / wrong -2049 / net +2743 pts; median per fire +15.30 (n=175)
- backtest best call: 2026-08-03 03:44 +199.5pts remaining (episode 209.2pts, major)
- backtest worst false alarm: 2026-07-27 12:56 -252.9pts adverse
- forward payoff: right +2644 / wrong -5255 / net -2610 pts; median per fire -9.95 (n=274)
- forward best call: 2026-08-26 17:22 +175.5pts remaining (episode 153.9pts, major)
- forward worst false alarm: 2026-08-26 13:58 -151.0pts adverse
- earliness (backtest): median 108.5 pts of move remaining at fire (n=7)

### H11 — 2 signals
*Price entering a low-volume price zone traverses it faster than baseline; entering a high-volume node it stalls or reverses at above-baseline rates.*
Grading: directional. Latest review: keep-watching (recommendation).

- Question **Q1-H11**: see the register entry (status there is authoritative).
- Question **Q2-H11**: see the register entry (status there is authoritative).
**S0-H11** — session × window grid (cells as in the matrix):

| session | backtest | forward |
|---|---|---|
| whole | ▼i-3.2pp (48/263) · p+2.6pp cap135.9 net+863/med+0.9 | ▼i-4.6pp (69/384) · p+4.3pp cap78.7 net+2905/med+1.6 |
| london | ·i-1.6pp (22/91) · p-2.3pp cap113.7 net+264/med-3.9 | ·i-1.7pp (26/104) · p+6.9pp cap85.5 net+1559/med+3.9 |
| overlap | (°▼i-7.9pp (0/20) · p+2.4pp cap232.1 net-137/med-23.4) | (°·i+0.7pp (6/63) · p-7.9pp cap106.6 net+429/med+6.1) |
| ny_only | ▼i-12.1pp (2/29) · p+14.5pp cap229.4 net+826/med+77.1 | ▼i-2.4pp (20/105) · p+1.4pp cap110.0 net+233/med-1.6 |
| dead | ·i-1.2pp (10/58) · p+10.8pp cap98.2 net+874/med-3.1 | ▼i-4.8pp (4/22) · p+7.6pp cap79.7 net+169/med+2.6 |
| asia | ▼i-2.8pp (14/65) · p-4.5pp cap108.5 net-964/med+3.6 | ▼i-9.1pp (13/90) · p+12.2pp cap66.7 net+515/med-1.4 |

- backtest payoff: right +10765 / wrong -9902 / net +863 pts; median per fire +0.90 (n=262)
- backtest best call: 2026-07-30 07:02 +741.2pts remaining (episode 832.8pts, major)
- backtest worst false alarm: 2026-07-29 13:50 -332.3pts adverse
- forward payoff: right +9471 / wrong -6567 / net +2905 pts; median per fire +1.65 (n=384)
- forward best call: 2026-08-24 09:01 +259.2pts remaining (episode 284.5pts, major)
- forward worst false alarm: 2026-08-24 13:14 -252.8pts adverse
- earliness (backtest): median 176.0 pts of move remaining at fire (n=14)

**S1-H11** — session × window grid (cells as in the matrix):

| session | backtest | forward |
|---|---|---|
| whole | ▼i-8.3pp (23/174) · p+4.9pp cap130.1 net+293/med-14.1 | ·i+1.5pp (90/373) · p+4.3pp cap78.2 net-1690/med-2.7 |
| london | ·i+0.6pp (14/53) · p-2.6pp cap109.7 net-436/med-14.7 | ·i-0.6pp (29/111) · p-0.1pp cap80.5 net-441/med-1.9 |
| overlap | (°·i-1.2pp (1/15) · p-10.9pp cap192.0 net-139/med-40.7) | (°▼i-8.8pp (0/15) · p+18.4pp cap75.2 net-475/med-69.7) |
| ny_only | ▼i-19.0pp (0/39) · p+10.0pp cap558.0 net+1758/med-19.4 | ▲i+9.8pp (15/48) · p+7.6pp cap80.9 net-38/med+1.4 |
| dead | (°·i-1.7pp (2/12) · p-3.3pp cap141.6 net-253/med+3.9) | ▲i+5.0pp (14/50) · p+16.3pp cap85.0 net+41/med+0.1 |
| asia | ▼i-13.4pp (6/55) · p+12.8pp cap124.1 net-637/med-13.4 | ▼i-2.0pp (32/149) · p-0.6pp cap68.0 net-777/med-3.4 |

- backtest payoff: right +9792 / wrong -9499 / net +293 pts; median per fire -14.05 (n=174)
- backtest best call: 2026-07-29 09:17 +555.3pts remaining (episode 632.8pts, major)
- backtest worst false alarm: 2026-07-29 19:07 -730.3pts adverse
- forward payoff: right +8040 / wrong -9730 / net -1690 pts; median per fire -2.70 (n=373)
- forward best call: 2026-08-21 10:37 +253.4pts remaining (episode 309.6pts, major)
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
| whole | (°▼i-21.5pp (0/1) · p+77.9pp cap95.7 net+93/med+93.0) | (°▼i-22.6pp (0/1) · p-23.3pp cap— net-37/med-37.2) |
| london | (°▼i-25.8pp (0/1) · p+69.1pp cap95.7 net+93/med+93.0) | — |
| overlap | — | — |
| ny_only | — | (°▼i-21.4pp (0/1) · p-9.1pp cap— net-37/med-37.2) |
| dead | — | — |
| asia | — | — |

- backtest payoff: right +93 / wrong +0 / net +93 pts; median per fire +93.00 (n=1)
- forward payoff: right +0 / wrong -37 / net -37 pts; median per fire -37.20 (n=1)
- forward worst false alarm: 2026-08-25 18:46 -56.7pts adverse

### H14 — 1 signal
*Counter-trend No Demand / No Supply prints in an established trend mark absorption and precede trend continuation.*
Grading: directional. Latest review: keep-watching (recommendation).

**S0-H14** — session × window grid (cells as in the matrix):

| session | backtest | forward |
|---|---|---|
| whole | ·i+0.1pp (36/167) · p-13.7pp cap70.2 net-692/med+6.9 | ▼i-7.5pp (41/272) · p-6.8pp cap53.7 net-2082/med-7.0 |
| london | ▼i-10.4pp (4/26) · p-19.4pp cap41.8 net-1762/med-17.1 | ▼i-4.7pp (13/59) · p+2.3pp cap55.7 net+90/med-7.0 |
| overlap | (°▼i-7.9pp (0/17) · p-37.6pp cap— net+433/med+24.0) | (°▼i-6.7pp (1/47) · p-22.1pp cap149.2 net-1488/med-46.4) |
| ny_only | ▲i+14.3pp (17/51) · p-13.1pp cap— net+410/med+13.6 | ▲i+11.9pp (18/54) · p-7.2pp cap101.5 net-192/med+5.0 |
| dead | (°▼i-7.3pp (2/18) · p-11.6pp cap— net-56/med+4.5) | (°▼i-6.3pp (2/12) · p-11.4pp cap68.8 net-247/med-18.6) |
| asia | ·i-0.7pp (13/55) · p+0.1pp cap85.1 net+282/med+6.6 | ▼i-16.5pp (7/100) · p-6.4pp cap49.2 net-244/med-3.1 |

- backtest payoff: right +2905 / wrong -3598 / net -692 pts; median per fire +6.90 (n=167)
- backtest best call: 2026-08-03 03:48 +195.6pts remaining (episode 209.2pts, major)
- backtest worst false alarm: 2026-07-27 12:59 -334.6pts adverse
- forward payoff: right +3134 / wrong -5216 / net -2082 pts; median per fire -6.95 (n=272)
- forward best call: 2026-08-26 17:14 +195.8pts remaining (episode 153.9pts, major)
- forward worst false alarm: 2026-08-26 14:00 -167.8pts adverse
- earliness (backtest): median 107.3 pts of move remaining at fire (n=10)

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
| whole | (°▼i-11.5pp (1/10) · p+27.9pp cap121.0 net+274/med+0.1) | (°▼i-14.3pp (1/12) · p+18.4pp cap76.1 net+365/med+26.8) |
| london | — | — |
| overlap | — | — |
| ny_only | (°▼i-9.0pp (1/10) · p+36.9pp cap121.0 net+274/med+0.1) | (°▼i-13.1pp (1/12) · p+32.6pp cap76.1 net+365/med+26.8) |
| dead | — | — |
| asia | — | — |

- backtest payoff: right +666 / wrong -392 / net +274 pts; median per fire +0.05 (n=10)
- backtest best call: 2026-08-03 19:30 +30.1pts remaining (episode 61.6pts)
- backtest worst false alarm: 2026-07-23 19:30 -188.1pts adverse
- forward payoff: right +381 / wrong -16 / net +365 pts; median per fire +26.80 (n=12)
- forward best call: 2026-08-21 19:30 +25.6pts remaining (episode 56.1pts)
- forward worst false alarm: 2026-08-26 19:30 -47.2pts adverse
- earliness (backtest): median 30.1 pts of move remaining at fire (n=1)

### H17 — 1 signal
*A climax reversal signal followed by absorption within five bars — effort meeting a quiet counter-party — marks a genuine exhaustion turn: the two-chapter story (exhaustion needs absorption to become reversal).*
Grading: directional. Latest review: rows (recommendation).

**S0-H17** — session × window grid (cells as in the matrix):

| session | backtest | forward |
|---|---|---|
| whole | (°▼i-8.2pp (2/15) · p+17.9pp cap166.0 net+681/med+10.2) | ▲i+2.4pp (9/36) · p+15.6pp cap80.3 net+249/med+18.8 |
| london | (°▼i-5.8pp (1/5) · p+9.1pp cap125.1 net-18/med-23.3) | (°▲i+9.0pp (5/14) · p-3.0pp cap95.9 net-206/med-10.1) |
| overlap | — | — |
| ny_only | — | (°▼i-21.4pp (0/2) · p-9.1pp cap— net+74/med+36.8) |
| dead | (°·i+1.6pp (1/5) · p+8.4pp cap360.0 net+282/med+13.9) | (°▲i+4.3pp (3/11) · p+34.8pp cap66.9 net+116/med+23.7) |
| asia | (°▼i-24.3pp (0/5) · p+40.1pp cap172.4 net+417/med+120.1) | (°▼i-12.4pp (1/9) · p+21.0pp cap79.2 net+266/med+33.3) |

- backtest payoff: right +958 / wrong -277 / net +681 pts; median per fire +10.20 (n=15)
- backtest best call: 2026-07-29 23:42 +191.5pts remaining (episode 157.1pts)
- backtest worst false alarm: 2026-07-28 07:57 -96.5pts adverse
- forward payoff: right +1108 / wrong -858 / net +249 pts; median per fire +18.80 (n=36)
- forward best call: 2026-08-20 09:44 +291.5pts remaining (episode 306.7pts, major)
- forward worst false alarm: 2026-08-20 11:26 -192.8pts adverse
- earliness (backtest): median 150.3 pts of move remaining at fire (n=2)

### H18 — 1 signal
*A gap-traversal signal followed by a same-direction effortless print within five bars — travel meeting no opposition — continues: the map says vacuum, the tape confirms no resistance.*
Grading: directional. Latest review: rows (recommendation).

**S0-H18** — session × window grid (cells as in the matrix):

| session | backtest | forward |
|---|---|---|
| whole | ▼i-7.7pp (8/58) · p-8.3pp cap127.3 net-1784/med-23.8 | ·i+1.4pp (18/75) · p+4.7pp cap106.1 net+505/med-0.7 |
| london | ▲i+3.4pp (7/24) · p-22.6pp cap111.1 net-559/med-16.3 | (°▲i+6.6pp (6/18) · p+12.8pp cap112.0 net+48/med-10.9) |
| overlap | (°▼i-7.9pp (0/6) · p+29.1pp cap141.5 net-621/med-85.3) | (°▲i+7.9pp (2/12) · p-1.6pp cap88.9 net+295/med+37.9) |
| ny_only | (°▼i-19.0pp (0/3) · p-13.1pp cap— net-88/med-59.0) | ▲i+3.6pp (6/24) · p-0.8pp cap82.8 net-114/med-4.4 |
| dead | (°▼i-18.4pp (0/7) · p+2.7pp cap62.0 net-92/med-3.5) | (°▼i-23.0pp (0/2) · p-19.7pp cap— net+8/med+4.0) |
| asia | (°▼i-18.7pp (1/18) · p-14.3pp cap140.0 net-424/med-20.4) | (°▼i-2.4pp (4/19) · p+13.4pp cap102.8 net+268/med+19.3) |

- backtest payoff: right +1006 / wrong -2790 / net -1784 pts; median per fire -23.75 (n=58)
- backtest best call: 2026-07-31 10:15 +476.0pts remaining (episode 521.8pts, major)
- backtest worst false alarm: 2026-07-29 13:54 -255.0pts adverse
- forward payoff: right +2103 / wrong -1598 / net +505 pts; median per fire -0.70 (n=75)
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
| whole | ·i-1.9pp (40/204) · p+0.9pp cap180.0 net+1513/med+6.5 | ▲i+2.0pp (64/260) · p-2.5pp cap85.8 net-340/med-0.2 |
| london | ▼i-15.3pp (4/38) · p-2.0pp cap98.9 net-152/med+12.8 | ▲i+4.3pp (22/71) · p-3.4pp cap102.5 net-248/med+5.3 |
| overlap | (°▼i-7.9pp (0/20) · p+2.4pp cap185.4 net+387/med+17.1) | (°▼i-8.8pp (0/10) · p-24.9pp cap164.5 net+189/med+32.9) |
| ny_only | ▼i-4.7pp (7/49) · p+25.7pp cap260.5 net+2978/med+38.3 | ▼i-5.5pp (7/44) · p+0.0pp cap128.4 net+305/med-1.1 |
| dead | ·i-1.3pp (6/35) · p-5.9pp cap263.2 net-1043/med+14.8 | ▲i+10.3pp (12/36) · p+13.6pp cap80.4 net-336/med-5.8 |
| asia | ▲i+12.8pp (23/62) · p-8.6pp cap147.6 net-656/med-11.6 | ·i-0.3pp (23/99) · p-6.2pp cap77.7 net-250/med-0.6 |

- backtest payoff: right +10830 / wrong -9317 / net +1513 pts; median per fire +6.45 (n=204)
- backtest best call: 2026-07-30 06:41 +804.0pts remaining (episode 832.8pts, major)
- backtest worst false alarm: 2026-07-29 19:16 -700.8pts adverse
- forward payoff: right +6256 / wrong -6596 / net -340 pts; median per fire -0.25 (n=260)
- forward best call: 2026-08-21 11:30 +297.2pts remaining (episode 309.6pts, major)
- forward worst false alarm: 2026-08-19 12:53 -316.2pts adverse
- earliness (backtest): median 103.0 pts of move remaining at fire (n=16)

### H20 — 1 signal
*A wide-bar close-through of a session extreme (the same conditioned wide-bar class the retest anchor fires on; resolution = the close beyond the level, not a rejection back inside) initiates continuation in the break direction.*
Grading: directional. Latest review: rows (recommendation).

**S0-H20** — session × window grid (cells as in the matrix):

| session | backtest | forward |
|---|---|---|
| whole | ▼i-10.5pp (1/46) · p+8.5pp cap277.1 [cls 39.3%/12.7%i] net+1398/med+2.9 | ▼i-11.7pp (2/52) · p+10.5pp cap85.4 [cls 37.6%/15.5%i] net-652/med-11.3 |
| london | (°▲i+13.5pp (1/3) · p-38.7pp cap— [cls 38.7%/19.8%i] net-182/med-90.2) | (°▼i-13.9pp (1/11) · p-8.4pp cap97.6 [cls 35.7%/23.0%i] net-424/med-23.1) |
| overlap | (°▼i-6.8pp (0/34) · p+17.3pp cap277.1 [cls 47.4%/6.8%i] net+1975/med+63.9) | (°▼i-5.2pp (0/15) · p-2.1pp cap77.4 [cls 48.8%/5.2%i] net-645/med-43.5) |
| ny_only | (°▼i-6.9pp (0/2) · p-32.6pp cap— [cls 32.6%/6.9%i] net+16/med+7.9) | — |
| dead | (°▼i-13.5pp (0/4) · p-23.8pp cap— [cls 23.8%/13.5%i] net-155/med-45.4) | (°▲i+8.3pp (1/5) · p+1.7pp cap88.8 [cls 38.3%/11.7%i] net-144/med+12.4) |
| asia | (°▼i-18.0pp (0/3) · p-25.2pp cap— [cls 25.2%/18.0%i] net-256/med-75.9) | ▼i-21.2pp (0/21) · p+34.3pp cap79.8 [cls 27.6%/21.2%i] net+561/med+21.1 |

- backtest payoff: right +3786 / wrong -2388 / net +1398 pts; median per fire +2.90 (n=46)
- backtest best call: 2026-07-31 09:07 +2.0pts remaining (episode 98.0pts)
- backtest worst false alarm: 2026-07-31 13:34 -574.3pts adverse
- forward payoff: right +1263 / wrong -1916 / net -652 pts; median per fire -11.30 (n=52)
- forward best call: 2026-08-26 22:01 +81.5pts remaining (episode 81.5pts)
- forward worst false alarm: 2026-08-19 14:12 -233.2pts adverse
- earliness (backtest): median 2.0 pts of move remaining at fire (n=1)


---

# us30 (us30fut) — CANONICAL

Store span (1M, close ts): 2026-07-19 22:02:00+00:00 → 2026-08-31 18:48:00+00:00. Volume type: real futures volume (register 40 first-sync sanity; canonical verdict at this instrument's validation evening).

## Summary Matrix (page 1)

Engine `79c2cdd41` — OBSERVATIONAL signal scoreboard - move-detection, not trading; no fills exist here by construction; never validation (docs/hypothesis_lifecycle.md stage 4)

**Review labels are RECOMMENDATIONS — none actioned, review pending operator familiarity.** Cells: marker + precision LIFT vs that context's OWN chance rate, (hits/fires), payoff net/median points (directional rows; either-direction rows have no payoff by construction). ▲/▼ = beyond ±2pp of chance, · = within. (°…) = small-n (fires<20 or episodes<10): dimmed, excluded from any future label arithmetic. Read READING_GUIDE.md first; full detail in hypothesis_performance.json.

| H | label | backtest whole | backtest london | forward whole | forward london |
|---|---|---|---|---|---|
| *context* | | 110 ep; chance 24.0%dir/44.6%either | 36 ep; chance 36.6%dir/66.3%either | 116 ep; chance 24.5%dir/45.5%either | 36 ep; chance 37.2%dir/67.5%either |
| S0-H1 | keep-watching | ·i+1.2pp (11/49) · p+10.7pp cap154.0 net-83/med-8.0 | (°▲i+10.8pp (6/17) · p-1.3pp cap104.0 net-113/med-17.5) | ▲i+5.8pp (39/140) · p+3.4pp cap60.5 net-680/med+0.8 | ▲i+3.1pp (12/46) · p-8.9pp cap66.0 net-1361/med-20.0 |
| S1-H1 | keep-watching | (°▼i-21.2pp (0/2) · p-24.0pp cap— net-18/med-9.2) | (°▼i-24.5pp (0/1) · p-36.6pp cap— net-50/med-50.0) | (°▲i+5.7pp (5/18) · p+3.3pp cap59.5 net-404/med-7.8) | (°▲i+27.0pp (3/6) · p-37.2pp cap— net-612/med-81.8) |
| S0-H2 | promote-candidate | ▼i-7.0pp (40/281) · p+2.3pp cap133.2 net-2432/med-4.0 | ·i-1.9pp (14/62) · p-1.1pp cap116.2 net-337/med-20.0 | ▼i-5.1pp (80/470) · p+0.8pp cap66.0 net+200/med-0.5 | ▼i-9.0pp (17/121) · p+8.3pp cap79.0 net+1306/med+6.0 |
| S1-H2 | promote-candidate | ▼i-4.8pp (36/220) · p+3.7pp cap134.5 net-505/med-2.8 | ·i-0.5pp (12/50) · p+1.4pp cap119.0 net-218/med-18.0 | ▼i-2.2pp (67/337) · p-1.4pp cap66.5 net-268/med-1.0 | ·i-0.6pp (17/76) · p+1.0pp cap82.0 net+479/med+0.0 |
| S0-H3 | keep-watching | (°▲i+3.8pp (1/4) · p+1.0pp cap81.0 net+59/med+13.2) | (°▲i+25.5pp (1/2) · p-36.6pp cap— net-22/med-11.0) | (°▼i-22.1pp (0/6) · p+25.5pp cap57.0 net+114/med+36.8) | (°▼i-23.0pp (0/1) · p-37.2pp cap— net-52/med-52.5) |
| S0-H4 | keep-watching | (°▲i+17.3pp (5/13) · p+14.5pp cap83.0 net+194/med+15.0) | (°▼i-24.5pp (0/7) · p+34.8pp cap83.0 net+392/med+71.0) | — | — |
| S0-H5 | keep-watching | (°▼i-21.2pp (0/1) · p-24.0pp cap— net-135/med-135.0) | (°▼i-24.5pp (0/1) · p-36.6pp cap— net-135/med-135.0) | (°▼i-22.1pp (0/1) · p+75.5pp cap215.0 net+24/med+24.0) | (°▼i-23.0pp (0/1) · p+62.8pp cap215.0 net+24/med+24.0) |
| S0-H6 | keep-watching | ▼i-9.8pp (3/52) · p-21.4pp cap175.0 [cls 40.6%/15.6%i] net-1151/med-25.2 | ▼i-7.4pp (3/24) · p-28.4pp cap164.5 [cls 40.9%/19.9%i] net-664/med-30.0 | ▲i+10.3pp (22/83) · p-4.9pp cap100.5 [cls 41.0%/16.2%i] net-475/med-2.0 | ·i+1.6pp (8/37) · p+9.5pp cap88.5 [cls 41.9%/20.0%i] net-214/med+7.5 |
| S0-H7 | keep-watching | ▲i+5.6pp (11/41) · p-2.0pp cap111.0 net+205/med-9.0 | (°▲i+6.7pp (5/16) · p-5.4pp cap111.0 net-161/med-7.0) | ▲i+2.0pp (19/79) · p+0.8pp cap70.0 net+243/med-0.5 | ▲i+3.1pp (6/23) · p-11.1pp cap158.0 net-200/med-22.5 |
| S0-H7 (either-dir) | keep-watching | ·i+0.0pp (16/41) · p-3.1pp cap66.5 | (°▼i-12.7pp (5/16) · p+2.5pp cap60.5) | ▼i-7.1pp (27/79) · p+10.2pp cap26.5 | ▼i-14.4pp (7/23) · p+6.4pp cap25.5 |
| S0-H8 | keep-watching | ▼i-13.4pp (72/281) · p+7.7pp cap76.0 | ▼i-5.2pp (24/62) · p+6.3pp cap60.5 | ▼i-7.3pp (160/470) · p-1.5pp cap45.5 | ▼i-7.6pp (45/121) · p+1.9pp cap60.0 |
| S0-H9 | keep-watching | ▼i-13.7pp (3/40) · p-1.5pp cap66.0 net-353/med-14.7 | (°▼i-24.5pp (0/3) · p-3.3pp cap52.0 net-198/med-61.5) | ▼i-8.8pp (6/45) · p-4.5pp cap99.0 net-369/med-17.8 | (°▼i-4.2pp (3/16) · p+6.6pp cap113.5 net+36/med-7.5) |
| S1-H9 | keep-watching | (°▼i-21.2pp (0/9) · p-1.8pp cap273.0 net+460/med+1.5) | (°▼i-24.5pp (0/1) · p-36.6pp cap— net-38/med-38.0) | ▼i-13.4pp (2/23) · p-7.1pp cap100.8 net-315/med-16.0 | (°▲i+2.0pp (2/8) · p-12.2pp cap169.5 net-305/med-84.8) |
| S0-H10 | deprioritize | ·i-1.7pp (30/154) · p+0.0pp cap71.0 net+1774/med+11.0 | ▼i-19.5pp (2/40) · p+3.4pp cap116.0 net+1480/med+27.5 | ▼i-6.8pp (44/288) · p+1.5pp cap60.5 net-54/med-3.0 | ▼i-5.4pp (15/85) · p+5.2pp cap74.8 net-454/med-12.0 |
| S0-H11 | keep-watching | ·i-0.6pp (85/413) · p+3.4pp cap98.0 net+1254/med+3.0 | ▼i-5.5pp (31/163) · p+0.8pp cap91.0 net-404/med+5.0 | ·i-0.6pp (108/502) · p+0.4pp cap75.0 net+206/med-4.5 | ▼i-4.5pp (33/178) · p+0.4pp cap81.0 net+862/med-0.2 |
| S1-H11 | keep-watching | ▲i+6.8pp (53/189) · p+0.9pp cap167.0 net+1560/med+0.5 | (°▼i-15.4pp (1/11) · p+8.9pp cap194.5 net+136/med-24.5) | ▼i-4.1pp (66/367) · p+0.8pp cap80.0 net-345/med+1.5 | ·i+1.1pp (33/137) · p-5.1pp cap79.0 net+1424/med+8.5 |
| S0-H12 | keep-watching | — | — | — | — |
| S0-H13 | keep-watching | (°▲i+78.8pp (1/1) · p-24.0pp cap— net-206/med-206.0) | (°▲i+75.5pp (1/1) · p-36.6pp cap— net-206/med-206.0) | (°▼i-22.1pp (0/3) · p+42.2pp cap151.2 net+138/med+70.5) | (°▼i-23.0pp (0/1) · p-37.2pp cap— net-58/med-58.0) |
| S0-H14 | keep-watching | ▲i+3.8pp (37/148) · p+2.4pp cap76.0 net+2606/med+12.5 | ▼i-18.1pp (3/47) · p+10.2pp cap113.8 net+1414/med+12.5 | ▼i-6.9pp (39/256) · p+7.9pp cap67.5 net+1358/med-0.8 | ▼i-3.5pp (15/77) · p+7.0pp cap74.8 net+586/med-7.0 |
| S0-H15 | keep-watching | — | — | — | — |
| S0-H16 | keep-watching | (°▼i-21.2pp (0/10) · p+36.0pp cap98.2 net+522/med+37.5) | — | (°▼i-22.1pp (0/12) · p+17.2pp cap70.0 net+276/med+32.5) | — |
| S0-H17 | rows | ▼i-2.0pp (5/26) · p+2.9pp cap119.5 net-167/med-10.5 | (°▲i+5.5pp (3/10) · p-6.6pp cap157.5 net+113/med+12.2) | ▲i+7.0pp (25/86) · p-3.6pp cap50.5 net-716/med-6.5 | ▲i+3.9pp (7/26) · p-18.0pp cap71.5 net-787/med-38.5 |
| S0-H18 | rows | ▲i+2.7pp (16/67) · p+2.9pp cap102.5 net+355/med+2.5 | ·i+0.5pp (7/28) · p+2.7pp cap87.5 net+681/med+46.2 | ·i+0.7pp (18/79) · p-3.0pp cap74.0 net-470/med-7.5 | ▲i+2.0pp (7/28) · p-8.6pp cap67.5 net-73/med+1.2 |
| S0-H19 | rows | ▼i-11.9pp (16/172) · p+9.1pp cap131.4 net+2236/med+3.2 | ▼i-5.7pp (6/32) · p+4.0pp cap141.0 net+708/med+34.0 | ▼i-4.1pp (55/306) · p-1.3pp cap77.5 net+1200/med+2.0 | ·i-1.7pp (16/75) · p-2.5pp cap89.2 net-214/med+6.0 |
| S0-H20 | rows | ▼i-12.2pp (2/58) · p-11.3pp cap114.0 [cls 40.6%/15.6%i] net+27/med+18.2 | ▼i-14.5pp (2/37) · p-16.6pp cap87.5 [cls 40.9%/19.9%i] net-532/med+4.5 | ▼i-13.0pp (2/63) · p+1.9pp cap113.5 [cls 41.0%/16.2%i] net-842/med-34.5 | ▼i-15.7pp (2/46) · p+10.3pp cap115.8 [cls 41.9%/20.0%i] net-214/med-12.5 |
| **union coverage** | | 40.0% (44/110) | 33.3% (12/36) | 90.5% (105/116) | 88.9% (32/36) |

Not graded:  — see register entries.

## Hypothesis Cards (page 2)

### H1 — 2 signals
*A climactic bar — extreme volume on a wide spread late in an extended move — marks exhaustion, and price then reverses against the climax direction.*
Grading: directional. Latest review: keep-watching (recommendation).

- Question **Q1-H1**: see the register entry (status there is authoritative).
**S0-H1** — session × window grid (cells as in the matrix):

| session | backtest | forward |
|---|---|---|
| whole | ·i+1.2pp (11/49) · p+10.7pp cap154.0 net-83/med-8.0 | ▲i+5.8pp (39/140) · p+3.4pp cap60.5 net-680/med+0.8 |
| london | (°▲i+10.8pp (6/17) · p-1.3pp cap104.0 net-113/med-17.5) | ▲i+3.1pp (12/46) · p-8.9pp cap66.0 net-1361/med-20.0 |
| overlap | — | (°▼i-13.7pp (0/2) · p+19.5pp cap186.5 net+119/med+59.5) |
| ny_only | (°▼i-3.8pp (2/13) · p+40.3pp cap253.5 net-62/med-15.5) | (°▲i+8.9pp (4/14) · p-3.4pp cap143.5 net+42/med+0.5) |
| dead | (°▲i+28.3pp (3/7) · p-7.2pp cap— net-157/med-8.0) | ▲i+21.6pp (12/27) · p+14.7pp cap61.5 net+388/med+16.0 |
| asia | (°▼i-25.0pp (0/12) · p+9.4pp cap91.2 net+248/med+27.0) | ▼i-3.5pp (11/51) · p+8.0pp cap40.2 net+133/med+2.0 |

- backtest payoff: right +1958 / wrong -2041 / net -83 pts; median per fire -8.00 (n=49)
- backtest best call: 2026-07-29 16:24 +398.0pts remaining (episode 602.0pts, major)
- backtest worst false alarm: 2026-07-29 19:22 -450.0pts adverse
- forward payoff: right +2623 / wrong -3303 / net -680 pts; median per fire +0.75 (n=140)
- forward best call: 2026-08-20 09:19 +408.0pts remaining (episode 415.5pts, major)
- forward worst false alarm: 2026-08-20 11:25 -261.5pts adverse
- earliness (backtest): median 128.0 pts of move remaining at fire (n=10)

**S1-H1** — session × window grid (cells as in the matrix):

| session | backtest | forward |
|---|---|---|
| whole | (°▼i-21.2pp (0/2) · p-24.0pp cap— net-18/med-9.2) | (°▲i+5.7pp (5/18) · p+3.3pp cap59.5 net-404/med-7.8) |
| london | (°▼i-24.5pp (0/1) · p-36.6pp cap— net-50/med-50.0) | (°▲i+27.0pp (3/6) · p-37.2pp cap— net-612/med-81.8) |
| overlap | — | — |
| ny_only | — | — |
| dead | — | (°▼i-6.1pp (1/6) · p+42.5pp cap59.5 net+185/med+42.2) |
| asia | (°▼i-25.0pp (0/1) · p-23.9pp cap— net+32/med+31.5) | (°▼i-8.4pp (1/6) · p+6.0pp cap54.5 net+23/med+1.5) |

- backtest payoff: right +32 / wrong -50 / net -18 pts; median per fire -9.25 (n=2)
- backtest worst false alarm: 2026-07-29 12:17 -67.0pts adverse
- forward payoff: right +325 / wrong -729 / net -404 pts; median per fire -7.75 (n=18)
- forward best call: 2026-08-30 23:48 +62.0pts remaining (episode 62.0pts)
- forward worst false alarm: 2026-08-20 11:47 -199.5pts adverse

### H2 — 2 signals
*A failed probe beyond a prior extreme — an upthrust above or spring below that closes back inside — reverses against the probe.*
Grading: directional. Latest review: promote-candidate (recommendation).

**S0-H2** — session × window grid (cells as in the matrix):

| session | backtest | forward |
|---|---|---|
| whole | ▼i-7.0pp (40/281) · p+2.3pp cap133.2 net-2432/med-4.0 | ▼i-5.1pp (80/470) · p+0.8pp cap66.0 net+200/med-0.5 |
| london | ·i-1.9pp (14/62) · p-1.1pp cap116.2 net-337/med-20.0 | ▼i-9.0pp (17/121) · p+8.3pp cap79.0 net+1306/med+6.0 |
| overlap | (°▼i-11.4pp (0/22) · p+3.6pp cap177.5 net-1080/med-77.8) | (°▼i-5.7pp (2/25) · p+5.5pp cap176.0 net-462/med-74.0) |
| ny_only | ▼i-15.9pp (2/60) · p+23.2pp cap224.8 net-1257/med-11.1 | ▼i-6.0pp (10/73) · p-5.0pp cap121.5 net-643/med-5.0 |
| dead | ·i+0.0pp (6/41) · p+2.6pp cap100.8 net-18/med-2.6 | ·i-1.5pp (19/89) · p+9.4pp cap60.5 net+378/med+4.5 |
| asia | ▼i-6.2pp (18/96) · p-5.1pp cap82.5 net+261/med+1.2 | ▼i-5.3pp (32/162) · p-5.1pp cap47.8 net-378/med-0.8 |

- backtest payoff: right +10496 / wrong -12928 / net -2432 pts; median per fire -4.00 (n=281)
- backtest best call: 2026-07-29 06:34 +888.5pts remaining (episode 952.0pts, major)
- backtest worst false alarm: 2026-07-29 18:55 -695.0pts adverse
- forward payoff: right +9291 / wrong -9091 / net +200 pts; median per fire -0.50 (n=470)
- forward best call: 2026-08-20 09:10 +401.0pts remaining (episode 415.5pts, major)
- forward worst false alarm: 2026-08-19 12:55 -270.0pts adverse
- earliness (backtest): median 105.2 pts of move remaining at fire (n=22)

**S1-H2** — session × window grid (cells as in the matrix):

| session | backtest | forward |
|---|---|---|
| whole | ▼i-4.8pp (36/220) · p+3.7pp cap134.5 net-505/med-2.8 | ▼i-2.2pp (67/337) · p-1.4pp cap66.5 net-268/med-1.0 |
| london | ·i-0.5pp (12/50) · p+1.4pp cap119.0 net-218/med-18.0 | ·i-0.6pp (17/76) · p+1.0pp cap82.0 net+479/med+0.0 |
| overlap | (°▼i-11.4pp (0/17) · p-3.4pp cap182.5 net-983/med-92.0) | (°▼i-4.6pp (2/22) · p+5.9pp cap173.0 net-364/med-74.2) |
| ny_only | ▼i-14.3pp (2/41) · p+32.8pp cap239.5 net+169/med-15.0 | ▼i-2.5pp (10/58) · p-5.3pp cap99.5 net-417/med-4.0 |
| dead | ▲i+4.8pp (6/31) · p+2.5pp cap99.5 net-162/med-5.0 | ·i-1.8pp (13/62) · p+7.0pp cap67.5 net+325/med+2.8 |
| asia | ▼i-5.2pp (16/81) · p-5.4pp cap83.0 net+689/med+6.0 | ▼i-4.1pp (25/119) · p-2.9pp cap47.0 net-290/med-1.0 |

- backtest payoff: right +8589 / wrong -9094 / net -505 pts; median per fire -2.80 (n=220)
- backtest best call: 2026-07-29 06:34 +888.5pts remaining (episode 952.0pts, major)
- backtest worst false alarm: 2026-07-29 18:55 -695.0pts adverse
- forward payoff: right +6102 / wrong -6370 / net -268 pts; median per fire -1.00 (n=337)
- forward best call: 2026-08-20 09:10 +401.0pts remaining (episode 415.5pts, major)
- forward worst false alarm: 2026-08-20 11:54 -201.0pts adverse
- earliness (backtest): median 106.0 pts of move remaining at fire (n=21)

### H3 — 1 signal
*Repeated absorption — high effort with no result — at a price level precedes a breakout through that level.*
Grading: directional. Latest review: keep-watching (recommendation).

**S0-H3** — session × window grid (cells as in the matrix):

| session | backtest | forward |
|---|---|---|
| whole | (°▲i+3.8pp (1/4) · p+1.0pp cap81.0 net+59/med+13.2) | (°▼i-22.1pp (0/6) · p+25.5pp cap57.0 net+114/med+36.8) |
| london | (°▲i+25.5pp (1/2) · p-36.6pp cap— net-22/med-11.0) | (°▼i-23.0pp (0/1) · p-37.2pp cap— net-52/med-52.5) |
| overlap | — | — |
| ny_only | — | (°▼i-19.7pp (0/2) · p+39.5pp cap59.5 net+88/med+44.2) |
| dead | — | — |
| asia | (°▼i-25.0pp (0/2) · p+26.1pp cap81.0 net+81/med+40.5) | (°▼i-25.1pp (0/3) · p+39.4pp cap52.8 net+78/med+34.5) |

- backtest payoff: right +99 / wrong -40 / net +59 pts; median per fire +13.25 (n=4)
- backtest best call: 2026-07-30 09:10 +122.0pts remaining (episode 205.5pts)
- backtest worst false alarm: 2026-07-30 09:10 -83.5pts adverse
- forward payoff: right +180 / wrong -66 / net +114 pts; median per fire +36.75 (n=6)
- forward worst false alarm: 2026-08-26 07:41 -64.0pts adverse
- earliness (backtest): median 122.0 pts of move remaining at fire (n=1)

### H4 — 1 signal
*In an established trend, a quiet (low-volume) pullback resolves with trend resumption.*
Grading: directional. Latest review: keep-watching (recommendation).

**S0-H4** — session × window grid (cells as in the matrix):

| session | backtest | forward |
|---|---|---|
| whole | (°▲i+17.3pp (5/13) · p+14.5pp cap83.0 net+194/med+15.0) | — |
| london | (°▼i-24.5pp (0/7) · p+34.8pp cap83.0 net+392/med+71.0) | — |
| overlap | (°▼i-11.4pp (0/1) · p-32.8pp cap— net-166/med-165.5) | — |
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
| whole | (°▼i-21.2pp (0/1) · p-24.0pp cap— net-135/med-135.0) | (°▼i-22.1pp (0/1) · p+75.5pp cap215.0 net+24/med+24.0) |
| london | (°▼i-24.5pp (0/1) · p-36.6pp cap— net-135/med-135.0) | (°▼i-23.0pp (0/1) · p+62.8pp cap215.0 net+24/med+24.0) |
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
| whole | ▼i-9.8pp (3/52) · p-21.4pp cap175.0 [cls 40.6%/15.6%i] net-1151/med-25.2 | ▲i+10.3pp (22/83) · p-4.9pp cap100.5 [cls 41.0%/16.2%i] net-475/med-2.0 |
| london | ▼i-7.4pp (3/24) · p-28.4pp cap164.5 [cls 40.9%/19.9%i] net-664/med-30.0 | ·i+1.6pp (8/37) · p+9.5pp cap88.5 [cls 41.9%/20.0%i] net-214/med+7.5 |
| overlap | (°▼i-9.2pp (0/18) · p-19.1pp cap195.5 [cls 41.3%/9.2%i] net+234/med+6.8) | (°▲i+20.9pp (13/42) · p-17.1pp cap155.0 [cls 43.3%/10.1%i] net-216/med-9.2) |
| ny_only | (°▼i-5.4pp (0/6) · p+7.7pp cap329.0 [cls 42.3%/5.4%i] net-856/med-92.0) | — |
| dead | (°▼i-7.4pp (0/3) · p-11.8pp cap— [cls 11.8%/7.4%i] net+58/med+5.5) | — |
| asia | (°▼i-20.7pp (0/1) · p-40.2pp cap— [cls 40.2%/20.7%i] net+77/med+77.0) | (°▲i+10.2pp (1/4) · p-41.2pp cap— [cls 41.2%/14.8%i] net-46/med-3.2) |

- backtest payoff: right +1398 / wrong -2549 / net -1151 pts; median per fire -25.25 (n=52)
- backtest best call: 2026-07-28 12:23 +197.5pts remaining (episode 226.5pts, major)
- backtest worst false alarm: 2026-07-28 15:11 -288.5pts adverse
- forward payoff: right +2161 / wrong -2636 / net -475 pts; median per fire -2.00 (n=83)
- forward best call: 2026-08-20 12:09 +137.5pts remaining (episode 184.5pts, major)
- forward worst false alarm: 2026-08-31 13:29 -311.9pts adverse
- earliness (backtest): median 27.5 pts of move remaining at fire (n=3)

### H7 — 1 signal
*Quiet decline at a session extreme is disguised accumulation: effortless (low-volume) weakness reverses UP once selling fails to attract participation (mirror: quiet advance at a high reverses down).*
Grading: directional + either-direction (dual). Latest review: keep-watching (recommendation).

- Question **Q1-H7**: see the register entry (status there is authoritative).
**S0-H7** — session × window grid (cells as in the matrix):

| session | backtest | forward |
|---|---|---|
| whole | ▲i+5.6pp (11/41) · p-2.0pp cap111.0 net+205/med-9.0 | ▲i+2.0pp (19/79) · p+0.8pp cap70.0 net+243/med-0.5 |
| london | (°▲i+6.7pp (5/16) · p-5.4pp cap111.0 net-161/med-7.0) | ▲i+3.1pp (6/23) · p-11.1pp cap158.0 net-200/med-22.5 |
| overlap | (°▼i-11.4pp (0/3) · p+33.9pp cap287.0 net+471/med+272.0) | (°▲i+11.3pp (2/8) · p+7.0pp cap198.5 net+104/med-18.5) |
| ny_only | (°▼i-19.2pp (0/4) · p-13.5pp cap— net-21/med-5.0) | (°·i+1.7pp (3/14) · p-3.4pp cap109.0 net+316/med+16.0) |
| dead | (°▲i+10.4pp (1/4) · p-7.2pp cap— net-1/med-2.0) | (°▲i+43.9pp (2/3) · p-7.5pp cap— net+13/med-0.5) |
| asia | (°▲i+10.7pp (5/14) · p-9.6pp cap76.0 net-84/med-13.8) | ▼i-5.7pp (6/31) · p+5.0pp cap44.5 net+10/med+5.5 |

- backtest payoff: right +1609 / wrong -1404 / net +205 pts; median per fire -9.00 (n=41)
- backtest best call: 2026-07-31 09:51 +528.0pts remaining (episode 572.5pts, major)
- backtest worst false alarm: 2026-07-28 10:48 -242.0pts adverse
- forward payoff: right +2070 / wrong -1826 / net +243 pts; median per fire -0.50 (n=79)
- forward best call: 2026-08-19 13:56 +166.0pts remaining (episode 236.0pts)
- forward worst false alarm: 2026-08-19 12:12 -262.0pts adverse
- earliness (backtest): median 110.5 pts of move remaining at fire (n=9)

**S0-H7 (either-dir)** — session × window grid (cells as in the matrix):

| session | backtest | forward |
|---|---|---|
| whole | ·i+0.0pp (16/41) · p-3.1pp cap66.5 | ▼i-7.1pp (27/79) · p+10.2pp cap26.5 |
| london | (°▼i-12.7pp (5/16) · p+2.5pp cap60.5) | ▼i-14.4pp (7/23) · p+6.4pp cap25.5 |
| overlap | (°▼i-22.8pp (0/3) · p+6.2pp cap287.0) | (°▼i-2.4pp (2/8) · p+20.5pp cap102.0) |
| ny_only | (°▼i-10.3pp (1/4) · p-26.1pp cap—) | (°▲i+4.9pp (6/14) · p-13.2pp cap109.0) |
| dead | (°▲i+21.4pp (2/4) · p-14.4pp cap—) | (°▲i+58.6pp (3/3) · p-14.9pp cap—) |
| asia | (°▲i+11.3pp (8/14) · p-16.6pp cap37.0) | ▼i-15.5pp (9/31) · p+12.5pp cap22.5 |

- backtest payoff: n/a by construction (either-direction)
- backtest best call: 2026-07-31 09:51 +528.0pts remaining (episode 572.5pts, major)
- backtest worst false alarm: 2026-07-30 16:13 -170.0pts adverse
- forward payoff: n/a by construction (either-direction)
- forward best call: 2026-08-28 11:03 +222.5pts remaining (episode 232.0pts, major)
- forward worst false alarm: 2026-08-20 15:23 -98.0pts adverse
- earliness (backtest): median 85.0 pts of move remaining at fire (n=11)

### H8 — 1 signal
*Reversal-signature bar anatomy (upthrust/spring) predicts imminent range expansion irrespective of direction.*
Grading: either-direction. Latest review: keep-watching (recommendation).

**S0-H8** — session × window grid (cells as in the matrix):

| session | backtest | forward |
|---|---|---|
| whole | ▼i-13.4pp (72/281) · p+7.7pp cap76.0 | ▼i-7.3pp (160/470) · p-1.5pp cap45.5 |
| london | ▼i-5.2pp (24/62) · p+6.3pp cap60.5 | ▼i-7.6pp (45/121) · p+1.9pp cap60.0 |
| overlap | (°▼i-22.8pp (0/22) · p+21.3pp cap114.2) | (°▼i-15.4pp (3/25) · p+25.5pp cap76.0) |
| ny_only | ▼i-27.0pp (5/60) · p+37.2pp cap154.5 | ▼i-14.7pp (17/73) · p-6.6pp cap20.5 |
| dead | ▼i-11.5pp (7/41) · p+10.0pp cap10.5 | ·i+0.2pp (37/89) · p+7.6pp cap56.0 |
| asia | ▼i-8.3pp (36/96) · p-7.7pp cap47.2 | ▼i-8.7pp (58/162) · p-6.9pp cap23.0 |

- backtest payoff: n/a by construction (either-direction)
- backtest best call: 2026-07-29 06:34 +888.5pts remaining (episode 952.0pts, major)
- backtest worst false alarm: 2026-07-27 16:47 -152.0pts adverse
- forward payoff: n/a by construction (either-direction)
- forward best call: 2026-08-20 09:10 +401.0pts remaining (episode 415.5pts, major)
- forward worst false alarm: 2026-08-19 16:19 -145.5pts adverse
- earliness (backtest): median 99.2 pts of move remaining at fire (n=26)

### H9 — 2 signals
*Persistent lower-TF directional pressure that recruits expanding participation at the parent timeframe precedes continuation beyond what the parent label alone predicts; pressure without participation expansion does not.*
Grading: directional. Latest review: keep-watching (recommendation).

- Question **Q2-H9**: see the register entry (status there is authoritative).
**S0-H9** — session × window grid (cells as in the matrix):

| session | backtest | forward |
|---|---|---|
| whole | ▼i-13.7pp (3/40) · p-1.5pp cap66.0 net-353/med-14.7 | ▼i-8.8pp (6/45) · p-4.5pp cap99.0 net-369/med-17.8 |
| london | (°▼i-24.5pp (0/3) · p-3.3pp cap52.0 net-198/med-61.5) | (°▼i-4.2pp (3/16) · p+6.6pp cap113.5 net+36/med-7.5) |
| overlap | (°▼i-11.4pp (0/2) · p-32.8pp cap— net-19/med-9.5) | — |
| ny_only | (°▼i-9.2pp (1/10) · p-3.5pp cap464.5 net-196/med-66.5) | (°▼i-19.7pp (0/10) · p-10.5pp cap— net-100/med-13.0) |
| dead | (°▼i-14.6pp (0/7) · p-7.2pp cap— net+60/med+15.5) | (°▼i-22.8pp (0/4) · p+17.5pp cap88.0 net+8/med-3.5) |
| asia | (°▼i-13.9pp (2/18) · p+15.0pp cap66.0 net-1/med-11.2) | (°▼i-5.1pp (3/15) · p-20.6pp cap52.0 net-313/med-29.5) |

- backtest payoff: right +876 / wrong -1229 / net -353 pts; median per fire -14.70 (n=38)
- backtest best call: 2026-08-03 05:40 +463.0pts remaining (episode 472.0pts, major)
- backtest worst false alarm: 2026-08-03 17:15 -176.0pts adverse
- forward payoff: right +912 / wrong -1282 / net -369 pts; median per fire -17.75 (n=44)
- forward best call: 2026-08-28 12:10 +159.5pts remaining (episode 197.0pts, major)
- forward worst false alarm: 2026-08-18 07:00 -127.5pts adverse
- earliness (backtest): median 351.5 pts of move remaining at fire (n=2)

**S1-H9** — session × window grid (cells as in the matrix):

| session | backtest | forward |
|---|---|---|
| whole | (°▼i-21.2pp (0/9) · p-1.8pp cap273.0 net+460/med+1.5) | ▼i-13.4pp (2/23) · p-7.1pp cap100.8 net-315/med-16.0 |
| london | (°▼i-24.5pp (0/1) · p-36.6pp cap— net-38/med-38.0) | (°▲i+2.0pp (2/8) · p-12.2pp cap169.5 net-305/med-84.8) |
| overlap | — | — |
| ny_only | (°▼i-19.2pp (0/4) · p+11.5pp cap464.5 net+421/med+15.3) | (°▼i-19.7pp (0/6) · p-10.5pp cap— net-25/med-13.0) |
| dead | — | (°▼i-22.8pp (0/2) · p+42.5pp cap88.0 net+12/med+5.8) |
| asia | (°▼i-25.0pp (0/4) · p+1.1pp cap81.5 net+76/med+12.8) | (°▼i-25.1pp (0/7) · p-13.0pp cap52.0 net+4/med+5.0) |

- backtest payoff: right +601 / wrong -141 / net +460 pts; median per fire +1.50 (n=9)
- backtest worst false alarm: 2026-07-27 16:10 -84.0pts adverse
- forward payoff: right +449 / wrong -764 / net -315 pts; median per fire -16.00 (n=23)
- forward best call: 2026-08-18 07:00 +64.9pts remaining (episode 148.4pts, major)
- forward worst false alarm: 2026-08-18 07:00 -127.5pts adverse

### H10 — 1 signal
*In an established 1-minute trend, no-demand/no-supply prints in the trend's direction signal continuation.*
Grading: directional. Latest review: deprioritize (recommendation).

**S0-H10** — session × window grid (cells as in the matrix):

| session | backtest | forward |
|---|---|---|
| whole | ·i-1.7pp (30/154) · p+0.0pp cap71.0 net+1774/med+11.0 | ▼i-6.8pp (44/288) · p+1.5pp cap60.5 net-54/med-3.0 |
| london | ▼i-19.5pp (2/40) · p+3.4pp cap116.0 net+1480/med+27.5 | ▼i-5.4pp (15/85) · p+5.2pp cap74.8 net-454/med-12.0 |
| overlap | (°▼i-11.4pp (0/5) · p-32.8pp cap— net+36/med+33.0) | (°▲i+26.3pp (6/15) · p-30.5pp cap— net+20/med+2.5) |
| ny_only | ▼i-3.8pp (4/26) · p+1.9pp cap80.9 net-348/med+48.8 | ▼i-7.2pp (8/64) · p-5.8pp cap84.0 net-269/med+1.0 |
| dead | ▲i+15.4pp (6/20) · p-7.2pp cap— net-74/med-5.7 | ▼i-10.9pp (5/42) · p-0.4pp cap41.5 net-356/med-10.8 |
| asia | ▲i+3.6pp (18/63) · p+3.1pp cap50.5 net+680/med+8.0 | ▼i-12.9pp (10/82) · p+12.9pp cap52.0 net+1005/med+8.0 |

- backtest payoff: right +4228 / wrong -2454 / net +1774 pts; median per fire +11.00 (n=154)
- backtest best call: 2026-07-29 06:18 +859.5pts remaining (episode 952.0pts, major)
- backtest worst false alarm: 2026-08-03 17:10 -197.0pts adverse
- forward payoff: right +4830 / wrong -4884 / net -54 pts; median per fire -3.00 (n=288)
- forward best call: 2026-08-31 09:59 +350.0pts remaining (episode 340.0pts, major)
- forward worst false alarm: 2026-08-27 12:57 -190.5pts adverse
- earliness (backtest): median 87.5 pts of move remaining at fire (n=11)

### H11 — 2 signals
*Price entering a low-volume price zone traverses it faster than baseline; entering a high-volume node it stalls or reverses at above-baseline rates.*
Grading: directional. Latest review: keep-watching (recommendation).

- Question **Q1-H11**: see the register entry (status there is authoritative).
- Question **Q2-H11**: see the register entry (status there is authoritative).
**S0-H11** — session × window grid (cells as in the matrix):

| session | backtest | forward |
|---|---|---|
| whole | ·i-0.6pp (85/413) · p+3.4pp cap98.0 net+1254/med+3.0 | ·i-0.6pp (108/502) · p+0.4pp cap75.0 net+206/med-4.5 |
| london | ▼i-5.5pp (31/163) · p+0.8pp cap91.0 net-404/med+5.0 | ▼i-4.5pp (33/178) · p+0.4pp cap81.0 net+862/med-0.2 |
| overlap | (°▼i-7.6pp (1/26) · p+21.0pp cap261.2 net+491/med+4.0) | (°▼i-8.4pp (3/57) · p-2.4pp cap121.5 net+297/med-3.5) |
| ny_only | ▲i+7.0pp (11/42) · p-1.6pp cap239.5 net+1037/med+15.2 | ▲i+10.1pp (25/84) · p+2.6pp cap113.5 net-95/med-5.5 |
| dead | ▼i-6.6pp (4/50) · p+14.8pp cap99.5 net+478/med+1.2 | ·i-1.1pp (10/46) · p-5.3pp cap74.6 net-283/med-6.5 |
| asia | ▲i+3.8pp (38/132) · p-7.2pp cap62.5 net-348/med+2.0 | ·i+1.9pp (37/137) · p-5.4pp cap39.8 net-576/med-4.5 |

- backtest payoff: right +12694 / wrong -11440 / net +1254 pts; median per fire +3.00 (n=413)
- backtest best call: 2026-07-29 06:20 +858.0pts remaining (episode 952.0pts, major)
- backtest worst false alarm: 2026-07-31 13:24 -492.5pts adverse
- forward payoff: right +10231 / wrong -10025 / net +206 pts; median per fire -4.50 (n=501)
- forward best call: 2026-08-19 09:21 +393.5pts remaining (episode 377.5pts, major)
- forward worst false alarm: 2026-08-19 12:55 -270.0pts adverse
- earliness (backtest): median 90.5 pts of move remaining at fire (n=23)

**S1-H11** — session × window grid (cells as in the matrix):

| session | backtest | forward |
|---|---|---|
| whole | ▲i+6.8pp (53/189) · p+0.9pp cap167.0 net+1560/med+0.5 | ▼i-4.1pp (66/367) · p+0.8pp cap80.0 net-345/med+1.5 |
| london | (°▼i-15.4pp (1/11) · p+8.9pp cap194.5 net+136/med-24.5) | ·i+1.1pp (33/137) · p-5.1pp cap79.0 net+1424/med+8.5 |
| overlap | (°▲i+23.1pp (10/29) · p+12.0pp cap250.5 net+278/med+23.0) | (°▲i+10.4pp (14/58) · p+5.7pp cap130.0 net-916/med-12.5) |
| ny_only | ▼i-4.3pp (7/47) · p+14.2pp cap181.4 net+1460/med+17.0 | ▼i-6.6pp (11/84) · p-4.5pp cap110.0 net-591/med-4.0 |
| dead | ▲i+26.3pp (9/22) · p+11.0pp cap86.0 net+232/med+18.2 | ▼i-18.3pp (1/22) · p+1.6pp cap95.5 net+168/med+0.2 |
| asia | ▲i+7.5pp (26/80) · p-8.9pp cap66.2 net-546/med-6.2 | ▼i-14.5pp (7/66) · p+4.5pp cap38.5 net-431/med-6.5 |

- backtest payoff: right +9216 / wrong -7657 / net +1560 pts; median per fire +0.50 (n=189)
- backtest best call: 2026-07-28 04:46 +523.0pts remaining (episode 543.0pts, major)
- backtest worst false alarm: 2026-07-29 18:58 -665.0pts adverse
- forward payoff: right +9487 / wrong -9832 / net -345 pts; median per fire +1.50 (n=367)
- forward best call: 2026-08-20 09:30 +392.0pts remaining (episode 415.5pts, major)
- forward worst false alarm: 2026-08-28 14:28 -314.0pts adverse
- earliness (backtest): median 97.5 pts of move remaining at fire (n=8)

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
| whole | (°▲i+78.8pp (1/1) · p-24.0pp cap— net-206/med-206.0) | (°▼i-22.1pp (0/3) · p+42.2pp cap151.2 net+138/med+70.5) |
| london | (°▲i+75.5pp (1/1) · p-36.6pp cap— net-206/med-206.0) | (°▼i-23.0pp (0/1) · p-37.2pp cap— net-58/med-58.0) |
| overlap | — | (°▼i-13.7pp (0/1) · p+69.5pp cap177.5 net+70/med+70.5) |
| ny_only | — | (°▼i-19.7pp (0/1) · p+89.5pp cap125.0 net+125/med+125.0) |
| dead | — | — |
| asia | — | — |

- backtest payoff: right +0 / wrong -206 / net -206 pts; median per fire -206.00 (n=1)
- backtest best call: 2026-07-28 10:27 +-158.5pts remaining (episode 93.5pts)
- backtest worst false alarm: 2026-07-28 10:27 -252.0pts adverse
- forward payoff: right +196 / wrong -58 / net +138 pts; median per fire +70.50 (n=3)
- forward worst false alarm: 2026-08-31 12:13 -129.5pts adverse
- earliness (backtest): median -158.5 pts of move remaining at fire (n=1)

### H14 — 1 signal
*Counter-trend No Demand / No Supply prints in an established trend mark absorption and precede trend continuation.*
Grading: directional. Latest review: keep-watching (recommendation).

**S0-H14** — session × window grid (cells as in the matrix):

| session | backtest | forward |
|---|---|---|
| whole | ▲i+3.8pp (37/148) · p+2.4pp cap76.0 net+2606/med+12.5 | ▼i-6.9pp (39/256) · p+7.9pp cap67.5 net+1358/med-0.8 |
| london | ▼i-18.1pp (3/47) · p+10.2pp cap113.8 net+1414/med+12.5 | ▼i-3.5pp (15/77) · p+7.0pp cap74.8 net+586/med-7.0 |
| overlap | (°▼i-11.4pp (0/7) · p-32.8pp cap— net-40/med+17.0) | (°▲i+17.1pp (4/13) · p-30.5pp cap— net-348/med-12.0) |
| ny_only | ▼i-2.0pp (5/29) · p-6.6pp cap85.7 net+804/med+53.0 | ·i+1.1pp (11/53) · p+2.7pp cap118.4 net-89/med+1.0 |
| dead | (°▲i+38.0pp (10/19) · p-1.9pp cap104.9 net-80/med-14.4) | ▼i-19.8pp (1/33) · p+10.7pp cap38.2 net+47/med-2.5 |
| asia | ▲i+16.3pp (19/46) · p+6.5pp cap40.8 net+508/med+7.5 | ▼i-15.1pp (8/80) · p+17.7pp cap53.2 net+1163/med+10.8 |

- backtest payoff: right +4618 / wrong -2012 / net +2606 pts; median per fire +12.50 (n=148)
- backtest best call: 2026-08-03 05:18 +451.0pts remaining (episode 472.0pts, major)
- backtest worst false alarm: 2026-07-28 13:00 -258.0pts adverse
- forward payoff: right +5268 / wrong -3909 / net +1358 pts; median per fire -0.75 (n=256)
- forward best call: 2026-08-31 09:58 +350.0pts remaining (episode 340.0pts, major)
- forward worst false alarm: 2026-08-27 14:26 -222.0pts adverse
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
| whole | (°▼i-21.2pp (0/10) · p+36.0pp cap98.2 net+522/med+37.5) | (°▼i-22.1pp (0/12) · p+17.2pp cap70.0 net+276/med+32.5) |
| london | — | — |
| overlap | — | — |
| ny_only | (°▼i-19.2pp (0/10) · p+46.5pp cap98.2 net+522/med+37.5) | (°▼i-19.7pp (0/12) · p+31.2pp cap70.0 net+276/med+32.5) |
| dead | — | — |
| asia | — | — |

- backtest payoff: right +588 / wrong -66 / net +522 pts; median per fire +37.50 (n=10)
- backtest worst false alarm: 2026-07-28 19:30 -58.0pts adverse
- forward payoff: right +431 / wrong -154 / net +276 pts; median per fire +32.50 (n=12)
- forward worst false alarm: 2026-08-21 19:30 -73.0pts adverse

### H17 — 1 signal
*A climax reversal signal followed by absorption within five bars — effort meeting a quiet counter-party — marks a genuine exhaustion turn: the two-chapter story (exhaustion needs absorption to become reversal).*
Grading: directional. Latest review: rows (recommendation).

**S0-H17** — session × window grid (cells as in the matrix):

| session | backtest | forward |
|---|---|---|
| whole | ▼i-2.0pp (5/26) · p+2.9pp cap119.5 net-167/med-10.5 | ▲i+7.0pp (25/86) · p-3.6pp cap50.5 net-716/med-6.5 |
| london | (°▲i+5.5pp (3/10) · p-6.6pp cap157.5 net+113/med+12.2) | ▲i+3.9pp (7/26) · p-18.0pp cap71.5 net-787/med-38.5 |
| overlap | — | (°▼i-13.7pp (0/2) · p+19.5pp cap196.0 net+99/med+49.5) |
| ny_only | (°▲i+30.8pp (1/2) · p-13.5pp cap— net-281/med-140.5) | (°▲i+2.5pp (2/9) · p-10.5pp cap— net+7/med+16.5) |
| dead | (°▲i+10.4pp (1/4) · p-7.2pp cap— net-211/med-48.2) | (°▲i+27.2pp (8/16) · p-1.3pp cap63.5 net+150/med+2.2) |
| asia | (°▼i-25.0pp (0/10) · p+16.1pp cap75.8 net+212/med+33.2) | ·i-0.9pp (8/33) · p+6.0pp cap33.0 net-184/med-12.0 |

- backtest payoff: right +792 / wrong -958 / net -167 pts; median per fire -10.50 (n=26)
- backtest best call: 2026-07-29 16:25 +398.5pts remaining (episode 602.0pts, major)
- backtest worst false alarm: 2026-07-29 16:25 -203.5pts adverse
- forward payoff: right +1375 / wrong -2090 / net -716 pts; median per fire -6.50 (n=86)
- forward best call: 2026-08-20 09:21 +405.0pts remaining (episode 415.5pts, major)
- forward worst false alarm: 2026-08-20 11:26 -260.0pts adverse
- earliness (backtest): median 97.5 pts of move remaining at fire (n=5)

### H18 — 1 signal
*A gap-traversal signal followed by a same-direction effortless print within five bars — travel meeting no opposition — continues: the map says vacuum, the tape confirms no resistance.*
Grading: directional. Latest review: rows (recommendation).

**S0-H18** — session × window grid (cells as in the matrix):

| session | backtest | forward |
|---|---|---|
| whole | ▲i+2.7pp (16/67) · p+2.9pp cap102.5 net+355/med+2.5 | ·i+0.7pp (18/79) · p-3.0pp cap74.0 net-470/med-7.5 |
| london | ·i+0.5pp (7/28) · p+2.7pp cap87.5 net+681/med+46.2 | ▲i+2.0pp (7/28) · p-8.6pp cap67.5 net-73/med+1.2 |
| overlap | (°▼i-11.4pp (0/9) · p+11.6pp cap252.2 net-157/med-78.0) | (°▼i-13.7pp (0/11) · p-3.2pp cap109.5 net-260/med+3.5) |
| ny_only | (°▼i-2.5pp (1/6) · p+3.2pp cap147.5 net-94/med-19.0) | (°▲i+26.5pp (6/13) · p-2.8pp cap74.0 net+26/med+7.0) |
| dead | (°▼i-14.6pp (0/5) · p-7.2pp cap— net+32/med-6.6) | (°▼i-6.1pp (1/6) · p-7.5pp cap— net-92/med-17.5) |
| asia | (°▲i+17.1pp (8/19) · p-13.4pp cap61.5 net-107/med+2.5) | ▼i-6.1pp (4/21) · p-3.5pp cap48.0 net-71/med-10.0 |

- backtest payoff: right +2707 / wrong -2352 / net +355 pts; median per fire +2.50 (n=67)
- backtest best call: 2026-08-03 05:12 +445.5pts remaining (episode 472.0pts, major)
- backtest worst false alarm: 2026-07-28 15:04 -332.5pts adverse
- forward payoff: right +1317 / wrong -1788 / net -470 pts; median per fire -7.50 (n=79)
- forward best call: 2026-08-18 09:56 +194.0pts remaining (episode 240.0pts, major)
- forward worst false alarm: 2026-08-19 15:13 -190.0pts adverse
- earliness (backtest): median 120.0 pts of move remaining at fire (n=11)

### H19 — 1 signal
*A probe-failure reversal signal followed by continued wide-loud effort in the anchor bar's own close direction within five bars is NOT the start of the claimed reversal — a SUPPRESSION/FADE configuration, and it says so.*
Grading: directional. Latest review: rows (recommendation).

- Question **Q1-H19**: see the register entry (status there is authoritative).
**S0-H19** — session × window grid (cells as in the matrix):

| session | backtest | forward |
|---|---|---|
| whole | ▼i-11.9pp (16/172) · p+9.1pp cap131.4 net+2236/med+3.2 | ▼i-4.1pp (55/306) · p-1.3pp cap77.5 net+1200/med+2.0 |
| london | ▼i-5.7pp (6/32) · p+4.0pp cap141.0 net+708/med+34.0 | ·i-1.7pp (16/75) · p-2.5pp cap89.2 net-214/med+6.0 |
| overlap | (°▼i-11.4pp (0/12) · p+50.5pp cap148.0 net+894/med+109.5) | (°▼i-13.7pp (0/18) · p+36.2pp cap155.5 net+497/med+103.8) |
| ny_only | ▼i-14.4pp (2/42) · p+24.6pp cap317.8 net+879/med+3.2 | ▼i-15.6pp (2/49) · p-4.4pp cap143.5 net+387/med+13.0 |
| dead | ▼i-11.5pp (1/32) · p+8.4pp cap107.0 net-17/med-1.0 | ·i+0.4pp (13/56) · p+1.4pp cap67.1 net-24/med-8.5 |
| asia | ▼i-12.0pp (7/54) · p+0.2pp cap68.5 net-228/med-3.0 | ▼i-2.9pp (24/108) · p-4.2pp cap54.0 net+555/med+2.0 |

- backtest payoff: right +9284 / wrong -7047 / net +2236 pts; median per fire +3.25 (n=172)
- backtest best call: 2026-07-28 04:49 +523.0pts remaining (episode 543.0pts, major)
- backtest worst false alarm: 2026-07-29 19:00 -643.0pts adverse
- forward payoff: right +6605 / wrong -5405 / net +1200 pts; median per fire +2.00 (n=306)
- forward best call: 2026-08-20 09:13 +395.5pts remaining (episode 415.5pts, major)
- forward worst false alarm: 2026-08-28 14:30 -277.5pts adverse
- earliness (backtest): median 102.5 pts of move remaining at fire (n=11)

### H20 — 1 signal
*A wide-bar close-through of a session extreme (the same conditioned wide-bar class the retest anchor fires on; resolution = the close beyond the level, not a rejection back inside) initiates continuation in the break direction.*
Grading: directional. Latest review: rows (recommendation).

**S0-H20** — session × window grid (cells as in the matrix):

| session | backtest | forward |
|---|---|---|
| whole | ▼i-12.2pp (2/58) · p-11.3pp cap114.0 [cls 40.6%/15.6%i] net+27/med+18.2 | ▼i-13.0pp (2/63) · p+1.9pp cap113.5 [cls 41.0%/16.2%i] net-842/med-34.5 |
| london | ▼i-14.5pp (2/37) · p-16.6pp cap87.5 [cls 40.9%/19.9%i] net-532/med+4.5 | ▼i-15.7pp (2/46) · p+10.3pp cap115.8 [cls 41.9%/20.0%i] net-214/med-12.5 |
| overlap | (°▼i-9.2pp (0/12) · p+8.7pp cap148.8 [cls 41.3%/9.2%i] net+728/med+69.0) | (°▼i-10.1pp (0/11) · p-16.0pp cap108.0 [cls 43.3%/10.1%i] net-463/med-56.0) |
| ny_only | (°▼i-5.4pp (0/4) · p-17.3pp cap217.5 [cls 42.3%/5.4%i] net-81/med-9.4) | (°▼i-16.7pp (0/1) · p-10.3pp cap— [cls 10.3%/16.7%i] net-22/med-22.0) |
| dead | (°▼i-7.4pp (0/2) · p-11.8pp cap— [cls 11.8%/7.4%i] net-51/med-25.7) | (°▼i-8.0pp (0/1) · p-16.0pp cap— [cls 16.0%/8.0%i] net-45/med-44.6) |
| asia | (°▼i-20.7pp (0/3) · p-6.9pp cap40.5 [cls 40.2%/20.7%i] net-36/med+11.0) | (°▼i-14.8pp (0/4) · p-41.2pp cap— [cls 41.2%/14.8%i] net-100/med-25.5) |

- backtest payoff: right +1911 / wrong -1883 / net +27 pts; median per fire +18.25 (n=58)
- backtest best call: 2026-07-28 12:44 +200.0pts remaining (episode 347.0pts, major)
- backtest worst false alarm: 2026-07-27 13:28 -308.4pts adverse
- forward payoff: right +2356 / wrong -3198 / net -842 pts; median per fire -34.50 (n=63)
- forward best call: 2026-08-17 08:26 +-12.5pts remaining (episode 45.5pts)
- forward worst false alarm: 2026-08-19 12:51 -260.0pts adverse
- earliness (backtest): median 200.0 pts of move remaining at fire (n=1)


---

Appendix: the per-session detail beyond London and every horizon-mark payoff live in hypothesis_performance.json (generated, same run).