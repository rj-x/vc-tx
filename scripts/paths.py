"""Single source of truth for pipeline paths.

Everything resolves relative to the project root (the parent of scripts/),
so collect.py and store.py work from any working directory.
"""

import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(ROOT, "data")          # raw store (exactly as fetched)
CLEAN_DIR = os.path.join(ROOT, "clean_finsa")  # clean store (engine reads only this)
