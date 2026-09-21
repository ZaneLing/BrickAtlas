#!/usr/bin/env python3
"""Freeze new visual identities, prompts and counterfactual render instructions."""
from collections import Counter
from itertools import permutations
import re

from common import DATA, DATASET, PUBLIC, ROOT, VERSION, digest, frozen, original_tasks, save, sha

SEED = 20260920
PALETTE = [
    {"name": "Red", "ldraw_code": "4", "hex": "#C91A09"},
    {"name": "Blue", "ldraw_code": "1", "hex": "#0055BF"},
    {"name": "Yellow", "ldraw_code": "14", "hex": "#F2CD37"},
    {"name": "Black", "ldraw_code": "0", "hex": "#05131D"},
]
IDENTITY_TEXT = (
    "References select objects in the supplied image only. A label such as B0001 "
    "is an image-local display reference, not a request to retrieve a historical "
    "source instance. Renders may have edited appearances or label assignments. "
    "Answer only from the current image."
)
SYSTEM_PROMPT = (
    "Answer the visual question using only the supplied image and its identity contract. "
    "Return exactly one JSON object with the field choiceId, containing one listed option ID. "
    "Do not add prose, markdown, other fields, or use tools."
)


def target(t):
    return re.search(r"\bB\d{4,}\b", t["promptEn"]).group()


def same_linear(a, b):
    return all(abs(a[i]-b[i]) < 1e-6 for i in [0, 1, 2, 4, 5, 6, 8, 9, 10])


