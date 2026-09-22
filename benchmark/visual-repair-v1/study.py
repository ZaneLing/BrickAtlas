#!/usr/bin/env python3
"""Provider-neutral native packets, no-purchase local study and receipt analysis."""
import argparse
import json
from collections import Counter, defaultdict
from functools import lru_cache
from statistics import mean

import numpy as np

from baselines import configurations, predict
from common import ASSETS, CONDITIONS, HERE, ROOT, SEED, VERSION, digest, filehash, read, reference, write
from evaluate import evaluate

QUESTION = (
    "Match the unlabeled reference geometry to exactly one candidate card; ignore orientation "
    "and use its current printed ID as bound_terminal. The graph IDs refer to the current display, "
    "not source part identities. Together with fixed_terminals it must lie in one connected component. "
    "Only paths inside the supplied undirected graph count. Initially every listed missing vertex "
    "and its incident edges is unavailable. Restoring one listed vertex costs 1 and reinstates "
    "its original edges to present neighbors. Return every minimum-cost restoration set, its own "
    "final component sizes, minimum_cost, and whether budget suffices. Graph unavailability is not "
    "a physical removal. Order is irrelevant; duplicate vertices/solutions and unlisted actions are invalid."
)
FORMAT = {
    "bound_terminal": "one candidate ID string",
    "minimum_cost": "nonnegative integer",
    "budget_sufficient": "boolean",
    "solutions": [{"restored": "array of IDs", "component_sizes": "array of positive integers"}],
}


def packet(task, condition, answer):
    data = task["input"].copy()
    images = []
    question, output = QUESTION, FORMAT
    if condition in ("multimodal", "atomic_binding"):
        images = [{"path": task["image"], "sha256": filehash(ROOT / task["image"]),
                   "mime_type": "image/png", "width": 1600, "height": 900}]
    if condition == "oracle_binding":
        data["bound_terminal"] = answer["bound_terminal"]
        question = ("Use the supplied oracle bound_terminal; no visual inference is requested. "
                    + QUESTION[QUESTION.index("Together with fixed_terminals"):])
    if condition == "atomic_binding":
        data = {"candidate_ids": data["candidate_ids"]}
        question = ("Match the unlabeled reference geometry to one candidate card; ignore orientation. "
                    "Return only its current printed ID as bound_terminal.")
        output = {"bound_terminal": "one candidate ID string"}
    return {"version": VERSION, "condition": condition, "question": question,
            "input": data, "images": images, "output_schema": output}


