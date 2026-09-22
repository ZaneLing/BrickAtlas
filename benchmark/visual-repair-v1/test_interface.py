"""Ephemeral synthetic/mocked regressions; no model calls or evidence writes."""
import base64
import copy
import subprocess
import unittest
from unittest.mock import patch

import numpy as np

from common import HERE, VERSION, digest, read
from joint import CONTRACT, interface_metrics, validate_comparisons
from portable import collect, lock_run, verify_run_lock
from qualification import FLAGS, build_eligibility, validate_eligibility
from study import analyze, envelope, load_manifest, metrics, validate_receipts

CONFIG_IDS = dict(zip(("atomic_binding", "oracle_binding", "multimodal"), ("a", "o", "m")))


def outcome_fixture(disjoint=False):
    rows = []
    for group in range(2):
        for construction in range(2):
            for replicate in range(2):
                for fault in ("fault_0", "fault_1"):
                    for arm in ("anchor", "changing", "preserving"):
                        for condition, cid in CONFIG_IDS.items():
                            correct = construction == (int(disjoint) if condition != "multimodal" else 0)
                            rows.append({
                                "id": f"{group}-{construction}-{replicate}-{fault}-{arm}",
                                "construction_id": f"{group}-{construction}", "dependence_group": str(group),
                                "replicate": replicate, "structural_arm": fault, "visual_arm": arm,
                                "repeat": 0, "split": "heldout", "config_id": cid, "condition": condition,
                                "binding_correct": correct, "repair_exact": correct and condition != "atomic_binding",
                                "missing": False, "invalid": False,
                            })
    return rows


def human_fixtures(queue, gold):
    # Exercises provenance validation in memory only, never returned as evidence.
    return [{
        "kind": "human", "synthetic": False, "queue_lock_sha256": queue["lock_sha256"],
        "assignment_id": a["assignment_id"], "reviewer_id": "test-only-" + a["reviewer_slot"],
        "responses": [{"task_id": i["task_id"], "prompt_sha256": i["packet"]["sha256"],
                       "bound_terminal": gold[i["task_id"]]["bound_terminal"],
                       **{f: True for f in FLAGS}, "comment": "ephemeral unit fixture, not a real judgment"}
                      for i in a["items"]],
    } for a in queue["assignments"]]


