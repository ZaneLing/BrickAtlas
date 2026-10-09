"""Adversarial integration checks and labelled software-control reports."""
from __future__ import annotations

import copy
import json
from pathlib import Path
import tempfile
import unittest

from build import HERE, load_bank, write_json
from cases import CASES
from engine import AssemblyDomain, minimum_detaches, no_undo, verify_distances
from evaluate import evaluate, episode_score, score_counterfactual
from probes import ProbeSet
from session import Session, replay_export

OUT = HERE.parents[1] / "tem/brickplan-v1/validation"
BANKS = None


def banks():
    global BANKS
    if BANKS is None:
        BANKS = [load_bank(c["id"]) for c in CASES]
    return BANKS


def send(session, action):
    return session.submit({"requestId": f"step-{session.revision}", "revision": session.revision,
                           "action": action})


def complete(session, table):
    for a in session.domain.witness(session.state, session.task["goal"], table):
        result = send(session, session.public_action(a))
        if result["result"]["code"] != "OK":
            raise AssertionError(result)
    if not session.terminated:
        send(session, {"type": "finish"})


def control_submission(policy):
    submission = {"schema": "brickplan-submission/1.0", "episodes": {}, "choices": {},
                  "lookahead": {}, "counterfactual": {},
                  "metadata": {"controller": policy, "softwareValidationOnly": True,
                               "modelOrHumanResults": False}}
    for domain, tasks, costs, _ in banks():
        for task in tasks["episodes"]:
            session = Session(domain, task, seed=31)
            table = costs[str(task["goal"])]
            if policy in ("fault-and-recover", "attach-only") and task["mode"] == "full":
                cp = tasks["choices"][0]
                for action in domain.witness(0, cp["start"], domain.distances(cp["start"])):
                    send(session, session.public_action(action))
            if policy in ("oracle", "fault-and-recover"):
                if policy == "fault-and-recover" and task["mode"] in ("full", "checkpoint"):
                    cp = tasks["choices"][0]
                    if session.state == cp["start"]:
                        index = next(i for i, label in enumerate(cp["labels"]) if label["noUndoLoss"])
                        send(session, session.public_action(cp["candidates"][index]))
                if policy == "fault-and-recover" and task["mode"] == "repair":
                    # A real blocked insertion precedes the explicit diagnosis.
                    site = next(i for i in range(domain.n) if not session.state & (1 << i)
                                and domain.transition(session.state, "attach", i)[1] == "MOTION_BLOCKED")
                    send(session, session.public_action({"type": "attach", "site": site}))
                send(session, {"type": "diagnose",
                               "needsRework": no_undo(session.state, task["goal"], table) is False})
                complete(session, table)
            elif policy == "attach-only":
                # Deliberately poor software control: prefer a known trap then never detach.
                cp = tasks["choices"][0]
                if session.state == cp["start"]:
                    index = next(i for i, label in enumerate(cp["labels"]) if label["noUndoLoss"])
                    send(session, session.public_action(cp["candidates"][index]))
                while not session.terminated:
                    actions = [dict(type=op, site=site) for op, site, _ in domain.moves(session.state)
                               if op == "attach"]
                    if not actions:
                        send(session, {"type": "finish"})
                        break
                    send(session, session.public_action(actions[0]))
            else:
                raise ValueError(policy)
            submission["episodes"][task["id"]] = session.export()
        for p in tasks["choices"]:
            desired_loss = policy == "attach-only"
            submission["choices"][p["id"]] = {"choice": next(
                i for i, l in enumerate(p["labels"]) if l["noUndoLoss"] == desired_loss)}
        for p in tasks["lookahead"]:
            submission["lookahead"][p["id"]] = {"firstConflict":
                p["firstConflict"] if policy != "attach-only" else None}
        for p in tasks["counterfactual"]:
            for m in p["members"]:
                submission["counterfactual"][f"{p['id']}/{m['id']}"] = {
                    "choice": m["optimalChoices"][0] if policy != "attach-only" else 0}
    return submission