def freeze():
    tasks = read(HERE / "public.json")["tasks"]
    gold = {t["id"]: t["answer"] for t in read(HERE / "gold.json")["tasks"]}
    observations = []
    for task in tasks:
        for condition in CONDITIONS:
            value = packet(task, condition, gold[task["id"]])
            path = HERE / "native" / condition / (task["id"] + ".json")
            write(path, value)
            observations.append({"task_id": task["id"], "condition": condition,
                                 "construction_id": task["construction_id"], "split": task["split"],
                                 "dependence_group": task["dependence_group"], "packet": reference(path)})
    config_rows = [{**c, "kind": "algorithmic", "revision": filehash(HERE / "baselines.py"),
                    "repeats": 1, "settings": {"deterministic": True, "seed": SEED,
                    "tools": "only public packet, permitted PNG bytes, generic font atlas, exact graph solver"}}
                   for c in configurations()]
    sources = [reference(HERE / f) for f in ("public.json", "gold.json", "sampling-ledger.json",
               "render-specs.json", "captures.json", "evaluate.py", "baselines.py", "study.py",
               "common.py", "portable.py", "qualification.py", "build.py", "verify.py", "review.html")]
    roster = read(ROOT / "benchmark/experiment-plans/model-budget-20260920/config.json")
    planned = []
    for m in roster["api_models"] + roster["local_models"]:
        text_only = m.get("track") == "graph-only"
        planned.append({"id": m["id"], "name": m["name"],
                        "requested_model": m.get("api_id", m.get("repo")),
                        "conditions": ["no_image", "oracle_binding"] if text_only else list(CONDITIONS),
                        "status": "planned-uncollected-not-run-locked", "revision": None,
                        "adapter_sha256": None, "mode_comparisons": [],
                        "settings": None, "results": None})
    write(HERE / "planned-models.json", {"version": VERSION, "model_count": len(planned), "models": planned,
          "contract": "Native JSON plus exact full PNG bytes. External runs require precollection lock of model revision, adapter hash, settings and complete planned observations. No unsupported effort comparisons.",
          "collection_performed": False})
    manifest = {
        "version": VERSION, "study_id": "visual-repair-v1-local-algorithms",
        "status": "executable-no-purchase-algorithmic-study",
        "conditions": list(CONDITIONS), "configurations": config_rows,
        "observations": observations, "sources": sources,
        "image_policy": "Exact native 1600x900 PNG bytes, one image; no external crop or private source access. Legal baselines may compute on allowed pixels.",
        "failure_policy": "One planned attempt. Missing, refusal, parse failure and transport failure retain denominator; no successful-only retries.",
        "analysis_unit": "12 observations/construction; transitive source/contributor/design/template groups. Shared anchors never independent.",
        "planned_runs": len(tasks) * len(config_rows),
        "font_calibration": reference(ASSETS / "font-calibration.png"),
        "empirical_model_or_human_results": None,
        "shortcut_threshold": .80,
    }
    manifest["lock_sha256"] = digest(manifest)
    write(HERE / "study-manifest.json", manifest)
    print({"packets": len(observations), "local_configurations": len(config_rows),
           "planned_local_runs": manifest["planned_runs"], "planned_models": len(planned)})


def load_manifest():
    manifest = read(HERE / "study-manifest.json")
    lock = manifest.pop("lock_sha256")
    assert digest(manifest) == lock, "Manifest lock mismatch"
    manifest["lock_sha256"] = lock
    for source in [*manifest["sources"], manifest["font_calibration"]]:
        assert filehash(ROOT / source["path"]) == source["sha256"], source["path"]
    return manifest


def checked_packet(observation):
    ref = observation["packet"]
    path = ROOT / ref["path"]
    assert filehash(path) == ref["sha256"], path
    value = read(path)
    for image in value["images"]:
        assert filehash(ROOT / image["path"]) == image["sha256"], image["path"]
    return value


def verify_native_inputs(manifest):
    seen = {}
    for obs in manifest["observations"]:
        ref = obs["packet"]
        if filehash(ROOT / ref["path"]) != ref["sha256"]:
            raise ValueError("Changed native packet")
        value = read(ROOT / ref["path"])
        if value["condition"] != obs["condition"] or value["version"] != VERSION:
            raise ValueError("Off-condition/version native packet")
        for image in value["images"]:
            path, expected = image["path"], image["sha256"]
            if path not in seen:
                seen[path] = filehash(ROOT / path)
            if seen[path] != expected:
                raise ValueError("Changed native image")


def envelope(manifest, config, observation, response, error=None):
    return {"version": VERSION, "study_lock_sha256": manifest["lock_sha256"],
            "kind": config["kind"], "config_id": config["id"], "revision": config["revision"],
            "settings_sha256": digest(config["settings"]),
            "task_id": observation["task_id"], "condition": observation["condition"], "repeat": 0,
            "input_sha256": observation["packet"]["sha256"], "synthetic": False,
            "response": response, "error": error}


def run():
    manifest = load_manifest()
    observations = {(o["task_id"], o["condition"]): o for o in manifest["observations"]}
    receipts = []
    # No gold loaded here: even the oracle receives only its declared native packet.
    for config in manifest["configurations"]:
        cache = {}
        for obs in observations.values():
            if obs["condition"] != config["condition"]:
                continue
            value = checked_packet(obs)
            key = digest(value)
            try:
                if key not in cache:
                    cache[key] = predict(value, config["rule"])
                receipts.append(envelope(manifest, config, obs, cache[key]))
            except (ValueError, OSError, KeyError) as error:
                receipts.append(envelope(manifest, config, obs, None, str(error)))
        print(config["id"], sum(r["config_id"] == config["id"] for r in receipts), flush=True)
    write(HERE / "algorithmic-receipts.json", receipts)
    return receipts


