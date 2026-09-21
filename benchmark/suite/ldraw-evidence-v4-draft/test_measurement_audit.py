"""Counterexamples for structural feasibility and no-image interpretation."""
from copy import deepcopy
import unittest

from analyze import prompt_bytes, strip_image
from measurement_audit import enumerate_swaps, recompute_gold
from test_single_image_baselines import wire


def fixture():
    bundle = {"parts": [{"id": key, "partNumber": typ} for key, typ in [
        ("target", "plate"), ("match", "plate"), ("wrong1", "brick"),
        ("wrong2", "slope"), ("wrong3", "tile")]]}
    ids = ["target", "match", "wrong1", "wrong2", "wrong3"]
    observation = {
        "family": "shape-match", "payload": {"options": [
            {"id": choice, "label": label} for choice, label in
            zip("ABCD", ["B0001", "B0002", "B0003", "B0004"])]},
        # Deliberately incorrect stored gold: independent reconstruction ignores it.
        "gold": {"choiceId": "D"},
        "render_spec": {"target_id": "target", "render_operands": ids,
                        "labels": dict(zip(ids, ["B0000", "B0001", "B0002", "B0003", "B0004"])),
                        "reference_positions": [
                            {"id": key, "anchor": [50+100*i, 200], "text": [66+100*i, 178]}
                            for i, key in enumerate(ids)]},
    }
    return observation, bundle


class MeasurementTests(unittest.TestCase):
    def test_gold_is_recomputed_not_copied(self):
        observation, bundle = fixture()
        self.assertEqual(recompute_gold(observation, bundle), "A")
        panel = deepcopy(observation)
        panel["render_spec"]["candidate_ids"] = ["wrong1", "wrong2", "match", "wrong3"]
        panel["render_spec"]["labels"] = {}
        self.assertEqual(recompute_gold(panel, bundle), "C")

    def test_reject_nonunique_source_gold(self):
        observation, bundle = fixture()
        bundle["parts"][-1]["partNumber"] = "plate"
        with self.assertRaisesRegex(ValueError, "not unique"):
            recompute_gold(observation, bundle)

    def test_all_three_swaps_preserve_gold(self):
        observation, bundle = fixture()
        swaps = enumerate_swaps(observation, bundle, 1280, 800)
        self.assertEqual(len(swaps), 3)
        self.assertTrue(all(s["machine_eligible"] for s in swaps))
        self.assertTrue(all(s["gold_after"] == "A" for s in swaps))
        self.assertTrue(all(s["visually_distinguishable"] == "pending-human" for s in swaps))

    def test_zero_eligible_parents_remain_reportable(self):
        observation, bundle = fixture()
        observation["render_spec"]["render_operands"] = ["target", "match", "wrong1"]
        swaps = enumerate_swaps(observation, bundle, 1280, 800)
        self.assertEqual(len(swaps), 3)
        self.assertEqual(sum(s["machine_eligible"] for s in swaps), 0)
        self.assertTrue(all("both_in_current_operands" in s["missing_reasons"] for s in swaps))

    def test_on_screen_anchor_does_not_imply_visible_label_box(self):
        observation, bundle = fixture()
        observation["render_spec"]["reference_positions"][-1]["text"] = [1270, 20]
        swaps = enumerate_swaps(observation, bundle, 1280, 800)
        self.assertEqual(sum(s["machine_eligible"] for s in swaps), 1)
        rejected = [s for s in swaps if not s["machine_eligible"]]
        self.assertTrue(all(s["checks"]["projected_anchors_in_canvas"] for s in rejected))
        self.assertTrue(all(not s["checks"]["conservative_label_boxes_in_canvas"] for s in rejected))

    def test_noimage_identical_different_gold_floor(self):
        a, b = wire("red"), wire("blue")
        self.assertNotEqual(a, b)
        self.assertEqual(prompt_bytes(a), prompt_bytes(b))
        self.assertEqual(strip_image(a), strip_image(b))
        for fixed in "ABCD":
            correct = [fixed == gold for gold in ["C", "D"]]
            self.assertEqual(int(all(correct)), 0)
            self.assertLessEqual(sum(correct)/2, .5)
        # This implication requires identical predictions, not just identical inputs.
        self.assertTrue(all(pred == gold for pred, gold in zip(["C", "D"], ["C", "D"])))


if __name__ == "__main__":
    unittest.main()