class CertificationTests(unittest.TestCase):
    def test_exhaustive_graph_and_witnesses(self):
        for domain, tasks, costs, cert in banks():
            reachable = domain.distances(0)
            for goal, table in costs.items():
                check = verify_distances(domain, int(goal), table, reachable)
                self.assertEqual(check["reachableStates"], cert["reachableStates"])
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
            self.assertEqual(cert["mandatoryOrder"]["chainLengthParts"], 4)

    def test_fail_closed_geometry_and_cost_tampering(self):
        d, _, costs, _ = banks()[0]
        for mutate in (
            lambda g: g["paths"].pop(),
            lambda g: g["paths"].append(g["paths"][0]),
            lambda g: g["paths"][0]["pairs"].pop(),
            lambda g: g["paths"][0]["pairs"][0].update(status="UNKNOWN"),
            lambda g: g["endpoints"].pop(),
            lambda g: g["endpoints"][0].update(status="BLOCKED"),
            lambda g: g["mutable"].__setitem__(0, g["mutable"][1]),
        ):
            altered = copy.deepcopy(d.geometry)
            mutate(altered)
            with self.assertRaises(ValueError):
                AssemblyDomain(altered, d.source)
        corrupted = list(costs[str(d.full)])
        corrupted[0] += 2
        with self.assertRaises(ValueError):
            verify_distances(d, d.full, corrupted, d.distances(0))

    def test_counterfactual_dynamics_and_both_required(self):
        for d, tasks, _, _ in banks():
            p = tasks["counterfactual"][0]
            for m in p["members"]:
                self.assertTrue(all(m["goal"] & (1 << a["site"]) for a in p["candidates"]))
                # Observation goals change; execution codes and occupancy do not.
                task = dict(id="cf", start=p["start"], goal=m["goal"], budget=64,
                            inspectBudget=32, diagnoseBudget=8)
                s = Session(d, task, 7)
                action = p["candidates"][0]
                expected, code = d.transition(p["start"], action["type"], action["site"])
                self.assertEqual(send(s, s.public_action(action))["result"]["code"], code)
                self.assertEqual(s.state, expected)
            for pair in ("switchPair", "invariancePair"):
                members = [m for m in p["members"] if m["id"] in p[pair]]
                self.assertEqual(members[0]["goal"].bit_count(), members[1]["goal"].bit_count())

    def test_original_sources_and_clearance_covers(self):
        # Verify every serialized CLEAR cover actually covers the entire declared path.
        for d, _, _, _ in banks():
            for path in d.geometry["paths"]:
                for pair in path["pairs"]:
                    if pair["method"] != "lipschitz-distance-cover":
                        continue
                    previous = 0
                    for low, high, mid, distance in pair["intervals"]:
                        self.assertAlmostEqual(low, previous, places=8)
                        self.assertAlmostEqual(mid, (low + high) / 2, places=8)
                        self.assertGreater(distance, (high - low) / 2 + d.geometry["guardLDU"])
                        previous = high
                    self.assertAlmostEqual(previous, path["lengthLDU"])
            self.assertFalse(d.source["provenance"]["sourceGeometryModified"])


