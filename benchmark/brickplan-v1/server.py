"""Local development arena. Static allowlist; no private task/oracle downloads."""
from __future__ import annotations

import argparse
import copy
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import json
import mimetypes
from pathlib import Path
import random
import re
import secrets
import threading
from urllib.parse import urlsplit

from build import HERE, load_bank
from cases import CASES
from evaluate import episode_score
from probes import ProbeSet
from session import Session, replay_export

ROOT = HERE.parents[1]


class Arena:
    def __init__(self, store, probe_seed=20260930):
        self.banks = [load_bank(c["id"]) for c in CASES]
        self.store = Path(store)
        self.store.mkdir(parents=True, exist_ok=True)
        self.sessions, self.tasks, self.lock = {}, {}, threading.RLock()
        all_tasks = [(bank, t) for bank in self.banks for t in bank[1]["episodes"]]
        random.Random(924).shuffle(all_tasks)
        for i, (bank, task) in enumerate(all_tasks):
            self.tasks[f"E{i+1:03d}"] = (bank, task)
        self.probes = ProbeSet(self.banks, probe_seed)
        self.answers = {}
        answers_file = self.store / "probe-answers.json"
        if answers_file.exists():
            saved = json.loads(answers_file.read_text())
            if saved["seed"] != probe_seed:
                raise ValueError("Stored probes use another seed; choose a fresh run directory")
            self.answers = saved["answers"]
        self.probe_seed = probe_seed
        for file in self.store.glob("session-*.json"):
            data = json.loads(file.read_text())
            bank, task = next((b, t) for b, t in self.tasks.values()
                              if t["id"] == data["taskId"])
            self.sessions[file.stem.removeprefix("session-")] = replay_export(bank[0], task, data)

    def atomic_json(self, name, value):
        path = self.store / name
        temporary = path.with_suffix(".tmp")
        temporary.write_text(json.dumps(value, separators=(",", ":")))
        temporary.replace(path)

    def catalog(self):
        return {"track": "known-pose-structured", "tasks": [
            {"id": key, "case": task["case"],
             "startType": "full build" if task["mode"] == "full" else "continuation",
             "budget": task["budget"]}
            for key, (_, task) in self.tasks.items()]}

    def create(self, payload):
        if not isinstance(payload, dict) or set(payload) - {"taskId", "seed"}:
            raise ValueError("Expected taskId and optional seed")
        bank, task = self.tasks[payload["taskId"]]
        session = Session(bank[0], task, payload.get("seed", secrets.randbits(32)))
        session_id = secrets.token_hex(12)
        self.sessions[session_id] = session
        self.atomic_json(f"session-{session_id}.json", session.export())
        return {"sessionId": session_id, "taskId": payload["taskId"], "observation": session.observation()}

    def get(self, path):
        if path == "/api/tasks":
            return self.catalog()
        if path == "/api/probes":
            return {"probes": self.probes.catalog()}
        if path.startswith("/api/probes/"):
            key = path.rsplit("/", 1)[1]
            return self.probes.get(key)
        match = re.fullmatch(r"/api/sessions/([a-f0-9]{24})(?:/(history|export|score|replay))?", path)
        if not match:
            raise KeyError("Unknown route")
        session, action = self.sessions[match[1]], match[2]
        if action is None:
            public_id = next(key for key, (_, task) in self.tasks.items()
                             if task["id"] == session.task["id"])
            return {"sessionId": match[1], "taskId": public_id, "observation": session.observation()}
        if action == "history":
            return {"events": [{"revision": e["revision"], "attempt": e["attempt"],
                                "action": e["request"]["action"], "code": e["code"]}
                               for e in session.events]}
        if not session.terminated:
            raise ValueError("Finish the episode before exporting, scoring, or reviewing it")
        if action == "export":
            return session.export()
        if action == "score":
            bank = next(b for b in self.banks if b[3]["case"] == session.task["case"])
            return episode_score(bank[0], session.task, bank[2], session.export())
        replay = Session(session.domain, session.task, session.seed)
        frames = [{"observation": replay.observation(), "action": None, "code": "INITIAL"}]
        for event in session.events:
            replay.submit(event["request"])
            frames.append({"observation": replay.observation(), "action": event["request"]["action"],
                           "code": event["code"]})
        return {"frames": frames}

    def post(self, path, payload):
        if path == "/api/sessions":
            return self.create(payload)
        match = re.fullmatch(r"/api/sessions/([a-f0-9]{24})/actions", path)
        if match:
            session = self.sessions[match[1]]
            # Roll back in-memory state too if persistence fails.
            before = copy.deepcopy(session)
            try:
                result = session.submit(payload)
                self.atomic_json(f"session-{match[1]}.json", session.export())
                return result
            except OSError:
                self.sessions[match[1]] = before
                raise
        match = re.fullmatch(r"/api/probes/(Q[0-9]{3})/answer", path)
        if match and match[1] in self.probes.entries:
            key = match[1]
            if key in self.answers:
                raise ValueError("Probe already answered; responses are frozen")
            proposed = {**self.answers, key: payload}
            self.atomic_json("probe-answers.json", {"seed": self.probe_seed, "answers": proposed})
            self.answers = proposed
            return {"recorded": True}
        raise KeyError("Unknown route")


