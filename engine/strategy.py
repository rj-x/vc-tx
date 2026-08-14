"""Strategy-definition schema (2026-08-14). Declarative YAML; one engine,
multiple feeds — a definition executes through the IDENTICAL code path in
lab, paper, and narrate. Candidate references by prose per guard convention.

mode: engine       -> the full hypothesis/gating pipeline (config overrides
                      + exit scheme + risk); frozen_v1 is this mode.
mode: signal_rules -> compositional entries: rules = list of {direction,
                      all: [conditions]} (OR across rules, AND within);
                      conditions over labels (any TF incl. ladder rungs),
                      location (ref class + Signal-ATR distance), segment,
                      phase (context/signal TF), migration chains
                      (min_rungs, recruited). Exits by named scheme.
"""

import hashlib

import yaml


def load_definition(path):
    d = yaml.safe_load(open(path))
    d.setdefault("mode", "engine")
    d["_hash"] = hashlib.sha256(open(path, "rb").read()).hexdigest()[:16]
    if d["mode"] not in ("engine", "signal_rules"):
        raise ValueError(f"unknown mode {d['mode']}")
    for r in d.get("rules") or []:
        for c in r.get("all", []):
            if c.get("type") == "migration":
                raise NotImplementedError(
                    "migration conditions are a v1.1 STUB (snapshot wiring "
                    "pending) - definitions using them are refused until "
                    "wired; see register item 14")
    return d


def apply_definition(cfg, d):
    for k, v in (d.get("config_overrides") or {}).items():
        cfg = cfg.override(k, v)
    if d.get("exit_scheme"):
        cfg = cfg.override("trade.exit_scheme", d["exit_scheme"])
    if d.get("risk", {}).get("risk_frac"):
        cfg = cfg.override("trade.risk_frac", d["risk"]["risk_frac"])
    if d["mode"] == "signal_rules":
        cfg = cfg.override("session_model.ladder", True)   # rules may use rungs
    return cfg


def rule_matches(rule, snap):
    """snap: per-signal-close snapshot {labels: {(tf,name)}, segment,
    location: {ref_class, dist_atr}, phases: {context, signal},
    migration: {max_rungs, any_recruited}}."""
    for c in rule.get("all", []):
        t = c["type"]
        if t == "label":
            if (c["tf"], c["name"]) not in snap["labels"]:
                return False
        elif t == "segment":
            if snap["segment"] not in c["in"]:
                return False
        elif t == "location":
            loc = snap.get("location") or {}
            if c.get("ref_class_in") and loc.get("ref_class") not in c["ref_class_in"]:
                return False
            if c.get("max_abs_atr") is not None:
                da = loc.get("dist_atr")
                if da is None or abs(da) > c["max_abs_atr"]:
                    return False
        elif t == "phase":
            if snap["phases"].get(c.get("tf", "context")) not in c["in"]:
                return False
        elif t == "migration":
            m = snap.get("migration") or {}
            if m.get("max_rungs", 0) < c.get("min_rungs", 1):
                return False
            if c.get("recruited") and not m.get("any_recruited"):
                return False
        else:
            raise ValueError(f"unknown condition type {t}")
    return True
