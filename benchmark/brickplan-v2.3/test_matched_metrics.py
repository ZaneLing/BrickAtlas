"""Tiny synthetic UNIT-ONLY fixtures; never benchmark/model/human evidence."""
import copy
import itertools
import json
import math
import random
import unittest

from matched_controls import (
    equivalence_certificate, fit_source_majority, generate_controls,
    inventory_state_continuation, predict_source_majority, reduced_representations,
)
from matched_metrics import (
    HISTORICAL, MATCH_FLAGS, PRIMARY, fingerprint, hierarchical_pair_weights,
    matched_pair_scores, source_cluster_bootstrap, visual_pair_definitions,
)


def empty_bank():
    return {"schema": "synthetic-unit-only/2.3", "episodes": [], "probes": [], "pairs": []}


def add_pair(bank, key, source="S1", intervention="I1", start=1,
             split="heldout-source", cohort=PRIMARY, labels=(None, 2)):
    members = []
    plan = [{"type": "detach", "site": 0}, {"type": "audit", "site": 0},
            {"type": "attach", "site": 0}]
    for side, label in enumerate(labels):
        task_id, probe_id = f"{key}-task-{side}", f"{key}/{side}"
        bank["episodes"].append({
            "id": task_id, "profile": f"{source}-{intervention}-{side}", "sourceGroup": source,
            "split": split, "goal": 3, "capacity": 2, "jobs": [0],
        })
        bank["probes"].append({
            "id": probe_id, "taskId": task_id, "kind": "geometry-continuation",
            "state": {"assembly": start, "done": 0}, "plan": copy.deepcopy(plan),
            "firstConflict": label,
        })
        members.append(probe_id)
    bank["pairs"].append({
        "id": key, "kind": "visual-geometry", "members": members,
        "sourceGroup": source, "split": split, "interventionId": intervention,
        "evaluationCohort": cohort, "introducedVersion": "2.3" if cohort == PRIMARY else "2.2",
        "fixedContext": {**{flag: cohort == PRIMARY for flag in MATCH_FLAGS},
                         "removedSourceIndices": [[10], [11]]},
    })
    return members


def oracle_answers(bank):
    """Fixture labels only, not an actual model or a physical oracle."""
    return {p["id"]: {"firstConflict": p["firstConflict"]} for p in bank["probes"]}


def primary(report, split="heldout-source"):
    return report["cohorts"][PRIMARY]["bySplit"][split]


def public_fixture(identifier="Q1"):
    return {
        "id": identifier, "kind": "geometry-continuation", "revision": 0, "answered": False,
        "question": "UNIT-ONLY question",
        "proposedPlan": [{"type": "detach", "partId": "P001"},
                         {"type": "audit", "partId": "P001"},
                         {"type": "attach", "partId": "P001", "siteId": "S001"}],
        "responseSchema": {"firstConflict": "integer or null"},
        "observation": {
            "taskId": identifier, "sessionId": identifier, "track": "image-id",
            "partIds": ["P001", "P002"], "siteIds": ["S001", "S002"],
            "registration": [{"partId": "P001", "siteId": "S001"},
                             {"partId": "P002", "siteId": "S002"}],
            "rack": {"capacity": 2, "occupiedHolders": 1}, "actionBudget": 10,
            "workOrders": [{"partId": "P001", "completed": False}],
            "inspectionHistory": [{"frameId": "view-1-left", "atRevision": 1, "view": "left"}],
        },
    }


def geometry_fixture():
    return {
        "parts": [{"partNumber": "3001.dat", "colorCode": color, "rawMatrix": [i, 0, 0],
                   "sourceIndex": i} for i, color in enumerate((4, 1, 4, 4))],
        "mutable": [0, 1],
    }


