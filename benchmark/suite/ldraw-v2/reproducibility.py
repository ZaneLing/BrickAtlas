"""Rebuild LDraw-2 and assert exact determinism, including actual request bytes."""
import hashlib
import json
import os
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[3]
DATA = ROOT / "benchmark/ldraw-v2"


def fingerprints():
    files = list((ROOT / "public/benchmark/ldraw-v2/models").glob("*.json"))
    files += list((ROOT / "public/benchmark/ldraw-v2/inputs").glob("*.json"))
    files += list((DATA / "request-snapshots/standard").glob("*.json"))
    files += [DATA / "release.json"]
    return {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest()
            for p in sorted(files)}


before = fingerprints()
env = {**os.environ, "PATH": str(ROOT / ".tools/node-v22.23.2-darwin-arm64/bin")
       + os.pathsep + os.environ["PATH"]}
result = subprocess.run(["npm", "run", "--prefix", "benchmark/suite/ldraw-v2", "ldraw:build"],
                        cwd=ROOT, env=env, capture_output=True, text=True)
(DATA / "rebuild-log.txt").write_text(result.stdout + result.stderr)
assert result.returncode == 0, "See rebuild-log.txt"
after = fingerprints()
assert before == after, [p for p, h in before.items() if after.get(p) != h]
(DATA / "reproducibility.json").write_text(json.dumps({
    "status": "passed", "filesCompared": len(before),
    "requestBytesIncluded": True, "generatorRerun": True, "sha256": after,
}, indent=2) + "\n")
print(json.dumps({"status": "passed", "filesCompared": len(before)}))
