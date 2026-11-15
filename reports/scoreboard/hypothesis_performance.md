# Hypothesis Performance — Per-Instrument

Terms: [docs/GLOSSARY.md](../../docs/GLOSSARY.md).

Engine `66be26997` — register 40 fence as amended 2026-08-19 (operator): one section per instrument, each computed only from that instrument's own store and native calendar; uk100 canonical, ger40/nas100/us30 PROVISIONAL (validation pending). Numbers are NEVER pooled across instruments — cross-instrument aggregation is a future registration. This first cross-instrument read is EXPLORATORY: expectations deliberately unregistered; anything interesting becomes a pre-registered question before it becomes a claim.

---

# uk100 (uk100fut) — CANONICAL

Store span (1M, close ts): 2026-07-12 22:06:00+00:00 → 2026-11-06 20:59:00+00:00. Volume type: real futures volume (step-zero audit).

## Summary Matrix (page 1)

Engine `66be26997` — OBSERVATIONAL signal scoreboard - move-detection, not trading; no fills exist here by construction; never validation (docs/hypothesis_lifecycle.md stage 4)

**Review labels are RECOMMENDATIONS — none actioned, review pending operator familiarity.** Cells: marker + precision LIFT vs that context's OWN chance rate, (hits/fires), payoff net/median points (directional rows; either-direction rows have no payoff by construction). ▲/▼ = beyond ±2pp of chance, · = within. (°…) = small-n (fires<20 or episodes<10): dimmed, excluded from any future label arithmetic. Read READING_GUIDE.md first; full detail in hypothesis_performance.json.

| H | label | backtest whole | backtest london | forward whole | forward london |
|---|---|---|---|---|---|
| *context* | | 178 ep; chance 23.7%dir/44.4%either | 53 ep; chance 24.9%dir/47.1%either | 592 ep; chance 25.0%dir/45.9%either | 159 ep; chance 27.6%dir/52.6%either |
| S0-H1 | keep-watching | ▲i+8.0pp (22/69) · p-0.5pp cap39.0 net+194/med+2.8 | ▲i+5.2pp (7/22) · p+6.9pp cap38.8 net+133/med+3.0 | ·i-1.4pp (105/531) · p-0.1pp cap22.2 net-178/med-0.3 | ▲i+2.0pp (32/130) · p-2.2pp cap26.0 net-249/med-1.6 |
| S1-H1 | keep-watching | (°▼i-3.9pp (1/5) · p-3.7pp cap59.3 net+9/med+3.0) | — | ·i-0.7pp (8/39) · p-12.2pp cap18.5 net-17/med-1.4 | (°▲i+13.8pp (4/11) · p-9.4pp cap25.8 net-52/med-13.8) |
| S0-H2 | promote-candidate | ·i-0.8pp (80/347) · p+1.4pp cap34.5 net+781/med+1.5 | ▼i-4.1pp (18/80) · p+7.6pp cap39.6 net+521/med+9.2 | ▼i-4.1pp (381/2233) · p-1.0pp cap25.0 net+2348/med+0.2 | ▼i-8.0pp (65/444) · p-2.1pp cap32.0 net+490/med+0.8 |
| S1-H2 | promote-candidate | ·i-0.5pp (59/252) · p+0.9pp cap34.1 net+540/med+0.9 | ·i+0.5pp (16/59) · p+7.3pp cap38.8 net+559/med+12.0 | ·i-1.4pp (325/1638) · p-0.5pp cap23.3 net+1107/med+0.2 | ▼i-4.6pp (57/316) · p-1.7pp cap30.8 net-96/med+0.0 |
| S0-H3 | keep-watching | — | — | ▲i+4.8pp (13/50) · p+5.0pp cap18.5 net+16/med+0.8 | (°▲i+10.7pp (3/9) · p-5.4pp cap23.4 net-13/med-1.0) |
| S0-H4 | keep-watching | (°▲i+19.0pp (3/7) · p-23.7pp cap— net+14/med+0.5) | (°▼i-26.6pp (0/1) · p-24.9pp cap— net+6/med+5.5) | (°▼i-21.2pp (0/1) · p+75.0pp cap33.5 net+8/med+8.5) | — |
| S0-H5 | keep-watching | — | — | (°▼i-21.2pp (0/1) · p-25.0pp cap— net+5/med+5.0) | — |
| S0-H6 | keep-watching | ·i+1.6pp (9/59) · p+8.2pp cap33.8 [cls 37.6%/13.7%i] net+391/med+5.7 | ·i+0.4pp (4/31) · p+20.6pp cap32.9 [cls 37.5%/12.5%i] net+282/med+16.0 | ·i+0.5pp (46/401) · p+6.4pp cap27.5 [cls 43.0%/11.0%i] net+675/med+4.0 | ·i-1.6pp (22/217) · p+9.6pp cap27.5 [cls 39.2%/11.7%i] net+1020/med+6.0 |
| S0-H7 | keep-watching | ▲i+4.7pp (32/112) · p+8.4pp cap30.3 net+7/med+2.8 | ▲i+5.1pp (13/41) · p+6.8pp cap27.3 net-217/med+2.7 | ▲i+3.4pp (107/435) · p+3.3pp cap24.2 net+283/med+0.7 | ·i+1.9pp (37/151) · p+6.2pp cap28.8 net+74/med-0.2 |
| S0-H7 (either-dir) | keep-watching | ▼i-3.5pp (44/112) · p+10.1pp cap18.5 | ▼i-3.4pp (18/41) · p+6.6pp cap22.7 | ▼i-2.9pp (156/435) · p+3.8pp cap12.5 | ▼i-5.9pp (55/151) · p+5.0pp cap18.5 |
| S0-H8 | keep-watching | ▼i-3.6pp (136/347) · p+2.0pp cap17.0 | ▼i-16.1pp (25/80) · p+7.9pp cap33.1 | ▼i-5.9pp (735/2233) · p-1.9pp cap11.5 | ▼i-8.3pp (151/444) · p-5.1pp cap21.5 |
| S0-H9 | keep-watching | ▲i+5.2pp (16/55) · p+5.4pp cap31.9 net+319/med+3.5 | (°▼i-17.5pp (1/11) · p+20.6pp cap45.0 net+108/med+12.5) | ▼i-4.6pp (51/308) · p-1.0pp cap24.8 net+469/med+0.0 | ·i-0.4pp (14/63) · p-3.8pp cap28.7 net-163/med-2.5 |
| S1-H9 | keep-watching | (°▼i-13.4pp (2/19) · p+23.7pp cap45.0 net+263/med+12.8) | (°▼i-26.6pp (0/8) · p+25.1pp cap57.1 net+148/med+17.8) | ▼i-16.6pp (6/131) · p-0.6pp cap30.3 net+96/med+0.9 | ▼i-18.6pp (1/25) · p-3.6pp cap35.5 net-147/med-3.5 |
| S0-H10 | deprioritize | ▼i-8.5pp (45/293) · p-3.9pp cap26.6 net-240/med-1.4 | ▼i-13.0pp (9/66) · p+2.4pp cap33.2 net-62/med+1.9 | ·i+1.9pp (290/1257) · p-6.3pp cap19.2 net-906/med-0.7 | ▲i+6.2pp (101/351) · p-1.7pp cap25.8 net-228/med-1.0 |
| S0-H11 | keep-watching | ·i+0.8pp (78/316) · p+1.6pp cap33.1 net-647/med-2.4 | ·i+1.8pp (42/148) · p-1.3pp cap35.0 net+250/med-0.6 | ▼i-5.5pp (136/868) · p-1.2pp cap27.8 net+46/med+0.5 | ▼i-3.5pp (89/465) · p-6.7pp cap30.5 net-570/med-1.0 |
| S1-H11 | keep-watching | ▼i-5.8pp (28/155) · p-1.8pp cap33.2 net-617/med-0.7 | ▼i-2.3pp (9/37) · p-8.7pp cap34.0 net-466/med-15.7 | ▼i-5.0pp (245/1515) · p+1.3pp cap22.5 net+92/med-0.3 | ▼i-6.2pp (90/548) · p+1.4pp cap24.3 net-241/med-0.5 |
| S0-H12 | keep-watching | — | — | — | — |
| S0-H13 | keep-watching | (°▲i+26.1pp (1/2) · p+26.3pp cap37.0 net+28/med+13.8) | (°▲i+23.4pp (1/2) · p+25.1pp cap37.0 net+28/med+13.8) | ▲i+3.1pp (9/37) · p-3.4pp cap30.5 net-51/med-1.5 | (°▲i+10.7pp (5/15) · p+5.7pp cap36.7 net+12/med-2.8) |
| S0-H14 | keep-watching | ▼i-8.3pp (46/294) · p-8.7pp cap24.8 net-695/med-1.9 | ▼i-10.5pp (10/62) · p-5.5pp cap28.1 net-81/med+3.1 | ·i+0.2pp (286/1336) · p-5.8pp cap19.4 net-1399/med-0.8 | ▲i+2.4pp (89/356) · p-0.4pp cap26.0 net-510/med-2.0 |
| S0-H15 | keep-watching | — | — | — | — |
| S0-H16 | keep-watching | (°▼i-3.9pp (3/15) · p+3.0pp cap33.4 net+5/med+6.0) | — | ▼i-9.3pp (7/59) · p-1.3pp cap26.6 net+76/med-1.3 | — |
| S0-H17 | rows | ▲i+10.2pp (14/41) · p-6.6pp cap41.5 net+76/med+2.5 | (°▲i+9.1pp (5/14) · p+3.7pp cap40.0 net+32/med+4.4) | ·i-0.6pp (58/281) · p-1.5pp cap22.7 net-18/med-0.5 | ▲i+4.2pp (19/71) · p-2.2pp cap30.8 net+25/med+0.5 |
| S0-H18 | rows | ▼i-4.2pp (12/61) · p+4.2pp cap34.0 net+169/med-1.0 | ▼i-14.6pp (3/25) · p+11.1pp cap45.5 net+266/med+1.3 | ▼i-8.2pp (21/161) · p+4.2pp cap24.2 net+160/med+1.5 | ▼i-6.6pp (13/81) · p-6.6pp cap27.2 net-160/med-0.5 |
| S0-H19 | rows | ▼i-4.7pp (41/213) · p-2.6pp cap35.2 net-631/med-1.5 | ▼i-13.0pp (6/44) · p-13.5pp cap55.5 net-334/med-11.0 | ▼i-4.0pp (231/1345) · p-2.8pp cap22.5 net-1948/med-0.2 | ▼i-3.2pp (47/242) · p-5.3pp cap30.8 net-515/med-1.1 |
| S0-H20 | rows | ▼i-9.7pp (2/50) · p-7.6pp cap62.0 [cls 37.6%/13.7%i] net-221/med-9.7 | ▼i-12.5pp (0/28) · p+1.8pp cap75.5 [cls 37.5%/12.5%i] net+241/med-5.2 | ▼i-8.8pp (7/312) · p+8.0pp cap29.1 [cls 43.0%/11.0%i] net+851/med-1.2 | ▼i-7.4pp (7/162) · p+5.2pp cap27.5 [cls 39.2%/11.7%i] net-541/med-6.2 |
| **union coverage** | | 60.1% (107/178) | 58.5% (31/53) | 83.3% (493/592) | 84.9% (135/159) |

### Dual-convention side-by-side — load-bearing patterns

| pattern | context | initiation | participation (cap) |
|---|---|---|---|
| Q1-H1 away cells (S0-H1) | uk100fut/forward | 19.8% (105/531) | 24.9% (cap 22.2) |
| Q1-H1 away cells (S0-H1) | ger40fut/forward | 22.7% (120/529) | 25.9% (cap 59.3) |
| Q1-H1 away cells (S0-H1) | nas100fut/forward | 20.4% (100/490) | 32.0% (cap 109.8) |
| Q1-H1 away cells (S0-H1) | us30fut/forward | 22.0% (167/758) | 28.8% (cap 104.5) |
| H2 forward (S0-H2) | uk100fut/forward | 17.1% (381/2233) | 24.0% (cap 25.0) |
| H2 forward (S0-H2) | ger40fut/forward | 18.6% (408/2188) | 23.5% (cap 60.5) |
| H2 forward (S0-H2) | nas100fut/forward | 16.2% (395/2438) | 27.8% (cap 103.9) |
| H2 forward (S0-H2) | us30fut/forward | 15.4% (411/2676) | 27.4% (cap 109.5) |
| H2 forward (S1-H2) | uk100fut/forward | 19.8% (325/1638) | 24.5% (cap 23.3) |
| H2 forward (S1-H2) | ger40fut/forward | 20.3% (321/1583) | 23.3% (cap 61.2) |
| H2 forward (S1-H2) | nas100fut/forward | 18.5% (324/1747) | 27.4% (cap 105.4) |
| H2 forward (S1-H2) | us30fut/forward | 16.9% (330/1950) | 26.3% (cap 103.5) |
| S0-H8 (either-dir) | uk100fut/backtest | 39.2% (136/347) | 46.4% (cap 17.0) |
| S0-H8 (either-dir) | ger40fut/backtest | 29.1% (68/234) | 53.4% (cap 36.4) |
| S0-H8 (either-dir) | nas100fut/backtest | 36.6% (117/320) | 43.4% (cap 69.4) |
| S0-H8 (either-dir) | us30fut/backtest | 26.7% (75/281) | 53.0% (cap 74.5) |
| S0-H6 (conditioned) | uk100fut/backtest | 15.3% (9/59) | 45.8% (cap 33.8) |
| S0-H6 (conditioned) | ger40fut/backtest | 2.8% (1/36) | 41.7% (cap 56.7) |
| S0-H6 (conditioned) | nas100fut/backtest | 17.2% (5/29) | 31.0% (cap 260.8) |
| S0-H6 (conditioned) | us30fut/backtest | 5.8% (3/52) | 19.2% (cap 175.0) |
| S0-H8 (either-dir) | uk100fut/forward | 32.9% (735/2233) | 44.0% (cap 11.5) |
| S0-H8 (either-dir) | ger40fut/forward | 38.0% (832/2188) | 44.0% (cap 29.6) |
| S0-H8 (either-dir) | nas100fut/forward | 33.2% (810/2438) | 48.6% (cap 65.7) |
| S0-H8 (either-dir) | us30fut/forward | 32.4% (868/2676) | 47.5% (cap 60.8) |
| S0-H6 (conditioned) | uk100fut/forward | 11.5% (46/401) | 49.4% (cap 27.5) |
| S0-H6 (conditioned) | ger40fut/forward | 17.0% (78/459) | 41.4% (cap 65.2) |
| S0-H6 (conditioned) | nas100fut/forward | 18.2% (73/402) | 39.8% (cap 103.5) |
| S0-H6 (conditioned) | us30fut/forward | 17.5% (86/492) | 39.2% (cap 123.0) |


Not graded:  — see register entries.

## Hypothesis Cards (page 2)

### H1 — 2 signals
*A climactic bar — extreme volume on a wide spread late in an extended move — marks exhaustion, and price then reverses against the climax direction.*
Grading: directional. Latest review: keep-watching (recommendation).

- Question **Q1-H1**: see the register entry (status there is authoritative).
**S0-H1** — session × window grid (cells as in the matrix):

| session | backtest | forward |
|---|---|---|
| whole | ▲i+8.0pp (22/69) · p-0.5pp cap39.0 net+194/med+2.8 | ·i-1.4pp (105/531) · p-0.1pp cap22.2 net-178/med-0.3 |
| london | ▲i+5.2pp (7/22) · p+6.9pp cap38.8 net+133/med+3.0 | ▲i+2.0pp (32/130) · p-2.2pp cap26.0 net-249/med-1.6 |
| overlap | (°▼i-16.7pp (0/2) · p+24.1pp cap27.5 net+35/med+17.7) | ▼i-4.7pp (3/30) · p-14.8pp cap34.5 net-7/med-0.1 |
| ny_only | ▲i+18.9pp (9/22) · p+7.9pp cap46.9 net+17/med+1.6 | ▼i-4.8pp (21/153) · p+9.2pp cap27.2 net+112/med+0.0 |
| dead | (°▲i+2.6pp (4/12) · p+7.4pp cap15.3 net+30/med+1.1) | ▲i+7.6pp (28/74) · p+5.1pp cap13.8 net+56/med+1.4 |
| asia | (°▼i-3.8pp (2/11) · p-23.8pp cap59.3 net-22/med-2.6) | ▼i-5.9pp (21/144) · p+0.1pp cap16.9 net-91/med-0.8 |

- backtest payoff: right +639 / wrong -445 / net +194 pts; median per fire +2.75 (n=68)
- backtest best call: 2026-07-29 04:04 +105.2pts remaining (episode 102.8pts, major)
- backtest worst false alarm: 2026-07-23 12:17 -70.7pts adverse
- forward payoff: right +3206 / wrong -3384 / net -178 pts; median per fire -0.30 (n=529)
- forward best call: 2026-09-18 09:51 +148.5pts remaining (episode 130.0pts, major)
- forward worst false alarm: 2026-10-01 06:37 -92.0pts adverse
- earliness (backtest): median 35.3 pts of move remaining at fire (n=21)

**S1-H1** — session × window grid (cells as in the matrix):

| session | backtest | forward |
|---|---|---|
| whole | (°▼i-3.9pp (1/5) · p-3.7pp cap59.3 net+9/med+3.0) | ·i-0.7pp (8/39) · p-12.2pp cap18.5 net-17/med-1.4 |
| london | — | (°▲i+13.8pp (4/11) · p-9.4pp cap25.8 net-52/med-13.8) |
| overlap | — | (°▼i-14.7pp (0/5) · p-24.8pp cap— net-24/med-7.8) |
| ny_only | (°▼i-22.0pp (0/1) · p-10.3pp cap— net-13/med-13.3) | (°▼i-18.5pp (0/2) · p-9.8pp cap— net-4/med-2.2) |
| dead | (°▼i-30.7pp (0/1) · p-17.6pp cap— net+3/med+3.0) | (°▲i+3.1pp (3/9) · p-17.9pp cap— net+10/med-1.6) |
| asia | (°▲i+11.3pp (1/3) · p+0.4pp cap59.3 net+19/med+5.5) | (°▼i-12.2pp (1/12) · p-9.6pp cap17.0 net+53/med+0.3) |

- backtest payoff: right +59 / wrong -50 / net +9 pts; median per fire +3.00 (n=5)
- backtest best call: 2026-07-29 04:04 +105.2pts remaining (episode 102.8pts, major)
- backtest worst false alarm: 2026-07-30 05:53 -37.6pts adverse
- forward payoff: right +189 / wrong -206 / net -17 pts; median per fire -1.40 (n=39)
- forward best call: 2026-10-02 07:58 +65.0pts remaining (episode 82.5pts, major)
- forward worst false alarm: 2026-08-20 15:03 -30.7pts adverse
- earliness (backtest): median 105.2 pts of move remaining at fire (n=1)

### H2 — 2 signals
*A failed probe beyond a prior extreme — an upthrust above or spring below that closes back inside — reverses against the probe.*
Grading: directional. Latest review: promote-candidate (recommendation).

**S0-H2** — session × window grid (cells as in the matrix):

| session | backtest | forward |
|---|---|---|
| whole | ·i-0.8pp (80/347) · p+1.4pp cap34.5 net+781/med+1.5 | ▼i-4.1pp (381/2233) · p-1.0pp cap25.0 net+2348/med+0.2 |
| london | ▼i-4.1pp (18/80) · p+7.6pp cap39.6 net+521/med+9.2 | ▼i-8.0pp (65/444) · p-2.1pp cap32.0 net+490/med+0.8 |
| overlap | (°▼i-7.6pp (1/11) · p+1.4pp cap39.0 net+21/med+3.5) | ▼i-3.1pp (15/129) · p+3.9pp cap36.3 net+724/med+5.3 |
| ny_only | ▼i-5.6pp (9/55) · p+4.2pp cap40.8 net-487/med-2.5 | ▼i-2.5pp (85/532) · p+3.4pp cap31.2 net+686/med-0.2 |
| dead | ▼i-2.9pp (25/90) · p+1.3pp cap23.2 net+180/med+0.8 | ▼i-6.9pp (71/305) · p-1.5pp cap14.5 net+117/med+0.2 |
| asia | ▲i+2.3pp (27/111) · p-3.2pp cap29.8 net+546/med+2.7 | ▼i-2.9pp (145/823) · p-2.4pp cap18.7 net+331/med+0.0 |

- backtest payoff: right +3270 / wrong -2490 / net +781 pts; median per fire +1.50 (n=347)
- backtest best call: 2026-07-30 04:03 +155.1pts remaining (episode 178.3pts, major)
- backtest worst false alarm: 2026-07-24 06:52 -98.0pts adverse
- forward payoff: right +15314 / wrong -12965 / net +2348 pts; median per fire +0.20 (n=2231)
- forward best call: 2026-11-04 03:18 +362.5pts remaining (episode 364.5pts, major)
- forward worst false alarm: 2026-09-01 08:00 -94.5pts adverse
- earliness (backtest): median 29.3 pts of move remaining at fire (n=37)

**S1-H2** — session × window grid (cells as in the matrix):

| session | backtest | forward |
|---|---|---|
| whole | ·i-0.5pp (59/252) · p+0.9pp cap34.1 net+540/med+0.9 | ·i-1.4pp (325/1638) · p-0.5pp cap23.3 net+1107/med+0.2 |
| london | ·i+0.5pp (16/59) · p+7.3pp cap38.8 net+559/med+12.0 | ▼i-4.6pp (57/316) · p-1.7pp cap30.8 net-96/med+0.0 |
| overlap | (°▼i-7.6pp (1/11) · p+1.4pp cap39.0 net+21/med+3.5) | ▼i-2.5pp (11/90) · p+3.0pp cap34.3 net+259/med+3.6 |
| ny_only | ▼i-4.5pp (7/40) · p+4.7pp cap38.6 net-304/med-2.1 | ·i+0.0pp (72/390) · p+4.0pp cap30.6 net+917/med+0.7 |
| dead | ▼i-6.1pp (15/61) · p+5.4pp cap23.0 net+201/med+0.8 | ▼i-6.4pp (57/240) · p+0.9pp cap14.4 net+33/med-0.2 |
| asia | ▲i+2.7pp (20/81) · p-8.2pp cap28.4 net+62/med-1.2 | ·i+0.8pp (128/602) · p-2.2pp cap16.2 net-5/med-0.1 |

- backtest payoff: right +2121 / wrong -1581 / net +540 pts; median per fire +0.95 (n=252)
- backtest best call: 2026-07-30 04:03 +155.1pts remaining (episode 178.3pts, major)
- backtest worst false alarm: 2026-07-29 19:00 -94.0pts adverse
- forward payoff: right +10698 / wrong -9591 / net +1107 pts; median per fire +0.20 (n=1637)
- forward best call: 2026-11-04 03:18 +362.5pts remaining (episode 364.5pts, major)
- forward worst false alarm: 2026-09-01 08:00 -94.5pts adverse
- earliness (backtest): median 32.1 pts of move remaining at fire (n=34)

### H3 — 1 signal
*Repeated absorption — high effort with no result — at a price level precedes a breakout through that level.*
Grading: directional. Latest review: keep-watching (recommendation).

**S0-H3** — session × window grid (cells as in the matrix):

| session | backtest | forward |
|---|---|---|
| whole | — | ▲i+4.8pp (13/50) · p+5.0pp cap18.5 net+16/med+0.8 |
| london | — | (°▲i+10.7pp (3/9) · p-5.4pp cap23.4 net-13/med-1.0) |
| overlap | — | (°▼i-14.7pp (0/2) · p-24.8pp cap— net-42/med-20.9) |
| ny_only | — | (°▼i-6.0pp (1/8) · p-9.8pp cap— net-7/med+1.4) |
| dead | — | (°▲i+3.1pp (1/3) · p+48.8pp cap14.9 net+9/med-0.2) |
| asia | — | ▲i+8.1pp (8/28) · p+4.7pp cap18.0 net+69/med+1.8 |

- forward payoff: right +218 / wrong -201 / net +16 pts; median per fire +0.75 (n=50)
- forward best call: 2026-10-15 05:18 +82.8pts remaining (episode 84.5pts, major)
- forward worst false alarm: 2026-11-03 14:30 -44.0pts adverse

### H4 — 1 signal
*In an established trend, a quiet (low-volume) pullback resolves with trend resumption.*
Grading: directional. Latest review: keep-watching (recommendation).

**S0-H4** — session × window grid (cells as in the matrix):

| session | backtest | forward |
|---|---|---|
| whole | (°▲i+19.0pp (3/7) · p-23.7pp cap— net+14/med+0.5) | (°▼i-21.2pp (0/1) · p+75.0pp cap33.5 net+8/med+8.5) |
| london | (°▼i-26.6pp (0/1) · p-24.9pp cap— net+6/med+5.5) | — |
| overlap | — | — |
| ny_only | (°▲i+28.0pp (3/6) · p-10.3pp cap— net+8/med-0.1) | — |
| dead | — | — |
| asia | — | (°▼i-20.5pp (0/1) · p+65.4pp cap33.5 net+8/med+8.5) |

- backtest payoff: right +27 / wrong -13 / net +14 pts; median per fire +0.50 (n=7)
- backtest best call: 2026-07-28 16:11 +11.3pts remaining (episode 28.8pts)
- backtest worst false alarm: 2026-07-28 16:11 -17.5pts adverse
- forward payoff: right +8 / wrong +0 / net +8 pts; median per fire +8.50 (n=1)
- earliness (backtest): median 11.3 pts of move remaining at fire (n=1)

### H5 — 1 signal
*A buying climax that extends far above its trend mean mean-reverts (climax-extension fade; registered short-side only).*
Grading: directional. Latest review: keep-watching (recommendation).

**S0-H5** — session × window grid (cells as in the matrix):

| session | backtest | forward |
|---|---|---|
| whole | — | (°▼i-21.2pp (0/1) · p-25.0pp cap— net+5/med+5.0) |
| london | — | — |
| overlap | — | — |
| ny_only | — | (°▼i-18.5pp (0/1) · p-9.8pp cap— net+5/med+5.0) |
| dead | — | — |
| asia | — | — |

- forward payoff: right +5 / wrong +0 / net +5 pts; median per fire +5.00 (n=1)
- forward worst false alarm: 2026-09-25 16:15 -2.2pts adverse

### H6 — 1 signal
*A wide-spread rejection bar at a session extreme (measured day-relative, volume-agnostic) reverses away from the extreme.*
Grading: directional. Latest review: keep-watching (recommendation).

- Question **Q1-H6**: see the register entry (status there is authoritative).
- Question **Q2-H6**: see the register entry (status there is authoritative).
- Question **Q3-H6**: see the register entry (status there is authoritative).
**S0-H6** — session × window grid (cells as in the matrix):

| session | backtest | forward |
|---|---|---|
| whole | ·i+1.6pp (9/59) · p+8.2pp cap33.8 [cls 37.6%/13.7%i] net+391/med+5.7 | ·i+0.5pp (46/401) · p+6.4pp cap27.5 [cls 43.0%/11.0%i] net+675/med+4.0 |
| london | ·i+0.4pp (4/31) · p+20.6pp cap32.9 [cls 37.5%/12.5%i] net+282/med+16.0 | ·i-1.6pp (22/217) · p+9.6pp cap27.5 [cls 39.2%/11.7%i] net+1020/med+6.0 |
| overlap | (°▲i+32.2pp (3/6) · p-30.8pp cap— [cls 30.8%/17.8%i] net-87/med-15.4) | ▲i+3.6pp (8/46) · p+8.6pp cap30.7 [cls 32.7%/13.8%i] net+19/med+2.5 |
| ny_only | (°▲i+35.6pp (2/4) · p-20.9pp cap— [cls 20.9%/14.4%i] net+0/med+6.5) | (°▼i-3.0pp (1/15) · p-6.6pp cap51.2 [cls 19.9%/9.7%i] net-59/med-2.5) |
| dead | (°▼i-9.6pp (0/5) · p-19.1pp cap— [cls 19.1%/9.6%i] net-25/med-6.4) | (°▲i+40.8pp (1/2) · p+29.6pp cap55.0 [cls 20.4%/9.2%i] net+20/med+9.8) |
| asia | (°▼i-13.9pp (0/13) · p+24.6pp cap44.8 [cls 44.6%/13.9%i] net+220/med+5.7) | ▲i+2.2pp (14/121) · p+2.6pp cap23.3 [cls 55.3%/9.4%i] net-325/med-0.4 |

