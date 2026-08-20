# Hypothesis Performance — Per-Instrument

Engine `6e7db5af5` — register 40 fence as amended 2026-08-19 (operator): one section per instrument, each computed only from that instrument's own store and native calendar; uk100 canonical, ger40/nas100/us30 PROVISIONAL (validation pending). Numbers are NEVER pooled across instruments — cross-instrument aggregation is a future registration. This first cross-instrument read is EXPLORATORY: expectations deliberately unregistered; anything interesting becomes a pre-registered question before it becomes a claim.

---

# uk100 (uk100fut) — CANONICAL

Store span (1M, close ts): 2026-07-12 22:06:00+00:00 → 2026-08-20 12:11:00+00:00. Volume type: real futures volume (step-zero audit).

## Summary Matrix (page 1)

Engine `6e7db5af5` — OBSERVATIONAL signal scoreboard - move-detection, not trading; no fills exist here by construction; never validation (docs/hypothesis_lifecycle.md stage 4)

**Review labels are RECOMMENDATIONS — none actioned, review pending operator familiarity.** Cells: marker + precision LIFT vs that context's OWN chance rate, (hits/fires), payoff net/median points (directional rows; either-direction rows have no payoff by construction). ▲/▼ = beyond ±2pp of chance, · = within. (°…) = small-n (fires<20 or episodes<10): dimmed, excluded from any future label arithmetic. Read READING_GUIDE.md first; full detail in signal_scoreboard.json.

| H | label | backtest whole | backtest london | forward whole | forward london |
|---|---|---|---|---|---|
| *context* | | 180 ep; chance 23.6%dir/44.3%either | 52 ep; chance 24.9%dir/47.1%either | 41 ep; chance 25.1%dir/45.2%either | 9 ep; chance 25.4%dir/47.3%either |
| S0-H1 | keep-watching | ·-0.4pp (16/69) net+194/med+2.8 | ▲+6.9pp (7/22) net+133/med+3.0 | ▲+2.2pp (9/33) net+26/med+0.8 | (°·-0.4pp (2/8) net+4/med+2.6) |
| S1-H1 | keep-watching | (°▼-3.6pp (1/5) net+9/med+3.0) | — | (°▲+8.2pp (1/3) net+0/med+3.5) | (°▲+7.9pp (1/3) net+0/med+3.5) |
| S0-H2 | promote-candidate | ·+1.5pp (87/347) net+781/med+1.5 | ▲+7.6pp (26/80) net+521/med+9.2 | ▲+3.2pp (34/120) net-83/med-1.0 | (°▼-3.5pp (7/32) net-16/med-1.8) |
| S1-H2 | promote-candidate | ·+1.0pp (62/252) net+540/med+0.9 | ▲+7.3pp (19/59) net+559/med+12.0 | ▲+4.1pp (31/106) net-106/med-1.1 | (°▼-4.0pp (6/28) net-28/med-1.8) |
| S0-H3 | keep-watching | — | — | (°▲+3.5pp (2/7) net-29/med-0.5) | (°▲+7.9pp (1/3) net-27/med-5.0) |
| S0-H4 | keep-watching | (°▼-23.6pp (0/7) net+14/med+0.5) | (°▼-24.9pp (0/1) net+6/med+5.5) | — | — |
| S0-H5 | keep-watching | — | — | — | — |
| S0-H6 | keep-watching | ▲+8.1pp (27/59) [cls-chance 37.7% vs uncond 23.6%] net+391/med+5.7 | ▲+20.6pp (18/31) [cls-chance 37.5% vs uncond 24.9%] net+282/med+16.0 | (°▲+11.4pp (8/15) [cls-chance 41.9% vs uncond 25.1%] net+71/med+6.0) | (°▲+11.8pp (5/10) [cls-chance 38.2% vs uncond 25.4%] net+52/med+4.3) |
| S0-H7 | keep-watching | ▲+8.5pp (36/112) net+7/med+2.8 | ▲+6.8pp (13/41) net-217/med+2.7 | ▲+2.5pp (8/29) net+65/med+2.2 | (°▲+14.6pp (6/15) net+26/med-1.0) |
| S0-H7 (either-dir) | keep-watching | ▲+10.2pp (61/112) | ▲+6.6pp (22/41) | ·-0.4pp (13/29) | (°▲+19.4pp (10/15)) |
| S0-H8 | keep-watching | ▲+2.4pp (162/347) | ▲+7.9pp (44/80) | ·+1.5pp (56/120) | (°▼-6.7pp (13/32)) |
| S0-H9 | keep-watching | ▲+3.7pp (15/55) net+319/med+3.5 | (°▲+20.6pp (5/11) net+108/med+12.5) | (°▼-17.4pp (1/13) net-22/med-3.1) | — |
| S1-H9 | keep-watching | (°▲+23.8pp (9/19) net+263/med+12.8) | (°▲+25.1pp (4/8) net+148/med+17.8) | (°▼-25.1pp (0/4) net-10/med-2.2) | — |
| S0-H10 | deprioritize | ▼-4.5pp (56/293) net-240/med-1.4 | ▲+2.4pp (18/66) net-62/med+1.9 | ▼-17.4pp (6/78) net-225/med-3.5 | (°▼-15.4pp (1/10) net+27/med+4.8) |
| S0-H11 | keep-watching | ▲+2.3pp (82/316) net-647/med-2.4 | ·-1.3pp (35/148) net+250/med-0.6 | ·-1.8pp (14/60) net+210/med+4.5 | (°▼-16.0pp (3/32) net+139/med+4.9) |
| S0-H12 | keep-watching | — | — | — | — |
| **union coverage** | | 56.1% (101/180) | 53.8% (28/52) | 85.4% (35/41) | 88.9% (8/9) |

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



