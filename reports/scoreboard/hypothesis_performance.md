# Hypothesis Performance — Per-Instrument

Engine `01e9d5694` — register 40 fence as amended 2026-08-19 (operator): one section per instrument, each computed only from that instrument's own store and native calendar; uk100 canonical, ger40/nas100/us30 PROVISIONAL (validation pending). Numbers are NEVER pooled across instruments — cross-instrument aggregation is a future registration. This first cross-instrument read is EXPLORATORY: expectations deliberately unregistered; anything interesting becomes a pre-registered question before it becomes a claim.

---

# uk100 (uk100fut) — CANONICAL

Store span (1M, close ts): 2026-07-12 22:06:00+00:00 → 2026-08-21 19:59:00+00:00. Volume type: real futures volume (step-zero audit).

## Summary Matrix (page 1)

Engine `01e9d5694` — OBSERVATIONAL signal scoreboard - move-detection, not trading; no fills exist here by construction; never validation (docs/hypothesis_lifecycle.md stage 4)

**Review labels are RECOMMENDATIONS — none actioned, review pending operator familiarity.** Cells: marker + precision LIFT vs that context's OWN chance rate, (hits/fires), payoff net/median points (directional rows; either-direction rows have no payoff by construction). ▲/▼ = beyond ±2pp of chance, · = within. (°…) = small-n (fires<20 or episodes<10): dimmed, excluded from any future label arithmetic. Read READING_GUIDE.md first; full detail in hypothesis_performance.json.

| H | label | backtest whole | backtest london | forward whole | forward london |
|---|---|---|---|---|---|
| *context* | | 181 ep; chance 23.6%dir/44.4%either | 52 ep; chance 24.9%dir/47.2%either | 54 ep; chance 24.3%dir/44.4%either | 12 ep; chance 28.1%dir/53.4%either |
| S0-H1 | keep-watching | ▲i+9.0pp (23/69) · p+1.0pp cap38.8 net+194/med+2.8 | ▲i+5.8pp (7/22) · p+11.5pp cap38.5 net+133/med+3.0 | ▲i+6.1pp (14/50) · p-4.3pp cap12.7 net-4/med-0.5 | (°▲i+26.6pp (6/13) · p-12.7pp cap26.2 net-3/med-1.2) |
| S1-H1 | keep-watching | (°▼i-4.3pp (1/5) · p-3.6pp cap59.3 net+9/med+3.0) | — | (°▲i+3.1pp (1/4) · p+0.7pp cap33.0 net+7/med-1.6) | (°▲i+13.7pp (1/3) · p+5.2pp cap33.0 net+28/med+10.5) |
| S0-H2 | promote-candidate | ·i-0.4pp (83/347) · p+1.2pp cap34.8 net+781/med+1.5 | ▼i-3.5pp (18/80) · p+6.3pp cap40.0 net+521/med+9.2 | ▼i-3.7pp (28/154) · p+3.0pp cap13.1 net-22/med-0.7 | ▼i-3.7pp (7/44) · p-5.4pp cap28.0 net-14/med-1.2 |
| S1-H2 | promote-candidate | ·i+0.3pp (62/252) · p+0.6pp cap34.2 net+540/med+0.9 | ·i+1.1pp (16/59) · p+5.6pp cap39.0 net+559/med+12.0 | ▼i-4.3pp (23/131) · p+4.7pp cap13.1 net-9/med-0.8 | ·i+0.4pp (7/35) · p-5.2pp cap28.9 net-15/med-1.8 |
| S0-H3 | keep-watching | — | — | (°·i-1.9pp (2/10) · p+15.7pp cap7.0 net-14/med+0.3) | (°▲i+13.7pp (1/3) · p+5.2pp cap19.5 net-24/med-5.0) |
| S0-H4 | keep-watching | (°▲i+18.6pp (3/7) · p-23.6pp cap— net+14/med+0.5) | (°▼i-26.0pp (0/1) · p-24.9pp cap— net+6/med+5.5) | — | — |
| S0-H5 | keep-watching | — | — | — | — |
| S0-H6 | keep-watching | ·i-1.7pp (8/59) · p+8.2pp cap33.8 [cls 37.6%/15.3%i] net+391/med+5.7 | ·i+1.4pp (4/31) · p+20.7pp cap32.9 [cls 37.4%/11.5%i] net+282/med+16.0 | ▲i+3.1pp (4/25) · p+14.3pp cap19.6 [cls 41.7%/12.9%i] net+147/med+5.8 | (°▲i+6.1pp (3/17) · p+19.6pp cap18.2 [cls 39.2%/11.5%i] net+104/med+5.8) |
| S0-H7 | keep-watching | ▲i+8.7pp (37/112) · p+5.9pp cap32.0 net+7/med+2.8 | ▲i+15.5pp (17/41) · p+1.9pp cap32.0 net-217/med+2.7 | ▼i-10.0pp (5/42) · p+6.7pp cap23.2 net+102/med+2.1 | (°▼i-14.3pp (1/19) · p+8.7pp cap24.2 net+4/med-1.0) |
| S0-H7 (either-dir) | keep-watching | ·i+0.0pp (49/112) · p+7.4pp cap15.8 | ▲i+7.2pp (22/41) · p+1.6pp cap20.0 | ▼i-7.2pp (14/42) · p+0.8pp cap19.7 | (°▼i-11.5pp (5/19) · p+4.5pp cap20.0) |
| S0-H8 | keep-watching | ▼i-2.9pp (142/347) · p+1.7pp cap17.3 | ▼i-15.3pp (25/80) · p+5.3pp cap34.5 | ▼i-6.1pp (53/154) · p+3.0pp cap7.6 | ·i-1.4pp (16/44) · p-5.7pp cap10.5 |
| S0-H9 | keep-watching | ▲i+4.8pp (16/55) · p+3.7pp cap37.2 net+319/med+3.5 | (°▼i-16.9pp (1/11) · p+20.6pp cap45.0 net+108/med+12.5) | (°▲i+28.1pp (7/14) · p-17.2pp cap16.0 net-18/med-3.1) | — |
| S1-H9 | keep-watching | (°▼i-13.8pp (2/19) · p+23.8pp cap45.0 net+263/med+12.8) | (°▼i-26.0pp (0/8) · p+25.1pp cap57.1 net+148/med+17.8) | (°▲i+3.1pp (1/4) · p-24.3pp cap— net-10/med-2.2) | — |
| S0-H10 | deprioritize | ▼i-8.9pp (45/293) · p-4.5pp cap27.1 net-240/med-1.4 | ▼i-13.9pp (8/66) · p+2.4pp cap33.2 net-62/med+1.9 | ▲i+2.8pp (24/97) · p-15.0pp cap12.7 net-241/med-2.0 | (°▼i-11.3pp (1/12) · p-11.4pp cap21.5 net+27/med+4.8) |
| S0-H11 | keep-watching | ▲i+2.9pp (86/316) · p+2.3pp cap32.6 net-647/med-2.4 | ▲i+3.1pp (43/148) · p-1.3pp cap35.0 net+250/med-0.6 | ▼i-2.5pp (13/67) · p-0.4pp cap16.7 net+181/med+3.2 | ▼i-7.5pp (4/33) · p-12.9pp cap20.7 net+157/med+4.8 |
| S1-H11 | keep-watching | ▼i-5.6pp (29/155) · p-1.0pp cap33.0 net-617/med-0.7 | ·i-1.7pp (9/37) · p-8.7pp cap34.0 net-466/med-15.7 | ▼i-8.0pp (11/79) · p+16.2pp cap14.6 net-178/med+0.5 | ▲i+4.7pp (9/37) · p+4.3pp cap18.0 net-226/med-8.8 |
| S0-H12 | keep-watching | — | — | — | — |
| S0-H13 | keep-watching | (°▲i+25.7pp (1/2) · p+26.4pp cap37.0 net+28/med+13.8) | (°▲i+24.0pp (1/2) · p+25.1pp cap37.0 net+28/med+13.8) | (°▼i-21.9pp (0/3) · p+9.0pp cap6.7 net-33/med-6.1) | — |
| S0-H14 | keep-watching | ▼i-8.7pp (46/294) · p-9.0pp cap24.8 net-695/med-1.9 | ▼i-9.9pp (10/62) · p-5.5pp cap28.1 net-81/med+3.1 | ·i-1.3pp (21/102) · p-15.5pp cap8.9 net-195/med-1.5 | (°▼i-9.6pp (1/10) · p-8.1pp cap20.5 net+14/med+0.1) |
| S0-H15 | keep-watching | — | — | — | — |
| S0-H16 | keep-watching | (°▼i-4.3pp (3/15) · p+3.1pp cap33.4 net+5/med+6.0) | — | (°▲i+18.1pp (2/5) · p-4.3pp cap24.7 net+11/med+1.0) | — |
| **union coverage** | | 60.8% (110/181) | 59.6% (31/52) | 85.2% (46/54) | 91.7% (11/12) |

### Dual-convention side-by-side — load-bearing patterns

| pattern | context | initiation | participation (cap) |
|---|---|---|---|
| Q1-H1 away cells (S0-H1) | uk100fut/forward | 28.0% (14/50) | 20.0% (cap 12.7) |
| Q1-H1 away cells (S0-H1) | ger40fut/forward | 24.0% (12/50) | 32.0% (cap 36.2) |
| Q1-H1 away cells (S0-H1) | nas100fut/forward | 37.1% (13/35) | 37.1% (cap 74.9) |
| Q1-H1 away cells (S0-H1) | us30fut/forward | 19.7% (13/66) | 33.3% (cap 54.8) |
| H2 forward (S0-H2) | uk100fut/forward | 18.2% (28/154) | 27.3% (cap 13.1) |
| H2 forward (S0-H2) | ger40fut/forward | 22.1% (31/140) | 25.7% (cap 34.2) |
| H2 forward (S0-H2) | nas100fut/forward | 20.6% (45/218) | 30.7% (cap 75.1) |
| H2 forward (S0-H2) | us30fut/forward | 17.8% (40/225) | 27.6% (cap 67.8) |
| H2 forward (S1-H2) | uk100fut/forward | 17.6% (23/131) | 29.0% (cap 13.1) |
| H2 forward (S1-H2) | ger40fut/forward | 23.8% (24/101) | 28.7% (cap 33.1) |
| H2 forward (S1-H2) | nas100fut/forward | 23.6% (37/157) | 30.6% (cap 74.4) |
| H2 forward (S1-H2) | us30fut/forward | 23.4% (39/167) | 23.4% (cap 63.5) |
| S0-H8 (either-dir) | uk100fut/backtest | 40.9% (142/347) | 46.1% (cap 17.3) |
| S0-H8 (either-dir) | ger40fut/backtest | 30.8% (72/234) | 53.0% (cap 35.5) |
| S0-H8 (either-dir) | nas100fut/backtest | 36.6% (117/320) | 43.4% (cap 65.1) |
| S0-H8 (either-dir) | us30fut/backtest | 26.0% (73/281) | 52.0% (cap 76.5) |
| S0-H6 (conditioned) | uk100fut/backtest | 13.6% (8/59) | 45.8% (cap 33.8) |
| S0-H6 (conditioned) | ger40fut/backtest | 5.6% (2/36) | 38.9% (cap 59.3) |
| S0-H6 (conditioned) | nas100fut/backtest | 17.2% (5/29) | 31.0% (cap 260.8) |
| S0-H6 (conditioned) | us30fut/backtest | 9.6% (5/52) | 19.2% (cap 175.0) |
| S0-H8 (either-dir) | uk100fut/forward | 34.4% (53/154) | 47.4% (cap 7.6) |
| S0-H8 (either-dir) | ger40fut/forward | 45.0% (63/140) | 40.7% (cap 23.4) |
| S0-H8 (either-dir) | nas100fut/forward | 48.6% (106/218) | 51.4% (cap 56.8) |
| S0-H8 (either-dir) | us30fut/forward | 34.2% (77/225) | 48.9% (cap 42.5) |
| S0-H6 (conditioned) | uk100fut/forward | 16.0% (4/25) | 56.0% (cap 19.6) |
| S0-H6 (conditioned) | ger40fut/forward | 46.7% (28/60) | 30.0% (cap 45.6) |
| S0-H6 (conditioned) | nas100fut/forward | 11.4% (5/44) | 38.6% (cap 97.4) |
| S0-H6 (conditioned) | us30fut/forward | 23.4% (11/47) | 40.4% (cap 88.5) |


Not graded:  — see register entries.

## Hypothesis Cards (page 2)

### H1 — 2 signals
*A climactic bar — extreme volume on a wide spread late in an extended move — marks exhaustion, and price then reverses against the climax direction.*
Grading: directional. Latest review: keep-watching (recommendation).

- Question **Q1-H1**: see the register entry (status there is authoritative).
**S0-H1** — session × window grid (cells as in the matrix):

| session | backtest | forward |
|---|---|---|
| whole | ▲i+9.0pp (23/69) · p+1.0pp cap38.8 net+194/med+2.8 | ▲i+6.1pp (14/50) · p-4.3pp cap12.7 net-4/med-0.5 |
| london | ▲i+5.8pp (7/22) · p+11.5pp cap38.5 net+133/med+3.0 | (°▲i+26.6pp (6/13) · p-12.7pp cap26.2 net-3/med-1.2) |
| overlap | (°▼i-16.3pp (0/2) · p+23.9pp cap27.5 net+35/med+17.7) | (°▼i-25.8pp (0/2) · p-26.1pp cap— net-22/med-10.8) |
| ny_only | ▲i+19.6pp (9/22) · p+8.0pp cap46.9 net+17/med+1.6 | (°▼i-18.9pp (0/13) · p-6.0pp cap— net+8/med+0.8) |
| dead | (°▲i+2.6pp (4/12) · p+7.4pp cap15.3 net+30/med+1.1) | (°▲i+37.9pp (6/9) · p+15.6pp cap10.0 net+18/med+1.5) |
| asia | (°▲i+2.9pp (3/11) · p-23.4pp cap59.3 net-22/med-2.6) | (°▼i-7.5pp (2/13) · p+1.5pp cap9.1 net-6/med-1.0) |

- backtest payoff: right +639 / wrong -445 / net +194 pts; median per fire +2.75 (n=68)
- backtest best call: 2026-07-29 04:04 +105.2pts remaining (episode 102.8pts, major)
- backtest worst false alarm: 2026-07-23 12:17 -70.7pts adverse
- forward payoff: right +160 / wrong -164 / net -4 pts; median per fire -0.50 (n=50)
- forward best call: 2026-08-21 09:11 +74.0pts remaining (episode 95.0pts, major)
- forward worst false alarm: 2026-08-20 15:03 -30.7pts adverse
- earliness (backtest): median 29.0 pts of move remaining at fire (n=23)

**S1-H1** — session × window grid (cells as in the matrix):

| session | backtest | forward |
|---|---|---|
| whole | (°▼i-4.3pp (1/5) · p-3.6pp cap59.3 net+9/med+3.0) | (°▲i+3.1pp (1/4) · p+0.7pp cap33.0 net+7/med-1.6) |
| london | — | (°▲i+13.7pp (1/3) · p+5.2pp cap33.0 net+28/med+10.5) |
| overlap | — | (°▼i-25.8pp (0/1) · p-26.1pp cap— net-21/med-21.2) |
| ny_only | (°▼i-21.3pp (0/1) · p-10.2pp cap— net-13/med-13.3) | — |
| dead | (°▼i-30.7pp (0/1) · p-17.6pp cap— net+3/med+3.0) | — |
| asia | (°▲i+8.9pp (1/3) · p+0.8pp cap59.3 net+19/med+5.5) | — |

- backtest payoff: right +59 / wrong -50 / net +9 pts; median per fire +3.00 (n=5)
- backtest best call: 2026-07-29 04:04 +105.2pts remaining (episode 102.8pts, major)
- backtest worst false alarm: 2026-07-30 05:53 -37.6pts adverse
- forward payoff: right +42 / wrong -35 / net +7 pts; median per fire -1.65 (n=4)
- forward best call: 2026-08-17 12:27 +5.7pts remaining (episode 19.5pts)
- forward worst false alarm: 2026-08-20 15:03 -30.7pts adverse
- earliness (backtest): median 105.2 pts of move remaining at fire (n=1)

### H2 — 2 signals
*A failed probe beyond a prior extreme — an upthrust above or spring below that closes back inside — reverses against the probe.*
Grading: directional. Latest review: promote-candidate (recommendation).

**S0-H2** — session × window grid (cells as in the matrix):

| session | backtest | forward |
|---|---|---|
| whole | ·i-0.4pp (83/347) · p+1.2pp cap34.8 net+781/med+1.5 | ▼i-3.7pp (28/154) · p+3.0pp cap13.1 net-22/med-0.7 |
| london | ▼i-3.5pp (18/80) · p+6.3pp cap40.0 net+521/med+9.2 | ▼i-3.7pp (7/44) · p-5.4pp cap28.0 net-14/med-1.2 |
| overlap | (°▼i-7.2pp (1/11) · p+1.2pp cap39.0 net+21/med+3.5) | (°▲i+14.2pp (4/10) · p+3.9pp cap30.2 net+69/med+7.0) |
| ny_only | ▼i-3.1pp (10/55) · p+4.3pp cap40.8 net-487/med-2.5 | ▼i-11.8pp (2/28) · p-6.0pp cap— net-10/med-0.8 |
| dead | ▼i-2.9pp (25/90) · p+1.3pp cap23.2 net+180/med+0.8 | (°▼i-3.8pp (5/20) · p+12.3pp cap6.8 net-0/med+0.5) |
| asia | ·i+1.7pp (29/111) · p-2.8pp cap29.8 net+546/med+2.7 | ▼i-3.7pp (10/52) · p+7.2pp cap9.4 net-67/med-1.7 |

- backtest payoff: right +3270 / wrong -2490 / net +781 pts; median per fire +1.50 (n=347)
- backtest best call: 2026-07-30 04:03 +155.1pts remaining (episode 178.3pts, major)
- backtest worst false alarm: 2026-07-24 06:52 -98.0pts adverse
- forward payoff: right +571 / wrong -593 / net -22 pts; median per fire -0.65 (n=154)
- forward best call: 2026-08-20 11:41 +45.8pts remaining (episode 70.0pts, major)
- forward worst false alarm: 2026-08-20 14:42 -45.3pts adverse
- earliness (backtest): median 28.4 pts of move remaining at fire (n=38)

**S1-H2** — session × window grid (cells as in the matrix):

| session | backtest | forward |
|---|---|---|
| whole | ·i+0.3pp (62/252) · p+0.6pp cap34.2 net+540/med+0.9 | ▼i-4.3pp (23/131) · p+4.7pp cap13.1 net-9/med-0.8 |
| london | ·i+1.1pp (16/59) · p+5.6pp cap39.0 net+559/med+12.0 | ·i+0.4pp (7/35) · p-5.2pp cap28.9 net-15/med-1.8 |
| overlap | (°▼i-7.2pp (1/11) · p+1.2pp cap39.0 net+21/med+3.5) | (°▲i+7.5pp (3/9) · p+7.2pp cap30.2 net+81/med+10.2) |
| ny_only | ·i-1.3pp (8/40) · p+4.8pp cap38.6 net-304/med-2.1 | ▼i-10.9pp (2/25) · p-6.0pp cap— net+0/med-0.8 |
| dead | ▼i-6.1pp (15/61) · p+5.4pp cap23.0 net+201/med+0.8 | (°▼i-5.3pp (4/17) · p+11.7pp cap6.7 net-4/med+1.4) |
| asia | ▲i+2.8pp (22/81) · p-7.8pp cap28.4 net+62/med-1.2 | ▼i-7.3pp (7/45) · p+11.9pp cap9.1 net-71/med-2.2 |

- backtest payoff: right +2121 / wrong -1581 / net +540 pts; median per fire +0.95 (n=252)
- backtest best call: 2026-07-30 04:03 +155.1pts remaining (episode 178.3pts, major)
- backtest worst false alarm: 2026-07-29 19:00 -94.0pts adverse
- forward payoff: right +500 / wrong -509 / net -9 pts; median per fire -0.80 (n=131)
- forward best call: 2026-08-20 11:41 +45.8pts remaining (episode 70.0pts, major)
- forward worst false alarm: 2026-08-20 11:41 -39.0pts adverse
- earliness (backtest): median 31.3 pts of move remaining at fire (n=35)

### H3 — 1 signal
*Repeated absorption — high effort with no result — at a price level precedes a breakout through that level.*
Grading: directional. Latest review: keep-watching (recommendation).

**S0-H3** — session × window grid (cells as in the matrix):

| session | backtest | forward |
|---|---|---|
| whole | — | (°·i-1.9pp (2/10) · p+15.7pp cap7.0 net-14/med+0.3) |
| london | — | (°▲i+13.7pp (1/3) · p+5.2pp cap19.5 net-24/med-5.0) |
| overlap | — | — |
| ny_only | — | (°▲i+14.4pp (1/3) · p-6.0pp cap— net+3/med+0.8) |
| dead | — | (°▼i-28.8pp (0/1) · p+82.3pp cap7.1 net-0/med-0.2) |
| asia | — | (°▼i-22.9pp (0/3) · p+29.7pp cap6.8 net+7/med+4.5) |

