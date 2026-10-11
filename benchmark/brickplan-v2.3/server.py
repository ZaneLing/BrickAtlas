"""Local Arena and authoritative study store; evaluator assets are never static."""
import argparse
import base64
import copy
import gzip
import hashlib
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import json
import mimetypes
from pathlib import Path
import re
import secrets
import threading
from urllib.parse import urlsplit
import zipfile

from bank import HERE, ROOT, load_oracle, make_mission, task_bank, task_by_id, write_json
from evaluate import evaluate, validate_assignments
from metrics import trajectory_metrics
from mission import canonical_hash
from probes import Probe, probe_by_id, public_mapping
from session import Session, TRACKS, replay_export


def run_config(run_id="practice", participant="reviewer", track="image-id", seed=0,
               study=False, assignments=None):
    bank = task_bank()
    return {"schema": "brickplan-run/2.0", "bankHash": canonical_hash(bank),
            "identity": {"runId": run_id, "participantId": participant, "condition": track},
            "seed": seed, "study": study, "assignments": assignments or {
                "episodes": [t["id"] for t in bank["episodes"]],
                "probes": [p["id"] for p in bank["probes"]]}}


class Arena:
    def __init__(self, store, config, render_images=True):
        self.store, self.config = Path(store), copy.deepcopy(config)
        if (config.get("schema") != "brickplan-run/2.0" or config.get("bankHash") != canonical_hash(task_bank())
                or type(config.get("seed")) is not int or not 0 <= config["seed"] < 2**32
                or type(config.get("study")) is not bool
                or set(config.get("identity", {})) != {"runId", "participantId", "condition"}
                or any(not isinstance(v, str) or not v for v in config["identity"].values())
                or config["identity"]["condition"] not in TRACKS):
            raise ValueError("Invalid run configuration")
        validate_assignments(config["assignments"])
        self.store.mkdir(parents=True, exist_ok=True)
        path = self.store / "run-config.json"
        if path.exists() and json.loads(path.read_text()) != config:
            raise ValueError("Run configuration changed; choose a fresh store")
        self.atomic("run-config.json", config)
        self.identity, self.seed = config["identity"], config["seed"]
        self.track, self.study = self.identity["condition"], config["study"]
        self.render_images, self.lock = render_images, threading.RLock()
        self.preview_lock = threading.Lock()
        # Mapping is made from the entire bank, so assignment subsets cannot reveal
        # order, tier or paired membership and do not change IDs.
        self.tasks = {k: v for k, v in public_mapping(
            [t["id"] for t in task_bank()["episodes"]], self.seed, "E").items()
            if v in config["assignments"]["episodes"]}
        self.probe_ids = {k: v for k, v in public_mapping(
            [p["id"] for p in task_bank()["probes"]], self.seed, "Q").items()
            if v in config["assignments"]["probes"]}
        self.sessions, self.probes, self.starts = {}, {}, {}
        state_path = self.store / "state.json"
        if state_path.exists():
            data = json.loads(state_path.read_text())
            self.starts = data["starts"]
            for key, record in data["sessions"].items():
                if record["taskId"] not in self.tasks.values() or record["seed"] != self.seed:
                    raise ValueError("Stored assignment mismatch")
                if record["identity"] != {**self.identity, "sessionId": key}:
                    raise ValueError("Stored run identity mismatch")
                task = task_by_id(record["taskId"])
                self.sessions[key] = replay_export(make_mission(task), task, record)
            for key, requests in data["probes"].items():
                probe = self.probe(key)
                for request in requests:
                    probe.submit(request)
        self.models = None

    def model_manager(self):
        if self.study:
            raise ValueError("Model demonstrations are outside the study run")
        if self.models is None:
            from model_runs import ModelRuns
            self.models = ModelRuns(self)
        return self.models

    def media(self, value):
        """Replace repeated base64 stimuli with immutable, content-addressed PNGs."""
        if isinstance(value, dict):
            if value.get("mime") == "image/png" and "base64" in value:
                data = base64.b64decode(value["base64"])
                name = hashlib.sha256(data).hexdigest() + ".png"
                folder = self.store / "media"
                folder.mkdir(exist_ok=True)
                path = folder / name
                if not path.exists():
                    path.write_bytes(data)
                return {k: v for k, v in value.items() if k != "base64"} | {"url": f"/media/{name}"}
            return {key: self.media(item) for key, item in value.items()}
        if isinstance(value, list):
            return [self.media(item) for item in value]
        return value

    def media_file(self, path):
        if not re.fullmatch(r"/media/[a-f0-9]{64}\.png", path):
            raise KeyError("Unknown image")
        name = path.split("/")[-1]
        local = self.store / "media" / name
        if local.exists():
            return local
        if not self.study:
            return HERE / "cases/media" / name
        raise KeyError("Unknown image")

    def atomic(self, name, data):
        target = self.store / name
        temp = target.with_suffix(".tmp")
        temp.write_text(json.dumps(data, separators=(",", ":"), allow_nan=False))
        temp.replace(target)

    def persist(self):
        self.atomic("state.json", {"starts": self.starts,
                    "sessions": {k: s.export() for k, s in self.sessions.items()},
                    "probes": {k: p.events for k, p in self.probes.items()}})

    def probe(self, key):
        if key not in self.probes:
            self.probes[key] = Probe(probe_by_id(self.probe_ids[key]), key, self.seed, self.identity)
        return self.probes[key]

    def present(self, session, revision=None):
        # Reconstruct an earlier response on an idempotent retry, including after restart.
        if revision is not None and revision != session.revision:
            original = session
            session = Session(original.mission, original.task, self.seed, self.track, identity=original.identity)
            for event in original.events[:revision]:
                session.submit(event["request"])
        session.render_images = self.render_images
        observation = session.observation()
        session.render_images = False
        observation["taskId"] = next(k for k, v in self.tasks.items() if v == session.task["id"])
        return observation

    def submission(self):
        # Practice repeats have no participant-level score; latest attempt is exported.
        episodes = {s.task["id"]: s.export() for s in self.sessions.values()}
        return {"schema": "brickplan-submission/2.0", "identity": self.identity,
                "seed": self.seed, "bankHash": self.config["bankHash"],
                "assignments": self.config["assignments"], "episodes": episodes,
                "probes": {p.probe["id"]: p.export() for p in self.probes.values() if p.answer is not None}}

    def get(self, path):
        match = re.fullmatch(r"/api/scene/preview/([EQ][0-9]{3,})", path)
        if match and not self.study:
            from scenes import preview_scene
            return preview_scene(self, match[1])
        match = re.fullmatch(r"/api/sessions/([a-f0-9]{24})/scene", path)
        if match and not self.study:
            from scenes import scene
            return scene(self.sessions[match[1]])
        match = re.fullmatch(r"/api/model-runs/([a-f0-9]{24}|case-local)/scene", path)
        if match and not self.study:
            from scenes import model_scene
            return model_scene(self, match[1])
        if path == "/api/catalogue" and not self.study:
            from catalogue import catalogue
            return catalogue(self)
        match = re.fullmatch(r"/api/preview/([EQ][0-9]{3,})", path)
        if match and not self.study:
            from catalogue import preview
            return preview(self, match[1])
        match = re.fullmatch(r"/api/probes/(Q[0-9]{3,})/review", path)
        if match and not self.study:
            from catalogue import answer_review
            return answer_review(self, match[1])
        if path == "/api/models":
            return self.model_manager().list()
        match = re.fullmatch(r"/api/model-runs/([a-f0-9]{24}|case-local)", path)
        if match:
            return self.model_manager().get(match[1])
        if path == "/api/tasks":
            return {"release": "2.3", "track": self.track, "study": self.study, "identity": self.identity,
                    "seed": self.seed, "bankHash": self.config["bankHash"],
                    "assignmentHash": canonical_hash(self.config["assignments"]),
                    "tasks": [{"id": k, **({} if self.study else {
                        "profile": task_by_id(v)["profile"], "tier": task_by_id(v)["tier"]}),
                        "sessions": [sid for sid, s in self.sessions.items() if s.task["id"] == v]}
                              for k, v in self.tasks.items()]}
        if path == "/api/probes":
            return {"probes": [{"id": k, "kind": probe_by_id(v)["kind"],
                               "answered": k in self.probes and self.probes[k].answer is not None}
                              for k, v in self.probe_ids.items()]}
        match = re.fullmatch(r"/api/probes/(Q[0-9]{3,})", path)
        if match:
            return self.probe(match[1]).public(self.render_images)
        match = re.fullmatch(r"/api/sessions/([a-f0-9]{24})(?:/(history|score|replay|review3d|export|frame/[0-9]+))?", path)
        if not match:
            raise KeyError("Unknown route")
        sid, kind = match.groups()
        session = self.sessions[sid]
        if kind is None:
            return {"sessionId": sid, "observation": self.present(session)}
        events = [{"revision": e["revision"], "attempt": e["attempt"], "action": e["request"]["action"],
                   "code": e["code"]} for e in session.events]
        if kind == "history":
            return {"events": events}
        if kind == "export":
            return {"schema": "brickplan-public-trajectory/2.0", "identity": session.identity, "events": events}
        if self.study or not session.terminated:
            raise ValueError("Scores and free review require an ended practice episode")
        if kind == "score":
            return trajectory_metrics(load_oracle(session.task["id"]), session)
        if kind == "replay":
            return {"frames": [{"code": "INITIAL", "action": None}] + events}
        if kind.startswith("frame/"):
            revision = int(kind.split("/")[1])
            if revision > session.revision:
                raise KeyError("Unknown frame")
            return {"observation": self.present(session, revision)}
        if kind == "review3d":
            from visual import meshes
            d = session.domain
            return {"scope": "Unscored practice review. Exploded poses are diagrams only.",
                    "parts": d.parts, "mutable": d.mutable, "fixed": sorted(d.fixed),
                    "meshes": {p["partNumber"]: meshes()[p["partNumber"]] for p in d.parts},
                    "siteIds": session.site_ids, "partIds": session.part_ids,
                    "goal": session.mission.goal,
                    "frames": [session.task["start"]] + [e["after"] for e in session.events]}
        raise KeyError("Unknown route")

    def post(self, path, payload):
        if path == "/api/model-runs":
            return self.model_manager().create(payload)
        match = re.fullmatch(r"/api/model-runs/([a-f0-9]{24})/(step|run|stop)", path)
        if match:
            return self.model_manager().control(*match.groups())
        if path == "/api/sessions":
            if (not isinstance(payload, dict) or set(payload) != {"taskId", "requestId"}
                    or not isinstance(payload["requestId"], str)
                    or not 1 <= len(payload["requestId"]) <= 100):
                raise ValueError("Start requires taskId and requestId; seed is fixed by the run")
            key = payload["requestId"]
            if key in self.starts:
                digest, sid = self.starts[key]
                if digest != canonical_hash(payload):
                    raise ValueError("Start request ID reused with different content")
                return {"sessionId": sid, "observation": self.present(self.sessions[sid], 0)}
            task = task_by_id(self.tasks[payload["taskId"]])
            if self.study and any(s.task["id"] == task["id"] for s in self.sessions.values()):
                raise ValueError("Study assignments may be started only once")
            sid = secrets.token_hex(12)
            session = Session(make_mission(task), task, self.seed, self.track,
                              identity={**self.identity, "sessionId": sid})
            self.sessions[sid] = session
            self.starts[key] = (canonical_hash(payload), sid)
            try:
                self.persist()
            except OSError:
                del self.sessions[sid], self.starts[key]
                raise
            return {"sessionId": sid, "observation": self.present(session)}
        match = re.fullmatch(r"/api/sessions/([a-f0-9]{24})/actions", path)
        if match:
            session = self.sessions[match[1]]
            before = session.export()
            result = session.submit(payload)
            try:
                self.persist()
            except OSError:
                self.sessions[match[1]] = replay_export(session.mission, session.task, before)
                raise
            result["observation"] = self.present(session, result["result"]["revision"])
            return result
        match = re.fullmatch(r"/api/probes/(Q[0-9]{3,})/actions", path)
        if match:
            key, probe = match[1], self.probe(match[1])
            before = copy.deepcopy(probe.events)
            result = probe.submit(payload)
            try:
                self.persist()
            except OSError:
                del self.probes[key]
                for request in before:
                    self.probe(key).submit(request)
                raise
            # Ack is immutable; caller fetches current observation separately.
            return result
        raise KeyError("Unknown route")


