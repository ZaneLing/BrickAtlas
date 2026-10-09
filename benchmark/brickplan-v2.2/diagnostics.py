"""Construction-only controls for future conflicts, visual geometry and repair."""
from dataclasses import asdict
import json
import random

from mission import AssemblyDomain, Mission, State, canonical_hash
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


def geometry_pairs(builder, profiles):
    """Identical future plans, different independently qualified fixed context."""
    from bank import DATA
    path = DATA / "geometry-contrasts.json"
    if not path.exists():
        return []
    manifest = json.loads(path.read_text())
    lookup = {p["id"]: p for p in profiles}
    used_profiles = {t["profile"] for t in builder.episodes if t["kind"] == "visual-geometry-context"}
    for spec in manifest["pairs"]:
        if spec.get("introducedVersion") == "2.1":
            spec["retainedFutureContrasts"] = sum(
                p["kind"] == "visual-geometry" and p["id"].startswith(spec["id"] + "/")
                for p in builder.pairs)
            spec["sampling"] = "Preserved immutable 2.1 regression examples."
            continue
        maximum_pairs = 4 if spec.get("introducedVersion") == "2.1" else 2
        ds = [AssemblyDomain.load(DATA / p) for p in spec["profiles"]]
        cap = min(lookup[p]["capacity"] for p in spec["profiles"])
        graphs = [PhysicalGraph(d, cap, d.full) for d in ds]
        if graphs[0].states == graphs[1].states and graphs[0].edges == graphs[1].edges:
            spec["retainedFutureContrasts"] = 0
            spec["exclusion"] = "Identical executable physical component under the declared capacity."
            ds[0].supported.cache_clear()
            continue
        common = sorted(set(graphs[0].states) & set(graphs[1].states))
        rng = random.Random(spec["id"])
        rng.shuffle(common)
        retained = 0
        inspectable = [i for i in range(ds[0].n)
                       if all(any(not s & (1 << i) for s in g.states) for g in graphs)]
        inspectable.sort(key=lambda i: (not (ds[0].fixed_neighbors ^ ds[1].fixed_neighbors) & (1 << i), i))
        candidates = []
        for jobs in [()] + [(i,) for i in inspectable]:
            oracles = [Oracle(Mission(d, cap, d.full, jobs), g) for d, g in zip(ds, graphs)]
            for start in [ds[0].full, *common[:2048]]:
                state = State(start)
                if any(o.distance(state) <= 0 for o in oracles):
                    continue
                for direction in (0, 1):
                    good, other = oracles[direction], oracles[1 - direction]
                    plan = good.witness(state)
                    conflict = other.mission.replay(state, plan)["firstConflict"]
                    if conflict is not None and conflict >= 3:
                        candidates.append((oracles, state, plan, conflict))
                        break
                if len(candidates) >= maximum_pairs:
                    break
            if len(candidates) >= maximum_pairs:
                break
        for oracles, state, plan, conflict in candidates:
                pair_id = spec["id"] + f"/future-{retained:02d}"
                members = []
                for index, oracle in enumerate(oracles):
                    profile = lookup[spec["profiles"][index]]
                    task = builder.episode(profile, oracle, state, None,
                                           "visual-geometry-context", diagnostics=False)
                    used_profiles.add(profile["id"])
                    probe_id = pair_id + "/" + ("a" if index == 0 else "b")
                    builder.probes.append({
                        "id": probe_id, "kind": "geometry-continuation", "taskId": task["id"],
                        "state": asdict(state), "pairId": pair_id,
                        "plan": [a.json() for a in plan],
                        "firstConflict": oracle.mission.replay(state, plan)["firstConflict"],
                        "prompt": "Use the visible fixed support geometry to predict the FIRST illegal operation in this sequence (1-based), or null if every operation is legal. Registered pieces, their original poses, capacity and work orders are unchanged across the paired question."})
                    members.append(probe_id)
                builder.pairs.append({
                    "id": pair_id, "kind": "visual-geometry", "members": members,
                    "sameRegisteredPiecesAndPoses": True, "samePlan": True,
                    "sameStartGoalCapacityJobs": True, "sharedLegalPrefix": conflict - 1,
                    "fixedContext": spec["fixedContext"],
                    "qualification": spec["qualification"]})
                retained += 1
        spec["retainedFutureContrasts"] = retained
        spec["futureSampling"] = {
            "maximumPairs": maximum_pairs, "maximumCommonStarts": 2048,
            "selection": "Seeded common states; full-target witness conflicts after at least two legal operations.",
            "conditioning": "Mechanism-conditioned diagnostic; separate from frozen source episodes."}
        ds[0].supported.cache_clear()
        Mission.lower_bound.cache_clear()
    builder.geometry_census = manifest
    return [{**lookup[p], "registeredSites": d.n, "fixedParts": len(d.fixed),
             "sourceParts": len(d.parts), "hasAnswerChangingContrast": p in used_profiles}
            for p in sorted(lookup) if lookup[p]["sampling"] == "geometry-contrast"
            for d in [AssemblyDomain.load(DATA / p)]]
