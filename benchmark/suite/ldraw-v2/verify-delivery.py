#!/usr/bin/env python3
"""Final evidence and local document-link check; no model or human simulation."""
import argparse
import hashlib
import json
import urllib.request
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
DATA = ROOT / "benchmark/ldraw-v2"


def read(name):
    return json.loads((DATA / name).read_text())


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--base-url", default="http://127.0.0.1:5175")
    args = parser.parse_args()
    publication = read("publication-verification.json")
    ui = read("ui-verification.json")
    oracle = read("verification.json")
    experiments = read("phase-4-checks.json")
    runner = read("runner-verification.json")
    package = read("delivery-manifest.json")
    assert all(r["status"] == "passed" for r in [publication, ui, oracle, experiments, runner])
    assert len(ui["checks"]["models"]) == 24
    assert sum(m["loaded"] for m in ui["checks"]["models"]) == 15334
    assert not ui["pageErrors"]
    assert oracle["tasks"] == 617 and oracle["independentSourceOracle"] == 617
    assert experiments["modelApiCalls"] == runner["modelApiCalls"] == 0
    assert publication["appendixItems"] == 617 and publication["nullResultCells"] == 264
    frozen = read("v1-frozen-manifest.json")
    assert len(frozen["files"]) == 2131
    for row in frozen["files"]:
        assert hashlib.sha256((ROOT / row["path"]).read_bytes()).hexdigest() == row["sha256"], row["path"]
    # Also retain the earlier standalone preservation receipt.
    preservation = json.loads((DATA / "phase-5-preservation.txt").read_text())
    assert preservation["protectedFiles"] == 2131 and preservation["changed"] == []
    for path, digest in package["documents"].items():
        assert hashlib.sha256((ROOT / path).read_bytes()).hexdigest() == digest
    archive = ROOT / "benchmark/paper/brickatlas-ldraw-v2-source.zip"
    with zipfile.ZipFile(archive) as zipped:
        assert zipped.testzip() is None
        assert len(zipped.namelist()) == package["sourceArchiveFiles"]
    links = []
    for path in ["ldraw-v2.html", "benchmark/ldraw-v2/docs/main-v2.pdf",
                 "benchmark/ldraw-v2/docs/supplement-v2.pdf",
                 "benchmark/ldraw-v2/docs/brickatlas-ldraw-v2-source.zip"]:
        with urllib.request.urlopen(args.base_url.rstrip("/") + "/" + path, timeout=15) as response:
            body = response.read()
            assert response.status == 200 and len(body) > 0
            local = ROOT / ("dist-ldraw-v2" if path.endswith(".html") else "public") / path
            assert hashlib.sha256(body).digest() == hashlib.sha256(local.read_bytes()).digest()
            links.append({"path": path, "status": response.status, "bytes": len(body)})
    report = {
        "status": "passed", "phase": 5, "v1PreservedFiles": preservation["protectedFiles"],
        "publications": publication["pdfs"], "websiteSourcesLoaded": 24, "instancesLoaded": 15334,
        "taskOracle": 617, "conditionRequests": experiments["conditionRequests"],
        "freshRunnerCanaries": len(runner["wireCanaries"]), "modelApiCalls": 0,
        "documentLinks": links, "packageIntegrity": True,
        "requiredHumanTaskReviews": 251, "requiredPhysicalPairReviews": 573,
        "independentHumanCertification": "pending", "diagnosticLocalization": "unvalidated",
        "optionalPhase3": "skipped-by-default; modular claims only"}
    (DATA / "phase-5-checks.json").write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
