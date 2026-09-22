#!/usr/bin/env python3
"""Finite-source census, frozen split, bounded search and repair certificates."""
import itertools
import math
import random
import re
from collections import Counter, defaultdict

from common import ASSETS, HERE, ROOT, SEED, VERSION, digest, read, reference, write

MAX_PROPOSALS = 512


def reachability(nodes, edges, absent=()):
    remaining = set(nodes) - set(absent)
    adj = {n: set() for n in remaining}
    for a, b in edges:
        if a in adj and b in adj:
            adj[a].add(b)
            adj[b].add(a)
    groups = []
    while remaining:
        seen, queue = set(), [min(remaining)]
        while queue:
            node = queue.pop()
            if node not in seen:
                seen.add(node)
                queue.extend(adj[node] - seen)
        groups.append(sorted(seen))
        remaining -= seen
    return sorted(groups, key=lambda g: (-len(g), g))


def enumerate_repairs(nodes, edges, missing, fixed, candidates):
    # Bitset reachability enumerates each subset once for all four bindings.
    index = {v: i for i, v in enumerate(nodes)}
    bits = {v: 1 << i for v, i in index.items()}
    adj = [0] * len(nodes)
    for a, b in edges:
        adj[index[a]] |= bits[b]
        adj[index[b]] |= bits[a]
    present = ((1 << len(nodes)) - 1) ^ sum(bits[v] for v in missing)
    required = [sum(bits[v] for v in fixed) | bits[c] for c in candidates]
    answers = [None] * len(candidates)
    for size in range(len(missing) + 1):
        unfinished = [i for i, a in enumerate(answers) if a is None]
        if not unfinished:
            break
        for restored in itertools.combinations(missing, size):
            active = present | sum(bits[v] for v in restored)
            seen, frontier = 0, bits[fixed[0]]
            while frontier:
                seen |= frontier
                neighbors, todo = 0, frontier
                while todo:
                    bit = todo & -todo
                    neighbors |= adj[bit.bit_length() - 1]
                    todo ^= bit
                frontier = neighbors & active & ~seen
            for i in unfinished:
                if seen & required[i] == required[i]:
                    if answers[i] is None:
                        answers[i] = {"minimum_cost": size, "sets": []}
                    answers[i]["sets"].append(tuple(sorted(restored)))
    return answers


def topology_key(nodes, edges):
    adj = {n: [] for n in nodes}
    for a, b in edges:
        adj[a].append(b)
        adj[b].append(a)
    colors = {n: str(len(adj[n])) for n in nodes}
    # Equal refinement hashes conservatively merge possible collisions.
    for _ in range(len(nodes)):
        colors = {n: digest([colors[n], sorted(colors[k] for k in adj[n])]) for n in nodes}
    return digest([len(nodes), len(edges), sorted(colors.values())])


def design_key(parts):
    positions = {p["instanceId"]: p["originalMatrix"][12:15] for p in parts}
    pairs = []
    for a, b in itertools.combinations(parts, 2):
        pa, pb = positions[a["instanceId"]], positions[b["instanceId"]]
        pairs.append([*sorted([a["partNumber"], b["partNumber"]]),
                      round(math.dist(pa, pb), 2)])
    return digest([sorted(p["partNumber"] for p in parts), sorted(pairs)])


