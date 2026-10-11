"""Generate original LDraw observation meshes with locked-source provenance."""
import hashlib
import importlib.util
import json
from pathlib import Path

from bank import task_bank, write_json
from mission import canonical_hash

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location(
    "brickplan_locked_mesh_export", HERE.parent / "brickplan-v1/render_assets.py")
exporter = importlib.util.module_from_spec(spec)
spec.loader.exec_module(exporter)
# The immutable flattener retains its locked library path; only outputs change.
exporter.HERE = HERE


def main():
    bank = task_bank()
    profiles = sorted(p["id"] for p in bank["profiles"])
    stems, models = set(), {}
    for profile in profiles:
        folder = HERE / "data" / profile
        geometry = json.loads((folder / "geometry.json").read_text())
        stems.update(p["partNumber"] for p in geometry["parts"])
        model = json.loads((folder / "source.json").read_text())["provenance"]["sourceModel"]
        record = {key: model[key] for key in ("id", "title", "author", "license", "sourceUrl")}
        assert model["id"] not in models or models[model["id"]] == record
        models[model["id"]] = record
    meshes, hashes = {}, {}
    for stem in sorted(stems):
        groups, sources = exporter.triangles(stem + ".dat")
        if not groups:
            raise ValueError(f"No original source triangles for {stem}")
        meshes[stem] = {color: [round(v, 6) for v in vertices] for color, vertices in groups.items()}
        hashes.update(sources)
    out = HERE / "arena/meshes.json"
    out.parent.mkdir(exist_ok=True)
    out.write_text(json.dumps({"schema": "brickplan-display/1.0", "meshes": meshes},
                             separators=(",", ":")))
    write_json(HERE / "data/render-provenance.json", {
        "source": "Original locked LDraw recursive triangles; no substitute box meshes.",
        "bankHash": canonical_hash(bank), "profiles": profiles, "parts": len(stems),
        "files": hashes, "triangles": sum(len(v) // 9 for g in meshes.values() for v in g.values()),
        "assetSha256": hashlib.sha256(out.read_bytes()).hexdigest(),
        "selection": "Declared final-bank profiles only; excluded and incomplete construction folders are not inputs.",
    })
    notices = {}
    for relative in sorted(hashes):
        lines = (exporter.LIBRARY / relative).read_text().splitlines()
        notices[relative] = [line for line in lines if line.startswith(("0 Author:", "0 !LICENSE"))]
        assert any("!LICENSE" in line for line in notices[relative]), relative
    write_json(HERE / "ASSET-LICENSES.json", {
        "derivation": "Original LDraw triangles flattened for display; source geometry unchanged.",
        "partLicenseUrl": "https://creativecommons.org/licenses/by/4.0/",
        "modelLicenseUrl": "https://creativecommons.org/licenses/by/2.0/",
        "models": [models[key] for key in sorted(models)], "sourceNotices": notices,
    })
    print(f"Rendered {len(stems)} original parts for {len(profiles)} final-bank profiles.")


if __name__ == "__main__":
    main()
