#!/usr/bin/env python3
"""Lock and execute an explicit local adapter; no vendor SDK or paid call built in."""
import argparse
import base64
import json
import subprocess
import sys
from copy import deepcopy
from pathlib import Path

from common import HERE, ROOT, VERSION, canonical, digest, filehash, read, reference, write
from study import analyze, checked_packet, envelope, load_manifest


def check_settings(settings):
    required = {"output_token_limit", "temperature", "effort", "timeout_seconds",
                "image_policy", "tools", "repeats"}
    if set(settings) != required:
        raise ValueError(f"Settings must explicitly contain {sorted(required)}")
    if type(settings["output_token_limit"]) is not int or settings["output_token_limit"] < 1024:
        raise ValueError("Explicit sufficient output cap required")
    if settings["image_policy"] != "native-full-png" or settings["tools"] != [] or settings["repeats"] != 1:
        raise ValueError("Only native images, no tools and one attempt are supported")
    if type(settings["timeout_seconds"]) is not int or not 1 <= settings["timeout_seconds"] <= 3600:
        raise ValueError("Invalid timeout")
    if settings["temperature"] is not None and type(settings["temperature"]) not in (int, float):
        raise ValueError("Temperature must be numeric or explicitly unsupported null")
    if settings["effort"] not in (None, "provider-default"):
        raise ValueError("Unsupported effort comparison removed from this study")


def lock_run(model_id, revision, adapter, settings):
    planned = read(HERE / "planned-models.json")["models"]
    model = next((m for m in planned if m["id"] == model_id), None)
    if model is None:
        raise ValueError("Unknown planned model")
    if not revision or revision.lower() in ("latest", "main", "default", "preview"):
        raise ValueError("Pin an immutable model/checkpoint revision or a declared provider backend revision")
    check_settings(settings)
    adapter = Path(adapter).resolve()
    if not adapter.is_file() or not adapter.is_relative_to(HERE):
        raise ValueError("Place explicit local adapter in this new benchmark version")
    manifest = deepcopy(load_manifest())
    manifest.pop("lock_sha256")
    manifest["base_study_lock_sha256"] = read(HERE / "study-manifest.json")["lock_sha256"]
    manifest["study_id"] = f"{VERSION}-planned-{model_id}-{digest([revision, filehash(adapter)])[:12]}"
    manifest["status"] = "external-model-run-locked-uncollected"
    manifest["adapter"] = reference(adapter)
    manifest["model"] = model
    manifest["configurations"] = [
        {"id": f"{model_id}-{condition}", "kind": "model", "condition": condition,
         "revision": revision, "settings": settings, "repeats": 1}
        for condition in model["conditions"]]
    manifest["observations"] = [o for o in manifest["observations"] if o["condition"] in model["conditions"]]
    manifest["planned_runs"] = len(manifest["observations"])
    manifest["lock_sha256"] = digest(manifest)
    return manifest


def verify_run_lock(manifest):
    core = dict(manifest)
    lock = core.pop("lock_sha256")
    if digest(core) != lock:
        raise ValueError("External run lock mismatch")
    if manifest["base_study_lock_sha256"] != load_manifest()["lock_sha256"]:
        raise ValueError("External lock has stale study")
    adapter = manifest["adapter"]
    if filehash(ROOT / adapter["path"]) != adapter["sha256"]:
        raise ValueError("Adapter changed after run lock")
    for config in manifest["configurations"]:
        check_settings(config["settings"])


def collect(manifest, destination):
    verify_run_lock(manifest)
    receipts = []
    configs = {c["condition"]: c for c in manifest["configurations"]}
    adapter = ROOT / manifest["adapter"]["path"]
    for obs in manifest["observations"]:
        config = configs[obs["condition"]]
        packet = checked_packet(obs)
        # Only native text and full image bytes cross the adapter boundary.
        payload = {"model": manifest["model"]["requested_model"], "revision": config["revision"],
                   "settings": config["settings"], "native_input_sha256": obs["packet"]["sha256"],
                   "native": {k: v for k, v in packet.items() if k != "images"},
                   "images": [{"mime_type": i["mime_type"], "sha256": i["sha256"],
                               "base64": base64.b64encode((ROOT / i["path"]).read_bytes()).decode()}
                              for i in packet["images"]]}
        try:
            proc = subprocess.run([sys.executable, str(adapter)], input=canonical(payload),
                                  stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                  timeout=config["settings"]["timeout_seconds"], check=False)
            raw = proc.stdout.decode("utf8", errors="replace")
            if proc.returncode:
                receipts.append(envelope(manifest, config, obs, None, f"adapter_exit_{proc.returncode}"))
            else:
                # Preserve malformed model output for the semantic parser.
                receipts.append(envelope(manifest, config, obs, raw))
        except (OSError, subprocess.TimeoutExpired) as exc:
            receipts.append(envelope(manifest, config, obs, None, type(exc).__name__))
        write(destination, receipts)
    return receipts


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("command", choices=("lock", "collect", "analyze"))
    parser.add_argument("--model")
    parser.add_argument("--revision")
    parser.add_argument("--adapter")
    parser.add_argument("--settings")
    parser.add_argument("--lock", required=True)
    parser.add_argument("--receipts")
    parser.add_argument("--output")
    parser.add_argument("--execute-local-adapter", action="store_true")
    args = parser.parse_args()
    if args.command == "lock":
        write(args.lock, lock_run(args.model, args.revision, args.adapter, read(args.settings)))
    elif args.command == "collect":
        if not args.execute_local_adapter:
            raise SystemExit("Collection requires explicit --execute-local-adapter; no external collection has been performed.")
        collect(read(args.lock), args.receipts)
    else:
        manifest = read(args.lock)
        verify_run_lock(manifest)
        report = analyze(read(args.receipts), manifest=manifest, write_output=False)
        write(args.output, report)
