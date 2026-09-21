"""Freeze/verify v1 and rebuild it in a disposable namespace, never in place."""
import argparse
import datetime
import fcntl
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import tarfile
import tempfile

ROOT = Path(__file__).resolve().parents[3]
DATA = ROOT / "benchmark/ldraw-v2"
MANIFEST = DATA / "v1-frozen-manifest.json"


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n")


def protected():
    scopes = [
        ("benchmark/ldraw-v1", "source-and-v1-release"),
        ("benchmark/suite/ldraw", "v1-implementation"),
        ("public/benchmark/ldraw", "v1-published-artifact"),
        ("benchmark/paper", "v1-publication"),
    ]
    for directory, role in scopes:
        for p in sorted((ROOT / directory).rglob("*")):
            if not p.is_file() or p.suffix in {".log", ".aux", ".out", ".synctex"}:
                continue
            rel = p.relative_to(ROOT).as_posix()
            item_role = role
            if p.parent == ROOT / "public/benchmark/ldraw/inputs" and p.suffix == ".json":
                item_role = "model_input"
            if p.parent == ROOT / "public/benchmark/ldraw/models" and p.suffix == ".json":
                item_role = "internal_scoring"
            yield {"path": rel, "role": item_role, "sha256": sha(p), "bytes": p.stat().st_size}


def verify():
    frozen = json.loads(MANIFEST.read_text())
    failures = [r["path"] for r in frozen["files"]
                if not (ROOT / r["path"]).is_file() or sha(ROOT / r["path"]) != r["sha256"]]
    if failures:
        raise RuntimeError("STOP: protected v1 changed: " + ", ".join(failures))
    result = {"protectedFiles": len(frozen["files"]), "changed": failures,
              "modelInputs": sum(r["role"] == "model_input" for r in frozen["files"]),
              "internalBundles": sum(r["role"] == "internal_scoring" for r in frozen["files"])}
    assert result["modelInputs"] == result["internalBundles"] == 24
    return result


def freeze():
    if MANIFEST.exists():
        raise RuntimeError("Already frozen; use --verify. Never re-baseline changed assets.")
    dirty = subprocess.check_output(["git", "diff", "--name-only", "--",
                                     "benchmark/ldraw-v1", "benchmark/suite/ldraw",
                                     "public/benchmark/ldraw", "benchmark/paper"],
                                    cwd=ROOT, text=True).strip()
    if dirty:
        raise RuntimeError("STOP: tracked v1 modifications before freeze:\n" + dirty)
    runtime = ROOT / "benchmark/.runtime"
    locks = []
    for p in sorted(runtime.rglob("*")):
        if not p.is_file() or "site-packages" in p.parts or ".cache" in p.parts:
            continue
        if p.name != "lock" and p.suffix != ".lock":
            continue
        held = False
        with p.open("rb") as handle:
            try:
                fcntl.flock(handle, fcntl.LOCK_EX | fcntl.LOCK_NB)
                fcntl.flock(handle, fcntl.LOCK_UN)
            except BlockingIOError:
                held = True
        locks.append({"path": str(p.relative_to(ROOT)), "held": held})
    processes = subprocess.check_output(["ps", "-axo", "pid,ppid,etime,command"], text=True)
    relevant = [line.strip() for line in processes.splitlines()
                if str(ROOT) in line and any(x in line for x in
                   ("run-model", "suite/ldraw/", "train.py", "run_local.py"))]
    if any(r["held"] for r in locks) or relevant:
        raise RuntimeError("STOP: active experiment lock/process needs inspection")
    records = list(protected())
    stamp = datetime.datetime.now(datetime.timezone.utc).isoformat()
    write(MANIFEST, {"version": "brickatlas-ldraw-2", "frozenAt": stamp,
                    "gitCommit": subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip(),
                    "files": records})
    for name in ("questions.ts", "score.ts"):
        shutil.copy2(ROOT / "benchmark/suite/ldraw" / name,
                     ROOT / "benchmark/suite/ldraw-v2" / name)
    for name in ("models", "inputs"):
        (ROOT / "public/benchmark/ldraw-v2" / name).mkdir(parents=True, exist_ok=True)
    (DATA / "sources").symlink_to("../ldraw-v1/sources", target_is_directory=True)
    legacy = sorted(p for p in runtime.rglob("result.json")
                    if "site-packages" not in p.parts)
    backup = DATA / "backups/legacy-results.tar.gz"
    backup.parent.mkdir(parents=True, exist_ok=True)
    with tarfile.open(backup, "w:gz") as archive:
        for p in legacy:
            archive.add(p, arcname=str(p.relative_to(ROOT)))
            sibling = p.with_name("manifest.json")
            if sibling.exists():
                archive.add(sibling, arcname=str(sibling.relative_to(ROOT)))
    write(DATA / "phase-0-runtime.json", {
        "checkedAt": stamp, "locks": locks, "activeExperimentProcesses": relevant,
        "ldrawV1ResultsFound": False, "legacyResultFilesBackedUp": len(legacy),
        "backup": str(backup.relative_to(ROOT)), "backupSha256": sha(backup),
        "note": "Legacy training results are historical, not LDraw v1/v2 evidence. No process was stopped."})
    (DATA / "VERSION.md").write_text(
        "# BrickAtlas LDraw-2\n\n"
        f"Freeze: {stamp}\n\n"
        "v1 remains immutable. `v1-frozen-manifest.json` records every protected file, "
        "SHA256 and the distinct model_input / internal_scoring roles (24 each).\n\n"
        "Original sources are referenced through `sources -> ../ldraw-v1/sources`; "
        "they must never be written through this link. New questions, evidence, "
        "experiments and publication artifacts use the ldraw-v2 namespace.\n\n"
        "Phase 0 copied the v1 question generator and scorer byte for byte. "
        "The v1 build is exercised only in a disposable copy because its CLI "
        "unconditionally rewrites frozen outputs.\n")
    print(json.dumps(verify()))


