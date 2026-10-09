"""Independent discrete audit: no imports from BrickPlan runtime/oracle modules.

Geometry is an input contract, not independently measured by this script.
All output is confined to this review directory.
"""
from array import array
from collections import Counter, defaultdict, deque
from functools import lru_cache
import csv
import gzip
import hashlib
import json
from pathlib import Path
import random
import time

OUT = Path(__file__).resolve().parent
ROOT = OUT.parents[2]
RELEASE = ROOT / "benchmark/brickplan-v2.1"
DATA = RELEASE / "data"


def digest(v):
    return hashlib.sha256(json.dumps(v, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def dump(name, value):
    (OUT / name).write_text(json.dumps(value, indent=2) + "\n")


def state(v):
    return v["assembly"], v["done"]


def action(v):
    return v["type"], v["site"]


class Rules:
    def __init__(self, profile):
        self.geo = json.loads((DATA / profile / "geometry.json").read_text())
        self.src = json.loads((DATA / profile / "source.json").read_text())
        self.mutable = self.geo["mutable"]
        self.n = len(self.mutable)
        local = {v: i for i, v in enumerate(self.mutable)}
        self.fixed = set(range(len(self.geo["parts"]))) - set(local)
        # Undirected stud edges, independently translated into site adjacency.
        adj = defaultdict(set)
        for e in self.src["edges"]:
            assert e["family"] == "stud"
            adj[e["a"]].add(e["b"])
            adj[e["b"]].add(e["a"])
        self.neighbor = [sum(1 << local[j] for j in adj[i] if j in local) for i in self.mutable]
        self.anchor = sum(1 << local[i] for i in self.mutable if adj[i] & self.fixed)
        reached, todo = set(), [min(self.fixed)]
        while todo:
            i = todo.pop()
            if i not in reached:
                reached.add(i)
                todo.extend((adj[i] & self.fixed) - reached)
        assert reached == self.fixed
        self.blocked = [0] * self.n
        for p in self.geo["paths"]:
            for pair in p["pairs"]:
                assert pair["status"] in ("CLEAR", "BLOCKED")
                if pair["status"] == "BLOCKED":
                    assert pair["obstacle"] in local
                    self.blocked[local[p["moving"]]] |= 1 << local[pair["obstacle"]]

    @lru_cache(maxsize=None)
    def connected(self, a):
        reached = a & self.anchor
        previous = -1
        while reached != previous:
            previous = reached
            for i in range(self.n):
                if reached & (1 << i):
                    reached |= self.neighbor[i] & a
        return reached == a

    def physical(self, a, cap):
        for i in range(self.n):
            b = a ^ (1 << i)
            if (not a & self.blocked[i] and self.n - b.bit_count() <= cap
                    and self.connected(b)):
                yield ("detach" if a & (1 << i) else "attach", i), b


class Model:
    def __init__(self, rules, task, physical=None):
        self.r, self.cap, self.goal, self.jobs = rules, task["capacity"], task["goal"], task["jobs"]
        self.width = 1 << len(self.jobs)
        self.jobbit = {i: 1 << j for j, i in enumerate(self.jobs)}
        if physical is None:
            seen, todo = {self.goal}, deque([self.goal])
            raw_edges = {}
            while todo:
                a = todo.popleft()
                row = list(rules.physical(a, self.cap))
                raw_edges[a] = row
                for _, b in row:
                    if b not in seen:
                        seen.add(b)
                        todo.append(b)
            self.states = sorted(seen)
            self.index = {s: i for i, s in enumerate(self.states)}
            self.edges = [[(op, self.index[b]) for op, b in raw_edges[a]] for a in self.states]
        else:
            self.states, self.index, self.edges = physical
        self.target = self.index[self.goal] * self.width + self.width - 1
        self.costs = self.reverse_distances([self.target])

    def encode(self, x):
        return self.index[x[0]] * self.width + x[1]

    def decode(self, node):
        i, f = divmod(node, self.width)
        return self.states[i], f

    def next(self, node):
        i, f = divmod(node, self.width)
        for act, b in self.edges[i]:
            yield act, b * self.width + f
        for s, bit in self.jobbit.items():
            if not f & bit and not self.states[i] & (1 << s):
                yield ("audit", s), i * self.width + (f | bit)

    def reverse_distances(self, targets, forbidden=None):
        dist = array("i", [-1]) * (len(self.states) * self.width)
        q = deque()
        for node in targets:
            dist[node] = 0
            q.append(node)
        while q:
            node = q.popleft()
            i, f = divmod(node, self.width)
            predecessors = [b * self.width + f for _, b in self.edges[i]]
            predecessors.extend(i * self.width + (f ^ bit) for s, bit in self.jobbit.items()
                                if f & bit and not self.states[i] & (1 << s))
            for before in predecessors:
                if before != forbidden and dist[before] < 0:
                    dist[before] = dist[node] + 1
                    q.append(before)
        return dist

    def step(self, x, act, geometry=True):
        a, f = x
        op, s = act
        bit = 1 << s
        if op == "audit":
            code = ("NO_WORK_ORDER" if s not in self.jobbit else
                    "ALREADY_AUDITED" if f & self.jobbit[s] else
                    "AUDIT_REQUIRES_RACK" if a & bit else "OK")
            return ((a, f | self.jobbit[s]) if code == "OK" else x), code
        if (op == "attach") == bool(a & bit):
            return x, "SITE_OCCUPIED" if op == "attach" else "SITE_EMPTY"
        if geometry and a & self.r.blocked[s]:
            return x, "MOTION_BLOCKED"
        b = a ^ bit
        if geometry and not self.r.connected(b):
            return x, "UNSUPPORTED_ASSEMBLY"
        if self.r.n - b.bit_count() > self.cap:
            return x, "RACK_FULL"
        return (b, f), "OK"

    def replay(self, x, plan, geometry=True):
        history = [x]
        for i, a in enumerate(plan, 1):
            x, code = self.step(x, action(a), geometry)
            history.append(x)
            if code != "OK":
                return i, code, history
        return None, "OK", history

    def bound(self, x):
        a, f = x
        pending = [s for s, bit in self.jobbit.items() if not f & bit]
        remove = a & ~self.goal
        for s in pending:
            remove |= a & (1 << s)
        for s in range(self.r.n):
            if self.goal & ~a & (1 << s):
                remove |= a & self.r.blocked[s]
        prev = -1
        while remove != prev:
            prev = remove
            for s in range(self.r.n):
                if remove & (1 << s):
                    remove |= a & self.r.blocked[s]
        return (a ^ self.goal).bit_count() + 2 * (remove & self.goal).bit_count() + len(pending)

    def corridor(self, node):
        found, todo = {node}, [node]
        while todo:
            u = todo.pop()
            for _, v in self.next(u):
                if self.costs[v] == self.costs[u] - 1 and v not in found:
                    found.add(v)
                    todo.append(v)
        found.discard(self.target)
        return found


def text_plan_control(public):
    """Public plan/ledger/holder-count only; unknown initial per-piece occupancy.

    First use of each piece is assumed consistent; later self-contradictions
    and holder overflows are detected. No images, source ID, or private states.
    """
    obs = public["observation"]
    holders, cap = obs["rack"]["occupiedHolders"], obs["rack"]["capacity"]
    occupied = {}
    jobs = {j["partId"]: j["completed"] for j in obs["workOrders"]}
    for i, act in enumerate(public["proposedPlan"], 1):
        op, part = act["type"], act["partId"]
        if op == "audit":
            if part not in jobs or jobs[part] or occupied.get(part, False):
                return i
            occupied[part] = False
            jobs[part] = True
        elif op == "detach":
            if occupied.get(part, True) is False or holders == cap:
                return i
            occupied[part] = False
            holders += 1
        else:
            if occupied.get(part, False) is True or holders == 0:
                return i
            occupied[part] = True
            holders -= 1
    return None


def main():
    bank = json.loads((DATA / "tasks.private.json").read_text())
    tasks = {t["id"]: t for t in bank["episodes"]}
    public = {r["stableId"]: r for r in map(json.loads, (RELEASE / "release/questions.jsonl").read_text().splitlines())}
    probes = defaultdict(list)
    for p in bank["probes"]:
        probes[p["taskId"]].append(p)
    all_rows, table_checks = [], []
    rule_cache, physical_cache = {}, {}
    grouped = defaultdict(list)
    for t in tasks.values():
        grouped[t["oracleFile"]].append(t)
    for table_name, group in grouped.items():
        t = group[0]
        if t["profile"] not in rule_cache:
            rule_cache[t["profile"]] = Rules(t["profile"])
        rules = rule_cache[t["profile"]]
        physical_key = t["profile"], t["capacity"]
        model = Model(rules, t, physical_cache.get(physical_key))
        physical_cache[physical_key] = model.states, model.index, model.edges
        saved = json.loads(gzip.decompress((DATA / table_name).read_bytes()))
        mismatch = [i for i, (a, b) in enumerate(zip(model.costs, saved["costs"])) if a != b]
        table_checks.append({"oracleFile": table_name, "states": len(model.costs),
                             "lengthMatches": len(model.costs) == len(saved["costs"]),
                             "costMismatches": len(mismatch), "examples": mismatch[:10],
                             "freshCostsHash": hashlib.sha256(model.costs.tobytes()).hexdigest()})
        print("TABLE", table_name, len(model.costs), "mismatches", len(mismatch), flush=True)
        for t in group:
            base = {"stableId": t["id"], "publicId": public[t["id"]]["id"], "form": "episode",
                    "source": t["sourceGroup"], "profile": t["profile"], "kind": t["kind"],
                    "split": t["split"], "tier": t["tier"]}
            x = state(t["start"])
            node = model.encode(x)
            conflict, code, history = model.replay(x, t["witness"])
            best = sorted(act for act, n in model.next(node) if model.costs[n] + 1 == model.costs[node])
            checks = {"supportedStart": rules.connected(x[0]),
                      "capacityValid": rules.n - x[0].bit_count() <= model.cap,
                      "optimalCost": t["optimalCost"] == model.costs[node],
                      "witnessLegal": conflict is None,
                      "witnessTerminal": history[-1] == (t["goal"], model.width - 1),
                      "witnessLength": len(t["witness"]) == model.costs[node],
                      "initialActions": best == sorted(map(action, t["initialOptimalActions"])),
                      "lowerBound": t["relaxedLowerBound"] == model.bound(x),
                      "budgetFeasible": t["maxActions"] >= model.costs[node],
                      "tier": t["tier"] == "D" + str(1 + (model.costs[node] > 8)
                                                       + (model.costs[node] > 16) + (model.costs[node] > 24))}
            base.update(checks=checks, passed=all(checks.values()), exactCost=model.costs[node],
                        lowerBound=model.bound(x), stateSequence=history)
            all_rows.append(base)
            for p in probes[t["id"]]:
                row = {**base, "stableId": p["id"], "publicId": public[p["id"]]["id"],
                       "form": "probe", "kind": p["kind"]}
                row.pop("stateSequence")
                px = state(p["state"])
                pn = model.encode(px)
                row.update(exactCost=model.costs[pn], lowerBound=model.bound(px))
                checks = {"supportedCheckpoint": rules.connected(px[0]),
                          "capacityValid": rules.n - px[0].bit_count() <= model.cap}
                if "plan" in p:
                    conflict, code, hist = model.replay(px, p["plan"])
                    relax_conflict, _, _ = model.replay(px, p["plan"], False)
                    text_pred = text_plan_control(json.loads(public[p["id"]]["publicInputJSON"]))
                    checks["firstConflict"] = conflict == p["firstConflict"]
                    row.update(answer=conflict, conflictCode=code, planLength=len(p["plan"]),
                               geometryFreeKnownOccupancyAnswer=relax_conflict,
                               geometryFreeKnownOccupancyCorrect=relax_conflict == conflict,
                               textOnlyAnswer=text_pred, textOnlyCorrect=text_pred == conflict)
                else:
                    options = [action(a) for a in p["choices"]]
                    actual = {a: n for a, n in model.next(pn)}
                    checks["allCandidatesLegal"] = all(a in actual for a in options)
                    checks["candidatesCompleteUnique"] = len(options) == len(set(options)) == len(actual)
                    costs = model.costs
                    if p["kind"] == "delayed-repair":
                        checkpoint = state(p["checkpoint"])
                        cn = model.encode(checkpoint)
                        conflict, _, hist = model.replay(checkpoint, p["history"])
                        corridor = model.corridor(cn)
                        costs = model.reverse_distances(corridor, forbidden=model.target)
                        checks.update(historyLegal=conflict is None, historyEndsAtCheckpoint=hist[-1] == px,
                                      lagLength=len(p["history"]) == p["lagAfterError"] + 1,
                                      distinctHistory=len(set(hist)) == len(hist),
                                      firstActionCostly=1 + model.costs[model.encode(hist[1])] > model.costs[cn],
                                      outsideCorridor=all(model.encode(h) not in corridor for h in hist[1:]),
                                      repairCost=costs[pn] == p["minimumRepairCost"],
                                      checkpointCost=model.costs[cn] == p["checkpointRemainingOptimal"])
                        row.update(repairCost=costs[pn], lag=p["lagAfterError"])
                    remaining = [costs[actual[a]] for a in options]
                    optimum = [i for i, c in enumerate(remaining) if c >= 0 and c + 1 == costs[pn]]
                    checks["optimalChoices"] = optimum == p["optimalChoices"]
                    field = "remainingRepairCost" if p["kind"] == "delayed-repair" else "remainingCost"
                    checks["allCandidateCosts"] = remaining == [v[field] for v in p["labels"]]
                    checks["labelActionAlignment"] = options == [action(v["action"]) for v in p["labels"]]
                    checks["conditionalExtraCosts"] = [
                        (1 + c - costs[pn]) if c >= 0 else None for c in remaining
                    ] == [v["conditionalExtraCost"] for v in p["labels"]]
                    # Candidate order in the public seed-0 presentation.
                    order = list(range(len(options)))
                    random.Random(f"0/{p['id']}").shuffle(order)
                    row.update(answerPrivate=optimum, answerPublic=sorted(order.index(i) for i in optimum),
                               candidateCosts=remaining, candidates=len(options), correctCandidates=len(optimum),
                               randomAccuracy=len(optimum) / len(options), allOptionsCorrect=len(optimum) == len(options))
                    if p["kind"] == "next-action":
                        values = [model.bound(model.decode(actual[a])) for a in options]
                        chosen = [i for i, v in enumerate(values) if v == min(values)]
                        checks["depthOneEvidence"] = (
                            bool(set(chosen) & set(optimum)) == p["horizonEvidence"]["1"]["anyOptimal"]
                            and abs(len(set(chosen) & set(optimum)) / len(chosen)
                                    - p["horizonEvidence"]["1"]["optimalFractionUnderUniformTies"]) < 1e-12)
                        audits = [i for i, a in enumerate(options) if a[0] == "audit"]
                        row.update(depthOneAnyOptimal=bool(set(chosen) & set(optimum)),
                                   depthOneUniformAccuracy=len(set(chosen) & set(optimum)) / len(chosen),
                                   auditChoiceAvailable=bool(audits),
                                   auditChoiceAllOptimal=bool(audits) and set(audits) <= set(optimum))
                    else:
                        last = action(p["history"][-1])
                        inverse = ({"attach": "detach", "detach": "attach"}.get(last[0], "unaudit"), last[1])
                        row.update(inverseLastLegal=inverse in options,
                                   inverseLastCorrect=inverse in options and options.index(inverse) in optimum)
                row.update(checks=checks, passed=all(checks.values()))
                all_rows.append(row)
        # Keep process memory bounded while preserving reusable physical graphs.
        if len(physical_cache) > 10:
            physical_cache.pop(next(iter(physical_cache)))
    assert len(all_rows) == 884
    idrows = {r["stableId"]: r for r in all_rows}
    pair_checks = []
    pmap = {p["id"]: p for p in bank["probes"]}
    for pair in bank["pairs"]:
        a, b = [idrows[i] for i in pair["members"]]
        checks = {"bothMembersPass": a["passed"] and b["passed"]}
        if pair["kind"] == "interior-order":
            pa, pb = [pmap[i] for i in pair["members"]]
            prefix = pair["sharedLegalPrefix"]
            checks.update(sameState=pa["state"] == pb["state"],
                          sameMultiset=Counter(map(action, pa["plan"])) == Counter(map(action, pb["plan"])),
                          sameFirstLast=(pa["plan"][0], pa["plan"][-1]) == (pb["plan"][0], pb["plan"][-1]),
                          matchedPrefix=pa["plan"][:prefix] == pb["plan"][:prefix],
                          answerChanges=(a["answer"] is None) != (b["answer"] is None))
        elif pair["kind"] in ("visual-geometry", "appearance-invariant"):
            pa, pb = [pmap[i] for i in pair["members"]]
            checks.update(samePlan=pa["plan"] == pb["plan"], sameState=pa["state"] == pb["state"],
                          answerRelation=(a["answer"] != b["answer"]) == (pair["kind"] == "visual-geometry"))
        else:
            ta, tb = [tasks[i] for i in pair["members"]]
            checks.update(sameAssembly=ta["start"]["assembly"] == tb["start"]["assembly"],
                          disjointOptimalActions=not set(map(action, ta["initialOptimalActions"]))
                          & set(map(action, tb["initialOptimalActions"])))
        pair_checks.append({"id": pair["id"], "kind": pair["kind"], "checks": checks,
                            "passed": all(checks.values())})
    duplicates = defaultdict(list)
    episode_sigs, unique_context = defaultdict(list), defaultdict(list)
    for r in all_rows:
        item = tasks[r["stableId"]] if r["form"] == "episode" else pmap[r["stableId"]]
        t = item if r["form"] == "episode" else tasks[item["taskId"]]
        sig = [t["profile"], t["capacity"], t["goal"], t["jobs"], item.get("state", t["start"])]
        unique_context[digest([t["profile"], item.get("state", t["start"])["assembly"], t["goal"]])].append(r["publicId"])
        if r["form"] == "episode":
            episode_sigs[digest(sig)].append(r["publicId"])
        else:
            sig += [item["kind"].replace("appearance-continuation", "continuation"),
                    item.get("plan"), item.get("choices"), item.get("checkpoint"),
                    item.get("history"), item.get("appearance", "original")]
        duplicates[digest(sig)].append(r["publicId"])
    stats = {"bankHash": digest(bank), "rows": len(all_rows),
             "passed": sum(r["passed"] for r in all_rows),
             "failures": [r for r in all_rows if not r["passed"]],
             "tableCount": len(table_checks), "tableStates": sum(r["states"] for r in table_checks),
             "tableMismatches": sum(r["costMismatches"] for r in table_checks),
             "pairCount": len(pair_checks), "pairFailures": [r for r in pair_checks if not r["passed"]],
             "sourceRows": dict(Counter(r["source"] for r in all_rows)),
             "sourceEpisodes": dict(Counter(t["sourceGroup"] for t in tasks.values())),
             "activeProfiles": len({t["profile"] for t in tasks.values()}),
             "uniqueEpisodeSpecifications": len(episode_sigs),
             "uniqueProfileOccupancyGoalContexts": len(unique_context),
             "duplicateGroups": [ids for ids in duplicates.values() if len(ids) > 1],
             "duplicateExcess": sum(len(ids) - 1 for ids in duplicates.values())}
    for kind in sorted({r["kind"] for r in all_rows if r["form"] == "probe"}):
        rows = [r for r in all_rows if r["kind"] == kind]
        s = {"rows": len(rows), "sourceGroups": sorted({r["source"] for r in rows})}
        if "answer" in rows[0]:
            s.update(conflictCodes=dict(Counter(r["conflictCode"] for r in rows)),
                     textOnlyCorrect=sum(r["textOnlyCorrect"] for r in rows),
                     geometryFreeKnownOccupancyCorrect=sum(r["geometryFreeKnownOccupancyCorrect"] for r in rows))
        else:
            s.update(allOptionsCorrect=sum(r["allOptionsCorrect"] for r in rows),
                     meanRandomAccuracy=sum(r["randomAccuracy"] for r in rows) / len(rows),
                     candidateCountHistogram=dict(Counter(r["candidates"] for r in rows)))
            if kind == "next-action":
                s.update(depthOneAnyOptimal=sum(r["depthOneAnyOptimal"] for r in rows),
                         depthOneUniformAccuracy=sum(r["depthOneUniformAccuracy"] for r in rows) / len(rows),
                         auditChoiceAvailable=sum(r["auditChoiceAvailable"] for r in rows),
                         auditChoiceAllOptimal=sum(r["auditChoiceAllOptimal"] for r in rows))
            else:
                s.update(inverseLastLegal=sum(r["inverseLastLegal"] for r in rows),
                         inverseLastCorrect=sum(r["inverseLastCorrect"] for r in rows),
                         repairCosts=dict(Counter(r["repairCost"] for r in rows)))
        stats[kind] = s
    dump("instance-audit.json", all_rows)
    dump("oracle-audit.json", table_checks)
    dump("pair-audit.json", pair_checks)
    dump("audit-summary.json", stats)
    fields = ["publicId", "stableId", "form", "kind", "source", "profile", "split", "tier",
              "passed", "answer", "answerPublic", "exactCost", "repairCost", "candidates",
              "correctCandidates", "allOptionsCorrect", "textOnlyCorrect",
              "geometryFreeKnownOccupancyCorrect", "inverseLastCorrect", "checks"]
    with (OUT / "instance-audit.csv").open("w") as f:
        writer = csv.DictWriter(f, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        for row in sorted(all_rows, key=lambda r: r["publicId"]):
            writer.writerow({**row, "checks": json.dumps(row["checks"], sort_keys=True)})
    print(json.dumps(stats, indent=2), flush=True)


if __name__ == "__main__":
    main()
