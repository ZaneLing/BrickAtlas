"""Flatten the locked LDraw sources for browser display, preserving part geometry."""
from __future__ import annotations

from collections import defaultdict
from functools import lru_cache
import hashlib
import json
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
LIBRARY = HERE.parents[1] / "assets-source/ldraw-library/locked"


def resolve(name):
    name = name.lower().replace("\\", "/")
    if ".." in Path(name).parts or Path(name).is_absolute():
        raise ValueError("Invalid LDraw reference")
    for root in (LIBRARY / "parts", LIBRARY / "p", LIBRARY):
        path = root / name
        if path.is_file():
            return path
    raise FileNotFoundError(name)


@lru_cache(maxsize=None)
def triangles(name, ancestry=()):
    if name in ancestry or len(ancestry) > 40:
        raise ValueError("Cyclic LDraw references")
    path = resolve(name)
    groups = defaultdict(list)
    sources = {str(path.relative_to(LIBRARY)): hashlib.sha256(path.read_bytes()).hexdigest()}
    for line in path.read_text(errors="strict").splitlines():
        fields = line.strip().split()
        if not fields or fields[0] not in ("1", "3", "4"):
            continue
        kind, color = fields[:2]
        if kind == "1":
            values = list(map(float, fields[2:14]))
            mat = np.eye(4)
            mat[:3, 3], mat[:3, :3] = values[:3], np.asarray(values[3:]).reshape(3, 3)
            child, hashes = triangles(" ".join(fields[14:]).replace("\\", "/").lower(), (*ancestry, name))
            sources.update(hashes)
            for child_color, vertices in child.items():
                pts = np.asarray(vertices).reshape(-1, 3) @ mat[:3, :3].T + mat[:3, 3]
                groups[color if child_color == "16" else child_color].extend(pts.ravel().tolist())
        else:
            coords = np.asarray(list(map(float, fields[2:]))).reshape(-1, 3)
            for indices in ((0, 1, 2),) if kind == "3" else ((0, 1, 2), (0, 2, 3)):
                groups[color].extend(coords[list(indices)].ravel().tolist())
    return dict(groups), sources


def main():
    stems = set()
    for geometry in (HERE / "data").glob("*/geometry.json"):
        stems.update(p["partNumber"] for p in json.loads(geometry.read_text())["parts"])
    meshes, hashes = {}, {}
    for stem in sorted(stems):
        groups, sources = triangles(stem + ".dat")
        if not groups:
            raise ValueError(f"No source triangles for {stem}")
        meshes[stem] = {c: [round(v, 6) for v in vertices] for c, vertices in groups.items()}
        hashes.update(sources)
    out = HERE / "arena"
    out.mkdir(exist_ok=True)
    (out / "meshes.json").write_text(json.dumps({"schema": "brickplan-display/1.0", "meshes": meshes},
                                               separators=(",", ":")))
    (HERE / "data/render-provenance.json").write_text(json.dumps({
        "source": "Original locked LDraw recursive triangles; no substitute box meshes.",
        "parts": len(stems), "files": hashes,
        "triangles": sum(len(v) // 9 for g in meshes.values() for v in g.values()),
        "assetSha256": hashlib.sha256((out / "meshes.json").read_bytes()).hexdigest(),
    }, indent=2, sort_keys=True) + "\n")
    notices = {}
    for relative in sorted(hashes):
        lines = (LIBRARY / relative).read_text().splitlines()
        notices[relative] = [line for line in lines
                             if line.startswith(("0 Author:", "0 !LICENSE"))]
        if not any("!LICENSE" in line for line in notices[relative]):
            raise ValueError(f"Missing source license: {relative}")
    models = []
    for source in sorted((HERE / "data").glob("*/source.json")):
        model = json.loads(source.read_text())["provenance"]["sourceModel"]
        models.append({key: model[key] for key in ("id", "title", "author", "license", "sourceUrl")})
    (HERE / "ASSET-LICENSES.json").write_text(json.dumps({
        "derivation": "Original LDraw triangles flattened for display; source geometry unchanged.",
        "partLicenseUrl": "https://creativecommons.org/licenses/by/4.0/",
        "modelLicenseUrl": "https://creativecommons.org/licenses/by/2.0/",
        "models": models, "sourceNotices": notices,
    }, indent=2, sort_keys=True) + "\n")
    print(f"Rendered {len(stems)} original parts from {len(hashes)} locked source files.")


if __name__ == "__main__":
    main()
