"""Provider-neutral runner with durable calls and explicit budget trust boundaries.

No provider adapter is included or invoked by default. A trusted external adapter
must enforce per-call limits before contacting its provider, encode image fields,
and report usage. Currency cannot be independently verified by this runner.
"""
import argparse
from collections import defaultdict
import hashlib
import json
import math
import os
from pathlib import Path
import subprocess
import time
import uuid

from client import Client
from session import TRACKS

TEMPLATE = {
    "schema": "brickplan-study/2.0", "runId": None, "participantId": None, "condition": "image-id",
    "seed": 0, "model": None, "modelVersion": None, "provider": None, "reasoningSetting": None,
    "temperature": 0, "promptFile": None, "policyCommand": [], "policyWorkingDirectory": None,
    "url": "http://127.0.0.1:8769", "callsLog": "calls.jsonl", "timeoutSeconds": 60,
    "maxRequests": 1000, "budgetMode": "reported-usage",
    "maxInputTokens": 24000, "maxOutputTokens": 2048, "contextLimit": 32768,
    "totalTokensLimit": 1000000, "maxRequestCostUSD": 0.10, "providerCostLimitUSD": 10,
    "usageTrust": "Trusted adapter/provider reports; not an independent billing verification.",
    "retryRule": "No automatic provider retries. Unresolved or rejected calls block resume.",
    "isolationRule": "Run policy on a separate host without evaluator files. A different cwd alone is not a sandbox.",
}


def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def positive(value, integer=False):
    return (type(value) is int if integer else type(value) in (int, float)) and math.isfinite(value) and value > 0


