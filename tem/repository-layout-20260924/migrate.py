#!/usr/bin/env python3
"""One-shot, byte-preserving repository relocation; never regenerates evidence."""
import hashlib
import json
import os
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
MANIFEST = HERE / "moves.json"


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    assert not MANIFEST.exists(), "Migration already recorded."
    tracked = set(subprocess.check_output(
        ["git", "ls-files", "-z"], cwd=ROOT).decode().split("\0"))
    rows = []

    def move(source, target, compatibility=False):
        old, new = ROOT / source, ROOT / target
        if not old.exists():
            return
        assert not new.exists(), target
        files = []
        for path in sorted(old.rglob("*")) if old.is_dir() else [old]:
            if path.is_symlink():
                files.append({"path": str(path.relative_to(old)) if old.is_dir() else "",
                              "link": os.readlink(path)})
            elif path.is_file():
                files.append({"path": str(path.relative_to(old)) if old.is_dir() else "",
                              "sha256": sha(path), "bytes": path.stat().st_size,
                              "tracked": str(path.relative_to(ROOT)) in tracked})
        new.parent.mkdir(parents=True, exist_ok=True)
        old.rename(new)
        if compatibility:
            old.symlink_to(os.path.relpath(new, old.parent), target_is_directory=new.is_dir())
        rows.append({"old": source, "new": target, "compatibility": compatibility, "files": files})

    for name in ["src", "public", "tests", "docs"]:
        move(name, f"web/{name}", name in {"src", "public"})
    for path in sorted(ROOT.glob("*.html")):
        move(path.name, f"web/{path.name}")
    for name in ["vite.config.ts", "vite.ldraw-v2.config.ts", "playwright.config.ts",
                 "tsconfig.json", "netlify.toml", "vercel.json"]:
        move(name, f"web/{name}")
    move("assets-built", "tem/assets-built", True)
    for source, target in [
        ("dist", "tem/build/web"), ("dist-ldraw-v2", "tem/build/ldraw-v2"),
        ("test-results", "tem/verification/playwright-results"),
        ("playwright-report", "tem/verification/playwright-report"),
        (".preview", "tem/local/preview"), (".dbg", "tem/local/debug"),
        (".recording", "tem/local/recording"),
        ("tsconfig.tsbuildinfo", "tem/build/typescript/tsconfig.tsbuildinfo"),
        ("paper/__pycache__", "tem/build/paper/__pycache__"),
        ("paper/verification.json", "tem/verification/paper/verification.json"),
    ]:
        move(source, target)
    for path in sorted((ROOT / "paper").iterdir()):
        if path.suffix in {".aux", ".log", ".bbl", ".blg", ".brf", ".out"}:
            move(str(path.relative_to(ROOT)), f"tem/build/paper/{path.name}")
    for path in sorted((ROOT / "paper/figures").iterdir()):
        if path.stem not in {"repair-task", "repair-factorial", "source-atlas"}:
            move(str(path.relative_to(ROOT)), f"tem/paper/previous-assets/figures/{path.name}")
    for path in sorted((ROOT / "paper/generated").iterdir()):
        if not path.name.startswith("repair-"):
            move(str(path.relative_to(ROOT)), f"tem/paper/previous-assets/generated/{path.name}")
    for name in ["build_figures.py", "complex_figures.py", "visual-evidence.json",
                 "figure-provenance.json", "capture_complex.ts"]:
        move(f"paper/{name}", f"tem/paper/previous-assets/{name}")
    for name in ["complex-render.html", "complex-render.ts"]:
        move(f"paper/{name}", f"web/paper/{name}")

    removed = []
    for pattern in ["CODEX*.md", "CVPR*.md", "debug-*.md"]:
        for path in sorted(ROOT.glob(pattern)):
            assert path.is_symlink()
            removed.append({"old": path.name, "new": str(path.resolve().relative_to(ROOT)),
                            "link": os.readlink(path)})
            path.unlink()
    mounts = {
        "web/benchmark": "../benchmark", "web/scripts": "../scripts",
        "web/atlas.config.ts": "../atlas.config.ts",
        "web/assets-source": "../assets-source", "web/assets-built": "../tem/assets-built",
        "netlify.toml": "web/netlify.toml", "vercel.json": "web/vercel.json",
    }
    for name, target in mounts.items():
        (ROOT / name).symlink_to(target)
    rebased = []
    for path in sorted((ROOT / "web/public/benchmark").rglob("*")):
        if path.is_symlink() and not path.exists():
            old = os.readlink(path)
            new = "../" + old
            assert (path.parent / new).exists(), path
            path.unlink()
            path.symlink_to(new)
            rebased.append({"path": str(path.relative_to(ROOT)), "old": old, "new": new})
    MANIFEST.write_text(json.dumps({
        "schema": 1, "base_commit": subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip(),
        "moves": rows, "removed_aliases": removed, "mounts": mounts,
        "rebased_links": rebased,
        "preexisting_uncommitted": {
            "old": "assets-built/e2e-report.json", "new": "tem/assets-built/e2e-report.json",
            "sha256": "8692b48342732c2aa1371057d96ec4e9d8fd59bb99a9b3d09b5d04fb922965a7",
        },
    }, indent=2) + "\n")
    print(f"Moved {len(rows)} paths; recorded all original file bytes and links.")


if __name__ == "__main__":
    main()
