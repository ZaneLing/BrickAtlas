#!/usr/bin/env python3
"""Bind an internal review to exact research bytes, excluding runtime artifacts."""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]


def snapshot():
    names = subprocess.check_output(
        ["git", "ls-files", "-c", "-o", "--exclude-standard", "--",
         "paper", "benchmark", "src/benchmark-v2", "public/benchmark",
         "README.md", "README.zh-CN.md"], cwd=ROOT, text=True).splitlines()
    names += [str(p.relative_to(ROOT)) for p in (ROOT / "public/models").glob("*/manifest.json")]
    files = {}
    for name in sorted(set(names)):
        path = ROOT / name
        if not path.is_file() or path.is_symlink():
            continue
        if any(part in {"__pycache__", ".runtime", ".venv", "node_modules"} for part in path.parts):
            continue
        if name.startswith("benchmark/paper/") or "/tem/" in str(path.resolve()):
            continue
        if path.suffix in {".gz", ".zip", ".log", ".aux", ".out", ".bbl", ".blg", ".pyc", ".xdv"}:
            continue
        files[name] = hashlib.sha256(path.read_bytes()).hexdigest()
    digest = hashlib.sha256(json.dumps(files, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
    return {"base_commit": subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip(),
            "sha256": digest, "file_count": len(files), "files": files}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("round", type=int)
    parser.add_argument("--verify", action="store_true")
    args = parser.parse_args()
    path = HERE / f"round-{args.round:02d}" / "snapshot.json"
    current = snapshot()
    if args.verify:
        old = json.loads(path.read_text())
        assert current["sha256"] == old["sha256"], "Research files changed after review snapshot"
        print(f"Verified {current['file_count']} research files: {current['sha256']}")
    else:
        if path.exists():
            raise SystemExit("Snapshot already exists; create a new round rather than overwrite history.")
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(current, indent=2) + "\n")
        print(f"{path}: {current['file_count']} files, SHA256 {current['sha256']}")


if __name__ == "__main__":
    main()