def main():
    catalog = frozen("benchmark/ldraw-v2/catalog.json")
    all_tasks = original_tasks()
    tasks = sorted((t for t in all_tasks.values() if t["family"] in {"color", "shape-match"}),
                   key=lambda t: digest([SEED, t["id"]]))
    bundles = {m["id"]: frozen(f"public/benchmark/ldraw-v2/models/{m['id']}.json") for m in catalog}
    manifests = {m["id"]: frozen(f"public/models/{m['id']}/manifest.json") for m in catalog}
    old_renders = frozen("benchmark/ldraw-v2/paired-renders.json")["images"]
    render_map = {(r["taskId"], r["mode"]): r for r in old_renders}
    contracts = frozen("benchmark/ldraw-v2/task-contracts.json")["contracts"]
    registry = {c["family"]: {"id": c["family"], "display_name": c["name"],
                             "legacy_role": c["classification"]} for c in contracts}
    registry["shape-match"]["display_name"] = "Part-type"
    registry["color"]["display_name"] = "Color"
    save(DATA / "family-registry.json", {"analysis_version": VERSION, "families": registry}, immutable=True)
    identity = {"contract_id": "current-display-reference-v2", "model_visible": IDENTITY_TEXT,
                "canonical_identity": "source_hash + instance_id; evaluator provenance only",
                "display_referent": "visible object currently selected by the image-local reference",
                "source_truth": "original source type/color/transform; never rewritten",
                "observation_answer": "current visible appearance or displayed candidate reference",
                "color_mechanism": "rendered body-color counterfactual; source geometry and poses fixed",
                "shape_match_mechanism": "candidate display-label reassignment; source part types fixed",
                "old_results_transferable": False}
    save(DATA / "identity-contract.json", identity, immutable=True)
    observations, pairs, jobs, donors = [], [], [], []
    color_index = 0
    for t in tasks:
        sid, parent = t["modelId"], t["id"]
        label = target(t)
        source_parts = {p["id"]: p for p in bundles[sid]["parts"]}
        instance = next(r["id"] for r in t["references"] if r["label"] == label)
        part = source_parts[instance]
        common = {"parent_task_id": parent, "source_id": sid, "source_hash": t["source_hash"],
                  "family": t["family"], "display_name": registry[t["family"]]["display_name"],
                  "canonical_target": {"source_hash": t["source_hash"], "instance_id": instance},
                  "source_truth": {"part_number": part["partNumber"], "color": part["color"]},
                  "identity_contract_hash": digest(identity)}
        family = t["family"]
        if family == "color":
            ca, cb = list(permutations(range(len(PALETTE)), 2))[color_index % 12]
            color_index += 1
            option_colors = sorted(PALETTE, key=lambda p: digest([SEED, parent, p["name"]]))
            options = [{"id": chr(65+i), "label": p["name"]} for i, p in enumerate(option_colors)]
            prompt = f"What color is the object currently marked {label} in this image?"
            scene_instances = {p["instanceId"]: p for p in manifests[sid]["instances"]}
            candidates = [p for p in source_parts.values() if p["partNumber"] == part["partNumber"]
                          and p["color"] != part["color"] and p["color"] in {o["label"] for o in t["options"]}]
            donors.append({"parent_task_id": parent, "source_id": sid, "target": instance,
                           "same_type_different_color_donors": [p["id"] for p in candidates],
                           "same_linear_transform_donors": [p["id"] for p in candidates if same_linear(
                               scene_instances[p["id"]]["originalMatrix"], scene_instances[instance]["originalMatrix"])],
                           "analysis_role": "feasibility audit only; not color-specific model results"})
            arms = []
            for arm, color_id in [("A", ca), ("B", cb)]:
                palette = PALETTE[color_id]
                arms.append((arm, {"choiceId": next(o["id"] for o in options if o["label"] == palette["name"])},
                             {"kind": "appearance-color", "model_id": sid, "target_id": instance,
                              "labels": {instance: label}, "body_color": palette,
                              "material_policy": "opaque body; fixed roughness/metalness; fixed source edge material",
                              "render_operands": [instance], "source_poses_preserved": True}))
            mechanism = "rendered-appearance-change"
        else:
            prompt = (f"Which displayed candidate label currently marks an object with the same visible part "
                      f"geometry as the target marked {label}? Ignore color and pose. Answer from this image, "
                      "not from historical source identities.")
            options = [{"id": o["id"], "label": o["label"]} for o in t["options"]]
            arms = []
            for arm, mode in [("A", "crop"), ("B", "wrong")]:
                r = render_map[(parent, mode)]
                answer = t["answer"] if arm == "A" else {"choiceId": r["mismatch"]["alternateChoiceId"]}
                arms.append((arm, answer, {"kind": "preserved-render", "model_id": sid,
                    "target_id": instance, "labels": r["labels"], "render_operands": r["renderOperands"],
                    "source_file": "public/" + r["file"], "source_sha256": r["sha256"],
                    "camera": r["camera"], "projections": r["projections"], "source_poses_preserved": True}))
            mechanism = "candidate-reference-change"
        this = []
        for arm, gold, job in arms:
            obs_id = "obs-" + digest([DATASET, parent, arm, job, prompt])[:24]
            payload = {"identity_contract": IDENTITY_TEXT, "question": prompt,
                       "format": "single-choice", "options": options}
            row = {**common, "observation_id": obs_id, "arm": arm, "role": "primary",
                   "mechanism": mechanism, "payload": payload, "gold": gold,
                   "gold_semantics": next(o["label"] for o in options if o["id"] == gold["choiceId"]),
                   "display_referents": {v: {"source_hash": t["source_hash"], "instance_id": k}
                                        for k, v in job["labels"].items()},
                   "render_spec": job, "render_spec_hash": digest(job),
                   "qa_status": "pending-two-independent-human-reviews"}
            if family == "color":
                row["appearance_world"] = {"kind": "explicit-rendered-counterfactual",
                                           "current_body_color": job["body_color"]["name"],
                                           "source_color_unchanged": part["color"]}
            observations.append(row); this.append(row)
            if job["kind"] != "preserved-render":
                jobs.append({"observation_id": obs_id, **job})
        assert this[0]["gold_semantics"] != this[1]["gold_semantics"]
        assert this[0]["payload"] == this[1]["payload"]
        pairs.append({"pair_id": "pair-" + digest([DATASET, parent])[:24],
                      "parent_task_id": parent, "source_id": sid, "family": family,
                      "a": this[0]["observation_id"], "b": this[1]["observation_id"],
                      "mechanism": mechanism, "truth_policy": "observation-answer-change"})
        if family == "shape-match":
            # A position interface is a declared auxiliary condition, never pooled with primary pairs.
            ordered = sorted(t["options"], key=lambda o: o["id"])
            ids = [next(r["id"] for r in t["references"] if r["label"] == o["label"]) for o in ordered]
            panel_options = [{"id": o["id"], "label": s} for o, s in zip(
                ordered, ["Leftmost", "Second from left", "Third from left", "Rightmost"])]
            job = {"kind": "position-panels", "model_id": sid, "target_id": instance,
                   "candidate_ids": ids, "render_operands": [instance]+ids, "labels": {},
                   "source_poses_preserved": True,
                   "panel_policy": "Upper target panel; four lower candidates left to right; no text in image",
                   "panel_boxes": [[320, 0, 640, 340], [0, 390, 320, 400], [320, 390, 320, 400],
                                   [640, 390, 320, 400], [960, 390, 320, 400]]}
            obs_id = "obs-" + digest([DATASET, parent, job])[:24]
            row = {**common, "observation_id": obs_id, "arm": None, "role": "position-reference-control",
                   "mechanism": "position-reference-and-access-change",
                   "payload": {"identity_contract": IDENTITY_TEXT,
                       "question": "The upper panel is the target. Which of the four lower candidate panels, "
                                   "read from left to right, shows the same visible part geometry? Ignore color and pose.",
                       "format": "single-choice", "options": panel_options},
                   "gold": t["answer"], "gold_semantics": next(
                       o["label"] for o in panel_options if o["id"] == t["answer"]["choiceId"]),
                   "display_referents": {}, "render_spec": job, "render_spec_hash": digest(job),
                   "qa_status": "pending-two-independent-human-reviews"}
            observations.append(row); jobs.append({"observation_id": obs_id, **job})
    primary = [r for r in observations if r["role"] == "primary"]
    assert len(primary) == 2*len(tasks) == 280
    assert len({r["observation_id"] for r in observations}) == len(observations)
    observations.sort(key=lambda r: digest([SEED, "independent-trial-order", r["observation_id"]]))
    manifest = {"dataset": DATASET, "analysis_version": VERSION, "schema_version": 2,
                "role": "internal-scoring-provenance", "seed": SEED,
                "contract_sha256": sha(DATA / "identity-contract.json"),
                "family_registry_sha256": sha(DATA / "family-registry.json"),
                "system_prompt": SYSTEM_PROMPT, "system_prompt_hash": digest(SYSTEM_PROMPT),
                "parent_count": len(tasks), "source_count": len(catalog),
                "primary_observations": len(primary), "primary_pairs": len(pairs),
                "auxiliary_observations": len(observations)-len(primary),
                "pairs": pairs, "observations": observations,
                "status": "render-plan-frozen-before-human-and-model-evidence",
                "model_results": None, "human_results": None,
                "legacy_policy": "No prompt/render/QA/model result transfer from evidence-v1."}
    save(DATA / "visual-manifest.json", manifest, immutable=True)
    save(DATA / "donor-feasibility.json", {
        "analysis_version": VERSION, "parents": len(donors),
        "same_type_eligible": sum(bool(r["same_type_different_color_donors"]) for r in donors),
        "same_linear_transform_eligible": sum(bool(r["same_linear_transform_donors"]) for r in donors),
        "rows": donors}, immutable=True)
    save(PUBLIC / "render-plan.json", {"role": "evaluator-render-instructions-not-model-input",
         "dataset": DATASET, "jobs": jobs}, immutable=True)
    print({"status": "passed", "primary_pairs": len(pairs), "primary_observations": len(primary),
           "auxiliary_observations": len(observations)-len(primary), "new_renders": len(jobs),
           "family_pairs": dict(Counter(p["family"] for p in pairs))})


if __name__ == "__main__":
    main()
