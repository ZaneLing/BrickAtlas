"""Semantic, shortcut, observation and protocol acceptance checks."""
import copy
from collections import defaultdict
import hashlib
import json
from pathlib import Path
import tempfile

from build import HERE, load_bank, write_json
from cases import CASES
from engine import canonical_hash
from evaluate import evaluate, episode_score
from online import no_rework
from probes import ProbeSet
from server import Arena
from session import Session, replay_export

OUT = HERE.parents[1] / "tem/brickplan-v1.2/validation"


def submit(s, action):
    return s.submit({"requestId": str(s.revision), "revision": s.revision, "action": action})


def raises(fn):
    try:
        fn()
    except (ValueError, KeyError):
        return
    raise AssertionError("Expected rejection")


def main():
    banks = [load_bank(c["id"]) for c in CASES]
    checks = []
    def passed(name):
        checks.append(name)
        print("PASS", name, flush=True)
    for old in ("brickplan-v1", "brickplan-v1.1"):
        folder = HERE.with_name(old)
        freeze = json.loads((folder / "release-check.json").read_text())
        for name, expected in freeze["artifactSha256"].items():
            assert hashlib.sha256((folder / name).read_bytes()).hexdigest() == expected, (old, name)
    passed("All frozen 1.0 and 1.1 artifacts unchanged")
    matched = defaultdict(list)
    shortcuts = []
    for d, tasks, costs, cert in banks:
        assert canonical_hash(tasks) == cert["tasksHash"]
        for task in tasks["episodes"]:
            for track in ("image-id", "known-pose-structured"):
                s = Session(d, task, 42, track)
                for action in task["completionWitness"]:
                    submit(s, s.public_action(action))
                if not s.terminated:
                    submit(s, {"type": "finish"})
                score = episode_score(d, task, costs, s.export())
                assert score["success"] and score["actionRegret"] == score["detachRegret"] == 0
        for p in tasks["lookahead"]:
            assert d.replay(p["start"], p["plan"])["firstConflict"] == p["firstConflict"]
            matched[p["matchedPair"]].append(p)
            first = p["plan"][0]
            after, _ = d.transition(p["start"], first["type"], first["site"])
            last = p["plan"][-1]
            _, code = d.transition(after, last["type"], last["site"])
            prediction = p["horizon"] if code != "OK" else None
            shortcuts.append(prediction == p["firstConflict"])
        t = tasks["episodes"][-1]
        a = t["legalGoalDirectedTrap"]
        after, code = d.transition(t["start"], a["type"], a["site"])
        assert code == "OK" and 1 + costs[str(t["goal"])][after] > t["optimalActions"]
    passed("All 15 exact episode witnesses replay in both observation tracks")
    for members in matched.values():
        a, b = members
        assert a["start"] == b["start"] and a["goal"] == b["goal"]
        assert a["plan"][0] == b["plan"][0] and a["plan"][-1] == b["plan"][-1]
        signature = lambda p: sorted((x["type"], x["site"]) for x in p["plan"])
        assert signature(a) == signature(b)
        assert (a["firstConflict"] is None) != (b["firstConflict"] is None)
    assert sum(shortcuts) / len(shortcuts) <= .5
    passed("36 matched pairs resist endpoint/action-bag shortcuts; exact geometric conflicts")
    probes = ProbeSet(banks, 20261005, "image-id")
    presented = {}
    for key, entry in probes.entries.items():
        public = probes.get(key)
        if entry["kind"] == "lookahead":
            presented[entry["key"]] = public
    for members in matched.values():
        a, b = [presented[p["id"]] for p in members]
        assert a["observation"] == b["observation"]
        assert a["proposedPlan"][0] == b["proposedPlan"][0]
        assert a["proposedPlan"][-1] == b["proposedPlan"][-1]
    passed("Public matched observations and physical instance IDs are identical")
    d, tasks, costs, _ = banks[0]
    task = next(t for t in tasks["episodes"] if t["mode"] == "checkpoint")
    choice = tasks["choices"][0]
    trap = next(a for a,l in zip(choice["candidates"], choice["labels"]) if l["noUndoLoss"])
    s = Session(d, task, 3)
    submit(s, s.public_action(trap))
    pending = episode_score(d, task, costs, s.export())["online"]
    assert pending["selfInducedEvents"][0]["outcome"] == "censored"
    assert pending["decisions"][0]["eligible"]["noUndo"]
    assert pending["decisions"][0]["loss"]["noUndo"]
    submit(s, {"type": "diagnose", "needsRework": True})
    submit(s, s.public_action({"type": "detach", "site": trap["site"]}))
    submit(s, s.public_action(trap))
    submit(s, {"type": "diagnose", "needsRework": False})
    submit(s, {"type": "diagnose", "needsRework": True})
    submit(s, {"type": "finish"})
    events = episode_score(d, task, costs, s.export())["online"]["selfInducedEvents"]
    assert len(events) == 2
    assert events[0]["outcome"] == "restored" and events[0]["diagnosis"] is True
    assert events[0]["detachesToRestore"] == 1
    assert events[1]["outcome"] == "terminated_unrestored" and events[1]["diagnosis"] is False
    passed("Self-induced detection after structural actions, restoration, recurrence and censoring")
    invalid = Session(d, task, 3)
    while not invalid.terminated:
        submit(invalid, {"type": "attach", "partId": "P999", "siteId": "S999"})
    score = episode_score(d, task, costs, invalid.export())
    assert score["firstBudgetLoss"] == task["budget"] - task["optimalActions"] + 1
    assert not any(any(e["eligible"].values()) for e in score["online"]["decisions"])
    passed("Invalid attempts consume budget but never enter legal-choice denominators")
    missing = evaluate({"schema": "brickplan-submission/1.2"})
    assert missing["structures"] == 3 and missing["independentProvenanceGroups"] == 2
    assert missing["successRate"]["denominator"] == 15 and missing["missingEpisodes"] == 15
    assert all(g["curve"][0]["survivors"] == 0 for g in missing["planSurvival"]["noRework"])
    passed("Data-derived census and missing-episode survival censoring")
    forged = copy.deepcopy(s.export())
    forged["events"][0]["after"] ^= 1
    raises(lambda: replay_export(d, task, forged))
    wrongtask = {**task, "budget": task["budget"] + 1}
    raises(lambda: replay_export(d, wrongtask, s.export()))
    passed("Authoritative replay rejects forged results and changed task budgets")
    with tempfile.TemporaryDirectory() as folder:
        arena = Arena(folder, track="image-id")
        key = next(iter(arena.tasks))
        response = arena.create({"taskId": key, "seed": 3})
        obs = response["observation"]
        forbidden = {"matrix", "required", "installedPartId", "partType", "direction",
                     "pathLengthLDU", "blockers", "neighbors", "optimalActions", "start", "goal"}
        def keys(x):
            if isinstance(x, dict):
                return set(x) | set().union(*(keys(v) for v in x.values()))
            if isinstance(x, list):
                return set().union(*(keys(v) for v in x))
            return set()
        assert not keys(obs) & forbidden and len(obs["images"]) == 4
        sid = response["sessionId"]
        sess = arena.sessions[sid]
        request = {"requestId": "idempotent", "revision": 0, "action": {"type": "inspect", "view": "top"}}
        first = arena.post(f"/api/sessions/{sid}/actions", request)
        assert first == arena.post(f"/api/sessions/{sid}/actions", request)
        assert sess.inspections == 1
        raises(lambda: arena.post(f"/api/sessions/{sid}/actions", {**request, "action":{"type":"finish"}}))
        probe = next(iter(arena.probes.entries))
        for _ in range(33):
            arena.probes.inspect(probe, "top")
        assert arena.probes.entries[probe]["session"].inspections == 32
        passed("Raster-only policy payload, idempotence and enforced view limits")
        arena.post(f"/api/probes/{probe}/answer", {"firstConflict": None})
        raises(lambda: arena.post(f"/api/probes/{probe}/inspect", {"view": "front"}))
        restored = Arena(folder, track="image-id")
        assert restored.sessions[sid].inspections == 1
        raises(lambda: Arena(folder, track="known-pose-structured"))
        passed("Persistent run identity, session restart and frozen probe answers")
    with tempfile.TemporaryDirectory() as folder:
        arena = Arena(folder, study=True)
        result = arena.create({"taskId": next(iter(arena.tasks)), "seed": 1})
        sid = result["sessionId"]
        arena.post(f"/api/sessions/{sid}/actions",
                   {"requestId": "stop", "revision": 0, "action":{"type":"finish"}})
        raises(lambda: arena.get(f"/api/sessions/{sid}/score"))
        raises(lambda: arena.get(f"/api/sessions/{sid}/replay"))
        raises(lambda: arena.create({"taskId": result["taskId"], "seed": 1}))
        passed("Study mode blocks repeated tasks, scores and replay")
    write_json(OUT / "semantic-summary.json", {
        "passed": True, "softwareValidationOnly": True, "checks": checks,
        "matchedPairs": len(matched), "endpointShortcutCorrect": sum(shortcuts),
        "endpointShortcutTotal": len(shortcuts),
    })


if __name__ == "__main__":
    main()