class Runner:
    def __init__(self, config):
        self.config = config
        required = ("runId", "participantId", "condition", "model", "modelVersion", "provider",
                    "reasoningSetting", "promptFile", "policyWorkingDirectory")
        if any(not isinstance(config.get(k), str) or not config[k] for k in required):
            raise ValueError("Fill run identity, model metadata, prompt and policy directory")
        if (config.get("schema") != "brickplan-study/2.0"
                or config["condition"] not in TRACKS
                or type(config.get("seed")) is not int or not 0 <= config["seed"] < 2**32):
            raise ValueError("Invalid study schema, condition or seed")
        command = config.get("policyCommand")
        if not isinstance(command, list) or not command or not all(isinstance(x, str) and x for x in command):
            raise ValueError("policyCommand must be a non-empty argv list")
        root = Path(__file__).resolve().parents[2]
        cwd = Path(config["policyWorkingDirectory"]).resolve()
        if not cwd.is_dir() or cwd == root or root in cwd.parents:
            raise ValueError("Use a policy directory outside the evaluator repository")
        for k in ("maxRequests", "maxInputTokens", "maxOutputTokens", "contextLimit"):
            if not positive(config.get(k), True):
                raise ValueError(f"Invalid {k}")
        if not positive(config.get("timeoutSeconds")):
            raise ValueError("Invalid adapter timeout")
        if config["maxInputTokens"] + config["maxOutputTokens"] > config["contextLimit"]:
            raise ValueError("Input and output reservation exceeds context limit")
        if config.get("budgetMode") not in ("reported-usage", "unavailable"):
            raise ValueError("Choose reported-usage or explicitly unavailable budget accounting")
        self.enforced = config["budgetMode"] == "reported-usage"
        if self.enforced:
            for k in ("totalTokensLimit", "maxRequestCostUSD", "providerCostLimitUSD"):
                if not positive(config.get(k), k == "totalTokensLimit"):
                    raise ValueError(f"Invalid {k}")
        elif any(config.get(k) is not None for k in
                 ("totalTokensLimit", "maxRequestCostUSD", "providerCostLimitUSD")):
            raise ValueError("Unavailable accounting must set aggregate token/currency limits to null")
        self.prompt = Path(config["promptFile"]).read_text()
        self.prompt_hash = hashlib.sha256(self.prompt.encode()).hexdigest()
        self.config_hash = digest(config)
        self.log = Path(config["callsLog"])
        self.log.parent.mkdir(parents=True, exist_ok=True)
        self.calls, self.tokens, self.cost = 0, 0, 0.0
        self.blocked = False
        self.assignment = None
        if self.log.exists():
            starts, results = {}, {}
            for line in self.log.read_text().splitlines():
                row = json.loads(line)
                if row["configHash"] != self.config_hash or row["promptSha256"] != self.prompt_hash:
                    raise ValueError("Call log belongs to another configuration or prompt")
                target = starts if row["event"] == "request" else results
                if row["callId"] in target:
                    raise ValueError("Duplicate call log identity")
                target[row["callId"]] = row
            if set(starts) != set(results) or any(r["status"] != "accepted" for r in results.values()):
                raise ValueError("Call log has unresolved or rejected usage; reconcile before a new run")
            self.calls = len(starts)
            assignments = [row["payload"].get("assignment") for row in starts.values()]
            if assignments:
                self.assignment = assignments[0]
                if any(value != self.assignment for value in assignments):
                    raise ValueError("Call log mixes assignment certificates")
            for row in results.values():
                usage = row.get("usage")
                if self.enforced:
                    self.tokens += usage["inputTokens"] + usage["outputTokens"]
                    self.cost += usage["costUSD"]

    def bind(self, catalog):
        c = self.config
        if (not catalog["study"] or catalog["seed"] != c["seed"]
                or catalog["identity"] != {k: c[k] for k in ("runId", "participantId", "condition")}):
            raise ValueError("Authoritative run identity, seed or study condition differs")
        assignment = {k: catalog[k] for k in ("bankHash", "assignmentHash", "seed")}
        if self.calls and self.assignment != assignment:
            raise ValueError("Cannot resume against a changed assignment certificate")
        self.assignment = assignment

    def append(self, row):
        with self.log.open("a") as file:
            file.write(json.dumps({**row, "configHash": self.config_hash, "promptSha256": self.prompt_hash},
                                  allow_nan=False) + "\n")
            file.flush()
            os.fsync(file.fileno())

    def __call__(self, observation, history=None):
        c = self.config
        if self.blocked or self.calls >= c["maxRequests"]:
            raise ValueError("Request budget exhausted or previous call unresolved")
        if self.enforced:
            if self.tokens + c["maxInputTokens"] + c["maxOutputTokens"] > c["totalTokensLimit"]:
                raise ValueError("Insufficient token budget for another full request reservation")
            if self.cost + c["maxRequestCostUSD"] > c["providerCostLimitUSD"] + 1e-12:
                raise ValueError("Insufficient currency budget for another full request reservation")
        call_id = uuid.uuid4().hex
        payload = {"schema": "brickplan-adapter-input/2.0", "callId": call_id,
                   "assignment": self.assignment,
                   "identity": {k: c[k] for k in ("runId", "participantId", "condition")},
                   "prompt": self.prompt, "input": observation, "history": history or [],
                   "settings": {k: c[k] for k in (
                       "model", "modelVersion", "provider", "temperature", "reasoningSetting",
                       "maxInputTokens", "maxOutputTokens", "contextLimit", "maxRequestCostUSD", "budgetMode")}}
        self.append({"event": "request", "callId": call_id, "timestamp": time.time(),
                     "inputHash": digest(payload), "payload": payload})
        self.calls += 1
        self.blocked = True  # Cleared only after complete, accepted and durably logged usage.
        start = time.monotonic()
        raw, stderr, usage, status, error = None, None, None, "rejected", None
        try:
            result = subprocess.run(c["policyCommand"], input=json.dumps(payload), text=True,
                                    capture_output=True, cwd=c["policyWorkingDirectory"],
                                    timeout=c["timeoutSeconds"], check=False)
            raw, stderr = result.stdout, result.stderr
            if result.returncode:
                raise ValueError(f"Adapter exited with status {result.returncode}")
            def reject(value):
                raise ValueError("Non-finite adapter JSON")
            answer = json.loads(raw, parse_constant=reject)
            if not isinstance(answer, dict) or not isinstance(answer.get("action"), dict):
                raise ValueError("Adapter must return an action object")
            usage = answer.get("usage")
            if self.enforced:
                if (not isinstance(usage, dict) or any(
                        type(usage.get(k)) is not int or usage[k] < 0 for k in ("inputTokens", "outputTokens"))
                        or type(usage.get("costUSD")) not in (int, float)
                        or not math.isfinite(usage["costUSD"]) or usage["costUSD"] < 0
                        or not isinstance(usage.get("providerRequestId"), str) or not usage["providerRequestId"]
                        or answer.get("limitsEnforced") is not True):
                    raise ValueError("Missing or invalid trusted usage/limit confirmation")
                if (usage["inputTokens"] > c["maxInputTokens"] or usage["outputTokens"] > c["maxOutputTokens"]
                        or usage["costUSD"] > c["maxRequestCostUSD"]):
                    raise ValueError("Adapter exceeded its reserved per-call limit")
                self.tokens += usage["inputTokens"] + usage["outputTokens"]
                self.cost += usage["costUSD"]
            status = "accepted"
        except subprocess.TimeoutExpired as exc:
            raw = exc.stdout.decode() if isinstance(exc.stdout, bytes) else exc.stdout
            stderr = exc.stderr.decode() if isinstance(exc.stderr, bytes) else exc.stderr
            error = "Adapter timeout; provider usage unknown"
        except (ValueError, OSError, TypeError) as exc:
            error = str(exc)
        self.append({"event": "response", "callId": call_id, "timestamp": time.time(),
                     "seconds": time.monotonic() - start, "status": status, "usage": usage,
                     "rawOutput": raw, "stderr": stderr, "error": error,
                     "outputHash": hashlib.sha256((raw or "").encode()).hexdigest()})
        if status != "accepted":
            raise ValueError(error)
        self.blocked = False
        return answer["action"]


