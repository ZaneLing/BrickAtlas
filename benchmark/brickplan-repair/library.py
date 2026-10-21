"""Source-exact compact repair library; independent of the frozen task bank.

Author-time geometry runs with benchmark/.runtime/mlx-env/bin/python.
All source selection, rejected variants, paths and counterfactuals are exported.
"""
from __future__ import annotations

import argparse
from collections import Counter, deque
from copy import deepcopy
from functools import lru_cache
import hashlib
import json
import math
from pathlib import Path
import sys
import time

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "deliverables/brickplan-repair-library"
sys.path.insert(0, str(ROOT / "benchmark/brickplan-v1"))
from geometry import (AXIS_INVERSE, endpoint_pair, load_source, mesh_for, parse_ldr,
                      path_pair, sha256, world_bounds)
from bricknet.data import load_aliases, load_catalog
from bricknet.graph import _part_info
sys.path.insert(0, str(Path(__file__).resolve().parent))
from engine import Domain
from static_bench import TYPES, TAXONOMY, part_name, replacement_kind

SCOPE = ("Original rigid-part connected subassembly, with exact source transforms. "
         "Guarded inset-mesh endpoints and straight extraction paths; connector graph "
         "anchored by an explicit fixture. Ideal attachment; no clutch, force or "
         "unrestricted robot-path guarantee. UNKNOWN is forbidden.")


def dump(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n")


def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True).encode()).hexdigest()


def line(p):
    m = np.asarray(p["matrix"])
    return "1 16 " + " ".join(map(str, [*m[:3, 3], *m[:3, :3].flat])) + f" {p['canonical']}.dat"


def geometry_key(p):
    return p["canonical"], tuple(np.round(np.asarray(p["matrix"]).ravel(), 8))


class Qualifier:
    def __init__(self):
        self.endpoints, self.paths, self.connections = {}, {}, {}

    def endpoint(self, a, b):
        key = tuple(sorted((geometry_key(a), geometry_key(b))))
        if key not in self.endpoints:
            self.endpoints[key] = endpoint_pair(a, b)
        return self.endpoints[key]

    def path(self, a, b, length):
        key = (geometry_key(a), geometry_key(b), tuple(np.round(a["direction"], 8)), length)
        if key not in self.paths:
            self.paths[key] = path_pair(a, b, length)
        return self.paths[key]

    def connection(self, a, b):
        key = tuple(sorted((geometry_key(a), geometry_key(b))))
        if key not in self.connections:
            graph = parse_ldr(line(a) + "\n" + line(b))
            edges = []
            # Stud connections require exact alignment, not the parser's 3-LDU
            # search tolerance. Non-stud connectors retain their native overlap
            # semantics, and still require endpoint + extraction qualification.
            for e in graph.edges:
                ia, ib = int(e["a"]), int(e["b"])
                ma, mb = np.asarray([a, b][ia]["matrix"]), np.asarray([a, b][ib]["matrix"])
                fa = ma @ _part_info(graph.part_ids[ia]).frames[int(e["a_conn"])]
                fb = mb @ _part_info(graph.part_ids[ib]).frames[int(e["b_conn"])]
                if e["family"] == "stud" and np.linalg.norm(fa[:3, 3]-fb[:3, 3]) > .025:
                    continue
                edges.append(dict(family=str(e["family"]), position=fa[:3, 3].tolist(),
                                  axis=(-fa[:3, 1]).tolist()))
            self.connections[key] = edges
        return self.connections[key]

    def candidate(self, key, p, fixed, candidates, length, label, kind):
        row = dict(actor=key.split(":")[0], label=label, kind=kind, part=p,
                   endpointBlocked=[], pathBlocked=[], support=[], evidence=[])
        for other, q in {**fixed, **{k: v["part"] for k, v in candidates.items()}}.items():
            if key == other:
                continue
            ep = self.endpoint(p, q)
            path = self.path(p, q, length) if ep["status"] == "CLEAR" else dict(status="BLOCKED", method="endpoint-not-clear")
            conns = self.connection(p, q) if ep["status"] == "CLEAR" else []
            if ep["status"] != "CLEAR":
                row["endpointBlocked"].append(other)
            if path["status"] != "CLEAR":
                row["pathBlocked"].append(other)
            if conns:
                row["support"].append(other)
            row["evidence"].append(dict(obstacle=other, endpoint=ep, path=path, connectors=conns))
        return row


