#!/usr/bin/env python3
"""Verify canonical locations, preserved research bytes and recorded path edits."""
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
EDITS = {
    "web/vite.config.ts": "Vite root, build/cache paths and test discovery",
    "web/vite.ldraw-v2.config.ts": "Vite root and build/cache paths",
    "web/playwright.config.ts": "Test discovery and report destinations",
    "web/tsconfig.json": "Compiler inputs and cache destination",
    "web/netlify.toml": "Production output destination",
    "web/vercel.json": "Production output destination",
    "web/docs/DEPLOYMENT.md": "Deployment paths",
    "web/src/workers/depth.worker.ts": "One extra parent for the installed WASM dependency",
}


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    data = json.loads((HERE / "moves.json").read_text())
    dirty = data["preexisting_uncommitted"]
    original_report = subprocess.check_output(
        ["git", "show", f"{data['base_commit']}:{dirty['old']}"], cwd=ROOT)
    report_hashes = {dirty["sha256"], hashlib.sha256(original_report).hexdigest()}
    rebased = {r["path"]: r["new"] for r in data["rebased_links"]}
    unchanged, adjusted, runtime = 0, [], 0
    for move in data["moves"]:
        destination = ROOT / move["new"]
        if move["new"].startswith(("tem/build/", "tem/local/",
                                    "tem/verification/playwright-")):
            runtime += len(move["files"])
            continue
        assert destination.exists(), destination
        if move["compatibility"]:
            assert (ROOT / move["old"]).is_symlink()
            assert (ROOT / move["old"]).resolve() == destination.resolve()
        for item in move["files"]:
            path = destination / item["path"] if item["path"] else destination
            name = str(path.relative_to(ROOT))
            if item.get("tracked") is False and not path.exists():
                continue  # Local media/cache files need not exist in a clone.
            if "link" in item:
                assert path.is_symlink() and path.exists(), path
                assert os.readlink(path) == rebased.get(name, item["link"]), path
            elif name == dirty["new"]:
                assert sha(path) in report_hashes, path
                unchanged += 1
            elif name in EDITS:
                adjusted.append({"path": name, "reason": EDITS[name],
                                 "before_sha256": item["sha256"], "after_sha256": sha(path)})
            else:
                assert sha(path) == item["sha256"], path
                unchanged += 1
    for name, target in data["mounts"].items():
        assert os.readlink(ROOT / name) == target and (ROOT / name).exists(), name
    for item in data["removed_aliases"]:
        assert not (ROOT / item["old"]).exists()
        assert (ROOT / item["new"]).is_file()
    working_change_preserved = sha(ROOT / dirty["new"]) == dirty["sha256"]

    base = data["base_commit"]
    protected = [
        "paper/main.tex", "paper/main.pdf", "paper/supplement.tex", "paper/supplement.pdf",
        "paper/experiments.json", "paper/repair-figure-provenance.json",
        "paper/build_repair_assets.py",
    ]
    protected += [str(p.relative_to(ROOT)) for p in (ROOT / "paper/figures").glob("*")]
    protected += [str(p.relative_to(ROOT)) for p in (ROOT / "paper/generated").glob("*")]
    for name in protected:
        original = subprocess.check_output(["git", "show", f"{base}:{name}"], cwd=ROOT)
        assert hashlib.sha256(original).hexdigest() == sha(ROOT / name), name
    # All versioned scientific packages and all original review records stay exact.
    changes = subprocess.check_output(["git", "diff", "--name-only", base, "--",
                                      "benchmark", "tem/agent-iterations/round-*",
                                      "tem/papers", "tem/revisions"], cwd=ROOT, text=True)
    assert not changes.strip(), changes
    missing = []
    for relative in ["README.md", "README.zh-CN.md", "paper/README.md",
                     "web/README.md", "tem/README.md", "tem/agent-iterations/README.md",
                     "tem/paper/previous-assets/README.md"]:
        path = ROOT / relative
        for target in re.findall(r"\]\(([^)]+)\)", path.read_text()):
            if re.match(r"(https?://|#)", target):
                continue
            if not (path.parent / target.split("#")[0]).exists():
                missing.append(f"{relative}: {target}")
    assert not missing, missing
    result = {"status": "passed", "base_commit": base, "moves": len(data["moves"]),
              "unchanged_relocated_files": unchanged, "path_adjustments": adjusted,
              "regenerable_local_files_recorded": runtime,
              "protected_publication_files": len(protected),
              "frozen_benchmark_and_review_bytes_unchanged": True,
              "preexisting_working_change_preserved": working_change_preserved,
              "report_policy": "Local working bytes or original Git bytes in a fresh clone; both recorded.",
              "documentation_links": "passed"}
    (HERE / "layout-verification.json").write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({k: v for k, v in result.items() if k != "path_adjustments"}, indent=2))


if __name__ == "__main__":
    main()
