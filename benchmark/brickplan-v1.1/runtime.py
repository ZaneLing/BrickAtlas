"""Bind the unchanged 1.0 executor to this explicitly versioned case bank.

Call activate before importing any executor module. Each process serves one
release. The frozen 1.0 files are read-only dependencies, never rewritten.
"""
from functools import lru_cache
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
BASE = HERE.with_name("brickplan-v1")
OUT = ROOT / "tem/brickplan-v1.1/validation"


def activate():
    if getattr(activate, "done", False):
        return
    if any(name in sys.modules for name in ("build", "cases", "server", "evaluate", "collect")):
        raise RuntimeError("Activate the release before importing executor modules")
    sys.path.insert(0, str(BASE))
    import cases
    from extension_cases import EXTRA_CASES
    cases.CASES = [*cases.CASES, *EXTRA_CASES]
    import build
    build.HERE = HERE
    build.DATA = HERE / "data"
    # Banks are immutable within a process; verify on first load, share thereafter.
    # Restart after rebuilding so persisted tasks and in-memory oracles agree.
    build.load_bank = lru_cache(maxsize=None)(build.load_bank)
    activate.done = True
