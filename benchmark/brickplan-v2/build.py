"""Deterministic mechanism-conditioned challenge bank; no VLM results."""
from collections import Counter
from dataclasses import asdict
from itertools import combinations
import json

from bank import DATA, PROFILES, domain, write_json
from mission import Mission, State, canonical_hash
from oracle import Oracle, PhysicalGraph
from policies import astar, choice_horizon


def rank_starts(oracle, flags=0):
    m = oracle.mission
    return sorted([(oracle.distance(s) - m.lower_bound(s), oracle.distance(s), s.assembly)
                   for assembly in oracle.graph.states
                   if oracle.distance(s := State(assembly, flags)) > 0], reverse=True)


def diverse(ranking, number=2):
    chosen = []
    for gap, cost, assembly in ranking:
        if not chosen or all((assembly ^ x[2]).bit_count() >= 4 for x in chosen):
            chosen.append((gap, cost, assembly))
        if len(chosen) == number:
            break
    return chosen


class Builder:
    def __init__(self):
        self.episodes, self.probes, self.pairs, self.certificates = [], [], [], {}
        self.oracle_names, self.tables = {}, {}
        self.counts = Counter()

    def certify(self, oracle):
        m = oracle.mission
        key = canonical_hash({"mission": m.transition_hash, "goal": m.goal, "graph": oracle.graph.hash})
        if key not in self.oracle_names:
            path = f"oracles/{key[:24]}.json.gz"
            (DATA / "oracles").mkdir(parents=True, exist_ok=True)
            digest = oracle.save(DATA / path)
            checks = oracle.verify()
            self.oracle_names[key] = path
            self.certificates[path] = {
                **checks, "contentHash": digest, "graphHash": oracle.graph.hash,
                "missionHash": m.transition_hash, "capacity": m.capacity,
                "jobs": list(m.jobs), "goal": m.goal}
            print("CERTIFIED", path, checks["productStates"], checks["maxRelaxationGap"], flush=True)
        return self.oracle_names[key]

    def horizon(self, oracle):
        key = (oracle.graph.hash, oracle.mission.transition_hash, oracle.mission.goal)
        if key not in self.tables:
            self.tables[key] = oracle.horizon_tables()
        return self.tables[key]

    def episode(self, profile, oracle, start, tier, kind, pair_id=None, diagnostics=True):
        m = oracle.mission
        self.counts[profile["id"]] += 1
        task_id = f'{profile["id"]}-{self.counts[profile["id"]]:02d}'
        witness = oracle.witness(start)
        result = m.replay(start, witness)
        assert result["firstConflict"] is None and result["state"] == m.terminal
        strong = astar(m, start, max_expansions=500000, seed=0)
        assert strong.solved and len(strong.plan) == oracle.distance(start)
        row = {
            "id": task_id, "profile": profile["id"], "sourceGroup": profile["sourceGroup"],
            "split": profile["split"], "tier": tier, "kind": kind,
            "start": asdict(start), "goal": m.goal, "jobs": list(m.jobs), "capacity": m.capacity,
            # Public budgets depend only on visible problem size, never answer costs.
            "maxActions": 6 * m.domain.n + 2 * len(m.jobs), "maxViews": 12, "maxDiagnoses": 12,
            "optimalCost": oracle.distance(start), "relaxedLowerBound": m.lower_bound(start),
            "relaxationGap": oracle.distance(start) - m.lower_bound(start),
            "initialOptimalActions": [a.json() for a in oracle.optimal_actions(start)],
            "oracleFile": self.certify(oracle), "witness": [a.json() for a in witness],
            "astarClosureExpansionsSeed0": strong.expansions,
            "pairId": pair_id}
        if tier == "D4":
            assert row["relaxationGap"] >= 4 and len(m.jobs) >= 2
            assert strong.expansions > 100
        if tier in ("D2", "D3"):
            assert row["relaxationGap"] >= 2 or pair_id is not None
        self.episodes.append(row)
        if diagnostics:
            self.make_probes(row, oracle, result["states"])
        print("TASK", task_id, tier, kind, row["optimalCost"], row["relaxationGap"], strong.expansions, flush=True)
        return row

    def make_probes(self, task, oracle, states):
        tables = self.horizon(oracle)
        candidates = []
        horizon_rows = []
        for step, state in enumerate(states[:-1]):
            options = list(oracle.mission.moves(state))
            horizon = choice_horizon(oracle, state, tables)
            horizon_rows.append(horizon)
            if any(oracle.distance(after) >= oracle.distance(state) for _, after in options):
                score = (not horizon["8"]["allOptimal"], not horizon["4"]["allOptimal"],
                         oracle.distance(state) - oracle.mission.lower_bound(state), oracle.distance(state))
                candidates.append((score, -step, state, horizon))
        task["witnessHorizon"] = {
            str(depth): {"decisions": len(horizon_rows),
                         "optimisticCorrect": sum(x[str(depth)]["anyOptimal"] for x in horizon_rows),
                         "pessimisticCorrect": sum(x[str(depth)]["allOptimal"] for x in horizon_rows)}
            for depth in (1, 2, 4, 8)}
        for j, (_, neg_step, state, horizon) in enumerate(sorted(candidates, reverse=True)[:2]):
            options = sorted(oracle.mission.moves(state), key=lambda item: item[0])
            labels = [{"action": a.json(), "remainingCost": oracle.distance(after),
                       "conditionalExtraCost": 1 + oracle.distance(after) - oracle.distance(state),
                       "unreachable": oracle.distance(after) < 0}
                      for a, after in options]
            self.probes.append({
                "id": f'{task["id"]}/choice-{j}', "kind": "next-action", "taskId": task["id"],
                "state": asdict(state), "witnessStep": -neg_step,
                "choices": [a.json() for a, _ in options], "labels": labels,
                "optimalChoices": [i for i, x in enumerate(labels) if x["conditionalExtraCost"] == 0],
                "horizonEvidence": horizon,
                "prompt": "Choose the next action minimizing total operations needed to finish all declared work."})
        # Matched continuation pairs have identical first and last actions and
        # the same action multiset. A changed interior order is the sole contrast.
        witness = oracle.witness(State(**task["start"]))
        for i in range(1, len(witness) - 2):
            corrupted = witness.copy()
            corrupted[i], corrupted[i + 1] = corrupted[i + 1], corrupted[i]
            check = oracle.mission.replay(State(**task["start"]), corrupted)
            if check["firstConflict"] is not None:
                pair_id = f'{task["id"]}/continuation'
                members = []
                for label, plan, conflict in (("a", witness, None), ("b", corrupted, check["firstConflict"])):
                    probe_id = pair_id + "/" + label
                    self.probes.append({
                        "id": probe_id, "kind": "continuation", "taskId": task["id"],
                        "state": task["start"], "pairId": pair_id,
                        "plan": [a.json() for a in plan], "firstConflict": conflict,
                        "prompt": "Report the first illegal operation (1-based), or null if every operation is legal."})
                    members.append(probe_id)
                self.pairs.append({"id": pair_id, "kind": "interior-order", "members": members,
                                   "sameFirstAndLast": True, "sameActionMultiset": True})
                break

    def history_pair(self, profile, oracle):
        if len(oracle.mission.jobs) != 2:
            return
        m = oracle.mission
        candidates = []
        for assembly in oracle.graph.states:
            a, b = State(assembly, 1), State(assembly, 2)
            aa, ab = set(oracle.optimal_actions(a)), set(oracle.optimal_actions(b))
            # Avoid a trivial immediate "audit the only available work order".
            if aa and ab and aa.isdisjoint(ab) and all(x.type != "audit" for x in aa | ab):
                candidates.append((min(oracle.distance(a), oracle.distance(b)),
                                   abs(oracle.distance(a) - oracle.distance(b)), assembly))
        if not candidates:
            return
        _, _, assembly = max(candidates)
        pair_id = profile["id"] + "/history"
        members = [self.episode(profile, oracle, State(assembly, flag), "D3",
                                "same-assembly-different-ledger", pair_id, diagnostics=False)
                   for flag in (1, 2)]
        self.pairs.append({
            "id": pair_id, "kind": "history", "members": [x["id"] for x in members],
            "sameAssembly": True, "disjointOptimalActions": True,
            "scope": "Explicit ledger changes future obligations; no hidden-memory claim."})

    def work_pair(self, profile, graph, job_a, job_b):
        ma = Mission(graph.domain, graph.capacity, graph.domain.full, [job_a])
        mb = Mission(graph.domain, graph.capacity, graph.domain.full, [job_b])
        a, b = Oracle(ma, graph), Oracle(mb, graph)
        candidates = []
        for assembly in graph.states:
            state = State(assembly)
            aa, ab = set(a.optimal_actions(state)), set(b.optimal_actions(state))
            if aa and ab and aa.isdisjoint(ab) and all(x.type != "audit" for x in aa | ab):
                candidates.append((min(a.distance(state), b.distance(state)), assembly))
        if not candidates:
            return
        _, assembly = max(candidates)
        pair_id = profile["id"] + "/work-order"
        members = [self.episode(profile, o, State(assembly), "D3",
                                "changed-future-work", pair_id, diagnostics=False) for o in (a, b)]
        self.pairs.append({
            "id": pair_id, "kind": "counterfactual-work", "members": [x["id"] for x in members],
            "sameAssembly": True, "samePhysicalGoal": True, "disjointOptimalActions": True})

    def profile(self, profile):
        d, cap = domain(profile["id"]), profile["capacity"]
        finite = PhysicalGraph(d, cap, d.full)
        unlimited = PhysicalGraph(d, d.n, d.full)
        reachable_sites = [i for i in range(d.n) if any(not s & (1 << i) for s in unlimited.states)]
        exposed = [i for i in range(d.n) if any(not s & (1 << i) for s in finite.states)]
        exposed.sort(key=lambda i: (-Mission(d, d.n, d.full, [i]).removal_closure(State(d.full)).bit_count(), i))
        profile = {**profile, "registeredSites": d.n, "reachableMovableSites": len(reachable_sites),
                   "fixedParts": len(d.fixed), "sourceParts": len(d.parts),
                   "lockedInFullComponent": sorted(set(range(d.n)) - set(reachable_sites))}
        control = Oracle(Mission(d, d.n, d.full), unlimited)
        fewest = min(unlimited.states, key=lambda s: (s.bit_count(), s))
        self.episode(profile, control, State(fewest), "D1", "unlimited-rack-control")
        alternative = next(x for x in rank_starts(control)
                           if x[2] != fewest and x[0] == 0)
        self.episode(profile, control, State(alternative[2]), "D1", "unlimited-rework-control")
        goals = [d.full] + [d.full ^ (1 << i) for i in exposed[:4]
                           if d.full ^ (1 << i) in finite.index]
        resources = []
        for goal in goals:
            oracle = Oracle(Mission(d, cap, goal), finite)
            ranking = rank_starts(oracle)
            resources.append((ranking[0][:2], goal, oracle, ranking))
        selected = [x for x in resources if x[1] == d.full]
        other = [x for x in resources if x[1] != d.full]
        if other:
            selected.append(max(other, key=lambda x: (x[0], -x[1])))
        for _, _, oracle, ranking in selected:
            if ranking[0][0] >= 2:
                for gap, _, assembly in diverse([x for x in ranking if x[0] >= 2]):
                    self.episode(profile, oracle, State(assembly), "D2", "finite-rack-reconfiguration")
        services = []
        for pair in combinations(exposed[:4], 2):
            oracle = Oracle(Mission(d, cap, d.full, pair), finite)
            ranking = rank_starts(oracle)
            if ranking:
                services.append((ranking[0][:2], pair, oracle, ranking))
        _, jobs, service, ranking = max(services, key=lambda x: (x[0], tuple(-i for i in x[1])))
        if ranking[0][0] >= 2:
            for _, _, assembly in diverse([x for x in ranking if x[0] >= 2]):
                self.episode(profile, service, State(assembly), "D3", "inspection-and-resource")
            self.history_pair(profile, service)
            self.work_pair(profile, finite, *jobs)
        else:
            self.episode(profile, service, State(ranking[0][2]), "D1", "easy-inspection-control")
        complex_oracle = Oracle(Mission(d, cap, d.full, exposed[:4]), finite)
        ranking = rank_starts(complex_oracle)
        for gap, _, assembly in diverse([x for x in ranking if x[0] >= 2]):
            evidence = astar(complex_oracle.mission, State(assembly), max_expansions=101)
            tier = "D4" if gap >= 4 and not evidence.solved else "D3"
            self.episode(profile, complex_oracle, State(assembly), tier, "multi-inspection-scheduling")
        self.tables.clear()
        d.supported.cache_clear()
        control.mission.lower_bound.cache_clear()
        return profile


