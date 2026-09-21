#!/usr/bin/env python3
"""Isolated text-graph requests and receipt-bound strong/control reporting."""
import argparse
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import urllib.error
import urllib.request

from common import DATA, ROOT, VERSION, digest, frozen, load, save, sha
from estimates import estimate, wilson
from graph_audit import PRIOR, inspect
from run import parse_receipt, request_bytes, validate_adapter, write_new

SYSTEM = ("Answer using only the supplied hypothetical undirected graph. Return exactly one JSON object "
          "with the integer field value. Do not add prose, markdown, other fields, or use tools.")
INPUTS = "benchmark/ldraw-evidence-v1/matched-graphs-v1/inputs.json"


def code_hashes():
    return {name: sha(Path(__file__).with_name(name)) for name in
            ["common.py", "graph_run.py", "graph_audit.py", "estimates.py", "run.py"]}


def observations():
    public = frozen(INPUTS)
    return {o["id"]: {"messages": [{"role": "system", "content": SYSTEM},
        {"role": "user", "content": [{"type": "text", "text": json.dumps(o["payload"], ensure_ascii=True,
                                                                       separators=(",", ":"))}]}]}
            for o in public["observations"]}


def checked_audit():
    prior, audit = frozen(PRIOR), load(DATA / "graph-audit.json")
    assert audit["prior_manifest_sha256"] == sha(ROOT / PRIOR)
    assert all(sha(Path(__file__).with_name(name)) == value for name, value in audit["code_hashes"].items())
    rebuilt = [inspect(o["id"], o["source_id"], o["parent_task_id"], o["input"], o["gold"]["value"])
               for o in prior["observations"]]
    assert digest(rebuilt) == digest(audit["observations"]), "Graph gold/features do not reproduce from frozen inputs"
    strong = {p["parent_task_id"] for p in prior["pairs"] if p["gold_delta"]
              and p["matching"].endswith("surviving-degrees")}
    assert len(audit["pairs"]) == len(prior["pairs"])
    byid = {o["id"]: o for o in rebuilt}
    for row, original in zip(audit["pairs"], prior["pairs"]):
        assert all(row[k] == value for k, value in original.items())
        role = ("strong-change" if original["parent_task_id"] in strong else "degree-visible-control") if original[
            "gold_delta"] else ("strong-invariance" if original["parent_task_id"] in strong else "degree-visible-invariance")
        assert row["role"] == role
        assert row["a_gold"] == byid[row["a"]]["gold"] and row["b_gold"] == byid[row["b"]]["gold"]
    return audit


def parse_graph(receipt, max_value, adapter):
    parsed = parse_receipt(receipt, [], adapter)
    if parsed["failure_reason"] != "invalid-format":
        return parsed
    # The shared parser has already checked provider revision, JSON syntax,
    # duplicate keys, non-finite values, refusal, and transport/API status.
    value = json.loads(parsed["output"])
    valid = (isinstance(value, dict) and set(value) == {"value"}
             and type(value["value"]) is int and 0 <= value["value"] <= max_value)
    return {**parsed, "answer": value if valid else None, "valid_format": valid,
            "failure_reason": None if valid else "invalid-format"}


def run(directory, adapter, live=False):
    validate_adapter(adapter, live)
    if live:
        api_key = os.environ.get("BRICKATLAS_API_KEY")
        assert api_key
    wires = observations()
    dest = Path(directory).resolve()
    assert not dest.exists(), "Never overwrite or resume a run"
    dest.mkdir(parents=True)
    manifest = {"analysis_version": VERSION, "role": "hypothetical-graphs",
        "mode": "live-inference" if live else "offline-dry-run", "status": "running",
        "started": datetime.now(timezone.utc).isoformat(), "adapter": adapter, "adapter_hash": digest(adapter),
        "inputs_sha256": sha(ROOT / INPUTS), "partition_sha256": sha(DATA / "graph-partitions.json"),
        "code_hashes": code_hashes(), "requests": [], "calls": 0}
    for oid, wire in wires.items():
        path = dest / "requests" / (oid + ".json")
        write_new(path, request_bytes(wire, adapter))
        manifest["requests"].append({"observation_id": oid, "file": str(path.relative_to(dest)), "sha256": sha(path)})
    save(dest / "manifest.json", manifest)
    if live:
        for r in manifest["requests"]:
            receipt = {"observation_id": r["observation_id"], "request_sha256": r["sha256"],
                "evidence_kind": "provider-http-receipt", "started": datetime.now(timezone.utc).isoformat()}
            req = urllib.request.Request(adapter["endpoint"], data=(dest / r["file"]).read_bytes(),
                headers={"Authorization": "Bearer " + api_key, "Content-Type": "application/json"}, method="POST")
            try:
                with urllib.request.urlopen(req, timeout=adapter["timeout_seconds"]) as response:
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
    manifest.update(status="complete" if live else "dry-run-complete", finished=datetime.now(timezone.utc).isoformat())
    save(dest / "manifest.json", manifest)
    return manifest


