"""Version boundaries and immutable artifact helpers for display-grounded evidence."""
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
DATA = ROOT / "benchmark/ldraw-evidence-v2"
PUBLIC = ROOT / "public/benchmark/evidence-v2"
VERSION = "ldraw2-evidence-v2"
DATASET = "brickatlas-display-v2"


def load(path):
    return json.loads(Path(path).read_text())


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, ensure_ascii=True,
                                     separators=(",", ":"), allow_nan=False).encode()).hexdigest()


def save(path, value, immutable=False):
    path = Path(path)
    text = json.dumps(value, indent=2, ensure_ascii=True, allow_nan=False) + "\n"
    if immutable and path.exists() and path.read_text() != text:
        raise ValueError(f"Immutable artifact differs: {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text)


def frozen(relative):
    lock = load(DATA / "preservation-lock.json")
    row = next((r for r in lock["files"] if r["path"] == relative), None)
    if row is None and (DATA / "render-assets-lock.json").exists():
        row = next((r for r in load(DATA / "render-assets-lock.json")["files"]
                    if r["path"] == relative), None)
    if row is None or row.get("sha256") != sha(ROOT / relative):
        raise ValueError(f"Frozen input missing or changed: {relative}")
    return load(ROOT / relative)


def original_tasks():
    result = {}
    for m in frozen("benchmark/ldraw-v2/catalog.json"):
        b = frozen(f"public/benchmark/ldraw-v2/models/{m['id']}.json")
        for t in b["tasks"]:
            if t["id"] in result:
                raise ValueError("Duplicate parent task")
            result[t["id"]] = {**t, "source_hash": m["sourceHash"]}
    return result


def text_payload(body):
    users = [m for m in body["messages"] if m["role"] == "user"]
    if len(users) != 1:
        raise ValueError("Exactly one independent user request required")
    texts = [c["text"] for c in users[0]["content"] if c["type"] == "text"]
    if len(texts) != 1:
        raise ValueError("Exactly one question payload required")
    return json.loads(texts[0])
