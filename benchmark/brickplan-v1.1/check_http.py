"""Exercise every assigned episode/probe through HTTP, collection and restart."""
import json
from pathlib import Path
import tempfile
from threading import Thread
from http.server import ThreadingHTTPServer
from runtime import activate, OUT

activate()
from build import write_json
from client import Client
from collect import collect
from evaluate import evaluate
from server import Arena, handler_for
from validate_http import rejected


def main():
    with tempfile.TemporaryDirectory() as temporary:
        arena = Arena(temporary)
        server = ThreadingHTTPServer(("127.0.0.1", 0), handler_for(arena))
        thread = Thread(target=server.serve_forever, daemon=True)
        thread.start()
        client = Client(f"http://127.0.0.1:{server.server_port}")
        selected = {}
        try:
            for route in ("/data/release.json", "/data/airframe/costs.private.json.gz",
                          "/session.py", "/../engine.py"):
                rejected(client, route, None, 404)
            assert len(client.tasks()) == len(arena.tasks)
            for public_id, (_, task) in arena.tasks.items():
                response = client.start(public_id, 31)
                key, obs = response["sessionId"], response["observation"]
                assert response["taskId"] == public_id
                assert client.request(f"/api/sessions/{key}")["taskId"] == public_id
                selected[task["id"]] = key
                rejected(client, f"/api/sessions/{key}/score", None, 409)
                envelope = {"requestId": "diagnosis", "revision": obs["revision"],
                            "action": {"type": "diagnose", "needsRework": task["minimumDetaches"] > 0}}
                response = client.request(f"/api/sessions/{key}/actions", envelope)
                assert response == client.request(f"/api/sessions/{key}/actions", envelope)
                rejected(client, f"/api/sessions/{key}/actions",
                         dict(envelope, requestId="stale"), 409)
                obs = response["observation"]
                for action in task["completionWitness"]:
                    response = client.act(key, obs, arena.sessions[key].public_action(action))
                    assert response["result"]["code"] == "OK"
                    obs = response["observation"]
                if not obs["terminated"]:
                    client.act(key, obs, {"type": "finish"})
                score = client.request(f"/api/sessions/{key}/score")
                assert score["success"] and score["actionRegret"] == 0
                frames = client.request(f"/api/sessions/{key}/replay")["frames"]
                record = client.request(f"/api/sessions/{key}/export")
                assert len(frames) == len(record["events"]) + 1
                assert frames[-1]["observation"]["terminated"]
            for key, entry in arena.probes.entries.items():
                private = next(p for bank in arena.banks for p in bank[1][entry["kind"]]
                               if entry["key"].startswith(p["id"]))
                if entry["kind"] == "lookahead":
                    answer = {"firstConflict": private["firstConflict"]}
                elif entry["kind"] == "choices":
                    index = next(i for i, label in enumerate(private["labels"]) if not label["noUndoLoss"])
                    answer = {"choice": entry["order"].index(index)}
                else:
                    member = next(m for m in private["members"] if entry["key"].endswith("/" + m["id"]))
                    answer = {"choice": entry["order"].index(member["optimalChoices"][0])}
                client.request(f"/api/probes/{key}/answer", answer)
                rejected(client, f"/api/probes/{key}/answer", answer, 409)
            restored = Arena(temporary)
            for key in selected.values():
                assert restored.get(f"/api/sessions/{key}") == arena.get(f"/api/sessions/{key}")
            assert restored.answers == arena.answers
            submission = collect(Path(temporary), selected, {"softwareValidationOnly": True})
            report = evaluate(submission)
            assert report["successRate"]["value"] == 1
            assert report["counterfactual"]["jointCorrectSwitch"]["value"] == 1
            assert report["counterfactual"]["correctInvariance"]["value"] == 1
            assert all(b["exactFirstConflictAccuracy"]["value"] == 1
                       for b in report["lookahead"]["distanceCurve"].values())
            summary = {
                "passed": True, "softwareValidationOnly": True,
                "httpEpisodes": len(arena.tasks), "httpProbeResponses": len(arena.probes.entries),
                "restartRecoveredSessions": len(selected),
                "checks": ["private routes", "terminal-only scoring", "idempotent retry",
                           "revision conflict", "authoritative replay", "frozen answers",
                           "restart restoration", "collect and evaluate"],
            }
            write_json(OUT / "http-summary.json", summary)
            print(json.dumps(summary, indent=2))
        finally:
            server.shutdown()
            server.server_close()
            thread.join()


if __name__ == "__main__":
    main()