---

# ger40 (ger40fut) — PROVISIONAL

> **PROVISIONAL — validation pending (register 40 fence as amended 2026-08-19): replay-only study over the synced store; canonical status, live attachment, and Asia/pause-sensitive cell interpretation await this instrument's validation evening. EXPLORATORY first cross-instrument look — expectations deliberately unregistered; anything interesting becomes a pre-registered question before it becomes a claim. NO POOLING across instruments.**
>
> - drift-adjustment segments and engine tod baselines run on the provider/London trading-day structure; native cash-hour segmentation is part of this instrument's validation evening
> - sessions = the registered register-37 world-clock partition (native-tz, DST-proof) applied to this instrument's own bars; 'london' is not the home session of the US pairs
> - the forward window (>= go_live) is also a replay over the synced store — this instrument has NO live attachment yet

Store span (1M, close ts): 2026-07-19 22:42:00+00:00 → 2026-08-19 22:24:00+00:00. Volume type: real futures volume (register 40 first-sync sanity; canonical verdict at this instrument's validation evening).

## Summary Matrix (page 1)

Engine `6e7db5af5` — OBSERVATIONAL signal scoreboard - move-detection, not trading; no fills exist here by construction; never validation (docs/hypothesis_lifecycle.md stage 4)

**Review labels are RECOMMENDATIONS — none actioned, review pending operator familiarity.** Cells: marker + precision LIFT vs that context's OWN chance rate, (hits/fires), payoff net/median points (directional rows; either-direction rows have no payoff by construction). ▲/▼ = beyond ±2pp of chance, · = within. (°…) = small-n (fires<20 or episodes<10): dimmed, excluded from any future label arithmetic. Read READING_GUIDE.md first; full detail in signal_scoreboard.json.

| H | label | backtest whole | backtest london | forward whole | forward london |
|---|---|---|---|---|---|
| *context* | | 110 ep; chance 23.9%dir/45.2%either | 27 ep; chance 26.4%dir/51.2%either | 33 ep; chance 22.2%dir/40.1%either | 8 ep; chance 23.1%dir/43.1%either |
| S0-H1 | keep-watching | ▲+10.8pp (17/49) net-83/med+0.7 | (°▲+33.6pp (3/5) net+198/med+39.9) | ▲+16.5pp (12/31) net+197/med-0.3 | (°▲+43.6pp (4/6) net+94/med+23.1) |
| S1-H1 | keep-watching | (°▼-23.9pp (0/3) net-72/med-34.2) | (°▼-26.4pp (0/1) net-54/med-53.5) | (°▼-22.2pp (0/1) net-7/med-7.4) | — |
| S0-H2 | promote-candidate | ·+0.5pp (57/234) net-661/med-5.2 | (°▼-13.1pp (2/15) net+93/med+9.8) | ▲+10.0pp (28/87) net-69/med-2.3 | (°▲+7.7pp (4/13) net+66/med-11.4) |
| S1-H2 | promote-candidate | ▲+2.2pp (46/176) net-760/med-8.3 | (°▼-11.0pp (2/13) net+136/med+14.0) | ▲+15.9pp (24/63) net+141/med+1.0 | (°▲+10.2pp (3/9) net+86/med-11.4) |
| S0-H3 | keep-watching | (°▼-11.4pp (1/8) net-28/med+2.0) | — | (°▼-22.2pp (0/3) net+2/med+0.5) | (°▼-23.1pp (0/1) net+19/med+18.8) |
| S0-H4 | keep-watching | ▲+5.5pp (10/34) net+72/med+10.0 | (°▼-16.4pp (1/10) net-30/med-3.7) | — | — |
| S0-H5 | keep-watching | — | — | — | — |
| S0-H6 | keep-watching | ▲+3.9pp (14/36) [cls-chance 35.0% vs uncond 23.9%] net-192/med-10.4 | (°▼-7.4pp (5/18) [cls-chance 35.2% vs uncond 26.4%] net-56/med-10.3) | ▼-5.7pp (17/50) [cls-chance 39.7% vs uncond 22.2%] net-508/med-6.8 | (°▼-15.4pp (6/26) [cls-chance 38.5% vs uncond 23.1%] net-501/med-21.4) |
| S0-H7 | keep-watching | ▲+11.7pp (21/59) net+761/med+4.2 | ▲+23.6pp (10/20) net+719/med+33.0 | (°▼-2.2pp (2/10) net-7/med+1.1) | (°·+1.9pp (2/8) net+53/med+12.4) |
| S0-H7 (either-dir) | keep-watching | ▲+19.2pp (38/59) | ▲+23.8pp (15/20) | (°·-0.1pp (4/10)) | (°▲+6.9pp (4/8)) |
| S0-H8 | keep-watching | ▲+7.8pp (124/234) | (°▼-31.2pp (3/15)) | ▲+4.7pp (39/87) | (°▼-4.6pp (5/13)) |
| S0-H9 | keep-watching | ▼-8.5pp (8/52) net-426/med-4.1 | (°▼-26.4pp (0/3) net+17/med+22.6) | (°▼-22.2pp (0/7) net-143/med-5.5) | (°▼-23.1pp (0/1) net-114/med-114.2) |
| S1-H9 | keep-watching | (°▲+26.1pp (4/8) net-53/med+13.1) | — | (°▼-22.2pp (0/2) net-122/med-61.0) | (°▼-23.1pp (0/1) net-114/med-114.2) |
| S0-H10 | deprioritize | ▼-4.2pp (29/147) net-391/med+3.2 | ▼-16.1pp (4/39) net-463/med-12.5 | ·+1.5pp (14/59) net+25/med+2.1 | (°▲+6.9pp (3/10) net-36/med-11.8) |
| S0-H11 | keep-watching | ▼-3.6pp (15/74) net-452/med-6.0 | (°▼-5.0pp (3/14) net-472/med-58.8) | ·+0.1pp (25/112) net-379/med-6.6 | (°▼-6.8pp (8/49) net-182/med-10.1) |
| S0-H12 | keep-watching | — | — | — | — |
| **union coverage** | | 43.6% (48/110) | 25.9% (7/27) | 72.7% (24/33) | 87.5% (7/8) |

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



---

# nas100 (nas100fut) — PROVISIONAL

> **PROVISIONAL — validation pending (register 40 fence as amended 2026-08-19): replay-only study over the synced store; canonical status, live attachment, and Asia/pause-sensitive cell interpretation await this instrument's validation evening. EXPLORATORY first cross-instrument look — expectations deliberately unregistered; anything interesting becomes a pre-registered question before it becomes a claim. NO POOLING across instruments.**
>
> - drift-adjustment segments and engine tod baselines run on the provider/London trading-day structure; native cash-hour segmentation is part of this instrument's validation evening
> - sessions = the registered register-37 world-clock partition (native-tz, DST-proof) applied to this instrument's own bars; 'london' is not the home session of the US pairs
> - the forward window (>= go_live) is also a replay over the synced store — this instrument has NO live attachment yet

Store span (1M, close ts): 2026-07-19 22:02:00+00:00 → 2026-08-19 22:25:00+00:00. Volume type: real futures volume (register 40 first-sync sanity; canonical verdict at this instrument's validation evening).

## Summary Matrix (page 1)

Engine `6e7db5af5` — OBSERVATIONAL signal scoreboard - move-detection, not trading; no fills exist here by construction; never validation (docs/hypothesis_lifecycle.md stage 4)

**Review labels are RECOMMENDATIONS — none actioned, review pending operator familiarity.** Cells: marker + precision LIFT vs that context's OWN chance rate, (hits/fires), payoff net/median points (directional rows; either-direction rows have no payoff by construction). ▲/▼ = beyond ±2pp of chance, · = within. (°…) = small-n (fires<20 or episodes<10): dimmed, excluded from any future label arithmetic. Read READING_GUIDE.md first; full detail in signal_scoreboard.json.

| H | label | backtest whole | backtest london | forward whole | forward london |
|---|---|---|---|---|---|
| *context* | | 115 ep; chance 22.0%dir/41.6%either | 41 ep; chance 30.9%dir/56.0%either | 32 ep; chance 21.9%dir/40.9%either | 11 ep; chance 31.8%dir/58.3%either |
| S0-H1 | keep-watching | ▲+16.2pp (13/34) net+122/med-15.7 | (°▼-18.4pp (1/8) net-257/med-46.2) | (°▲+21.0pp (6/14) net+208/med+11.4) | (°▲+18.2pp (2/4) net+38/med+1.6) |
| S1-H1 | keep-watching | (°▲+44.7pp (2/3) net+465/med+128.4) | — | — | — |
| S0-H2 | promote-candidate | ▼-2.6pp (62/320) net-3528/med-1.4 | ▼-7.2pp (14/59) net-313/med-30.0 | ▲+6.6pp (35/123) net-802/med-5.0 | ·-0.7pp (14/45) net-545/med-5.0 |
| S1-H2 | promote-candidate | ▼-2.2pp (44/222) net-1379/med-4.2 | ▼-5.3pp (11/43) net-382/med-31.5 | ▲+5.1pp (24/89) net-423/med-2.1 | ▼-9.2pp (7/31) net-354/med-5.0 |
| S0-H3 | keep-watching | (°▲+78.0pp (1/1) net+106/med+105.8) | (°▲+69.1pp (1/1) net+106/med+105.8) | — | — |
| S0-H4 | keep-watching | — | — | (°▲+38.1pp (6/10) net-18/med-7.4) | (°▲+8.2pp (2/5) net+26/med+9.5) |
| S0-H5 | keep-watching | — | — | — | — |
| S0-H6 | keep-watching | ▼-8.0pp (9/29) [cls-chance 39.0% vs uncond 22.0%] net-232/med-11.8 | (°▼-38.2pp (0/5) [cls-chance 38.2% vs uncond 30.9%] net-719/med-105.3) | ·+0.4pp (12/31) [cls-chance 38.3% vs uncond 21.9%] net+204/med-5.5 | (°·-1.8pp (3/9) [cls-chance 35.1% vs uncond 31.8%] net+100/med+16.3) |
| S0-H7 | keep-watching | ·+0.0pp (11/50) net+77/med-7.8 | (°▼-5.9pp (4/16) net-167/med-6.6) | (°·+0.3pp (4/18) net+388/med+5.4) | (°▼-15.1pp (1/6) net+172/med-27.2) |
| S0-H7 (either-dir) | keep-watching | ▲+4.4pp (23/50) | (°·+0.2pp (9/16)) | (°▲+9.1pp (9/18)) | (°▼-8.3pp (3/6)) |
| S0-H8 | keep-watching | ·+1.8pp (139/320) | ▲+3.3pp (35/59) | ▲+11.1pp (64/123) | ▼-7.2pp (23/45) |
| S0-H9 | keep-watching | ·+0.7pp (20/88) net+593/med-4.3 | (°▲+2.4pp (3/9) net+410/med+11.6) | ▼-8.3pp (9/66) net-538/med-9.7 | (°·+1.5pp (1/3) net-444/med-246.5) |
| S1-H9 | keep-watching | ▲+6.0pp (7/25) net-373/med+10.8 | (°▼-30.9pp (0/5) net-57/med+2.3) | (°·-1.9pp (1/5) net-500/med-25.7) | (°▼-31.8pp (0/2) net-493/med-246.5) |
| S0-H10 | deprioritize | ▼-6.0pp (28/175) net+2743/med+15.3 | (°▼-17.6pp (2/15) net-356/med-1.7) | ▼-3.1pp (25/133) net-1407/med-8.1 | (°▲+27.0pp (10/17) net+208/med+2.7) |
| S0-H11 | keep-watching | ▲+2.3pp (64/263) net+863/med+0.9 | ▼-2.3pp (26/91) net+264/med-3.9 | ·+0.1pp (35/159) net+960/med+2.4 | ▼-8.7pp (6/26) net+117/med-10.2 |
| S0-H12 | keep-watching | — | — | — | — |
| **union coverage** | | 40.0% (46/115) | 31.7% (13/41) | 84.4% (27/32) | 90.9% (10/11) |

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



---

# us30 (us30fut) — PROVISIONAL

> **PROVISIONAL — validation pending (register 40 fence as amended 2026-08-19): replay-only study over the synced store; canonical status, live attachment, and Asia/pause-sensitive cell interpretation await this instrument's validation evening. EXPLORATORY first cross-instrument look — expectations deliberately unregistered; anything interesting becomes a pre-registered question before it becomes a claim. NO POOLING across instruments.**
>
> - drift-adjustment segments and engine tod baselines run on the provider/London trading-day structure; native cash-hour segmentation is part of this instrument's validation evening
> - sessions = the registered register-37 world-clock partition (native-tz, DST-proof) applied to this instrument's own bars; 'london' is not the home session of the US pairs
> - the forward window (>= go_live) is also a replay over the synced store — this instrument has NO live attachment yet

Store span (1M, close ts): 2026-07-19 22:02:00+00:00 → 2026-08-19 22:25:00+00:00. Volume type: real futures volume (register 40 first-sync sanity; canonical verdict at this instrument's validation evening).

## Summary Matrix (page 1)

Engine `6e7db5af5` — OBSERVATIONAL signal scoreboard - move-detection, not trading; no fills exist here by construction; never validation (docs/hypothesis_lifecycle.md stage 4)

**Review labels are RECOMMENDATIONS — none actioned, review pending operator familiarity.** Cells: marker + precision LIFT vs that context's OWN chance rate, (hits/fires), payoff net/median points (directional rows; either-direction rows have no payoff by construction). ▲/▼ = beyond ±2pp of chance, · = within. (°…) = small-n (fires<20 or episodes<10): dimmed, excluded from any future label arithmetic. Read READING_GUIDE.md first; full detail in signal_scoreboard.json.

| H | label | backtest whole | backtest london | forward whole | forward london |
|---|---|---|---|---|---|
| *context* | | 109 ep; chance 24.0%dir/44.6%either | 35 ep; chance 36.4%dir/66.0%either | 30 ep; chance 22.8%dir/43.6%either | 9 ep; chance 37.6%dir/70.6%either |
| S0-H1 | keep-watching | ▲+8.7pp (16/49) net-83/med-8.0 | (°▼-7.0pp (5/17) net-113/med-17.5) | ▲+12.2pp (14/40) net-43/med-1.2 | (°▲+8.6pp (6/13) net+80/med-9.5) |
| S1-H1 | keep-watching | (°▼-24.0pp (0/2) net-18/med-9.2) | (°▼-36.4pp (0/1) net-50/med-50.0) | (°▼-22.8pp (0/1) net-50/med-50.0) | (°▼-37.6pp (0/1) net-50/med-50.0) |
| S0-H2 | promote-candidate | ·+1.6pp (72/281) net-2432/med-4.0 | ▼-2.5pp (21/62) net-337/med-20.0 | ▲+4.2pp (38/141) net-600/med-1.0 | (°·-0.4pp (16/43) net-554/med-10.0) |
| S1-H2 | promote-candidate | ▲+2.8pp (59/220) net-505/med-2.8 | ·-0.4pp (18/50) net-218/med-18.0 | ▲+3.4pp (28/107) net+223/med-0.5 | (°▼-5.5pp (9/28) net+86/med+0.8) |
| S0-H3 | keep-watching | (°·+1.0pp (1/4) net+59/med+13.2) | (°▼-36.4pp (0/2) net-22/med-11.0) | — | — |
| S0-H4 | keep-watching | (°▲+14.5pp (5/13) net+194/med+15.0) | (°▲+35.0pp (5/7) net+392/med+71.0) | — | — |
| S0-H5 | keep-watching | (°▼-24.0pp (0/1) net-135/med-135.0) | (°▼-36.4pp (0/1) net-135/med-135.0) | (°▲+77.2pp (1/1) net+24/med+24.0) | (°▲+62.4pp (1/1) net+24/med+24.0) |
| S0-H6 | keep-watching | ▼-21.3pp (10/52) [cls-chance 40.5% vs uncond 24.0%] net-1151/med-25.2 | ▼-28.4pp (3/24) [cls-chance 40.9% vs uncond 36.4%] net-664/med-30.0 | ▲+4.5pp (12/26) [cls-chance 41.7% vs uncond 22.8%] net-408/med-7.5 | (°▲+47.1pp (10/11) [cls-chance 43.8% vs uncond 37.6%] net+357/med+27.0) |
| S0-H7 | keep-watching | ▼-2.0pp (9/41) net+205/med-9.0 | (°▼-5.2pp (5/16) net-161/med-7.0) | (°▲+12.5pp (6/17) net+114/med+4.0) | (°▲+2.4pp (2/5) net-175/med-36.0) |
| S0-H7 (either-dir) | keep-watching | ▼-3.1pp (17/41) | (°▲+2.8pp (11/16)) | (°▲+21.1pp (11/17)) | (°▲+29.4pp (5/5)) |
| S0-H8 | keep-watching | ▲+7.4pp (146/281) | ▲+6.6pp (45/62) | ▲+3.2pp (66/141) | (°▼-7.8pp (27/43)) |
| S0-H9 | keep-watching | ·-1.5pp (9/40) net-353/med-14.7 | (°▼-3.1pp (1/3) net-198/med-61.5) | (°▼-17.2pp (1/18) net-752/med-33.5) | (°▼-23.3pp (1/7) net-558/med-93.5) |
| S1-H9 | keep-watching | (°·-1.8pp (2/9) net+460/med+1.5) | (°▼-36.4pp (0/1) net-38/med-38.0) | (°▼-11.7pp (1/9) net-570/med-76.0) | (°▼-20.9pp (1/6) net-500/med-95.5) |
| S0-H10 | deprioritize | ·+0.0pp (37/154) net+1774/med+11.0 | ▲+3.6pp (16/40) net+1480/med+27.5 | ▼-7.3pp (20/129) net-237/med-1.0 | (°▼-17.6pp (5/25) net-195/med-18.5) |
| S0-H11 | keep-watching | ▲+3.4pp (113/413) net+1254/med+3.0 | ·+1.0pp (61/163) net-404/med+5.0 | ▲+3.4pp (61/233) net-738/med-6.0 | (°▼-3.9pp (35/104) net-264/med-5.0) |
| S0-H12 | keep-watching | — | — | — | — |
| **union coverage** | | 40.4% (44/109) | 34.3% (12/35) | 90.0% (27/30) | 88.9% (8/9) |

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



---

Appendix: the per-session detail beyond London and every horizon-mark payoff live in signal_scoreboard.json (generated, same run).