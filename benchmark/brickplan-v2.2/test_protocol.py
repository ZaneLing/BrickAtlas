"""Protocol boundaries and budget enforcement, with offline adapters only."""
import copy
import json
from pathlib import Path
import sys
import tempfile
import threading
import unittest
from unittest.mock import patch
from http.server import ThreadingHTTPServer

from bank import task_bank
from client import Client
from evaluate import evaluate
from server import Arena, handler_for, run_config
from study import Runner, TEMPLATE


class ProtocolTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.path = Path(self.temp.name)
        self.task = task_bank()["episodes"][0]
        self.p = task_bank()["probes"][0]
        self.config = run_config("test-run", "test-person", "structured", 73, True,
                                 {"episodes": [self.task["id"]], "probes": [self.p["id"]]})
        self.arena = Arena(self.path, self.config, render_images=False)
        self.key = next(iter(self.arena.tasks))
        self.qkey = next(iter(self.arena.probe_ids))

    def tearDown(self):
        self.temp.cleanup()

    def start(self):
        return self.arena.post("/api/sessions", {"requestId": "start", "taskId": self.key})

    def test_restart_idempotence_identity_and_single_start(self):
        first = self.start()
        sid = first["sessionId"]
        request = {"requestId": "view", "revision": 0, "action": {"type": "inspect", "view": "top"}}
        response = self.arena.post(f"/api/sessions/{sid}/actions", request)
        self.arena = Arena(self.path, self.config, render_images=False)
        self.assertEqual(first, self.start())
        self.assertEqual(response, self.arena.post(f"/api/sessions/{sid}/actions", request))
        self.assertEqual(self.arena.sessions[sid].views, 1)
        with self.assertRaises(ValueError):
            self.arena.post("/api/sessions", {"requestId": "again", "taskId": self.key})
        with self.assertRaises(ValueError):
            self.arena.post("/api/sessions", {"requestId": "seed", "taskId": self.key, "seed": 9})
        with self.assertRaises(ValueError):
            Arena(self.path, {**self.config, "seed": 74}, False)
        request["action"]["view"] = "front"
        with self.assertRaises(ValueError):
            self.arena.post(f"/api/sessions/{sid}/actions", request)
        report = evaluate(self.arena.submission())
        self.assertEqual(report["trajectory"]["census"]["censored"], 1)
        self.assertEqual(report["probes"]["assigned"], 1)

    def test_persistence_failure_rolls_back(self):
        sid = self.start()["sessionId"]
        before = self.arena.sessions[sid].export()
        with patch.object(self.arena, "persist", side_effect=OSError("fixture failure")):
            with self.assertRaises(OSError):
                self.arena.post(f"/api/sessions/{sid}/actions", {
                    "requestId": "bad", "revision": 0, "action": {"type": "detach", "partId": "P999"}})
        self.assertEqual(before, self.arena.sessions[sid].export())
        self.assertEqual(before, Arena(self.path, self.config, False).sessions[sid].export())

    def test_probe_multiview_normalization_and_freeze(self):
        self.config = run_config("active-test", "test-person", "image-id-active", 73, True,
                                 {"episodes": [self.task["id"]], "probes": [self.p["id"]]})
        self.path = self.path / "active"
        self.arena = Arena(self.path, self.config, render_images=False)
        probe = self.arena.probe(self.qkey)
        for i in range(12):
            request = {"requestId": f"v{i}", "revision": i, "action": {"type": "inspect", "view": "top"}}
            ack = self.arena.post(f"/api/probes/{self.qkey}/actions", request)
            self.assertEqual(ack, self.arena.post(f"/api/probes/{self.qkey}/actions", request))
        with self.assertRaises(ValueError):
            self.arena.post(f"/api/probes/{self.qkey}/actions",
                            {"requestId": "limit", "revision": 12, "action": {"type": "inspect", "view": "front"}})
        self.arena = Arena(self.path, self.config, False)
        public = self.arena.get(f"/api/probes/{self.qkey}")
        self.assertEqual(len(public["observation"]["inspectionHistory"]), 12)
        self.assertEqual(public["observation"]["remainingViews"], 0)
        self.assertNotIn("optimalChoices", public)
        request = {"requestId": "answer", "revision": 12,
                   "action": {"type": "answer", "answer": {"choice": probe.order.index(self.p["optimalChoices"][0])}}}
        ack = self.arena.post(f"/api/probes/{self.qkey}/actions", request)
        self.assertEqual(ack, self.arena.post(f"/api/probes/{self.qkey}/actions", request))
        self.assertEqual(evaluate(self.arena.submission())["probes"]["correct"]["value"], 1)
        tampered = self.arena.submission()
        tampered["probes"][self.p["id"]]["requests"][0]["action"]["view"] = "invalid"
        with self.assertRaises(ValueError):
            evaluate(tampered)
        request["requestId"] = "second"
        with self.assertRaises(ValueError):
            self.arena.post(f"/api/probes/{self.qkey}/actions", request)
        with patch.object(self.arena, "persist", side_effect=OSError):
            # Duplicate remains an ack only; failure must not corrupt frozen data.
            request["requestId"] = "answer"
            with self.assertRaises(OSError):
                self.arena.post(f"/api/probes/{self.qkey}/actions", request)
        self.assertTrue(self.arena.get(f"/api/probes/{self.qkey}")["answered"])

    def test_real_http_allowlist_and_finish(self):
        http = ThreadingHTTPServer(("127.0.0.1", 0), handler_for(self.arena))
        worker = threading.Thread(target=http.serve_forever, daemon=True)
        worker.start()
        client = Client(f"http://127.0.0.1:{http.server_port}")
        try:
            self.assertEqual(client.request("/api/tasks")["identity"], self.config["identity"])
            sid = client.request("/api/sessions", {"taskId": self.key, "requestId": "http"})["sessionId"]
            client.request(f"/api/sessions/{sid}/actions",
                           {"requestId": "finish", "revision": 0, "action": {"type": "finish"}})
            for path in ("/data/tasks.private.json", "/arena/meshes.json", "/review.js",
                         f"/api/sessions/{sid}/score", f"/api/sessions/{sid}/review3d"):
                with self.assertRaises(ValueError):
                    client.request(path)
            self.assertEqual(len(client.request(f"/api/sessions/{sid}/history")["events"]), 1)
        finally:
            http.shutdown()
            http.server_close()
            worker.join()

    def test_offline_adapter_http_collection_pipeline(self):
        http = ThreadingHTTPServer(("127.0.0.1", 0), handler_for(self.arena))
        worker = threading.Thread(target=http.serve_forever, daemon=True)
        worker.start()
        prompt = self.path / "prompt.txt"
        prompt.write_text("Offline transport fixture; not a model measurement.")
        code = (
            "import json,sys; p=json.load(sys.stdin); "
            "a={'type':'finish'} if p['input']['kind']=='episode' else "
            "{'type':'answer','answer':{'choice':0}}; "
            "print(json.dumps({'action':a,'limitsEnforced':True,'usage':"
            "{'inputTokens':8,'outputTokens':2,'costUSD':0,'providerRequestId':p['callId']}}))"
        )
        config = {**TEMPLATE, **self.config["identity"], "seed": 73,
                  "model": "fixture", "modelVersion": "0", "provider": "offline", "reasoningSetting": "none",
                  "promptFile": str(prompt), "policyWorkingDirectory": str(self.path),
                  "policyCommand": [sys.executable, "-c", code], "callsLog": str(self.path / "calls.jsonl")}
        client, runner = Client(f"http://127.0.0.1:{http.server_port}"), Runner(config)
        try:
            catalog = client.request("/api/tasks")
            runner.bind(catalog)
            client.episode(catalog["tasks"][0], runner)
            client.probe(self.qkey, runner)
            collected = Arena(self.path, self.config, False).submission()
            report = evaluate(collected)
            self.assertEqual(report["trajectory"]["census"]["terminated"], 1)
            self.assertEqual(report["trajectory"]["success"]["value"], 0)
            self.assertEqual(report["probes"]["observed"], 1)
            self.assertEqual(runner.calls, 2)
            resumed = Runner(config)
            resumed.bind(catalog)
            with self.assertRaises(ValueError):
                resumed.bind({**catalog, "assignmentHash": "changed"})
        finally:
            http.shutdown()
            http.server_close()
            worker.join()


class RunnerTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.path = Path(self.temp.name)
        (self.path / "prompt.txt").write_text("Offline fixture. Return one action.")
        self.config = {**copy.deepcopy(TEMPLATE), "runId": "r", "participantId": "p",
                       "model": "fixture", "modelVersion": "0", "provider": "offline",
                       "reasoningSetting": "none", "promptFile": str(self.path / "prompt.txt"),
                       "policyWorkingDirectory": str(self.path), "callsLog": str(self.path / "calls.jsonl"),
                       "maxInputTokens": 20, "maxOutputTokens": 10, "contextLimit": 32,
                       "totalTokensLimit": 100, "maxRequestCostUSD": 0.03, "providerCostLimitUSD": 0.05}

    def tearDown(self):
        self.temp.cleanup()

    def adapter(self, response):
        self.config["policyCommand"] = [sys.executable, "-c",
            "import json,sys; request=json.load(sys.stdin); print(" + repr(json.dumps(response)) + ")"]

    def good(self):
        return {"action": {"type": "finish"}, "limitsEnforced": True,
                "usage": {"inputTokens": 8, "outputTokens": 2, "costUSD": 0.03, "providerRequestId": "offline"}}

    def test_currency_reservation_and_resume(self):
        self.adapter(self.good())
        runner = Runner(self.config)
        self.assertEqual(runner({"taskId": "E000", "requestId": "x"}), {"type": "finish"})
        for current in (runner, Runner(self.config)):
            with self.assertRaisesRegex(ValueError, "currency"):
                current({})
        rows = [json.loads(x) for x in Path(self.config["callsLog"]).read_text().splitlines()]
        self.assertEqual(len(rows), 2)
        self.assertEqual(rows[0]["payload"]["input"]["requestId"], "x")
        self.assertIn("rawOutput", rows[1])

    def test_missing_usage_fails_closed(self):
        self.adapter({"action": {"type": "finish"}})
        runner = Runner(self.config)
        with self.assertRaisesRegex(ValueError, "usage"):
            runner({})
        with self.assertRaises(ValueError):
            runner({})
        with self.assertRaisesRegex(ValueError, "unresolved or rejected"):
            Runner(self.config)

    def test_limit_violation_and_unknown_inflight(self):
        response = self.good()
        response["usage"]["outputTokens"] = 11
        self.adapter(response)
        with self.assertRaisesRegex(ValueError, "exceeded"):
            Runner(self.config)({})
        Path(self.config["callsLog"]).unlink()
        runner = Runner(self.config)
        runner.append({"event": "request", "callId": "inflight"})
        with self.assertRaisesRegex(ValueError, "unresolved"):
            Runner(self.config)

    def test_request_and_token_preflight(self):
        self.adapter(self.good())
        self.config.update(providerCostLimitUSD=10, totalTokensLimit=29)
        with self.assertRaisesRegex(ValueError, "token budget"):
            Runner(self.config)({})
        self.assertFalse(Path(self.config["callsLog"]).exists())
        self.config.update(totalTokensLimit=100, maxRequests=1)
        runner = Runner(self.config)
        runner({})
        with self.assertRaisesRegex(ValueError, "Request budget"):
            runner({})

    def test_unavailable_is_explicit(self):
        self.adapter({"action": {"type": "finish"}})
        self.config["budgetMode"] = "unavailable"
        with self.assertRaisesRegex(ValueError, "null"):
            Runner(self.config)
        self.config.update(totalTokensLimit=None, maxRequestCostUSD=None, providerCostLimitUSD=None)
        self.assertEqual(Runner(self.config)({}), {"type": "finish"})


if __name__ == "__main__":
    unittest.main()