- forward payoff: right +26 / wrong -39 / net -14 pts; median per fire +0.30 (n=10)
- forward best call: 2026-08-20 11:13 +45.0pts remaining (episode 70.0pts, major)
- forward worst false alarm: 2026-08-20 11:13 -39.0pts adverse

### H4 — 1 signal
*In an established trend, a quiet (low-volume) pullback resolves with trend resumption.*
Grading: directional. Latest review: keep-watching (recommendation).

**S0-H4** — session × window grid (cells as in the matrix):

| session | backtest | forward |
|---|---|---|
| whole | (°▲i+18.6pp (3/7) · p-23.6pp cap— net+14/med+0.5) | — |
| london | (°▼i-26.0pp (0/1) · p-24.9pp cap— net+6/med+5.5) | — |
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

**S0-H6** — session × window grid (cells as in the matrix):

| session | backtest | forward |
|---|---|---|
| whole | ·i-1.7pp (8/59) · p+8.2pp cap33.8 [cls 37.6%/15.3%i] net+391/med+5.7 | ▲i+3.1pp (4/25) · p+14.3pp cap19.6 [cls 41.7%/12.9%i] net+147/med+5.8 |
| london | ·i+1.4pp (4/31) · p+20.7pp cap32.9 [cls 37.4%/11.5%i] net+282/med+16.0 | (°▲i+6.1pp (3/17) · p+19.6pp cap18.2 [cls 39.2%/11.5%i] net+104/med+5.8) |
| overlap | (°▲i+32.8pp (3/6) · p-30.0pp cap— [cls 30.0%/17.2%i] net-87/med-15.4) | (°▲i+20.1pp (1/2) · p+21.6pp cap30.7 [cls 28.4%/29.9%i] net+25/med+12.5) |
| ny_only | (°▲i+10.6pp (1/4) · p-20.5pp cap— [cls 20.5%/14.4%i] net+0/med+6.5) | (°▼i-6.4pp (0/2) · p-6.4pp cap— [cls 6.4%/6.4%i] net-7/med-3.4) |
| dead | (°▼i-9.6pp (0/5) · p-19.1pp cap— [cls 19.1%/9.6%i] net-25/med-6.4) | — |
| asia | (°▼i-20.7pp (0/13) · p+24.4pp cap44.8 [cls 44.8%/20.7%i] net+220/med+5.7) | (°▼i-10.2pp (0/4) · p+19.5pp cap19.0 [cls 55.5%/10.2%i] net+25/med+7.2) |

- backtest payoff: right +818 / wrong -428 / net +391 pts; median per fire +5.70 (n=59)
- backtest best call: 2026-07-31 08:00 +72.8pts remaining (episode 68.5pts, major)
- backtest worst false alarm: 2026-07-22 08:07 -80.3pts adverse
- forward payoff: right +202 / wrong -55 / net +147 pts; median per fire +5.80 (n=25)
- forward best call: 2026-08-21 14:04 +20.5pts remaining (episode 26.0pts)
- forward worst false alarm: 2026-08-20 07:02 -32.0pts adverse
- earliness (backtest): median 21.6 pts of move remaining at fire (n=8)

### H7 — 1 signal
*Quiet decline at a session extreme is disguised accumulation: effortless (low-volume) weakness reverses UP once selling fails to attract participation (mirror: quiet advance at a high reverses down).*
Grading: directional + either-direction (dual). Latest review: keep-watching (recommendation).

- Question **Q1-H7**: see the register entry (status there is authoritative).
**S0-H7** — session × window grid (cells as in the matrix):

| session | backtest | forward |
|---|---|---|
| whole | ▲i+8.7pp (37/112) · p+5.9pp cap32.0 net+7/med+2.8 | ▼i-10.0pp (5/42) · p+6.7pp cap23.2 net+102/med+2.1 |
| london | ▲i+15.5pp (17/41) · p+1.9pp cap32.0 net-217/med+2.7 | (°▼i-14.3pp (1/19) · p+8.7pp cap24.2 net+4/med-1.0) |
| overlap | ▼i-3.3pp (3/23) · p+8.7pp cap39.2 net+227/med+8.7 | (°·i-0.8pp (1/4) · p-1.1pp cap45.3 net+43/med+2.6) |
| ny_only | (°·i+0.1pp (3/14) · p+4.1pp cap27.6 net-24/med+0.0) | (°▲i+14.4pp (3/9) · p-6.0pp cap— net+23/med+2.2) |
| dead | (°▲i+49.3pp (4/5) · p+2.4pp cap51.1 net+60/med+3.5) | (°▼i-28.8pp (0/1) · p-17.7pp cap— net+0/med+0.0) |
| asia | ▲i+10.1pp (10/29) · p+5.4pp cap20.7 net-38/med+0.7 | (°▼i-22.9pp (0/9) · p+18.6pp cap14.0 net+32/med+3.2) |

- backtest payoff: right +1097 / wrong -1090 / net +7 pts; median per fire +2.80 (n=112)
- backtest best call: 2026-07-24 11:09 +98.2pts remaining (episode 98.2pts, major)
- backtest worst false alarm: 2026-07-30 06:55 -94.0pts adverse
- forward payoff: right +269 / wrong -167 / net +102 pts; median per fire +2.10 (n=42)
- forward best call: 2026-08-18 19:09 +7.5pts remaining (episode 10.0pts)
- forward worst false alarm: 2026-08-20 12:44 -43.0pts adverse
- earliness (backtest): median 17.4 pts of move remaining at fire (n=31)

**S0-H7 (either-dir)** — session × window grid (cells as in the matrix):

| session | backtest | forward |
|---|---|---|
| whole | ·i+0.0pp (49/112) · p+7.4pp cap15.8 | ▼i-7.2pp (14/42) · p+0.8pp cap19.7 |
| london | ▲i+7.2pp (22/41) · p+1.6pp cap20.0 | (°▼i-11.5pp (5/19) · p+4.5pp cap20.0) |
| overlap | ·i+0.2pp (7/23) · p+5.3pp cap32.5 | (°·i-1.5pp (2/4) · p-2.2pp cap22.7) |
| ny_only | (°▼i-16.4pp (3/14) · p+8.6pp cap13.4) | (°▲i+34.5pp (6/9) · p-12.1pp cap—) |
| dead | (°▲i+27.3pp (4/5) · p-12.9pp cap51.1) | (°▲i+44.2pp (1/1) · p-35.4pp cap—) |
| asia | ·i-0.9pp (13/29) · p+9.3pp cap10.1 | (°▼i-40.8pp (0/9) · p+4.7pp cap13.5) |

- backtest payoff: n/a by construction (either-direction)
- backtest best call: 2026-07-24 11:09 +98.2pts remaining (episode 98.2pts, major)
- backtest worst false alarm: 2026-07-23 16:44 -25.7pts adverse
- forward payoff: n/a by construction (either-direction)
- forward best call: 2026-08-19 10:10 +54.5pts remaining (episode 62.8pts, major)
- forward worst false alarm: 2026-08-17 10:09 -18.3pts adverse
- earliness (backtest): median 15.0 pts of move remaining at fire (n=42)

### H8 — 1 signal
*Reversal-signature bar anatomy (upthrust/spring) predicts imminent range expansion irrespective of direction.*
Grading: either-direction. Latest review: keep-watching (recommendation).

**S0-H8** — session × window grid (cells as in the matrix):

| session | backtest | forward |
|---|---|---|
| whole | ▼i-2.9pp (142/347) · p+1.7pp cap17.3 | ▼i-6.1pp (53/154) · p+3.0pp cap7.6 |
| london | ▼i-15.3pp (25/80) · p+5.3pp cap34.5 | ·i-1.4pp (16/44) · p-5.7pp cap10.5 |
| overlap | (°▼i-12.0pp (2/11) · p+12.4pp cap18.3) | (°·i-1.5pp (5/10) · p-12.2pp cap29.3) |
| ny_only | ▼i-5.1pp (18/55) · p+23.6pp cap6.9 | ▼i-21.5pp (3/28) · p-8.5pp cap-0.2 |
| dead | ▼i-3.8pp (44/90) · p+1.5pp cap13.9 | (°▼i-15.8pp (8/20) · p+24.6pp cap5.8) |
| asia | ▲i+2.0pp (53/111) · p-9.2pp cap19.0 | ·i-0.4pp (21/52) · p+5.3pp cap7.9 |

- backtest payoff: n/a by construction (either-direction)
- backtest best call: 2026-07-30 04:03 +155.1pts remaining (episode 178.3pts, major)
- backtest worst false alarm: 2026-07-22 10:02 -37.0pts adverse
- forward payoff: n/a by construction (either-direction)
- forward best call: 2026-08-21 08:59 +65.5pts remaining (episode 95.0pts, major)
- forward worst false alarm: 2026-08-20 08:48 -18.3pts adverse
- earliness (backtest): median 26.6 pts of move remaining at fire (n=57)

### H9 — 2 signals
*Persistent lower-TF directional pressure that recruits expanding participation at the parent timeframe precedes continuation beyond what the parent label alone predicts; pressure without participation expansion does not.*
Grading: directional. Latest review: keep-watching (recommendation).

**S0-H9** — session × window grid (cells as in the matrix):

| session | backtest | forward |
|---|---|---|
| whole | ▲i+4.8pp (16/55) · p+3.7pp cap37.2 net+319/med+3.5 | (°▲i+28.1pp (7/14) · p-17.2pp cap16.0 net-18/med-3.1) |
| london | (°▼i-16.9pp (1/11) · p+20.6pp cap45.0 net+108/med+12.5) | — |
| overlap | — | (°▼i-25.8pp (0/1) · p-26.1pp cap— net-1/med-1.0) |
| ny_only | (°▲i+20.4pp (5/12) · p+14.8pp cap69.9 net+115/med+2.8) | (°▲i+31.1pp (2/4) · p+19.0pp cap16.0 net+14/med+5.2) |
| dead | (°▼i-3.4pp (3/11) · p-8.5pp cap26.6 net+11/med+1.0) | — |
| asia | ▲i+8.9pp (7/21) · p-3.9pp cap16.9 net+86/med+6.8 | (°▲i+32.7pp (5/9) · p-37.0pp cap— net-32/med-3.1) |

- backtest payoff: right +558 / wrong -239 / net +319 pts; median per fire +3.50 (n=53)
- backtest best call: 2026-08-03 03:40 +73.2pts remaining (episode 81.3pts, major)
- backtest worst false alarm: 2026-07-30 09:15 -59.3pts adverse
- forward payoff: right +27 / wrong -46 / net -18 pts; median per fire -3.10 (n=14)
- forward best call: 2026-08-21 15:30 +16.7pts remaining (episode 20.0pts)
- forward worst false alarm: 2026-08-14 16:30 -13.2pts adverse
- earliness (backtest): median 15.6 pts of move remaining at fire (n=10)

**S1-H9** — session × window grid (cells as in the matrix):

| session | backtest | forward |
|---|---|---|
| whole | (°▼i-13.8pp (2/19) · p+23.8pp cap45.0 net+263/med+12.8) | (°▲i+3.1pp (1/4) · p-24.3pp cap— net-10/med-2.2) |
| london | (°▼i-26.0pp (0/8) · p+25.1pp cap57.1 net+148/med+17.8) | — |
| overlap | — | (°▼i-25.8pp (0/1) · p-26.1pp cap— net-1/med-1.0) |
| ny_only | (°▼i-21.3pp (0/4) · p+64.8pp cap69.9 net+105/med+31.6) | — |
| dead | (°▼i-10.7pp (1/5) · p+2.4pp cap26.6 net+6/med+2.3) | — |
| asia | (°▲i+25.6pp (1/2) · p+17.5pp cap20.2 net+4/med+2.1) | (°▲i+10.4pp (1/3) · p-37.0pp cap— net-9/med-3.5) |

- backtest payoff: right +377 / wrong -114 / net +263 pts; median per fire +12.75 (n=18)
- backtest best call: 2026-07-19 23:10 +9.2pts remaining (episode 30.7pts)
- backtest worst false alarm: 2026-07-30 09:15 -59.3pts adverse
- forward payoff: right +2 / wrong -12 / net -10 pts; median per fire -2.25 (n=4)
- forward best call: 2026-08-20 02:15 +-1.0pts remaining (episode 8.8pts)
- forward worst false alarm: 2026-08-18 02:00 -11.5pts adverse
- earliness (backtest): median 9.2 pts of move remaining at fire (n=1)

### H10 — 1 signal
*In an established 1-minute trend, no-demand/no-supply prints in the trend's direction signal continuation.*
Grading: directional. Latest review: deprioritize (recommendation).

**S0-H10** — session × window grid (cells as in the matrix):

| session | backtest | forward |
|---|---|---|
| whole | ▼i-8.9pp (45/293) · p-4.5pp cap27.1 net-240/med-1.4 | ▲i+2.8pp (24/97) · p-15.0pp cap12.7 net-241/med-2.0 |
| london | ▼i-13.9pp (8/66) · p+2.4pp cap33.2 net-62/med+1.9 | (°▼i-11.3pp (1/12) · p-11.4pp cap21.5 net+27/med+4.8) |
| overlap | (°▼i-16.3pp (0/7) · p-26.1pp cap— net+27/med+6.8) | (°▼i-25.8pp (0/6) · p-26.1pp cap— net-73/med-14.0) |
| ny_only | ▼i-2.0pp (16/83) · p-0.6pp cap25.3 net+51/med-1.5 | ·i-1.0pp (5/28) · p-2.4pp cap13.5 net-22/med-0.8 |
| dead | ·i-0.1pp (11/36) · p-3.7pp cap11.5 net-110/med-2.5 | (°▼i-11.2pp (3/17) · p-11.8pp cap14.8 net-20/med-0.7) |
| asia | ▼i-14.5pp (10/101) · p-7.7pp cap27.0 net-147/med-1.5 | ▲i+21.2pp (15/34) · p-22.3pp cap9.3 net-153/med-4.7 |

- backtest payoff: right +1533 / wrong -1773 / net -240 pts; median per fire -1.40 (n=293)
- backtest best call: 2026-07-23 10:20 +90.0pts remaining (episode 104.8pts, major)
- backtest worst false alarm: 2026-07-28 13:10 -62.5pts adverse
- forward payoff: right +148 / wrong -389 / net -241 pts; median per fire -2.00 (n=97)
- forward best call: 2026-08-14 16:54 +22.5pts remaining (episode 16.8pts)
- forward worst false alarm: 2026-08-17 14:08 -24.2pts adverse
- earliness (backtest): median 21.6 pts of move remaining at fire (n=24)

### H11 — 2 signals
*Price entering a low-volume price zone traverses it faster than baseline; entering a high-volume node it stalls or reverses at above-baseline rates.*
Grading: directional. Latest review: keep-watching (recommendation).

**S0-H11** — session × window grid (cells as in the matrix):

| session | backtest | forward |
|---|---|---|
| whole | ▲i+2.9pp (86/316) · p+2.3pp cap32.6 net-647/med-2.4 | ▼i-2.5pp (13/67) · p-0.4pp cap16.7 net+181/med+3.2 |
| london | ▲i+3.1pp (43/148) · p-1.3pp cap35.0 net+250/med-0.6 | ▼i-7.5pp (4/33) · p-12.9pp cap20.7 net+157/med+4.8 |
| overlap | ▲i+8.7pp (10/40) · p-18.6pp cap33.5 net-403/med-11.8 | (°▲i+11.7pp (3/8) · p+36.4pp cap20.5 net+39/med+8.7) |
| ny_only | ▼i-5.5pp (6/38) · p+18.7pp cap34.0 net-267/med-1.6 | ▲i+5.1pp (6/25) · p+14.0pp cap12.5 net+19/med+1.8 |
| dead | ▼i-15.7pp (3/20) · p+37.4pp cap18.5 net+59/med+0.7 | — |
| asia | ▲i+9.9pp (24/70) · p-1.1pp cap19.4 net-286/med-4.5 | (°▼i-22.9pp (0/1) · p+63.0pp cap4.0 net-34/med-33.5) |

- backtest payoff: right +2555 / wrong -3203 / net -647 pts; median per fire -2.35 (n=316)
- backtest best call: 2026-07-22 06:08 +129.2pts remaining (episode 163.2pts, major)
- backtest worst false alarm: 2026-07-22 07:36 -96.5pts adverse
- forward payoff: right +388 / wrong -206 / net +181 pts; median per fire +3.20 (n=67)
- forward best call: 2026-08-17 13:04 +22.8pts remaining (episode 32.3pts)
- forward worst false alarm: 2026-08-21 13:35 -27.0pts adverse
- earliness (backtest): median 20.5 pts of move remaining at fire (n=27)

**S1-H11** — session × window grid (cells as in the matrix):

| session | backtest | forward |
|---|---|---|
| whole | ▼i-5.6pp (29/155) · p-1.0pp cap33.0 net-617/med-0.7 | ▼i-8.0pp (11/79) · p+16.2pp cap14.6 net-178/med+0.5 |
| london | ·i-1.7pp (9/37) · p-8.7pp cap34.0 net-466/med-15.7 | ▲i+4.7pp (9/37) · p+4.3pp cap18.0 net-226/med-8.8 |
| overlap | ▼i-16.3pp (0/30) · p+3.9pp cap34.5 net+73/med-1.6 | (°▼i-25.8pp (0/9) · p+51.7pp cap24.2 net+46/med+7.0) |
| ny_only | ▼i-7.0pp (6/42) · p+4.1pp cap20.6 net+75/med+0.7 | (°▼i-18.9pp (0/10) · p-6.0pp cap— net+1/med+2.9) |
| dead | (°▲i+44.3pp (3/4) · p-17.6pp cap— net-21/med-4.5) | (°·i-0.2pp (2/7) · p+39.4pp cap14.6 net+6/med+2.0) |
| asia | ·i+1.8pp (11/42) · p+0.8pp cap34.3 net-277/med-0.9 | (°▼i-22.9pp (0/16) · p+19.2pp cap11.0 net-5/med+1.2) |

- backtest payoff: right +1033 / wrong -1650 / net -617 pts; median per fire -0.70 (n=155)
- backtest best call: 2026-07-24 03:18 +96.3pts remaining (episode 104.3pts, major)
- backtest worst false alarm: 2026-07-31 07:01 -103.0pts adverse
- forward payoff: right +320 / wrong -499 / net -178 pts; median per fire +0.50 (n=79)
- forward best call: 2026-08-20 11:09 +45.0pts remaining (episode 70.0pts, major)
- forward worst false alarm: 2026-08-20 11:15 -40.7pts adverse
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
| whole | (°▲i+25.7pp (1/2) · p+26.4pp cap37.0 net+28/med+13.8) | (°▼i-21.9pp (0/3) · p+9.0pp cap6.7 net-33/med-6.1) |
| london | (°▲i+24.0pp (1/2) · p+25.1pp cap37.0 net+28/med+13.8) | — |
| overlap | — | — |
| ny_only | — | (°▼i-18.9pp (0/1) · p-6.0pp cap— net-3/med-3.0) |
| dead | — | — |
| asia | — | (°▼i-22.9pp (0/2) · p+13.0pp cap6.7 net-30/med-14.8) |

- backtest payoff: right +28 / wrong +0 / net +28 pts; median per fire +13.75 (n=2)
- backtest best call: 2026-07-24 09:09 +43.2pts remaining (episode 42.7pts)
- backtest worst false alarm: 2026-07-24 09:09 -5.8pts adverse
- forward payoff: right +0 / wrong -33 / net -33 pts; median per fire -6.10 (n=3)
- forward worst false alarm: 2026-08-21 05:25 -10.3pts adverse
- earliness (backtest): median 43.2 pts of move remaining at fire (n=1)

### H14 — 1 signal
*Counter-trend No Demand / No Supply prints in an established trend mark absorption and precede trend continuation.*
Grading: directional. Latest review: keep-watching (recommendation).

**S0-H14** — session × window grid (cells as in the matrix):

| session | backtest | forward |
|---|---|---|
| whole | ▼i-8.7pp (46/294) · p-9.0pp cap24.8 net-695/med-1.9 | ·i-1.3pp (21/102) · p-15.5pp cap8.9 net-195/med-1.5 |
| london | ▼i-9.9pp (10/62) · p-5.5pp cap28.1 net-81/med+3.1 | (°▼i-9.6pp (1/10) · p-8.1pp cap20.5 net+14/med+0.1) |
| overlap | (°▼i-16.3pp (0/4) · p-1.1pp cap24.0 net+20/med+5.6) | (°▼i-25.8pp (0/9) · p-26.1pp cap— net-131/med-16.0) |
| ny_only | ▼i-5.1pp (16/99) · p-1.1pp cap24.5 net-174/med-3.1 | ·i-1.8pp (6/35) · p-3.1pp cap14.5 net+19/med+1.7 |
| dead | ▲i+8.7pp (13/33) · p-11.5pp cap17.2 net-105/med-2.4 | (°▼i-5.7pp (3/13) · p-17.7pp cap— net-15/med+0.0) |
| asia | ▼i-17.1pp (7/96) · p-12.7pp cap30.8 net-355/med-3.6 | ▲i+8.5pp (11/35) · p-19.9pp cap8.7 net-82/med-3.6 |