def rebuild():
    verify()
    node_bin = ROOT / ".tools/node-v22.23.2-darwin-arm64/bin"
    env = {**os.environ, "PATH": str(node_bin) + os.pathsep + os.environ["PATH"]}
    with tempfile.TemporaryDirectory(prefix="brickatlas-v1-rebuild-") as temp:
        stage = Path(temp)
        (stage / "benchmark").mkdir()
        (stage / "public/benchmark").mkdir(parents=True)
        shutil.copytree(ROOT / "benchmark/ldraw-v1", stage / "benchmark/ldraw-v1")
        shutil.copytree(ROOT / "benchmark/suite/ldraw", stage / "benchmark/suite/ldraw")
        shutil.copy2(ROOT / "benchmark/package.json", stage / "benchmark/package.json")
        shutil.copy2(ROOT / "package.json", stage / "package.json")
        for name in ("node_modules", "src", "scripts", "assets-source"):
            (stage / name).symlink_to(ROOT / name, target_is_directory=True)
        # Legacy parser loads assets-source relative to cwd; npm --prefix uses benchmark/.
        (stage / "benchmark/assets-source").symlink_to(ROOT / "assets-source", target_is_directory=True)
        models = stage / "public/models"
        models.mkdir()
        for p in (ROOT / "public/models").iterdir():
            (models / p.name).symlink_to(p, target_is_directory=p.is_dir())
        restored = []
        for p in (ROOT / "benchmark/.runtime/retired-site").iterdir():
            if (p / "manifest.json").is_file() and not (models / p.name).exists():
                (models / p.name).symlink_to(p, target_is_directory=True)
                restored.append(p.name)
        outcome = subprocess.run(["npm", "run", "--prefix", "benchmark", "ldraw:build"],
                                 cwd=stage, env=env, capture_output=True, text=True)
        (DATA / "phase-0-v1-build.txt").write_text(outcome.stdout + outcome.stderr)
        if outcome.returncode:
            raise RuntimeError("Isolated v1 build failed; see phase-0-v1-build.txt")
        compared = []
        for p in sorted((stage / "public/benchmark/ldraw").rglob("*")):
            if p.is_file():
                rel = p.relative_to(stage)
                assert sha(p) == sha(ROOT / rel), str(rel)
                compared.append(str(rel))
        # Independent source reparse verification also writes only in the copy.
        outcome = subprocess.run(["npm", "run", "--prefix", "benchmark", "ldraw:verify"],
                                 cwd=stage, env=env, capture_output=True, text=True)
        (DATA / "phase-0-v1-verify.txt").write_text(outcome.stdout + outcome.stderr)
        if outcome.returncode:
            raise RuntimeError("Isolated v1 verification failed")
        shutil.copy2(stage / "benchmark/ldraw-v1/verification.json",
                     DATA / "source-reparse-verification.json")
    write(DATA / "phase-0-checks.json", {"status": "passed", **verify(),
          "isolatedV1Build": "passed", "rebuiltFilesEqual": compared,
          "retiredCandidateDependenciesRestoredInTemporaryCopy": restored,
          "inPlaceV1BuildKnownIssue": "Retired candidate manifests are missing from public/models; the original command is not safe/reproducible in place.",
          "independentSourceReparse": "passed"})
    print(json.dumps({"status": "passed", "rebuiltFilesEqual": len(compared), **verify()}))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--freeze", action="store_true")
    parser.add_argument("--verify", action="store_true")
    parser.add_argument("--rebuild", action="store_true")
    args = parser.parse_args()
    if args.freeze:
        freeze()
    elif args.rebuild:
        rebuild()
    else:
        print(json.dumps(verify()))
