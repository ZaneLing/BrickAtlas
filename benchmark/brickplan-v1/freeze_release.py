"""Package acceptance evidence and hash the exact delivered release artifacts."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

from build import HERE, load_bank, write_json
from cases import CASES


def main():
    reports = HERE.parents[1] / "tem/brickplan-v1/validation"
    evidence = {name: json.loads((reports / file).read_text()) for name, file in (
        ("semantic", "summary.json"), ("http", "http-summary.json"), ("browser", "arena-summary.json"))}
    assert all(item["passed"] and item["softwareValidationOnly"] for item in evidence.values())
    certificates = [load_bank(config["id"])[3] for config in CASES]
    assert sum(c["reachableStates"] for c in certificates) == 58616
    assert sum(c["directedTransitions"] for c in certificates) == 568648
    assert all(c["unknownGeometry"] == 0 for c in certificates)
    assert (HERE / "paper.pdf").is_file()
    artifacts = {}
    for path in sorted(HERE.rglob("*")):
        if (path.is_file() and "__pycache__" not in path.parts
                and path.name != "release-check.json" and path.suffix != ".pyc"):
            artifacts[str(path.relative_to(HERE))] = hashlib.sha256(path.read_bytes()).hexdigest()
    write_json(HERE / "release-check.json", {
        "schema": "brickplan-release-check/1.0", "releaseDate": "2026-09-30",
        "track": "known-pose-structured", "modelOrHumanResults": False,
        "evidence": evidence, "structures": 2, "independentProvenanceGroups": 1,
        "episodes": 8, "probeResponses": 26, "artifactSha256": artifacts,
    })
    print(f"Frozen {len(artifacts)} artifacts with semantic, HTTP, and browser acceptance evidence.")


if __name__ == "__main__":
    main()
