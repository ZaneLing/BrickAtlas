"""Freeze and verify release bytes, predecessor integrity and published claims."""
import argparse
from collections import Counter
import gzip
import hashlib
import importlib.metadata
import json
import platform
from pathlib import Path

import fitz
from PIL import Image

from bank import DATA, HERE, ROOT, task_bank, write_json
from controls import summarize
from mission import canonical_hash

MANIFEST = DATA / "release.json"
REPORT = HERE / "release-check.json"
ARCHIVE = ROOT / "tem/research/20261008-brickplan-cvpr-upgrade"
WORKBENCH = ROOT / "tem/research/20261009-react-workbench"


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def predecessor_check():
    snapshot_path = DATA / "predecessor-hashes.json"
    if not snapshot_path.exists():
        raise FileNotFoundError("Freeze requires the pre-change predecessor snapshot")
    snapshot = json.loads(snapshot_path.read_text())
    counts = {}
    for version, files in snapshot.items():
        for name, digest in files.items():
            path = HERE.parent / version / name
            if not path.is_file() or sha(path) != digest:
                raise AssertionError(f"Frozen predecessor changed: {version}/{name}")
        counts[version] = len(files)
    return counts


def claim_check():
    bank = task_bank()
    controls = json.loads((DATA / "software-controls.json").read_text())
    records = json.loads(gzip.decompress((DATA / "software-control-records.json.gz").read_bytes()))
    for name, entry in controls["policies"].items():
        rows = [r for r in records if r["policy"] == name]
        assert summarize(rows) == entry["all"], name
        for field, attribute in (("byTier", "tier"), ("bySourceGroup", "sourceGroup"), ("bySeed", "seed")):
            for key, summary in entry[field].items():
                assert summarize([r for r in rows if str(r[attribute]) == key]) == summary, (name, field, key)
        assert len({(r["taskId"], r["seed"]) for r in rows}) == len(rows)
    assert controls["humanResults"] is None and controls["visualModelResults"] is None
    cert = json.loads((DATA / "certificate.json").read_text())
    assert all(c["bellmanVerified"] and c["runtimeEdgesVerified"] and c["lowerBoundVerified"]
               and c["reachableProductStates"] == c["productStates"] for c in cert["oracles"].values())
    expected = {"EpisodeCount": len(bank["episodes"]), "ProbeCount": len(bank["probes"]),
                "PairCount": len(bank["pairs"]), "ProfileCount": len(bank["profiles"]),
                "SourceCount": len({p["sourceGroup"] for p in bank["profiles"]}),
                "OracleCount": len(cert["oracles"]),
                "ProductCount": sum(c["productStates"] for c in cert["oracles"].values()),
                "EdgeCount": sum(c["directedTransitions"] for c in cert["oracles"].values()),
                "MaxGap": max(t["relaxationGap"] for t in bank["episodes"]),
                "OldLabels": sum(r["checked"] for r in json.loads((DATA / "predecessor-static-audit.json").read_text()))}
    stats = json.loads((DATA / "publication-statistics.json").read_text())
    assert stats["counts"] == expected and stats["bankHash"] == canonical_hash(bank)
    assert stats["byTier"] == Counter(t["tier"] for t in bank["episodes"])
    for name, value in expected.items():
        assert rf"\newcommand{{\{name}}}{{{value:,}}}" in (HERE / "generated.tex").read_text()
    provenance = json.loads((HERE / "figures/provenance.json").read_text())
    assert provenance["bankHash"] == canonical_hash(bank)
    assert provenance["meshSha256"] == sha(HERE / "arena/meshes.json")
    for item in provenance["figures"]:
        assert item["sha256"] == sha(HERE / "figures" / item["file"])
    assert json.loads((DATA / "semantic-validation.json").read_text())["passed"]
    browser = json.loads((DATA / "workbench-validation.json").read_text())
    assert browser["status"] == "passed" and not browser["errors"] and len(browser["checks"]) >= 9
    for name, digest in browser["frontendFiles"].items():
        assert sha(ROOT / name) == digest, f"Frontend changed since browser validation: {name}"
    integration = json.loads((DATA / "workbench-integration.json").read_text())
    assert integration["status"] == "passed" and not integration["errors"]
    assert all(integration[key] for key in ("liveLocalCall", "studyIsolation", "staticSubpath"))
    audit = json.loads((DATA / "upgrade-audit.json").read_text())
    assert audit["passed"] and audit["census"]["episodes"] == len(bank["episodes"])
    assert audit["census"]["probes"] == len(bank["probes"])
    case_provenance = json.loads((HERE / "cases/provenance.json").read_text())
    assert case_provenance["realInference"] and case_provenance["bankHash"] == canonical_hash(bank)
    assert case_provenance["traceSha256"] == sha(HERE / "cases/local-vlm.json")
    case = json.loads((HERE / "cases/local-vlm.json").read_text())
    assert case_provenance["calls"] == len(case["steps"]) == 4
    assert all(s["status"] == "executed" and s["rawOutput"] and s["feedback"]["code"] == "INVALID_ACTION"
               for s in case["steps"])
    for name, digest in case_provenance["images"].items():
        path = HERE / "cases/media" / name
        assert sha(path) == digest and Image.open(path).width == 1920
    from bank import task_by_id, make_mission
    from session import replay_export
    task = task_by_id(case["stableTaskId"])
    replayed = replay_export(make_mission(task), task, json.loads(
        (HERE / "cases/local-vlm.authoritative.json").read_text()))
    assert len(replayed.events) == len(case["steps"]) + 1  # Controller terminates after call limit.
    template = json.loads((HERE / "cvpr-template-provenance.json").read_text())
    for name, item in template["files"].items():
        assert sha(HERE / name) == item["sha256"]
    pdf = fitz.open(HERE / "paper.pdf")
    text = "\n".join(page.get_text() for page in pdf)
    assert "??" not in text and not any("\u4e00" <= c <= "\u9fff" for c in text)
    assert len(pdf) <= 8 and all(tuple(page.rect) == (0, 0, 612, 792) for page in pdf)
    assert all(token in text for token in ("1,802,728", "4,372", "75,454", "Pending", "739", "145"))
    supplement = fitz.open(HERE / "supplement.pdf")
    supplement_text = "\n".join(page.get_text() for page in supplement)
    assert "??" not in supplement_text and not any("\u4e00" <= c <= "\u9fff" for c in supplement_text)
    assert r"\usepackage[margin" not in (HERE / "paper.tex").read_text()
    return {"bankHash": canonical_hash(bank), "controlRecords": len(records),
            "paperPages": len(pdf), "supplementPages": len(supplement), "counts": expected,
            "claimDataAgreement": True, "figureHashesVerified": True,
            "semanticEvidencePassed": True, "browserEvidencePassed": True,
            "workbenchIntegrationPassed": True, "nativeImagesVerified": True,
            "realModelCaseVerified": True, "officialTemplateHashesVerified": True}