def portable_archive():
    """Recreate a download after extraction without recursively embedding itself."""
    path = HERE / "release/brickplan-v2.3-release.zip"
    if not path.exists():
        inventory = ROOT / "BUNDLE-MANIFEST.json"
        names = json.loads(inventory.read_text())
        path.parent.mkdir(exist_ok=True)
        temporary = path.with_suffix(".tmp")
        with zipfile.ZipFile(temporary, "w", zipfile.ZIP_DEFLATED) as archive:
            for name in [*names, "BUNDLE-MANIFEST.json"]:
                source = (ROOT / name).resolve()
                if not source.is_relative_to(ROOT.resolve()):
                    raise ValueError("Invalid bundle inventory path")
                archive.write(source, "brickplan-v2.3/" + name)
        temporary.replace(path)
    return path


def handler_for(arena):
    app = HERE / "arena/app"
    static = {"/": app / "index.html", "/play": app / "index.html",
              "/ASSET-LICENSES.json": HERE / "ASSET-LICENSES.json"}
    # Only compiled frontend assets are public; no arbitrary filesystem serving.
    for asset in (app / "assets").glob("*"):
        if asset.is_file() and asset.suffix in (".js", ".css"):
            static[f"/assets/{asset.name}"] = asset
    if not arena.study:
        for name in ("paper.pdf", "supplement.pdf", "DATASET-CARD.md", "MODEL-INTEGRATION.md", "VALIDITY.md"):
            static[f"/{name}"] = HERE / name
        for name in ("brickplan-v2.3-release.zip", "questions.jsonl", "manifest.json"):
            static[f"/download/{name}"] = HERE / "release" / name
        static["/download/brickplan-cvpr-overleaf.zip"] = ROOT / "deliverables/brickplan-paper/brickplan-cvpr-overleaf.zip"
        if not static["/download/manifest.json"].exists():
            static["/download/manifest.json"] = HERE / "data/release.json"

    class Handler(BaseHTTPRequestHandler):
        def log_message(self, *args):
            pass

        def reply(self, value, status=200):
            with arena.lock:
                value = arena.media(value)
            self.send_bytes(json.dumps(value, allow_nan=False).encode(), "application/json", status)

        def send_bytes(self, data, mime, status=200, immutable=False):
            compress = (len(data) > 1024 and "gzip" in self.headers.get("Accept-Encoding", "")
                        and (mime == "application/json" or mime in ("text/javascript", "application/javascript", "text/css")))
            if compress:
                data = gzip.compress(data, compresslevel=3, mtime=0)
            self.send_response(status)
            self.send_header("Content-Type", mime)
            if compress:
                self.send_header("Content-Encoding", "gzip")
                self.send_header("Vary", "Accept-Encoding")
            self.send_header("Cache-Control", "private, max-age=31536000, immutable" if immutable else "no-store")
            self.send_header("X-Content-Type-Options", "nosniff")
            self.send_header("Content-Length", str(len(data)))
            self.end_headers()
            try:
                self.wfile.write(data)
            except (BrokenPipeError, ConnectionResetError):
                # Navigation may cancel an in-flight HD preview response.
                pass

        def do_GET(self):
            try:
                path = urlsplit(self.path).path
                if path in static:
                    file = static[path]
                    if path == "/download/brickplan-v2.3-release.zip":
                        with arena.lock:
                            file = portable_archive()
                    self.send_bytes(file.read_bytes(), mimetypes.guess_type(str(file))[0] or "application/octet-stream",
                                    immutable=path.startswith("/assets/"))
                elif path.startswith("/media/"):
                    self.send_bytes(arena.media_file(path).read_bytes(), "image/png", immutable=True)
                elif not arena.study and re.fullmatch(r"/api/preview/[EQ][0-9]{3,}", path):
                    # Previews create independent sessions. Their CPU work must
                    # not hold the authoritative action/3D request lock.
                    with arena.preview_lock:
                        value = arena.get(path)
                    self.reply(value)
                elif not arena.study and re.fullmatch(r"/api/scene/preview/[EQ][0-9]{3,}", path):
                    self.reply(arena.get(path))
                else:
                    with arena.lock:
                        self.reply(arena.get(path))
            except (KeyError, StopIteration, FileNotFoundError):
                self.reply({"error": "Not found"}, 404)
            except (ValueError, TypeError) as exc:
                self.reply({"error": str(exc)}, 409)

        def do_POST(self):
            origin = self.headers.get("Origin")
            if origin and origin != f"http://{self.headers.get('Host')}":
                self.reply({"error": "Cross-origin request rejected"}, 403)
                return
            try:
                size = int(self.headers.get("Content-Length", "0"))
                if not 0 < size <= 65536:
                    raise ValueError("Body size must be 1..65536 bytes")
                def reject(value):
                    raise ValueError("Non-finite JSON value")
                payload = json.loads(self.rfile.read(size), parse_constant=reject)
                with arena.lock:
                    self.reply(arena.post(urlsplit(self.path).path, payload))
            except (KeyError, StopIteration):
                self.reply({"error": "Not found"}, 404)
            except (ValueError, TypeError) as exc:
                self.reply({"error": str(exc)}, 409)
            except OSError:
                self.reply({"error": "Persistence failed; request not committed"}, 503)
    return Handler


