"""Exact-byte QA eligibility tests; no human judgments are fabricated."""
from copy import deepcopy
from common import DATA, VERSION, load, save
from wire_qa import template, validate_feedback, qualify_pairs
from evidence_adaptation import analyze

fixtures = load(DATA / "receipt-test-fixtures.json")["outputs"]
a, b = fixtures["visual_A"], fixtures["visual_B"]
qa = template(a)
assert all(r["decision"] == "pending" for r in qa["observations"])
assert "gold" not in str(qa) and "answer" not in str(qa)
validate_feedback(qa, qa)
for field in ["image_hashes", "request_hash", "wire_dimensions"]:
    bad = deepcopy(qa)
    bad["observations"][0][field] = "different"
    try:
        validate_feedback(qa, bad)
        raise AssertionError(field)
    except ValueError:
        pass
bad = deepcopy(qa); bad["observations"].append(bad["observations"][0])
try:
    validate_feedback(qa, bad)
    raise AssertionError("Duplicate QA accepted")
except ValueError:
    pass
bad = deepcopy(qa); bad["observations"][0]["decision"] = "decidable"
try:
    validate_feedback(qa, bad)
    raise AssertionError("Unattested judgment accepted")
except ValueError:
    pass
analysis = analyze(a, b, {"id": "visual-mismatch", "a": a["condition"], "b": b["condition"],
                        "truth_policy": "fact-change", "taskIds": a["task_ids"]}, 200)
qualified = qualify_pairs(analysis, [validate_feedback(qa, qa)])
assert qualified["full_pair_denominator"] == 2
assert qualified["QA_comparable_pairs"] == 0
assert qualified["QA_comparable_result"] is None
assert qualified["full_result_preserved"] == analysis["summary"]
save(DATA / "wire-qa-test-report.json", {
    "analysis_version": VERSION, "passed": True, "evidence_kind": "synthetic-validation-only",
    "checks": ["no golds/model outputs in QA", "exact image/request/dimension binding",
               "duplicate rejection", "native-size blinded reviewer attestation",
               "pending QA is not certified", "full denominator and original results preserved"],
    "human_results": None})
print("PASS: exact-wire QA contract; no visual item silently excluded or certified")
