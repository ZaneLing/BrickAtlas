"""Predeclared source admission; reject geometry, never observed solver difficulty."""
from collections import deque
import argparse
import hashlib
import json
import math
from pathlib import Path
import sys
from source_inputs import registry_path, intake_path
from source_fidelity import fidelity

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(HERE.parent / "brickplan-v1"))
from geometry import load_source, qualify, endpoint_pair
from engine import AssemblyDomain, canonical_hash


def components(vertices, edges):
    adjacency = {i: set() for i in vertices}
    for edge in edges:
        a, b = edge["a"], edge["b"]
        if edge["family"] == "stud" and a in adjacency and b in adjacency:
            adjacency[a].add(b)
            adjacency[b].add(a)
    unseen, result = set(vertices), []
    while unseen:
        stack, found = [min(unseen)], set()
        while stack:
            node = stack.pop()
            if node not in found:
                found.add(node)
                stack.extend(sorted(adjacency[node] - found, reverse=True))
        unseen -= found
        result.append(found)
    return sorted(result, key=lambda c: (-len(c), min(c)))


def bounded_component(vertices, edges, limit):
    adjacency = {i: set() for i in vertices}
    for e in edges:
        if e["family"] == "stud" and e["a"] in vertices and e["b"] in vertices:
            adjacency[e["a"]].add(e["b"])
            adjacency[e["b"]].add(e["a"])
    queue, seen, result = deque([min(vertices)]), {min(vertices)}, []
    while queue and len(result) < limit:
        i = queue.popleft()
        result.append(i)
        for j in sorted(adjacency[i] - seen):
            seen.add(j)
            queue.append(j)
    return set(result)


