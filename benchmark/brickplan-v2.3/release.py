"""Freeze and verify release bytes, predecessor integrity and published claims."""
import argparse
from collections import Counter
import gzip
import hashlib
import importlib.metadata
import json
import platform
from pathlib import Path
import re
import zipfile

import fitz
from PIL import Image

from bank import DATA, HERE, ROOT, task_bank, write_json
from controls import summarize
from mission import canonical_hash

MANIFEST = DATA / "release.json"
REPORT = HERE / "release-check.json"
ARCHIVE = ROOT / "tem/research/20261008-brickplan-cvpr-upgrade"
REVISION = ROOT / "tem/research/20261009-brickplan-v22-revision"
WORKBENCH = Path("/tmp/brickplan-v23-work/frontend")


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def predecessor_check():
    snapshot_path = DATA / "predecessor-hashes.json"
    if not snapshot_path.exists():
        raise FileNotFoundError("Freeze requires the pre-change predecessor snapshot")
    snapshot = json.loads(snapshot_path.read_text())
    v21 = v21_snapshot()
    if "brickplan-v2.1" in snapshot:
        assert snapshot["brickplan-v2.1"] == v21, "Predecessor snapshot changed"
    snapshot["brickplan-v2.1"] = v21
    counts = {}
    for version, files in snapshot.items():
        for name, digest in files.items():
            path = HERE.parent / version / name
            if not path.is_file() or sha(path) != digest:
                raise AssertionError(f"Frozen predecessor changed: {version}/{name}")
        counts[version] = len(files)
    return counts


def v21_snapshot():
    original = REVISION / "predecessor-sha256.json"
    if original.exists():
        snapshot = json.loads(original.read_text())
        prefix = "benchmark/brickplan-v2.1/"
        assert snapshot and all(name.startswith(prefix) for name in snapshot)
        return {name.removeprefix(prefix): digest for name, digest in snapshot.items()}
    # A clean checkout retains the frozen snapshot without local research logs.
    return json.loads((DATA / "predecessor-hashes.json").read_text())["brickplan-v2.1"]


def prepare_evidence():
    bank_hash = canonical_hash(task_bank())
    reports = ("workbench-validation.json", "workbench-integration.json")
    for name in reports:
        evidence = WORKBENCH / name if (WORKBENCH / name).exists() else DATA / name
        report = json.loads(evidence.read_text())
        assert report["status"] == "passed" and not report["errors"]
        assert report["bankHash"] == bank_hash, f"Stale frontend evidence: {name}"
    snapshot = v21_snapshot()
    folder = DATA / "historical/2.1"
    archived = {}
    for name in (*reports, "browser-validation.json", "portal-validation.json", "release.json"):
        path = DATA / name
        if path.exists() and sha(path) == snapshot.get("data/" + name):
            folder.mkdir(parents=True, exist_ok=True)
            destination = folder / name
            if destination.exists():
                assert sha(destination) == sha(path), f"Historical archive conflict: {name}"
            path.replace(destination)
        if (folder / name).exists():
            assert sha(folder / name) == snapshot["data/" + name]
            archived[name] = sha(folder / name)
    if archived:
        write_json(folder / "provenance.json", {
            "release": "2.1", "scope": "Inherited evidence, not validation of BrickPlan 2.3.",
            "files": archived})
    for name in reports:
        if (WORKBENCH / name).exists():
            (DATA / name).write_bytes((WORKBENCH / name).read_bytes())