def transformed(p, rotation=None, pivot=None, delta=None):
    p = deepcopy(p)
    for key in ("matrix", "rawMatrix"):
        m = np.asarray(p[key])
        if rotation is not None:
            pivot = np.asarray(pivot)
            m[:3, 3] = pivot + rotation @ (m[:3, 3] - pivot)
            m[:3, :3] = rotation @ m[:3, :3]
        if delta is not None:
            m[:3, 3] += delta
        p[key] = m.tolist()
    if rotation is not None:
        p["direction"] = (rotation @ p["direction"]).tolist()
    return p


def substitute(p, stem, color=None):
    """A separate physical spare, aligned in the target's raw part frame."""
    aliases = load_aliases()
    canonical, alias = aliases.get(stem, (stem, np.eye(4)))
    _, _, _, mesh_hash = mesh_for(canonical)
    q = deepcopy(p)
    q.update(partNumber=stem, name=part_name(stem), canonical=canonical, meshSha256=mesh_hash,
             matrix=(np.asarray(p["rawMatrix"]) @ alias).tolist(),
             sourcePartSha256=sha256(ROOT / f"assets-source/ldraw-library/locked/parts/{stem}.dat"),
             sourceInstanceId=f"spare-for:{p['sourceInstanceId']}", sourceIndex=None,
             derivedFromSourceIndex=p["sourceIndex"])
    if color:
        q.update(colorCode=color[0], colorHex=color[1])
    return q


def connected_set(vertices, adjacency, start=None):
    if not vertices:
        return set()
    seen, todo = set(), [min(vertices) if start is None else start]
    while todo:
        i = todo.pop()
        if i not in seen:
            seen.add(i)
            todo.extend((adjacency[i] & vertices) - seen)
    return seen


def read_source(model, repair_rounded=False, correction_limit=.25):
    path = ROOT / "web/public/models" / model / "manifest.json"
    manifest = json.loads(path.read_text())
    prov_path = path.with_name("provenance.json")
    provenance = json.loads(prov_path.read_text()) if prov_path.exists() else {}
    conflicts = {r["partNumber"] for r in provenance.get("embeddedPartLockedPathConflicts", [])}
    parts, rejected = [], []
    # Isolate unsupported parts instead of letting a single unsupported connector
    # or nonrigid source transform discard the entire model.
    for i, row in enumerate(manifest["instances"]):
        try:
            if row["partNumber"] in conflicts:
                raise ValueError("Embedded source part differs from locked library")
            item, _, _ = load_source(model, [i])
            parts.extend(item)
        except Exception as exc:
            rejected.append(dict(sourceIndex=i, partNumber=row["partNumber"], reason=str(exc)[:240]))
    graph = parse_ldr("\n".join(line(p) for p in parts))
    adjacency = {i: set() for i in range(len(parts))}
    for edge in graph.edges:
        a, b = int(edge["a"]), int(edge["b"])
        adjacency[a].add(b)
        adjacency[b].add(a)
    notes = []
    for version in ("2.3", "2.2"):
        p = ROOT / f"benchmark/brickplan-v{version}/data/source-admission.json"
        if p.exists():
            for r in json.loads(p.read_text()).get("sources", []):
                if r.get("model") == model and r.get("exclusionStage") == "source-fidelity":
                    notes.append(r.get("reason", "Full-model source fidelity excluded"))
    source = dict(
        modelId=model, manifestSha256=sha256(path), sourceHash=manifest.get("sourceHash"),
        scope="Exact original rigid-part subset; does not claim complete kit reconstruction.",
        fullModelFidelityNotes=list(dict.fromkeys(notes)), rejectedInstances=rejected,
        originalPartCount=len(manifest["instances"]), validRigidParts=len(parts))
    if repair_rounded:
        parts, adjacency, corrections = rounded_source(manifest, projection_only=repair_rounded == "projection",
                                                       correction_limit=correction_limit)
        source.update(scope="Connector-reconstructed rigid subset of a source with rounded nonrigid transforms.",
                      sourceGeometryModified=True, poseCorrections=corrections, validRigidParts=len(parts))
        source["fullModelFidelityNotes"].append(
            "Source matrices are rounded and not rigid. This target is a declared connector reconstruction, "
            "not an exact-pose source crop. Original matrices and per-instance corrections are retained.")
        source["poseCorrectionMethod"] = "rotation-projection-only" if repair_rounded == "projection" else "connector-reconstruction"
        source["maximumAllowedVertexCorrectionLDU"] = correction_limit
        if repair_rounded == "projection":
            source["scope"] = "Rigid rotation projection of rounded source transforms; source translations unchanged."
            source["fullModelFidelityNotes"][-1] = (
                "Source rotations contain scale/rounding error. Rotations were projected to SO(3), "
                "translations retained, and resulting endpoints/connections/paths requalified. "
                "This is a declared derived target, not an exact-pose crop.")
    return manifest, parts, adjacency, source


