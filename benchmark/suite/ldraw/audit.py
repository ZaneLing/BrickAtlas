"""Connector and inset-mesh evidence over unchanged OMR instances."""
from pathlib import Path
from collections import Counter
import hashlib
import json
import os
import importlib.metadata
import numpy as np
import bricknet
from bricknet.data import load_catalog, load_aliases
from bricknet.graph import parse_ldr
from bricknet.collision import colliding_pairs, data_dir

ROOT = Path(__file__).resolve().parents[3]
DATA = ROOT / "benchmark/ldraw-v1"
(DATA / "audits").mkdir(exist_ok=True)
catalog, aliases = load_catalog(), load_aliases()
rows = []
for file in sorted((DATA / "flat").glob("*.ldr")):
    source_manifest = ROOT / "public/models" / file.stem / "manifest.json"
    digest = hashlib.sha256(source_manifest.read_bytes()).hexdigest()
    output = DATA / "audits" / f"{file.stem}.json"
    if output.exists():
        saved = json.loads(output.read_text())
        if saved.get("manifestSha256") == digest and saved.get("auditVersion") == 2 and saved.get("collisionStatus") == "complete":
            rows.append(saved)
            continue
    manifest = json.loads(source_manifest.read_text())
    lines = file.read_text().splitlines()
    known, unknown, canonical_mats = [], [], []
    for index, line in enumerate(lines):
        t = line.split()
        stem = " ".join(t[14:]).removesuffix(".dat")
        canonical = aliases.get(stem, (stem, None))[0]
        if canonical not in catalog.stem_to_id:
            unknown.append({"instanceId": manifest["instances"][index]["instanceId"], "partNumber": stem})
            continue
        known.append(index)
        values = np.asarray(t[2:14], dtype=float)
        mat = np.eye(4)
        mat[:3,3] = values[:3]
        mat[:3,:3] = values[3:].reshape(3,3)
        if stem in aliases:
            mat = mat @ aliases[stem][1]
        canonical_mats.append(mat)
    try:
        graph = parse_ldr("\n".join(lines[i] for i in known))
        mapped = lambda i: manifest["instances"][known[int(i)]]["instanceId"]
        edges = [{"a": mapped(e["a"]), "b": mapped(e["b"]), "family": str(e["family"]),
                  "aConnector": int(e["a_conn"]), "bConnector": int(e["b_conn"]),
                  "yawOrSlide": float(e["yaw"]), "flip": bool(e["flip"]),
                  "rotation": e["rot"].tolist()} for e in graph.edges]
        components = [[mapped(i) for i in c] for c in graph.components]
        components.extend([[p["instanceId"]] for p in unknown])
        seen = Counter((p["partNumber"], tuple(round(x,6) for x in p["originalMatrix"]))
                       for p in manifest["instances"])
        missing_meshes = sorted({catalog.id_to_stem[pid] for pid in graph.part_ids
                                 if not (data_dir() / "inset" / f"{catalog.id_to_stem[pid]}.ply").exists()})
        pairs = []
        if not missing_meshes:
            # Use original alias-transformed poses, not parse_ldr's SVD-normalized poses.
            pairs = [(mapped(a),mapped(b)) for a,b in colliding_pairs(graph.part_ids, canonical_mats)]
        fixed = {frozenset((e["a"],e["b"])) for e in edges if e["family"] == "fixed"}
        mating = {frozenset((e["a"],e["b"])) for e in edges}
        row = {"id": file.stem, "auditVersion": 2, "manifestSha256": digest, "instances": len(lines),
               "connectorCoverage": len(known)/len(lines), "unsupported": unknown,
               "edges": edges, "byFamily": dict(Counter(e["family"] for e in edges)),
               "components": components, "componentSizes": sorted(map(len,components),reverse=True),
               "duplicatePlacements": sum(n-1 for n in seen.values() if n>1),
               "collisionStatus": "complete" if not missing_meshes else "missing-meshes",
               "missingMeshes": missing_meshes, "collisionPairs": pairs,
               "nonFixedCollisionPairs": [p for p in pairs if frozenset(p) not in fixed],
               "nonMatingCollisionPairs": [p for p in pairs if frozenset(p) not in mating],
               "graphPoseNormalizationMax": float(np.max(np.abs(np.asarray(canonical_mats)-graph.transforms))),
               "sourceGeometryModified": False,
               "engine": f"bricknet-{importlib.metadata.version('bricknet')}",
               "scope": "Upstream connector tolerances and inset mesh intersections; unknown parts remain explicit, separate scene objects are not glued together; no load/force validation."}
        output.write_text(json.dumps(row,indent=2)+"\n")
        rows.append(row)
        print(file.stem, len(lines), "parts", len(edges), "edges", "components",
              row["componentSizes"][:12], "unknown",len(unknown),"collisions",len(row["nonFixedCollisionPairs"]),flush=True)
    except Exception as e:
        print(file.stem, "ERROR", repr(e), flush=True)
        output.write_text(json.dumps({"id":file.stem,"error":str(e),"manifestSha256":digest})+"\n")
(DATA / "audit-summary.json").write_text(json.dumps([{k:v for k,v in r.items()
    if k not in ["edges","components","collisionPairs","nonFixedCollisionPairs"]} for r in rows],indent=2)+"\n")
