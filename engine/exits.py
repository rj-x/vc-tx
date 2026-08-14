"""Trade-management library (2026-08-14): named, unit-tested exit schemes.
THE PRE-DECLARED EXIT-COMPARISON UNIVERSE FOR WALK-FORWARD (register item 14).
Each scheme is a config object with explicit parameters. Trailing obeys the
same intrabar rules as stops (1M resolution, stop-first on ambiguity,
gap-through fills at open) — schemes only MOVE levels; the broker fills.

Schemes: fixed_points, r_multiple, atr_k, beyond_swing_n, beyond_signature_n,
trail_atr, trail_swing, breakeven_at_r. Composable: one initial-stop source,
optional target, optional trailing/breakeven modifiers.
"""

LONG, SHORT = 1, -1


class ExitScheme:
    """cfg example: {name: r_multiple, r: 2.0, trail: {name: trail_atr, k: 2},
    breakeven_at_r: 1.0, stop: {name: beyond_signature_n, buffer_ticks: 2}}"""

    def __init__(self, cfg_dict, tick=1.0):
        if hasattr(cfg_dict, "raw"):
            cfg_dict = cfg_dict.raw()     # accept Cfg wrappers
        self.c = dict(cfg_dict or {})
        self.tick = tick
        self.name = self.c.get("name", "r_multiple")

    # ---- initial stop (fut points; router supplies signature default) ----
    def initial_stop(self, d, fill, signature_stop, atr, swings):
        s = self.c.get("stop", {"name": "beyond_signature_n"})
        n = s.get("name", "beyond_signature_n")
        if n == "beyond_signature_n":
            return signature_stop
        if n == "fixed_points":
            return fill - d * s["points"]
        if n == "atr_k":
            return fill - d * s["k"] * atr if atr else signature_stop
        if n == "beyond_swing_n":
            idx = s.get("n", 1)
            lv = (swings or {}).get("low" if d == LONG else "high")
            buf = s.get("buffer_ticks", 2) * self.tick
            if lv is None:
                return signature_stop
            return lv - buf if d == LONG else lv + buf
        raise ValueError(f"unknown stop scheme {n}")

    # ---- target ----
    def target(self, d, fill, stop):
        if self.name == "r_multiple":
            return fill + d * self.c.get("r", 2.0) * abs(fill - stop)
        if self.name == "fixed_points":
            return fill + d * self.c["points"]
        return None                        # opposing/context_flip/time handled upstream

    # ---- per-bar level updates (trailing tightens only, never loosens) ----
    def update_stop(self, pos, bar_hi, bar_lo, atr, swings):
        d, stop = pos["dir"], pos["stop"]
        new = stop
        tr = self.c.get("trail")
        if tr:
            if tr["name"] == "trail_atr" and atr:
                cand = (bar_hi - tr["k"] * atr if d == LONG
                        else bar_lo + tr["k"] * atr)
                new = max(new, cand) if d == LONG else min(new, cand)
            elif tr["name"] == "trail_swing" and swings:
                lv = swings.get("low" if d == LONG else "high")
                if lv is not None:
                    buf = tr.get("buffer_ticks", 2) * self.tick
                    cand = lv - buf if d == LONG else lv + buf
                    new = max(new, cand) if d == LONG else min(new, cand)
        be = self.c.get("breakeven_at_r")
        if be is not None and pos.get("stop_dist"):
            trigger = pos["entry"] + d * be * pos["stop_dist"]
            reached = bar_hi >= trigger if d == LONG else bar_lo <= trigger
            if reached:
                new = max(new, pos["entry"]) if d == LONG else min(new, pos["entry"])
        return new