def rounded_source(manifest, projection_only=False, correction_limit=.25):
    """Recover rigid connector poses only within a measured small source error.

    This is explicitly a derived target, never passed off as unmodified source.
    The root remains at its source location; canonical connectors determine
    descendants. Every selected pair is requalified by the usual mesh checks.
    """
    from bricknet.graph import decode_graph
    aliases, provisional = load_aliases(), []
    for original in manifest["instances"]:
        try:
            raw = AXIS_INVERSE @ np.asarray(original["originalMatrix"]).reshape(4, 4).T
            rot = raw[:3, :3]
            error = float(np.max(np.abs(rot.T @ rot-np.eye(3))))
            if error > .006 or np.linalg.det(rot) < .99:
                continue
            u, _, vt = np.linalg.svd(rot)
            rigid = raw.copy()
            rigid[:3, :3] = u @ vt
            stem = original["partNumber"]
            canonical, alias = aliases.get(stem, (stem, np.eye(4)))
            _, _, _, mesh_hash = mesh_for(canonical)
            part = dict(sourceIndex=original["index"], sourceInstanceId=original["instanceId"],
                        partNumber=stem, canonical=canonical, colorCode=original["colorCode"],
                        colorHex=original["colorHex"], name=original["displayName"],
                        rawMatrix=rigid.tolist(), matrix=(rigid @ alias).tolist(),
                        sourceOriginalRawMatrix=raw.tolist(), originalMatrix=original["originalMatrix"],
                        direction=(-rigid[:3, 1]).tolist(), meshSha256=mesh_hash,
                        sourcePartSha256=sha256(ROOT / f"assets-source/ldraw-library/locked/parts/{stem}.dat"),
                        orthogonalityError=0., sourceOrthogonalityError=error)
            parse_ldr(line(part))
            provisional.append(part)
        except (ValueError, RuntimeError, KeyError, IndexError):
            continue
    graph = parse_ldr("\n".join(line(p) for p in provisional))
    decoded = decode_graph(graph)
    parts, corrections = [], []
    for comp in graph.components:
        root = min(comp)
        anchor = np.asarray(provisional[root]["matrix"])
        for i in sorted(comp):
            part = provisional[i]
            canonical, alias = aliases.get(part["partNumber"], (part["partNumber"], np.eye(4)))
            matrix = np.asarray(part["matrix"]) if projection_only else anchor @ decoded[i]
            source = np.asarray(part["sourceOriginalRawMatrix"]) @ alias
            points = vertices(canonical)
            original_world = points @ source[:3, :3].T+source[:3, 3]
            recovered_world = points @ matrix[:3, :3].T+matrix[:3, 3]
            deviation = float(np.linalg.norm(original_world-recovered_world, axis=1).max())
            # The declared source correction limit is retained in provenance.
            # Larger inconsistencies remain excluded, never silently snapped.
            if deviation > correction_limit:
                continue
            raw = matrix @ np.linalg.inv(alias)
            part.update(matrix=matrix.tolist(), rawMatrix=raw.tolist(), direction=(-matrix[:3, 1]).tolist(),
                        reconstructedPose=True, maxSourceVertexDeviationLDU=deviation)
            parts.append(part)
            corrections.append(dict(sourceIndex=part["sourceIndex"], maxVertexDisplacementLDU=deviation,
                                    sourceOrthogonalityError=part["sourceOrthogonalityError"]))
    graph = parse_ldr("\n".join(line(p) for p in parts))
    adjacency = {i: set() for i in range(len(parts))}
    for e in graph.edges:
        a, b = int(e["a"]), int(e["b"])
        adjacency[a].add(b)
        adjacency[b].add(a)
    return parts, adjacency, corrections


