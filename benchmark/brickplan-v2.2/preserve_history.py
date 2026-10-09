"""Snapshot the historical case's original task; never relabel old inference."""
import json
from bank import HERE, write_json
from mission import canonical_hash


def main():
    previous = json.loads((HERE.parent / "brickplan-v2.1/data/tasks.private.json").read_text())
    record = json.loads((HERE / "cases/local-vlm.authoritative.json").read_text())
    task = next(t for t in previous["episodes"] if t["id"] == record["taskId"])
    assert canonical_hash(task) == record["taskHash"]
    provenance = json.loads((HERE / "cases/provenance.json").read_text())
    assert provenance["bankHash"] == canonical_hash(previous)
    write_json(HERE / "cases/task.v2.1.json", task)
    write_json(HERE / "cases/historical-release.json", {
        "release": "2.1", "bankHash": canonical_hash(previous),
        "taskHash": canonical_hash(task), "taskId": task["id"],
        "interpretation": "Historical integration trace on BrickPlan 2.1. Not a new 2.2 model measurement.",
        "responseAndImageBytesUnchanged": True})


if __name__ == "__main__":
    main()
