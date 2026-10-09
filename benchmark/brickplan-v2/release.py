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

from bank import DATA, HERE, ROOT, task_bank, write_json
from controls import summarize
from mission import canonical_hash

MANIFEST = DATA / "release.json"
REPORT = HERE / "release-check.json"
ARCHIVE = ROOT / "tem/research/20261008-brickplan-overhaul"


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
    browser = json.loads((DATA / "browser-validation.json").read_text())
    assert browser["status"] == "passed" and not browser["errors"] and len(browser["checks"]) == 10
    pdf = fitz.open(HERE / "paper.pdf")
    text = "\n".join(page.get_text() for page in pdf)
    assert "??" not in text and not any("\u4e00" <= c <= "\u9fff" for c in text)
    assert all(token in text for token in ("1,802,728", "2,555", "75,454", "Not evaluated", "98", "69"))
    return {"bankHash": canonical_hash(bank), "controlRecords": len(records),
            "paperPages": len(pdf), "counts": expected,
            "claimDataAgreement": True, "figureHashesVerified": True,
            "semanticEvidencePassed": True, "browserEvidencePassed": True}


def release_paths():
    ignored = {MANIFEST, REPORT}
    return sorted(p for p in HERE.rglob("*") if p.is_file() and p not in ignored
                  and "__pycache__" not in p.parts and not p.name.startswith(".")
                  and p.suffix not in (".pyc", ".aux", ".log", ".out", ".synctex"))


def dependencies():
    files = [HERE.parent / "brickplan-v1.2" / n for n in ("engine.py", "visual.py", "raster.c")]
    files += [HERE.parent / "brickplan-v1/render_assets.py", ROOT / "package.json", ROOT / "package-lock.json"]
    files += [ROOT / "node_modules/three" / n for n in ("build/three.module.min.js", "build/three.core.min.js", "LICENSE")]
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
        if not snapshot.exists():
            snapshot.write_bytes((ARCHIVE / "predecessor-hashes.json").read_bytes())
        browser = DATA / "browser-validation.json"
        if not browser.exists():
            browser.write_bytes((ROOT / "tem/brickplan-v2/validation/browser-validation.json").read_bytes())
    prior = predecessor_check()
    claims = claim_check()
    files = {str(p.relative_to(HERE)): sha(p) for p in release_paths()}
    if args.command == "freeze":
        write_json(MANIFEST, {
            "schema": "brickplan-release/2.0", "files": files, "dependencies": dependencies(),
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
