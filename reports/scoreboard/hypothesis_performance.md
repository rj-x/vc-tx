# Hypothesis Performance — Per-Instrument

Engine `f3eda9699` — register 40 fence as amended 2026-08-19 (operator): one section per instrument, each computed only from that instrument's own store and native calendar; uk100 canonical, ger40/nas100/us30 PROVISIONAL (validation pending). Numbers are NEVER pooled across instruments — cross-instrument aggregation is a future registration. This first cross-instrument read is EXPLORATORY: expectations deliberately unregistered; anything interesting becomes a pre-registered question before it becomes a claim.

---

# uk100 (uk100fut) — CANONICAL

Store span (1M, close ts): 2026-07-12 22:06:00+00:00 → 2026-08-19 22:15:00+00:00. Volume type: real futures volume (step-zero audit).

## Summary Matrix (page 1)

Engine `f3eda9699` — OBSERVATIONAL signal scoreboard - move-detection, not trading; no fills exist here by construction; never validation (docs/hypothesis_lifecycle.md stage 4)

**Review labels are RECOMMENDATIONS — none actioned, review pending operator familiarity.** Cells: marker + precision LIFT vs that context's OWN chance rate, (hits/fires), payoff net/median points (directional rows; either-direction rows have no payoff by construction). ▲/▼ = beyond ±2pp of chance, · = within. (°…) = small-n (fires<20 or episodes<10): dimmed, excluded from any future label arithmetic. Read READING_GUIDE.md first; full detail in signal_scoreboard.json.

| H | label | backtest whole | backtest london | forward whole | forward london |
|---|---|---|---|---|---|
| *context* | | 180 ep; chance 23.6%dir/44.3%either | 53 ep; chance 24.9%dir/47.1%either | 32 ep; chance 25.1%dir/44.8%either | 7 ep; chance 26.8%dir/49.2%either |
| H1 | keep-watching | ·-0.4pp (16/69) net+194/med+2.8 | ▲+6.9pp (7/22) net+133/med+3.0 | ·-0.1pp (6/24) net-5/med-0.8 | (°▲+13.2pp (2/5) net-4/med-1.0) |
| H2 | promote-candidate | ·+1.2pp (86/347) net+781/med+1.5 | ▲+6.3pp (25/80) net+521/med+9.2 | ▲+3.9pp (27/93) net-73/med-0.8 | (°▼-11.0pp (3/19) net-27/med-2.5) |
| H3 | keep-watching | — | — | (°▲+14.9pp (2/5) net+8/med-0.2) | (°▲+23.2pp (1/2) net+8/med+3.8) |
| H4 | keep-watching | (°▼-23.6pp (0/7) net+14/med+0.5) | (°▼-24.9pp (0/1) net+6/med+5.5) | — | — |
| H5 | keep-watching | — | — | — | — |
| H6 | keep-watching | ▲+8.0pp (27/59) [cls-chance 37.8% vs uncond 23.6%] net+391/med+5.7 | ▲+20.6pp (18/31) [cls-chance 37.5% vs uncond 24.9%] net+282/med+16.0 | (°▲+11.5pp (6/11) [cls-chance 43.0% vs uncond 25.1%] net+75/med+7.0) | (°▲+7.8pp (3/6) [cls-chance 42.2% vs uncond 26.8%] net+56/med+10.1) |
| H7 | keep-watching | ▲+5.9pp (33/112) net+7/med+2.8 | ·+1.9pp (11/41) net-217/med+2.7 | ▼-8.4pp (4/24) net+7/med+1.1 | (°·-1.8pp (3/12) net-24/med-5.2) |
| H7 (either-dir) | keep-watching | ▲+7.5pp (58/112) | ·+1.7pp (20/41) | ▼-11.5pp (8/24) | (°·+0.8pp (6/12)) |
| H8 | keep-watching | ·+1.8pp (160/347) | ▲+5.4pp (42/80) | ·-1.8pp (40/93) | (°▼-12.4pp (7/19)) |
| H9 | keep-watching | ▲+3.7pp (15/55) net+319/med+3.5 | (°▲+20.6pp (5/11) net+108/med+12.5) | (°▼-16.8pp (1/12) net-18/med-3.1) | — |
| H10 | deprioritize | ▼-4.8pp (55/293) net-240/med-1.4 | ▲+2.4pp (18/66) net-62/med+1.9 | ▼-17.3pp (6/77) net-227/med-3.5 | (°▼-16.8pp (1/10) net+27/med+4.8) |
| H11 | keep-watching | ▲+2.3pp (82/316) net-647/med-2.4 | ·-1.3pp (35/148) net+250/med-0.6 | ·-1.4pp (14/59) net+199/med+4.3 | (°▼-17.1pp (3/31) net+128/med+4.8) |
| H12 | keep-watching | — | — | — | — |
| **union coverage** | | 56.7% (102/180) | 52.8% (28/53) | 81.2% (26/32) | 85.7% (6/7) |

Not graded:  — see register entries.

## Hypothesis Cards (page 2)

### H1
*A climactic bar — extreme volume on a wide spread late in an extended move — marks exhaustion, and price then reverses against the climax direction.*
Grading: directional. Latest review: keep-watching (recommendation).

**H1** — session × window grid (cells as in the matrix):

| session | backtest | forward |
|---|---|---|
| whole | ·-0.4pp (16/69) net+194/med+2.8 | ·-0.1pp (6/24) net-5/med-0.8 |
| london | ▲+6.9pp (7/22) net+133/med+3.0 | (°▲+13.2pp (2/5) net-4/med-1.0) |
| overlap | (°▲+23.9pp (1/2) net+35/med+17.7) | (°▼-26.5pp (0/1) net-0/med-0.3) |
| ny_only | ▲+8.0pp (4/22) net+17/med+1.6 | (°▼-8.5pp (0/6) net-1/med+0.0) |
| dead | (°▲+7.4pp (3/12) net+30/med+1.1) | (°▲+18.4pp (1/3) net+3/med+1.7) |
| asia | (°▼-23.4pp (1/11) net-22/med-2.6) | (°▼-8.1pp (3/9) net-3/med-1.0) |

- backtest payoff: right +639 / wrong -445 / net +194 pts; median per fire +2.75 (n=68)
- backtest best call: 2026-07-29 04:04 +105.2pts remaining (episode 102.8pts, major)
- backtest worst false alarm: 2026-07-23 12:17 -70.7pts adverse
- forward payoff: right +52 / wrong -57 / net -5 pts; median per fire -0.80 (n=23)
- forward best call: 2026-08-17 10:30 +46.5pts remaining (episode 42.7pts, major)
- forward worst false alarm: 2026-08-18 12:05 -20.7pts adverse
- earliness (backtest): median 29.0 pts of move remaining at fire (n=23)

### H2
*A failed probe beyond a prior extreme — an upthrust above or spring below that closes back inside — reverses against the probe.*
Grading: directional. Latest review: promote-candidate (recommendation).

**H2** — session × window grid (cells as in the matrix):

| session | backtest | forward |
|---|---|---|
| whole | ·+1.2pp (86/347) net+781/med+1.5 | ▲+3.9pp (27/93) net-73/med-0.8 |
| london | ▲+6.3pp (25/80) net+521/med+9.2 | (°▼-11.0pp (3/19) net-27/med-2.5) |
| overlap | (°·+1.2pp (3/11) net+21/med+3.5) | (°▼-26.5pp (0/4) net+5/med+1.6) |
| ny_only | ▲+4.3pp (8/55) net-487/med-2.5 | (°▼-8.5pp (0/20) net-3/med-0.9) |
| dead | ·+1.3pp (17/90) net+180/med+0.8 | (°▲+25.1pp (4/10) net+10/med+2.0) |
| asia | ▼-2.8pp (33/111) net+546/med+2.7 | ▲+8.6pp (20/40) net-59/med-1.4 |

- backtest payoff: right +3270 / wrong -2490 / net +781 pts; median per fire +1.50 (n=347)
- backtest best call: 2026-07-30 04:03 +155.1pts remaining (episode 178.3pts, major)
- backtest worst false alarm: 2026-07-24 06:52 -98.0pts adverse
- forward payoff: right +259 / wrong -333 / net -73 pts; median per fire -0.80 (n=93)
- forward best call: 2026-08-17 10:33 +37.0pts remaining (episode 42.7pts, major)
- forward worst false alarm: 2026-08-19 12:44 -36.0pts adverse
- earliness (backtest): median 27.5 pts of move remaining at fire (n=39)

### H3
*Repeated absorption — high effort with no result — at a price level precedes a breakout through that level.*
Grading: directional. Latest review: keep-watching (recommendation).

**H3** — session × window grid (cells as in the matrix):

| session | backtest | forward |
|---|---|---|
| whole | — | (°▲+14.9pp (2/5) net+8/med-0.2) |
| london | — | (°▲+23.2pp (1/2) net+8/med+3.8) |
| overlap | — | — |
| ny_only | — | (°▼-8.5pp (0/2) net+0/med+0.1) |
| dead | — | (°▲+85.1pp (1/1) net-0/med-0.2) |
| asia | — | — |

- forward payoff: right +13 / wrong -6 / net +8 pts; median per fire -0.20 (n=5)
- forward best call: 2026-08-18 18:23 +13.0pts remaining (episode 10.0pts)
- forward worst false alarm: 2026-08-18 08:40 -12.5pts adverse

### H4
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

### H5
*A buying climax that extends far above its trend mean mean-reverts (climax-extension fade; registered short-side only).*
Grading: directional. Latest review: keep-watching (recommendation).

**H5** — session × window grid (cells as in the matrix):

| session | backtest | forward |
|---|---|---|
| whole | — | — |
| london | — | — |
| overlap | — | — |
| ny_only | — | — |
| dead | — | — |
| asia | — | — |


### H6
*A wide-spread rejection bar at a session extreme (measured day-relative, volume-agnostic) reverses away from the extreme.*
Grading: directional. Latest review: keep-watching (recommendation).

**H6** — session × window grid (cells as in the matrix):

| session | backtest | forward |
|---|---|---|
| whole | ▲+8.0pp (27/59) [cls-chance 37.8% vs uncond 23.6%] net+391/med+5.7 | (°▲+11.5pp (6/11) [cls-chance 43.0% vs uncond 25.1%] net+75/med+7.0) |
| london | ▲+20.6pp (18/31) [cls-chance 37.5% vs uncond 24.9%] net+282/med+16.0 | (°▲+7.8pp (3/6) [cls-chance 42.2% vs uncond 26.8%] net+56/med+10.1) |
| overlap | (°▼-30.7pp (0/6) [cls-chance 30.7% vs uncond 26.1%] net-87/med-15.4) | — |
| ny_only | (°▼-20.5pp (0/4) [cls-chance 20.5% vs uncond 10.2%] net+0/med+6.5) | (°▼-5.4pp (0/1) [cls-chance 5.4% vs uncond 8.5%] net-6/med-5.7) |
| dead | (°▼-19.1pp (0/5) [cls-chance 19.1% vs uncond 17.6%] net-25/med-6.4) | — |
| asia | (°▲+24.2pp (9/13) [cls-chance 45.0% vs uncond 32.5%] net+220/med+5.7) | (°▲+19.9pp (3/4) [cls-chance 55.1% vs uncond 41.4%] net+25/med+7.2) |

