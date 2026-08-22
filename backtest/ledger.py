"""Opportunity ledger — a REVIEW SURFACE, not an evidential artifact.

Generated (never hand-written) from narrative events: one row per
hypothesis instance, plus 1min SPRING/UPTHRUST label prints as "signature
moments, not hypotheses — observational". No new analysis; no forward
returns (that's the event study's job). CSV columns are chart-overlay
friendly (ISO timestamps in BOTH conventions, price level, marker type)
for manual TradingView placement.
"""

import csv

import pandas as pd

_TFMIN = {"1min": 1, "3min": 3, "5min": 5, "15min": 15, "30min": 30,
          "1h": 60, "1d": None}

CSV_COLS = ["timestamp_close_iso", "timestamp_open_iso", "marker_type",
            "price_level", "direction", "segment", "outcome", "gate_branch",
            "strength_trajectory", "variant", "entry", "stop", "exit",
            "location_ref", "location_level", "dist_pts", "dist_signal_atr"]


def _iso(ts):
    return pd.Timestamp(ts).isoformat()


def _open_iso(ts, tf):
    m = _TFMIN.get(tf)
    return _iso(pd.Timestamp(ts) - pd.Timedelta(minutes=m)) if m else ""


def hypothesis_rows(events, trades, sig_tf, variant):
    """One row per hypothesis instance (by id) seen in `events`."""
    hyp = {}
    for e in events:
        h = e.get("h")
        if not h or h.get("id") is None:
            continue
        r = hyp.setdefault(h["id"], {
            "spec": h["spec"], "dir": h["dir"],
            "sig_extreme": h.get("sig_extreme"),
            "segment": h.get("spawn_segment", "cash"),
            "spawn_ts": None, "strengths": ["1.0"], "gate_branch": "",
            "outcome": "EXPIRED", "entry": "", "stop": "", "exit": "",
            "_confirmed": False, "_traded": False, "_obs": False,
        })
        t = e["type"]
        if t == "SPAWNED":
            r["spawn_ts"] = e["ts"]
            r["segment"] = h.get("spawn_segment", r["segment"])
        elif t == "STRENGTH":
            r["strengths"].append(f"{h['strength']:.1f}")
        elif t == "CONFIRM":
            r["_confirmed"] = True
        elif t in ("GATE", "GATE_RECHECK"):
            r["gate_branch"] = e.get("branch", r["gate_branch"])
        elif t in ("REFUTED", "EXPIRED", "KILLED_WEAK"):
            r["outcome"] = t
        elif t == "CONFIRMED_PENDING_GATE":
            r["_confirmed"] = True
        elif t in ("SIGNAL_EXTENDED_OBSERVATIONAL", "SIGNAL_NARRATIVE_ONLY"):
            r["_obs"] = t == "SIGNAL_EXTENDED_OBSERVATIONAL"
        elif t == "ENTRY":
            r["_traded"] = True
            r["entry"] = e.get("fill", e.get("price"))
            r["stop"] = e.get("stop")
            r["_entry_ts"] = e.get("entry_ts")
    by_entry = {str(t["entry_ts"]): t for t in trades}
    out = []
    for hid in sorted(hyp):
        r = hyp[hid]
        if r["spawn_ts"] is None:
            continue                      # pre-window fragment (narrate)
        if r["_traded"]:
            r["outcome"] = "CONFIRMED_TRADED"
            tr = by_entry.get(str(r.get("_entry_ts")))
            if tr:
                r["exit"] = tr["exit"]
        elif r["_obs"]:
            r["outcome"] = "EXTENDED_OBSERVATIONAL"
        elif r["_confirmed"]:
            r["outcome"] = "CONFIRMED_GATED"
        out.append({
            "timestamp_close_iso": _iso(r["spawn_ts"]),
            "timestamp_open_iso": _open_iso(r["spawn_ts"], sig_tf),
            "marker_type": f"{r['spec']}_{'LONG' if r['dir'] == 1 else 'SHORT'}",
            "price_level": r["sig_extreme"],
            "direction": "LONG" if r["dir"] == 1 else "SHORT",
            "segment": r["segment"], "outcome": r["outcome"],
            "gate_branch": r["gate_branch"],
            "strength_trajectory": "->".join(r["strengths"]),
            "variant": variant, "entry": r["entry"], "stop": r["stop"],
            "exit": r["exit"], "location_ref": "", "location_level": "",
            "dist_pts": "", "dist_signal_atr": "",
        })
    return out


