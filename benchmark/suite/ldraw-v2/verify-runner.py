#!/usr/bin/env python3
"""Offline adapter/condition canaries and protected-path rejection."""
import json
import hashlib
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
HERE = Path(__file__).resolve().parent
DATA = ROOT / "benchmark/ldraw-v2"
NODE = ROOT / ".tools/node-v22.23.2-darwin-arm64/bin/node"
CLI = ROOT / "node_modules/tsx/dist/cli.mjs"
plan = json.loads((ROOT / "benchmark/paper/ldraw-v2-experiments.json").read_text())
revision = hashlib.sha256(b"".join(p.read_bytes() for p in [
    HERE / "run-model.ts", HERE / "score.ts", ROOT / "src/benchmark-v2/scoring.ts"])).hexdigest()[:12]
rows = []
for i, condition in enumerate(plan["conditions"]):
    adapter = "claude" if i % 2 else "gpt41"
    out = DATA / "dry-runs" / f"final-{revision}-{adapter}-{condition['id']}-canary"
    if not out.exists():
        command = [str(NODE), str(CLI), str(HERE / "run-model.ts"), "--adapter",
                   str(HERE / f"model-adapters/{adapter}.json"), "--condition", condition["id"],
                   "--limit", "1", "--out", str(out)]
        subprocess.run(command, check=True, capture_output=True)
    manifest = json.loads((out / "manifest.json").read_text())
    assert manifest["status"] == "dry-run-complete" and manifest["calls"] == 0 and manifest["results"] is None
    for filename, digest in manifest["codeHashes"].items():
        assert hashlib.sha256((HERE / filename).read_bytes()).hexdigest() == digest
    assert "../../../src/benchmark-v2/scoring.ts" in manifest["codeHashes"]
    rows.append({"condition": condition["id"], "adapter": adapter, "requests": len(manifest["requests"]),
                 "manifest": str((out / "manifest.json").relative_to(ROOT))})
forbidden = subprocess.run([
    str(NODE), str(CLI), str(HERE / "run-model.ts"), "--adapter",
    str(HERE / "model-adapters/gpt41.json"), "--input",
    str(ROOT / "public/benchmark/ldraw-v2/models/31028.json"),
    "--out", str(DATA / "dry-runs/forbidden-must-not-exist")], capture_output=True, text=True)
assert forbidden.returncode != 0 and "only versioned inputs" in forbidden.stderr
assert not (DATA / "dry-runs/forbidden-must-not-exist").exists()
report = {"status": "passed", "modelApiCalls": 0, "wireCanaries": rows, "runnerInternalPathRejected": True}
(DATA / "runner-verification.json").write_text(json.dumps(report, indent=2) + "\n")
print(f"Offline runner canaries: {len(rows)} conditions; internal path rejected before output.")