class RuntimeTests(unittest.TestCase):
    def test_identity_equivalence_invalid_id_budget_and_replay(self):
        d, tasks, _, _ = banks()[0]
        s = Session(d, tasks["episodes"][0], 319)
        available = list(d.moves(0))
        op, site, _ = next(a for a in available if a[0] == "attach")
        equivalents = [p for p, kind in s.part_types.items() if kind == s.part_type(site)]
        chosen = next((p for p in equivalents if p != s.part_ids[site]), equivalents[0])
        self.assertEqual(send(s, {"type": op, "partId": chosen, "siteId": s.site_ids[site]})["result"]["code"], "OK")
        self.assertEqual(s.installed[site], chosen)
        send(s, {"type": "attach", "partId": "P999", "siteId": s.site_ids[site]})
        send(s, {"type": "attach", "siteId": []})
        self.assertEqual(s.attempts, 3)
        self.assertEqual(replay_export(d, s.task, s.export()).state, s.state)
        tampered = s.export()
        tampered["events"][0]["after"] = 0
        with self.assertRaises(ValueError):
            replay_export(d, s.task, tampered)
        duplicated = s.export()
        duplicated["events"].append(duplicated["events"][-1])
        with self.assertRaises(ValueError):
            replay_export(d, s.task, duplicated)

    def test_idempotency_revision_and_observation_no_answers(self):
        d, tasks, _, _ = banks()[0]
        s = Session(d, tasks["episodes"][0], 319)
        request = {"requestId": "once", "revision": 0, "action": {"type": "bad"}}
        first = s.submit(request)
        self.assertEqual(first, s.submit(request))
        self.assertEqual(s.attempts, 1)
        with self.assertRaises(ValueError):
            s.submit(dict(request, action={"type": "finish"}))
        with self.assertRaises(ValueError):
            s.submit(dict(request, requestId="stale"))
        text = json.dumps(s.observation())
        for forbidden in ("blocker", "sourceIndex", "optimal", "Witness", "minimumDetaches", "needsRework\": true"):
            self.assertNotIn(forbidden, text)
        self.assertEqual(len(s.observation()["sites"]), d.n)
        for _ in range(s.task["inspectBudget"] + 2):
            send(s, {"type": "inspect", "view": "top"})
        self.assertFalse(s.terminated)
        self.assertEqual(s.attempts, 1)
        self.assertEqual(s.inspections, s.task["inspectBudget"])

    def test_budget_failure_is_charged_and_terminal(self):
        d, tasks, _, _ = banks()[0]
        s = Session(d, tasks["episodes"][0])
        for _ in range(s.task["budget"]):
            send(s, None)
        self.assertTrue(s.terminated)
        self.assertEqual(s.attempts, s.task["budget"])
        with self.assertRaises(ValueError):
            send(s, {"type": "finish"})

    def test_persistence_and_private_route(self):
        from server import Arena
        with tempfile.TemporaryDirectory() as temporary:
            arena = Arena(temporary)
            public_id = next(iter(arena.tasks))
            result = arena.create({"taskId": public_id, "seed": 2})
            key = result["sessionId"]
            request = {"requestId": "one", "revision": 0, "action": {"type": "bad"}}
            response = arena.post(f"/api/sessions/{key}/actions", request)
            restored = Arena(temporary)
            self.assertEqual(restored.get(f"/api/sessions/{key}")["observation"], response["observation"])
            self.assertEqual(restored.post(f"/api/sessions/{key}/actions", request), response)
            with self.assertRaises(ValueError):
                restored.get(f"/api/sessions/{key}/export")
            with self.assertRaises(KeyError):
                restored.get("/data/roadster-body/costs.private.json.gz")

    def test_public_probes_hide_condition_and_permute(self):
        probe_set = ProbeSet(banks(), 219)
        self.assertEqual(len(probe_set.catalog()), 26)
        answers = {}
        for key, e in probe_set.entries.items():
            public = probe_set.get(key)
            serialized = json.dumps(public)
            for forbidden in ("conditionalCosts", "optimalChoices", "conflict/", "control/", "labels", "sourceIndex"):
                self.assertNotIn(forbidden, serialized)
            if e["kind"] == "lookahead":
                self.assertEqual(len(public["proposedPlan"]), public["horizon"])
                answers[key] = {"firstConflict": None}
            else:
                answers[key] = {"choice": 0}
        normalized, positions = probe_set.normalize(answers)
        self.assertEqual(positions, {"0": 10})
        self.assertEqual(len(normalized["lookahead"]), 16)