def main():
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="command", required=True)
    configure = sub.add_parser("configure")
    configure.add_argument("output", type=Path)
    configure.add_argument("--run-id", required=True)
    configure.add_argument("--participant", required=True)
    configure.add_argument("--track", choices=TRACKS, default="image-id")
    configure.add_argument("--seed", type=int, default=0)
    configure.add_argument("--assignments", type=Path)
    serve = sub.add_parser("serve")
    serve.add_argument("--config", type=Path)
    serve.add_argument("--store", type=Path, default=ROOT / "tem/brickplan-v2.3/practice")
    serve.add_argument("--port", type=int, default=8783)
    serve.add_argument("--host", default="127.0.0.1")
    collect = sub.add_parser("collect")
    collect.add_argument("--store", type=Path, required=True)
    collect.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    if args.command == "configure":
        assignments = json.loads(args.assignments.read_text()) if args.assignments else None
        config = run_config(args.run_id, args.participant, args.track, args.seed, True, assignments)
        validate_assignments(config["assignments"])
        write_json(args.output, config)
    elif args.command == "collect":
        config = json.loads((args.store / "run-config.json").read_text())
        arena = Arena(args.store, config, render_images=False)
        submission = arena.submission()
        write_json(args.output, submission)
        write_json(args.output.with_suffix(".report.json"), evaluate(submission))
    else:
        config = json.loads(args.config.read_text()) if args.config else run_config()
        arena = Arena(args.store, config)
        server = ThreadingHTTPServer((args.host, args.port), handler_for(arena))
        print(f"BrickPlan 2.3 ({arena.track}, {'study' if arena.study else 'practice'}): http://{args.host}:{args.port}", flush=True)
        server.serve_forever()


if __name__ == "__main__":
    main()
