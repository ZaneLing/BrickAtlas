"""Freeze local audit implementation, catalog and mesh provenance."""
from pathlib import Path
import hashlib
import importlib.metadata
import json
import bricknet
from bricknet.data import load_aliases, load_catalog
from bricknet.collision import data_dir

root = Path(__file__).resolve().parents[3]
package = Path(bricknet.__file__).parent
out = root / "benchmark/ldraw-v1"
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
catalog, aliases = load_catalog(), load_aliases()
stems = set()
for row in json.loads((out / "catalog.json").read_text()):
    manifest = json.loads((root / "public/models" / row["id"] / "manifest.json").read_text())
    for p in manifest["instances"]:
        stem = p["partNumber"]
        canonical = aliases.get(stem, (stem, None))[0]
        if canonical in catalog.stem_to_id:
            stems.add(canonical)
meshes = {s: sha(data_dir() / "inset" / (s + ".ply")) for s in sorted(stems)}
evidence = {
    "packages": {name: importlib.metadata.version(name) for name in ["bricknet", "meshlib", "numpy", "scipy"]},
    "implementation": {p.name: sha(p) for p in package.glob("*.py")},
    "dataFiles": {str(p.relative_to(package)): sha(p) for p in package.rglob("*") if p.is_file() and p.suffix in [".xz", ".json", ".npz"]},
    "usedInsetMeshes": meshes,
    "tolerancesLDU": {"connectorPosition": 3.0, "axisDot": 0.95, "axleAxisDot": 0.9,
      "axlePerpendicular": 2.05, "axleMinimumOverlap": 4.0, "meshInsetPerSurface": 0.25,
      "intersectionPerturbation": 1e-6},
    "limitations": "Mesh audit covers supported types only. Rotation SVD normalization applies to connector inference; intersections and rendering use original source poses.",
}
(out / "tool-evidence.json").write_text(json.dumps(evidence, indent=2)+"\n")
print(len(meshes), "used inset mesh hashes")
