#!/usr/bin/env python3
"""Parent-disjoint human review, independent adjudication and exact-wire validation."""
import argparse
from collections import Counter, defaultdict
from datetime import datetime
import json
from pathlib import Path
import secrets
import shutil
import zipfile

from common import DATA, ROOT, VERSION, digest, load, save, sha

DECISIONS = ["decidable", "ambiguous", "unanswerable", "contradictory"]
CHECKS = ["unique_target_reference", "unique_visual_option", "sufficient_visibility", "no_reference_contradiction"]
REASONS = ["none", "target_reference", "multiple_visual_answers", "no_visual_answer",
           "occlusion", "resolution", "reference_contradiction", "other"]
SLOTS = [f"reviewer-{i}" for i in range(1, 7)]


def assets():
    m, index = load(DATA / "visual-manifest.json"), load(DATA / "observation-index.json")
    assert index["manifest_sha256"] == sha(DATA / "visual-manifest.json")
    assert index["renders_sha256"] == sha(DATA / "renders.json")
    observations = {o["observation_id"]: o for o in m["observations"]}
    wires = {w["observation_id"]: w for w in index["observations"]}
    for w in wires.values():
        assert sha(ROOT / w["file"]) == w["wire_observation_sha256"], "Changed wire invalidates QA"
    return m, observations, wires


def assigned_slots(observations):
    groups = defaultdict(list)
    for o in observations.values():
        groups[o["parent_task_id"]].append(o["observation_id"])
    assignment = {}
    for parent, ids in sorted(groups.items()):
        slots = sorted(SLOTS, key=lambda s: digest([VERSION, "parent-disjoint", parent, s]))
        for index, oid in enumerate(sorted(ids, key=lambda i: digest([VERSION, "arm", i]))):
            assignment[oid] = slots[index*2:index*2+2]
            assert len(assignment[oid]) == 2
    return assignment


def validate_assignment(mapping, observations, directory=None):
    assert set(mapping["slots"]) == set(SLOTS)
    expected = assigned_slots(observations)
    found = defaultdict(list)
    for slot, spec in mapping["slots"].items():
        parents = set()
        if directory:
            queue_path=Path(directory)/slot/"queue.json"
            assert sha(queue_path) == spec["queue_sha256"]
            queue=load(queue_path)
            assert queue["slot"]==slot
            actual={r["review_id"]:r for r in queue["queue"]}
            assert len(actual)==len(queue["queue"]) and set(actual)==set(spec["items"])
            wires={w["observation_id"]:w for w in load(DATA/"observation-index.json")["observations"]}
        for token,record in spec["items"].items():
            oid = record["observation_id"]
            assert oid in observations
            if directory:
                assert actual[token]==queue_row(oid,token,wires), "Reviewer did not receive the exact frozen observation"
                assert record["wire_observation_sha256"]==wires[oid]["wire_observation_sha256"]
            parent = observations[oid]["parent_task_id"]
            assert parent not in parents, "Reviewer exposed to multiple observations of one parent"
            parents.add(parent); found[oid].append(slot)
    assert set(found) == set(observations)
    assert all(sorted(found[o]) == sorted(s) for o, s in expected.items()), "Assignment changed"
    return {"endpoints": len(observations), "reviews": sum(map(len,found.values())),
            "reviewer_slots": 6, "cross_arm_or_auxiliary_exposures": 0}


def queue_row(oid, token, wires):
    w = wires[oid]
    wire = load(ROOT / w["file"])
    content = wire["messages"][1]["content"]
    return {"review_id": token, "wire_observation_sha256": w["wire_observation_sha256"],
            "system_text": wire["messages"][0]["content"], "payload": json.loads(content[0]["text"]),
            "image": content[1]["image_url"]["url"], "width": w["width"], "height": w["height"]}


def package_queue(folder, slot, queue):
    save(folder / "queue.json", {"slot": slot, "queue": queue, "decisions": DECISIONS,
                                "checks": CHECKS, "reasons": REASONS}, immutable=True)
    shutil.copyfile(Path(__file__).with_name("qa-review.html"), folder / "index.html")
    with zipfile.ZipFile(folder.parent / (slot + ".zip"), "x", compression=zipfile.ZIP_DEFLATED) as package:
        package.write(folder / "queue.json", "queue.json")
        package.write(folder / "index.html", "index.html")