- backtest payoff: right +818 / wrong -428 / net +391 pts; median per fire +5.70 (n=59)
- backtest best call: 2026-07-31 08:00 +72.8pts remaining (episode 70.3pts, major)
- backtest worst false alarm: 2026-07-22 08:07 -80.3pts adverse
- forward payoff: right +4211 / wrong -3536 / net +675 pts; median per fire +4.00 (n=401)
- forward best call: 2026-10-02 08:13 +82.7pts remaining (episode 82.5pts, major)
- forward worst false alarm: 2026-10-01 06:58 -100.0pts adverse
- earliness (backtest): median 21.6 pts of move remaining at fire (n=8)

### H7 — 1 signal
*Quiet decline at a session extreme is disguised accumulation: effortless (low-volume) weakness reverses UP once selling fails to attract participation (mirror: quiet advance at a high reverses down).*
Grading: directional + either-direction (dual). Latest review: keep-watching (recommendation).

- Question **Q1-H7**: see the register entry (status there is authoritative).
**S0-H7** — session × window grid (cells as in the matrix):

| session | backtest | forward |
|---|---|---|
| whole | ▲i+4.7pp (32/112) · p+8.4pp cap30.3 net+7/med+2.8 | ▲i+3.4pp (107/435) · p+3.3pp cap24.2 net+283/med+0.7 |
| london | ▲i+5.1pp (13/41) · p+6.8pp cap27.3 net-217/med+2.7 | ·i+1.9pp (37/151) · p+6.2pp cap28.8 net+74/med-0.2 |
| overlap | ▼i-3.7pp (3/23) · p+13.2pp cap38.8 net+227/med+8.7 | ▲i+8.3pp (14/61) · p+3.1pp cap34.0 net+24/med+1.8 |
| ny_only | (°·i-0.6pp (3/14) · p+4.0pp cap27.6 net-24/med+0.0) | ▲i+3.0pp (14/65) · p+2.5pp cap29.8 net+143/med+3.5 |
| dead | (°▲i+49.3pp (4/5) · p+2.4pp cap51.1 net+60/med+3.5) | (°▼i-2.4pp (5/18) · p-1.2pp cap27.9 net+43/med-1.2) |
| asia | ▲i+9.0pp (9/29) · p+5.0pp cap20.7 net-38/med+0.7 | ▲i+5.9pp (37/140) · p-3.2pp cap15.1 net-1/med+0.1 |

- backtest payoff: right +1097 / wrong -1090 / net +7 pts; median per fire +2.80 (n=112)
- backtest best call: 2026-07-22 04:18 +132.7pts remaining (episode 138.3pts, major)
- backtest worst false alarm: 2026-07-30 06:55 -94.0pts adverse
- forward payoff: right +3254 / wrong -2972 / net +283 pts; median per fire +0.70 (n=435)
- forward best call: 2026-10-01 04:35 +166.3pts remaining (episode 175.3pts, major)
- forward worst false alarm: 2026-11-05 15:11 -91.3pts adverse
- earliness (backtest): median 29.8 pts of move remaining at fire (n=29)

**S0-H7 (either-dir)** — session × window grid (cells as in the matrix):

| session | backtest | forward |
|---|---|---|
| whole | ▼i-3.5pp (44/112) · p+10.1pp cap18.5 | ▼i-2.9pp (156/435) · p+3.8pp cap12.5 |
| london | ▼i-3.4pp (18/41) · p+6.6pp cap22.7 | ▼i-5.9pp (55/151) · p+5.0pp cap18.5 |
| overlap | ·i-0.6pp (7/23) · p+10.0pp cap31.2 | ·i+0.2pp (18/61) · p+6.3pp cap20.2 |
| ny_only | (°▼i-17.6pp (3/14) · p+8.3pp cap13.4) | ▲i+5.0pp (25/65) · p+3.7pp cap18.0 |
| dead | (°▲i+27.3pp (4/5) · p-12.8pp cap51.1) | (°▼i-8.8pp (8/18) · p+0.0pp cap9.4) |
| asia | ·i+0.6pp (12/29) · p+9.3pp cap10.1 | ·i-1.2pp (50/140) · p-6.6pp cap9.8 |

- backtest payoff: n/a by construction (either-direction)
- backtest best call: 2026-07-22 04:18 +132.7pts remaining (episode 138.3pts, major)
- backtest worst false alarm: 2026-07-23 16:44 -25.7pts adverse
- forward payoff: n/a by construction (either-direction)
- forward best call: 2026-10-01 04:35 +166.3pts remaining (episode 175.3pts, major)
- forward worst false alarm: 2026-11-04 10:35 -28.3pts adverse
- earliness (backtest): median 16.8 pts of move remaining at fire (n=40)

### H8 — 1 signal
*Reversal-signature bar anatomy (upthrust/spring) predicts imminent range expansion irrespective of direction.*
Grading: either-direction. Latest review: keep-watching (recommendation).

**S0-H8** — session × window grid (cells as in the matrix):

| session | backtest | forward |
|---|---|---|
| whole | ▼i-3.6pp (136/347) · p+2.0pp cap17.0 | ▼i-5.9pp (735/2233) · p-1.9pp cap11.5 |
| london | ▼i-16.1pp (25/80) · p+7.9pp cap33.1 | ▼i-8.3pp (151/444) · p-5.1pp cap21.5 |
| overlap | (°▼i-12.8pp (2/11) · p+3.6pp cap18.9) | ▼i-4.5pp (32/129) · p-6.0pp cap28.8 |
| ny_only | ▼i-8.1pp (17/55) · p+23.3pp cap6.9 | ▼i-3.8pp (158/532) · p+4.5pp cap15.8 |
| dead | ▼i-3.8pp (44/90) · p+1.6pp cap13.9 | ▼i-12.9pp (123/305) · p+1.5pp cap6.6 |
| asia | ▲i+2.4pp (48/111) · p-9.2pp cap19.0 | ▼i-4.0pp (271/823) · p-0.9pp cap9.8 |

- backtest payoff: n/a by construction (either-direction)
- backtest best call: 2026-07-30 04:03 +155.1pts remaining (episode 178.3pts, major)
- backtest worst false alarm: 2026-07-30 11:13 -30.5pts adverse
- forward payoff: n/a by construction (either-direction)
- forward best call: 2026-11-04 03:02 +364.0pts remaining (episode 364.5pts, major)
- forward worst false alarm: 2026-11-06 10:35 -36.0pts adverse
- earliness (backtest): median 27.2 pts of move remaining at fire (n=57)

### H9 — 2 signals
*Persistent lower-TF directional pressure that recruits expanding participation at the parent timeframe precedes continuation beyond what the parent label alone predicts; pressure without participation expansion does not.*
Grading: directional. Latest review: keep-watching (recommendation).

- Question **Q2-H9**: see the register entry (status there is authoritative).
**S0-H9** — session × window grid (cells as in the matrix):

| session | backtest | forward |
|---|---|---|
| whole | ▲i+5.2pp (16/55) · p+5.4pp cap31.9 net+319/med+3.5 | ▼i-4.6pp (51/308) · p-1.0pp cap24.8 net+469/med+0.0 |
| london | (°▼i-17.5pp (1/11) · p+20.6pp cap45.0 net+108/med+12.5) | ·i-0.4pp (14/63) · p-3.8pp cap28.7 net-163/med-2.5 |
| overlap | — | ▲i+21.7pp (12/33) · p+17.6pp cap31.7 net+367/med+5.2 |
| ny_only | (°▲i+19.7pp (5/12) · p+14.7pp cap69.9 net+115/med+2.8) | ▼i-7.5pp (9/82) · p+13.4pp cap18.0 net+135/med+0.7 |
| dead | (°▼i-3.4pp (3/11) · p-8.5pp cap26.6 net+11/med+1.0) | ▼i-24.1pp (2/33) · p-11.8pp cap10.0 net+47/med+0.8 |
| asia | ▲i+11.3pp (7/21) · p+0.4pp cap13.5 net+86/med+6.8 | ▼i-6.1pp (14/97) · p-9.9pp cap24.2 net+82/med-2.0 |

- backtest payoff: right +558 / wrong -239 / net +319 pts; median per fire +3.50 (n=53)
- backtest best call: 2026-08-03 03:40 +73.2pts remaining (episode 81.3pts, major)
- backtest worst false alarm: 2026-07-30 09:15 -59.3pts adverse
- forward payoff: right +1979 / wrong -1510 / net +469 pts; median per fire +0.00 (n=303)
- forward best call: 2026-10-15 04:30 +77.8pts remaining (episode 84.5pts, major)
- forward worst false alarm: 2026-09-01 08:00 -94.5pts adverse
- earliness (backtest): median 15.6 pts of move remaining at fire (n=10)

**S1-H9** — session × window grid (cells as in the matrix):

| session | backtest | forward |
|---|---|---|
| whole | (°▼i-13.4pp (2/19) · p+23.7pp cap45.0 net+263/med+12.8) | ▼i-16.6pp (6/131) · p-0.6pp cap30.3 net+96/med+0.9 |
| london | (°▼i-26.6pp (0/8) · p+25.1pp cap57.1 net+148/med+17.8) | ▼i-18.6pp (1/25) · p-3.6pp cap35.5 net-147/med-3.5 |
| overlap | — | (°▼i-14.7pp (0/6) · p+25.2pp cap57.0 net+129/med+7.5) |
| ny_only | (°▼i-22.0pp (0/4) · p+64.7pp cap69.9 net+105/med+31.6) | ▼i-18.5pp (0/38) · p+19.1pp cap22.7 net-19/med-2.4 |
| dead | (°▼i-10.7pp (1/5) · p+2.4pp cap26.6 net+6/med+2.3) | (°▼i-23.1pp (1/14) · p-17.9pp cap— net+56/med+4.6) |
| asia | (°▲i+28.0pp (1/2) · p+17.1pp cap20.2 net+4/med+2.1) | ▼i-12.2pp (4/48) · p-9.6pp cap22.2 net+78/med+0.8 |

- backtest payoff: right +377 / wrong -114 / net +263 pts; median per fire +12.75 (n=18)
- backtest best call: 2026-07-19 23:10 +9.2pts remaining (episode 30.7pts)
- backtest worst false alarm: 2026-07-30 09:15 -59.3pts adverse
- forward payoff: right +936 / wrong -840 / net +96 pts; median per fire +0.90 (n=128)
- forward best call: 2026-10-15 04:30 +77.8pts remaining (episode 84.5pts, major)
- forward worst false alarm: 2026-09-01 08:00 -94.5pts adverse
- earliness (backtest): median 9.2 pts of move remaining at fire (n=1)

### H10 — 1 signal
*In an established 1-minute trend, no-demand/no-supply prints in the trend's direction signal continuation.*
Grading: directional. Latest review: deprioritize (recommendation).

**S0-H10** — session × window grid (cells as in the matrix):

| session | backtest | forward |
|---|---|---|
| whole | ▼i-8.5pp (45/293) · p-3.9pp cap26.6 net-240/med-1.4 | ·i+1.9pp (290/1257) · p-6.3pp cap19.2 net-906/med-0.7 |
| london | ▼i-13.0pp (9/66) · p+2.4pp cap33.2 net-62/med+1.9 | ▲i+6.2pp (101/351) · p-1.7pp cap25.8 net-228/med-1.0 |
| overlap | (°▼i-16.7pp (0/7) · p-25.9pp cap— net+27/med+6.8) | ▼i-3.8pp (10/92) · p-12.8pp cap23.0 net-168/med+0.2 |
| ny_only | ·i-1.5pp (17/83) · p-0.7pp cap25.3 net+51/med-1.5 | ·i+1.7pp (59/292) · p-5.3pp cap13.5 net+31/med+0.0 |
| dead | ·i-0.1pp (11/36) · p-3.7pp cap11.5 net-110/med-2.5 | ·i+0.0pp (48/159) · p-6.0pp cap13.5 net-208/med-0.7 |
| asia | ▼i-14.1pp (8/101) · p-6.2pp cap24.7 net-147/med-1.5 | ·i-0.7pp (72/363) · p-6.8pp cap11.2 net-332/med-1.7 |

- backtest payoff: right +1533 / wrong -1773 / net -240 pts; median per fire -1.40 (n=293)
- backtest best call: 2026-07-23 10:20 +90.0pts remaining (episode 104.8pts, major)
- backtest worst false alarm: 2026-07-28 13:10 -62.5pts adverse
- forward payoff: right +5455 / wrong -6361 / net -906 pts; median per fire -0.70 (n=1254)
- forward best call: 2026-10-19 04:56 +107.2pts remaining (episode 107.2pts, major)
- forward worst false alarm: 2026-10-06 09:37 -51.2pts adverse
- earliness (backtest): median 19.9 pts of move remaining at fire (n=25)

### H11 — 2 signals
*Price entering a low-volume price zone traverses it faster than baseline; entering a high-volume node it stalls or reverses at above-baseline rates.*
Grading: directional. Latest review: keep-watching (recommendation).

- Question **Q1-H11**: see the register entry (status there is authoritative).
- Question **Q2-H11**: see the register entry (status there is authoritative).
**S0-H11** — session × window grid (cells as in the matrix):

| session | backtest | forward |
|---|---|---|
| whole | ·i+0.8pp (78/316) · p+1.6pp cap33.1 net-647/med-2.4 | ▼i-5.5pp (136/868) · p-1.2pp cap27.8 net+46/med+0.5 |
| london | ·i+1.8pp (42/148) · p-1.3pp cap35.0 net+250/med-0.6 | ▼i-3.5pp (89/465) · p-6.7pp cap30.5 net-570/med-1.0 |
| overlap | ▲i+8.3pp (10/40) · p-18.4pp cap33.5 net-403/med-11.8 | ▼i-6.6pp (10/124) · p+7.5pp cap36.8 net+418/med+3.6 |
| ny_only | ▼i-6.2pp (6/38) · p+18.6pp cap34.0 net-267/med-1.6 | ▼i-3.3pp (20/132) · p+5.4pp cap17.9 net+201/med+2.5 |
| dead | ▼i-15.7pp (3/20) · p+37.4pp cap18.5 net+59/med+0.7 | ▼i-17.2pp (3/23) · p-9.2pp cap12.6 net-163/med-4.5 |
| asia | ▲i+2.3pp (17/70) · p-4.3pp cap23.7 net-286/med-4.5 | ▼i-9.2pp (14/124) · p+4.1pp cap16.6 net+161/med+2.0 |

- backtest payoff: right +2555 / wrong -3203 / net -647 pts; median per fire -2.35 (n=316)
- backtest best call: 2026-07-22 04:01 +129.4pts remaining (episode 138.3pts, major)
- backtest worst false alarm: 2026-07-22 07:36 -96.5pts adverse
- forward payoff: right +6306 / wrong -6260 / net +46 pts; median per fire +0.50 (n=868)
- forward best call: 2026-11-05 12:57 +193.0pts remaining (episode 190.0pts, major)
- forward worst false alarm: 2026-11-05 15:01 -107.0pts adverse
- earliness (backtest): median 25.5 pts of move remaining at fire (n=25)

**S1-H11** — session × window grid (cells as in the matrix):

| session | backtest | forward |
|---|---|---|
| whole | ▼i-5.8pp (28/155) · p-1.8pp cap33.2 net-617/med-0.7 | ▼i-5.0pp (245/1515) · p+1.3pp cap22.5 net+92/med-0.3 |
| london | ▼i-2.3pp (9/37) · p-8.7pp cap34.0 net-466/med-15.7 | ▼i-6.2pp (90/548) · p+1.4pp cap24.3 net-241/med-0.5 |
| overlap | ▼i-16.7pp (0/30) · p+4.1pp cap34.5 net+73/med-1.6 | ▼i-3.6pp (21/189) · p+3.8pp cap31.5 net+588/med+1.7 |
| ny_only | ▼i-7.7pp (6/42) · p+1.6pp cap20.8 net+75/med+0.7 | ▼i-5.6pp (33/256) · p+3.9pp cap26.5 net+50/med-0.2 |
| dead | (°▲i+44.3pp (3/4) · p-17.6pp cap— net-21/med-4.5) | ·i-0.6pp (24/81) · p-4.3pp cap14.6 net-115/med-0.3 |
| asia | ·i+1.8pp (10/42) · p+0.4pp cap34.3 net-277/med-0.9 | ▼i-3.0pp (77/441) · p-2.9pp cap15.6 net-191/med-0.3 |

- backtest payoff: right +1033 / wrong -1650 / net -617 pts; median per fire -0.70 (n=155)
- backtest best call: 2026-07-24 03:18 +96.3pts remaining (episode 104.3pts, major)
- backtest worst false alarm: 2026-07-31 07:01 -103.0pts adverse
- forward payoff: right +8699 / wrong -8608 / net +92 pts; median per fire -0.30 (n=1515)
- forward best call: 2026-10-15 04:27 +82.5pts remaining (episode 84.5pts, major)
- forward worst false alarm: 2026-09-15 06:58 -73.3pts adverse
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
| whole | (°▲i+26.1pp (1/2) · p+26.3pp cap37.0 net+28/med+13.8) | ▲i+3.1pp (9/37) · p-3.4pp cap30.5 net-51/med-1.5 |
| london | (°▲i+23.4pp (1/2) · p+25.1pp cap37.0 net+28/med+13.8) | (°▲i+10.7pp (5/15) · p+5.7pp cap36.7 net+12/med-2.8) |
| overlap | — | (°▲i+35.3pp (2/4) · p-24.8pp cap— net-26/med-4.5) |
| ny_only | — | (°▼i-18.5pp (0/3) · p-9.8pp cap— net+8/med+4.3) |
| dead | — | (°▼i-30.2pp (0/1) · p-17.9pp cap— net-4/med-3.9) |
| asia | — | (°▼i-6.2pp (2/14) · p-13.2pp cap12.8 net-40/med+0.2) |

- backtest payoff: right +28 / wrong +0 / net +28 pts; median per fire +13.75 (n=2)
- backtest best call: 2026-07-24 09:09 +43.2pts remaining (episode 42.7pts)
- backtest worst false alarm: 2026-07-24 09:09 -5.8pts adverse
- forward payoff: right +146 / wrong -196 / net -51 pts; median per fire -1.50 (n=37)
- forward best call: 2026-09-25 13:45 +53.5pts remaining (episode 74.2pts, major)
- forward worst false alarm: 2026-10-22 07:03 -29.0pts adverse
- earliness (backtest): median 43.2 pts of move remaining at fire (n=1)

### H14 — 1 signal
*Counter-trend No Demand / No Supply prints in an established trend mark absorption and precede trend continuation.*
Grading: directional. Latest review: keep-watching (recommendation).

**S0-H14** — session × window grid (cells as in the matrix):

| session | backtest | forward |
|---|---|---|
| whole | ▼i-8.3pp (46/294) · p-8.7pp cap24.8 net-695/med-1.9 | ·i+0.2pp (286/1336) · p-5.8pp cap19.4 net-1399/med-0.8 |
| london | ▼i-10.5pp (10/62) · p-5.5pp cap28.1 net-81/med+3.1 | ▲i+2.4pp (89/356) · p-0.4pp cap26.0 net-510/med-2.0 |
| overlap | (°▼i-16.7pp (0/4) · p-0.9pp cap24.0 net+20/med+5.6) | ▼i-8.2pp (6/92) · p-11.8pp cap25.2 net-302/med-1.1 |
| ny_only | ▼i-4.8pp (17/99) · p-1.2pp cap24.5 net-174/med-3.1 | ▲i+2.1pp (70/339) · p-3.9pp cap15.5 net-279/med+0.0 |
| dead | ▲i+8.7pp (13/33) · p-11.5pp cap17.2 net-105/med-2.4 | ▲i+4.8pp (56/160) · p-6.0pp cap15.6 net-212/med-1.1 |
| asia | ▼i-15.8pp (6/96) · p-12.1pp cap27.6 net-355/med-3.6 | ▼i-3.8pp (65/389) · p-6.8pp cap11.8 net-96/med-1.0 |

- backtest payoff: right +1293 / wrong -1989 / net -695 pts; median per fire -1.95 (n=294)
- backtest best call: 2026-07-31 11:45 +89.0pts remaining (episode 93.7pts, major)
- backtest worst false alarm: 2026-07-28 05:56 -59.0pts adverse
- forward payoff: right +5866 / wrong -7265 / net -1399 pts; median per fire -0.80 (n=1335)
- forward best call: 2026-10-19 04:36 +102.5pts remaining (episode 107.2pts, major)
- forward worst false alarm: 2026-08-27 08:05 -54.2pts adverse
- earliness (backtest): median 22.4 pts of move remaining at fire (n=24)

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
| whole | (°▼i-3.9pp (3/15) · p+3.0pp cap33.4 net+5/med+6.0) | ▼i-9.3pp (7/59) · p-1.3pp cap26.6 net+76/med-1.3 |
| london | — | — |
| overlap | (°▲i+3.3pp (3/15) · p+0.8pp cap33.4 net+5/med+6.0) | ▼i-2.8pp (7/59) · p-1.1pp cap26.6 net+76/med-1.3 |
| ny_only | — | — |
| dead | — | — |
| asia | — | — |

- backtest payoff: right +173 / wrong -169 / net +5 pts; median per fire +6.00 (n=15)
- backtest best call: 2026-08-03 15:00 +4.5pts remaining (episode 28.5pts)
- backtest worst false alarm: 2026-07-16 15:00 -61.7pts adverse
- forward payoff: right +509 / wrong -433 / net +76 pts; median per fire -1.30 (n=59)
- forward best call: 2026-09-28 15:00 +40.3pts remaining (episode 55.8pts, major)
- forward worst false alarm: 2026-09-08 15:00 -37.8pts adverse
- earliness (backtest): median -4.5 pts of move remaining at fire (n=3)

### H17 — 1 signal
*A climax reversal signal followed by absorption within five bars — effort meeting a quiet counter-party — marks a genuine exhaustion turn: the two-chapter story (exhaustion needs absorption to become reversal).*
Grading: directional. Latest review: rows (recommendation).

**S0-H17** — session × window grid (cells as in the matrix):

| session | backtest | forward |
|---|---|---|
| whole | ▲i+10.2pp (14/41) · p-6.6pp cap41.5 net+76/med+2.5 | ·i-0.6pp (58/281) · p-1.5pp cap22.7 net-18/med-0.5 |
| london | (°▲i+9.1pp (5/14) · p+3.7pp cap40.0 net+32/med+4.4) | ▲i+4.2pp (19/71) · p-2.2pp cap30.8 net+25/med+0.5 |
| overlap | (°▼i-16.7pp (0/1) · p-25.9pp cap— net+12/med+12.0) | (°▼i-2.2pp (2/16) · p-6.0pp cap31.5 net-51/med-3.5) |
| ny_only | (°▲i+18.0pp (6/15) · p+3.0pp cap53.0 net+34/med+2.5) | ▼i-2.5pp (12/75) · p-0.5pp cap29.2 net-24/med-1.2 |
| dead | (°▲i+29.3pp (3/5) · p-17.6pp cap— net-5/med-1.3) | ▲i+19.8pp (16/32) · p+7.1pp cap9.8 net-30/med-0.3 |
| asia | (°▼i-22.0pp (0/6) · p-16.2pp cap60.8 net+3/med-2.3) | ▼i-10.2pp (9/87) · p-0.1pp cap16.9 net+63/med-0.2 |

- backtest payoff: right +396 / wrong -320 / net +76 pts; median per fire +2.50 (n=41)
- backtest best call: 2026-07-30 12:44 +66.8pts remaining (episode 77.3pts, major)
- backtest worst false alarm: 2026-07-23 12:18 -71.0pts adverse
- forward payoff: right +1516 / wrong -1534 / net -18 pts; median per fire -0.50 (n=281)
- forward best call: 2026-10-23 05:50 +83.3pts remaining (episode 84.5pts, major)
- forward worst false alarm: 2026-11-03 14:29 -45.0pts adverse
- earliness (backtest): median 26.1 pts of move remaining at fire (n=12)

### H18 — 1 signal
*A gap-traversal signal followed by a same-direction effortless print within five bars — travel meeting no opposition — continues: the map says vacuum, the tape confirms no resistance.*
Grading: directional. Latest review: rows (recommendation).

**S0-H18** — session × window grid (cells as in the matrix):

| session | backtest | forward |
|---|---|---|
| whole | ▼i-4.2pp (12/61) · p+4.2pp cap34.0 net+169/med-1.0 | ▼i-8.2pp (21/161) · p+4.2pp cap24.2 net+160/med+1.5 |
| london | ▼i-14.6pp (3/25) · p+11.1pp cap45.5 net+266/med+1.3 | ▼i-6.6pp (13/81) · p-6.6pp cap27.2 net-160/med-0.5 |
| overlap | (°▲i+10.6pp (3/11) · p-7.7pp cap36.4 net-81/med-6.8) | ▼i-14.7pp (0/34) · p+13.4pp cap34.5 net+232/med+11.8 |
| ny_only | (°▲i+11.3pp (2/6) · p-10.3pp cap— net+11/med+0.1) | ▲i+6.5pp (5/20) · p+5.2pp cap19.2 net+9/med+2.6 |
| dead | (°▼i-30.7pp (0/1) · p+82.4pp cap19.2 net+18/med+17.6) | (°▲i+19.8pp (1/2) · p-17.9pp cap— net-18/med-9.2) |
| asia | (°·i+0.2pp (4/18) · p-5.1pp cap22.3 net-44/med-1.9) | ▼i-12.2pp (2/24) · p+23.7pp cap13.9 net+98/med+4.8 |

- backtest payoff: right +650 / wrong -482 / net +169 pts; median per fire -1.00 (n=61)
- backtest best call: 2026-07-27 03:05 +77.3pts remaining (episode 83.2pts, major)
- backtest worst false alarm: 2026-07-30 14:37 -50.0pts adverse
- forward payoff: right +1417 / wrong -1257 / net +160 pts; median per fire +1.50 (n=161)
- forward best call: 2026-10-08 09:52 +82.7pts remaining (episode 107.7pts, major)
- forward worst false alarm: 2026-11-05 14:35 -97.8pts adverse
- earliness (backtest): median 15.2 pts of move remaining at fire (n=10)

### H19 — 1 signal
*A probe-failure reversal signal followed by continued wide-loud effort in the anchor bar's own close direction within five bars is NOT the start of the claimed reversal — a SUPPRESSION/FADE configuration, and it says so.*
Grading: directional. Latest review: rows (recommendation).

- Question **Q1-H19**: see the register entry (status there is authoritative).
**S0-H19** — session × window grid (cells as in the matrix):

| session | backtest | forward |
|---|---|---|
| whole | ▼i-4.7pp (41/213) · p-2.6pp cap35.2 net-631/med-1.5 | ▼i-4.0pp (231/1345) · p-2.8pp cap22.5 net-1948/med-0.2 |
| london | ▼i-13.0pp (6/44) · p-13.5pp cap55.5 net-334/med-11.0 | ▼i-3.2pp (47/242) · p-5.3pp cap30.8 net-515/med-1.1 |
| overlap | (°▼i-16.7pp (0/4) · p+24.1pp cap37.6 net+8/med+5.3) | ▼i-2.2pp (10/80) · p-11.0pp cap39.8 net-516/med-7.7 |
| ny_only | ▼i-12.9pp (3/33) · p+35.2pp cap41.7 net+263/med+0.7 | ▼i-2.0pp (57/345) · p+2.7pp cap27.5 net-521/med-0.5 |
| dead | ·i+1.2pp (23/72) · p-3.7pp cap21.2 net-100/med-0.8 | ▼i-9.8pp (37/181) · p-1.9pp cap17.2 net-5/med+0.3 |
| asia | ▼i-7.0pp (9/60) · p-11.2pp cap27.3 net-469/med-2.0 | ▼i-4.4pp (80/497) · p-2.2pp cap17.5 net-391/med+0.1 |

- backtest payoff: right +1487 / wrong -2118 / net -631 pts; median per fire -1.50 (n=213)
- backtest best call: 2026-07-27 03:04 +78.6pts remaining (episode 83.2pts, major)
- backtest worst false alarm: 2026-07-30 06:58 -85.0pts adverse
- forward payoff: right +8150 / wrong -10098 / net -1948 pts; median per fire -0.20 (n=1345)
- forward best call: 2026-11-04 03:03 +367.5pts remaining (episode 364.5pts, major)
- forward worst false alarm: 2026-10-01 06:51 -101.0pts adverse
- earliness (backtest): median 25.8 pts of move remaining at fire (n=22)

