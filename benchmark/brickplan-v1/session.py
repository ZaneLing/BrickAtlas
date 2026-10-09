"""Shared human/agent state machine. No oracle is called by action execution."""
from __future__ import annotations

import copy
import random

from engine import canonical_hash

VIEWS = ("isometric", "front", "rear", "left", "right", "top", "bottom")


class Session:
    def __init__(self, domain, task, seed=0):
        if type(seed) is not int or not 0 <= seed < 2**32:
            raise ValueError("seed must be a 32-bit unsigned integer")
        self.domain, self.task, self.seed = domain, copy.deepcopy(task), seed
        self.state = task["start"]
        if not domain.supported(self.state):
            raise ValueError("Unsupported initial state")
        rng = random.Random(seed)
        indices = list(range(domain.n))
        rng.shuffle(indices)
        self.site_ids = {i: f"S{indices[i]+1:03d}" for i in range(domain.n)}
        self.sites = {v: k for k, v in self.site_ids.items()}
        rng.shuffle(indices)
        self.part_ids = {i: f"P{indices[i]+1:03d}" for i in range(domain.n)}
        fixed_order = sorted(domain.fixed)
        rng.shuffle(fixed_order)
        self.fixed_ids = {local: f"F{i+1:03d}" for i, local in enumerate(fixed_order)}
        self.part_types = {
            self.part_ids[i]: self.part_type(i) for i in range(domain.n)}
        # Initial assignment is arbitrary within each physical equivalence class.
        self.installed = {i: self.part_ids[i] for i in range(domain.n) if self.state & (1 << i)}
        self.attempts = self.inspections = self.diagnoses = self.revision = 0
        self.terminated, self.termination, self.view = False, None, "isometric"
        self.events, self.requests = [], {}

    def part_type(self, site):
        part = self.domain.parts[self.domain.mutable[site]]
        return f"{part['canonical']}:{part['colorCode']}"

    def public_action(self, action):
        site = action["site"]
        if action["type"] == "detach":
            return {"type": "detach", "partId": self.installed[site]}
        available = sorted(p for p, kind in self.part_types.items()
                           if kind == self.part_type(site) and p not in self.installed.values())
        if not available:
            raise ValueError("No matching inventory for public action")
        return {"type": "attach", "partId": available[0], "siteId": self.site_ids[site]}

    def observation(self):
        sites = []
        for i, local in enumerate(self.domain.mutable):
            p = self.domain.parts[local]
            sites.append({
                "id": self.site_ids[i], "partType": self.part_type(i),
                "partNumber": p["partNumber"], "name": p["name"], "color": p["colorHex"],
                "matrix": p["rawMatrix"], "direction": p["direction"],
                "pathLengthLDU": next(path["lengthLDU"] for path in self.domain.geometry["paths"]
                                      if path["moving"] == local),
                "required": bool(self.task["goal"] & (1 << i)),
                "installedPartId": self.installed.get(i),
            })
        return {
            "schema": "brickplan-observation/1.0", "track": "known-pose-structured",
            "revision": self.revision, "view": self.view,
            "actionBudget": self.task["budget"], "attempts": self.attempts,
            "remainingActions": self.task["budget"] - self.attempts,
            "remainingInspections": self.task["inspectBudget"] - self.inspections,
            "remainingDiagnoses": self.task["diagnoseBudget"] - self.diagnoses,
            "terminated": self.terminated, "termination": self.termination,
            "sites": sorted(sites, key=lambda p: p["id"]),
            "inventory": [{"id": p, "partType": self.part_types[p]}
                          for p in sorted(self.part_types) if p not in self.installed.values()],
            "fixed": [{"id": self.fixed_ids[i], "partNumber": self.domain.parts[i]["partNumber"],
                       "color": self.domain.parts[i]["colorHex"],
                       "matrix": self.domain.parts[i]["rawMatrix"]}
                      for i in sorted(self.domain.fixed, key=self.fixed_ids.get)],
            "fixture": "All fixed F-parts form one connected, explicitly clamped rigid base.",
            "actions": {
                "attach": {"type": "attach", "partId": "P...", "siteId": "S..."},
                "detach": {"type": "detach", "partId": "P..."},
                "inspect": {"type": "inspect", "view": list(VIEWS)},
                "diagnose": {"type": "diagnose", "needsRework": "boolean"},
                "finish": {"type": "finish"},
            },
        }

    def submit(self, request):
        if (not isinstance(request, dict) or set(request) != {"requestId", "revision", "action"}
                or not isinstance(request["requestId"], str) or not 1 <= len(request["requestId"]) <= 100
                or type(request["revision"]) is not int):
            raise ValueError("Envelope requires requestId, integer revision, and action")
        request_id = request["requestId"]
        digest = canonical_hash(request)
        if request_id in self.requests:
            old_digest, response = self.requests[request_id]
            if old_digest != digest:
                raise ValueError("requestId reused with a different request")
            return copy.deepcopy(response)
        if request["revision"] != self.revision:
            raise ValueError("Revision conflict; re-read the observation")
        if self.terminated:
            raise ValueError("Episode has ended")
        action = request["action"]
        before = self.state
        code, site, removed = "INVALID_ACTION", None, None
        action_type = action.get("type") if isinstance(action, dict) else None
        structural = True
        if action_type == "finish" and set(action) == {"type"}:
            structural = False
            code = "FINISHED"
            self.terminated, self.termination = True, "finish"
        elif action_type == "inspect" and set(action) == {"type", "view"} and action["view"] in VIEWS:
            structural = False
            if self.inspections < self.task["inspectBudget"]:
                self.inspections += 1
                self.view, code = action["view"], "INSPECTED"
            else:
                code = "INSPECTION_LIMIT"
        elif (action_type == "diagnose" and set(action) == {"type", "needsRework"}
              and type(action["needsRework"]) is bool):
            structural = False
            if self.diagnoses < self.task["diagnoseBudget"]:
                self.diagnoses += 1
                code = "DIAGNOSIS_RECORDED"
            else:
                code = "DIAGNOSIS_LIMIT"
        elif (action_type == "attach" and set(action) == {"type", "partId", "siteId"}
              and isinstance(action["partId"], str) and isinstance(action["siteId"], str)):
            site, part = self.sites.get(action["siteId"]), action["partId"]
            if site is None:
                code = "UNKNOWN_SITE"
            elif part not in self.part_types:
                code = "UNKNOWN_PART"
            elif part in self.installed.values():
                code = "PART_NOT_IN_INVENTORY"
            elif self.part_types[part] != self.part_type(site):
                code = "INCOMPATIBLE_PART"
            else:
                self.state, code = self.domain.transition(self.state, "attach", site)
                if code == "OK":
                    self.installed[site] = part
        elif (action_type == "detach" and set(action) == {"type", "partId"}
              and isinstance(action["partId"], str)):
            site = next((i for i, p in self.installed.items() if p == action["partId"]), None)
            if site is None:
                code = "PART_NOT_INSTALLED"
            else:
                self.state, code = self.domain.transition(self.state, "detach", site)
                if code == "OK":
                    removed = self.installed.pop(site)
        if structural:
            self.attempts += 1
        if self.attempts >= self.task["budget"]:
            self.terminated, self.termination = True, "action_budget"
        self.revision += 1
        event = {
            "request": copy.deepcopy(request), "revision": self.revision,
            "before": before, "after": self.state, "site": site, "code": code,
            "structural": structural, "attempt": self.attempts, "removedPartId": removed,
        }
        self.events.append(event)
        response = {"result": {"code": code, "revision": self.revision},
                    "observation": self.observation()}
        self.requests[request_id] = (digest, copy.deepcopy(response))
        return response

    def export(self):
        return {"schema": "brickplan-trajectory/1.0", "taskId": self.task["id"],
                "transitionHash": self.domain.transition_hash, "seed": self.seed,
                "events": copy.deepcopy(self.events)}


def replay_export(domain, task, record):
    if (record.get("schema") != "brickplan-trajectory/1.0"
            or record.get("taskId") != task["id"]
            or record.get("transitionHash") != domain.transition_hash):
        raise ValueError("Trajectory identity or release mismatch")
    session = Session(domain, task, record["seed"])
    for supplied in record["events"]:
        previous_revision = session.revision
        session.submit(supplied["request"])
        if session.revision != previous_revision + 1 or supplied != session.events[-1]:
            raise ValueError("Trajectory result does not match authoritative replay")
    return session
