"""Real HTTP conformance and private fixture preparation for DOM validation."""
import json
from http.server import ThreadingHTTPServer
import tempfile
import threading
from urllib.request import Request, urlopen
from urllib.error import HTTPError

from build import HERE, write_json
from server import Arena, handler_for
from session import Session

OUT = HERE.parents[1] / "tem/brickplan-v1.2/validation"


def call(base, path, data=None, status=200, headers=None):
    req = Request(base + path, data=json.dumps(data).encode() if data is not None else None,
                  headers={"Content-Type": "application/json", **(headers or {})})
    try:
        response = urlopen(req, timeout=60)
    except HTTPError as e:
        response = e
    body = response.read()
    assert response.status == status, (path, response.status, body[:200])
    return json.loads(body)


def main():
    checks = []
    for track in ("image-id", "known-pose-structured"):
        with tempfile.TemporaryDirectory() as folder:
            arena = Arena(folder, track=track, study=True)
            server = ThreadingHTTPServer(("127.0.0.1", 0), handler_for(arena))
            thread = threading.Thread(target=server.serve_forever, daemon=True)
            thread.start()
            base = f"http://127.0.0.1:{server.server_port}"
            try:
                task = call(base, "/api/tasks")["tasks"][0]["id"]
                response = call(base, "/api/sessions", {"taskId": task, "seed": 10})
                sid, obs = response["sessionId"], response["observation"]
                assert ("sites" in obs) == (track == "known-pose-structured")
                assert len(obs["images"]) == 4
                action = {"requestId":"view", "revision":0, "action":{"type":"inspect","view":"front"}}
                first = call(base, f"/api/sessions/{sid}/actions", action)
                assert first == call(base, f"/api/sessions/{sid}/actions", action)
                assert first["observation"]["remainingInspections"] == 31
                call(base, f"/api/sessions/{sid}/actions", {**action,"requestId":"stale"}, status=409)
                for path in ("/meshes.json", "/data/release.json", "/data/airframe/tasks.private.json",
                             "/vendor/three.module.js", "/../data/airframe/geometry.json"):
                    call(base, path, status=404)
                for kind in ("choices", "lookahead", "counterfactual"):
                    key = next(k for k,e in arena.probes.entries.items() if e["kind"] == kind)
                    p = call(base, f"/api/probes/{key}")
                    before = p["observation"]["remainingInspections"]
                    p = call(base, f"/api/probes/{key}/inspect", {"view":"top"})
                    assert p["observation"]["remainingInspections"] == before - 1
                    answer = {"firstConflict":None} if kind == "lookahead" else {"choice":0}
                    call(base, f"/api/probes/{key}/answer", answer)
                    call(base, f"/api/probes/{key}/answer", answer, status=409)
                    call(base, f"/api/probes/{key}/inspect", {"view":"left"}, status=409)
                call(base, f"/api/sessions/{sid}/actions",
                     {"requestId":"finish","revision":1,"action":{"type":"finish"}})
                call(base, f"/api/sessions/{sid}/score", status=409)
                call(base, f"/api/sessions/{sid}/frame/0", status=409)
                exported = call(base, f"/api/sessions/{sid}/export")
                assert all("before" not in e and "after" not in e for e in exported["events"])
                call(base, "/api/sessions", {"taskId":task,"seed":10}, status=403,
                     headers={"Origin":"http://example.invalid"})
                restored = Arena(folder, track=track, study=True)
                assert all(restored.probes.entries[k]["session"].inspections == 1
                           for k in restored.probe_views)
                checks.append({"track":track,"passed":True,"allProbeKinds":True,
                               "persistentProbeBudgets":True,"privateRoutesDenied":True})
            finally:
                server.shutdown()
                server.server_close()
    # The fixture is evaluator-only. Browser actors receive only public actions.
    base = "http://127.0.0.1:8768"
    with tempfile.TemporaryDirectory() as folder:
        arena = Arena(folder)
        fixtures = []
        for key, (bank, task) in arena.tasks.items():
            if task["mode"] not in ("repair", "reconfigure"):
                continue
            response = call(base, "/api/sessions", {"taskId": key, "seed": 31})
            local = Session(bank[0], task, 31, track="image-id")
            actions = []
            for a in task["completionWitness"]:
                action = local.public_action(a)
                actions.append(action)
                local.submit({"requestId": str(local.revision), "revision": local.revision, "action": action})
            actions.append({"type": "finish"})
            fixtures.append({"case":task["case"],"mode":task["mode"],"sessionId":response["sessionId"],
                             "actions":actions,"optimalActions":task["optimalActions"]})
    write_json(OUT / "ui-fixtures.json", {"url":base,"fixtures":fixtures})
    write_json(OUT / "http-summary.json", {"passed":True,"softwareValidationOnly":True,"checks":checks})
    print("HTTP verified both tracks; six browser fixtures prepared.", flush=True)


if __name__ == "__main__":
    main()
