"""Source-pose and straight-path audit, separate from the runtime task scorer.

Clear paths use the 1-Lipschitz property of surface distance under translation.
A midpoint distance greater than half an interval's translation plus the guard
certifies that entire interval. Surface intersections supply blocking witnesses.
These are guarded floating-point certificates over the supplied inset meshes,
not force or unrestricted-motion certificates.
"""
from __future__ import annotations

from functools import lru_cache
from pathlib import Path
import hashlib
import json
import math
import os

import numpy as np
import meshlib.mrmeshpy as mm

ROOT = Path(__file__).resolve().parents[2]
os.environ.setdefault("BRICKNET_DATA", str(ROOT / "benchmark/.runtime/bricknet-data"))
from bricknet.data import load_aliases, load_catalog
from bricknet.graph import parse_ldr
from bricknet.collision import data_dir

GUARD_LDU = 0.002
MIN_INTERVAL_LDU = 0.0005
MAX_NODES = 8192
AXIS_INVERSE = np.diag([2.5, -2.5, -2.5, 1.0])


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def xf(mat: np.ndarray):
    out = mm.AffineXf3f()
    out.A = mm.Matrix3f(*(mm.Vector3f(*row) for row in mat[:3, :3]))
    out.b = mm.Vector3f(*mat[:3, 3])
    return out


@lru_cache(maxsize=None)
def mesh_for(stem: str):
    path = data_dir() / "inset" / f"{stem}.ply"
    mesh = mm.loadMesh(str(path))
    reflection = np.diag([1.0, 1.0, -1.0, 1.0])
    mesh.transform(xf(reflection))
    # Reflection changes handedness. Preserve outward normals for containment.
    if mesh.volume() < 0:
        mesh.topology.flipOrientation()
    if stem in ("3022", "3003") and not mesh.topology.isClosed():
        holes = mesh.topology.findHoleRepresentiveEdges()
        if len(holes) != 1:
            raise ValueError(f"{stem} repair contract changed: expected one triangular hole")
        ring = mesh.topology.getLeftRing(holes[0])
        points = [mesh.points[mesh.topology.org(edge)] for edge in ring]
        # Upstream has one missing triangle within the solid stud at (-10, 10).
        # Original 3022.dat and 3003.dat -> s/3003s02.dat -> stug-2x2.dat
        # reference stud.dat -> 4-4disc.dat, explicitly closing this top.
        # All three inset vertices must lie on y=-3.75 and inside radius 5.8.
        if len(points) != 3 or any(abs(p.y + 3.75) > 0.001
                                  or math.hypot(p.x + 10, p.z - 10) > 5.8 for p in points):
            raise ValueError(f"{stem} hole differs from the source-verified stud-cap defect")
        mm.fillHole(mesh, holes[0])
    if not mesh.topology.isClosed():
        raise ValueError(f"Open collision mesh cannot be qualified: {stem}")
    box = mesh.computeBoundingBox()
    lo = np.array([box.min.x, box.min.y, box.min.z])
    hi = np.array([box.max.x, box.max.y, box.max.z])
    return mesh, lo, hi, sha256(path)


def world_bounds(part: dict):
    _, lo, hi, _ = mesh_for(part["canonical"])
    matrix = np.asarray(part["matrix"])
    rot, offset = matrix[:3, :3], matrix[:3, 3]
    corners = rot * np.array([lo, hi])[:, None, :]
    return offset + corners.min(axis=0).sum(axis=1), offset + corners.max(axis=0).sum(axis=1)


def bounds_separate(a, b, guard: float = GUARD_LDU) -> bool:
    return bool(np.any(a[1] + guard < b[0]) or np.any(b[1] + guard < a[0]))


