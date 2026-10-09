"""Dependency-free model adapter. The policy receives only public observations."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from urllib.request import Request, urlopen
import uuid


class Client:
    def __init__(self, base_url="http://127.0.0.1:8766"):
        self.base_url = base_url.rstrip("/")

    def request(self, path, payload=None):
        request = Request(self.base_url + path,
                          data=None if payload is None else json.dumps(payload).encode(),
                          headers={"Content-Type": "application/json"},
                          method="GET" if payload is None else "POST")
        with urlopen(request, timeout=30) as response:
            return json.load(response)

    def tasks(self):
        return self.request("/api/tasks")["tasks"]

    def start(self, task_id, seed=0):
        return self.request("/api/sessions", {"taskId": task_id, "seed": seed})

    def act(self, session_id, observation, action, request_id=None):
        """On network uncertainty, retry with the SAME request_id and revision."""
        return self.request(f"/api/sessions/{session_id}/actions",
                            {"requestId": request_id or uuid.uuid4().hex,
                             "revision": observation["revision"], "action": action})

    def run_episode(self, task_id, policy, seed=0):
        """policy(observation, history) -> one action dict; no private solver access."""
        current = self.start(task_id, seed)
        key, obs = current["sessionId"], current["observation"]
        history = []
        max_calls = obs["actionBudget"] + obs["remainingInspections"] + obs["remainingDiagnoses"] + 1
        for _ in range(max_calls):
            if obs["terminated"]:
                break
            action = policy(obs, list(history))
            result = self.act(key, obs, action)
            history.append({"action": action, "result": result["result"]})
            obs = result["observation"]
        if not obs["terminated"]:
            self.act(key, obs, {"type": "finish"})
        return {"sessionId": key, "trajectory": self.request(f"/api/sessions/{key}/export")}

    def run_probes(self, policy):
        """policy(public_probe) -> response dict. Answers are frozen by the server."""
        for item in self.request("/api/probes")["probes"]:
            probe = self.request(f"/api/probes/{item['id']}")
            self.request(f"/api/probes/{item['id']}/answer", policy(probe))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", default="http://127.0.0.1:8766")
    parser.add_argument("--export", metavar="SESSION_ID")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    client = Client(args.url)
    data = client.request(f"/api/sessions/{args.export}/export") if args.export else client.tasks()
    text = json.dumps(data, indent=2) + "\n"
    if args.output:
        args.output.write_text(text)
    else:
        print(text)


if __name__ == "__main__":
    main()
