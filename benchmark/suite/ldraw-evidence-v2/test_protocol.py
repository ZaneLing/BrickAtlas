"""Regression tests use explicitly synthetic judgments, never human evidence."""
import copy
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from common import DATA, ROOT, digest, load, save
import qa
import run


class ProtocolTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.assignment = DATA / "qa/initial"
        cls.mapping = load(cls.assignment / "private-mapping.json")
        cls.manifest, cls.obs, cls.wires = qa.assets()
        cls.adapter = load(DATA / "adapter.example.json")
        cls.feedback = []
        for i, slot in enumerate(["reviewer-1", "reviewer-2"]):
            assignment = cls.mapping["slots"][slot]
            reviews = []
            for key, item in assignment["items"].items():
                o = cls.obs[item["observation_id"]]
                reviews.append({"review_id": key, "wire_observation_sha256": item["wire_observation_sha256"],
                    "reviewer": "fixture-person-" + str(i), "author_kind": "synthetic-fixture",
                    "timestamp": "2026-09-19T01:00:00+00:00", "decision": "decidable",
                    "visual_choice": o["gold"]["choiceId"], "reason_code": "none", "reason": "Software fixture only.",
                    "checks": {k: True for k in qa.CHECKS},
                    "native_size_attestation": True, "independence_attestation": True})
            cls.feedback.append({"slot": slot, "queue_sha256": assignment["queue_sha256"],
                "evidence_kind": "synthetic-fixture", "reviewer": "fixture-person-" + str(i), "reviews": reviews})

    def combine(self, feedback=None, adjudications=None):
        with tempfile.TemporaryDirectory() as d:
            files = []
            for i, f in enumerate(self.feedback if feedback is None else feedback):
                file = Path(d) / f"feedback-{i}.json"; save(file, f); files.append(file)
            ap = Path(d) / "adjudication.json" if adjudications else None
            if ap:
                save(ap, {"evidence_kind": "synthetic-fixture", "adjudications": adjudications})
            return qa.combine(self.assignment, files, ap, fixture=True)

    def find_review(self, feedback, oid):
        return next(r for r in feedback["reviews"]
                    if self.mapping["slots"][feedback["slot"]]["items"][r["review_id"]]["observation_id"] == oid)

    def test_complete_two_sided_universe(self):
        result = self.combine()
        self.assertEqual(result["primary_final"], 280)
        self.assertEqual(result["raw_review_count"], 694)
        self.assertEqual(result["qa_comparable_pairs"], 140)
        self.assertEqual(result["agreement"]["decision"]["raw_agreement"], 1)
        self.assertIsNone(result["agreement"]["decision"]["cohen_kappa"])

    def test_only_b_reviews_cannot_qualify_pairs(self):
        feedback = copy.deepcopy(self.feedback)
        for f in feedback:
            f["reviews"] = [r for r in f["reviews"] if self.obs[
                self.mapping["slots"][f["slot"]]["items"][r["review_id"]]["observation_id"]]["arm"] == "B"]
        result = self.combine(feedback)
        self.assertEqual(result["primary_final"], 140)
        self.assertEqual(result["qa_comparable_pairs"], 0)
        self.assertFalse(result["primary_ready_for_inference"])

    def test_one_reviewer_is_insufficient(self):
        self.assertEqual(self.combine(self.feedback[:1])["primary_final"], 0)

    def test_same_person_two_slots_rejected(self):
        feedback = copy.deepcopy(self.feedback)
        feedback[1]["reviewer"] = feedback[0]["reviewer"]
        for r in feedback[1]["reviews"]:
            r["reviewer"] = feedback[0]["reviewer"]
        with self.assertRaises(AssertionError):
            self.combine(feedback)

    def test_duplicate_review_rejected(self):
        feedback = copy.deepcopy(self.feedback)
        feedback[0]["reviews"].append(feedback[0]["reviews"][0])
        with self.assertRaises(AssertionError):
            self.combine(feedback)

    def test_changed_wire_rejected(self):
        feedback = copy.deepcopy(self.feedback)
        feedback[0]["reviews"][0]["wire_observation_sha256"] = "0" * 64
        with self.assertRaises(AssertionError):
            self.combine(feedback)

    def test_disagreement_and_third_person_adjudication(self):
        feedback = copy.deepcopy(self.feedback)
        oid = self.manifest["pairs"][0]["a"]
        first = self.find_review(feedback[0], oid)
        second = self.find_review(feedback[1], oid)
        second.update(decision="ambiguous", reason_code="multiple_visual_answers", visual_choice=None)
        second["checks"]["unique_visual_option"] = False
        result = self.combine(feedback)
        self.assertEqual(len(result["adjudication_queue"]), 1)
        self.assertEqual(result["primary_final"], 279)
        adjudication = {**first, "observation_id": oid, "reviewer": "fixture-third-person",
                        "review_hashes": [digest(first), digest(second)]}
        final = self.combine(feedback, [adjudication])
        row = next(r for r in final["rows"] if r["observation_id"] == oid)
        self.assertEqual(len(row["reviews"]), 2)
        self.assertEqual(row["reviews"][1]["decision"], "ambiguous")
        self.assertEqual(row["final_decision"], "decidable")
        adjudication["reviewer"] = first["reviewer"]
        with self.assertRaises(AssertionError):
            self.combine(feedback, [adjudication])

    def test_same_decision_different_choice_requires_adjudication(self):
        feedback = copy.deepcopy(self.feedback)
        oid = self.manifest["pairs"][0]["a"]
        r = self.find_review(feedback[1], oid)
        r["visual_choice"] = next(o["id"] for o in self.obs[oid]["payload"]["options"] if o["id"] != r["visual_choice"])
        result = self.combine(feedback)
        self.assertEqual(result["primary_final"], 279)
        self.assertEqual(len(result["adjudication_queue"]), 1)

    def test_human_oracle_conflict_blocks_inference(self):
        feedback = copy.deepcopy(self.feedback)
        oid = self.manifest["pairs"][0]["a"]
        wrong = next(o["id"] for o in self.obs[oid]["payload"]["options"] if o["id"] != self.obs[oid]["gold"]["choiceId"])
        for f in feedback:
            self.find_review(f, oid)["visual_choice"] = wrong
        result = self.combine(feedback)
        row = next(r for r in result["rows"] if r["observation_id"] == oid)
        self.assertEqual(row["final_decision"], "pending")
        self.assertIn("human-oracle-conflict", row["final_reason"])

    def test_synthetic_cannot_pass_human_gate(self):
        with tempfile.TemporaryDirectory() as d:
            file = Path(d) / "fixture.json"; save(file, self.combine())
            with self.assertRaises(AssertionError):
                qa.verify_final(file)

    def test_kappa_matches_known_case(self):
        pairs = [[{"d": a}, {"d": b}] for a, b in [("a", "a"), ("a", "b"), ("b", "b"), ("b", "a")]]
        report = qa.agreement(pairs, lambda r: r["d"])
        self.assertEqual(report["raw_agreement"], .5)
        self.assertEqual(report["cohen_kappa"], 0)

    def test_raw_receipt_strict_parsing_and_revision(self):
        def receipt(output):
            return {"http_status": 200, "raw_response": json.dumps({
                "model": self.adapter["response_model"], "choices": [{"message": {"content": output}}]})}
        self.assertTrue(run.parse_receipt(receipt('{"choiceId":"A"}'), ["A"], self.adapter)["valid_format"])
        for text in ['{"choiceId":"A","choiceId":"B"}', '{"choiceId":"A","explanation":"x"}',
                     '```json\n{"choiceId":"A"}\n```', '{"choiceId":"Z"}', '{"choiceId":null}']:
            self.assertFalse(run.parse_receipt(receipt(text), ["A"], self.adapter)["valid_format"])
        bad = receipt('{"choiceId":"A"}')
        bad["raw_response"] = bad["raw_response"].replace(self.adapter["response_model"], "other-model")
        with self.assertRaises(AssertionError):
            run.parse_receipt(bad, ["A"], self.adapter)
        self.assertEqual(run.parse_receipt(None, ["A"], self.adapter)["failure_reason"], "missing-receipt")

    def test_offline_wire_and_request_tamper(self):
        with tempfile.TemporaryDirectory() as d:
            path = Path(d) / "dry-run"
            run.run(path, self.adapter, role="primary")
            result = run.verify(path)
            self.assertEqual(len(result["rows"]), 280)
            self.assertTrue(all(r["success"] is None for r in result["rows"]))
            request = next((path / "requests").glob("*.json"))
            body = load(request); body["messages"][1]["content"][0]["text"] += " changed"
            save(request, body)
            with self.assertRaises(AssertionError):
                run.verify(path)

    def test_live_pending_gate_fails_before_network_or_directory_creation(self):
        adapter = {**self.adapter, "provider": "test", "model": "pinned", "model_revision": "pinned",
                   "api_revision": "2026-09", "response_model": "pinned", "endpoint": "https://localhost/v1"}
        with tempfile.TemporaryDirectory() as d:
            qa_file = Path(d) / "pending.json"
            save(qa_file, qa.combine(self.assignment, []))
            path = Path(d) / "must-not-exist"
            with patch("urllib.request.urlopen") as network:
                with self.assertRaises(AssertionError):
                    run.run(path, adapter, str(qa_file), live=True)
                network.assert_not_called()
            self.assertFalse(path.exists())


if __name__ == "__main__":
    unittest.main(verbosity=2)
