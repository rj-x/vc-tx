# Runbook — Instrument Validation Evening (register 40)

**Purpose:** promote one instrument pair from PROVISIONAL to canonical.
Order: **nas100 → ger40 → us30.** Until an instrument's evening passes,
its data stays replay-only-PROVISIONAL (fence as amended 2026-08-19):
no canonical status, no live attachment, no Asia/pause-sensitive cell
interpretation.

**Total supervised time, honestly: ~35 minutes live** (one ~18-minute
probe capture you must start on time, plus ~15 minutes of paste-and-read
checks that same evening). Checks (ii)–(iv) are automated commands; only
the probe start and the final read are truly supervised.

**Recommended windows (start the probe at the native cash open — the
busy-tape baseline the uk100 template used):**

| pair | native open | probe start (UTC, DST-current) |
|---|---|---|
| nas100/nas100fut | 09:30 America/New_York | 13:30Z (EDT) / 14:30Z (EST) |
| ger40/ger40fut | 09:00 Europe/Berlin | 07:00Z (CEST) / 08:00Z (CET) |
| us30/us30fut | 09:30 America/New_York | 13:30Z / 14:30Z |

Replace `<fut>`/`<cash>` below (e.g. `nas100fut`/`nas100`).

## (i) Feed probe — SUPERVISED start (measured-contract template)

```
venv/bin/python scripts/feed_probe.py --minutes 18 --instr <fut>
```

**Do NOT inherit the FTSE findings** — this measures THIS feed's contract:
forming-bar index, settled-bar immutability, settle timing. EXPECTED:
same contract as uk100fut (0 = forming, ≥1 immutable). ANOMALY = register
finding; the instrument stays PROVISIONAL.

## (ii) Volume provenance verdict — automated (verified, not assumed)

```
venv/bin/python - <<'EOF'
import pandas as pd
fut, cash = "<fut>", "<cash>"
f = pd.read_csv(f"clean_finsa/{fut}_1min.csv", parse_dates=["time"]).set_index("time")
c = pd.read_csv(f"clean_finsa/{cash}_1min.csv", parse_dates=["time"]).set_index("time")
j = f[["volume"]].join(c[["volume"]], rsuffix="_cash", how="inner")
j = j[(j["volume"] > 0) & (j["volume_cash"] > 0)]
import numpy as np
g = np.gcd.reduce(f["volume"].astype(int).values[-5000:] % (1 << 31))
print("fut volume quantum (gcd of last 5k bars):", g)
print("cash/fut per-bar ratio median:", round((j["volume_cash"]/j["volume"]).median(), 2))
print("fut zero-volume in-cash bars %:", round(100 * (f[f["in_cash"]]["volume"] == 0).mean(), 2))
d = f[f["in_cash"]]["volume"].resample("1D").sum()
print("fut daily in-cash volume, last 5 nonzero:", list(d[d > 0].tail(5).astype(int)))
EOF
```

EXPECTED (the uk100 pattern): small integer quantum (raw contract
counts); a stable cash/fut scaling ratio; ~0% zero-volume in-cash bars;
daily totals plausibly matching the exchange future's ADV (eyeball vs
public ADV for that index future — the supervised judgment in this step).
VERDICT written per pair: "real futures volume" / "scaled" / "synthetic
(FLAG — parks the instrument)".

## (iii) Session boundaries vs the native calendar — automated + read

```
venv/bin/python - <<'EOF'
import pandas as pd
fut = "<fut>"
df = pd.read_csv(f"clean_finsa/{fut}_1min.csv", parse_dates=["time"]).set_index("time")
t = df.index[-7*1440:]
gaps = t.to_series().diff()
big = gaps[gaps > pd.Timedelta(minutes=5)]
print("recurring gaps (last ~7 days), UTC:")
for ts, g in big.items():
    print(f"  {ts - g} -> {ts}  ({g})")
EOF
```

Read the gap pattern against the market's OWN calendar (the finding-24
lesson, applied per market): daily maintenance pause (which UTC hour?
does it move with THIS market's DST or the provider's?), weekend
boundaries, holiday stubs. EXPECTED: one recurring daily pause + weekend
gap, boundaries sharp. Record the measured pause window in the register
amendment — it seeds this instrument's watchdog/session facts the way
21:00→22:05Z did for FTSE.

## (iv) Store verification in the daily run — automated

Already runs in `scripts/sync_daily.sh`; the check is reading it:
today's log shows `<fut> 14/14 passed` and `<cash> 14/14 passed`, and
`store.py verify` exits 0. Any failure = investigate before the evening
can pass.

## The register amendment a passing evening produces (template)

Append to register 40, per instrument:

> **Register 40 amendment — <pair> VALIDATED (date).** (i) Feed contract
> measured (capture `logs/feed_probe/<file>`): [forming index /
> immutability / settle timing findings]. (ii) Volume provenance:
> [verdict + quantum + ratio]. (iii) Native session boundaries measured:
> [pause window UTC + calendar anchor]. (iv) Store verification green in
> the daily run. **PROVISIONAL → CANONICAL** for replay studies AND live
> semantics; Asia/pause-sensitive cells gain "regime measured (date)".
> Remaining fences: sealed windows (register 30) and the no-pooling rule
> (register 40e) unchanged.

Then: update DATA.md's registry row (drop **validation pending**), and
the scoreboard's `PROVISIONAL_INSTRS` tuple loses the instrument — one
line, cited to the amendment.

**A failing check does the opposite:** the instrument STAYS provisional,
the anomaly becomes a numbered register finding, and nothing is worked
around (register 40d: flagged, not patched).
