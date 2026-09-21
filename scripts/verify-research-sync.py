#!/usr/bin/env python3
"""Verify that the Git index preserves the research archive's exact bytes."""
import hashlib
import json
import os
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[1]


def load(path):
    return json.loads((ROOT / path).read_text())


def git_blob(data):
    return hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()


def verify():
    index = {}
    for record in subprocess.check_output(
            ["git", "ls-files", "-s", "-z"], cwd=ROOT).decode().split("\0"):
        if record:
            metadata, path = record.split("\t", 1)
            mode, oid, stage = metadata.split()
            assert stage == "0", path
            index[path] = (mode, oid)
    def file(relative, expected):
        path = (ROOT / relative).resolve()
        actual = str(path.relative_to(ROOT))
        data = path.read_bytes()
        assert hashlib.sha256(data).hexdigest() == expected, relative
        assert actual in index and index[actual][1] == git_blob(data), actual
    def link(relative, target=None):
        path = ROOT / relative
        assert path.is_symlink(), relative
        actual = os.readlink(path)
        if target is not None:
            assert actual == target, relative
        assert index[relative] == ("120000", git_blob(actual.encode())), relative
    count = 0
    for row in load("benchmark/ldraw-evidence-v4-draft/baseline-lock.json")["files"]:
        if row["path"].endswith(".tar.gz"):
            continue
        if "target" in row:
            link(row["path"], row["target"])
        else:
            file(row["path"], row["sha256"])
        count += 1
    moves = load("tem/relocation-manifest.json")["moves"]
    for move in moves:
        if move["git_policy"] == "local-recovery-only":
            continue
        link(move["old"])
        for row in move["files"]:
            file(row["path"], row["sha256"])
    print(json.dumps({"status": "passed", "frozen_index_entries": count,
                      "relocations": len(moves),
                      "local_recovery_archives_excluded": True}, indent=2))


if __name__ == "__main__":
    verify()
