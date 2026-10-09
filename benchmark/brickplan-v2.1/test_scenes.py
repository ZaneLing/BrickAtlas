"""Practice geometry is exact, read-only and unreachable from study routes."""
import json
from pathlib import Path
import tempfile
import unittest

from bank import HERE, make_mission, task_by_id
from scenes import scene
from server import Arena, run_config
from session import replay_export


class SceneTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.arena = Arena(self.temp.name, run_config(), False)

    def tearDown(self):
        self.temp.cleanup()

    def test_preview_is_read_only_and_preserves_source_poses(self):
        before = (Path(self.temp.name) / "state.json")
        key = next(iter(self.arena.tasks))
        public = self.arena.get(f"/api/scene/preview/{key}")
        self.assertFalse(before.exists())
        self.assertEqual(self.arena.sessions, {})
        self.assertEqual(self.arena.probes, {})
        mission = make_mission(task_by_id(self.arena.tasks[key]))
        self.assertEqual(public["parts"], mission.domain.parts)
        self.assertEqual(public["mutable"], mission.domain.mutable)
        for private in ("optimalCost", "legalActions", "labels", "graph", "optimalChoices"):
            self.assertNotIn(private, public)
        probe = next(iter(self.arena.probe_ids))
        self.arena.get(f"/api/scene/preview/{probe}")
        self.assertEqual(self.arena.probes, {})

    def test_live_frames_and_recorded_case_follow_authoritative_events(self):
        key = next(iter(self.arena.tasks))
        start = self.arena.post("/api/sessions", {"taskId": key, "requestId": "scene-test"})
        sid = start["sessionId"]
        self.arena.post(f"/api/sessions/{sid}/actions", {
            "requestId": "finish", "revision": 0, "action": {"type": "finish"}})
        frames = self.arena.get(f"/api/sessions/{sid}/scene")
        self.assertEqual(frames["frames"][-1], self.arena.sessions[sid].events[-1]["after"])
        record = json.loads((HERE / "cases/local-vlm.authoritative.json").read_text())
        task = task_by_id(record["taskId"])
        expected = scene(replay_export(make_mission(task), task, record))
        self.assertEqual(self.arena.get("/api/model-runs/case-local/scene"), expected)

    def test_study_blocks_all_scene_variants(self):
        study = Arena(Path(self.temp.name) / "study", run_config(study=True), False)
        task = next(iter(study.tasks))
        sid = study.post("/api/sessions", {"taskId": task, "requestId": "study"})["sessionId"]
        for path in (f"/api/scene/preview/{task}", f"/api/sessions/{sid}/scene",
                     "/api/model-runs/case-local/scene"):
            with self.subTest(path=path), self.assertRaises((KeyError, ValueError)):
                study.get(path)
        self.assertNotIn("meshes", study.get(f"/api/sessions/{sid}")["observation"])


if __name__ == "__main__":
    unittest.main()
