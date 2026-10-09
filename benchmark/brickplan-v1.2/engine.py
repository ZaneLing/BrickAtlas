"""Finite, goal-independent assembly transitions and exact shortest-path oracles.

Runtime policies use AssemblyDomain.transition. Cost tables belong to the
separate evaluator and must never be included in an observation.
"""
from __future__ import annotations

from array import array
from collections import deque
from functools import lru_cache
from pathlib import Path
import hashlib
import json


def canonical_hash(value) -> str:
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


class AssemblyDomain:
    def __init__(self, geometry: dict, source: dict):
        self.geometry = geometry
        self.source = source
        self.parts = geometry["parts"]
        self.mutable = geometry["mutable"]
        self.n = len(self.mutable)
        if not 0 < self.n <= 22:
            raise ValueError("Finite certification supports 1..22 movable sites")
        if len(set(self.mutable)) != self.n or any(
                type(i) is not int or not 0 <= i < len(self.parts) for i in self.mutable):
            raise ValueError("Invalid or duplicated mutable part indices")
        if len({p["sourceIndex"] for p in self.parts}) != len(self.parts):
            raise ValueError("Duplicated source instances")
        endpoints = geometry["endpoints"]
        expected_pairs = {(a, b) for a in range(len(self.parts)) for b in range(a)}
        if (len(endpoints) != len(expected_pairs)
                or {(e["a"], e["b"]) for e in endpoints} != expected_pairs
                or any(e["status"] != "CLEAR" for e in endpoints)):
            raise ValueError("Incomplete or unqualified endpoint geometry")
        self.full = (1 << self.n) - 1
        self.local_to_site = {local: site for site, local in enumerate(self.mutable)}
        self.source_to_site = {self.parts[local]["sourceIndex"]: site
                               for site, local in enumerate(self.mutable)}
        self.neighbors = [0] * self.n
        self.fixed_neighbors = 0
        self.blockers = [0] * self.n
        self.fixed = set(range(len(self.parts))) - set(self.mutable)
        if not self.fixed:
            raise ValueError("An explicit fixed subassembly is required")
        fixed_adjacency = {i: set() for i in self.fixed}
        for edge in source["edges"]:
            if edge["family"] != "stud":
                raise ValueError("1.0 only qualifies rigidly held stud connections")
            a, b = edge["a"], edge["b"]
            if a == b or a not in range(len(self.parts)) or b not in range(len(self.parts)):
                raise ValueError("Invalid connector edge")
            if a in self.fixed and b in self.fixed:
                fixed_adjacency[a].add(b)
                fixed_adjacency[b].add(a)
            for x, y in ((a, b), (b, a)):
                if x in self.local_to_site:
                    i = self.local_to_site[x]
                    if y in self.local_to_site:
                        self.neighbors[i] |= 1 << self.local_to_site[y]
                    else:
                        self.fixed_neighbors |= 1 << i
        seen, stack = set(), [min(self.fixed)]
        while stack:
            i = stack.pop()
            if i not in seen:
                seen.add(i)
                stack.extend(fixed_adjacency[i] - seen)
        if seen != self.fixed:
            raise ValueError(f"Fixed source subassembly is disconnected: {sorted(self.fixed-seen)}")
        if (len(geometry["paths"]) != self.n
                or {p["moving"] for p in geometry["paths"]} != set(self.mutable)):
            raise ValueError("Incomplete movable-path coverage")
        for path in geometry["paths"]:
            if not isinstance(path["lengthLDU"], (int, float)) or not 0 < path["lengthLDU"] < 100000:
                raise ValueError("Invalid path length")
            site = self.local_to_site[path["moving"]]
            expected = set(range(len(self.parts))) - {path["moving"]}
            if {p["obstacle"] for p in path["pairs"]} != expected or len(path["pairs"]) != len(expected):
                raise ValueError("Incomplete or duplicated path-pair coverage")
            for pair in path["pairs"]:
                if pair["status"] not in ("CLEAR", "BLOCKED"):
                    raise ValueError("Unknown geometry cannot enter a certified domain")
                if pair["status"] == "BLOCKED":
                    if pair["obstacle"] in self.fixed:
                        raise ValueError("Permanently blocked site")
                    self.blockers[site] |= 1 << self.local_to_site[pair["obstacle"]]
        self.transition_hash = canonical_hash({
            "version": "brickplan-transition/1.0",
            "neighbors": self.neighbors,
            "fixedNeighbors": self.fixed_neighbors,
            "blockers": self.blockers,
            "geometryHash": canonical_hash(geometry),
        })

    @classmethod
    def load(cls, case_dir: Path):
        return cls(json.loads((case_dir / "geometry.json").read_text()),
                   json.loads((case_dir / "source.json").read_text()))

    @lru_cache(maxsize=None)
    def supported(self, state: int) -> bool:
        if not isinstance(state, int) or isinstance(state, bool) or state < 0 or state > self.full:
            return False
        reached = state & self.fixed_neighbors
        frontier = reached
        while frontier:
            bit = frontier & -frontier
            frontier ^= bit
            connected = self.neighbors[bit.bit_length() - 1] & state & ~reached
            reached |= connected
            frontier |= connected
        return reached == state

    def transition(self, state: int, operation: str, site: int) -> tuple[int, str]:
        if not self.supported(state):
            raise ValueError("Input state is outside the supported domain")
        if not isinstance(site, int) or isinstance(site, bool) or not 0 <= site < self.n:
            return state, "UNKNOWN_SITE"
        if operation not in ("attach", "detach"):
            return state, "INVALID_ACTION"
        bit = 1 << site
        if operation == "attach" and state & bit:
            return state, "SITE_OCCUPIED"
        if operation == "detach" and not state & bit:
            return state, "SITE_EMPTY"
        if state & self.blockers[site]:
            return state, "MOTION_BLOCKED"
        after = state ^ bit
        if not self.supported(after):
            return state, "UNSUPPORTED_ASSEMBLY"
        return after, "OK"

    def moves(self, state: int):
        """All successful permitted structural transitions; no goal parameter."""
        for site in range(self.n):
            if state & self.blockers[site]:
                continue
            bit = 1 << site
            if state & bit:
                after = state ^ bit
                if self.supported(after):
                    yield "detach", site, after
            elif self.fixed_neighbors & bit or self.neighbors[site] & state:
                yield "attach", site, state | bit

    def distances(self, start: int) -> array:
        if not self.supported(start):
            raise ValueError("Cannot solve from an unsupported state")
        distances = array("i", [-1]) * (self.full + 1)
        distances[start] = 0
        queue = deque([start])
        while queue:
            state = queue.popleft()
            next_distance = distances[state] + 1
            for _, _, after in self.moves(state):
                if distances[after] < 0:
                    distances[after] = next_distance
                    queue.append(after)
        return distances

    def witness(self, start: int, goal: int, distances: array | list[int]) -> list[dict]:
        if distances[start] < 0:
            raise ValueError("No completion witness")
        steps = []
        state = start
        while state != goal:
            candidates = [(op, site, after) for op, site, after in self.moves(state)
                          if distances[after] == distances[state] - 1]
            if not candidates:
                raise ValueError("Distance table has no decreasing witness")
            op, site, after = min(candidates, key=lambda x: (x[0] != "attach", x[1]))
            steps.append({"type": op, "site": site})
            state = after
        return steps

    def replay(self, start: int, plan: list[dict]) -> dict:
        state = start
        states = [state]
        for index, action in enumerate(plan, 1):
            state, code = self.transition(state, action.get("type"), action.get("site"))
            states.append(state)
            if code != "OK":
                return {"firstConflict": index, "code": code, "state": state, "states": states}
        return {"firstConflict": None, "code": "OK", "state": state, "states": states}


