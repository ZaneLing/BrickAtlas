#!/usr/bin/env python3
"""Content snapshot for the five-issue revision; never regenerates v1 or v2."""
import argparse
import datetime
import hashlib
import json
import os
from pathlib import Path
import subprocess
import tarfile

ROOT = Path(__file__).resolve().parents[3]
DATA = ROOT / "benchmark/ldraw-evidence-v1"
LOCK = DATA / "baseline-lock.json"
SCOPES = [
    "benchmark/ldraw-v2", "public/benchmark/ldraw-v2", "benchmark/suite/ldraw-v2",
    "src/benchmark-v2", "dist-ldraw-v2", "benchmark/paper/figures-v2",
    "benchmark/paper/tables-v2", "src/benchmark/engine.ts", "src/benchmark/types.ts",
    "src/benchmark/ldrawTypes.ts", "src/benchmark/NumberedOverlay.ts",
    "ldraw-v2.html", "ldraw-v2-render.html", "vite.ldraw-v2.config.ts",
    "package.json", "package-lock.json", "CVPR_V2_FIVE_ISSUES_GUIDE.md",
]
FINGERPRINTS = {
    "benchmark/paper/main-v2.pdf": "e324c6ea7fc3b2618519d27bc3b1bb1952ddde058403a4bc767e0fd19721fb7f",
    "benchmark/paper/main-v2.tex": "aee16704d5547d56ed4113cc3152fca89f677b6985e37790ab64007992a242ef",
    "benchmark/suite/ldraw-v2/conditions.ts": "e079afb58bff884420b13f324c840999875eba96c63a93ece82f290e3fca0fd0",
    "benchmark/suite/ldraw-v2/paired-analysis.py": "dfd59fcdde77c6e8d4a838326774b0fc89daef67b864c76917c680a47f358c9e",
}


def sha(path):
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def entries():
    paths = set()
    for name in SCOPES:
        p = ROOT / name
        if p.is_dir() and not p.is_symlink():
            paths.update(q for q in p.rglob("*") if q.is_file() or q.is_symlink())
        else:
            paths.add(p)
    paths.update(p for p in (ROOT / "benchmark/paper").iterdir()
                 if p.is_file() and ("-v2" in p.name or "ldraw-v2" in p.name))
    for p in sorted(paths):
        if p.is_symlink():
            yield {"path": str(p.relative_to(ROOT)), "kind": "symlink", "target": os.readlink(p)}
        else:
            yield {"path": str(p.relative_to(ROOT)), "kind": "file",
                   "sha256": sha(p), "bytes": p.stat().st_size}


def verify_v1():
    baseline = json.loads((ROOT / "benchmark/ldraw-v2/v1-frozen-manifest.json").read_text())
    for row in baseline["files"]:
        assert sha(ROOT / row["path"]) == row["sha256"], ("v1 changed", row["path"])
    return len(baseline["files"])


def verify():
    lock = json.loads(LOCK.read_text())
    for r in lock["files"]:
        p = ROOT / r["path"]
        if r["kind"] == "symlink":
            assert p.is_symlink() and os.readlink(p) == r["target"], r["path"]
        else:
            assert sha(p) == r["sha256"], ("v2 baseline changed", r["path"])
    assert sha(DATA / lock["archive"]) == lock["archive_sha256"]
    return {"status": "passed", "v2_files": len(lock["files"]), "v1_files": verify_v1(),
            "content_archive_verified": True}


def create():
    assert not LOCK.exists(), "Snapshot already exists; use --verify"
    for path, digest in FINGERPRINTS.items():
        assert sha(ROOT / path) == digest, ("guide fingerprint mismatch", path)
    v1 = verify_v1()
    # Report only process identity; do not print command lines or credentials.
    processes = subprocess.check_output(["ps", "-axo", "pid=,command="], text=True)
    active = []
    for line in processes.splitlines():
        if any(s in line for s in ["tsx run-model.ts", "ldraw-v2/run-model.ts", "ldraw-v2/release.ts"]):
            active.append(line.strip().split()[0])
    assert not active, ("active v2 writer PIDs", active)
    DATA.mkdir(parents=True, exist_ok=True)
    records = list(entries())
    archive = DATA / "v2-before-five-issues.tar.gz"
    with tarfile.open(archive, "w:gz", compresslevel=1) as tar:
        for r in records:
            tar.add(ROOT / r["path"], arcname=r["path"], recursive=False)
    with tarfile.open(archive, "r:gz") as tar:
        for r in records:
            if r["kind"] == "file":
                h = hashlib.sha256()
                with tar.extractfile(r["path"]) as f:
                    for chunk in iter(lambda: f.read(1024 * 1024), b""):
                        h.update(chunk)
                assert h.hexdigest() == r["sha256"], ("backup corrupted", r["path"])
    lock = {"analysis_version": "ldraw2-evidence-v1", "frozen_at": datetime.datetime.now(datetime.timezone.utc).isoformat(),
            "git_commit": subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip(),
            "v1_files": v1, "files": records, "guide_fingerprints": FINGERPRINTS,
            "archive": archive.name, "archive_sha256": sha(archive),
            "tracked_status": "Snapshot includes untracked files; branch alone is not protection"}
    LOCK.write_text(json.dumps(lock, indent=2) + "\n")
    return verify()


if __name__ == "__main__":
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--create", action="store_true")
    p.add_argument("--verify", action="store_true")
    args = p.parse_args()
    print(json.dumps(create() if args.create else verify(), indent=2))