def historical_case_check():
    provenance = json.loads((HERE / "cases/provenance.json").read_text())
    history = json.loads((HERE / "cases/historical-release.json").read_text())
    task = json.loads((HERE / "cases/task.v2.1.json").read_text())
    case = json.loads((HERE / "cases/local-vlm.json").read_text())
    original = json.loads((HERE.parent / "brickplan-v2.1/data/tasks.private.json").read_text())
    assert history["release"] == "2.1" and history["responseAndImageBytesUnchanged"]
    assert provenance["realInference"] and provenance["bankHash"] == history["bankHash"] == canonical_hash(original)
    assert task == next(t for t in original["episodes"] if t["id"] == history["taskId"])
    assert history["taskHash"] == canonical_hash(task)
    assert case["stableTaskId"] == history["taskId"]
    assert provenance["traceSha256"] == sha(HERE / "cases/local-vlm.json")
    snapshot = v21_snapshot()
    preserved = ["cases/local-vlm.json", "cases/local-vlm.authoritative.json", "cases/provenance.json"]
    preserved += ["cases/media/" + name for name in provenance["images"]]
    for name in preserved:
        assert sha(HERE / name) == snapshot[name], f"Historical case bytes changed: {name}"
    assert provenance["calls"] == len(case["steps"]) > 0
    assert all(s["status"] == "executed" and s["rawOutput"] and s["feedback"]["code"] == "INVALID_ACTION"
               for s in case["steps"])
    for name, digest in provenance["images"].items():
        path = HERE / "cases/media" / name
        assert sha(path) == digest and Image.open(path).width == 1920
    from bank import make_mission
    from session import replay_export
    replayed = replay_export(make_mission(task), task, json.loads(
        (HERE / "cases/local-vlm.authoritative.json").read_text()))
    assert len(replayed.events) == len(case["steps"]) + 1
    return {"release": history["release"], "bankHash": history["bankHash"],
            "taskHash": history["taskHash"], "traceSha256": provenance["traceSha256"],
            "calls": len(case["steps"]), "responseAndImageBytesUnchanged": True}


def overleaf_check():
    from export_overleaf import collect
    folder = ROOT / "deliverables/brickplan-paper"
    manifest = json.loads((folder / "manifest.json").read_text())
    archive_path = folder / "brickplan-cvpr-overleaf.zip"
    assert manifest["archiveSha256"] == sha(archive_path), "Overleaf archive changed"
    inventory = json.loads((folder / "overleaf/SOURCE-MANIFEST.json").read_text())
    expected = {"main.tex" if name == "paper.tex" else name for name in collect()} | {"README.md"}
    assert set(inventory) == expected, "Re-export Overleaf for the current manuscript"
    with zipfile.ZipFile(archive_path) as archive:
        for name, digest in inventory.items():
            assert hashlib.sha256(archive.read(name)).hexdigest() == digest
            if name != "README.md":
                assert sha(HERE / ("paper.tex" if name == "main.tex" else name)) == digest, \
                    f"Stale Overleaf source: {name}; rerun export_overleaf.py --check"
    for name, target, key in (("paper.pdf", "brickplan-main.pdf", "main"),
                              ("supplement.pdf", "brickplan-supplement.pdf", "supplement")):
        assert sha(HERE / name) == sha(folder / target), "Overleaf PDFs are stale"
        check = manifest["checks"][key]
        assert check["independentCompilePassed"] and check["textMatchesPublishedPDF"]
        assert check["pages"] == len(fitz.open(HERE / name))
    return {"archiveSha256": sha(archive_path), "sourceFiles": len(inventory), "independentCompilePassed": True}