def export(destination):
    m, observations, wires = assets()
    dest = Path(destination)
    if dest.exists():
        raise ValueError("New directory required; reviewer assignments are immutable")
    dest.mkdir(parents=True)
    mapping = {"analysis_version": VERSION, "index_sha256": sha(DATA / "observation-index.json"),
               "slots": {}, "protocol": "six distinct people; at most one observation per parent per person, including auxiliary panels"}
    assigned = assigned_slots(observations)
    for slot in SLOTS:
        queue, keys = [], {}
        for oid in sorted([o for o in observations if slot in assigned[o]], key=lambda _: secrets.token_hex(16)):
            w = wires[oid]
            token = "q-" + secrets.token_hex(12)
            queue.append(queue_row(oid, token, wires))
            keys[token] = {"observation_id": oid, "wire_observation_sha256": w["wire_observation_sha256"]}
        folder = dest / slot
        package_queue(folder, slot, queue)
        mapping["slots"][slot] = {"queue_sha256": sha(folder / "queue.json"), "items": keys}
    mapping["exposure_audit"] = validate_assignment(mapping, observations, dest)
    save(dest / "private-mapping.json", mapping, immutable=True)
    save(dest / "status.json", {"primary_observations": 280, "auxiliary_observations": 67,
         "required_primary_reviews": 560, "required_auxiliary_reviews": 134,
         "actual_human_reviews": 0, "final_primary_decisions": 0, "status": "pending-humans"}, immutable=True)
    print({"status": "exported", "reviewers": 6, "total_required_reviews": 694,
           "slot_counts": {s: len(v["items"]) for s,v in mapping["slots"].items()}, "directory": str(dest)})


def signature(review):
    return (review["decision"], review["visual_choice"], tuple(review["checks"][k] for k in CHECKS))


def validate_review(r, options, fixture=False):
    assert r["decision"] in DECISIONS and r["reason_code"] in REASONS
    assert isinstance(r["reason"], str) and r["reason"].strip()
    assert set(r["checks"]) == set(CHECKS) and all(type(v) is bool for v in r["checks"].values())
    assert r["native_size_attestation"] is True and r["independence_attestation"] is True
    assert r["author_kind"] == ("synthetic-fixture" if fixture else "human"), "Genuine humans required"
    assert isinstance(r["reviewer"], str) and len(r["reviewer"].strip()) >= 2
    assert datetime.fromisoformat(r["timestamp"].replace("Z", "+00:00")).tzinfo is not None
    assert r["visual_choice"] is None or r["visual_choice"] in options
    if r["decision"] == "decidable":
        assert all(r["checks"].values()) and r["visual_choice"] in options and r["reason_code"] == "none"
    else:
        assert r["reason_code"] != "none"


def agreement(pairs, field):
    labels = [(field(a), field(b)) for a, b in pairs]
    n = len(labels)
    if not n:
        return {"n": 0, "raw_agreement": None, "cohen_kappa": None, "undefined_reason": "no double reviews"}
    a, b = Counter(x for x, _ in labels), Counter(y for _, y in labels)
    raw = sum(x == y for x, y in labels) / n
    expected = sum(a[k] * b[k] for k in a.keys() | b.keys()) / n**2
    return {"n": n, "raw_agreement": raw, "expected_agreement": expected,
            "cohen_kappa": (raw - expected) / (1 - expected) if expected < 1 else None,
            "undefined_reason": "degenerate marginals" if expected == 1 else None,
            "confusion": [{"reviewer_1": x, "reviewer_2": y, "n": c}
                          for (x, y), c in Counter(labels).items()]}


