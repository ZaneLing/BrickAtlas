"""Observe the existing matrix and validate each completed job without rerunning it."""
import argparse
import fcntl
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parents[2]
EXPECTED = ["base-seed17"] + [f"{condition}-seed{seed}"
                           for condition in ("single", "multi", "leave-edit") for seed in (17, 29, 43)]


def matrix_running(root):
    with (root / "matrix.lock").open("a") as lock:
        try:
            fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError:
            return True
        return False


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--pid", type=int, help="Optional matrix PID, additionally checked for compatibility")
    parser.add_argument("--once", action="store_true", help="Validate current evidence and exit without waiting")
    args = parser.parse_args()
    root = ROOT / ".runtime/vlm-training"
    root.mkdir(parents=True, exist_ok=True)
    local_node = ROOT.parent / ".tools/node-v22.23.2-darwin-arm64/bin/node"
    node = os.environ.get("NODE_BINARY") or (str(local_node) if local_node.exists() else shutil.which("node"))
    if not node:
        raise RuntimeError("Node 22 is required (PATH or NODE_BINARY)")
    tsx = ROOT.parent / "node_modules/tsx/dist/cli.mjs"
    cli = ROOT / "suite/study/cli.ts"

    def run(*command):
        subprocess.run([str(arg) for arg in command], cwd=ROOT.parent, check=True)

    def status(value):
        tmp = root / "validation-status.tmp"
        tmp.write_text(json.dumps(value, indent=2) + "\n")
        tmp.replace(root / "validation-status.json")
        print(json.dumps(value), flush=True)

    with (root / "validation.lock").open("a") as lock:
        fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        seen = None
        try:
            while True:
                ready = {name for name in EXPECTED if (root / name / "result.json").exists()}
                if ready != seen:
                    run(node, tsx, cli, "import-local")
                    run(sys.executable, Path(__file__).with_name("merge-audit.py"))
                    run(node, tsx, cli, "replay-local")
                    run(node, tsx, cli, "report")
                    run(node, ROOT / "paper/generate-study.mjs")
                    complete = len(ready) == len(EXPECTED)
                    if complete:
                        run(node, tsx, Path(__file__).with_name("clean-test.ts"))
                    run(node, tsx, Path(__file__).with_name("release-check.ts"),
                        *(["--require-complete"] if complete else []))
                    seen = ready
                    status({"status": "complete" if complete else ("validated" if args.once else "watching"), "checkedAt": time.time(),
                            "completedJobs": len(ready), "expected": len(EXPECTED), "validated": sorted(ready)})
                if len(ready) == len(EXPECTED) or args.once:
                    return
                if not matrix_running(root):
                    # The last result may have been written after this iteration's snapshot.
                    latest = {name for name in EXPECTED if (root / name / "result.json").exists()}
                    if latest != ready:
                        continue
                    raise RuntimeError(f"Matrix stopped with {len(ready)}/{len(EXPECTED)} jobs complete")
                if args.pid:
                    os.kill(args.pid, 0)
                time.sleep(30)
        except Exception as error:
            status({"status": "failed", "checkedAt": time.time(), "error": str(error),
                    "validated": sorted(seen or [])})
            raise


if __name__ == "__main__":
    main()
