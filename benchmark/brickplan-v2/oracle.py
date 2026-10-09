"""Evaluator-only compressed exact graphs and directed Bellman certificates."""
from array import array
from collections import deque
from dataclasses import asdict
import gzip
import json

import numpy as np

from mission import Action, State, canonical_hash


class PhysicalGraph:
    def __init__(self, domain, capacity, root):
        self.domain, self.capacity = domain, capacity
        self.states, self.index, self.edges = [root], {root: 0}, []
        for state in self.states:
            row = []
            for op, site, after in domain.moves(state):
                if domain.n - after.bit_count() > capacity:
                    continue
                if after not in self.index:
                    self.index[after] = len(self.states)
                    self.states.append(after)
                row.append((op, site, self.index[after]))
            self.edges.append(row)
        # Stable numbering for any root in the same connected component.
        old_states, old_edges = self.states, self.edges
        self.states = sorted(old_states)
        self.index = {s: i for i, s in enumerate(self.states)}
        self.edges = [[] for _ in self.states]
        for p, state in enumerate(old_states):
            self.edges[self.index[state]] = [
                (op, site, self.index[old_states[n]]) for op, site, n in old_edges[p]]
        self.hash = canonical_hash({
            "physical": domain.transition_hash, "capacity": capacity,
            "states": self.states, "edges": self.edges})