def select_cluster(parts, adjacency, q, max_parts=11, prefer_complex=False):
    components, remaining = [], set(range(len(parts)))
    while remaining:
        comp = connected_set(remaining, adjacency)
        components.append(comp)
        remaining -= comp
    components.sort(key=lambda s: (-len(s), min(s)))
    proposals = []
    for comp in components[:8]:
        if len(comp) < 2:
            continue
        ranked = sorted(comp, key=lambda i: (-len(adjacency[i]), parts[i]["sourceIndex"]))
        seeds = list(dict.fromkeys([ranked[0], min(comp),
                                   min(comp, key=lambda i: parts[i]["matrix"][1][3]),
                                   ranked[min(3, len(ranked)-1)]]))
        for seed in seeds:
            kept, todo, seen = [], deque([seed]), {seed}
            while todo and len(kept) < max_parts:
                i = todo.popleft()
                if any(q.endpoint(parts[i], parts[j])["status"] != "CLEAR" for j in kept):
                    continue
                if kept and not any(j in adjacency[i] and q.connection(parts[i], parts[j]) for j in kept):
                    continue
                kept.append(i)
                neighbors = sorted(adjacency[i] - seen,
                                   key=lambda j: (abs(j-seed), -len(adjacency[j]), j))
                todo.extend(neighbors)
                seen.update(neighbors)
            if len(kept) >= 2:
                proposals.append(kept)
        if proposals and max(map(len, proposals)) >= max_parts-2:
            break
    if not proposals:
        raise ValueError("No collision-free connected source subset with at least two parts")
    best = None
    for kept in proposals:
        bounds = [world_bounds(parts[i]) for i in kept]
        extent = np.max([b[1] for b in bounds], axis=0)-np.min([b[0] for b in bounds], axis=0)
        length = float(math.ceil(np.linalg.norm(extent)+64))
        anchors = sorted(kept, key=lambda i: (-parts[i]["matrix"][1][3], -len(adjacency[i]), i))[:3]
        # One original part is clamped to the workcell. All other pieces remain
        # real, movable source parts, so no large hidden fixed obstacle set.
        for anchor in anchors:
            chosen, unresolved = {}, 0
            for i in kept:
                if i == anchor:
                    continue
                p = parts[i]
                dirs = [np.asarray(p["direction"]), -np.asarray(p["direction"])]
                for j in kept:
                    if j != i:
                        for edge in q.connection(p, parts[j]):
                            dirs.extend([np.asarray(edge["axis"]), -np.asarray(edge["axis"])])
                directions = {tuple(np.round(d/np.linalg.norm(d), 7)) for d in dirs if np.linalg.norm(d) > .5}
                scores = []
                for d in sorted(directions, key=lambda d: (not np.allclose(d, p["direction"]), d)):
                    moved = dict(p, direction=list(d))
                    pairs = {j: q.path(moved, parts[j], length) for j in kept if j != i}
                    score = (pairs[anchor]["status"] != "CLEAR",
                             sum(r["status"] != "CLEAR" for r in pairs.values()),
                             sum(r["status"] == "UNKNOWN" for r in pairs.values()))
                    scores.append((score, list(d)))
                score, direction = min(scores, key=lambda x: x[0])
                unresolved += int(score[0])
                chosen[i] = dict(p, direction=direction)
            blocking_pairs = sum(sum(q.path(chosen[i], parts[j], length)["status"] != "CLEAR"
                                     for j in kept if j != i) for i in chosen) if prefer_complex else 0
            score = (len(kept)-unresolved*4, -unresolved, blocking_pairs, len(kept))
            if best is None or score > best[0]:
                best = score, kept, anchor, chosen, length
        if not prefer_complex and best and best[0][1] == 0 and len(kept) >= max_parts-1:
            break
    _, kept, anchor, chosen, length = best
    fixed = {"F001": parts[anchor]}
    candidates = {}
    for number, i in enumerate(sorted(set(kept)-{anchor}, key=lambda j: parts[j]["sourceIndex"]), 1):
        actor = f"P{number:03}"
        candidates[actor+":goal"] = dict(actor=actor, part=chosen[i], label="目标位置", kind="goal")
    certificate = dict(schema="brickplan-repair-library-qualification/1", fixed=fixed, candidates=candidates,
                       extractionLengthLDU=length, scaleMetresPerLDU=.0004, boundary=SCOPE)
    qualify_candidates(certificate, q)
    return certificate


