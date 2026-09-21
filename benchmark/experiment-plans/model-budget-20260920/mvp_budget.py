#!/usr/bin/env python3
"""Public catalog inspection and MVP budget arithmetic; never calls a model."""
import argparse
import csv
import hashlib
import json
from pathlib import Path
import re
import urllib.request

HERE = Path(__file__).resolve().parent
OUT = HERE / "mvp"
MODEL_URL = "https://openrouter.ai/api/v1/models"
IDS = {
    "astra": "openai/gpt-6-astra",
    "sol": "openai/gpt-5.6-sol",
    "luna": "openai/gpt-5.6-luna",
    "fable": "anthropic/claude-fable-5.1",
    "sonnet": "anthropic/claude-sonnet-5",
    "gemini_pro": "google/gemini-3.1-pro-preview",
    "gemini_flash": "google/gemini-3.8-flash",
    "qwen9": "qwen/qwen3.5-9b",
    "qwen27": "qwen/qwen3.5-27b",
    "intern8": None,
    "intern38": None,
    "gemma4": "google/gemma-3-4b-it",
    "gemma27": "google/gemma-3-27b-it",
    "qwen_text32": "qwen/qwen3-32b",
    "r1_distill32": "deepseek/deepseek-r1-distill-qwen-32b"
}


def save(name, value):
    (OUT / name).write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n")


def fetch(url):
    with urllib.request.urlopen(url, timeout=30) as response:
        assert response.status == 200
        return response.read()


def pick_endpoint(endpoints, model, counts):
    valid = [e for e in endpoints if e.get("status") == 0
             and int(e.get("max_completion_tokens") or 0) >= 8192]
    if not valid:
        return None
    if model.get("provider") == "OpenAI":
        pool = [e for e in valid if e.get("tag") == "openai"]
    elif model.get("provider") == "Anthropic":
        pool = [e for e in valid if e.get("tag") == "anthropic"]
    elif model.get("provider") == "Google":
        pool = [e for e in valid if "Google" in e.get("provider_name", "")
                and not any(t in e.get("tag", "") for t in ["flex", "fast", "batch"])]
    else:
        pool = [e for e in valid if e.get("quantization") in ["bf16", "fp16", "fp32"]]
    pool = pool or [e for e in valid if not any(
        word in e.get("tag", "") for word in ["flex", "fast", "batch"])] or valid
    n = counts["graph"] if model.get("track") == "graph-only" else sum(counts.values())
    inputs = 300*n + (0 if model.get("track") == "graph-only" else 2000*counts["visual"])
    return min(pool, key=lambda e: (
        inputs * float(e["pricing"]["prompt"]) + n*2048*float(e["pricing"]["completion"]),
        e.get("tag", "")
    ))