def inventory():
    models, records, source_rows = {}, [], []
    for entry in read(ROOT / "benchmark/ldraw-v2/catalog.json"):
        sid = entry["id"]
        mp = ROOT / f"public/models/{sid}/manifest.json"
        bp = ROOT / f"public/benchmark/ldraw-v2/models/{sid}.json"
        m, b = read(mp), read(bp)
        models[sid] = m
        credits = [re.sub(r"\s*\[[^\]]*\]", "", c).strip()
                   for c in entry["author"].split(", OMR by ")]
        source_rows.append({"source_id": sid, "contributors": credits,
                            "manifest": reference(mp), "graph": reference(bp),
                            "license": entry["license"], "source_url": entry["sourceUrl"]})
        submodels = {s["id"]: s for s in m["submodels"]}
        unsupported = {p["instanceId"] for p in b["audit"]["unsupported"]}
        for sub in m["submodels"]:
            if sub["parentId"] is None:
                continue
            descendants = {sub["id"]}
            while True:
                more = {s["id"] for s in submodels.values() if s["parentId"] in descendants}
                if more <= descendants:
                    break
                descendants |= more
            parts = [p for p in m["instances"] if p["parentSubmodelId"] in descendants]
            if not 12 <= len(parts) <= 100:
                continue
            nodes = sorted(p["instanceId"] for p in parts)
            nset = set(nodes)
            edges = sorted({tuple(sorted((e["a"], e["b"]))) for e in b["audit"]["edges"]
                            if e["a"] in nset and e["b"] in nset})
            intersections = [p for p in b["audit"]["nonMatingCollisionPairs"] if set(p) <= nset]
            reason = ("unsupported_connector" if nset & unsupported else
                      "disconnected" if len(reachability(nodes, edges)) != 1 else None)
            records.append({"candidate_id": digest([sid, sub["id"]])[:20],
                            "source_id": sid, "submodel_id": sub["id"],
                            "nodes": nodes, "edges": edges, "parts": len(nodes),
                            "recognized_edges": len(edges), "intersections": intersections,
                            "census_eligible": reason is None,
                            "exclusion": reason or ("recorded_intersection" if intersections else None),
                            "design_group": design_key(parts),
                            "template_group": topology_key(nodes, edges)})
    return models, records, source_rows


