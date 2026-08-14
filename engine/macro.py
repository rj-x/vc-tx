"""Macro release calendar — validation-on-load, not trust-on-load.

A corrupt row in this file mistags silently; validation makes it loud.
Every consumer (campaign tagger, staging fetcher) loads through here and
HARD-FAILS on: schema mismatch, non-Z-suffixed or unparseable timestamps,
non-monotonic ordering, or the NFP anchor violation (any row whose name
contains "Non-Farm" must sit at 12:30 or 13:30 UTC — US DST-dependent).

Scope contract (register, amended 2026-08-14): CAPTURE-ALL at staging,
CONSUME-FILTERED per instrument config (macro_relevance); live schema
utc_time,currency,impact,name; used for ex-post tagging and the macro-spike volume check
exclusively; never engine-facing without clock-gating (actuals are
post-release information).
"""

import pandas as pd

SCHEMA = ["utc_time", "currency", "impact", "name"]
IMPACTS = {"High", "Medium", "Low", "Holiday"}
NFP_ANCHORS = {(12, 30), (13, 30)}


class MacroCalendarError(ValueError):
    pass


def load_and_validate(path, warn_fn=print):
    """Returns the calendar with a parsed `ts` column, or raises
    MacroCalendarError. An empty (header-only) file is valid. Warns (never
    fails) via warn_fn when the newest event is stale (>~10 days)."""
    df = pd.read_csv(path)
    if list(df.columns)[:4] != SCHEMA:      # staging may carry extras
        raise MacroCalendarError(           # (forecast/previous); live is lean
            f"{path}: schema {list(df.columns)[:4]} != {SCHEMA}")
    if not df.empty:
        bad = ~df["impact"].isin(IMPACTS)
        if bad.any():
            raise MacroCalendarError(
                f"{path}: invalid impact values: "
                f"{df.loc[bad, 'impact'].unique().tolist()}")
    if df.empty:
        df["ts"] = pd.Series(dtype="datetime64[ns, UTC]")
        return df
    bad_suffix = ~df["utc_time"].astype(str).str.endswith("Z")
    if bad_suffix.any():
        raise MacroCalendarError(
            f"{path}: rows without Z suffix: "
            f"{df.loc[bad_suffix, 'utc_time'].tolist()}")
    try:
        ts = pd.to_datetime(df["utc_time"], utc=True,
                            format="%Y-%m-%dT%H:%M:%SZ")
    except (ValueError, TypeError) as e:
        raise MacroCalendarError(f"{path}: unparseable utc_time: {e}") from e
    if not ts.is_monotonic_increasing:
        raise MacroCalendarError(f"{path}: timestamps not monotonically "
                                 f"non-decreasing")
    nfp = df["name"].str.contains("Non-Farm", case=False, na=False)
    for t in ts[nfp]:
        if (t.hour, t.minute) not in NFP_ANCHORS:
            raise MacroCalendarError(
                f"{path}: NFP anchor violation — '{t}' not at 12:30/13:30 UTC")
    out = df.copy()
    out["ts"] = ts

    # staleness guard: if the newest event is >~10 days old, a week went
    # uncaptured and needs manual backfill (warn — validity is unaffected)
    age_days = (pd.Timestamp.now(tz="UTC") - ts.max()) / pd.Timedelta(days=1)
    if age_days > 10:
        warn_fn(f"!! MACRO CALENDAR STALE: newest event in {path} is "
                f"{age_days:.0f} days old — a week likely went uncaptured; "
                f"backfill manually (see DATA.md/register ruling 4).")
    return out
