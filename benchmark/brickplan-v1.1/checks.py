"""Extend the frozen adversarial suite with census-independent bank checks."""
import json
import unittest
from runtime import activate, HERE, OUT, BASE, ROOT

activate()
import validate as original
from build import mandatory_order, write_json
from engine import canonical_hash, no_undo, verify_distances
from evaluate import evaluate
from probes import ProbeSet


class CertificationTests(original.CertificationTests):
    def test_exhaustive_graph_and_witnesses(self):
        groups = set()
        for domain, tasks, costs, cert in original.banks():
            groups.add(cert["provenanceGroup"])
            reachable = domain.distances(0)
            for goal, table in costs.items():
                self.assertEqual(verify_distances(domain, int(goal), table, reachable),
                                 cert["goals"][goal])
            order = mandatory_order(domain, reachable, costs[str(domain.full)])
            self.assertEqual(order, cert["mandatoryOrder"])
            self.assertGreaterEqual(order["chainLengthParts"], 5 if cert["case"] == "airframe" else 4)
            self.assertEqual(cert["fullOptimalActions"], domain.n)
            for task in tasks["episodes"]:
                self.assertEqual(domain.replay(0, task["startWitness"])["state"], task["start"])
                replay = domain.replay(task["start"], task["completionWitness"])
                self.assertIsNone(replay["firstConflict"])
                self.assertEqual(replay["state"], task["goal"])
                if task["mode"] == "repair":
                    self.assertEqual(task["minimumDetaches"], 3)
                    self.assertFalse(no_undo(task["start"], task["goal"], costs[str(task["goal"])]))
            matched = [t for t in tasks["episodes"] if t["mode"] in ("repair", "healthy")]
            self.assertEqual(matched[0]["budget"], matched[1]["budget"])
            self.assertEqual(matched[0]["start"].bit_count(), matched[1]["start"].bit_count())
        self.assertGreaterEqual(len(groups), 2)

    def test_frozen_base_unchanged_and_extension_geometry_hash(self):
        import hashlib
        frozen = json.loads((BASE / "release-check.json").read_text())
        for name, expected in frozen["artifactSha256"].items():
            self.assertEqual(hashlib.sha256((BASE / name).read_bytes()).hexdigest(), expected, name)
        for domain, _, _, cert in original.banks():
            self.assertEqual(cert["geometryHash"], canonical_hash(domain.geometry))

    def test_probe_labels_and_explicit_checkpoint_against_exact_oracles(self):
        for domain, tasks, costs, _ in original.banks():
            for probe in tasks["choices"]:
                labels = []
                for action in probe["candidates"]:
                    after, code = domain.transition(probe["start"], action["type"], action["site"])
                    self.assertEqual(code, "OK")
                    table = costs[str(probe["goal"])]
                    labels.append({"noUndoLoss": not no_undo(after, probe["goal"], table),
                                   "budgetLoss": 1 + table[after] > probe["budget"]})
                self.assertEqual(labels, probe["labels"])
                self.assertEqual({label["noUndoLoss"] for label in labels}, {True, False})
            for probe in tasks["lookahead"]:
                replay = domain.replay(probe["start"], probe["plan"])
                self.assertEqual(replay["firstConflict"], probe["firstConflict"])
            for probe in tasks["counterfactual"]:
                replay = domain.replay(0, probe["startWitness"])
                self.assertIsNone(replay["firstConflict"])
                self.assertEqual(replay["state"], probe["start"])
                for member in probe["members"]:
                    qs = []
                    for action in probe["candidates"]:
                        after, code = domain.transition(probe["start"], action["type"], action["site"])
                        self.assertEqual(code, "OK")
                        qs.append(1 + costs[str(member["goal"])][after])
                    self.assertEqual(qs, member["conditionalCosts"])
                    self.assertEqual([i for i, q in enumerate(qs) if q == min(qs)],
                                     member["optimalChoices"])

    def test_source_instances_match_locked_manifests(self):
        import hashlib
        for domain, _, _, _ in original.banks():
            provenance = domain.source["provenance"]
            path = ROOT / "web/public/models" / provenance["modelId"] / "manifest.json"
            raw = path.read_bytes()
            self.assertEqual(hashlib.sha256(raw).hexdigest(), provenance["manifestSha256"])
            manifest = json.loads(raw)
            self.assertEqual([p["sourceIndex"] for p in domain.parts],
                             provenance["includedSourceIndices"])
            for part in domain.parts:
                instance = manifest["instances"][part["sourceIndex"]]
                for field in ("originalMatrix", "partNumber", "colorCode", "colorHex"):
                    self.assertEqual(part[field], instance[field])
                self.assertEqual(part["sourceInstanceId"], instance["instanceId"])
                source = ROOT / "assets-source/ldraw-library/locked/parts" / (part["partNumber"] + ".dat")
                self.assertEqual(hashlib.sha256(source.read_bytes()).hexdigest(),
                                 part["sourcePartSha256"])


