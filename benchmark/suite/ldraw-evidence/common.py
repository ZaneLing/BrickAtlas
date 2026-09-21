"""Immutable inputs and small shared contracts for evidence analysis."""
import hashlib
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
DATA = ROOT / "benchmark/ldraw-evidence-v1"
VERSION = "ldraw2-evidence-v1"
RELEASE = "brickatlas-ldraw-2"


def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, ensure_ascii=True,
                                     separators=(",", ":"), allow_nan=False).encode()).hexdigest()


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def load(path):
    return json.loads(Path(path).read_text())


def save(path, value):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, ensure_ascii=True, allow_nan=False) + "\n")


def read_frozen(relative):
    lock = load(DATA / "baseline-lock.json")
    row = next((r for r in lock["files"] if r["path"] == relative), None)
    if row is None or row["kind"] != "file" or sha(ROOT / relative) != row["sha256"]:
        raise ValueError(f"Input absent from baseline or changed: {relative}")
    return load(ROOT / relative)


def public_tasks():
    catalog = read_frozen("benchmark/ldraw-v2/catalog.json")
    result = {}
    for m in catalog:
        b = read_frozen(f"public/benchmark/ldraw-v2/inputs/{m['id']}.json")
        if b["version"] != RELEASE or b["role"] != "model-input":
            raise ValueError("Wrong public-input role/version")
        for t in b["tasks"]:
            if t["id"] in result:
                raise ValueError("Duplicate task")
            result[t["id"]] = {**t, "source_hash": b["sourceHash"]}
    return result


def internal_tasks():
    catalog = read_frozen("benchmark/ldraw-v2/catalog.json")
    tasks = {}
    for m in catalog:
        b = read_frozen(f"public/benchmark/ldraw-v2/models/{m['id']}.json")
        if b["version"] != RELEASE or b["role"] != "internal-scoring-review":
            raise ValueError("Wrong scoring role/version")
        tasks.update({t["id"]: t for t in b["tasks"]})
    return tasks


def dataset_lock():
    catalog = read_frozen("benchmark/ldraw-v2/catalog.json")
    return {"release": RELEASE, "sources": [
        {"id": m["id"], "source_hash": m["sourceHash"],
         "input_sha256": sha(ROOT / f"public/benchmark/ldraw-v2/inputs/{m['id']}.json"),
         "internal_sha256": sha(ROOT / f"public/benchmark/ldraw-v2/models/{m['id']}.json")}
        for m in catalog]}


def text_payload(body):
    users = [m for m in body["messages"] if m["role"] == "user"]
    if len(users) != 1 or not isinstance(users[0]["content"], list):
        raise ValueError("Expected exactly one user content list")
    texts = [c["text"] for c in users[0]["content"] if c["type"] == "text"]
    if len(texts) != 1:
        raise ValueError("Expected exactly one question payload")
    payload = json.loads(texts[0])
    if set(payload) - {"question", "format", "input", "options"}:
        raise ValueError("Unexpected request fields")
    return payload


def target_label(payload):
    match = re.search(r"\bB\d{4,}\b", payload["question"])
    if not match:
        raise ValueError("No target label")
    return match.group()
