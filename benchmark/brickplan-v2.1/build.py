"""Deterministic mechanism-conditioned challenge bank; no VLM results."""
from collections import Counter
from dataclasses import asdict
from itertools import combinations
import json
import random
import copy

from bank import DATA, PROFILES, domain, write_json
from mission import AssemblyDomain, Mission, State, canonical_hash
from oracle import Oracle, PhysicalGraph
from policies import astar, choice_horizon
from diagnostics import continuation_pairs, delayed_repair_probes, geometry_pairs


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
        self.continuations, self.repair_census = [], []

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
            "split": profile["split"], "tier": "D" + str(
                1 + (len(witness) > 8) + (len(witness) > 16) + (len(witness) > 24)),
            "kind": kind, "sampling": profile["sampling"],
            "descriptors": {"optimalOperations": len(witness), "registeredSites": m.domain.n,
                            "rackCapacity": m.capacity, "workOrders": len(m.jobs),
                            "initialOccupied": start.assembly.bit_count(),
                            "legacyMechanismStratum": tier},
            "start": asdict(start), "goal": m.goal, "jobs": list(m.jobs), "capacity": m.capacity,
            # Public budgets depend only on visible problem size, never answer costs.
            "maxActions": 6 * m.domain.n + 2 * len(m.jobs), "maxViews": 12, "maxDiagnoses": 12,
            "optimalCost": oracle.distance(start), "relaxedLowerBound": m.lower_bound(start),
            "relaxationGap": oracle.distance(start) - m.lower_bound(start),
            "initialOptimalActions": [a.json() for a in oracle.optimal_actions(start)],
            "oracleFile": self.certify(oracle), "witness": [a.json() for a in witness],
            "astarClosureExpansionsSeed0": strong.expansions,
            "pairId": pair_id}
        self.episodes.append(row)
        if diagnostics:
            self.make_probes(row, oracle, result["states"])
        print("TASK", task_id, row["tier"], kind, row["optimalCost"], row["relaxationGap"], strong.expansions, flush=True)
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
                # Frozen checkpoint sampling on new sources; legacy strata keep
                # their historical selection and are identified as development.
                score = ((canonical_hash({"task": task["id"], "step": step}),)
                         if task["sampling"] == "frozen-source-plan" else
                         (not horizon["8"]["allOptimal"], not horizon["4"]["allOptimal"],
                          oracle.distance(state) - oracle.mission.lower_bound(state), oracle.distance(state)))
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
        self.continuations.extend(continuation_pairs(task, oracle))
        repair, census = delayed_repair_probes(task, oracle, states)
        self.probes.extend(repair)
        self.repair_census.append(census)

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
        d, cap = AssemblyDomain.load(DATA / profile["id"]), profile["capacity"]
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

    def frozen_profile(self, profile):
        """Seeded starts/jobs fixed independently of solver performance."""
        d = AssemblyDomain.load(DATA / profile["id"])
        cap = profile["capacity"]
        graph = PhysicalGraph(d, cap, d.full)
        rng = random.Random(f'20261008/{profile["sourceGroup"]}')
        sites = [i for i in range(d.n) if any(not s & (1 << i) for s in graph.states)]
        rng.shuffle(sites)
        partial = [s for s in graph.states if s != d.full]
        goals = [d.full] + (rng.sample(partial, 1) if partial else [])
        rows = []
        for goal in goals:
            for job_count in (0, min(2, len(sites)), min(4, len(sites))):
                jobs = tuple(sorted(sites[:job_count]))
                if (goal, jobs) in rows:
                    continue
                rows.append((goal, jobs))
                oracle = Oracle(Mission(d, cap, goal, jobs), graph)
                # Reachability is the only oracle-based admission check.
                starts = [s for s in graph.states if oracle.distance(State(s)) > 0]
                for assembly in rng.sample(starts, min(2, len(starts))):
                    self.episode(profile, oracle, State(assembly), None,
                                 "inspection-and-resource" if jobs else "finite-rack-reconfiguration")
        self.tables.clear()
        d.supported.cache_clear()
        return {**profile, "registeredSites": d.n, "fixedParts": len(d.fixed),
                "sourceParts": len(d.parts), "reachableMovableSites": len(sites),
                "lockedInFullComponent": sorted(set(range(d.n)) - set(sites))}

    def finalize_continuations(self):
        # Equal conflict-position bins, without no-op padding or repeated-state
        # walks. Every valid plan is an exact witness. All candidates are saved
        # in the census before balanced selection.
        bins = {}
        for candidate in self.continuations:
            bins.setdefault(candidate["bin"], []).append(candidate)
        quota = min([24, *(len(rows) for rows in bins.values())])
        chosen = []
        for bucket, rows in sorted(bins.items()):
            rows.sort(key=lambda r: canonical_hash({"pair": r["pair"]["id"], "seed": 20261008}))
            chosen.extend(rows[:quota])
        for row in chosen:
            self.probes.extend(row["probes"])
            self.pairs.append(row["pair"])
        return {"conflictBins": {"early": [2, 5], "middle": [6, 10], "late": [11, None]},
                "candidatesByBin": {k: len(v) for k, v in bins.items()},
                "selectedPairsPerBin": quota,
                "noPadding": True, "selectionScope": "Diagnostic stratification; source episodes are unchanged."}


