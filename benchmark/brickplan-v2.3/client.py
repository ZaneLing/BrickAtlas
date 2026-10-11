"""Public HTTP client; consumes only Arena observations and public identities."""
import json
import uuid
from urllib.error import HTTPError
from urllib.request import Request, urlopen


class Client:
    def __init__(self, url):
        self.url = url.rstrip("/")

    def request(self, path, payload=None):
        data = json.dumps(payload).encode() if payload is not None else None
        try:
            with urlopen(Request(self.url + path, data=data,
                                 headers={"Content-Type": "application/json"}), timeout=120) as response:
                return json.load(response)
        except HTTPError as exc:
            raise ValueError(json.load(exc).get("error", str(exc))) from exc

    def episode(self, task, policy):
        existing = task["sessions"]
        if existing:
            response = self.request(f"/api/sessions/{existing[-1]}")
        else:
            response = self.request("/api/sessions", {"taskId": task["id"], "requestId": uuid.uuid4().hex})
        sid, obs = response["sessionId"], response["observation"]
        history = self.request(f"/api/sessions/{sid}/history")["events"]
        while not obs["terminated"]:
            request_id = uuid.uuid4().hex
            action = policy({"taskId": task["id"], "sessionId": sid, "requestId": request_id,
                             "kind": "episode", "observation": obs}, history)
            result = self.request(f"/api/sessions/{sid}/actions",
                                  {"requestId": request_id, "revision": obs["revision"], "action": action})
            history.append({"revision": result["result"]["revision"], "action": action, "code": result["result"]["code"]})
            obs = result["observation"]
        return sid

    def probe(self, key, policy):
        probe = self.request(f"/api/probes/{key}")
        while not probe["answered"]:
            request_id = uuid.uuid4().hex
            action = policy({"probeId": key, "requestId": request_id, "kind": "probe", "probe": probe}, [])
            if action.get("type") not in ("inspect", "answer"):
                raise ValueError("Probe policy must return inspect or answer action")
            self.request(f"/api/probes/{key}/actions",
                         {"requestId": request_id, "revision": probe["revision"], "action": action})
            probe = self.request(f"/api/probes/{key}")
