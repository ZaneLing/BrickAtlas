"""Shared human/agent protocol with registered identities and bounded inspection."""
from dataclasses import asdict
import copy
import random

from mission import Action, State, canonical_hash

VIEWS = ("isometric", "front", "rear", "left", "right", "top", "bottom", "exploded-reference")
TRACKS = ("image-id", "structured")


class Session:
    def __init__(self, mission, task, seed=0, track="structured", render_images=False, identity=None):
        if type(seed) is not int or not 0 <= seed < 2**32:
            raise ValueError("Seed must be an unsigned 32-bit integer")
        if track not in TRACKS:
            raise ValueError("Unknown observation condition")
        self.mission, self.domain, self.task = mission, mission.domain, copy.deepcopy(task)
        self.seed, self.track, self.render_images = seed, track, render_images
        self.identity = copy.deepcopy(identity or {"runId": "offline", "sessionId": "offline",
                                                  "participantId": "software", "condition": track})
        if self.identity.get("condition") != track:
            raise ValueError("Identity/condition mismatch")
        self.state = State(**task["start"])
        if not mission.valid(self.state):
            raise ValueError("Invalid initial state")
        rng = random.Random(seed)
        indices = list(range(self.domain.n))
        rng.shuffle(indices)
        self.site_ids = {i: f"S{indices[i] + 1:03d}" for i in range(self.domain.n)}
        rng.shuffle(indices)
        self.part_ids = {i: f"P{indices[i] + 1:03d}" for i in range(self.domain.n)}
        self.sites = {v: k for k, v in self.site_ids.items()}
        self.pieces = {v: k for k, v in self.part_ids.items()}
        fixed = sorted(self.domain.fixed)
        rng.shuffle(fixed)
        self.fixed_ids = {local: f"F{i + 1:03d}" for i, local in enumerate(fixed)}
        self.attempts = self.views = self.diagnoses = self.revision = 0
        self.terminated, self.termination, self.view = False, None, "isometric"
        self.events, self.requests, self.view_records = [], {}, []
        self.image_cache = {}

    def public_action(self, action):
        if isinstance(action, dict):
            action = Action(**action)
        value = {"type": action.type, "partId": self.part_ids[action.site]}
        if action.type == "attach":
            value["siteId"] = self.site_ids[action.site]
        return value

    def _images(self, state, view):
        key = (state, view)
        if key not in self.image_cache:
            from visual import observation_images
            self.image_cache[key] = observation_images(self, state, view)
        return self.image_cache[key]

    def observation(self):
        d, m = self.domain, self.mission
        result = {
            "schema": "brickplan-observation/2.0", "taskId": self.task["id"],
            "track": self.track, "sessionId": self.identity["sessionId"],
            "revision": self.revision, "view": self.view,
            "attempts": self.attempts, "remainingActions": self.task["maxActions"] - self.attempts,
            "actionBudget": self.task["maxActions"], "remainingViews": self.task["maxViews"] - self.views,
            "remainingDiagnoses": self.task["maxDiagnoses"] - self.diagnoses,
            "terminated": self.terminated, "termination": self.termination,
            "rack": {"capacity": m.capacity, "occupiedHolders": d.n - self.state.assembly.bit_count(),
                     "rule": "Each detached registered piece uses one universal oversized holder."},
            "workOrders": sorted([
                {"partId": self.part_ids[site], "operation": "inspect-off-assembly",
                 "completed": bool(self.state.done & bit)}
                for site, bit in m.job_bit.items()], key=lambda x: x["partId"]),
            "partIds": sorted(self.pieces), "siteIds": sorted(self.sites),
            "registration": sorted([{"partId": self.part_ids[i], "siteId": self.site_ids[i]}
                                     for i in range(d.n)], key=lambda x: x["partId"]),
            "identityRule": "Each P piece fits only its registered original S site; pieces are not interchangeable.",
            "fixture": "All F pieces form one connected clamped base. Only named P pieces may be moved.",
            "completion": "Match the target assembly and complete every declared off-assembly inspection.",
            "diagnosisQuestion": "Since your last diagnosis (or the start), did a legal operation add avoidable future cost?",
            "actions": {
                "attach": {"type": "attach", "partId": "P...", "siteId": "S..."},
                "detach": {"type": "detach", "partId": "P..."},
                "audit": {"type": "audit", "partId": "P..."},
                "inspect": {"type": "inspect", "view": list(VIEWS)},
                "diagnose": {"type": "diagnose", "avoidableError": "boolean"},
                "finish": {"type": "finish"}},
            "inspectionHistory": []}
        if self.track == "structured":
            result["sites"] = sorted([{
                "id": self.site_ids[i], "registeredPartId": self.part_ids[i],
                "installed": bool(self.state.assembly & (1 << i)),
                "required": bool(m.goal & (1 << i)),
                "partNumber": d.parts[local]["partNumber"], "color": d.parts[local]["colorHex"],
                "matrix": d.parts[local]["rawMatrix"], "direction": d.parts[local]["direction"],
                "pathLengthLDU": next(p["lengthLDU"] for p in d.geometry["paths"] if p["moving"] == local),
            } for i, local in enumerate(d.mutable)], key=lambda x: x["id"])
            result["fixed"] = [
                {"id": self.fixed_ids[local], "partNumber": d.parts[local]["partNumber"],
                 "color": d.parts[local]["colorHex"], "matrix": d.parts[local]["rawMatrix"]}
                for local in sorted(d.fixed, key=self.fixed_ids.get)]
        if self.render_images:
            result["images"] = self._images(self.state, self.view)
        for record in self.view_records:
            public = {"frameId": record["frameId"], "atRevision": record["atRevision"], "view": record["view"]}
            if self.render_images:
                public["images"] = self._images(State(**record["state"]), record["view"])
            result["inspectionHistory"].append(public)
        return result

    def submit(self, request):
        if (not isinstance(request, dict) or set(request) != {"requestId", "revision", "action"}
                or not isinstance(request["requestId"], str) or not 1 <= len(request["requestId"]) <= 100
                or type(request["revision"]) is not int):
            raise ValueError("Envelope requires a request ID, integer revision, and action")
        request_id, digest = request["requestId"], canonical_hash(request)
        if request_id in self.requests:
            old_digest, response = self.requests[request_id]
            if old_digest != digest:
                raise ValueError("Request ID reused with different content")
            return copy.deepcopy(response)
        if self.terminated:
            raise ValueError("Episode ended")
        if request["revision"] != self.revision:
            raise ValueError("Stale revision")
        action = request["action"]
        kind = action.get("type") if isinstance(action, dict) else None
        before, code, cost, internal = self.state, "INVALID_ACTION", 1, None
        if kind == "finish" and set(action) == {"type"}:
            code, cost = "FINISHED", 0
            self.terminated, self.termination = True, "finish"
        elif kind == "inspect" and set(action) == {"type", "view"} and action["view"] in VIEWS:
            if self.views < self.task["maxViews"]:
                self.views += 1
                self.view, code, cost = action["view"], "INSPECTED", 0
                record = {"state": asdict(before), "view": self.view, "atRevision": self.revision + 1}
                record["frameId"] = canonical_hash({**record, "seed": self.seed})[:24]
                self.view_records.append(record)
            else:
                code = "VIEW_LIMIT"
        elif (kind == "diagnose" and set(action) == {"type", "avoidableError"}
              and type(action["avoidableError"]) is bool):
            if self.diagnoses < self.task["maxDiagnoses"]:
                self.diagnoses += 1
                code, cost = "DIAGNOSIS_RECORDED", 0
            else:
                code = "DIAGNOSIS_LIMIT"
        elif kind in ("attach", "detach", "audit"):
            expected = {"type", "partId", "siteId"} if kind == "attach" else {"type", "partId"}
            if set(action) == expected and isinstance(action.get("partId"), str):
                site = self.pieces.get(action["partId"])
                if site is None:
                    code = "UNKNOWN_PART"
                elif kind == "attach" and not isinstance(action["siteId"], str):
                    code = "UNKNOWN_SITE"
                elif kind == "attach" and action["siteId"] != self.site_ids[site]:
                    code = "REGISTERED_SITE_MISMATCH"
                else:
                    internal = Action(kind, site)
                    self.state, code = self.mission.transition(before, internal)
        self.attempts += cost
        if self.attempts >= self.task["maxActions"]:
            self.terminated, self.termination = True, "action-budget"
        self.revision += 1
        event = {"request": copy.deepcopy(request), "revision": self.revision,
                 "before": asdict(before), "after": asdict(self.state),
                 "internalAction": internal.json() if internal else None,
                 "code": code, "cost": cost, "attempt": self.attempts}
        self.events.append(event)
        response = {"result": {"code": code, "revision": self.revision}, "observation": self.observation()}
        # Store compact responses for non-rendering tests; rendered protocol
        # responses preserve exact idempotence including their inspection history.
        self.requests[request_id] = (digest, copy.deepcopy(response))
        return response

    def export(self):
        return {"schema": "brickplan-trajectory/2.0", "taskId": self.task["id"],
                "taskHash": canonical_hash(self.task), "missionHash": self.mission.transition_hash,
                "seed": self.seed, "track": self.track, "identity": copy.deepcopy(self.identity),
                "events": copy.deepcopy(self.events), "terminated": self.terminated,
                "termination": self.termination}


def replay_export(mission, task, record):
    if (record.get("schema") != "brickplan-trajectory/2.0" or record.get("taskId") != task["id"]
            or record.get("taskHash") != canonical_hash(task)
            or record.get("missionHash") != mission.transition_hash):
        raise ValueError("Trajectory identity/certificate mismatch")
    session = Session(mission, task, record["seed"], record["track"], identity=record["identity"])
    for supplied in record["events"]:
        old_revision = session.revision
        session.submit(supplied["request"])
        if session.revision != old_revision + 1 or session.events[-1] != supplied:
            raise ValueError("Authoritative replay mismatch")
    if record != session.export():
        raise ValueError("Trajectory summary mismatch")
    return session
