"""Reproducible, fail-closed release construction. Private answers are never served."""
from __future__ import annotations

import argparse
from collections import deque
import gzip
import json
from pathlib import Path

from cases import CASES
from engine import AssemblyDomain, canonical_hash, minimum_detaches, no_undo, verify_distances

HERE = Path(__file__).resolve().parent
DATA = HERE / "data"


def write_json(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n")


def write_gzip(path, value):
    path.write_bytes(gzip.compress(json.dumps(value, sort_keys=True, separators=(",", ":")).encode(),
                                   mtime=0))


def budget(cost):
    return cost + max(4, (cost + 1) // 2)


def find_checkpoint(domain, distances, reachable, minimum_actions=3):
    for state in sorted((s for s, d in enumerate(reachable) if d >= 0),
                        key=lambda s: (reachable[s], s)):
        if reachable[state] < minimum_actions or not no_undo(state, domain.full, distances):
            continue
        good, bad = [], []
        for op, site, after in domain.moves(state):
            if op == "attach":
                (good if no_undo(after, domain.full, distances) else bad).append(site)
        if good and bad:
            return state, good, bad
    raise ValueError("No certified locally legal dead-end choice")


def mandatory_order(domain, reachable, remaining):
    """Exact pairwise precedence shared by ALL detach-free complete trajectories."""
    before = [domain.full ^ (1 << i) for i in range(domain.n)]
    prefixes = 0
    for state, distance in enumerate(reachable):
        if distance != state.bit_count() or not no_undo(state, domain.full, remaining):
            continue
        prefixes += 1
        for site in range(domain.n):
            if state & (1 << site):
                before[site] &= state ^ (1 << site)
    chains = {}
    def chain(site, seen=()):
        if site in seen:
            raise ValueError("Cyclic supposedly mandatory order")
        if site not in chains:
            parents = [chain(i, (*seen, site)) for i in range(domain.n) if before[site] & (1 << i)]
            chains[site] = max(parents, key=len, default=[]) + [site]
        return chains[site]
    longest = max((chain(i) for i in range(domain.n)), key=len)
    return {"noUndoPrefixStates": prefixes,
            "mandatoryPairs": [[i, j] for j in range(domain.n) for i in range(domain.n)
                               if before[j] & (1 << i)],
            "longestMandatoryChainSites": longest, "chainLengthParts": len(longest),
            "dependencyDepthEdges": len(longest) - 1,
            "scope": "All completions from empty movable sites without any detach, fixed goal."}


def continuations(domain, start, horizon):
    """Matched plans: same state/prefix; terminal geometric failure vs legal attach."""
    queue = deque([(start, [])])
    seen = {start}
    while queue:
        state, prefix = queue.popleft()
        if len(prefix) == horizon - 1:
            blocked = [i for i in range(domain.n)
                       if not state & (1 << i)
                       and domain.transition(state, "attach", i)[1] == "MOTION_BLOCKED"]
            legal = [site for op, site, _ in domain.moves(state) if op == "attach"]
            if blocked and legal:
                return (prefix + [{"type": "attach", "site": blocked[0]}],
                        prefix + [{"type": "attach", "site": legal[0]}])
            continue
        for op, site, after in domain.moves(state):
            if op == "attach" and after not in seen:
                seen.add(after)
                queue.append((after, prefix + [{"type": op, "site": site}]))
    raise ValueError(f"No matched continuation at horizon {horizon}")


def build_case(config, rebuild_geometry=False):
    folder = DATA / config["id"]
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
    trap, code = domain.transition(start, "attach", bad[0])
    assert code == "OK" and no_undo(trap, domain.full, full_cost) is False
    repairs = [s for s, d in enumerate(reachable) if d >= 0
               and minimum_detaches(s, domain.full, full_cost) == 3]
    if not repairs:
        raise ValueError("No nontrivial repair requiring three detach operations")
    repair = max(repairs, key=lambda s: (s.bit_count(), -reachable[s], -s))
    healthy = next((s for s, d in enumerate(reachable)
                    if d >= 0 and s.bit_count() == repair.bit_count()
                    and no_undo(s, domain.full, full_cost)), None)
    if healthy is None:
        raise ValueError("No size-matched healthy diagnosis control")

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
        "candidates": [{"type": "attach", "site": i} for i in sorted(good + bad)],
    }
    choice["labels"] = []
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
                "id": f"{config['id']}/lookahead/{horizon}/{variant}",
                "case": config["id"], "start": current_start, "goal": domain.full,
                "horizon": horizon, "plan": plan, "firstConflict": expected,
                "failureCode": replay["code"],
                "causalDepth": 1 if expected else 0,
                "interveningActions": "Legal goal-directed attachments; do not imply deeper causality.",
            })

    cf = config["counterfactual"]
    closure = [domain.source_to_site[i] for i in cf["closureSources"]]
    interiors = [domain.source_to_site[i] for i in cf["interiorSources"]]
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
        raise ValueError("Counterfactual pair does not uniquely reverse the best candidate")
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
        raise ValueError("No goal-size-matched invariance control")
    counterfactual = {
        "id": f"{config['id']}/counterfactual", "case": config["id"], "start": checkpoint,
        "candidates": candidates, "members": [a, b, *controls],
        "switchPair": ["a", "b"], "invariancePair": ["control-0", "control-1"],
        "startWitness": domain.witness(0, checkpoint, domain.distances(checkpoint)),
        "scope": "Optimal choice among the two offered closures; neither is asserted globally optimal.",
    }
    tasks = {"episodes": episodes, "choices": [choice], "lookahead": lookahead,
             "counterfactual": [counterfactual]}
    # Every source/start and goal must belong to the complete certified component.
    for episode in episodes:
        assert domain.replay(0, episode["startWitness"])["state"] == episode["start"]
        result = domain.replay(episode["start"], episode["completionWitness"])
        assert result["firstConflict"] is None and result["state"] == episode["goal"]
    certificate = {
        "schema": "brickplan-certificate/1.0", "case": config["id"],
        "transitionHash": domain.transition_hash, "tasksHash": canonical_hash(tasks),
        "costsHash": canonical_hash(costs), "sourceHash": canonical_hash(domain.source),
        "geometryHash": canonical_hash(domain.geometry), "goals": checks,
        "parts": len(domain.parts), "movableSites": domain.n,
        "fixedParts": len(domain.fixed), "connectorEdges": len(domain.source["edges"]),
        "endpointPairs": len(domain.geometry["endpoints"]),
        "motionPairs": sum(len(p["pairs"]) for p in domain.geometry["paths"]),
        "blockedMotionPairs": sum(r["status"] == "BLOCKED"
                                  for p in domain.geometry["paths"] for r in p["pairs"]),
        "unknownGeometry": 0, "provenanceGroup": "LEGO-31027",
        "fullOptimalActions": full_cost[0], "repairMinimumDetaches": 3,
        "mandatoryOrder": mandatory_order(domain, reachable, full_cost),
        **checks[str(domain.full)],
    }
    write_json(folder / "tasks.private.json", tasks)
    write_gzip(folder / "costs.private.json.gz", costs)
    write_json(folder / "certificate.json", certificate)
    return certificate


def load_bank(case_id, verify=True):
    folder = DATA / case_id
    domain = AssemblyDomain.load(folder)
    tasks = json.loads((folder / "tasks.private.json").read_text())
    costs = json.loads(gzip.decompress((folder / "costs.private.json.gz").read_bytes()))
    cert = json.loads((folder / "certificate.json").read_text())
    if verify and (cert["transitionHash"] != domain.transition_hash
                   or cert["tasksHash"] != canonical_hash(tasks)
                   or cert["costsHash"] != canonical_hash(costs)
                   or cert["sourceHash"] != canonical_hash(domain.source)):
        raise ValueError("Release certificate mismatch; rebuild or restore the frozen release")
    return domain, tasks, costs, cert


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--geometry", action="store_true", help="Re-run original mesh/path qualification")
    parser.add_argument("--case", choices=[c["id"] for c in CASES])
    args = parser.parse_args()
    reports = [build_case(c, args.geometry) for c in CASES if not args.case or c["id"] == args.case]
    if not args.case:
        write_json(DATA / "release.json", {"schema": "brickplan-release/1.0",
                   "independentProvenanceGroups": 1, "structures": 2, "cases": reports,
                   "modelOrHumanResults": False})


if __name__ == "__main__":
    main()
