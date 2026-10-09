"""Declared software controls using transitions and static relations, never costs."""
from collections import Counter
from dataclasses import dataclass
import heapq
import itertools
import random
import time

from mission import Action


@dataclass
class SearchResult:
    plan: list
    solved: bool
    expansions: int
    generated: int
    elapsed_seconds: float
    reason: str

    def summary(self):
        return {"solved": self.solved, "planLength": len(self.plan), "expansions": self.expansions,
                "generated": self.generated, "elapsedSeconds": self.elapsed_seconds, "reason": self.reason}


def astar(mission, start, max_expansions=500000, heuristic="closure", seed=0):
    """Graph A* with reopening, deterministic tie order, and enforced node budget.

    No cost table, reachability index, or precomputed plan is used. h is computed
    solely from the input assembly, declared jobs, target and blocker relations.
    """
    clock = time.monotonic()
    rng = random.Random(seed)
    rank = list(range(mission.domain.n))
    rng.shuffle(rank)
    priority = {site: i for i, site in enumerate(rank)}
    h = (mission.lower_bound if heuristic == "closure" else lambda s: (
        (s.assembly ^ mission.goal).bit_count() + len(mission.pending(s))))
    ticket = itertools.count()
    heap = [(h(start), h(start), next(ticket), 0, start)]
    distance, parents = {start: 0}, {}
    expansions, generated = 0, 1
    while heap:
        _, _, _, g, state = heapq.heappop(heap)
        if distance[state] != g:
            continue
        if state == mission.terminal:
            plan = []
            while state != start:
                previous, action = parents[state]
                plan.append(action)
                state = previous
            return SearchResult(plan[::-1], True, expansions, generated,
                                time.monotonic() - clock, "goal")
        if expansions >= max_expansions:
            return SearchResult([], False, expansions, generated, time.monotonic() - clock, "expansion-budget")
        expansions += 1
        moves = sorted(mission.moves(state), key=lambda x: (
            x[0].type != "audit", x[0].type != "attach", priority[x[0].site]))
        for action, after in moves:
            if g + 1 >= distance.get(after, float("inf")):
                continue
            distance[after] = g + 1
            parents[after] = state, action
            lower = h(after)
            heapq.heappush(heap, (g + 1 + lower, lower, next(ticket), g + 1, after))
            generated += 1
    return SearchResult([], False, expansions, generated, time.monotonic() - clock, "unreachable")


def rollout(mission, start, policy, max_actions, seed=0):
    rng = random.Random(seed)
    order = list(range(mission.domain.n))
    rng.shuffle(order)
    rank = {site: i for i, site in enumerate(order)}
    state, actions, visits = start, [], Counter({start: 1})
    for _ in range(max_actions):
        if state == mission.terminal:
            break
        options = list(mission.moves(state))
        if not options:
            break
        if policy == "legal-random":
            action, after = rng.choice(options)
        elif policy == "relaxed-greedy":
            action, after = min(options, key=lambda x: (
                mission.lower_bound(x[1]), visits[x[1]], x[0].type != "audit", rank[x[0].site]))
        elif policy == "capacity-dispatch":
            # A no-search resource adaptation of the old all-removals rule.
            # Complete available work; remove mandatory blockers; attach a safe
            # target piece; when the rack is full, stage the least blocking part.
            removal = mission.removal_closure(state)
            pending = set(mission.pending(state))

            def score(item):
                a, target = item
                bit = 1 << a.site
                creates = (mission.removal_closure(target) & ~removal).bit_count()
                if a.type == "audit":
                    phase = 0
                elif a.type == "detach" and removal & bit:
                    phase = 1
                elif a.type == "attach" and mission.goal & bit and a.site not in pending and creates == 0:
                    phase = 2
                elif a.type == "attach":
                    phase = 3
                else:
                    phase = 4
                return (visits[target], phase, creates, mission.lower_bound(target), rank[a.site])

            action, after = min(options, key=score)
        else:
            raise ValueError("Unknown rollout control")
        actions.append(action)
        state = after
        visits[state] += 1
    return {"plan": actions, "solved": state == mission.terminal, "state": state,
            "cost": len(actions), "expansions": 0}


def choice_horizon(oracle, state, tables, depths=(1, 2, 4, 8)):
    """Optimistic/pessimistic tie bounds for choosing the next action."""
    node = oracle.encode(state)
    options = list(oracle.next(node))
    if not options or oracle.costs[node] <= 0:
        return {}
    good = {a for a, after in options if oracle.costs[after] == oracle.costs[node] - 1}
    result = {}
    for depth in depths:
        q = {a: 1 + int(tables[depth - 1][after]) for a, after in options}
        predicted = {a for a, value in q.items() if value == min(q.values())}
        result[str(depth)] = {
            "anyOptimal": bool(predicted & good), "allOptimal": predicted <= good,
            "optimalFractionUnderUniformTies": len(predicted & good) / len(predicted),
            "tiedChoices": len(predicted), "optimalChoices": len(good),
            "selected": [a.json() for a in sorted(predicted)]}
    return result