class JointTests(unittest.TestCase):
    def test_same_complete_marginals_opposite_joint_failures(self):
        aligned, disjoint = outcome_fixture(), outcome_fixture(True)
        for condition in CONFIG_IDS:
            self.assertEqual(metrics([r for r in aligned if r["condition"] == condition]),
                             metrics([r for r in disjoint if r["condition"] == condition]))
        good = interface_metrics(aligned, CONFIG_IDS)
        bad = interface_metrics(disjoint, CONFIG_IDS)
        for report, failures in ((good, 0), (bad, 24)):
            joint = report["joint_failure_given_atomic_oracle"]
            self.assertEqual(joint["eligible_n"], 24)
            self.assertEqual(joint["eligible_groups"], 2)
            self.assertEqual(joint["failure_n"], failures)
            self.assertEqual(joint["micro"], failures / 24)
            self.assertEqual(joint["group_macro"], failures / 24)
            self.assertEqual(len(report["contingency"]), 8)
            self.assertEqual(sum(report["contingency"].values()), 48)
        self.assertEqual(good["contingency"]["111"], 24)
        self.assertEqual(bad["contingency"]["110"], 24)

    def test_zero_joint_eligibility_undefined_not_perfect(self):
        rows = outcome_fixture()
        for row in rows:
            if row["condition"] == "atomic_binding":
                row["binding_correct"] = False
        j = interface_metrics(rows, CONFIG_IDS)["joint_failure_given_atomic_oracle"]
        self.assertEqual((j["eligible_n"], j["eligible_groups"], j["failure_n"]), (0, 0, 0))
        self.assertIsNone(j["micro"])
        self.assertIsNone(j["group_macro"])
        self.assertIsNone(j["ci95_group_sensitivity"])
        self.assertEqual(j["bootstrap_defined_draws"], 0)
        self.assertEqual(j["group_values"], {"0": None, "1": None})

    def test_zero_eligible_groups_retained_in_resampling(self):
        rows = outcome_fixture()
        for row in rows:
            if row["condition"] == "atomic_binding" and row["dependence_group"] == "0":
                row["binding_correct"] = False
        result = interface_metrics(rows, CONFIG_IDS)
        j = result["joint_failure_given_atomic_oracle"]
        self.assertEqual(result["bootstrap"]["group_order"], ["0", "1"])
        self.assertEqual((j["eligible_groups"], j["zero_eligible_groups"]), (1, 1))
        self.assertIsNone(j["ci95_group_sensitivity"])
        self.assertGreater(j["bootstrap_defined_draws"], 0)
        self.assertLess(j["bootstrap_defined_draws"], 2000)

    def test_unequal_group_weighting_and_shared_contrast_draws(self):
        rows = [r for r in outcome_fixture() if r["construction_id"] in ("0-0", "1-0")]
        # Keep one slot from group 0 and three from group 1.
        ids = {g: sorted({r["id"] for r in rows if r["dependence_group"] == g})[:n]
               for g, n in (("0", 1), ("1", 3))}
        rows = [r for r in rows if r["id"] in ids[r["dependence_group"]]]
        for row in rows:
            if row["condition"] == "multimodal" and row["dependence_group"] == "0":
                row["repair_exact"] = row["binding_correct"] = False
        report = interface_metrics(rows, CONFIG_IDS)
        j = report["joint_failure_given_atomic_oracle"]
        self.assertEqual((j["micro"], j["group_macro"]), (.25, .5))
        for name in ("delta_repair", "delta_binding"):
            d = report[name]
            self.assertEqual((d["micro"], d["group_macro"]), (-.25, -.5))
            self.assertEqual(d["group_values"], {"0": -1., "1": 0.})
            self.assertEqual(d["ci95_group_sensitivity"], [-j["ci95_group_sensitivity"][1],
                                                         -j["ci95_group_sensitivity"][0]])
        rng = np.random.default_rng(CONTRACT["bootstrap"]["seed"])
        draws = rng.integers(0, 2, size=(2000, 2))
        pooled = np.array([1., 0.])[draws].sum(axis=1) / np.array([1., 3.])[draws].sum(axis=1)
        self.assertEqual(j["ci95_micro_group_sensitivity"], np.quantile(pooled, [.025, .975]).tolist())

    def test_missing_planned_receipt_not_complete_case_dropped(self):
        rows = outcome_fixture()
        for row in rows:
            if row["condition"] == "multimodal":
                row["missing"] = True
        report = interface_metrics(rows, CONFIG_IDS)
        self.assertEqual(report["planned_count"], 48)
        self.assertEqual(report["joint_failure_given_atomic_oracle"]["failure_n"], 24)
        self.assertEqual(report["delta_repair"]["micro"], -.5)

    def test_invalid_output_never_gets_partial_binding_credit(self):
        rows = outcome_fixture()
        for row in rows:
            if row["condition"] == "atomic_binding":
                row["invalid"] = True
        report = interface_metrics(rows, CONFIG_IDS)
        self.assertEqual(report["joint_failure_given_atomic_oracle"]["eligible_n"], 0)
        self.assertEqual(report["delta_binding"]["micro"], .5)

    def test_missing_condition_and_off_cell_rejected(self):
        rows = outcome_fixture()
        with self.assertRaises(ValueError):
            interface_metrics([r for r in rows if r["condition"] != "oracle_binding"], CONFIG_IDS)
        rows[0]["replicate"] = 9
        with self.assertRaises(ValueError):
            interface_metrics(rows, CONFIG_IDS)

    def test_duplicate_cell_rejected(self):
        rows = outcome_fixture()
        with self.assertRaises(ValueError):
            interface_metrics(rows + [rows[0]], CONFIG_IDS)

    def test_empty_subset_all_estimates_null(self):
        report = interface_metrics([], CONFIG_IDS)
        self.assertEqual(report["planned_count"], 0)
        self.assertEqual(sum(report["contingency"].values()), 0)
        for key in ("joint_failure_given_atomic_oracle", "delta_repair", "delta_binding"):
            self.assertIsNone(report[key]["micro"])
            self.assertIsNone(report[key]["group_macro"])
        self.assertIsNone(metrics([], "atomic_binding")["repair_exact"])

    def test_whole_construction_exclusion_keeps_all_cells(self):
        rows = [r for r in outcome_fixture(True) if r["construction_id"] not in ("0-1", "1-1")]
        report = interface_metrics(rows, CONFIG_IDS)
        self.assertEqual(report["planned_count"], 24)
        self.assertEqual(report["joint_failure_given_atomic_oracle"]["eligible_n"], 0)
        self.assertEqual(report["delta_repair"]["micro"], 1)


class LockedIntegrationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.manifest = load_manifest()
        cls.queue = read(HERE / "qualification-queue.json")
        cls.gold = {t["id"]: t["answer"] for t in read(HERE / "gold.json")["tasks"]}
        cls.human_rows = human_fixtures(cls.queue, cls.gold)
        cls.all_qualified = build_eligibility(cls.human_rows, [])
        cls.pending = read(HERE / "qualification-eligibility.json")
        cls.model = next(m for m in read(HERE / "planned-models.json")["models"] if "multimodal" in m["conditions"])
        cls.settings = {"output_token_limit": 2048, "temperature": None, "effort": None,
                        "timeout_seconds": 5, "image_policy": "native-full-png", "tools": [], "repeats": 1}

    def model_lock(self, eligibility=None):
        # Existing source used solely as an adapter hash fixture, never executed.
        return lock_run(self.model["id"], "unit-test-revision", HERE / "portable.py",
                        self.settings, eligibility or self.pending)

    def test_incompatible_comparison_revision_settings_identity_kind(self):
        for field, value in (("revision", "different"), ("settings", {}), ("system_id", "other"),
                             ("kind", "model"), ("repeats", 2)):
            manifest = copy.deepcopy(self.manifest)
            comparison = manifest["comparison_groups"][0]
            config = next(c for c in manifest["configurations"] if c["id"] == comparison["config_ids"]["atomic_binding"])
            config[field] = value
            with self.subTest(field=field), self.assertRaises(ValueError):
                validate_comparisons(manifest)

    def test_missing_required_configuration_rejected(self):
        manifest = copy.deepcopy(self.manifest)
        manifest["configurations"] = [c for c in manifest["configurations"] if c["condition"] != "atomic_binding"]
        with self.assertRaises(ValueError):
            validate_comparisons(manifest)

    def test_same_model_different_run_receipt_rejected(self):
        one, two = self.model_lock(), self.model_lock(self.all_qualified)
        self.assertNotEqual(one["lock_sha256"], two["lock_sha256"])
        obs = one["observations"][0]
        config = next(c for c in one["configurations"] if c["condition"] == obs["condition"])
        receipt = envelope(one, config, obs, None, "unit-test-failure")
        with self.assertRaises(ValueError):
            validate_receipts(two, [receipt])

    def test_portable_lock_embeds_revalidated_eligibility_and_full_collection(self):
        manifest = self.model_lock()
        verify_run_lock(manifest)
        self.assertEqual(manifest["eligibility"], self.pending)
        self.assertEqual(manifest["planned_runs"], 4032)
        self.assertEqual(len(manifest["observations"]), 4032)
        self.assertEqual(manifest["eligibility"]["sets"]["qualified"], [])
        with self.assertRaises(ValueError):
            validate_eligibility(self.all_qualified, manifest)

    def test_incomplete_portable_membership_rejected_even_if_rehashed(self):
        manifest = self.model_lock()
        manifest["observations"].pop()
        manifest.pop("lock_sha256")
        manifest["lock_sha256"] = digest(manifest)
        with self.assertRaises(ValueError):
            verify_run_lock(manifest)

    def test_rehashed_eligibility_edit_not_validated_human_evidence(self):
        artifact = copy.deepcopy(self.pending)
        artifact["sets"]["qualified"] = artifact["sets"]["full"][:1]
        artifact.pop("lock_sha256")
        artifact["lock_sha256"] = digest(artifact)
        with self.assertRaises(ValueError):
            validate_eligibility(artifact, self.manifest)

    def test_off_study_eligibility_rejected(self):
        artifact = copy.deepcopy(self.pending)
        artifact["study_lock_sha256"] = "another-study"
        artifact.pop("lock_sha256")
        artifact["lock_sha256"] = digest(artifact)
        with self.assertRaises(ValueError):
            validate_eligibility(artifact, self.manifest)

    def test_no_exclusions_qualified_equals_full_in_analyzer(self):
        # Real local algorithm responses; hypothetical qualification stays in memory.
        receipts = read(HERE / "algorithmic-receipts.json")
        report = analyze(receipts, self.manifest, write_output=False, eligibility=self.all_qualified)
        released = {c["id"]: c for c in read(HERE / "baseline-report.json")["configurations"]}
        for config in report["configurations"]:
            for split in ("dev", "heldout", "all"):
                self.assertEqual(config[split], config["qualified"][split])
                self.assertEqual(config[split], released[config["id"]][split])
        for comparison in report["interface"]:
            self.assertEqual(comparison["full"], comparison["qualified"])
        self.assertEqual(report["analysis_sets"]["qualified"]["task_count"], 1008)
        silhouette = next(c for c in report["configurations"] if c["id"] == "silhouette-repair")
        self.assertEqual(silhouette["heldout"]["repair_exact"]["n"], 684)
        self.assertEqual(silhouette["heldout"]["repair_exact"]["micro"], 624 / 684)
        self.assertEqual(silhouette["heldout"]["repair_exact"]["group_macro"], 0.7829090909090909)

    def test_pending_vs_rejected_and_construction_wide_subset(self):
        assignments = self.queue["assignments"][:6]
        rows = copy.deepcopy(self.human_rows[:6])
        rows[0]["responses"][0]["labels_readable"] = False
        artifact = build_eligibility(rows, [])
        self.assertEqual(artifact["qualification"]["needs_adjudication_constructions"], 1)
        adj = {
            "construction_id": assignments[0]["construction_id"], "visual_arm": assignments[0]["visual_arm"],
            "reviewer_id": "test-only-independent-adjudicator", "kind": "human", "synthetic": False,
            "queue_lock_sha256": self.queue["lock_sha256"], "retain": False, "reason": "ephemeral fixture",
            "prompt_sha256s": sorted(i["packet"]["sha256"] for i in assignments[0]["items"]),
        }
        artifact = build_eligibility(rows, [adj])
        self.assertEqual(artifact["qualification"]["rejected_constructions"], 1)
        self.assertEqual(artifact["qualification"]["pending_constructions"], 83)
        self.assertEqual(len(artifact["sets"]["full"]), 84)
        self.assertEqual(artifact["sets"]["qualified"], [])
        all_rows = copy.deepcopy(self.human_rows)
        all_rows[0] = rows[0]
        excluded = build_eligibility(all_rows, [adj])
        report = analyze([], self.manifest, write_output=False, eligibility=excluded)
        self.assertEqual(report["analysis_sets"]["qualified"]["task_count"], 996)
        for config in report["configurations"]:
            self.assertEqual(config["all"]["planned_count"], 1008)
            self.assertEqual(config["qualified"]["all"]["planned_count"], 996)
        for comparison in report["interface"]:
            self.assertEqual(comparison["qualified"]["all"]["planned_count"], 996)

    def test_missing_malformed_transport_failures_keep_joint_denominator(self):
        manifest = self.model_lock()
        obs_by_key = {(o["task_id"], o["condition"]): o for o in manifest["observations"]}
        tid = manifest["observations"][0]["task_id"]
        receipts = []
        for config in manifest["configurations"]:
            if config["condition"] == "atomic_binding":
                continue  # Planned but missing, not an absent condition.
            obs = obs_by_key[tid, config["condition"]]
            response = self.gold[tid] if config["condition"] == "oracle_binding" else "malformed"
            receipts.append(envelope(manifest, config, obs, response,
                                     "adapter_exit_1" if config["condition"] == "multimodal" else None))
        report = analyze(receipts, manifest, write_output=False)
        result = report["interface"][0]["full"]["all"]
        self.assertEqual(result["planned_count"], 1008)
        self.assertEqual(result["contingency"]["010"], 1)
        self.assertEqual(result["contingency"]["000"], 1007)
        self.assertEqual(result["joint_failure_given_atomic_oracle"]["eligible_n"], 0)
        self.assertIsNone(report["interface"][0]["qualified"]["all"]["delta_repair"]["micro"])


