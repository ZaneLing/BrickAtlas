"""Versioned task construction; retain source poses and re-certify new goal tables."""
import copy
import gzip
import json
import random
from pathlib import Path

from build import DATA, HERE, budget, load_bank, write_json, write_gzip
from cases import CASES
from engine import AssemblyDomain, canonical_hash, minimum_detaches, verify_distances


def balanced_plans(domain, reachable, seed):
    rng = random.Random(seed)
    output = []
    for length in (4, 6, 8):
        needed = set(range(2, length))
        for trial in range(100000):
            start = rng.choice(reachable)
            state, plan = start, []
            for _ in range(length):
                op, site, state = rng.choice(list(domain.moves(state)))
                plan.append({"type": op, "site": site})
            if len({a["type"] for a in plan}) != 2:
                continue
            i, j = sorted(rng.sample(range(1, length - 1), 2))
            changed = copy.deepcopy(plan)
            changed[i], changed[j] = changed[j], changed[i]
            replay = domain.replay(start, changed)
            conflict = replay["firstConflict"]
            if conflict not in needed or replay["code"] not in ("MOTION_BLOCKED", "UNSUPPORTED_ASSEMBLY"):
                continue
            needed.remove(conflict)
            for variant, actions, first, code in (
                    ("conflict", changed, conflict, replay["code"]),
                    ("control", plan, None, "OK")):
                output.append({
                    "start": start, "goal": domain.full, "horizon": length, "plan": actions,
                    "firstConflict": first, "failureCode": code,
                    "matchedPair": f"L{length}-K{conflict}",
                    "variant": variant,
                    "intervention": "Swap two interior actions; preserve action multiset and endpoints.",
                })
            if not needed:
                break
        if needed:
            raise ValueError(f"No certified matched plans for {length}: {needed}")
    return output


def main():
    certs = []
    for index, config in enumerate(CASES):
        case = config["id"]
        old = HERE.with_name("brickplan-v1.1") / "data" / case
        folder = DATA / case
        d = AssemblyDomain.load(folder)
        tasks = json.loads((old / "tasks.private.json").read_text())
        costs = json.loads(gzip.decompress((old / "costs.private.json.gz").read_bytes()))
        cert = json.loads((old / "certificate.json").read_text())
        reachable = [s for s, v in enumerate(costs[str(d.full)]) if v >= 0]
        tasks["lookahead"] = balanced_plans(d, reachable, 1200 + index)
        for i, probe in enumerate(tasks["lookahead"]):
            probe.update(id=f"{case}/continuation/{i:02d}", case=case)
            probe["matchedPair"] = f"{case}/{probe['matchedPair']}"
        # A separate partial-target reconfiguration protocol. This is still the
        # certified access-order mechanism, not a newly claimed support mechanism.
        candidates = []
        for goalstr, table in costs.items():
            goal = int(goalstr)
            if goal == d.full:
                continue
            for state in reachable:
                if not state & ~goal or (goal & ~state).bit_count() < 3:
                    continue
                extra = table[state] - (state ^ goal).bit_count()
                if extra < 4:
                    continue
                legal = list(d.moves(state))
                good = [m for m in legal if table[m[2]] == table[state] - 1]
                bad = [m for m in legal if table[m[2]] > table[state]
                       and (m[0] == "attach") == bool(goal & (1 << m[1]))]
                if good and bad:
                    candidates.append((extra, table[state], -state, goal, state, good, bad))
        if not candidates:
            raise ValueError(f"No partial-target access-order reconfiguration for {case}")
        _, _, _, goal, state, good, bad = max(candidates, key=lambda x: x[:3])
        table = costs[str(goal)]
        task = {
            "id": f"{case}/reconfigure", "case": case, "mode": "reconfigure",
            "start": state, "goal": goal, "optimalActions": table[state],
            "minimumDetaches": minimum_detaches(state, goal, table),
            "budget": budget(table[state]), "inspectBudget": 32, "diagnoseBudget": 8,
            "startWitness": d.witness(0, state, d.distances(state)),
            "completionWitness": d.witness(state, goal, table),
            "mechanism": "Partial-target access-order reconfiguration; support-rerouting not established.",
            "hammingLowerBound": (state ^ goal).bit_count(),
            "legalGoalDirectedTrap": {"type": bad[0][0], "site": bad[0][1]},
            "trapExtraActions": 1 + table[bad[0][2]] - table[state],
        }
        tasks["episodes"].append(task)
        for episode in tasks["episodes"]:
            for start, plan, end in ((0, episode["startWitness"], episode["start"]),
                                     (episode["start"], episode["completionWitness"], episode["goal"])):
                result = d.replay(start, plan)
                assert result["firstConflict"] is None and result["state"] == end
        cert.update(schema="brickplan-certificate/1.2", tasksHash=canonical_hash(tasks),
                    costsHash=canonical_hash(costs), revisionMechanism=task["mechanism"])
        # Verify every cost table again against all reachable edges.
        reference = costs[str(d.full)]
        cert["goals"] = {g: verify_distances(d, int(g), t, reference) for g, t in costs.items()}
        write_json(folder / "tasks.private.json", tasks)
        write_gzip(folder / "costs.private.json.gz", costs)
        write_json(folder / "certificate.json", cert)
        certs.append(cert)
        print(case, "certified", len(tasks["lookahead"]), "probes", task["optimalActions"],
              "reconfiguration actions", flush=True)
    banks = [load_bank(c["id"]) for c in CASES]
    write_json(DATA / "release.json", {
        "schema": "brickplan-release/1.2", "structures": len(certs),
        "independentProvenanceGroups": len({c["provenanceGroup"] for c in certs}),
        "episodes": sum(len(b[1]["episodes"]) for b in banks),
        "probeResponses": sum(len(b[1]["choices"]) + len(b[1]["lookahead"]) +
                              sum(len(p["members"]) for p in b[1]["counterfactual"]) for b in banks),
        "cases": certs, "modelOrHumanResults": False,
    })


if __name__ == "__main__":
    main()
