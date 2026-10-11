"""Regression tests for the review's actual failure modes."""
import unittest
import copy
import tempfile

from bank import task_bank, load_oracle, make_mission
from evaluate import evaluate
from mission import canonical_hash
from probes import Probe
from quality import inverse_last
from session import Session, replay_export
from server import Arena, run_config


class QualityTests(unittest.TestCase):
    def submission(self, ids, condition="image-id"):
        bank = task_bank()
        return {"schema": "brickplan-submission/2.0", "bankHash": canonical_hash(bank),
                "identity": {"runId": "quality-test", "participantId": "software", "condition": condition},
                "assignments": {"episodes": [], "probes": ids}, "seed": 37,
                "episodes": {}, "probes": {}}

    def answer(self, submission, p):
        item = Probe(p, p["id"], submission["seed"], submission["identity"])
        answer = ({"choice": item.order.index(p["optimalChoices"][0])} if "choices" in p
                  else {"firstConflict": p["firstConflict"]})
        item.submit({"requestId": "a", "revision": 0, "action": {"type": "answer", "answer": answer}})
        submission["probes"][p["id"]] = item.export()

    def test_all_correct_calibration_does_not_raise_discriminative_score(self):
        probes = task_bank()["probes"]
        calibration = next(p for p in probes if p["scoringRole"] == "calibration")
        discriminative = next(p for p in probes if p["scoringRole"] == "discriminative")
        sub = self.submission([calibration["id"], discriminative["id"]])
        self.answer(sub, calibration)
        result = evaluate(sub)["probes"]
        self.assertEqual(result["correct"], {"numerator": 0, "denominator": 1, "value": 0})
        self.assertEqual(result["calibration"]["problemMacro"]["value"], 1)
        self.assertEqual(result["discriminative"]["sourceMacro"]["value"], 0)

    def test_missing_duplicate_is_retained_within_one_problem(self):
        groups = {}
        for p in task_bank()["probes"]:
            if p["scoringRole"] == "discriminative":
                groups.setdefault(p["canonicalProblem"], []).append(p)
        a, b = next(v[:2] for v in groups.values() if len(v) >= 2)
        sub = self.submission([a["id"], b["id"]])
        self.answer(sub, a)
        score = evaluate(sub)["probes"]["discriminative"]
        self.assertEqual(score["independentProblems"], 1)
        self.assertEqual(score["assignedRows"], 2)
        self.assertEqual(score["problemMacro"]["value"], 0.5)
        self.assertEqual(score["sourceMacro"]["value"], 0.5)

    def test_fixed_initial_views_and_active_acquisition_are_separate(self):
        p = next(p for p in task_bank()["probes"] if p["kind"] == "geometry-continuation")
        static = Probe(p, "QTEST", 37, self.submission([])["identity"])
        public = static.public(False)["observation"]
        self.assertEqual(public["observationProtocol"]["initialViews"], ["isometric", "left", "rear", "right"])
        self.assertEqual(public["observationProtocol"]["acquiredViews"], 0)
        self.assertEqual([r["view"] for r in public["inspectionHistory"]], ["left", "rear", "right"])
        request = {"requestId": "view", "revision": 0, "action": {"type": "inspect", "view": "left"}}
        with self.assertRaisesRegex(ValueError, "Static"):
            static.submit(request)
        active = Probe(p, "QTEST", 37, self.submission([], "image-id-active")["identity"])
        self.assertEqual(active.public(False)["observation"]["inspectionHistory"], [])
        active.submit(request)
        self.assertEqual(active.public(False)["observation"]["observationProtocol"]["acquiredViews"], 1)

    def test_public_inverse_rule_survives_identity_and_choice_permutation(self):
        for p in task_bank()["probes"]:
            if p["kind"] != "delayed-repair":
                continue
            for seed in (0, 37):
                item = Probe(p, "QTEST", seed, self.submission([])["identity"])
                public = item.public(False)
                index = inverse_last(public["repairContext"]["executedHistory"], public["candidates"])
                internal = item.order[index] if index is not None else None
                self.assertEqual(internal, p["inverseLastControl"]["choice"])
                self.assertNotIn("scoringRole", public)
                self.assertNotIn("recoveryCohort", public)

    def test_acquired_frame_metadata_is_independent_of_private_occupancy(self):
        task = next(t for t in task_bank()["episodes"] if t["id"] == "source-10036-05")
        graph = load_oracle(task["id"]).graph
        groups = {}
        for assembly in graph.states:
            groups.setdefault(assembly.bit_count(), []).append(assembly)
        a, b = next(values[:2] for values in groups.values() if len(values) > 1)
        request = {"requestId": "view", "revision": 0, "action": {"type": "inspect", "view": "left"}}
        for track in ("image-id", "image-id-active"):
            for seed in (0, 37):
                observations = []
                for assembly in (a, b):
                    altered = {**task, "start": {**task["start"], "assembly": assembly}}
                    session = Session(make_mission(altered), altered, seed, track)
                    response = session.submit(request)
                    self.assertEqual(response, session.submit(request))
                    restored = replay_export(session.mission, altered, session.export())
                    self.assertEqual(restored.observation(), response["observation"])
                    observations.append(response["observation"])
                # Same disclosed inventory/ledger and action; no state fingerprint.
                self.assertEqual(observations[0], observations[1])
                self.assertEqual(observations[0]["inspectionHistory"][0]["frameId"], "view-1-left")
        p = next(p for p in task_bank()["probes"] if p["taskId"] == task["id"])
        for seed in (0, 37):
            frames = []
            for assembly in (a, b):
                altered = copy.deepcopy(p)
                altered["state"]["assembly"] = assembly
                probe = Probe(altered, "QTEST", seed, self.submission([], "image-id-active")["identity"])
                probe.submit(request)
                frames.append(probe.public(False)["observation"]["inspectionHistory"])
            self.assertEqual(frames[0], frames[1])

    def test_acquired_frame_ids_survive_restart_and_idempotent_retry(self):
        for track in ("image-id", "image-id-active"):
            for seed in (0, 37):
                with tempfile.TemporaryDirectory() as folder:
                    config = run_config(track=track, seed=seed)
                    arena = Arena(folder, config, False)
                    key = next(iter(arena.tasks))
                    sid = arena.post("/api/sessions", {"taskId": key, "requestId": "start"})["sessionId"]
                    request = {"requestId": "view", "revision": 0,
                               "action": {"type": "inspect", "view": "rear"}}
                    path = f"/api/sessions/{sid}/actions"
                    response = arena.post(path, request)
                    restarted = Arena(folder, config, False)
                    self.assertEqual(response, restarted.post(path, request))
                    self.assertEqual(restarted.sessions[sid].views, 1)
                    self.assertEqual(restarted.sessions[sid].observation()["inspectionHistory"][0]["frameId"],
                                     "view-1-rear")


if __name__ == "__main__":
    unittest.main()
