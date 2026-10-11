"""Construction-only controls for future conflicts, visual geometry and repair."""
from dataclasses import asdict
from collections import deque
import json
import random

from mission import Action, AssemblyDomain, Mission, State, canonical_hash
from oracle import Oracle, PhysicalGraph
from metrics import optimal_corridor, repair_distances


def continuation_pairs(task, oracle):
    witness = oracle.witness(State(**task["start"]))
    candidates = {}
    for i in range(1, len(witness) - 2):
        for j in range(i + 1, len(witness) - 1):
            plan = witness.copy()
            plan[i], plan[j] = plan[j], plan[i]
            conflict = oracle.mission.replay(State(**task["start"]), plan)["firstConflict"]
            if conflict == i + 1 and conflict not in candidates:
                candidates[conflict] = plan
    result = []
    for conflict, plan in sorted(candidates.items()):
        pair_id = f'{task["id"]}/continuation-{conflict:02d}'
        probes = []
        rows = [(witness, None), (plan, conflict)]
        random.Random(pair_id).shuffle(rows)
        for member, (actions, label) in zip(("a", "b"), rows):
            probes.append({
                "id": pair_id + "/" + member, "kind": "continuation", "taskId": task["id"],
                "state": task["start"], "pairId": pair_id, "firstConflict": label,
                "plan": [a.json() for a in actions],
                "prompt": "Execute the proposed sequence mentally under the visible assembly, rack and work orders. Report the FIRST illegal operation (1-based), or null if every operation is legal."})
        result.append({
            "bin": "early" if conflict <= 5 else "middle" if conflict <= 10 else "late",
            "probes": probes, "pair": {
                "id": pair_id, "kind": "interior-order", "members": [p["id"] for p in probes],
                "sameFirstAndLast": True, "sameActionMultiset": True,
                "sharedLegalPrefix": conflict - 1, "firstConflict": conflict,
                "validPlanIsOptimalWitness": True}})
    return result


def delayed_repair_probes(task, oracle, states):
    rng = random.Random("repair/" + task["id"])
    checkpoints = list(enumerate(states[:-1]))
    rng.shuffle(checkpoints)
    census = {"taskId": task["id"], "fixedLags": [1, 3, 5], "retainedLags": []}
    for step, checkpoint in checkpoints:
        mistakes = [(a, s) for a, s in oracle.mission.moves(checkpoint)
                    if oracle.distance(s) >= oracle.distance(checkpoint)]
        rng.shuffle(mistakes)
        if not mistakes:
            continue
        corridor = optimal_corridor(oracle, checkpoint) - {oracle.target}
        distances = repair_distances(oracle, corridor)
        action, current = mistakes[0]
        history, visited = [action], {checkpoint, current}
        probes = []
        for lag in range(1, 6):
            options = [(a, s) for a, s in oracle.mission.moves(current)
                       if s not in visited and oracle.encode(s) not in corridor
                       and s != oracle.mission.terminal and distances[oracle.encode(s)] > 0]
            if not options:
                break
            action, current = rng.choice(sorted(options, key=lambda x: x[0]))
            history.append(action)
            visited.add(current)
            if lag not in (1, 3, 5):
                continue
            choices = sorted(oracle.mission.moves(current), key=lambda x: x[0])
            cost = distances[oracle.encode(current)]
            labels = [{"action": a.json(),
                       "remainingRepairCost": distances[oracle.encode(s)],
                       "conditionalExtraCost": (1 + distances[oracle.encode(s)] - cost
                                                if distances[oracle.encode(s)] >= 0 else None)}
                      for a, s in choices]
            probes.append({
                "id": f'{task["id"]}/repair-lag-{lag}', "kind": "delayed-repair",
                "taskId": task["id"], "state": asdict(current),
                "checkpoint": asdict(checkpoint), "witnessStep": step,
                "history": [a.json() for a in history],
                "lagAfterError": lag, "minimumRepairCost": cost,
                "checkpointRemainingOptimal": oracle.distance(checkpoint),
                "choices": [a.json() for a, _ in choices], "labels": labels,
                "optimalChoices": [i for i, label in enumerate(labels)
                                   if label["conditionalExtraCost"] == 0],
                "prompt": "A legal but avoidably costly action was followed by the listed operations. Choose the next action that minimizes operations to rejoin ANY nonterminal state on an optimal completion from the displayed pre-error checkpoint. Reaching the goal alone does not count as repair."})
            census["retainedLags"].append(lag)
        if probes:
            census["checkpointStep"] = step
            return probes, census
    census["exclusion"] = "No seeded distinct-state delayed path outside the nonterminal optimal corridor."
    return [], census