class MatchedMetricTests(unittest.TestCase):
    def test_exact_joint_not_binary_flip_or_bool(self):
        bank = empty_bank()
        a, b = add_pair(bank, "p")
        for answer in ({"firstConflict": 1}, {"firstConflict": True},
                       {"firstConflict": 2.0}, {}, None, {"firstConflict": 2, "extra": 1}):
            report = matched_pair_scores(bank, [a, b], {a: {"firstConflict": None}, b: answer})
            self.assertEqual(primary(report)["sourceMacro"]["value"], 0)
        result = matched_pair_scores(bank, [a, b], oracle_answers(bank))
        self.assertEqual(primary(result)["sourceMacro"]["value"], 1)

    def test_missing_and_one_sided_assignments_are_not_dropped(self):
        bank = empty_bank()
        a, b = add_pair(bank, "p")
        c, d = add_pair(bank, "unassigned", intervention="I2")
        score = matched_pair_scores(bank, [a], {a: {"firstConflict": None}})
        census = primary(score)["census"]
        self.assertEqual(census["bankPairs"], 2)
        self.assertEqual(census["eligiblePairs"], 1)
        self.assertEqual(census["oneSidedPairs"], 1)
        self.assertEqual(census["unassignedPairIds"], ["unassigned"])
        self.assertEqual(census["incompletePairIds"], ["p"])
        self.assertEqual(primary(score)["pairMicro"]["value"], 0)
        self.assertEqual(score["pairs"][0]["unassignedMembers"], [b])
        score = matched_pair_scores(bank, [a, b], {})
        self.assertEqual(primary(score)["census"]["missingAssignedResponses"], 2)
        self.assertEqual(primary(score)["pairMicro"]["denominator"], 1)
        self.assertNotIn(c, [a, b])
        self.assertNotIn(d, [a, b])

    def test_empty_assignments_are_null_not_perfect(self):
        bank = empty_bank()
        add_pair(bank, "p")
        score = primary(matched_pair_scores(bank, [], {}))
        self.assertIsNone(score["sourceMacro"]["value"])
        self.assertIsNone(score["uncertainty"]["lower"])
        self.assertEqual(score["uncertainty"]["status"], "no-assigned-sources")

    def test_invalid_null_distinct_from_valid_null(self):
        bank = empty_bank()
        a, b = add_pair(bank, "p")
        report = matched_pair_scores(bank, [a, b], {a: {}, b: {"firstConflict": 2}})
        self.assertEqual(primary(report)["census"]["invalidResponses"], 1)
        self.assertEqual(report["pairs"][0]["validAnswers"], 1)
        self.assertFalse(report["pairs"][0]["jointCorrect"])

    def test_hierarchy_and_duplicate_starts(self):
        bank = empty_bank()
        for i in range(5):
            add_pair(bank, f"repeat-{i}")
        failed_start = add_pair(bank, "other-start", start=2)
        add_pair(bank, "other-intervention", intervention="I2")
        failed_source = add_pair(bank, "other-source", source="S2")
        answers = oracle_answers(bank)
        for p in failed_start + failed_source:
            answers.pop(p)
        result = primary(matched_pair_scores(bank, list(oracle_answers(bank)), answers))
        self.assertEqual(result["independentSources"], 2)
        self.assertEqual(result["independentInterventions"], 3)
        self.assertEqual(result["independentStarts"], 4)
        self.assertEqual(result["sourceMacro"]["value"], 0.375)
        self.assertEqual(result["pairMicro"]["value"], 6 / 8)
        self.assertEqual(result["bySource"]["S1"]["accuracy"], 0.75)
        self.assertEqual(result["leaveOneSourceOut"], {"S1": 0, "S2": 0.75})

    def test_missing_repeat_retains_weight_within_start(self):
        bank = empty_bank()
        members = add_pair(bank, "observed")
        missing = add_pair(bank, "missing")
        answers = {p: v for p, v in oracle_answers(bank).items() if p in members}
        result = primary(matched_pair_scores(bank, members + missing, answers))
        self.assertEqual(result["independentStarts"], 1)
        self.assertEqual(result["sourceMacro"]["value"], 0.5)

    def test_cohort_and_split_separation(self):
        bank = empty_bank()
        add_pair(bank, "heldout")
        add_pair(bank, "development", source="D1", split="development")
        legacy = add_pair(bank, "historical", source="H1", cohort=HISTORICAL)
        answers = {p: v for p, v in oracle_answers(bank).items() if p in legacy}
        report = matched_pair_scores(bank, list(oracle_answers(bank)), answers)
        self.assertEqual(primary(report)["sourceMacro"]["value"], 0)
        self.assertEqual(primary(report, "development")["sourceMacro"]["value"], 0)
        self.assertEqual(report["cohorts"][HISTORICAL]["all"]["sourceMacro"]["value"], 1)

    def test_contract_and_split_errors(self):
        for mutate in (
            lambda b: b["pairs"][0]["fixedContext"].update(equalPartCount=False),
            lambda b: b["pairs"][0].update(introducedVersion="2.2"),
            lambda b: b["pairs"][0].pop("evaluationCohort"),
            lambda b: b["episodes"][1].update(sourceGroup="other"),
            lambda b: b["episodes"][1].update(capacity=1),
            lambda b: b["probes"][1].update(firstConflict=None),
            lambda b: b["pairs"][0]["fixedContext"].update(removedSourceIndices=[[1, 1], [2]]),
        ):
            bank = empty_bank()
            add_pair(bank, "p")
            mutate(bank)
            with self.assertRaises(ValueError):
                visual_pair_definitions(bank)
        bank = empty_bank()
        add_pair(bank, "p")
        add_pair(bank, "q", split="development")
        with self.assertRaisesRegex(ValueError, "development and heldout"):
            visual_pair_definitions(bank)

    def test_legacy_cohort_and_intervention_fallback(self):
        bank = empty_bank()
        add_pair(bank, "p", cohort=HISTORICAL)
        add_pair(bank, "q", cohort=HISTORICAL, start=2)
        for pair in bank["pairs"]:
            pair.pop("evaluationCohort")
            pair.pop("interventionId")
        rows = visual_pair_definitions(bank)
        self.assertEqual(rows[0]["interventionId"], rows[1]["interventionId"])
        self.assertTrue(rows[0]["cohortInferred"])
        self.assertEqual(rows[0]["evaluationCohort"], HISTORICAL)

    def test_unknown_duplicate_and_unassigned_responses_rejected(self):
        bank = empty_bank()
        a, b = add_pair(bank, "p")
        for assigned, answers in (([a, a], {}), (["unknown"], {}),
                                  ([a], {b: {"firstConflict": 2}})):
            with self.assertRaises(ValueError):
                matched_pair_scores(bank, assigned, answers)

    def test_intervention_aliases_rejected_and_member_order_invariant(self):
        bank = empty_bank()
        add_pair(bank, "p")
        add_pair(bank, "q")
        rows = visual_pair_definitions(bank)
        bank["pairs"][1]["members"].reverse()
        reversed_rows = visual_pair_definitions(bank)
        self.assertEqual(rows[1]["startId"], reversed_rows[1]["startId"])
        self.assertEqual(rows[1]["interventionId"], reversed_rows[1]["interventionId"])
        bank["pairs"][1]["fixedContext"]["removedSourceIndices"].reverse()
        self.assertEqual(reversed_rows, visual_pair_definitions(bank))
        bank["pairs"][1]["interventionId"] = "fake-independent-intervention"
        with self.assertRaisesRegex(ValueError, "multiple intervention"):
            visual_pair_definitions(bank)

    def test_nonvisual_assignments_do_not_change_pair_scores(self):
        bank = empty_bank()
        members = add_pair(bank, "p")
        answers = oracle_answers(bank)
        expected = matched_pair_scores(bank, members, answers)
        bank["probes"].append({"id": "nonvisual", "kind": "next-action"})
        actual = matched_pair_scores(bank, members + ["nonvisual"],
                                     {**answers, "nonvisual": {"choice": 0}})
        self.assertEqual(expected, actual)

    def test_seeded_bootstrap_is_order_invariant_and_matches_reference(self):
        means = {"C": 0.5, "A": 0, "B": 1}
        report = source_cluster_bootstrap(means, seed=73, samples=137, confidence=0.8)
        self.assertEqual(report, source_cluster_bootstrap(
            dict(reversed(list(means.items()))), seed=73, samples=137, confidence=0.8))
        rng = random.Random(73)
        draws = sorted(sum(rng.choice([0, 1, 0.5]) for _ in range(3)) / 3 for _ in range(137))
        position = 136 * 0.1
        lower = draws[math.floor(position)] + (
            draws[math.ceil(position)] - draws[math.floor(position)]) * (position % 1)
        self.assertAlmostEqual(report["lower"], lower)
        self.assertEqual(report["estimate"], 0.5)
        self.assertEqual(report["resamples"], 137)

    def test_bootstrap_small_groups_disabled_and_bad_parameters(self):
        for values, status in (({}, "no-assigned-sources"), ({"A": 1}, "fewer-than-two-sources")):
            result = source_cluster_bootstrap(values)
            self.assertEqual(result["status"], status)
            self.assertIsNone(result["lower"])
            self.assertIsNone(result["upper"])
            self.assertEqual(result["resamples"], 0)
        self.assertEqual(source_cluster_bootstrap({"A": 0, "B": 1}, samples=0)["status"], "disabled")
        self.assertEqual(source_cluster_bootstrap({"A": 0, "B": 0})["upper"], 0)
        for params in ({"seed": True}, {"seed": -1}, {"samples": -1},
                       {"samples": 1.5}, {"confidence": 1}, {"confidence": float("nan")}):
            with self.assertRaises(ValueError):
                source_cluster_bootstrap({}, **params)
        with self.assertRaises(ValueError):
            source_cluster_bootstrap({"A": float("nan")})


