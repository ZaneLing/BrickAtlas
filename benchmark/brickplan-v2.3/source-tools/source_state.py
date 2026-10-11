"""Resolve frozen intake state without changing registered paths or bytes."""
from pathlib import Path

LEGACY_STATE_PATH = Path("tem/research/20261010-brickplan-v23-diversity/source-intake")
ARCHIVED_STATE_PATH = Path("benchmark/brickplan-v2.3/data/source-intake")


def source_state(root):
    legacy = root / LEGACY_STATE_PATH
    return legacy if legacy.exists() else root / ARCHIVED_STATE_PATH