def release_paths():
    ignored = {MANIFEST, REPORT}
    return sorted(p for p in HERE.rglob("*") if p.is_file() and p not in ignored
                  and HERE / "release" not in p.parents
                  and "__pycache__" not in p.parts and not p.name.startswith(".")
                  and p.suffix not in (".pyc", ".aux", ".log", ".out", ".synctex", ".bbl", ".blg", ".brf"))


def dependencies():
    files = [HERE.parent / "brickplan-v1.2" / n for n in ("engine.py", "visual.py", "raster.c")]
    files += [HERE.parent / "brickplan-v1/render_assets.py", ROOT / "package.json", ROOT / "package-lock.json"]
    files += [ROOT / "node_modules/three" / n for n in ("build/three.module.min.js", "build/three.core.min.js", "LICENSE")]
    for folder in (ROOT / "web/brickplan", ROOT / "deliverables/brickplan-paper"):
        files += [p for p in folder.rglob("*") if p.is_file() and "node_modules" not in p.parts
                  and not any(part.startswith(".") for part in p.relative_to(folder).parts)]
    provenance = json.loads((DATA / "render-provenance.json").read_text())
    library = ROOT / "assets-source/ldraw-library/locked"
    for relative, digest in provenance["files"].items():
        path = library / relative
        assert sha(path) == digest, f"Locked source mismatch: {relative}"
        files.append(path)
    return {str(p.relative_to(ROOT)): sha(p) for p in files}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("command", choices=("freeze", "check"))
    args = parser.parse_args()
    if args.command == "freeze":
        snapshot = DATA / "predecessor-hashes.json"
        prior = json.loads(snapshot.read_text())
        prior["brickplan-v2"] = json.loads((ARCHIVE / "v2-predecessor-hashes.json").read_text())
        write_json(snapshot, prior)
        for name in ("workbench-validation.json", "workbench-integration.json"):
            (DATA / name).write_bytes((WORKBENCH / name).read_bytes())
    prior = predecessor_check()
    claims = claim_check()
    files = {str(p.relative_to(HERE)): sha(p) for p in release_paths()}
    if args.command == "freeze":
        write_json(MANIFEST, {
            "schema": "brickplan-release/2.1", "files": files, "dependencies": dependencies(),
            "predecessorsUnchanged": prior, "claims": claims,
            "environment": {"python": platform.python_version(), "platform": platform.platform(),
                            "packages": {p: importlib.metadata.version(p)
                                         for p in ("numpy", "Pillow", "matplotlib", "PyMuPDF")}},
            "scope": "Byte integrity and recorded software evidence, not a cryptographic trust boundary."})
    frozen = json.loads(MANIFEST.read_text())
    if files != frozen["files"]:
        changes = sorted(name for name in files.keys() | frozen["files"].keys()
                         if files.get(name) != frozen["files"].get(name))
        raise AssertionError(f"Release files differ: {changes}")
    for name, digest in frozen["dependencies"].items():
        assert sha(ROOT / name) == digest, f"Dependency changed: {name}"
    assert claims == frozen["claims"]
    report = {"passed": True, "releaseManifestSha256": sha(MANIFEST),
              "releaseFiles": len(files), "dependencyFiles": len(frozen["dependencies"]),
              "predecessorsUnchanged": prior, **claims}
    write_json(REPORT, report)
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
