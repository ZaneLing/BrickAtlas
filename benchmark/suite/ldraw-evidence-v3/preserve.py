#!/usr/bin/env python3
"""Incrementally archive evidence-v2 and retain all ancestor content locks."""
import argparse
import hashlib
import os
import tarfile

from common import ROOT, DATA, PRIOR_DATA, VERSION, load, save, sha


def verify():
    lock = load(DATA / "preservation-lock.json")
    for r in lock["files"]:
        p = ROOT / r["path"]
        if "target" in r:
            assert p.is_symlink() and os.readlink(p) == r["target"], r["path"]
        else:
            assert p.stat().st_size == r["bytes"] and sha(p) == r["sha256"], r["path"]
    for r in lock["archives"]:
        assert sha(ROOT / r["path"]) == r["sha256"], r["path"]
    return {"status": "passed", "frozen_files": len(lock["files"]),
            "content_archives": len(lock["archives"]), "prior_release_modified": False}


def create():
    assert not (DATA / "preservation-lock.json").exists()
    old = load(PRIOR_DATA / "preservation-lock.json")
    assets = load(PRIOR_DATA / "render-assets-lock.json")
    delivered = load(PRIOR_DATA / "delivery-manifest.json")
    rows = {r["path"]: r for r in old["files"] + assets["files"] + delivered["files"]}
    new_paths = {r["path"] for r in delivered["files"]}
    for relative in ["CVPR_EVIDENCE_V2_REVIEW.md",
                     "benchmark/ldraw-evidence-v2/delivery-manifest.json",
                     "benchmark/ldraw-evidence-v2/delivery-verification.json"]:
        p = ROOT / relative
        rows[relative] = {"path": relative, "sha256": sha(p), "bytes": p.stat().st_size}
        new_paths.add(relative)
    for r in rows.values():
        p = ROOT / r["path"]
        if "target" in r:
            assert os.readlink(p) == r["target"]
        else:
            assert sha(p) == r["sha256"], ("Prior release changed", r["path"])
    DATA.mkdir(parents=True, exist_ok=True)
    archive = DATA / "evidence-v2-preserved.tar.gz"
    with tarfile.open(archive, "w:gz", compresslevel=1) as package:
        for relative in sorted(new_paths):
            package.add(ROOT / relative, arcname=relative, recursive=False)
    with tarfile.open(archive) as package:
        for relative in sorted(new_paths):
            assert hashlib.sha256(package.extractfile(relative).read()).hexdigest() == rows[relative]["sha256"]
    save(DATA / "preservation-lock.json", {
        "analysis_version": VERSION, "files": sorted(rows.values(), key=lambda r:r["path"]),
        "archives": [{"path": str(archive.relative_to(ROOT)), "sha256": sha(archive)}] + [
            {"path": str((PRIOR_DATA / lock["archive"]).relative_to(ROOT)), "sha256": lock["archive_sha256"]}
            for lock in [old, assets]],
        "newly_archived_files": len(new_paths), "review_sha256": sha(ROOT / "CVPR_EVIDENCE_V2_REVIEW.md"),
        "policy": "Incremental exact-byte archive plus preserved ancestor archives; never overwrite an earlier release."
    }, immutable=True)
    return verify()


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--create", action="store_true")
    args = p.parse_args()
    print(create() if args.create else verify())