def optimal_shared_prefix(good, other, boundary, preferred=4):
    """Find real optimal predecessors, never pad a plan with no-ops or undo loops."""
    queue = deque([(boundary, [])])
    seen, fallback = {boundary}, None
    while queue:
        current, prefix = queue.popleft()
        if len(prefix) >= 2:
            fallback = current, prefix
        if len(prefix) == preferred:
            return current, prefix
        if len(seen) > 4096:
            break
        for op, site, index in good.graph.edges[good.graph.index[current.assembly]]:
            assembly = good.graph.states[index]
            previous = State(assembly, current.done)
            reverse = Action("attach" if op == "detach" else "detach", site)
            if (previous not in seen and assembly in other.graph.index
                    and good.distance(previous) == good.distance(current) + 1
                    and other.mission.transition(previous, reverse) == (current, "OK")):
                seen.add(previous)
                queue.append((previous, [reverse, *prefix]))
    return fallback


def geometry_candidates(ds, graphs, cap, pair_id, maximum=2):
    """Search Bellman-equality paths through a differing edge, including tied optima."""
    boundary = []
    for direction, graph in enumerate(graphs):
        other = graphs[1 - direction]
        for assembly in graph.states:
            if assembly not in other.index:
                continue
            for op, site, index in graph.edges[graph.index[assembly]]:
                after = graph.states[index]
                if after not in other.index:
                    boundary.append((direction, assembly, Action(op, site), after))
    boundary.sort(key=lambda r: canonical_hash(
        {"seed": 20261010, "pair": pair_id, "edge": [r[0], r[1], r[2].json(), r[3]]}))
    # Every boundary detach site is considered for an explicit work order.
    jobs_to_try = sorted({r[2].site for r in boundary})
    result, identities = [], set()
    for jobs in [()] + [(site,) for site in jobs_to_try]:
        oracles = [Oracle(Mission(d, cap, d.full, jobs), g) for d, g in zip(ds, graphs)]
        for direction, assembly, action, after in boundary:
            good, other = oracles[direction], oracles[1 - direction]
            state, target = State(assembly), State(after)
            if good.distance(target) < 0 or good.distance(state) != 1 + good.distance(target):
                continue
            preferred = (2, 4, 6)[int(canonical_hash(
                {"pair": pair_id, "assembly": assembly, "jobs": jobs})[:8], 16) % 3]
            prefix = optimal_shared_prefix(good, other, state, preferred)
            if prefix is None:
                continue
            start, actions = prefix
            if other.distance(start) <= 0:
                continue
            plan = [*actions, action, *good.witness(target)]
            key = canonical_hash({"start": asdict(start), "jobs": jobs,
                                  "plan": [a.json() for a in plan]})
            if key in identities:
                continue
            replay = good.mission.replay(start, plan)
            conflict = other.mission.replay(start, plan)["firstConflict"]
            assert replay["firstConflict"] is None and replay["state"] == good.mission.terminal
            assert len(plan) == good.distance(start)
            assert conflict == len(actions) + 1 and conflict >= 3
            identities.add(key)
            result.append((oracles, start, plan, conflict))
            if len(result) == maximum:
                return result, len(boundary)
    return result, len(boundary)


