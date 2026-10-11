"""Bank-independent tests; all generated fixtures live in temporary directories."""
from copy import deepcopy
import json
from pathlib import Path
import sys
import tempfile
from types import SimpleNamespace
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "benchmark/brickplan-v2.3"))

import catalogue
from mission import canonical_hash
import package_release


def fixture():
    bank = {"episodes": [], "probes": [], "pairs": [], "profiles": []}
    arena = SimpleNamespace(tasks={}, probe_ids={}, study=False, seed=0, track="image-id")
    for index, cohort in enumerate(("primary-matched", "historical-unmatched-regression")):
        profile = f"profile-{index}"
        bank["profiles"].append({"id": profile, "introducedVersion": "2.3", "sampling": "fixture"})
        members = []
        for side in range(2):
            task_id, probe_id = f"task-{index}-{side}", f"probe-{index}-{side}"
            bank["episodes"].append({
                "id": task_id, "profile": profile, "sourceGroup": f"kit-{index}",
                "split": "heldout-source" if index == 0 else "development",
                "tier": "D1", "kind": "visual-geometry-context",
            })
            bank["probes"].append({"id": probe_id, "taskId": task_id, "kind": "geometry-continuation"})
            number = index * 2 + side + 1000
            arena.tasks[f"E{number}"] = task_id
            arena.probe_ids[f"Q{number}"] = probe_id
            members.append(probe_id)
        bank["pairs"].append({"kind": "visual-geometry", "evaluationCohort": cohort, "members": members})
    return bank, arena


class CatalogueContracts(unittest.TestCase):
    def setUp(self):
        self.bank, self.arena = fixture()

    def catalogue(self):
        with patch.object(catalogue, "task_bank", return_value=self.bank):
            return catalogue.catalogue(self.arena)

    def test_counts_and_cohorts_follow_bank_not_constants(self):
        original = deepcopy(self.bank)
        cat = self.catalogue()
        self.assertEqual(cat["release"], "2.3")
        self.assertEqual(cat["bankHash"], canonical_hash(self.bank))
        self.assertEqual(cat["counts"], {"episodes": 4, "probes": 4, "sources": 2, "pairs": 2})
        self.assertEqual(sum(row["count"] for row in cat["taxonomy"]), 8)
        self.assertEqual([c["probes"] for c in cat["cohorts"]], [2, 2])
        self.assertEqual([c["heldoutSources"] for c in cat["cohorts"]], [1, 0])
        self.assertEqual(self.bank, original)

    def test_subset_counts_only_complete_visible_pairs(self):
        del self.arena.probe_ids["Q1001"]
        cat = self.catalogue()
        self.assertEqual(cat["counts"]["pairs"], 1)
        self.assertEqual(cat["cohorts"][0]["probes"], 1)
        self.assertEqual(cat["cohorts"][0]["pairs"], 0)
        self.assertEqual(cat["cohorts"][1]["pairs"], 1)

    def test_direct_study_catalogue_is_denied(self):
        self.arena.study = True
        with self.assertRaisesRegex(ValueError, "controlled study"):
            self.catalogue()

    def test_question_export_keeps_metadata_outside_policy_input(self):
        public = {"id": "Q1000", "question": "Locate the first conflict.",
                  "observation": {"partIds": ["P001"], "revision": 0}}
        with tempfile.TemporaryDirectory(prefix="brickplan-contracts-") as temporary:
            folder = Path(temporary)
            with patch.object(package_release, "OUT", folder), \
                    patch.object(catalogue, "task_bank", return_value=self.bank), \
                    patch.object(package_release, "preview", return_value=public):
                cat = package_release.export_questions(self.arena)
            rows = [json.loads(line) for line in (folder / "questions.jsonl").read_text().splitlines()]
            self.assertEqual(len(rows), len(cat["questions"]))
            for row, question in zip(rows, cat["questions"]):
                self.assertEqual(row["stableId"], question["stableId"])
                self.assertEqual(row["evaluationCohort"], question["evaluationCohort"])
                self.assertEqual(json.loads(row["publicInputJSON"]), public)
                self.assertEqual(json.loads(row["stimulusRecipe"])["endpoint"], f"/api/preview/{row['id']}")

    def test_primary_geometry_sample_even_when_historical_is_first(self):
        cat = self.catalogue()
        cat["questions"].reverse()
        selected = package_release.sample_question(cat, "geometry")
        self.assertEqual(selected["evaluationCohort"], "primary-matched")

    def test_no_historical_fallback_for_missing_primary_sample(self):
        cat = self.catalogue()
        cat["questions"] = [q for q in cat["questions"] if q["evaluationCohort"] != "primary-matched"]
        with self.assertRaisesRegex(ValueError, "geometry requires primary-matched"):
            package_release.sample_question(cat, "geometry")

    def test_export_rejects_changed_inventory_producer_or_bank(self):
        with tempfile.TemporaryDirectory(prefix="brickplan-manifest-") as temporary:
            folder = Path(temporary)
            output = folder / "release"
            output.mkdir()
            (output / "samples").mkdir()
            (folder / "producer.py").write_text("fixture")
            (output / "catalogue.json").write_text(json.dumps(self.catalogue()))
            (output / "sample.json").write_text("{}")
            manifest = {
                "bankHash": canonical_hash(self.bank),
                "runtimeFiles": {"producer.py": package_release.sha(folder / "producer.py")},
                "files": {name: package_release.sha(output / name) for name in ("catalogue.json", "sample.json")},
            }
            (output / "export-manifest.json").write_text(json.dumps(manifest))
            with patch.object(package_release, "HERE", folder), patch.object(package_release, "OUT", output), \
                    patch.object(package_release, "EXPORT_RUNTIME", ("producer.py",)), \
                    patch.object(package_release, "EXPORT_FILES", ("catalogue.json", "sample.json")), \
                    patch.object(package_release, "task_bank", return_value=self.bank):
                self.assertEqual(package_release.check_export()["release"], "2.3")
                (output / "samples/stale.json").write_text("{}")
                with self.assertRaisesRegex(AssertionError, "Unexpected public export files"):
                    package_release.check_export()
                (output / "samples/stale.json").unlink()
                (folder / "producer.py").write_text("changed")
                with self.assertRaisesRegex(AssertionError, "runtime inputs"):
                    package_release.check_export()
                (folder / "producer.py").write_text("fixture")
                with patch.object(package_release, "task_bank", return_value={}):
                    with self.assertRaisesRegex(AssertionError, "current bank"):
                        package_release.check_export()


if __name__ == "__main__":
    unittest.main()
