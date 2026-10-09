"""Declared software controls. Never interpreted as human or VLM performance."""
from collections import Counter
import random

from build import HERE, load_bank, write_json
from cases import CASES
from evaluate import evaluate
from online import no_rework
from session import Session

OUT = HERE.parents[1] / "tem/brickplan-v1.2/validation"


def static_rule(d, start, goal):
    """Privileged static blocker closure, followed by legal goal attachments."""
    state, removals = start, start & ~goal
    for i in range(d.n):
        if goal & (1 << i) and not start & (1 << i):
            removals |= start & d.blockers[i]
    while True:
        enlarged = removals
        for i in range(d.n):
            if removals & (1 << i):
                enlarged |= start & d.blockers[i]
        if enlarged == removals:
            break
        removals = enlarged
    actions = []
    while removals:
        move = next((m for m in d.moves(state) if m[0] == "detach" and removals & (1 << m[1])), None)
        if move is None:
            return actions
        op, site, state = move
        actions.append({"type": op, "site": site})
        removals &= ~(1 << site)
    while state != goal:
        move = next((m for m in d.moves(state) if m[0] == "attach" and goal & (1 << m[1])
                     and all(not d.blockers[j] & (1 << m[1]) for j in range(d.n)
                             if goal & (1 << j) and not state & (1 << j) and j != m[1])), None)
        if move is None:
            return actions
        op, site, state = move
        actions.append({"type": op, "site": site})
    return actions


def bounded(d, state, goal, depth, visits):
    """Breadth-limited online lookahead with Hamming leaf heuristic; no cost table."""
    layer = [(state, [])]
    seen = {state}
    candidates, expanded = [], 0
    for _ in range(depth):
        next_layer = []
        for current, plan in layer:
            expanded += 1
            for op, site, after in d.moves(current):
                if after in seen:
                    continue
                seen.add(after)
                p = plan + [{"type": op, "site": site}]
                if after == goal:
                    return p[0], expanded
                next_layer.append((after, p))
                h = (after ^ goal).bit_count()
                candidates.append(((len(p) + h, visits[after], h,
                                    tuple((a["type"], a["site"]) for a in p)), p[0]))
        layer = next_layer
    return min(candidates, key=lambda x: x[0])[1], expanded


def public_greedy(obs, rng, rejected):
    """Uses only public structured IDs, occupancy and type compatibility."""
    extras = [s for s in obs["sites"] if s["installedPartId"] and not s["required"]]
    candidates = [{"type": "detach", "partId": s["installedPartId"]} for s in extras]
    for site in obs["sites"]:
        if site["required"] and not site["installedPartId"]:
            candidates += [{"type": "attach", "partId": p["id"], "siteId": site["id"]}
                           for p in obs["inventory"] if p["partType"] == site["partType"]]
    for action in candidates:
        if str(sorted(action.items())) not in rejected:
            return action
    installed = [s for s in obs["sites"] if s["installedPartId"]]
    return {"type": "detach", "partId": rng.choice(installed)["installedPartId"]} if installed else {"type": "finish"}


def run(policy, seed):
    submission = {"schema": "brickplan-submission/1.2", "episodes": {},
                  "metadata": {"softwareValidationOnly": True, "policy": policy, "seed": seed,
                               "track": "image-id" if policy == "blind-random" else "known-pose-structured"}}
    expanded = 0
    for config in CASES:
        d, tasks, costs, _ = load_bank(config["id"])
        for task in tasks["episodes"]:
            rng = random.Random(seed)
            session = Session(d, task, seed, track=submission["metadata"]["track"])
            table = costs[str(task["goal"])]
            plan = static_rule(d, task["start"], task["goal"]) if policy == "static-relations" else []
            visits, rejected = Counter({session.state: 1}), set()
            while not session.terminated:
                if policy in ("oracle", "static-relations") and session.state == task["goal"]:
                    action = {"type": "finish"}
                elif policy == "oracle":
                    chosen = d.witness(session.state, task["goal"], table)[0]
                    action = session.public_action(chosen)
                elif policy == "static-relations":
                    action = session.public_action(plan.pop(0)) if plan else {"type": "finish"}
                elif policy.startswith("search-"):
                    if session.state == task["goal"]:
                        action = {"type": "finish"}
                    else:
                        chosen, count = bounded(d, session.state, task["goal"], int(policy[-1]), visits)
                        expanded += count
                        action = session.public_action(chosen)
                elif policy == "public-greedy":
                    obs = session.observation()
                    if all(s["required"] == bool(s["installedPartId"]) for s in obs["sites"]):
                        action = {"type": "finish"}
                    else:
                        action = public_greedy(obs, rng, rejected)
                elif policy == "legal-random":
                    # Privileged current-validity control, clearly not an image policy.
                    if session.state == task["goal"]:
                        action = {"type": "finish"}
                    else:
                        op, site, _ = rng.choice(list(d.moves(session.state)))
                        action = session.public_action({"type": op, "site": site})
                else:
                    obs = session.observation()
                    part = rng.choice(obs["partIds"])
                    action = ({"type": "attach", "partId": part, "siteId": rng.choice(obs["siteIds"])}
                              if rng.random() < .5 else {"type": "detach", "partId": part})
                previous = session.state
                session.submit({"requestId": str(session.revision), "revision": session.revision, "action": action})
                if session.state == previous:
                    rejected.add(str(sorted(action.items())))
                else:
                    rejected.clear()
                    visits[session.state] += 1
            submission["episodes"][task["id"]] = session.export()
        if policy == "oracle":
            for kind in ("choices", "lookahead", "counterfactual"):
                submission.setdefault(kind, {})
            for p in tasks["choices"]:
                submission["choices"][p["id"]] = {"choice": next(i for i,l in enumerate(p["labels"]) if not l["budgetLoss"])}
            for p in tasks["lookahead"]:
                submission["lookahead"][p["id"]] = {"firstConflict": p["firstConflict"]}
            for p in tasks["counterfactual"]:
                for m in p["members"]:
                    submission["counterfactual"][f"{p['id']}/{m['id']}"] = {"choice": m["optimalChoices"][0]}
    report = evaluate(submission)
    report["expandedSearchNodes"] = expanded
    write_json(OUT / f"{policy}-{seed}.submission.json", submission)
    write_json(OUT / f"{policy}-{seed}.report.json", report)
    return report


def main():
    rows = []
    scopes = {
        "oracle": "Private exact distance tables; software ceiling",
        "static-relations": "Private connector/blocker graph + legal moves; no state search or cost oracle",
        "search-1": "Private transition model, depth 1, Hamming leaves",
        "search-2": "Private transition model, depth 2, Hamming leaves",
        "search-4": "Private transition model, depth 4, Hamming leaves",
        "public-greedy": "Public structured observation; compatible pieces, rejected-action memory",
        "legal-random": "Private current legal-action set; uniform random",
        "blind-random": "Public image-ID payload; ignores pixels, samples all P/S IDs",
    }
    for policy, scope in scopes.items():
        for seed in ((0,) if policy in ("oracle", "static-relations") else range(3)):
            report = run(policy, seed)
            row = {"policy": policy, "seed": seed, "scope": scope, "success": report["successRate"],
                   "byMode": report["successByMode"], "online": report["online"],
                   "expandedSearchNodes": report["expandedSearchNodes"]}
            rows.append(row)
            print(policy, seed, report["successRate"], flush=True)
    write_json(OUT / "controls.json", {"softwareValidationOnly": True, "rows": rows})


if __name__ == "__main__":
    main()
