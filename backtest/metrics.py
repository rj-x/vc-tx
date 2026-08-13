"""Trade metrics + leakage tripwire (prompt Part 8)."""

import pandas as pd


def _phase(ts):
    lon = pd.Timestamp(ts).tz_convert("Europe/London")
    return "pre_US" if lon.hour + lon.minute / 60.0 < 14.5 else "post_US"


def summarize(trades, equity0):
    if not trades:
        return {"n": 0}
    df = pd.DataFrame(trades)
    wins = df[df["pnl"] > 0]
    losses = df[df["pnl"] <= 0]
    gross_w = wins["pnl"].sum()
    gross_l = -losses["pnl"].sum()
    eq = pd.concat([pd.Series([equity0]), df["equity_after"]], ignore_index=True)
    dd = (eq - eq.cummax())
    return {
        "n": len(df),
        "win_rate": round(len(wins) / len(df), 3),
        "avg_r": round(df["r_multiple"].mean(), 3),
        "profit_factor": (round(gross_w / gross_l, 3) if gross_l > 0
                          else float("inf")),
        "total_pnl": round(df["pnl"].sum(), 2),
        "max_drawdown": round(dd.min(), 2),
        "avg_hold_signal_bars": round(df["signal_bars_held"].mean(), 1),
        "eod_exits": int((df["reason"] == "EOD_EXIT").sum()),
    }


def breakdowns(trades, equity0):
    df = pd.DataFrame(trades) if trades else pd.DataFrame()
    out = {"overall": summarize(trades, equity0)}
    if df.empty:
        return out
    df["phase"] = df["entry_ts"].map(_phase)
    for key, col in (("by_spec", None), ("by_gate_tag", "gate_tag"),
                     ("by_reason", "reason"), ("by_phase", "phase"),
                     ("by_confirm_branch", "confirm_branch"),
                     ("by_entry_tag", "entry_tag")):
        if col is None:
            groups = df.groupby(df["spec"] + df["hdir"].map(
                {1: " LONG", -1: " SHORT"}))
        else:
            groups = df.groupby(df[col].fillna("(none)"))
        out[key] = {str(g): summarize(gdf.to_dict("records"), equity0)
                    for g, gdf in groups}
    return out


def tripwire(overall):
    """Exceptional results are presumed leakage until re-verified
    (Non-Negotiable #6). Returns list of triggered flags."""
    flags = []
    if overall.get("n", 0) == 0:
        return flags
    if overall["profit_factor"] != float("inf") and overall["profit_factor"] > 2.5:
        flags.append(f"profit_factor {overall['profit_factor']} > 2.5")
    if overall["win_rate"] > 0.65 and overall.get("avg_r", 0) >= 1.0:
        flags.append(f"win_rate {overall['win_rate']} > 0.65 at avg_r "
                     f"{overall['avg_r']}")
    return flags