def freeze_groups(records, sources):
    parent = {s["source_id"]: s["source_id"] for s in sources}

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    memberships = defaultdict(set)
    for s in sources:
        for credit in s["contributors"]:
            memberships["contributor:" + credit].add(s["source_id"])
    for r in records:
        if r["exclusion"] is None:
            memberships["design:" + r["design_group"]].add(r["source_id"])
            memberships["template:" + r["template_group"]].add(r["source_id"])
    for members in memberships.values():
        for a, b in itertools.combinations(sorted(members), 2):
            parent[find(a)] = find(b)
    clusters = defaultdict(list)
    for source in parent:
        clusters[find(source)].append(source)
    groups = {source: "group-" + digest(sorted(members))[:12]
              for members in clusters.values() for source in members}
    active = sorted({groups[r["source_id"]] for r in records if r["exclusion"] is None},
                    key=lambda g: digest([SEED, "split", g]))
    dev = set(active[:max(1, len(active) // 3)])
    for r in records:
        r["dependence_group"] = groups[r["source_id"]]
        r["split"] = "dev" if r["dependence_group"] in dev else "heldout"
    return [{"id": g, "split": "dev" if g in dev else "heldout",
             "sources": sorted(s for s in groups if groups[s] == g)}
            for g in active]


def search(record, model):
    rng = random.Random(digest([SEED, "search", record["candidate_id"]]))
    nodes, edges = record["nodes"], record["edges"]
    pmap = {p["instanceId"]: p for p in model["instances"]}
    types = defaultdict(list)
    for node in nodes:
        types[pmap[node]["partNumber"]].append(node)
    reject = Counter()
    if len(types) < 4:
        return None, {"proposals": 0, "rejections": {"fewer_than_four_types": 1}}
    for attempt in range(MAX_PROPOSALS):
        candidates = [rng.choice(types[t]) for t in rng.sample(sorted(types), 4)]
        available = sorted(set(nodes) - set(candidates))
        fixed = rng.sample(available, 2)
        pool = sorted(set(available) - set(fixed))
        # Leave one present vertex for the structural exchange.
        m0 = sorted(rng.sample(pool, min(8, len(pool) - 1)))
        m1 = sorted(set(m0) - {rng.choice(m0)} |
                    {rng.choice(sorted(set(pool) - set(m0)))})
        answers = [enumerate_repairs(nodes, edges, m, fixed, candidates) for m in (m0, m1)]
        pair = None
        for a, b in itertools.combinations(range(4), 2):
            four = [answers[f][t] for f in range(2) for t in (a, b)]
            if any(x is None or x["minimum_cost"] < 2 for x in four):
                continue
            opts = [[set(answers[f][t]["sets"]) for t in (a, b)] for f in range(2)]
            if any(opts[f][0] & opts[f][1] for f in range(2)):
                continue
            if any(opts[0][t] & opts[1][t] for t in range(2)):
                continue
            pair = (a, b)
            break
        if pair is None:
            reject["dependency_or_cost"] += 1
            continue
        # Record this gold-conditioned search, not a random sample of faults.
        return {"candidates": candidates, "fixed": fixed, "missing": [m0, m1],
                "target": pair[0], "alternate": pair[1], "answers": answers}, {
                    "proposals": attempt + 1, "selected_proposal": attempt,
                    "rejections": dict(reject)}
    return None, {"proposals": MAX_PROPOSALS, "rejections": dict(reject)}


def build():
    models, records, sources = inventory()
    groups = freeze_groups(records, sources)
    used, designs = defaultdict(set), {}
    ordered = sorted(records, key=lambda r: digest([SEED, "order", r["candidate_id"]]))
    deduplicated = []
    for r in ordered:
        if r["exclusion"]:
            continue
        if used[r["source_id"]] & set(r["nodes"]):
            r["exclusion"] = "nested_or_overlapping"
        elif r["design_group"] in designs:
            r["exclusion"] = "duplicate_design"
            r["duplicate_of"] = designs[r["design_group"]]
        else:
            deduplicated.append(r)
            used[r["source_id"]].update(r["nodes"])
            designs[r["design_group"]] = r["candidate_id"]
    tasks, gold, renders, selected = [], [], {}, []
    for r in deduplicated:
        solution, search_log = search(r, models[r["source_id"]])
        r["search"] = search_log
        if solution is None:
            r["exclusion"] = "search_exhausted"
            continue
        selected.append(r)
        cid = "construction-" + r["candidate_id"]
        r["construction_id"] = cid
        r["selection"] = solution
        for replicate in range(2):
            # IDs, order, task names, fault names, and image names use independent domains.
            rng = random.Random(digest([SEED, "ids", cid, replicate]))
            mapping = dict(zip(r["nodes"], [f"V{x:04d}" for x in rng.sample(range(1000, 10000), len(r["nodes"]))]))
            order_rng = random.Random(digest([SEED, "cards", cid, replicate]))
            order = list(range(4))
            order_rng.shuffle(order)
            candidates = solution["candidates"]
            target, alternate = solution["target"], solution["alternate"]
            distractors = [i for i in range(4) if i not in (target, alternate)]
            r.setdefault("private_id_maps", []).append(mapping)
            for arm in ("anchor", "changing", "preserving"):
                binding = list(range(4))
                if arm != "anchor":
                    a, b = (target, alternate) if arm == "changing" else distractors
                    binding[a], binding[b] = binding[b], binding[a]
                image_id = "image-" + digest([SEED, "image", cid, replicate, arm])[:20]
                renders[image_id] = {
                    "model": r["source_id"], "construction_id": cid,
                    "replicate": replicate, "arm": arm,
                    "source_ids": r["nodes"], "reference_id": candidates[target],
                    "cards": [{"source_id": candidates[i], "label": mapping[candidates[binding[i]]]}
                              for i in order],
                    "width": 1600, "height": 900,
                }
                bound_index = binding[target]
                for fault in range(2):
                    task_id = "task-" + digest([SEED, "task", cid, replicate, arm, fault])[:20]
                    norder = list(r["nodes"])
                    rng.shuffle(norder)
                    eorder = list(r["edges"])
                    rng.shuffle(eorder)
                    missing = solution["missing"][fault]
                    corder = candidates.copy()
                    rng.shuffle(corder)
                    answer = solution["answers"][fault][bound_index]
                    budget = 2 + int(digest([SEED, "budget", cid])[:2], 16) % 3
                    public_input = {"graph": {"nodes": [mapping[n] for n in norder],
                                               "edges": [[mapping[a], mapping[b]] for a, b in eorder]},
                                    "missing": [mapping[n] for n in missing],
                                    "fixed_terminals": [mapping[n] for n in solution["fixed"]],
                                    "candidate_ids": [mapping[n] for n in corder],
                                    "budget": budget, "cost_per_vertex": 1}
                    # All serialization stays fixed across both intervention axes.
                    text_rng = random.Random(digest([SEED, "text", cid, replicate]))
                    for key in ("missing", "fixed_terminals", "candidate_ids"):
                        public_input[key].sort()
                        text_rng.shuffle(public_input[key])
                    public_input["graph"]["nodes"].sort()
                    text_rng.shuffle(public_input["graph"]["nodes"])
                    public_input["graph"]["edges"].sort()
                    text_rng.shuffle(public_input["graph"]["edges"])
                    missing_order = sorted(solution["missing"][0])
                    text_rng.shuffle(missing_order)
                    if fault:
                        removed = next(iter(set(solution["missing"][0]) - set(missing)))
                        added = next(iter(set(missing) - set(solution["missing"][0])))
                        missing_order[missing_order.index(removed)] = added
                    public_input["missing"] = [mapping[n] for n in missing_order]
                    tasks.append({"id": task_id, "construction_id": cid, "source_id": r["source_id"],
                                  "dependence_group": r["dependence_group"], "split": r["split"],
                                  "replicate": replicate, "visual_arm": arm,
                                  "structural_arm": f"fault_{fault}", "input": public_input,
                                  "image": f"public/benchmark/{VERSION}/images/{image_id}.png"})
                    solutions = []
                    for restored in answer["sets"]:
                        components = reachability(r["nodes"], r["edges"], set(missing) - set(restored))
                        solutions.append({"restored": [mapping[n] for n in restored],
                                          "component_sizes": [len(g) for g in components]})
                    gold.append({"id": task_id, "answer": {
                        "bound_terminal": mapping[candidates[bound_index]],
                        "minimum_cost": answer["minimum_cost"],
                        "budget_sufficient": answer["minimum_cost"] <= budget,
                        "solutions": solutions}})
        print(f"{cid}: {r['source_id']} {r['parts']} nodes, proposal {search_log['proposals']}", flush=True)
    assert selected, "No qualifying constructions; preserve ledger and revise version explicitly."
    counts = Counter(r["exclusion"] or "selected" for r in records)
    summary = {
        "version": VERSION, "candidate_count": sum(r["census_eligible"] for r in records),
        "eligible_count": sum(r["census_eligible"] and not r["intersections"] for r in records),
        "deduplicated_count": len(deduplicated), "construction_count": len(selected),
        "source_count": len({r["source_id"] for r in selected}),
        "dependence_group_count": len({r["dependence_group"] for r in selected}),
        "dev_constructions": sum(r["split"] == "dev" for r in selected),
        "heldout_constructions": sum(r["split"] == "heldout" for r in selected),
        "dev_groups": len({r["dependence_group"] for r in selected if r["split"] == "dev"}),
        "heldout_groups": len({r["dependence_group"] for r in selected if r["split"] == "heldout"}),
        "observation_count": len(tasks),
        "visual_changing_pairs": 4 * len(selected), "visual_preserving_pairs": 4 * len(selected),
        "structural_pairs": 6 * len(selected), "exclusions": dict(counts),
        "node_range": [min(r["parts"] for r in selected), max(r["parts"] for r in selected)],
        "edge_range": [min(r["recognized_edges"] for r in selected), max(r["recognized_edges"] for r in selected)],
        "minimum_cost_range": [min(g["answer"]["minimum_cost"] for g in gold), max(g["answer"]["minimum_cost"] for g in gold)],
        "optimum_count_range": [min(len(g["answer"]["solutions"]) for g in gold), max(len(g["answer"]["solutions"]) for g in gold)],
        "physical_scope": "Exact recognized graph, not physical extraction, insertion, stability or dynamics.",
        "population_scope": "Finite checked-in source resource; no broad unseen-design population claim.",
        "precision": {"target_half_width": .20, "normal_worst_case_groups_required": 25,
                      "attained": len({r["dependence_group"] for r in selected}) >= 25,
                      "interpretation": "Sensitivity target only; views cannot increase independent group count."},
    }
    write(HERE / "public.json", {"version": VERSION, "family": "visually-bound-minimum-terminal-repair", "tasks": tasks})
    write(HERE / "gold.json", {"version": VERSION, "status": "constructor-certificates-not-responses", "tasks": gold})
    write(HERE / "render-specs.json", renders)
    write(HERE / "sampling-ledger.json", {"version": VERSION, "seed": SEED,
          "max_proposals": MAX_PROPOSALS, "groups_frozen_before_search": groups, "sources": sources,
          "group_rule": "Transitive shared source/contributor/design/unlabeled-topology-refinement; hash collisions merge, never split.",
          "design_rule": "Part-number multiset and typed pairwise source-origin distances rounded to 0.01 mm; conservative signature, not full shape isomorphism.",
          "records": records})
    write(HERE / "summary.json", summary)
    ASSETS.mkdir(parents=True, exist_ok=True)
    print(summary)


if __name__ == "__main__":
    build()
