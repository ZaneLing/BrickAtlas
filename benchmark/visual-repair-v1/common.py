"""Shared serialization only; constructor and evaluator use separate graph code."""
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
ASSETS = ROOT / "public/benchmark/visual-repair-v1"
VERSION = "visual-repair-v1"
SEED = "BA-visual-repair-20260922-v1"
CONDITIONS = ("multimodal", "no_image", "oracle_binding", "atomic_binding")


def read(path):
    return json.loads(Path(path).read_text())


def write(path, data):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=True, allow_nan=False) + "\n")


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"), allow_nan=False).encode()


def digest(value):
    return hashlib.sha256(canonical(value)).hexdigest()


def filehash(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def reference(path):
    return {"path": str(Path(path).relative_to(ROOT)), "sha256": filehash(path)}
