#!/usr/bin/env python3
"""Exact-input OpenAI-compatible runner; live visual inference requires completed human QA."""
import argparse
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import re
import urllib.error
import urllib.request

from common import DATA, ROOT, VERSION, DATASET, digest, load, save, sha
from qa import assets, verify_final

CODE_FILES = ["common.py", "qa.py", "run.py", "seal.py"]


def code_hashes():
    return {name: sha(Path(__file__).with_name(name)) for name in CODE_FILES}


def validate_adapter(a, live=False):
    assert set(a) == {"provider", "endpoint", "model", "model_revision", "api_revision",
                      "response_model", "max_tokens", "timeout_seconds", "temperature"}
    assert a["temperature"] == 0 and type(a["max_tokens"]) is int and 1 <= a["max_tokens"] <= 2048
    assert type(a["timeout_seconds"]) is int and 1 <= a["timeout_seconds"] <= 300
    assert all(isinstance(a[k], str) and a[k] for k in
               ["provider", "endpoint", "model", "model_revision", "api_revision", "response_model"])
    assert a["endpoint"].startswith("https://") or a["endpoint"].startswith("http://127.0.0.1:")
    assert "@" not in a["endpoint"], "No credentials in endpoint"
    if live:
        assert not any(re.search("REQUIRED|PLACEHOLDER|EXAMPLE", str(v), re.I) for v in a.values())


def request_bytes(wire, adapter):
    # No canonical identity, arm, family, gold, pairing, source records, or render instruction is serialized.
    body = {"model": adapter["model"], "messages": wire["messages"], "temperature": adapter["temperature"],
            "max_tokens": adapter["max_tokens"], "stream": False}
    return (json.dumps(body, ensure_ascii=True, separators=(",", ":")) + "\n").encode()


def parse_receipt(receipt, options, adapter):
    if receipt is None:
        return {"answer": None, "valid_format": False, "failure_reason": "missing-receipt", "output": None}
    if "transport_error" in receipt:
        assert receipt["raw_response"] is None and receipt["http_status"] is None
        return {"answer": None, "valid_format": False,
                "failure_reason": "timeout" if receipt["transport_error"] == "timeout" else "api-error", "output": None}
    assert type(receipt["http_status"]) is int and isinstance(receipt["raw_response"], str)
    raw = None
    try:
        raw = json.loads(receipt["raw_response"])
    except (ValueError, TypeError):
        pass
    if not 200 <= receipt["http_status"] < 300:
        return {"answer": None, "valid_format": False, "failure_reason": "api-error", "output": None}
    if not isinstance(raw, dict):
        return {"answer": None, "valid_format": False, "failure_reason": "invalid-provider-response", "output": None}
    assert raw.get("model") == adapter["response_model"], "Served model differs from pinned response revision"
    choices = raw.get("choices")
    message = choices[0].get("message", {}) if isinstance(choices, list) and choices and isinstance(choices[0], dict) else {}
    output = message.get("content")
    if message.get("refusal"):
        return {"answer": None, "valid_format": False, "failure_reason": "refusal", "output": output}
    if not isinstance(output, str):
        return {"answer": None, "valid_format": False, "failure_reason": "missing-output", "output": None}
    try:
        # Duplicate keys, NaN and additional prose are invalid, not silently normalized.
        def pairs(items):
            if len({k for k, _ in items}) != len(items):
                raise ValueError("duplicate key")
            return dict(items)
        answer = json.loads(output, object_pairs_hook=pairs,
                            parse_constant=lambda _: (_ for _ in ()).throw(ValueError("nonfinite")))
    except (ValueError, TypeError):
        return {"answer": None, "valid_format": False, "failure_reason": "invalid-json", "output": output}
    valid = (isinstance(answer, dict) and set(answer) == {"choiceId"}
             and isinstance(answer["choiceId"], str) and answer["choiceId"] in options)
    return {"answer": answer if valid else None, "valid_format": valid,
            "failure_reason": None if valid else "invalid-format", "output": output}


