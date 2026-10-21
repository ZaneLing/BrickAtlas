"""JSON-lines local adapter; emits image paths, never calls an inference API.

Send one action object on stdin. stdout contains public observations only.
Image roles and anonymous handles are safe to send to an API; private run
records and the design gallery must not be included in a model request.
"""
import argparse
from copy import deepcopy
import hashlib
import io
import json
from pathlib import Path
import re
import sys
import uuid

from core import OUT, ROOT, Episode, dump, render_certificate, sha256
import numpy as np
from render import PALETTE
from dynamic_v5.vision import DynamicVisionRenderer


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--module", required=True)
    parser.add_argument("--condition", default="dynamic-missing",
                        choices=[m+"-"+f for m in ("static", "dynamic")
                                 for f in ("control", "missing", "wrong-color", "extra-layer")])
    parser.add_argument("--seed", type=int, default=0)
    args = parser.parse_args()
    catalogue = json.loads((OUT / "gallery-data.js.json").read_text())
    public_module = next((m for m in catalogue if m["id"] == args.module), None)
    if public_module is None:
        raise ValueError("Unknown module")
    base = OUT / args.module
    cert = json.loads((base / "certificate.private.json").read_text())
    cases = json.loads((base / "cases.private.json").read_text())
    case = next(c for c in cases if c["id"] == args.module + "-" + args.condition)
    ep = Episode(cert, case, args.seed)
    config = (ROOT / "assets-source/ldraw-library/locked/LDConfig.ldr").read_text()
    PALETTE.update(dict(re.findall(r"CODE\s+(\d+)\s+VALUE\s+(#[0-9A-Fa-f]{6})", config)))
    renderer = DynamicVisionRenderer(render_certificate(cert), runtime=ep.runtime)
    pts = np.concatenate([renderer.bounds[k] for k, r in cert["candidates"].items()
                          if r["kind"] == "goal"])
    lo, hi = pts.min(0)-[20, 28, 20], pts.max(0)+[20, 20, 20]
    renderer.bounds["_module_frame"] = np.array(
        [[x,y,z] for x in (lo[0],hi[0]) for y in (lo[1],hi[1]) for z in (lo[2],hi[2])])
    directory = OUT / "runs" / uuid.uuid4().hex
    directory.mkdir(parents=True)
    def asset(data, role, **meta):
        digest = hashlib.sha256(data).hexdigest()
        path = directory / (digest + ".png")
        if not path.exists():
            path.write_bytes(data)
        return dict(role=role, file=str(path), sha256=digest, **meta)
    def render(state, role, view="isometric", only=None, full_scene=False, **meta):
        image, _ = renderer.rgb(state, view, size=(900,660), supersample=1, only=only,
                                 frame_keys=None if only or full_scene else ["_module_frame"])
        stream = io.BytesIO()
        image.save(stream, format="PNG")
        return asset(stream.getvalue(), role, view=view, **meta)
    static_assets = []
    for step in public_module["manual"]:
        static_assets.append(asset((OUT / step["partImage"]).read_bytes(),
                                   "instruction-piece", step=step["step"]))
        for view, filename in step["after"].items():
            static_assets.append(asset((OUT / filename).read_bytes(), "instruction-after",
                                       step=step["step"], view=view))
    initial = {a: "" for a in ep.runtime.actors}
    complete_goal = {a: "" for a in ep.runtime.actors}
    complete_goal.update({r["actor"]: k for k, r in cert["candidates"].items() if r["kind"] == "goal"})
    static_assets.append(render(initial, "scene-overview-initial", full_scene=True))
    static_assets.append(render(complete_goal, "scene-overview-final", full_scene=True))
    for view in ("isometric", "rear", "top"):
        static_assets.append(render(initial, "module-start", view))
        static_assets.append(render(complete_goal, "full-completion-reference", view))
        static_assets.append(render(case["goal"], "acceptance-target", view))
    for actor in sorted(ep.actor_alias, key=ep.actor_alias.get):
        key = next(k for k, r in cert["candidates"].items() if r["actor"] == actor)
        static_assets.append(render({actor: key}, "inventory", only=actor,
                                    partId=ep.actor_alias[actor]))
    def observation():
        obs = ep.observe()
        assets = list(static_assets)
        for view in ("isometric", "rear", "top"):
            assets.append(render(ep.state, "current-now", view))
            if ep.previous is not None:
                assets.append(render(ep.previous, "before-last-action", view))
        fb = ep.feedback or {}
        if fb.get("code") == "INSPECT" and "candidate" in fb:
            key = ep.poses[fb["candidate"]]
            actor = cert["candidates"][key]["actor"]
            assets.append(render({**ep.state, actor:key}, "candidate-preview",
                                 fb["view"], candidate=fb["candidate"]))
        elif fb.get("code") == "INSPECT" and "partId" in fb:
            actor = ep.actors[fb["partId"]]
            key = next(k for k, r in cert["candidates"].items() if r["actor"] == actor)
            assets.append(render({actor:key}, "inventory-inspection", fb["view"],
                                 only=actor, partId=fb["partId"]))
        obs["images"] = assets
        return obs
    print(json.dumps(observation(), ensure_ascii=False), flush=True)
    for line in sys.stdin:
        try:
            ep.step(json.loads(line))
            print(json.dumps(observation(), ensure_ascii=False), flush=True)
        except (ValueError, KeyError, TypeError, json.JSONDecodeError) as exc:
            print(json.dumps(dict(code="INVALID_REQUEST", message=str(exc)), ensure_ascii=False), flush=True)
        if ep.done:
            break
    dump(directory / "record.private.json", dict(caseId=case["id"], seed=args.seed,
                                                score=ep.score(), history=ep.history,
                                                finalState=ep.state))


if __name__ == "__main__":
    main()
