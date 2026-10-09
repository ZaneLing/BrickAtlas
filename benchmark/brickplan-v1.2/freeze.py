"""Freeze only the verified 1.2 deliverable; preserve prior releases byte-for-byte."""
import hashlib
import json
from pathlib import Path

from build import HERE, load_bank, write_json
from cases import CASES
from evaluate import evaluate

ROOT = HERE.parents[1]
OUT = ROOT / "tem/brickplan-v1.2/validation"


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    previous = {}
    for name in ("brickplan-v1", "brickplan-v1.1"):
        folder = HERE.with_name(name)
        manifest = json.loads((folder / "release-check.json").read_text())
        for file, digest in manifest["artifactSha256"].items():
            assert sha(folder / file) == digest, (name, file)
        previous[name] = {"artifacts":len(manifest["artifactSha256"]),
                          "manifestSha256":sha(folder / "release-check.json")}
    release = json.loads((HERE / "data/release.json").read_text())
    banks = [load_bank(c["id"]) for c in CASES]
    assert release["structures"] == len(banks)
    assert release["episodes"] == sum(len(b[1]["episodes"]) for b in banks)
    assert release["independentProvenanceGroups"] == len({b[3]["provenanceGroup"] for b in banks})
    reports = {}
    for name in ("semantic", "http", "browser"):
        path = OUT / f"{name}-summary.json"
        value = json.loads(path.read_text())
        assert value["passed"] and value["softwareValidationOnly"]
        reports[name] = value
    assert len(reports["browser"]["completed"]) == 6
    oracle = json.loads((OUT / "oracle-0.report.json").read_text())
    replayed = evaluate(json.loads((OUT / "oracle-0.submission.json").read_text()))
    assert replayed == {k:v for k,v in oracle.items() if k != "expandedSearchNodes"}
    assert oracle["successRate"]["numerator"] == oracle["successRate"]["denominator"] == release["episodes"]
    assert oracle["structures"] == release["structures"]
    assert oracle["independentProvenanceGroups"] == release["independentProvenanceGroups"]
    assert all(r["actionRegret"] == 0 for r in oracle["regretAndEfficiency"])
    assert all(x["exactFirstConflictAccuracy"]["value"] == 1 for x in oracle["lookahead"]["distanceCurve"].values())
    cli = json.loads((OUT / "browser.cli-report.json").read_text())
    assert cli["successRate"]["numerator"] == 6 and cli["successRate"]["denominator"] == release["episodes"]
    assert cli["track"] == "image-id" and cli["structures"] == release["structures"]
    assert json.loads((OUT / "final-smoke.json").read_text())["passed"]
    assert (HERE / "paper.pdf").stat().st_size > 10000
    for frame in json.loads((HERE / "figures/provenance.json").read_text())["frames"]:
        assert sha(HERE / "figures" / frame["file"]) == frame["sha256"]
    artifacts, links = {}, {}
    for path in sorted(HERE.rglob("*")):
        if "__pycache__" in path.parts or path.suffix == ".pyc" or path.name == "release-check.json":
            continue
        relative = str(path.relative_to(HERE))
        if path.is_symlink():
            links[relative] = str(path.readlink())
        if path.is_file():
            artifacts[relative] = sha(path)
    external = {}
    for path in sorted(OUT.glob("*.json")):
        external[str(path.relative_to(ROOT))] = sha(path)
    write_json(HERE / "release-check.json", {
        "schema":"brickplan-release-check/1.2", "date":"2026-10-05",
        "modelOrHumanResults":False, "previousReleases":previous,
        "structures":release["structures"],"sourceGroups":release["independentProvenanceGroups"],
        "episodes":release["episodes"],"probeResponses":release["probeResponses"],
        "evidence":reports, "artifactSha256":artifacts, "relativeDependencies":links,
        "externalEvidenceSha256":external,
        "unresolved": ["Static relation rule solves all episodes", "Only two source groups",
                       "No measured VLM/human or physical construction study"],
    })
    print(f"Frozen {len(artifacts)} artifacts; prior releases unchanged: {previous}")


if __name__ == "__main__":
    main()