def claim_check():
    bank = task_bank()
    controls = json.loads((DATA / "software-controls.json").read_text())
    records = json.loads(gzip.decompress((DATA / "software-control-records.json.gz").read_bytes()))
    for name, entry in controls["policies"].items():
        rows = [r for r in records if r["policy"] == name]
        assert summarize(rows) == entry["all"], name
        for field, attribute in (("byTier", "tier"), ("bySourceGroup", "sourceGroup"),
                                 ("bySeed", "seed"), ("bySplit", "split")):
            for key, summary in entry[field].items():
                assert summarize([r for r in rows if str(r[attribute]) == key]) == summary, (name, field, key)
        assert len({(r["taskId"], r["seed"]) for r in rows}) == len(rows)
    assert controls["humanResults"] is None and controls["visualModelResults"] is None
    cert = json.loads((DATA / "certificate.json").read_text())
    assert cert["tasksHash"] == canonical_hash(bank)
    assert all(c["bellmanVerified"] and c["runtimeEdgesVerified"] and c["lowerBoundVerified"]
               and c["reachableProductStates"] == c["productStates"] for c in cert["oracles"].values())
    observation = json.loads((DATA / "observation-certificate.json").read_text())
    pairs = [p for p in bank["pairs"] if p["kind"] == "visual-geometry"]
    assert observation["bankHash"] == canonical_hash(bank) and observation["complete"]
    assert observation["initialViews"] == ["isometric", "left", "rear", "right"]
    assert observation["pairsChecked"] == len(pairs) == len(observation["pairs"])
    assert {p["pairId"] for p in observation["pairs"]} == {p["id"] for p in pairs}
    assert all(p["passed"] and p["differentStaticInput"] and p["sameSemanticText"]
               for p in observation["pairs"])
    independent = json.loads((DATA / "independent-audit/summary.json").read_text())
    assert independent["bankHash"] == canonical_hash(bank)
    assert independent["rows"] == independent["passed"] == len(bank["episodes"]) + len(bank["probes"])
    assert independent["tableCount"] == len(cert["oracles"])
    assert independent["tableStates"] == sum(c["productStates"] for c in cert["oracles"].values())
    assert independent["pairCount"] == len(bank["pairs"])
    assert not independent["failures"] and not independent["pairFailures"] and independent["tableMismatches"] == 0
    independent_tables = json.loads((DATA / "independent-audit/oracle-audit.json").read_text())
    assert len(independent_tables) == len(cert["oracles"])
    assert all(r["lengthMatches"] and r["costMismatches"] == 0 for r in independent_tables)
    sources = json.loads((DATA / "source-question-audit.json").read_text())
    assert sources["passed"] and sources["bankHash"] == canonical_hash(bank)
    assert sources["questionsChecked"] == len(bank["episodes"]) + len(bank["probes"])
    assert {r["id"] for r in sources["questions"]} == {
        r["id"] for r in bank["episodes"] + bank["probes"]}
    assert all(r["passed"] and r["originalPosesVerified"] and r["sourceGraphRecomputed"]
               for r in sources["sources"])
    for row in sources["sources"]:
        if row["modelId"].startswith("v23-"):
            assert row["independentLeafMappingsVerified"]
            proof = DATA / "source-intake/leaf-proofs" / (row["modelId"] + ".json.gz")
            assert hashlib.sha256(gzip.decompress(proof.read_bytes())).hexdigest() == row["independentLeafProofSha256"]
    primary = [p for p in pairs if p.get("evaluationCohort") == "primary-matched"]
    assert {r["id"] for r in sources["matchedPairs"]} == {p["id"] for p in primary}
    assert all(r["passed"] for r in sources["matchedPairs"])
    assert sources["independentSourceGroups"] > 16 and sources["matchedHeldoutSources"]
    matched = json.loads((DATA / "matched-controls.json").read_text())
    assert matched["bankHash"] == canonical_hash(bank) and matched["primaryPairs"] == len(primary)
    assert matched["status"] == "generated" and matched["visualModelResults"] is None
    assert matched["humanResults"] is None
    for audit in matched["matchingContractAudit"].values():
        assert audit["checkedPairs"] == len(primary) and not audit["unequalPairIds"]
    for name in ("count-only", "part-type-color-presence", "part-type-color-count",
                 "sequence-only", "public-metadata", "public-metadata-and-inventory"):
        evidence = matched["certificates"][name]["cohorts"]["primary-matched"]["all"]
        assert evidence["pairs"] == evidence["identicalRepresentationPairs"] == len(primary)
        assert evidence["jointSourceMacro"]["tight"]
        assert evidence["jointSourceMacro"]["upperBound"]["value"] == 0
    expected = {"EpisodeCount": len(bank["episodes"]), "ProbeCount": len(bank["probes"]),
                "PairCount": len(bank["pairs"]), "ProfileCount": len(bank["profiles"]),
                "SourceCount": len({t["sourceGroup"] for t in bank["episodes"]}),
                "OracleCount": len(cert["oracles"]),
                "ProductCount": sum(c["productStates"] for c in cert["oracles"].values()),
                "EdgeCount": sum(c["directedTransitions"] for c in cert["oracles"].values()),
                "MaxGap": max(t["relaxationGap"] for t in bank["episodes"]),
                "OldLabels": sum(r["checked"] for r in json.loads((DATA / "predecessor-static-audit.json").read_text())),
                "CalibrationCount": sum(p["scoringRole"] == "calibration" for p in bank["probes"]),
                "DiscriminativeCount": sum(p["scoringRole"] == "discriminative" for p in bank["probes"]),
                "ProblemCount": len({p["canonicalProblem"] for p in bank["probes"]}),
                "PolicyRuns": len({(r["taskId"], r["seed"]) for r in records if r["policy"] != "oracle"}),
                "RawPolicyRuns": len(records)}
    stats = json.loads((DATA / "publication-statistics.json").read_text())
    assert all(stats["counts"][key] == value for key, value in expected.items())
    assert stats["bankHash"] == canonical_hash(bank)
    from documents import publication_inputs, publication_summary
    assert stats["counts"] == publication_summary(bank, publication_inputs(bank))["counts"]
    assert stats["byTier"] == Counter(t["tier"] for t in bank["episodes"])
    for name, value in stats["counts"].items():
        assert rf"\newcommand{{\{name}}}{{{value:,}}}" in (HERE / "generated.tex").read_text()
    provenance = json.loads((HERE / "figures/provenance.json").read_text())
    assert provenance["bankHash"] == canonical_hash(bank)
    assert provenance["meshSha256"] == sha(HERE / "arena/meshes.json")
    assert provenance["captionFileSha256"] == sha(HERE / "figure-captions.tex")
    for name, caption in provenance["captions"].items():
        assert rf"\newcommand{{\{name}}}{{{caption}}}" in (HERE / "figure-captions.tex").read_text()
    case = next(r for r in provenance["figures"] if r["file"] == "geometry-contrast.png")
    pair = next(p for p in primary if p["id"] == case["pair"])
    new_groups = {p["sourceGroup"] for p in bank["profiles"]
                  if p.get("introducedVersion") == "2.3" and p["sampling"] != "geometry-contrast"}
    assert pair["split"] == "heldout-source" and case["sourceGroup"] in new_groups
    assert case["evaluationCohort"] == "primary-matched"
    for item in provenance["figures"]:
        assert item["sha256"] == sha(HERE / "figures" / item["file"])
    semantic = json.loads((DATA / "semantic-validation.json").read_text())
    assert semantic["passed"] and semantic["bankHash"] == canonical_hash(bank)
    assert not any((DATA / name).exists() for name in ("browser-validation.json", "portal-validation.json")), \
        "Legacy UI evidence must be archived, not published as current validation"
    browser = json.loads((DATA / "workbench-validation.json").read_text())
    assert browser["status"] == "passed" and not browser["errors"] and len(browser["checks"]) >= 9
    assert browser["bankHash"] == canonical_hash(bank)
    for name, digest in browser["frontendFiles"].items():
        assert sha(ROOT / name) == digest, f"Frontend changed since browser validation: {name}"
    integration = json.loads((DATA / "workbench-integration.json").read_text())
    assert integration["status"] == "passed" and not integration["errors"]
    assert integration["bankHash"] == canonical_hash(bank)
    assert all(integration[key] for key in ("historicalCaseReplay", "studyIsolation", "staticSubpath",
                                          "staticMultiview", "activeAcquisition"))
    audit = json.loads((DATA / "upgrade-audit.json").read_text())
    assert audit["passed"] and audit["census"]["episodes"] == len(bank["episodes"])
    assert audit["bankHash"] == canonical_hash(bank)
    assert audit["census"]["probes"] == len(bank["probes"])
    geometry = json.loads((DATA / "geometry-probe-audit.json").read_text())
    assert geometry["bankHash"] == canonical_hash(bank)
    assert geometry["pairs"] == [p for p in bank["pairs"] if p["kind"] == "visual-geometry"]
    assert geometry["probes"] == [p for p in bank["probes"] if p["kind"] == "geometry-continuation"]
    assert geometry["episodes"] == sum(t["kind"] == "visual-geometry-context" for t in bank["episodes"])
    historical_case = historical_case_check()
    template = json.loads((HERE / "cvpr-template-provenance.json").read_text())
    for name, item in template["files"].items():
        assert sha(HERE / name) == item["sha256"]
    pdf = fitz.open(HERE / "paper.pdf")
    text = "\n".join(page.get_text() for page in pdf)
    assert "??" not in text and not any("\u4e00" <= c <= "\u9fff" for c in text)
    assert len(pdf) <= 8 and all(tuple(page.rect) == (0, 0, 612, 792) for page in pdf)
    numbers = set(re.findall(r"(?<![\d,])\d+(?:,\d{3})*(?![\d,])", text))
    assert all(f"{expected[name]:,}" in numbers or str(expected[name]) in numbers
               for name in ("EpisodeCount", "ProbeCount", "SourceCount", "CalibrationCount",
                            "DiscriminativeCount", "ProblemCount"))
    supplement = fitz.open(HERE / "supplement.pdf")
    supplement_text = "\n".join(page.get_text() for page in supplement)
    assert "??" not in supplement_text and not any("\u4e00" <= c <= "\u9fff" for c in supplement_text)
    assert r"\usepackage[margin" not in (HERE / "paper.tex").read_text()
    return {"bankHash": canonical_hash(bank), "controlRecords": len(records),
            "paperPages": len(pdf), "supplementPages": len(supplement), "counts": stats["counts"],
            "claimDataAgreement": True, "figureHashesVerified": True,
            "semanticEvidencePassed": True, "browserEvidencePassed": True,
            "workbenchIntegrationPassed": True, "nativeImagesVerified": True,
            "historicalModelCase": historical_case, "officialTemplateHashesVerified": True,
            "sourceQuestionAuditPassed": True, "matchedInventoryControlsPassed": True,
            "primaryMatchedPairs": len(primary),
            "matchedSourceGroups": sources["matchedSourceGroups"],
            "matchedHeldoutSources": sources["matchedHeldoutSources"]}


