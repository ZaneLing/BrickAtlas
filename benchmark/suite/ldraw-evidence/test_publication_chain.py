"""Run while synthetic raw receipts still exist; exercise numeric AND null states."""
from copy import deepcopy
from pathlib import Path
import sys
import tempfile

from common import ROOT, DATA, VERSION, save
from evidence_adaptation import validate_run
from reporting import selection, new_index, register, verify_index, publish, GROUPS

directory = Path(sys.argv[1])
run = validate_run(directory, allow_synthetic=True)
sel = selection()
assert [len(sel["groups"][k]) for k in GROUPS] == [140, 146, 290, 41]
assert len(set(sum(sel["groups"].values(), []))) == len(sel["all_task_ids"]) == 617
# The test has its own explicit 11-item selection, never the real experiment index.
sel["conditions"]["standard"] = run["task_ids"]
index = new_index(sel)
index["evidence_kind"] = "synthetic-validation-only"
with tempfile.TemporaryDirectory(prefix="publication-fixture-", dir=DATA) as tmp:
    out = Path(tmp)
    assert verify_index(index, sel)["complete"] == 0
    publish(index, sel, out / "null-tables", allow_synthetic=True)
    assert "--" in (out / "null-tables/core-visual.tex").read_text()
    try:
        register(index, sel, directory, out / "rejected")
        raise AssertionError("Synthetic run leaked into real ingestion")
    except Exception as exc:
        assert not isinstance(exc, AssertionError)
    register(index, sel, directory, out / "results", allow_synthetic=True)
    result = verify_index(index, sel, allow_synthetic=True)
    assert result["complete"] == 1
    publish(index, sel, out / "numeric-tables", allow_synthetic=True)
    assert "100.00 [100.00, 100.00]" in (out / "numeric-tables/core-visual.tex").read_text()
    complete = next(e for e in index["entries"] if e["status"] == "complete")
    for mutate in ["number", "denominator", "null", "duplicate", "artifact"]:
        bad = deepcopy(index)
        entry = next(e for e in bad["entries"] if e["status"] == "complete")
        if mutate == "number":
            entry["metrics"]["all_task_descriptive"]["successes"] = 0
        elif mutate == "denominator":
            entry["expected_task_ids"] = entry["expected_task_ids"][:-1]
        elif mutate == "null":
            next(e for e in bad["entries"] if e["status"] == "not-run")["metrics"] = {"accuracy": 0}
        elif mutate == "duplicate":
            bad["entries"].append(bad["entries"][0])
        else:
            entry["analysis"]["sha256"] = "changed"
        try:
            verify_index(bad, sel, allow_synthetic=True)
            raise AssertionError(f"Accepted {mutate} tampering")
        except ValueError:
            pass
    save(DATA / "publication-test-report.json", {
        "analysis_version": VERSION, "evidence_kind": "synthetic-validation-only", "passed": True,
        "tests": ["all four roles and family denominators", "null renders as --", "actual receipts validate",
                  "all 11 families score through frozen executable contract", "completed numeric table generated",
                  "number/denominator/null/duplicate/hash tampering rejected", "synthetic production ingestion rejected"],
        "fixture_items": len(run["rows"]), "real_model_results": None})
print("PASS: raw receipts -> selection -> immutable index -> numeric TeX -> independent verification")
