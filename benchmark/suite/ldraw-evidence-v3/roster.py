#!/usr/bin/env python3
"""Immutable model inclusion contract and exact expected-run-set validation."""
from datetime import datetime, timezone
from pathlib import Path

from common import DATA, ROOT, VERSION, digest, load, save, sha

MODELS = [
    ("gpt41", "GPT-4.1", "gpt-4.1-2025-04-14",
     "Non-reasoning instruction-following reference model in the existing candidate-family plan."),
    ("gpt4o", "GPT-4o", "gpt-4o-2024-08-06",
     "Earlier full-size multimodal reference using the same supported transport."),
    ("gpt4o-mini", "GPT-4o mini", "gpt-4o-mini-2024-07-18",
     "Smaller multimodal reference to examine paired behavior across service tiers."),
]
CONDITIONS = ("visual", "no-image", "graph")


def freeze():
    assert not (DATA / "model-roster.json").exists(), "Roster changes require a new study version"
    entries = []
    for key, name, revision, reason in MODELS:
        adapter = {"provider": "OpenAI", "endpoint": "https://api.openai.com/v1/chat/completions",
            "model": revision, "model_revision": revision, "api_revision": "v1/chat/completions",
            "response_model": revision, "max_tokens": 128, "timeout_seconds": 90, "temperature": 0}
        path = DATA / "adapters" / f"{key}.json"
        save(path, adapter, immutable=True)
        entries.append({"model_id": key, "display_name": name, "provider": "OpenAI",
            "requested_model_revision": revision, "expected_served_model_revision": revision,
            "adapter_file": str(path.relative_to(ROOT)), "adapter_file_sha256": sha(path),
            "adapter_hash": digest(adapter), "endpoint": adapter["endpoint"],
            "api_revision": adapter["api_revision"], "transport": "openai-chat-completions-native-png",
            "image_detail": "high", "image_resolution": [1280, 800], "temperature": 0,
            "max_tokens": 128, "timeout_seconds": 90, "attempts_per_observation": 1,
            "repeat_count": 1, "automatic_retries": 0, "primary": True, "inclusion_reason": reason,
            "planned_runs": [{"run_id": f"{key}-{condition}-r1", "condition": condition,
                "relative_directory": f"model-runs/{key}-{condition}-r1",
                "planned_observations": 219 if condition == "graph" else 347}
                for condition in CONDITIONS]})
    value = {"analysis_version": VERSION, "frozen_at": datetime.now(timezone.utc).isoformat(),
        "freeze_kind": "local immutable protocol commitment before inference; not an external registry timestamp",
        "entries": entries, "expected_run_count": 9,
        "inclusion_scope": "Three documented immutable snapshots using the implemented native-image transport; not a comprehensive or latest-model leaderboard.",
        "candidate_plan_boundary": "Earlier unfrozen family names were candidates, not a committed run roster. Unsupported provider transports and local models are outside this study.",
        "estimand": "one fixed invocation set per served revision and condition; no across-call stability claim",
        "exclusion_policy": "No planned model, condition or failed observation may be omitted. Missing/extra runs or mismatched hashes block empirical tables.",
        "failure_policy": "All scheduled observations remain in denominators. HTTP errors, refusals, timeouts, missing receipts and explicitly closed unattempted requests are separate failures.",
        "interruption_policy": "Close an existing interrupted run with a retained reason and timestamp; never resume, retry or replace it. Unattempted requests are not provider receipts.",
        "rank_policy": "Report points and paired source/author intervals. Intervals containing zero do not support a directional ranking. No cross-call stability inference.",
        "no_image_policy": "Remove only image content from reviewed visual messages; preserve exact question/options. This is an evidence-withdrawal dependency baseline, not a human-decidable visual condition.",
        "documentation_checked": [
            {"url": "https://developers.openai.com/api/docs/models/" + slug, "snapshot": revision,
             "verified_fields": ["documented snapshot ID", "image input", "Chat Completions support"],
             "live_provider_access_verified": False}
            for slug, (_, _, revision, _) in zip(["gpt-4.1", "gpt-4o", "gpt-4o-mini"], MODELS)]}
    save(DATA / "model-roster.json", value, immutable=True)
    save(DATA / "roster-lock.json", {"model_roster_sha256": sha(DATA / "model-roster.json"),
         "analysis_version": VERSION}, immutable=True)
    print({"status": "frozen", "models": len(entries), "expected_runs": 9,
           "scheduled_observations": 3*(347*2+219), "real_calls": 0})


def checked():
    r = load(DATA / "model-roster.json")
    assert r["analysis_version"] == VERSION
    assert sha(DATA / "model-roster.json") == load(DATA / "roster-lock.json")["model_roster_sha256"]
    ids = []
    for entry in r["entries"]:
        assert sha(ROOT / entry["adapter_file"]) == entry["adapter_file_sha256"]
        adapter = load(ROOT / entry["adapter_file"])
        assert digest(adapter) == entry["adapter_hash"]
        assert adapter["model_revision"] == adapter["response_model"] == entry["expected_served_model_revision"]
        assert entry["attempts_per_observation"] == entry["repeat_count"] == 1
        assert entry["automatic_retries"] == 0
        assert {p["condition"] for p in entry["planned_runs"]} == set(CONDITIONS)
        ids.extend(p["run_id"] for p in entry["planned_runs"])
    assert r["entries"] and len(ids) == len(set(ids)) == r["expected_run_count"]
    return r


def planned():
    r = checked()
    return {p["run_id"]: {"model": e, **p} for e in r["entries"] for p in e["planned_runs"]}


def specification(model_id, condition):
    rows = [p for p in planned().values() if p["model"]["model_id"] == model_id and p["condition"] == condition]
    assert len(rows) == 1, "Unplanned model or condition"
    return rows[0]


def exact_run_set(directory):
    """Validate the entire dedicated run root, not a caller-selected list."""
    root = Path(directory)
    expected = planned()
    observed = {p.name for p in root.iterdir() if p.is_dir()} if root.exists() else set()
    missing, extra = set(expected)-observed, observed-set(expected)
    assert not missing and not extra, {"missing_planned_runs": sorted(missing), "unplanned_runs": sorted(extra)}
    for run_id in expected:
        assert (root / run_id / "manifest.json").is_file(), ("Run has no manifest", run_id)
    return {run_id: root / run_id for run_id in sorted(expected)}


def pending_index(destination):
    r = checked()
    save(destination, {"analysis_version": VERSION, "model_roster_sha256": sha(DATA / "model-roster.json"),
        "status": "protocol-only-no-empirical-table", "complete": False,
        "expected_runs": r["expected_run_count"], "observed_runs": 0,
        "rows": [{"run_id": p["run_id"], "model_id": p["model"]["model_id"],
                  "condition": p["condition"], "status": "not-run",
                  "manifest_sha256": None, "request_index_sha256": None,
                  "receipt_set_sha256": None, "qa_snapshot_sha256": None,
                  "paper_row": p["model"]["model_id"] + "/" + p["condition"]}
                 for p in planned().values()]}, immutable=True)


if __name__ == "__main__":
    freeze()
    pending_index(DATA / "model-run-index.json")
