# Hypothesis Performance — Per-Instrument

Engine `98e5c99b0` — register 40 fence as amended 2026-08-19 (operator): one section per instrument, each computed only from that instrument's own store and native calendar; uk100 canonical, ger40/nas100/us30 PROVISIONAL (validation pending). Numbers are NEVER pooled across instruments — cross-instrument aggregation is a future registration. This first cross-instrument read is EXPLORATORY: expectations deliberately unregistered; anything interesting becomes a pre-registered question before it becomes a claim.

---

# uk100 (uk100fut) — CANONICAL

Store span (1M, close ts): 2026-07-12 22:06:00+00:00 → 2026-08-20 13:31:00+00:00. Volume type: real futures volume (step-zero audit).

## Summary Matrix (page 1)

Engine `98e5c99b0` — OBSERVATIONAL signal scoreboard - move-detection, not trading; no fills exist here by construction; never validation (docs/hypothesis_lifecycle.md stage 4)

**Review labels are RECOMMENDATIONS — none actioned, review pending operator familiarity.** Cells: marker + precision LIFT vs that context's OWN chance rate, (hits/fires), payoff net/median points (directional rows; either-direction rows have no payoff by construction). ▲/▼ = beyond ±2pp of chance, · = within. (°…) = small-n (fires<20 or episodes<10): dimmed, excluded from any future label arithmetic. Read READING_GUIDE.md first; full detail in hypothesis_performance.json.

| H | label | backtest whole | backtest london | forward whole | forward london |
|---|---|---|---|---|---|
| *context* | | 180 ep; chance 23.6%dir/44.3%either | 52 ep; chance 24.8%dir/47.1%either | 42 ep; chance 25.1%dir/45.3%either | 11 ep; chance 25.5%dir/47.6%either |
| S0-H1 | keep-watching | ·-0.4pp (16/69) net+194/med+2.8 | ▲+7.0pp (7/22) net+133/med+3.0 | ▲+5.2pp (10/33) net+25/med-0.3 | (°▲+12.0pp (3/8) net+3/med+1.1) |
| S1-H1 | keep-watching | (°▼-3.6pp (1/5) net+9/med+3.0) | — | (°▲+41.6pp (2/3) net+28/med+10.5) | (°▲+41.2pp (2/3) net+28/med+10.5) |
| S0-H2 | promote-candidate | ·+1.2pp (86/347) net+781/med+1.5 | ▲+6.4pp (25/80) net+521/med+9.2 | ▲+3.4pp (35/123) net-76/med-1.0 | ▼-2.6pp (8/35) net-8/med-1.0 |
| S1-H2 | promote-candidate | ·+0.6pp (61/252) net+540/med+0.9 | ▲+5.7pp (18/59) net+559/med+12.0 | ▲+4.3pp (32/109) net-98/med-1.0 | ▼-2.9pp (7/31) net-19/med-1.0 |
| S0-H3 | keep-watching | — | — | (°▲+3.5pp (2/7) net-26/med-0.5) | (°▲+7.8pp (1/3) net-24/med-5.0) |
| S0-H4 | keep-watching | (°▼-23.6pp (0/7) net+14/med+0.5) | (°▼-24.8pp (0/1) net+6/med+5.5) | — | — |
| S0-H5 | keep-watching | — | — | — | — |
| S0-H6 | keep-watching | ▲+8.1pp (27/59) [cls-chance 37.7% vs uncond 23.6%] net+391/med+5.7 | ▲+20.7pp (18/31) [cls-chance 37.4% vs uncond 24.8%] net+282/med+16.0 | (°▲+11.4pp (8/15) [cls-chance 41.9% vs uncond 25.1%] net+71/med+6.0) | (°▲+11.4pp (5/10) [cls-chance 38.6% vs uncond 25.5%] net+52/med+4.3) |
| S0-H7 | keep-watching | ▲+5.9pp (33/112) net+7/med+2.8 | ▲+2.0pp (11/41) net-217/med+2.7 | ·-1.8pp (7/30) net+51/med+1.9 | (°▲+5.7pp (5/16) net+12/med-2.5) |
| S0-H7 (either-dir) | keep-watching | ▲+7.5pp (58/112) | ·+1.7pp (20/41) | ▼-2.0pp (13/30) | (°▲+14.9pp (10/16)) |
| S0-H8 | keep-watching | ▲+2.1pp (161/347) | ▲+6.7pp (43/80) | ▲+3.5pp (60/123) | ·+1.0pp (17/35) |
| S0-H9 | keep-watching | ▲+3.7pp (15/55) net+319/med+3.5 | (°▲+20.7pp (5/11) net+108/med+12.5) | (°▼-17.4pp (1/13) net-22/med-3.1) | — |
| S1-H9 | keep-watching | (°▲+23.8pp (9/19) net+263/med+12.8) | (°▲+25.2pp (4/8) net+148/med+17.8) | (°▼-25.1pp (0/4) net-10/med-2.2) | — |
| S0-H10 | deprioritize | ▼-4.5pp (56/293) net-240/med-1.4 | ▲+2.5pp (18/66) net-62/med+1.9 | ▼-17.4pp (6/78) net-225/med-3.5 | (°▼-15.5pp (1/10) net+27/med+4.8) |
| S0-H11 | keep-watching | ▲+2.3pp (82/316) net-647/med-2.4 | ·-1.2pp (35/148) net+250/med-0.6 | ·-0.5pp (15/61) net+197/med+4.3 | ▼-13.4pp (4/33) net+125/med+4.8 |
| S0-H12 | keep-watching | — | — | — | — |
| S0-H13 | keep-watching | (°▲+26.4pp (1/2) net+28/med+13.8) | (°▲+25.2pp (1/2) net+28/med+13.8) | (°▼-25.1pp (0/1) net-3/med-3.0) | — |
| **union coverage** | | 56.1% (101/180) | 53.8% (28/52) | 85.7% (36/42) | 90.9% (10/11) |

