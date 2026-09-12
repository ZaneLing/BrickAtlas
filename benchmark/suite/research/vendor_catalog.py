"""Import the MIT-licensed bundled BrickNet catalog, not its gated model dataset."""
import hashlib
import json
import lzma
from pathlib import Path
import urllib.request

ROOT = Path(__file__).resolve().parents[2]
REVISION = "b09a689c4929bd27f59c9bb9446237967aa332c9"
BASE = f"https://raw.githubusercontent.com/kulits/BrickNet/{REVISION}/"
FILES = ["LICENSE", "DATA.md", "src/bricknet/_data/v1/labels.json.xz",
         "src/bricknet/_data/v1/part_names.json", "src/bricknet/_data/v1/part_aliases.json.xz"]


def main():
    vendor = ROOT / ".runtime/vendor/bricknet"
    vendor.mkdir(parents=True, exist_ok=True)
    hashes = {}
    for name in FILES:
        target = vendor / Path(name).name
        if not target.exists():
            request = urllib.request.Request(BASE + name, headers={"User-Agent": "BrickAtlas-research-catalog"})
            with urllib.request.urlopen(request, timeout=60) as response:
                payload = response.read()
            target.write_bytes(payload)
        hashes[name] = hashlib.sha256(target.read_bytes()).hexdigest()
    license_text = (vendor / "LICENSE").read_text()
    if "MIT License" not in license_text or "Peter Kulits" not in license_text:
        raise RuntimeError("Unexpected upstream license")
    names = json.loads((vendor / "part_names.json").read_text())
    labels = json.loads(lzma.decompress((vendor / "labels.json.xz").read_bytes()))
    aliases = json.loads(lzma.decompress((vendor / "part_aliases.json.xz").read_bytes()))
    (vendor / "normalized-aliases.json").write_text(json.dumps(aliases, separators=(",", ":")))
    kinds, subtypes = {}, {}
    connectors = {}
    rejected = []
    import math
    for part, annotations in labels.items():
        entries = []
        for kind in sorted(annotations):
            for subtype in sorted(annotations[kind]):
                values = annotations[kind][subtype]
                polarities = values if isinstance(values, dict) else {"neutral": values}
                for polarity in sorted(polarities):
                    for row in polarities[polarity]:
                        expected_lengths = (3,) if kind == "ball" else (6,) if kind in ("axle", "fixed", "hinge") else (5,)
                        if len(row) not in expected_lengths or not all(isinstance(x, (int, float)) and math.isfinite(x) for x in row):
                            rejected.append({"part": part, "kind": kind, "subtype": subtype})
                            continue
                        entry = {"id": len(entries), "kind": kind, "subtype": subtype,
                                 "polarity": polarity, "positionLdu": row[:3],
                                 "pitchDeg": row[3] if len(row) >= 5 else None,
                                 "rollDeg": row[4] if len(row) >= 5 else None}
                        if len(row) == 6:
                            entry["yawDeg" if kind == "fixed" else "spanLdu" if kind == "axle" else "reservedColumn"] = row[5]
                        entries.append(entry)
                        kinds[kind] = kinds.get(kind, 0) + 1
                        subtypes[f"{kind}/{subtype}/{polarity}"] = subtypes.get(f"{kind}/{subtype}/{polarity}", 0) + 1
        connectors[part] = entries
    result = {"schema": "bricknet-catalog-import-v1", "source": "https://github.com/kulits/BrickNet",
              "revision": REVISION, "license": "MIT", "copyright": "Copyright (c) 2026 Peter Kulits",
              "fileHashes": hashes, "namedParts": len(names), "annotatedParts": len(connectors),
              "connectorCounts": kinds, "subtypeCounts": subtypes, "rejectedRows": rejected,
              "gatedModelDatasetDownloaded": False,
              "verification": "Structural schema validation only; not independently validated mating/collision geometry",
              "notes": "This is upstream annotated data, not original BrickAtlas annotation. Main grid suite still uses its declared grid catalog."}
    (vendor / "normalized-connectors.json").write_text(json.dumps(connectors, separators=(",", ":")))
    result["normalizedSha256"] = hashlib.sha256((vendor / "normalized-connectors.json").read_bytes()).hexdigest()
    output = ROOT / "suite/artifacts/research"
    output.mkdir(parents=True, exist_ok=True)
    (output / "connector-import.json").write_text(json.dumps(result, indent=2) + "\n")
    (output / "BRICKNET_LICENSE.txt").write_text(license_text)
    print(json.dumps({key: result[key] for key in ("revision", "namedParts", "annotatedParts", "connectorCounts",
                                                 "rejectedRows", "gatedModelDatasetDownloaded")}, indent=2))


if __name__ == "__main__":
    main()