- backtest payoff: right +1293 / wrong -1989 / net -695 pts; median per fire -1.95 (n=294)
- backtest best call: 2026-07-22 06:03 +134.2pts remaining (episode 163.2pts, major)
- backtest worst false alarm: 2026-07-28 05:56 -59.0pts adverse
- forward payoff: right +190 / wrong -386 / net -195 pts; median per fire -1.50 (n=102)
- forward best call: 2026-08-17 03:50 +24.2pts remaining (episode 24.8pts, major)
- forward worst false alarm: 2026-08-14 15:13 -25.8pts adverse
- earliness (backtest): median 23.5 pts of move remaining at fire (n=24)

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
| whole | (°▼i-4.3pp (3/15) · p+3.1pp cap33.4 net+5/med+6.0) | (°▲i+18.1pp (2/5) · p-4.3pp cap24.7 net+11/med+1.0) |
| london | — | — |
| overlap | (°▲i+3.7pp (3/15) · p+0.6pp cap33.4 net+5/med+6.0) | (°▲i+14.2pp (2/5) · p-6.1pp cap24.7 net+11/med+1.0) |
| ny_only | — | — |
| dead | — | — |
| asia | — | — |

- backtest payoff: right +173 / wrong -169 / net +5 pts; median per fire +6.00 (n=15)
- backtest best call: 2026-08-03 15:00 +4.5pts remaining (episode 28.5pts)
- backtest worst false alarm: 2026-07-16 15:00 -61.7pts adverse
- forward payoff: right +30 / wrong -19 / net +11 pts; median per fire +1.00 (n=5)
- forward best call: 2026-08-21 15:00 +5.2pts remaining (episode 20.0pts)
- forward worst false alarm: 2026-08-17 15:00 -15.8pts adverse
- earliness (backtest): median 1.2 pts of move remaining at fire (n=3)


---

# ger40 (ger40fut) — PROVISIONAL

> **PROVISIONAL — validation pending (register 40 fence as amended 2026-08-19): replay-only study over the synced store; canonical status, live attachment, and Asia/pause-sensitive cell interpretation await this instrument's validation evening. EXPLORATORY first cross-instrument look — expectations deliberately unregistered; anything interesting becomes a pre-registered question before it becomes a claim. NO POOLING across instruments.**
>
> - drift-adjustment segments and engine tod baselines run on the provider/London trading-day structure; native cash-hour segmentation is part of this instrument's validation evening
> - sessions = the registered register-37 world-clock partition (native-tz, DST-proof) applied to this instrument's own bars; 'london' is not the home session of the US pairs
> - the forward window (>= go_live) is also a replay over the synced store — this instrument has NO live attachment yet