def load_source(model: str, included: list[int]) -> tuple[list[dict], list[dict], dict]:
    manifest_path = ROOT / f"web/public/models/{model}/manifest.json"
    manifest = json.loads(manifest_path.read_text())
    aliases = load_aliases()
    parts, lines = [], []
    for source_index in included:
        original = manifest["instances"][source_index]
        raw_matrix = AXIS_INVERSE @ np.asarray(original["originalMatrix"]).reshape(4, 4).T
        stem = original["partNumber"]
        canonical, alias = aliases.get(stem, (stem, np.eye(4)))
        matrix = raw_matrix @ alias
        rotation = matrix[:3, :3]
        error = float(np.max(np.abs(rotation.T @ rotation - np.eye(3))))
        if error > 1e-5 or abs(np.linalg.det(rotation) - 1) > 1e-5:
            raise ValueError(f"Non-rigid mutable-domain pose: {model}:{source_index}")
        mesh, lo, hi, mesh_hash = mesh_for(canonical)
        source_file = ROOT / f"assets-source/ldraw-library/locked/parts/{stem}.dat"
        parts.append({
            "sourceIndex": source_index,
            "sourceInstanceId": original["instanceId"],
            "partNumber": stem,
            "canonical": canonical,
            "colorCode": original["colorCode"],
            "colorHex": original["colorHex"],
            "name": original["displayName"],
            "matrix": matrix.tolist(),
            "rawMatrix": raw_matrix.tolist(),
            "originalMatrix": original["originalMatrix"],
            "direction": (-rotation[:, 1]).tolist(),
            "meshSha256": mesh_hash,
            "sourcePartSha256": sha256(source_file),
            "orthogonalityError": error,
        })
        nums = list(matrix[:3, 3]) + list(rotation.ravel())
        lines.append(f"1 {original['colorCode']} " + " ".join(map(str, nums)) + f" {canonical}.dat")
    graph = parse_ldr("\n".join(lines))
    edges = [{"a": int(e["a"]), "b": int(e["b"]), "family": str(e["family"]),
              "aConnector": int(e["a_conn"]), "bConnector": int(e["b_conn"])}
             for e in graph.edges]
    provenance = {
        "modelId": model,
        "manifestSha256": sha256(manifest_path),
        "sourceHash": manifest.get("sourceHash"),
        "sourceModel": manifest["model"],
        "includedSourceIndices": included,
        "sourceGeometryModified": False,
        "derivation": "Selected original instances; no pose edits, inserted spacers, or synthetic bricks.",
    }
    return parts, edges, provenance


@lru_cache(maxsize=None)
def mesh_components(stem: str):
    return mm.getAllComponents(mesh_for(stem)[0])


def contains_surface_component(a, b, transform, components):
    # This is called only after proving no surface intersections. Checking each
    # connected shell avoids a nearest-face normal giving an asymmetric sign
    # on interlocking, nonconvex LEGO parts.
    return any(mm.isNonIntersectingInside(mm.MeshPart(a, region), b, transform) for region in components)


def endpoint_pair(a: dict, b: dict) -> dict:
    bounds_a, bounds_b = world_bounds(a), world_bounds(b)
    if bounds_separate(bounds_a, bounds_b):
        return {"status": "CLEAR", "method": "separating-aabb"}
    mesh_a, *_ = mesh_for(a["canonical"])
    mesh_b, *_ = mesh_for(b["canonical"])
    relative = np.linalg.inv(np.asarray(a["matrix"])) @ np.asarray(b["matrix"])
    transform = xf(relative)
    if len(mm.findCollidingTriangles(mesh_a, mesh_b, transform, True)):
        return {"status": "BLOCKED", "method": "triangle-intersection"}
    if (contains_surface_component(mesh_a, mesh_b, transform, mesh_components(a["canonical"])) or
            contains_surface_component(mesh_b, mesh_a, xf(np.linalg.inv(relative)), mesh_components(b["canonical"]))):
        return {"status": "BLOCKED", "method": "bidirectional-component-containment"}
    distance = math.sqrt(max(0.0, mm.findDistance(mesh_a, mesh_b, transform).distSq))
    return {"status": "CLEAR" if distance > GUARD_LDU else "UNKNOWN",
            "method": "mesh-distance", "distance": distance}


