"""Broker simulator — prompt Part 7 + Part A execution-vehicle
pre-registration (2026-08-13).

Two vehicles (config execution_vehicle.mode):

direct   — legacy: fills on the signal instrument itself, whole contracts,
           commission + flat slippage.
cash_cfd — deployment reality: signals/levels/stops/R computed on uk100fut;
           EXECUTION on the uk100 cash CFD (spread bet). Fills at the cash
           leg's measured bid/ask (long entry at ask, exit at bid; mirror
           for shorts), intrabar resolution on cash 1M, per-GBP-per-point
           sizing with a configurable minimum stake, NO commission, no roll
           on the execution leg. Stop/target LEVELS are mapped from futures
           to cash by the basis measured at entry (fut - cash); intraday
           basis stability (std 0.19 pts, 2026-08-13) + the EOD-flat
           precondition (asserted here) make that offset sound — basis
           steps/drift never touch an open position. R distances stay in
           futures points.

Common fill discipline: decisions on closes, fills no earlier than next
bar; stop-first when one 1M bar touches stop and target; gap-through-stop
fills at the (worse) open.
"""

LONG, SHORT = 1, -1


class Broker:
    def __init__(self, cfg, narrative, eod_fn=None, point_value=1.0,
                 tick_size=1.0, inert=False):
        self.cfg = cfg
        self.narrative = narrative
        self.eod_fn = eod_fn or (lambda ts: False)
        self.point_value = point_value
        self.tick = tick_size
        self.mode = cfg.execution_vehicle.mode
        if (self.mode == "cash_cfd" and cfg.execution_vehicle.require_eod_flat
                and not inert):
            if eod_fn is None:
                raise ValueError(
                    "cash_cfd vehicle requires EOD-flat: an eod_fn must be "
                    "wired (basis-offset stops are only sound intraday)")
        self.equity = cfg.trade.starting_equity
        self.position = None
        self.trades = []
        self.skipped_size = 0
        self.current_quote = None       # cash-leg 1M quote {o,h,l,c,spread}

    # ------------------------------------------------------------- quotes

    def set_quote(self, quote):
        """Cash execution-leg quote for the current exec timestamp
        (mid OHLC + measured spread). Set by the loop before exec-bar
        processing; None where the quote leg has a gap."""
        self.current_quote = quote

    def _ask(self, px):
        return px + self.current_quote["spread"] / 2

    def _bid(self, px):
        return px - self.current_quote["spread"] / 2

    # ------------------------------------------------------------------ entry

    def open_position(self, entry):
        if self.mode == "direct":
            return self._open_direct(entry)
        return self._open_cash_cfd(entry)

    def _open_cash_cfd(self, entry):
        """entry carries FUTURES prices (order price, stop). Map to the cash
        leg via the basis at entry; fill at ask (long) / bid (short)."""
        v = self.cfg.execution_vehicle
        q = self.current_quote
        if q is None:
            self._log("SKIPPED_SIZE", entry["entry_ts"],
                      reason="no_cash_quote_at_entry")
            self.skipped_size += 1
            return False
        d = entry["dir"]
        basis = entry["price"] - q["open"]           # fut - cash, at entry
        fill = self._ask(q["open"]) if d == LONG else self._bid(q["open"])
        entry["fill"] = fill
        entry["basis_at_entry"] = basis
        stop_cash = entry["stop"] - basis
        stop_dist = abs(entry["price"] - entry["stop"])   # R stays in fut pts
        if stop_dist <= 0:
            self._log("SKIPPED_SIZE", entry["entry_ts"], reason="zero_stop_distance")
            self.skipped_size += 1
            return False
        risk = self.equity * self.cfg.trade.risk_frac
        stake = int(risk / stop_dist * 100) / 100.0       # GBP/pt, 1p steps
        if stake < v.min_stake_per_point:
            self.skipped_size += 1
            self._log("SKIPPED_SIZE", entry["entry_ts"], stake=stake,
                      min_stake=v.min_stake_per_point)
            return False
        t = self.cfg.trade
        self.position = {
            "vehicle": "cash_cfd", "dir": d, "entry": fill,
            "entry_ts": entry["entry_ts"], "stop": stop_cash,
            "stop_dist": stop_dist, "stake": stake, "contracts": None,
            "basis_at_entry": basis,
            "target": (fill + d * t.r_target * stop_dist
                       if t.exit_mode == "fixed_r" else None),
            "signal_bars_held": 0, "exit_pending": None, "meta": entry,
        }
        return True

    def _open_direct(self, entry):
        t = self.cfg.trade
        d = entry["dir"]
        fill = entry["price"] + t.slippage_ticks * self.tick * d
        entry["fill"] = fill
        stop_dist = abs(fill - entry["stop"])
        if stop_dist <= 0:
            self._log("SKIPPED_SIZE", entry["entry_ts"], reason="zero_stop_distance")
            self.skipped_size += 1
            return False
        risk = self.equity * t.risk_frac
        contracts = int(risk // (stop_dist * self.point_value))
        if contracts < 1:
            self.skipped_size += 1
            self._log("SKIPPED_SIZE", entry["entry_ts"],
                      stop_dist=stop_dist, risk=risk)
            return False
        r = t.r_target * stop_dist
        self.position = {
            "vehicle": "direct", "dir": d, "entry": fill,
            "entry_ts": entry["entry_ts"], "stop": entry["stop"],
            "stop_dist": stop_dist, "contracts": contracts, "stake": None,
            "basis_at_entry": None,
            "target": (fill + r if d == LONG else fill - r)
            if t.exit_mode == "fixed_r" else None,
            "signal_bars_held": 0, "exit_pending": None, "meta": entry,
        }
        return True

    # -------------------------------------------------------------- exec bars

    def on_exec_bar(self, bar):
        """Exits resolved on the EXECUTION LEG's 1M bars: the cash quote in
        cash_cfd mode (long exits at bid, short at ask), the bar itself in
        direct mode."""
        p = self.position
        if p is None:
            return
        d = p["dir"]
        if p["vehicle"] == "cash_cfd":
            q = self.current_quote
            if q is None:
                self._log("EXEC_QUOTE_GAP", bar.ts)
                return
            side = self._bid if d == LONG else self._ask   # exit side
            o, hi, lo = side(q["open"]), side(q["high"]), side(q["low"])
            close_px = side(q["close"])
        else:
            o, hi, lo, close_px = bar.open, bar.high, bar.low, bar.close
        if p["exit_pending"] is not None:
            self._close(bar.ts, o, p["exit_pending"], raw=True)
            return
        if (d == LONG and o <= p["stop"]) or (d == SHORT and o >= p["stop"]):
            self._close(bar.ts, o, "STOP_GAP", raw=True)
            return
        stop_hit = (lo <= p["stop"] if d == LONG else hi >= p["stop"])
        tgt = p["target"]
        tgt_hit = (tgt is not None
                   and (hi >= tgt if d == LONG else lo <= tgt))
        if stop_hit:                       # stop first when both touch
            self._close(bar.ts, p["stop"], "STOP", raw=True)
            return
        if tgt_hit:
            self._close(bar.ts, tgt, "TARGET", raw=True)
            return
        if self.eod_fn(bar.ts):
            self._close(bar.ts, close_px, "EOD_EXIT", raw=True)

    # ------------------------------------------------------- signal-TF closes

    def on_signal_close(self, bar, ctx_tf, opposing_confirm):
        p = self.position
        if p is None:
            return
        p["signal_bars_held"] += 1
        t = self.cfg.trade
        if p["signal_bars_held"] >= t.time_stop_bars:
            p["exit_pending"] = "TIME_STOP"
            return
        if t.exit_mode == "opposing" and opposing_confirm:
            p["exit_pending"] = "OPPOSING_CONFIRM"
            return
        if t.exit_mode == "context_flip" and ctx_tf is not None:
            against = "MARKDOWN" if p["dir"] == LONG else "MARKUP"
            if ctx_tf.phase == against:
                p["exit_pending"] = "CONTEXT_FLIP"

    # ------------------------------------------------------------------ close

    def _close(self, ts, price, reason, raw=False):
        p = self.position
        d = p["dir"]
        if p["vehicle"] == "cash_cfd":
            fill = price                   # price is already on the exit side
            points = (fill - p["entry"]) * d
            gross = points * p["stake"]    # GBP/pt sizing; no commission
            costs = 0.0
        else:
            t = self.cfg.trade
            slip = t.slippage_ticks * self.tick
            fill = price - slip * d
            points = (fill - p["entry"]) * d
            gross = points * self.point_value * p["contracts"]
            costs = 2 * t.commission_per_contract * p["contracts"]
        pnl = gross - costs
        self.equity += pnl
        trade = {
            "entry_ts": p["entry_ts"], "exit_ts": ts, "dir": d,
            "entry": p["entry"], "exit": fill, "stop": p["stop"],
            "contracts": p["contracts"], "stake": p["stake"],
            "vehicle": p["vehicle"], "basis_at_entry": p["basis_at_entry"],
            "points": points,
            "r_multiple": points / p["stop_dist"] if p["stop_dist"] else 0.0,
            "pnl": pnl, "costs": costs, "reason": reason,
            "equity_after": self.equity,
            "spec": p["meta"]["h"]["spec"], "hdir": p["meta"]["h"]["dir"],
            "gate_tag": p["meta"].get("gate_tag"),
            "confirm_branch": p["meta"]["h"].get("confirm_branch"),
            "entry_tag": p["meta"].get("tag"),
            "signal_bars_held": p["signal_bars_held"],
        }
        self.trades.append(trade)
        self.position = None
        self._log("EXIT", ts, reason=reason, price=fill,
                  r=round(trade["r_multiple"], 2), pnl=round(pnl, 2),
                  equity=round(self.equity, 2))

    def _log(self, typ, ts, **payload):
        self.narrative.log(typ, ts=ts, **payload)