def validate_receipts(manifest, receipts):
    configs = {c["id"]: c for c in manifest["configurations"]}
    observations = {(o["task_id"], o["condition"]): o for o in manifest["observations"]}
    accepted = {}
    for row in receipts:
        if row.get("synthetic") is not False:
            raise ValueError("Synthetic receipt cannot enter this study")
        if row.get("version") != VERSION or row.get("study_lock_sha256") != manifest["lock_sha256"]:
            raise ValueError("Off-version receipt")
        config = configs.get(row.get("config_id"))
        if not config:
            raise ValueError("Unplanned configuration")
        if row.get("kind") != config["kind"] or row["kind"] not in ("algorithmic", "model"):
            raise ValueError("Receipt evidence kind does not match configuration")
        obs = observations.get((row.get("task_id"), row.get("condition")))
        if not obs or row["condition"] != config["condition"] or row.get("repeat") != 0:
            raise ValueError("Unplanned observation/condition/repeat")
        if row.get("revision") != config["revision"] or row.get("settings_sha256") != digest(config["settings"]):
            raise ValueError("Off-revision/settings receipt")
        if row.get("input_sha256") != obs["packet"]["sha256"]:
            raise ValueError("Input hash mismatch")
        key = (config["id"], obs["task_id"])
        if key in accepted:
            raise ValueError("Duplicate planned receipt")
        accepted[key] = row
    return accepted


def estimates(rows, field):
    if not rows:
        return {"n": 0, "micro": None, "group_macro": None, "groups": 0,
                "group_values": {}, "ci95_group_sensitivity": None, "leave_one_group_out": []}
    groups = defaultdict(list)
    for r in rows:
        groups[r["dependence_group"]].append(float(r[field]))
    values = {g: mean(v) for g, v in sorted(groups.items())}
    arr = np.array(list(values.values()))
    ci = None
    if len(values) > 1:
        rng = np.random.default_rng(20260922)
        means = arr[rng.integers(0, len(arr), size=(2000, len(arr)))].mean(axis=1)
        ci = np.quantile(means, [.025, .975]).tolist()
    return {"n": len(rows), "micro": mean(float(r[field]) for r in rows),
            "group_macro": mean(values.values()), "groups": len(groups), "group_values": values,
            "ci95_group_sensitivity": ci,
            "leave_one_group_out": [{"omitted": g, "group_macro": mean(v for k, v in values.items() if k != g)}
                                   for g in values if len(values) > 1]}


def metrics(rows):
    atomic = bool(rows) and rows[0]["condition"] == "atomic_binding"
    score = "binding_correct" if atomic else "repair_exact"
    buckets = defaultdict(dict)
    for row in rows:
        buckets[row["construction_id"], row["replicate"]][row["structural_arm"], row["visual_arm"]] = row
    pairs = defaultdict(list)
    for cells in buckets.values():
        common = {"dependence_group": next(iter(cells.values()))["dependence_group"]}
        for fault in ("fault_0", "fault_1"):
            for arm, metric in (("changing", "changing_both_correct"), ("preserving", "preserving_both_correct")):
                if (fault, "anchor") in cells and (fault, arm) in cells:
                    pairs[metric].append({**common, "value": cells[fault, "anchor"][score] and cells[fault, arm][score]})
        for arm in ("anchor", "changing", "preserving"):
            if ("fault_0", arm) in cells and ("fault_1", arm) in cells:
                pairs["structural_both_correct"].append({**common, "value": cells["fault_0", arm][score] and cells["fault_1", arm][score]})
        pairs["factorial_all_correct"].append({**common, "value": len(cells) == 6 and all(r[score] for r in cells.values())})
    result = {name: estimates(rows, field) for name, field in (
        ("binding_accuracy", "binding_correct"), ("repair_exact", "repair_exact"),
        ("invalid_rate", "invalid"), ("missing_rate", "missing"))}
    result.update({name: estimates(values, "value") for name, values in pairs.items()})
    bound = [r for r in rows if r["binding_correct"]]
    result["repair_given_binding"] = estimates(bound, "repair_exact") if not atomic else None
    result["planned_count"] = len(rows)
    result["received_count"] = sum(not r["missing"] for r in rows)
    if atomic:
        result["repair_exact"] = None
        result["structural_both_correct"] = None
        result["note"] = "Atomic binding is duplicated across faults by plan; not additional independent perception evidence."
    return result


