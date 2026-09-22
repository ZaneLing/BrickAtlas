#!/usr/bin/env python3
"""Reproduce construction, free study, qualification queue and focused checks."""
import os
import subprocess
import sys

from common import HERE, ROOT, VERSION, filehash, read, reference, write


def validate_all():
    records = []
    generated = ("public.json", "gold.json", "sampling-ledger.json", "summary.json", "render-specs.json")
    before = {name: filehash(HERE / name) for name in generated}
    env = dict(os.environ)
    env.pop("PYTHONPATH", None)
    env["PYTHONNOUSERSITE"] = "1"
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    node = ROOT / ".tools/node-v22.23.2-darwin-arm64/bin/node"

    def execute(name, command, cwd=ROOT):
        process = subprocess.run([str(v) for v in command], cwd=cwd, env=env,
                                 capture_output=True, text=True, check=False)
        record = {"name": name, "command": [str(v) for v in command],
                  "cwd": str(cwd.relative_to(ROOT)) or ".",
                  "status": "passed" if process.returncode == 0 else "failed",
                  "returncode": process.returncode,
                  "stdout": process.stdout, "stderr": process.stderr}
        records.append(record)
        print(name, record["status"], flush=True)
        if process.returncode:
            write(HERE / "validation.json", {"version": VERSION, "status": "failed", "checks": records})
            raise RuntimeError(process.stderr or process.stdout)

    execute("rebuild", [sys.executable, HERE / "build.py"])
    after = {name: filehash(HERE / name) for name in generated}
    assert before == after, "Construction regeneration not byte-identical"
    records.append({"name": "byte_identical_constructor_regeneration", "status": "passed", "sha256": after})
    execute("independent_graph_pixel_source_audit", [sys.executable, HERE / "verify.py"])
    execute("manifest_local_study_qualification_analysis", [sys.executable, HERE / "study.py", "all"])
    execute("semantic_receipt_joint_qualification_adapter_tests", [
        sys.executable, "-m", "unittest", "discover", "-s", HERE, "-p", "test_*.py", "-v"])
    execute("typescript", [node, ROOT / "node_modules/typescript/bin/tsc", "--noEmit",
            "--target", "ES2022", "--module", "ESNext", "--moduleResolution", "Bundler",
            "--resolveJsonModule", "--allowSyntheticDefaultImports", "--skipLibCheck",
            "--types", "vite/client,node", HERE / "render.ts", HERE / "capture.ts", HERE / "test_review_ui.ts"])
    execute("reviewer_ui_canary_no_judgments", [node, ROOT / "node_modules/tsx/dist/cli.mjs", HERE / "test_review_ui.ts"])
    result = {"version": VERSION, "status": "passed", "python": sys.version,
              "checks": records, "summary": read(HERE / "summary.json"),
              "artifacts": [reference(HERE / f) for f in (*generated, "study-manifest.json",
                  "baseline-report.json", "algorithmic-receipts.json", "algorithmic-scores.json",
                  "dependency-audit.json", "qualification-queue.json", "qualification-status.json",
                  "qualification-eligibility.json", "ui-verification.json")],
              "model_calls": 0, "human_judgments": 0, "paid_calls": 0}
    write(HERE / "validation.json", result)
    print({"status": "passed", "check_count": len(records), "artifact_count": len(result["artifacts"])})


if __name__ == "__main__":
    validate_all()
