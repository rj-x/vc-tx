"""Config loading. All thresholds live in config.yaml (project root);
tests override individual keys via Cfg.override()."""

import copy
import os

import yaml

_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEFAULT_PATH = os.path.join(_ROOT, "config.yaml")


class Cfg:
    """Read-only attribute/dict hybrid over nested config."""

    def __init__(self, d):
        self._d = d

    def __getattr__(self, k):
        try:
            v = self._d[k]
        except KeyError:
            raise AttributeError(f"missing config key: {k}") from None
        return Cfg(v) if isinstance(v, dict) else v

    def __getitem__(self, k):
        v = self._d[k]
        return Cfg(v) if isinstance(v, dict) else v

    def get(self, k, default=None):
        v = self._d.get(k, default)
        return Cfg(v) if isinstance(v, dict) else v

    def override(self, path, value):
        """Return a new Cfg with dotted `path` set to `value`."""
        d = copy.deepcopy(self._d)
        node = d
        keys = path.split(".")
        for k in keys[:-1]:
            node = node.setdefault(k, {})
        node[keys[-1]] = value
        return Cfg(d)

    def raw(self):
        return copy.deepcopy(self._d)


def load(path=DEFAULT_PATH):
    with open(path) as f:
        return Cfg(yaml.safe_load(f))
