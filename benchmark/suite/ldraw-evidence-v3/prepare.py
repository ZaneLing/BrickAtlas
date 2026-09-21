#!/usr/bin/env python3
"""Freeze new Part-type observations and retain unaffected exact components."""
from copy import deepcopy

from common import DATA, DATASET, PUBLIC, ROOT, VERSION, digest, frozen, save, sha, load
from assignment import bounds_audit, candidate_inventory, shortcut_predictions


def main():
    old = frozen("benchmark/ldraw-evidence-v2/visual-manifest.json")
    original = {o["observation_id"]: o for o in old["observations"]}
    assignment = load(DATA / "part-type-assignment.json")
    assert assignment["contract_sha256"] == sha(DATA / "assignment-contract.json")
    inventory = candidate_inventory()
    assert inventory == load(DATA / "candidate-inventory.json")["rows"]
    by_parent = {r["parent_task_id"]: r for r in inventory}
    assigned = {r["parent_task_id"]: r for r in assignment["rows"]}
    assert len(assigned) == 67
    for r in assigned.values():
        a, predictions = shortcut_predictions(by_parent[r["parent_task_id"]], r["option_labels"])
        assert a == r["a_gold"] and predictions == r["oracle_A_predictions"]
    bounds_audit(list(assigned.values()))
    registry = frozen("benchmark/ldraw-evidence-v2/family-registry.json")
    save(DATA / "family-registry.json", {**registry, "analysis_version": VERSION}, immutable=True)
    identity = frozen("benchmark/ldraw-evidence-v2/identity-contract.json")
    save(DATA / "identity-contract.json", identity, immutable=True)
    observations = [deepcopy(o) for o in old["observations"] if
                    o["family"] == "color" or o["role"] == "position-reference-control"]
    pairs = [deepcopy(p) for p in old["pairs"] if p["family"] == "color"]
    jobs = []
    for parent, config in sorted(assigned.items()):
        prior = next(p for p in old["pairs"] if p["parent_task_id"] == parent)
        anchor = original[prior["a"]]
        inv = by_parent[parent]
        labels = dict(anchor["render_spec"]["labels"])
        payload = deepcopy(anchor["payload"])
        payload["options"] = [{"id": chr(65+i), "label": label} for i,label in enumerate(config["option_labels"])]
        endpoints = []
        for arm in ["A", "B"]:
            display = dict(labels)
            if arm == "B":
                a, b = inv["matching_id"], config["swap_instance_id"]
                display[a], display[b] = display[b], display[a]
            spec = {"kind": "candidate-labels", "model_id": inv["source_id"], "target_id": inv["target_id"],
                "labels": display, "render_operands": anchor["render_spec"]["render_operands"],
                "camera": anchor["render_spec"]["camera"],
                "reference_positions": [{k:p[k] for k in ["id", "anchor", "text"]}
                                       for p in anchor["render_spec"]["projections"]],
                "label_policy": "fixed per-instance anchor/text positions and draw order from source A; no geometry edits",
                "source_poses_preserved": True}
            oid = "obs3-" + digest([DATASET, parent, arm, spec, payload])[:24]
            gold = {"choiceId": config[arm.lower()+"_gold"]}
            row = {**{k:deepcopy(anchor[k]) for k in ["parent_task_id", "source_id", "source_hash", "family",
                    "display_name", "canonical_target", "source_truth", "identity_contract_hash"]},
                "observation_id": oid, "arm": arm, "role": "primary", "mechanism": "balanced-candidate-reference-change",
                "payload": payload, "gold": gold, "gold_semantics": next(
                    o["label"] for o in payload["options"] if o["id"] == gold["choiceId"]),
                "display_referents": {v: {"source_hash": anchor["source_hash"], "instance_id": k}
                                     for k,v in display.items()},
                "render_spec": spec, "render_spec_hash": digest(spec),
                "assignment_sha256": sha(DATA / "part-type-assignment.json"),
                "parent_observation_version": "brickatlas-display-v2",
                "qa_status": "pending-arm-disjoint-independent-human-reviews"}
            observations.append(row); jobs.append({"observation_id": oid, **spec}); endpoints.append(oid)
        pairs.append({**{k:prior[k] for k in ["parent_task_id", "source_id", "family", "truth_policy"]},
            "pair_id": "pair3-" + digest([DATASET, parent])[:24], "a": endpoints[0], "b": endpoints[1],
            "mechanism": "balanced-candidate-reference-change"})
    observations.sort(key=lambda o:digest([VERSION, "independent-requests", o["observation_id"]]))
    save(DATA / "visual-manifest.json", {
        "dataset": DATASET, "analysis_version": VERSION, "schema_version": 3,
        "role": "internal-scoring-provenance", "contract_sha256": sha(DATA / "identity-contract.json"),
        "family_registry_sha256": sha(DATA / "family-registry.json"),
        "assignment_sha256": sha(DATA / "part-type-assignment.json"),
        "system_prompt": old["system_prompt"], "system_prompt_hash": old["system_prompt_hash"],
        "component_versions": {"color": "brickatlas-display-v2", "shape-match": DATASET,
                              "position-reference-control": "brickatlas-display-v2", "graphs": "matched-graphs-v1"},
        "parent_count": 140, "source_count": 24, "primary_observations": 280,
        "primary_pairs": 140, "auxiliary_observations": 67,
        "pairs": pairs, "observations": observations,
        "legacy_policy": "Part-type primary endpoints require entirely new QA and responses. Other exact stimulus components are unchanged; human exposure protocol is new.",
        "status": "frozen-before-QA-and-model-evidence", "human_results": None, "model_results": None},
        immutable=True)
    save(PUBLIC / "render-plan.json", {"dataset": DATASET,
        "role": "evaluator-render-instructions-not-model-input", "jobs": jobs}, immutable=True)
    prior_renders = frozen("benchmark/ldraw-evidence-v2/renders.json")
    retained_ids = {o["observation_id"] for o in observations if not o["observation_id"].startswith("obs3-")}
    save(DATA / "retained-renders.json", {"dataset": DATASET,
         "images": [r for r in prior_renders["images"] if r["observation_id"] in retained_ids]}, immutable=True)
    save(DATA / "retained-components.json", {
        "color_pairs": 73, "color_observations": 146, "auxiliary_observations": 67,
        "graph_inputs": "benchmark/ldraw-evidence-v1/matched-graphs-v1/inputs.json",
        "graph_audit": "benchmark/ldraw-evidence-v2/graph-audit.json",
        "graph_partitions": "benchmark/ldraw-evidence-v2/graph-partitions.json",
        "historical_dossiers": "public/benchmark/evidence-v2/dossiers.json",
        "file_hashes": {p:sha(ROOT / p) for p in [
            "benchmark/ldraw-evidence-v1/matched-graphs-v1/inputs.json",
            "benchmark/ldraw-evidence-v2/graph-audit.json", "benchmark/ldraw-evidence-v2/graph-partitions.json",
            "public/benchmark/evidence-v2/dossiers.json"]}}, immutable=True)
    print({"status": "prepared", "new_primary_part_type_endpoints": len(jobs),
           "retained_exact_observations": len(retained_ids)})


if __name__ == "__main__":
    main()
