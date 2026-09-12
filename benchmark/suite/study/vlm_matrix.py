"""Serial GPU jobs with persisted console logs and no unrecorded overwrite."""
import argparse
import fcntl
import json
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[2]
SCRIPT = Path(__file__).with_name("train_vlm.py")
parser = argparse.ArgumentParser()
parser.add_argument("--probe", action="store_true")
args = parser.parse_args()
root = ROOT / ".runtime/vlm-training"
root.mkdir(parents=True, exist_ok=True)
with (root / "matrix.lock").open("a") as lock:
    fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
    if args.probe:
        with (root / "probe.log").open("w") as log:
            result = subprocess.run([sys.executable, "-u", str(SCRIPT), "--condition=multi", "--probe"],
                                    stdout=log, stderr=subprocess.STDOUT)
        print((root / "probe.log").read_text(), flush=True)
        sys.exit(result.returncode)
    jobs = [("base", 17)] + [(condition, seed) for condition in ("single", "multi", "leave-edit") for seed in (17, 29, 43)]
    for condition, seed in jobs:
        output = root / f"{condition}-seed{seed}"
        output.mkdir(exist_ok=True)
        if (output / "result.json").exists():
            print(json.dumps({"condition": condition, "seed": seed, "status": "already-complete"}), flush=True)
            continue
        if (output / "manifest.json").exists():
            raise RuntimeError(f"Incomplete job {output.name}; preserve evidence and recover explicitly before restarting")
        with (output / "console.log").open("a") as log:
            result = subprocess.run([sys.executable, "-u", str(SCRIPT), f"--condition={condition}", f"--seed={seed}"],
                                    stdout=log, stderr=subprocess.STDOUT)
        print(json.dumps({"condition": condition, "seed": seed, "exit": result.returncode}), flush=True)
        if result.returncode:
            print((output / "console.log").read_text()[-12000:], flush=True)
            sys.exit(result.returncode)
