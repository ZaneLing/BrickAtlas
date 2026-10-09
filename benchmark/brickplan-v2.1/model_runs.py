"""Bounded live model calls over the public protocol, with durable evidence."""
import base64
import copy
from datetime import datetime, timezone
from functools import lru_cache
import hashlib
import json
import os
from pathlib import Path
import re
import secrets
import subprocess
import threading
import time
import urllib.error
import urllib.request

from bank import HERE, ROOT

SYSTEM = """You are solving BrickPlan. Inspect the supplied images and public state.
Match the target assembly and complete every work order within the budget.
Each P piece fits only its registered S site. F pieces are a clamped base.
attach/detach must follow the geometry and preserve stud support. Every detached
piece occupies one rack holder. audit completes an inspection only off assembly.
inspect acquires a camera view. finish ends your attempt.
Return ONLY one JSON object: {"action":{"type":"..."},"explanation":"one brief sentence"}.
Use exactly the action fields in the observation. No markdown. Do not invent IDs.
An invalid response consumes an action; use executor feedback to correct it.
The images are ordered: current assembly, target, rack, site reference, piece catalog.
Give an action and a short justification, not a chain of thought."""
IMAGE_ORDER = ("current", "target", "rack", "siteReference", "catalog")


@lru_cache(maxsize=4)
def fingerprint(folder):
    digest = hashlib.sha256()
    for file in sorted(Path(folder).glob("*.safetensors")):
        digest.update(file.name.encode())
        with file.open("rb") as stream:
            while block := stream.read(1024 * 1024):
                digest.update(block)
    return digest.hexdigest()


def providers():
    local = Path(os.environ.get("BRICKPLAN_LOCAL_MODEL", HERE.parent / ".runtime/models/smolvlm-256m"))
    remote = bool(os.environ.get("BRICKPLAN_API_BASE") and os.environ.get("BRICKPLAN_MODEL"))
    return [{"id": "local", "name": "SmolVLM-256M · MLX", "available": local.is_dir(),
             "model": "HuggingFaceTB/SmolVLM-256M-Instruct", "cost": "local"},
            {"id": "openai-compatible", "name": os.environ.get("BRICKPLAN_MODEL", "OpenAI-compatible API"),
             "model": os.environ.get("BRICKPLAN_MODEL"), "available": remote, "cost": "provider pricing"}]


def parse_action(raw):
    """Extract one explicit JSON object; never repair or synthesize a model action."""
    text = raw.strip()
    if text.startswith("```") and text.endswith("```"):
        text = re.sub(r"^```(?:json)?\s*", "", text)[:-3].strip()
    result = json.loads(text)
    if not isinstance(result, dict):
        raise ValueError("Expected JSON object")
    action = result.get("action")
    if not isinstance(action, dict):
        raise ValueError("Missing action object")
    return action, str(result.get("explanation", ""))[:2000]


