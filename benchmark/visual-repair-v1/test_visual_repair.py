"""Synthetic/adversarial fixtures only; never write empirical receipt artifacts."""
import copy
import json
import unittest

from baselines import image_bindings
from common import HERE, ROOT, digest, read
from evaluate import evaluate, solve
from portable import check_settings
from qualification import FLAGS, validate as validate_qualification
from study import analyze, checked_packet, envelope, load_manifest, packet, validate_receipts


def fixture():
    return {"graph": {"nodes": ["a", "b", "x", "y", "c", "z", "d", "e"],
                      "edges": [["a", "x"], ["x", "c"], ["a", "y"], ["y", "c"], ["c", "b"]]},
            "missing": ["x", "y", "z"], "fixed_terminals": ["a", "b"],
            "candidate_ids": ["c", "z", "d", "e"], "budget": 1, "cost_per_vertex": 1}


class SemanticTests(unittest.TestCase):
    def setUp(self):
        self.data = fixture()
        self.answer = solve(self.data, "c")

    def test_independent_alternative_optima(self):
        self.assertEqual(self.answer["minimum_cost"], 1)
        self.assertEqual({tuple(s["restored"]) for s in self.answer["solutions"]}, {("x",), ("y",)})
        self.assertTrue(evaluate(self.data, "c", self.answer)["repair_exact"])

    def test_arbitrary_solution_and_component_order(self):
        self.answer["solutions"].reverse()
        for sol in self.answer["solutions"]:
            sol["restored"].reverse()
            sol["component_sizes"].reverse()
        self.assertTrue(evaluate(self.data, "c", json.dumps(self.answer))["repair_exact"])

    def test_missing_optimum(self):
        self.answer["solutions"].pop()
        r = evaluate(self.data, "c", self.answer)
        self.assertTrue(r["valid"])
        self.assertFalse(r["complete"])
        self.assertFalse(r["repair_exact"])

    def test_duplicate_solution(self):
        self.answer["solutions"].append(self.answer["solutions"][0])
        self.assertFalse(evaluate(self.data, "c", self.answer)["valid"])

    def test_duplicate_vertex(self):
        self.answer["solutions"][0]["restored"] *= 2
        self.assertFalse(evaluate(self.data, "c", self.answer)["valid"])

    def test_restore_unavailable_membership(self):
        self.answer["solutions"][0]["restored"] = ["a"]
        self.assertFalse(evaluate(self.data, "c", self.answer)["valid"])

    def test_infeasible(self):
        self.answer["solutions"][0]["restored"] = ["z"]
        self.assertFalse(evaluate(self.data, "c", self.answer)["feasible"])

    def test_feasible_nonminimal(self):
        self.answer["solutions"] = [{"restored": ["x", "y"], "component_sizes": [5, 1, 1]}]
        self.answer["minimum_cost"] = 2
        r = evaluate(self.data, "c", self.answer)
        self.assertTrue(r["feasible"])
        self.assertFalse(r["minimal"])

    def test_wrong_component_sizes(self):
        self.answer["solutions"][0]["component_sizes"] = [100]
        self.assertFalse(evaluate(self.data, "c", self.answer)["component_results_correct"])

    def test_budget_mismatch(self):
        self.answer["budget_sufficient"] = False
        self.assertIn("wrong_budget", evaluate(self.data, "c", self.answer)["errors"])

    def test_cost_boolean_rejected(self):
        self.answer["minimum_cost"] = True
        self.assertFalse(evaluate(self.data, "c", self.answer)["valid"])

    def test_unknown_binding(self):
        self.answer["bound_terminal"] = "bad"
        self.assertFalse(evaluate(self.data, "c", self.answer)["valid"])

    def test_wrong_valid_binding(self):
        r = evaluate(self.data, "z", self.answer)
        self.assertTrue(r["valid"])
        self.assertFalse(r["repair_exact"])
        self.assertFalse(r["binding_correct"])

    def test_atomic_does_not_receive_repair_credit(self):
        r = evaluate(self.data, "c", {"bound_terminal": "c"}, atomic=True)
        self.assertTrue(r["binding_correct"])
        self.assertFalse(r["repair_exact"])

    def test_malformed_outputs(self):
        for raw in (None, "", "not json", "[]", "```json\n{}\n```", '{"bound_terminal":"c","bound_terminal":"z"}'):
            with self.subTest(raw=raw):
                self.assertFalse(evaluate(self.data, "c", raw)["valid"])

    def test_nonfinite_and_extra_fields(self):
        self.assertFalse(evaluate(self.data, "c", '{"minimum_cost":NaN}')["valid"])
        self.answer["explanation"] = "unexpected field"
        self.assertFalse(evaluate(self.data, "c", self.answer)["valid"])


class StudyTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.manifest = load_manifest()
        cls.config = cls.manifest["configurations"][0]
        cls.obs = next(o for o in cls.manifest["observations"] if o["condition"] == cls.config["condition"])
        cls.tasks = {t["id"]: t for t in read(HERE / "public.json")["tasks"]}
        cls.gold = {t["id"]: t["answer"] for t in read(HERE / "gold.json")["tasks"]}

    def receipt(self):
        # Ephemeral fixture only, with no write to any released response path.
        return envelope(self.manifest, self.config, self.obs, self.gold[self.obs["task_id"]])

    def test_manifest_denominator_and_modes(self):
        self.assertEqual(len(self.manifest["configurations"]), 15)
        self.assertEqual(self.manifest["planned_runs"], len(self.tasks) * 15)
        self.assertEqual(set(self.manifest["conditions"]), {"multimodal", "no_image", "oracle_binding", "atomic_binding"})

    def test_synthetic_receipt_rejected(self):
        row = self.receipt()
        row["synthetic"] = True
        with self.assertRaises(ValueError):
            validate_receipts(self.manifest, [row])

    def test_off_version_revision_settings_and_input_rejected(self):
        for key in ("version", "revision", "settings_sha256", "input_sha256", "study_lock_sha256"):
            row = self.receipt()
            row[key] = "not-the-frozen-value"
            with self.subTest(key=key), self.assertRaises(ValueError):
                validate_receipts(self.manifest, [row])

    def test_duplicate_receipts_rejected(self):
        row = self.receipt()
        with self.assertRaises(ValueError):
            validate_receipts(self.manifest, [row, row])

    def test_missing_and_malformed_stay_in_full_denominator(self):
        row = self.receipt()
        row["response"] = "malformed"
        report = analyze([row], self.manifest, write_output=False)
        self.assertEqual(report["planned_count"], len(self.tasks) * 15)
        metrics = report["configurations"][0]["all"]
        self.assertEqual(metrics["planned_count"], len(self.tasks))
        self.assertEqual(metrics["received_count"], 1)
        self.assertEqual(metrics["repair_exact"]["micro"], 0)
        self.assertAlmostEqual(metrics["invalid_rate"]["micro"], 1/len(self.tasks))
        self.assertAlmostEqual(metrics["missing_rate"]["micro"], (len(self.tasks)-1)/len(self.tasks))
        self.assertIsNone(metrics["repair_given_binding"]["micro"])

    def test_no_private_metadata_in_native(self):
        forbidden = {"task_id", "source_id", "construction_id", "visual_arm", "structural_arm",
                     "partNumber", "reference_id", "originalMatrix", "source_hash"}
        for obs in self.manifest["observations"][:20]:
            p = checked_packet(obs)
            self.assertFalse(forbidden & p.keys())
            if obs["condition"] in ("no_image", "atomic_binding"):
                self.assertNotIn("bound_terminal", p["input"])
            if obs["condition"] == "atomic_binding":
                self.assertEqual(set(p["input"]), {"candidate_ids"})
            if obs["condition"] in ("no_image", "oracle_binding"):
                self.assertFalse(p["images"])

    def test_native_controls_exact_text_and_images(self):
        task = next(iter(self.tasks.values()))
        rows = [t for t in self.tasks.values() if t["construction_id"] == task["construction_id"] and t["replicate"] == 0]
        packets = {(t["structural_arm"], t["visual_arm"]): packet(t, "multimodal", self.gold[t["id"]]) for t in rows}
        a, c, p = [packets["fault_0", arm] for arm in ("anchor", "changing", "preserving")]
        self.assertEqual({k:v for k,v in a.items() if k!="images"}, {k:v for k,v in c.items() if k!="images"})
        self.assertEqual({k:v for k,v in a.items() if k!="images"}, {k:v for k,v in p.items() if k!="images"})
        b = packets["fault_1", "anchor"]
        self.assertEqual(a["images"], b["images"])
        self.assertEqual({k:v for k,v in a["input"].items() if k!="missing"}, {k:v for k,v in b["input"].items() if k!="missing"})

    def test_legal_ocr_uses_pixels(self):
        frames = [f for f in read(HERE / "captures.json")["frames"] if "cards" in f]
        for frame in frames[::max(1, len(frames)//20)]:
            got = image_bindings(frame["file"])["ocr_labels"]
            self.assertEqual(got, [c["label"] for c in frame["cards"]])

    def test_provider_settings_guard(self):
        with self.assertRaises(ValueError):
            check_settings({})


class QualificationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.queue = read(HERE / "qualification-queue.json")
        cls.gold = {t["id"]: t["answer"] for t in read(HERE / "gold.json")["tasks"]}

    def synthetic_fixture(self, assignment, person="test-only-person"):
        return {"kind": "human", "synthetic": True, "queue_lock_sha256": self.queue["lock_sha256"],
                "assignment_id": assignment["assignment_id"], "reviewer_id": person,
                "responses": [{"task_id": i["task_id"], "prompt_sha256": i["packet"]["sha256"],
                               "bound_terminal": self.gold[i["task_id"]]["bound_terminal"],
                               **{f: True for f in FLAGS}, "comment": "unit fixture, never empirical"}
                              for i in assignment["items"]]}

    def test_six_slots_two_per_arm(self):
        assignments = self.queue["assignments"]
        cid = assignments[0]["construction_id"]
        rows = [a for a in assignments if a["construction_id"] == cid]
        self.assertEqual(len(rows), 6)
        self.assertEqual(len({a["reviewer_slot"] for a in rows}), 6)
        self.assertTrue(all(len(a["items"]) == 4 for a in rows))
        self.assertTrue(all(sum(a["visual_arm"] == arm for a in rows) == 2 for arm in ("anchor", "changing", "preserving")))

    def test_synthetic_judgment_rejected(self):
        with self.assertRaises(ValueError):
            validate_qualification([self.synthetic_fixture(self.queue["assignments"][0])], [])

    def test_wrong_prompt_rejected(self):
        row = self.synthetic_fixture(self.queue["assignments"][0])
        row["synthetic"] = False  # in-memory provenance-contract branch test only
        row["responses"][0]["prompt_sha256"] = "wrong"
        with self.assertRaises(ValueError):
            validate_qualification([row], [])

    def test_same_person_cannot_take_two_slots(self):
        rows = [self.synthetic_fixture(a) for a in self.queue["assignments"][:2]]
        for row in rows:
            row["synthetic"] = False
        with self.assertRaises(ValueError):
            validate_qualification(rows, [])

    def test_pending_does_not_become_qualified(self):
        report = validate_qualification([], [])
        self.assertEqual(report["qualified_constructions"], 0)
        self.assertEqual(report["pending_constructions"], 84)
        self.assertIsNone(report["human_results"])

    def test_same_person_adjudication_rejected(self):
        assignments = self.queue["assignments"][:2]
        rows = [self.synthetic_fixture(a, f"test-only-person-{i}") for i, a in enumerate(assignments)]
        for row in rows:
            row["synthetic"] = False
        adj = {"kind": "human", "synthetic": False, "queue_lock_sha256": self.queue["lock_sha256"],
               "construction_id": assignments[0]["construction_id"],
               "visual_arm": assignments[0]["visual_arm"], "reviewer_id": rows[0]["reviewer_id"],
               "retain": True, "reason": "test-only", "prompt_sha256s": []}
        with self.assertRaises(ValueError):
            validate_qualification(rows, [adj])


if __name__ == "__main__":
    unittest.main()
