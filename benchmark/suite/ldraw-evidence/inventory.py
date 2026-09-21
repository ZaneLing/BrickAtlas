#!/usr/bin/env python3
"""Inventory candidate run artifacts without treating historical pilots as v2."""
import argparse
import subprocess
from pathlib import Path
from common import ROOT, DATA, VERSION, load, save, sha


def main():
    argparse.ArgumentParser(description=__doc__).parse_args()
    command = ["rg", "--files", "--hidden", "-g", "*manifest*.json",
               "-g", "submissions.json", "-g", "scores.json",
               "-g", "!**/site-packages/**", "-g", "!**/node_modules/**",
               "-g", "!**/lib/**", "-g", "!**/.cache/**", "-g", "!**/.git/**",
               "benchmark", "public", ".preview"]
    paths = subprocess.check_output(command, cwd=ROOT, text=True).splitlines()
    v2, historical, responses = [], [], []
    for relative in paths:
        p = ROOT / relative
        if "ldraw-evidence-v1" in relative:
            continue
        if p.name in {"submissions.json", "scores.json"}:
            responses.append({"path": relative, "sha256": sha(p)})
            continue
        try:
            d = load(p)
        except (ValueError, OSError):
            continue
        if not isinstance(d, dict):
            continue
        if d.get("release") == "brickatlas-ldraw-2" and "mode" in d:
            v2.append({"path": relative, "sha256": sha(p), "mode": d["mode"],
                       "status": d.get("status"), "calls": d.get("calls"),
                       "condition": d.get("condition"), "requests": len(d.get("requests", []))})
        elif d.get("status") == "complete":
            historical.append({"path": relative, "sha256": sha(p),
                               "role": "not-established-as-v2-evidence"})
    report = {"analysis_version": VERSION, "searched_roots": ["benchmark", "public", ".preview"],
              "v2_runs": sorted(v2, key=lambda r: r["path"]),
              "v2_live_runs": [r for r in v2 if r["mode"] == "live-inference"],
              "response_artifacts": responses, "historical_complete_manifests": historical,
              "model_results_status": "not-run" if not any(r["mode"] == "live-inference" for r in v2) else "requires-receipt-validation",
              "scope": "Local workspace inventory; no external run locations supplied."}
    save(DATA / "run-inventory.json", report)
    print({"v2_runs": len(v2), "live": len(report["v2_live_runs"]), "response_artifacts": len(responses)})


if __name__ == "__main__":
    main()
