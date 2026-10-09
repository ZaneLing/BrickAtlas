"""Public transition model for registered-piece assembly and rack inspection.

The frozen mesh-qualified physical executor is reused without modification.
This module never imports an oracle or a task answer.
"""
from dataclasses import dataclass
from functools import lru_cache
import importlib.util
from pathlib import Path

HERE = Path(__file__).resolve().parent
_spec = importlib.util.spec_from_file_location(
    "brickplan_frozen_physics", HERE.parent / "brickplan-v1.2/engine.py")
_physics = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_physics)
AssemblyDomain = _physics.AssemblyDomain
canonical_hash = _physics.canonical_hash


@dataclass(frozen=True, order=True)
class State:
    assembly: int
    done: int = 0


@dataclass(frozen=True, order=True)
class Action:
    type: str
    site: int

    def json(self):
        return {"type": self.type, "site": self.site}


class Mission:
    """One immutable job specification; flags refer to jobs in declared order.

    Physical P_i is registered to original S_i. Interchangeability is explicitly
    outside this protocol, even for geometrically identical source instances.
    Each detached piece occupies one universal oversized rack holder.
    """

    def __init__(self, domain, capacity, goal, jobs=()):
        self.domain = domain
        if type(capacity) is not int or not 0 <= capacity <= domain.n:
            raise ValueError("Invalid rack capacity")
        if not domain.supported(goal) or domain.n - goal.bit_count() > capacity:
            raise ValueError("Invalid terminal assembly")
        self.jobs = tuple(jobs)
        if len(set(self.jobs)) != len(self.jobs) or any(
                type(i) is not int or not 0 <= i < domain.n for i in self.jobs):
            raise ValueError("Invalid or duplicate inspection job")
        if len(self.jobs) > 8:
            raise ValueError("This release certifies at most eight work orders")
        self.capacity, self.goal = capacity, goal
        self.job_bit = {site: 1 << j for j, site in enumerate(self.jobs)}
        self.all_done = (1 << len(self.jobs)) - 1
        self.terminal = State(goal, self.all_done)
        self.transition_hash = canonical_hash({
            "schema": "brickplan-mission/2.0", "physical": domain.transition_hash,
            "capacity": capacity, "jobs": self.jobs,
            "identity": "one-registered-piece-per-original-site",
        })

    def valid(self, state):
        return (isinstance(state, State) and type(state.done) is int
                and 0 <= state.done <= self.all_done
                and self.domain.supported(state.assembly)
                and self.domain.n - state.assembly.bit_count() <= self.capacity)

    def transition(self, state, action):
        if not self.valid(state):
            raise ValueError("Invalid mission state")
        if not isinstance(action, Action):
            return state, "INVALID_ACTION"
        site, op = action.site, action.type
        if type(site) is not int or not 0 <= site < self.domain.n:
            return state, "UNKNOWN_PIECE"
        if op == "audit":
            if site not in self.job_bit:
                return state, "NO_WORK_ORDER"
            if state.done & self.job_bit[site]:
                return state, "ALREADY_AUDITED"
            if state.assembly & (1 << site):
                return state, "AUDIT_REQUIRES_RACK"
            return State(state.assembly, state.done | self.job_bit[site]), "OK"
        after, code = self.domain.transition(state.assembly, op, site)
        if code != "OK":
            return state, code
        if self.domain.n - after.bit_count() > self.capacity:
            return state, "RACK_FULL"
        return State(after, state.done), "OK"

    def moves(self, state):
        for site, bit in self.job_bit.items():
            if not state.done & bit and not state.assembly & (1 << site):
                yield Action("audit", site), State(state.assembly, state.done | bit)
        for op, site, after in self.domain.moves(state.assembly):
            if self.domain.n - after.bit_count() <= self.capacity:
                yield Action(op, site), State(after, state.done)

    def pending(self, state):
        return tuple(site for site, bit in self.job_bit.items() if not state.done & bit)

    def removal_closure(self, state):
        s, goal, d = state.assembly, self.goal, self.domain
        remove = s & ~goal
        for site in self.pending(state):
            remove |= s & (1 << site)
        missing = goal & ~s
        while missing:
            bit = missing & -missing
            missing ^= bit
            remove |= s & d.blockers[bit.bit_length() - 1]
        frontier = remove
        while frontier:
            bit = frontier & -frontier
            frontier ^= bit
            extra = s & d.blockers[bit.bit_length() - 1] & ~remove
            remove |= extra
            frontier |= extra
        return remove

    @lru_cache(maxsize=500000)
    def lower_bound(self, state):
        """Admissible static closure bound, dropping rack and support scheduling.

        Every pending audit costs one. Every occupied target piece in the
        mandatory removal closure must be detached and reattached. Other
        occupancy differences cost at least one. No exactness is assumed.
        """
        return ((state.assembly ^ self.goal).bit_count()
                + 2 * (self.removal_closure(state) & self.goal).bit_count()
                + len(self.pending(state)))

    def replay(self, start, actions):
        state, states = start, [start]
        for step, action in enumerate(actions, 1):
            state, code = self.transition(state, action)
            states.append(state)
            if code != "OK":
                return {"state": state, "states": states, "firstConflict": step, "code": code}
        return {"state": state, "states": states, "firstConflict": None, "code": "OK"}
