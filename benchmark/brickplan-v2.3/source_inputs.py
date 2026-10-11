"""Resolve unchanged, predeclared intake inputs in research and clean checkouts."""
import hashlib
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]


def registry_path(plan):
    recorded = ROOT / plan["candidateRegistry"]
    archived = HERE / "data/source-intake/candidate-registry.frozen.json"
    path = recorded if recorded.exists() else archived
    assert hashlib.sha256(path.read_bytes()).hexdigest() == plan["candidateRegistrySha256"]
    if archived.exists():
        assert archived.read_bytes() == path.read_bytes()
    return path


def intake_path(plan, model):
    archived = HERE / "data/source-intake/results" / f"{model}.json"
    recorded = registry_path(plan).parent / "results" / f"{model}.json"
    if archived.exists() and recorded.exists():
        assert archived.read_bytes() == recorded.read_bytes()
    return recorded if recorded.exists() else archived


def frozen_plan_path():
    archived = HERE / "data/source-intake/source-plan.frozen.json"
    recorded = ROOT / "tem/research/20261010-brickplan-v23-diversity/source-plan.frozen.json"
    if archived.exists() and recorded.exists():
        assert archived.read_bytes() == recorded.read_bytes()
    return recorded if recorded.exists() else archived