def qualify_model(model, plan, metadata):
    profile_id = "source-" + model
    folder = HERE / "data" / profile_id
    row = {"model": model, "sourceGroup": metadata["kit"], "attempts": [],
           "rejectedInstances": [], "components": [], "planHash": canonical_hash(plan)}
    try:
        intake = json.loads(intake_path(plan, model).read_text())
        if intake["status"] != "manifest-ready":
            row.update(qualified=False, exclusionStage="source-intake",
                       reason=intake.get("error", intake["status"]))
            return row
        proof = fidelity(model, plan)
        row["sourceFidelity"] = proof
        if not proof["passed"]:
            row.update(qualified=False, exclusionStage="source-fidelity", reason=proof["reason"])
            return row
        manifest = json.loads((ROOT / f"web/public/models/{model}/manifest.json").read_text())
        original_provenance = json.loads(
            (ROOT / f"web/public/models/{model}/provenance.json").read_text())
        original = original_provenance["source"]
        assert hashlib.sha256((ROOT / original["path"]).read_bytes()).hexdigest() == original["sha256"]
        assert manifest["sourceHash"] == original["sha256"]
        assert original_provenance["model"]["setNumber"] == metadata["setNumber"]
        assert original_provenance["candidateRegistrySha256"] == plan["candidateRegistrySha256"]
        conflicting_parts = {r["partNumber"] for r in
                             original_provenance.get("embeddedPartLockedPathConflicts", [])}
        good = []
        for i, part in enumerate(manifest["instances"]):
            try:
                if part["partNumber"] in conflicting_parts:
                    raise ValueError("Embedded original part differs from the locked collision/render source")
                load_source(model, [i])
                good.append(i)
            except Exception as exc:
                row["rejectedInstances"].append(
                    {"sourceIndex": i, "part": part["partNumber"], "reason": str(exc)[:200]})
        parts, edges, provenance = load_source(model, good)
        row["validInstances"] = len(good)
        limits = plan["qualification"]
        candidate_components = components(set(range(len(parts))), edges)[:limits["maximumComponents"]]
        for component_index, original_comp in enumerate(candidate_components):
            if len(original_comp) <= limits["minimumRegisteredSites"]:
                continue
            comp = bounded_component(original_comp, edges, limits["maximumSourceSubassemblyParts"])
            detail = {"component": component_index, "originalParts": len(original_comp),
                      "candidateParts": len(comp), "endpointPruning": []}
            row["components"].append(detail)
            retained = []
            for i in sorted(comp):
                conflicts = [(j, endpoint_pair(parts[i], parts[j])) for j in retained]
                bad = [(j, check) for j, check in conflicts if check["status"] != "CLEAR"]
                if bad:
                    detail["endpointPruning"].append({
                        "removedSourceIndex": parts[i]["sourceIndex"],
                        "conflicts": [{"sourceIndex": parts[j]["sourceIndex"], **check}
                                      for j, check in bad]})
                else:
                    retained.append(i)
            if not retained:
                continue
            comp = components(set(retained), edges)[0]
            detail["collisionFreeComponentParts"] = len(comp)
            for count in dict.fromkeys((min(limits["maximumRegisteredSites"], len(comp) - 1),
                                       *limits["registeredCountFallbacks"])):
                if len(comp) <= count or count < limits["minimumRegisteredSites"]:
                    continue
                mutable = sorted(comp, key=lambda i: (parts[i]["rawMatrix"][1][3], i))[:count]
                fixed = components(comp - set(mutable), edges)[0]
                included = components(set(mutable) | fixed, edges)[0]
                mutable_sources = [parts[i]["sourceIndex"] for i in mutable if i in included]
                if len(mutable_sources) < limits["minimumRegisteredSites"] or not included.intersection(fixed):
                    continue
                selected, selected_edges, prov = load_source(
                    model, sorted(parts[i]["sourceIndex"] for i in included))
                try:
                    geometry = qualify(selected, mutable_sources, folder / "geometry.json")
                    source = {
                        "provenance": prov,
                        "edges": [e for e in selected_edges if e["family"] == "stud"],
                        "ignoredNonStudEdges": [e for e in selected_edges if e["family"] != "stud"],
                        "connectionScope": "Stud connectivity only; original source placements."}
                    domain = AssemblyDomain(geometry, source)
                    if not domain.supported(domain.full) or not list(domain.moves(domain.full)):
                        raise ValueError("No executable nontrivial full-assembly component")
                    # Exhaust only the physical component; no cost table or policy.
                    capacity = math.ceil(0.6 * domain.n)
                    queue, seen, removable = deque([domain.full]), {domain.full}, 0
                    while queue:
                        state = queue.popleft()
                        removable |= domain.full ^ state
                        for _, _, after in domain.moves(state):
                            if after not in seen and domain.n - after.bit_count() <= capacity:
                                seen.add(after)
                                queue.append(after)
                    if removable.bit_count() < limits["minimumReachableMovableSites"]:
                        raise ValueError(
                            f"Only {removable.bit_count()} reachable movable sites under rack capacity {capacity}")
                    (folder / "source.json").write_text(json.dumps(source, indent=2) + "\n")
                    profile = {
                        "id": profile_id, "title": metadata["title"] + " subassembly",
                        "sourceGroup": metadata["kit"], "sourceTheme": metadata["theme"],
                        "intakeStratum": metadata["intakeStratum"],
                        "capacity": capacity,
                        "split": "heldout-source" if model in plan["heldoutCandidates"] else "development",
                        "sampling": "frozen-source-plan", "introducedVersion": "2.3",
                        "registeredSites": domain.n, "sourceParts": len(domain.parts),
                        "reachableMovableSites": removable.bit_count()}
                    row.update(qualified=True, profile=profile,
                               transitionHash=domain.transition_hash,
                               geometryHash=canonical_hash(geometry), sourceHash=canonical_hash(source),
                               physicalStates=len(seen), reachabilityCapacity=capacity)
                    domain.supported.cache_clear()
                    print("ADMITTED", profile, flush=True)
                    return row
                except Exception as exc:
                    row["attempts"].append({"component": component_index,
                                            "registeredCandidateCount": count, "reason": str(exc)})
                    print("REJECT", model, count, str(exc)[:240], flush=True)
        row["qualified"] = False
    except Exception as exc:
        row.update(qualified=False, reason=str(exc))
    return row


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", help="Qualify one frozen candidate, writing an isolated record")
    parser.add_argument("--aggregate", action="store_true", help="Require and aggregate every frozen record")
    args = parser.parse_args()
    plan = json.loads((HERE / "source-plan.json").read_text())
    registry_bytes = registry_path(plan).read_bytes()
    assert hashlib.sha256(registry_bytes).hexdigest() == plan["candidateRegistrySha256"]
    registry = {r["id"]: r for r in json.loads(registry_bytes)["candidates"]}
    started = HERE / "data/source-admission-v23-started.json"
    if started.exists():
        assert json.loads(started.read_text())["planHash"] == canonical_hash(plan)
    else:
        started.write_text(json.dumps({"planHash": canonical_hash(plan)}, indent=2) + "\n")
    records = HERE / "data/source-admission-records"
    records.mkdir(exist_ok=True)
    models = [args.model] if args.model else plan["newCandidates"]
    assert set(models) <= set(plan["newCandidates"])
    for model in models:
        target = records / f"{model}.json"
        if target.exists():
            row = json.loads(target.read_text())
            assert row["planHash"] == canonical_hash(plan)
        else:
            assert not args.aggregate, f"Missing source admission record: {model}"
            row = qualify_model(model, plan, registry[model])
        proof = fidelity(model, plan)
        if row["qualified"] and not proof["passed"]:
            history = HERE / "data/source-admission-history" / f"{model}.before-source-fidelity.json"
            history.parent.mkdir(exist_ok=True)
            if history.exists():
                assert json.loads(history.read_text()) == row
            else:
                history.write_text(json.dumps(row, indent=2) + "\n")
            row.update(qualified=False, geometryQualifiedBeforeSourceAudit=True,
                       exclusionStage="source-fidelity", reason=proof["reason"])
        row["sourceFidelity"] = proof
        assert not row["qualified"] or proof["passed"]
        target.write_text(json.dumps(row, indent=2) + "\n")
        print("SOURCE_ADMISSION", model, row["qualified"], proof["passed"], flush=True)
    if args.model:
        return
    predecessor = json.loads((HERE.parent / "brickplan-v2.2/data/source-admission.json").read_text())
    additions = [json.loads((records / f"{model}.json").read_text()) for model in plan["newCandidates"]]
    assert all(r["planHash"] == canonical_hash(plan) for r in additions)
    (HERE / "data/source-admission.json").write_text(json.dumps({
        "schema": "brickplan-source-admission/2.3", "planHash": canonical_hash(plan),
        "predecessorAdmissionHash": canonical_hash(predecessor),
        "selectionOrder": plan["qualification"]["selection"],
        "sources": predecessor["sources"] + additions,
        "profiles": predecessor["profiles"] + [r["profile"] for r in additions if r["qualified"]],
        "newCandidateCount": len(additions), "newQualifiedCount": sum(r["qualified"] for r in additions)
    }, indent=2) + "\n")


if __name__ == "__main__":
    main()