class Oracle:
    def __init__(self, mission, graph=None, costs=None):
        self.mission = mission
        self.graph = graph or PhysicalGraph(mission.domain, mission.capacity, mission.goal)
        if (self.graph.capacity != mission.capacity
                or self.graph.domain.transition_hash != mission.domain.transition_hash
                or mission.goal not in self.graph.index):
            raise ValueError("Graph does not implement this mission")
        self.width = 1 << len(mission.jobs)
        self.size = len(self.graph.states) * self.width
        self.target = self.encode(mission.terminal)
        self.costs = array("i", costs) if costs is not None else self.solve()
        if len(self.costs) != self.size:
            raise ValueError("Wrong product graph size")

    def encode(self, state):
        return self.graph.index[state.assembly] * self.width + state.done

    def decode(self, node):
        physical, flags = divmod(node, self.width)
        return State(self.graph.states[physical], flags)

    def distance(self, state):
        if not self.mission.valid(state) or state.assembly not in self.graph.index:
            return -1
        return self.costs[self.encode(state)]

    def next(self, node):
        p, flags = divmod(node, self.width)
        assembly = self.graph.states[p]
        for j, site in enumerate(self.mission.jobs):
            if not flags & (1 << j) and not assembly & (1 << site):
                yield Action("audit", site), p * self.width + (flags | (1 << j))
        for op, site, after in self.graph.edges[p]:
            yield Action(op, site), after * self.width + flags

    def solve(self):
        costs = array("i", [-1]) * self.size
        costs[self.target] = 0
        queue = deque([self.target])
        while queue:
            node = queue.popleft()
            p, flags = divmod(node, self.width)
            assembly = self.graph.states[p]
            for _, _, neighbor in self.graph.edges[p]:
                pred = neighbor * self.width + flags
                if costs[pred] < 0:
                    costs[pred] = costs[node] + 1
                    queue.append(pred)
            for j, site in enumerate(self.mission.jobs):
                if flags & (1 << j) and not assembly & (1 << site):
                    pred = p * self.width + (flags ^ (1 << j))
                    if costs[pred] < 0:
                        costs[pred] = costs[node] + 1
                        queue.append(pred)
        return costs

    def witness(self, start):
        if self.distance(start) < 0:
            raise ValueError("Unreachable mission")
        node, actions = self.encode(start), []
        while node != self.target:
            good = [(a, n) for a, n in self.next(node)
                    if self.costs[n] == self.costs[node] - 1]
            action, node = min(good, key=lambda item: (
                item[0].type != "audit", item[0].type != "attach", item[0].site))
            actions.append(action)
        return actions

    def optimal_actions(self, state):
        value = self.distance(state)
        if value <= 0:
            return []
        return [a for a, after in self.mission.moves(state)
                if self.distance(after) == value - 1]

    def forward_distances(self, start):
        """Directed checkpoint distances, used to define a recovery corridor."""
        distances = array("i", [-1]) * self.size
        node = self.encode(start)
        distances[node] = 0
        queue = deque([node])
        while queue:
            node = queue.popleft()
            for _, after in self.next(node):
                if distances[after] < 0:
                    distances[after] = distances[node] + 1
                    queue.append(after)
        return distances

    def verify(self):
        """Exhaustive Bellman + reachability + heuristic check, not just replay."""
        if self.costs[self.target] != 0:
            raise AssertionError("Terminal cost")
        edges, reachable, loose, max_gap = 0, 0, 0, 0
        # Each physical edge must match the independent runtime in both directions.
        for p, assembly in enumerate(self.graph.states):
            runtime = {(a.type, a.site, after.assembly)
                       for a, after in self.mission.moves(State(assembly, self.mission.all_done))}
            encoded = {(op, site, self.graph.states[n]) for op, site, n in self.graph.edges[p]}
            if runtime != encoded:
                raise AssertionError("Graph/runtime edge mismatch")
            for op, site, n in self.graph.edges[p]:
                reverse = "detach" if op == "attach" else "attach"
                restored, code = self.mission.domain.transition(self.graph.states[n], reverse, site)
                if code != "OK" or restored != assembly:
                    raise AssertionError("Asymmetric physical edge")
        for node, value in enumerate(self.costs):
            state = self.decode(node)
            candidates = []
            for action, after in self.next(node):
                # Audit edges use a second path through the runtime contract.
                if action.type == "audit":
                    result, code = self.mission.transition(state, action)
                    if code != "OK" or result != self.decode(after):
                        raise AssertionError("Incorrect inspection edge")
                edges += 1
                if self.costs[after] >= 0:
                    candidates.append(1 + self.costs[after])
            expected = 0 if node == self.target else min(candidates, default=-1)
            if value != expected:
                raise AssertionError(("Bellman", node, value, expected))
            if value >= 0:
                reachable += 1
                gap = value - self.mission.lower_bound(state)
                if gap < 0:
                    raise AssertionError("Nonadmissible static closure bound")
                loose += gap > 0
                max_gap = max(max_gap, gap)
        return {"productStates": self.size, "reachableProductStates": reachable,
                "directedTransitions": edges, "bellmanVerified": True,
                "runtimeEdgesVerified": True, "lowerBoundVerified": True,
                "statesExceedingRelaxation": loose, "maxRelaxationGap": max_gap}

    def horizon_tables(self, depths=(1, 2, 4, 8)):
        """Exact depth-limited minimax-free search using the strong static bound.

        H_0=h; H_d(x)=min_a(1+H_{d-1}(T(x,a))); terminal is absorbing.
        This computes actual conditional choice values, not supplied-plan length.
        """
        current = np.array([self.mission.lower_bound(self.decode(i))
                            for i in range(self.size)], dtype=np.int32).reshape(-1, self.width)
        physical, neighbor = [], []
        for p, row in enumerate(self.graph.edges):
            for _, _, after in row:
                physical.append(p)
                neighbor.append(after)
        physical = np.array(physical)
        neighbor = np.array(neighbor)
        flags = np.arange(self.width)
        tables = {0: current.copy().reshape(-1)}
        for depth in range(1, max(depths) + 1):
            following = np.full_like(current, 1000000)
            for flag in range(self.width):
                np.minimum.at(following[:, flag], physical, 1 + current[neighbor, flag])
            for j, site in enumerate(self.mission.jobs):
                rows = np.array([p for p, s in enumerate(self.graph.states) if not s & (1 << site)])
                incomplete = flags[(flags & (1 << j)) == 0]
                if len(rows):
                    ix = np.ix_(rows, incomplete)
                    following[ix] = np.minimum(following[ix], 1 + current[np.ix_(rows, incomplete | (1 << j))])
            following.reshape(-1)[self.target] = 0
            current = following
            if depth in depths or depth + 1 in depths:
                tables[depth] = current.copy().reshape(-1)
        return tables

    def save(self, path):
        value = {"schema": "brickplan-oracle/2.0", "graphHash": self.graph.hash,
                 "missionHash": self.mission.transition_hash, "goal": self.mission.goal,
                 "costs": list(self.costs)}
        path.write_bytes(gzip.compress(json.dumps(value, separators=(",", ":"), sort_keys=True).encode(), mtime=0))
        return canonical_hash(value)

    @classmethod
    def load(cls, mission, graph, path, expected_hash=None):
        value = json.loads(gzip.decompress(path.read_bytes()))
        if expected_hash is not None and canonical_hash(value) != expected_hash:
            raise ValueError("Oracle content certificate mismatch")
        if (value["schema"] != "brickplan-oracle/2.0" or value["graphHash"] != graph.hash
                or value["missionHash"] != mission.transition_hash or value["goal"] != mission.goal):
            raise ValueError("Oracle identity mismatch")
        return cls(mission, graph, value["costs"])
