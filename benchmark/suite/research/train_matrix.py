"""Run local baselines serially; do not overlap GPU jobs or overwrite completed runs."""
import fcntl
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parents[2]
SCRIPT = Path(__file__).with_name("train_local.py")
JOBS = [("base", 17), ("single", 17), ("multi", 17), ("multi", 29), ("multi", 43)]


def main():
    directory = ROOT / ".runtime/local-training"
    directory.mkdir(parents=True, exist_ok=True)
    with (directory / "matrix.lock").open("w") as lock:
        fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        spec = {"jobs": JOBS, "steps": 120, "max_length": 3072, "max_new_tokens": 1200,
                "script_sha256": hashlib.sha256(SCRIPT.read_bytes()).hexdigest(),
                "note": "Text/structure LoRA pilots. Three multi seeds; step-matched single/multi, not token-matched."}
        spec_path = directory / "matrix-plan.json"
        if spec_path.exists() and json.loads(spec_path.read_text()) != json.loads(json.dumps(spec)):
            raise RuntimeError("Matrix differs from frozen plan")
        spec_path.write_text(json.dumps(spec, indent=2))
        for condition, seed in JOBS:
            output = directory / f"{condition}-seed{seed}"
            result_path = output / "result.json"
            if result_path.exists():
                result = json.loads(result_path.read_text())
                assert result["status"] == "complete"
                assert result["script_sha256"] == spec["script_sha256"]
                print(json.dumps({"job": condition, "seed": seed, "status": "already-complete"}), flush=True)
                continue
            output.mkdir(parents=True, exist_ok=True)
            if (output / "manifest.json").exists():
                raise RuntimeError("Incomplete prior run requires explicit recovery; will not overwrite")
            print(json.dumps({"job": condition, "seed": seed, "status": "starting", "at": time.time()}), flush=True)
            with (output / "console.log").open("w") as log:
                subprocess.run([sys.executable, "-u", str(SCRIPT), "--condition", condition, "--seed", str(seed),
                                "--steps", "120"], stdout=log, stderr=subprocess.STDOUT, check=True)
            print(json.dumps({"job": condition, "seed": seed, "status": "complete"}), flush=True)


if __name__ == "__main__":
    main()