def qualify_candidates(cert, q):
    original = deepcopy(cert["candidates"])
    cert["candidates"] = {k: q.candidate(k, r["part"], cert["fixed"], original,
                                      cert["extractionLengthLDU"], r["label"], r["kind"])
                          for k, r in original.items()}


def skeleton(cert, model, edits=None, roots=(), kind="control", title=None):
    edits = edits or {}
    goals = {r["actor"]: k for k, r in cert["candidates"].items() if r["kind"] == "goal"}
    actors = sorted(set(goals) | set(edits))
    goal = {a: goals.get(a, "") for a in actors}
    initial = {**goal, **edits}
    choices = {a: list(dict.fromkeys(k for k in (goal[a], initial[a]) if k)) for a in actors}
    return dict(id=f"{model}:{kind}:"+digest(edits)[:8], modelId=model, title=title or TYPES.get(kind, kind),
                description="", kind=kind, actors=actors, choices=choices, initial=initial, goal=goal,
                roots=[dict(eventId=f"root-{i+1}", partId=a, type=t, stage="Root")
                       for i, (a, t) in enumerate(roots)],
                propagation=[], sourceLabels=["S", "A"], rackCapacity=len(actors),
                sourceExample=model, sourcePieces=1+len(goals), contract=cert["boundary"])


def inverse(action, before):
    return (dict(type="attach", partId=action["partId"], candidate=before[action["partId"]])
            if action["type"] == "detach" else dict(type="detach", partId=action["partId"]))


def difficulty(cost):
    return "D1" if cost <= 2 else "D2" if cost <= 5 else "D3" if cost <= 9 else "D4"


def annotate(case, domain):
    initial = domain.pack(case, case["initial"])
    if domain.valid(case, initial) != "OK":
        raise ValueError(domain.valid(case, initial))
    goal = domain.pack(case, case["goal"])
    if domain.valid(case, goal) != "OK":
        raise ValueError("Invalid target")
    plan = domain.plan(case, initial)
    if plan is None:
        raise ValueError("No exact repair path in the qualified finite domain")
    case["oraclePlan"], case["expectedOptimum"] = plan, len(plan)
    case["difficulty"] = difficulty(len(plan))
    case["description"] = ("无需拆装；直接提交评分。" if not case["roots"] else
                           f"按右侧目标修复；最低 {len(plan)} 次拆装，操作对象使用唯一 ID。")
    if not case["roots"]:
        case["causalReplay"] = dict(origin=case["goal"], events=[])
        return case
    # Replay from the last disassembly point: inject a wrong physical piece,
    # skip a required insertion, or use a wrong pose, then close the covers.
    last_detach = max((i for i, a in enumerate(plan) if a["type"] == "detach"), default=-1)
    prefix, suffix = plan[:last_detach+1], plan[last_detach+1:]
    state, reverse = initial, []
    for action in prefix:
        reverse.insert(0, inverse(action, domain.unpack(case, state)))
        state, v = domain.transition(case, state, action)
        assert v["code"] == "OK"
    changed = {a for a in case["actors"] if case["initial"][a] != case["goal"][a]}
    wrong = [a for a in reverse if a["partId"] in changed]
    correct = [a for a in suffix if a["partId"] in changed]
    covers = [a for a in reverse if a["partId"] not in changed]
    events = []
    for i, root in enumerate(case["roots"]):
        # Multi-root missing/colour cases have explicit actor groups. A
        # spacer-height root owns both the spacer and the displaced top.
        group = set(root.get("affectedActors", [root["partId"]]))
        if len(case["roots"]) == 1:
            group = changed
        events.append(dict(eventId=root["eventId"], rootId=root["eventId"], stage="Root",
                           actions=[a for a in wrong if a["partId"] in group],
                           correctedActions=[a for a in correct if a["partId"] in group]))
    for i, action in enumerate(covers):
        event = dict(eventId=f"close-{i+1}", stage="Propagation", actions=[action])
        events.append(event)
        case["propagation"].append(dict(eventId=event["eventId"], partId=action["partId"], stage="Propagation"))
    case["causalReplay"] = dict(origin=domain.unpack(case, state), events=events)
    cf = domain.root_counterfactuals(case)
    if not cf[-1]["failureAvoided"] or any(r["failureAvoided"] for r in cf[:-1]):
        raise ValueError("Root set not sufficient and minimal under causal replay")
    return case