def combine(directory, feedback_files, adjudication_file=None, fixture=False):
    m, obs, wires = assets()
    directory = Path(directory)
    mapping = load(directory / "private-mapping.json")
    assert mapping["index_sha256"] == sha(DATA / "observation-index.json"), "Changed inputs invalidate all assignments"
    exposure = validate_assignment(mapping, obs, directory)
    raw, reviewer_by_slot = defaultdict(dict), {}
    imported = []
    for path in feedback_files:
        feedback = load(path)
        slot = feedback["slot"]
        assignment = mapping["slots"][slot]
        assert sha(directory / slot / "queue.json") == assignment["queue_sha256"]
        assert feedback["queue_sha256"] == assignment["queue_sha256"]
        assert feedback["evidence_kind"] == ("synthetic-fixture" if fixture else "independent-human-review")
        identity = feedback["reviewer"]
        if slot in reviewer_by_slot:
            assert identity == reviewer_by_slot[slot], "Reviewer identity changed within slot"
        reviewer_by_slot[slot] = identity
        imported.append({"file": str(Path(path).resolve()), "sha256": sha(path)})
        for review in feedback["reviews"]:
            assignment_row = assignment["items"][review["review_id"]]
            oid = assignment_row["observation_id"]
            assert review["wire_observation_sha256"] == wires[oid]["wire_observation_sha256"] == assignment_row["wire_observation_sha256"]
            assert review["reviewer"] == identity
            validate_review(review, [o["id"] for o in obs[oid]["payload"]["options"]], fixture)
            assert slot not in raw[oid], "Duplicate review for a reviewer/observation"
            raw[oid][slot] = review
    assert len(set(reviewer_by_slot.values())) == len(reviewer_by_slot), "All six reviewer slots require distinct people"
    adjudications = {}
    if adjudication_file:
        document = load(adjudication_file)
        assert document["evidence_kind"] == ("synthetic-fixture" if fixture else "independent-human-adjudication")
        if not fixture:
            rebuilt = adjudication_document(document["assignment_directory"],
                                             [r["file"] for r in document["source_feedback"]])
            assert document == rebuilt, "Adjudication import must reproduce from raw feedback"
        imported.append({"file": str(Path(adjudication_file).resolve()), "sha256": sha(adjudication_file)})
        adjudicator_parents = defaultdict(set)
        for r in document["adjudications"]:
            oid = r["observation_id"]
            assert oid in obs and oid not in adjudications
            validate_review(r, [o["id"] for o in obs[oid]["payload"]["options"]], fixture)
            assert r["wire_observation_sha256"] == wires[oid]["wire_observation_sha256"]
            assert r["reviewer"] not in reviewer_by_slot.values(), "Third independent adjudicator required"
            parent = obs[oid]["parent_task_id"]
            assert parent not in adjudicator_parents[r["reviewer"]], "Adjudicator saw another observation of this parent"
            adjudicator_parents[r["reviewer"]].add(parent)
            adjudications[oid] = r
    rows, double, conflicts, consumed = [], [], [], set()
    for oid, o in obs.items():
        reviews = [raw[oid][slot] for slot in sorted(raw[oid])]
        row = {"observation_id": oid, "wire_observation_sha256": wires[oid]["wire_observation_sha256"],
               "role": o["role"], "source_id": o["source_id"], "family": o["family"],
               "display_name": o["display_name"], "reviews": reviews,
               "adjudication": None, "final_decision": "pending", "final_reason": "missing-independent-review",
               "final_visual_choice": None, "disagreement": None}
        if len(reviews) == 2:
            double.append(reviews)
            disagreement = signature(reviews[0]) != signature(reviews[1])
            row["disagreement"] = disagreement
            final = reviews[0] if not disagreement else adjudications.get(oid)
            if disagreement:
                if final:
                    assert final["review_hashes"] == [digest(r) for r in reviews], "Adjudication bound to stale reviews"
                    row["adjudication"] = final
                    consumed.add(oid)
                else:
                    row["final_reason"] = "adjudication-required"
                    conflicts.append({"observation_id": oid, "wire_observation_sha256": wires[oid]["wire_observation_sha256"],
                                      "review_hashes": [digest(r) for r in reviews], "reviews": reviews,
                                      "observation": load(ROOT / wires[oid]["file"])})
            if final:
                row.update(final_decision=final["decision"], final_reason=final["reason_code"],
                           final_visual_choice=final["visual_choice"])
                if final["decision"] == "decidable" and final["visual_choice"] != o["gold"]["choiceId"]:
                    row.update(final_decision="pending", final_reason="human-oracle-conflict-requires-dataset-revision")
        rows.append(row)
    assert consumed == set(adjudications), "Adjudication allowed only on actual disagreements"
    byid = {r["observation_id"]: r for r in rows}
    pair_rows = [{"pair_id": p["pair_id"], "family": p["family"], "source_id": p["source_id"],
                  "a": byid[p["a"]]["final_decision"], "b": byid[p["b"]]["final_decision"],
                  "both_decidable": all(byid[p[k]]["final_decision"] == "decidable" for k in ["a", "b"]),
                  "exclusion_reasons": sorted({byid[p[k]]["final_reason"] for k in ["a", "b"]
                                               if byid[p[k]]["final_decision"] != "decidable"})}
                 for p in m["pairs"]]
    primary = [r for r in rows if r["role"] == "primary"]
    return {"analysis_version": VERSION, "evidence_kind": "synthetic-fixture" if fixture else "human-qa",
            "index_sha256": sha(DATA / "observation-index.json"),
            "assignment_directory": str(directory.resolve()), "mapping_sha256": sha(directory / "private-mapping.json"),
            "feedback_files": imported, "reviewer_count": len(set(reviewer_by_slot.values())),
            "exposure_audit": exposure,
            "reviewer_slots": reviewer_by_slot,
            "raw_review_count": sum(len(r["reviews"]) for r in rows),
            "agreement": {"decision": agreement(double, lambda r: r["decision"]),
                          "visual_choice": agreement(double, lambda r: r["visual_choice"] or "no-choice"),
                          "checks": {k: agreement(double, lambda r, k=k: str(r["checks"][k])) for k in CHECKS},
                          "interpretation": "Pooled two-rating agreement; rater identities vary by endpoint. Cohen kappa is descriptive, with separate fixed-rater-pair reports."},
            "agreement_by_rater_pair": {"/".join(slots): agreement(
                [r["reviews"] for r in rows if len(r["reviews"]) == 2 and
                 sorted(x["reviewer"] for x in r["reviews"]) == list(slots)], lambda r:r["decision"])
                for slots in sorted({tuple(sorted(x["reviewer"] for x in r["reviews"]))
                                     for r in rows if len(r["reviews"]) == 2})},
            "agreement_by_role": {role: agreement(
                [r["reviews"] for r in rows if r["role"] == role and len(r["reviews"]) == 2], lambda r: r["decision"])
                for role in ["primary", "position-reference-control"]},
            "primary_total": len(primary), "primary_final": sum(r["final_decision"] != "pending" for r in primary),
            "primary_ready_for_inference": all(r["final_decision"] != "pending" for r in primary),
            "all_ready_for_inference": all(r["final_decision"] != "pending" for r in rows),
            "rows": rows, "pairs": pair_rows, "adjudication_queue": conflicts,
            "exclusions": dict(Counter(reason for r in pair_rows for reason in r["exclusion_reasons"])),
            "family_coverage": {family: {
                "planned_pairs": sum(p["family"] == family for p in pair_rows),
                "planned_sources": len({p["source_id"] for p in pair_rows if p["family"] == family}),
                "qa_pairs": sum(p["family"] == family and p["both_decidable"] for p in pair_rows),
                "qa_sources": len({p["source_id"] for p in pair_rows if p["family"] == family and p["both_decidable"]}),
                "exclusion_sources": {reason: len({p["source_id"] for p in pair_rows
                    if p["family"] == family and reason in p["exclusion_reasons"]})
                    for reason in {reason for p in pair_rows if p["family"] == family for reason in p["exclusion_reasons"]}}
            } for family in ["color", "shape-match"]},
            "qa_comparable_pairs": sum(p["both_decidable"] for p in pair_rows)}


