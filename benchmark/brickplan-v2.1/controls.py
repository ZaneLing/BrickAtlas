"""Real offline software experiments, separate from unmeasured visual performance."""
from collections import Counter, defaultdict
from dataclasses import asdict
import platform
import time

from bank import DATA, ROOT, load_oracle, make_mission, task_bank, write_json
from mission import Mission, State
from policies import astar, rollout

POLICIES = {
    "oracle": "Private exact product-state costs; software ceiling only.",
    "relaxed-greedy": "Current legal actions + static closure Q; visited-state tie break; no search.",
    "capacity-dispatch": "Resource-aware removal/inspection/staging rules; visited-state escape; no search.",
    "astar-100": "Full transition model, static closure lower bound; 100 expansions per episode.",
    "astar-1000": "Full transition model, static closure lower bound; 1,000 expansions per episode.",
    "astar-500000": "Full transition model, static closure lower bound; 500,000 expansions per episode.",
    "astar-hamming": "Same A* with occupancy + unfinished-audit lower bound; 500,000 expansions.",
    "legal-random": "Uniform current legal actions; no target-conditioned policy.",
    "assembly-only": "Ablation: solve physical target while dropping inspection obligations.",
    "unlimited-rack": "Ablation: plan with unlimited rack, execute under actual capacity.",
}


def run(task, name, seed):
    m, start = make_mission(task), State(**task["start"])
    clock = time.monotonic()
    expansions, generated, reason = 0, 0, "action-budget"
    if name == "oracle":
        plan = load_oracle(task["id"]).witness(start)
        reason = "goal"
    elif name in ("relaxed-greedy", "capacity-dispatch", "legal-random"):
        roll = rollout(m, start, name, task["maxActions"], seed)
        plan = roll["plan"]
        reason = "goal" if roll["solved"] else "action-budget"
    else:
        budget = int(name.split("-")[-1]) if name in ("astar-100", "astar-1000", "astar-500000") else 500000
        planning = m
        planning_start = start
        if name == "assembly-only":
            planning = Mission(m.domain, m.capacity, m.goal)
            planning_start = State(start.assembly)
        elif name == "unlimited-rack":
            planning = Mission(m.domain, m.domain.n, m.goal, m.jobs)
        result = astar(planning, planning_start, budget,
                       "hamming" if name == "astar-hamming" else "closure", seed)
        plan, expansions, generated, reason = result.plan, result.expansions, result.generated, result.reason
    state, executed, invalid = start, 0, []
    for action in plan[:task["maxActions"]]:
        state, code = m.transition(state, action)
        executed += 1
        if code != "OK":
            invalid.append({"step": executed, "action": action.json(), "code": code})
            # Model-mismatch ablations terminate at their first executor rejection.
            reason = "executor-rejection"
            break
    solved = state == m.terminal
    if solved:
        assert executed >= task["optimalCost"]
    return {
        "taskId": task["id"], "profile": task["profile"], "sourceGroup": task["sourceGroup"],
        "tier": task["tier"], "split": task["split"], "policy": name, "seed": seed,
        "success": solved, "operations": executed, "optimal": task["optimalCost"],
        "regret": executed - task["optimalCost"] if solved else None,
        "expansions": expansions, "generated": generated, "stopReason": reason,
        "invalidAttempts": invalid, "elapsedSeconds": time.monotonic() - clock,
        "plan": [a.json() for a in plan], "finalState": asdict(state)}


def summarize(rows):
    n, solved = len(rows), [r for r in rows if r["success"]]
    regrets = [r["regret"] for r in solved]
    return {"assigned": n, "completed": len(solved), "successRate": len(solved) / n if n else None,
            "optimalCompletions": sum(r["regret"] == 0 for r in solved),
            "meanSuccessfulRegret": sum(regrets) / len(regrets) if regrets else None,
            "medianExpansions": sorted(r["expansions"] for r in rows)[n // 2] if n else None,
            "maximumExpansions": max((r["expansions"] for r in rows), default=None),
            "totalSeconds": sum(r["elapsedSeconds"] for r in rows),
            "stops": dict(Counter(r["stopReason"] for r in rows))}


def main():
    bank = task_bank()
    rows, summaries = [], {}
    out = ROOT / "tem/brickplan-v2.1/validation"
    for policy in POLICIES:
        seeds = [0] if policy == "oracle" else [0, 1, 2]
        current = [run(task, policy, seed) for seed in seeds for task in bank["episodes"]]
        rows += current
        summaries[policy] = {
            "scope": POLICIES[policy], "all": summarize(current),
            "byTier": {tier: summarize([r for r in current if r["tier"] == tier])
                       for tier in ("D1", "D2", "D3", "D4")},
            "bySourceGroup": {group: summarize([r for r in current if r["sourceGroup"] == group])
                              for group in sorted({r["sourceGroup"] for r in current})},
            "bySplit": {split: summarize([r for r in current if r["split"] == split])
                        for split in sorted({r["split"] for r in current})},
            "bySeed": {str(seed): summarize([r for r in current if r["seed"] == seed]) for seed in seeds}}
        print(policy, summaries[policy]["all"], flush=True)
        write_json(out / "controls.records.json", rows)
    write_json(DATA / "software-controls.json", {
        "schema": "brickplan-software-controls/2.1", "softwareValidationOnly": True,
        "platform": platform.platform(), "python": platform.python_version(), "policies": summaries,
        "visualModelResults": None, "humanResults": None,
        "uncertainty": "Seeds are tie-order repeats, not independent source samples. Report source-group and sampling splits; no population CI claimed."})


if __name__ == "__main__":
    main()