def add_variant(cert, q, key, p, label, kind, edits, model):
    """Admission includes the entire faulty state and its executable repair."""
    old = deepcopy(cert["candidates"])
    cert["candidates"][key] = dict(actor=key.split(":")[0], part=p, label=label, kind=kind)
    qualify_candidates(cert, q)
    case = skeleton(cert, model, edits, [(key.split(":")[0], kind)], kind)
    try:
        annotate(case, Domain(cert, {}))
    except (ValueError, AssertionError):
        cert["candidates"] = old
        return None
    return case


def generate_model(model, repair_rounded=False, correction_limit=.25):
    started = time.time()
    print("SOURCE", model, flush=True)
    manifest, parts, adjacency, source = read_source(model, repair_rounded=repair_rounded, correction_limit=correction_limit)
    q = Qualifier()
    print("CLUSTER", model, len(parts), flush=True)
    cert = select_cluster(parts, adjacency, q)
    cert.update(modelId=model, source=source)
    if source.get("sourceGeometryModified"):
        cert["boundary"] = SCOPE.replace("Original rigid-part connected subassembly, with exact source transforms.",
                                         f"Declared rigid correction of inconsistent source transforms; maximum allowed vertex displacement {correction_limit*.4:.2f} mm.")
    source["includedSourceIndices"] = sorted([p["sourceIndex"] for p in cert["fixed"].values()] +
                                            [r["part"]["sourceIndex"] for r in cert["candidates"].values()])
    source.setdefault("sourceGeometryModified", False)
    cases, attempts = [], Counter()
    d = Domain(cert, {})
    goals = list(cert["candidates"])
    baseline = annotate(skeleton(cert, model, kind="control", title="无故障对照"), d)
    cases.append(baseline)
    missing = []
    for key in goals:
        actor = key.split(":")[0]
        try:
            c = annotate(skeleton(cert, model, {actor: ""}, [(actor, "missing")], "missing",
                                  f"{actor} 漏件"), d)
            missing.append(c)
        except (ValueError, AssertionError) as exc:
            attempts["missing:"+str(exc)[:60]] += 1
        p = cert["candidates"][key]["part"]
        spare = "W"+actor[1:]
        color = ("1", "#0055BF") if p["colorHex"].lower() != "#0055bf" else ("4", "#C91A09")
        wrong = substitute(p, p["partNumber"], color)
        c = add_variant(cert, q, spare+":color", wrong, "错色替代件", "wrong_color",
                        {actor: "", spare: spare+":color"}, model)
        if c:
            c["title"] = f"{actor} → {spare} 错色替换"
            cases.append(c)
        else:
            attempts["wrong_color:unreachable"] += 1
    cases.extend(missing)
    # Geometry proposals are deliberately bounded and recorded. An inadmissible
    # proposal never becomes an apparently executable error card.
    counts = Counter()
    for key in goals:
        actor, p = key.split(":")[0], cert["candidates"][key]["part"]
        raw = np.asarray(p["rawMatrix"])
        # Shift in the original plate plane; the UI reports the actual vector.
        for axis in (0, 2):
            if counts["offset"] >= 2:
                break
            for sign in (1, -1):
                delta = sign*20*raw[:3, axis]
                # A horizontal stud offset is world horizontal, never a vertical
                # move on a side-facing part mislabeled as horizontal.
                if abs(delta[1]) > .025:
                    continue
                alt = transformed(p, delta=delta)
                cid = actor+f":offset{axis}{'p' if sign > 0 else 'm'}"
                c = add_variant(cert, q, cid, alt, "水平偏移一颗 stud", "offset", {actor: cid}, model)
                attempts["offset:tested"] += 1
                if c:
                    c["title"] = f"{actor} 偏移一颗 stud"
                    cases.append(c)
                    counts["offset"] += 1
                    break
        if counts["rotation"] < 2:
            connections = [edge for other in goals if other != key
                           for edge in q.connection(p, cert["candidates"][other]["part"])]
            connections += [edge for fixed in cert["fixed"].values() for edge in q.connection(p, fixed)]
            pivots = list({tuple(np.round(e["position"], 5)) for e in connections if e["family"] == "stud"})[:4]
            axis = raw[:3, 1]
            cross = np.array([[0, -axis[2], axis[1]], [axis[2], 0, -axis[0]], [-axis[1], axis[0], 0]])
            rotation = np.outer(axis, axis)+cross  # 90 degrees about the part's Y axis.
            for pi, pivot in enumerate(pivots):
                alt = transformed(p, rotation=rotation, pivot=pivot)
                # Identical geometric occupancy is not an orientation error.
                if occupancy_equivalent(p, alt):
                    continue
                cid = actor+f":turn{pi}"
                c = add_variant(cert, q, cid, alt, "绕连接点转错 90°", "rotation", {actor: cid}, model)
                attempts["rotation:tested"] += 1
                if c:
                    c["title"] = f"{actor} 朝向错误"
                    cases.append(c)
                    counts["rotation"] += 1
                    break
        for kind, stems in (("wrong_type", ["3022", "3023", "3069b", "3070b", "3005"]),
                            ("wrong_size", ["3023", "3022", "3710", "3623", "3004", "3005"])):
            if counts[kind]:
                continue
            for stem in stems:
                if stem == p["partNumber"]:
                    continue
                try:
                    alt = substitute(p, stem)
                    # Size and shape/function are mutually exclusive definitions.
                    if replacement_kind(p, alt) != kind:
                        continue
                    if kind == "wrong_type" and occupancy_equivalent(p, alt):
                        continue
                    spare = ("T" if kind == "wrong_type" else "Z")+actor[1:]
                    cid = spare+":"+kind
                    c = add_variant(cert, q, cid, alt, TYPES[kind], kind, {actor: "", spare: cid}, model)
                    attempts[kind+":tested"] += 1
                    if c:
                        c["title"] = f"{actor} → {spare} {TYPES[kind]}"
                        cases.append(c)
                        counts[kind] += 1
                        break
                except (ValueError, KeyError, RuntimeError):
                    attempts[kind+":unsupported_part"] += 1
        # A real extra studded plate supports the elevated part. The offset is
        # never accepted without its actual connector and collision evidence.
        if not counts["height_layer"] and np.allclose(p["direction"], [0, -1, 0]):
            for stem in ("3022", "3023", "3024", "3710"):
                try:
                    extra = substitute(p, stem)
                    extra_actor, raised = "E"+actor[1:], actor+":raised"
                    old = deepcopy(cert["candidates"])
                    cert["candidates"][extra_actor+":extra"] = dict(actor=extra_actor, part=extra,
                                                                    label="多余垫片", kind="extra")
                    cert["candidates"][raised] = dict(actor=actor, part=transformed(p, delta=[0, -8, 0]),
                                                     label="垫高一层 plate", kind="height_layer")
                    qualify_candidates(cert, q)
                    c = skeleton(cert, model, {actor: raised, extra_actor: extra_actor+":extra"},
                                 [(extra_actor, "extra")], "height_layer", f"{actor} 多垫一层 / 多余件")
                    try:
                        annotate(c, Domain(cert, {}))
                        c["tags"] = ["extra", "height_layer"]
                        cases.append(c)
                        counts["height_layer"] += 1
                        break
                    except (ValueError, AssertionError):
                        cert["candidates"] = old
                    attempts["height_layer:tested"] += 1
                except (ValueError, KeyError, RuntimeError):
                    attempts["height_layer:unsupported_part"] += 1
    # Requalify final union, as every candidate must reference every obstacle.
    qualify_candidates(cert, q)
    d = Domain(cert, {})
    # Compound static cases are generated by curate_model after qualification.
    validated = []
    for c in cases:
        try:
            # Keep the individual case choices small; the editor can assemble a
            # different union and must rerun this same exact validation.
            state = d.pack(c, c["initial"])
            assert d.valid(c, state) == "OK"
            plan = d.plan(c, state)
            assert plan is not None and len(plan) == c["expectedOptimum"]
            for action in plan:
                state, check = d.transition(c, state, action)
                assert check["code"] == "OK"
            assert state == d.pack(c, c["goal"])
            cf = d.root_counterfactuals(c)
            assert cf[-1]["failureAvoided"]
            assert not any(r["failureAvoided"] for r in cf[:-1])
            c["counterfactuals"] = cf
            validated.append(c)
        except (ValueError, AssertionError) as exc:
            attempts[c["kind"]+":causal_replay_rejected"] += 1
    if not any(c["kind"] != "control" for c in validated):
        raise ValueError("No nontrivial reachable repair case")
    cert["contentSha256"] = digest(cert)
    folder = OUT / "models" / model
    dump(folder / "qualification.json", cert)
    dump(folder / "cases.json", {c["id"]: c for c in validated})
    dump(folder / "static-proposals.json", {c["id"]: c for c in validated})
    coverage = []
    for tax_id, label, kinds in TAXONOMY:
        ids = [c["id"] for c in validated if c["kind"] in kinds or set(c.get("tags", [])) & set(kinds)]
        reason = None if ids else ("Requires rendered visibility evidence; not inferred from geometric blockers."
                                  if tax_id == "visibility" else
                                  "No admitted connected, collision-free, repairable variant in this source subset and proposal set.")
        coverage.append(dict(id=tax_id, label=label, status="covered" if ids else "not_admitted",
                             caseIds=ids, reason=reason))
    record = dict(modelId=model, title=manifest["model"]["title"], status="ready",
                  originalParts=source["originalPartCount"], caseParts=1+len(goals),
                  mutableParts=len(goals), fixedParts=1, caseCount=len(validated),
                  sourceIndices=source["includedSourceIndices"], sourceNotes=source["fullModelFidelityNotes"],
                  kinds=dict(Counter(c["kind"] for c in validated)), coverage=coverage,
                  difficulty=dict(Counter(c["difficulty"] for c in validated)),
                  attempts=dict(attempts), generationSeconds=round(time.time()-started, 2),
                  qualificationSha256=cert["contentSha256"], source=source,
                  cases=[{k: c[k] for k in ("id", "title", "kind", "difficulty", "expectedOptimum")} for c in validated])
    dump(folder / "record.json", record)
    from static_bench import curate_model
    return curate_model(folder)