def verify_final(path, role="primary"):
    result = load(path)
    assert result["evidence_kind"] == "human-qa", "Synthetic QA is never eligible"
    assert result["index_sha256"] == sha(DATA / "observation-index.json")
    assert sha(Path(result["assignment_directory"]) / "private-mapping.json") == result["mapping_sha256"]
    # Recompute decisions from retained original files, never trust a hand-edited summary.
    files, adjudication = [], None
    for entry in result["feedback_files"]:
        assert sha(entry["file"]) == entry["sha256"], "Raw human review changed"
        if load(entry["file"])["evidence_kind"] == "independent-human-adjudication":
            assert adjudication is None
            adjudication = entry["file"]
        else:
            files.append(entry["file"])
    rebuilt = combine(result["assignment_directory"], files, adjudication)
    assert rebuilt == result, "QA summary does not reproduce from raw reviews"
    key = "primary_ready_for_inference" if role == "primary" else "all_ready_for_inference"
    assert result[key], "Human QA gate: final decisions for both sides are required before model inference"
    return result


def export_adjudication(snapshot, destination):
    current = load(snapshot)
    assert current["evidence_kind"] == "human-qa"
    assert current["index_sha256"] == sha(DATA / "observation-index.json")
    dest = Path(destination)
    assert not dest.exists()
    dest.mkdir(parents=True)
    assert current["adjudication_queue"], "No categorical disagreements"
    _, obs, wires = assets()
    byparent = defaultdict(list)
    for o in obs.values():
        byparent[o["parent_task_id"]].append(o["observation_id"])
    # Role is never revealed by a slot; no slot receives two observations of a parent.
    slots = {oid: "adjudicator-" + str(i+1) for parent, ids in byparent.items()
             for i, oid in enumerate(sorted(ids, key=lambda x:digest(["adjudication",x])))}
    mapping = {}
    for slot in ["adjudicator-1", "adjudicator-2", "adjudicator-3"]:
        queue, keys = [], {}
        for conflict in sorted(current["adjudication_queue"], key=lambda _: secrets.token_hex(16)):
            oid = conflict["observation_id"]
            if slots[oid] != slot:
                continue
            key = "q-" + secrets.token_hex(12)
            row = queue_row(oid,key,wires)
            row["peer_reviews"] = [{k:r[k] for k in ["decision","checks","visual_choice","reason"]}
                                   for r in conflict["reviews"]]
            queue.append(row)
            keys[key] = {k:conflict[k] for k in ["observation_id","wire_observation_sha256","review_hashes"]}
        if queue:
            package_queue(dest / slot,slot,queue)
            mapping[slot] = {"queue_sha256":sha(dest / slot / "queue.json"),"items":keys}
    save(dest / "private-mapping.json", {"snapshot": str(Path(snapshot).resolve()), "snapshot_sha256": sha(snapshot),
         "slots": mapping}, immutable=True)


