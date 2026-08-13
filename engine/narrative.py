"""Narrative log — structured JSONL so every decision is auditable, plus a
human-readable dump (Part 6). In-memory during a run; write() persists."""

import json


class Narrative:
    def __init__(self, tf=""):
        self.tf = tf
        self.events = []

    def log(self, typ, ts=None, **payload):
        self.events.append({"ts": ts, "tf": self.tf, "type": typ, **payload})

    def of_type(self, *types):
        return [e for e in self.events if e["type"] in types]

    def write_jsonl(self, path):
        with open(path, "w") as f:
            for e in self.events:
                f.write(json.dumps(e, default=str) + "\n")

    def human(self):
        lines = []
        for e in self.events:
            core = {k: v for k, v in e.items() if k not in ("ts", "tf", "type")}
            h = core.pop("h", None)
            hs = ""
            if h:
                tag = f" tag={h['tag']}" if h.get("tag") else ""
                hs = (f" [{h['spec']}#{h['id']} {'LONG' if h['dir'] == 1 else 'SHORT'}"
                      f" s={h['strength']:.1f} {h['state']}{tag}]")
            extra = f" {core}" if core else ""
            lines.append(f"t={e['ts']:<6} {e['tf']:<6} {e['type']:<28}{hs}{extra}")
        return "\n".join(lines)
