"""Behavioral fixtures for evidence interpretation, not benchmark measurements."""
from copy import deepcopy
import unittest
from common import DATA, load, save, VERSION
from evidence_adaptation import normalize, pair_rows, summarize, analyze
from estimators import estimate, paired_difference

FIX = load(DATA / "receipt-test-fixtures.json")["outputs"]


def spec(a, b, name="visual-mismatch", truth="fact-change"):
    return {"id": name, "a": a["condition"], "b": b["condition"], "truth_policy": truth,
            "taskIds": a["task_ids"]}


def compare(a="visual_A", b="visual_B"):
    x, y = FIX[a], FIX[b]
    return pair_rows(x, y, spec(x, y))


class AdaptationTests(unittest.TestCase):
    def test_both_correct_zero_delta(self):
        out = summarize(compare(), "fact-change", 200)
        self.assertEqual(out["metrics"]["delta_A_minus_B"]["micro"], 0)
        self.assertEqual(out["paired_both_correct"]["micro"], 1)
        self.assertEqual(out["new_evidence_accuracy"]["micro"], 1)

    def test_old_answer(self):
        out = summarize(compare(b="visual_old"), "fact-change", 200)
        self.assertEqual(out["B_categories"]["old-answer"], 2)
        self.assertEqual(out["paired_both_correct"]["micro"], 0)

    def test_other_legal_answer(self):
        a, b = deepcopy(FIX["visual_A"]), deepcopy(FIX["visual_B"])
        for x, y in zip(a["rows"], b["rows"]):
            other = next(o["id"] for o in y["payload"]["options"]
                         if o["id"] not in [x["gold"]["choiceId"], y["gold"]["choiceId"]])
            y.update(answer={"choiceId": other}, success=0, original_gold_success=0, failure_reason="incorrect")
        out = summarize(pair_rows(a, b, spec(a, b)), "fact-change", 200)
        self.assertEqual(out["B_categories"]["other-legal-answer"], 2)

    def test_all_invalid(self):
        out = summarize(compare(b="visual_invalid"), "fact-change", 200)
        self.assertEqual(out["B_categories"]["invalid-or-missing"], 2)
        self.assertEqual(sum(out["B_categories"].values()), out["denominator"])

    def test_zero_condition_denominator(self):
        a, b = deepcopy(FIX["visual_A"]), FIX["visual_B"]
        for r in a["rows"]:
            r.update(answer=None, success=0, original_gold_success=0, failure_reason="invalid-json")
        out = summarize(pair_rows(a, b, spec(a, b)), "fact-change", 200)
        self.assertIsNone(out["adaptation_given_A_correct"]["value"])
        self.assertEqual(out["adaptation_given_A_correct"]["denominator"], 0)
        self.assertEqual(out["denominator"], 2)

    def test_missing_B_not_intersection(self):
        out = summarize(compare(b="visual_missing"), "fact-change", 200)
        self.assertEqual(out["denominator"], 2)
        self.assertEqual(out["paired_both_correct"]["micro"], .5)
        self.assertEqual(out["B_categories"]["invalid-or-missing"], 1)
        a, b = FIX["visual_A"], deepcopy(FIX["visual_B"])
        b["rows"].pop()
        with self.assertRaisesRegex(ValueError, "universe"):
            pair_rows(a, b, spec(a, b))

    def test_provenance_rejected(self):
        a = FIX["visual_A"]
        for key in ["analysis_version", "model_revision", "adapter_hash", "prompt_hash", "dataset_hash", "code_hashes"]:
            b = deepcopy(FIX["visual_B"])
            b[key] = "mismatched"
            with self.subTest(key=key), self.assertRaisesRegex(ValueError, "provenance"):
                pair_rows(a, b, spec(a, b))

    def test_duplicate_pairs_rejected(self):
        a, b = FIX["visual_A"], deepcopy(FIX["visual_B"])
        b["rows"].append(b["rows"][0])
        with self.assertRaisesRegex(ValueError, "Duplicate"):
            pair_rows(a, b, spec(a, b))
        s = spec(a, FIX["visual_B"]); s["taskIds"] = [s["taskIds"][0]] * 2
        with self.assertRaisesRegex(ValueError, "Duplicate"):
            pair_rows(a, FIX["visual_B"], s)

    def test_graph_both_and_baseline_gap(self):
        a, b = FIX["graph_A"], FIX["graph_B"]
        result = analyze(a, b, spec(a, b, "edge-causal-control"), 200)
        self.assertEqual(result["summary"]["paired_both_correct"]["micro"], 1)
        removal = result["summary"]["graph_removal"]["model_minus_baseline_both_correct"]
        self.assertEqual(removal["node-only"]["micro"], 1)
        self.assertEqual(removal["BFS"]["micro"], 0)

    def test_set_order_and_duplicates(self):
        payload = next(r["payload"] for r in FIX["graph_A"]["rows"] if r["family"] == "neighbors")
        ids = [o["id"] for o in payload["options"][:2]]
        self.assertEqual(normalize({"choiceIds": ids}, payload), normalize({"choiceIds": ids[::-1]}, payload))
        self.assertIsNone(normalize({"choiceIds": ids + ids[:1]}, payload))

    def test_correct_and_wrong_consistency(self):
        a, b = deepcopy(FIX["visual_A"]), deepcopy(FIX["visual_id"])
        s = spec(a, b, "label-binding", "semantic-invariance")
        rows = pair_rows(a, b, s)
        self.assertTrue(all(r["transition"] == "both-correct" for r in rows))
        for x, y in zip(a["rows"], b["rows"]):
            wrong = next(o["id"] for o in x["payload"]["options"] if o["id"] != x["gold"]["choiceId"])
            for r in [x, y]:
                r.update(answer={"choiceId": wrong}, success=0, original_gold_success=0, failure_reason="incorrect")
        rows = pair_rows(a, b, s)
        self.assertTrue(all(r["transition"] == "both-wrong-same-legal-semantics" for r in rows))
        out = summarize(rows, "semantic-invariance", 200)
        self.assertEqual(out["metrics"]["same_legal_output"]["micro"], 1)
        self.assertEqual(out["metrics"]["both_correct"]["micro"], 0)

    def test_parent_source_weighting(self):
        rows = [{"parent_task_id": "p1", "source_id": "s1", "a": 1, "b": 0}] * 8
        rows += [{"parent_task_id": "p2", "source_id": "s1", "a": 0, "b": 1},
                 {"parent_task_id": "p3", "source_id": "s2", "a": 0, "b": 1}]
        out = estimate(rows, "a", 200)
        self.assertEqual(out["micro"], .8)
        self.assertEqual(out["source_macro"], .25)
        self.assertEqual(out["parents"], 3)
        self.assertEqual(out["sources"], 2)
        self.assertEqual(paired_difference(rows, "a", "b", 200)["source_macro"], -.5)

    def test_invalid_outputs_do_not_count_as_stability(self):
        a, b = deepcopy(FIX["visual_A"]), deepcopy(FIX["visual_id"])
        for r in a["rows"] + b["rows"]:
            r.update(answer=None, success=0, original_gold_success=0, failure_reason="invalid-json")
        rows = pair_rows(a, b, spec(a, b, "label-binding", "semantic-invariance"))
        self.assertTrue(all(r["transition"] == "both-wrong-different-or-invalid" for r in rows))
        self.assertTrue(all(r["same_legal_output"] == 0 for r in rows))


if __name__ == "__main__":
    result = unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.loadTestsFromTestCase(AdaptationTests))
    save(DATA / "adaptation-test-report.json", {
        "analysis_version": VERSION, "evidence_kind": "synthetic-validation-only",
        "tests": result.testsRun, "failures": len(result.failures), "errors": len(result.errors),
        "passed": result.wasSuccessful(), "benchmark_model_results": None})
    raise SystemExit(not result.wasSuccessful())
