"""Freeze extension evidence and identify the unchanged base dependency."""
import hashlib
import json
from runtime import HERE, BASE, OUT


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    frozen = json.loads((BASE / "release-check.json").read_text())
    for name, expected in frozen["artifactSha256"].items():
        if digest(BASE / name) != expected:
            raise ValueError(f"Frozen 1.0 changed: {name}")
    evidence = {key: json.loads((OUT / filename).read_text()) for key, filename in (
        ("semantic", "summary.json"), ("http", "http-summary.json"), ("browser", "arena-summary.json"))}
    if not all(e["passed"] and e["softwareValidationOnly"] for e in evidence.values()):
        raise ValueError("Incomplete acceptance evidence")
    release = json.loads((HERE / "data/release.json").read_text())
    cli_path = OUT / "oracle.cli-report.json"
    cli = json.loads(cli_path.read_text())
    assert cli.pop("benchmarkRelease") == "1.1"
    certificates = {c["case"]: c["transitionHash"] for c in release["cases"]}
    assert cli.pop("caseCertificates") == certificates
    assert cli == json.loads((OUT / "oracle.report.json").read_text())
    assert cli["successRate"]["numerator"] == cli["successRate"]["denominator"] == release["episodes"]
    evidence["versionedCli"] = {
        "passed": True, "softwareValidationOnly": True, "benchmarkRelease": "1.1",
        "caseCertificates": certificates, "reportSha256": digest(cli_path),
        "identicalToSemanticOracle": True, "episodes": release["episodes"],
    }
    assert evidence["http"]["httpEpisodes"] == release["episodes"]
    assert evidence["http"]["httpProbeResponses"] == release["probeResponses"]
    assert len(evidence["browser"]["completed"]) == 2 * release["structures"]
    assert all(c["unknownGeometry"] == 0 for c in release["cases"])
    assert release["independentProvenanceGroups"] >= 2
    assert next(c for c in release["cases"] if c["case"] == "airframe")["mandatoryOrder"]["chainLengthParts"] >= 5
    assert (HERE / "paper.pdf").is_file()
    artifacts, links = {}, {}
    for path in sorted(HERE.rglob("*")):
        if "__pycache__" in path.parts or path.suffix == ".pyc" or path.name == "release-check.json":
            continue
        relative = str(path.relative_to(HERE))
        if path.is_symlink():
            links[relative] = str(path.readlink())
        if path.is_file():
            artifacts[relative] = digest(path)
    output = {
        "schema": "brickplan-release-check/1.1", "releaseDate": "2026-10-02",
        "baseReleaseManifestSha256": digest(BASE / "release-check.json"),
        "unchangedBaseArtifacts": len(frozen["artifactSha256"]),
        "structures": release["structures"], "episodes": release["episodes"],
        "independentProvenanceGroups": release["independentProvenanceGroups"],
        "probeResponses": release["probeResponses"], "modelOrHumanResults": False,
        "evidence": evidence, "artifactSha256": artifacts, "relativeDependencies": links,
    }
    (HERE / "release-check.json").write_text(json.dumps(output, indent=2, sort_keys=True) + "\n")
    print(f"Frozen {len(artifacts)} extension artifacts; all {len(frozen['artifactSha256'])} base artifacts unchanged.")


if __name__ == "__main__":
    main()
