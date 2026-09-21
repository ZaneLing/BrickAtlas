#!/usr/bin/env python3
"""Relocate historical research material without changing sealed file bytes."""
import argparse
import hashlib
import json
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "tem/relocation-manifest.json"


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def candidates():
    paths = {Path("benchmark/paper"): Path("tem/papers/legacy-tree")}
    patterns = [
        "CODEX*.md", "CVPR*.md", "debug-*.md",
        "benchmark/*UPGRADE*.md", "benchmark/PLAN*.md", "benchmark/REVIEW_REPORT*.md",
        "benchmark/suite/RESEARCH_*.md", "benchmark/suite/study/PAPER_AUDIT.md",
        "benchmark/ldraw-v2/PHASE*.md", "benchmark/ldraw-v2/UPGRADE_STATUS.md",
        "benchmark/ldraw-evidence-v*/ISSUE*.md", "benchmark/ldraw-evidence-v*/CHECKLIST.md",
        "benchmark/ldraw-evidence-v*/FINAL-REPORT.md",
        "benchmark/ldraw-evidence-v*/research-story.md",
        "benchmark/ldraw-evidence-v*/REVISION-CONTRACT.md",
        "benchmark/ldraw-evidence-v*/REVIEW-RESPONSE.md",
        "benchmark/ldraw-evidence-v*/CODEX_PHASE_TRACKER.md",
        "benchmark/ldraw-evidence-v*/PHASE_*.md",
        "benchmark/ldraw-evidence-v2/*-ACCEPTANCE.md",
        "benchmark/ldraw-evidence-v*/inspection",
        "benchmark/ldraw-v2/paper-inspection",
        "benchmark/ldraw-evidence-v4-draft/work",
        "public/benchmark/evidence-v*/paper",
        "public/benchmark/evidence-v*/REVISION-CONTRACT.md",
        "public/benchmark/evidence-v*/REVIEW-RESPONSE.md",
    ]
    for pattern in patterns:
        for path in ROOT.glob(pattern):
            rel = path.relative_to(ROOT)
            paths[rel] = Path("tem/revisions") / rel
    for path in (ROOT / "benchmark").glob("ldraw*/**/*.tar.gz"):
        rel = path.relative_to(ROOT)
        paths[rel] = Path("tem/recovery") / rel
    return sorted(paths.items(), key=lambda p: str(p[0]))


def archive():
    rows = json.loads(MANIFEST.read_text())["moves"] if MANIFEST.exists() else []
    existing = {row["old"]: row for row in rows}
    for source, target in candidates():
        old, new = ROOT / source, ROOT / target
        if str(source) in existing:
            assert existing[str(source)]["new"] == str(target)
            continue
        if old.is_symlink() or not old.exists() or new.exists():
            raise ValueError(f"Unexpected relocation state: {source}")
        files = sorted(p for p in old.rglob("*") if p.is_file()) if old.is_dir() else [old]
        entries = [{"path": str(p.relative_to(ROOT)), "sha256": sha(p),
                    "bytes": p.stat().st_size} for p in files]
        new.parent.mkdir(parents=True, exist_ok=True)
        old.rename(new)
        old.symlink_to(os.path.relpath(new, old.parent), target_is_directory=new.is_dir())
        rows.append({"old": str(source), "new": str(target),
                     "git_policy": "local-recovery-only" if "tem/recovery/" in str(target) else "versioned",
                     "files": entries})
    MANIFEST.write_text(json.dumps({
        "schema": 1, "purpose": "Physical archive with byte-preserving compatibility links",
        "moves": rows}, indent=2) + "\n")
    verify()


def verify():
    data = json.loads(MANIFEST.read_text())
    total = 0
    for row in data["moves"]:
        old, new = ROOT / row["old"], ROOT / row["new"]
        if row["git_policy"] == "local-recovery-only" and not new.exists():
            continue
        assert old.is_symlink(), row["old"]
        assert old.resolve() == new.resolve(), row["old"]
        for item in row["files"]:
            assert sha(ROOT / item["path"]) == item["sha256"], item["path"]
            total += 1
    print(f"Verified {len(data['moves'])} relocations, {total} unchanged historical files.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--verify", action="store_true")
    args = parser.parse_args()
    verify() if args.verify else archive()