def adjudication_document(directory, feedback_files):
    directory = Path(directory)
    mapping = load(directory / "private-mapping.json")
    assert sha(mapping["snapshot"]) == mapping["snapshot_sha256"]
    current = load(mapping["snapshot"])
    prior_reviewers = {r["reviewer"] for row in current["rows"] for r in row["reviews"]}
    reviews, seen, identities, files = [], set(), {}, []
    for feedback in feedback_files:
        f = load(feedback); slot = f["slot"]; spec = mapping["slots"][slot]
        assert f["queue_sha256"] == spec["queue_sha256"] == sha(directory / slot / "queue.json")
        assert f["evidence_kind"] == "independent-human-review" and f["reviewer"] not in prior_reviewers
        assert slot not in identities, "Combine one retained feedback export per adjudicator slot"
        identities[slot] = f["reviewer"]
        files.append({"file":str(Path(feedback).resolve()),"sha256":sha(feedback)})
        for r in f["reviews"]:
            key = r["review_id"]
            assert key not in seen and r["reviewer"] == f["reviewer"]
            seen.add(key)
            row = spec["items"][key]
            assert r["wire_observation_sha256"] == row["wire_observation_sha256"]
            reviews.append({**r,**row})
    assert len(identities) == len(set(identities.values())), "Distinct adjudicators per slot required"
    return {"evidence_kind":"independent-human-adjudication","assignment_directory":str(directory.resolve()),
            "mapping_sha256":sha(directory / "private-mapping.json"),"source_feedback":files,"adjudications":reviews}


def main():
    p = argparse.ArgumentParser()
    s = p.add_subparsers(dest="command", required=True)
    e = s.add_parser("export"); e.add_argument("directory")
    c = s.add_parser("combine"); c.add_argument("directory"); c.add_argument("output")
    c.add_argument("--feedback", nargs="*", default=[]); c.add_argument("--adjudication")
    v = s.add_parser("verify"); v.add_argument("file"); v.add_argument("--role", default="primary")
    ae = s.add_parser("adjudication-export"); ae.add_argument("snapshot"); ae.add_argument("directory")
    ai = s.add_parser("adjudication-import"); ai.add_argument("directory"); ai.add_argument("output")
    ai.add_argument("--feedback", nargs="+", required=True)
    a = p.parse_args()
    if a.command == "export":
        export(a.directory)
    elif a.command == "combine":
        assert not Path(a.output).exists(), "Do not overwrite review snapshots"
        result = combine(a.directory, a.feedback, a.adjudication)
        save(a.output, result, immutable=True)
        print({k: result[k] for k in ["raw_review_count", "primary_total", "primary_final", "qa_comparable_pairs"]})
    elif a.command == "verify":
        verify_final(a.file, a.role)
        print("Human QA gate passed")
    elif a.command == "adjudication-export":
        export_adjudication(a.snapshot, a.directory)
    else:
        save(a.output, adjudication_document(a.directory,a.feedback), immutable=True)


if __name__ == "__main__":
    main()