def no_undo(state: int, goal: int, distances: array | list[int]) -> bool | None:
    distance = distances[state]
    if distance < 0:
        return None
    return not state & ~goal and distance == goal.bit_count() - state.bit_count()


def minimum_detaches(state: int, goal: int, distances: array | list[int]) -> int | None:
    if distances[state] < 0:
        return None
    balance = goal.bit_count() - state.bit_count()
    difference = distances[state] - balance
    if difference < 0 or difference % 2:
        raise ValueError("Cost table violates single-part action conservation")
    return difference // 2


def verify_distances(domain: AssemblyDomain, goal: int, distances: array | list[int],
                     reachable: array | list[int]) -> dict:
    """Bellman certificate check over every state in the reachable component."""
    if len(distances) != domain.full + 1 or distances[goal] != 0:
        raise ValueError("Malformed goal-distance table")
    states, edges = 0, 0
    for state in range(domain.full + 1):
        if reachable[state] < 0:
            if distances[state] >= 0:
                raise ValueError("Goal table has a different reachable component")
            continue
        states += 1
        distance = distances[state]
        if distance < 0 or (distance == 0) != (state == goal):
            raise ValueError("Wrong reachable or terminal label")
        descending = state == goal
        for op, site, after in domain.moves(state):
            edges += 1
            reverse_op = "detach" if op == "attach" else "attach"
            restored, code = domain.transition(after, reverse_op, site)
            if code != "OK" or restored != state:
                raise ValueError("Declared reversible motion has a non-reversible edge")
            if distances[after] < 0 or abs(distances[after] - distance) > 1:
                raise ValueError("Bellman inequality violated")
            descending |= distances[after] == distance - 1
        if not descending:
            raise ValueError("Nonterminal state lacks a decreasing witness")
        minimum_detaches(state, goal, distances)
    return {"reachableStates": states, "directedTransitions": edges, "bellmanVerified": True}