def refresh(config, catalog_path):
    raw = Path(catalog_path).read_bytes() if catalog_path else fetch(MODEL_URL)
    (OUT / "openrouter-catalog.json").write_bytes(raw)
    catalog = json.loads(raw)["data"]
    index = {r["id"]: r for r in catalog}
    rows = []
    for model in config["api_models"] + config["local_models"]:
        key, slug = model["id"], IDS[model["id"]]
        normalized = lambda value: re.sub(r"[^a-z0-9]", "", value.lower())
        related = [m["id"] for m in catalog if
                   normalized(model["name"]) in normalized(m["id"] + " " + m["name"])]
        if slug not in index and len(related) == 1:
            slug = related[0]
        row = {"id": key, "name": model["name"], "track": model.get("track", "vlm"),
               "requested_openrouter_id": slug, "listed": slug in index,
               "related_catalog_ids": related}
        if not row["listed"]:
            row.update({"route": "self-host-original-weight",
                        "reason": "Exact model not present in this catalog snapshot; not a claim of permanent unavailability.",
                        "model_metadata": None, "selected_endpoint": None})
            rows.append(row)
            continue
        meta = index[slug]
        modalities = meta["architecture"]["input_modalities"]
        assert row["track"] == "graph-only" or "image" in modalities
        row["model_metadata"] = {k: meta.get(k) for k in [
            "id", "canonical_slug", "architecture", "pricing", "supported_parameters", "reasoning"
        ]}
        url = MODEL_URL + "/" + slug + "/endpoints"
        row["endpoint_url"] = url
        try:
            cached = {
                "qwen27": "/tmp/brickatlas-or-qwen27-endpoints.json",
                "gemma4": "/tmp/brickatlas-or-gemma4-endpoints.json",
                "sol": "/tmp/brickatlas-or-sol-endpoints.json"
            }.get(key) if catalog_path else None
            endpoint_raw = Path(cached).read_bytes() if cached and Path(cached).exists() else fetch(url)
            (OUT / f"endpoints-{key}.json").write_bytes(endpoint_raw)
            row["endpoints_sha256"] = hashlib.sha256(endpoint_raw).hexdigest()
            choice = pick_endpoint(json.loads(endpoint_raw)["data"]["endpoints"], model, config["mvp"]["counts"])
            row["selected_endpoint"] = None if choice is None else {k: choice.get(k) for k in [
                "name", "tag", "provider_name", "quantization", "pricing",
                "max_completion_tokens", "supported_parameters", "status"
            ]}
        except Exception as error:
            row["selected_endpoint"] = None
            row["endpoint_read_error"] = str(error)
        row["route"] = "openrouter"
        row["price_basis"] = "selected-listed-endpoint" if row["selected_endpoint"] else "model-catalog-only"
        rows.append(row)
        print(key, row["price_basis"], flush=True)
    value = {
        "checked_on": config["price_checked_date"], "source": MODEL_URL,
        "catalog_entries": len(catalog), "catalog_sha256": hashlib.sha256(raw).hexdigest(),
        "models": rows, "listed_count": sum(r["listed"] for r in rows),
        "not_listed_count": sum(not r["listed"] for r in rows),
        "live_model_invocations": 0,
        "interpretation": "Catalog/modalities/endpoint metadata only. Listing is not account access or a successful image inference. Endpoint suggestions are a budget basis, not a frozen live routing configuration."
    }
    save("openrouter-audit.json", value)
    return value


