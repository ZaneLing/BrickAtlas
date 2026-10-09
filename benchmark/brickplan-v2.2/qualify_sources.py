"""Predeclared source admission; reject geometry, never observed solver difficulty."""
from collections import deque
import json
import math
from pathlib import Path
import sys

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


def main():
    plan = json.loads((HERE / "source-plan.json").read_text())
    predecessor = json.loads((HERE.parent / "brickplan-v2.1/data/source-admission.json").read_text())
    rows, profiles = predecessor["sources"].copy(), predecessor["profiles"].copy()
    for model in plan["newCandidates"]:
        profile_id = "source-" + model
        folder = HERE / "data" / profile_id
        row = {"model": model, "attempts": [], "rejectedInstances": []}
        try:
            manifest = json.loads((ROOT / f"web/public/models/{model}/manifest.json").read_text())
            good = []
            for i, part in enumerate(manifest["instances"]):
                try:
                    load_source(model, [i])
                    good.append(i)
                except Exception as exc:
                    row["rejectedInstances"].append(
                        {"sourceIndex": i, "part": part["partNumber"], "reason": str(exc)[:200]})
            parts, edges, provenance = load_source(model, good)
            comp = components(set(range(len(parts))), edges)[0]
            comp = bounded_component(comp, edges, 180)
            row["validInstances"] = len(good)
            row["candidateParts"] = len(comp)
            # Geometry-only refinement after the all-or-nothing first pass:
            # greedily retain collision-free source instances in source order,
            # then keep the largest remaining stud-connected component.
            # This runs before any policy or oracle is evaluated on new sources.
            retained = []
            row["endpointPruning"] = []
            for i in sorted(comp):
                conflicts = [(j, endpoint_pair(parts[i], parts[j])) for j in retained]
                bad = [(j, check) for j, check in conflicts if check["status"] != "CLEAR"]
                if bad:
                    row["endpointPruning"].append({
                        "removedSourceIndex": parts[i]["sourceIndex"],
                        "conflicts": [{"sourceIndex": parts[j]["sourceIndex"], **check}
                                      for j, check in bad]})
                else:
                    retained.append(i)
            comp = components(set(retained), edges)[0]
            row["collisionFreeComponentParts"] = len(comp)
            # Fixed, deterministic geometric fallbacks. No oracle is used here.
            for count in dict.fromkeys((min(16, len(comp) - 1), 12, 8, 4, 2, 1)):
                if len(comp) <= count:
                    continue
                mutable = sorted(comp, key=lambda i: (parts[i]["rawMatrix"][1][3], i))[:count]
                fixed = components(comp - set(mutable), edges)[0]
                included = components(set(mutable) | fixed, edges)[0]
                mutable_sources = [parts[i]["sourceIndex"] for i in mutable if i in included]
                if not mutable_sources or not included.intersection(fixed):
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
                    (folder / "source.json").write_text(json.dumps(source, indent=2) + "\n")
                    profile = {
                        "id": profile_id, "title": f"Source {model} subassembly",
                        "sourceGroup": model.removeprefix("omr-"),
                        "capacity": math.ceil(0.6 * domain.n),
                        "split": "heldout-source" if model in plan["heldoutCandidates"] else "development",
                        "sampling": "frozen-source-plan",
                        "introducedVersion": "2.2",
                        "registeredSites": domain.n, "sourceParts": len(domain.parts)}
                    profiles.append(profile)
                    row.update(qualified=True, profile=profile,
                               transitionHash=domain.transition_hash)
                    print("ADMITTED", profile, flush=True)
                    break
                except Exception as exc:
                    row["attempts"].append({"registeredCandidateCount": count, "reason": str(exc)})
                    print("REJECT", model, count, str(exc)[:240], flush=True)
            else:
                row["qualified"] = False
        except Exception as exc:
            row.update(qualified=False, reason=str(exc))
        rows.append(row)
        (HERE / "data/source-admission.json").write_text(json.dumps({
            "schema": "brickplan-source-admission/2.2", "planHash": canonical_hash(plan),
            "predecessorAdmissionHash": canonical_hash(predecessor),
            "selectionOrder": "Geometry before solver; source-order endpoint pruning then connected component; registered count fallbacks min(16,n-1),12,8,4,2,1.",
            "sources": rows, "profiles": profiles}, indent=2) + "\n")


if __name__ == "__main__":
    main()