def handler_for(arena):
    static = {
        "/": HERE / "arena/index.html",
        "/app.js": HERE / "arena/app.js",
        "/style.css": HERE / "arena/style.css",
        "/meshes.json": HERE / "arena/meshes.json",
        "/ASSET-LICENSES.json": HERE / "ASSET-LICENSES.json",
        "/vendor/three.module.js": ROOT / "node_modules/three/build/three.module.js",
        "/vendor/three.core.js": ROOT / "node_modules/three/build/three.core.js",
        "/vendor/OrbitControls.js": ROOT / "node_modules/three/examples/jsm/controls/OrbitControls.js",
    }

    class Handler(BaseHTTPRequestHandler):
        def reply(self, value, status=200):
            data = json.dumps(value, allow_nan=False).encode()
            self.send_response(status)
            self.send_header("Content-Type", "application/json")
            self.send_header("Cache-Control", "no-store")
            self.send_header("Content-Length", str(len(data)))
            self.end_headers()
            self.wfile.write(data)

        def do_GET(self):
            path = urlsplit(self.path).path
            try:
                if path in static:
                    file = static[path]
                    data = file.read_bytes()
                    self.send_response(200)
                    self.send_header("Content-Type", mimetypes.guess_type(str(file))[0] or "application/octet-stream")
                    self.send_header("Content-Length", str(len(data)))
                    self.end_headers()
                    self.wfile.write(data)
                else:
                    with arena.lock:
                        self.reply(arena.get(path))
            except (KeyError, FileNotFoundError):
                self.reply({"error": "Not found"}, 404)
            except ValueError as exc:
                self.reply({"error": str(exc)}, 409)

        def do_POST(self):
            # Same-origin browser clients and non-browser SDK clients only.
            origin = self.headers.get("Origin")
            if origin and origin != f"http://{self.headers.get('Host')}":
                self.reply({"error": "Cross-origin request rejected"}, 403)
                return
            try:
                size = int(self.headers.get("Content-Length", "0"))
                if not 0 < size <= 65536:
                    raise ValueError("Request body size must be 1..65536 bytes")
                def reject_constant(value):
                    raise ValueError(f"Non-finite JSON value: {value}")
                payload = json.loads(self.rfile.read(size), parse_constant=reject_constant)
                with arena.lock:
                    self.reply(arena.post(urlsplit(self.path).path, payload))
            except KeyError:
                self.reply({"error": "Not found"}, 404)
            except (ValueError, TypeError) as exc:
                self.reply({"error": str(exc)}, 409)
            except OSError:
                self.reply({"error": "Persistence failed; action not committed"}, 503)

    return Handler


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--port", type=int, default=8766)
    parser.add_argument("--store", type=Path, default=ROOT / "tem/brickplan-v1/sessions")
    parser.add_argument("--probe-seed", type=int, default=20260930)
    args = parser.parse_args()
    arena = Arena(args.store, args.probe_seed)
    server = ThreadingHTTPServer(("127.0.0.1", args.port), handler_for(arena))
    print(f"BrickPlan 1.0: http://127.0.0.1:{args.port}", flush=True)
    server.serve_forever()


if __name__ == "__main__":
    main()
