#!/usr/bin/env python3
"""Offline budget arithmetic and an optional tokenizer proxy; no model calls."""
import argparse
import csv
import hashlib
import json
from pathlib import Path
import statistics
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]


def save(name, value):
    (HERE / name).write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n")


def workload(tokenizer_path):
    if tokenizer_path:
        sys.path.insert(0, tokenizer_path)
    import tiktoken
    encoder = tiktoken.get_encoding("o200k_base")
    rows = {}
    for condition in ["visual", "no-image", "graph"]:
        folder = ROOT / "benchmark/ldraw-evidence-v3/wire-audit" / f"gpt41-{condition}-r1"
        values = []
        for path in sorted((folder / "requests").glob("*.json")):
            request = json.loads(path.read_text())
            texts = [
                m["content"] if isinstance(m["content"], str)
                else "\n".join(c["text"] for c in m["content"] if c["type"] == "text")
                for m in request["messages"]
            ]
            values.append(sum(len(encoder.encode(text)) for text in texts) + 12)
        expected = 219 if condition == "graph" else 347
        assert len(values) == expected
        rows[condition] = {
            "requests": len(values), "text_tokens_proxy": sum(values),
            "mean": statistics.mean(values), "max": max(values),
            "source_manifest_sha256": hashlib.sha256((folder / "manifest.json").read_bytes()).hexdigest()
        }
    result = {
        "role": "offline-text-token-proxy-not-provider-usage",
        "encoder": "o200k_base", "tiktoken_version": tiktoken.__version__,
        "assumed_message_overhead_tokens": 12, "image_tokens_included": False,
        "conditions": rows, "text_tokens_per_complete_vlm_round": sum(r["text_tokens_proxy"] for r in rows.values()),
        "provider_calls": 0
    }
    save("workload-audit.json", result)
    return result


def calculate(config):
    n_vlm = sum(config["counts"].values())
    assert n_vlm == 913
    input_tokens = (config["text_input_tokens_budget_per_vlm_round"]
                    + config["counts"]["visual"] * config["image_tokens_budget_per_observation"])
    api = {m["id"]: m for m in config["api_models"]}
    local = {m["id"]: m for m in config["local_models"]}
    model_rows = []
    for model in api.values():
        for output in config["output_token_scenarios"]:
            cost = (input_tokens * model["input_per_million"]
                    + n_vlm * output * model["output_per_million"]) / 1_000_000
            model_rows.append({
                "model": model["name"], "billed_output_tokens_per_call": output,
                "requests": n_vlm, "usd_one_round": cost,
                "cny_one_round": cost * config["usd_cny_budget_assumption"]
            })
    profiles = []
    for profile in config["profiles"]:
        repeats = profile["repeats"]
        ids_api = profile["api"] + profile["extra_api_configurations"]
        requests_api = repeats * n_vlm * len(ids_api)
        gpu_usd = 0.0
        device_hours = 0.0
        requests_local = 0
        gpu_rows = []
        for key in profile["local"]:
            model = local[key]
            runs = repeats * (1 + profile["extra_local_configurations"].count(key))
            hours = (model["setup_wall_hours"] + runs * model["wall_hours_per_round"]) * model["devices"]
            cost = hours * model["usd_per_device_hour"]
            calls = runs * (n_vlm if model["track"] == "vlm" else config["counts"]["graph"])
            gpu_usd += cost
            device_hours += hours
            requests_local += calls
            gpu_rows.append({"model": model["name"], "gpu": model["gpu"], "device_hours": hours,
                             "usd": cost, "requests": calls})
        scenarios = []
        for output in config["output_token_scenarios"]:
            api_usd = repeats * sum(
                (input_tokens * api[key]["input_per_million"]
                 + n_vlm * output * api[key]["output_per_million"]) / 1_000_000
                for key in ids_api
            )
            # GPU hours stay an explicit independent assumption, not a measured
            # consequence of the API output-token scenario.
            subtotal = api_usd + gpu_usd + profile["storage_usd"]
            reserve = subtotal * config["contingency_fraction"]
            scenarios.append({
                "billed_api_output_tokens_per_call": output,
                "api_usd": api_usd, "gpu_usd_assumed": gpu_usd,
                "storage_usd": profile["storage_usd"],
                "subtotal_usd": subtotal, "contingency_usd": reserve,
                "total_usd": subtotal + reserve,
                "total_cny": (subtotal + reserve) * config["usd_cny_budget_assumption"],
                "gpu_hours_double_total_cny": (api_usd + 2*gpu_usd + profile["storage_usd"])
                    * (1+config["contingency_fraction"]) * config["usd_cny_budget_assumption"]
            })
        profiles.append({
            "profile": profile["id"], "complete_repeats": repeats,
            "distinct_models": len(profile["api"]) + len(profile["local"]),
            "additional_mode_configurations": len(profile["extra_api_configurations"]) + len(profile["extra_local_configurations"]),
            "api_requests": requests_api, "local_requests": requests_local,
            "total_requests": requests_api + requests_local,
            "gpu_device_hours_assumed": device_hours, "gpu_rows": gpu_rows,
            "scenarios": scenarios
        })
    return {
        "status": "planning-estimate-not-observed-spend",
        "input_tokens_budget_per_vlm_round": input_tokens,
        "vlm_requests_per_round": n_vlm,
        "currency_assumption": config["usd_cny_budget_assumption"],
        "model_costs": model_rows, "profiles": profiles,
        "limitations": [
            "Output-token and GPU-time scenarios are assumptions, not measured throughput or usage.",
            "No cache, batch, free-tier or credit discounts are assumed.",
            "GPU time must be calibrated separately when reasoning length changes.",
            "Engineering labor, human qualification, taxes and paid tools are not line items.",
            "No live inference or procurement occurred."
        ]
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--tokenizer-path")
    parser.add_argument("--audit-workload", action="store_true")
    args = parser.parse_args()
    config = json.loads((HERE / "config.json").read_text())
    if args.audit_workload:
        audit = workload(args.tokenizer_path)
        assert audit["text_tokens_per_complete_vlm_round"] < config["text_input_tokens_budget_per_vlm_round"]
    result = calculate(config)
    save("budget.json", result)
    with (HERE / "api-costs.csv").open("w") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(result["model_costs"][0]))
        writer.writeheader()
        writer.writerows(result["model_costs"])
    for profile in result["profiles"]:
        print(profile["profile"], profile["total_requests"], "requests",
              [(row["billed_api_output_tokens_per_call"], round(row["total_cny"], 2),
                round(row["gpu_hours_double_total_cny"], 2)) for row in profile["scenarios"]])


if __name__ == "__main__":
    main()
