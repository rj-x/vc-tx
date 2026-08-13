"""ContextTracker — slow-moving background state per timeframe (Part 3).

Strictly trailing: swings confirm k bars after the fact; every property
reflects state through the last bar passed to update(). The classifier
queries this object BEFORE update(bar_N) — i.e. state as of bar N-1 —
per the per-bar processing order.
"""

from collections import deque

# post-climax direction = direction of trades it permits (RULES Sec 8c):
# post-SELLING-climax permits LONGS (+1); post-BUYING-climax permits SHORTS
CLIMAX_LABELS = {"POTENTIAL_SELLING_CLIMAX": +1, "POTENTIAL_BUYING_CLIMAX": -1}
# registry direction: +1 = extreme is a LOW (tested from above, long context);
# -1 = extreme is a HIGH
_REGISTRY_SPECS = {
    "POTENTIAL_SELLING_CLIMAX": ("low", +1),
    "SPRING": ("low", +1),
    "POTENTIAL_BUYING_CLIMAX": ("high", -1),
    "UPTHRUST": ("high", -1),
}


class ContextTracker:
    def __init__(self, cfg, tf=""):
        self.cfg = cfg
        c = cfg.context
        self.tf = tf
        self.k = c.swing_k
        self.idx = -1
        self._bars = deque(maxlen=max(300, c.new_low_lookback + 5,
                                      c.get("move_lookback", 20) + 5))
        self._trs = deque(maxlen=c.atr_period)
        self.atr = None
        self.swings = []                 # confirmed: {type,'H'/'L', idx, price}
        self.trend = 0                   # +1 / -1 / 0
        self.trend_age = 0
        self.phase = "RANGING"
        self.post_climax = None          # {'dir': +1|-1, 'remaining': int}
        self.range_hi = None
        self.range_lo = None
        self._swings_wo_extreme = 0
        self._last_extreme_idx = 0
        self.levels = []                 # recent swing prices, newest last
        self.signature_registry = []     # {'label','idx','extreme','rel_volume','dir'}
        self.impulse_reaction = None     # 'IMPULSE' | 'REACTION' | None
        self.pullback = None             # {'start_idx','rel_vols':[],'lows':[],'max_rel_vol'}
        self.phase_log = []              # (idx, phase, trigger)

    # ------------------------------------------------------------------ update

    def update(self, bar, feats, qualified_label):
        self.idx += 1
        self._last_feats = feats
        prev_close = self._bars[-1].close if self._bars else None
        self._bars.append(bar)

        # ATR (simple mean of TR over period; session-gap clip is config, v2)
        tr = bar.spread if prev_close is None else max(
            bar.spread, abs(bar.high - prev_close), abs(bar.low - prev_close))
        self._trs.append(tr)
        if len(self._trs) == self._trs.maxlen:
            self.atr = sum(self._trs) / len(self._trs)

        self._confirm_swings()
        self._update_phase(qualified_label)
        self._update_impulse_reaction()
        self._update_registry(bar, feats, qualified_label)

    def _confirm_swings(self):
        """A swing at bar i is confirmed only at bar i+k (fractal, Part 3)."""
        k = self.k
        if len(self._bars) < 2 * k + 1:
            return
        window = list(self._bars)[-(2 * k + 1):]
        cand = window[k]
        cand_idx = self.idx - k
        # ruling 2026-08-13 (register 8): confirmation carries across the
        # session boundary — ratified as spec; tagged for diagnostics
        gap = len({b.session_id for b in window}) > 1
        if all(cand.high > b.high for b in window[:k] + window[k + 1:]):
            self._add_swing("H", cand_idx, cand.high, gap)
        if all(cand.low < b.low for b in window[:k] + window[k + 1:]):
            self._add_swing("L", cand_idx, cand.low, gap)

    def _add_swing(self, typ, idx, price, across_gap=False):
        if any(s["idx"] == idx and s["type"] == typ for s in self.swings):
            return
        self.swings.append({"type": typ, "idx": idx, "price": price,
                            "confirmed_across_gap": across_gap})
        self.swing_count = getattr(self, "swing_count", 0) + 1
        if across_gap:
            self.cross_gap_swings = getattr(self, "cross_gap_swings", 0) + 1
        if len(self.swings) > 40:
            self.swings = self.swings[-40:]

        # key levels (dedupe within ATR fraction; most recent wins)
        tol = ((self.cfg.context.level_identity_atr_frac * self.atr)
               if self.atr else 0.0)
        self.levels = [lv for lv in self.levels if abs(lv - price) > tol]
        self.levels.append(price)
        self.levels = self.levels[-12:]

        # trend from the last two swing highs + last two swing lows
        highs = [s for s in self.swings if s["type"] == "H"][-2:]
        lows = [s for s in self.swings if s["type"] == "L"][-2:]
        new_trend = self.trend
        if len(highs) == 2 and len(lows) == 2:
            hh = highs[1]["price"] > highs[0]["price"]
            hl = lows[1]["price"] > lows[0]["price"]
            lh = highs[1]["price"] < highs[0]["price"]
            ll = lows[1]["price"] < lows[0]["price"]
            if hh and hl:
                new_trend = 1
            elif lh and ll:
                new_trend = -1
            else:
                new_trend = 0
        if new_trend != self.trend:
            self.trend = new_trend
            self._trend_start_idx = self.idx

        # range tracking: new extreme beyond the established range?
        if self.range_hi is None:
            self.range_hi = price if typ == "H" else self.range_hi
            self.range_lo = price if typ == "L" else self.range_lo
            self._last_extreme_idx = idx
            return
        extended = False
        if typ == "H" and (self.range_hi is None or price > self.range_hi):
            self.range_hi = price
            extended = True
        if typ == "L" and (self.range_lo is None or price < self.range_lo):
            self.range_lo = price
            extended = True
        if extended:
            self._swings_wo_extreme = 0
            self._last_extreme_idx = idx
        else:
            self._swings_wo_extreme += 1

    def _update_phase(self, qualified_label):
        c = self.cfg.context
        if qualified_label in CLIMAX_LABELS:
            self.post_climax = {"dir": CLIMAX_LABELS[qualified_label],
                                "remaining": c.post_climax_bars}
            self._set_phase("POST_CLIMAX", qualified_label)
            return
        if self.post_climax is not None:
            self.post_climax["remaining"] -= 1
            if self.post_climax["remaining"] > 0:
                self._set_phase("POST_CLIMAX", "countdown")
                return
            self.post_climax = None      # resolve to structural phase below

        ranging = (self._swings_wo_extreme >= c.ranging_swings
                   or (self.idx - self._last_extreme_idx) >= c.ranging_bars)
        if ranging or self.trend == 0:
            self._set_phase("RANGING",
                            "no_new_extreme" if ranging else "no_trend")
        elif self.trend == 1:
            self._set_phase("MARKUP", "swing_structure")
        else:
            self._set_phase("MARKDOWN", "swing_structure")

    def _set_phase(self, phase, trigger):
        if phase != self.phase:
            self.phase_log.append((self.idx, phase, trigger))
            self._phase_change_idx = self.idx
        self.phase = phase
        self.trend_age = (self.idx - getattr(self, "_trend_start_idx", self.idx)
                          if self.trend != 0 else 0)

    def _update_impulse_reaction(self):
        c = self.cfg.context
        st = c.get("st_window", 5)
        prev_flag = self.impulse_reaction
        if self.phase == "RANGING" or self.trend == 0 or len(self._bars) < st + 1:
            self.impulse_reaction = None
        else:
            bars = list(self._bars)
            st_dir = 1 if bars[-1].close > bars[-st - 1].close else -1
            self.impulse_reaction = ("IMPULSE" if st_dir == self.trend
                                     else "REACTION")
        # pullback bookkeeping (H4): a new pullback starts on the transition
        # INTO 'REACTION'; bars are appended only while the flag is REACTION.
        if self.impulse_reaction == "REACTION":
            if prev_flag != "REACTION":
                self.pullback = {"start_idx": self.idx, "rel_vols": [],
                                 "lows": [], "highs": [], "max_rel_vol": 0.0,
                                 "last_idx": None}
            if self.pullback is not None:
                b, f = self._bars[-1], self._last_feats
                if f is not None and f.rel_volume is not None:
                    self.pullback["rel_vols"].append(f.rel_volume)
                    self.pullback["max_rel_vol"] = max(
                        self.pullback["max_rel_vol"], f.rel_volume)
                self.pullback["lows"].append(b.low)
                self.pullback["highs"].append(b.high)
                self.pullback["last_idx"] = self.idx

    def _update_registry(self, bar, feats, qualified_label):
        c = self.cfg.context
        if qualified_label in _REGISTRY_SPECS:
            attr, direction = _REGISTRY_SPECS[qualified_label]
            self.signature_registry.append({
                "label": qualified_label, "idx": self.idx,
                "extreme": getattr(bar, attr),
                "rel_volume": feats.rel_volume, "dir": direction,
            })
        self.signature_registry = [
            s for s in self.signature_registry
            if self.idx - s["idx"] <= c.signature_registry_max_age]

    _last_feats = None

    # -------------------------------------------------------------- properties

    @property
    def close(self):
        return self._bars[-1].close if self._bars else None

    @property
    def phase_age(self):
        return self.idx - getattr(self, "_phase_change_idx", 0)

    def trend_mean(self, period):
        """SMA of closes over `period` (H5 gate). None during warmup."""
        if len(self._bars) < period:
            return None
        closes = [b.close for b in list(self._bars)[-period:]]
        return sum(closes) / period

    def _near_level(self, side):
        """side=+1: nearest level at/below close (support);
        side=-1: at/above (resistance)."""
        if self.atr is None or not self._bars or not self.levels:
            return None
        close = self.close
        tol = self.cfg.context.level_atr_mult * self.atr
        cands = [lv for lv in self.levels
                 if (lv <= close if side > 0 else lv >= close)
                 and abs(close - lv) <= tol]
        return min(cands, key=lambda lv: abs(close - lv)) if cands else None

    @property
    def near_support(self):
        return self._near_level(+1) is not None

    @property
    def nearest_support_level(self):
        return self._near_level(+1)

    @property
    def near_resistance(self):
        return self._near_level(-1) is not None

    @property
    def nearest_resistance_level(self):
        return self._near_level(-1)

    def nearest_level(self, price):
        """(level, distance) of nearest key level to price, else (None, None)."""
        if not self.levels:
            return None, None
        lv = min(self.levels, key=lambda x: abs(price - x))
        return lv, abs(price - lv)

    @property
    def at_range_high(self):
        return (self.phase == "RANGING" and self.range_hi is not None
                and self.atr is not None
                and abs(self.close - self.range_hi)
                <= self.cfg.context.level_atr_mult * self.atr)

    @property
    def at_range_low(self):
        return (self.phase == "RANGING" and self.range_lo is not None
                and self.atr is not None
                and abs(self.close - self.range_lo)
                <= self.cfg.context.level_atr_mult * self.atr)

    def _move(self, direction):
        c = self.cfg.context
        lb = c.get("move_lookback", 20)
        if self.atr is None or len(self._bars) < lb:
            return False
        bars = list(self._bars)[-lb:]
        if direction > 0:      # rally: rise from the window's low
            return (self.close - min(b.low for b in bars)) >= c.move_atr_mult * self.atr
        return (max(b.high for b in bars) - self.close) >= c.move_atr_mult * self.atr

    @property
    def after_rally(self):
        return self._move(+1)

    @property
    def after_decline(self):
        return self._move(-1)

    @property
    def post_climax_dir(self):
        return self.post_climax["dir"] if self.post_climax else None

    def is_new_low(self, bar):
        lb = self.cfg.context.new_low_lookback
        bars = list(self._bars)[-lb:]          # inclusive of current bar
        return bool(bars) and bar.low <= min(b.low for b in bars)

    def is_new_high(self, bar):
        lb = self.cfg.context.new_low_lookback
        bars = list(self._bars)[-lb:]
        return bool(bars) and bar.high >= max(b.high for b in bars)

    def last_swing_low_before(self, idx):
        lows = [s for s in self.swings if s["type"] == "L" and s["idx"] < idx]
        return lows[-1]["price"] if lows else None

    def last_swing_high_before(self, idx):
        highs = [s for s in self.swings if s["type"] == "H" and s["idx"] < idx]
        return highs[-1]["price"] if highs else None
