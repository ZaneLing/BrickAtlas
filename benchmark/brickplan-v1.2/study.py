"""Provider-neutral public-observation runner and descriptive report aggregation.

No provider is contacted by default. The user supplies a JSON-over-stdin policy
command; run that process on a policy host without evaluator filesystem access.
"""
import argparse
from collections import defaultdict
import hashlib
import json
from pathlib import Path
import subprocess
import time

from client import Client


TEMPLATE = {
    "status": "unfilled; no empirical results", "participantId": None,
    "condition": None, "model": None, "provider": None, "modelVersion": None,
    "promptFile": None, "maxOutputTokens": None, "contextLimit": None,
    "reasoningSetting": None, "temperature": None, "providerCostLimitUSD": None,
    "track": "image-id", "seed": 0, "timeoutSeconds": 120,
    "policyCommand": [], "policyWorkingDirectory": None,
    "callsLog": "calls.jsonl", "url": "http://127.0.0.1:8768",
    "splitRule": "Group roadster-body and kart-deck together; airframe is the other source group.",
    "retryRule": "No automatic provider retry; preserve missing or unfinished runs on interruption.",
}


def main():
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="command", required=True)
    template = sub.add_parser("template")
    template.add_argument("output", type=Path)
    run = sub.add_parser("run")
    run.add_argument("manifest", type=Path)
    run.add_argument("--probes", action="store_true")
    run.add_argument("--task", action="append", default=[])
    analyze = sub.add_parser("analyze")
    analyze.add_argument("reports", nargs="+", type=Path)
    analyze.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    if args.command == "template":
        args.output.write_text(json.dumps(TEMPLATE, indent=2) + "\n")
    elif args.command == "analyze":
        groups = defaultdict(list)
        for path in args.reports:
            report = json.loads(path.read_text())
            meta = report["metadata"]
            key = (meta.get("condition", meta.get("policy", "unspecified")), report["track"])
            groups[key].append({"file": str(path), "success": report["successRate"],
                                "coverage": report["successRate"]["denominator"] - report["missingEpisodes"],
                                "online": report["online"]})
        args.output.write_text(json.dumps({
            "interpretation": "Descriptive repeated-run summaries; two source groups do not support reliable population inference.",
            "conditions": [{"condition": k[0], "track": k[1], "runs": v} for k,v in groups.items()],
        }, indent=2) + "\n")
    else:
        config = json.loads(args.manifest.read_text())
        required = ("participantId", "condition", "model", "provider", "modelVersion",
                    "promptFile", "maxOutputTokens", "contextLimit", "reasoningSetting",
                    "providerCostLimitUSD", "policyCommand", "policyWorkingDirectory")
        if any(config.get(k) in (None, "", []) for k in required):
            raise ValueError("Fill participant, model, prompt, budgets, and policy command before running")
        if not isinstance(config["policyCommand"], list) or not all(isinstance(x,str) for x in config["policyCommand"]):
            raise ValueError("policyCommand must be an argv list, never shell code")
        client = Client(config["url"])
        catalog = client.request("/api/tasks")
        if not catalog["study"] or catalog["track"] != config["track"]:
            raise ValueError("Use a fresh --study server with the declared observation track")
        prompt = Path(config["promptFile"]).read_text()
        prompt_hash = hashlib.sha256(prompt.encode()).hexdigest()
        log = Path(config["callsLog"])
        def policy(observation, history=None):
            payload = {"prompt": prompt, "input": observation, "history": history or [],
                       "settings": {k:config.get(k) for k in
                                    ("model","modelVersion","maxOutputTokens","contextLimit",
                                     "reasoningSetting","temperature","providerCostLimitUSD")}}
            start = time.monotonic()
            # The adapter is responsible for enforcing provider token/currency limits
            # and placing PNG base64 into the provider's image-message fields.
            result = subprocess.run(config["policyCommand"], input=json.dumps(payload),
                                    capture_output=True, text=True, timeout=config["timeoutSeconds"],
                                    cwd=config["policyWorkingDirectory"], check=True)
            answer = json.loads(result.stdout)
            with log.open("a") as f:
                f.write(json.dumps({"participantId":config["participantId"],"condition":config["condition"],
                                    "promptSha256":prompt_hash,"seconds":time.monotonic()-start,
                                    "response":answer}) + "\n")
            return answer
        if args.probes:
            client.run_probes(policy)
        else:
            selected = args.task or [t["id"] for t in catalog["tasks"]]
            for task_id in selected:
                result = client.run_episode(task_id, policy, config["seed"])
                print(json.dumps({"taskId":task_id,"sessionId":result["sessionId"]}), flush=True)


if __name__ == "__main__":
    main()