def main():
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="command", required=True)
    template = sub.add_parser("template")
    template.add_argument("output", type=Path)
    run = sub.add_parser("run")
    run.add_argument("manifest", type=Path)
    run.add_argument("--only", choices=("episodes", "probes", "all"), default="all")
    analyze = sub.add_parser("analyze")
    analyze.add_argument("reports", nargs="+", type=Path)
    analyze.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    if args.command == "template":
        args.output.write_text(json.dumps(TEMPLATE, indent=2) + "\n")
    elif args.command == "analyze":
        groups = defaultdict(list)
        seen = set()
        for file in args.reports:
            report = json.loads(file.read_text())
            identity = report["identity"]
            key = (identity["runId"], identity["participantId"], identity["condition"])
            if key in seen:
                raise ValueError("Duplicate run; do not count a repeated file as independent evidence")
            seen.add(key)
            groups[identity["condition"]].append({
                "file": str(file), "identity": identity, "assignmentHash": report["assignmentHash"],
                "trajectory": report["trajectory"], "bySourceGroup": report["bySourceGroup"]})
        args.output.write_text(json.dumps({
            "scope": "Descriptive run summaries. Use report-specific source and canonical-problem denominators; seeds/repeated participants are not independent cases.",
            "conditions": groups}, indent=2) + "\n")
    else:
        config = json.loads(args.manifest.read_text())
        runner, client = Runner(config), Client(config["url"])
        catalog = client.request("/api/tasks")
        runner.bind(catalog)
        if args.only in ("episodes", "all"):
            for task in catalog["tasks"]:
                print(json.dumps({"taskId": task["id"], "sessionId": client.episode(task, runner)}), flush=True)
        if args.only in ("probes", "all"):
            for probe in client.request("/api/probes")["probes"]:
                if not probe["answered"]:
                    client.probe(probe["id"], runner)


if __name__ == "__main__":
    main()
