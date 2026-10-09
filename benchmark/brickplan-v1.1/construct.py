"""Extended task constructor: explicit CF checkpoints, unchanged engine/metrics.

Adapted from the frozen 1.0 constructor. Unlike its two checkpoint presets, an
extension may explicitly omit downstream covers at a counterfactual checkpoint.
Every such checkpoint still requires exact reachability and local-legal checks.
"""
from build import (budget, continuations, find_checkpoint, mandatory_order,
                   write_gzip, write_json)
from engine import AssemblyDomain, canonical_hash, minimum_detaches, no_undo, verify_distances


def build_case(config, data, rebuild_geometry=False):
    folder = data / config["id"]
    if rebuild_geometry:
        from geometry import load_source, qualify
        parts, edges, provenance = load_source(config["model"], config["included"])
        qualify(parts, config["mutable"], folder / "geometry.json", config.get("reversePaths", []))
        write_json(folder / "source.json", {"provenance": provenance, "edges": edges})
    domain = AssemblyDomain.load(folder)
    reachable = domain.distances(0)
    costs, checks = {}, {}

    def cost(goal):
        if str(goal) not in costs:
            table = domain.distances(goal)
            checks[str(goal)] = verify_distances(domain, goal, table, reachable)
            costs[str(goal)] = list(table)
            print(config["id"], "certified goal", goal, checks[str(goal)], flush=True)
        return costs[str(goal)]

    full_cost = cost(domain.full)
    start, good, bad = find_checkpoint(domain, full_cost, reachable)
    repair = max((s for s, distance in enumerate(reachable) if distance >= 0
                  and minimum_detaches(s, domain.full, full_cost) == 3),
                 key=lambda s: (s.bit_count(), -reachable[s], -s))
    healthy = next(s for s, distance in enumerate(reachable) if distance >= 0
                   and s.bit_count() == repair.bit_count() and no_undo(s, domain.full, full_cost))
    episodes = []
    for mode, state in (("full", 0), ("checkpoint", start), ("repair", repair), ("healthy", healthy)):
        episodes.append({
            "id": f"{config['id']}/{mode}", "case": config["id"], "mode": mode,
            "start": state, "goal": domain.full,
            "budget": budget(full_cost[repair] if mode in ("repair", "healthy") else full_cost[state]),
            "inspectBudget": 32, "diagnoseBudget": 8,
            "optimalActions": full_cost[state],
            "minimumDetaches": minimum_detaches(state, domain.full, full_cost),
            "startWitness": domain.witness(0, state, domain.distances(state)),
            "completionWitness": domain.witness(state, domain.full, full_cost),
        })
    choice = {
        "id": f"{config['id']}/choice", "case": config["id"], "start": start,
        "goal": domain.full, "budget": full_cost[start],
        "candidates": [{"type": "attach", "site": site} for site in sorted(good + bad)], "labels": [],
    }
    for action in choice["candidates"]:
        after, code = domain.transition(start, action["type"], action["site"])
        assert code == "OK"
        choice["labels"].append({"noUndoLoss": not no_undo(after, domain.full, full_cost),
                                 "budgetLoss": 1 + full_cost[after] > choice["budget"]})
    lookahead = []
    probe_start, _, probe_bad = find_checkpoint(domain, full_cost, reachable, minimum_actions=0)
    probe_trap, _ = domain.transition(probe_start, "attach", probe_bad[0])
    for horizon in (1, 2, 4, 8):
        failed, legal = continuations(domain, probe_trap, max(1, horizon - 1))
        if horizon > 1:
            prefix = [{"type": "attach", "site": probe_bad[0]}]
            failed, legal = prefix + failed, prefix + legal
        current_start = probe_trap if horizon == 1 else probe_start
        for variant, plan in (("conflict", failed), ("control", legal)):
            replay = domain.replay(current_start, plan)
            expected = horizon if variant == "conflict" else None
            assert replay["firstConflict"] == expected
            lookahead.append({
                "id": f"{config['id']}/lookahead/{horizon}/{variant}", "case": config["id"],
                "start": current_start, "goal": domain.full, "horizon": horizon, "plan": plan,
                "firstConflict": expected, "failureCode": replay["code"],
                "causalDepth": 1 if expected else 0,
                "interveningActions": "Legal goal-directed attachments; do not imply deeper causality.",
            })

    cf = config["counterfactual"]
    closure = [domain.source_to_site[i] for i in cf["closureSources"]]
    interiors = [domain.source_to_site[i] for i in cf["interiorSources"]]
    if len(closure) != 2 or len(interiors) != 2 or len(set(closure + interiors)) != 4:
        raise ValueError("Expected two distinct closures and two distinct interiors")
    if "checkpointOccupiedSources" in cf:
        sources = cf["checkpointOccupiedSources"]
        if len(sources) != len(set(sources)):
            raise ValueError("Duplicate checkpoint source")
        checkpoint = sum(1 << domain.source_to_site[i] for i in sources)
    else:
        checkpoint = 0 if cf["checkpoint"] == "empty" else domain.full ^ sum(
            1 << i for i in closure + interiors)
    if reachable[checkpoint] < 0:
        raise ValueError("Unreachable counterfactual checkpoint")
    candidates = [{"type": "attach", "site": i} for i in closure]
    afters = [domain.transition(checkpoint, "attach", i) for i in closure]
    if any(code != "OK" for _, code in afters):
        raise ValueError("Counterfactual candidates must both be locally legal")

    def member(goal, name):
        table = cost(goal)
        qs = [1 + table[after] for after, _ in afters]
        return {"id": name, "goal": goal, "conditionalCosts": qs,
                "optimalChoices": [i for i, q in enumerate(qs) if q == min(qs)]}

    a, b = [member(domain.full ^ (1 << interior), tag)
            for interior, tag in zip(interiors, ("a", "b"))]
    if len(a["optimalChoices"]) != 1 or len(b["optimalChoices"]) != 1 or a["optimalChoices"] == b["optimalChoices"]:
        raise ValueError(f"No unique counterfactual reversal: {a}, {b}")
    controls = []
    for site in range(domain.n):
        control_goal = a["goal"] & ~(1 << site)
        if site in closure + interiors or reachable[control_goal] < 0:
            continue
        proposed = member(control_goal, f"control-{len(controls)}")
        if proposed["optimalChoices"] == a["optimalChoices"]:
            controls.append(proposed)
            if len(controls) == 2:
                break
    if len(controls) != 2:
        raise ValueError("No goal-size-matched invariance controls")
    counterfactual = {
        "id": f"{config['id']}/counterfactual", "case": config["id"], "start": checkpoint,
        "candidates": candidates, "members": [a, b, *controls],
        "switchPair": ["a", "b"], "invariancePair": ["control-0", "control-1"],
        "startWitness": domain.witness(0, checkpoint, domain.distances(checkpoint)),
        "scope": "Optimal choice among the two offered closures; neither is asserted globally optimal.",
    }
    tasks = {"episodes": episodes, "choices": [choice], "lookahead": lookahead,
             "counterfactual": [counterfactual]}
    for episode in episodes:
        assert domain.replay(0, episode["startWitness"])["state"] == episode["start"]
        result = domain.replay(episode["start"], episode["completionWitness"])
        assert result["firstConflict"] is None and result["state"] == episode["goal"]
    certificate = {
        "schema": "brickplan-certificate/1.0", "case": config["id"],
        "transitionHash": domain.transition_hash, "tasksHash": canonical_hash(tasks),
        "costsHash": canonical_hash(costs), "sourceHash": canonical_hash(domain.source),
        "geometryHash": canonical_hash(domain.geometry), "goals": checks,
        "parts": len(domain.parts), "movableSites": domain.n, "fixedParts": len(domain.fixed),
        "connectorEdges": len(domain.source["edges"]), "endpointPairs": len(domain.geometry["endpoints"]),
        "motionPairs": sum(len(p["pairs"]) for p in domain.geometry["paths"]),
        "blockedMotionPairs": sum(r["status"] == "BLOCKED"
                                  for p in domain.geometry["paths"] for r in p["pairs"]),
        "unknownGeometry": 0, "provenanceGroup": config["provenanceGroup"],
        "fullOptimalActions": full_cost[0], "repairMinimumDetaches": 3,
        "mandatoryOrder": mandatory_order(domain, reachable, full_cost),
        **checks[str(domain.full)],
    }
    write_json(folder / "tasks.private.json", tasks)
    write_gzip(folder / "costs.private.json.gz", costs)
    write_json(folder / "certificate.json", certificate)
    return certificate
