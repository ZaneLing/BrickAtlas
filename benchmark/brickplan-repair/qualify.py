"""Author-time qualification of finite, physically connected repair variants.

Run with benchmark/.runtime/mlx-env/bin/python. This does not modify the frozen
E002 bank. Candidate endpoints and vertical paths use the original inset meshes.
"""
from copy import deepcopy
import hashlib
import json
from pathlib import Path
import sys

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "deliverables/brickplan-repair"
sys.path.insert(0, str(ROOT / "robotics/brickplan-mujoco"))
from export_scene import fresh_session
sys.path.insert(0, str(ROOT / "benchmark/brickplan-v1"))
from geometry import endpoint_pair, path_pair, parse_ldr


def shifted(part, delta):
    p = deepcopy(part)
    for key in ("matrix", "rawMatrix"):
        m = np.asarray(p[key])
        m[:3, 3] += delta
        p[key] = m.tolist()
    return p


def line(p):
    m = np.asarray(p["matrix"])
    values = [*m[:3, 3], *m[:3, :3].ravel()]
    return "1 16 " + " ".join(map(str, values)) + f" {p['canonical']}.dat"


def connected(a, b):
    graph = parse_ldr(line(a) + "\n" + line(b))
    return any(e["family"] == "stud" for e in graph.edges)


def main():
    session = fresh_session()
    parts = session.domain.parts
    fixed = {session.fixed_ids[i]: parts[i] for i in session.domain.fixed}
    candidates = {}
    for i, local in enumerate(session.domain.mutable):
        actor = session.part_ids[i]
        candidates[actor + ":goal"] = dict(actor=actor, label="目标位置", part=parts[local])
    candidates["P002:offset"] = dict(actor="P002", label="水平偏移 1 stud",
                                    part=shifted(parts[24], [20, 0, 0]))
    candidates["P002:raised"] = dict(actor="P002", label="多垫一层 plate",
                                    part=shifted(parts[24], [0, -8, 0]))
    rotated = deepcopy(parts[21])
    # 90 degrees world yaw around an actual mating stud, not the AABB centre.
    theta = np.pi / 2
    rot = np.array([[np.cos(theta), 0, -np.sin(theta)], [0, 1, 0],
                    [np.sin(theta), 0, np.cos(theta)]])
    pivot = np.array([-10., -56., 10.])
    for key in ("matrix", "rawMatrix"):
        m = np.asarray(rotated[key])
        m[:3, 3] = pivot + rot @ (m[:3, 3] - pivot)
        m[:3, :3] = rot @ m[:3, :3]
        rotated[key] = m.tolist()
    candidates["P005:turned"] = dict(actor="P005", label="转错 90°（仍有真实 stud 连接）", part=rotated)
    candidates["E001:extra"] = dict(actor="E001", label="额外垫片", part=shifted(parts[23], [0, -8, 0]))
    wrong = deepcopy(parts[18])
    wrong.update(colorCode=1, colorHex="#0055BF")
    candidates["W006:wrong"] = dict(actor="W006", label="错色替代件", part=wrong)
    wrong = deepcopy(parts[23])
    raw = np.asarray(parts[24]["rawMatrix"])
    wrong["matrix"] = (raw @ np.linalg.inv(np.asarray(wrong["rawMatrix"])) @ np.asarray(wrong["matrix"])).tolist()
    wrong["rawMatrix"] = raw.tolist()
    # Same colour isolates wrong type from colour faults.
    wrong.update(colorCode=parts[24]["colorCode"], colorHex=parts[24]["colorHex"])
    candidates["W002:wrong"] = dict(actor="W002", label="错型号替代件", part=wrong)
    evidence = []
    for key, candidate in candidates.items():
        p = candidate["part"]
        candidate.update(endpointBlocked=[], pathBlocked=[], support=[])
        for other, q in {**fixed, **{k: v["part"] for k, v in candidates.items() if k != key}}.items():
            endpoint = endpoint_pair(p, q)
            path = path_pair(p, q, 330.) if endpoint["status"] == "CLEAR" else {"status": "BLOCKED", "method": "endpoint-not-clear"}
            edge = endpoint["status"] == "CLEAR" and connected(p, q)
            if endpoint["status"] != "CLEAR":
                candidate["endpointBlocked"].append(other)
            if path["status"] != "CLEAR":
                candidate["pathBlocked"].append(other)
            if edge:
                candidate["support"].append(other)
            evidence.append(dict(candidate=key, obstacle=other, endpoint=endpoint, path=path, stud=edge))
        print(f"Qualified {key}: {len(candidate['support'])} support neighbours", flush=True)
    payload = dict(schema="brickplan-repair-qualification/1", sourceTask=session.task["id"],
                   sourceMissionHash=session.mission.transition_hash, scaleMetresPerLDU=.0004,
                   extractionLengthLDU=330, fixed=fixed, candidates=candidates, evidence=evidence,
                   boundary="Guarded inset-mesh endpoint and straight +Z path qualification, plus stud graph connectivity. Unknown is forbidden. No force or arbitrary-path guarantee.")
    payload["contentSha256"] = hashlib.sha256(json.dumps(payload, sort_keys=True).encode()).hexdigest()
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "qualification.json").write_text(json.dumps(payload, indent=2) + "\n")


if __name__ == "__main__":
    main()
