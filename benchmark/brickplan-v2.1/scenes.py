"""Original LDraw geometry for unscored practice; never a model observation."""
from dataclasses import asdict
import json

from bank import HERE, make_mission, task_by_id
from probes import Probe, probe_by_id
from session import Session, replay_export


def scene(session, grayscale=False):
    from visual import meshes
    domain = session.domain
    return {
        "schema": "brickplan-practice-scene/2.1",
        "scope": "Unscored practice inspection. Exploded poses are diagrams only.",
        "parts": domain.parts, "mutable": domain.mutable, "fixed": sorted(domain.fixed),
        "meshes": {p["partNumber"]: meshes()[p["partNumber"]] for p in domain.parts},
        "siteIds": session.site_ids, "partIds": session.part_ids, "fixedIds": session.fixed_ids,
        "goal": session.mission.goal, "revision": session.revision,
        "frames": [session.task["start"]] + [e["after"] for e in session.events],
        "current": asdict(session.state), "grayscale": grayscale,
    }


def preview_scene(arena, key):
    if key in arena.probe_ids:
        probe = Probe(probe_by_id(arena.probe_ids[key]), key, arena.seed, arena.identity)
        return scene(probe.session, probe.probe.get("appearance") == "grayscale")
    task = task_by_id(arena.tasks[key])
    return scene(Session(make_mission(task), task, arena.seed, arena.track))


def model_scene(arena, key):
    if key == "case-local":
        record = json.loads((HERE / "cases/local-vlm.authoritative.json").read_text())
        task = task_by_id(record["taskId"])
        return scene(replay_export(make_mission(task), task, record))
    run = arena.model_manager().get(key)
    return scene(arena.sessions[run["sessionId"]])