Store span (1M, close ts): 2026-07-19 22:42:00+00:00 → 2026-08-21 19:59:00+00:00. Volume type: real futures volume (register 40 first-sync sanity; canonical verdict at this instrument's validation evening).

## Summary Matrix (page 1)

Engine `01e9d5694` — OBSERVATIONAL signal scoreboard - move-detection, not trading; no fills exist here by construction; never validation (docs/hypothesis_lifecycle.md stage 4)

**Review labels are RECOMMENDATIONS — none actioned, review pending operator familiarity.** Cells: marker + precision LIFT vs that context's OWN chance rate, (hits/fires), payoff net/median points (directional rows; either-direction rows have no payoff by construction). ▲/▼ = beyond ±2pp of chance, · = within. (°…) = small-n (fires<20 or episodes<10): dimmed, excluded from any future label arithmetic. Read READING_GUIDE.md first; full detail in hypothesis_performance.json.

| H | label | backtest whole | backtest london | forward whole | forward london |
|---|---|---|---|---|---|
| *context* | | 110 ep; chance 23.8%dir/45.1%either | 27 ep; chance 26.4%dir/51.2%either | 58 ep; chance 21.5%dir/39.7%either | 16 ep; chance 23.9%dir/45.5%either |
| S0-H1 | keep-watching | ▼i-2.6pp (9/49) · p+10.9pp cap89.9 net-83/med+0.7 | (°▼i-21.1pp (0/5) · p+33.6pp cap89.9 net+198/med+39.9) | ·i+0.3pp (12/50) · p+10.5pp cap36.2 net+127/med-1.8 | (°▲i+11.6pp (5/13) · p+14.6pp cap50.3 net+47/med+11.2) |
| S1-H1 | keep-watching | (°▼i-21.0pp (0/3) · p-23.8pp cap— net-72/med-34.2) | (°▼i-21.1pp (0/1) · p-26.4pp cap— net-54/med-53.5) | (°▲i+26.3pp (1/2) · p-21.5pp cap— net-28/med-14.2) | — |
| S0-H2 | promote-candidate | ▼i-7.8pp (31/234) · p+0.6pp cap77.8 net-661/med-5.2 | (°▼i-7.8pp (2/15) · p-13.1pp cap86.6 net+93/med+9.8) | ·i-1.6pp (31/140) · p+4.2pp cap34.2 net-188/med-1.9 | ·i+1.7pp (8/28) · p-6.0pp cap66.5 net-93/med-11.2 |
| S1-H2 | promote-candidate | ▼i-6.8pp (25/176) · p+2.3pp cap77.4 net-760/med-8.3 | (°▼i-5.7pp (2/13) · p-11.0pp cap86.6 net+136/med+14.0) | ·i+0.1pp (24/101) · p+7.2pp cap33.1 net+58/med-1.0 | (°▲i+6.4pp (6/18) · p-7.2pp cap83.2 net-23/med-12.2) |
| S0-H3 | keep-watching | (°▲i+4.0pp (2/8) · p-11.3pp cap70.3 net-28/med+2.0) | — | (°▲i+6.3pp (3/10) · p-21.5pp cap— net-26/med-8.2) | (°▼i-26.9pp (0/1) · p-23.9pp cap— net+19/med+18.8) |
| S0-H4 | keep-watching | ▼i-3.4pp (6/34) · p+5.6pp cap53.4 net+72/med+10.0 | (°▲i+8.9pp (3/10) · p-16.4pp cap50.2 net-30/med-3.7) | — | — |
| S0-H5 | keep-watching | — | — | — | — |
| S0-H6 | keep-watching | ▼i-8.1pp (2/36) · p+3.9pp cap59.3 [cls 35.0%/13.7%i] net-192/med-10.4 | (°▼i-4.3pp (1/18) · p-7.4pp cap78.7 [cls 35.2%/9.9%i] net-56/med-10.3) | ▲i+25.2pp (28/60) · p-7.7pp cap45.6 [cls 37.7%/21.5%i] net-865/med-10.4 | ▲i+38.1pp (21/34) · p-19.0pp cap53.4 [cls 36.6%/23.7%i] net-879/med-24.9 |
| S0-H7 | keep-watching | ·i-0.7pp (12/59) · p+11.8pp cap97.8 net+761/med+4.2 | ▼i-11.1pp (2/20) · p+23.6pp cap86.9 net+719/med+33.0 | ▲i+12.3pp (9/25) · p-5.5pp cap85.5 net-179/med-4.4 | (°▲i+17.5pp (8/18) · p-7.2pp cap88.2 net-172/med-4.6) |
| S0-H7 (either-dir) | keep-watching | ▼i-5.3pp (20/59) · p+19.3pp cap50.2 | ▼i-10.2pp (6/20) · p+23.8pp cap57.4 | ▲i+7.9pp (13/25) · p+4.3pp cap14.6 | (°▲i+11.7pp (11/18) · p+10.1pp cap11.6) |
| S0-H8 | keep-watching | ▼i-8.4pp (72/234) · p+7.9pp cap35.5 | (°▼i-20.2pp (3/15) · p-31.2pp cap68.2) | ·i+0.9pp (63/140) · p+1.0pp cap23.4 | ▼i-10.1pp (11/28) · p-9.8pp cap29.6 |
| S0-H9 | keep-watching | ▲i+4.0pp (13/52) · p-8.4pp cap55.5 net-426/med-4.1 | (°▼i-21.1pp (0/3) · p-26.4pp cap— net+17/med+22.6) | (°▲i+16.3pp (4/10) · p-21.5pp cap— net-210/med-6.6) | (°▲i+23.1pp (1/2) · p-23.9pp cap— net-158/med-78.9) |
| S1-H9 | keep-watching | (°▼i-21.0pp (0/8) · p+26.2pp cap101.1 net-53/med+13.1) | — | (°▲i+43.0pp (2/3) · p-21.5pp cap— net-127/med-7.7) | (°▲i+73.1pp (1/1) · p-23.9pp cap— net-114/med-114.2) |
| S0-H10 | deprioritize | ▲i+4.9pp (38/147) · p-4.1pp cap49.6 net-391/med+3.2 | ▲i+2.0pp (9/39) · p-16.1pp cap80.6 net-463/med-12.5 | ▲i+2.5pp (21/80) · p+2.3pp cap28.9 net+169/med+3.0 | (°▲i+6.4pp (5/15) · p+2.8pp cap42.4 net+73/med+17.1) |
| S0-H11 | keep-watching | ·i-0.7pp (15/74) · p-3.5pp cap68.3 net-452/med-6.0 | (°▼i-21.1pp (0/14) · p-5.0pp cap73.1 net-472/med-58.8) | ▼i-4.9pp (34/181) · p+0.6pp cap45.2 net-416/med-5.5 | ·i+0.9pp (27/97) · p-5.3pp cap53.4 net-220/med-3.0 |
| S1-H11 | keep-watching | ·i-0.1pp (63/301) · p+6.1pp cap82.4 net+1221/med+5.2 | ▲i+8.4pp (33/112) · p-0.5pp cap85.3 net+267/med+1.2 | ▼i-4.5pp (29/151) · p+6.3pp cap39.9 net-236/med+4.1 | ▼i-11.0pp (10/63) · p+19.0pp cap46.2 net-417/med-10.4 |
| S0-H12 | keep-watching | — | — | — | — |
| S0-H13 | keep-watching | (°▼i-4.3pp (1/6) · p+59.5pp cap74.2 net+397/med+58.7) | (°▼i-21.1pp (0/2) · p+73.6pp cap116.8 net+181/med+90.7) | (°·i+1.3pp (1/4) · p-21.5pp cap— net-27/med-2.0) | (°▲i+6.4pp (1/3) · p-23.9pp cap— net-22/med+0.9) |
| S0-H14 | keep-watching | ·i-1.5pp (22/113) · p+3.6pp cap50.3 net+312/med+0.5 | ▼i-2.6pp (5/27) · p-11.6pp cap80.6 net-256/med-4.2 | ▲i+6.9pp (26/85) · p+5.6pp cap27.2 net-50/med+1.5 | (°▲i+13.1pp (6/15) · p-3.9pp cap59.0 net-199/med-31.2) |
| S0-H15 | keep-watching | — | — | — | — |
| S0-H16 | keep-watching | (°▼i-21.0pp (0/10) · p-3.8pp cap126.3 net+8/med-16.3) | — | (°▼i-3.7pp (1/5) · p-1.5pp cap44.9 net-8/med+18.0) | — |
| **union coverage** | | 47.3% (52/110) | 33.3% (9/27) | 86.2% (50/58) | 93.8% (15/16) |

Not graded:  — see register entries.

## Hypothesis Cards (page 2)

### H1 — 2 signals
*A climactic bar — extreme volume on a wide spread late in an extended move — marks exhaustion, and price then reverses against the climax direction.*
Grading: directional. Latest review: keep-watching (recommendation).

- Question **Q1-H1**: see the register entry (status there is authoritative).
**S0-H1** — session × window grid (cells as in the matrix):

| session | backtest | forward |
|---|---|---|
| whole | ▼i-2.6pp (9/49) · p+10.9pp cap89.9 net-83/med+0.7 | ·i+0.3pp (12/50) · p+10.5pp cap36.2 net+127/med-1.8 |
| london | (°▼i-21.1pp (0/5) · p+33.6pp cap89.9 net+198/med+39.9) | (°▲i+11.6pp (5/13) · p+14.6pp cap50.3 net+47/med+11.2) |
| overlap | — | (°▲i+7.8pp (1/3) · p+13.9pp cap51.7 net+44/med+28.7) |
| ny_only | (°▼i-19.1pp (0/10) · p+18.8pp cap83.5 net-289/med-3.9) | (°▼i-7.4pp (1/8) · p-6.0pp cap— net-17/med-5.9) |
| dead | (°▲i+3.4pp (2/7) · p+40.7pp cap89.2 net+93/med+34.1) | (°▲i+14.5pp (3/8) · p-13.1pp cap— net-52/med-3.9) |
| asia | ▲i+3.0pp (7/27) · p-6.7pp cap94.2 net-85/med-12.0 | (°▼i-12.0pp (2/18) · p+20.1pp cap25.4 net+105/med+8.4) |

- backtest payoff: right +1327 / wrong -1411 / net -83 pts; median per fire +0.70 (n=49)
- backtest best call: 2026-07-29 03:13 +188.0pts remaining (episode 262.8pts, major)
- backtest worst false alarm: 2026-07-29 19:11 -164.0pts adverse
- forward payoff: right +499 / wrong -372 / net +127 pts; median per fire -1.75 (n=50)
- forward best call: 2026-08-20 04:29 +162.0pts remaining (episode 176.7pts, major)
- forward worst false alarm: 2026-08-20 11:25 -69.6pts adverse
- earliness (backtest): median 97.9 pts of move remaining at fire (n=8)

**S1-H1** — session × window grid (cells as in the matrix):

| session | backtest | forward |
|---|---|---|
| whole | (°▼i-21.0pp (0/3) · p-23.8pp cap— net-72/med-34.2) | (°▲i+26.3pp (1/2) · p-21.5pp cap— net-28/med-14.2) |
| london | (°▼i-21.1pp (0/1) · p-26.4pp cap— net-54/med-53.5) | — |
| overlap | — | — |
| ny_only | — | (°▼i-19.9pp (0/1) · p-6.0pp cap— net-7/med-7.4) |
| dead | — | — |
| asia | (°▼i-22.9pp (0/2) · p-32.6pp cap— net-19/med-9.3) | (°▲i+76.9pp (1/1) · p-35.5pp cap— net-21/med-21.0) |

- backtest payoff: right +16 / wrong -88 / net -72 pts; median per fire -34.20 (n=3)
- backtest worst false alarm: 2026-07-28 10:36 -60.8pts adverse
- forward payoff: right +0 / wrong -28 / net -28 pts; median per fire -14.20 (n=2)
- forward best call: 2026-08-20 04:29 +162.0pts remaining (episode 176.7pts, major)
- forward worst false alarm: 2026-08-20 04:29 -21.0pts adverse

### H2 — 2 signals
*A failed probe beyond a prior extreme — an upthrust above or spring below that closes back inside — reverses against the probe.*
Grading: directional. Latest review: promote-candidate (recommendation).

**S0-H2** — session × window grid (cells as in the matrix):

| session | backtest | forward |
|---|---|---|
| whole | ▼i-7.8pp (31/234) · p+0.6pp cap77.8 net-661/med-5.2 | ·i-1.6pp (31/140) · p+4.2pp cap34.2 net-188/med-1.9 |
| london | (°▼i-7.8pp (2/15) · p-13.1pp cap86.6 net+93/med+9.8) | ·i+1.7pp (8/28) · p-6.0pp cap66.5 net-93/med-11.2 |
| overlap | (°▼i-13.3pp (0/11) · p-14.7pp cap122.7 net-195/med-38.7) | (°·i-0.5pp (2/8) · p-19.4pp cap— net-144/med-26.1) |
| ny_only | ▼i-9.3pp (6/61) · p+11.8pp cap77.4 net-1116/med-16.7 | ▲i+5.1pp (7/28) · p-6.0pp cap— net+9/med-1.9 |
| dead | ▼i-9.8pp (8/52) · p+6.7pp cap90.8 net+604/med+2.2 | (°▼i-4.0pp (4/21) · p+20.2pp cap31.3 net-6/med-1.2) |
| asia | ▼i-7.1pp (15/95) · p-3.1pp cap80.0 net-47/med-10.6 | ▼i-4.9pp (10/55) · p+8.1pp cap28.8 net+46/med+3.0 |

- backtest payoff: right +4896 / wrong -5557 / net -661 pts; median per fire -5.20 (n=234)
- backtest best call: 2026-07-27 03:23 +214.5pts remaining (episode 245.3pts, major)
- backtest worst false alarm: 2026-07-29 19:00 -192.8pts adverse
- forward payoff: right +1186 / wrong -1374 / net -188 pts; median per fire -1.85 (n=140)
- forward best call: 2026-08-21 09:51 +110.5pts remaining (episode 144.6pts, major)
- forward worst false alarm: 2026-08-20 06:15 -106.5pts adverse
- earliness (backtest): median 97.8 pts of move remaining at fire (n=19)

**S1-H2** — session × window grid (cells as in the matrix):

| session | backtest | forward |
|---|---|---|
| whole | ▼i-6.8pp (25/176) · p+2.3pp cap77.4 net-760/med-8.3 | ·i+0.1pp (24/101) · p+7.2pp cap33.1 net+58/med-1.0 |
| london | (°▼i-5.7pp (2/13) · p-11.0pp cap86.6 net+136/med+14.0) | (°▲i+6.4pp (6/18) · p-7.2pp cap83.2 net-23/med-12.2) |
| overlap | (°▼i-13.3pp (0/7) · p-9.5pp cap122.7 net-89/med-38.1) | (°▲i+7.8pp (2/6) · p-19.4pp cap— net-74/med-13.0) |
| ny_only | ▼i-10.2pp (4/45) · p+17.7pp cap77.0 net-1094/med-25.7 | (°·i+1.2pp (4/19) · p-6.0pp cap— net+39/med+1.0) |
| dead | ▼i-10.2pp (6/40) · p+11.1pp cap74.9 net+699/med+7.8 | (°▲i+3.7pp (4/15) · p+26.9pp cap32.2 net+17/med-1.2) |
| asia | ▼i-4.6pp (13/71) · p-5.8pp cap83.8 net-413/med-26.4 | ▼i-4.5pp (8/43) · p+11.0pp cap28.8 net+100/med+3.0 |

- backtest payoff: right +3792 / wrong -4553 / net -760 pts; median per fire -8.35 (n=176)
- backtest best call: 2026-07-29 03:05 +193.7pts remaining (episode 262.8pts, major)
- backtest worst false alarm: 2026-07-29 19:00 -192.8pts adverse
- forward payoff: right +973 / wrong -915 / net +58 pts; median per fire -1.00 (n=101)
- forward best call: 2026-08-21 03:58 +90.8pts remaining (episode 94.3pts, major)
- forward worst false alarm: 2026-08-20 06:15 -106.5pts adverse
- earliness (backtest): median 97.8 pts of move remaining at fire (n=17)

### H3 — 1 signal
*Repeated absorption — high effort with no result — at a price level precedes a breakout through that level.*
Grading: directional. Latest review: keep-watching (recommendation).

**S0-H3** — session × window grid (cells as in the matrix):

| session | backtest | forward |
|---|---|---|
| whole | (°▲i+4.0pp (2/8) · p-11.3pp cap70.3 net-28/med+2.0) | (°▲i+6.3pp (3/10) · p-21.5pp cap— net-26/med-8.2) |
| london | — | (°▼i-26.9pp (0/1) · p-23.9pp cap— net+19/med+18.8) |
| overlap | — | — |
| ny_only | (°▲i+20.9pp (2/5) · p+8.8pp cap70.3 net+132/med+41.2) | (°·i+0.1pp (1/5) · p-6.0pp cap— net-10/med-14.9) |
| dead | — | — |
| asia | (°▼i-22.9pp (0/3) · p-32.6pp cap— net-160/med-56.5) | (°▲i+26.9pp (2/4) · p-35.5pp cap— net-34/med-8.2) |

- backtest payoff: right +132 / wrong -160 / net -28 pts; median per fire +2.00 (n=8)
- backtest best call: 2026-07-27 18:10 +51.7pts remaining (episode 62.9pts)
- backtest worst false alarm: 2026-07-30 01:57 -65.7pts adverse
- forward payoff: right +58 / wrong -84 / net -26 pts; median per fire -8.20 (n=10)
- forward best call: 2026-08-20 19:13 +19.4pts remaining (episode 23.5pts)
- forward worst false alarm: 2026-08-20 00:52 -24.0pts adverse
- earliness (backtest): median 51.7 pts of move remaining at fire (n=1)

### H4 — 1 signal
*In an established trend, a quiet (low-volume) pullback resolves with trend resumption.*
Grading: directional. Latest review: keep-watching (recommendation).

**S0-H4** — session × window grid (cells as in the matrix):

| session | backtest | forward |
|---|---|---|
| whole | ▼i-3.4pp (6/34) · p+5.6pp cap53.4 net+72/med+10.0 | — |
| london | (°▲i+8.9pp (3/10) · p-16.4pp cap50.2 net-30/med-3.7) | — |
| overlap | (°▼i-13.3pp (0/6) · p+9.5pp cap59.3 net-4/med-8.4) | — |
| ny_only | (°▲i+14.2pp (2/6) · p+22.1pp cap25.4 net-9/med+10.8) | — |
| dead | (°·i-0.2pp (1/4) · p+8.6pp cap34.8 net-14/med+32.4) | — |
| asia | (°▼i-22.9pp (0/8) · p+17.4pp cap63.4 net+129/med+17.4) | — |

- backtest payoff: right +556 / wrong -484 / net +72 pts; median per fire +10.00 (n=33)
- backtest best call: 2026-08-03 11:48 +80.2pts remaining (episode 142.0pts, major)
- backtest worst false alarm: 2026-07-26 23:29 -102.8pts adverse
- earliness (backtest): median 71.2 pts of move remaining at fire (n=3)

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

**S0-H6** — session × window grid (cells as in the matrix):

| session | backtest | forward |
|---|---|---|
| whole | ▼i-8.1pp (2/36) · p+3.9pp cap59.3 [cls 35.0%/13.7%i] net-192/med-10.4 | ▲i+25.2pp (28/60) · p-7.7pp cap45.6 [cls 37.7%/21.5%i] net-865/med-10.4 |
| london | (°▼i-4.3pp (1/18) · p-7.4pp cap78.7 [cls 35.2%/9.9%i] net-56/med-10.3) | ▲i+38.1pp (21/34) · p-19.0pp cap53.4 [cls 36.6%/23.7%i] net-879/med-24.9 |
| overlap | (°▼i-13.2pp (0/1) · p+71.6pp cap122.7 [cls 28.4%/13.2%i] net+108/med+108.3) | (°▲i+18.7pp (3/6) · p-3.2pp cap47.6 [cls 19.9%/31.3%i] net-12/med-10.5) |
| ny_only | — | — |
| dead | (°▼i-12.5pp (0/3) · p-25.0pp cap— [cls 25.0%/12.5%i] net+29/med+13.4) | — |
| asia | (°▼i-12.6pp (1/14) · p+19.1pp cap39.1 [cls 38.0%/19.7%i] net-274/med-21.8) | ▲i+3.6pp (4/20) · p+8.4pp cap43.7 [cls 46.6%/16.4%i] net+26/med+3.3 |

- backtest payoff: right +682 / wrong -874 / net -192 pts; median per fire -10.40 (n=36)
- backtest best call: 2026-07-30 06:22 +154.2pts remaining (episode 172.0pts, major)
- backtest worst false alarm: 2026-08-03 07:10 -108.0pts adverse
- forward payoff: right +429 / wrong -1294 / net -865 pts; median per fire -10.45 (n=60)
- forward best call: 2026-08-19 03:31 +81.3pts remaining (episode 94.3pts, major)
- forward worst false alarm: 2026-08-18 07:07 -124.1pts adverse
- earliness (backtest): median 150.2 pts of move remaining at fire (n=2)

### H7 — 1 signal
*Quiet decline at a session extreme is disguised accumulation: effortless (low-volume) weakness reverses UP once selling fails to attract participation (mirror: quiet advance at a high reverses down).*
Grading: directional + either-direction (dual). Latest review: keep-watching (recommendation).

- Question **Q1-H7**: see the register entry (status there is authoritative).
**S0-H7** — session × window grid (cells as in the matrix):

| session | backtest | forward |
|---|---|---|
| whole | ·i-0.7pp (12/59) · p+11.8pp cap97.8 net+761/med+4.2 | ▲i+12.3pp (9/25) · p-5.5pp cap85.5 net-179/med-4.4 |
| london | ▼i-11.1pp (2/20) · p+23.6pp cap86.9 net+719/med+33.0 | (°▲i+17.5pp (8/18) · p-7.2pp cap88.2 net-172/med-4.6) |
| overlap | (°▼i-6.6pp (1/15) · p+22.9pp cap91.3 net+56/med-29.0) | (°▼i-25.5pp (0/2) · p-19.4pp cap— net+11/med+5.5) |
| ny_only | (°▼i-2.4pp (1/6) · p+5.5pp cap101.1 net+59/med+7.7) | (°▲i+5.1pp (1/4) · p-6.0pp cap— net-46/med-15.2) |
| dead | (°▲i+24.8pp (2/4) · p+8.6pp cap128.8 net-15/med-28.8) | — |
| asia | (°▲i+20.0pp (6/14) · p-18.3pp cap99.9 net-58/med-10.2) | (°▼i-23.1pp (0/1) · p+64.5pp cap36.0 net+28/med+27.8) |

- backtest payoff: right +1756 / wrong -995 / net +761 pts; median per fire +4.20 (n=59)
- backtest best call: 2026-07-27 03:04 +247.0pts remaining (episode 245.3pts, major)
- backtest worst false alarm: 2026-07-27 13:57 -91.8pts adverse
- forward payoff: right +275 / wrong -454 / net -179 pts; median per fire -4.40 (n=25)
- forward best call: 2026-08-20 10:49 +65.1pts remaining (episode 83.9pts)
- forward worst false alarm: 2026-08-21 07:20 -80.9pts adverse
- earliness (backtest): median 74.6 pts of move remaining at fire (n=11)

**S0-H7 (either-dir)** — session × window grid (cells as in the matrix):

| session | backtest | forward |
|---|---|---|
| whole | ▼i-5.3pp (20/59) · p+19.3pp cap50.2 | ▲i+7.9pp (13/25) · p+4.3pp cap14.6 |
| london | ▼i-10.2pp (6/20) · p+23.8pp cap57.4 | (°▲i+11.7pp (11/18) · p+10.1pp cap11.6) |
| overlap | (°▼i-19.9pp (1/15) · p+33.2pp cap65.0) | (°▼i-51.0pp (0/2) · p-38.7pp cap—) |
| ny_only | (°·i-0.7pp (2/6) · p+11.4pp cap52.5) | (°▲i+11.0pp (2/4) · p-12.0pp cap—) |
| dead | (°▲i+4.0pp (2/4) · p+43.1pp cap-2.7) | — |
| asia | (°▲i+21.5pp (9/14) · p-16.4pp cap7.9) | (°▼i-42.5pp (0/1) · p+37.6pp cap36.0) |

- backtest payoff: n/a by construction (either-direction)
- backtest best call: 2026-07-27 03:04 +247.0pts remaining (episode 245.3pts, major)
- backtest worst false alarm: 2026-07-29 11:19 -63.7pts adverse
- forward payoff: n/a by construction (either-direction)
- forward best call: 2026-08-18 12:01 +128.8pts remaining (episode 149.0pts, major)
- forward worst false alarm: 2026-08-19 16:29 -39.5pts adverse
- earliness (backtest): median 74.6 pts of move remaining at fire (n=17)

### H8 — 1 signal
*Reversal-signature bar anatomy (upthrust/spring) predicts imminent range expansion irrespective of direction.*
Grading: either-direction. Latest review: keep-watching (recommendation).

**S0-H8** — session × window grid (cells as in the matrix):

| session | backtest | forward |
|---|---|---|
| whole | ▼i-8.4pp (72/234) · p+7.9pp cap35.5 | ·i+0.9pp (63/140) · p+1.0pp cap23.4 |
| london | (°▼i-20.2pp (3/15) · p-31.2pp cap68.2) | ▼i-10.1pp (11/28) · p-9.8pp cap29.6 |
| overlap | (°▼i-17.5pp (1/11) · p+16.8pp cap37.2) | (°▲i+11.5pp (5/8) · p-1.2pp cap9.7) |
| ny_only | ▼i-7.8pp (16/61) · p+32.2pp cap32.0 | ▲i+3.9pp (12/28) · p-12.0pp cap— |
| dead | ▼i-13.3pp (17/52) · p+0.8pp cap53.2 | (°▲i+22.3pp (13/21) · p+27.8pp cap21.6) |
| asia | ▼i-6.0pp (35/95) · p+8.1pp cap29.9 | ▼i-2.5pp (22/55) · p-2.4pp cap24.8 |

- backtest payoff: n/a by construction (either-direction)
- backtest best call: 2026-07-27 03:23 +214.5pts remaining (episode 245.3pts, major)
- backtest worst false alarm: 2026-07-27 16:30 -74.5pts adverse
- forward payoff: n/a by construction (either-direction)
- forward best call: 2026-08-20 04:27 +159.0pts remaining (episode 176.7pts, major)
- forward worst false alarm: 2026-08-18 09:32 -59.6pts adverse
- earliness (backtest): median 80.1 pts of move remaining at fire (n=27)

### H9 — 2 signals
*Persistent lower-TF directional pressure that recruits expanding participation at the parent timeframe precedes continuation beyond what the parent label alone predicts; pressure without participation expansion does not.*
Grading: directional. Latest review: keep-watching (recommendation).

**S0-H9** — session × window grid (cells as in the matrix):

| session | backtest | forward |
|---|---|---|
| whole | ▲i+4.0pp (13/52) · p-8.4pp cap55.5 net-426/med-4.1 | (°▲i+16.3pp (4/10) · p-21.5pp cap— net-210/med-6.6) |
| london | (°▼i-21.1pp (0/3) · p-26.4pp cap— net+17/med+22.6) | (°▲i+23.1pp (1/2) · p-23.9pp cap— net-158/med-78.9) |
| overlap | (°▼i-13.3pp (0/2) · p-23.8pp cap— net+112/med+55.8) | (°▼i-25.5pp (0/1) · p-19.4pp cap— net-18/med-17.7) |
| ny_only | ▲i+12.7pp (7/22) · p-6.7pp cap32.0 net-517/med-19.3 | (°▲i+20.1pp (2/5) · p-6.0pp cap— net-24/med-2.6) |
| dead | (°·i-0.2pp (3/12) · p+16.9pp cap101.1 net+200/med+3.0) | (°▲i+77.0pp (1/1) · p-13.1pp cap— net-5/med-5.3) |
| asia | (°·i+0.2pp (3/13) · p-9.5pp cap49.0 net-238/med-8.5) | (°▼i-23.1pp (0/1) · p-35.5pp cap— net-6/med-5.5) |

- backtest payoff: right +725 / wrong -1151 / net -426 pts; median per fire -4.10 (n=51)
- backtest best call: 2026-07-31 05:00 +184.4pts remaining (episode 184.2pts, major)
- backtest worst false alarm: 2026-07-29 18:45 -160.1pts adverse
- forward payoff: right +21 / wrong -231 / net -210 pts; median per fire -6.60 (n=10)
- forward best call: 2026-08-17 16:10 +57.7pts remaining (episode 67.4pts)
- forward worst false alarm: 2026-08-18 07:00 -118.4pts adverse
- earliness (backtest): median 70.2 pts of move remaining at fire (n=7)

**S1-H9** — session × window grid (cells as in the matrix):

| session | backtest | forward |
|---|---|---|
| whole | (°▼i-21.0pp (0/8) · p+26.2pp cap101.1 net-53/med+13.1) | (°▲i+43.0pp (2/3) · p-21.5pp cap— net-127/med-7.7) |
| london | — | (°▲i+73.1pp (1/1) · p-23.9pp cap— net-114/med-114.2) |
| overlap | (°▼i-13.3pp (0/1) · p-23.8pp cap— net+56/med+55.8) | — |
| ny_only | (°▼i-19.1pp (0/2) · p-11.2pp cap— net-320/med-160.1) | (°▼i-19.9pp (0/1) · p-6.0pp cap— net-8/med-7.7) |
| dead | (°▼i-25.2pp (0/5) · p+63.6pp cap101.1 net+211/med+19.4) | (°▲i+77.0pp (1/1) · p-13.1pp cap— net-5/med-5.3) |
| asia | — | — |

- backtest payoff: right +294 / wrong -348 / net -53 pts; median per fire +13.05 (n=8)
- backtest worst false alarm: 2026-07-29 18:45 -160.1pts adverse
- forward payoff: right +0 / wrong -127 / net -127 pts; median per fire -7.70 (n=3)
- forward best call: 2026-08-20 22:55 +25.2pts remaining (episode 31.1pts)
- forward worst false alarm: 2026-08-18 07:00 -118.4pts adverse

### H10 — 1 signal
*In an established 1-minute trend, no-demand/no-supply prints in the trend's direction signal continuation.*
Grading: directional. Latest review: deprioritize (recommendation).

**S0-H10** — session × window grid (cells as in the matrix):

| session | backtest | forward |
|---|---|---|
| whole | ▲i+4.9pp (38/147) · p-4.1pp cap49.6 net-391/med+3.2 | ▲i+2.5pp (21/80) · p+2.3pp cap28.9 net+169/med+3.0 |
| london | ▲i+2.0pp (9/39) · p-16.1pp cap80.6 net-463/med-12.5 | (°▲i+6.4pp (5/15) · p+2.8pp cap42.4 net+73/med+17.1) |
| overlap | (°▼i-13.3pp (0/9) · p-1.6pp cap59.5 net-114/med-21.0) | (°▲i+12.0pp (3/8) · p-6.9pp cap47.7 net+50/med+4.8) |
| ny_only | ▼i-4.4pp (5/34) · p+3.5pp cap46.4 net+237/med+4.4 | ▼i-4.9pp (3/20) · p+14.0pp cap21.4 net+84/med+6.4 |
| dead | (°▲i+3.4pp (4/14) · p-16.4pp cap— net-275/med-13.8) | (°·i-0.8pp (2/9) · p-13.1pp cap— net+9/med+1.5) |
| asia | ▲i+16.3pp (20/51) · p+2.7pp cap47.5 net+224/med+6.3 | ▲i+5.5pp (8/28) · p+0.2pp cap28.3 net-48/med-5.2 |

- backtest payoff: right +1730 / wrong -2121 / net -391 pts; median per fire +3.20 (n=147)
- backtest best call: 2026-07-27 03:28 +219.3pts remaining (episode 245.3pts, major)
- backtest worst false alarm: 2026-07-26 23:29 -102.8pts adverse
- forward payoff: right +701 / wrong -532 / net +169 pts; median per fire +3.00 (n=79)
- forward best call: 2026-08-21 04:12 +83.0pts remaining (episode 94.3pts, major)
- forward worst false alarm: 2026-08-17 09:56 -79.5pts adverse
- earliness (backtest): median 83.8 pts of move remaining at fire (n=10)

### H11 — 2 signals
*Price entering a low-volume price zone traverses it faster than baseline; entering a high-volume node it stalls or reverses at above-baseline rates.*
Grading: directional. Latest review: keep-watching (recommendation).

**S0-H11** — session × window grid (cells as in the matrix):

| session | backtest | forward |
|---|---|---|
| whole | ·i-0.7pp (15/74) · p-3.5pp cap68.3 net-452/med-6.0 | ▼i-4.9pp (34/181) · p+0.6pp cap45.2 net-416/med-5.5 |
| london | (°▼i-21.1pp (0/14) · p-5.0pp cap73.1 net-472/med-58.8) | ·i+0.9pp (27/97) · p-5.3pp cap53.4 net-220/med-3.0 |
| overlap | (°·i-0.8pp (2/16) · p-17.6pp cap68.3 net-166/med-13.2) | (°▼i-25.5pp (0/9) · p-19.4pp cap— net+10/med-1.1) |
| ny_only | (°▼i-19.1pp (0/4) · p-11.2pp cap— net-18/med-18.5) | (°▲i+13.4pp (2/6) · p-6.0pp cap— net-54/med-24.1) |
| dead | (°▲i+17.7pp (3/7) · p-2.1pp cap52.6 net+1/med+4.1) | (°▼i-14.7pp (1/12) · p+3.6pp cap17.5 net-33/med-0.5) |
| asia | ▲i+7.4pp (10/33) · p-2.3pp cap64.5 net+203/med-1.1 | ▼i-16.1pp (4/57) · p-0.4pp cap37.1 net-119/med-6.1 |

- backtest payoff: right +1359 / wrong -1811 / net -452 pts; median per fire -5.95 (n=74)
- backtest best call: 2026-07-29 04:03 +262.2pts remaining (episode 262.8pts, major)
- backtest worst false alarm: 2026-07-31 07:03 -171.6pts adverse
- forward payoff: right +1958 / wrong -2373 / net -416 pts; median per fire -5.50 (n=181)
- forward best call: 2026-08-21 09:38 +105.1pts remaining (episode 144.6pts, major)
- forward worst false alarm: 2026-08-20 07:09 -100.4pts adverse
- earliness (backtest): median 104.9 pts of move remaining at fire (n=8)

**S1-H11** — session × window grid (cells as in the matrix):

| session | backtest | forward |
|---|---|---|
| whole | ·i-0.1pp (63/301) · p+6.1pp cap82.4 net+1221/med+5.2 | ▼i-4.5pp (29/151) · p+6.3pp cap39.9 net-236/med+4.1 |
| london | ▲i+8.4pp (33/112) · p-0.5pp cap85.3 net+267/med+1.2 | ▼i-11.0pp (10/63) · p+19.0pp cap46.2 net-417/med-10.4 |
| overlap | ▼i-3.3pp (2/20) · p-13.8pp cap84.7 net+3/med+13.2 | (°▼i-2.4pp (6/26) · p+7.5pp cap40.4 net+87/med+3.4) |
| ny_only | ▼i-10.6pp (4/47) · p+10.1pp cap83.3 net+89/med+1.0 | ▲i+7.1pp (10/37) · p-6.0pp cap— net+104/med+2.0 |
| dead | ▲i+10.1pp (12/34) · p+7.1pp cap86.7 net+169/med+5.3 | (°▼i-17.1pp (1/17) · p+10.4pp cap19.6 net+156/med+6.8) |
| asia | ▼i-9.3pp (12/88) · p+14.0pp cap82.1 net+693/med+16.2 | (°·i+1.9pp (2/8) · p+14.5pp cap16.9 net-166/med+0.5) |

- backtest payoff: right +7407 / wrong -6186 / net +1221 pts; median per fire +5.20 (n=301)
- backtest best call: 2026-07-30 00:35 +150.2pts remaining (episode 237.6pts, major)
- backtest worst false alarm: 2026-07-29 19:32 -168.0pts adverse
- forward payoff: right +1585 / wrong -1821 / net -236 pts; median per fire +4.10 (n=151)
- forward best call: 2026-08-19 23:11 +72.9pts remaining (episode 72.3pts, major)
- forward worst false alarm: 2026-08-20 06:33 -145.0pts adverse
- earliness (backtest): median 58.0 pts of move remaining at fire (n=21)

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
| whole | (°▼i-4.3pp (1/6) · p+59.5pp cap74.2 net+397/med+58.7) | (°·i+1.3pp (1/4) · p-21.5pp cap— net-27/med-2.0) |
| london | (°▼i-21.1pp (0/2) · p+73.6pp cap116.8 net+181/med+90.7) | (°▲i+6.4pp (1/3) · p-23.9pp cap— net-22/med+0.9) |
| overlap | — | — |
| ny_only | — | (°▼i-19.9pp (0/1) · p-6.0pp cap— net-5/med-5.0) |
| dead | (°▼i-25.2pp (0/1) · p+83.6pp cap74.2 net+51/med+51.0) | — |
| asia | (°▲i+10.4pp (1/3) · p+34.1pp cap78.8 net+164/med+56.1) | — |

- backtest payoff: right +397 / wrong +0 / net +397 pts; median per fire +58.70 (n=6)
- backtest best call: 2026-07-28 02:15 +115.9pts remaining (episode 109.7pts, major)
- backtest worst false alarm: 2026-07-28 02:15 -2.8pts adverse
- forward payoff: right +13 / wrong -40 / net -27 pts; median per fire -2.05 (n=4)
- forward best call: 2026-08-21 09:44 +113.7pts remaining (episode 144.6pts, major)
- forward worst false alarm: 2026-08-21 09:44 -41.4pts adverse
- earliness (backtest): median 115.9 pts of move remaining at fire (n=1)

### H14 — 1 signal
*Counter-trend No Demand / No Supply prints in an established trend mark absorption and precede trend continuation.*
Grading: directional. Latest review: keep-watching (recommendation).

**S0-H14** — session × window grid (cells as in the matrix):

| session | backtest | forward |
|---|---|---|
| whole | ·i-1.5pp (22/113) · p+3.6pp cap50.3 net+312/med+0.5 | ▲i+6.9pp (26/85) · p+5.6pp cap27.2 net-50/med+1.5 |
| london | ▼i-2.6pp (5/27) · p-11.6pp cap80.6 net-256/med-4.2 | (°▲i+13.1pp (6/15) · p-3.9pp cap59.0 net-199/med-31.2) |
| overlap | (°▼i-13.3pp (0/11) · p-23.8pp cap— net-138/med-20.3) | (°▲i+24.5pp (5/10) · p+10.6pp cap50.3 net-2/med-8.2) |
| ny_only | ▼i-14.8pp (1/23) · p+23.6pp cap43.2 net+392/med+21.1 | (°▼i-8.8pp (2/18) · p+16.2pp cap20.4 net+78/med+5.5) |
| dead | (°▲i+19.2pp (4/9) · p-16.4pp cap— net-178/med-20.1) | (°▲i+13.4pp (4/11) · p-13.1pp cap— net+35/med+3.0) |
| asia | ▲i+5.0pp (12/43) · p+11.6pp cap58.5 net+492/med+8.2 | ▲i+5.9pp (9/31) · p+6.4pp cap23.5 net+39/med+1.4 |

- backtest payoff: right +1733 / wrong -1421 / net +312 pts; median per fire +0.50 (n=113)
- backtest best call: 2026-07-31 04:56 +164.7pts remaining (episode 169.2pts, major)
- backtest worst false alarm: 2026-07-28 09:44 -94.3pts adverse
- forward payoff: right +734 / wrong -783 / net -50 pts; median per fire +1.50 (n=85)
- forward best call: 2026-08-21 04:05 +84.8pts remaining (episode 94.3pts, major)
- forward worst false alarm: 2026-08-17 09:54 -87.2pts adverse
- earliness (backtest): median 78.0 pts of move remaining at fire (n=6)

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
| whole | (°▼i-21.0pp (0/10) · p-3.8pp cap126.3 net+8/med-16.3) | (°▼i-3.7pp (1/5) · p-1.5pp cap44.9 net-8/med+18.0) |
| london | — | — |
| overlap | (°▼i-13.3pp (0/10) · p-3.8pp cap126.3 net+8/med-16.3) | (°▼i-5.5pp (1/5) · p+0.6pp cap44.9 net-8/med+18.0) |
| ny_only | — | — |
| dead | — | — |
| asia | — | — |

- backtest payoff: right +262 / wrong -254 / net +8 pts; median per fire -16.30 (n=10)
- backtest worst false alarm: 2026-07-27 15:00 -114.5pts adverse
- forward payoff: right +70 / wrong -79 / net -8 pts; median per fire +18.00 (n=5)
- forward best call: 2026-08-20 15:00 +43.7pts remaining (episode 52.1pts)
- forward worst false alarm: 2026-08-17 15:00 -54.6pts adverse


---

# nas100 (nas100fut) — PROVISIONAL

> **PROVISIONAL — validation pending (register 40 fence as amended 2026-08-19): replay-only study over the synced store; canonical status, live attachment, and Asia/pause-sensitive cell interpretation await this instrument's validation evening. EXPLORATORY first cross-instrument look — expectations deliberately unregistered; anything interesting becomes a pre-registered question before it becomes a claim. NO POOLING across instruments.**
>
> - drift-adjustment segments and engine tod baselines run on the provider/London trading-day structure; native cash-hour segmentation is part of this instrument's validation evening
> - sessions = the registered register-37 world-clock partition (native-tz, DST-proof) applied to this instrument's own bars; 'london' is not the home session of the US pairs
> - the forward window (>= go_live) is also a replay over the synced store — this instrument has NO live attachment yet

Store span (1M, close ts): 2026-07-19 22:02:00+00:00 → 2026-08-21 20:29:00+00:00. Volume type: real futures volume (register 40 first-sync sanity; canonical verdict at this instrument's validation evening).

## Summary Matrix (page 1)

Engine `01e9d5694` — OBSERVATIONAL signal scoreboard - move-detection, not trading; no fills exist here by construction; never validation (docs/hypothesis_lifecycle.md stage 4)

**Review labels are RECOMMENDATIONS — none actioned, review pending operator familiarity.** Cells: marker + precision LIFT vs that context's OWN chance rate, (hits/fires), payoff net/median points (directional rows; either-direction rows have no payoff by construction). ▲/▼ = beyond ±2pp of chance, · = within. (°…) = small-n (fires<20 or episodes<10): dimmed, excluded from any future label arithmetic. Read READING_GUIDE.md first; full detail in hypothesis_performance.json.

| H | label | backtest whole | backtest london | forward whole | forward london |
|---|---|---|---|---|---|
| *context* | | 114 ep; chance 22.0%dir/41.6%either | 41 ep; chance 30.9%dir/56.1%either | 56 ep; chance 21.3%dir/40.7%either | 17 ep; chance 32.6%dir/62.1%either |
| S0-H1 | keep-watching | ▲i+4.8pp (9/34) · p+16.2pp cap184.4 net+122/med-15.7 | (°▲i+11.7pp (3/8) · p-18.4pp cap153.6 net-257/med-46.2) | ▲i+14.6pp (13/35) · p+15.8pp cap74.9 net+289/med+18.4 | ▲i+11.3pp (8/20) · p+2.4pp cap96.9 net-27/med+7.8 |
| S1-H1 | keep-watching | (°▲i+11.6pp (1/3) · p+44.7pp cap279.0 net+465/med+128.4) | — | (°▼i-22.5pp (0/1) · p+78.7pp cap74.3 net+74/med+74.3) | (°▼i-28.7pp (0/1) · p+67.4pp cap74.3 net+74/med+74.3) |
| S0-H2 | promote-candidate | ▼i-3.3pp (59/320) · p-2.3pp cap157.6 net-3528/med-1.4 | ·i+1.3pp (16/59) · p-5.5pp cap106.7 net-313/med-30.0 | ·i-1.9pp (45/218) · p+9.4pp cap75.1 net-61/med-1.9 | ▼i-2.6pp (23/88) · p+3.8pp cap88.0 net+291/med+2.6 |
| S1-H2 | promote-candidate | ▼i-2.8pp (42/222) · p-1.7pp cap144.4 net-1379/med-4.2 | ▲i+4.4pp (13/43) · p-3.0pp cap101.9 net-382/med-31.5 | ·i+1.1pp (37/157) · p+9.3pp cap74.4 net-6/med+3.5 | ▲i+3.0pp (19/60) · p-0.9pp cap85.6 net-74/med+2.6 |
| S0-H3 | keep-watching | (°▼i-21.7pp (0/1) · p+78.0pp cap105.8 net+106/med+105.8) | (°▼i-25.8pp (0/1) · p+69.1pp cap105.8 net+106/med+105.8) | — | — |
| S0-H4 | keep-watching | — | — | (°▼i-22.5pp (0/10) · p+38.7pp cap38.4 net-18/med-7.4) | (°▼i-28.7pp (0/5) · p+7.4pp cap31.1 net+26/med+9.5) |
| S0-H5 | keep-watching | — | — | — | — |
| S0-H6 | keep-watching | ▲i+4.4pp (5/29) · p-8.2pp cap260.8 [cls 39.2%/12.8%i] net-232/med-11.8 | (°▲i+60.2pp (4/5) · p-38.7pp cap— [cls 38.7%/19.8%i] net-719/med-105.3) | ▼i-5.6pp (5/44) · p+3.0pp cap97.4 [cls 35.6%/17.0%i] net+403/med-1.9 | (°▲i+4.1pp (4/13) · p+3.6pp cap90.7 [cls 34.9%/26.7%i] net+354/med+16.3) |
| S0-H7 | keep-watching | ▼i-5.7pp (8/50) · p+0.0pp cap169.0 net+77/med-7.8 | (°·i-0.8pp (4/16) · p-5.9pp cap123.6 net-167/med-6.6) | ▲i+2.5pp (10/40) · p+3.7pp cap101.6 net+273/med+10.8 | (°▲i+17.5pp (6/13) · p-9.5pp cap105.7 net+18/med-19.6) |
| S0-H7 (either-dir) | keep-watching | ▼i-10.5pp (15/50) · p+4.4pp cap46.5 | (°▲i+2.2pp (8/16) · p+0.1pp cap23.3) | ▼i-2.2pp (16/40) · p+11.8pp cap47.3 | (°▲i+4.4pp (8/13) · p+7.1pp cap44.5) |
| S0-H8 | keep-watching | ▼i-3.9pp (117/320) · p+1.8pp cap65.1 | ▼i-7.1pp (24/59) · p+4.9pp cap53.7 | ▲i+6.4pp (106/218) · p+10.7pp cap56.8 | ▲i+5.4pp (55/88) · p-1.9pp cap68.3 |
| S0-H9 | keep-watching | ▲i+2.2pp (21/88) · p+0.7pp cap129.2 net+593/med-4.3 | (°▼i-25.8pp (0/9) · p+2.4pp cap76.3 net+410/med+11.6) | ▼i-6.6pp (11/69) · p-6.8pp cap62.5 net-613/med-9.9 | (°▲i+21.3pp (2/4) · p+17.4pp cap57.7 net-462/med-132.2) |
| S1-H9 | keep-watching | ▼i-13.7pp (2/25) · p+6.0pp cap265.9 net-373/med+10.8 | (°▼i-25.8pp (0/5) · p-30.9pp cap— net-57/med+2.3) | (°▲i+20.4pp (3/7) · p-7.0pp cap52.5 net-557/med-25.7) | (°▲i+71.3pp (2/2) · p-32.6pp cap— net-493/med-246.5) |
| S0-H10 | deprioritize | ·i-0.6pp (37/175) · p-6.0pp cap92.8 net+2743/med+15.3 | (°▼i-12.5pp (2/15) · p-17.6pp cap46.2 net-356/med-1.7) | ▼i-15.6pp (10/145) · p-2.7pp cap49.8 net-1420/med-8.1 | ▼i-15.7pp (3/23) · p+10.9pp cap47.8 net+79/med-0.6 |
| S0-H11 | keep-watching | ▼i-3.4pp (48/263) · p+2.3pp cap136.1 net+863/med+0.9 | ·i-1.6pp (22/91) · p-2.3pp cap113.7 net+264/med-3.9 | ▼i-2.4pp (34/169) · p+2.4pp cap76.8 net+1035/med+2.4 | ▲i+10.0pp (12/31) · p-0.3pp cap175.6 net+564/med-2.6 |
| S1-H11 | keep-watching | ▼i-8.5pp (23/174) · p+5.0pp cap130.1 net+293/med-14.1 | ·i+0.6pp (14/53) · p-2.6pp cap109.7 net-436/med-14.7 | ▲i+9.5pp (48/150) · p+1.4pp cap88.4 net-712/med-0.9 | ·i+0.6pp (12/41) · p-0.9pp cap109.8 net-434/med-2.5 |
| S0-H12 | keep-watching | — | — | — | — |
| S0-H13 | keep-watching | (°▼i-21.7pp (0/1) · p+78.0pp cap95.7 net+93/med+93.0) | (°▼i-25.8pp (0/1) · p+69.1pp cap95.7 net+93/med+93.0) | — | — |
| S0-H14 | keep-watching | ·i+0.5pp (37/167) · p-13.6pp cap70.2 net-692/med+6.9 | ▼i-10.4pp (4/26) · p-19.4pp cap41.8 net-1762/med-17.1 | ▼i-18.5pp (6/149) · p-3.2pp cap52.7 net-694/med-5.7 | ▼i-28.7pp (0/20) · p+12.4pp cap74.6 net+552/med+14.1 |
| S0-H15 | keep-watching | — | — | — | — |
| S0-H16 | keep-watching | (°▼i-11.7pp (1/10) · p+28.0pp cap121.0 net+274/med+0.1) | — | (°▼i-5.8pp (1/6) · p-4.6pp cap53.5 net+109/med+21.2) | — |
| **union coverage** | | 45.6% (52/114) | 39.0% (16/41) | 91.1% (51/56) | 94.1% (16/17) |

Not graded:  — see register entries.

## Hypothesis Cards (page 2)

### H1 — 2 signals
*A climactic bar — extreme volume on a wide spread late in an extended move — marks exhaustion, and price then reverses against the climax direction.*
Grading: directional. Latest review: keep-watching (recommendation).

- Question **Q1-H1**: see the register entry (status there is authoritative).
**S0-H1** — session × window grid (cells as in the matrix):

| session | backtest | forward |
|---|---|---|
| whole | ▲i+4.8pp (9/34) · p+16.2pp cap184.4 net+122/med-15.7 | ▲i+14.6pp (13/35) · p+15.8pp cap74.9 net+289/med+18.4 |
| london | (°▲i+11.7pp (3/8) · p-18.4pp cap153.6 net-257/med-46.2) | ▲i+11.3pp (8/20) · p+2.4pp cap96.9 net-27/med+7.8 |
| overlap | — | — |
| ny_only | (°·i-1.8pp (2/11) · p+41.6pp cap291.5 net-215/med-87.5) | (°▲i+48.6pp (2/3) · p-5.4pp cap— net+35/med+22.6) |
| dead | (°▲i+31.2pp (4/8) · p+1.0pp cap406.7 net-181/med-23.6) | (°▲i+14.2pp (3/8) · p+50.5pp cap68.4 net+263/med+44.3) |
| asia | (°▼i-24.3pp (0/7) · p+51.6pp cap178.9 net+776/med+154.4) | (°▼i-25.7pp (0/4) · p+1.9pp cap74.9 net+17/med+11.8) |

- backtest payoff: right +2899 / wrong -2777 / net +122 pts; median per fire -15.65 (n=34)
- backtest best call: 2026-07-29 18:02 +663.1pts remaining (episode 667.1pts, major)
- backtest worst false alarm: 2026-07-29 19:01 -712.5pts adverse
- forward payoff: right +1144 / wrong -855 / net +289 pts; median per fire +18.40 (n=35)
- forward best call: 2026-08-20 09:43 +293.2pts remaining (episode 306.7pts, major)
- forward worst false alarm: 2026-08-20 11:25 -184.0pts adverse
- earliness (backtest): median 183.0 pts of move remaining at fire (n=8)

**S1-H1** — session × window grid (cells as in the matrix):

| session | backtest | forward |
|---|---|---|
| whole | (°▲i+11.6pp (1/3) · p+44.7pp cap279.0 net+465/med+128.4) | (°▼i-22.5pp (0/1) · p+78.7pp cap74.3 net+74/med+74.3) |
| london | — | (°▼i-28.7pp (0/1) · p+67.4pp cap74.3 net+74/med+74.3) |
| overlap | — | — |
| ny_only | — | — |
| dead | (°▲i+31.2pp (1/2) · p+38.5pp cap406.7 net+337/med+168.5) | — |
| asia | (°▼i-24.3pp (0/1) · p+80.2pp cap151.3 net+128/med+128.4) | — |

- backtest payoff: right +521 / wrong -56 / net +465 pts; median per fire +128.40 (n=3)
- backtest best call: 2026-07-28 23:45 +372.3pts remaining (episode 501.5pts, major)
- backtest worst false alarm: 2026-07-28 23:45 -141.6pts adverse
- forward payoff: right +74 / wrong +0 / net +74 pts; median per fire +74.30 (n=1)
- earliness (backtest): median 372.3 pts of move remaining at fire (n=1)

### H2 — 2 signals
*A failed probe beyond a prior extreme — an upthrust above or spring below that closes back inside — reverses against the probe.*
Grading: directional. Latest review: promote-candidate (recommendation).

**S0-H2** — session × window grid (cells as in the matrix):

| session | backtest | forward |
|---|---|---|
| whole | ▼i-3.3pp (59/320) · p-2.3pp cap157.6 net-3528/med-1.4 | ·i-1.9pp (45/218) · p+9.4pp cap75.1 net-61/med-1.9 |
| london | ·i+1.3pp (16/59) · p-5.5pp cap106.7 net-313/med-30.0 | ▼i-2.6pp (23/88) · p+3.8pp cap88.0 net+291/med+2.6 |
| overlap | (°▼i-4.8pp (1/32) · p-12.5pp cap193.4 net-742/med-38.1) | (°▼i-2.9pp (0/12) · p-25.9pp cap153.4 net-208/med-3.8) |
| ny_only | ▼i-10.1pp (7/71) · p+2.6pp cap234.9 net-3199/med-7.4 | (°▲i+19.4pp (6/16) · p+0.8pp cap85.5 net+15/med+2.8) |
| dead | ·i+0.0pp (9/48) · p+5.2pp cap284.2 net+874/med+2.4 | (°▲i+10.0pp (5/15) · p+28.0pp cap71.3 net+44/med+4.5) |
| asia | ·i-0.7pp (26/110) · p-0.7pp cap116.8 net-147/med+10.2 | ▼i-13.1pp (11/87) · p+7.9pp cap60.8 net-204/med-4.4 |

- backtest payoff: right +13405 / wrong -16933 / net -3528 pts; median per fire -1.35 (n=320)
- backtest best call: 2026-07-30 07:00 +812.7pts remaining (episode 832.8pts, major)
- backtest worst false alarm: 2026-07-29 19:00 -719.1pts adverse
- forward payoff: right +5254 / wrong -5315 / net -61 pts; median per fire -1.85 (n=218)
- forward best call: 2026-08-21 11:28 +288.7pts remaining (episode 309.6pts, major)
- forward worst false alarm: 2026-08-19 12:55 -322.0pts adverse
- earliness (backtest): median 107.8 pts of move remaining at fire (n=25)

**S1-H2** — session × window grid (cells as in the matrix):

| session | backtest | forward |
|---|---|---|
| whole | ▼i-2.8pp (42/222) · p-1.7pp cap144.4 net-1379/med-4.2 | ·i+1.1pp (37/157) · p+9.3pp cap74.4 net-6/med+3.5 |
| london | ▲i+4.4pp (13/43) · p-3.0pp cap101.9 net-382/med-31.5 | ▲i+3.0pp (19/60) · p-0.9pp cap85.6 net-74/med+2.6 |
| overlap | (°▼i-7.9pp (0/20) · p-2.5pp cap185.1 net+164/med+49.0) | (°▼i-2.9pp (0/10) · p-24.2pp cap153.4 net-118/med-3.8) |
| ny_only | ▼i-11.7pp (4/48) · p-0.4pp cap194.2 net-1585/med-19.9 | (°▲i+27.4pp (5/11) · p+3.7pp cap85.5 net+70/med+14.5) |
| dead | ▲i+2.4pp (7/33) · p+0.6pp cap206.8 net+152/med-7.9 | (°▲i+6.7pp (3/10) · p+18.0pp cap80.9 net-9/med+3.1) |
| asia | ·i-1.2pp (18/78) · p+0.7pp cap108.5 net+272/med+15.2 | ▼i-10.5pp (10/66) · p+13.3pp cap62.2 net+126/med+5.0 |

- backtest payoff: right +8973 / wrong -10352 / net -1379 pts; median per fire -4.15 (n=222)
- backtest best call: 2026-07-30 07:00 +812.7pts remaining (episode 832.8pts, major)
- backtest worst false alarm: 2026-07-29 19:16 -700.8pts adverse
- forward payoff: right +3652 / wrong -3658 / net -6 pts; median per fire +3.50 (n=157)
- forward best call: 2026-08-21 11:28 +288.7pts remaining (episode 309.6pts, major)
- forward worst false alarm: 2026-08-19 13:09 -291.0pts adverse
- earliness (backtest): median 118.9 pts of move remaining at fire (n=23)

### H3 — 1 signal
*Repeated absorption — high effort with no result — at a price level precedes a breakout through that level.*
Grading: directional. Latest review: keep-watching (recommendation).

**S0-H3** — session × window grid (cells as in the matrix):

| session | backtest | forward |
|---|---|---|
| whole | (°▼i-21.7pp (0/1) · p+78.0pp cap105.8 net+106/med+105.8) | — |
| london | (°▼i-25.8pp (0/1) · p+69.1pp cap105.8 net+106/med+105.8) | — |
| overlap | — | — |
| ny_only | — | — |
| dead | — | — |
| asia | — | — |

- backtest payoff: right +106 / wrong +0 / net +106 pts; median per fire +105.80 (n=1)

### H4 — 1 signal
*In an established trend, a quiet (low-volume) pullback resolves with trend resumption.*
Grading: directional. Latest review: keep-watching (recommendation).

**S0-H4** — session × window grid (cells as in the matrix):

| session | backtest | forward |
|---|---|---|
| whole | — | (°▼i-22.5pp (0/10) · p+38.7pp cap38.4 net-18/med-7.4) |
| london | — | (°▼i-28.7pp (0/5) · p+7.4pp cap31.1 net+26/med+9.5) |
| overlap | — | — |
| ny_only | — | — |
| dead | — | — |
| asia | — | (°▼i-25.7pp (0/5) · p+56.9pp cap44.3 net-44/med-8.1) |

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

**S0-H6** — session × window grid (cells as in the matrix):

| session | backtest | forward |
|---|---|---|
| whole | ▲i+4.4pp (5/29) · p-8.2pp cap260.8 [cls 39.2%/12.8%i] net-232/med-11.8 | ▼i-5.6pp (5/44) · p+3.0pp cap97.4 [cls 35.6%/17.0%i] net+403/med-1.9 |
| london | (°▲i+60.2pp (4/5) · p-38.7pp cap— [cls 38.7%/19.8%i] net-719/med-105.3) | (°▲i+4.1pp (4/13) · p+3.6pp cap90.7 [cls 34.9%/26.7%i] net+354/med+16.3) |
| overlap | (°·i-1.8pp (1/20) · p-7.3pp cap263.9 [cls 47.3%/6.8%i] net+333/med+9.0) | (°▼i-3.9pp (0/22) · p+0.6pp cap100.2 [cls 44.9%/3.9%i] net+230/med-1.9) |
| ny_only | — | (°▼i-10.0pp (0/1) · p+0.0pp cap— [cls 0.0%/10.0%i] net-31/med-30.7) |
| dead | (°▼i-13.5pp (0/3) · p-23.8pp cap— [cls 23.8%/13.5%i] net+42/med+18.9) | (°▼i-23.1pp (0/1) · p-19.2pp cap— [cls 19.2%/23.1%i] net+16/med+15.9) |
| asia | (°▼i-17.8pp (0/1) · p+75.0pp cap129.0 [cls 25.0%/17.8%i] net+112/med+111.8) | (°▼i-5.9pp (1/7) · p+1.6pp cap94.1 [cls 27.0%/20.2%i] net-167/med-69.2) |

- backtest payoff: right +1875 / wrong -2108 / net -232 pts; median per fire -11.80 (n=29)
- backtest best call: 2026-08-03 11:04 +303.5pts remaining (episode 396.3pts, major)
- backtest worst false alarm: 2026-07-27 13:46 -514.5pts adverse
- forward payoff: right +1556 / wrong -1153 / net +403 pts; median per fire -1.90 (n=44)
- forward best call: 2026-08-17 09:59 +125.3pts remaining (episode 181.2pts, major)
- forward worst false alarm: 2026-08-18 13:40 -161.0pts adverse
- earliness (backtest): median 78.8 pts of move remaining at fire (n=2)

### H7 — 1 signal
*Quiet decline at a session extreme is disguised accumulation: effortless (low-volume) weakness reverses UP once selling fails to attract participation (mirror: quiet advance at a high reverses down).*
Grading: directional + either-direction (dual). Latest review: keep-watching (recommendation).

- Question **Q1-H7**: see the register entry (status there is authoritative).
**S0-H7** — session × window grid (cells as in the matrix):

| session | backtest | forward |
|---|---|---|
| whole | ▼i-5.7pp (8/50) · p+0.0pp cap169.0 net+77/med-7.8 | ▲i+2.5pp (10/40) · p+3.7pp cap101.6 net+273/med+10.8 |
| london | (°·i-0.8pp (4/16) · p-5.9pp cap123.6 net-167/med-6.6) | (°▲i+17.5pp (6/13) · p-9.5pp cap105.7 net+18/med-19.6) |
| overlap | (°▲i+4.6pp (1/8) · p+25.0pp cap183.1 net+464/med+8.3) | (°▼i-2.9pp (0/8) · p+15.8pp cap115.7 net+99/med+26.9) |
| ny_only | (°▲i+5.0pp (2/8) · p-12.9pp cap— net-76/med-18.5) | (°▼i-18.1pp (0/7) · p-5.4pp cap— net+114/med+23.8) |
| dead | (°·i+1.2pp (1/5) · p-11.5pp cap— net+53/med+23.0) | (°▲i+10.0pp (1/3) · p-12.0pp cap— net+71/med+21.8) |
| asia | (°▼i-24.3pp (0/13) · p-4.4pp cap142.4 net-196/med-24.5) | (°▲i+7.6pp (3/9) · p+10.2pp cap47.3 net-29/med+18.5) |

- backtest payoff: right +2351 / wrong -2274 / net +77 pts; median per fire -7.75 (n=50)
- backtest best call: 2026-07-29 09:26 +577.3pts remaining (episode 632.8pts, major)
- backtest worst false alarm: 2026-07-31 13:43 -365.8pts adverse
- forward payoff: right +1297 / wrong -1023 / net +273 pts; median per fire +10.80 (n=40)
- forward best call: 2026-08-19 13:50 +160.3pts remaining (episode 160.3pts)
- forward worst false alarm: 2026-08-20 12:41 -171.4pts adverse
- earliness (backtest): median 308.2 pts of move remaining at fire (n=7)

**S0-H7 (either-dir)** — session × window grid (cells as in the matrix):

| session | backtest | forward |
|---|---|---|
| whole | ▼i-10.5pp (15/50) · p+4.4pp cap46.5 | ▼i-2.2pp (16/40) · p+11.8pp cap47.3 |
| london | (°▲i+2.2pp (8/16) · p+0.1pp cap23.3) | (°▲i+4.4pp (8/13) · p+7.1pp cap44.5) |
| overlap | (°▼i-3.3pp (1/8) · p+30.0pp cap118.7) | (°▼i-5.8pp (0/8) · p-2.0pp cap113.3) |
| ny_only | (°·i+0.3pp (3/8) · p-12.8pp cap18.8) | (°▼i-17.2pp (1/7) · p-10.8pp cap—) |
| dead | (°▼i-15.0pp (1/5) · p-22.2pp cap—) | (°▼i-7.3pp (1/3) · p+10.5pp cap21.8) |
| asia | (°▼i-29.9pp (2/13) · p-0.7pp cap35.7) | (°▲i+18.6pp (6/9) · p+22.1pp cap23.7) |

- backtest payoff: n/a by construction (either-direction)
- backtest best call: 2026-07-29 09:26 +577.3pts remaining (episode 632.8pts, major)
- backtest worst false alarm: 2026-07-29 02:54 -123.2pts adverse
- forward payoff: n/a by construction (either-direction)
- forward best call: 2026-08-20 16:14 +108.2pts remaining (episode 148.1pts)
- forward worst false alarm: 2026-08-20 14:49 -108.6pts adverse
- earliness (backtest): median 170.9 pts of move remaining at fire (n=14)

### H8 — 1 signal
*Reversal-signature bar anatomy (upthrust/spring) predicts imminent range expansion irrespective of direction.*
Grading: either-direction. Latest review: keep-watching (recommendation).

**S0-H8** — session × window grid (cells as in the matrix):

| session | backtest | forward |
|---|---|---|
| whole | ▼i-3.9pp (117/320) · p+1.8pp cap65.1 | ▲i+6.4pp (106/218) · p+10.7pp cap56.8 |
| london | ▼i-7.1pp (24/59) · p+4.9pp cap53.7 | ▲i+5.4pp (55/88) · p-1.9pp cap68.3 |
| overlap | (°▼i-9.6pp (2/32) · p-4.4pp cap69.4) | (°▼i-5.8pp (0/12) · p-47.8pp cap72.5) |
| ny_only | ▼i-13.3pp (17/71) · p+18.4pp cap52.0 | (°▲i+37.3pp (11/16) · p-4.6pp cap85.5) |
| dead | ▼i-3.8pp (15/48) · p+2.8pp cap133.9 | (°▲i+19.4pp (9/15) · p+37.2pp cap65.3) |
| asia | ▲i+8.3pp (59/110) · p-3.7pp cap81.9 | ▼i-12.5pp (31/87) · p+9.4pp cap52.6 |

- backtest payoff: n/a by construction (either-direction)
- backtest best call: 2026-07-30 06:39 +793.0pts remaining (episode 832.8pts, major)
- backtest worst false alarm: 2026-07-29 19:48 -233.6pts adverse
- forward payoff: n/a by construction (either-direction)
- forward best call: 2026-08-21 11:26 +303.6pts remaining (episode 309.6pts, major)
- forward worst false alarm: 2026-08-20 17:21 -107.3pts adverse
- earliness (backtest): median 130.5 pts of move remaining at fire (n=32)

### H9 — 2 signals
*Persistent lower-TF directional pressure that recruits expanding participation at the parent timeframe precedes continuation beyond what the parent label alone predicts; pressure without participation expansion does not.*
Grading: directional. Latest review: keep-watching (recommendation).

**S0-H9** — session × window grid (cells as in the matrix):

| session | backtest | forward |
|---|---|---|
| whole | ▲i+2.2pp (21/88) · p+0.7pp cap129.2 net+593/med-4.3 | ▼i-6.6pp (11/69) · p-6.8pp cap62.5 net-613/med-9.9 |
| london | (°▼i-25.8pp (0/9) · p+2.4pp cap76.3 net+410/med+11.6) | (°▲i+21.3pp (2/4) · p+17.4pp cap57.7 net-462/med-132.2) |
| overlap | (°▼i-7.9pp (0/10) · p+12.5pp cap306.3 net+540/med+51.3) | (°▼i-2.9pp (0/7) · p-19.9pp cap73.7 net-43/med-10.2) |
| ny_only | ▲i+28.0pp (12/25) · p-4.9pp cap125.7 net-148/med-7.0 | ·i-0.7pp (4/23) · p+3.3pp cap61.4 net-203/med-9.7 |
| dead | (°▲i+4.7pp (4/17) · p+17.9pp cap265.9 net+98/med-5.5) | (°▼i-23.3pp (0/5) · p-12.0pp cap— net+23/med+6.0) |
| asia | ▼i-5.8pp (5/27) · p-1.3pp cap78.6 net-307/med-10.2 | ▼i-9.0pp (5/30) · p-6.4pp cap58.2 net+72/med-9.6 |

- backtest payoff: right +3019 / wrong -2427 / net +593 pts; median per fire -4.35 (n=88)
- backtest best call: 2026-08-03 03:30 +174.2pts remaining (episode 209.2pts, major)
- backtest worst false alarm: 2026-07-29 18:45 -500.8pts adverse
- forward payoff: right +859 / wrong -1473 / net -613 pts; median per fire -9.95 (n=68)
- forward best call: 2026-08-17 15:30 +189.7pts remaining (episode 134.5pts)
- forward worst false alarm: 2026-08-19 13:00 -321.5pts adverse
- earliness (backtest): median 116.8 pts of move remaining at fire (n=6)

**S1-H9** — session × window grid (cells as in the matrix):

| session | backtest | forward |
|---|---|---|
| whole | ▼i-13.7pp (2/25) · p+6.0pp cap265.9 net-373/med+10.8 | (°▲i+20.4pp (3/7) · p-7.0pp cap52.5 net-557/med-25.7) |
| london | (°▼i-25.8pp (0/5) · p-30.9pp cap— net-57/med+2.3) | (°▲i+71.3pp (2/2) · p-32.6pp cap— net-493/med-246.5) |
| overlap | (°▼i-7.9pp (0/1) · p+62.5pp cap306.3 net+150/med+150.3) | — |
| ny_only | (°▼i-20.0pp (0/3) · p-12.9pp cap— net-373/med+63.9) | (°▲i+31.9pp (1/2) · p-5.4pp cap— net-94/med-47.2) |
| dead | (°▼i-18.8pp (0/8) · p+51.0pp cap265.9 net+174/med+55.5) | — |
| asia | (°·i+0.7pp (2/8) · p-7.3pp cap78.6 net-267/med-8.6) | (°▼i-25.7pp (0/3) · p+10.2pp cap52.5 net+30/med+14.4) |

- backtest payoff: right +1181 / wrong -1554 / net -373 pts; median per fire +10.80 (n=25)
- backtest best call: 2026-07-30 03:00 +120.0pts remaining (episode 134.4pts)
- backtest worst false alarm: 2026-07-29 18:45 -500.8pts adverse
- forward payoff: right +61 / wrong -618 / net -557 pts; median per fire -25.70 (n=7)
- forward best call: 2026-08-19 18:40 +56.7pts remaining (episode 74.5pts)
- forward worst false alarm: 2026-08-19 13:00 -321.5pts adverse
- earliness (backtest): median 120.0 pts of move remaining at fire (n=1)

### H10 — 1 signal
*In an established 1-minute trend, no-demand/no-supply prints in the trend's direction signal continuation.*
Grading: directional. Latest review: deprioritize (recommendation).

**S0-H10** — session × window grid (cells as in the matrix):

| session | backtest | forward |
|---|---|---|
| whole | ·i-0.6pp (37/175) · p-6.0pp cap92.8 net+2743/med+15.3 | ▼i-15.6pp (10/145) · p-2.7pp cap49.8 net-1420/med-8.1 |
| london | (°▼i-12.5pp (2/15) · p-17.6pp cap46.2 net-356/med-1.7) | ▼i-15.7pp (3/23) · p+10.9pp cap47.8 net+79/med-0.6 |
| overlap | (°▼i-7.9pp (0/18) · p-37.5pp cap— net+764/med+45.5) | (°▼i-2.9pp (0/20) · p-19.2pp cap119.2 net-674/med-50.1) |
| ny_only | ▲i+2.9pp (11/48) · p-6.7pp cap88.9 net+398/med+12.5 | ▼i-13.9pp (1/24) · p+7.1pp cap32.3 net-176/med-14.9 |
| dead | (°▼i-6.3pp (2/16) · p+1.0pp cap254.7 net+551/med+8.9) | (°▼i-6.6pp (2/12) · p-12.0pp cap— net-141/med-8.9) |
| asia | ▲i+3.9pp (22/78) · p+7.1pp cap99.1 net+1385/med+15.6 | ▼i-19.6pp (4/66) · p-6.4pp cap49.3 net-508/med-7.0 |

- backtest payoff: right +4792 / wrong -2049 / net +2743 pts; median per fire +15.30 (n=175)
- backtest best call: 2026-08-03 03:44 +199.5pts remaining (episode 209.2pts, major)
- backtest worst false alarm: 2026-07-27 12:56 -252.9pts adverse
- forward payoff: right +1185 / wrong -2605 / net -1420 pts; median per fire -8.10 (n=145)
- forward best call: 2026-08-17 04:16 +81.2pts remaining (episode 90.6pts, major)
- forward worst false alarm: 2026-08-18 01:03 -109.1pts adverse
- earliness (backtest): median 108.5 pts of move remaining at fire (n=7)

### H11 — 2 signals
*Price entering a low-volume price zone traverses it faster than baseline; entering a high-volume node it stalls or reverses at above-baseline rates.*
Grading: directional. Latest review: keep-watching (recommendation).

**S0-H11** — session × window grid (cells as in the matrix):

| session | backtest | forward |
|---|---|---|
| whole | ▼i-3.4pp (48/263) · p+2.3pp cap136.1 net+863/med+0.9 | ▼i-2.4pp (34/169) · p+2.4pp cap76.8 net+1035/med+2.4 |
| london | ·i-1.6pp (22/91) · p-2.3pp cap113.7 net+264/med-3.9 | ▲i+10.0pp (12/31) · p-0.3pp cap175.6 net+564/med-2.6 |
| overlap | (°▼i-7.9pp (0/20) · p+2.5pp cap232.1 net-137/med-23.4) | (°▼i-2.9pp (0/22) · p-2.4pp cap82.0 net+80/med+39.9) |
| ny_only | ▼i-13.1pp (2/29) · p+14.7pp cap229.4 net+826/med+77.1 | ▼i-5.2pp (8/62) · p-2.2pp cap44.9 net-49/med+0.3 |
| dead | ·i-1.6pp (10/58) · p+10.9pp cap98.2 net+874/med-3.1 | (°·i-1.9pp (3/14) · p+16.6pp cap79.7 net-117/med-10.8) |
| asia | ▼i-2.8pp (14/65) · p-6.0pp cap112.5 net-964/med+3.6 | ·i+1.8pp (11/40) · p+19.4pp cap67.2 net+558/med+13.2 |

- backtest payoff: right +10765 / wrong -9902 / net +863 pts; median per fire +0.90 (n=262)
- backtest best call: 2026-07-30 07:02 +741.2pts remaining (episode 832.8pts, major)
- backtest worst false alarm: 2026-07-29 13:50 -332.3pts adverse
- forward payoff: right +3954 / wrong -2919 / net +1035 pts; median per fire +2.40 (n=169)
- forward best call: 2026-08-19 10:07 +228.8pts remaining (episode 238.9pts, major)
- forward worst false alarm: 2026-08-20 11:38 -181.6pts adverse
- earliness (backtest): median 176.0 pts of move remaining at fire (n=14)

**S1-H11** — session × window grid (cells as in the matrix):

| session | backtest | forward |
|---|---|---|
| whole | ▼i-8.5pp (23/174) · p+5.0pp cap130.1 net+293/med-14.1 | ▲i+9.5pp (48/150) · p+1.4pp cap88.4 net-712/med-0.9 |
| london | ·i+0.6pp (14/53) · p-2.6pp cap109.7 net-436/med-14.7 | ·i+0.6pp (12/41) · p-0.9pp cap109.8 net-434/med-2.5 |
| overlap | (°·i-1.2pp (1/15) · p-10.8pp cap192.0 net-139/med-40.7) | (°▼i-2.9pp (0/2) · p-34.2pp cap— net-61/med-30.4) |
| ny_only | ▼i-20.0pp (0/39) · p+10.2pp cap558.0 net+1758/med-19.4 | (°▼i-18.1pp (0/5) · p+14.6pp cap116.2 net+159/med+34.0) |
| dead | (°▼i-2.1pp (2/12) · p-3.2pp cap141.6 net-253/med+3.9) | (°▲i+26.7pp (4/8) · p+13.0pp cap88.0 net-1/med+0.1) |
| asia | ▼i-13.4pp (6/55) · p+12.9pp cap124.1 net-637/med-13.4 | ▲i+8.3pp (32/94) · p-4.0pp cap65.0 net-375/med-1.2 |

- backtest payoff: right +9792 / wrong -9499 / net +293 pts; median per fire -14.05 (n=174)
- backtest best call: 2026-07-29 09:17 +555.3pts remaining (episode 632.8pts, major)
- backtest worst false alarm: 2026-07-29 19:07 -730.3pts adverse
- forward payoff: right +3056 / wrong -3768 / net -712 pts; median per fire -0.90 (n=150)
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
| whole | (°▼i-21.7pp (0/1) · p+78.0pp cap95.7 net+93/med+93.0) | — |
| london | (°▼i-25.8pp (0/1) · p+69.1pp cap95.7 net+93/med+93.0) | — |
| overlap | — | — |
| ny_only | — | — |
| dead | — | — |
| asia | — | — |

- backtest payoff: right +93 / wrong +0 / net +93 pts; median per fire +93.00 (n=1)

### H14 — 1 signal
*Counter-trend No Demand / No Supply prints in an established trend mark absorption and precede trend continuation.*
Grading: directional. Latest review: keep-watching (recommendation).

**S0-H14** — session × window grid (cells as in the matrix):

| session | backtest | forward |
|---|---|---|
| whole | ·i+0.5pp (37/167) · p-13.6pp cap70.2 net-692/med+6.9 | ▼i-18.5pp (6/149) · p-3.2pp cap52.7 net-694/med-5.7 |
| london | ▼i-10.4pp (4/26) · p-19.4pp cap41.8 net-1762/med-17.1 | ▼i-28.7pp (0/20) · p+12.4pp cap74.6 net+552/med+14.1 |
| overlap | (°▼i-7.9pp (0/17) · p-37.5pp cap— net+433/med+24.0) | (°▼i-2.9pp (0/23) · p-21.2pp cap101.2 net-792/med-40.9) |
| ny_only | ▲i+15.3pp (18/51) · p-12.9pp cap— net+410/med+13.6 | ▼i-11.9pp (2/32) · p-2.3pp cap101.5 net-363/med-10.4 |
| dead | (°▼i-7.7pp (2/18) · p-11.5pp cap— net-56/med+4.5) | (°▼i-9.0pp (1/7) · p-12.0pp cap— net-35/med-4.6) |
| asia | ·i-0.7pp (13/55) · p+0.2pp cap85.1 net+282/med+6.6 | ▼i-21.2pp (3/67) · p-2.2pp cap48.4 net-56/med-4.0 |

- backtest payoff: right +2905 / wrong -3598 / net -692 pts; median per fire +6.90 (n=167)
- backtest best call: 2026-08-03 03:48 +195.6pts remaining (episode 209.2pts, major)
- backtest worst false alarm: 2026-07-27 12:59 -334.6pts adverse
- forward payoff: right +1878 / wrong -2572 / net -694 pts; median per fire -5.70 (n=149)
- forward best call: 2026-08-17 04:14 +80.5pts remaining (episode 90.6pts, major)
- forward worst false alarm: 2026-08-18 01:23 -150.9pts adverse
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
| whole | (°▼i-11.7pp (1/10) · p+28.0pp cap121.0 net+274/med+0.1) | (°▼i-5.8pp (1/6) · p-4.6pp cap53.5 net+109/med+21.2) |
| london | — | — |
| overlap | — | — |
| ny_only | (°▼i-10.0pp (1/10) · p+37.1pp cap121.0 net+274/med+0.1) | (°·i-1.4pp (1/6) · p+11.3pp cap53.5 net+109/med+21.2) |
| dead | — | — |
| asia | — | — |

- backtest payoff: right +666 / wrong -392 / net +274 pts; median per fire +0.05 (n=10)
- backtest best call: 2026-08-03 19:30 +30.1pts remaining (episode 61.6pts)
- backtest worst false alarm: 2026-07-23 19:30 -188.1pts adverse
- forward payoff: right +124 / wrong -16 / net +109 pts; median per fire +21.25 (n=6)
- forward best call: 2026-08-21 19:30 +25.6pts remaining (episode 56.1pts)
- forward worst false alarm: 2026-08-21 19:30 -33.9pts adverse
- earliness (backtest): median 30.1 pts of move remaining at fire (n=1)


---

# us30 (us30fut) — PROVISIONAL

> **PROVISIONAL — validation pending (register 40 fence as amended 2026-08-19): replay-only study over the synced store; canonical status, live attachment, and Asia/pause-sensitive cell interpretation await this instrument's validation evening. EXPLORATORY first cross-instrument look — expectations deliberately unregistered; anything interesting becomes a pre-registered question before it becomes a claim. NO POOLING across instruments.**
>
> - drift-adjustment segments and engine tod baselines run on the provider/London trading-day structure; native cash-hour segmentation is part of this instrument's validation evening
> - sessions = the registered register-37 world-clock partition (native-tz, DST-proof) applied to this instrument's own bars; 'london' is not the home session of the US pairs
> - the forward window (>= go_live) is also a replay over the synced store — this instrument has NO live attachment yet

Store span (1M, close ts): 2026-07-19 22:02:00+00:00 → 2026-08-21 20:29:00+00:00. Volume type: real futures volume (register 40 first-sync sanity; canonical verdict at this instrument's validation evening).

## Summary Matrix (page 1)

Engine `01e9d5694` — OBSERVATIONAL signal scoreboard - move-detection, not trading; no fills exist here by construction; never validation (docs/hypothesis_lifecycle.md stage 4)

**Review labels are RECOMMENDATIONS — none actioned, review pending operator familiarity.** Cells: marker + precision LIFT vs that context's OWN chance rate, (hits/fires), payoff net/median points (directional rows; either-direction rows have no payoff by construction). ▲/▼ = beyond ±2pp of chance, · = within. (°…) = small-n (fires<20 or episodes<10): dimmed, excluded from any future label arithmetic. Read READING_GUIDE.md first; full detail in hypothesis_performance.json.

| H | label | backtest whole | backtest london | forward whole | forward london |
|---|---|---|---|---|---|
| *context* | | 110 ep; chance 23.9%dir/44.5%either | 36 ep; chance 36.3%dir/65.9%either | 51 ep; chance 23.3%dir/44.4%either | 15 ep; chance 38.1%dir/71.7%either |
| S0-H1 | keep-watching | ▲i+3.3pp (12/49) · p+8.8pp cap158.0 net-83/med-8.0 | (°▲i+16.7pp (7/17) · p-6.9pp cap103.5 net-113/med-17.5) | ·i-1.6pp (13/66) · p+10.0pp cap54.8 net-862/med-1.2 | ▲i+7.7pp (8/28) · p-6.0pp cap80.0 net-966/med-20.0 |
| S1-H1 | keep-watching | (°▼i-21.2pp (0/2) · p-23.9pp cap— net-18/med-9.2) | (°▼i-24.5pp (0/1) · p-36.3pp cap— net-50/med-50.0) | (°▲i+16.2pp (3/8) · p-10.8pp cap68.5 net-619/med-62.2) | (°▲i+29.1pp (3/6) · p-38.1pp cap— net-612/med-81.8) |
| S0-H2 | promote-candidate | ▼i-6.3pp (42/281) · p+1.4pp cap138.9 net-2432/med-4.0 | ·i-0.3pp (15/62) · p-2.4pp cap119.0 net-337/med-20.0 | ▼i-3.5pp (40/225) · p+4.3pp cap67.8 net+479/med-1.0 | ▼i-5.2pp (14/89) · p+1.2pp cap82.0 net+724/med+6.0 |
| S1-H2 | promote-candidate | ▼i-4.8pp (36/220) · p+2.5pp cap139.2 net-505/med-2.8 | ·i-0.5pp (12/50) · p-0.3pp cap126.8 net-218/med-18.0 | ▲i+2.1pp (39/167) · p+0.1pp cap63.5 net+38/med-1.0 | ▲i+5.0pp (14/54) · p-8.5pp cap85.8 net+64/med-5.8 |
| S0-H3 | keep-watching | (°▼i-21.2pp (0/4) · p+1.1pp cap81.0 net+59/med+13.2) | (°▼i-24.5pp (0/2) · p-36.3pp cap— net-22/med-11.0) | (°▼i-21.3pp (0/1) · p-23.3pp cap— net-13/med-13.0) | — |
| S0-H4 | keep-watching | (°▲i+17.3pp (5/13) · p+14.6pp cap83.0 net+194/med+15.0) | (°▼i-24.5pp (0/7) · p+35.1pp cap83.0 net+392/med+71.0) | — | — |
| S0-H5 | keep-watching | (°▼i-21.2pp (0/1) · p-23.9pp cap— net-135/med-135.0) | (°▼i-24.5pp (0/1) · p-36.3pp cap— net-135/med-135.0) | (°▼i-21.3pp (0/1) · p+76.7pp cap215.0 net+24/med+24.0) | (°▼i-20.9pp (0/1) · p+61.9pp cap215.0 net+24/med+24.0) |
| S0-H6 | keep-watching | ▼i-6.1pp (5/52) · p-21.3pp cap175.0 [cls 40.5%/15.7%i] net-1151/med-25.2 | ·i+0.9pp (5/24) · p-28.3pp cap164.5 [cls 40.8%/19.9%i] net-664/med-30.0 | ▲i+7.2pp (11/47) · p-0.8pp cap88.5 [cls 41.2%/16.2%i] net-523/med-11.5 | ·i-1.5pp (4/21) · p+24.5pp cap96.8 [cls 42.2%/20.5%i] net+380/med+26.5 |
| S0-H7 | keep-watching | ▲i+5.6pp (11/41) · p-1.9pp cap111.0 net+205/med-9.0 | (°▲i+6.7pp (5/16) · p-5.1pp cap111.0 net-161/med-7.0) | ·i-0.2pp (8/38) · p+8.3pp cap70.0 net+426/med+4.8 | (°▼i-8.4pp (1/8) · p-0.6pp cap71.5 net-141/med-32.0) |
| S0-H7 (either-dir) | keep-watching | ·i-0.3pp (16/41) · p-3.0pp cap66.5 | (°▼i-14.0pp (5/16) · p+2.9pp cap60.5) | ▼i-7.3pp (12/38) · p+8.2pp cap36.0 | (°▼i-29.3pp (1/8) · p+28.3pp cap26.5) |
| S0-H8 | keep-watching | ▼i-13.3pp (73/281) · p+7.5pp cap76.5 | ▼i-6.5pp (24/62) · p+6.7pp cap60.5 | ▼i-4.7pp (77/225) · p+4.5pp cap42.5 | ▼i-5.8pp (32/89) · p-6.5pp cap58.8 |
| S0-H9 | keep-watching | ▼i-13.7pp (3/40) · p-1.4pp cap66.0 net-353/med-14.7 | (°▼i-24.5pp (0/3) · p-3.0pp cap52.0 net-198/med-61.5) | ▼i-11.3pp (2/20) · p-13.3pp cap169.5 net-558/med-31.0 | (°·i+1.3pp (2/9) · p-15.9pp cap169.5 net-363/med-76.0) |
| S1-H9 | keep-watching | (°▼i-21.2pp (0/9) · p-1.7pp cap273.0 net+460/med+1.5) | (°▼i-24.5pp (0/1) · p-36.3pp cap— net-38/med-38.0) | (°▼i-3.1pp (2/11) · p-5.1pp cap169.5 net-375/med-31.0) | (°▲i+4.1pp (2/8) · p-13.1pp cap169.5 net-305/med-84.8) |
| S0-H10 | deprioritize | ·i-1.7pp (30/154) · p+0.1pp cap71.0 net+1774/med+11.0 | ▼i-19.5pp (2/40) · p+3.7pp cap116.0 net+1480/med+27.5 | ▼i-5.3pp (25/156) · p-2.8pp cap56.0 net+230/med-0.5 | ▲i+3.5pp (10/41) · p-1.5pp cap74.0 net+196/med-11.0 |
| S0-H11 | keep-watching | ·i-0.4pp (86/413) · p+3.5pp cap98.0 net+1254/med+3.0 | ▼i-5.5pp (31/163) · p+1.1pp cap91.0 net-404/med+5.0 | ·i-0.1pp (68/321) · p+4.7pp cap71.5 net-142/med-5.0 | ▼i-2.3pp (24/129) · p-0.9pp cap75.0 net+175/med+0.0 |
| S1-H11 | keep-watching | ▲i+4.7pp (49/189) · p+1.5pp cap163.5 net+1560/med+0.5 | (°▼i-15.4pp (1/11) · p+9.2pp cap194.5 net+136/med-24.5) | ▼i-6.8pp (12/83) · p+4.4pp cap118.0 net+218/med-14.0 | ▼i-4.6pp (8/49) · p+0.7pp cap184.0 net+1074/med-14.0 |
| S0-H12 | keep-watching | — | — | — | — |
| S0-H13 | keep-watching | (°▲i+78.8pp (1/1) · p-23.9pp cap— net-206/med-206.0) | (°▲i+75.5pp (1/1) · p-36.3pp cap— net-206/med-206.0) | — | — |
| S0-H14 | keep-watching | ▲i+3.8pp (37/148) · p+1.8pp cap76.0 net+2606/med+12.5 | ▼i-18.1pp (3/47) · p+8.4pp cap121.5 net+1414/med+12.5 | ▼i-6.3pp (20/133) · p-3.8pp cap81.5 net-216/med-5.0 | ▲i+4.1pp (10/40) · p-3.1pp cap92.5 net+362/med-5.0 |
| S0-H15 | keep-watching | — | — | — | — |
| S0-H16 | keep-watching | (°▼i-21.2pp (0/10) · p+26.1pp cap100.0 net+522/med+37.5) | — | (°▼i-21.3pp (0/6) · p+26.7pp cap63.0 net+125/med+43.5) | — |
| **union coverage** | | 40.0% (44/110) | 33.3% (12/36) | 94.1% (48/51) | 93.3% (14/15) |

Not graded:  — see register entries.

## Hypothesis Cards (page 2)

### H1 — 2 signals
*A climactic bar — extreme volume on a wide spread late in an extended move — marks exhaustion, and price then reverses against the climax direction.*
Grading: directional. Latest review: keep-watching (recommendation).

- Question **Q1-H1**: see the register entry (status there is authoritative).
**S0-H1** — session × window grid (cells as in the matrix):

| session | backtest | forward |
|---|---|---|
| whole | ▲i+3.3pp (12/49) · p+8.8pp cap158.0 net-83/med-8.0 | ·i-1.6pp (13/66) · p+10.0pp cap54.8 net-862/med-1.2 |
| london | (°▲i+16.7pp (7/17) · p-6.9pp cap103.5 net-113/med-17.5) | ▲i+7.7pp (8/28) · p-6.0pp cap80.0 net-966/med-20.0 |
| overlap | — | (°▼i-13.8pp (0/2) · p+19.5pp cap186.5 net+119/med+59.5) |
| ny_only | (°▼i-3.8pp (2/13) · p+40.3pp cap253.5 net-62/med-15.5) | (°▲i+12.7pp (1/3) · p-11.2pp cap— net+40/med+2.5) |
| dead | (°▲i+28.3pp (3/7) · p-7.1pp cap— net-157/med-8.0) | (°▲i+12.1pp (2/7) · p+11.1pp cap44.0 net+46/med+7.0) |
| asia | (°▼i-25.0pp (0/12) · p+9.3pp cap91.2 net+248/med+27.0) | ▼i-18.7pp (2/26) · p+16.8pp cap39.0 net-101/med+1.5 |

- backtest payoff: right +1958 / wrong -2041 / net -83 pts; median per fire -8.00 (n=49)
- backtest best call: 2026-07-29 16:24 +398.0pts remaining (episode 602.0pts, major)
- backtest worst false alarm: 2026-07-29 19:22 -450.0pts adverse
- forward payoff: right +1200 / wrong -2062 / net -862 pts; median per fire -1.25 (n=66)
- forward best call: 2026-08-20 09:19 +408.0pts remaining (episode 415.0pts, major)
- forward worst false alarm: 2026-08-20 11:25 -261.5pts adverse
- earliness (backtest): median 128.0 pts of move remaining at fire (n=10)

**S1-H1** — session × window grid (cells as in the matrix):

| session | backtest | forward |
|---|---|---|
| whole | (°▼i-21.2pp (0/2) · p-23.9pp cap— net-18/med-9.2) | (°▲i+16.2pp (3/8) · p-10.8pp cap68.5 net-619/med-62.2) |
| london | (°▼i-24.5pp (0/1) · p-36.3pp cap— net-50/med-50.0) | (°▲i+29.1pp (3/6) · p-38.1pp cap— net-612/med-81.8) |
| overlap | — | — |
| ny_only | — | — |
| dead | — | — |
| asia | (°▼i-25.0pp (0/1) · p-24.0pp cap— net+32/med+31.5) | (°▼i-26.4pp (0/2) · p+24.5pp cap68.5 net-6/med-3.2) |

- backtest payoff: right +32 / wrong -50 / net -18 pts; median per fire -9.25 (n=2)
- backtest worst false alarm: 2026-07-29 12:17 -67.0pts adverse
- forward payoff: right +49 / wrong -668 / net -619 pts; median per fire -62.25 (n=8)
- forward best call: 2026-08-20 11:47 +4.0pts remaining (episode 182.0pts, major)
- forward worst false alarm: 2026-08-20 11:47 -199.5pts adverse

### H2 — 2 signals
*A failed probe beyond a prior extreme — an upthrust above or spring below that closes back inside — reverses against the probe.*
Grading: directional. Latest review: promote-candidate (recommendation).

**S0-H2** — session × window grid (cells as in the matrix):

| session | backtest | forward |
|---|---|---|
| whole | ▼i-6.3pp (42/281) · p+1.4pp cap138.9 net-2432/med-4.0 | ▼i-3.5pp (40/225) · p+4.3pp cap67.8 net+479/med-1.0 |
| london | ·i-0.3pp (15/62) · p-2.4pp cap119.0 net-337/med-20.0 | ▼i-5.2pp (14/89) · p+1.2pp cap82.0 net+724/med+6.0 |
| overlap | (°▼i-11.4pp (0/22) · p+3.7pp cap177.5 net-1080/med-77.8) | (°▲i+2.9pp (2/12) · p-5.5pp cap185.5 net-58/med-44.5) |
| ny_only | ▼i-14.2pp (3/60) · p+21.5pp cap239.5 net-1257/med-11.1 | ▲i+9.0pp (8/27) · p-7.5pp cap96.5 net-317/med-6.5 |
| dead | ·i+0.0pp (6/41) · p+2.7pp cap100.8 net-18/med-2.6 | (°▲i+11.5pp (7/25) · p+4.8pp cap37.5 net+24/med-1.0) |
| asia | ▼i-6.2pp (18/96) · p-6.3pp cap83.0 net+261/med+1.2 | ▼i-13.9pp (9/72) · p+3.7pp cap43.5 net+106/med+0.0 |

- backtest payoff: right +10496 / wrong -12928 / net -2432 pts; median per fire -4.00 (n=281)
- backtest best call: 2026-07-29 06:34 +888.5pts remaining (episode 948.5pts, major)
- backtest worst false alarm: 2026-07-29 18:55 -695.0pts adverse
- forward payoff: right +4848 / wrong -4369 / net +479 pts; median per fire -1.00 (n=225)
- forward best call: 2026-08-20 09:10 +401.0pts remaining (episode 415.0pts, major)
- forward worst false alarm: 2026-08-19 12:55 -270.0pts adverse
- earliness (backtest): median 106.0 pts of move remaining at fire (n=23)

**S1-H2** — session × window grid (cells as in the matrix):

| session | backtest | forward |
|---|---|---|
| whole | ▼i-4.8pp (36/220) · p+2.5pp cap139.2 net-505/med-2.8 | ▲i+2.1pp (39/167) · p+0.1pp cap63.5 net+38/med-1.0 |
| london | ·i-0.5pp (12/50) · p-0.3pp cap126.8 net-218/med-18.0 | ▲i+5.0pp (14/54) · p-8.5pp cap85.8 net+64/med-5.8 |
| overlap | (°▼i-11.4pp (0/17) · p-3.3pp cap182.5 net-983/med-92.0) | (°▲i+2.9pp (2/12) · p-5.5pp cap185.5 net-58/med-44.5) |
| ny_only | ▼i-14.3pp (2/41) · p+30.4pp cap249.0 net+169/med-15.0 | ▲i+15.8pp (8/22) · p-6.7pp cap96.5 net-88/med+1.0 |
| dead | ▲i+4.8pp (6/31) · p+2.6pp cap99.5 net-162/med-5.0 | (°▲i+10.8pp (6/22) · p+5.9pp cap37.5 net+55/med+0.0) |
| asia | ▼i-5.2pp (16/81) · p-6.7pp cap83.0 net+689/med+6.0 | ▼i-10.6pp (9/57) · p+4.3pp cap43.5 net+64/med-0.5 |

- backtest payoff: right +8589 / wrong -9094 / net -505 pts; median per fire -2.80 (n=220)
- backtest best call: 2026-07-29 06:34 +888.5pts remaining (episode 948.5pts, major)
- backtest worst false alarm: 2026-07-29 18:55 -695.0pts adverse
- forward payoff: right +3054 / wrong -3016 / net +38 pts; median per fire -1.00 (n=167)
- forward best call: 2026-08-20 09:10 +401.0pts remaining (episode 415.0pts, major)
- forward worst false alarm: 2026-08-20 11:54 -201.0pts adverse
- earliness (backtest): median 106.0 pts of move remaining at fire (n=21)

### H3 — 1 signal
*Repeated absorption — high effort with no result — at a price level precedes a breakout through that level.*
Grading: directional. Latest review: keep-watching (recommendation).

**S0-H3** — session × window grid (cells as in the matrix):

| session | backtest | forward |
|---|---|---|
| whole | (°▼i-21.2pp (0/4) · p+1.1pp cap81.0 net+59/med+13.2) | (°▼i-21.3pp (0/1) · p-23.3pp cap— net-13/med-13.0) |
| london | (°▼i-24.5pp (0/2) · p-36.3pp cap— net-22/med-11.0) | — |
| overlap | — | — |
| ny_only | — | — |
| dead | — | — |
| asia | (°▼i-25.0pp (0/2) · p+26.0pp cap81.0 net+81/med+40.5) | (°▼i-26.4pp (0/1) · p-25.5pp cap— net-13/med-13.0) |

- backtest payoff: right +99 / wrong -40 / net +59 pts; median per fire +13.25 (n=4)
- backtest worst false alarm: 2026-07-30 09:10 -83.5pts adverse
- forward payoff: right +0 / wrong -13 / net -13 pts; median per fire -13.00 (n=1)
- forward worst false alarm: 2026-08-21 04:18 -16.0pts adverse

### H4 — 1 signal
*In an established trend, a quiet (low-volume) pullback resolves with trend resumption.*
Grading: directional. Latest review: keep-watching (recommendation).

**S0-H4** — session × window grid (cells as in the matrix):

| session | backtest | forward |
|---|---|---|
| whole | (°▲i+17.3pp (5/13) · p+14.6pp cap83.0 net+194/med+15.0) | — |
| london | (°▼i-24.5pp (0/7) · p+35.1pp cap83.0 net+392/med+71.0) | — |
| overlap | (°▼i-11.4pp (0/1) · p-32.7pp cap— net-166/med-165.5) | — |
| ny_only | — | — |
| dead | (°▲i+85.4pp (5/5) · p-7.1pp cap— net-33/med-6.9) | — |
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
| whole | (°▼i-21.2pp (0/1) · p-23.9pp cap— net-135/med-135.0) | (°▼i-21.3pp (0/1) · p+76.7pp cap215.0 net+24/med+24.0) |
| london | (°▼i-24.5pp (0/1) · p-36.3pp cap— net-135/med-135.0) | (°▼i-20.9pp (0/1) · p+61.9pp cap215.0 net+24/med+24.0) |
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

**S0-H6** — session × window grid (cells as in the matrix):

| session | backtest | forward |
|---|---|---|
| whole | ▼i-6.1pp (5/52) · p-21.3pp cap175.0 [cls 40.5%/15.7%i] net-1151/med-25.2 | ▲i+7.2pp (11/47) · p-0.8pp cap88.5 [cls 41.2%/16.2%i] net-523/med-11.5 |
| london | ·i+0.9pp (5/24) · p-28.3pp cap164.5 [cls 40.8%/19.9%i] net-664/med-30.0 | ·i-1.5pp (4/21) · p+24.5pp cap96.8 [cls 42.2%/20.5%i] net+380/med+26.5 |
| overlap | (°▼i-9.2pp (0/18) · p-18.9pp cap195.5 [cls 41.1%/9.2%i] net+234/med+6.8) | (°▲i+19.1pp (7/24) · p-19.6pp cap82.5 [cls 40.4%/10.1%i] net-840/med-31.5) |
| ny_only | (°▼i-5.4pp (0/6) · p+8.1pp cap329.0 [cls 41.9%/5.4%i] net-856/med-92.0) | — |
| dead | (°▼i-7.4pp (0/3) · p-13.2pp cap— [cls 13.2%/7.4%i] net+58/med+5.5) | — |
| asia | (°▼i-20.7pp (0/1) · p-40.2pp cap— [cls 40.2%/20.7%i] net+77/med+77.0) | (°▼i-11.7pp (0/2) · p-46.8pp cap— [cls 46.8%/11.7%i] net-62/med-31.0) |

- backtest payoff: right +1398 / wrong -2549 / net -1151 pts; median per fire -25.25 (n=52)
- backtest best call: 2026-07-28 12:23 +197.5pts remaining (episode 226.5pts, major)
- backtest worst false alarm: 2026-07-28 15:11 -288.5pts adverse
- forward payoff: right +908 / wrong -1432 / net -523 pts; median per fire -11.50 (n=47)
- forward best call: 2026-08-20 12:09 +137.5pts remaining (episode 182.0pts, major)
- forward worst false alarm: 2026-08-20 13:55 -166.0pts adverse
- earliness (backtest): median 43.0 pts of move remaining at fire (n=3)

### H7 — 1 signal
*Quiet decline at a session extreme is disguised accumulation: effortless (low-volume) weakness reverses UP once selling fails to attract participation (mirror: quiet advance at a high reverses down).*
Grading: directional + either-direction (dual). Latest review: keep-watching (recommendation).

- Question **Q1-H7**: see the register entry (status there is authoritative).
**S0-H7** — session × window grid (cells as in the matrix):

| session | backtest | forward |
|---|---|---|
| whole | ▲i+5.6pp (11/41) · p-1.9pp cap111.0 net+205/med-9.0 | ·i-0.2pp (8/38) · p+8.3pp cap70.0 net+426/med+4.8 |
| london | (°▲i+6.7pp (5/16) · p-5.1pp cap111.0 net-161/med-7.0) | (°▼i-8.4pp (1/8) · p-0.6pp cap71.5 net-141/med-32.0) |
| overlap | (°▼i-11.4pp (0/3) · p+34.0pp cap287.0 net+471/med+272.0) | (°▲i+6.2pp (1/5) · p+29.5pp cap198.5 net+322/med+112.0) |
| ny_only | (°▼i-19.2pp (0/4) · p-13.5pp cap— net-21/med-5.0) | (°▲i+9.4pp (3/10) · p-11.2pp cap— net+164/med+16.0) |
| dead | (°▲i+10.4pp (1/4) · p-7.1pp cap— net-1/med-2.0) | (°▲i+83.5pp (1/1) · p-3.2pp cap— net-0/med-0.5) |
| asia | (°▲i+10.7pp (5/14) · p-9.7pp cap76.0 net-84/med-13.8) | (°▼i-12.1pp (2/14) · p+17.4pp cap38.8 net+82/med+4.8) |

- backtest payoff: right +1609 / wrong -1404 / net +205 pts; median per fire -9.00 (n=41)
- backtest best call: 2026-07-31 09:51 +528.0pts remaining (episode 572.5pts, major)
- backtest worst false alarm: 2026-07-28 10:48 -242.0pts adverse
- forward payoff: right +1241 / wrong -814 / net +426 pts; median per fire +4.75 (n=38)
- forward best call: 2026-08-19 13:56 +166.0pts remaining (episode 236.0pts)
- forward worst false alarm: 2026-08-19 12:12 -262.0pts adverse
- earliness (backtest): median 110.5 pts of move remaining at fire (n=9)

**S0-H7 (either-dir)** — session × window grid (cells as in the matrix):

| session | backtest | forward |
|---|---|---|
| whole | ·i-0.3pp (16/41) · p-3.0pp cap66.5 | ▼i-7.3pp (12/38) · p+8.2pp cap36.0 |
| london | (°▼i-14.0pp (5/16) · p+2.9pp cap60.5) | (°▼i-29.3pp (1/8) · p+28.3pp cap26.5) |
| overlap | (°▼i-22.8pp (0/3) · p+6.4pp cap287.0) | (°▼i-5.6pp (1/5) · p+22.2pp cap191.2) |
| ny_only | (°▼i-10.3pp (1/4) · p-26.1pp cap—) | (°▲i+10.7pp (5/10) · p-22.5pp cap—) |
| dead | (°▲i+21.3pp (2/4) · p-14.3pp cap—) | (°▲i+70.5pp (1/1) · p-6.3pp cap—) |
| asia | (°▲i+11.2pp (8/14) · p-16.9pp cap37.0) | (°▼i-15.2pp (4/14) · p+8.9pp cap36.0) |

- backtest payoff: n/a by construction (either-direction)
- backtest best call: 2026-07-31 09:51 +528.0pts remaining (episode 572.5pts, major)
- backtest worst false alarm: 2026-07-30 16:13 -170.0pts adverse
- forward payoff: n/a by construction (either-direction)
- forward best call: 2026-08-21 03:52 +192.5pts remaining (episode 197.5pts, major)
- forward worst false alarm: 2026-08-20 15:23 -98.0pts adverse
- earliness (backtest): median 85.0 pts of move remaining at fire (n=11)

### H8 — 1 signal
*Reversal-signature bar anatomy (upthrust/spring) predicts imminent range expansion irrespective of direction.*
Grading: either-direction. Latest review: keep-watching (recommendation).

**S0-H8** — session × window grid (cells as in the matrix):

| session | backtest | forward |
|---|---|---|
| whole | ▼i-13.3pp (73/281) · p+7.5pp cap76.5 | ▼i-4.7pp (77/225) · p+4.5pp cap42.5 |
| london | ▼i-6.5pp (24/62) · p+6.7pp cap60.5 | ▼i-5.8pp (32/89) · p-6.5pp cap58.8 |
| overlap | (°▼i-22.8pp (0/22) · p+21.5pp cap114.2) | (°·i-0.6pp (3/12) · p+8.9pp cap62.2) |
| ny_only | ▼i-25.3pp (6/60) · p+37.2pp cap154.5 | ▲i+12.6pp (14/27) · p-11.4pp cap8.0 |
| dead | ▼i-11.6pp (7/41) · p+10.1pp cap10.5 | (°▲i+14.5pp (11/25) · p+1.7pp cap37.5) |
| asia | ▼i-8.4pp (36/96) · p-9.0pp cap39.0 | ▼i-20.2pp (17/72) · p+6.0pp cap28.0 |

- backtest payoff: n/a by construction (either-direction)
- backtest best call: 2026-07-29 06:34 +888.5pts remaining (episode 948.5pts, major)
- backtest worst false alarm: 2026-07-27 16:47 -152.0pts adverse
- forward payoff: n/a by construction (either-direction)
- forward best call: 2026-08-20 09:10 +401.0pts remaining (episode 415.0pts, major)
- forward worst false alarm: 2026-08-19 16:19 -145.5pts adverse
- earliness (backtest): median 100.5 pts of move remaining at fire (n=27)

### H9 — 2 signals
*Persistent lower-TF directional pressure that recruits expanding participation at the parent timeframe precedes continuation beyond what the parent label alone predicts; pressure without participation expansion does not.*
Grading: directional. Latest review: keep-watching (recommendation).

**S0-H9** — session × window grid (cells as in the matrix):

| session | backtest | forward |
|---|---|---|
| whole | ▼i-13.7pp (3/40) · p-1.4pp cap66.0 net-353/med-14.7 | ▼i-11.3pp (2/20) · p-13.3pp cap169.5 net-558/med-31.0 |
| london | (°▼i-24.5pp (0/3) · p-3.0pp cap52.0 net-198/med-61.5) | (°·i+1.3pp (2/9) · p-15.9pp cap169.5 net-363/med-76.0) |
| overlap | (°▼i-11.4pp (0/2) · p-32.7pp cap— net-19/med-9.5) | — |
| ny_only | (°▼i-9.2pp (1/10) · p-3.5pp cap464.5 net-196/med-66.5) | (°▼i-20.6pp (0/5) · p-11.2pp cap— net-78/med-13.0) |
| dead | (°▼i-14.6pp (0/7) · p-7.1pp cap— net+60/med+15.5) | (°▼i-16.5pp (0/2) · p-3.2pp cap— net-4/med-3.5) |
| asia | (°▼i-13.9pp (2/18) · p+14.9pp cap66.0 net-1/med-11.2) | (°▼i-26.4pp (0/4) · p-25.5pp cap— net-113/med-31.5) |

- backtest payoff: right +876 / wrong -1229 / net -353 pts; median per fire -14.70 (n=38)
- backtest best call: 2026-08-03 05:40 +463.0pts remaining (episode 472.0pts, major)
- backtest worst false alarm: 2026-08-03 17:15 -176.0pts adverse
- forward payoff: right +257 / wrong -815 / net -558 pts; median per fire -31.00 (n=19)
- forward best call: 2026-08-18 07:00 +64.9pts remaining (episode 148.4pts, major)
- forward worst false alarm: 2026-08-18 07:00 -127.5pts adverse
- earliness (backtest): median 351.5 pts of move remaining at fire (n=2)

**S1-H9** — session × window grid (cells as in the matrix):

| session | backtest | forward |
|---|---|---|
| whole | (°▼i-21.2pp (0/9) · p-1.7pp cap273.0 net+460/med+1.5) | (°▼i-3.1pp (2/11) · p-5.1pp cap169.5 net-375/med-31.0) |
| london | (°▼i-24.5pp (0/1) · p-36.3pp cap— net-38/med-38.0) | (°▲i+4.1pp (2/8) · p-13.1pp cap169.5 net-305/med-84.8) |
| overlap | — | — |
| ny_only | (°▼i-19.2pp (0/4) · p+11.5pp cap464.5 net+421/med+15.3) | (°▼i-20.6pp (0/2) · p-11.2pp cap— net-41/med-20.5) |
| dead | — | — |
| asia | (°▼i-25.0pp (0/4) · p+1.0pp cap81.5 net+76/med+12.8) | (°▼i-26.4pp (0/1) · p-25.5pp cap— net-30/med-29.5) |

- backtest payoff: right +601 / wrong -141 / net +460 pts; median per fire +1.50 (n=9)
- backtest worst false alarm: 2026-07-27 16:10 -84.0pts adverse
- forward payoff: right +248 / wrong -624 / net -375 pts; median per fire -31.00 (n=11)
- forward best call: 2026-08-18 07:00 +64.9pts remaining (episode 148.4pts, major)
- forward worst false alarm: 2026-08-18 07:00 -127.5pts adverse

### H10 — 1 signal
*In an established 1-minute trend, no-demand/no-supply prints in the trend's direction signal continuation.*
Grading: directional. Latest review: deprioritize (recommendation).

**S0-H10** — session × window grid (cells as in the matrix):

| session | backtest | forward |
|---|---|---|
| whole | ·i-1.7pp (30/154) · p+0.1pp cap71.0 net+1774/med+11.0 | ▼i-5.3pp (25/156) · p-2.8pp cap56.0 net+230/med-0.5 |
| london | ▼i-19.5pp (2/40) · p+3.7pp cap116.0 net+1480/med+27.5 | ▲i+3.5pp (10/41) · p-1.5pp cap74.0 net+196/med-11.0 |
| overlap | (°▼i-11.4pp (0/5) · p-32.7pp cap— net+36/med+33.0) | (°▼i-13.8pp (0/1) · p-30.5pp cap— net+72/med+71.5) |
| ny_only | ▼i-3.8pp (4/26) · p+1.9pp cap80.9 net-348/med+48.8 | ▼i-8.1pp (6/48) · p-7.0pp cap98.0 net-509/med-5.5 |
| dead | ▲i+15.4pp (6/20) · p-7.1pp cap— net-74/med-5.7 | (°▼i-7.4pp (2/22) · p-3.2pp cap— net-64/med-3.2) |
| asia | ▲i+3.6pp (18/63) · p+3.0pp cap50.5 net+680/med+8.0 | ▼i-10.5pp (7/44) · p+8.6pp cap48.5 net+535/med+8.5 |

- backtest payoff: right +4228 / wrong -2454 / net +1774 pts; median per fire +11.00 (n=154)
- backtest best call: 2026-07-29 06:18 +859.5pts remaining (episode 948.5pts, major)
- backtest worst false alarm: 2026-08-03 17:10 -197.0pts adverse
- forward payoff: right +2315 / wrong -2086 / net +230 pts; median per fire -0.50 (n=156)
- forward best call: 2026-08-17 09:48 +176.5pts remaining (episode 249.0pts, major)
- forward worst false alarm: 2026-08-21 12:45 -141.0pts adverse
- earliness (backtest): median 87.5 pts of move remaining at fire (n=11)

### H11 — 2 signals
*Price entering a low-volume price zone traverses it faster than baseline; entering a high-volume node it stalls or reverses at above-baseline rates.*
Grading: directional. Latest review: keep-watching (recommendation).

**S0-H11** — session × window grid (cells as in the matrix):

| session | backtest | forward |
|---|---|---|
| whole | ·i-0.4pp (86/413) · p+3.5pp cap98.0 net+1254/med+3.0 | ·i-0.1pp (68/321) · p+4.7pp cap71.5 net-142/med-5.0 |
| london | ▼i-5.5pp (31/163) · p+1.1pp cap91.0 net-404/med+5.0 | ▼i-2.3pp (24/129) · p-0.9pp cap75.0 net+175/med+0.0 |
| overlap | (°▼i-7.6pp (1/26) · p+21.1pp cap261.2 net+491/med+4.0) | (°▼i-10.7pp (1/32) · p-2.4pp cap128.5 net+148/med-16.2) |
| ny_only | ▲i+9.4pp (12/42) · p-1.6pp cap239.5 net+1037/med+15.2 | ·i-1.2pp (7/36) · p+16.6pp cap109.5 net+18/med-7.8 |
| dead | ▼i-6.6pp (4/50) · p+14.9pp cap99.5 net+478/med+1.2 | (°▼i-5.0pp (3/26) · p-3.2pp cap— net-211/med-7.0) |
| asia | ▲i+3.8pp (38/132) · p-7.3pp cap62.5 net-348/med+2.0 | ▲i+7.3pp (33/98) · p-2.0pp cap35.0 net-273/med-4.5 |

- backtest payoff: right +12694 / wrong -11440 / net +1254 pts; median per fire +3.00 (n=413)
- backtest best call: 2026-07-29 06:20 +858.0pts remaining (episode 948.5pts, major)
- backtest worst false alarm: 2026-07-31 13:24 -492.5pts adverse
- forward payoff: right +5972 / wrong -6115 / net -142 pts; median per fire -5.00 (n=321)
- forward best call: 2026-08-19 09:21 +393.5pts remaining (episode 377.5pts, major)
- forward worst false alarm: 2026-08-19 12:55 -270.0pts adverse
- earliness (backtest): median 90.5 pts of move remaining at fire (n=23)

**S1-H11** — session × window grid (cells as in the matrix):

| session | backtest | forward |
|---|---|---|
| whole | ▲i+4.7pp (49/189) · p+1.5pp cap163.5 net+1560/med+0.5 | ▼i-6.8pp (12/83) · p+4.4pp cap118.0 net+218/med-14.0 |
| london | (°▼i-15.4pp (1/11) · p+9.2pp cap194.5 net+136/med-24.5) | ▼i-4.6pp (8/49) · p+0.7pp cap184.0 net+1074/med-14.0 |
| overlap | (°▲i+23.1pp (10/29) · p+12.1pp cap250.5 net+278/med+23.0) | (°▲i+86.2pp (1/1) · p-30.5pp cap— net-256/med-255.5) |
| ny_only | ▼i-12.8pp (3/47) · p+14.2pp cap181.4 net+1460/med+17.0 | (°▼i-20.6pp (0/7) · p-11.2pp cap— net-357/med-52.0) |
| dead | ▲i+26.3pp (9/22) · p+11.1pp cap86.0 net+232/med+18.2 | (°▼i-16.5pp (0/3) · p-3.2pp cap— net-51/med-25.5) |
| asia | ▲i+7.5pp (26/80) · p-7.8pp cap65.5 net-546/med-6.2 | ▼i-13.4pp (3/23) · p-8.1pp cap26.8 net-192/med-7.5 |

- backtest payoff: right +9216 / wrong -7657 / net +1560 pts; median per fire +0.50 (n=189)
- backtest best call: 2026-07-28 04:46 +523.0pts remaining (episode 543.0pts, major)
- backtest worst false alarm: 2026-07-29 18:58 -665.0pts adverse
- forward payoff: right +2743 / wrong -2525 / net +218 pts; median per fire -14.00 (n=83)
- forward best call: 2026-08-20 09:30 +392.0pts remaining (episode 415.0pts, major)
- forward worst false alarm: 2026-08-19 11:55 -277.0pts adverse
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
| whole | (°▲i+78.8pp (1/1) · p-23.9pp cap— net-206/med-206.0) | — |
| london | (°▲i+75.5pp (1/1) · p-36.3pp cap— net-206/med-206.0) | — |
| overlap | — | — |
| ny_only | — | — |
| dead | — | — |
| asia | — | — |

- backtest payoff: right +0 / wrong -206 / net -206 pts; median per fire -206.00 (n=1)
- backtest best call: 2026-07-28 10:27 +-158.5pts remaining (episode 93.5pts)
- backtest worst false alarm: 2026-07-28 10:27 -252.0pts adverse
- earliness (backtest): median -158.5 pts of move remaining at fire (n=1)

### H14 — 1 signal
*Counter-trend No Demand / No Supply prints in an established trend mark absorption and precede trend continuation.*
Grading: directional. Latest review: keep-watching (recommendation).

**S0-H14** — session × window grid (cells as in the matrix):

| session | backtest | forward |
|---|---|---|
| whole | ▲i+3.8pp (37/148) · p+1.8pp cap76.0 net+2606/med+12.5 | ▼i-6.3pp (20/133) · p-3.8pp cap81.5 net-216/med-5.0 |
| london | ▼i-18.1pp (3/47) · p+8.4pp cap121.5 net+1414/med+12.5 | ▲i+4.1pp (10/40) · p-3.1pp cap92.5 net+362/med-5.0 |
| overlap | (°▼i-11.4pp (0/7) · p-32.7pp cap— net-40/med+17.0) | (°▲i+19.5pp (1/3) · p-30.5pp cap— net+1/med-10.0) |
| ny_only | ▼i-2.0pp (5/29) · p-3.2pp cap84.4 net+804/med+53.0 | ▼i-14.9pp (2/35) · p+3.1pp cap118.0 net-578/med-20.0 |
| dead | (°▲i+38.0pp (10/19) · p-1.8pp cap104.9 net-80/med-14.4) | (°▼i-11.7pp (1/21) · p-3.2pp cap— net-28/med-2.5) |
| asia | ▲i+16.3pp (19/46) · p+4.3pp cap35.0 net+508/med+7.5 | ▼i-8.8pp (6/34) · p-4.9pp cap43.0 net+28/med+1.0 |

- backtest payoff: right +4618 / wrong -2012 / net +2606 pts; median per fire +12.50 (n=148)
- backtest best call: 2026-08-03 05:18 +451.0pts remaining (episode 472.0pts, major)
- backtest worst false alarm: 2026-07-28 13:00 -258.0pts adverse
- forward payoff: right +1843 / wrong -2058 / net -216 pts; median per fire -5.00 (n=133)
- forward best call: 2026-08-17 09:50 +175.0pts remaining (episode 249.0pts, major)
- forward worst false alarm: 2026-08-21 12:50 -124.0pts adverse
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
| whole | (°▼i-21.2pp (0/10) · p+26.1pp cap100.0 net+522/med+37.5) | (°▼i-21.3pp (0/6) · p+26.7pp cap63.0 net+125/med+43.5) |
| london | — | — |
| overlap | — | — |
| ny_only | (°▼i-19.2pp (0/10) · p+36.5pp cap100.0 net+522/med+37.5) | (°▼i-20.6pp (0/6) · p+38.8pp cap63.0 net+125/med+43.5) |
| dead | — | — |
| asia | — | — |

- backtest payoff: right +588 / wrong -66 / net +522 pts; median per fire +37.50 (n=10)
- backtest worst false alarm: 2026-07-28 19:30 -58.0pts adverse
- forward payoff: right +198 / wrong -73 / net +125 pts; median per fire +43.50 (n=6)
- forward worst false alarm: 2026-08-21 19:30 -73.0pts adverse


---

Appendix: the per-session detail beyond London and every horizon-mark payoff live in hypothesis_performance.json (generated, same run).