class MatchedControlTests(unittest.TestCase):
    def test_identical_representations_preclude_joint_exact_correctness(self):
        bank = empty_bank()
        a, b = add_pair(bank, "p")
        labels = {a: None, b: 2}
        cert = equivalence_certificate(visual_pair_definitions(bank), {a: [1], b: [1]}, labels)
        self.assertEqual(cert["impossibleJointPairs"], 1)
        self.assertEqual(cert["memberMicroUpperBound"]["value"], 0.5)
        self.assertEqual(cert["jointSourceMacro"]["upperBound"]["value"], 0)
        self.assertTrue(cert["jointSourceMacro"]["tight"])

    def test_joint_optima_cannot_choose_inconsistent_class_labels(self):
        bank = empty_bank()
        a, b = add_pair(bank, "p")
        c, d = add_pair(bank, "q", intervention="I2", labels=(1, None))
        cert = equivalence_certificate(
            visual_pair_definitions(bank),
            {a: "shared", b: "other1", c: "shared", d: "other2"},
            {a: None, b: 2, c: 1, d: None})
        self.assertEqual(cert["impossibleJointPairs"], 0)
        self.assertTrue(cert["jointSourceMacro"]["tight"])
        self.assertEqual(cert["jointSourceMacro"]["upperBound"]["value"], 0.5)

    def test_joint_solver_matches_tiny_exhaustive_search(self):
        rng = random.Random(91)
        for trial in range(20):
            bank = empty_bank()
            for index in range(4):
                add_pair(bank, f"p{index}", intervention=f"I{index}",
                         labels=rng.choice([(None, 1), (1, 2), (2, None)]))
            rows = visual_pair_definitions(bank)
            labels = {p["id"]: p["firstConflict"] for p in bank["probes"]}
            reps = {p: rng.randrange(3) for p in labels}
            weights = hierarchical_pair_weights(rows)
            optimum = max(sum(weights[r["pairId"]] for r in rows
                              if all(values[reps[p]] == labels[p] for p in r["members"]))
                          for values in itertools.product((None, 1, 2), repeat=3))
            cert = equivalence_certificate(rows, reps, labels)["jointSourceMacro"]
            self.assertEqual(cert["upperBound"]["value"], optimum, trial)
            self.assertEqual(cert["achievable"]["value"], optimum, trial)
            witness = cert["witnessClassLabels"]
            self.assertEqual(sum(weights[r["pairId"]] for r in rows if all(
                witness[fingerprint(reps[p])] == labels[p] for p in r["members"])), optimum)

    def test_limited_joint_enumeration_does_not_claim_achievability(self):
        bank = empty_bank()
        a, b = add_pair(bank, "p")
        c, d = add_pair(bank, "q", intervention="I2", labels=(1, None))
        cert = equivalence_certificate(
            visual_pair_definitions(bank), {a: "shared", b: "x", c: "shared", d: "y"},
            {a: None, b: 2, c: 1, d: None}, maximum_assignments=0)["jointSourceMacro"]
        self.assertEqual(cert["status"], "enumeration-budget")
        self.assertFalse(cert["tight"])
        self.assertLess(cert["achievable"]["value"], cert["upperBound"]["value"])

    def test_global_inventory_does_not_encode_fixed_instance_geometry(self):
        public, geo = public_fixture(), geometry_fixture()
        state = {"assembly": 1, "done": 0}
        original = reduced_representations(public, geo, state, 3)
        changed = copy.deepcopy(geo)
        changed["parts"][2].update(rawMatrix=[1000, 0, 0], sourceIndex=8000)
        swapped = reduced_representations(public, changed, state, 3)
        self.assertEqual(original, swapped)
        changed["parts"][2]["colorCode"] = 9
        recolored = reduced_representations(public, changed, state, 3)
        self.assertNotEqual(original["part-type-color-count"], recolored["part-type-color-count"])
        self.assertEqual(original["count-only"], recolored["count-only"])

    def test_presence_vs_multiset_and_no_part_order_features(self):
        geo = geometry_fixture()
        state = {"assembly": 1, "done": 0}
        original = reduced_representations(public_fixture(), geo, state, 3)
        geo["parts"].append(copy.deepcopy(geo["parts"][-1]))
        extra = reduced_representations(public_fixture(), geo, state, 3)
        self.assertEqual(original["part-type-color-presence"], extra["part-type-color-presence"])
        self.assertNotEqual(original["part-type-color-count"], extra["part-type-color-count"])
        geo["parts"][2:] = reversed(geo["parts"][2:])
        self.assertEqual(extra, reduced_representations(public_fixture(), geo, state, 3))

    def test_public_metadata_retains_budget_and_frame_differences(self):
        state, geo = {"assembly": 1, "done": 0}, geometry_fixture()
        first = reduced_representations(public_fixture("Q1"), geo, state, 3)
        second = reduced_representations(public_fixture("Q2"), geo, state, 3)
        self.assertEqual(first["public-metadata"], second["public-metadata"])
        self.assertNotEqual(first["public-metadata-with-addresses"],
                            second["public-metadata-with-addresses"])
        altered = public_fixture("Q2")
        altered["observation"]["actionBudget"] += 1
        self.assertNotEqual(first["public-metadata"],
                            reduced_representations(altered, geo, state, 3)["public-metadata"])
        altered["observation"]["sites"] = []
        with self.assertRaises(ValueError):
            reduced_representations(altered, geo, state, 3)

    def test_certificate_reports_specific_public_differences(self):
        bank = empty_bank()
        a, b = add_pair(bank, "p")
        p, q = public_fixture(), public_fixture()
        q["observation"]["inspectionHistory"][0]["frameId"] = "changed"
        cert = equivalence_certificate(visual_pair_definitions(bank), {a: p, b: q}, {a: None, b: 2})
        self.assertEqual(cert["pairCertificates"][0]["differingPaths"],
                         ["$.observation.inspectionHistory[0].frameId"])
        self.assertEqual(cert["jointSourceMacro"]["upperBound"]["value"], 1)

    def test_label_free_rule_and_privileged_occupancy_scope(self):
        public = public_fixture()
        self.assertEqual(inventory_state_continuation(public), {"firstConflict": None})
        public["firstConflict"] = 1
        public["privateOracle"] = {"answer": 1}
        self.assertEqual(inventory_state_continuation(public), {"firstConflict": None})
        public["observation"]["sites"] = [{"registeredPartId": "P001", "installed": False}]
        self.assertEqual(inventory_state_continuation(public), {"firstConflict": 1})
        public["observation"].pop("sites")
        public["proposedPlan"][1] = {"type": "detach", "partId": "P001"}
        self.assertEqual(inventory_state_continuation(public), {"firstConflict": 2})

    def test_rule_work_orders_registration_and_capacity(self):
        for action, mutate in (
            ({"type": "audit", "partId": "P002"}, lambda o: None),
            ({"type": "attach", "partId": "P001", "siteId": "S002"}, lambda o: None),
            ({"type": "detach", "partId": "P001"}, lambda o: o["rack"].update(capacity=1)),
        ):
            public = public_fixture()
            public["proposedPlan"] = [action]
            mutate(public["observation"])
            self.assertEqual(inventory_state_continuation(public), {"firstConflict": 1})

    def test_partial_occupancy_inferences_respect_global_count(self):
        public = public_fixture()
        public["observation"]["workOrders"].append({"partId": "P002", "completed": False})
        public["proposedPlan"] = [{"type": "audit", "partId": p} for p in ("P001", "P002")]
        self.assertEqual(inventory_state_continuation(public), {"firstConflict": 2})
        public["observation"]["sites"] = [
            {"registeredPartId": part, "installed": False} for part in ("P001", "P002")]
        with self.assertRaisesRegex(ValueError, "Inconsistent public rack"):
            inventory_state_continuation(public)

    def test_source_majority_never_fits_heldout_and_no_training_is_null(self):
        bank = empty_bank()
        add_pair(bank, "dev", source="D1", split="development")
        heldout = add_pair(bank, "heldout", source="H1", labels=(1, 2))
        rows = visual_pair_definitions(bank)
        train = [r for r in rows if r["split"] == "development"]
        labels = {p["id"]: p["firstConflict"] for p in bank["probes"] if p["id"] not in heldout}
        model = fit_source_majority(train, labels)
        self.assertIsNone(model["fallbackLabel"])
        predictions = predict_source_majority(model, rows)
        self.assertEqual(predictions[heldout[0]], {"firstConflict": None})
        with self.assertRaises(ValueError):
            fit_source_majority(rows, {p["id"]: p["firstConflict"] for p in bank["probes"]})
        with self.assertRaises(ValueError):
            fit_source_majority(train, {**labels, heldout[0]: 1})
        self.assertEqual(predict_source_majority(fit_source_majority([], {}), rows), {})

    def test_generator_unit_only_end_to_end_and_test_label_noninterference(self):
        bank = empty_bank()
        add_pair(bank, "dev", source="D1", split="development")
        heldout = add_pair(bank, "heldout", source="H1")
        public = {p["id"]: public_fixture(p["id"]) for p in bank["probes"]}
        geometries = {t["profile"]: geometry_fixture() for t in bank["episodes"]}
        report = generate_controls(bank, public, geometries, samples=11)
        self.assertIsNone(report["visualModelResults"])
        self.assertIsNone(report["humanResults"])
        self.assertEqual(report["primaryPairs"], 2)
        cert = report["certificates"]["count-only"]["cohorts"][PRIMARY]["all"]
        self.assertEqual(cert["jointSourceMacro"]["upperBound"]["value"], 0)
        self.assertEqual(cert["memberMicroUpperBound"]["value"], 0.5)
        before = copy.deepcopy(report["sourceMajority"])
        for probe in bank["probes"]:
            if probe["id"] in heldout:
                probe["firstConflict"] = 1 if probe["firstConflict"] is None else 3
        altered = generate_controls(bank, public, geometries, samples=11)
        self.assertEqual(before["model"], altered["sourceMajority"]["model"])
        self.assertEqual(before["predictions"], altered["sourceMajority"]["predictions"])
        self.assertNotEqual(before["heldoutScores"], altered["sourceMajority"]["heldoutScores"])
        json.dumps(report, allow_nan=False)

    def test_empty_generator_does_not_report_real_results(self):
        report = generate_controls(empty_bank(), {}, {}, samples=0)
        self.assertEqual(report["status"], "no-primary-matched-pairs")
        self.assertIsNone(report["sourceMajority"]["heldoutScores"])
        cert = report["certificates"]["count-only"]["cohorts"][PRIMARY]["all"]
        self.assertIsNone(cert["memberMicroUpperBound"]["value"])
        self.assertIsNone(cert["jointSourceMacro"]["upperBound"]["value"])

    def test_contract_audit_reports_actual_inventory_mismatch(self):
        bank = empty_bank()
        add_pair(bank, "p")
        public = {p["id"]: public_fixture(p["id"]) for p in bank["probes"]}
        geometries = {t["profile"]: geometry_fixture() for t in bank["episodes"]}
        geometries[bank["episodes"][1]["profile"]]["parts"][2]["colorCode"] = 9
        report = generate_controls(bank, public, geometries, samples=0)
        self.assertEqual(report["matchingContractAudit"]["part-type-color-count"]["unequalPairIds"], ["p"])
        self.assertEqual(report["matchingContractAudit"]["count-only"]["unequalPairIds"], [])
        public[bank["probes"][1]["id"]]["observation"]["track"] = "image-id-active"
        with self.assertRaisesRegex(ValueError, "mix observation conditions"):
            generate_controls(bank, public, geometries, samples=0)

    def test_fractional_weights_have_attainable_finite_bounds(self):
        bank = empty_bank()
        for i in range(13):
            add_pair(bank, f"p{i}", intervention=f"I{i}")
        rows = visual_pair_definitions(bank)
        labels = {p["id"]: p["firstConflict"] for p in bank["probes"]}
        cert = equivalence_certificate(rows, {p: p for p in labels}, labels)
        self.assertEqual(cert["memberSourceMacroUpperBound"]["value"], 1)
        self.assertEqual(cert["jointSourceMacro"]["upperBound"]["value"], 1)
        self.assertEqual(cert["jointSourceMacro"]["achievable"]["value"], 1)


if __name__ == "__main__":
    unittest.main()
