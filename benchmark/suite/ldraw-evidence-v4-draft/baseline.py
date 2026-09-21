"""Read-only boundary to the sealed v3 inputs; all new outputs use WORK/PAPER."""
import hashlib
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[3]
WORK = ROOT / "benchmark/ldraw-evidence-v4-draft"
PAPER = ROOT / "benchmark/paper/evidence-v4-draft"
BASE = ROOT / "benchmark/ldraw-evidence-v3"
BASE_SUITE = ROOT / "benchmark/suite/ldraw-evidence-v3"
BASE_PUBLIC = ROOT / "public/benchmark/evidence-v3"
VERSION = "ldraw2-evidence-v4-draft"
# Import the preserved computation helpers without redirecting their writes.
# Only read-only functions may be called from this path.
sys.path.append(str(BASE_SUITE))
from common import original_tasks


def load(path):
    return json.loads(Path(path).read_text())


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def checked(path):
    path = Path(path)
    relative = str(path.relative_to(ROOT))
    row = next(r for r in load(WORK / "baseline-lock.json")["files"] if r["path"] == relative)
    assert sha(path) == row["sha256"], relative
    return load(path)


def save(path, value):
    path = Path(path).resolve()
    assert path.is_relative_to(WORK) or path.is_relative_to(PAPER), "New artifacts cannot overwrite sealed inputs"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, ensure_ascii=True, allow_nan=False) + "\n")
