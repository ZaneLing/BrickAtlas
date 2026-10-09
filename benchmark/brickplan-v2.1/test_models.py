"""Regression tests for model evidence, public-input isolation and bounded calls."""
import base64
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import json
import os
from pathlib import Path
import tempfile
import threading
import unittest
from unittest.mock import patch

from bank import task_bank
from model_runs import ModelRuns, IMAGE_ORDER, parse_action
from server import Arena, run_config


class ModelTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.task = task_bank()["episodes"][0]
        self.arena = Arena(Path(self.temp.name), run_config(assignments={"episodes": [self.task["id"]], "probes": []}), False)
        self.manager = self.arena.model_manager()
        self.key = next(iter(self.arena.tasks))
        self.provider = patch("model_runs.providers", return_value=[{"id": "local", "model": "offline-fixture", "available": True}])
        self.provider.start()
        self.original = self.arena.present
        def present(session, revision=None):
            obs = self.original(session, revision)
            # Transport-only fixture bytes; never exported as scientific evidence.
            obs["images"] = {name: {"mime": "image/png", "base64": base64.b64encode(b"test-raster").decode(),
                                     "width": 1, "height": 1} for name in IMAGE_ORDER}
            return obs
        self.arena.present = present

    def tearDown(self):
        self.provider.stop()
        self.temp.cleanup()

    def run_record(self, limit=2):
        return self.manager.create({"taskId": self.key, "provider": "local", "maxCalls": limit})

    def test_bad_output_feedback_budget_and_restart(self):
        run = self.run_record()
        seen = []
        def inference(record, prompt, images):
            seen.append(json.loads(prompt))
            self.assertNotIn("optimalCost", prompt)
            self.assertNotIn("sites", seen[-1]["observation"])
            self.assertEqual(len(images), 5)
            return {"rawOutput": "not JSON", "usage": {"inputTokens": 1, "outputTokens": 1, "costUSD": 0}}
        with patch.object(self.manager, "inference", inference):
            self.manager.work(run["id"], True)
        result = self.manager.get(run["id"])
        self.assertEqual(result["stopReason"], "call-budget")
        self.assertEqual(len(result["steps"]), 2)
        self.assertEqual(seen[1]["recentHistory"][0]["feedback"]["code"], "INVALID_ACTION")
        self.assertEqual(result["score"]["operations"], 2)
        self.assertEqual(result["score"]["success"], False)
        resumed = Arena(Path(self.temp.name), self.arena.config, False).model_manager()
        self.assertEqual(resumed.get(run["id"]), result)
        with self.assertRaises(ValueError):
            resumed.control(run["id"], "run")

    def test_stop_during_call_never_executes_returned_action(self):
        run = self.run_record()
        def inference(record, prompt, images):
            record["status"] = "stopping"
            return {"rawOutput": '{"action":{"type":"detach","partId":"P001"}}'}
        with patch.object(self.manager, "inference", inference):
            self.manager.work(run["id"], True)
        result = self.manager.get(run["id"])
        self.assertEqual(result["steps"][0]["feedback"]["code"], "CANCELLED_BEFORE_EXECUTION")
        self.assertEqual(result["score"]["operations"], 0)
        self.assertEqual(result["stopReason"], "user-stop")

    def test_study_routes_and_parser(self):
        study = Arena(Path(self.temp.name) / "study", run_config(study=True), False)
        with self.assertRaises(ValueError):
            study.model_manager()
        with self.assertRaises(KeyError):
            study.get("/api/catalogue")
        self.assertEqual(parse_action('```json\n{"action":{"type":"finish"}}\n```')[0], {"type": "finish"})
        with self.assertRaises(ValueError):
            parse_action('some prose {"action":{"type":"finish"}}')

    def test_compatible_api_sends_pixels_and_hides_key(self):
        bodies = []
        class Provider(BaseHTTPRequestHandler):
            def log_message(self, *args):
                pass
            def do_POST(self):
                bodies.append(json.loads(self.rfile.read(int(self.headers["Content-Length"]))))
                data = json.dumps({"id": "fixture-request", "model": "fixture",
                    "choices": [{"message": {"content": '{"action":{"type":"finish"}}'}}],
                    "usage": {"prompt_tokens": 12, "completion_tokens": 7}}).encode()
                self.send_response(200);self.end_headers();self.wfile.write(data)
        http = ThreadingHTTPServer(("127.0.0.1", 0), Provider)
        worker = threading.Thread(target=http.serve_forever, daemon=True);worker.start()
        try:
            run = self.run_record();run["provider"] = "openai-compatible"
            images = list(run["initialObservation"]["images"].values())
            with patch.dict(os.environ, {"BRICKPLAN_API_BASE": f"http://127.0.0.1:{http.server_port}/v1",
                                         "BRICKPLAN_API_KEY": "fixture-secret"}):
                result = self.manager.inference(run, "fixture prompt", images)
            self.assertEqual(len(bodies[0]["messages"][1]["content"]), 6)
            self.assertTrue(bodies[0]["messages"][1]["content"][1]["image_url"]["url"].startswith("data:image/png;base64,"))
            self.assertEqual(result["usage"]["outputTokens"], 7)
            self.assertNotIn("fixture-secret", json.dumps(result))
        finally:
            http.shutdown();http.server_close();worker.join()


if __name__ == "__main__":
    unittest.main()