@lru_cache(maxsize=512)
def vertices(stem):
    mesh, *_ = mesh_for(stem)
    # Surface vertices, including stud geometry; AABB alone cannot disambiguate
    # a 90-degree rotation of an asymmetric part.
    return np.array([[p.x, p.y, p.z] for p in mesh.points.vec])


def occupancy_equivalent(a, b):
    from scipy.spatial import cKDTree
    va, vb = vertices(a["canonical"]), vertices(b["canonical"])
    ma, mb = np.asarray(a["matrix"]), np.asarray(b["matrix"])
    wa, wb = va @ ma[:3, :3].T+ma[:3, 3], vb @ mb[:3, :3].T+mb[:3, 3]
    if not np.allclose(wa.min(0), wb.min(0), atol=.02) or not np.allclose(wa.max(0), wb.max(0), atol=.02):
        return False
    return bool(max(cKDTree(wa).query(wb)[0].max(), cKDTree(wb).query(wa)[0].max()) < .025)


def aggregate():
    from static_bench import aggregate as aggregate_static
    return aggregate_static()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", action="append")
    parser.add_argument("--aggregate", action="store_true")
    parser.add_argument("--force", action="store_true")
    parser.add_argument("--shard", help="Zero-based shard INDEX/COUNT")
    parser.add_argument("--no-aggregate", action="store_true")
    parser.add_argument("--repair-rounded", action="store_true",
                        help="Declare a connector-reconstructed target for rounded source transforms")
    parser.add_argument("--projection-only", action="store_true",
                        help="Normalize near-rigid source rotations without connector position reconstruction")
    parser.add_argument("--correction-limit", type=float, default=.25,
                        help="Maximum declared source reconstruction vertex displacement in LDU")
    args = parser.parse_args()
    OUT.mkdir(parents=True, exist_ok=True)
    if args.aggregate:
        aggregate()
        return
    models = args.model or [p.parent.name for p in sorted((ROOT / "web/public/models").glob("*/manifest.json"))]
    if args.shard:
        index, count = map(int, args.shard.split("/"))
        models = models[index::count]
    for model in models:
        target = OUT / "models" / model / "record.json"
        if target.exists() and not args.force:
            print("EXISTS", model, flush=True)
            continue
        try:
            row = generate_model(model, repair_rounded="projection" if args.projection_only else args.repair_rounded,
                                 correction_limit=args.correction_limit)
            print("READY", model, row["caseCount"], row["kinds"], flush=True)
        except Exception as exc:
            import traceback
            traceback.print_exc()
            m = json.loads((ROOT / "web/public/models" / model / "manifest.json").read_text())
            dump(target, dict(modelId=model, title=m["model"]["title"], status="excluded",
                              originalParts=len(m["instances"]), caseCount=0, reason=str(exc)))
            print("EXCLUDED", model, str(exc), flush=True)
    if not args.no_aggregate:
        aggregate()


if __name__ == "__main__":
    main()