### H20 — 1 signal
*A wide-bar close-through of a session extreme (the same conditioned wide-bar class the retest anchor fires on; resolution = the close beyond the level, not a rejection back inside) initiates continuation in the break direction.*
Grading: directional. Latest review: rows (recommendation).

**S0-H20** — session × window grid (cells as in the matrix):

| session | backtest | forward |
|---|---|---|
| whole | ▼i-9.7pp (2/50) · p-7.6pp cap62.0 [cls 37.6%/13.7%i] net-221/med-9.7 | ▼i-8.8pp (7/312) · p+8.0pp cap29.1 [cls 43.0%/11.0%i] net+851/med-1.2 |
| london | ▼i-12.5pp (0/28) · p+1.8pp cap75.5 [cls 37.5%/12.5%i] net+241/med-5.2 | ▼i-7.4pp (7/162) · p+5.2pp cap27.5 [cls 39.2%/11.7%i] net-541/med-6.2 |
| overlap | (°▼i-17.8pp (0/4) · p-30.8pp cap— [cls 30.8%/17.8%i] net-47/med-11.6) | ▼i-13.8pp (0/22) · p-0.9pp cap26.7 [cls 32.7%/13.8%i] net+19/med+2.6 |
| ny_only | (°▲i+10.6pp (1/4) · p-20.9pp cap— [cls 20.9%/14.4%i] net+29/med+7.3) | (°▼i-9.7pp (0/14) · p-5.6pp cap22.9 [cls 19.9%/9.7%i] net-47/med-3.6) |
| dead | (°▲i+23.7pp (1/3) · p-19.1pp cap— [cls 19.1%/9.6%i] net-41/med-14.3) | (°▼i-9.2pp (0/1) · p-20.4pp cap— [cls 20.4%/9.2%i] net+12/med+11.9) |
| asia | (°▼i-13.9pp (0/11) · p-8.2pp cap27.8 [cls 44.6%/13.9%i] net-404/med-29.8) | ▼i-9.4pp (0/113) · p+13.7pp cap36.4 [cls 55.3%/9.4%i] net+1407/med+5.0 |

- backtest payoff: right +648 / wrong -869 / net -221 pts; median per fire -9.65 (n=50)
- backtest best call: 2026-07-20 16:42 +48.5pts remaining (episode 41.7pts)
- backtest worst false alarm: 2026-07-24 06:50 -96.0pts adverse
- forward payoff: right +3890 / wrong -3039 / net +851 pts; median per fire -1.25 (n=312)
- forward best call: 2026-11-03 12:01 +78.2pts remaining (episode 95.7pts, major)
- forward worst false alarm: 2026-10-05 06:59 -71.2pts adverse
- earliness (backtest): median 31.9 pts of move remaining at fire (n=2)


---

# ger40 (ger40fut) — CANONICAL

