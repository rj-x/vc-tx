"""SignalRouter — RULES.md Sec 2 Phase C + Sec 9 execution refinement.

Owns: position state, the single pending entry (refinement or scheduled
direct entry), cancellations, entry tagging. The broker's fill/exit
mechanics (Part 7) live elsewhere; here a completed entry emits an ENTRY
event and sets the position.
"""

from .hypotheses import SPECS, LONG


class SignalRouter:
    def __init__(self, cfg, narrative, embargo_fn=None, tick_size=1.0,
                 broker=None, narrative_only=False):
        self.cfg = cfg
        self.narrative = narrative
        self.embargo_fn = embargo_fn or (lambda ts: False)
        self.tick = tick_size
        self.broker = broker          # owns the position once entered
        self.narrative_only = narrative_only   # narrate mode: never act
        self.pending = None           # refinement/scheduled-entry dict
        self.entries = []             # completed entries (audit)

    @property
    def position(self):
        return self.broker.position if self.broker else None

    # ------------------------------------------------------- Phase C routing

    def route_signal(self, h, bar, ctx, manager):
        if getattr(h, "observational", False) or bar.segment != "cash":
            # Part B: hypotheses spawned or graduating outside cash hours
            # are permanently observational — no refinement, no entries,
            # structurally (spawning-for-trading stays cash-session-only)
            self._log("SIGNAL_EXTENDED_OBSERVATIONAL", bar, h=h.describe())
            return
        if self.narrative_only:
            # narrate mode (labels/phases/hypotheses only): the signal is
            # narrated, never acted — no refinement, no entries, no trades
            self._log("SIGNAL_NARRATIVE_ONLY", bar, h=h.describe())
            return
        if self.position is not None:
            self._log("SIGNAL_UNACTED_IN_POSITION", bar, h=h.describe())
            return
        if self.pending is not None:
            if h.dir != self.pending["dir"]:
                # v3.1 guard split: cancel opposed pending, then act
                self._cancel("REFINEMENT_CANCELLED_OPPOSED", bar)
            else:
                self._log("SIGNAL_UNACTED_PENDING", bar, h=h.describe())
                return
        stop_ref = self._signature_stop(h, manager)
        if self.cfg.execution.enabled:
            self.pending = {
                "kind": "refinement", "h": h, "dir": h.dir,
                "graduation_ts": bar.ts, "bars_seen": [],
                "triggered": False, "entry_tag": "ENTRY_REFINED",
                "signature_stop": stop_ref,
            }
            self._log("REFINEMENT_STARTED", bar, h=h.describe())
        else:
            self.pending = {
                "kind": "scheduled", "h": h, "dir": h.dir,
                "graduation_ts": bar.ts, "entry_tag": "ENTRY_DIRECT",
                "signature_stop": stop_ref,
            }
            self._log("ENTRY_SCHEDULED", bar, h=h.describe())

    def _signature_stop(self, h, manager):
        buf = self.cfg.hypotheses.stop_buffer_ticks * self.tick
        if h.spec == "H3":
            base = h.zone_lo if h.dir == LONG else h.zone_hi
        elif h.spec == "H4":
            base = manager.h4_stop(h)
        else:
            base = h.sig_extreme
        return base - buf if h.dir == LONG else base + buf

    # ------------------------------------------- Signal-TF close (refutation)

    def on_signal_close(self, bar, feats, cores, ctx, cfg, env):
        """Sec 9: parent refutation on any Signal-TF close cancels a pending
        refinement."""
        if self.pending is None or self.pending["kind"] != "refinement":
            return
        if self.pending["graduation_ts"] == bar.ts:
            return          # refutation applies to SUBSEQUENT closes; also
                            # avoids double-calling stateful refute predicates
                            # (H5's counter) on the graduation bar itself
        h = self.pending["h"]
        if SPECS[h.spec]["refute"](h, env):
            self._cancel("REFINEMENT_CANCELLED_REFUTED", bar)

    # ------------------------------------------------------------ exec bars

    def on_exec_bar(self, bar):
        """Called for each Execution-TF bar close, AFTER higher TFs at the
        same timestamp (Sec 1 descending order). Window bar 1 = first exec
        bar closing STRICTLY AFTER the graduation timestamp."""
        p = self.pending
        if p is None:
            return
        if p["kind"] == "scheduled":
            return                          # handled at next Signal-TF open
        if bar.ts <= p["graduation_ts"]:
            return                          # not in window

        ecfg = self.cfg.execution
        if p["triggered"]:
            # entry at THIS bar's open (the bar after the trigger bar)
            self._enter(p, price=bar.open, ts=bar.ts, bar=bar)
            return

        if self.embargo_fn(bar.ts):
            self._cancel("REFINEMENT_ABANDONED_EMBARGO", bar)
            return

        p["bars_seen"].append(bar)
        thr = ecfg.close_pos_trigger
        with_dir = (bar.direction > 0 if p["dir"] == LONG else bar.direction < 0)
        cp = bar.close_pos
        hit = with_dir and (cp > thr if p["dir"] == LONG else cp < 1 - thr)
        self._log("TRIGGER_CHECK", bar, h=p["h"].describe(),
                  window_bar=len(p["bars_seen"]), close_pos=round(cp, 3),
                  with_direction=with_dir, hit=hit)
        if hit:
            p["triggered"] = True
            self._log("REFINEMENT_TRIGGERED", bar, h=p["h"].describe())
            return
        if len(p["bars_seen"]) >= ecfg.window:
            if ecfg.fallback == "enter":
                p["triggered"] = True
                p["entry_tag"] = "ENTRY_FALLBACK"
                p["use_signature_stop"] = True
                self._log("REFINEMENT_FALLBACK", bar, h=p["h"].describe())
            else:
                self._cancel("REFINEMENT_ABANDONED_NO_TRIGGER", bar)

    # ------------------------------------------------ Signal-TF open (direct)

    def on_signal_open(self, bar):
        """Direct-entry path: scheduled entry executes at the next Signal-TF
        bar's open."""
        p = self.pending
        if p is None or p["kind"] != "scheduled":
            return
        self._enter(p, price=bar.open, ts=bar.ts, bar=bar)

    # ----------------------------------------------------------------- entry

    def _enter(self, p, price, ts, bar):
        if self.embargo_fn(ts):
            self._cancel("ENTRY_ABANDONED_EMBARGO", bar)
            return
        h = p["h"]
        sig_stop = p["signature_stop"]
        stop, basis, local = sig_stop, "signature", None
        ecfg = self.cfg.execution
        if (p["kind"] == "refinement" and not p.get("use_signature_stop")
                and ecfg.stop_choice == "tighter_of" and p["bars_seen"]):
            buf = self.cfg.hypotheses.stop_buffer_ticks * self.tick
            if p["dir"] == LONG:
                local = min(b.low for b in p["bars_seen"]) - buf
                if local > stop:                 # tighter = higher stop for longs
                    stop, basis = local, "exec_local"
            else:
                local = max(b.high for b in p["bars_seen"]) + buf
                if local < stop:
                    stop, basis = local, "exec_local"
        entry = {"entry_ts": ts, "dir": p["dir"], "price": price, "stop": stop,
                 "stop_basis": basis, "signature_stop": sig_stop,
                 "exec_local_stop": local,
                 "tag": p["entry_tag"], "gate_tag": h.tag, "h": h.describe()}
        self.pending = None
        if self.broker is not None and not self.broker.open_position(entry):
            return                    # SKIPPED_SIZE — logged by the broker
        self.entries.append(entry)
        self._log("ENTRY", bar, **entry)

    def _cancel(self, reason, bar):
        h = self.pending["h"]
        self.pending = None
        self._log(reason, bar, h=h.describe())

    def _log(self, typ, bar, **payload):
        self.narrative.log(typ, ts=bar.ts, **payload)
