# BrickAtlas OMR Whole-Model Cases v1

This is the primary object-source registry for new BrickAtlas benchmark work.
It replaces random-growth structures as the source of publication-facing
examples and future visual/semantic tasks.

## Contents

- [All 15 complete models](ALL_MODELS.png)
- 15 complete OMR/LDraw models already shipped by the BrickAtlas web app.
- 39 source-named semantic subassemblies.
- 54 case records grouped into 15 source files and 13 set families.
- 9,935 placed instances, 624 unique part numbers, and 42 colors.
- Complete models range from 36 to 4,281 placed instances.
- 1,752 stored construction steps: seven models use source STEP metadata;
  eight use explicitly labeled editorial demonstrations.

## Quality Rules

Whole-model cases must:

1. Preserve the complete licensed source MPD and dependency closure.
2. Have an explicit author, source URL, license, source hash, and preview.
3. Remain recognizable as a complete object or scene.
4. Retain original part identities, colors, transforms, and hierarchy.

Semantic subassembly cases must:

1. Be explicitly named in the source hierarchy.
2. Include the complete descendant closure of that source submodel.
3. Contain at least six placed instances.
4. Exclude random crops, `stepXX` fragments, minifig-only cases, lamps,
   cones, and unnamed numerical fragments.
5. Keep all cases from one model in the same statistical source group.

## Status of the Old Procedural Layer

The 5,120 random-growth structures and their 117,910 derived conditions are
retained only for historical mechanism regression and scorer tests. They are
not part of this primary case registry, must not appear in publication-facing
dataset galleries, and must not be counted as current benchmark object scale.

## Files

- `manifest.json`: complete whole-model and semantic-subassembly records.
- `summary.json`: release counts.
- `ATTRIBUTION.md`: per-model author, license, and source.
- `release-manifest.json`: release and upstream manifest hashes.