Store span (1M, close ts): 2026-07-19 22:42:00+00:00 → 2026-11-06 20:59:00+00:00. Volume type: real futures volume (register 40 first-sync sanity; canonical verdict at this instrument's validation evening).

## Summary Matrix (page 1)

Engine `66be26997` — OBSERVATIONAL signal scoreboard - move-detection, not trading; no fills exist here by construction; never validation (docs/hypothesis_lifecycle.md stage 4)

**Review labels are RECOMMENDATIONS — none actioned, review pending operator familiarity.** Cells: marker + precision LIFT vs that context's OWN chance rate, (hits/fires), payoff net/median points (directional rows; either-direction rows have no payoff by construction). ▲/▼ = beyond ±2pp of chance, · = within. (°…) = small-n (fires<20 or episodes<10): dimmed, excluded from any future label arithmetic. Read READING_GUIDE.md first; full detail in hypothesis_performance.json.

| H | label | backtest whole | backtest london | forward whole | forward london |
|---|---|---|---|---|---|
| *context* | | 110 ep; chance 23.4%dir/45.2%either | 28 ep; chance 26.3%dir/51.1%either | 587 ep; chance 24.4%dir/45.1%either | 157 ep; chance 25.7%dir/49.0%either |
| S0-H1 | keep-watching | ▼i-2.6pp (9/49) · p+11.3pp cap89.9 net-83/med+0.7 | (°▼i-21.1pp (0/5) · p+33.7pp cap89.9 net+198/med+39.9) | ▲i+2.0pp (120/529) · p+1.5pp cap59.3 net-947/med-0.2 | ▲i+5.5pp (36/129) · p+0.7pp cap71.8 net-952/med-7.8 |
| S1-H1 | keep-watching | (°▼i-21.0pp (0/3) · p-23.4pp cap— net-72/med-34.2) | (°▼i-21.1pp (0/1) · p-26.3pp cap— net-54/med-53.5) | ▲i+6.1pp (11/41) · p+0.0pp cap73.6 net+547/med+4.6 | (°▼i-5.7pp (2/12) · p-9.0pp cap72.5 net-121/med-1.4) |
| S0-H2 | promote-candidate | ▼i-9.5pp (27/234) · p+2.7pp cap76.2 net-661/med-5.2 | (°▼i-7.8pp (2/15) · p-13.0pp cap86.6 net+93/med+9.8) | ▼i-2.1pp (408/2188) · p-0.9pp cap60.5 net-651/med-0.1 | ·i-1.1pp (83/389) · p-6.4pp cap88.3 net-68/med-1.1 |
| S1-H2 | promote-candidate | ▼i-9.1pp (21/176) · p+4.4pp cap76.2 net-760/med-8.3 | (°▼i-5.7pp (2/13) · p-10.9pp cap86.6 net+136/med+14.0) | ·i-0.4pp (321/1583) · p-1.1pp cap61.2 net-545/med-0.2 | ·i+1.3pp (66/278) · p-5.6pp cap87.8 net+140/med-1.5 |
| S0-H3 | keep-watching | (°▲i+4.0pp (2/8) · p-10.9pp cap70.3 net-28/med+2.0) | — | ·i-1.2pp (17/87) · p-2.6pp cap36.0 net-356/med-2.6 | (°▼i-22.4pp (0/7) · p-11.4pp cap186.0 net-63/med-4.0) |
| S0-H4 | keep-watching | ▼i-9.2pp (4/34) · p+9.0pp cap50.2 net+72/med+10.0 | (°▲i+8.9pp (3/10) · p-16.3pp cap50.2 net-30/med-3.7) | (°▼i-20.7pp (0/5) · p-24.4pp cap— net-708/med-223.1) | (°▼i-22.4pp (0/3) · p-25.7pp cap— net-708/med-227.8) |
| S0-H5 | keep-watching | — | — | (°▼i-20.7pp (0/2) · p+25.6pp cap29.7 net+44/med+22.1) | — |
| S0-H6 | keep-watching | ▼i-10.9pp (1/36) · p+7.2pp cap56.7 [cls 34.5%/13.7%i] net-192/med-10.4 | (°▼i-4.3pp (1/18) · p-7.5pp cap78.7 [cls 35.3%/9.9%i] net-56/med-10.3) | ▲i+4.7pp (78/459) · p-0.8pp cap65.2 [cls 42.2%/12.3%i] net-1478/med+0.1 | ·i+1.8pp (33/247) · p-2.0pp cap68.6 [cls 39.7%/11.6%i] net-2083/med-1.8 |
| S0-H7 | keep-watching | ▼i-2.4pp (11/59) · p+12.2pp cap97.8 net+761/med+4.2 | ▼i-11.1pp (2/20) · p+23.7pp cap86.9 net+719/med+33.0 | ·i+1.3pp (87/396) · p+2.1pp cap68.4 net-1744/med-0.3 | ▲i+4.6pp (44/163) · p+0.7pp cap88.2 net-1012/med-5.4 |
| S0-H7 (either-dir) | keep-watching | ▼i-7.3pp (19/59) · p+19.2pp cap50.2 | ▼i-10.5pp (6/20) · p+23.9pp cap57.4 | ▼i-7.7pp (123/396) · p+5.9pp cap29.6 | ▼i-8.3pp (54/163) · p+8.1pp cap32.5 |
| S0-H8 | keep-watching | ▼i-10.4pp (68/234) · p+8.2pp cap36.4 | (°▼i-20.5pp (3/15) · p-31.1pp cap68.2) | ·i-0.8pp (832/2188) · p-1.1pp cap29.6 | ·i+0.5pp (163/389) · p-8.9pp cap37.0 |
| S0-H9 | keep-watching | ▲i+2.1pp (12/52) · p-8.0pp cap55.5 net-426/med-4.1 | (°▼i-21.1pp (0/3) · p-26.3pp cap— net+17/med+22.6) | ·i+0.3pp (64/305) · p-3.1pp cap58.9 net+726/med-0.6 | ▼i-8.9pp (5/37) · p+14.8pp cap98.3 net+1204/med+31.2 |
| S1-H9 | keep-watching | (°▼i-21.0pp (0/8) · p+26.6pp cap101.1 net-53/med+13.1) | — | ▼i-15.2pp (6/109) · p+0.4pp cap63.6 net+632/med-1.5 | (°▼i-16.2pp (1/16) · p+11.8pp cap114.1 net+675/med+45.6) |
| S0-H10 | deprioritize | ▲i+5.5pp (39/147) · p-5.0pp cap49.6 net-391/med+3.2 | ▲i+2.0pp (9/39) · p-16.0pp cap80.6 net-463/med-12.5 | ·i-0.1pp (234/1137) · p-2.7pp cap45.8 net-640/med-1.1 | ▲i+3.2pp (54/211) · p-2.0pp cap71.2 net-1589/med-9.9 |
| S0-H11 | keep-watching | ▼i-2.1pp (14/74) · p-3.1pp cap68.3 net-452/med-6.0 | (°▼i-21.1pp (0/14) · p-4.9pp cap73.1 net-472/med-58.8) | ·i-1.7pp (361/1905) · p+3.5pp cap60.6 net-3303/med-2.1 | ·i+0.1pp (182/809) · p+1.6pp cap77.6 net+791/med+0.8 |
| S1-H11 | keep-watching | ·i+1.6pp (68/301) · p+7.2pp cap81.8 net+1221/med+5.2 | ▲i+9.3pp (34/112) · p-1.3pp cap84.4 net+267/med+1.2 | ▼i-4.9pp (291/1846) · p+3.8pp cap61.3 net+539/med+2.5 | ▼i-6.5pp (100/627) · p+4.6pp cap70.2 net+227/med+2.4 |
| S0-H12 | keep-watching | — | — | — | — |
| S0-H13 | keep-watching | (°▼i-4.3pp (1/6) · p+59.9pp cap74.2 net+397/med+58.7) | (°▼i-21.1pp (0/2) · p+73.7pp cap116.8 net+181/med+90.7) | ▼i-10.4pp (3/29) · p+6.6pp cap66.9 net-24/med+0.9 | (°▼i-14.7pp (1/13) · p-2.6pp cap98.3 net-77/med-9.9) |
| S0-H14 | keep-watching | ·i+1.1pp (25/113) · p+3.1pp cap53.9 net+312/med+0.5 | ▼i-2.6pp (5/27) · p-11.5pp cap80.6 net-256/med-4.2 | ▼i-2.9pp (214/1205) · p-2.5pp cap44.5 net-1822/med-0.7 | ▲i+4.2pp (64/241) · p-3.3pp cap70.7 net-3185/med-16.3 |
| S0-H15 | keep-watching | — | — | — | — |
| S0-H16 | keep-watching | (°▼i-21.0pp (0/10) · p-3.4pp cap126.3 net+8/med-16.3) | — | ▼i-9.0pp (7/60) · p-1.1pp cap73.5 net-16/med+10.6 | — |
| S0-H17 | rows | ·i+0.7pp (5/23) · p+7.0pp cap90.2 net+36/med+0.7 | (°▼i-21.1pp (0/3) · p+40.4pp cap96.2 net+198/med+78.9) | ▲i+2.9pp (67/284) · p+1.3pp cap54.0 net-6/med-0.2 | ▲i+6.2pp (22/77) · p-2.3pp cap76.8 net-533/med-4.8 |
| S0-H18 | rows | (°·i-1.0pp (3/15) · p-10.1pp cap102.0 net-232/med-14.3) | (°▼i-21.1pp (0/3) · p+7.0pp cap135.4 net-19/med-38.6) | ▼i-6.0pp (53/361) · p+5.2pp cap67.5 net-738/med-1.0 | ▼i-4.1pp (35/191) · p+1.5pp cap81.2 net-686/med-1.6 |
| S0-H19 | rows | ▼i-3.3pp (26/147) · p+5.9pp cap74.2 net+179/med+3.6 | (°·i+1.1pp (2/9) · p-26.3pp cap— net-51/med-14.3) | ·i+0.5pp (279/1319) · p-0.9pp cap65.8 net+581/med+0.2 | ▲i+7.5pp (60/201) · p-5.8pp cap77.1 net-822/med-3.7 |
| S0-H20 | rows | ▼i-13.7pp (0/35) · p+5.5pp cap57.3 [cls 34.5%/13.7%i] net-450/med-4.3 | (°▼i-9.9pp (0/19) · p+6.8pp cap61.4 [cls 35.3%/9.9%i] net+20/med+11.4) | ▼i-8.1pp (16/378) · p+0.1pp cap65.9 [cls 42.2%/12.3%i] net+1234/med+2.4 | ▼i-6.9pp (10/211) · p+0.6pp cap74.0 [cls 39.7%/11.6%i] net+1047/med+5.8 |
| **union coverage** | | 47.3% (52/110) | 35.7% (10/28) | 84.3% (495/587) | 87.9% (138/157) |

Not graded:  — see register entries.

## Hypothesis Cards (page 2)

### H1 — 2 signals
*A climactic bar — extreme volume on a wide spread late in an extended move — marks exhaustion, and price then reverses against the climax direction.*
Grading: directional. Latest review: keep-watching (recommendation).

- Question **Q1-H1**: see the register entry (status there is authoritative).
**S0-H1** — session × window grid (cells as in the matrix):

| session | backtest | forward |
|---|---|---|
| whole | ▼i-2.6pp (9/49) · p+11.3pp cap89.9 net-83/med+0.7 | ▲i+2.0pp (120/529) · p+1.5pp cap59.3 net-947/med-0.2 |
| london | (°▼i-21.1pp (0/5) · p+33.7pp cap89.9 net+198/med+39.9) | ▲i+5.5pp (36/129) · p+0.7pp cap71.8 net-952/med-7.8 |
| overlap | — | ·i-1.8pp (5/33) · p+12.5pp cap117.1 net+512/med+28.7 |
| ny_only | (°▼i-18.3pp (0/10) · p+18.5pp cap83.5 net-289/med-3.9) | ▼i-4.6pp (17/143) · p+10.2pp cap65.3 net+158/med+5.6 |
| dead | (°·i+1.9pp (2/7) · p+40.8pp cap89.2 net+93/med+34.1) | ▲i+12.1pp (27/70) · p+1.3pp cap44.8 net-69/med-0.4 |
| asia | ▲i+2.4pp (7/27) · p-5.3pp cap94.2 net-85/med-12.0 | ·i+1.6pp (35/154) · p-2.9pp cap41.4 net-596/med-0.2 |

- backtest payoff: right +1327 / wrong -1411 / net -83 pts; median per fire +0.70 (n=49)
- backtest best call: 2026-07-29 03:13 +188.0pts remaining (episode 269.7pts, major)
- backtest worst false alarm: 2026-07-29 19:11 -164.0pts adverse
- forward payoff: right +8880 / wrong -9827 / net -947 pts; median per fire -0.20 (n=527)
- forward best call: 2026-11-04 03:06 +705.5pts remaining (episode 687.7pts, major)
- forward worst false alarm: 2026-09-01 08:06 -208.4pts adverse
- earliness (backtest): median 98.4 pts of move remaining at fire (n=8)

**S1-H1** — session × window grid (cells as in the matrix):

| session | backtest | forward |
|---|---|---|
| whole | (°▼i-21.0pp (0/3) · p-23.4pp cap— net-72/med-34.2) | ▲i+6.1pp (11/41) · p+0.0pp cap73.6 net+547/med+4.6 |
| london | (°▼i-21.1pp (0/1) · p-26.3pp cap— net-54/med-53.5) | (°▼i-5.7pp (2/12) · p-9.0pp cap72.5 net-121/med-1.4) |
| overlap | — | (°▲i+83.0pp (1/1) · p-23.9pp cap— net+31/med+30.6) |
| ny_only | — | (°▲i+5.7pp (2/9) · p+1.0pp cap92.7 net+93/med+5.0) |
| dead | — | (°▲i+11.0pp (3/8) · p+21.7pp cap140.1 net+362/med+19.9) |
| asia | (°▼i-23.5pp (0/2) · p-31.2pp cap— net-19/med-9.3) | (°▲i+6.2pp (3/11) · p+1.0pp cap56.5 net+182/med+9.3) |

- backtest payoff: right +16 / wrong -88 / net -72 pts; median per fire -34.20 (n=3)
- backtest worst false alarm: 2026-07-28 10:36 -60.8pts adverse
- forward payoff: right +970 / wrong -423 / net +547 pts; median per fire +4.60 (n=40)
- forward best call: 2026-11-06 05:01 +286.4pts remaining (episode 283.9pts, major)
- forward worst false alarm: 2026-11-03 12:48 -157.6pts adverse

### H2 — 2 signals
*A failed probe beyond a prior extreme — an upthrust above or spring below that closes back inside — reverses against the probe.*
Grading: directional. Latest review: promote-candidate (recommendation).

**S0-H2** — session × window grid (cells as in the matrix):

| session | backtest | forward |
|---|---|---|
| whole | ▼i-9.5pp (27/234) · p+2.7pp cap76.2 net-661/med-5.2 | ▼i-2.1pp (408/2188) · p-0.9pp cap60.5 net-651/med-0.1 |
| london | (°▼i-7.8pp (2/15) · p-13.0pp cap86.6 net+93/med+9.8) | ·i-1.1pp (83/389) · p-6.4pp cap88.3 net-68/med-1.1 |
| overlap | (°▼i-11.1pp (0/11) · p-15.0pp cap122.7 net-195/med-38.7) | ·i+1.6pp (27/145) · p-3.2pp cap82.9 net-466/med-4.7 |
| ny_only | ▼i-6.8pp (7/61) · p+13.1pp cap77.0 net-1116/med-16.7 | ▼i-4.4pp (68/561) · p+6.3pp cap76.7 net+657/med+0.0 |
| dead | ▼i-11.3pp (8/52) · p+6.8pp cap90.8 net+604/med+2.2 | ▼i-3.3pp (68/293) · p+7.4pp cap41.6 net+274/med+0.5 |
| asia | ▼i-13.0pp (10/95) · p+1.4pp cap75.6 net-47/med-10.6 | ·i-0.9pp (162/800) · p-4.3pp cap45.7 net-1048/med+0.4 |

- backtest payoff: right +4896 / wrong -5557 / net -661 pts; median per fire -5.20 (n=234)
- backtest best call: 2026-07-27 03:23 +214.5pts remaining (episode 245.3pts, major)
- backtest worst false alarm: 2026-07-29 19:00 -192.8pts adverse
- forward payoff: right +36102 / wrong -36754 / net -651 pts; median per fire -0.10 (n=2186)
- forward best call: 2026-11-04 02:58 +678.0pts remaining (episode 687.7pts, major)
- forward worst false alarm: 2026-11-03 23:38 -210.1pts adverse
- earliness (backtest): median 97.8 pts of move remaining at fire (n=19)

**S1-H2** — session × window grid (cells as in the matrix):

| session | backtest | forward |
|---|---|---|
| whole | ▼i-9.1pp (21/176) · p+4.4pp cap76.2 net-760/med-8.3 | ·i-0.4pp (321/1583) · p-1.1pp cap61.2 net-545/med-0.2 |
| london | (°▼i-5.7pp (2/13) · p-10.9pp cap86.6 net+136/med+14.0) | ·i+1.3pp (66/278) · p-5.6pp cap87.8 net+140/med-1.5 |
| overlap | (°▼i-11.1pp (0/7) · p-9.8pp cap122.7 net-89/med-38.1) | ▲i+3.4pp (20/98) · p-4.5pp cap80.2 net-848/med-6.3 |
| ny_only | ▼i-7.2pp (5/45) · p+17.4pp cap77.0 net-1094/med-25.7 | ▼i-4.2pp (49/398) · p+5.7pp cap78.5 net+1046/med+0.5 |
| dead | ▼i-11.7pp (6/40) · p+11.2pp cap74.9 net+699/med+7.8 | ·i-0.5pp (56/215) · p+6.1pp cap39.9 net-170/med+0.1 |
| asia | ▼i-12.2pp (8/71) · p-0.2pp cap75.9 net-413/med-26.4 | ·i+0.8pp (130/594) · p-4.4pp cap45.7 net-712/med-0.1 |

- backtest payoff: right +3792 / wrong -4553 / net -760 pts; median per fire -8.35 (n=176)
- backtest best call: 2026-07-29 03:05 +193.7pts remaining (episode 269.7pts, major)
- backtest worst false alarm: 2026-07-29 19:00 -192.8pts adverse
- forward payoff: right +26235 / wrong -26780 / net -545 pts; median per fire -0.25 (n=1582)
- forward best call: 2026-11-04 03:16 +698.1pts remaining (episode 687.7pts, major)
- forward worst false alarm: 2026-11-03 23:38 -210.1pts adverse
- earliness (backtest): median 97.8 pts of move remaining at fire (n=17)

### H3 — 1 signal
*Repeated absorption — high effort with no result — at a price level precedes a breakout through that level.*
Grading: directional. Latest review: keep-watching (recommendation).

**S0-H3** — session × window grid (cells as in the matrix):

| session | backtest | forward |
|---|---|---|
| whole | (°▲i+4.0pp (2/8) · p-10.9pp cap70.3 net-28/med+2.0) | ·i-1.2pp (17/87) · p-2.6pp cap36.0 net-356/med-2.6 |
| london | — | (°▼i-22.4pp (0/7) · p-11.4pp cap186.0 net-63/med-4.0) |
| overlap | — | (°▼i-17.0pp (0/5) · p-3.9pp cap115.9 net-138/med-23.3) |
| ny_only | (°▲i+21.7pp (2/5) · p+8.5pp cap70.3 net+132/med+41.2) | (°▲i+3.5pp (3/15) · p-10.1pp cap— net-27/med-6.4) |
| dead | — | — |
| asia | (°▼i-23.5pp (0/3) · p-31.2pp cap— net-160/med-56.5) | ▲i+2.2pp (14/60) · p-7.1pp cap30.8 net-128/med-0.5 |

- backtest payoff: right +132 / wrong -160 / net -28 pts; median per fire +2.00 (n=8)
- backtest best call: 2026-07-27 18:10 +51.7pts remaining (episode 62.9pts)
- backtest worst false alarm: 2026-07-30 01:57 -65.7pts adverse
- forward payoff: right +952 / wrong -1308 / net -356 pts; median per fire -2.60 (n=87)
- forward best call: 2026-09-15 05:07 +225.3pts remaining (episode 279.3pts, major)
- forward worst false alarm: 2026-09-09 09:25 -136.1pts adverse
- earliness (backtest): median 51.7 pts of move remaining at fire (n=1)

### H4 — 1 signal
*In an established trend, a quiet (low-volume) pullback resolves with trend resumption.*
Grading: directional. Latest review: keep-watching (recommendation).

**S0-H4** — session × window grid (cells as in the matrix):

| session | backtest | forward |
|---|---|---|
| whole | ▼i-9.2pp (4/34) · p+9.0pp cap50.2 net+72/med+10.0 | (°▼i-20.7pp (0/5) · p-24.4pp cap— net-708/med-223.1) |
| london | (°▲i+8.9pp (3/10) · p-16.3pp cap50.2 net-30/med-3.7) | (°▼i-22.4pp (0/3) · p-25.7pp cap— net-708/med-227.8) |
| overlap | (°▼i-11.1pp (0/6) · p+9.2pp cap59.3 net-4/med-8.4) | — |
| ny_only | (°▼i-18.3pp (0/6) · p+21.8pp cap25.4 net-9/med+10.8) | (°▼i-16.5pp (0/2) · p-10.1pp cap— net+0/med+0.1) |
| dead | (°·i-1.7pp (1/4) · p+8.7pp cap34.8 net-14/med+32.4) | — |
| asia | (°▼i-23.5pp (0/8) · p+31.3pp cap61.0 net+129/med+17.4) | — |

- backtest payoff: right +556 / wrong -484 / net +72 pts; median per fire +10.00 (n=33)
- backtest best call: 2026-08-03 11:48 +80.2pts remaining (episode 142.0pts, major)
- backtest worst false alarm: 2026-07-26 23:29 -102.8pts adverse
- forward payoff: right +1 / wrong -708 / net -708 pts; median per fire -223.10 (n=5)
- forward worst false alarm: 2026-11-05 14:06 -257.2pts adverse
- earliness (backtest): median 75.7 pts of move remaining at fire (n=2)

### H5 — 1 signal
*A buying climax that extends far above its trend mean mean-reverts (climax-extension fade; registered short-side only).*
Grading: directional. Latest review: keep-watching (recommendation).

**S0-H5** — session × window grid (cells as in the matrix):

| session | backtest | forward |
|---|---|---|
| whole | — | (°▼i-20.7pp (0/2) · p+25.6pp cap29.7 net+44/med+22.1) |
| london | — | — |
| overlap | — | — |
| ny_only | — | (°▼i-16.5pp (0/1) · p-10.1pp cap— net+14/med+14.5) |
| dead | — | — |
| asia | — | (°▼i-21.1pp (0/1) · p+64.6pp cap29.7 net+30/med+29.7) |

- forward payoff: right +44 / wrong +0 / net +44 pts; median per fire +22.10 (n=2)
- forward worst false alarm: 2026-09-25 16:15 -6.6pts adverse

### H6 — 1 signal
*A wide-spread rejection bar at a session extreme (measured day-relative, volume-agnostic) reverses away from the extreme.*
Grading: directional. Latest review: keep-watching (recommendation).

- Question **Q1-H6**: see the register entry (status there is authoritative).
- Question **Q2-H6**: see the register entry (status there is authoritative).
- Question **Q3-H6**: see the register entry (status there is authoritative).
**S0-H6** — session × window grid (cells as in the matrix):

| session | backtest | forward |
|---|---|---|
| whole | ▼i-10.9pp (1/36) · p+7.2pp cap56.7 [cls 34.5%/13.7%i] net-192/med-10.4 | ▲i+4.7pp (78/459) · p-0.8pp cap65.2 [cls 42.2%/12.3%i] net-1478/med+0.1 |
| london | (°▼i-4.3pp (1/18) · p-7.5pp cap78.7 [cls 35.3%/9.9%i] net-56/med-10.3) | ·i+1.8pp (33/247) · p-2.0pp cap68.6 [cls 39.7%/11.6%i] net-2083/med-1.8 |
| overlap | (°▼i-11.3pp (0/1) · p+71.3pp cap122.7 [cls 28.7%/11.3%i] net+108/med+108.3) | ▲i+4.1pp (8/37) · p+10.0pp cap83.0 [cls 27.8%/17.5%i] net+298/med-5.5 |
| ny_only | — | ▼i-4.4pp (1/26) · p+11.6pp cap70.3 [cls 23.0%/8.2%i] net+298/med+10.8 |
| dead | (°▼i-7.5pp (0/3) · p-22.5pp cap— [cls 22.5%/7.5%i] net+29/med+13.4) | (°▼i-10.2pp (0/4) · p+51.9pp cap142.7 [cls 23.1%/10.2%i] net+299/med+58.5) |
| asia | (°▼i-20.6pp (0/14) · p+27.7pp cap40.0 [cls 36.6%/20.6%i] net-274/med-21.8) | ▲i+12.1pp (36/145) · p-2.8pp cap46.3 [cls 51.8%/12.7%i] net-290/med+0.1 |

- backtest payoff: right +682 / wrong -874 / net -192 pts; median per fire -10.40 (n=36)
- backtest best call: 2026-07-28 12:35 +146.2pts remaining (episode 195.2pts, major)
- backtest worst false alarm: 2026-08-03 07:10 -108.0pts adverse
- forward payoff: right +9596 / wrong -11074 / net -1478 pts; median per fire +0.10 (n=459)
- forward best call: 2026-09-22 12:37 +187.7pts remaining (episode 193.7pts, major)
- forward worst false alarm: 2026-10-01 06:35 -211.6pts adverse
- earliness (backtest): median 146.2 pts of move remaining at fire (n=1)

### H7 — 1 signal
*Quiet decline at a session extreme is disguised accumulation: effortless (low-volume) weakness reverses UP once selling fails to attract participation (mirror: quiet advance at a high reverses down).*
Grading: directional + either-direction (dual). Latest review: keep-watching (recommendation).

- Question **Q1-H7**: see the register entry (status there is authoritative).
**S0-H7** — session × window grid (cells as in the matrix):

| session | backtest | forward |
|---|---|---|
| whole | ▼i-2.4pp (11/59) · p+12.2pp cap97.8 net+761/med+4.2 | ·i+1.3pp (87/396) · p+2.1pp cap68.4 net-1744/med-0.3 |
| london | ▼i-11.1pp (2/20) · p+23.7pp cap86.9 net+719/med+33.0 | ▲i+4.6pp (44/163) · p+0.7pp cap88.2 net-1012/med-5.4 |
| overlap | (°▼i-11.1pp (0/15) · p+22.6pp cap91.3 net+56/med-29.0) | ·i+1.0pp (11/61) · p-5.9pp cap76.3 net+80/med+3.2 |
| ny_only | (°·i-1.6pp (1/6) · p+5.2pp cap101.1 net+59/med+7.7) | ▼i-2.2pp (8/56) · p+0.6pp cap60.0 net-24/med+0.5 |
| dead | (°▲i+23.3pp (2/4) · p+8.7pp cap128.8 net-15/med-28.8) | (°▲i+2.1pp (4/14) · p-1.5pp cap42.9 net-29/med-6.4) |
| asia | (°▲i+19.4pp (6/14) · p-16.9pp cap99.9 net-58/med-10.2) | ·i-1.5pp (20/102) · p+6.8pp cap39.8 net-759/med+0.0 |

- backtest payoff: right +1756 / wrong -995 / net +761 pts; median per fire +4.20 (n=59)
- backtest best call: 2026-07-27 03:04 +247.0pts remaining (episode 245.3pts, major)
- backtest worst false alarm: 2026-07-27 13:57 -91.8pts adverse
- forward payoff: right +7315 / wrong -9059 / net -1744 pts; median per fire -0.35 (n=396)
- forward best call: 2026-11-04 11:40 +358.8pts remaining (episode 389.1pts, major)
- forward worst false alarm: 2026-11-06 10:00 -242.5pts adverse
- earliness (backtest): median 84.0 pts of move remaining at fire (n=10)

**S0-H7 (either-dir)** — session × window grid (cells as in the matrix):

| session | backtest | forward |
|---|---|---|
| whole | ▼i-7.3pp (19/59) · p+19.2pp cap50.2 | ▼i-7.7pp (123/396) · p+5.9pp cap29.6 |
| london | ▼i-10.5pp (6/20) · p+23.9pp cap57.4 | ▼i-8.3pp (54/163) · p+8.1pp cap32.5 |
| overlap | (°▼i-22.0pp (0/15) · p+32.7pp cap65.0) | ▼i-5.8pp (17/61) · p-12.9pp cap64.6 |
| ny_only | (°·i-0.9pp (2/6) · p+10.6pp cap52.5) | ▼i-4.8pp (15/56) · p-2.1pp cap50.2 |
| dead | (°·i+1.0pp (2/4) · p+43.3pp cap-2.7) | (°▼i-12.5pp (5/14) · p+5.9pp cap8.3) |
| asia | (°▲i+20.9pp (9/14) · p-16.3pp cap7.9) | ▼i-8.1pp (32/102) · p+9.4pp cap25.8 |

- backtest payoff: n/a by construction (either-direction)
- backtest best call: 2026-07-27 03:04 +247.0pts remaining (episode 245.3pts, major)
- backtest worst false alarm: 2026-07-29 11:19 -63.7pts adverse
- forward payoff: n/a by construction (either-direction)
- forward best call: 2026-11-04 11:40 +358.8pts remaining (episode 389.1pts, major)
- forward worst false alarm: 2026-11-06 14:46 -86.2pts adverse
- earliness (backtest): median 76.6 pts of move remaining at fire (n=16)

### H8 — 1 signal
*Reversal-signature bar anatomy (upthrust/spring) predicts imminent range expansion irrespective of direction.*
Grading: either-direction. Latest review: keep-watching (recommendation).

**S0-H8** — session × window grid (cells as in the matrix):

| session | backtest | forward |
|---|---|---|
| whole | ▼i-10.4pp (68/234) · p+8.2pp cap36.4 | ·i-0.8pp (832/2188) · p-1.1pp cap29.6 |
| london | (°▼i-20.5pp (3/15) · p-31.1pp cap68.2) | ·i+0.5pp (163/389) · p-8.9pp cap37.0 |
| overlap | (°▼i-12.9pp (1/11) · p+16.3pp cap37.2) | ▲i+4.9pp (56/145) · p+3.0pp cap30.4 |
| ny_only | ▼i-6.3pp (17/61) · p+33.0pp cap32.1 | ▼i-5.4pp (147/561) · p+9.8pp cap44.9 |
| dead | ▼i-16.3pp (17/52) · p+1.0pp cap53.2 | ▼i-2.1pp (135/293) · p+7.7pp cap30.7 |
| asia | ▼i-11.8pp (30/95) · p+8.2pp cap29.9 | ·i+1.9pp (331/800) · p-5.1pp cap25.6 |

- backtest payoff: n/a by construction (either-direction)
- backtest best call: 2026-07-27 03:23 +214.5pts remaining (episode 245.3pts, major)
- backtest worst false alarm: 2026-07-27 16:40 -76.3pts adverse
- forward payoff: n/a by construction (either-direction)
- forward best call: 2026-11-04 02:58 +678.0pts remaining (episode 687.7pts, major)
- forward worst false alarm: 2026-11-05 17:08 -116.3pts adverse
- earliness (backtest): median 80.1 pts of move remaining at fire (n=27)

### H9 — 2 signals
*Persistent lower-TF directional pressure that recruits expanding participation at the parent timeframe precedes continuation beyond what the parent label alone predicts; pressure without participation expansion does not.*
Grading: directional. Latest review: keep-watching (recommendation).

- Question **Q2-H9**: see the register entry (status there is authoritative).
**S0-H9** — session × window grid (cells as in the matrix):

| session | backtest | forward |
|---|---|---|
| whole | ▲i+2.1pp (12/52) · p-8.0pp cap55.5 net-426/med-4.1 | ·i+0.3pp (64/305) · p-3.1pp cap58.9 net+726/med-0.6 |
| london | (°▼i-21.1pp (0/3) · p-26.3pp cap— net+17/med+22.6) | ▼i-8.9pp (5/37) · p+14.8pp cap98.3 net+1204/med+31.2 |
| overlap | (°▼i-11.1pp (0/2) · p-24.1pp cap— net+112/med+55.8) | ▲i+10.6pp (8/29) · p-6.7pp cap86.0 net-54/med+3.2 |
| ny_only | ▲i+9.0pp (6/22) · p-7.0pp cap32.0 net-517/med-19.3 | ▲i+11.7pp (35/124) · p+2.0pp cap45.6 net-535/med-5.7 |
| dead | (°·i-1.7pp (3/12) · p+17.0pp cap101.1 net+200/med+3.0) | ▼i-15.7pp (4/37) · p-5.0pp cap47.1 net+222/med-0.7 |
| asia | (°·i-0.4pp (3/13) · p-8.1pp cap49.0 net-238/med-8.5) | ▼i-5.7pp (12/78) · p-2.1pp cap43.6 net-111/med-0.2 |

- backtest payoff: right +725 / wrong -1151 / net -426 pts; median per fire -4.10 (n=51)
- backtest best call: 2026-07-31 05:00 +184.4pts remaining (episode 184.2pts, major)
- backtest worst false alarm: 2026-07-29 18:45 -160.1pts adverse
- forward payoff: right +4297 / wrong -3571 / net +726 pts; median per fire -0.55 (n=298)
- forward best call: 2026-10-16 13:30 +269.0pts remaining (episode 267.7pts, major)
- forward worst false alarm: 2026-10-21 18:30 -127.3pts adverse
- earliness (backtest): median 56.3 pts of move remaining at fire (n=6)

**S1-H9** — session × window grid (cells as in the matrix):

| session | backtest | forward |
|---|---|---|
| whole | (°▼i-21.0pp (0/8) · p+26.6pp cap101.1 net-53/med+13.1) | ▼i-15.2pp (6/109) · p+0.4pp cap63.6 net+632/med-1.5 |
| london | — | (°▼i-16.2pp (1/16) · p+11.8pp cap114.1 net+675/med+45.6) |
| overlap | (°▼i-11.1pp (0/1) · p-24.1pp cap— net+56/med+55.8) | (°▼i-17.0pp (0/4) · p+1.1pp cap90.9 net-130/med-45.9) |
| ny_only | (°▼i-18.3pp (0/2) · p-11.5pp cap— net-320/med-160.1) | ▼i-10.3pp (2/32) · p+18.0pp cap63.6 net+36/med-5.9 |
| dead | (°▼i-26.7pp (0/5) · p+63.7pp cap101.1 net+211/med+19.4) | ▼i-16.5pp (2/20) · p+4.2pp cap47.1 net+228/med+14.3 |
| asia | — | ▼i-18.4pp (1/37) · p-16.5pp cap59.5 net-178/med-13.8 |

- backtest payoff: right +294 / wrong -348 / net -53 pts; median per fire +13.05 (n=8)
- backtest worst false alarm: 2026-07-29 18:45 -160.1pts adverse
- forward payoff: right +2182 / wrong -1551 / net +632 pts; median per fire -1.50 (n=105)
- forward best call: 2026-09-18 10:00 +243.2pts remaining (episode 264.3pts, major)
- forward worst false alarm: 2026-08-18 07:00 -118.4pts adverse

### H10 — 1 signal
*In an established 1-minute trend, no-demand/no-supply prints in the trend's direction signal continuation.*
Grading: directional. Latest review: deprioritize (recommendation).

**S0-H10** — session × window grid (cells as in the matrix):

| session | backtest | forward |
|---|---|---|
| whole | ▲i+5.5pp (39/147) · p-5.0pp cap49.6 net-391/med+3.2 | ·i-0.1pp (234/1137) · p-2.7pp cap45.8 net-640/med-1.1 |
| london | ▲i+2.0pp (9/39) · p-16.0pp cap80.6 net-463/med-12.5 | ▲i+3.2pp (54/211) · p-2.0pp cap71.2 net-1589/med-9.9 |
| overlap | (°▼i-11.1pp (0/9) · p-13.0pp cap60.8 net-114/med-21.0) | ▲i+4.0pp (17/81) · p-5.4pp cap62.7 net-91/med-3.8 |
| ny_only | ·i-0.7pp (6/34) · p+9.1pp cap46.0 net+237/med+4.4 | ·i-1.0pp (42/271) · p+1.0pp cap39.2 net+343/med-0.5 |
| dead | (°·i+1.9pp (4/14) · p-16.3pp cap— net-275/med-13.8) | ▼i-8.9pp (25/142) · p-3.8pp cap23.9 net-329/med-1.6 |
| asia | ▲i+15.7pp (20/51) · p-1.8pp cap51.4 net+224/med+6.3 | ·i+1.1pp (96/432) · p-4.2pp cap34.3 net+1026/med+0.8 |

- backtest payoff: right +1730 / wrong -2121 / net -391 pts; median per fire +3.20 (n=147)
- backtest best call: 2026-07-27 03:28 +219.3pts remaining (episode 245.3pts, major)
- backtest worst false alarm: 2026-08-03 06:31 -111.9pts adverse
- forward payoff: right +13047 / wrong -13687 / net -640 pts; median per fire -1.05 (n=1136)
- forward best call: 2026-09-09 03:21 +340.6pts remaining (episode 349.6pts, major)
- forward worst false alarm: 2026-11-05 14:00 -261.9pts adverse
- earliness (backtest): median 81.0 pts of move remaining at fire (n=11)

### H11 — 2 signals
*Price entering a low-volume price zone traverses it faster than baseline; entering a high-volume node it stalls or reverses at above-baseline rates.*
Grading: directional. Latest review: keep-watching (recommendation).

- Question **Q1-H11**: see the register entry (status there is authoritative).
- Question **Q2-H11**: see the register entry (status there is authoritative).
**S0-H11** — session × window grid (cells as in the matrix):

| session | backtest | forward |
|---|---|---|
| whole | ▼i-2.1pp (14/74) · p-3.1pp cap68.3 net-452/med-6.0 | ·i-1.7pp (361/1905) · p+3.5pp cap60.6 net-3303/med-2.1 |
| london | (°▼i-21.1pp (0/14) · p-4.9pp cap73.1 net-472/med-58.8) | ·i+0.1pp (182/809) · p+1.6pp cap77.6 net+791/med+0.8 |
| overlap | (°▼i-11.1pp (0/16) · p-11.6pp cap66.2 net-166/med-13.2) | ▼i-6.2pp (20/186) · p+3.0pp cap72.0 net-220/med-1.4 |
| ny_only | (°▼i-18.3pp (0/4) · p-11.5pp cap— net-18/med-18.5) | ·i-1.4pp (33/219) · p-5.1pp cap49.5 net-1821/med-9.6 |
| dead | (°▲i+16.2pp (3/7) · p-2.0pp cap52.6 net+1/med+4.1) | ▼i-7.0pp (23/118) · p-0.5pp cap38.9 net-510/med-2.9 |
| asia | ▲i+9.8pp (11/33) · p-3.9pp cap70.3 net+203/med-1.1 | ▼i-3.1pp (103/573) · p+4.9pp cap37.1 net-1544/med-0.8 |

- backtest payoff: right +1359 / wrong -1811 / net -452 pts; median per fire -5.95 (n=74)
- backtest best call: 2026-07-31 04:52 +178.0pts remaining (episode 184.2pts, major)
- backtest worst false alarm: 2026-07-31 07:03 -171.6pts adverse
- forward payoff: right +34762 / wrong -38065 / net -3303 pts; median per fire -2.10 (n=1903)
- forward best call: 2026-11-05 12:42 +359.5pts remaining (episode 440.8pts, major)
- forward worst false alarm: 2026-11-05 14:33 -263.1pts adverse
- earliness (backtest): median 73.8 pts of move remaining at fire (n=7)

**S1-H11** — session × window grid (cells as in the matrix):

| session | backtest | forward |
|---|---|---|
| whole | ·i+1.6pp (68/301) · p+7.2pp cap81.8 net+1221/med+5.2 | ▼i-4.9pp (291/1846) · p+3.8pp cap61.3 net+539/med+2.5 |
| london | ▲i+9.3pp (34/112) · p-1.3pp cap84.4 net+267/med+1.2 | ▼i-6.5pp (100/627) · p+4.6pp cap70.2 net+227/med+2.4 |
| overlap | (°·i-1.1pp (2/20) · p-9.1pp cap79.2 net+3/med+13.2) | ▼i-2.0pp (35/233) · p-1.2pp cap83.2 net+369/med+5.4 |
| ny_only | ▼i-9.8pp (4/47) · p+9.8pp cap83.3 net+89/med+1.0 | ·i-0.5pp (52/324) · p+1.9pp cap70.0 net+716/med+3.9 |
| dead | ▲i+17.4pp (15/34) · p+7.2pp cap86.7 net+169/med+5.3 | ▼i-7.7pp (21/112) · p+7.4pp cap41.7 net+204/med+3.6 |
| asia | ▼i-8.7pp (13/88) · p+17.7pp cap76.2 net+693/med+16.2 | ▼i-6.0pp (83/550) · p+3.1pp cap41.5 net-977/med+0.7 |

- backtest payoff: right +7407 / wrong -6186 / net +1221 pts; median per fire +5.20 (n=301)
- backtest best call: 2026-07-30 00:35 +150.2pts remaining (episode 237.6pts, major)
- backtest worst false alarm: 2026-07-29 19:32 -168.0pts adverse
- forward payoff: right +33593 / wrong -33054 / net +539 pts; median per fire +2.45 (n=1846)
- forward best call: 2026-09-09 02:52 +350.2pts remaining (episode 349.6pts, major)
- forward worst false alarm: 2026-11-06 09:45 -249.9pts adverse
- earliness (backtest): median 58.0 pts of move remaining at fire (n=23)

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
| whole | (°▼i-4.3pp (1/6) · p+59.9pp cap74.2 net+397/med+58.7) | ▼i-10.4pp (3/29) · p+6.6pp cap66.9 net-24/med+0.9 |
| london | (°▼i-21.1pp (0/2) · p+73.7pp cap116.8 net+181/med+90.7) | (°▼i-14.7pp (1/13) · p-2.6pp cap98.3 net-77/med-9.9) |
| overlap | — | (°▼i-17.0pp (0/5) · p+16.1pp cap61.1 net+46/med-5.4) |
| ny_only | — | (°▲i+3.5pp (1/5) · p-10.1pp cap— net+62/med+13.2) |
| dead | (°▼i-26.7pp (0/1) · p+83.7pp cap74.2 net+51/med+51.0) | (°▼i-26.5pp (0/1) · p+84.2pp cap29.2 net+29/med+29.2) |
| asia | (°▲i+9.8pp (1/3) · p+35.5pp cap78.8 net+164/med+56.1) | (°·i-1.1pp (1/5) · p+24.6pp cap43.6 net-85/med+23.6) |

- backtest payoff: right +397 / wrong +0 / net +397 pts; median per fire +58.70 (n=6)
- backtest best call: 2026-07-28 02:15 +115.9pts remaining (episode 109.7pts, major)
- backtest worst false alarm: 2026-07-28 02:15 -2.8pts adverse
- forward payoff: right +410 / wrong -435 / net -24 pts; median per fire +0.90 (n=29)
- forward best call: 2026-08-21 09:44 +113.7pts remaining (episode 144.6pts, major)
- forward worst false alarm: 2026-10-08 06:01 -107.8pts adverse
- earliness (backtest): median 115.9 pts of move remaining at fire (n=1)

### H14 — 1 signal
*Counter-trend No Demand / No Supply prints in an established trend mark absorption and precede trend continuation.*
Grading: directional. Latest review: keep-watching (recommendation).

**S0-H14** — session × window grid (cells as in the matrix):

| session | backtest | forward |
|---|---|---|
| whole | ·i+1.1pp (25/113) · p+3.1pp cap53.9 net+312/med+0.5 | ▼i-2.9pp (214/1205) · p-2.5pp cap44.5 net-1822/med-0.7 |
| london | ▼i-2.6pp (5/27) · p-11.5pp cap80.6 net-256/med-4.2 | ▲i+4.2pp (64/241) · p-3.3pp cap70.7 net-3185/med-16.3 |
| overlap | (°▼i-11.1pp (0/11) · p-24.1pp cap— net-138/med-20.3) | ▲i+6.2pp (16/69) · p-6.5pp cap63.7 net+32/med-0.4 |
| ny_only | ▼i-9.6pp (2/23) · p+27.6pp cap43.2 net+392/med+21.1 | ▼i-3.7pp (35/273) · p-2.0pp cap49.1 net+506/med-0.1 |
| dead | (°▲i+40.0pp (6/9) · p-16.3pp cap— net-178/med-20.1) | ▼i-16.3pp (19/187) · p-5.1pp cap24.7 net-602/med-0.8 |
| asia | ▲i+4.4pp (12/43) · p+8.3pp cap59.4 net+492/med+8.2 | ▼i-2.7pp (80/435) · p+0.5pp cap30.8 net+1427/med+1.8 |

- backtest payoff: right +1733 / wrong -1421 / net +312 pts; median per fire +0.50 (n=113)
- backtest best call: 2026-07-31 04:56 +164.7pts remaining (episode 169.2pts, major)
- backtest worst false alarm: 2026-08-03 06:28 -123.0pts adverse
- forward payoff: right +13461 / wrong -15282 / net -1822 pts; median per fire -0.70 (n=1204)
- forward best call: 2026-09-09 03:26 +341.3pts remaining (episode 349.6pts, major)
- forward worst false alarm: 2026-11-05 14:05 -258.3pts adverse
- earliness (backtest): median 76.1 pts of move remaining at fire (n=8)

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
| whole | (°▼i-21.0pp (0/10) · p-3.4pp cap126.3 net+8/med-16.3) | ▼i-9.0pp (7/60) · p-1.1pp cap73.5 net-16/med+10.6 |
| london | — | — |
| overlap | (°▼i-11.1pp (0/10) · p-4.1pp cap126.3 net+8/med-16.3) | ▼i-5.3pp (7/60) · p-0.6pp cap73.5 net-16/med+10.6 |
| ny_only | — | — |
| dead | — | — |
| asia | — | — |

- backtest payoff: right +262 / wrong -254 / net +8 pts; median per fire -16.30 (n=10)
- backtest worst false alarm: 2026-07-27 15:00 -114.5pts adverse
- forward payoff: right +1204 / wrong -1220 / net -16 pts; median per fire +10.55 (n=60)
- forward best call: 2026-09-28 15:00 +184.1pts remaining (episode 221.4pts, major)
- forward worst false alarm: 2026-09-14 15:00 -160.8pts adverse

### H17 — 1 signal
*A climax reversal signal followed by absorption within five bars — effort meeting a quiet counter-party — marks a genuine exhaustion turn: the two-chapter story (exhaustion needs absorption to become reversal).*
Grading: directional. Latest review: rows (recommendation).

**S0-H17** — session × window grid (cells as in the matrix):

| session | backtest | forward |
|---|---|---|
| whole | ·i+0.7pp (5/23) · p+7.0pp cap90.2 net+36/med+0.7 | ▲i+2.9pp (67/284) · p+1.3pp cap54.0 net-6/med-0.2 |
| london | (°▼i-21.1pp (0/3) · p+40.4pp cap96.2 net+198/med+78.9) | ▲i+6.2pp (22/77) · p-2.3pp cap76.8 net-533/med-4.8 |
| overlap | — | (°▼i-5.2pp (2/17) · p+17.3pp cap83.8 net+92/med+7.2) |
| ny_only | (°▼i-18.3pp (0/2) · p-11.5pp cap— net-67/med-33.6) | ▼i-5.2pp (7/62) · p+2.8pp cap55.8 net+336/med+4.2 |
| dead | (°▲i+13.3pp (2/5) · p+23.7pp cap109.2 net-58/med+0.7) | ▲i+19.0pp (15/33) · p-0.6pp cap41.4 net-164/med-3.7 |
| asia | (°·i-0.4pp (3/13) · p-8.1pp cap75.2 net-37/med-9.0) | ·i+1.0pp (21/95) · p+1.4pp cap37.0 net+262/med-1.2 |

- backtest payoff: right +670 / wrong -634 / net +36 pts; median per fire +0.70 (n=23)
- backtest best call: 2026-07-28 23:06 +114.4pts remaining (episode 208.8pts, major)
- backtest worst false alarm: 2026-07-28 23:06 -138.5pts adverse
- forward payoff: right +4234 / wrong -4240 / net -6 pts; median per fire -0.25 (n=284)
- forward best call: 2026-11-04 03:09 +715.5pts remaining (episode 687.7pts, major)
- forward worst false alarm: 2026-11-05 14:48 -170.7pts adverse
- earliness (backtest): median 105.3 pts of move remaining at fire (n=4)

### H18 — 1 signal
*A gap-traversal signal followed by a same-direction effortless print within five bars — travel meeting no opposition — continues: the map says vacuum, the tape confirms no resistance.*
Grading: directional. Latest review: rows (recommendation).

**S0-H18** — session × window grid (cells as in the matrix):

| session | backtest | forward |
|---|---|---|
| whole | (°·i-1.0pp (3/15) · p-10.1pp cap102.0 net-232/med-14.3) | ▼i-6.0pp (53/361) · p+5.2pp cap67.5 net-738/med-1.0 |
| london | (°▼i-21.1pp (0/3) · p+7.0pp cap135.4 net-19/med-38.6) | ▼i-4.1pp (35/191) · p+1.5pp cap81.2 net-686/med-1.6 |
| overlap | (°▼i-11.1pp (0/6) · p-24.1pp cap— net-52/med-6.5) | ▼i-7.2pp (4/41) · p+10.2pp cap92.0 net+662/med+8.0 |
| ny_only | — | ▼i-8.2pp (2/24) · p-1.8pp cap109.7 net-0/med-3.8 |
| dead | (°▲i+73.3pp (1/1) · p-16.3pp cap— net-14/med-14.3) | (°▲i+6.8pp (3/9) · p+6.4pp cap32.1 net-199/med-3.0) |
| asia | (°▲i+16.5pp (2/5) · p-11.2pp cap68.5 net-146/med-6.4) | ▼i-11.7pp (9/96) · p+3.1pp cap41.7 net-514/med+0.7 |

- backtest payoff: right +233 / wrong -464 / net -232 pts; median per fire -14.30 (n=15)
- backtest best call: 2026-08-03 05:12 +128.8pts remaining (episode 142.4pts, major)
- backtest worst false alarm: 2026-07-31 06:36 -175.9pts adverse
- forward payoff: right +7098 / wrong -7836 / net -738 pts; median per fire -1.00 (n=361)
- forward best call: 2026-11-05 13:20 +386.0pts remaining (episode 440.8pts, major)
- forward worst false alarm: 2026-11-05 14:34 -290.1pts adverse
- earliness (backtest): median 70.1 pts of move remaining at fire (n=2)

### H19 — 1 signal
*A probe-failure reversal signal followed by continued wide-loud effort in the anchor bar's own close direction within five bars is NOT the start of the claimed reversal — a SUPPRESSION/FADE configuration, and it says so.*
Grading: directional. Latest review: rows (recommendation).

- Question **Q1-H19**: see the register entry (status there is authoritative).
**S0-H19** — session × window grid (cells as in the matrix):

| session | backtest | forward |
|---|---|---|
| whole | ▼i-3.3pp (26/147) · p+5.9pp cap74.2 net+179/med+3.6 | ·i+0.5pp (279/1319) · p-0.9pp cap65.8 net+581/med+0.2 |
| london | (°·i+1.1pp (2/9) · p-26.3pp cap— net-51/med-14.3) | ▲i+7.5pp (60/201) · p-5.8pp cap77.1 net-822/med-3.7 |
| overlap | (°▲i+3.2pp (1/7) · p+47.3pp cap75.9 net+81/med+40.1) | ▲i+8.9pp (22/85) · p+7.9pp cap100.2 net+474/med+4.8 |
| ny_only | ▼i-11.2pp (3/42) · p+31.4pp cap80.8 net+903/med+21.6 | ▼i-4.6pp (46/386) · p+7.5pp cap81.1 net+60/med-0.8 |
| dead | ▼i-4.0pp (10/44) · p-4.9pp cap58.4 net-463/med-4.3 | ·i-1.0pp (42/165) · p+1.2pp cap37.8 net+71/med+0.8 |
| asia | ·i-1.3pp (10/45) · p+2.1pp cap64.2 net-291/med+10.6 | ·i+1.5pp (109/482) · p-4.9pp cap53.3 net+798/med+0.8 |

- backtest payoff: right +3647 / wrong -3468 / net +179 pts; median per fire +3.60 (n=147)
- backtest best call: 2026-07-30 00:50 +147.0pts remaining (episode 237.6pts, major)
- backtest worst false alarm: 2026-07-29 18:59 -189.5pts adverse
- forward payoff: right +23907 / wrong -23326 / net +581 pts; median per fire +0.20 (n=1319)
- forward best call: 2026-11-04 03:06 +705.5pts remaining (episode 687.7pts, major)
- forward worst false alarm: 2026-11-06 09:33 -259.2pts adverse
- earliness (backtest): median 88.8 pts of move remaining at fire (n=14)

### H20 — 1 signal
*A wide-bar close-through of a session extreme (the same conditioned wide-bar class the retest anchor fires on; resolution = the close beyond the level, not a rejection back inside) initiates continuation in the break direction.*
Grading: directional. Latest review: rows (recommendation).

**S0-H20** — session × window grid (cells as in the matrix):

| session | backtest | forward |
|---|---|---|
| whole | ▼i-13.7pp (0/35) · p+5.5pp cap57.3 [cls 34.5%/13.7%i] net-450/med-4.3 | ▼i-8.1pp (16/378) · p+0.1pp cap65.9 [cls 42.2%/12.3%i] net+1234/med+2.4 |
| london | (°▼i-9.9pp (0/19) · p+6.8pp cap61.4 [cls 35.3%/9.9%i] net+20/med+11.4) | ▼i-6.9pp (10/211) · p+0.6pp cap74.0 [cls 39.7%/11.6%i] net+1047/med+5.8 |
| overlap | (°▼i-11.3pp (0/3) · p-28.7pp cap— [cls 28.7%/11.3%i] net-186/med-32.7) | ▼i-14.6pp (1/35) · p-10.7pp cap58.7 [cls 27.8%/17.5%i] net-648/med-7.6 |
| ny_only | — | ·i+0.9pp (2/22) · p-18.5pp cap68.5 [cls 23.0%/8.2%i] net-296/med-11.5 |
| dead | (°▼i-7.5pp (0/3) · p+10.8pp cap44.1 [cls 22.5%/7.5%i] net-286/med-97.1) | (°▲i+4.1pp (1/7) · p+19.8pp cap70.3 [cls 23.1%/10.2%i] net-226/med-6.5) |
| asia | (°▼i-20.6pp (0/10) · p+13.4pp cap57.7 [cls 36.6%/20.6%i] net+2/med+8.8) | ▼i-10.8pp (2/103) · p+11.3pp cap54.2 [cls 51.8%/12.7%i] net+1358/med+10.8 |

- backtest payoff: right +504 / wrong -954 / net -450 pts; median per fire -4.30 (n=35)
- backtest worst false alarm: 2026-07-27 13:49 -141.5pts adverse
- forward payoff: right +9029 / wrong -7795 / net +1234 pts; median per fire +2.40 (n=378)
- forward best call: 2026-10-26 05:02 +209.6pts remaining (episode 238.8pts, major)
- forward worst false alarm: 2026-10-05 06:59 -174.6pts adverse


---

# nas100 (nas100fut) — CANONICAL

Store span (1M, close ts): 2026-07-19 22:02:00+00:00 → 2026-11-06 21:29:00+00:00. Volume type: real futures volume (register 40 first-sync sanity; canonical verdict at this instrument's validation evening).

## Summary Matrix (page 1)

Engine `66be26997` — OBSERVATIONAL signal scoreboard - move-detection, not trading; no fills exist here by construction; never validation (docs/hypothesis_lifecycle.md stage 4)

**Review labels are RECOMMENDATIONS — none actioned, review pending operator familiarity.** Cells: marker + precision LIFT vs that context's OWN chance rate, (hits/fires), payoff net/median points (directional rows; either-direction rows have no payoff by construction). ▲/▼ = beyond ±2pp of chance, · = within. (°…) = small-n (fires<20 or episodes<10): dimmed, excluded from any future label arithmetic. Read READING_GUIDE.md first; full detail in hypothesis_performance.json.

| H | label | backtest whole | backtest london | forward whole | forward london |
|---|---|---|---|---|---|
| *context* | | 115 ep; chance 22.1%dir/41.8%either | 41 ep; chance 31.0%dir/56.1%either | 625 ep; chance 23.7%dir/45.1%either | 196 ep; chance 30.8%dir/57.5%either |
| S0-H1 | keep-watching | ▲i+4.6pp (9/34) · p+16.1pp cap184.4 net+122/med-15.7 | (°▲i+11.7pp (3/8) · p-18.5pp cap153.6 net-257/med-46.2) | ·i-1.0pp (100/490) · p+8.3pp cap109.8 net+3360/med+3.4 | ▲i+2.1pp (45/168) · p+5.5pp cap97.7 net+695/med+3.1 |
| S1-H1 | keep-watching | (°▲i+11.4pp (1/3) · p+44.6pp cap279.0 net+465/med+128.4) | — | ▲i+11.9pp (8/24) · p+13.8pp cap86.0 net+286/med+8.1 | (°▲i+18.2pp (3/7) · p+26.3pp cap76.2 net+318/med+54.9) |
| S0-H2 | promote-candidate | ▼i-3.5pp (59/320) · p-2.1pp cap156.4 net-3528/med-1.4 | ·i+1.3pp (16/59) · p-5.6pp cap106.7 net-313/med-30.0 | ▼i-5.2pp (395/2438) · p+4.1pp cap103.9 net+11212/med+2.5 | ·i-0.2pp (141/575) · p+2.9pp cap95.6 net+1908/med+3.3 |
| S1-H2 | promote-candidate | ▼i-3.0pp (42/222) · p-0.9pp cap140.3 net-1379/med-4.2 | ▲i+4.4pp (13/43) · p-0.8pp cap97.1 net-382/med-31.5 | ▼i-2.9pp (324/1747) · p+3.7pp cap105.4 net+7583/med+3.2 | ▲i+2.7pp (113/412) · p+3.4pp cap96.5 net+1771/med+5.7 |
| S0-H3 | keep-watching | (°▼i-21.9pp (0/1) · p+77.9pp cap105.8 net+106/med+105.8) | (°▼i-25.8pp (0/1) · p+69.0pp cap105.8 net+106/med+105.8) | (°▼i-9.6pp (2/17) · p+11.6pp cap75.0 net-442/med-15.9) | (°▲i+25.3pp (1/2) · p-30.8pp cap— net-95/med-47.4) |
| S0-H4 | keep-watching | — | — | ▼i-11.4pp (6/60) · p+29.6pp cap55.6 net+845/med+17.3 | (°▼i-5.9pp (3/16) · p+25.4pp cap46.7 net+149/med+17.4) |
| S0-H5 | keep-watching | — | — | (°▲i+28.6pp (1/2) · p-23.7pp cap— net-87/med-43.5) | (°▼i-24.7pp (0/1) · p-30.8pp cap— net-49/med-49.0) |
| S0-H6 | keep-watching | ▲i+4.2pp (5/29) · p-8.1pp cap260.8 [cls 39.1%/13.0%i] net-232/med-11.8 | (°▲i+59.8pp (4/5) · p-38.3pp cap— [cls 38.3%/20.2%i] net-719/med-105.3) | ▲i+3.4pp (73/402) · p+3.0pp cap103.5 [cls 36.8%/14.8%i] net-57/med-1.9 | ▲i+5.9pp (35/129) · p+8.9pp cap90.5 [cls 34.5%/21.2%i] net+870/med+11.8 |
| S0-H7 | keep-watching | ▼i-5.9pp (8/50) · p-0.1pp cap169.0 net+77/med-7.8 | (°·i-0.8pp (4/16) · p-6.0pp cap123.6 net-167/med-6.6) | ·i+1.1pp (80/356) · p+2.4pp cap82.9 net+784/med+5.5 | ▲i+5.0pp (30/101) · p+1.9pp cap82.9 net+485/med+5.5 |
| S0-H7 (either-dir) | keep-watching | ▼i-11.2pp (15/50) · p+4.2pp cap46.5 | (°·i+1.0pp (8/16) · p+0.1pp cap23.3) | ▼i-6.0pp (121/356) · p+5.7pp cap46.2 | ·i-0.9pp (46/101) · p+0.9pp cap54.3 |
| S0-H8 | keep-watching | ▼i-4.6pp (117/320) · p+1.6pp cap69.4 | ▼i-8.3pp (24/59) · p+4.9pp cap53.7 | ▼i-6.8pp (810/2438) · p+3.5pp cap65.7 | ▼i-2.7pp (251/575) · p+0.8pp cap66.1 |
| S0-H9 | keep-watching | ▲i+2.0pp (21/88) · p+0.6pp cap129.2 net+593/med-4.3 | (°▼i-25.8pp (0/9) · p+2.3pp cap76.3 net+410/med+11.6) | ·i-1.2pp (134/662) · p-3.0pp cap64.9 net-584/med-2.0 | ▼i-3.0pp (28/129) · p+3.3pp cap77.5 net-543/med-1.9 |
| S1-H9 | keep-watching | ▼i-13.9pp (2/25) · p+5.9pp cap265.9 net-373/med+10.8 | (°▼i-25.8pp (0/5) · p-31.0pp cap— net-57/med+2.3) | ▼i-15.3pp (8/131) · p+0.0pp cap168.7 net+2040/med+10.2 | ▼i-10.4pp (4/28) · p-2.2pp cap97.5 net+51/med+6.4 |
| S0-H10 | deprioritize | ·i+1.0pp (40/175) · p-5.5pp cap88.9 net+2743/med+15.3 | (°▼i-12.5pp (2/15) · p-17.7pp cap46.2 net-356/med-1.7) | ·i-1.8pp (298/1518) · p-1.0pp cap56.4 net+4092/med-1.7 | ·i-1.6pp (86/372) · p-0.2pp cap56.0 net+3667/med-1.9 |
| S0-H11 | keep-watching | ▼i-3.6pp (48/263) · p+2.2pp cap136.1 net+863/med+0.9 | ·i-1.6pp (22/91) · p-2.4pp cap113.7 net+264/med-3.9 | ▼i-5.1pp (417/2558) · p+3.1pp cap90.6 net+4341/med-0.9 | ▼i-4.9pp (156/788) · p+4.2pp cap90.6 net+3463/med-3.4 |
| S1-H11 | keep-watching | ▼i-8.1pp (24/174) · p+3.8pp cap133.5 net+293/med-14.1 | ·i+0.6pp (14/53) · p-2.7pp cap109.7 net-436/med-14.7 | ▼i-2.6pp (379/2015) · p+1.4pp cap87.8 net-2702/med-1.2 | ▼i-2.3pp (127/566) · p-2.4pp cap90.5 net-1659/med+0.3 |
| S0-H12 | keep-watching | — | — | — | — |
| S0-H13 | keep-watching | (°▼i-21.9pp (0/1) · p+77.9pp cap95.7 net+93/med+93.0) | (°▼i-25.8pp (0/1) · p+69.0pp cap95.7 net+93/med+93.0) | (°▲i+5.3pp (4/15) · p-10.4pp cap45.5 net-220/med-23.5) | (°▼i-24.7pp (0/1) · p-30.8pp cap— net-43/med-42.8) |
| S0-H14 | keep-watching | ·i+1.5pp (39/167) · p-13.1pp cap66.9 net-692/med+6.9 | ▼i-10.4pp (4/26) · p-19.5pp cap41.8 net-1762/med-17.1 | ·i-1.6pp (292/1472) · p-2.2pp cap60.0 net+5193/med-0.1 | ▼i-2.8pp (72/329) · p-2.5pp cap63.8 net+3802/med-4.8 |
| S0-H15 | keep-watching | — | — | — | — |
| S0-H16 | keep-watching | (°▼i-11.9pp (1/10) · p+27.9pp cap121.0 net+274/med+0.1) | — | ▼i-8.3pp (8/61) · p+7.4pp cap76.1 net+543/med+5.7 | — |
| S0-H17 | rows | (°▼i-8.6pp (2/15) · p+17.9pp cap166.0 net+681/med+10.2) | (°▼i-5.8pp (1/5) · p+9.0pp cap125.1 net-18/med-23.3) | ·i+0.0pp (50/234) · p+5.8pp cap102.5 net+1992/med+6.6 | ·i+0.6pp (22/87) · p+3.7pp cap88.1 net+82/med+5.5 |
| S0-H18 | rows | ▼i-8.1pp (8/58) · p-8.3pp cap127.3 net-1784/med-23.8 | ▲i+3.4pp (7/24) · p-22.7pp cap111.1 net-559/med-16.3 | ▼i-8.5pp (49/380) · p+4.2pp cap104.6 net+3465/med+2.0 | ▼i-5.6pp (25/131) · p+1.3pp cap98.8 net+790/med+2.7 |
| S0-H19 | rows | ▼i-2.3pp (40/204) · p+0.9pp cap180.0 net+1513/med+6.5 | ▼i-15.3pp (4/38) · p-2.1pp cap98.9 net-152/med+12.8 | ·i-1.9pp (328/1683) · p-0.9pp cap108.2 net-10882/med-3.6 | ·i-0.6pp (91/378) · p-6.5pp cap96.6 net-2721/med-5.1 |
| S0-H20 | rows | ▼i-10.8pp (1/46) · p+8.7pp cap277.1 [cls 39.1%/13.0%i] net+1398/med+2.9 | (°▲i+13.1pp (1/3) · p-38.3pp cap— [cls 38.3%/20.2%i] net-182/med-90.2) | ▼i-10.4pp (18/410) · p+1.5pp cap100.6 [cls 36.8%/14.8%i] net+2478/med+4.3 | ▼i-15.7pp (7/128) · p+0.7pp cap72.1 [cls 34.5%/21.2%i] net+2078/med+13.4 |
| **union coverage** | | 46.1% (53/115) | 39.0% (16/41) | 81.3% (508/625) | 81.1% (159/196) |

Not graded:  — see register entries.

## Hypothesis Cards (page 2)

### H1 — 2 signals
*A climactic bar — extreme volume on a wide spread late in an extended move — marks exhaustion, and price then reverses against the climax direction.*
Grading: directional. Latest review: keep-watching (recommendation).

- Question **Q1-H1**: see the register entry (status there is authoritative).
**S0-H1** — session × window grid (cells as in the matrix):

| session | backtest | forward |
|---|---|---|
| whole | ▲i+4.6pp (9/34) · p+16.1pp cap184.4 net+122/med-15.7 | ·i-1.0pp (100/490) · p+8.3pp cap109.8 net+3360/med+3.4 |
| london | (°▲i+11.7pp (3/8) · p-18.5pp cap153.6 net-257/med-46.2) | ▲i+2.1pp (45/168) · p+5.5pp cap97.7 net+695/med+3.1 |
| overlap | — | ·i-1.4pp (2/24) · p-3.9pp cap223.2 net+48/med-47.5 |
| ny_only | (°·i-1.8pp (2/11) · p+41.6pp cap291.5 net-215/med-87.5) | ▼i-8.6pp (13/123) · p+14.5pp cap178.2 net+1742/med+15.0 |
| dead | (°▲i+31.2pp (4/8) · p+0.8pp cap406.7 net-181/med-23.6) | ·i-1.1pp (21/97) · p+15.9pp cap86.0 net+410/med-3.1 |
| asia | (°▼i-25.0pp (0/7) · p+51.5pp cap178.9 net+776/med+154.4) | ·i+1.7pp (19/78) · p+8.2pp cap95.5 net+465/med+7.3 |

- backtest payoff: right +2899 / wrong -2777 / net +122 pts; median per fire -15.65 (n=34)
- backtest best call: 2026-07-29 18:02 +663.1pts remaining (episode 667.1pts, major)
- backtest worst false alarm: 2026-07-29 19:01 -712.5pts adverse
- forward payoff: right +20130 / wrong -16770 / net +3360 pts; median per fire +3.35 (n=488)
- forward best call: 2026-11-04 03:06 +578.9pts remaining (episode 523.1pts, major)
- forward worst false alarm: 2026-11-05 15:54 -524.2pts adverse
- earliness (backtest): median 183.0 pts of move remaining at fire (n=8)

**S1-H1** — session × window grid (cells as in the matrix):

| session | backtest | forward |
|---|---|---|
| whole | (°▲i+11.4pp (1/3) · p+44.6pp cap279.0 net+465/med+128.4) | ▲i+11.9pp (8/24) · p+13.8pp cap86.0 net+286/med+8.1 |
| london | — | (°▲i+18.2pp (3/7) · p+26.3pp cap76.2 net+318/med+54.9) |
| overlap | — | — |
| ny_only | — | (°▼i-19.2pp (0/4) · p+11.9pp cap117.9 net-27/med-20.5) |
| dead | (°▲i+31.2pp (1/2) · p+38.3pp cap406.7 net+337/med+168.5) | (°▲i+2.3pp (2/8) · p+36.0pp cap96.6 net+107/med+47.5) |
| asia | (°▼i-25.0pp (0/1) · p+80.1pp cap151.3 net+128/med+128.4) | (°▲i+37.3pp (3/5) · p-25.1pp cap— net-113/med-25.9) |

- backtest payoff: right +521 / wrong -56 / net +465 pts; median per fire +128.40 (n=3)
- backtest best call: 2026-07-28 23:45 +372.3pts remaining (episode 501.5pts, major)
- backtest worst false alarm: 2026-07-28 23:45 -141.6pts adverse
- forward payoff: right +914 / wrong -629 / net +286 pts; median per fire +8.10 (n=24)
- forward best call: 2026-10-26 10:43 +220.7pts remaining (episode 220.7pts, major)
- forward worst false alarm: 2026-11-05 17:12 -231.0pts adverse
- earliness (backtest): median 372.3 pts of move remaining at fire (n=1)

### H2 — 2 signals
*A failed probe beyond a prior extreme — an upthrust above or spring below that closes back inside — reverses against the probe.*
Grading: directional. Latest review: promote-candidate (recommendation).

**S0-H2** — session × window grid (cells as in the matrix):

| session | backtest | forward |
|---|---|---|
| whole | ▼i-3.5pp (59/320) · p-2.1pp cap156.4 net-3528/med-1.4 | ▼i-5.2pp (395/2438) · p+4.1pp cap103.9 net+11212/med+2.5 |
| london | ·i+1.3pp (16/59) · p-5.6pp cap106.7 net-313/med-30.0 | ·i-0.2pp (141/575) · p+2.9pp cap95.6 net+1908/med+3.3 |
| overlap | (°▼i-4.8pp (1/32) · p-12.7pp cap193.4 net-742/med-38.1) | ▼i-3.4pp (17/270) · p+6.9pp cap156.6 net+5078/med+14.8 |
| ny_only | ▼i-10.1pp (7/71) · p+2.6pp cap234.9 net-3199/med-7.4 | ▼i-8.5pp (56/522) · p+5.9pp cap169.8 net-114/med-4.3 |
| dead | ·i+0.0pp (9/48) · p+5.0pp cap284.2 net+874/med+2.4 | ▼i-6.3pp (53/323) · p+8.3pp cap89.8 net+897/med-0.9 |
| asia | ·i-1.4pp (26/110) · p+0.1pp cap113.5 net-147/med+10.2 | ▼i-5.6pp (128/748) · p+2.2pp cap79.7 net+3443/med+4.4 |

- backtest payoff: right +13405 / wrong -16933 / net -3528 pts; median per fire -1.35 (n=320)
- backtest best call: 2026-07-30 07:00 +812.7pts remaining (episode 832.8pts, major)
- backtest worst false alarm: 2026-07-29 19:00 -719.1pts adverse
- forward payoff: right +87368 / wrong -76156 / net +11212 pts; median per fire +2.45 (n=2438)
- forward best call: 2026-11-04 03:18 +528.9pts remaining (episode 523.1pts, major)
- forward worst false alarm: 2026-11-05 15:00 -746.0pts adverse
- earliness (backtest): median 111.3 pts of move remaining at fire (n=25)

**S1-H2** — session × window grid (cells as in the matrix):

| session | backtest | forward |
|---|---|---|
| whole | ▼i-3.0pp (42/222) · p-0.9pp cap140.3 net-1379/med-4.2 | ▼i-2.9pp (324/1747) · p+3.7pp cap105.4 net+7583/med+3.2 |
| london | ▲i+4.4pp (13/43) · p-0.8pp cap97.1 net-382/med-31.5 | ▲i+2.7pp (113/412) · p+3.4pp cap96.5 net+1771/med+5.7 |
| overlap | (°▼i-7.9pp (0/20) · p-2.7pp cap185.1 net+164/med+49.0) | ▼i-3.3pp (13/202) · p+8.5pp cap155.7 net+3615/med+24.1 |
| ny_only | ▼i-11.7pp (4/48) · p-0.4pp cap194.2 net-1585/med-19.9 | ▼i-6.6pp (48/381) · p+6.8pp cap175.7 net+2142/med-2.6 |
| dead | ▲i+2.4pp (7/33) · p+0.4pp cap206.8 net+152/med-7.9 | ▼i-4.3pp (40/217) · p+4.9pp cap86.4 net-1437/med-2.9 |
| asia | ·i-1.9pp (18/78) · p+1.9pp cap106.9 net+272/med+15.2 | ▼i-2.1pp (110/535) · p+0.5pp cap81.8 net+1492/med+3.4 |

- backtest payoff: right +8973 / wrong -10352 / net -1379 pts; median per fire -4.15 (n=222)
- backtest best call: 2026-07-30 07:00 +812.7pts remaining (episode 832.8pts, major)
- backtest worst false alarm: 2026-07-29 19:16 -700.8pts adverse
- forward payoff: right +61335 / wrong -53752 / net +7583 pts; median per fire +3.20 (n=1747)
- forward best call: 2026-11-04 03:18 +528.9pts remaining (episode 523.1pts, major)
- forward worst false alarm: 2026-11-05 15:00 -746.0pts adverse
- earliness (backtest): median 118.9 pts of move remaining at fire (n=23)

### H3 — 1 signal
*Repeated absorption — high effort with no result — at a price level precedes a breakout through that level.*
Grading: directional. Latest review: keep-watching (recommendation).

**S0-H3** — session × window grid (cells as in the matrix):

| session | backtest | forward |
|---|---|---|
| whole | (°▼i-21.9pp (0/1) · p+77.9pp cap105.8 net+106/med+105.8) | (°▼i-9.6pp (2/17) · p+11.6pp cap75.0 net-442/med-15.9) |
| london | (°▼i-25.8pp (0/1) · p+69.0pp cap105.8 net+106/med+105.8) | (°▲i+25.3pp (1/2) · p-30.8pp cap— net-95/med-47.4) |
| overlap | — | — |
| ny_only | — | — |
| dead | — | (°▼i-22.7pp (0/2) · p+36.0pp cap46.1 net+7/med+3.6) |
| asia | — | (°▼i-15.0pp (1/13) · p+13.4pp cap88.3 net-354/med-67.5) |

- backtest payoff: right +106 / wrong +0 / net +106 pts; median per fire +105.80 (n=1)
- forward payoff: right +388 / wrong -830 / net -442 pts; median per fire -15.90 (n=17)
- forward best call: 2026-10-13 03:41 +77.4pts remaining (episode 71.2pts)
- forward worst false alarm: 2026-10-30 00:02 -177.5pts adverse

### H4 — 1 signal
*In an established trend, a quiet (low-volume) pullback resolves with trend resumption.*
Grading: directional. Latest review: keep-watching (recommendation).

**S0-H4** — session × window grid (cells as in the matrix):

| session | backtest | forward |
|---|---|---|
| whole | — | ▼i-11.4pp (6/60) · p+29.6pp cap55.6 net+845/med+17.3 |
| london | — | (°▼i-5.9pp (3/16) · p+25.4pp cap46.7 net+149/med+17.4) |
| overlap | — | (°▼i-9.7pp (0/11) · p+12.4pp cap96.1 net+240/med+48.3) |
| ny_only | — | ▼i-4.9pp (3/21) · p+39.3pp cap69.4 net+615/med+43.0 |
| dead | — | (°▼i-22.7pp (0/2) · p-14.0pp cap— net+8/med+3.8) |
| asia | — | (°▼i-22.7pp (0/10) · p+44.9pp cap38.6 net-168/med-8.4) |

- forward payoff: right +1804 / wrong -959 / net +845 pts; median per fire +17.30 (n=60)
- forward best call: 2026-10-06 12:24 +100.2pts remaining (episode 130.2pts, major)
- forward worst false alarm: 2026-10-06 14:36 -94.8pts adverse

### H5 — 1 signal
*A buying climax that extends far above its trend mean mean-reverts (climax-extension fade; registered short-side only).*
Grading: directional. Latest review: keep-watching (recommendation).

**S0-H5** — session × window grid (cells as in the matrix):

| session | backtest | forward |
|---|---|---|
| whole | — | (°▲i+28.6pp (1/2) · p-23.7pp cap— net-87/med-43.5) |
| london | — | (°▼i-24.7pp (0/1) · p-30.8pp cap— net-49/med-49.0) |
| overlap | — | — |
| ny_only | — | (°▲i+80.8pp (1/1) · p-13.1pp cap— net-38/med-37.9) |
| dead | — | — |
| asia | — | — |

- forward payoff: right +0 / wrong -87 / net -87 pts; median per fire -43.45 (n=2)
- forward best call: 2026-09-24 16:30 +75.4pts remaining (episode 165.5pts)
- forward worst false alarm: 2026-09-24 16:30 -113.6pts adverse

### H6 — 1 signal
*A wide-spread rejection bar at a session extreme (measured day-relative, volume-agnostic) reverses away from the extreme.*
Grading: directional. Latest review: keep-watching (recommendation).

- Question **Q1-H6**: see the register entry (status there is authoritative).
- Question **Q2-H6**: see the register entry (status there is authoritative).
- Question **Q3-H6**: see the register entry (status there is authoritative).
**S0-H6** — session × window grid (cells as in the matrix):

| session | backtest | forward |
|---|---|---|
| whole | ▲i+4.2pp (5/29) · p-8.1pp cap260.8 [cls 39.1%/13.0%i] net-232/med-11.8 | ▲i+3.4pp (73/402) · p+3.0pp cap103.5 [cls 36.8%/14.8%i] net-57/med-1.9 |
| london | (°▲i+59.8pp (4/5) · p-38.3pp cap— [cls 38.3%/20.2%i] net-719/med-105.3) | ▲i+5.9pp (35/129) · p+8.9pp cap90.5 [cls 34.5%/21.2%i] net+870/med+11.8 |
| overlap | (°·i-1.8pp (1/20) · p-7.4pp cap263.9 [cls 47.4%/6.8%i] net+333/med+9.0) | ▲i+2.7pp (15/160) · p-0.1pp cap114.6 [cls 45.1%/6.7%i] net-997/med-1.7 |
| ny_only | — | ▲i+6.2pp (4/24) · p+16.0pp cap177.3 [cls 25.7%/10.5%i] net+213/med-17.9 |
| dead | (°▼i-13.5pp (0/3) · p-23.0pp cap— [cls 23.0%/13.5%i] net+42/med+18.9) | (°▲i+13.8pp (4/15) · p-8.5pp cap85.1 [cls 28.5%/12.9%i] net-327/med-14.5) |
| asia | (°▼i-18.2pp (0/1) · p+74.8pp cap129.0 [cls 25.2%/18.2%i] net+112/med+111.8) | ▲i+2.1pp (15/74) · p-7.4pp cap95.2 [cls 33.1%/18.2%i] net+183/med-9.7 |

- backtest payoff: right +1875 / wrong -2108 / net -232 pts; median per fire -11.80 (n=29)
- backtest best call: 2026-08-03 11:04 +303.5pts remaining (episode 396.3pts, major)
- backtest worst false alarm: 2026-07-27 13:46 -514.5pts adverse
- forward payoff: right +15211 / wrong -15268 / net -57 pts; median per fire -1.85 (n=402)
- forward best call: 2026-11-04 03:16 +538.4pts remaining (episode 523.1pts, major)
- forward worst false alarm: 2026-11-05 15:00 -746.0pts adverse
- earliness (backtest): median 78.8 pts of move remaining at fire (n=2)

### H7 — 1 signal
*Quiet decline at a session extreme is disguised accumulation: effortless (low-volume) weakness reverses UP once selling fails to attract participation (mirror: quiet advance at a high reverses down).*
Grading: directional + either-direction (dual). Latest review: keep-watching (recommendation).

- Question **Q1-H7**: see the register entry (status there is authoritative).
**S0-H7** — session × window grid (cells as in the matrix):

| session | backtest | forward |
|---|---|---|
| whole | ▼i-5.9pp (8/50) · p-0.1pp cap169.0 net+77/med-7.8 | ·i+1.1pp (80/356) · p+2.4pp cap82.9 net+784/med+5.5 |
| london | (°·i-0.8pp (4/16) · p-6.0pp cap123.6 net-167/med-6.6) | ▲i+5.0pp (30/101) · p+1.9pp cap82.9 net+485/med+5.5 |
| overlap | (°▲i+4.6pp (1/8) · p+24.8pp cap183.1 net+464/med+8.3) | ▲i+6.6pp (7/43) · p+1.8pp cap145.4 net-36/med+14.7 |
| ny_only | (°▲i+5.0pp (2/8) · p-12.9pp cap— net-76/med-18.5) | ▼i-5.4pp (8/58) · p+7.6pp cap108.0 net+838/med+15.7 |
| dead | (°·i+1.2pp (1/5) · p-11.7pp cap— net+53/med+23.0) | ▼i-13.6pp (2/22) · p-9.5pp cap71.3 net-382/med-10.2 |
| asia | (°▼i-25.0pp (0/13) · p-4.5pp cap142.4 net-196/med-24.5) | ▲i+2.3pp (33/132) · p-0.9pp cap72.1 net-120/med+2.8 |

- backtest payoff: right +2351 / wrong -2274 / net +77 pts; median per fire -7.75 (n=50)
- backtest best call: 2026-07-29 09:26 +577.3pts remaining (episode 632.8pts, major)
- backtest worst false alarm: 2026-07-31 13:43 -365.8pts adverse
- forward payoff: right +10485 / wrong -9701 / net +784 pts; median per fire +5.50 (n=356)
- forward best call: 2026-10-30 05:07 +806.3pts remaining (episode 806.3pts, major)
- forward worst false alarm: 2026-11-05 15:10 -623.7pts adverse
- earliness (backtest): median 308.2 pts of move remaining at fire (n=7)

**S0-H7 (either-dir)** — session × window grid (cells as in the matrix):

| session | backtest | forward |
|---|---|---|
| whole | ▼i-11.2pp (15/50) · p+4.2pp cap46.5 | ▼i-6.0pp (121/356) · p+5.7pp cap46.2 |
| london | (°·i+1.0pp (8/16) · p+0.1pp cap23.3) | ·i-0.9pp (46/101) · p+0.9pp cap54.3 |
| overlap | (°▼i-3.3pp (1/8) · p+29.8pp cap118.7) | ▼i-2.4pp (7/43) · p+1.8pp cap97.4 |
| ny_only | (°·i+0.4pp (3/8) · p-12.8pp cap18.8) | ▼i-11.9pp (14/58) · p+9.4pp cap73.5 |
| dead | (°▼i-14.4pp (1/5) · p-22.6pp cap—) | ▼i-31.1pp (2/22) · p+5.0pp cap17.8 |
| asia | (°▼i-31.4pp (2/13) · p-0.9pp cap35.7) | ▼i-3.5pp (52/132) · p+2.6pp cap30.2 |

- backtest payoff: n/a by construction (either-direction)
- backtest best call: 2026-07-29 09:26 +577.3pts remaining (episode 632.8pts, major)
- backtest worst false alarm: 2026-07-29 02:54 -123.2pts adverse
- forward payoff: n/a by construction (either-direction)
- forward best call: 2026-10-30 05:07 +806.3pts remaining (episode 806.3pts, major)
- forward worst false alarm: 2026-11-06 02:01 -165.5pts adverse
- earliness (backtest): median 170.9 pts of move remaining at fire (n=14)

### H8 — 1 signal
*Reversal-signature bar anatomy (upthrust/spring) predicts imminent range expansion irrespective of direction.*
Grading: either-direction. Latest review: keep-watching (recommendation).

**S0-H8** — session × window grid (cells as in the matrix):

| session | backtest | forward |
|---|---|---|
| whole | ▼i-4.6pp (117/320) · p+1.6pp cap69.4 | ▼i-6.8pp (810/2438) · p+3.5pp cap65.7 |
| london | ▼i-8.3pp (24/59) · p+4.9pp cap53.7 | ▼i-2.7pp (251/575) · p+0.8pp cap66.1 |
| overlap | (°▼i-9.6pp (2/32) · p-4.6pp cap69.4) | ▼i-3.9pp (40/270) · p+9.4pp cap96.5 |
| ny_only | ▼i-13.2pp (17/71) · p+18.4pp cap52.0 | ▼i-8.0pp (146/522) · p+6.9pp cap112.5 |
| dead | ▼i-3.2pp (15/48) · p+2.4pp cap133.9 | ▼i-7.4pp (106/323) · p+11.3pp cap65.3 |
| asia | ▲i+6.8pp (59/110) · p-3.9pp cap84.3 | ▼i-7.2pp (267/748) · p+0.6pp cap55.7 |

- backtest payoff: n/a by construction (either-direction)
- backtest best call: 2026-07-30 06:39 +793.0pts remaining (episode 832.8pts, major)
- backtest worst false alarm: 2026-07-29 19:48 -233.6pts adverse
- forward payoff: n/a by construction (either-direction)
- forward best call: 2026-11-04 06:18 +498.4pts remaining (episode 436.5pts, major)
- forward worst false alarm: 2026-11-05 16:23 -285.8pts adverse
- earliness (backtest): median 130.5 pts of move remaining at fire (n=32)

### H9 — 2 signals
*Persistent lower-TF directional pressure that recruits expanding participation at the parent timeframe precedes continuation beyond what the parent label alone predicts; pressure without participation expansion does not.*
Grading: directional. Latest review: keep-watching (recommendation).

- Question **Q2-H9**: see the register entry (status there is authoritative).
**S0-H9** — session × window grid (cells as in the matrix):

| session | backtest | forward |
|---|---|---|
| whole | ▲i+2.0pp (21/88) · p+0.6pp cap129.2 net+593/med-4.3 | ·i-1.2pp (134/662) · p-3.0pp cap64.9 net-584/med-2.0 |
| london | (°▼i-25.8pp (0/9) · p+2.3pp cap76.3 net+410/med+11.6) | ▼i-3.0pp (28/129) · p+3.3pp cap77.5 net-543/med-1.9 |
| overlap | (°▼i-7.9pp (0/10) · p+12.3pp cap306.3 net+540/med+51.3) | ▲i+11.1pp (21/101) · p-17.3pp cap112.0 net-5/med+2.7 |
| ny_only | ▲i+28.0pp (12/25) · p-4.9pp cap125.7 net-148/med-7.0 | ▼i-6.7pp (19/152) · p-1.3pp cap65.5 net-2286/med-9.2 |
| dead | (°▲i+4.7pp (4/17) · p+17.7pp cap265.9 net+98/med-5.5) | ▼i-10.0pp (9/71) · p-5.5pp cap184.3 net+669/med-1.4 |
| asia | ▼i-6.5pp (5/27) · p-1.4pp cap78.6 net-307/med-10.2 | ▲i+4.6pp (57/209) · p+0.3pp cap48.7 net+1582/med+0.0 |

- backtest payoff: right +3019 / wrong -2427 / net +593 pts; median per fire -4.35 (n=88)
- backtest best call: 2026-08-03 17:00 +141.6pts remaining (episode 136.6pts)
- backtest worst false alarm: 2026-07-29 18:45 -500.8pts adverse
- forward payoff: right +15635 / wrong -16218 / net -584 pts; median per fire -2.05 (n=642)
- forward best call: 2026-11-04 06:30 +459.9pts remaining (episode 436.5pts, major)
- forward worst false alarm: 2026-11-05 14:25 -984.0pts adverse
- earliness (backtest): median 74.7 pts of move remaining at fire (n=6)

**S1-H9** — session × window grid (cells as in the matrix):

| session | backtest | forward |
|---|---|---|
| whole | ▼i-13.9pp (2/25) · p+5.9pp cap265.9 net-373/med+10.8 | ▼i-15.3pp (8/131) · p+0.0pp cap168.7 net+2040/med+10.2 |
| london | (°▼i-25.8pp (0/5) · p-31.0pp cap— net-57/med+2.3) | ▼i-10.4pp (4/28) · p-2.2pp cap97.5 net+51/med+6.4 |
| overlap | (°▼i-7.9pp (0/1) · p+62.3pp cap306.3 net+150/med+150.3) | (°▼i-9.7pp (0/14) · p-4.5pp cap281.5 net+304/med+14.7) |
| ny_only | (°▼i-20.0pp (0/3) · p-12.9pp cap— net-373/med+63.9) | ▼i-9.8pp (3/32) · p-10.0pp cap339.3 net-876/med-11.3 |
| dead | (°▼i-18.8pp (0/8) · p+50.8pp cap265.9 net+174/med+55.5) | (°▼i-22.7pp (0/19) · p+7.1pp cap290.2 net+829/med+14.4) |
| asia | (°·i+0.0pp (2/8) · p-7.4pp cap78.6 net-267/med-8.6) | ▼i-20.1pp (1/38) · p+11.7pp cap101.2 net+1732/med+20.9 |

- backtest payoff: right +1181 / wrong -1554 / net -373 pts; median per fire +10.80 (n=25)
- backtest best call: 2026-07-30 03:00 +120.0pts remaining (episode 134.4pts)
- backtest worst false alarm: 2026-07-29 18:45 -500.8pts adverse
- forward payoff: right +6327 / wrong -4288 / net +2040 pts; median per fire +10.25 (n=126)
- forward best call: 2026-11-04 06:30 +459.9pts remaining (episode 436.5pts, major)
- forward worst false alarm: 2026-11-04 04:25 -470.3pts adverse
- earliness (backtest): median 120.0 pts of move remaining at fire (n=1)

### H10 — 1 signal
*In an established 1-minute trend, no-demand/no-supply prints in the trend's direction signal continuation.*
Grading: directional. Latest review: deprioritize (recommendation).

**S0-H10** — session × window grid (cells as in the matrix):

| session | backtest | forward |
|---|---|---|
| whole | ·i+1.0pp (40/175) · p-5.5pp cap88.9 net+2743/med+15.3 | ·i-1.8pp (298/1518) · p-1.0pp cap56.4 net+4092/med-1.7 |
| london | (°▼i-12.5pp (2/15) · p-17.7pp cap46.2 net-356/med-1.7) | ·i-1.6pp (86/372) · p-0.2pp cap56.0 net+3667/med-1.9 |
| overlap | (°▼i-7.9pp (0/18) · p-37.7pp cap— net+764/med+45.5) | ▲i+4.7pp (30/208) · p-6.2pp cap117.1 net+652/med-11.0 |
| ny_only | ▲i+2.9pp (11/48) · p-4.6pp cap86.1 net+398/med+12.5 | ▲i+6.9pp (77/295) · p+2.5pp cap68.1 net+889/med+4.5 |
| dead | (°▼i-6.3pp (2/16) · p+0.8pp cap254.7 net+551/med+8.9) | ▼i-5.5pp (27/157) · p-7.0pp cap40.6 net-672/med-2.5 |
| asia | ▲i+7.1pp (25/78) · p+7.0pp cap99.1 net+1385/med+15.6 | ▼i-6.7pp (78/486) · p-1.0pp cap45.2 net-446/med+1.4 |

- backtest payoff: right +4792 / wrong -2049 / net +2743 pts; median per fire +15.30 (n=175)
- backtest best call: 2026-08-03 05:33 +168.5pts remaining (episode 160.7pts, major)
- backtest worst false alarm: 2026-07-27 12:56 -252.9pts adverse
- forward payoff: right +29975 / wrong -25883 / net +4092 pts; median per fire -1.70 (n=1517)
- forward best call: 2026-11-02 10:55 +656.6pts remaining (episode 680.3pts, major)
- forward worst false alarm: 2026-10-02 14:26 -268.1pts adverse
- earliness (backtest): median 78.8 pts of move remaining at fire (n=8)

### H11 — 2 signals
*Price entering a low-volume price zone traverses it faster than baseline; entering a high-volume node it stalls or reverses at above-baseline rates.*
Grading: directional. Latest review: keep-watching (recommendation).

- Question **Q1-H11**: see the register entry (status there is authoritative).
- Question **Q2-H11**: see the register entry (status there is authoritative).
**S0-H11** — session × window grid (cells as in the matrix):

| session | backtest | forward |
|---|---|---|
| whole | ▼i-3.6pp (48/263) · p+2.2pp cap136.1 net+863/med+0.9 | ▼i-5.1pp (417/2558) · p+3.1pp cap90.6 net+4341/med-0.9 |
| london | ·i-1.6pp (22/91) · p-2.4pp cap113.7 net+264/med-3.9 | ▼i-4.9pp (156/788) · p+4.2pp cap90.6 net+3463/med-3.4 |
| overlap | (°▼i-7.9pp (0/20) · p+2.3pp cap232.1 net-137/med-23.4) | ▼i-2.2pp (20/268) · p+2.7pp cap131.5 net-588/med+5.5 |
| ny_only | ▼i-13.1pp (2/29) · p+14.7pp cap229.4 net+826/med+77.1 | ▼i-6.3pp (61/474) · p+3.4pp cap124.7 net-638/med-1.8 |
| dead | ·i-1.6pp (10/58) · p+10.7pp cap98.2 net+874/med-3.1 | ▼i-3.9pp (51/271) · p+0.4pp cap83.4 net+566/med+1.0 |
| asia | ▼i-3.5pp (14/65) · p-6.1pp cap112.5 net-964/med+3.6 | ▼i-5.7pp (129/757) · p+0.8pp cap67.6 net+1538/med+0.3 |

- backtest payoff: right +10765 / wrong -9902 / net +863 pts; median per fire +0.90 (n=262)
- backtest best call: 2026-07-30 07:02 +741.2pts remaining (episode 832.8pts, major)
- backtest worst false alarm: 2026-07-29 13:50 -332.3pts adverse
- forward payoff: right +67520 / wrong -63179 / net +4341 pts; median per fire -0.90 (n=2556)
- forward best call: 2026-10-14 07:10 +621.8pts remaining (episode 641.7pts, major)
- forward worst false alarm: 2026-11-05 14:36 -875.2pts adverse
- earliness (backtest): median 176.0 pts of move remaining at fire (n=14)

**S1-H11** — session × window grid (cells as in the matrix):

| session | backtest | forward |
|---|---|---|
| whole | ▼i-8.1pp (24/174) · p+3.8pp cap133.5 net+293/med-14.1 | ▼i-2.6pp (379/2015) · p+1.4pp cap87.8 net-2702/med-1.2 |
| london | ·i+0.6pp (14/53) · p-2.7pp cap109.7 net-436/med-14.7 | ▼i-2.3pp (127/566) · p-2.4pp cap90.5 net-1659/med+0.3 |
| overlap | (°·i-1.2pp (1/15) · p-11.0pp cap192.0 net-139/med-40.7) | ▼i-4.6pp (11/215) · p+8.3pp cap123.5 net-734/med-3.3 |
| ny_only | ▼i-20.0pp (0/39) · p+10.2pp cap558.0 net+1758/med-19.4 | ▼i-3.8pp (49/319) · p+0.1pp cap118.9 net+334/med-1.5 |
| dead | (°▼i-2.1pp (2/12) · p-3.4pp cap141.6 net-253/med+3.9) | ▲i+6.8pp (83/281) · p+4.5pp cap86.0 net+440/med-0.5 |
| asia | ▼i-12.3pp (7/55) · p+9.2pp cap127.2 net-637/med-13.4 | ▼i-5.5pp (109/634) · p+0.5pp cap67.6 net-1082/med-1.8 |

- backtest payoff: right +9792 / wrong -9499 / net +293 pts; median per fire -14.05 (n=174)
- backtest best call: 2026-07-29 09:17 +555.3pts remaining (episode 632.8pts, major)
- backtest worst false alarm: 2026-07-29 19:07 -730.3pts adverse
- forward payoff: right +53914 / wrong -56616 / net -2702 pts; median per fire -1.20 (n=2015)
- forward best call: 2026-11-05 11:12 +1677.5pts remaining (episode 1706.4pts, major)
- forward worst false alarm: 2026-11-05 14:11 -924.4pts adverse
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
| whole | (°▼i-21.9pp (0/1) · p+77.9pp cap95.7 net+93/med+93.0) | (°▲i+5.3pp (4/15) · p-10.4pp cap45.5 net-220/med-23.5) |
| london | (°▼i-25.8pp (0/1) · p+69.0pp cap95.7 net+93/med+93.0) | (°▼i-24.7pp (0/1) · p-30.8pp cap— net-43/med-42.8) |
| overlap | — | (°▼i-9.7pp (0/3) · p-33.1pp cap— net-53/med-24.2) |
| ny_only | — | (°▼i-19.2pp (0/3) · p-13.1pp cap— net-100/med-37.2) |
| dead | — | (°▲i+10.6pp (1/3) · p+19.3pp cap29.4 net-97/med-33.0) |
| asia | — | (°▲i+37.3pp (3/5) · p-5.1pp cap61.6 net+73/med+18.0) |

- backtest payoff: right +93 / wrong +0 / net +93 pts; median per fire +93.00 (n=1)
- forward payoff: right +163 / wrong -383 / net -220 pts; median per fire -23.50 (n=15)
- forward best call: 2026-10-19 00:30 +163.4pts remaining (episode 144.2pts)
- forward worst false alarm: 2026-10-12 13:50 -110.4pts adverse

### H14 — 1 signal
*Counter-trend No Demand / No Supply prints in an established trend mark absorption and precede trend continuation.*
Grading: directional. Latest review: keep-watching (recommendation).

**S0-H14** — session × window grid (cells as in the matrix):

| session | backtest | forward |
|---|---|---|
| whole | ·i+1.5pp (39/167) · p-13.1pp cap66.9 net-692/med+6.9 | ·i-1.6pp (292/1472) · p-2.2pp cap60.0 net+5193/med-0.1 |
| london | ▼i-10.4pp (4/26) · p-19.5pp cap41.8 net-1762/med-17.1 | ▼i-2.8pp (72/329) · p-2.5pp cap63.8 net+3802/med-4.8 |
| overlap | (°▼i-7.9pp (0/17) · p-37.7pp cap— net+433/med+24.0) | ·i-1.4pp (16/192) · p-2.9pp cap113.7 net+1093/med-9.2 |
| ny_only | ▲i+15.3pp (18/51) · p-12.9pp cap— net+410/med+13.6 | ▲i+10.4pp (88/297) · p-1.0pp cap75.0 net+693/med+7.2 |
| dead | (°▼i-7.7pp (2/18) · p-11.7pp cap— net-56/med+4.5) | ·i-0.3pp (34/152) · p-6.8pp cap75.0 net-76/med-2.0 |
| asia | ▲i+2.3pp (15/55) · p+1.9pp cap76.0 net+282/med+6.6 | ▼i-6.4pp (82/502) · p-1.6pp cap45.3 net-318/med+1.9 |

- backtest payoff: right +2905 / wrong -3598 / net -692 pts; median per fire +6.90 (n=167)
- backtest best call: 2026-08-03 05:34 +164.0pts remaining (episode 160.7pts, major)
- backtest worst false alarm: 2026-07-27 12:59 -334.6pts adverse
- forward payoff: right +30365 / wrong -25173 / net +5193 pts; median per fire -0.10 (n=1471)
- forward best call: 2026-09-23 22:46 +424.0pts remaining (episode 427.6pts, major)
- forward worst false alarm: 2026-11-04 14:13 -510.0pts adverse
- earliness (backtest): median 101.1 pts of move remaining at fire (n=12)

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
| whole | (°▼i-11.9pp (1/10) · p+27.9pp cap121.0 net+274/med+0.1) | ▼i-8.3pp (8/61) · p+7.4pp cap76.1 net+543/med+5.7 |
| london | — | — |
| overlap | — | — |
| ny_only | (°▼i-10.0pp (1/10) · p+37.1pp cap121.0 net+274/med+0.1) | ▼i-6.1pp (8/61) · p+18.0pp cap76.1 net+543/med+5.7 |
| dead | — | — |
| asia | — | — |

- backtest payoff: right +666 / wrong -392 / net +274 pts; median per fire +0.05 (n=10)
- backtest best call: 2026-08-03 19:30 +30.1pts remaining (episode 61.6pts)
- backtest worst false alarm: 2026-07-23 19:30 -188.1pts adverse
- forward payoff: right +1654 / wrong -1112 / net +543 pts; median per fire +5.70 (n=61)
- forward best call: 2026-10-22 19:30 +118.1pts remaining (episode 118.1pts)
- forward worst false alarm: 2026-10-30 19:30 -170.8pts adverse
- earliness (backtest): median 30.1 pts of move remaining at fire (n=1)

### H17 — 1 signal
*A climax reversal signal followed by absorption within five bars — effort meeting a quiet counter-party — marks a genuine exhaustion turn: the two-chapter story (exhaustion needs absorption to become reversal).*
Grading: directional. Latest review: rows (recommendation).

**S0-H17** — session × window grid (cells as in the matrix):

| session | backtest | forward |
|---|---|---|
| whole | (°▼i-8.6pp (2/15) · p+17.9pp cap166.0 net+681/med+10.2) | ·i+0.0pp (50/234) · p+5.8pp cap102.5 net+1992/med+6.6 |
| london | (°▼i-5.8pp (1/5) · p+9.0pp cap125.1 net-18/med-23.3) | ·i+0.6pp (22/87) · p+3.7pp cap88.1 net+82/med+5.5 |
| overlap | — | (°▲i+5.7pp (2/13) · p-10.0pp cap120.5 net-49/med-50.9) |
| ny_only | — | ▼i-19.2pp (0/44) · p+11.9pp cap175.3 net+1192/med+19.0 |
| dead | (°·i+1.2pp (1/5) · p+8.3pp cap360.0 net+282/med+13.9) | ▲i+7.3pp (12/40) · p+11.0pp cap95.2 net+342/med+2.5 |
| asia | (°▼i-25.0pp (0/5) · p+40.1pp cap172.4 net+417/med+120.1) | ▲i+5.3pp (14/50) · p+4.9pp cap85.5 net+424/med+7.8 |

- backtest payoff: right +958 / wrong -277 / net +681 pts; median per fire +10.20 (n=15)
- backtest best call: 2026-07-29 23:42 +191.5pts remaining (episode 157.1pts)
- backtest worst false alarm: 2026-07-28 07:57 -96.5pts adverse
- forward payoff: right +8494 / wrong -6502 / net +1992 pts; median per fire +6.60 (n=233)
- forward best call: 2026-11-04 03:07 +586.6pts remaining (episode 523.1pts, major)
- forward worst false alarm: 2026-11-04 00:40 -315.0pts adverse
- earliness (backtest): median 150.3 pts of move remaining at fire (n=2)

### H18 — 1 signal
*A gap-traversal signal followed by a same-direction effortless print within five bars — travel meeting no opposition — continues: the map says vacuum, the tape confirms no resistance.*
Grading: directional. Latest review: rows (recommendation).

**S0-H18** — session × window grid (cells as in the matrix):

| session | backtest | forward |
|---|---|---|
| whole | ▼i-8.1pp (8/58) · p-8.3pp cap127.3 net-1784/med-23.8 | ▼i-8.5pp (49/380) · p+4.2pp cap104.6 net+3465/med+2.0 |
| london | ▲i+3.4pp (7/24) · p-22.7pp cap111.1 net-559/med-16.3 | ▼i-5.6pp (25/131) · p+1.3pp cap98.8 net+790/med+2.7 |
| overlap | (°▼i-7.9pp (0/6) · p+29.0pp cap141.5 net-621/med-85.3) | ·i-0.2pp (4/42) · p+16.9pp cap122.4 net+863/med+28.4 |
| ny_only | (°▼i-20.0pp (0/3) · p-12.9pp cap— net-88/med-59.0) | ▼i-5.1pp (10/71) · p-0.4pp cap117.0 net+188/med-0.5 |
| dead | (°▼i-18.8pp (0/7) · p+2.6pp cap62.0 net-92/med-3.5) | ▼i-17.1pp (2/36) · p-8.4pp cap240.1 net+545/med-0.6 |
| asia | (°▼i-19.4pp (1/18) · p-14.3pp cap140.0 net-424/med-20.4) | ▼i-14.7pp (8/100) · p+6.9pp cap86.5 net+1079/med+5.7 |

- backtest payoff: right +1006 / wrong -2790 / net -1784 pts; median per fire -23.75 (n=58)
- backtest best call: 2026-07-31 10:15 +476.0pts remaining (episode 521.8pts, major)
- backtest worst false alarm: 2026-07-29 13:54 -255.0pts adverse
- forward payoff: right +11902 / wrong -8437 / net +3465 pts; median per fire +2.00 (n=379)
- forward best call: 2026-10-14 07:22 +584.5pts remaining (episode 641.7pts, major)
- forward worst false alarm: 2026-10-20 13:41 -425.2pts adverse
- earliness (backtest): median 155.6 pts of move remaining at fire (n=5)

### H19 — 1 signal
*A probe-failure reversal signal followed by continued wide-loud effort in the anchor bar's own close direction within five bars is NOT the start of the claimed reversal — a SUPPRESSION/FADE configuration, and it says so.*
Grading: directional. Latest review: rows (recommendation).

- Question **Q1-H19**: see the register entry (status there is authoritative).
**S0-H19** — session × window grid (cells as in the matrix):

| session | backtest | forward |
|---|---|---|
| whole | ▼i-2.3pp (40/204) · p+0.9pp cap180.0 net+1513/med+6.5 | ·i-1.9pp (328/1683) · p-0.9pp cap108.2 net-10882/med-3.6 |
| london | ▼i-15.3pp (4/38) · p-2.1pp cap98.9 net-152/med+12.8 | ·i-0.6pp (91/378) · p-6.5pp cap96.6 net-2721/med-5.1 |
| overlap | (°▼i-7.9pp (0/20) · p+2.3pp cap185.4 net+387/med+17.1) | ·i+1.1pp (22/203) · p+3.4pp cap158.1 net-4684/med-15.6 |
| ny_only | ▼i-5.7pp (7/49) · p+25.9pp cap260.5 net+2978/med+38.3 | ·i+0.5pp (79/402) · p+2.6pp cap168.9 net-417/med-1.7 |
| dead | ·i-1.7pp (6/35) · p-6.0pp cap263.2 net-1043/med+14.8 | ▼i-2.4pp (42/207) · p+2.4pp cap90.7 net-980/med-2.7 |
| asia | ▲i+12.1pp (23/62) · p-8.6pp cap147.6 net-656/med-11.6 | ▼i-3.6pp (94/493) · p-0.6pp cap86.5 net-2080/med-3.2 |

- backtest payoff: right +10830 / wrong -9317 / net +1513 pts; median per fire +6.45 (n=204)
- backtest best call: 2026-07-30 06:41 +804.0pts remaining (episode 832.8pts, major)
- backtest worst false alarm: 2026-07-29 19:16 -700.8pts adverse
- forward payoff: right +54968 / wrong -65850 / net -10882 pts; median per fire -3.65 (n=1682)
- forward best call: 2026-11-04 06:22 +490.5pts remaining (episode 436.5pts, major)
- forward worst false alarm: 2026-11-05 14:52 -759.4pts adverse
- earliness (backtest): median 103.0 pts of move remaining at fire (n=16)

### H20 — 1 signal
*A wide-bar close-through of a session extreme (the same conditioned wide-bar class the retest anchor fires on; resolution = the close beyond the level, not a rejection back inside) initiates continuation in the break direction.*
Grading: directional. Latest review: rows (recommendation).

**S0-H20** — session × window grid (cells as in the matrix):

| session | backtest | forward |
|---|---|---|
| whole | ▼i-10.8pp (1/46) · p+8.7pp cap277.1 [cls 39.1%/13.0%i] net+1398/med+2.9 | ▼i-10.4pp (18/410) · p+1.5pp cap100.6 [cls 36.8%/14.8%i] net+2478/med+4.3 |
| london | (°▲i+13.1pp (1/3) · p-38.3pp cap— [cls 38.3%/20.2%i] net-182/med-90.2) | ▼i-15.7pp (7/128) · p+0.7pp cap72.1 [cls 34.5%/21.2%i] net+2078/med+13.4 |
| overlap | (°▼i-6.8pp (0/34) · p+17.3pp cap277.1 [cls 47.4%/6.8%i] net+1975/med+63.9) | ▼i-5.0pp (2/119) · p-3.1pp cap149.3 [cls 45.1%/6.7%i] net+654/med-15.0 |
| ny_only | (°▼i-9.2pp (0/2) · p-32.1pp cap— [cls 32.1%/9.2%i] net+16/med+7.9) | ▼i-2.2pp (3/36) · p+4.9pp cap143.4 [cls 25.7%/10.5%i] net+10/med-5.2 |
| dead | (°▼i-13.5pp (0/4) · p-23.0pp cap— [cls 23.0%/13.5%i] net-155/med-45.4) | ▼i-4.2pp (2/23) · p-2.4pp cap105.4 [cls 28.5%/12.9%i] net-1324/med-11.4 |
| asia | (°▼i-18.2pp (0/3) · p-25.2pp cap— [cls 25.2%/18.2%i] net-256/med-75.9) | ▼i-14.4pp (4/104) · p+10.2pp cap62.4 [cls 33.1%/18.2%i] net+1060/med+8.7 |

- backtest payoff: right +3786 / wrong -2388 / net +1398 pts; median per fire +2.90 (n=46)
- backtest best call: 2026-07-31 09:07 +2.0pts remaining (episode 98.0pts)
- backtest worst false alarm: 2026-07-31 13:34 -574.3pts adverse
- forward payoff: right +16368 / wrong -13890 / net +2478 pts; median per fire +4.30 (n=410)
- forward best call: 2026-10-16 16:03 +349.6pts remaining (episode 382.0pts, major)
- forward worst false alarm: 2026-11-05 15:53 -539.2pts adverse
- earliness (backtest): median 2.0 pts of move remaining at fire (n=1)


---

# us30 (us30fut) — CANONICAL

Store span (1M, close ts): 2026-07-19 22:02:00+00:00 → 2026-11-06 21:29:00+00:00. Volume type: real futures volume (register 40 first-sync sanity; canonical verdict at this instrument's validation evening).

## Summary Matrix (page 1)

Engine `66be26997` — OBSERVATIONAL signal scoreboard - move-detection, not trading; no fills exist here by construction; never validation (docs/hypothesis_lifecycle.md stage 4)

**Review labels are RECOMMENDATIONS — none actioned, review pending operator familiarity.** Cells: marker + precision LIFT vs that context's OWN chance rate, (hits/fires), payoff net/median points (directional rows; either-direction rows have no payoff by construction). ▲/▼ = beyond ±2pp of chance, · = within. (°…) = small-n (fires<20 or episodes<10): dimmed, excluded from any future label arithmetic. Read READING_GUIDE.md first; full detail in hypothesis_performance.json.

| H | label | backtest whole | backtest london | forward whole | forward london |
|---|---|---|---|---|---|
| *context* | | 107 ep; chance 24.1%dir/44.8%either | 35 ep; chance 36.9%dir/66.7%either | 582 ep; chance 25.2%dir/47.4%either | 163 ep; chance 36.6%dir/67.4%either |
| S0-H1 | keep-watching | ·i+1.8pp (11/49) · p+10.6pp cap154.0 net-83/med-8.0 | (°▲i+11.8pp (6/17) · p-1.6pp cap104.0 net-113/med-17.5) | ·i+1.5pp (167/758) · p+3.6pp cap104.5 net-4968/med+1.2 | ·i+1.4pp (62/263) · p-5.0pp cap113.0 net-3048/med-11.0 |
| S1-H1 | keep-watching | (°▼i-20.6pp (0/2) · p-24.1pp cap— net-18/med-9.2) | (°▼i-23.5pp (0/1) · p-36.9pp cap— net-50/med-50.0) | ▲i+10.8pp (21/67) · p+7.6pp cap101.8 net-826/med-24.1 | ▲i+14.5pp (11/30) · p-9.9pp cap121.5 net-1144/med-70.8 |
| S0-H2 | promote-candidate | ▼i-5.3pp (43/281) · p+2.6pp cap131.9 net-2432/med-4.0 | ·i+0.7pp (15/62) · p-1.4pp cap116.2 net-337/med-20.0 | ▼i-5.1pp (411/2676) · p+2.2pp cap109.5 net+23481/med+4.0 | ▼i-7.4pp (88/596) · p+2.8pp cap122.0 net+6988/med+5.2 |
| S1-H2 | promote-candidate | ▼i-3.3pp (38/220) · p+4.1pp cap133.2 net-505/med-2.8 | ▲i+2.5pp (13/50) · p+1.1pp cap119.0 net-218/med-18.0 | ▼i-3.6pp (330/1950) · p+1.1pp cap103.5 net+2675/med+1.0 | ▼i-3.8pp (75/407) · p+1.0pp cap119.5 net+2566/med-0.5 |
| S0-H3 | keep-watching | (°▲i+4.4pp (1/4) · p+0.9pp cap81.0 net+59/med+13.2) | (°▲i+26.5pp (1/2) · p-36.9pp cap— net-22/med-11.0) | ·i-1.4pp (9/47) · p+19.5pp cap84.0 net+1109/med+1.0 | (°▲i+4.5pp (4/15) · p+10.1pp cap102.0 net+49/med+1.0) |
| S0-H4 | keep-watching | (°▲i+17.9pp (5/13) · p+14.4pp cap83.0 net+194/med+15.0) | (°▼i-23.5pp (0/7) · p+34.5pp cap83.0 net+392/med+71.0) | — | — |
| S0-H5 | keep-watching | (°▼i-20.6pp (0/1) · p-24.1pp cap— net-135/med-135.0) | (°▼i-23.5pp (0/1) · p-36.9pp cap— net-135/med-135.0) | (°▼i-20.5pp (0/4) · p+49.8pp cap144.0 net+163/med+29.8) | (°▼i-22.2pp (0/3) · p+30.1pp cap179.5 net+136/med+32.5) |
| S0-H6 | keep-watching | ▼i-8.6pp (3/52) · p-21.7pp cap175.0 [cls 40.9%/14.4%i] net-1151/med-25.2 | ▼i-5.9pp (3/24) · p-29.3pp cap164.5 [cls 41.8%/18.4%i] net-664/med-30.0 | ▲i+3.8pp (86/492) · p-1.8pp cap123.0 [cls 41.0%/13.7%i] net+1883/med-3.0 | ▲i+2.0pp (43/228) · p-1.5pp cap117.8 [cls 41.0%/16.9%i] net+503/med-5.2 |
| S0-H7 | keep-watching | ▲i+8.7pp (12/41) · p-2.1pp cap111.0 net+205/med-9.0 | (°▲i+14.0pp (6/16) · p-5.7pp cap111.0 net-161/med-7.0) | ▲i+2.1pp (84/372) · p+1.4pp cap95.0 net-1817/med-1.2 | ·i+0.8pp (29/126) · p-5.6pp cap134.5 net-2328/med-25.5 |
| S0-H7 (either-dir) | keep-watching | ▲i+3.3pp (17/41) · p-3.3pp cap66.5 | (°▼i-5.6pp (6/16) · p+2.1pp cap60.5) | ▼i-7.0pp (117/372) · p+7.7pp cap40.5 | ▼i-12.1pp (38/126) · p+5.6pp cap35.9 |
| S0-H8 | keep-watching | ▼i-11.5pp (75/281) · p+8.2pp cap74.5 | ▼i-2.8pp (25/62) · p+9.1pp cap54.0 | ▼i-6.1pp (868/2676) · p+0.1pp cap60.8 | ▼i-7.1pp (210/596) · p-2.6pp cap79.0 |
| S0-H9 | keep-watching | ▼i-13.1pp (3/40) · p-1.6pp cap66.0 net-353/med-14.7 | (°▼i-23.5pp (0/3) · p-3.6pp cap52.0 net-198/med-61.5) | ▲i+2.5pp (94/409) · p-2.5pp cap89.0 net-2061/med-1.5 | ▲i+5.3pp (28/102) · p+3.6pp cap99.0 net-1038/med+12.8 |
| S1-H9 | keep-watching | (°▼i-20.6pp (0/9) · p-1.9pp cap273.0 net+460/med+1.5) | (°▼i-23.5pp (0/1) · p-36.9pp cap— net-38/med-38.0) | ▼i-15.0pp (6/109) · p-1.3pp cap142.8 net-136/med-4.0 | ▼i-13.1pp (3/33) · p-0.2pp cap142.8 net-192/med-5.5 |
| S0-H10 | deprioritize | ·i-1.1pp (30/154) · p-0.1pp cap71.0 net+1774/med+11.0 | ▼i-18.5pp (2/40) · p+3.1pp cap116.0 net+1480/med+27.5 | ▼i-3.1pp (302/1732) · p-0.1pp cap71.5 net+4891/med+2.5 | ▼i-4.1pp (80/441) · p+3.5pp cap97.0 net+2324/med+3.0 |
| S0-H11 | keep-watching | ·i+0.0pp (85/413) · p+3.3pp cap98.0 net+1254/med+3.0 | ▼i-5.1pp (30/163) · p+0.5pp cap91.0 net-404/med+5.0 | ▼i-4.0pp (388/2357) · p+1.2pp cap98.5 net+14768/med+2.0 | ▼i-6.9pp (100/655) · p+4.6pp cap101.5 net+5349/med+6.0 |
| S1-H11 | keep-watching | ▲i+6.4pp (51/189) · p+0.8pp cap167.0 net+1560/med+0.5 | (°▼i-14.4pp (1/11) · p+8.6pp cap194.5 net+136/med-24.5) | ▼i-4.5pp (446/2786) · p+3.6pp cap89.5 net+5437/med+1.5 | ▼i-3.7pp (202/1093) · p+1.5pp cap99.0 net+7261/med+8.0 |
| S0-H12 | keep-watching | — | — | (°▼i-20.5pp (0/1) · p-25.2pp cap— net+20/med+19.9) | (°▼i-22.2pp (0/1) · p-36.6pp cap— net+20/med+19.9) |
| S0-H13 | keep-watching | (°▲i+79.4pp (1/1) · p-24.1pp cap— net-206/med-206.0) | (°▲i+76.5pp (1/1) · p-36.9pp cap— net-206/med-206.0) | ▼i-11.0pp (2/21) · p+3.4pp cap149.8 net+273/med+3.0 | (°▼i-11.1pp (1/9) · p-3.3pp cap174.5 net+181/med-34.0) |
| S0-H14 | keep-watching | ▲i+4.4pp (37/148) · p+2.3pp cap76.0 net+2606/med+12.5 | ▼i-17.1pp (3/47) · p+12.0pp cap106.0 net+1414/med+12.5 | ▼i-5.0pp (248/1598) · p+2.5pp cap74.5 net+8816/med+1.5 | ▼i-6.6pp (64/410) · p+8.3pp cap97.0 net+4029/med+4.5 |
| S0-H15 | keep-watching | — | — | — | — |
| S0-H16 | keep-watching | (°▼i-20.6pp (0/10) · p+35.9pp cap98.2 net+522/med+37.5) | — | ▼i-12.3pp (5/61) · p-2.2pp cap102.0 net+600/med+12.5 | — |
| S0-H17 | rows | ▲i+2.5pp (6/26) · p+2.8pp cap119.5 net-167/med-10.5 | (°▲i+16.5pp (4/10) · p-6.9pp cap157.5 net+113/med+12.2) | ▲i+4.9pp (97/382) · p+0.7pp cap91.5 net-1038/med+1.0 | ▲i+6.2pp (38/134) · p-9.0pp cap115.0 net-1005/med-12.2 |
| S0-H18 | rows | ▲i+3.3pp (16/67) · p+2.8pp cap102.5 net+355/med+2.5 | ·i+1.5pp (7/28) · p+2.4pp cap87.5 net+681/med+46.2 | ▼i-5.9pp (56/383) · p+0.4pp cap110.8 net+981/med+0.5 | ▼i-8.0pp (15/106) · p+9.6pp cap90.5 net+356/med+9.5 |
| S0-H19 | rows | ▼i-10.7pp (17/172) · p+10.2pp cap130.0 net+2236/med+3.2 | ▼i-4.7pp (6/32) · p+6.9pp cap135.5 net+708/med+34.0 | ▼i-2.5pp (322/1786) · p-1.9pp cap110.0 net-16318/med-4.8 | ·i-0.3pp (80/365) · p-5.9pp cap115.7 net-3908/med-3.5 |
| S0-H20 | rows | ▼i-11.0pp (2/58) · p-13.3pp cap111.8 [cls 40.9%/14.4%i] net+27/med+18.2 | ▼i-13.0pp (2/37) · p-17.5pp cap87.5 [cls 41.8%/18.4%i] net-532/med+4.5 | ▼i-11.3pp (11/460) · p+1.2pp cap124.8 [cls 41.0%/13.7%i] net-2361/med-4.5 | ▼i-14.1pp (7/247) · p+10.0pp cap121.2 [cls 41.0%/16.9%i] net+1771/med+19.5 |
| **union coverage** | | 42.1% (45/107) | 40.0% (14/35) | 89.5% (521/582) | 91.4% (149/163) |

Not graded:  — see register entries.

## Hypothesis Cards (page 2)

### H1 — 2 signals
*A climactic bar — extreme volume on a wide spread late in an extended move — marks exhaustion, and price then reverses against the climax direction.*
Grading: directional. Latest review: keep-watching (recommendation).

- Question **Q1-H1**: see the register entry (status there is authoritative).
**S0-H1** — session × window grid (cells as in the matrix):

| session | backtest | forward |
|---|---|---|
| whole | ·i+1.8pp (11/49) · p+10.6pp cap154.0 net-83/med-8.0 | ·i+1.5pp (167/758) · p+3.6pp cap104.5 net-4968/med+1.2 |
| london | (°▲i+11.8pp (6/17) · p-1.6pp cap104.0 net-113/med-17.5) | ·i+1.4pp (62/263) · p-5.0pp cap113.0 net-3048/med-11.0 |
| overlap | — | ·i+1.1pp (4/34) · p-9.8pp cap186.5 net-1430/med-50.5 |
| ny_only | (°▼i-3.8pp (2/13) · p+40.3pp cap253.5 net-62/med-15.5) | ▼i-2.4pp (21/138) · p+11.8pp cap180.0 net-387/med+5.8 |
| dead | (°▲i+28.3pp (3/7) · p-7.2pp cap— net-157/med-8.0) | ▲i+3.9pp (24/96) · p+12.2pp cap83.6 net+499/med+6.5 |
| asia | (°▼i-24.7pp (0/12) · p+9.5pp cap91.2 net+248/med+27.0) | ·i+1.3pp (56/227) · p+4.9pp cap68.0 net-601/med+3.0 |

- backtest payoff: right +1958 / wrong -2041 / net -83 pts; median per fire -8.00 (n=49)
- backtest best call: 2026-07-29 16:24 +398.0pts remaining (episode 602.0pts, major)
- backtest worst false alarm: 2026-07-29 19:22 -450.0pts adverse
- forward payoff: right +24810 / wrong -29778 / net -4968 pts; median per fire +1.25 (n=758)
- forward best call: 2026-11-04 03:01 +2020.5pts remaining (episode 2016.0pts, major)
- forward worst false alarm: 2026-09-16 18:27 -808.1pts adverse
- earliness (backtest): median 128.0 pts of move remaining at fire (n=10)

**S1-H1** — session × window grid (cells as in the matrix):

| session | backtest | forward |
|---|---|---|
| whole | (°▼i-20.6pp (0/2) · p-24.1pp cap— net-18/med-9.2) | ▲i+10.8pp (21/67) · p+7.6pp cap101.8 net-826/med-24.1 |
| london | (°▼i-23.5pp (0/1) · p-36.9pp cap— net-50/med-50.0) | ▲i+14.5pp (11/30) · p-9.9pp cap121.5 net-1144/med-70.8 |
| overlap | — | (°▲i+39.3pp (3/6) · p+2.9pp cap257.0 net-380/med-77.8) |
| ny_only | — | (°▼i-5.1pp (1/8) · p+37.9pp cap202.0 net+676/med+40.5) |
| dead | — | (°▼i-10.0pp (1/9) · p+25.7pp cap59.5 net+10/med+30.5) |
| asia | (°▼i-24.7pp (0/1) · p-23.8pp cap— net+32/med+31.5) | (°▲i+12.3pp (5/14) · p+7.1pp cap68.5 net+10/med+8.2) |

- backtest payoff: right +32 / wrong -50 / net -18 pts; median per fire -9.25 (n=2)
- backtest worst false alarm: 2026-07-29 12:17 -67.0pts adverse
- forward payoff: right +2159 / wrong -2985 / net -826 pts; median per fire -24.10 (n=67)
- forward best call: 2026-09-03 09:59 +663.5pts remaining (episode 664.0pts, major)
- forward worst false alarm: 2026-11-05 15:47 -268.0pts adverse

### H2 — 2 signals
*A failed probe beyond a prior extreme — an upthrust above or spring below that closes back inside — reverses against the probe.*
Grading: directional. Latest review: promote-candidate (recommendation).

**S0-H2** — session × window grid (cells as in the matrix):

| session | backtest | forward |
|---|---|---|
| whole | ▼i-5.3pp (43/281) · p+2.6pp cap131.9 net-2432/med-4.0 | ▼i-5.1pp (411/2676) · p+2.2pp cap109.5 net+23481/med+4.0 |
| london | ·i+0.7pp (15/62) · p-1.4pp cap116.2 net-337/med-20.0 | ▼i-7.4pp (88/596) · p+2.8pp cap122.0 net+6988/med+5.2 |
| overlap | (°▼i-9.1pp (0/22) · p+8.0pp cap172.5 net-1080/med-77.8) | ▼i-7.1pp (8/220) · p+1.0pp cap199.0 net+5202/med+18.2 |
| ny_only | ▼i-15.9pp (2/60) · p+23.2pp cap224.8 net-1257/med-11.1 | ▼i-6.7pp (57/521) · p+5.6pp cap205.5 net+2681/med-1.0 |
| dead | ·i+0.0pp (6/41) · p+2.6pp cap100.8 net-18/med-2.6 | ▼i-4.4pp (67/401) · p+1.9pp cap79.8 net+3027/med+4.5 |
| asia | ▼i-3.9pp (20/96) · p-5.0pp cap82.5 net+261/med+1.2 | ▼i-3.0pp (191/938) · p+3.3pp cap74.0 net+5584/med+3.8 |

- backtest payoff: right +10496 / wrong -12928 / net -2432 pts; median per fire -4.00 (n=281)
- backtest best call: 2026-07-29 10:42 +781.0pts remaining (episode 752.0pts, major)
- backtest worst false alarm: 2026-07-29 18:55 -695.0pts adverse
- forward payoff: right +106202 / wrong -82721 / net +23481 pts; median per fire +4.00 (n=2674)
- forward best call: 2026-11-04 02:58 +1969.0pts remaining (episode 2016.0pts, major)
- forward worst false alarm: 2026-11-05 14:37 -1106.0pts adverse
- earliness (backtest): median 105.2 pts of move remaining at fire (n=24)

**S1-H2** — session × window grid (cells as in the matrix):

| session | backtest | forward |
|---|---|---|
| whole | ▼i-3.3pp (38/220) · p+4.1pp cap133.2 net-505/med-2.8 | ▼i-3.6pp (330/1950) · p+1.1pp cap103.5 net+2675/med+1.0 |
| london | ▲i+2.5pp (13/50) · p+1.1pp cap119.0 net-218/med-18.0 | ▼i-3.8pp (75/407) · p+1.0pp cap119.5 net+2566/med-0.5 |
| overlap | (°▼i-9.1pp (0/17) · p+2.4pp cap151.5 net-983/med-92.0) | ▼i-5.7pp (8/160) · p-3.5pp cap188.0 net-3118/med+5.0 |
| ny_only | ▼i-14.3pp (2/41) · p+32.8pp cap239.5 net+169/med-15.0 | ▼i-5.7pp (46/385) · p+4.5pp cap187.5 net-1484/med-3.0 |
| dead | ▲i+4.8pp (6/31) · p+2.5pp cap99.5 net-162/med-5.0 | ▼i-5.2pp (46/290) · p+1.0pp cap85.5 net+1463/med+1.0 |
| asia | ▼i-3.7pp (17/81) · p-5.3pp cap83.0 net+689/med+6.0 | ·i-1.5pp (155/708) · p+3.6pp cap73.2 net+3249/med+3.5 |

- backtest payoff: right +8589 / wrong -9094 / net -505 pts; median per fire -2.80 (n=220)
- backtest best call: 2026-07-29 10:42 +781.0pts remaining (episode 752.0pts, major)
- backtest worst false alarm: 2026-07-29 18:55 -695.0pts adverse
- forward payoff: right +67404 / wrong -64729 / net +2675 pts; median per fire +1.00 (n=1948)
- forward best call: 2026-11-04 02:58 +1969.0pts remaining (episode 2016.0pts, major)
- forward worst false alarm: 2026-11-05 14:37 -1106.0pts adverse
- earliness (backtest): median 106.0 pts of move remaining at fire (n=23)

### H3 — 1 signal
*Repeated absorption — high effort with no result — at a price level precedes a breakout through that level.*
Grading: directional. Latest review: keep-watching (recommendation).

**S0-H3** — session × window grid (cells as in the matrix):

| session | backtest | forward |
|---|---|---|
| whole | (°▲i+4.4pp (1/4) · p+0.9pp cap81.0 net+59/med+13.2) | ·i-1.4pp (9/47) · p+19.5pp cap84.0 net+1109/med+1.0 |
| london | (°▲i+26.5pp (1/2) · p-36.9pp cap— net-22/med-11.0) | (°▲i+4.5pp (4/15) · p+10.1pp cap102.0 net+49/med+1.0) |
| overlap | — | (°▼i-10.7pp (0/4) · p+69.6pp cap200.0 net+684/med+174.2) |
| ny_only | — | (°·i-0.9pp (1/6) · p+37.9pp cap165.5 net+418/med+49.2) |
| dead | — | (°▼i-21.1pp (0/2) · p-7.6pp cap— net+9/med+4.5) |
| asia | (°▼i-24.7pp (0/2) · p+26.2pp cap81.0 net+81/med+40.5) | ▼i-3.4pp (4/20) · p+6.4pp cap57.0 net-50/med-4.5 |

- backtest payoff: right +99 / wrong -40 / net +59 pts; median per fire +13.25 (n=4)
- backtest best call: 2026-07-30 09:10 +122.0pts remaining (episode 205.5pts)
- backtest worst false alarm: 2026-07-30 09:10 -83.5pts adverse
- forward payoff: right +1848 / wrong -738 / net +1109 pts; median per fire +1.00 (n=47)
- forward best call: 2026-10-22 12:09 +366.5pts remaining (episode 353.0pts, major)
- forward worst false alarm: 2026-10-22 15:39 -190.0pts adverse
- earliness (backtest): median 122.0 pts of move remaining at fire (n=1)

### H4 — 1 signal
*In an established trend, a quiet (low-volume) pullback resolves with trend resumption.*
Grading: directional. Latest review: keep-watching (recommendation).

**S0-H4** — session × window grid (cells as in the matrix):

| session | backtest | forward |
|---|---|---|
| whole | (°▲i+17.9pp (5/13) · p+14.4pp cap83.0 net+194/med+15.0) | — |
| london | (°▼i-23.5pp (0/7) · p+34.5pp cap83.0 net+392/med+71.0) | — |
| overlap | (°▼i-9.1pp (0/1) · p-32.9pp cap— net-166/med-165.5) | — |
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
| whole | (°▼i-20.6pp (0/1) · p-24.1pp cap— net-135/med-135.0) | (°▼i-20.5pp (0/4) · p+49.8pp cap144.0 net+163/med+29.8) |
| london | (°▼i-23.5pp (0/1) · p-36.9pp cap— net-135/med-135.0) | (°▼i-22.2pp (0/3) · p+30.1pp cap179.5 net+136/med+32.5) |
| overlap | — | — |
| ny_only | — | — |
| dead | — | — |
| asia | — | (°▼i-23.4pp (0/1) · p+71.4pp cap61.0 net+27/med+27.0) |

- backtest payoff: right +0 / wrong -135 / net -135 pts; median per fire -135.00 (n=1)
- backtest worst false alarm: 2026-07-28 11:30 -135.0pts adverse
- forward payoff: right +163 / wrong +0 / net +163 pts; median per fire +29.75 (n=4)
- forward worst false alarm: 2026-10-27 11:00 +10.0pts adverse

### H6 — 1 signal
*A wide-spread rejection bar at a session extreme (measured day-relative, volume-agnostic) reverses away from the extreme.*
Grading: directional. Latest review: keep-watching (recommendation).

- Question **Q1-H6**: see the register entry (status there is authoritative).
- Question **Q2-H6**: see the register entry (status there is authoritative).
- Question **Q3-H6**: see the register entry (status there is authoritative).
**S0-H6** — session × window grid (cells as in the matrix):

| session | backtest | forward |
|---|---|---|
| whole | ▼i-8.6pp (3/52) · p-21.7pp cap175.0 [cls 40.9%/14.4%i] net-1151/med-25.2 | ▲i+3.8pp (86/492) · p-1.8pp cap123.0 [cls 41.0%/13.7%i] net+1883/med-3.0 |
| london | ▼i-5.9pp (3/24) · p-29.3pp cap164.5 [cls 41.8%/18.4%i] net-664/med-30.0 | ▲i+2.0pp (43/228) · p-1.5pp cap117.8 [cls 41.0%/16.9%i] net+503/med-5.2 |
| overlap | (°▼i-7.9pp (0/18) · p-19.0pp cap195.5 [cls 41.2%/7.9%i] net+234/med+6.8) | ▲i+7.5pp (26/179) · p-1.9pp cap157.2 [cls 42.1%/7.0%i] net+1985/med-2.5 |
| ny_only | (°▼i-5.4pp (0/6) · p+7.7pp cap329.0 [cls 42.3%/5.4%i] net-856/med-92.0) | (°▲i+4.8pp (2/13) · p-1.0pp cap116.0 [cls 24.1%/10.6%i] net-240/med-11.0) |
| dead | (°▼i-7.4pp (0/3) · p-11.8pp cap— [cls 11.8%/7.4%i] net+58/med+5.5) | (°·i-0.2pp (1/10) · p+9.0pp cap170.7 [cls 11.0%/10.2%i] net+362/med+20.4) |
| asia | (°▼i-20.2pp (0/1) · p-39.6pp cap— [cls 39.6%/20.2%i] net+77/med+77.0) | ▲i+7.5pp (14/62) · p-4.8pp cap73.0 [cls 46.7%/15.1%i] net-726/med-3.2 |

- backtest payoff: right +1398 / wrong -2549 / net -1151 pts; median per fire -25.25 (n=52)
- backtest best call: 2026-07-28 12:23 +197.5pts remaining (episode 226.5pts, major)
- backtest worst false alarm: 2026-07-28 15:11 -288.5pts adverse
- forward payoff: right +23533 / wrong -21650 / net +1883 pts; median per fire -3.00 (n=490)
- forward best call: 2026-10-13 12:23 +568.0pts remaining (episode 692.5pts, major)
- forward worst false alarm: 2026-10-20 13:42 -407.0pts adverse
- earliness (backtest): median 27.5 pts of move remaining at fire (n=3)

### H7 — 1 signal
*Quiet decline at a session extreme is disguised accumulation: effortless (low-volume) weakness reverses UP once selling fails to attract participation (mirror: quiet advance at a high reverses down).*
Grading: directional + either-direction (dual). Latest review: keep-watching (recommendation).

- Question **Q1-H7**: see the register entry (status there is authoritative).
**S0-H7** — session × window grid (cells as in the matrix):

| session | backtest | forward |
|---|---|---|
| whole | ▲i+8.7pp (12/41) · p-2.1pp cap111.0 net+205/med-9.0 | ▲i+2.1pp (84/372) · p+1.4pp cap95.0 net-1817/med-1.2 |
| london | (°▲i+14.0pp (6/16) · p-5.7pp cap111.0 net-161/med-7.0) | ·i+0.8pp (29/126) · p-5.6pp cap134.5 net-2328/med-25.5 |
| overlap | (°▼i-9.1pp (0/3) · p+33.8pp cap287.0 net+471/med+272.0) | ▲i+5.6pp (8/49) · p+4.3pp cap159.0 net-891/med-13.5 |
| ny_only | (°▼i-19.2pp (0/4) · p-13.5pp cap— net-21/med-5.0) | ·i+0.4pp (11/61) · p-7.2pp cap109.0 net+1126/med+26.0 |
| dead | (°▲i+10.4pp (1/4) · p-7.2pp cap— net-1/med-2.0) | ▼i-2.6pp (5/27) · p+7.2pp cap83.8 net+191/med+8.5 |
| asia | (°▲i+11.0pp (5/14) · p-9.5pp cap76.0 net-84/med-13.8) | ▲i+5.0pp (31/109) · p+4.4pp cap54.8 net+84/med+0.0 |

- backtest payoff: right +1609 / wrong -1404 / net +205 pts; median per fire -9.00 (n=41)
- backtest best call: 2026-07-31 09:51 +528.0pts remaining (episode 569.0pts, major)
- backtest worst false alarm: 2026-07-28 10:48 -242.0pts adverse
- forward payoff: right +12115 / wrong -13932 / net -1817 pts; median per fire -1.25 (n=372)
- forward best call: 2026-10-23 05:42 +705.0pts remaining (episode 714.0pts, major)
- forward worst false alarm: 2026-11-05 15:33 -596.0pts adverse
- earliness (backtest): median 97.8 pts of move remaining at fire (n=10)

**S0-H7 (either-dir)** — session × window grid (cells as in the matrix):

| session | backtest | forward |
|---|---|---|
| whole | ▲i+3.3pp (17/41) · p-3.3pp cap66.5 | ▼i-7.0pp (117/372) · p+7.7pp cap40.5 |
| london | (°▼i-5.6pp (6/16) · p+2.1pp cap60.5) | ▼i-12.1pp (38/126) · p+5.6pp cap35.9 |
| overlap | (°▼i-18.3pp (0/3) · p+5.9pp cap287.0) | ·i-1.0pp (10/49) · p+8.3pp cap98.2 |
| ny_only | (°▼i-10.3pp (1/4) · p-26.1pp cap—) | ▼i-5.4pp (17/61) · p-10.4pp cap35.8 |
| dead | (°▲i+21.4pp (2/4) · p-14.4pp cap—) | ·i-0.8pp (10/27) · p+7.3pp cap61.0 |
| asia | (°▲i+11.6pp (8/14) · p-16.6pp cap37.0) | ▼i-5.0pp (42/109) · p+7.5pp cap36.0 |

- backtest payoff: n/a by construction (either-direction)
- backtest best call: 2026-07-31 09:51 +528.0pts remaining (episode 569.0pts, major)
- backtest worst false alarm: 2026-07-30 16:13 -170.0pts adverse
- forward payoff: n/a by construction (either-direction)
- forward best call: 2026-10-23 05:42 +705.0pts remaining (episode 714.0pts, major)
- forward worst false alarm: 2026-10-29 11:30 -141.5pts adverse
- earliness (backtest): median 84.8 pts of move remaining at fire (n=12)

### H8 — 1 signal
*Reversal-signature bar anatomy (upthrust/spring) predicts imminent range expansion irrespective of direction.*
Grading: either-direction. Latest review: keep-watching (recommendation).

**S0-H8** — session × window grid (cells as in the matrix):

| session | backtest | forward |
|---|---|---|
| whole | ▼i-11.5pp (75/281) · p+8.2pp cap74.5 | ▼i-6.1pp (868/2676) · p+0.1pp cap60.8 |
| london | ▼i-2.8pp (25/62) · p+9.1pp cap54.0 | ▼i-7.1pp (210/596) · p-2.6pp cap79.0 |
| overlap | (°▼i-18.3pp (0/22) · p+21.0pp cap114.2) | ▼i-10.9pp (23/220) · p+3.0pp cap129.5 |
| ny_only | ▼i-27.0pp (5/60) · p+37.2pp cap154.5 | ▼i-8.5pp (129/521) · p+7.2pp cap124.2 |
| dead | ▼i-11.5pp (7/41) · p+10.0pp cap10.5 | ▼i-5.9pp (128/401) · p+2.3pp cap52.5 |
| asia | ▼i-5.9pp (38/96) · p-7.7pp cap47.2 | ▼i-3.2pp (378/938) · p+1.8pp cap45.5 |

- backtest payoff: n/a by construction (either-direction)
- backtest best call: 2026-07-29 10:42 +781.0pts remaining (episode 752.0pts, major)
- backtest worst false alarm: 2026-07-27 16:47 -152.0pts adverse
- forward payoff: n/a by construction (either-direction)
- forward best call: 2026-11-04 02:58 +1969.0pts remaining (episode 2016.0pts, major)
- forward worst false alarm: 2026-11-05 17:25 -356.0pts adverse
- earliness (backtest): median 100.5 pts of move remaining at fire (n=27)

### H9 — 2 signals
*Persistent lower-TF directional pressure that recruits expanding participation at the parent timeframe precedes continuation beyond what the parent label alone predicts; pressure without participation expansion does not.*
Grading: directional. Latest review: keep-watching (recommendation).

- Question **Q2-H9**: see the register entry (status there is authoritative).
**S0-H9** — session × window grid (cells as in the matrix):

| session | backtest | forward |
|---|---|---|
| whole | ▼i-13.1pp (3/40) · p-1.6pp cap66.0 net-353/med-14.7 | ▲i+2.5pp (94/409) · p-2.5pp cap89.0 net-2061/med-1.5 |
| london | (°▼i-23.5pp (0/3) · p-3.6pp cap52.0 net-198/med-61.5) | ▲i+5.3pp (28/102) · p+3.6pp cap99.0 net-1038/med+12.8 |
| overlap | (°▼i-9.1pp (0/2) · p-32.9pp cap— net-19/med-9.5) | ▲i+15.5pp (11/42) · p-18.5pp cap176.0 net-832/med-34.5 |
| ny_only | (°▼i-9.2pp (1/10) · p-3.5pp cap464.5 net-196/med-66.5) | ▲i+2.2pp (20/101) · p-4.2pp cap150.5 net-604/med-12.5 |
| dead | (°▼i-14.6pp (0/7) · p-7.2pp cap— net+60/med+15.5) | ▲i+4.6pp (9/35) · p-4.7pp cap88.0 net-49/med-5.5 |
| asia | (°▼i-13.6pp (2/18) · p+15.1pp cap66.0 net-1/med-11.2) | ▼i-3.2pp (26/129) · p+0.9pp cap51.0 net+464/med+1.5 |

- backtest payoff: right +876 / wrong -1229 / net -353 pts; median per fire -14.70 (n=38)
- backtest best call: 2026-08-03 05:40 +463.0pts remaining (episode 472.0pts, major)
- backtest worst false alarm: 2026-08-03 17:15 -176.0pts adverse
- forward payoff: right +10573 / wrong -12634 / net -2061 pts; median per fire -1.50 (n=405)
- forward best call: 2026-10-13 11:55 +516.0pts remaining (episode 692.5pts, major)
- forward worst false alarm: 2026-11-05 14:00 -787.0pts adverse
- earliness (backtest): median 351.5 pts of move remaining at fire (n=2)

**S1-H9** — session × window grid (cells as in the matrix):

| session | backtest | forward |
|---|---|---|
| whole | (°▼i-20.6pp (0/9) · p-1.9pp cap273.0 net+460/med+1.5) | ▼i-15.0pp (6/109) · p-1.3pp cap142.8 net-136/med-4.0 |
| london | (°▼i-23.5pp (0/1) · p-36.9pp cap— net-38/med-38.0) | ▼i-13.1pp (3/33) · p-0.2pp cap142.8 net-192/med-5.5 |
| overlap | — | (°▼i-10.7pp (0/4) · p-30.4pp cap— net-481/med-106.8) |
| ny_only | (°▼i-19.2pp (0/4) · p+11.5pp cap464.5 net+421/med+15.3) | ▼i-7.6pp (3/30) · p+4.6pp cap150.5 net+279/med-8.5 |
| dead | — | (°▼i-21.1pp (0/8) · p+4.9pp cap88.0 net+25/med+14.5) |
| asia | (°▼i-24.7pp (0/4) · p+1.2pp cap81.5 net+76/med+12.8) | ▼i-23.4pp (0/34) · p-5.1pp cap70.5 net+232/med+6.5 |

- backtest payoff: right +601 / wrong -141 / net +460 pts; median per fire +1.50 (n=9)
- backtest worst false alarm: 2026-07-27 16:10 -84.0pts adverse
- forward payoff: right +4103 / wrong -4239 / net -136 pts; median per fire -4.00 (n=109)
- forward best call: 2026-10-14 16:15 +153.0pts remaining (episode 165.5pts)
- forward worst false alarm: 2026-10-29 09:45 -427.0pts adverse

### H10 — 1 signal
*In an established 1-minute trend, no-demand/no-supply prints in the trend's direction signal continuation.*
Grading: directional. Latest review: deprioritize (recommendation).

**S0-H10** — session × window grid (cells as in the matrix):

| session | backtest | forward |
|---|---|---|
| whole | ·i-1.1pp (30/154) · p-0.1pp cap71.0 net+1774/med+11.0 | ▼i-3.1pp (302/1732) · p-0.1pp cap71.5 net+4891/med+2.5 |
| london | ▼i-18.5pp (2/40) · p+3.1pp cap116.0 net+1480/med+27.5 | ▼i-4.1pp (80/441) · p+3.5pp cap97.0 net+2324/med+3.0 |
| overlap | (°▼i-9.1pp (0/5) · p-32.9pp cap— net+36/med+33.0) | ·i+0.4pp (12/108) · p-2.6pp cap122.5 net+304/med+2.2 |
| ny_only | ▼i-3.8pp (4/26) · p+1.9pp cap80.9 net-348/med+48.8 | ▲i+4.4pp (86/391) · p-1.4pp cap90.2 net+2163/med+9.0 |
| dead | ▲i+15.4pp (6/20) · p-7.2pp cap— net-74/med-5.7 | ▼i-8.0pp (26/199) · p-3.6pp cap46.0 net-640/med-1.5 |
| asia | ▲i+3.9pp (18/63) · p+3.2pp cap50.5 net+680/med+8.0 | ▼i-6.9pp (98/593) · p+1.2pp cap47.0 net+740/med+1.5 |

- backtest payoff: right +4228 / wrong -2454 / net +1774 pts; median per fire +11.00 (n=154)
- backtest best call: 2026-07-31 10:20 +555.5pts remaining (episode 569.0pts, major)
- backtest worst false alarm: 2026-08-03 17:10 -197.0pts adverse
- forward payoff: right +39840 / wrong -34949 / net +4891 pts; median per fire +2.50 (n=1730)
- forward best call: 2026-11-05 12:40 +2057.0pts remaining (episode 2148.0pts, major)
- forward worst false alarm: 2026-09-17 12:42 -416.5pts adverse
- earliness (backtest): median 87.5 pts of move remaining at fire (n=11)

### H11 — 2 signals
*Price entering a low-volume price zone traverses it faster than baseline; entering a high-volume node it stalls or reverses at above-baseline rates.*
Grading: directional. Latest review: keep-watching (recommendation).

- Question **Q1-H11**: see the register entry (status there is authoritative).
- Question **Q2-H11**: see the register entry (status there is authoritative).
**S0-H11** — session × window grid (cells as in the matrix):

| session | backtest | forward |
|---|---|---|
| whole | ·i+0.0pp (85/413) · p+3.3pp cap98.0 net+1254/med+3.0 | ▼i-4.0pp (388/2357) · p+1.2pp cap98.5 net+14768/med+2.0 |
| london | ▼i-5.1pp (30/163) · p+0.5pp cap91.0 net-404/med+5.0 | ▼i-6.9pp (100/655) · p+4.6pp cap101.5 net+5349/med+6.0 |
| overlap | (°▼i-5.3pp (1/26) · p+20.9pp cap261.2 net+491/med+4.0) | ▼i-3.8pp (15/217) · p+1.9pp cap180.8 net+4010/med+9.0 |
| ny_only | ▲i+7.0pp (11/42) · p-1.6pp cap239.5 net+1037/med+15.2 | ·i-1.3pp (95/584) · p+1.3pp cap129.5 net+1864/med+2.0 |
| dead | ▼i-6.6pp (4/50) · p+14.8pp cap99.5 net+478/med+1.2 | ▼i-2.5pp (51/274) · p+1.2pp cap81.5 net+232/med-1.5 |
| asia | ▲i+4.8pp (39/132) · p-7.1pp cap62.5 net-348/med+2.0 | ▼i-3.1pp (127/627) · p+0.3pp cap62.5 net+3312/med+2.0 |

- backtest payoff: right +12694 / wrong -11440 / net +1254 pts; median per fire +3.00 (n=413)
- backtest best call: 2026-07-31 09:39 +496.0pts remaining (episode 569.0pts, major)
- backtest worst false alarm: 2026-07-31 13:24 -492.5pts adverse
- forward payoff: right +76098 / wrong -61330 / net +14768 pts; median per fire +2.00 (n=2356)
- forward best call: 2026-09-03 09:58 +643.5pts remaining (episode 664.0pts, major)
- forward worst false alarm: 2026-11-05 15:23 -681.0pts adverse
- earliness (backtest): median 90.5 pts of move remaining at fire (n=23)

**S1-H11** — session × window grid (cells as in the matrix):

| session | backtest | forward |
|---|---|---|
| whole | ▲i+6.4pp (51/189) · p+0.8pp cap167.0 net+1560/med+0.5 | ▼i-4.5pp (446/2786) · p+3.6pp cap89.5 net+5437/med+1.5 |
| london | (°▼i-14.4pp (1/11) · p+8.6pp cap194.5 net+136/med-24.5) | ▼i-3.7pp (202/1093) · p+1.5pp cap99.0 net+7261/med+8.0 |
| overlap | (°▲i+25.4pp (10/29) · p+11.9pp cap250.5 net+278/med+23.0) | ▼i-2.1pp (29/339) · p-2.1pp cap145.0 net-2330/med-11.0 |
| ny_only | ▼i-4.3pp (7/47) · p+14.2pp cap181.4 net+1460/med+17.0 | ▼i-3.3pp (58/407) · p-4.0pp cap129.5 net-1710/med-6.5 |
| dead | ▲i+26.3pp (9/22) · p+11.0pp cap86.0 net+232/med+18.2 | ▼i-8.4pp (31/244) · p+4.7pp cap81.5 net+810/med+0.0 |
| asia | ▲i+5.3pp (24/80) · p-8.8pp cap66.2 net-546/med-6.2 | ▼i-5.5pp (126/703) · p+3.5pp cap59.0 net+1406/med+2.0 |

- backtest payoff: right +9216 / wrong -7657 / net +1560 pts; median per fire +0.50 (n=189)
- backtest best call: 2026-07-28 04:46 +523.0pts remaining (episode 543.0pts, major)
- backtest worst false alarm: 2026-07-29 18:58 -665.0pts adverse
- forward payoff: right +83202 / wrong -77765 / net +5437 pts; median per fire +1.50 (n=2782)
- forward best call: 2026-10-30 10:10 +814.5pts remaining (episode 896.0pts, major)
- forward worst false alarm: 2026-10-20 13:02 -489.0pts adverse
- earliness (backtest): median 97.5 pts of move remaining at fire (n=8)

### H12 — 1 signal
*A zone showing repeated visits with elevated volume, diminishing range-per-unit-volume, and drying pullback volume precedes a directional move away from the zone in the absorber's direction.*
Grading: directional. Latest review: keep-watching (recommendation).

**S0-H12** — session × window grid (cells as in the matrix):

| session | backtest | forward |
|---|---|---|
| whole | — | (°▼i-20.5pp (0/1) · p-25.2pp cap— net+20/med+19.9) |
| london | — | (°▼i-22.2pp (0/1) · p-36.6pp cap— net+20/med+19.9) |
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
| whole | (°▲i+79.4pp (1/1) · p-24.1pp cap— net-206/med-206.0) | ▼i-11.0pp (2/21) · p+3.4pp cap149.8 net+273/med+3.0 |
| london | (°▲i+76.5pp (1/1) · p-36.9pp cap— net-206/med-206.0) | (°▼i-11.1pp (1/9) · p-3.3pp cap174.5 net+181/med-34.0) |
| overlap | — | (°▼i-10.7pp (0/3) · p+2.9pp cap177.5 net-75/med-27.0) |
| ny_only | — | (°▲i+7.4pp (1/4) · p+12.9pp cap125.0 net+140/med+27.8) |
| dead | — | — |
| asia | — | (°▼i-23.4pp (0/5) · p-8.6pp cap47.0 net+28/med+12.0) |

- backtest payoff: right +0 / wrong -206 / net -206 pts; median per fire -206.00 (n=1)
- backtest best call: 2026-07-28 10:27 +-158.5pts remaining (episode 93.5pts)
- backtest worst false alarm: 2026-07-28 10:27 -252.0pts adverse
- forward payoff: right +843 / wrong -570 / net +273 pts; median per fire +3.00 (n=21)
- forward best call: 2026-10-26 17:06 +36.5pts remaining (episode 121.5pts)
- forward worst false alarm: 2026-09-22 08:26 -226.0pts adverse
- earliness (backtest): median -158.5 pts of move remaining at fire (n=1)

### H14 — 1 signal
*Counter-trend No Demand / No Supply prints in an established trend mark absorption and precede trend continuation.*
Grading: directional. Latest review: keep-watching (recommendation).

**S0-H14** — session × window grid (cells as in the matrix):

| session | backtest | forward |
|---|---|---|
| whole | ▲i+4.4pp (37/148) · p+2.3pp cap76.0 net+2606/med+12.5 | ▼i-5.0pp (248/1598) · p+2.5pp cap74.5 net+8816/med+1.5 |
| london | ▼i-17.1pp (3/47) · p+12.0pp cap106.0 net+1414/med+12.5 | ▼i-6.6pp (64/410) · p+8.3pp cap97.0 net+4029/med+4.5 |
| overlap | (°▼i-9.1pp (0/7) · p-32.9pp cap— net-40/med+17.0) | ▼i-2.9pp (8/102) · p-4.9pp cap126.2 net+538/med+1.5 |
| ny_only | ▼i-2.0pp (5/29) · p-6.6pp cap85.7 net+804/med+53.0 | ▲i+3.8pp (79/370) · p+1.7pp cap108.0 net+2553/med+8.5 |
| dead | (°▲i+38.0pp (10/19) · p-1.9pp cap104.9 net-80/med-14.4) | ▼i-10.2pp (19/174) · p+3.9pp cap58.5 net-47/med+0.0 |
| asia | ▲i+16.6pp (19/46) · p+4.5pp cap46.5 net+508/med+7.5 | ▼i-9.0pp (78/542) · p+1.1pp cap48.5 net+1743/med+0.5 |

- backtest payoff: right +4618 / wrong -2012 / net +2606 pts; median per fire +12.50 (n=148)
- backtest best call: 2026-08-03 05:18 +451.0pts remaining (episode 472.0pts, major)
- backtest worst false alarm: 2026-07-28 13:00 -258.0pts adverse
- forward payoff: right +39878 / wrong -31061 / net +8816 pts; median per fire +1.50 (n=1597)
- forward best call: 2026-09-16 16:41 +879.1pts remaining (episode 925.1pts, major)
- forward worst false alarm: 2026-10-21 13:07 -365.0pts adverse
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
| whole | (°▼i-20.6pp (0/10) · p+35.9pp cap98.2 net+522/med+37.5) | ▼i-12.3pp (5/61) · p-2.2pp cap102.0 net+600/med+12.5 |
| london | — | — |
| overlap | — | — |
| ny_only | (°▼i-19.2pp (0/10) · p+46.5pp cap98.2 net+522/med+37.5) | ▼i-9.4pp (5/61) · p+10.9pp cap102.0 net+600/med+12.5 |
| dead | — | — |
| asia | — | — |

- backtest payoff: right +588 / wrong -66 / net +522 pts; median per fire +37.50 (n=10)
- backtest worst false alarm: 2026-07-28 19:30 -58.0pts adverse
- forward payoff: right +1991 / wrong -1391 / net +600 pts; median per fire +12.50 (n=61)
- forward best call: 2026-09-23 19:30 +61.0pts remaining (episode 89.5pts)
- forward worst false alarm: 2026-09-16 19:30 -216.5pts adverse

### H17 — 1 signal
*A climax reversal signal followed by absorption within five bars — effort meeting a quiet counter-party — marks a genuine exhaustion turn: the two-chapter story (exhaustion needs absorption to become reversal).*
Grading: directional. Latest review: rows (recommendation).

**S0-H17** — session × window grid (cells as in the matrix):

| session | backtest | forward |
|---|---|---|
| whole | ▲i+2.5pp (6/26) · p+2.8pp cap119.5 net-167/med-10.5 | ▲i+4.9pp (97/382) · p+0.7pp cap91.5 net-1038/med+1.0 |
| london | (°▲i+16.5pp (4/10) · p-6.9pp cap157.5 net+113/med+12.2) | ▲i+6.2pp (38/134) · p-9.0pp cap115.0 net-1005/med-12.2 |
| overlap | — | (°▼i-3.6pp (1/14) · p-9.0pp cap195.0 net-995/med-89.0) |
| ny_only | (°▲i+30.8pp (1/2) · p-13.5pp cap— net-281/med-140.5) | ▼i-6.5pp (6/54) · p+10.1pp cap162.2 net+492/med+1.2 |
| dead | (°▲i+10.4pp (1/4) · p-7.2pp cap— net-211/med-48.2) | ▲i+6.4pp (14/51) · p+2.2pp cap81.5 net+28/med+3.0 |
| asia | (°▼i-24.7pp (0/10) · p+16.2pp cap75.8 net+212/med+33.2) | ▲i+6.1pp (38/129) · p+4.0pp cap71.2 net+443/med+5.0 |

- backtest payoff: right +792 / wrong -958 / net -167 pts; median per fire -10.50 (n=26)
- backtest best call: 2026-07-29 10:09 +794.0pts remaining (episode 752.0pts, major)
- backtest worst false alarm: 2026-07-29 16:25 -203.5pts adverse
- forward payoff: right +11290 / wrong -12328 / net -1038 pts; median per fire +1.00 (n=382)
- forward best call: 2026-11-04 03:25 +1993.5pts remaining (episode 2016.0pts, major)
- forward worst false alarm: 2026-09-25 15:26 -311.5pts adverse
- earliness (backtest): median 110.0 pts of move remaining at fire (n=6)

### H18 — 1 signal
*A gap-traversal signal followed by a same-direction effortless print within five bars — travel meeting no opposition — continues: the map says vacuum, the tape confirms no resistance.*
Grading: directional. Latest review: rows (recommendation).

**S0-H18** — session × window grid (cells as in the matrix):

| session | backtest | forward |
|---|---|---|
| whole | ▲i+3.3pp (16/67) · p+2.8pp cap102.5 net+355/med+2.5 | ▼i-5.9pp (56/383) · p+0.4pp cap110.8 net+981/med+0.5 |
| london | ·i+1.5pp (7/28) · p+2.4pp cap87.5 net+681/med+46.2 | ▼i-8.0pp (15/106) · p+9.6pp cap90.5 net+356/med+9.5 |
| overlap | (°▼i-9.1pp (0/9) · p+11.5pp cap252.2 net-157/med-78.0) | ▼i-4.7pp (3/50) · p+3.6pp cap170.0 net+308/med+2.8 |
| ny_only | (°▼i-2.5pp (1/6) · p+3.2pp cap147.5 net-94/med-19.0) | ▼i-3.0pp (14/96) · p-1.7pp cap141.2 net+157/med+1.0 |
| dead | (°▼i-14.6pp (0/5) · p-7.2pp cap— net+32/med-6.6) | ·i+1.1pp (8/36) · p-2.0pp cap87.0 net-284/med-8.8 |
| asia | (°▲i+17.4pp (8/19) · p-13.3pp cap61.5 net-107/med+2.5) | ▼i-6.6pp (16/95) · p-7.5pp cap63.2 net+446/med-3.0 |

- backtest payoff: right +2707 / wrong -2352 / net +355 pts; median per fire +2.50 (n=67)
- backtest best call: 2026-08-03 05:12 +445.5pts remaining (episode 472.0pts, major)
- backtest worst false alarm: 2026-07-28 15:04 -332.5pts adverse
- forward payoff: right +11784 / wrong -10802 / net +981 pts; median per fire +0.50 (n=383)
- forward best call: 2026-10-01 12:13 +581.5pts remaining (episode 584.0pts, major)
- forward worst false alarm: 2026-10-01 13:34 -501.0pts adverse
- earliness (backtest): median 120.0 pts of move remaining at fire (n=11)

### H19 — 1 signal
*A probe-failure reversal signal followed by continued wide-loud effort in the anchor bar's own close direction within five bars is NOT the start of the claimed reversal — a SUPPRESSION/FADE configuration, and it says so.*
Grading: directional. Latest review: rows (recommendation).

- Question **Q1-H19**: see the register entry (status there is authoritative).
**S0-H19** — session × window grid (cells as in the matrix):

| session | backtest | forward |
|---|---|---|
| whole | ▼i-10.7pp (17/172) · p+10.2pp cap130.0 net+2236/med+3.2 | ▼i-2.5pp (322/1786) · p-1.9pp cap110.0 net-16318/med-4.8 |
| london | ▼i-4.7pp (6/32) · p+6.9pp cap135.5 net+708/med+34.0 | ·i-0.3pp (80/365) · p-5.9pp cap115.7 net-3908/med-3.5 |
| overlap | (°▼i-9.1pp (0/12) · p+58.8pp cap144.0 net+894/med+109.5) | ▼i-5.2pp (9/163) · p+4.0pp cap201.5 net-3713/med-6.0 |
| ny_only | ▼i-14.4pp (2/42) · p+24.6pp cap317.8 net+879/med+3.2 | ▼i-2.9pp (55/374) · p+1.8pp cap221.3 net-1478/med-2.5 |
| dead | ▼i-11.5pp (1/32) · p+8.4pp cap107.0 net-17/med-1.0 | ▼i-6.6pp (37/255) · p+1.0pp cap89.3 net-2453/med-7.0 |
| asia | ▼i-9.9pp (8/54) · p+0.3pp cap68.5 net-228/med-3.0 | ·i-1.0pp (141/629) · p-0.9pp cap78.0 net-4765/med-3.0 |

- backtest payoff: right +9284 / wrong -7047 / net +2236 pts; median per fire +3.25 (n=172)
- backtest best call: 2026-07-28 04:49 +523.0pts remaining (episode 543.0pts, major)
- backtest worst false alarm: 2026-07-29 19:00 -643.0pts adverse
- forward payoff: right +62162 / wrong -78480 / net -16318 pts; median per fire -4.75 (n=1786)
- forward best call: 2026-11-04 03:24 +1990.5pts remaining (episode 2016.0pts, major)
- forward worst false alarm: 2026-11-05 14:33 -1086.5pts adverse
- earliness (backtest): median 100.0 pts of move remaining at fire (n=12)

### H20 — 1 signal
*A wide-bar close-through of a session extreme (the same conditioned wide-bar class the retest anchor fires on; resolution = the close beyond the level, not a rejection back inside) initiates continuation in the break direction.*
Grading: directional. Latest review: rows (recommendation).

**S0-H20** — session × window grid (cells as in the matrix):

| session | backtest | forward |
|---|---|---|
| whole | ▼i-11.0pp (2/58) · p-13.3pp cap111.8 [cls 40.9%/14.4%i] net+27/med+18.2 | ▼i-11.3pp (11/460) · p+1.2pp cap124.8 [cls 41.0%/13.7%i] net-2361/med-4.5 |
| london | ▼i-13.0pp (2/37) · p-17.5pp cap87.5 [cls 41.8%/18.4%i] net-532/med+4.5 | ▼i-14.1pp (7/247) · p+10.0pp cap121.2 [cls 41.0%/16.9%i] net+1771/med+19.5 |
| overlap | (°▼i-7.9pp (0/12) · p+0.5pp cap156.5 [cls 41.2%/7.9%i] net+728/med+69.0) | ▼i-7.0pp (0/99) · p-13.8pp cap169.8 [cls 42.1%/7.0%i] net-3805/med-42.0 |
| ny_only | (°▼i-5.4pp (0/4) · p-17.3pp cap217.5 [cls 42.3%/5.4%i] net-81/med-9.4) | ▼i-3.5pp (3/42) · p+16.4pp cap357.0 [cls 24.1%/10.6%i] net+1865/med+5.7 |
| dead | (°▼i-7.4pp (0/2) · p-11.8pp cap— [cls 11.8%/7.4%i] net-51/med-25.7) | (°▼i-10.2pp (0/6) · p-11.0pp cap— [cls 11.0%/10.2%i] net-336/med-45.3) |
| asia | (°▼i-20.2pp (0/3) · p-6.3pp cap40.5 [cls 39.6%/20.2%i] net-36/med+11.0) | ▼i-13.6pp (1/66) · p-11.9pp cap75.5 [cls 46.7%/15.1%i] net-1857/med-26.8 |

- backtest payoff: right +1911 / wrong -1883 / net +27 pts; median per fire +18.25 (n=58)
- backtest best call: 2026-07-28 12:44 +200.0pts remaining (episode 347.0pts, major)
- backtest worst false alarm: 2026-07-27 13:28 -308.4pts adverse
- forward payoff: right +20516 / wrong -22877 / net -2361 pts; median per fire -4.50 (n=460)
- forward best call: 2026-10-13 04:01 +361.5pts remaining (episode 376.5pts, major)
- forward worst false alarm: 2026-09-22 13:13 -474.5pts adverse
- earliness (backtest): median 200.0 pts of move remaining at fire (n=1)


---

Appendix: the per-session detail beyond London and every horizon-mark payoff live in hypothesis_performance.json (generated, same run).