def release_paths():
    ignored = {MANIFEST, REPORT}
    return sorted(p for p in HERE.rglob("*") if p.is_file() and p not in ignored
                  and HERE / "release" not in p.parents
                  and not {"build-fragments", "geometry-fragments"}.intersection(p.parts)
                  and "__pycache__" not in p.parts and not p.name.startswith(".")
                  and p.suffix not in (".pyc", ".aux", ".log", ".out", ".synctex", ".bbl", ".blg", ".brf"))


def dependencies():
    files = [HERE.parent / "brickplan-v1.2" / n for n in ("engine.py", "visual.py", "raster.c")]
    files += [HERE.parent / "brickplan-v1/render_assets.py", ROOT / "package.json", ROOT / "package-lock.json"]
    files += [ROOT / "node_modules/three" / n for n in ("build/three.module.min.js", "build/three.core.min.js", "LICENSE")]
    for folder in (ROOT / "web/brickplan", ROOT / "deliverables/brickplan-paper"):
        files += [p for p in folder.rglob("*") if p.is_file() and "node_modules" not in p.parts
                  and "__pycache__" not in p.parts
                  and not any(part.startswith(".") for part in p.relative_to(folder).parts)]
    provenance = json.loads((DATA / "render-provenance.json").read_text())
    library = ROOT / "assets-source/ldraw-library/locked"
    for relative, digest in provenance["files"].items():
        path = library / relative
        assert sha(path) == digest, f"Locked source mismatch: {relative}"
        files.append(path)
    source_audit = json.loads((DATA / "source-question-audit.json").read_text())
    for model in sorted({r["modelId"] for r in source_audit["sources"]}):
        folder = ROOT / "web/public/models" / model
        files.extend((folder / "manifest.json", folder / "provenance.json"))
        if model.startswith("v23-"):
            files.append(folder / "model.packed.mpd")
        record = json.loads((folder / "provenance.json").read_text())
        dependencies = list(record.get("dependencyFiles", []))
        if record.get("source"):
            dependencies.append(record["source"])
        for dependency in dependencies:
            path = ROOT / dependency["path"]
            assert sha(path) == dependency["sha256"], f"Source dependency mismatch: {path}"
            files.append(path)
    return {str(p.relative_to(ROOT)): sha(p) for p in files}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("command", choices=("prepare", "freeze", "check"))
    args = parser.parse_args()
    if args.command in ("prepare", "freeze"):
        prepare_evidence()
    if args.command == "prepare":
        print("Installed current-bank frontend evidence; inherited 2.1 UI reports archived.")
        return
    if args.command == "freeze":
        snapshot = DATA / "predecessor-hashes.json"
        prior = json.loads(snapshot.read_text())
        older = ARCHIVE / "v2-predecessor-hashes.json"
        if older.exists():
            prior["brickplan-v2"] = json.loads(older.read_text())
        assert prior.get("brickplan-v2"), "Missing frozen version-2 predecessor"
        prior["brickplan-v2.1"] = v21_snapshot()
        write_json(snapshot, prior)
    prior = predecessor_check()
    claims = claim_check()
    claims["overleafSnapshot"] = overleaf_check()
    files = {str(p.relative_to(HERE)): sha(p) for p in release_paths()}
    if args.command == "freeze":
        write_json(MANIFEST, {
            "schema": "brickplan-release/2.3", "files": files, "dependencies": dependencies(),
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
