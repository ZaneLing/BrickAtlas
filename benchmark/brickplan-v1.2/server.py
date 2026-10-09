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
from session import Session, replay_export, TRACKS, VIEWS

ROOT = HERE.parents[1]


class Arena:
    def __init__(self, store, probe_seed=20261005, track="image-id", study=False):
        self.banks = [load_bank(c["id"]) for c in CASES]
        self.store = Path(store)
        self.store.mkdir(parents=True, exist_ok=True)
        self.track, self.study = track, study
        run_config = {"track": track, "study": study, "probeSeed": probe_seed, "release": "1.2"}
        config_path = self.store / "run-config.json"
        if config_path.exists() and json.loads(config_path.read_text()) != run_config:
            raise ValueError("Run settings changed; use a fresh store")
        self.atomic_json("run-config.json", run_config)
        self.sessions, self.tasks, self.lock = {}, {}, threading.RLock()
        all_tasks = [(bank, t) for bank in self.banks for t in bank[1]["episodes"]]
        random.Random(924).shuffle(all_tasks)
        for i, (bank, task) in enumerate(all_tasks):
            self.tasks[f"E{i+1:03d}"] = (bank, task)
        self.probes = ProbeSet(self.banks, probe_seed, track=track, render_images=True)
        self.probe_views = {}
        views_file = self.store / "probe-views.json"
        if views_file.exists():
            self.probe_views = json.loads(views_file.read_text())
            for key, views in self.probe_views.items():
                for view in views:
                    self.probes.inspect(key, view)
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
            self.sessions[file.stem.removeprefix("session-")].render_images = True

    def atomic_json(self, name, value):
        path = self.store / name
        temporary = path.with_suffix(".tmp")
        temporary.write_text(json.dumps(value, separators=(",", ":")))
        temporary.replace(path)

    def catalog(self):
        return {"track": self.track, "study": self.study, "release": "1.2", "tasks": [
            {"id": key, "case": task["case"],
             "startType": "full build" if task["mode"] == "full" else "continuation",
             "budget": task["budget"]}
            for key, (_, task) in self.tasks.items()]}

    def create(self, payload):
        if not isinstance(payload, dict) or set(payload) - {"taskId", "seed"}:
            raise ValueError("Expected taskId and optional seed")
        bank, task = self.tasks[payload["taskId"]]
        if self.study and any(s.task["id"] == task["id"] for s in self.sessions.values()):
            raise ValueError("Study tasks may be started once per run")
        session = Session(bank[0], task, payload.get("seed", secrets.randbits(32)),
                          track=self.track, render_images=True)
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
        frame_match = re.fullmatch(r"/api/sessions/([a-f0-9]{24})/frame/([0-9]+)", path)
        if frame_match:
            session = self.sessions[frame_match[1]]
            if self.study or not session.terminated:
                raise ValueError("Review is available after a practice episode")
            n = int(frame_match[2])
            if n > len(session.events):
                raise KeyError("Unknown frame")
            replay = Session(session.domain, session.task, session.seed, track=session.track)
            for e in session.events[:n]:
                replay.submit(e["request"])
            replay.render_images = True
            return {"observation": replay.observation()}
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
            return {"schema": "brickplan-public-trajectory/1.2", "track": session.track,
                    "sessionId": match[1], "events": self.get(f"/api/sessions/{match[1]}/history")["events"]}
        if self.study:
            raise ValueError("Study scores and replay are evaluator-only")
        if action == "score":
            bank = next(b for b in self.banks if b[3]["case"] == session.task["case"])
            return episode_score(bank[0], session.task, bank[2], session.export())
        return {"frames": [{"action": None, "code": "INITIAL"}] +
                [{"action": e["request"]["action"], "code": e["code"]} for e in session.events]}

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
        match = re.fullmatch(r"/api/probes/(Q[0-9]{3})/inspect", path)
        if match and match[1] in self.probes.entries:
            key = match[1]
            if key in self.answers:
                raise ValueError("Probe already answered")
            if (not isinstance(payload, dict) or set(payload) != {"view"}
                    or payload["view"] not in VIEWS):
                raise ValueError("Expected view")
            entry = self.probes.entries[key]
            before = copy.deepcopy(entry["session"])
            result = self.probes.inspect(key, payload["view"])
            try:
                proposed = {**self.probe_views, key: self.probe_views.get(key, []) + [payload["view"]]}
                self.atomic_json("probe-views.json", proposed)
                self.probe_views = proposed
            except OSError:
                entry["session"] = before
                raise
            return {"result": result, **self.probes.get(key)}
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
        "/ASSET-LICENSES.json": HERE / "ASSET-LICENSES.json",
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
    parser.add_argument("--port", type=int, default=8768)
    parser.add_argument("--store", type=Path, default=ROOT / "tem/brickplan-v1.2/sessions")
    parser.add_argument("--probe-seed", type=int, default=20261005)
    parser.add_argument("--track", choices=TRACKS, default="image-id")
    parser.add_argument("--study", action="store_true")
    args = parser.parse_args()
    arena = Arena(args.store, args.probe_seed, args.track, args.study)
    server = ThreadingHTTPServer(("127.0.0.1", args.port), handler_for(arena))
    print(f"BrickPlan 1.2 ({args.track}): http://127.0.0.1:{args.port}", flush=True)
    server.serve_forever()


if __name__ == "__main__":
    main()
