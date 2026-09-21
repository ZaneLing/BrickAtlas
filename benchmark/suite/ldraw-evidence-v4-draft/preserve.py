#!/usr/bin/env python3
"""Read-only verification of v3 and an incremental recovery archive for this draft."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import subprocess
import tarfile

ROOT = Path(__file__).resolve().parents[3]
DATA = ROOT / "benchmark/ldraw-evidence-v4-draft"
BASE = ROOT / "benchmark/ldraw-evidence-v3"


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load(path):
    return json.loads(path.read_text())


def verify():
    lock = load(DATA / "baseline-lock.json")
    for row in lock["files"]:
        path = ROOT / row["path"]
        if "target" in row:
            assert path.is_symlink() and os.readlink(path) == row["target"], row["path"]
        else:
            assert path.stat().st_size == row["bytes"] and sha(path) == row["sha256"], row["path"]
    for row in lock["archives"]:
        assert sha(ROOT / row["path"]) == row["sha256"], row["path"]
    return {"status": "passed", "files": len(lock["files"]), "archives": len(lock["archives"]),
            "baseline_modified": False}


def create():
    assert not (DATA / "baseline-lock.json").exists(), "Never replace an existing recovery lock"
    DATA.mkdir(parents=True, exist_ok=True)
    entry = {
        "branch": subprocess.check_output(["git", "branch", "--show-current"], cwd=ROOT, text=True).strip(),
        "head": subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip(),
        "worktree_status": subprocess.check_output(["git", "status", "--short"], cwd=ROOT, text=True),
        "tracked_diff_stat": subprocess.check_output(["git", "diff", "--stat"], cwd=ROOT, text=True),
        "policy": "Pre-existing dirty/untracked work preserved; no reset, cleanup, commit or source overwrite.",
    }
    prior = load(BASE / "preservation-lock.json")
    delivered = load(BASE / "delivery-manifest.json")
    rows = {r["path"]: r for r in prior["files"] + delivered["files"]}
    extra = ["benchmark/ldraw-evidence-v3/delivery-manifest.json",
             "benchmark/ldraw-evidence-v3/delivery-verification.json",
             "CODEX_EVIDENCE_V3_FIVE_ISSUES_UPGRADE_PLAN.md", "CVPR_EVIDENCE_V3_REVIEW.md"]
    for relative in extra:
        path = ROOT / relative
        rows[relative] = {"path": relative, "sha256": sha(path), "bytes": path.stat().st_size}
    for row in rows.values():
        path = ROOT / row["path"]
        if "target" in row:
            assert os.readlink(path) == row["target"]
        else:
            assert sha(path) == row["sha256"], ("Baseline changed before work", row["path"])
    inherited_archives = {r["path"] for r in prior["archives"]}
    archive_paths = sorted(({r["path"] for r in delivered["files"]} | set(extra)) - inherited_archives)
    archive = DATA / "evidence-v3-baseline.tar.gz"
    with tarfile.open(archive, "w:gz", compresslevel=1) as output:
        for relative in archive_paths:
            output.add(ROOT / relative, arcname=relative, recursive=False)
    with tarfile.open(archive) as output:
        for relative in archive_paths:
            assert hashlib.sha256(output.extractfile(relative).read()).hexdigest() == rows[relative]["sha256"]
    lock = {
        "draft": "ldraw2-evidence-v4-draft", "baseline": "ldraw2-evidence-v3",
        "files": sorted(rows.values(), key=lambda r:r["path"]),
        "archives": prior["archives"] + [{"path": str(archive.relative_to(ROOT)), "sha256": sha(archive)}],
        "new_archive_files": len(archive_paths), "entry": entry,
        "baseline_pdfs": {n: sha(ROOT / f"benchmark/paper/evidence-v3/{n}.pdf")
                          for n in ["main", "supplement"]},
        "baseline_tests_log": "work/phase-0-baseline-tests.txt"
    }
    (DATA / "baseline-lock.json").write_text(json.dumps(lock, indent=2) + "\n")
    return verify()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--create", action="store_true")
    args = parser.parse_args()
    print(create() if args.create else verify())