def write_new(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("xb") as f:
        f.write(data)


def run(directory, adapter, qa_path=None, live=False, role="primary"):
    validate_adapter(adapter, live)
    m, obs, wires = assets()
    qa = verify_final(qa_path, role) if live else None
    if live:
        api_key = os.environ.get("BRICKATLAS_API_KEY")
        assert api_key, "Set BRICKATLAS_API_KEY outside the run artifacts"
        assert qa["raw_review_count"] >= 560
    dest = Path(directory).resolve()
    assert not dest.exists(), "Never overwrite or resume a run; create a new run directory"
    dest.mkdir(parents=True)
    ids = [o["observation_id"] for o in m["observations"] if role == "all" or o["role"] == "primary"]
    started = datetime.now(timezone.utc).isoformat()
    if qa:
        for row in qa["rows"]:
            for r in row["reviews"] + ([row["adjudication"]] if row["adjudication"] else []):
                assert datetime.fromisoformat(r["timestamp"].replace("Z", "+00:00")) <= datetime.fromisoformat(started)
    manifest = {"dataset": DATASET, "analysis_version": VERSION,
        "mode": "live-inference" if live else "offline-dry-run", "status": "running", "started": started,
        "adapter": adapter, "adapter_hash": digest(adapter), "index_sha256": sha(DATA / "observation-index.json"),
        "code_hashes": code_hashes(), "role": role, "observation_ids": ids, "calls": 0,
        "qa": {"file": str(Path(qa_path).resolve()), "sha256": sha(qa_path)} if qa else None, "requests": []}
    for oid in ids:
        w = wires[oid]
        path = dest / "requests" / (oid + ".json")
        write_new(path, request_bytes(load(ROOT / w["file"]), adapter))
        manifest["requests"].append({"observation_id": oid, "file": str(path.relative_to(dest)),
            "sha256": sha(path), "wire_observation_sha256": w["wire_observation_sha256"]})
    save(dest / "manifest.json", manifest)
    if live:
        for r in manifest["requests"]:
            receipt = {"observation_id": r["observation_id"], "request_sha256": r["sha256"],
                       "evidence_kind": "provider-http-receipt", "started": datetime.now(timezone.utc).isoformat()}
            request = urllib.request.Request(adapter["endpoint"], data=(dest / r["file"]).read_bytes(),
                headers={"Authorization": "Bearer " + api_key, "Content-Type": "application/json"}, method="POST")
            try:
                with urllib.request.urlopen(request, timeout=adapter["timeout_seconds"]) as response:
                    receipt.update(http_status=response.status, raw_response=response.read().decode("utf-8", errors="replace"))
            except urllib.error.HTTPError as error:
                receipt.update(http_status=error.code, raw_response=error.read().decode("utf-8", errors="replace"))
            except (urllib.error.URLError, TimeoutError, OSError) as error:
                receipt.update(http_status=None, raw_response=None,
                               transport_error="timeout" if "timed out" in str(error).lower() else "connection-error")
            receipt["finished"] = datetime.now(timezone.utc).isoformat()
            save(dest / "receipts" / (r["observation_id"] + ".json"), receipt, immutable=True)
            manifest["calls"] += 1
            save(dest / "manifest.json", manifest)
    manifest["status"] = "complete" if live else "dry-run-complete"
    manifest["finished"] = datetime.now(timezone.utc).isoformat()
    save(dest / "manifest.json", manifest)
    return manifest


def verify(directory):
    directory = Path(directory).resolve()
    manifest = load(directory / "manifest.json")
    assert manifest["dataset"] == DATASET and manifest["analysis_version"] == VERSION
    assert manifest["mode"] in ["offline-dry-run", "live-inference"], "No synthetic or legacy run can register"
    assert manifest["index_sha256"] == sha(DATA / "observation-index.json")
    assert manifest["code_hashes"] == code_hashes(), "Run code changed"
    adapter = manifest["adapter"]
    live = manifest["mode"] == "live-inference"
    validate_adapter(adapter, live)
    assert digest(adapter) == manifest["adapter_hash"]
    m, obs, wires = assets()
    assert manifest["role"] in ["primary", "all"]
    ids = [o["observation_id"] for o in m["observations"] if manifest["role"] == "all" or o["role"] == "primary"]
    assert manifest["observation_ids"] == ids
    assert len(manifest["requests"]) == len(ids) and {r["observation_id"] for r in manifest["requests"]} == set(ids)
    if live:
        assert manifest["status"] in ["running", "complete"] and manifest["qa"]
        assert sha(manifest["qa"]["file"]) == manifest["qa"]["sha256"]
        verified_qa = verify_final(manifest["qa"]["file"], manifest["role"])
        for r in verified_qa["rows"]:
            for raw in r["reviews"] + ([r["adjudication"]] if r["adjudication"] else []):
                assert datetime.fromisoformat(raw["timestamp"].replace("Z", "+00:00")) <= datetime.fromisoformat(manifest["started"])
    else:
        assert manifest["status"] == "dry-run-complete" and manifest["calls"] == 0 and manifest["qa"] is None
    receipt_files = list((directory / "receipts").glob("*.json"))
    assert all(p.stem in ids for p in receipt_files), "Unknown receipt"
    assert 0 <= len(receipt_files) <= manifest["calls"] <= len(ids)
    if not live:
        assert not receipt_files
    if live and manifest["status"] == "complete":
        assert manifest["calls"] == len(ids), "Incomplete planned call universe"
    rows = []
    for r in manifest["requests"]:
        oid, o = r["observation_id"], obs[r["observation_id"]]
        assert r["file"] == f"requests/{oid}.json"
        assert sha(directory / r["file"]) == r["sha256"]
        assert r["wire_observation_sha256"] == wires[oid]["wire_observation_sha256"]
        assert (directory / r["file"]).read_bytes() == request_bytes(load(ROOT / wires[oid]["file"]), adapter)
        receipt_path = directory / "receipts" / (oid + ".json")
        receipt = load(receipt_path) if receipt_path.exists() else None
        if receipt:
            assert live and receipt["evidence_kind"] == "provider-http-receipt"
            assert receipt["observation_id"] == oid and receipt["request_sha256"] == r["sha256"]
            assert datetime.fromisoformat(receipt["started"]) >= datetime.fromisoformat(manifest["started"])
            assert datetime.fromisoformat(receipt["finished"]) >= datetime.fromisoformat(receipt["started"])
        parsed = parse_receipt(receipt, [p["id"] for p in o["payload"]["options"]], adapter)
        rows.append({"observation_id": oid, "parent_task_id": o["parent_task_id"], "source_id": o["source_id"],
            "family": o["family"], "display_name": o["display_name"], "role": o["role"], "arm": o["arm"],
            "gold": o["gold"], "request_sha256": r["sha256"],
            "wire_observation_sha256": r["wire_observation_sha256"],
            "receipt_file": str(receipt_path) if receipt else None,
            "receipt_sha256": sha(receipt_path) if receipt else None, **parsed,
            "success": parsed["answer"] == o["gold"] if live else None,
            "valid_format": parsed["valid_format"] if live else None})
    return {"analysis_version": VERSION, "dataset": DATASET, "mode": manifest["mode"],
        "status": manifest["status"] if live else "not-run", "model_revision": adapter["model_revision"],
        "provider": adapter["provider"], "adapter_hash": digest(adapter),
        "index_sha256": manifest["index_sha256"], "manifest_file": str(directory / "manifest.json"),
        "manifest_sha256": sha(directory / "manifest.json"), "qa": manifest["qa"], "rows": rows}


def main():
    p = argparse.ArgumentParser(); s = p.add_subparsers(dest="command", required=True)
    r = s.add_parser("run"); r.add_argument("directory"); r.add_argument("--adapter", required=True)
    r.add_argument("--qa"); r.add_argument("--live", action="store_true")
    r.add_argument("--role", choices=["primary", "all"], default="primary")
    v = s.add_parser("verify"); v.add_argument("directory"); v.add_argument("output")
    a = p.parse_args()
    if a.command == "run":
        m = run(a.directory, load(a.adapter), a.qa, a.live, a.role)
        print({"status": m["status"], "observations": len(m["observation_ids"]), "calls": m["calls"]})
    else:
        assert not Path(a.output).exists()
        r = verify(a.directory); save(a.output, r, immutable=True)
        print({"status": r["status"], "rows": len(r["rows"])})


if __name__ == "__main__":
    main()
