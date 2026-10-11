"""Fail-closed original-model representation and source-identity admission."""
from functools import lru_cache
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]


@lru_cache(maxsize=1)
def source_audit():
    path = HERE / "data/source-intake/full-source-verification.json"
    content = path.read_bytes()
    report = json.loads(content)
    return report, hashlib.sha256(content).hexdigest()


def fidelity(model, plan):
    report, digest = source_audit()
    assert report["candidateRegistrySha256"] == plan["candidateRegistrySha256"]
    rows = {r["id"]: r for r in report["candidates"]}
    assert set(rows) == set(plan["newCandidates"])
    row = rows[model]
    identity = row.get("provenanceChecks") or {}
    passed = (row["status"] == "pass" and row.get("sourceFidelityReady") is True
              and row.get("lockedDependencyCompatible") is True
              and identity.get("status") == "pass"
              and identity.get("manifestAuthorAndLicenseMatchOriginal") is True)
    if row.get("manifestSha256"):
        manifest = ROOT / "web/public/models" / model / "manifest.json"
        assert hashlib.sha256(manifest.read_bytes()).hexdigest() == row["manifestSha256"]
        assert json.loads(manifest.read_text())["sourceHash"] == row["sourceHash"]
    return {
        "passed": passed, "auditSha256": digest,
        "fullHierarchyStatus": row["status"],
        "sourceIdentityStatus": identity.get("status"),
        "lockedDependencyCompatible": row.get("lockedDependencyCompatible"),
        "sourceHash": row.get("sourceHash"), "manifestSha256": row.get("manifestSha256"),
        "reason": None if passed else (
            row.get("error") or identity.get("rootIdentityIssue")
            or "Original source representation or identity was not fully verified."),
        "scope": "Whole original model representation and identity; geometric subassembly qualification is additional.",
    }
