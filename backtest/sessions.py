"""Session yardstick (register 37, registry entry `session_partition`;
operator order 2026-08-19). Boundaries in NATIVE exchange timezones so the
partition is DST-proof. Exact definition, one place:

  london  : [08:00 Europe/London      -> 09:30 America/New_York)
  overlap : [09:30 America/New_York   -> 16:30 Europe/London)
  ny_only : [16:30 Europe/London      -> 16:00 America/New_York)
  dead    : [16:00 America/New_York   -> 09:00 Asia/Tokyo)
  asia    : [09:00 Asia/Tokyo         -> 08:00 Europe/London)

INTERPRETATION FLAGS (operator-correctable by re-registration): (a) the
order's "(08:00-13:30 local)" parenthetical matches neither London-local
nor UTC arithmetic for "London-only ends at NY open"; the Overlap
definition ("NY open -> London close") was taken as authoritative and
London-only ends at 09:30 America/New_York. (b) "Asia open" was
unspecified; Tokyo cash open (09:00 Asia/Tokyo, DST-free) is used.
Finer cuts only by re-registration with a stated question. Episode
detection, perception, persistence remain 24/5 — sessions slice the
REPORTING, never the machinery.
"""

import pandas as pd

SESSIONS = ("london", "overlap", "ny_only", "dead", "asia")


def session_of(ts):
    t = pd.Timestamp(ts)
    t = t.tz_localize("UTC") if t.tzinfo is None else t
    lon = t.tz_convert("Europe/London")
    ny = t.tz_convert("America/New_York")
    tyo = t.tz_convert("Asia/Tokyo")
    lon_m = lon.hour * 60 + lon.minute
    ny_m = ny.hour * 60 + ny.minute
    tyo_m = tyo.hour * 60 + tyo.minute
    if lon_m >= 480 and ny_m < 570:
        return "london"
    if 570 <= ny_m < 960 and 480 <= lon_m < 990:
        return "overlap"
    if 570 <= ny_m < 960 and lon_m >= 990:
        return "ny_only"
    if tyo_m >= 540 and lon_m < 480:
        return "asia"
    return "dead"


def sessions_of_index(idx):
    """Vectorized session_of for a tz-aware DatetimeIndex -> str array."""
    import numpy as np
    lon = idx.tz_convert("Europe/London")
    ny = idx.tz_convert("America/New_York")
    tyo = idx.tz_convert("Asia/Tokyo")
    lon_m = lon.hour * 60 + lon.minute
    ny_m = ny.hour * 60 + ny.minute
    tyo_m = tyo.hour * 60 + tyo.minute
    out = np.full(len(idx), "dead", dtype=object)
    out[(tyo_m >= 540) & (lon_m < 480)] = "asia"
    out[(ny_m >= 570) & (ny_m < 960) & (lon_m >= 990)] = "ny_only"
    out[(ny_m >= 570) & (ny_m < 960) & (lon_m >= 480) & (lon_m < 990)] = "overlap"
    out[(lon_m >= 480) & (ny_m < 570)] = "london"
    return out