class AdapterDiagnosticTests(unittest.TestCase):
    def run_mock(self, result=None, exception=None):
        config = {"id": "fixture", "kind": "model", "condition": "no_image", "revision": "test",
                  "settings": {"timeout_seconds": 5}}
        obs = {"task_id": "test-task", "condition": "no_image", "packet": {"sha256": "test-input"}}
        manifest = {"version": VERSION, "lock_sha256": "test-lock", "configurations": [config],
                    "observations": [obs], "adapter": {"path": "unused-adapter.py"},
                    "model": {"requested_model": "unit-only"}}
        with patch("portable.verify_run_lock"), patch("portable.checked_packet", return_value={
                "condition": "no_image", "input": {}, "images": []}), patch("portable.write") as writer, \
                patch("portable.subprocess.run", return_value=result, side_effect=exception) as run:
            rows = collect(manifest, "unused-no-write.json")
        self.assertEqual(run.call_count, 1)
        self.assertEqual(writer.call_count, 1)
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["diagnostics"]["schema"], "visual-repair-adapter-diagnostics-v1")
        return rows[0]

    def test_nonzero_retains_exact_streams_and_returncode(self):
        stdout, stderr = b'{"partial":true}\xff', b"adapter transport error"
        row = self.run_mock(subprocess.CompletedProcess(["unused"], 7, stdout, stderr))
        self.assertIsNone(row["response"])
        self.assertEqual(row["error"], "adapter_exit_7")
        diagnostic = row["diagnostics"]
        self.assertEqual(diagnostic["returncode"], 7)
        self.assertEqual(diagnostic["stderr"], stderr.decode())
        self.assertEqual(base64.b64decode(diagnostic["stdout_base64"]), stdout)
        self.assertEqual(base64.b64decode(diagnostic["stderr_base64"]), stderr)
        self.assertFalse(diagnostic["timed_out"])

    def test_timeout_partial_streams_no_success_credit(self):
        row = self.run_mock(exception=subprocess.TimeoutExpired(
            ["unused"], 5, output=b'{"bound_terminal":"V1234"}', stderr=b"partial timeout stderr"))
        self.assertIsNone(row["response"])
        self.assertEqual(row["error"], "TimeoutExpired")
        diagnostic = row["diagnostics"]
        self.assertTrue(diagnostic["timed_out"])
        self.assertIsNone(diagnostic["returncode"])
        self.assertEqual(diagnostic["stdout"], '{"bound_terminal":"V1234"}')
        self.assertEqual(diagnostic["stderr"], "partial timeout stderr")
        self.assertEqual(diagnostic["timeout_seconds"], 5)

    def test_timeout_unavailable_streams_null(self):
        row = self.run_mock(exception=subprocess.TimeoutExpired(["unused"], 5))
        self.assertIsNone(row["diagnostics"]["stdout"])
        self.assertIsNone(row["diagnostics"]["stderr_base64"])

    def test_oserror_retains_exception(self):
        row = self.run_mock(exception=OSError("cannot launch"))
        self.assertEqual(row["error"], "OSError")
        self.assertEqual(row["diagnostics"]["exception_message"], "cannot launch")
        self.assertFalse(row["diagnostics"]["timed_out"])

    def test_successful_malformed_stdout_retained_for_parser(self):
        row = self.run_mock(subprocess.CompletedProcess(["unused"], 0, b"not-json", b"warning"))
        self.assertEqual(row["response"], "not-json")
        self.assertIsNone(row["error"])
        self.assertEqual(row["diagnostics"]["stderr"], "warning")


if __name__ == "__main__":
    unittest.main()
