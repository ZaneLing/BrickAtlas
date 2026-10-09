"""Opaque, permuted probe presentation and private answer normalization."""
from __future__ import annotations

import copy
import random

from session import Session


class ProbeSet:
    def __init__(self, banks, seed):
        self.entries = {}
        rng = random.Random(seed)
        entries = []
        for domain, tasks, _, _ in banks:
            for kind in ("choices", "lookahead"):
                for p in tasks[kind]:
                    entries.append((kind, domain, p, p["id"], p["goal"], seed + len(entries)))
            for p in tasks["counterfactual"]:
                # All members keep the same scene/instance IDs. Candidate positions vary.
                paired_seed = rng.randrange(2**32)
                for m in p["members"]:
                    entries.append(("counterfactual", domain, p, f"{p['id']}/{m['id']}",
                                    m["goal"], paired_seed))
        rng.shuffle(entries)
        for i, (kind, domain, p, key, goal, scene_seed) in enumerate(entries):
            task = {"id": key, "start": p["start"], "goal": goal, "budget": p.get("budget", 64),
                    "inspectBudget": 32, "diagnoseBudget": 0}
            session = Session(domain, task, scene_seed % 2**32)
            public = {"kind": kind, "observation": session.observation()}
            order = list(range(len(p.get("candidates", []))))
            rng.shuffle(order)
            if kind == "lookahead":
                plan = []
                for j, a in enumerate(p["plan"]):
                    action = session.public_action(a)
                    plan.append(action)
                    session.submit({"requestId": f"plan-{j}", "revision": session.revision, "action": action})
                public.update(horizon=p["horizon"], proposedPlan=plan,
                              question="Predict the first failing action (1-based), or null if all execute.",
                              responseSchema={"firstConflict": "integer or null"})
            else:
                public.update(candidates=[session.public_action(p["candidates"][j]) for j in order],
                              question="Choose a currently offered action that minimizes total completion actions.",
                              responseSchema={"choice": "0-based candidate index"})
            public_id = f"Q{i+1:03d}"
            self.entries[public_id] = {"key": key, "kind": kind, "order": order, "public": public}

    def catalog(self):
        return [{"id": key, "kind": e["kind"]} for key, e in self.entries.items()]

    def get(self, public_id):
        return copy.deepcopy(self.entries[public_id]["public"])

    def normalize(self, answers):
        output = {"choices": {}, "lookahead": {}, "counterfactual": {}}
        positions = {}
        for key, answer in answers.items():
            e = self.entries[key]
            converted = copy.deepcopy(answer)
            if e["kind"] != "lookahead" and isinstance(answer, dict) and set(answer) == {"choice"}:
                index = answer["choice"]
                if type(index) is int and 0 <= index < len(e["order"]):
                    converted["choice"] = e["order"][index]
                    positions[str(index)] = positions.get(str(index), 0) + 1
            output[e["kind"]][e["key"]] = converted
        return output, positions