def main():
    builder = Builder()
    profiles = [(builder.frozen_profile(p) if p["sampling"] == "frozen-source-plan"
                 else builder.profile(p)) for p in PROFILES if p["sampling"] != "geometry-contrast"]
    extra_profiles = geometry_pairs(builder, PROFILES)
    profiles.extend(extra_profiles)
    continuation_census = builder.finalize_continuations()
    controls = [p for p in builder.probes if p["kind"] == "continuation"]
    controls.sort(key=lambda p: canonical_hash({"appearanceControl": p["id"]}))
    for probe in controls[:12]:
        pair_id = probe["id"] + "/appearance"
        members = []
        for appearance in ("original", "grayscale"):
            control = copy.deepcopy(probe)
            control.update(id=pair_id + "/" + appearance, kind="appearance-continuation",
                           pairId=pair_id, appearance=appearance)
            builder.probes.append(control)
            members.append(control["id"])
        builder.pairs.append({"id": pair_id, "kind": "appearance-invariant", "members": members,
                              "sameGeometryStatePlanAnswer": True, "transformation": "grayscale pixels only"})
    bank = {"schema": "brickplan-bank/2.1", "profiles": profiles, "episodes": builder.episodes,
            "probes": builder.probes, "pairs": builder.pairs,
            "selection": "Legacy mechanism-conditioned development; predeclared new-source seeded sampling.",
            "continuationCensus": continuation_census, "repairCensus": builder.repair_census,
            "geometryCensus": builder.geometry_census,
            "tiers": {
                "D1": "1–8 optimal operations; an operation-length bin, not cognitive depth.",
                "D2": "9–16 optimal operations.",
                "D3": "17–24 optimal operations.",
                "D4": "25+ optimal operations.",
            }}
    write_json(DATA / "tasks.private.json", bank)
    write_json(DATA / "certificate.json", {
        "schema": "brickplan-certificate/2.1", "tasksHash": canonical_hash(bank),
        "oracles": builder.certificates,
        "sources": {p["id"]: {"geometryHash": canonical_hash(d.geometry),
                               "sourceHash": canonical_hash(d.source),
                               "transitionHash": d.transition_hash}
                    for p in profiles for d in [AssemblyDomain.load(DATA / p["id"])]},
        "census": {"episodes": len(builder.episodes), "probes": len(builder.probes),
                   "pairs": len(builder.pairs), "sourceGroups": len({p["sourceGroup"] for p in profiles}),
                   "byTier": dict(Counter(x["tier"] for x in builder.episodes))}})
    print("COMPLETE", len(builder.episodes), len(builder.probes), len(builder.pairs), flush=True)


if __name__ == "__main__":
    main()
