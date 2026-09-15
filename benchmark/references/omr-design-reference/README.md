# OMR/LDraw Design Reference

These licensed models are visual-complexity and hierarchy references only.
They are not BrickAtlas benchmark cases, are not included in benchmark sample
counts, and are not used as test answers or model inputs.

## Contents

- [All 15 complete models](ALL_MODELS.png)
- 15 complete OMR/LDraw models already shipped by the BrickAtlas web app.
- 39 source-named semantic subassemblies inspected as design references.
- 15 source files grouped into 13 set families.
- 9,935 placed instances, 624 unique part numbers, and 42 colors.
- Complete models range from 36 to 4,281 placed instances.
- 1,752 stored construction steps: seven models use source STEP metadata;
  eight use explicitly labeled editorial demonstrations.

## Reference Rules

Reference models preserve:

1. Preserve the complete licensed source MPD and dependency closure.
2. Have an explicit author, source URL, license, source hash, and preview.
3. Remain recognizable as a complete object or scene.
4. Retain original part identities, colors, transforms, and hierarchy.

Reference subassemblies are inspected only to learn what coherent functional
modules look like. They:

1. Be explicitly named in the source hierarchy.
2. Include the complete descendant closure of that source submodel.
3. Contain at least six placed instances.
4. Exclude random crops, `stepXX` fragments, minifig-only cases, lamps,
   cones, and unnamed numerical fragments.
5. Never enter a benchmark split or statistical source count.

## Status of the Old Procedural Layer

The 5,120 random-growth structures and their 117,910 derived conditions are
also retained only for historical mechanism regression and scorer tests.
Neither the OMR references nor the random-growth archive is a current
Mechanism-1 benchmark case source.

## Files

- `reference-manifest.json`: reference-only model and subassembly metadata.
- `ATTRIBUTION.md`: per-model author, license, and source.
