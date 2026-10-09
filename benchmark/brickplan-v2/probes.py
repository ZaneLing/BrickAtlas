"""Opaque diagnostic presentation, stable paired IDs and replayable view budgets."""
import copy
import random

from bank import make_mission, task_bank, task_by_id
from mission import canonical_hash
from session import Session, VIEWS


class Probe:
    def __init__(self, probe, public_id, seed, identity):
        self.probe, self.public_id, self.seed = probe, public_id, seed
        self.identity = copy.deepcopy(identity)
        task = copy.deepcopy(task_by_id(probe["taskId"]))
        task["start"] = probe["state"]
        self.session = Session(make_mission(task), task, seed, identity["condition"],
                               identity={**identity, "sessionId": public_id})
        self.order = list(range(len(probe.get("choices", []))))
        random.Random(f"{seed}/{probe['id']}").shuffle(self.order)
        self.requests, self.events, self.answer = {}, [], None
        self.revision = 0

    def public(self, render_images=True):
        session = self.session
        session.render_images = render_images
        observation = session.observation()
        session.render_images = False
        observation["taskId"] = self.public_id
        # Probes are frozen checkpoints, not interactive episodes.
        observation["actions"] = {"inspect": {"type": "inspect", "view": list(VIEWS)}}
        result = {"id": self.public_id, "kind": self.probe["kind"],
                  "question": self.probe["prompt"], "revision": self.revision,
                  "answered": self.answer is not None, "observation": observation}
        if self.probe["kind"] == "next-action":
            result["candidates"] = [session.public_action(self.probe["choices"][i]) for i in self.order]
            result["responseSchema"] = {"choice": "0-based candidate index"}
        else:
            result["proposedPlan"] = [session.public_action(a) for a in self.probe["plan"]]
            result["responseSchema"] = {"firstConflict": "1-based integer or null if all execute"}
        return result

    def submit(self, request):
        if (not isinstance(request, dict) or set(request) != {"requestId", "revision", "action"}
                or not isinstance(request["requestId"], str) or not 1 <= len(request["requestId"]) <= 100
                or type(request["revision"]) is not int):
            raise ValueError("Expected requestId, revision, action")
        key, digest = request["requestId"], canonical_hash(request)
        if key in self.requests:
            old, response = self.requests[key]
            if old != digest:
                raise ValueError("Request ID reused with different content")
            return copy.deepcopy(response)
        if self.answer is not None:
            raise ValueError("Probe answer is frozen")
        if request["revision"] != self.revision:
            raise ValueError("Stale revision")
        action = request["action"]
        if not isinstance(action, dict):
            raise ValueError("Invalid probe action")
        if (set(action) == {"type", "view"} and action["type"] == "inspect"
                and action["view"] in VIEWS):
            if self.session.views >= self.session.task["maxViews"]:
                raise ValueError("Probe view budget exhausted")
            self.session.submit({"requestId": key, "revision": self.session.revision, "action": action})
        elif set(action) == {"type", "answer"} and action["type"] == "answer":
            answer = action["answer"]
            if self.probe["kind"] == "next-action":
                if (not isinstance(answer, dict) or set(answer) != {"choice"}
                        or type(answer["choice"]) is not int or not 0 <= answer["choice"] < len(self.order)):
                    raise ValueError("Expected a valid candidate index")
                self.answer = {"choice": self.order[answer["choice"]]}
            else:
                if (not isinstance(answer, dict) or set(answer) != {"firstConflict"}
                        or not (answer["firstConflict"] is None
                                or type(answer["firstConflict"]) is int
                                and 1 <= answer["firstConflict"] <= len(self.probe["plan"]))):
                    raise ValueError("Expected a 1-based conflict index or null")
                self.answer = copy.deepcopy(answer)
        else:
            raise ValueError("Only inspect or answer is available on a probe")
        self.revision += 1
        self.events.append(copy.deepcopy(request))
        response = {"revision": self.revision, "recorded": self.answer is not None}
        self.requests[key] = (digest, response)
        return copy.deepcopy(response)

    def export(self):
        if self.answer is None:
            return None
        return {"probeId": self.probe["id"], "probeHash": canonical_hash(self.probe),
                "seed": self.seed, "identity": copy.deepcopy(self.identity),
                "answer": copy.deepcopy(self.answer), "requests": copy.deepcopy(self.events)}


def public_mapping(identifiers, seed, prefix):
    ordered = sorted(identifiers)
    random.Random(f"{prefix}/{seed}").shuffle(ordered)
    return {f"{prefix}{i + 1:03d}": key for i, key in enumerate(ordered)}


def probe_by_id(probe_id):
    return next(p for p in task_bank()["probes"] if p["id"] == probe_id)