Not graded:  — see register entries.

## Hypothesis Cards (page 2)

### H1
*A climactic bar — extreme volume on a wide spread late in an extended move — marks exhaustion, and price then reverses against the climax direction.*
Grading: directional. Latest review: keep-watching (recommendation).

**H1** — session × window grid (cells as in the matrix):

| session | backtest | forward |
|---|---|---|
| whole | — | — |
| london | — | — |
| overlap | — | — |
| ny_only | — | — |
| dead | — | — |
| asia | — | — |


### H2
*A failed probe beyond a prior extreme — an upthrust above or spring below that closes back inside — reverses against the probe.*
Grading: directional. Latest review: promote-candidate (recommendation).

**H2** — session × window grid (cells as in the matrix):

| session | backtest | forward |
|---|---|---|
| whole | — | — |
| london | — | — |
| overlap | — | — |
| ny_only | — | — |
| dead | — | — |
| asia | — | — |


### H3
*Repeated absorption — high effort with no result — at a price level precedes a breakout through that level.*
Grading: directional. Latest review: keep-watching (recommendation).

**H3** — session × window grid (cells as in the matrix):

| session | backtest | forward |
|---|---|---|
| whole | — | — |
| london | — | — |
| overlap | — | — |
| ny_only | — | — |
| dead | — | — |
| asia | — | — |


### H4
*In an established trend, a quiet (low-volume) pullback resolves with trend resumption.*
Grading: directional. Latest review: keep-watching (recommendation).

**H4** — session × window grid (cells as in the matrix):

| session | backtest | forward |
|---|---|---|
| whole | — | — |
| london | — | — |
| overlap | — | — |
| ny_only | — | — |
| dead | — | — |
| asia | — | — |


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
| whole | — | — |
| london | — | — |
| overlap | — | — |
| ny_only | — | — |
| dead | — | — |
| asia | — | — |


### H7
*Quiet decline at a session extreme is disguised accumulation: effortless (low-volume) weakness reverses UP once selling fails to attract participation (mirror: quiet advance at a high reverses down).*
Grading: directional. Latest review: keep-watching (recommendation).

**H7** — session × window grid (cells as in the matrix):

| session | backtest | forward |
|---|---|---|
| whole | — | — |
| london | — | — |
| overlap | — | — |
| ny_only | — | — |
| dead | — | — |
| asia | — | — |


### H8
*Reversal-signature bar anatomy (upthrust/spring) predicts imminent range expansion irrespective of direction.*
Grading: directional. Latest review: keep-watching (recommendation).

**H8** — session × window grid (cells as in the matrix):

| session | backtest | forward |
|---|---|---|
| whole | — | — |
| london | — | — |
| overlap | — | — |
| ny_only | — | — |
| dead | — | — |
| asia | — | — |


### H9
*Persistent lower-TF directional pressure that recruits expanding participation at the parent timeframe precedes continuation beyond what the parent label alone predicts; pressure without participation expansion does not.*
Grading: directional. Latest review: keep-watching (recommendation).

**H9** — session × window grid (cells as in the matrix):

| session | backtest | forward |
|---|---|---|
| whole | — | — |
| london | — | — |
| overlap | — | — |
| ny_only | — | — |
| dead | — | — |
| asia | — | — |


### H10
*In an established 1-minute trend, no-demand/no-supply prints in the trend's direction signal continuation.*
Grading: directional. Latest review: deprioritize (recommendation).

**H10** — session × window grid (cells as in the matrix):

| session | backtest | forward |
|---|---|---|
| whole | — | — |
| london | — | — |
| overlap | — | — |
| ny_only | — | — |
| dead | — | — |
| asia | — | — |


### H11
*Price entering a low-volume price zone traverses it faster than baseline; entering a high-volume node it stalls or reverses at above-baseline rates.*
Grading: directional. Latest review: keep-watching (recommendation).

**H11** — session × window grid (cells as in the matrix):

| session | backtest | forward |
|---|---|---|
| whole | — | — |
| london | — | — |
| overlap | — | — |
| ny_only | — | — |
| dead | — | — |
| asia | — | — |


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