def analyze(receipts, manifest=None, write_output=True):
    manifest = manifest or load_manifest()
    verify_native_inputs(manifest)
    accepted = validate_receipts(manifest, receipts)
    tasks = {t["id"]: t for t in read(HERE / "public.json")["tasks"]}
    gold = {t["id"]: t["answer"] for t in read(HERE / "gold.json")["tasks"]}
    rows = []
    cache = {}
    for config in manifest["configurations"]:
        for task in tasks.values():
            receipt = accepted.get((config["id"], task["id"]))
            response = receipt.get("response") if receipt and not receipt.get("error") else None
            key = (task["id"], config["condition"], digest(response))
            if key not in cache:
                cache[key] = evaluate(task["input"], gold[task["id"]]["bound_terminal"], response,
                                      config["condition"] == "atomic_binding")
            result = cache[key]
            rows.append({**{k: task[k] for k in ("id", "construction_id", "dependence_group", "split", "replicate", "structural_arm", "visual_arm")},
                         "config_id": config["id"], "condition": config["condition"], **result,
                         "missing": receipt is None, "invalid": receipt is not None and not result["valid"]})
    reports = []
    for config in manifest["configurations"]:
        cfg = [r for r in rows if r["config_id"] == config["id"]]
        reports.append({**config, **{split: metrics([r for r in cfg if r["split"] == split])
                                    for split in ("dev", "heldout")},
                        "all": metrics(cfg)})
    shallow = [r for r in reports if r["kind"] == "algorithmic" and r.get("rule") != "oracle" and
               (r["heldout"]["binding_accuracy"]["micro"] or 0) >= manifest["shortcut_threshold"]]
    evidence_kind = "algorithmic-not-model-or-human" if all(c["kind"] == "algorithmic" for c in reports) else "model"
    report = {"version": VERSION, "study_lock_sha256": manifest["lock_sha256"], "kind": evidence_kind,
              "planned_count": manifest["planned_runs"], "received_count": len(receipts),
              "threshold": manifest["shortcut_threshold"], "threshold_exceeding_configs": [r["id"] for r in shallow],
              "interpretation": ("Shallow-solvable binding stage: no strong perceptual-difficulty claim." if shallow else
                                 "No tested shallow rule reaches the frozen threshold; this does not establish model difficulty or rule out other shortcuts."),
              "uncertainty_scope": "Finite-source group sensitivity only. 10 held-out groups cannot meet the 25-group normal precision illustration.",
              "configurations": reports, "model_results": None, "human_results": None}
    if write_output:
        write(HERE / "baseline-report.json", report)
        write(HERE / "algorithmic-scores.json", rows)
    print({"planned": report["planned_count"], "received": len(receipts),
           "threshold_exceeding": report["threshold_exceeding_configs"]})
    return report


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("command", choices=("freeze", "run", "analyze", "all"))
    parser.add_argument("--receipts", type=str)
    args = parser.parse_args()
    if args.command in ("freeze", "all"):
        freeze()
    if args.command in ("run", "all"):
        run()
    if args.command in ("analyze", "all"):
        analyze(read(args.receipts or HERE / "algorithmic-receipts.json"))