- backtest payoff: right +818 / wrong -428 / net +391 pts; median per fire +5.70 (n=59)
- backtest best call: 2026-07-31 08:00 +72.8pts remaining (episode 68.5pts, major)
- backtest worst false alarm: 2026-07-22 08:07 -80.3pts adverse
- forward payoff: right +90 / wrong -15 / net +75 pts; median per fire +7.00 (n=11)
- forward best call: 2026-08-17 12:32 +6.7pts remaining (episode 19.5pts)
- forward worst false alarm: 2026-08-14 15:35 -14.5pts adverse
- earliness (backtest): median 21.6 pts of move remaining at fire (n=8)

### H7
*Quiet decline at a session extreme is disguised accumulation: effortless (low-volume) weakness reverses UP once selling fails to attract participation (mirror: quiet advance at a high reverses down).*
Grading: directional + either-direction (dual). Latest review: keep-watching (recommendation).

**H7** — session × window grid (cells as in the matrix):

| session | backtest | forward |
|---|---|---|
| whole | ▲+5.9pp (33/112) net+7/med+2.8 | ▼-8.4pp (4/24) net+7/med+1.1 |
| london | ·+1.9pp (11/41) net-217/med+2.7 | (°·-1.8pp (3/12) net-24/med-5.2) |
| overlap | ▲+8.7pp (8/23) net+227/med+8.7 | (°▼-26.5pp (0/2) net+2/med+1.0) |
| ny_only | (°▲+4.1pp (2/14) net-24/med+0.0) | (°▼-8.5pp (0/7) net+23/med+5.5) |
| dead | (°▲+2.4pp (1/5) net+60/med+3.5) | (°▼-14.9pp (0/1) net+0/med+0.0) |
| asia | ▲+5.4pp (11/29) net-38/med+0.7 | (°▲+8.6pp (1/2) net+6/med+3.0) |

- backtest payoff: right +1097 / wrong -1090 / net +7 pts; median per fire +2.80 (n=112)
- backtest best call: 2026-07-24 11:09 +98.2pts remaining (episode 98.2pts, major)
- backtest worst false alarm: 2026-07-30 06:55 -94.0pts adverse
- forward payoff: right +112 / wrong -104 / net +7 pts; median per fire +1.10 (n=24)
- forward best call: 2026-08-18 19:09 +7.5pts remaining (episode 10.0pts)
- forward worst false alarm: 2026-08-17 11:49 -29.5pts adverse
- earliness (backtest): median 22.6 pts of move remaining at fire (n=30)

**H7 (either-dir)** — session × window grid (cells as in the matrix):

| session | backtest | forward |
|---|---|---|
| whole | ▲+7.5pp (58/112) | ▼-11.5pp (8/24) |
| london | ·+1.7pp (20/41) | (°·+0.8pp (6/12)) |
| overlap | ▲+5.3pp (13/23) | (°▼-53.0pp (0/2)) |
| ny_only | (°▲+8.5pp (4/14)) | (°▼-16.9pp (0/7)) |
| dead | (°▼-12.8pp (1/5)) | (°▼-29.8pp (0/1)) |
| asia | ▲+9.4pp (20/29) | (°▲+31.9pp (2/2)) |

- backtest payoff: n/a by construction (either-direction)
- backtest best call: 2026-07-24 11:09 +98.2pts remaining (episode 98.2pts, major)
- backtest worst false alarm: 2026-07-23 16:44 -25.7pts adverse
- forward payoff: n/a by construction (either-direction)
- forward best call: 2026-08-19 10:10 +54.5pts remaining (episode 62.8pts, major)
- forward worst false alarm: 2026-08-17 10:09 -18.3pts adverse
- earliness (backtest): median 15.3 pts of move remaining at fire (n=41)

### H8
*Reversal-signature bar anatomy (upthrust/spring) predicts imminent range expansion irrespective of direction.*
Grading: either-direction. Latest review: keep-watching (recommendation).

**H8** — session × window grid (cells as in the matrix):

| session | backtest | forward |
|---|---|---|
| whole | ·+1.8pp (160/347) | ·-1.8pp (40/93) |
| london | ▲+5.4pp (42/80) | (°▼-12.4pp (7/19)) |
| overlap | (°▲+12.4pp (7/11)) | (°▼-53.0pp (0/4)) |
| ny_only | ▲+23.5pp (24/55) | (°▼-11.9pp (1/20)) |
| dead | ·+1.6pp (31/90) | (°▲+30.2pp (6/10)) |
| asia | ▼-9.1pp (56/111) | ▼-3.1pp (26/40) |

- backtest payoff: n/a by construction (either-direction)
- backtest best call: 2026-07-30 04:03 +155.1pts remaining (episode 178.3pts, major)
- backtest worst false alarm: 2026-07-22 10:02 -37.0pts adverse
- forward payoff: n/a by construction (either-direction)
- forward best call: 2026-08-18 10:57 +56.0pts remaining (episode 50.0pts, major)
- forward worst false alarm: 2026-08-19 14:46 -18.0pts adverse
- earliness (backtest): median 26.9 pts of move remaining at fire (n=58)

### H9
*Persistent lower-TF directional pressure that recruits expanding participation at the parent timeframe precedes continuation beyond what the parent label alone predicts; pressure without participation expansion does not.*
Grading: directional. Latest review: keep-watching (recommendation).

**H9** — session × window grid (cells as in the matrix):

| session | backtest | forward |
|---|---|---|
| whole | ▲+3.7pp (15/55) net+319/med+3.5 | (°▼-16.8pp (1/12) net-18/med-3.1) |
| london | (°▲+20.6pp (5/11) net+108/med+12.5) | — |
| overlap | — | (°▼-26.5pp (0/1) net-1/med-1.0) |
| ny_only | (°▲+14.8pp (3/12) net+115/med+2.8) | (°▲+24.8pp (1/3) net+11/med+6.8) |
| dead | (°▼-8.5pp (1/11) net+11/med+1.0) | — |
| asia | ▼-3.9pp (6/21) net+86/med+6.8 | (°▼-41.4pp (0/8) net-28/med-3.1) |

- backtest payoff: right +558 / wrong -239 / net +319 pts; median per fire +3.50 (n=53)
- backtest best call: 2026-08-03 03:40 +73.2pts remaining (episode 81.3pts, major)
- backtest worst false alarm: 2026-07-30 09:15 -59.3pts adverse
- forward payoff: right +24 / wrong -42 / net -18 pts; median per fire -3.10 (n=12)
- forward best call: 2026-08-17 15:40 +16.3pts remaining (episode 18.3pts)
- forward worst false alarm: 2026-08-14 16:30 -13.2pts adverse
- earliness (backtest): median 15.0 pts of move remaining at fire (n=11)

### H10
*In an established 1-minute trend, no-demand/no-supply prints in the trend's direction signal continuation.*
Grading: directional. Latest review: deprioritize (recommendation).

**H10** — session × window grid (cells as in the matrix):

| session | backtest | forward |
|---|---|---|
| whole | ▼-4.8pp (55/293) net-240/med-1.4 | ▼-17.3pp (6/77) net-227/med-3.5 |
| london | ▲+2.4pp (18/66) net-62/med+1.9 | (°▼-16.8pp (1/10) net+27/med+4.8) |
| overlap | (°▼-26.1pp (0/7) net+27/med+6.8) | (°▼-26.5pp (0/5) net-75/med-15.8) |
| ny_only | ·-0.6pp (8/83) net+51/med-1.5 | (°▼-3.5pp (1/20) net-21/med-1.0) |
| dead | ▼-3.7pp (5/36) net-110/med-2.5 | (°▼-14.9pp (0/15) net-24/med-2.0) |
| asia | ▼-8.7pp (24/101) net-147/med-1.5 | ▼-26.6pp (4/27) net-135/med-4.8 |

- backtest payoff: right +1533 / wrong -1773 / net -240 pts; median per fire -1.40 (n=293)
- backtest best call: 2026-07-23 10:20 +90.0pts remaining (episode 104.8pts, major)
- backtest worst false alarm: 2026-07-28 13:10 -62.5pts adverse
- forward payoff: right +115 / wrong -342 / net -227 pts; median per fire -3.50 (n=77)
- forward best call: 2026-08-14 16:54 +22.5pts remaining (episode 16.8pts)
- forward worst false alarm: 2026-08-17 14:08 -24.2pts adverse
- earliness (backtest): median 19.4 pts of move remaining at fire (n=26)

### H11
*Price entering a low-volume price zone traverses it faster than baseline; entering a high-volume node it stalls or reverses at above-baseline rates.*
Grading: directional. Latest review: keep-watching (recommendation).

**H11** — session × window grid (cells as in the matrix):

| session | backtest | forward |
|---|---|---|
| whole | ▲+2.3pp (82/316) net-647/med-2.4 | ·-1.4pp (14/59) net+199/med+4.3 |
| london | ·-1.3pp (35/148) net+250/med-0.6 | (°▼-17.1pp (3/31) net+128/med+4.8) |
| overlap | ▼-18.6pp (3/40) net-403/med-11.8 | (°▲+44.9pp (5/7) net+59/med+9.3) |
| ny_only | ▲+18.7pp (11/38) net-267/med-1.6 | (°▲+16.5pp (5/20) net+46/med+3.6) |
| dead | ▲+37.4pp (11/20) net+59/med+0.7 | — |
| asia | ·-1.1pp (22/70) net-286/med-4.5 | (°▲+58.6pp (1/1) net-34/med-33.5) |

- backtest payoff: right +2555 / wrong -3203 / net -647 pts; median per fire -2.35 (n=316)
- backtest best call: 2026-07-22 06:08 +129.2pts remaining (episode 163.2pts, major)
- backtest worst false alarm: 2026-07-22 07:36 -96.5pts adverse
- forward payoff: right +345 / wrong -146 / net +199 pts; median per fire +4.30 (n=59)
- forward best call: 2026-08-17 13:04 +22.8pts remaining (episode 32.3pts)
- forward worst false alarm: 2026-08-14 15:30 -21.3pts adverse
- earliness (backtest): median 20.5 pts of move remaining at fire (n=27)

### H12
*A zone showing repeated visits with elevated volume, diminishing range-per-unit-volume, and drying pullback volume precedes a directional move away from the zone in the absorber's direction.*
Grading: directional. Latest review: keep-watching (recommendation).

**H12** — session × window grid (cells as in the matrix):

| session | backtest | forward |
|---|---|---|
| whole | — | — |
| london | — | — |
| overlap | — | — |
| ny_only | — | — |
| dead | — | — |
| asia | — | — |



---

# ger40 (ger40fut) — PROVISIONAL

> **PROVISIONAL — validation pending (register 40 fence as amended 2026-08-19): replay-only study over the synced store; canonical status, live attachment, and Asia/pause-sensitive cell interpretation await this instrument's validation evening. EXPLORATORY first cross-instrument look — expectations deliberately unregistered; anything interesting becomes a pre-registered question before it becomes a claim. NO POOLING across instruments.**
>
> - drift-adjustment segments and engine tod baselines run on the provider/London trading-day structure; native cash-hour segmentation is part of this instrument's validation evening
> - sessions = the registered register-37 world-clock partition (native-tz, DST-proof) applied to this instrument's own bars; 'london' is not the home session of the US pairs
> - the forward window (>= go_live) is also a replay over the synced store — this instrument has NO live attachment yet