class RuntimeTests(original.RuntimeTests):
    def test_public_probes_hide_condition_and_permute(self):
        banks = original.banks()
        probe_set = ProbeSet(banks, 219)
        expected = sum(len(t["choices"]) + len(t["lookahead"])
                       + sum(len(p["members"]) for p in t["counterfactual"])
                       for _, t, _, _ in banks)
        self.assertEqual(len(probe_set.catalog()), expected)
        answers = {}
        choices = lookaheads = 0
        for key, entry in probe_set.entries.items():
            public = probe_set.get(key)
            serialized = json.dumps(public)
            for forbidden in ("conditionalCosts", "optimalChoices", "conflict/", "control/",
                              "labels", "sourceIndex"):
                self.assertNotIn(forbidden, serialized)
            if entry["kind"] == "lookahead":
                lookaheads += 1
                self.assertEqual(len(public["proposedPlan"]), public["horizon"])
                answers[key] = {"firstConflict": None}
            else:
                choices += 1
                answers[key] = {"choice": 0}
        normalized, positions = probe_set.normalize(answers)
        self.assertEqual(positions, {"0": choices})
        self.assertEqual(len(normalized["lookahead"]), lookaheads)


class MetricTests(original.MetricTests):
    def test_oracle_and_missing_denominators(self):
        perfect = evaluate(original.control_submission("oracle"))
        self.assertEqual(perfect["successRate"]["value"], 1)
        self.assertEqual(perfect["recovery"]["jointDetectionAndCompletion"]["value"], 1)
        self.assertTrue(all(r["actionRegret"] == 0 and r["detachRegret"] == 0
                            for r in perfect["regretAndEfficiency"]))
        missing = evaluate({"schema": "brickplan-submission/1.0"})
        self.assertEqual(missing["successRate"]["value"], 0)
        self.assertEqual(missing["missingEpisodes"],
                         sum(len(t["episodes"]) for _, t, _, _ in original.banks()))
        self.assertIsNone(missing["deadEndChoices"]["noUndoDeadEndRate"]["value"])
        self.assertEqual(missing["deadEndChoices"]["certifiedNoUndoAvoidanceAllAssigned"]["value"], 0)
        self.assertEqual(missing["lookahead"]["distanceCurve"]["8"]["exactFirstConflictAccuracy"]["value"], 0)
        curve = missing["planSurvival"]["noUndo"][0]["curve"]
        self.assertEqual((curve[-1]["lower"], curve[-1]["upper"]), (0, 1))


def main():
    suite = unittest.TestSuite(unittest.defaultTestLoader.loadTestsFromTestCase(cls)
                               for cls in (CertificationTests, RuntimeTests, MetricTests))
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    if not result.wasSuccessful():
        raise SystemExit(1)
    controls = {}
    for policy in ("oracle", "attach-only", "fault-and-recover"):
        submission = original.control_submission(policy)
        report = evaluate(submission)
        write_json(OUT / f"{policy}.submission.json", submission)
        write_json(OUT / f"{policy}.report.json", report)
        controls[policy] = {
            "successRate": report["successRate"],
            "recovery": report["recovery"]["completionRate"],
            "deadEndChoiceRate": report["deadEndChoices"]["noUndoDeadEndRate"],
        }
    summary = {"tests": result.testsRun, "passed": True, "softwareValidationOnly": True,
               "controls": controls}
    write_json(OUT / "summary.json", summary)
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