def geometry_pairs(builder, profiles):
    """Identical future plans, different independently qualified fixed context."""
    from bank import DATA, write_json
    path = DATA / "geometry-contrasts.json"
    if not path.exists():
        return []
    manifest = json.loads(path.read_text())
    lookup = {p["id"]: p for p in profiles}
    used_profiles = {t["profile"] for t in builder.episodes if t["kind"] == "visual-geometry-context"}
    for spec in manifest["pairs"]:
        if spec.get("introducedVersion") != "2.3":
            spec["retainedFutureContrasts"] = sum(
                p["kind"] == "visual-geometry" and p["id"].startswith(spec["id"] + "/")
                for p in builder.pairs)
            spec["sampling"] = "Historical unmatched regression; excluded from primary visual score."
            continue
        maximum_pairs = 2
        ds = [AssemblyDomain.load(DATA / p) for p in spec["profiles"]]
        cap = min(lookup[p]["capacity"] for p in spec["profiles"])
        cache_path = DATA / "geometry-fragments" / (spec["id"].replace("/", "-") + ".json")
        input_hash = canonical_hash({
            "spec": spec, "domains": [d.transition_hash for d in ds], "capacity": cap,
            "code": {name: (DATA.parent / name).read_text() for name in
                     ("build.py", "diagnostics.py", "oracle.py", "mission.py", "policies.py")}})
        cached = json.loads(cache_path.read_text()) if cache_path.exists() else None
        if cached and cached.get("inputHash") == input_hash:
            builder.episodes.extend(cached["episodes"])
            builder.probes.extend(cached["probes"])
            builder.pairs.extend(cached["pairs"])
            builder.certificates.update(cached["oracles"])
            builder.counts.update(t["profile"] for t in cached["episodes"])
            used_profiles.update(t["profile"] for t in cached["episodes"])
            spec.update(cached["census"])
            print("GEOMETRY_FRAGMENT", spec["id"], spec["retainedFutureContrasts"], flush=True)
            continue
        before = (len(builder.episodes), len(builder.probes), len(builder.pairs), set(builder.certificates))
        graphs = [PhysicalGraph(d, cap, d.full) for d in ds]
        if graphs[0].states == graphs[1].states and graphs[0].edges == graphs[1].edges:
            spec["retainedFutureContrasts"] = 0
            spec["exclusion"] = "Identical executable physical component under the declared capacity."
            ds[0].supported.cache_clear()
            continue
        rng = random.Random(spec["id"])
        retained = 0
        candidates, boundary_count = geometry_candidates(ds, graphs, cap, spec["id"], maximum_pairs)
        for oracles, state, plan, conflict in candidates:
                pair_id = spec["id"] + f"/future-{retained:02d}"
                members = []
                order = rng.sample([0, 1], 2)
                for member, index in enumerate(order):
                    oracle = oracles[index]
                    profile = lookup[spec["profiles"][index]]
                    task = builder.episode(profile, oracle, state, None,
                                           "visual-geometry-context", diagnostics=False)
                    used_profiles.add(profile["id"])
                    probe_id = pair_id + "/" + ("a" if member == 0 else "b")
                    builder.probes.append({
                        "id": probe_id, "kind": "geometry-continuation", "taskId": task["id"],
                        "state": asdict(state), "pairId": pair_id,
                        "evaluationCohort": "primary-matched",
                        "plan": [a.json() for a in plan],
                        "firstConflict": oracle.mission.replay(state, plan)["firstConflict"],
                        "prompt": "Use the visible fixed support geometry to predict the FIRST illegal operation in this sequence (1-based), or null if every operation is legal. Registered pieces, their original poses, capacity and work orders are unchanged across the paired question."})
                    members.append(probe_id)
                builder.pairs.append({
                    "id": pair_id, "kind": "visual-geometry", "members": members,
                    "introducedVersion": "2.3",
                    "sameRegisteredPiecesAndPoses": True, "samePlan": True,
                    "sameStartGoalCapacityJobs": True, "sharedLegalPrefix": conflict - 1,
                    "evaluationCohort": "primary-matched", "interventionId": spec["id"],
                    "sourceGroup": lookup[spec["profiles"][0]]["sourceGroup"],
                    "split": lookup[spec["profiles"][0]]["split"],
                    "validPlanIsOptimal": True,
                    "fixedContext": spec["fixedContext"],
                    "qualification": spec["qualification"]})
                retained += 1
        spec["retainedFutureContrasts"] = retained
        spec["futureSampling"] = {
            "maximumPairs": maximum_pairs, "boundaryEdges": boundary_count,
            "selection": "Seeded differing-edge order; Bellman-equality shared predecessors and exact optimal completion. Includes tied optimal plans. Preferred genuine legal prefixes 2/4/6; minimum 2.",
            "noPaddingOrRepeatedStates": True, "validPlanIsOptimal": True,
            "conditioning": "Mechanism-conditioned diagnostic; separate from frozen source episodes."}
        write_json(cache_path, {
            "inputHash": input_hash, "episodes": builder.episodes[before[0]:],
            "probes": builder.probes[before[1]:], "pairs": builder.pairs[before[2]:],
            "oracles": {k: v for k, v in builder.certificates.items() if k not in before[3]},
            "census": {k: spec[k] for k in ("retainedFutureContrasts", "futureSampling")},
        })
        ds[0].supported.cache_clear()
        Mission.lower_bound.cache_clear()
    builder.geometry_census = manifest
    return [{**lookup[p], "registeredSites": d.n, "fixedParts": len(d.fixed),
             "sourceParts": len(d.parts), "hasAnswerChangingContrast": p in used_profiles}
            for p in sorted(lookup) if lookup[p]["sampling"] == "geometry-contrast"
            for d in [AssemblyDomain.load(DATA / p)]]