class MetricTests(unittest.TestCase):
    def test_oracle_and_missing_denominators(self):
        perfect = evaluate(control_submission("oracle"))
        self.assertEqual(perfect["successRate"]["value"], 1)
        self.assertEqual(perfect["recovery"]["jointDetectionAndCompletion"]["value"], 1)
        self.assertTrue(all(r["actionRegret"] == 0 and r["detachRegret"] == 0
                            for r in perfect["regretAndEfficiency"]))
        missing = evaluate({"schema": "brickplan-submission/1.0"})
        self.assertEqual(missing["successRate"]["value"], 0)
        self.assertEqual(missing["missingEpisodes"], 8)
        self.assertIsNone(missing["deadEndChoices"]["noUndoDeadEndRate"]["value"])
        self.assertEqual(missing["deadEndChoices"]["certifiedNoUndoAvoidanceAllAssigned"]["value"], 0)
        self.assertEqual(missing["lookahead"]["distanceCurve"]["8"]["exactFirstConflictAccuracy"]["value"], 0)
        curve = missing["planSurvival"]["noUndo"][0]["curve"]
        self.assertEqual((curve[-1]["lower"], curve[-1]["upper"]), (0, 1))

    def test_fault_recovery_regret_and_survival(self):
        report = evaluate(control_submission("fault-and-recover"))
        self.assertEqual(report["successRate"]["value"], 1)
        for row in report["regretAndEfficiency"]:
            self.assertEqual(row["actionRegret"], 2 * row["detachRegret"] + row["failedAttempts"])
            if row["mode"] == "repair":
                self.assertEqual(row["failedAttempts"], 1)
                self.assertTrue(row["diagnosisAfterFailedAttempt"])
                self.assertEqual(row["detachRegret"], 0)
            if row["mode"] == "full":
                self.assertIsNotNone(row["firstNoUndoLoss"])
        for entry in report["planSurvival"]["noUndo"]:
            if entry["mode"] == "full":
                self.assertEqual(entry["curve"][-1]["firstLoss"], 1)
                self.assertEqual(entry["curve"][-1]["lower"], 0)

    def test_failure_cannot_have_regret_advantage(self):
        report = evaluate(control_submission("attach-only"))
        failed = [r for r in report["regretAndEfficiency"] if not r["success"]]
        self.assertTrue(failed)
        self.assertTrue(all(r["actionRegret"] is None and r["detachRegret"] is None for r in failed))
        self.assertEqual(report["deadEndChoices"]["noUndoDeadEndRate"]["value"], 1)
        self.assertEqual(report["recovery"]["completionRate"]["value"], 0)

    def test_switching_wrong_and_invalid_answers(self):
        probes = [p for _, tasks, _, _ in banks() for p in tasks["counterfactual"]]
        wrong = {f"{p['id']}/{m['id']}": {"choice": 1 - m["optimalChoices"][0]}
                 for p in probes for m in p["members"]}
        cf = score_counterfactual(probes, wrong)
        self.assertEqual(cf["switchRateCompletePairs"]["value"], 1)
        self.assertEqual(cf["jointCorrectSwitch"]["value"], 0)
        submitted = control_submission("oracle")
        first = next(iter(submitted["lookahead"]))
        submitted["lookahead"][first] = {"firstConflict": True}
        first_choice = next(iter(submitted["choices"]))
        submitted["choices"][first_choice] = {"choice": -1}
        report = evaluate(submitted)
        self.assertEqual(report["deadEndChoices"]["invalidRate"]["numerator"], 1)
        self.assertEqual(sum(x["invalid"] for x in report["lookahead"]["distanceCurve"].values()), 1)

    def test_first_diagnosis_no_spam_or_late_credit(self):
        d, tasks, costs, _ = banks()[0]
        task = next(t for t in tasks["episodes"] if t["mode"] == "repair")
        s = Session(d, task)
        send(s, {"type": "diagnose", "needsRework": False})
        send(s, {"type": "diagnose", "needsRework": True})
        complete(s, costs[str(task["goal"])])
        self.assertFalse(episode_score(d, task, costs, s.export())["checkpointDiagnosis"])
        s = Session(d, task)
        a = d.witness(s.state, task["goal"], costs[str(task["goal"])])[0]
        send(s, s.public_action(a))
        send(s, {"type": "diagnose", "needsRework": True})
        self.assertIsNone(episode_score(d, task, costs, s.export())["checkpointDiagnosis"])


def main():
    suite = unittest.defaultTestLoader.loadTestsFromModule(__import__(__name__))
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    if not result.wasSuccessful():
        raise SystemExit(1)
    controls = {}
    for policy in ("oracle", "attach-only", "fault-and-recover"):
        submission = control_submission(policy)
        report = evaluate(submission)
        write_json(OUT / f"{policy}.submission.json", submission)
        write_json(OUT / f"{policy}.report.json", report)
        controls[policy] = {
            "successRate": report["successRate"], "recovery": report["recovery"]["completionRate"],
            "deadEndChoiceRate": report["deadEndChoices"]["noUndoDeadEndRate"],
        }
    write_json(OUT / "summary.json", {"tests": result.testsRun, "passed": True,
                                     "softwareValidationOnly": True, "controls": controls})
    print(json.dumps({"tests": result.testsRun, "controls": controls}, indent=2))


if __name__ == "__main__":
    main()