def calculate(config, audit, include_modes):
    mvp = config["mvp"]
    counts = mvp["counts"]
    assert counts["visual"] == 2*(mvp["color_pairs"] + mvp["part_type_pairs"]) + mvp["position_panels"]
    assert counts["no_image"] == counts["visual"]
    assert counts["graph"] == 3*(mvp["strong_graph_parents"] + mvp["degree_visible_graph_parents"])
    assert mvp["repeats"] == 1
    full = sum(config["counts"].values())
    original = {r["id"]: r for r in config["api_models"] + config["local_models"]}
    scenarios = []
    for output in [2048, 8192]:
        api_usd, gpu_usd, api_requests, local_requests, device_hours = 0, 0, 0, 0, 0
        model_rows = []
        for row in audit["models"]:
            model = original[row["id"]]
            modes = 1 + (mvp["extra_mode_configurations"].count(row["id"]) if include_modes else 0)
            n = counts["graph"] if row["track"] == "graph-only" else sum(counts.values())
            calls = modes*n
            if row["route"] == "openrouter":
                selected = row["selected_endpoint"]
                pricing = selected["pricing"] if selected else row["model_metadata"]["pricing"]
                images = 0 if row["track"] == "graph-only" else counts["visual"]
                inp = n*mvp["text_tokens_per_request_budget"] + images*mvp["image_tokens_per_image_budget"]
                # Returned endpoint rates already include any advertised discount.
                cost = modes*(inp*float(pricing["prompt"]) + n*output*float(pricing["completion"]))
                api_usd += cost
                api_requests += calls
                model_rows.append({"model": row["name"], "route": "openrouter", "configurations": modes,
                                   "requests": calls, "usd": cost,
                                   "provider_tag": selected["tag"] if selected else None,
                                   "quantization": selected["quantization"] if selected else None})
            else:
                assert "devices" in model, "Missing API model needs a separately priced fallback"
                full_requests = config["counts"]["graph"] if row["track"] == "graph-only" else full
                hours = model["devices"]*(model["setup_wall_hours"] +
                    modes*model["wall_hours_per_round"]*n/full_requests)
                cost = hours*model["usd_per_device_hour"]
                gpu_usd += cost
                local_requests += calls
                device_hours += hours
                model_rows.append({"model": row["name"], "route": "self-host", "configurations": modes,
                                   "requests": calls, "device_hours_assumed": hours, "usd": cost})
        fee = max(api_usd*mvp["openrouter_credit_purchase_fee_fraction"],
                  mvp["openrouter_credit_purchase_min_fee_usd"])
        subtotal = api_usd + fee + gpu_usd + mvp["storage_usd"]
        scale = config["usd_cny_budget_assumption"]*(1+config["contingency_fraction"])
        scenarios.append({
            "billed_output_tokens_per_call": output, "model_rows": model_rows,
            "openrouter_usage_usd": api_usd, "single_credit_purchase_fee_usd": fee,
            "gpu_usd": gpu_usd, "gpu_device_hours_assumed": device_hours,
            "storage_usd": mvp["storage_usd"], "subtotal_usd": subtotal,
            "contingency_fraction": config["contingency_fraction"],
            "total_cny": subtotal*scale,
            "gpu_hours_double_total_cny": (subtotal + gpu_usd)*scale,
            "api_requests": api_requests, "local_requests": local_requests,
            "total_requests": api_requests + local_requests
        })
    return {
        "status": "mvp-budget-only-no-model-results", "all_distinct_models": len(original),
        "vlm_models": sum(m.get("track", "vlm") == "vlm" for m in original.values()),
        "text_only_models": sum(m.get("track") == "graph-only" for m in original.values()),
        "extra_mode_configurations": len(mvp["extra_mode_configurations"]) if include_modes else 0,
        "conditions_per_vlm_configuration": counts, "repeats": 1,
        "scenarios": scenarios,
        "notes": [
            "GPU preparation is paid once and is not scaled down with question count.",
            "Output length is an assumption including billed reasoning; GPU runtime is a separate unmeasured allowance.",
            "One net credit purchase is assumed: fee max(5.5% of credits, $0.80). Actual checkout and tax may differ.",
            "Selected IDs, subset answer-prior audit and exact-input human QA remain pending.",
            "No image generation, web search, training, engineering labor or human review cost is included."
        ]
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--refresh", action="store_true")
    parser.add_argument("--catalog")
    args = parser.parse_args()
    OUT.mkdir(exist_ok=True)
    config = json.loads((HERE / "config.json").read_text())
    audit = refresh(config, args.catalog) if args.refresh else json.loads((OUT / "openrouter-audit.json").read_text())
    results = {"base_all_models": calculate(config, audit, False),
               "all_models_plus_modes": calculate(config, audit, True)}
    save("budget.json", results)
    rows = results["all_models_plus_modes"]["scenarios"][0]["model_rows"]
    with (OUT / "costs-2k.csv").open("w") as stream:
        writer = csv.DictWriter(stream, fieldnames=[
            "model", "route", "configurations", "requests", "usd",
            "provider_tag", "quantization", "device_hours_assumed"
        ])
        writer.writeheader()
        writer.writerows(rows)
    for name, result in results.items():
        print(name, result["all_distinct_models"], "models", [
            (s["billed_output_tokens_per_call"], s["total_requests"], round(s["total_cny"], 2),
             round(s["gpu_hours_double_total_cny"], 2)) for s in result["scenarios"]
        ])


if __name__ == "__main__":
    main()
