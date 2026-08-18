"""Event-study layer (prompt Part 8): forward mid returns after every
CONFIRMED hypothesis — regardless of gating, sizing, EOD, or whether a trade
resulted — vs matched baseline bars. Reporting-layer only: computed after
the run, never fed back into decisions."""

import numpy as np
import pandas as pd

from backtest.horizons import STANDARD_HORIZONS as HORIZONS  # registry: standard outcome horizons (R1 ruling 2026-08-18)


def event_study(events, signal_bars):
    """events: narrative events; signal_bars: non-stub Signal-TF Bars in
    order. Baselines are matched by session phase (pre/post US open)."""
    bars = [b for b in signal_bars if not b.is_stub]
    closes = np.array([b.close for b in bars])
    ts_ix = {b.ts: i for i, b in enumerate(bars)}

    def _phase(ts):
        lon = pd.Timestamp(ts).tz_convert("Europe/London")
        return "pre_US" if lon.hour + lon.minute / 60.0 < 14.5 else "post_US"

    phases = np.array([_phase(b.ts) for b in bars])

    def fwd(i, k):
        return ((closes[i + k] - closes[i]) / closes[i]
                if i + k < len(closes) else None)

    graduated = {e["h"]["id"] for e in events if e["type"] == "GRADUATED"}
    rows = []
    for e in events:
        if e["type"] != "CONFIRM":
            continue
        i = ts_ix.get(e["ts"])
        if i is None:
            continue
        h = e["h"]
        row = {"spec": h["spec"], "dir": h["dir"],
               "gated_through": h["id"] in graduated,
               "branch": e.get("branch"), "phase": phases[i]}
        for k in HORIZONS:
            r = fwd(i, k)
            row[f"fwd_{k}"] = None if r is None else r * h["dir"]  # signed
        rows.append(row)

    ev = pd.DataFrame(rows)
    base = {}
    for ph in ("pre_US", "post_US"):
        mask = phases == ph
        for k in HORIZONS:
            rs = [(closes[i + k] - closes[i]) / closes[i]
                  for i in np.nonzero(mask)[0] if i + k < len(closes)]
            base[(ph, k)] = {"mean_abs": float(np.mean(np.abs(rs))) if rs else None,
                             "std": float(np.std(rs)) if rs else None,
                             "n": len(rs)}
    return ev, base


# label direction: sign under which a label's forward return counts as
# "correct" (bullish +1 / bearish -1); unsigned classes report raw returns
LABEL_DIR = {
    "VALIDATED_ADVANCE": 1, "EFFORTLESS_ADVANCE": 1, "SPRING": 1,
    "NO_SUPPLY": 1, "POTENTIAL_SELLING_CLIMAX": 1,
    "VALIDATED_DECLINE": -1, "EFFORTLESS_DECLINE": -1, "UPTHRUST": -1,
    "NO_DEMAND": -1, "POTENTIAL_BUYING_CLIMAX": -1,
    "ABSORPTION": 0, "TEST": 0, "APATHY": 0,
}


def label_event_study(events, signal_bars, sig_tf):
    """Per-LABEL-class forward returns — the powered readout while trade
    samples are thin. Reports BOTH raw and DRIFT-ADJUSTED excess returns:
    excess = label forward return minus the unconditional same-phase,
    same-horizon mean drift over the same window — a rising tape makes
    every bearish label look wrong-way in raw terms; excess removes that
    tape contamination."""
    bars = [b for b in signal_bars if not b.is_stub]
    closes = np.array([b.close for b in bars])
    ts_ix = {b.ts: i for i, b in enumerate(bars)}

    def _phase(ts):
        lon = pd.Timestamp(ts).tz_convert("Europe/London")
        return "pre_US" if lon.hour + lon.minute / 60.0 < 14.5 else "post_US"

    phases = np.array([_phase(b.ts) for b in bars])

    # unconditional signed drift per (phase, horizon) over the same window
    drift = {}
    for ph in ("pre_US", "post_US"):
        for k in HORIZONS:
            rs = [(closes[i + k] - closes[i]) / closes[i]
                  for i in np.nonzero(phases == ph)[0] if i + k < len(closes)]
            drift[(ph, k)] = float(np.mean(rs)) if rs else 0.0

    rows = []
    for e in events:
        if e["type"] != "LABEL" or e.get("tf") != sig_tf or not e.get("label"):
            continue
        i = ts_ix.get(e["ts"])
        if i is None:
            continue
        d = LABEL_DIR.get(e["label"], 0)
        row = {"label": e["label"], "signed": d != 0,
               "segment": e.get("segment", "cash")}
        for k in HORIZONS:
            if i + k < len(closes):
                raw = (closes[i + k] - closes[i]) / closes[i]
                exc = raw - drift[(phases[i], k)]
                row[f"raw_{k}"] = raw * d if d else raw
                row[f"exc_{k}"] = exc * d if d else exc
            else:
                row[f"raw_{k}"] = row[f"exc_{k}"] = None
        rows.append(row)
    ev = pd.DataFrame(rows)
    out = {"drift_bps": {f"{ph}_{k}": round(v * 1e4, 2)
                         for (ph, k), v in drift.items()}}
    if ev.empty:
        return out
    for (label, seg), g in ev.groupby(["label", "segment"]):
        label = f"{label} [{seg}]" if seg != "cash" else label
        entry = {"n": len(g), "signed": bool(g["signed"].iloc[0])}
        for k in HORIZONS:
            raw = g[f"raw_{k}"].dropna()
            exc = g[f"exc_{k}"].dropna()
            if len(raw):
                entry[f"raw_{k}_mean_bps"] = round(raw.mean() * 1e4, 2)
                entry[f"excess_{k}_mean_bps"] = round(exc.mean() * 1e4, 2)
                if entry["signed"]:
                    entry[f"excess_{k}_hit"] = round(float((exc > 0).mean()), 3)
        out[label] = entry
    return out


def summarize_event_study(ev, base):
    if ev is None or ev.empty:
        return {"n_confirms": 0}
    out = {"n_confirms": len(ev)}
    for (spec, gated), g in ev.groupby(["spec", "gated_through"]):
        key = f"{spec}{'_gated' if gated else '_ungated'}"
        entry = {"n": len(g)}
        for k in HORIZONS:
            vals = g[f"fwd_{k}"].dropna()
            if len(vals):
                entry[f"fwd_{k}_mean_bps"] = round(vals.mean() * 1e4, 2)
                entry[f"fwd_{k}_hit"] = round((vals > 0).mean(), 3)
        out[key] = entry
    out["baseline"] = {f"{ph}_{k}": v for (ph, k), v in base.items()}
    return out
