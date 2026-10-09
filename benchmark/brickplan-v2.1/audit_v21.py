"""Release assertions for shortcut controls, visual pairs and delayed repair."""
from collections import Counter, deque
from dataclasses import asdict
import json

from bank import DATA, domain, load_oracle, make_mission, task_bank, task_by_id, write_json
from metrics import optimal_corridor
from mission import Action, State


def forward_repair(oracle, state, corridor):
    """Independent forward BFS; the goal is never accepted or traversed."""
    queue = deque([(state, 0)])
    seen = {state}
    while queue:
        current, distance = queue.popleft()
        if oracle.encode(current) in corridor:
            return distance
        for _, after in oracle.mission.moves(current):
            if after not in seen and after != oracle.mission.terminal:
                seen.add(after)
                queue.append((after, distance + 1))
    return -1


def main():
    bank = task_bank()
    probes = {p["id"]: p for p in bank["probes"]}
    continuations = [p for p in probes.values() if p["kind"] == "continuation"]
    prefix_scores = {}
    for depth in (0, 1, 2, 3, 5, 8, 11, 16, 24, 32):
        correct = 0
        for probe in continuations:
            m = make_mission(task_by_id(probe["taskId"]))
            result = m.replay(State(**probe["state"]), [Action(**a) for a in probe["plan"][:depth]])
            correct += result["firstConflict"] == probe["firstConflict"]
        prefix_scores[str(depth)] = {"correct": correct, "total": len(continuations),
                                    "accuracy": correct / len(continuations)}
    for pair in bank["pairs"]:
        if pair["kind"] not in ("interior-order", "visual-geometry", "appearance-invariant"):
            continue
        a, b = [probes[p] for p in pair["members"]]
        for p in (a, b):
            m = make_mission(task_by_id(p["taskId"]))
            result = m.replay(State(**p["state"]), [Action(**x) for x in p["plan"]])
            assert result["firstConflict"] == p["firstConflict"]
        if pair["kind"] == "interior-order":
            assert a["state"] == b["state"]
            assert a["plan"][0] == b["plan"][0] and a["plan"][-1] == b["plan"][-1]
            assert Counter((x["type"], x["site"]) for x in a["plan"]) == Counter(
                (x["type"], x["site"]) for x in b["plan"])
            prefix = pair["sharedLegalPrefix"]
            assert a["plan"][:prefix] == b["plan"][:prefix]
            assert a["plan"][prefix] != b["plan"][prefix]
            assert (a["firstConflict"] is None) != (b["firstConflict"] is None)
        elif pair["kind"] == "visual-geometry":
            assert a["state"] == b["state"] and a["plan"] == b["plan"]
            assert a["firstConflict"] != b["firstConflict"]
            tasks = [task_by_id(p["taskId"]) for p in (a, b)]
            for key in ("start", "goal", "capacity", "jobs", "sourceGroup"):
                assert tasks[0][key] == tasks[1][key]
            domains = [domain(t["profile"]) for t in tasks]
            registered = [[{k: d.parts[i][k] for k in ("sourceIndex", "rawMatrix", "partNumber", "colorHex")}
                           for i in d.mutable] for d in domains]
            assert registered[0] == registered[1]
            assert all(d.supported(State(**a["state"]).assembly) for d in domains)
        else:
            assert a["plan"] == b["plan"] and a["firstConflict"] == b["firstConflict"]
            assert {a["appearance"], b["appearance"]} == {"original", "grayscale"}
    repair = [p for p in probes.values() if p["kind"] == "delayed-repair"]
    for p in repair:
        oracle = load_oracle(p["taskId"])
        checkpoint = State(**p["checkpoint"])
        history = [Action(**a) for a in p["history"]]
        replay = oracle.mission.replay(checkpoint, history)
        assert replay["firstConflict"] is None and asdict(replay["state"]) == p["state"]
        assert len(history) == 1 + p["lagAfterError"]
        assert len(set(replay["states"])) == len(replay["states"])
        assert 1 + oracle.distance(replay["states"][1]) > oracle.distance(checkpoint)
        corridor = optimal_corridor(oracle, checkpoint) - {oracle.target}
        assert all(oracle.encode(s) not in corridor for s in replay["states"][1:])
        assert forward_repair(oracle, replay["state"], corridor) == p["minimumRepairCost"]
        best = []
        for i, action in enumerate(p["choices"]):
            after, code = oracle.mission.transition(replay["state"], Action(**action))
            assert code == "OK"
            distance = forward_repair(oracle, after, corridor) if after != oracle.mission.terminal else -1
            assert distance == p["labels"][i]["remainingRepairCost"]
            if distance >= 0 and distance + 1 == p["minimumRepairCost"]:
                best.append(i)
        assert best == p["optimalChoices"]
    splits = {split: sorted({t["sourceGroup"] for t in bank["episodes"] if t["split"] == split})
              for split in ("development", "heldout-source")}
    assert not set(splits["development"]) & set(splits["heldout-source"])
    assert len(splits["heldout-source"]) >= 3
    for t in bank["episodes"]:
        assert t["tier"] == "D" + str(1 + (t["optimalCost"] > 8)
                                     + (t["optimalCost"] > 16) + (t["optimalCost"] > 24))
        if t["split"] == "heldout-source":
            assert t["sampling"] == "frozen-source-plan" and domain(t["profile"]).n <= 16
    conflicts = Counter(p["firstConflict"] for p in continuations if p["firstConflict"] is not None)
    choices = [p for p in probes.values() if p["kind"] == "next-action"]
    result = {
        "passed": True,
        "census": {"episodes": len(bank["episodes"]), "probes": len(probes),
                   "pairsByKind": dict(Counter(p["kind"] for p in bank["pairs"])),
                   "probesByKind": dict(Counter(p["kind"] for p in probes.values())),
                   "episodesByTier": dict(Counter(t["tier"] for t in bank["episodes"]))},
        "sourceGroups": splits, "conflictPositions": dict(sorted(conflicts.items())),
        "prefixReplayControl": prefix_scores,
        "depthOneOptimisticChoiceCoverage": {
            "correct": sum(p["horizonEvidence"]["1"]["anyOptimal"] for p in choices),
            "total": len(choices), "claim": "No necessary internal reasoning depth is inferred."},
        "repairByLag": {str(lag): dict(sorted(Counter(p["minimumRepairCost"] for p in repair
                                                    if p["lagAfterError"] == lag).items()))
                        for lag in (1, 3, 5)},
        "geometry": bank["geometryCensus"]["pairs"],
        "limitations": [
            "Geometry contrasts are development diagnostics; fixed-context part count may differ where explicitly flagged.",
            "New-source geometry pruning was refined after initial geometric failures, before any new-source solver or policy results.",
            "D1–D4 denote operation length; a shallow control can remain competitive.",
            "Population VLM and human experiments remain unmeasured."]}
    assert prefix_scores["2"]["accuracy"] < 0.7
    assert max(p["minimumRepairCost"] for p in repair) > 1
    assert any(p["kind"] == "visual-geometry" for p in bank["pairs"])
    write_json(DATA / "upgrade-audit.json", result)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