### H13
*After price breaks out of the session value area on declining volume and reclaims it on expanding volume, it continues toward the far side of the value area.*
Grading: directional. Latest review: keep-watching (recommendation).

**H13** — session × window grid (cells as in the matrix):

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

Store span (1M, close ts): 2026-07-19 22:42:00+00:00 → 2026-08-20 13:26:00+00:00. Volume type: real futures volume (register 40 first-sync sanity; canonical verdict at this instrument's validation evening).

## Summary Matrix (page 1)

Engine `98e5c99b0` — OBSERVATIONAL signal scoreboard - move-detection, not trading; no fills exist here by construction; never validation (docs/hypothesis_lifecycle.md stage 4)

**Review labels are RECOMMENDATIONS — none actioned, review pending operator familiarity.** Cells: marker + precision LIFT vs that context's OWN chance rate, (hits/fires), payoff net/median points (directional rows; either-direction rows have no payoff by construction). ▲/▼ = beyond ±2pp of chance, · = within. (°…) = small-n (fires<20 or episodes<10): dimmed, excluded from any future label arithmetic. Read READING_GUIDE.md first; full detail in hypothesis_performance.json.

| H | label | backtest whole | backtest london | forward whole | forward london |
|---|---|---|---|---|---|
| *context* | | 110 ep; chance 23.8%dir/45.1%either | 27 ep; chance 26.3%dir/51.1%either | 43 ep; chance 23.1%dir/42.3%either | 13 ep; chance 23.0%dir/43.4%either |
| S0-H1 | keep-watching | ▲+10.9pp (17/49) net-83/med+0.7 | (°▲+33.7pp (3/5) net+198/med+39.9) | ▲+11.0pp (14/41) net+68/med-3.9 | (°▲+22.5pp (5/11) net+23/med-7.8) |
| S1-H1 | keep-watching | (°▼-23.8pp (0/3) net-72/med-34.2) | (°▼-26.3pp (0/1) net-54/med-53.5) | (°▼-23.1pp (0/2) net-28/med-14.2) | — |
| S0-H2 | promote-candidate | ·+0.6pp (57/234) net-661/med-5.2 | (°▼-13.0pp (2/15) net+93/med+9.8) | ▲+6.6pp (35/118) net-195/med-2.9 | ▲+3.1pp (6/23) net-10/med-11.4 |
| S1-H2 | promote-candidate | ▲+2.3pp (46/176) net-760/med-8.3 | (°▼-10.9pp (2/13) net+136/med+14.0) | ▲+10.6pp (29/86) net+39/med-1.4 | (°▲+2.0pp (4/16) net+14/med-12.2) |
| S0-H3 | keep-watching | (°▼-11.3pp (1/8) net-28/med+2.0) | — | (°▼-23.1pp (0/6) net-32/med-8.2) | (°▼-23.0pp (0/1) net+19/med+18.8) |
| S0-H4 | keep-watching | ▲+5.6pp (10/34) net+72/med+10.0 | (°▼-16.3pp (1/10) net-30/med-3.7) | — | — |
| S0-H5 | keep-watching | — | — | — | — |
| S0-H6 | keep-watching | ▲+4.0pp (14/36) [cls-chance 34.9% vs uncond 23.8%] net-192/med-10.4 | (°▼-7.3pp (5/18) [cls-chance 35.1% vs uncond 26.3%] net-56/med-10.3) | ▼-7.1pp (18/56) [cls-chance 39.2% vs uncond 23.1%] net-835/med-9.2 | ▼-15.9pp (7/32) [cls-chance 37.8% vs uncond 23.0%] net-828/med-24.9 |
| S0-H7 | keep-watching | ▲+11.8pp (21/59) net+761/med+4.2 | ▲+23.7pp (10/20) net+719/med+33.0 | (°▼-2.0pp (4/19) net-85/med-4.4) | (°▼-4.2pp (3/16) net-53/med-2.4) |
| S0-H7 (either-dir) | keep-watching | ▲+19.3pp (38/59) | ▲+23.9pp (15/20) | (°▲+5.1pp (9/19)) | (°▲+6.6pp (8/16)) |
| S0-H8 | keep-watching | ▲+7.9pp (124/234) | (°▼-31.1pp (3/15)) | ▲+4.3pp (55/118) | ▲+4.4pp (11/23) |
| S0-H9 | keep-watching | ▼-8.4pp (8/52) net-426/med-4.1 | (°▼-26.3pp (0/3) net+17/med+22.6) | (°▼-23.1pp (0/7) net-143/med-5.5) | (°▼-23.0pp (0/1) net-114/med-114.2) |
| S1-H9 | keep-watching | (°▲+26.2pp (4/8) net-53/med+13.1) | — | (°▼-23.1pp (0/2) net-122/med-61.0) | (°▼-23.0pp (0/1) net-114/med-114.2) |
| S0-H10 | deprioritize | ▼-4.1pp (29/147) net-391/med+3.2 | ▼-16.0pp (4/39) net-463/med-12.5 | ▲+3.1pp (16/61) net+58/med+3.1 | (°▲+7.0pp (3/10) net-36/med-11.8) |
| S0-H11 | keep-watching | ▼-3.5pp (15/74) net-452/med-6.0 | (°▼-4.9pp (3/14) net-472/med-58.8) | ·-1.8pp (27/127) net-533/med-6.6 | ▼-5.7pp (9/52) net-272/med-11.2 |
| S0-H12 | keep-watching | — | — | — | — |
| S0-H13 | keep-watching | (°▲+59.5pp (5/6) net+397/med+58.7) | (°▲+73.7pp (2/2) net+181/med+90.7) | (°▼-23.1pp (0/1) net-5/med-5.0) | — |
| **union coverage** | | 43.6% (48/110) | 25.9% (7/27) | 76.7% (33/43) | 92.3% (12/13) |

Not graded:  — see register entries.

## Hypothesis Cards (page 2)

### H1
*A climactic bar — extreme volume on a wide spread late in an extended move — marks exhaustion, and price then reverses against the climax direction.*
Grading: directional. Latest review: keep-watching (recommendation).

**H1** — session × window grid (cells as in the matrix):

| session | backtest | forward |
|---|---|---|
| whole | — | — |
| london | — | — |
| overlap | — | — |
| ny_only | — | — |
| dead | — | — |
| asia | — | — |


### H2
*A failed probe beyond a prior extreme — an upthrust above or spring below that closes back inside — reverses against the probe.*
Grading: directional. Latest review: promote-candidate (recommendation).

**H2** — session × window grid (cells as in the matrix):

| session | backtest | forward |
|---|---|---|
| whole | — | — |
| london | — | — |
| overlap | — | — |
| ny_only | — | — |
| dead | — | — |
| asia | — | — |


### H3
*Repeated absorption — high effort with no result — at a price level precedes a breakout through that level.*
Grading: directional. Latest review: keep-watching (recommendation).

**H3** — session × window grid (cells as in the matrix):

| session | backtest | forward |
|---|---|---|
| whole | — | — |
| london | — | — |
| overlap | — | — |
| ny_only | — | — |
| dead | — | — |
| asia | — | — |


### H4
*In an established trend, a quiet (low-volume) pullback resolves with trend resumption.*
Grading: directional. Latest review: keep-watching (recommendation).

**H4** — session × window grid (cells as in the matrix):

| session | backtest | forward |
|---|---|---|
| whole | — | — |
| london | — | — |
| overlap | — | — |
| ny_only | — | — |
| dead | — | — |
| asia | — | — |


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
| whole | — | — |
| london | — | — |
| overlap | — | — |
| ny_only | — | — |
| dead | — | — |
| asia | — | — |


### H7
*Quiet decline at a session extreme is disguised accumulation: effortless (low-volume) weakness reverses UP once selling fails to attract participation (mirror: quiet advance at a high reverses down).*
Grading: directional. Latest review: keep-watching (recommendation).

**H7** — session × window grid (cells as in the matrix):

| session | backtest | forward |
|---|---|---|
| whole | — | — |
| london | — | — |
| overlap | — | — |
| ny_only | — | — |
| dead | — | — |
| asia | — | — |


### H8
*Reversal-signature bar anatomy (upthrust/spring) predicts imminent range expansion irrespective of direction.*
Grading: directional. Latest review: keep-watching (recommendation).

**H8** — session × window grid (cells as in the matrix):

| session | backtest | forward |
|---|---|---|
| whole | — | — |
| london | — | — |
| overlap | — | — |
| ny_only | — | — |
| dead | — | — |
| asia | — | — |


### H9
*Persistent lower-TF directional pressure that recruits expanding participation at the parent timeframe precedes continuation beyond what the parent label alone predicts; pressure without participation expansion does not.*
Grading: directional. Latest review: keep-watching (recommendation).

**H9** — session × window grid (cells as in the matrix):

| session | backtest | forward |
|---|---|---|
| whole | — | — |
| london | — | — |
| overlap | — | — |
| ny_only | — | — |
| dead | — | — |
| asia | — | — |


### H10
*In an established 1-minute trend, no-demand/no-supply prints in the trend's direction signal continuation.*
Grading: directional. Latest review: deprioritize (recommendation).

**H10** — session × window grid (cells as in the matrix):

| session | backtest | forward |
|---|---|---|
| whole | — | — |
| london | — | — |
| overlap | — | — |
| ny_only | — | — |
| dead | — | — |
| asia | — | — |


### H11
*Price entering a low-volume price zone traverses it faster than baseline; entering a high-volume node it stalls or reverses at above-baseline rates.*
Grading: directional. Latest review: keep-watching (recommendation).

**H11** — session × window grid (cells as in the matrix):

| session | backtest | forward |
|---|---|---|
| whole | — | — |
| london | — | — |
| overlap | — | — |
| ny_only | — | — |
| dead | — | — |
| asia | — | — |


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


### H13
*After price breaks out of the session value area on declining volume and reclaims it on expanding volume, it continues toward the far side of the value area.*
Grading: directional. Latest review: keep-watching (recommendation).

**H13** — session × window grid (cells as in the matrix):

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

Store span (1M, close ts): 2026-07-19 22:02:00+00:00 → 2026-08-20 13:27:00+00:00. Volume type: real futures volume (register 40 first-sync sanity; canonical verdict at this instrument's validation evening).

## Summary Matrix (page 1)

Engine `98e5c99b0` — OBSERVATIONAL signal scoreboard - move-detection, not trading; no fills exist here by construction; never validation (docs/hypothesis_lifecycle.md stage 4)

**Review labels are RECOMMENDATIONS — none actioned, review pending operator familiarity.** Cells: marker + precision LIFT vs that context's OWN chance rate, (hits/fires), payoff net/median points (directional rows; either-direction rows have no payoff by construction). ▲/▼ = beyond ±2pp of chance, · = within. (°…) = small-n (fires<20 or episodes<10): dimmed, excluded from any future label arithmetic. Read READING_GUIDE.md first; full detail in hypothesis_performance.json.

| H | label | backtest whole | backtest london | forward whole | forward london |
|---|---|---|---|---|---|
| *context* | | 114 ep; chance 22.0%dir/41.6%either | 40 ep; chance 30.9%dir/55.9%either | 42 ep; chance 22.3%dir/42.4%either | 14 ep; chance 31.5%dir/59.4%either |
| S0-H1 | keep-watching | ▲+16.2pp (13/34) net+122/med-15.7 | (°▼-18.4pp (1/8) net-257/med-46.2) | ▲+14.1pp (12/33) net+226/med+11.5 | ▲+3.5pp (7/20) net-27/med+7.8 |
| S1-H1 | keep-watching | (°▲+44.7pp (2/3) net+465/med+128.4) | — | (°▲+77.7pp (1/1) net+74/med+74.3) | (°▲+68.5pp (1/1) net+74/med+74.3) |
| S0-H2 | promote-candidate | ▼-2.0pp (64/320) net-3528/med-1.4 | ▼-5.5pp (15/59) net-313/med-30.0 | ▲+9.4pp (58/183) net-49/med-4.4 | ▲+3.9pp (29/82) net+206/med-0.8 |
| S1-H2 | promote-candidate | ·-1.3pp (46/222) net-1379/med-4.2 | ▼-3.0pp (12/43) net-382/med-31.5 | ▲+7.9pp (39/129) net-240/med+1.7 | ▼-2.4pp (16/55) net-199/med-5.0 |
| S0-H3 | keep-watching | (°▲+78.0pp (1/1) net+106/med+105.8) | (°▲+69.1pp (1/1) net+106/med+105.8) | — | — |
| S0-H4 | keep-watching | — | — | (°▲+37.7pp (6/10) net-18/med-7.4) | (°▲+8.5pp (2/5) net+26/med+9.5) |
| S0-H5 | keep-watching | — | — | — | — |
| S0-H6 | keep-watching | ▼-8.1pp (9/29) [cls-chance 39.1% vs uncond 22.0%] net-232/med-11.8 | (°▼-38.6pp (0/5) [cls-chance 38.6% vs uncond 30.9%] net-719/med-105.3) | ▲+4.5pp (14/34) [cls-chance 36.7% vs uncond 22.3%] net+368/med-2.4 | (°▲+6.5pp (5/12) [cls-chance 35.2% vs uncond 31.5%] net+265/med+16.6) |
| S0-H7 | keep-watching | ·+0.0pp (11/50) net+77/med-7.8 | (°▼-5.9pp (4/16) net-167/med-6.6) | ·-0.1pp (6/27) net+308/med+5.3 | (°▼-14.8pp (2/12) net+71/med-27.2) |
| S0-H7 (either-dir) | keep-watching | ▲+4.4pp (23/50) | (°·+0.3pp (9/16)) | ▲+16.9pp (16/27) | (°·-1.1pp (7/12)) |
| S0-H8 | keep-watching | ·+1.8pp (139/320) | ▲+3.4pp (35/59) | ▲+12.2pp (100/183) | ·-0.9pp (48/82) |
| S0-H9 | keep-watching | ·+0.7pp (20/88) net+593/med-4.3 | (°▲+2.4pp (3/9) net+410/med+11.6) | ▼-8.7pp (9/66) net-538/med-9.7 | (°·+1.8pp (1/3) net-444/med-246.5) |
| S1-H9 | keep-watching | ▲+6.0pp (7/25) net-373/med+10.8 | (°▼-30.9pp (0/5) net-57/med+2.3) | (°▼-2.3pp (1/5) net-500/med-25.7) | (°▼-31.5pp (0/2) net-493/med-246.5) |
| S0-H10 | deprioritize | ▼-6.0pp (28/175) net+2743/med+15.3 | (°▼-17.6pp (2/15) net-356/med-1.7) | ▼-4.3pp (24/133) net-1407/med-8.1 | (°▲+27.3pp (10/17) net+208/med+2.7) |
| S0-H11 | keep-watching | ▲+2.3pp (64/263) net+863/med+0.9 | ▼-2.3pp (26/91) net+264/med-3.9 | ·+1.5pp (39/164) net+1406/med+4.3 | ·+0.8pp (10/31) net+564/med-2.6 |
| S0-H12 | keep-watching | — | — | — | — |
| S0-H13 | keep-watching | (°▲+78.0pp (1/1) net+93/med+93.0) | (°▲+69.1pp (1/1) net+93/med+93.0) | — | — |
| **union coverage** | | 42.1% (48/114) | 37.5% (15/40) | 85.7% (36/42) | 92.9% (13/14) |

Not graded:  — see register entries.

## Hypothesis Cards (page 2)

### H1
*A climactic bar — extreme volume on a wide spread late in an extended move — marks exhaustion, and price then reverses against the climax direction.*
Grading: directional. Latest review: keep-watching (recommendation).

**H1** — session × window grid (cells as in the matrix):

| session | backtest | forward |
|---|---|---|
| whole | — | — |
| london | — | — |
| overlap | — | — |
| ny_only | — | — |
| dead | — | — |
| asia | — | — |


### H2
*A failed probe beyond a prior extreme — an upthrust above or spring below that closes back inside — reverses against the probe.*
Grading: directional. Latest review: promote-candidate (recommendation).

**H2** — session × window grid (cells as in the matrix):

| session | backtest | forward |
|---|---|---|
| whole | — | — |
| london | — | — |
| overlap | — | — |
| ny_only | — | — |
| dead | — | — |
| asia | — | — |


### H3
*Repeated absorption — high effort with no result — at a price level precedes a breakout through that level.*
Grading: directional. Latest review: keep-watching (recommendation).

**H3** — session × window grid (cells as in the matrix):

| session | backtest | forward |
|---|---|---|
| whole | — | — |
| london | — | — |
| overlap | — | — |
| ny_only | — | — |
| dead | — | — |
| asia | — | — |


### H4
*In an established trend, a quiet (low-volume) pullback resolves with trend resumption.*
Grading: directional. Latest review: keep-watching (recommendation).

**H4** — session × window grid (cells as in the matrix):

| session | backtest | forward |
|---|---|---|
| whole | — | — |
| london | — | — |
| overlap | — | — |
| ny_only | — | — |
| dead | — | — |
| asia | — | — |


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
| whole | — | — |
| london | — | — |
| overlap | — | — |
| ny_only | — | — |
| dead | — | — |
| asia | — | — |


### H7
*Quiet decline at a session extreme is disguised accumulation: effortless (low-volume) weakness reverses UP once selling fails to attract participation (mirror: quiet advance at a high reverses down).*
Grading: directional. Latest review: keep-watching (recommendation).

**H7** — session × window grid (cells as in the matrix):

| session | backtest | forward |
|---|---|---|
| whole | — | — |
| london | — | — |
| overlap | — | — |
| ny_only | — | — |
| dead | — | — |
| asia | — | — |


### H8
*Reversal-signature bar anatomy (upthrust/spring) predicts imminent range expansion irrespective of direction.*
Grading: directional. Latest review: keep-watching (recommendation).

**H8** — session × window grid (cells as in the matrix):

| session | backtest | forward |
|---|---|---|
| whole | — | — |
| london | — | — |
| overlap | — | — |
| ny_only | — | — |
| dead | — | — |
| asia | — | — |


### H9
*Persistent lower-TF directional pressure that recruits expanding participation at the parent timeframe precedes continuation beyond what the parent label alone predicts; pressure without participation expansion does not.*
Grading: directional. Latest review: keep-watching (recommendation).

**H9** — session × window grid (cells as in the matrix):

| session | backtest | forward |
|---|---|---|
| whole | — | — |
| london | — | — |
| overlap | — | — |
| ny_only | — | — |
| dead | — | — |
| asia | — | — |


### H10
*In an established 1-minute trend, no-demand/no-supply prints in the trend's direction signal continuation.*
Grading: directional. Latest review: deprioritize (recommendation).

**H10** — session × window grid (cells as in the matrix):

| session | backtest | forward |
|---|---|---|
| whole | — | — |
| london | — | — |
| overlap | — | — |
| ny_only | — | — |
| dead | — | — |
| asia | — | — |


### H11
*Price entering a low-volume price zone traverses it faster than baseline; entering a high-volume node it stalls or reverses at above-baseline rates.*
Grading: directional. Latest review: keep-watching (recommendation).

**H11** — session × window grid (cells as in the matrix):

| session | backtest | forward |
|---|---|---|
| whole | — | — |
| london | — | — |
| overlap | — | — |
| ny_only | — | — |
| dead | — | — |
| asia | — | — |


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


### H13
*After price breaks out of the session value area on declining volume and reclaims it on expanding volume, it continues toward the far side of the value area.*
Grading: directional. Latest review: keep-watching (recommendation).

**H13** — session × window grid (cells as in the matrix):

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

Store span (1M, close ts): 2026-07-19 22:02:00+00:00 → 2026-08-20 13:27:00+00:00. Volume type: real futures volume (register 40 first-sync sanity; canonical verdict at this instrument's validation evening).

## Summary Matrix (page 1)

Engine `98e5c99b0` — OBSERVATIONAL signal scoreboard - move-detection, not trading; no fills exist here by construction; never validation (docs/hypothesis_lifecycle.md stage 4)

**Review labels are RECOMMENDATIONS — none actioned, review pending operator familiarity.** Cells: marker + precision LIFT vs that context's OWN chance rate, (hits/fires), payoff net/median points (directional rows; either-direction rows have no payoff by construction). ▲/▼ = beyond ±2pp of chance, · = within. (°…) = small-n (fires<20 or episodes<10): dimmed, excluded from any future label arithmetic. Read READING_GUIDE.md first; full detail in hypothesis_performance.json.

| H | label | backtest whole | backtest london | forward whole | forward london |
|---|---|---|---|---|---|
| *context* | | 110 ep; chance 24.0%dir/44.7%either | 37 ep; chance 36.6%dir/66.3%either | 35 ep; chance 22.4%dir/42.8%either | 11 ep; chance 34.9%dir/66.3%either |
| S0-H1 | keep-watching | ▲+10.7pp (17/49) net-83/med-8.0 | (°·-1.3pp (6/17) net-113/med-17.5) | ▲+11.5pp (20/59) net-872/med+0.5 | ·-0.3pp (9/26) net-846/med-14.8 |
| S1-H1 | keep-watching | (°▼-24.0pp (0/2) net-18/med-9.2) | (°▼-36.6pp (0/1) net-50/med-50.0) | (°▼-2.4pp (1/5) net-444/med-94.5) | (°▼-34.9pp (0/4) net-492/med-133.2) |
| S0-H2 | promote-candidate | ▲+2.0pp (73/281) net-2432/med-4.0 | ·-1.1pp (22/62) net-337/med-20.0 | ▲+4.2pp (49/184) net+294/med-1.0 | ·+1.5pp (28/77) net+438/med+0.5 |
| S1-H2 | promote-candidate | ▲+3.3pp (60/220) net-505/med-2.8 | ·+1.4pp (19/50) net-218/med-18.0 | ·+1.1pp (32/136) net+137/med-1.0 | ▼-6.3pp (14/49) net+68/med+0.0 |
| S0-H3 | keep-watching | (°·+1.0pp (1/4) net+59/med+13.2) | (°▼-36.6pp (0/2) net-22/med-11.0) | — | — |
| S0-H4 | keep-watching | (°▲+14.5pp (5/13) net+194/med+15.0) | (°▲+34.8pp (5/7) net+392/med+71.0) | — | — |
| S0-H5 | keep-watching | (°▼-24.0pp (0/1) net-135/med-135.0) | (°▼-36.6pp (0/1) net-135/med-135.0) | (°▲+77.6pp (1/1) net+24/med+24.0) | (°▲+65.1pp (1/1) net+24/med+24.0) |
| S0-H6 | keep-watching | ▼-21.4pp (10/52) [cls-chance 40.6% vs uncond 24.0%] net-1151/med-25.2 | ▼-28.5pp (3/24) [cls-chance 41.0% vs uncond 36.6%] net-664/med-30.0 | ·-0.7pp (12/30) [cls-chance 40.7% vs uncond 22.4%] net-416/med-3.5 | (°▲+26.0pp (10/15) [cls-chance 40.7% vs uncond 34.9%] net+348/med+26.5) |
| S0-H7 | keep-watching | ▼-2.0pp (9/41) net+205/med-9.0 | (°▼-5.4pp (5/16) net-161/med-7.0) | ▲+13.3pp (10/28) net+168/med+4.8 | (°▲+8.0pp (3/7) net-113/med-36.0) |
| S0-H7 (either-dir) | keep-watching | ▼-3.2pp (17/41) | (°▲+2.5pp (11/16)) | ▲+17.9pp (17/28) | (°▲+33.7pp (7/7)) |
| S0-H8 | keep-watching | ▲+7.3pp (146/281) | ▲+6.3pp (45/62) | ▲+3.9pp (86/184) | ▼-6.6pp (46/77) |
| S0-H9 | keep-watching | ·-1.5pp (9/40) net-353/med-14.7 | (°▼-3.3pp (1/3) net-198/med-61.5) | ▼-12.4pp (2/20) net-558/med-31.0 | (°▼-12.7pp (2/9) net-363/med-76.0) |
| S1-H9 | keep-watching | (°·-1.8pp (2/9) net+460/med+1.5) | (°▼-36.6pp (0/1) net-38/med-38.0) | (°▼-4.2pp (2/11) net-375/med-31.0) | (°▼-9.9pp (2/8) net-305/med-84.8) |
| S0-H10 | deprioritize | ·+0.0pp (37/154) net+1774/med+11.0 | ▲+3.4pp (16/40) net+1480/med+27.5 | ▼-8.0pp (19/132) net-308/med-1.2 | ▼-18.9pp (4/25) net-195/med-18.5 |
| S0-H11 | keep-watching | ▲+3.4pp (113/413) net+1254/med+3.0 | ·+0.8pp (61/163) net-404/med+5.0 | ▲+4.7pp (64/236) net-540/med-5.8 | ·+0.6pp (38/107) net-66/med-5.0 |
| S0-H12 | keep-watching | — | — | — | — |
| S0-H13 | keep-watching | (°▼-24.0pp (0/1) net-206/med-206.0) | (°▼-36.6pp (0/1) net-206/med-206.0) | — | — |
| **union coverage** | | 40.0% (44/110) | 35.1% (13/37) | 88.6% (31/35) | 90.9% (10/11) |

Not graded:  — see register entries.

## Hypothesis Cards (page 2)

### H1
*A climactic bar — extreme volume on a wide spread late in an extended move — marks exhaustion, and price then reverses against the climax direction.*
Grading: directional. Latest review: keep-watching (recommendation).

**H1** — session × window grid (cells as in the matrix):

| session | backtest | forward |
|---|---|---|
| whole | — | — |
| london | — | — |
| overlap | — | — |
| ny_only | — | — |
| dead | — | — |
| asia | — | — |


### H2
*A failed probe beyond a prior extreme — an upthrust above or spring below that closes back inside — reverses against the probe.*
Grading: directional. Latest review: promote-candidate (recommendation).

**H2** — session × window grid (cells as in the matrix):

| session | backtest | forward |
|---|---|---|
| whole | — | — |
| london | — | — |
| overlap | — | — |
| ny_only | — | — |
| dead | — | — |
| asia | — | — |


### H3
*Repeated absorption — high effort with no result — at a price level precedes a breakout through that level.*
Grading: directional. Latest review: keep-watching (recommendation).

**H3** — session × window grid (cells as in the matrix):

| session | backtest | forward |
|---|---|---|
| whole | — | — |
| london | — | — |
| overlap | — | — |
| ny_only | — | — |
| dead | — | — |
| asia | — | — |


### H4
*In an established trend, a quiet (low-volume) pullback resolves with trend resumption.*
Grading: directional. Latest review: keep-watching (recommendation).

**H4** — session × window grid (cells as in the matrix):

| session | backtest | forward |
|---|---|---|
| whole | — | — |
| london | — | — |
| overlap | — | — |
| ny_only | — | — |
| dead | — | — |
| asia | — | — |


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
| whole | — | — |
| london | — | — |
| overlap | — | — |
| ny_only | — | — |
| dead | — | — |
| asia | — | — |


### H7
*Quiet decline at a session extreme is disguised accumulation: effortless (low-volume) weakness reverses UP once selling fails to attract participation (mirror: quiet advance at a high reverses down).*
Grading: directional. Latest review: keep-watching (recommendation).

**H7** — session × window grid (cells as in the matrix):

| session | backtest | forward |
|---|---|---|
| whole | — | — |
| london | — | — |
| overlap | — | — |
| ny_only | — | — |
| dead | — | — |
| asia | — | — |


### H8
*Reversal-signature bar anatomy (upthrust/spring) predicts imminent range expansion irrespective of direction.*
Grading: directional. Latest review: keep-watching (recommendation).

**H8** — session × window grid (cells as in the matrix):

| session | backtest | forward |
|---|---|---|
| whole | — | — |
| london | — | — |
| overlap | — | — |
| ny_only | — | — |
| dead | — | — |
| asia | — | — |


### H9
*Persistent lower-TF directional pressure that recruits expanding participation at the parent timeframe precedes continuation beyond what the parent label alone predicts; pressure without participation expansion does not.*
Grading: directional. Latest review: keep-watching (recommendation).

**H9** — session × window grid (cells as in the matrix):

| session | backtest | forward |
|---|---|---|
| whole | — | — |
| london | — | — |
| overlap | — | — |
| ny_only | — | — |
| dead | — | — |
| asia | — | — |


### H10
*In an established 1-minute trend, no-demand/no-supply prints in the trend's direction signal continuation.*
Grading: directional. Latest review: deprioritize (recommendation).

**H10** — session × window grid (cells as in the matrix):

| session | backtest | forward |
|---|---|---|
| whole | — | — |
| london | — | — |
| overlap | — | — |
| ny_only | — | — |
| dead | — | — |
| asia | — | — |


### H11
*Price entering a low-volume price zone traverses it faster than baseline; entering a high-volume node it stalls or reverses at above-baseline rates.*
Grading: directional. Latest review: keep-watching (recommendation).

**H11** — session × window grid (cells as in the matrix):

| session | backtest | forward |
|---|---|---|
| whole | — | — |
| london | — | — |
| overlap | — | — |
| ny_only | — | — |
| dead | — | — |
| asia | — | — |


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


### H13
*After price breaks out of the session value area on declining volume and reclaims it on expanding volume, it continues toward the far side of the value area.*
Grading: directional. Latest review: keep-watching (recommendation).

**H13** — session × window grid (cells as in the matrix):

| session | backtest | forward |
|---|---|---|
| whole | — | — |
| london | — | — |
| overlap | — | — |
| ny_only | — | — |
| dead | — | — |
| asia | — | — |



---

Appendix: the per-session detail beyond London and every horizon-mark payoff live in hypothesis_performance.json (generated, same run).