class ModelRuns:
    def __init__(self, arena):
        self.arena = arena
        self.directory = arena.store / "model-runs"
        self.directory.mkdir(exist_ok=True)
        self.runs = {}
        for path in self.directory.glob("*.json"):
            data = json.loads(path.read_text())
            if data["status"] in ("running", "stopping"):
                data["status"] = "interrupted"
                data["stopReason"] = "Server restarted; unresolved calls are not replayed."
            self.runs[data["id"]] = data
        self.active = None

    def persist(self, run):
        self.arena.atomic(f"model-runs/{run['id']}.json", run)

    def get(self, key):
        if key == "case-local":
            return json.loads((HERE / "cases/local-vlm.json").read_text())
        return copy.deepcopy(self.runs[key])

    def list(self):
        cases = []
        if (HERE / "cases/local-vlm.json").exists():
            cases = [{"id": "case-local", "title": "SmolVLM-256M · recorded real model case",
                      "recorded": True}]
        return {"providers": providers(), "runs": [
            {k: r[k] for k in ("id", "taskId", "model", "status", "createdAt")}
            for r in self.runs.values()], "cases": cases}

    def create(self, payload):
        if (set(payload) != {"taskId", "provider", "maxCalls"} or payload["taskId"] not in self.arena.tasks
                or type(payload["maxCalls"]) is not int or not 1 <= payload["maxCalls"] <= 32):
            raise ValueError("Select an episode, provider and maxCalls in 1..32")
        provider = next((p for p in providers() if p["id"] == payload["provider"] and p["available"]), None)
        if provider is None:
            raise ValueError("Provider is unavailable; configure it on the server")
        if self.active:
            raise ValueError("Another model call is in progress")
        key = secrets.token_hex(12)
        result = self.arena.post("/api/sessions", {"taskId": payload["taskId"], "requestId": f"model-{key}"})
        run = {"schema": "brickplan-model-run/2.1", "id": key, "taskId": payload["taskId"],
               "stableTaskId": self.arena.tasks[payload["taskId"]], "sessionId": result["sessionId"],
               "bankHash": self.arena.config["bankHash"], "seed": self.arena.seed,
               "track": self.arena.track, "provider": provider["id"], "model": provider["model"],
               "createdAt": datetime.now(timezone.utc).isoformat(), "status": "paused",
               "maxCalls": payload["maxCalls"], "maxOutputTokens": 192, "temperature": 0,
               "steps": [], "initialObservation": self.arena.media(result["observation"]),
               "stopReason": None, "systemPrompt": SYSTEM,
               "scope": "Real calls, qualitative integration case only; not a population benchmark result."}
        self.runs[key] = run
        self.persist(run)
        return copy.deepcopy(run)

    def control(self, key, mode):
        run = self.runs[key]
        if mode == "stop":
            if run["status"] == "running":
                run["status"] = "stopping"
            elif run["status"] == "paused":
                self.finish(run, "user-stop")
            self.persist(run)
        elif mode in ("step", "run"):
            if run["status"] != "paused" or self.active:
                raise ValueError("Run is not paused or another model call is in progress")
            if len(run["steps"]) >= run["maxCalls"]:
                raise ValueError("Call budget exhausted")
            self.active, run["status"] = key, "running"
            self.persist(run)
            threading.Thread(target=self.work, args=(key, mode == "run"), daemon=True).start()
        else:
            raise ValueError("Unknown model control")
        return copy.deepcopy(run)

    def finish(self, run, reason):
        session = self.arena.sessions[run["sessionId"]]
        if not session.terminated:
            result = self.arena.post(f"/api/sessions/{run['sessionId']}/actions",
                                    {"requestId": f"controller-stop-{run['id']}",
                                     "revision": session.revision, "action": {"type": "finish"}})
            run["controllerTermination"] = result["result"]
        run["status"], run["stopReason"] = "ended", reason
        run["score"] = self.arena.get(f"/api/sessions/{run['sessionId']}/score")
        run["finalObservation"] = self.arena.media(self.arena.present(session))

    def inference(self, run, prompt, images):
        if run["provider"] == "local":
            model = Path(os.environ.get("BRICKPLAN_LOCAL_MODEL", HERE.parent / ".runtime/models/smolvlm-256m"))
            executable = os.environ.get("BRICKPLAN_MODEL_PYTHON", str(HERE.parent / ".runtime/mlx-env/bin/python"))
            run["modelWeightsSHA256"] = fingerprint(model)
            request = {"modelPath": str(model), "prompt": SYSTEM + "\n\n" + prompt,
                       "images": [str(self.arena.media_file(x["url"])) for x in images],
                       "maxTokens": run["maxOutputTokens"]}
            env = os.environ.copy()
            env.pop("PYTHONPATH", None)
            env["PYTHONNOUSERSITE"] = "1"
            result = subprocess.run([executable, str(HERE / "model_worker.py")],
                                    input=json.dumps(request), capture_output=True, text=True,
                                    env=env, timeout=150)
            if result.returncode:
                # Internal log, never return arbitrary stderr (paths/tokens) to the browser.
                (self.directory / f"{run['id']}.worker.log").write_text(result.stderr)
                raise ValueError("Local inference failed; inspect the server worker log")
            return json.loads(result.stdout)
        content = [{"type": "text", "text": prompt}]
        for raster in images:
            data = base64.b64encode(self.arena.media_file(raster["url"]).read_bytes()).decode()
            content.append({"type": "image_url", "image_url": {"url": f"data:image/png;base64,{data}"}})
        body = {"model": run["model"], "messages": [{"role": "system", "content": SYSTEM},
                  {"role": "user", "content": content}], "max_tokens": run["maxOutputTokens"], "temperature": 0}
        headers = {"Content-Type": "application/json"}
        if os.environ.get("BRICKPLAN_API_KEY"):
            headers["Authorization"] = "Bearer " + os.environ["BRICKPLAN_API_KEY"]
        url = os.environ["BRICKPLAN_API_BASE"].rstrip("/") + "/chat/completions"
        request = urllib.request.Request(url, data=json.dumps(body).encode(), headers=headers, method="POST")
        try:
            with urllib.request.urlopen(request, timeout=150) as response:
                result = json.load(response)
        except urllib.error.HTTPError as exc:
            raise ValueError(f"Provider HTTP {exc.code}; response body omitted") from None
        except urllib.error.URLError:
            raise ValueError("Provider connection failed") from None
        usage = result.get("usage", {})
        return {"rawOutput": result["choices"][0]["message"].get("content") or "",
                "providerRequestId": result.get("id"), "providerModel": result.get("model"),
                "usage": {"inputTokens": usage.get("prompt_tokens"), "outputTokens": usage.get("completion_tokens"),
                          "costUSD": None, "source": "provider-reported"},
                "preprocessing": "Provider-managed; HD image bytes sent without client resizing"}

    def work(self, key, continuous):
        run = self.runs[key]
        try:
            while True:
                with self.arena.lock:
                    session = self.arena.sessions[run["sessionId"]]
                    obs = self.arena.media(self.arena.present(session))
                    if run["status"] == "stopping":
                        self.finish(run, "user-stop")
                        break
                    images = [obs["images"][name] for name in IMAGE_ORDER]
                    clean = {k: v for k, v in obs.items() if k not in ("images", "inspectionHistory")}
                    # All past view pixels remain accessible in the public input record.
                    # Current view is sent on each call; last four outputs/feedback form context.
                    history = [{k: s.get(k) for k in ("rawOutput", "action", "feedback")}
                               for s in run["steps"][-4:]]
                    prompt = json.dumps({"observation": clean, "recentHistory": history}, ensure_ascii=False)
                    step = {"index": len(run["steps"]) + 1, "status": "requesting",
                            "input": {"observation": obs, "prompt": prompt, "imageOrder": list(IMAGE_ORDER)},
                            "startedAt": datetime.now(timezone.utc).isoformat()}
                    run["steps"].append(step)
                    self.persist(run)
                clock = time.monotonic()
                result = self.inference(run, prompt, images)
                with self.arena.lock:
                    step.update(result)
                    step["latencySeconds"] = round(time.monotonic() - clock, 3)
                    if run["status"] == "stopping":
                        step.update(status="cancelled", feedback={"code": "CANCELLED_BEFORE_EXECUTION"})
                        self.finish(run, "user-stop")
                        break
                    try:
                        action, explanation = parse_action(result["rawOutput"])
                        step["explanation"] = explanation
                    except (ValueError, TypeError):
                        action = {"type": "invalid-model-output"}
                        step["parseError"] = "Expected one JSON object containing an action object."
                    step["action"] = action
                    # Commit raw output before executor mutation; an interrupted call is never replayed.
                    step["status"] = "responded"
                    self.persist(run)
                    response = self.arena.post(f"/api/sessions/{run['sessionId']}/actions",
                                               {"requestId": f"{key}-{step['index']}", "revision": obs["revision"],
                                                "action": action})
                    step.update(status="executed", feedback=response["result"],
                                after=self.arena.media(response["observation"]))
                    if session.terminated or len(run["steps"]) >= run["maxCalls"]:
                        self.finish(run, "model-finish" if session.terminated else "call-budget")
                        break
                    if not continuous:
                        run["status"] = "paused"
                        break
                    self.persist(run)
        except Exception as exc:
            with self.arena.lock:
                run["status"] = "error"
                # Never include unexpected exception text from a provider or subprocess.
                run["stopReason"] = str(exc) if isinstance(exc, ValueError) else type(exc).__name__
        finally:
            with self.arena.lock:
                self.active = None
                self.persist(run)
