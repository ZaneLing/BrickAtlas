#!/usr/bin/env python3
"""Final cross-artifact verification of the separately sealed evidence revision."""
import importlib.util
import json
from pathlib import Path

from common import DATA, ROOT, VERSION, load, save, sha
from reporting import selection, verify_index


def main():
    spec = importlib.util.spec_from_file_location("freeze", Path(__file__).with_name("freeze.py"))
    freeze = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(freeze)
    preserved = freeze.verify()
    manifest = load(DATA / "delivery-manifest.json")
    assert manifest["analysis_version"] == VERSION
    assert sha(DATA / "baseline-lock.json") == manifest["baseline_lock_sha256"]
    for row in manifest["files"]:
        path = ROOT / row["path"]
        assert path.stat().st_size == row["bytes"] and sha(path) == row["sha256"], row["path"]
    paper = ROOT / "benchmark/paper/evidence-v1"
    pdf = load(paper / "pdf-verification.json")
    visual = load(paper / "visual-inspection.json")
    assert pdf["status"] == visual["status"] == "passed"
    for name in ["main", "supplement"]:
        expected = sha(paper / f"{name}.pdf")
        assert expected == pdf["documents"][name]["sha256"] == visual["documents"][name]["sha256"]
        assert len(pdf["documents"][name]["pages"]) == visual["documents"][name]["pages"]
    compile_result = load(paper / "archive-compile-verification.json")
    assert compile_result["status"] == "passed"
    assert sha(paper / "paper-source.zip") == compile_result["archive_sha256"]
    for name, digest in load(paper / "package-verification.json")["web_copies"].items():
        assert sha(ROOT / "public/benchmark/evidence-v1" / name) == digest
    assert "- [ ]" not in (DATA / "CHECKLIST.md").read_text()
    for i in range(1, 6):
        assert (DATA / f"ISSUE-{i}-REPORT.md").exists()
    for name in ["adaptation-test-report.json", "wire-qa-test-report.json", "publication-test-report.json"]:
        assert load(DATA / name)["passed"], name
    for name in ["node-prior-audit.json", "graph-parity-verification.json",
                 "matched-graphs-v1/independent-verification.json", "literature/verification.json"]:
        assert load(DATA / name)["status"] == "passed", name
    fixtures = load(DATA / "receipt-test-fixtures.json")
    assert fixtures["fixture_only"] and len(fixtures["outputs"]) == 11
    result_state = verify_index(load(DATA / "results-index.json"), selection())
    qa = load(DATA / "qa/wrong-image-export-v1/qa-template.json")
    assert len(qa["observations"]) == 140
    assert all(r["decision"] == "pending" for r in qa["observations"])
    audit = load(DATA / "request-audits/gpt41-wrong-image/manifest.json")
    assert audit["calls"] == 0
    result = {
        "analysis_version": VERSION, "status": "passed", "preservation": preserved,
        "sealed_new_files": len(manifest["files"]),
        "manifest_sha256": sha(DATA / "delivery-manifest.json"),
        "original_questions": pdf["original_question_coverage"],
        "pdf_pages": {n: len(d["pages"]) for n, d in pdf["documents"].items()},
        "result_index": result_state, "receipt_fixtures": 11,
        "adaptation_tests": load(DATA / "adaptation-test-report.json")["tests"],
        "fresh_source_archive_compile": "passed",
        "human_status": "140 visual + 111 other flagged items + 573 physical candidates pending",
        "learned_model_conclusions": "not available",
        "browser_download_boundary": load(DATA / "browser-verification.json")["os_download_persistence"],
        "scope": "All five implementation/reporting issues accepted; no invented human or model evidence."}
    save(DATA / "final-validation.json", result)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