def signature_moment_rows(events, exec_tf, variant, scope="signatures"):
    """Section-2 rows. scope='signatures' (default): 1min SPRING/UPTHRUST
    prints. scope='all_labels': EVERY structural label at EVERY running TF
    (narrate needs --ladder for ladder-rung rows). Not hypotheses."""
    out = []
    for e in events:
        if e["type"] != "LABEL" or not e.get("label"):
            continue
        if scope == "signatures":
            if not (e.get("tf") == exec_tf
                    and e.get("label") in ("SPRING", "UPTHRUST")):
                continue
        if True:
            spring = e["label"] == "SPRING"
            out.append({
                "timestamp_close_iso": _iso(e["ts"]),
                "timestamp_open_iso": _open_iso(e["ts"], exec_tf),
                "marker_type": f"{e['label']}_{e.get('tf')}_OBSERVATIONAL",
                "price_level": (e.get("low") if spring else
                                e.get("high") if e["label"] == "UPTHRUST"
                                else e.get("close")),
                "direction": ("LONG" if spring else
                              "SHORT" if e["label"] == "UPTHRUST" else ""),
                "segment": e.get("segment", "cash"),
                "outcome": "SIGNATURE_MOMENT", "gate_branch": "",
                "strength_trajectory": "", "variant": variant,
                "entry": "", "stop": "", "exit": "",
                "location_ref": e.get("location_ref", ""),
                "location_level": e.get("location_level", ""),
                "dist_pts": e.get("dist_pts", ""),
                "dist_signal_atr": e.get("dist_signal_atr", ""),
            })
    return out


def write_ledger(hyp_rows, sig_rows, md_path, csv_path):
    with open(csv_path, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=CSV_COLS)
        w.writeheader()
        for r in hyp_rows + sig_rows:
            w.writerow(r)
    L = ["# Opportunity Ledger (GENERATED — review surface, non-evidential)",
         "Terms: [docs/GLOSSARY.md](docs/GLOSSARY.md).", "",
         "", "No forward returns here by design (event study's job). "
         "Timestamps in both conventions: close-stamped and open-stamped "
         "(close − TF).", "",
         "## Hypothesis instances", "",
         "| Spawn (close) | Type | Level | Segment | Strength | Outcome "
         "| Gate | Variant | Entry/Stop/Exit |", "|" + "---|" * 9]
    for r in hyp_rows:
        ese = (f"{r['entry']}/{r['stop']}/{r['exit']}"
               if r["entry"] != "" else "")
        L.append(f"| {r['timestamp_close_iso']} | {r['marker_type']} "
                 f"| {r['price_level']} | {r['segment']} "
                 f"| {r['strength_trajectory']} | {r['outcome']} "
                 f"| {r['gate_branch']} | {r['variant']} | {ese} |")
    L += ["", "## Signature moments (1min SPRING/UPTHRUST) — "
          "**not hypotheses; observational**", "",
          "| Close ts | Marker | Level | Segment | Location (dist pts / "
          "Signal-ATR) | Variant |",
          "|" + "---|" * 6]
    for r in sig_rows:
        loc = (f"{r['location_ref']} {r['dist_pts']}pts/"
               f"{r['dist_signal_atr']}ATR" if r["location_ref"] else "")
        L.append(f"| {r['timestamp_close_iso']} | {r['marker_type']} "
                 f"| {r['price_level']} | {r['segment']} | {loc} "
                 f"| {r['variant']} |")
    with open(md_path, "w") as f:
        f.write("\n".join(L) + "\n")