def main():
    builder = Builder()
    profiles = [builder.profile(p) for p in PROFILES]
    bank = {"schema": "brickplan-bank/2.0", "profiles": profiles, "episodes": builder.episodes,
            "probes": builder.probes, "pairs": builder.pairs,
            "selection": "Mechanism-conditioned challenge instances; not an unbiased population sample.",
            "tiers": {
                "D1": "Control: unlimited rack or a measured easy inspection mission.",
                "D2": "Capacity-constrained reconfiguration; exact relaxation gap >= 2.",
                "D3": "Inspection/resource mission or a certified history/work-order contrast.",
                "D4": "Multi-inspection: gap >= 4 and closure A* seed 0 needs >100 expansions.",
            }}
    write_json(DATA / "tasks.private.json", bank)
    write_json(DATA / "certificate.json", {
        "schema": "brickplan-certificate/2.0", "tasksHash": canonical_hash(bank),
        "oracles": builder.certificates,
        "sources": {p["id"]: {"geometryHash": canonical_hash(domain(p["id"]).geometry),
                               "sourceHash": canonical_hash(domain(p["id"]).source),
                               "transitionHash": domain(p["id"]).transition_hash} for p in PROFILES},
        "census": {"episodes": len(builder.episodes), "probes": len(builder.probes),
                   "pairs": len(builder.pairs), "sourceGroups": len({p["sourceGroup"] for p in profiles}),
                   "byTier": dict(Counter(x["tier"] for x in builder.episodes))}})
    print("COMPLETE", len(builder.episodes), len(builder.probes), len(builder.pairs), flush=True)


if __name__ == "__main__":
    main()