def verify(directory):
    dest = Path(directory).resolve()
    m, wires = load(dest / "manifest.json"), observations()
    assert m["analysis_version"] == VERSION and m["role"] == "hypothetical-graphs"
    assert m["mode"] in ["live-inference", "offline-dry-run"]
    live = m["mode"] == "live-inference"
    validate_adapter(m["adapter"], live)
    assert m["adapter_hash"] == digest(m["adapter"])
    assert m["code_hashes"] == code_hashes() and m["inputs_sha256"] == sha(ROOT / INPUTS)
    assert m["partition_sha256"] == sha(DATA / "graph-partitions.json")
    assert [r["observation_id"] for r in m["requests"]] == list(wires)
    receipts = list((dest / "receipts").glob("*.json"))
    assert all(p.stem in wires for p in receipts)
    assert 0 <= len(receipts) <= m["calls"] <= len(wires)
    if live:
        assert m["status"] in ["running", "complete"]
        if m["status"] == "complete":
            assert m["calls"] == len(wires)
    else:
        assert not receipts and m["calls"] == 0 and m["status"] == "dry-run-complete"
    audit = checked_audit()
    byid = {o["id"]: o for o in audit["observations"]}
    rows = []
    for r in m["requests"]:
        oid = r["observation_id"]
        assert r["file"] == f"requests/{oid}.json"
        assert sha(dest / r["file"]) == r["sha256"]
        assert (dest / r["file"]).read_bytes() == request_bytes(wires[oid], m["adapter"])
        path = dest / "receipts" / (oid + ".json")
        receipt = load(path) if path.exists() else None
        if receipt:
            assert live and receipt["evidence_kind"] == "provider-http-receipt"
            assert receipt["observation_id"] == oid and receipt["request_sha256"] == r["sha256"]
            assert datetime.fromisoformat(receipt["started"]) >= datetime.fromisoformat(m["started"])
            assert datetime.fromisoformat(receipt["finished"]) >= datetime.fromisoformat(receipt["started"])
        parsed = parse_graph(receipt, len(byid[oid]["surviving_nodes"]), m["adapter"])
        rows.append({"id": oid, "source_id": byid[oid]["source_id"], **parsed,
            "success": int(parsed["answer"] == {"value": byid[oid]["gold"]}) if live else None,
            "valid_format": parsed["valid_format"] if live else None,
            "request_sha256": r["sha256"], "receipt_file": str(path) if receipt else None,
            "receipt_sha256": sha(path) if receipt else None})
    return {"analysis_version": VERSION, "mode": m["mode"], "status": m["status"] if live else "not-run",
        "manifest_file": str(dest / "manifest.json"), "manifest_sha256": sha(dest / "manifest.json"),
        "model_revision": m["adapter"]["model_revision"], "adapter_hash": m["adapter_hash"], "rows": rows}


def analyze(directory):
    validated = verify(directory)
    assert validated["mode"] == "live-inference" and validated["status"] == "complete"
    audit = checked_audit()
    predictions = {r["id"]: r for r in validated["rows"]}
    paired = []
    for pair in audit["pairs"]:
        a, b = predictions[pair["a"]], predictions[pair["b"]]
        paired.append({**{k: pair[k] for k in ["pair_id", "source_id", "role", "a", "b"]},
            "accuracy": (a["success"] + b["success"]) / 2, "both": a["success"] * b["success"],
            "valid_both": int(a["valid_format"] and b["valid_format"]),
            "a_prediction": a["answer"], "b_prediction": b["answer"],
            "a_gold": pair["a_gold"], "b_gold": pair["b_gold"]})
    return {**validated, "audit_sha256": sha(DATA / "graph-audit.json"), "pair_rows": paired,
        "partitions": {role: {**{k: estimate([p for p in paired if p["role"] == role], k)
                                for k in ["accuracy", "both", "valid_both"]},
            "both_pair_wilson_ci95": wilson(sum(p["both"] for p in paired if p["role"] == role),
                                          sum(p["role"] == role for p in paired))}
            for role in audit["summary"]}, "interpretation": audit["protocol"]}


def main():
    p = argparse.ArgumentParser()
    s = p.add_subparsers(dest="command", required=True)
    r = s.add_parser("run"); r.add_argument("directory"); r.add_argument("--adapter", required=True)
    r.add_argument("--live", action="store_true")
    for command in ["verify", "analyze"]:
        a = s.add_parser(command); a.add_argument("directory"); a.add_argument("output")
    args = p.parse_args()
    if args.command == "run":
        result = run(args.directory, load(args.adapter), args.live)
        print({"mode": result["mode"], "calls": result["calls"], "requests": len(result["requests"])})
    else:
        assert not Path(args.output).exists()
        result = (verify if args.command == "verify" else analyze)(args.directory)
        save(args.output, result, immutable=True)
        print({"status": result["status"], "observations": len(result["rows"])})


if __name__ == "__main__":
    main()