Store span (1M, close ts): 2026-07-19 22:42:00+00:00 → 2026-08-19 12:20:00+00:00. Volume type: real futures volume (register 40 first-sync sanity; canonical verdict at this instrument's validation evening).

## Summary Matrix (page 1)

Engine `f3eda9699` — OBSERVATIONAL signal scoreboard - move-detection, not trading; no fills exist here by construction; never validation (docs/hypothesis_lifecycle.md stage 4)

**Review labels are RECOMMENDATIONS — none actioned, review pending operator familiarity.** Cells: marker + precision LIFT vs that context's OWN chance rate, (hits/fires), payoff net/median points (directional rows; either-direction rows have no payoff by construction). ▲/▼ = beyond ±2pp of chance, · = within. (°…) = small-n (fires<20 or episodes<10): dimmed, excluded from any future label arithmetic. Read READING_GUIDE.md first; full detail in signal_scoreboard.json.

| H | label | backtest whole | backtest london | forward whole | forward london |
|---|---|---|---|---|---|
| *context* | | 109 ep; chance 23.9%dir/45.1%either | 27 ep; chance 26.3%dir/51.1%either | 28 ep; chance 23.8%dir/42.8%either | 6 ep; chance 20.8%dir/38.4%either |
| H1 | keep-watching | ▲+10.8pp (17/49) net-83/med+0.7 | (°▲+33.7pp (3/5) net+198/med+39.9) | ▲+26.2pp (10/20) net+128/med+3.1 | (°▲+45.9pp (2/3) net-4/med-7.8) |
| H2 | promote-candidate | ·+0.0pp (56/234) net-661/med-5.2 | (°▼-13.0pp (2/15) net+93/med+9.8) | ▲+17.5pp (26/63) net+19/med+2.3 | (°·+1.4pp (2/9) net-17/med-11.4) |
| H3 | keep-watching | (°▼-11.4pp (1/8) net-28/med+2.0) | — | (°▼-23.8pp (0/2) net-16/med-8.2) | — |
| H4 | keep-watching | ▲+5.5pp (10/34) net+72/med+10.0 | (°▼-16.3pp (1/10) net-30/med-3.7) | — | — |
| H5 | keep-watching | — | — | — | — |
| H6 | keep-watching | ▲+3.9pp (14/36) [cls-chance 35.0% vs uncond 23.9%] net-192/med-10.4 | (°▼-7.4pp (5/18) [cls-chance 35.2% vs uncond 26.3%] net-56/med-10.3) | ▼-5.8pp (17/49) [cls-chance 40.5% vs uncond 23.8%] net-519/med-8.0 | (°▼-14.2pp (6/26) [cls-chance 37.3% vs uncond 20.8%] net-501/med-21.4) |
| H7 | keep-watching | ▲+11.7pp (21/59) net+761/med+4.2 | ▲+23.7pp (10/20) net+719/med+33.0 | (°▼-12.7pp (1/9) net+3/med+2.6) | (°▼-8.3pp (1/8) net+32/med+4.8) |
| H7 (either-dir) | keep-watching | ▲+19.3pp (38/59) | ▲+23.9pp (15/20) | (°▼-9.5pp (3/9)) | (°·-0.9pp (3/8)) |
| H8 | keep-watching | ▲+7.9pp (124/234) | (°▼-31.1pp (3/15)) | ▲+11.2pp (34/63) | (°▼-16.2pp (2/9)) |
| H9 | keep-watching | ▼-8.5pp (8/52) net-426/med-4.1 | (°▼-26.3pp (0/3) net+17/med+22.6) | (°▼-23.8pp (0/6) net-136/med-4.0) | (°▼-20.8pp (0/1) net-114/med-114.2) |
| H10 | deprioritize | ▼-4.2pp (29/147) net-391/med+3.2 | ▼-16.0pp (4/39) net-463/med-12.5 | ·+0.3pp (14/58) net+46/med+3.0 | (°▲+9.2pp (3/10) net-36/med-11.8) |
| H11 | keep-watching | ▼-3.6pp (15/74) net-452/med-6.0 | (°▼-4.9pp (3/14) net-472/med-58.8) | ·+0.1pp (22/92) net-344/med-6.6 | (°▼-9.4pp (5/44) net-190/med-11.2) |
| H12 | keep-watching | — | — | — | — |
| **union coverage** | | 44.0% (48/109) | 25.9% (7/27) | 67.9% (19/28) | 83.3% (5/6) |

Not graded:  — see register entries.

## Hypothesis Cards (page 2)

### H1
*A climactic bar — extreme volume on a wide spread late in an extended move — marks exhaustion, and price then reverses against the climax direction.*
Grading: directional. Latest review: keep-watching (recommendation).

**H1** — session × window grid (cells as in the matrix):

| session | backtest | forward |
|---|---|---|
| whole | ▲+10.8pp (17/49) net-83/med+0.7 | ▲+26.2pp (10/20) net+128/med+3.1 |
| london | (°▲+33.7pp (3/5) net+198/med+39.9) | (°▲+45.9pp (2/3) net-4/med-7.8) |
| overlap | — | (°▼-25.7pp (0/1) net+29/med+28.7) |
| ny_only | (°▲+18.7pp (3/10) net-289/med-3.9) | (°▼-7.5pp (0/1) net-7/med-7.3) |
| dead | (°▲+40.7pp (4/7) net+93/med+34.1) | (°▼-14.8pp (0/2) net-4/med-2.1) |
| asia | ▼-7.1pp (7/27) net-85/med-12.0 | (°▲+21.2pp (8/13) net+115/med+10.2) |

- backtest payoff: right +1327 / wrong -1411 / net -83 pts; median per fire +0.70 (n=49)
- backtest best call: 2026-07-29 03:13 +188.0pts remaining (episode 262.8pts, major)
- backtest worst false alarm: 2026-07-29 19:11 -164.0pts adverse
- forward payoff: right +223 / wrong -95 / net +128 pts; median per fire +3.15 (n=20)
- forward best call: 2026-08-17 10:30 +134.4pts remaining (episode 134.4pts, major)
- forward worst false alarm: 2026-08-17 12:27 -35.0pts adverse
- earliness (backtest): median 97.9 pts of move remaining at fire (n=8)

### H2
*A failed probe beyond a prior extreme — an upthrust above or spring below that closes back inside — reverses against the probe.*
Grading: directional. Latest review: promote-candidate (recommendation).

**H2** — session × window grid (cells as in the matrix):

| session | backtest | forward |
|---|---|---|
| whole | ·+0.0pp (56/234) net-661/med-5.2 | ▲+17.5pp (26/63) net+19/med+2.3 |
| london | (°▼-13.0pp (2/15) net+93/med+9.8) | (°·+1.4pp (2/9) net-17/med-11.4) |
| overlap | (°▼-14.6pp (1/11) net-195/med-38.7) | (°▼-25.7pp (0/5) net-27/med-8.0) |
| ny_only | ▲+10.0pp (13/61) net-1116/med-16.7 | (°▼-7.5pp (0/3) net-4/med-4.2) |
| dead | ▲+6.7pp (12/52) net+604/med+2.2 | (°▲+47.7pp (5/8) net+46/med+4.7) |
| asia | ▼-3.5pp (28/95) net-47/med-10.6 | ▲+9.7pp (19/38) net+22/med+3.8 |

- backtest payoff: right +4896 / wrong -5557 / net -661 pts; median per fire -5.20 (n=234)
- backtest best call: 2026-07-27 03:23 +214.5pts remaining (episode 245.3pts, major)
- backtest worst false alarm: 2026-07-29 19:00 -192.8pts adverse
- forward payoff: right +530 / wrong -510 / net +19 pts; median per fire +2.30 (n=63)
- forward best call: 2026-08-19 03:17 +82.8pts remaining (episode 94.3pts, major)
- forward worst false alarm: 2026-08-19 06:49 -69.4pts adverse
- earliness (backtest): median 97.8 pts of move remaining at fire (n=19)

### H3
*Repeated absorption — high effort with no result — at a price level precedes a breakout through that level.*
Grading: directional. Latest review: keep-watching (recommendation).

**H3** — session × window grid (cells as in the matrix):

| session | backtest | forward |
|---|---|---|
| whole | (°▼-11.4pp (1/8) net-28/med+2.0) | (°▼-23.8pp (0/2) net-16/med-8.2) |
| london | — | — |
| overlap | — | — |
| ny_only | (°▲+8.7pp (1/5) net+132/med+41.2) | (°▼-7.5pp (0/1) net-17/med-16.8) |
| dead | — | — |
| asia | (°▼-33.0pp (0/3) net-160/med-56.5) | (°▼-40.3pp (0/1) net+0/med+0.5) |

- backtest payoff: right +132 / wrong -160 / net -28 pts; median per fire +2.00 (n=8)
- backtest best call: 2026-07-27 18:10 +51.7pts remaining (episode 62.7pts)
- backtest worst false alarm: 2026-07-30 01:57 -65.7pts adverse
- forward payoff: right +0 / wrong -17 / net -16 pts; median per fire -8.15 (n=2)
- forward worst false alarm: 2026-08-18 19:15 -18.7pts adverse
- earliness (backtest): median 51.7 pts of move remaining at fire (n=1)

### H4
*In an established trend, a quiet (low-volume) pullback resolves with trend resumption.*
Grading: directional. Latest review: keep-watching (recommendation).

**H4** — session × window grid (cells as in the matrix):

| session | backtest | forward |
|---|---|---|
| whole | ▲+5.5pp (10/34) net+72/med+10.0 | — |
| london | (°▼-16.3pp (1/10) net-30/med-3.7) | — |
| overlap | (°▲+9.6pp (2/6) net-4/med-8.4) | — |
| ny_only | (°▲+22.0pp (2/6) net-9/med+10.8) | — |
| dead | (°▲+8.6pp (1/4) net-14/med+32.4) | — |
| asia | (°▲+17.0pp (4/8) net+129/med+17.4) | — |

- backtest payoff: right +556 / wrong -484 / net +72 pts; median per fire +10.00 (n=33)
- backtest best call: 2026-08-03 11:48 +80.2pts remaining (episode 142.0pts, major)
- backtest worst false alarm: 2026-07-26 23:29 -102.8pts adverse
- earliness (backtest): median 71.2 pts of move remaining at fire (n=3)

### H5
*A buying climax that extends far above its trend mean mean-reverts (climax-extension fade; registered short-side only).*
Grading: directional. Latest review: keep-watching (recommendation).

**H5** — session × window grid (cells as in the matrix):

| session | backtest | forward |
|---|---|---|
| whole | — | — |
| london | — | — |
| overlap | — | — |
| ny_only | — | — |
| dead | — | — |
| asia | — | — |


### H6
*A wide-spread rejection bar at a session extreme (measured day-relative, volume-agnostic) reverses away from the extreme.*
Grading: directional. Latest review: keep-watching (recommendation).

**H6** — session × window grid (cells as in the matrix):

| session | backtest | forward |
|---|---|---|
| whole | ▲+3.9pp (14/36) [cls-chance 35.0% vs uncond 23.9%] net-192/med-10.4 | ▼-5.8pp (17/49) [cls-chance 40.5% vs uncond 23.8%] net-519/med-8.0 |
| london | (°▼-7.4pp (5/18) [cls-chance 35.2% vs uncond 26.3%] net-56/med-10.3) | (°▼-14.2pp (6/26) [cls-chance 37.3% vs uncond 20.8%] net-501/med-21.4) |
| overlap | (°▲+72.1pp (1/1) [cls-chance 27.9% vs uncond 23.7%] net+108/med+108.3) | (°▲+4.2pp (1/4) [cls-chance 20.8% vs uncond 25.7%] net-4/med-10.5) |
| ny_only | — | — |
| dead | (°▼-25.0pp (0/3) [cls-chance 25.0% vs uncond 16.4%] net+29/med+13.4) | — |
| asia | (°▲+18.8pp (8/14) [cls-chance 38.3% vs uncond 33.0%] net-274/med-21.8) | (°▲+3.8pp (10/19) [cls-chance 48.8% vs uncond 40.3%] net-14/med+2.0) |

- backtest payoff: right +682 / wrong -874 / net -192 pts; median per fire -10.40 (n=36)
- backtest best call: 2026-07-30 06:22 +154.2pts remaining (episode 174.4pts, major)
- backtest worst false alarm: 2026-08-03 07:10 -108.0pts adverse
- forward payoff: right +371 / wrong -890 / net -519 pts; median per fire -8.00 (n=49)
- forward best call: 2026-08-19 03:31 +81.3pts remaining (episode 94.3pts, major)
- forward worst false alarm: 2026-08-18 07:07 -124.1pts adverse
- earliness (backtest): median 150.2 pts of move remaining at fire (n=2)

### H7
*Quiet decline at a session extreme is disguised accumulation: effortless (low-volume) weakness reverses UP once selling fails to attract participation (mirror: quiet advance at a high reverses down).*
Grading: directional + either-direction (dual). Latest review: keep-watching (recommendation).

**H7** — session × window grid (cells as in the matrix):

| session | backtest | forward |
|---|---|---|
| whole | ▲+11.7pp (21/59) net+761/med+4.2 | (°▼-12.7pp (1/9) net+3/med+2.6) |
| london | ▲+23.7pp (10/20) net+719/med+33.0 | (°▼-8.3pp (1/8) net+32/med+4.8) |
| overlap | (°▲+23.0pp (7/15) net+56/med-29.0) | (°▼-25.7pp (0/1) net-29/med-28.6) |
| ny_only | (°▲+5.4pp (1/6) net+59/med+7.7) | — |
| dead | (°▲+8.6pp (1/4) net-15/med-28.8) | — |
| asia | (°▼-18.7pp (2/14) net-58/med-10.2) | — |

- backtest payoff: right +1756 / wrong -995 / net +761 pts; median per fire +4.20 (n=59)
- backtest best call: 2026-07-27 03:04 +247.0pts remaining (episode 245.3pts, major)
- backtest worst false alarm: 2026-07-27 13:57 -91.8pts adverse
- forward payoff: right +84 / wrong -81 / net +3 pts; median per fire +2.60 (n=9)
- forward best call: 2026-08-19 10:29 +47.4pts remaining (episode 50.8pts)
- forward worst false alarm: 2026-08-18 07:12 -71.0pts adverse
- earliness (backtest): median 74.6 pts of move remaining at fire (n=11)

**H7 (either-dir)** — session × window grid (cells as in the matrix):

| session | backtest | forward |
|---|---|---|
| whole | ▲+19.3pp (38/59) | (°▼-9.5pp (3/9)) |
| london | ▲+23.9pp (15/20) | (°·-0.9pp (3/8)) |
| overlap | (°▲+33.4pp (12/15)) | (°▼-51.3pp (0/1)) |
| ny_only | (°▲+11.2pp (2/6)) | — |
| dead | (°▲+43.2pp (3/4)) | — |
| asia | (°▼-16.7pp (6/14)) | — |

- backtest payoff: n/a by construction (either-direction)
- backtest best call: 2026-07-27 03:04 +247.0pts remaining (episode 245.3pts, major)
- backtest worst false alarm: 2026-07-29 11:19 -63.7pts adverse
- forward payoff: n/a by construction (either-direction)
- forward best call: 2026-08-18 12:01 +128.8pts remaining (episode 149.0pts, major)
- forward worst false alarm: 2026-08-17 14:17 -28.6pts adverse
- earliness (backtest): median 74.6 pts of move remaining at fire (n=17)

### H8
*Reversal-signature bar anatomy (upthrust/spring) predicts imminent range expansion irrespective of direction.*
Grading: either-direction. Latest review: keep-watching (recommendation).

**H8** — session × window grid (cells as in the matrix):

| session | backtest | forward |
|---|---|---|
| whole | ▲+7.9pp (124/234) | ▲+11.2pp (34/63) |
| london | (°▼-31.1pp (3/15)) | (°▼-16.2pp (2/9)) |
| overlap | (°▲+17.0pp (7/11)) | (°▼-31.3pp (1/5)) |
| ny_only | ▲+32.0pp (33/61) | (°▼-15.1pp (0/3)) |
| dead | ·+0.9pp (17/52) | (°▲+47.5pp (6/8)) |
| asia | ▲+7.8pp (64/95) | ▼-3.1pp (25/38) |

- backtest payoff: n/a by construction (either-direction)
- backtest best call: 2026-07-27 03:23 +214.5pts remaining (episode 245.3pts, major)
- backtest worst false alarm: 2026-07-29 16:35 -74.4pts adverse
- forward payoff: n/a by construction (either-direction)
- forward best call: 2026-08-18 04:54 +90.7pts remaining (episode 106.9pts, major)
- forward worst false alarm: 2026-08-18 09:32 -59.6pts adverse
- earliness (backtest): median 80.1 pts of move remaining at fire (n=27)

### H9
*Persistent lower-TF directional pressure that recruits expanding participation at the parent timeframe precedes continuation beyond what the parent label alone predicts; pressure without participation expansion does not.*
Grading: directional. Latest review: keep-watching (recommendation).

**H9** — session × window grid (cells as in the matrix):

| session | backtest | forward |
|---|---|---|
| whole | ▼-8.5pp (8/52) net-426/med-4.1 | (°▼-23.8pp (0/6) net-136/med-4.0) |
| london | (°▼-26.3pp (0/3) net+17/med+22.6) | (°▼-20.8pp (0/1) net-114/med-114.2) |
| overlap | (°▼-23.7pp (0/2) net+112/med+55.8) | — |
| ny_only | ▼-6.8pp (1/22) net-517/med-19.3 | (°▼-7.5pp (0/4) net-16/med+2.1) |
| dead | (°▲+16.9pp (4/12) net+200/med+3.0) | — |
| asia | (°▼-9.9pp (3/13) net-238/med-8.5) | (°▼-40.3pp (0/1) net-6/med-5.5) |

- backtest payoff: right +725 / wrong -1151 / net -426 pts; median per fire -4.10 (n=51)
- backtest best call: 2026-07-31 05:00 +184.4pts remaining (episode 184.2pts, major)
- backtest worst false alarm: 2026-07-29 18:45 -160.1pts adverse
- forward payoff: right +21 / wrong -157 / net -136 pts; median per fire -4.05 (n=6)
- forward best call: 2026-08-17 16:10 +57.7pts remaining (episode 67.4pts)
- forward worst false alarm: 2026-08-18 07:00 -118.4pts adverse
- earliness (backtest): median 70.2 pts of move remaining at fire (n=7)

### H10
*In an established 1-minute trend, no-demand/no-supply prints in the trend's direction signal continuation.*
Grading: directional. Latest review: deprioritize (recommendation).

**H10** — session × window grid (cells as in the matrix):

| session | backtest | forward |
|---|---|---|
| whole | ▼-4.2pp (29/147) net-391/med+3.2 | ·+0.3pp (14/58) net+46/med+3.0 |
| london | ▼-16.0pp (4/39) net-463/med-12.5 | (°▲+9.2pp (3/10) net-36/med-11.8) |
| overlap | (°·-1.5pp (2/9) net-114/med-21.0) | (°▼-25.7pp (0/3) net+31/med+11.0) |
| ny_only | ▲+3.4pp (5/34) net+237/med+4.4 | (°▲+16.0pp (4/17) net+83/med+7.2) |
| dead | (°▼-16.4pp (0/14) net-275/med-13.8) | (°▼-14.8pp (0/8) net+8/med+1.2) |
| asia | ▲+2.3pp (18/51) net+224/med+6.3 | ▼-5.3pp (7/20) net-39/med-6.8 |

- backtest payoff: right +1730 / wrong -2121 / net -391 pts; median per fire +3.20 (n=147)
- backtest best call: 2026-07-27 03:28 +219.3pts remaining (episode 245.3pts, major)
- backtest worst false alarm: 2026-07-26 23:29 -102.8pts adverse
- forward payoff: right +433 / wrong -386 / net +46 pts; median per fire +3.00 (n=57)
- forward best call: 2026-08-18 05:07 +80.0pts remaining (episode 106.9pts, major)
- forward worst false alarm: 2026-08-17 09:56 -79.5pts adverse
- earliness (backtest): median 83.8 pts of move remaining at fire (n=10)

### H11
*Price entering a low-volume price zone traverses it faster than baseline; entering a high-volume node it stalls or reverses at above-baseline rates.*
Grading: directional. Latest review: keep-watching (recommendation).

**H11** — session × window grid (cells as in the matrix):

| session | backtest | forward |
|---|---|---|
| whole | ▼-3.6pp (15/74) net-452/med-6.0 | ·+0.1pp (22/92) net-344/med-6.6 |
| london | (°▼-4.9pp (3/14) net-472/med-58.8) | (°▼-9.4pp (5/44) net-190/med-11.2) |
| overlap | (°▼-17.5pp (1/16) net-166/med-13.2) | — |
| ny_only | (°▼-11.3pp (0/4) net-18/med-18.5) | — |
| dead | (°▼-2.1pp (1/7) net+1/med+4.1) | (°·+1.9pp (2/12) net-33/med-0.5) |
| asia | ▼-2.7pp (10/33) net+203/med-1.1 | ·+1.4pp (15/36) net-120/med-7.2 |

- backtest payoff: right +1359 / wrong -1811 / net -452 pts; median per fire -5.95 (n=74)
- backtest best call: 2026-07-29 04:03 +262.2pts remaining (episode 262.8pts, major)
- backtest worst false alarm: 2026-07-31 07:03 -171.6pts adverse
- forward payoff: right +756 / wrong -1099 / net -344 pts; median per fire -6.60 (n=92)
- forward best call: 2026-08-19 03:17 +82.8pts remaining (episode 94.3pts, major)
- forward worst false alarm: 2026-08-18 07:05 -87.8pts adverse
- earliness (backtest): median 104.9 pts of move remaining at fire (n=8)

### H12
*A zone showing repeated visits with elevated volume, diminishing range-per-unit-volume, and drying pullback volume precedes a directional move away from the zone in the absorber's direction.*
Grading: directional. Latest review: keep-watching (recommendation).

**H12** — session × window grid (cells as in the matrix):

| session | backtest | forward |
|---|---|---|
| whole | — | — |
| london | — | — |
| overlap | — | — |
| ny_only | — | — |
| dead | — | — |
| asia | — | — |



---

# nas100 (nas100fut) — PROVISIONAL

> **PROVISIONAL — validation pending (register 40 fence as amended 2026-08-19): replay-only study over the synced store; canonical status, live attachment, and Asia/pause-sensitive cell interpretation await this instrument's validation evening. EXPLORATORY first cross-instrument look — expectations deliberately unregistered; anything interesting becomes a pre-registered question before it becomes a claim. NO POOLING across instruments.**
>
> - drift-adjustment segments and engine tod baselines run on the provider/London trading-day structure; native cash-hour segmentation is part of this instrument's validation evening
> - sessions = the registered register-37 world-clock partition (native-tz, DST-proof) applied to this instrument's own bars; 'london' is not the home session of the US pairs
> - the forward window (>= go_live) is also a replay over the synced store — this instrument has NO live attachment yet

Store span (1M, close ts): 2026-07-19 22:02:00+00:00 → 2026-08-19 12:20:00+00:00. Volume type: real futures volume (register 40 first-sync sanity; canonical verdict at this instrument's validation evening).

## Summary Matrix (page 1)

Engine `f3eda9699` — OBSERVATIONAL signal scoreboard - move-detection, not trading; no fills exist here by construction; never validation (docs/hypothesis_lifecycle.md stage 4)

**Review labels are RECOMMENDATIONS — none actioned, review pending operator familiarity.** Cells: marker + precision LIFT vs that context's OWN chance rate, (hits/fires), payoff net/median points (directional rows; either-direction rows have no payoff by construction). ▲/▼ = beyond ±2pp of chance, · = within. (°…) = small-n (fires<20 or episodes<10): dimmed, excluded from any future label arithmetic. Read READING_GUIDE.md first; full detail in signal_scoreboard.json.

| H | label | backtest whole | backtest london | forward whole | forward london |
|---|---|---|---|---|---|
| *context* | | 115 ep; chance 22.0%dir/41.6%either | 41 ep; chance 30.9%dir/56.0%either | 25 ep; chance 22.4%dir/41.7%either | 10 ep; chance 28.8%dir/52.5%either |
| H1 | keep-watching | ▲+19.2pp (14/34) net+122/med-15.7 | (°▼-18.4pp (1/8) net-257/med-46.2) | (°▲+32.1pp (6/11) net+200/med+18.4) | (°▲+21.2pp (2/4) net+38/med+1.6) |
| H2 | promote-candidate | ▼-2.6pp (62/320) net-3528/med-1.4 | ▼-7.2pp (14/59) net-313/med-30.0 | ▲+4.3pp (28/105) net-256/med-2.1 | ▼-7.7pp (8/38) net+46/med+5.0 |
| H3 | keep-watching | (°▲+78.0pp (1/1) net+106/med+105.8) | (°▲+69.1pp (1/1) net+106/med+105.8) | — | — |
| H4 | keep-watching | — | — | (°▲+37.6pp (6/10) net-18/med-7.4) | (°▲+11.2pp (2/5) net+26/med+9.5) |
| H5 | keep-watching | — | — | — | — |
| H6 | keep-watching | ▼-8.1pp (9/29) [cls-chance 39.1% vs uncond 22.0%] net-232/med-11.8 | (°▼-38.2pp (0/5) [cls-chance 38.2% vs uncond 30.9%] net-719/med-105.3) | ▼-2.7pp (8/25) [cls-chance 34.7% vs uncond 22.4%] net-415/med-29.6 | (°▼-5.7pp (2/8) [cls-chance 30.7% vs uncond 28.8%] net-19/med-1.7) |
| H7 | keep-watching | ·+0.0pp (11/50) net+77/med-7.8 | (°▼-5.9pp (4/16) net-167/med-6.6) | (°▼-14.7pp (1/13) net-98/med-16.5) | (°▼-28.8pp (0/5) net-149/med-34.9) |
| H7 (either-dir) | keep-watching | ▲+4.4pp (23/50) | (°·+0.2pp (9/16)) | (°▼-3.2pp (5/13)) | (°▼-12.5pp (2/5)) |
| H8 | keep-watching | ·+1.8pp (139/320) | ▲+3.3pp (35/59) | ▲+9.7pp (54/105) | ▼-15.7pp (14/38) |
| H9 | keep-watching | ·+0.7pp (20/88) net+593/med-4.3 | (°▲+2.4pp (3/9) net+410/med+11.6) | ▼-7.9pp (9/62) net-34/med-6.7 | (°▲+71.2pp (1/1) net+49/med+49.1) |
| H10 | deprioritize | ▼-6.0pp (28/175) net+2743/med+15.3 | (°▼-17.6pp (2/15) net-356/med-1.7) | ▼-3.5pp (25/132) net-1380/med-8.1 | (°▲+30.0pp (10/17) net+208/med+2.7) |
| H11 | keep-watching | ▲+2.3pp (64/263) net+863/med+0.9 | ▼-2.3pp (26/91) net+264/med-3.9 | ·-0.3pp (32/145) net+536/med+1.7 | ▼-17.3pp (3/26) net-260/med-10.2 |
| H12 | keep-watching | — | — | — | — |
| **union coverage** | | 40.0% (46/115) | 31.7% (13/41) | 84.0% (21/25) | 90.0% (9/10) |

Not graded:  — see register entries.

## Hypothesis Cards (page 2)

### H1
*A climactic bar — extreme volume on a wide spread late in an extended move — marks exhaustion, and price then reverses against the climax direction.*
Grading: directional. Latest review: keep-watching (recommendation).

**H1** — session × window grid (cells as in the matrix):

| session | backtest | forward |
|---|---|---|
| whole | ▲+19.2pp (14/34) net+122/med-15.7 | (°▲+32.1pp (6/11) net+200/med+18.4) |
| london | (°▼-18.4pp (1/8) net-257/med-46.2) | (°▲+21.2pp (2/4) net+38/med+1.6) |
| overlap | — | — |
| ny_only | (°▲+50.6pp (7/11) net-215/med-87.5) | — |
| dead | (°·+0.9pp (1/8) net-181/med-23.6) | (°▲+64.6pp (3/4) net+150/med+51.1) |
| asia | (°▲+51.6pp (5/7) net+776/med+154.4) | (°▲+5.2pp (1/3) net+12/med+18.4) |

- backtest payoff: right +2899 / wrong -2777 / net +122 pts; median per fire -15.65 (n=34)
- backtest best call: 2026-07-29 18:02 +663.1pts remaining (episode 663.1pts, major)
- backtest worst false alarm: 2026-07-29 19:01 -712.5pts adverse
- forward payoff: right +274 / wrong -74 / net +200 pts; median per fire +18.40 (n=11)
- forward best call: 2026-08-17 10:30 +257.5pts remaining (episode 257.5pts, major)
- forward worst false alarm: 2026-08-18 02:17 -62.4pts adverse
- earliness (backtest): median 183.0 pts of move remaining at fire (n=8)

### H2
*A failed probe beyond a prior extreme — an upthrust above or spring below that closes back inside — reverses against the probe.*
Grading: directional. Latest review: promote-candidate (recommendation).

**H2** — session × window grid (cells as in the matrix):

| session | backtest | forward |
|---|---|---|
| whole | ▼-2.6pp (62/320) net-3528/med-1.4 | ▲+4.3pp (28/105) net-256/med-2.1 |
| london | ▼-7.2pp (14/59) net-313/med-30.0 | ▼-7.7pp (8/38) net+46/med+5.0 |
| overlap | (°▼-12.5pp (8/32) net-742/med-38.1) | — |
| ny_only | ▲+2.5pp (11/71) net-3199/med-7.4 | — |
| dead | ▲+5.1pp (8/48) net+874/med+2.4 | (°▲+32.5pp (3/7) net+43/med+15.9) |
| asia | ·-0.7pp (21/110) net-147/med+10.2 | ·+0.2pp (17/60) net-344/med-9.1 |

- backtest payoff: right +13405 / wrong -16933 / net -3528 pts; median per fire -1.35 (n=320)
- backtest best call: 2026-07-30 07:00 +812.7pts remaining (episode 832.8pts, major)
- backtest worst false alarm: 2026-07-29 19:00 -719.1pts adverse
- forward payoff: right +1962 / wrong -2218 / net -256 pts; median per fire -2.10 (n=105)
- forward best call: 2026-08-18 03:58 +206.5pts remaining (episode 236.7pts, major)
- forward worst false alarm: 2026-08-19 00:15 -135.2pts adverse
- earliness (backtest): median 111.6 pts of move remaining at fire (n=24)

### H3
*Repeated absorption — high effort with no result — at a price level precedes a breakout through that level.*
Grading: directional. Latest review: keep-watching (recommendation).

**H3** — session × window grid (cells as in the matrix):

| session | backtest | forward |
|---|---|---|
| whole | (°▲+78.0pp (1/1) net+106/med+105.8) | — |
| london | (°▲+69.1pp (1/1) net+106/med+105.8) | — |
| overlap | — | — |
| ny_only | — | — |
| dead | — | — |
| asia | — | — |

- backtest payoff: right +106 / wrong +0 / net +106 pts; median per fire +105.80 (n=1)

### H4
*In an established trend, a quiet (low-volume) pullback resolves with trend resumption.*
Grading: directional. Latest review: keep-watching (recommendation).

**H4** — session × window grid (cells as in the matrix):

| session | backtest | forward |
|---|---|---|
| whole | — | (°▲+37.6pp (6/10) net-18/med-7.4) |
| london | — | (°▲+11.2pp (2/5) net+26/med+9.5) |
| overlap | — | — |
| ny_only | — | — |
| dead | — | — |
| asia | — | (°▲+51.9pp (4/5) net-44/med-8.1) |

- forward payoff: right +65 / wrong -83 / net -18 pts; median per fire -7.40 (n=10)
- forward worst false alarm: 2026-08-17 06:55 -54.5pts adverse

### H5
*A buying climax that extends far above its trend mean mean-reverts (climax-extension fade; registered short-side only).*
Grading: directional. Latest review: keep-watching (recommendation).

**H5** — session × window grid (cells as in the matrix):

| session | backtest | forward |
|---|---|---|
| whole | — | — |
| london | — | — |
| overlap | — | — |
| ny_only | — | — |
| dead | — | — |
| asia | — | — |


### H6
*A wide-spread rejection bar at a session extreme (measured day-relative, volume-agnostic) reverses away from the extreme.*
Grading: directional. Latest review: keep-watching (recommendation).

**H6** — session × window grid (cells as in the matrix):

| session | backtest | forward |
|---|---|---|
| whole | ▼-8.1pp (9/29) [cls-chance 39.1% vs uncond 22.0%] net-232/med-11.8 | ▼-2.7pp (8/25) [cls-chance 34.7% vs uncond 22.4%] net-415/med-29.6 |
| london | (°▼-38.2pp (0/5) [cls-chance 38.2% vs uncond 30.9%] net-719/med-105.3) | (°▼-5.7pp (2/8) [cls-chance 30.7% vs uncond 28.8%] net-19/med-1.7) |
| overlap | (°▼-7.4pp (8/20) [cls-chance 47.4% vs uncond 37.5%] net+333/med+9.0) | (°·+0.0pp (4/8) [cls-chance 50.0% vs uncond 38.7%] net-215/med-54.5) |
| ny_only | — | (°·+0.0pp (0/1) [cls-chance 0.0% vs uncond 6.8%] net-31/med-30.7) |
| dead | (°▼-23.8pp (0/3) [cls-chance 23.8% vs uncond 11.6%] net+42/med+18.9) | (°▼-7.1pp (0/1) [cls-chance 7.1% vs uncond 10.4%] net+16/med+15.9) |
| asia | (°▲+74.8pp (1/1) [cls-chance 25.2% vs uncond 19.8%] net+112/med+111.8) | (°▼-3.1pp (2/7) [cls-chance 31.7% vs uncond 28.1%] net-167/med-69.2) |

- backtest payoff: right +1875 / wrong -2108 / net -232 pts; median per fire -11.80 (n=29)
- backtest best call: 2026-08-03 11:04 +303.5pts remaining (episode 396.3pts, major)
- backtest worst false alarm: 2026-07-27 13:46 -514.5pts adverse
- forward payoff: right +462 / wrong -877 / net -415 pts; median per fire -29.60 (n=25)
- forward best call: 2026-08-17 09:59 +201.6pts remaining (episode 257.5pts, major)
- forward worst false alarm: 2026-08-18 13:40 -161.0pts adverse
- earliness (backtest): median 78.8 pts of move remaining at fire (n=2)

### H7
*Quiet decline at a session extreme is disguised accumulation: effortless (low-volume) weakness reverses UP once selling fails to attract participation (mirror: quiet advance at a high reverses down).*
Grading: directional + either-direction (dual). Latest review: keep-watching (recommendation).

**H7** — session × window grid (cells as in the matrix):

| session | backtest | forward |
|---|---|---|
| whole | ·+0.0pp (11/50) net+77/med-7.8 | (°▼-14.7pp (1/13) net-98/med-16.5) |
| london | (°▼-5.9pp (4/16) net-167/med-6.6) | (°▼-28.8pp (0/5) net-149/med-34.9) |
| overlap | (°▲+25.0pp (5/8) net+464/med+8.3) | (°▲+61.3pp (1/1) net+105/med+105.1) |
| ny_only | (°▼-13.0pp (0/8) net-76/med-18.5) | (°▼-6.8pp (0/1) net+36/med+36.4) |
| dead | (°▼-11.6pp (0/5) net+53/med+23.0) | (°▼-10.4pp (0/1) net+5/med+5.3) |
| asia | (°▼-4.4pp (2/13) net-196/med-24.5) | (°▼-28.1pp (0/5) net-95/med-16.5) |

- backtest payoff: right +2351 / wrong -2274 / net +77 pts; median per fire -7.75 (n=50)
- backtest best call: 2026-07-29 09:26 +577.3pts remaining (episode 632.8pts, major)
- backtest worst false alarm: 2026-07-31 13:43 -365.8pts adverse
- forward payoff: right +198 / wrong -296 / net -98 pts; median per fire -16.50 (n=13)
- forward best call: 2026-08-19 11:02 +41.7pts remaining (episode 54.0pts)
- forward worst false alarm: 2026-08-18 07:34 -93.0pts adverse
- earliness (backtest): median 308.2 pts of move remaining at fire (n=7)

**H7 (either-dir)** — session × window grid (cells as in the matrix):

| session | backtest | forward |
|---|---|---|
| whole | ▲+4.4pp (23/50) | (°▼-3.2pp (5/13)) |
| london | (°·+0.2pp (9/16)) | (°▼-12.5pp (2/5)) |
| overlap | (°▲+30.0pp (8/8)) | (°▲+28.7pp (1/1)) |
| ny_only | (°▼-12.9pp (1/8)) | (°▼-13.6pp (0/1)) |
| dead | (°▼-22.4pp (0/5)) | (°▼-18.5pp (0/1)) |
| asia | (°·-0.7pp (5/13)) | (°▼-13.7pp (2/5)) |

- backtest payoff: n/a by construction (either-direction)
- backtest best call: 2026-07-29 09:26 +577.3pts remaining (episode 632.8pts, major)
- backtest worst false alarm: 2026-07-29 02:54 -123.2pts adverse
- forward payoff: n/a by construction (either-direction)
- forward best call: 2026-08-19 11:02 +41.7pts remaining (episode 54.0pts)
- forward worst false alarm: 2026-08-19 01:33 -58.0pts adverse
- earliness (backtest): median 170.9 pts of move remaining at fire (n=14)

### H8
*Reversal-signature bar anatomy (upthrust/spring) predicts imminent range expansion irrespective of direction.*
Grading: either-direction. Latest review: keep-watching (recommendation).

**H8** — session × window grid (cells as in the matrix):

| session | backtest | forward |
|---|---|---|
| whole | ·+1.8pp (139/320) | ▲+9.7pp (54/105) |
| london | ▲+3.3pp (35/59) | ▼-15.7pp (14/38) |
| overlap | (°▼-4.4pp (21/32)) | — |
| ny_only | ▲+18.3pp (31/71) | — |
| dead | ▲+2.6pp (12/48) | (°▲+52.9pp (5/7)) |
| asia | ▼-2.8pp (40/110) | ▲+4.6pp (35/60) |

- backtest payoff: n/a by construction (either-direction)
- backtest best call: 2026-07-30 06:39 +793.0pts remaining (episode 832.8pts, major)
- backtest worst false alarm: 2026-07-29 19:48 -233.6pts adverse
- forward payoff: n/a by construction (either-direction)
- forward best call: 2026-08-18 11:34 +234.2pts remaining (episode 234.0pts, major)
- forward worst false alarm: 2026-08-19 06:52 -66.7pts adverse
- earliness (backtest): median 130.6 pts of move remaining at fire (n=31)

### H9
*Persistent lower-TF directional pressure that recruits expanding participation at the parent timeframe precedes continuation beyond what the parent label alone predicts; pressure without participation expansion does not.*
Grading: directional. Latest review: keep-watching (recommendation).

**H9** — session × window grid (cells as in the matrix):

| session | backtest | forward |
|---|---|---|
| whole | ·+0.7pp (20/88) net+593/med-4.3 | ▼-7.9pp (9/62) net-34/med-6.7 |
| london | (°▲+2.4pp (3/9) net+410/med+11.6) | (°▲+71.2pp (1/1) net+49/med+49.1) |
| overlap | (°▲+12.5pp (5/10) net+540/med+51.3) | (°▼-22.0pp (1/6) net-28/med-10.2) |
| ny_only | ▼-5.0pp (2/25) net-148/med-7.0 | (°▲+2.7pp (2/21) net-109/med-9.7) |
| dead | (°▲+17.8pp (5/17) net+98/med-5.5) | (°▼-10.4pp (0/5) net+23/med+6.0) |
| asia | ·-1.3pp (5/27) net-307/med-10.2 | ▼-10.9pp (5/29) net+30/med-12.4 |

- backtest payoff: right +3019 / wrong -2427 / net +593 pts; median per fire -4.35 (n=88)
- backtest best call: 2026-08-03 03:30 +174.2pts remaining (episode 209.2pts, major)
- backtest worst false alarm: 2026-07-29 18:45 -500.8pts adverse
- forward payoff: right +813 / wrong -847 / net -34 pts; median per fire -6.70 (n=61)
- forward best call: 2026-08-17 04:30 +90.9pts remaining (episode 90.6pts, major)
- forward worst false alarm: 2026-08-17 16:25 -98.9pts adverse
- earliness (backtest): median 116.8 pts of move remaining at fire (n=6)

### H10
*In an established 1-minute trend, no-demand/no-supply prints in the trend's direction signal continuation.*
Grading: directional. Latest review: deprioritize (recommendation).

**H10** — session × window grid (cells as in the matrix):

| session | backtest | forward |
|---|---|---|
| whole | ▼-6.0pp (28/175) net+2743/med+15.3 | ▼-3.5pp (25/132) net-1380/med-8.1 |
| london | (°▼-17.6pp (2/15) net-356/med-1.7) | (°▲+30.0pp (10/17) net+208/med+2.7) |
| overlap | (°▼-37.5pp (0/18) net+764/med+45.5) | (°▼-32.8pp (1/17) net-825/med-53.5) |
| ny_only | ▼-6.8pp (3/48) net+398/med+12.5 | (°▲+6.8pp (3/22) net-166/med-15.8) |
| dead | (°·+0.9pp (2/16) net+551/med+8.9) | (°▼-10.4pp (0/10) net-88/med-5.7) |
| asia | ▲+7.1pp (21/78) net+1385/med+15.6 | ▼-11.4pp (11/66) net-508/med-7.0 |

- backtest payoff: right +4792 / wrong -2049 / net +2743 pts; median per fire +15.30 (n=175)
- backtest best call: 2026-08-03 03:44 +199.5pts remaining (episode 209.2pts, major)
- backtest worst false alarm: 2026-07-27 12:56 -252.9pts adverse
- forward payoff: right +1008 / wrong -2389 / net -1380 pts; median per fire -8.05 (n=132)
- forward best call: 2026-08-17 04:16 +81.2pts remaining (episode 90.6pts, major)
- forward worst false alarm: 2026-08-18 01:03 -109.1pts adverse
- earliness (backtest): median 132.5 pts of move remaining at fire (n=6)

### H11
*Price entering a low-volume price zone traverses it faster than baseline; entering a high-volume node it stalls or reverses at above-baseline rates.*
Grading: directional. Latest review: keep-watching (recommendation).

**H11** — session × window grid (cells as in the matrix):

| session | backtest | forward |
|---|---|---|
| whole | ▲+2.3pp (64/263) net+863/med+0.9 | ·-0.3pp (32/145) net+536/med+1.7 |
| london | ▼-2.3pp (26/91) net+264/med-3.9 | ▼-17.3pp (3/26) net-260/med-10.2 |
| overlap | (°▲+2.5pp (8/20) net-137/med-23.4) | (°·-1.2pp (6/16) net+506/med+50.1) |
| ny_only | ▲+14.6pp (8/29) net+826/med+77.1 | (°▼-2.9pp (2/51) net-148/med-1.6) |
| dead | ▲+10.8pp (13/58) net+874/med-3.1 | (°▲+22.9pp (4/12) net-119/med-10.8) |
| asia | ▼-6.0pp (9/65) net-964/med+3.6 | ▲+14.4pp (17/40) net+558/med+13.2 |

- backtest payoff: right +10765 / wrong -9902 / net +863 pts; median per fire +0.90 (n=262)
- backtest best call: 2026-07-30 07:02 +741.2pts remaining (episode 832.8pts, major)
- backtest worst false alarm: 2026-07-29 13:50 -332.3pts adverse
- forward payoff: right +2711 / wrong -2174 / net +536 pts; median per fire +1.70 (n=145)
- forward best call: 2026-08-17 09:59 +201.6pts remaining (episode 257.5pts, major)
- forward worst false alarm: 2026-08-18 14:13 -105.3pts adverse
- earliness (backtest): median 176.0 pts of move remaining at fire (n=14)

### H12
*A zone showing repeated visits with elevated volume, diminishing range-per-unit-volume, and drying pullback volume precedes a directional move away from the zone in the absorber's direction.*
Grading: directional. Latest review: keep-watching (recommendation).

**H12** — session × window grid (cells as in the matrix):

| session | backtest | forward |
|---|---|---|
| whole | — | — |
| london | — | — |
| overlap | — | — |
| ny_only | — | — |
| dead | — | — |
| asia | — | — |



---

# us30 (us30fut) — PROVISIONAL

> **PROVISIONAL — validation pending (register 40 fence as amended 2026-08-19): replay-only study over the synced store; canonical status, live attachment, and Asia/pause-sensitive cell interpretation await this instrument's validation evening. EXPLORATORY first cross-instrument look — expectations deliberately unregistered; anything interesting becomes a pre-registered question before it becomes a claim. NO POOLING across instruments.**
>
> - drift-adjustment segments and engine tod baselines run on the provider/London trading-day structure; native cash-hour segmentation is part of this instrument's validation evening
> - sessions = the registered register-37 world-clock partition (native-tz, DST-proof) applied to this instrument's own bars; 'london' is not the home session of the US pairs
> - the forward window (>= go_live) is also a replay over the synced store — this instrument has NO live attachment yet

Store span (1M, close ts): 2026-07-19 22:02:00+00:00 → 2026-08-19 12:21:00+00:00. Volume type: real futures volume (register 40 first-sync sanity; canonical verdict at this instrument's validation evening).

## Summary Matrix (page 1)

Engine `f3eda9699` — OBSERVATIONAL signal scoreboard - move-detection, not trading; no fills exist here by construction; never validation (docs/hypothesis_lifecycle.md stage 4)

**Review labels are RECOMMENDATIONS — none actioned, review pending operator familiarity.** Cells: marker + precision LIFT vs that context's OWN chance rate, (hits/fires), payoff net/median points (directional rows; either-direction rows have no payoff by construction). ▲/▼ = beyond ±2pp of chance, · = within. (°…) = small-n (fires<20 or episodes<10): dimmed, excluded from any future label arithmetic. Read READING_GUIDE.md first; full detail in signal_scoreboard.json.

| H | label | backtest whole | backtest london | forward whole | forward london |
|---|---|---|---|---|---|
| *context* | | 110 ep; chance 24.0%dir/44.5%either | 36 ep; chance 36.3%dir/65.9%either | 26 ep; chance 23.2%dir/44.5%either | 8 ep; chance 33.7%dir/63.8%either |
| H1 | keep-watching | ▲+8.7pp (16/49) net-83/med-8.0 | (°▼-6.9pp (5/17) net-113/med-17.5) | ▲+10.1pp (12/36) net-238/med-10.0 | (°▲+2.7pp (4/11) net-54/med-10.5) |
| H2 | promote-candidate | ·+1.6pp (72/281) net-2432/med-4.0 | ▼-2.4pp (21/62) net-337/med-20.0 | ▲+7.4pp (33/108) net-97/med+0.8 | (°·-0.4pp (12/36) net-153/med-5.8) |
| H3 | keep-watching | (°·+1.0pp (1/4) net+59/med+13.2) | (°▼-36.3pp (0/2) net-22/med-11.0) | — | — |
| H4 | keep-watching | (°▲+14.5pp (5/13) net+194/med+15.0) | (°▲+35.1pp (5/7) net+392/med+71.0) | — | — |
| H5 | keep-watching | (°▼-24.0pp (0/1) net-135/med-135.0) | (°▼-36.3pp (0/1) net-135/med-135.0) | — | — |
| H6 | keep-watching | ▼-21.3pp (10/52) [cls-chance 40.5% vs uncond 24.0%] net-1151/med-25.2 | ▼-28.3pp (3/24) [cls-chance 40.8% vs uncond 36.3%] net-664/med-30.0 | ▲+16.3pp (11/20) [cls-chance 38.7% vs uncond 23.2%] net+105/med+9.5 | (°▲+52.5pp (9/10) [cls-chance 37.5% vs uncond 33.7%] net+372/med+32.0) |
| H7 | keep-watching | ▼-2.0pp (9/41) net+205/med-9.0 | (°▼-5.1pp (5/16) net-161/med-7.0) | (°▲+12.5pp (5/14) net+122/med+6.5) | (°▲+6.3pp (2/5) net+33/med+9.0) |
| H7 (either-dir) | keep-watching | ▼-3.0pp (17/41) | (°▲+2.9pp (11/16)) | (°▲+12.6pp (8/14)) | (°▲+16.2pp (4/5)) |
| H8 | keep-watching | ▲+7.5pp (146/281) | ▲+6.7pp (45/62) | ▲+8.3pp (57/108) | (°▼-8.2pp (20/36)) |
| H9 | keep-watching | ·-1.5pp (9/40) net-353/med-14.7 | (°▼-3.0pp (1/3) net-198/med-61.5) | (°▼-23.2pp (0/15) net-618/med-37.0) | (°▼-33.7pp (0/6) net-464/med-86.8) |
| H10 | deprioritize | ·+0.0pp (37/154) net+1774/med+11.0 | ▲+3.7pp (16/40) net+1480/med+27.5 | ▼-7.7pp (20/129) net-284/med-1.0 | (°▼-13.7pp (5/25) net-242/med-18.5) |
| H11 | keep-watching | ▲+3.4pp (113/413) net+1254/med+3.0 | ·+1.1pp (61/163) net-404/med+5.0 | ▲+3.8pp (54/200) net-90/med-5.0 | (°·+0.0pp (31/92) net+99/med-4.5) |
| H12 | keep-watching | — | — | — | — |
| **union coverage** | | 40.0% (44/110) | 33.3% (12/36) | 88.5% (23/26) | 87.5% (7/8) |

Not graded:  — see register entries.

## Hypothesis Cards (page 2)

### H1
*A climactic bar — extreme volume on a wide spread late in an extended move — marks exhaustion, and price then reverses against the climax direction.*
Grading: directional. Latest review: keep-watching (recommendation).

**H1** — session × window grid (cells as in the matrix):

| session | backtest | forward |
|---|---|---|
| whole | ▲+8.7pp (16/49) net-83/med-8.0 | ▲+10.1pp (12/36) net-238/med-10.0 |
| london | (°▼-6.9pp (5/17) net-113/med-17.5) | (°▲+2.7pp (4/11) net-54/med-10.5) |
| overlap | — | (°▼-27.5pp (0/1) net-67/med-67.0) |
| ny_only | (°▲+40.3pp (7/13) net-62/med-15.5) | — |
| dead | (°▼-7.1pp (0/7) net-157/med-8.0) | (°▲+19.4pp (1/4) net+22/med+8.2) |
| asia | (°▲+9.2pp (4/12) net+248/med+27.0) | ▲+7.7pp (7/20) net-140/med-7.8 |

- backtest payoff: right +1958 / wrong -2041 / net -83 pts; median per fire -8.00 (n=49)
- backtest best call: 2026-07-29 16:24 +398.0pts remaining (episode 602.0pts, major)
- backtest worst false alarm: 2026-07-29 19:22 -450.0pts adverse
- forward payoff: right +444 / wrong -683 / net -238 pts; median per fire -10.00 (n=36)
- forward best call: 2026-08-17 10:30 +249.0pts remaining (episode 249.0pts, major)
- forward worst false alarm: 2026-08-18 14:54 -112.0pts adverse
- earliness (backtest): median 128.0 pts of move remaining at fire (n=10)

### H2
*A failed probe beyond a prior extreme — an upthrust above or spring below that closes back inside — reverses against the probe.*
Grading: directional. Latest review: promote-candidate (recommendation).

**H2** — session × window grid (cells as in the matrix):

| session | backtest | forward |
|---|---|---|
| whole | ·+1.6pp (72/281) net-2432/med-4.0 | ▲+7.4pp (33/108) net-97/med+0.8 |
| london | ▼-2.4pp (21/62) net-337/med-20.0 | (°·-0.4pp (12/36) net-153/med-5.8) |
| overlap | (°▲+3.7pp (8/22) net-1080/med-77.8) | (°▼-27.5pp (0/2) net-184/med-92.2) |
| ny_only | ▲+23.2pp (22/60) net-1257/med-11.1 | (°▼-12.0pp (0/1) net+8/med+7.5) |
| dead | ▲+2.7pp (4/41) net-18/med-2.6 | (°▲+11.1pp (2/12) net+92/med+3.0) |
| asia | ▼-6.4pp (17/96) net+261/med+1.2 | ▲+6.0pp (19/57) net+142/med+1.0 |

- backtest payoff: right +10496 / wrong -12928 / net -2432 pts; median per fire -4.00 (n=281)
- backtest best call: 2026-07-29 06:34 +888.5pts remaining (episode 948.5pts, major)
- backtest worst false alarm: 2026-07-29 18:55 -695.0pts adverse
- forward payoff: right +1528 / wrong -1626 / net -97 pts; median per fire +0.75 (n=108)
- forward best call: 2026-08-18 10:11 +230.5pts remaining (episode 240.0pts, major)
- forward worst false alarm: 2026-08-18 15:06 -141.0pts adverse
- earliness (backtest): median 105.2 pts of move remaining at fire (n=22)

### H3
*Repeated absorption — high effort with no result — at a price level precedes a breakout through that level.*
Grading: directional. Latest review: keep-watching (recommendation).

**H3** — session × window grid (cells as in the matrix):

| session | backtest | forward |
|---|---|---|
| whole | (°·+1.0pp (1/4) net+59/med+13.2) | — |
| london | (°▼-36.3pp (0/2) net-22/med-11.0) | — |
| overlap | — | — |
| ny_only | — | — |
| dead | — | — |
| asia | (°▲+25.9pp (1/2) net+81/med+40.5) | — |

- backtest payoff: right +99 / wrong -40 / net +59 pts; median per fire +13.25 (n=4)
- backtest worst false alarm: 2026-07-30 09:10 -83.5pts adverse

### H4
*In an established trend, a quiet (low-volume) pullback resolves with trend resumption.*
Grading: directional. Latest review: keep-watching (recommendation).

**H4** — session × window grid (cells as in the matrix):

| session | backtest | forward |
|---|---|---|
| whole | (°▲+14.5pp (5/13) net+194/med+15.0) | — |
| london | (°▲+35.1pp (5/7) net+392/med+71.0) | — |
| overlap | (°▼-32.7pp (0/1) net-166/med-165.5) | — |
| ny_only | — | — |
| dead | (°▼-7.1pp (0/5) net-33/med-6.9) | — |
| asia | — | — |

- backtest payoff: right +410 / wrong -216 / net +194 pts; median per fire +15.00 (n=13)
- backtest best call: 2026-08-03 22:58 +63.0pts remaining (episode 86.0pts)
- backtest worst false alarm: 2026-08-03 14:10 -174.0pts adverse
- earliness (backtest): median 63.0 pts of move remaining at fire (n=1)

### H5
*A buying climax that extends far above its trend mean mean-reverts (climax-extension fade; registered short-side only).*
Grading: directional. Latest review: keep-watching (recommendation).

**H5** — session × window grid (cells as in the matrix):

| session | backtest | forward |
|---|---|---|
| whole | (°▼-24.0pp (0/1) net-135/med-135.0) | — |
| london | (°▼-36.3pp (0/1) net-135/med-135.0) | — |
| overlap | — | — |
| ny_only | — | — |
| dead | — | — |
| asia | — | — |

- backtest payoff: right +0 / wrong -135 / net -135 pts; median per fire -135.00 (n=1)
- backtest worst false alarm: 2026-07-28 11:30 -135.0pts adverse

### H6
*A wide-spread rejection bar at a session extreme (measured day-relative, volume-agnostic) reverses away from the extreme.*
Grading: directional. Latest review: keep-watching (recommendation).

**H6** — session × window grid (cells as in the matrix):

| session | backtest | forward |
|---|---|---|
| whole | ▼-21.3pp (10/52) [cls-chance 40.5% vs uncond 24.0%] net-1151/med-25.2 | ▲+16.3pp (11/20) [cls-chance 38.7% vs uncond 23.2%] net+105/med+9.5 |
| london | ▼-28.3pp (3/24) [cls-chance 40.8% vs uncond 36.3%] net-664/med-30.0 | (°▲+52.5pp (9/10) [cls-chance 37.5% vs uncond 33.7%] net+372/med+32.0) |
| overlap | (°▼-18.9pp (4/18) [cls-chance 41.1% vs uncond 32.7%] net+234/med+6.8) | (°▼-19.5pp (2/9) [cls-chance 41.7% vs uncond 27.5%] net-262/med-14.5) |
| ny_only | (°▲+7.7pp (3/6) [cls-chance 42.3% vs uncond 13.5%] net-856/med-92.0) | — |
| dead | (°▼-11.8pp (0/3) [cls-chance 11.8% vs uncond 7.1%] net+58/med+5.5) | — |
| asia | (°▼-41.0pp (0/1) [cls-chance 41.0% vs uncond 24.1%] net+77/med+77.0) | (°▼-43.6pp (0/1) [cls-chance 43.6% vs uncond 27.3%] net-4/med-4.5) |

- backtest payoff: right +1398 / wrong -2549 / net -1151 pts; median per fire -25.25 (n=52)
- backtest best call: 2026-07-28 12:23 +197.5pts remaining (episode 226.5pts, major)
- backtest worst false alarm: 2026-07-28 15:11 -288.5pts adverse
- forward payoff: right +470 / wrong -365 / net +105 pts; median per fire +9.50 (n=20)
- forward best call: 2026-08-18 07:39 +108.4pts remaining (episode 148.4pts, major)
- forward worst false alarm: 2026-08-17 14:06 -119.5pts adverse
- earliness (backtest): median 43.0 pts of move remaining at fire (n=3)

### H7
*Quiet decline at a session extreme is disguised accumulation: effortless (low-volume) weakness reverses UP once selling fails to attract participation (mirror: quiet advance at a high reverses down).*
Grading: directional + either-direction (dual). Latest review: keep-watching (recommendation).

**H7** — session × window grid (cells as in the matrix):

| session | backtest | forward |
|---|---|---|
| whole | ▼-2.0pp (9/41) net+205/med-9.0 | (°▲+12.5pp (5/14) net+122/med+6.5) |
| london | (°▼-5.1pp (5/16) net-161/med-7.0) | (°▲+6.3pp (2/5) net+33/med+9.0) |
| overlap | (°▲+34.0pp (2/3) net+471/med+272.0) | — |
| ny_only | (°▼-13.5pp (0/4) net-21/med-5.0) | (°▼-12.0pp (0/5) net-16/med-15.5) |
| dead | (°▼-7.1pp (0/4) net-1/med-2.0) | — |
| asia | (°▼-9.8pp (2/14) net-84/med-13.8) | (°▲+47.7pp (3/4) net+105/med+22.2) |

- backtest payoff: right +1609 / wrong -1404 / net +205 pts; median per fire -9.00 (n=41)
- backtest best call: 2026-07-31 09:51 +528.0pts remaining (episode 572.5pts, major)
- backtest worst false alarm: 2026-07-28 10:48 -242.0pts adverse
- forward payoff: right +290 / wrong -168 / net +122 pts; median per fire +6.50 (n=14)
- forward best call: 2026-08-18 18:14 +56.5pts remaining (episode 66.5pts)
- forward worst false alarm: 2026-08-18 08:33 -63.0pts adverse
- earliness (backtest): median 110.5 pts of move remaining at fire (n=9)

**H7 (either-dir)** — session × window grid (cells as in the matrix):

| session | backtest | forward |
|---|---|---|
| whole | ▼-3.0pp (17/41) | (°▲+12.6pp (8/14)) |
| london | (°▲+2.9pp (11/16)) | (°▲+16.2pp (4/5)) |
| overlap | (°▲+6.4pp (2/3)) | — |
| ny_only | (°▼-26.1pp (0/4)) | (°▼-24.1pp (0/5)) |
| dead | (°▼-14.3pp (0/4)) | — |
| asia | (°▼-16.9pp (4/14)) | (°▲+46.9pp (4/4)) |

- backtest payoff: n/a by construction (either-direction)
- backtest best call: 2026-07-31 09:51 +528.0pts remaining (episode 572.5pts, major)
- backtest worst false alarm: 2026-07-30 16:13 -170.0pts adverse
- forward payoff: n/a by construction (either-direction)
- forward best call: 2026-08-18 06:57 +87.4pts remaining (episode 148.4pts, major)
- forward worst false alarm: 2026-08-18 18:14 -36.5pts adverse
- earliness (backtest): median 85.0 pts of move remaining at fire (n=11)

### H8
*Reversal-signature bar anatomy (upthrust/spring) predicts imminent range expansion irrespective of direction.*
Grading: either-direction. Latest review: keep-watching (recommendation).

**H8** — session × window grid (cells as in the matrix):

| session | backtest | forward |
|---|---|---|
| whole | ▲+7.5pp (146/281) | ▲+8.3pp (57/108) |
| london | ▲+6.7pp (45/62) | (°▼-8.2pp (20/36)) |
| overlap | (°▲+21.5pp (18/22)) | (°▲+50.9pp (2/2)) |
| ny_only | ▲+37.2pp (38/60) | (°▼-24.1pp (0/1)) |
| dead | ▲+10.1pp (10/41) | (°▲+5.5pp (2/12)) |
| asia | ▼-9.0pp (35/96) | ▲+4.8pp (33/57) |

- backtest payoff: n/a by construction (either-direction)
- backtest best call: 2026-07-29 06:34 +888.5pts remaining (episode 948.5pts, major)
- backtest worst false alarm: 2026-07-27 16:47 -152.0pts adverse
- forward payoff: n/a by construction (either-direction)
- forward best call: 2026-08-18 10:11 +230.5pts remaining (episode 240.0pts, major)
- forward worst false alarm: 2026-08-17 17:28 -72.0pts adverse
- earliness (backtest): median 99.2 pts of move remaining at fire (n=26)

### H9
*Persistent lower-TF directional pressure that recruits expanding participation at the parent timeframe precedes continuation beyond what the parent label alone predicts; pressure without participation expansion does not.*
Grading: directional. Latest review: keep-watching (recommendation).

**H9** — session × window grid (cells as in the matrix):

| session | backtest | forward |
|---|---|---|
| whole | ·-1.5pp (9/40) net-353/med-14.7 | (°▼-23.2pp (0/15) net-618/med-37.0) |
| london | (°▼-3.0pp (1/3) net-198/med-61.5) | (°▼-33.7pp (0/6) net-464/med-86.8) |
| overlap | (°▼-32.7pp (0/2) net-19/med-9.5) | — |
| ny_only | (°▼-3.5pp (1/10) net-196/med-66.5) | (°▼-12.0pp (0/3) net-38/med-2.0) |
| dead | (°▼-7.1pp (0/7) net+60/med+15.5) | (°▼-5.6pp (0/2) net-4/med-3.5) |
| asia | (°▲+14.8pp (7/18) net-1/med-11.2) | (°▼-27.3pp (0/4) net-113/med-31.5) |

- backtest payoff: right +876 / wrong -1229 / net -353 pts; median per fire -14.70 (n=38)
- backtest best call: 2026-08-03 05:40 +463.0pts remaining (episode 472.0pts, major)
- backtest worst false alarm: 2026-08-03 17:15 -176.0pts adverse
- forward payoff: right +32 / wrong -650 / net -618 pts; median per fire -37.00 (n=14)
- forward best call: 2026-08-18 07:00 +64.9pts remaining (episode 148.4pts, major)
- forward worst false alarm: 2026-08-18 07:00 -127.5pts adverse
- earliness (backtest): median 351.5 pts of move remaining at fire (n=2)

### H10
*In an established 1-minute trend, no-demand/no-supply prints in the trend's direction signal continuation.*
Grading: directional. Latest review: deprioritize (recommendation).

**H10** — session × window grid (cells as in the matrix):

| session | backtest | forward |
|---|---|---|
| whole | ·+0.0pp (37/154) net+1774/med+11.0 | ▼-7.7pp (20/129) net-284/med-1.0 |
| london | ▲+3.7pp (16/40) net+1480/med+27.5 | (°▼-13.7pp (5/25) net-242/med-18.5) |
| overlap | (°▼-32.7pp (0/5) net+36/med+33.0) | (°▼-27.5pp (0/1) net+72/med+71.5) |
| ny_only | ·+1.9pp (4/26) net-348/med+48.8 | (°▼-7.8pp (2/48) net-509/med-5.5) |
| dead | ▼-7.1pp (0/20) net-74/med-5.7 | (°▼-5.6pp (0/18) net-82/med-6.8) |
| asia | ▲+2.9pp (17/63) net+680/med+8.0 | ▲+7.8pp (13/37) net+477/med+9.0 |

- backtest payoff: right +4228 / wrong -2454 / net +1774 pts; median per fire +11.00 (n=154)
- backtest best call: 2026-07-29 06:18 +859.5pts remaining (episode 948.5pts, major)
- backtest worst false alarm: 2026-08-03 17:10 -197.0pts adverse
- forward payoff: right +1546 / wrong -1830 / net -284 pts; median per fire -1.00 (n=129)
- forward best call: 2026-08-17 09:48 +176.5pts remaining (episode 249.0pts, major)
- forward worst false alarm: 2026-08-18 12:33 -113.5pts adverse
- earliness (backtest): median 87.5 pts of move remaining at fire (n=11)

### H11
*Price entering a low-volume price zone traverses it faster than baseline; entering a high-volume node it stalls or reverses at above-baseline rates.*
Grading: directional. Latest review: keep-watching (recommendation).

**H11** — session × window grid (cells as in the matrix):

| session | backtest | forward |
|---|---|---|
| whole | ▲+3.4pp (113/413) net+1254/med+3.0 | ▲+3.8pp (54/200) net-90/med-5.0 |
| london | ·+1.1pp (61/163) net-404/med+5.0 | (°·+0.0pp (31/92) net+99/med-4.5) |
| overlap | (°▲+21.1pp (14/26) net+491/med+4.0) | (°▲+12.5pp (6/15) net+262/med+25.5) |
| ny_only | ·-1.6pp (5/42) net+1037/med+15.2 | (°▲+2.3pp (2/14) net-116/med-7.8) |
| dead | ▲+14.9pp (11/50) net+478/med+1.2 | (°▼-5.6pp (0/13) net-94/med-6.5) |
| asia | ▼-7.4pp (22/132) net-348/med+2.0 | ▼-4.6pp (15/66) net-240/med-4.2 |

- backtest payoff: right +12694 / wrong -11440 / net +1254 pts; median per fire +3.00 (n=413)
- backtest best call: 2026-07-29 06:20 +858.0pts remaining (episode 948.5pts, major)
- backtest worst false alarm: 2026-07-31 13:24 -492.5pts adverse
- forward payoff: right +3009 / wrong -3098 / net -90 pts; median per fire -5.00 (n=200)
- forward best call: 2026-08-18 09:56 +194.0pts remaining (episode 240.0pts, major)
- forward worst false alarm: 2026-08-18 12:53 -167.0pts adverse
- earliness (backtest): median 90.5 pts of move remaining at fire (n=23)

### H12
*A zone showing repeated visits with elevated volume, diminishing range-per-unit-volume, and drying pullback volume precedes a directional move away from the zone in the absorber's direction.*
Grading: directional. Latest review: keep-watching (recommendation).

**H12** — session × window grid (cells as in the matrix):

| session | backtest | forward |
|---|---|---|
| whole | — | — |
| london | — | — |
| overlap | — | — |
| ny_only | — | — |
| dead | — | — |
| asia | — | — |



---

Appendix: the per-session detail beyond London and every horizon-mark payoff live in signal_scoreboard.json (generated, same run).