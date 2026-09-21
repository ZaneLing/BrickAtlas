#!/usr/bin/env python3
"""Archive actual earlier release bytes, including untracked files, before revision."""
import argparse
import hashlib
import os
import tarfile
from common import DATA, ROOT, VERSION, load, save, sha


def verify():
    lock = load(DATA / "preservation-lock.json")
    for row in lock["files"]:
        p = ROOT / row["path"]
        if "target" in row:
            assert p.is_symlink() and os.readlink(p) == row["target"], row["path"]
        else:
            assert p.stat().st_size == row["bytes"] and sha(p) == row["sha256"], row["path"]
    assert sha(DATA / lock["archive"]) == lock["archive_sha256"]
    if (DATA / "render-assets-lock.json").exists():
        assets = load(DATA / "render-assets-lock.json")
        for row in assets["files"]:
            assert sha(ROOT / row["path"]) == row["sha256"], row["path"]
        assert sha(DATA / assets["archive"]) == assets["archive_sha256"]
    return {"status": "passed", "files": len(lock["files"]),
            "old_v2_files": lock["old_v2_files"], "old_v1_files": lock["old_v1_files"],
            "evidence_v1_sealed_files": lock["evidence_v1_sealed_files"],
            "content_archive_verified": True}


def create():
    assert not (DATA / "preservation-lock.json").exists(), "Use --verify for an existing freeze"
    old = load(ROOT / "benchmark/ldraw-evidence-v1/baseline-lock.json")
    v1 = load(ROOT / "benchmark/ldraw-v2/v1-frozen-manifest.json")
    delivered = load(ROOT / "benchmark/ldraw-evidence-v1/delivery-manifest.json")
    paths = set()
    for row in old["files"] + v1["files"] + delivered["files"]:
        p = ROOT / row["path"]
        if row.get("kind") == "symlink":
            assert os.readlink(p) == row["target"]
        else:
            assert sha(p) == row["sha256"], ("Earlier release already changed", row["path"])
        paths.add(p)
    for scope in ["benchmark/ldraw-evidence-v1", "benchmark/paper/evidence-v1",
                  "benchmark/suite/ldraw-evidence", "public/benchmark/evidence-v1",
                  "src/scene", "src/model"]:
        paths.update(p for p in (ROOT / scope).rglob("*") if p.is_file() or p.is_symlink())
    paths.update(ROOT / p for p in ["evidence-v1.html", "CVPR_EVIDENCE_V1_REVIEW.md"])
    rows = []
    for p in sorted(paths):
        row = {"path": str(p.relative_to(ROOT))}
        if p.is_symlink():
            row["target"] = os.readlink(p)
        else:
            row.update(sha256=sha(p), bytes=p.stat().st_size)
        rows.append(row)
    DATA.mkdir(parents=True, exist_ok=True)
    archive = DATA / "before-review-v2.tar.gz"
    with tarfile.open(archive, "w:gz", compresslevel=1) as tar:
        for row in rows:
            tar.add(ROOT / row["path"], arcname=row["path"], recursive=False)
    with tarfile.open(archive, "r:gz") as tar:
        for row in rows:
            if "sha256" in row:
                h = hashlib.sha256()
                with tar.extractfile(row["path"]) as stream:
                    for chunk in iter(lambda: stream.read(1024*1024), b""):
                        h.update(chunk)
                assert h.hexdigest() == row["sha256"], row["path"]
    save(DATA / "preservation-lock.json", {
        "analysis_version": VERSION, "files": rows,
        "old_v2_files": len(old["files"]), "old_v1_files": len(v1["files"]),
        "evidence_v1_sealed_files": len(delivered["files"]),
        "archive": archive.name, "archive_sha256": sha(archive),
        "review_sha256": sha(ROOT / "CVPR_EVIDENCE_V1_REVIEW.md"),
        "policy": "All earlier release bytes remain immutable; a branch is not the backup."},
        immutable=True)
    return verify()


def archive_render_assets():
    output = DATA / "render-assets-lock.json"
    assert not output.exists(), "Render assets already frozen"
    paths = []
    for m in load(ROOT / "benchmark/ldraw-v2/catalog.json"):
        paths.extend(p for p in (ROOT / "public/models" / m["id"]).rglob("*") if p.is_file())
    rows = [{"path": str(p.relative_to(ROOT)), "sha256": sha(p), "bytes": p.stat().st_size}
            for p in sorted(set(paths))]
    archive = DATA / "source-render-assets.tar.gz"
    with tarfile.open(archive, "w:gz", compresslevel=1) as tar:
        for row in rows:
            tar.add(ROOT / row["path"], arcname=row["path"], recursive=False)
    with tarfile.open(archive, "r:gz") as tar:
        for row in rows:
            assert hashlib.sha256(tar.extractfile(row["path"]).read()).hexdigest() == row["sha256"]
    save(output, {"analysis_version": VERSION, "files": rows, "archive": archive.name,
                  "archive_sha256": sha(archive), "role": "unaltered source render assets"}, immutable=True)
    return {"status": "passed", "render_assets": len(rows), "source_geometry_unchanged": True}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--create", action="store_true")
    parser.add_argument("--verify", action="store_true")
    parser.add_argument("--assets", action="store_true")
    args = parser.parse_args()
    print(archive_render_assets() if args.assets else create() if args.create else verify())