def path_pair(moving: dict, obstacle: dict, length: float) -> dict:
    """Certify final -> outside; reversal gives the same attach path."""
    move_bounds = world_bounds(moving)
    obstacle_bounds = world_bounds(obstacle)
    direction = np.asarray(moving["direction"])
    delta = direction * length
    swept = (np.minimum(move_bounds[0], move_bounds[0] + delta),
             np.maximum(move_bounds[1], move_bounds[1] + delta))
    if bounds_separate(swept, obstacle_bounds):
        return {"status": "CLEAR", "method": "separating-swept-aabb"}
    outside = (move_bounds[0] + delta, move_bounds[1] + delta)
    if not bounds_separate(outside, obstacle_bounds):
        return {"status": "UNKNOWN", "reason": "outside-pose-not-separated"}
    mesh_moving, *_ = mesh_for(moving["canonical"])
    mesh_obstacle, *_ = mesh_for(obstacle["canonical"])
    matrix = np.asarray(moving["matrix"])
    inverse = np.linalg.inv(np.asarray(obstacle["matrix"]))
    accepted, pending = [], [(0.0, length)]
    count = 0
    while pending:
        low, high = pending.pop()
        count += 1
        if count > MAX_NODES:
            return {"status": "UNKNOWN", "reason": "subdivision-budget", "queries": count}
        midpoint = (low + high) / 2
        moved = matrix.copy()
        moved[:3, 3] += direction * midpoint
        relative = xf(inverse @ moved)
        if len(mm.findCollidingTriangles(mesh_obstacle, mesh_moving, relative, True)):
            return {"status": "BLOCKED", "method": "intersection-witness",
                    "distanceAlongPath": midpoint, "queries": count}
        # Distances need not rely on the sign or normal orientation.
        distance = math.sqrt(max(0.0, mm.findDistance(mesh_obstacle, mesh_moving, relative).distSq))
        if distance > (high - low) / 2 + GUARD_LDU:
            accepted.append([low, high, midpoint, distance])
        elif high - low < MIN_INTERVAL_LDU:
            return {"status": "UNKNOWN", "reason": "clearance-below-guard", "queries": count}
        else:
            pending.extend(((low, midpoint), (midpoint, high)))
    return {"status": "CLEAR", "method": "lipschitz-distance-cover",
            "intervals": sorted(accepted), "queries": count}


def qualify(parts: list[dict], mutable_sources: list[int], output: Path,
            reverse_sources: list[int] = ()) -> dict:
    # Two underside plates mate by their own studs; their extraction is downward.
    # This changes the explicit motion contract, never the source placement.
    parts = [dict(p, direction=[-x for x in p["direction"]]) if p["sourceIndex"] in reverse_sources
             else dict(p) for p in parts]
    source_to_index = {p["sourceIndex"]: i for i, p in enumerate(parts)}
    mutable = [source_to_index[i] for i in mutable_sources]
    endpoints = []
    for a in range(len(parts)):
        for b in range(a):
            row = endpoint_pair(parts[a], parts[b])
            if row["status"] != "CLEAR":
                raise ValueError(f"Unqualified endpoint {a},{b}: {row}")
            endpoints.append({"a": a, "b": b, **row})
    paths = []
    for local_index in mutable:
        part = parts[local_index]
        bounds = [world_bounds(p) for p in parts]
        # The selected sites use axis-aligned source orientations. The generous
        # extent makes the external endpoint separate on every tested direction.
        extent = np.max([hi for _, hi in bounds], axis=0) - np.min([lo for lo, _ in bounds], axis=0)
        length = float(math.ceil(np.linalg.norm(extent) + 64.0))
        rows = []
        for j, obstacle in enumerate(parts):
            if j != local_index:
                rows.append({"obstacle": j, **path_pair(part, obstacle, length)})
        unknown = [r for r in rows if r["status"] == "UNKNOWN"]
        fixed_blockers = [r["obstacle"] for r in rows
                          if r["status"] == "BLOCKED" and r["obstacle"] not in mutable]
        if unknown or fixed_blockers:
            raise ValueError(f"Unqualified path source={part['sourceIndex']}: unknown={unknown}, fixed blockers={fixed_blockers}")
        print("qualified source", part["sourceIndex"], part["partNumber"],
              "blockers", [parts[r["obstacle"]]["sourceIndex"] for r in rows if r["status"] == "BLOCKED"], flush=True)
        paths.append({"moving": local_index, "lengthLDU": length, "pairs": rows})
    result = {
        "schema": "brickplan-geometry/1.0", "guardLDU": GUARD_LDU,
        "insetPerSurfaceLDU": 0.25, "scope": "Straight translations over versioned inset meshes.",
        "proxyRepairs": [dict(
            part=stem, operation="Fill one verified triangular stud-top face; no vertex changes.",
            sourceEvidence=names,
            sourceEvidenceHashes=[sha256(ROOT / "assets-source/ldraw-library/locked" / name) for name in names],
        ) for stem, names in {
            "3022": ["parts/3022.dat", "p/stud.dat", "p/4-4disc.dat"],
            "3003": ["parts/3003.dat", "parts/s/3003s01.dat", "parts/s/3003s02.dat",
                     "p/stug-2x2.dat", "p/stud.dat", "p/4-4disc.dat"],
        }.items() if any(p["canonical"] == stem for p in parts)],
        "parts": parts, "mutable": mutable, "endpoints": endpoints, "paths": paths,
    }
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    return result
