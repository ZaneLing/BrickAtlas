#!/usr/bin/env python3
"""Validate independent review records and the fixed acceptance gate."""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess

from snapshot import ROOT, snapshot as current_research_snapshot

HERE = Path(__file__).resolve().parent


def verify_committed_snapshot(expected):
    current = current_research_snapshot()
    assert current["sha256"] == expected["sha256"], "Accepted research bytes changed"
    assert current["files"] == expected["files"], "Accepted research file set changed"
    assert current["file_count"] == expected["file_count"] == len(expected["files"])
    tree = subprocess.check_output(["git", "ls-tree", "-rz", "HEAD"], cwd=ROOT)
    committed = {}
    for entry in tree.split(b"\0"):
        if not entry:
            continue
        metadata, name = entry.split(b"\t", 1)
        _, kind, oid = metadata.split()
        if kind == b"blob":
            committed[name.decode()] = oid.decode()
    object_format = subprocess.check_output(
        ["git", "rev-parse", "--show-object-format"], cwd=ROOT, text=True).strip()
    for name in expected["files"]:
        assert name in committed, f"Accepted research file is uncommitted: {name}"
        data = (ROOT / name).read_bytes()
        oid = hashlib.new(object_format, b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()
        assert oid == committed[name], f"Accepted research differs from HEAD: {name}"
    return {"status": "passed", "research_sha256": current["sha256"],
            "file_count": current["file_count"], "committed_research_verified": True,
            "verified_head": current["base_commit"]}


def verify_archived_snapshot(expected, commit):
    commit = subprocess.check_output(
        ["git", "rev-parse", "--verify", f"{commit}^{{commit}}"], cwd=ROOT, text=True).strip()
    assert commit == expected["base_commit"], "Use the exact reviewed commit"
    tree = subprocess.check_output(["git", "ls-tree", "-rz", commit], cwd=ROOT)
    objects = {}
    for entry in tree.split(b"\0"):
        if entry:
            metadata, name = entry.split(b"\t", 1)
            _, kind, oid = metadata.split()
            if kind == b"blob":
                objects[name.decode()] = oid.decode()
    names = sorted(expected["files"])
    assert all(name in objects for name in names)
    batch = subprocess.run(["git", "cat-file", "--batch"], cwd=ROOT,
                           input=("\n".join(objects[name] for name in names) + "\n").encode(),
                           stdout=subprocess.PIPE, check=True).stdout
    offset, files = 0, {}
    for name in names:
        end = batch.index(b"\n", offset)
        _, kind, size = batch[offset:end].split()
        assert kind == b"blob"
        offset = end + 1
        content = batch[offset:offset + int(size)]
        offset += int(size) + 1
        files[name] = hashlib.sha256(content).hexdigest()
    assert files == expected["files"], "Archived research bytes changed"
    digest = hashlib.sha256(json.dumps(files, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
    assert digest == expected["sha256"] and len(files) == expected["file_count"]
    return {"status": "passed", "scope": "archived-reviewed-commit-only",
            "verified_commit": commit, "research_sha256": digest,
            "file_count": len(files), "current_workspace_acceptance_claimed": False}


def audit(require_accept=False, archived_commit=None):
    rounds = []
    final_snapshot_check = None
    for directory in sorted(HERE.glob("round-*")):
        path = directory / "review.json"
        if not path.exists():
            continue
        review = json.loads(path.read_text())
        snapshot = json.loads((directory / "snapshot.json").read_text())
        assert review["round"] == int(directory.name.split("-")[-1])
        assert review["snapshot_sha256"] == snapshot["sha256"]
        assert 1 <= review["score"] <= 10 and 1 <= review["confidence"] <= 5
        assert isinstance(review["criteria"], (dict, list)) and review["criteria"]
        assert review["assumption"] and review["acceptance_rationale"]
        ids = []
        for issue in review["issues"]:
            for field in ["id", "severity", "status", "summary", "evidence", "why_it_matters", "closure_test"]:
                assert field in issue, (path, field)
            assert issue["severity"] in {"critical", "major", "minor"}
            assert issue["status"] in {"open", "closed"}
            ids.append(issue["id"])
        assert len(ids) == len(set(ids)), path
        blockers = [i["id"] for i in review["issues"] if i["status"] == "open" and i["severity"] in {"critical", "major"}]
        rounds.append({"round": review["round"], "verdict": review["verdict"], "score": review["score"],
                       "open_major_or_critical": blockers, "snapshot_sha256": snapshot["sha256"]})
    if require_accept:
        assert len(rounds) >= 2, "Need multiple independent review interactions"
        final = rounds[-1]
        assert final["score"] >= 7 and final["verdict"] in {"accept", "strong_accept"}
        assert not final["open_major_or_critical"]
        directory = HERE / f"round-{final['round']:02d}"
        validation = json.loads((directory / "validation.json").read_text())
        assert validation["status"] == "passed"
        assert validation["snapshot_sha256"] == final["snapshot_sha256"]
        assert all((directory / name).exists() for name in ["response.md", "changes.json", "report.md"])
        expected = json.loads((directory / "snapshot.json").read_text())
        final_snapshot_check = (verify_archived_snapshot(expected, archived_commit)
                                if archived_commit else verify_committed_snapshot(expected))
    return {"internal_simulation": True, "empirical_completion_is_review_assumption_only": True,
            "rounds": rounds, "acceptance_gate_passed": bool(require_accept),
            "final_snapshot_check": final_snapshot_check}


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--require-accept", action="store_true")
    parser.add_argument("--archived-commit", help="Verify the reviewed commit, not the modified workspace.")
    args = parser.parse_args()
    if args.archived_commit and not args.require_accept:
        parser.error("--archived-commit requires --require-accept")
    print(json.dumps(audit(args.require_accept, args.archived_commit), indent=2))
