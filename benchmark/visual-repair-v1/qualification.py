#!/usr/bin/env python3
"""Six-slot blinded qualification queue and strict real-judgment validator."""
import argparse
import itertools
import random
from collections import defaultdict

from common import HERE, ROOT, SEED, VERSION, digest, filehash, read, write
from study import checked_packet, load_manifest

FLAGS = ("reference_readable", "labels_readable", "unique_geometry_match", "graph_contract_clear")


def freeze_queue():
    manifest = load_manifest()
    tasks = read(HERE / "public.json")["tasks"]
    observations = {o["task_id"]: o for o in manifest["observations"] if o["condition"] == "multimodal"}
    grouped = defaultdict(list)
    for t in tasks:
        grouped[t["construction_id"]].append(t)
    assignments = []
    for cid, rows in sorted(grouped.items()):
        slots = [f"reviewer-slot-{i+1}" for i in range(6)]
        random.Random(digest([SEED, "reviewers", cid])).shuffle(slots)
        for arm_index, arm in enumerate(("anchor", "changing", "preserving")):
            entries = []
            for task in sorted((r for r in rows if r["visual_arm"] == arm), key=lambda r: (r["replicate"], r["structural_arm"])):
                obs = observations[task["id"]]
                native = checked_packet(obs)
                entries.append({"task_id": task["id"], "replicate": task["replicate"],
                                "structural_arm": task["structural_arm"],
                                "packet": obs["packet"], "image": native["images"][0],
                                "binding_shared_key": digest(native["images"][0])})
            for slot in slots[arm_index*2:arm_index*2+2]:
                assignments.append({"assignment_id": "qa-" + digest([cid, arm, slot])[:20],
                                    "construction_id": cid, "visual_arm": arm,
                                    "reviewer_slot": slot, "items": entries})
    queue = {"version": VERSION, "study_lock_sha256": manifest["lock_sha256"],
             "status": "pending-real-reviewers-no-generated-judgments",
             "reviewer_slots": [f"reviewer-slot-{i+1}" for i in range(6)],
             "assignments": assignments,
             "instructions": [
                 "One real person per reviewer slot, six distinct people. Slots are not fabricated reviewer identities.",
                 "Each construction assigns two reviewers to each visual arm. Never expose a reviewer to another visual arm of that construction.",
                 "Within the assigned arm, review both ID replicates and both fault packets. Shared PNGs repeat binding evidence, not independent exposure.",
                 "Open exact native PNG and JSON. Return bound_terminal and four boolean quality flags for every task; give a free-text reason for any false flag.",
                 "Any wrong binding, negative flag, or disagreement triggers independent adjudication by a person outside the two original reviewers.",
                 "No baseline or model outcomes are shown. Cluster subsequent judgments by construction and reviewer.",
             ],
             "required_response_fields": ["task_id", "prompt_sha256", "bound_terminal", *FLAGS, "comment"],
             "exclusion_rule": "Retain full construction in analysis unless independent preregistered human qualification rejects; report both full-machine and qualified-subset denominators. No post-model outcome filtering.",
             "metrics": "Binding agreement and flags are human judgments, not model scores. All values null until real receipts.",
             "summary": {"constructions": len(grouped), "reviewer_slots": 6,
                         "assignments": len(assignments), "item_judgments_planned": sum(len(a["items"]) for a in assignments),
                         "distinct_image_judgments_planned": len(assignments) * 2,
                         "received": 0, "qualified": 0, "binding_agreement": None}}
    queue["lock_sha256"] = digest(queue)
    write(HERE / "qualification-queue.json", queue)
    validate([], [], write_output=True)
    print(queue["summary"])
    return queue


def validate(receipts, adjudications, write_output=False):
    queue = read(HERE / "qualification-queue.json")
    lock = queue.pop("lock_sha256")
    if digest(queue) != lock:
        raise ValueError("Qualification queue lock mismatch")
    manifest = load_manifest()
    if queue["study_lock_sha256"] != manifest["lock_sha256"]:
        raise ValueError("Off-study qualification queue")
    assignments = {a["assignment_id"]: a for a in queue["assignments"]}
    gold = {t["id"]: t["answer"] for t in read(HERE / "gold.json")["tasks"]}
    slot_people, received, exposure = {}, {}, defaultdict(set)
    for receipt in receipts:
        if receipt.get("kind") != "human" or receipt.get("synthetic") is not False:
            raise ValueError("Only explicitly real human judgments accepted")
        if receipt.get("queue_lock_sha256") != lock:
            raise ValueError("Off-queue judgment")
        assignment = assignments.get(receipt.get("assignment_id"))
        if not assignment or assignment["assignment_id"] in received:
            raise ValueError("Unknown or duplicate assignment")
        person = receipt.get("reviewer_id")
        if not isinstance(person, str) or not person.strip():
            raise ValueError("Missing real reviewer pseudonym")
        slot = assignment["reviewer_slot"]
        if slot in slot_people and slot_people[slot] != person:
            raise ValueError("Reviewer slot changed person")
        slot_people[slot] = person
        if len(set(slot_people.values())) != len(slot_people):
            raise ValueError("One person cannot occupy two reviewer slots")
        exposure[assignment["construction_id"], person].add(assignment["visual_arm"])
        if len(exposure[assignment["construction_id"], person]) != 1:
            raise ValueError("Cross-arm reviewer exposure")
        items = {i["task_id"]: i for i in assignment["items"]}
        responses = receipt.get("responses", [])
        if len(responses) != len(items) or {r.get("task_id") for r in responses} != set(items):
            raise ValueError("Missing or duplicate qualification item")
        passing = True
        shared = {}
        for response in responses:
            item = items[response["task_id"]]
            if response.get("prompt_sha256") != item["packet"]["sha256"]:
                raise ValueError("Wrong qualification prompt hash")
            if filehash(ROOT / item["packet"]["path"]) != response["prompt_sha256"]:
                raise ValueError("Changed qualification prompt")
            if filehash(ROOT / item["image"]["path"]) != item["image"]["sha256"]:
                raise ValueError("Changed qualification PNG")
            if any(type(response.get(flag)) is not bool for flag in FLAGS):
                raise ValueError("Missing/nonboolean quality flag")
            if not isinstance(response.get("comment"), str):
                raise ValueError("Missing qualification comment")
            if not all(response[flag] for flag in FLAGS) and not response["comment"].strip():
                raise ValueError("Negative qualification needs reason")
            binding = response.get("bound_terminal")
            if not isinstance(binding, str):
                raise ValueError("Missing qualification binding")
            key = item["binding_shared_key"]
            if key in shared and shared[key] != binding:
                passing = False
            shared[key] = binding
            passing &= binding == gold[response["task_id"]]["bound_terminal"] and all(response[f] for f in FLAGS)
        received[assignment["assignment_id"]] = {"reviewer_id": person, "passing": bool(passing)}
    decisions = {}
    for adj in adjudications:
        key = (adj.get("construction_id"), adj.get("visual_arm"))
        originals = [a for a in assignments.values() if (a["construction_id"], a["visual_arm"]) == key]
        if len(originals) != 2 or any(a["assignment_id"] not in received for a in originals):
            raise ValueError("Adjudication needs both original judgments")
        original_people = {received[a["assignment_id"]]["reviewer_id"] for a in originals}
        if adj.get("reviewer_id") in original_people or not adj.get("reviewer_id"):
            raise ValueError("Adjudicator must be independent of both original reviewers")
        if adj.get("kind") != "human" or adj.get("synthetic") is not False or adj.get("queue_lock_sha256") != lock:
            raise ValueError("Invalid adjudication provenance")
        if key in decisions or type(adj.get("retain")) is not bool or not str(adj.get("reason", "")).strip():
            raise ValueError("Duplicate or malformed adjudication")
        expected_hashes = sorted(i["packet"]["sha256"] for i in originals[0]["items"])
        if sorted(adj.get("prompt_sha256s", [])) != expected_hashes:
            raise ValueError("Adjudication prompt hashes mismatch")
        decisions[key] = adj["retain"]
    rows = []
    constructions = sorted({a["construction_id"] for a in assignments.values()})
    for cid in constructions:
        arms = []
        for arm in ("anchor", "changing", "preserving"):
            original = [received.get(a["assignment_id"]) for a in assignments.values()
                        if a["construction_id"] == cid and a["visual_arm"] == arm]
            if any(r is None for r in original):
                status = "pending"
            elif all(r["passing"] for r in original):
                status = "qualified"
            elif (cid, arm) in decisions:
                status = "qualified" if decisions[cid, arm] else "rejected"
            else:
                status = "needs_adjudication"
            arms.append({"arm": arm, "status": status})
        rows.append({"construction_id": cid, "arms": arms,
                     "qualified": all(a["status"] == "qualified" for a in arms)})
    report = {"version": VERSION, "queue_lock_sha256": lock,
              "received_assignments": len(received), "planned_assignments": len(assignments),
              "qualified_constructions": sum(r["qualified"] for r in rows),
              "pending_constructions": sum(any(a["status"] == "pending" for a in r["arms"]) for r in rows),
              "rows": rows, "human_results": None if not receipts else "real receipts supplied separately"}
    if write_output:
        write(HERE / "qualification-status.json", report)
    return report


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("command", choices=("queue", "validate"))
    parser.add_argument("--receipts")
    parser.add_argument("--adjudications")
    args = parser.parse_args()
    if args.command == "queue":
        freeze_queue()
    else:
        print(validate(read(args.receipts) if args.receipts else [],
                       read(args.adjudications) if args.adjudications else [], True))
