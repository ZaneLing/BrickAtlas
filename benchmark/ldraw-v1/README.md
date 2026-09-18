# BrickAtlas LDraw-1

Current review release: **24 original OMR sources, 15,334 original part
instances, 617 questions in 11 families**. This replaces the synthetic
Hierarchy-3 active dataset. No historical physical pass or model score
transfers to this version.

Open `/benchmark` for the real-geometry library and `/benchmark/review` for
task review. Each instance has a B0001-style number shared by questions,
numbered screenshots, inventory, exports and scoring. Sources, author
credits and original SHA256 digests are downloadable. Existing human
feedback remains under its original browser-storage namespace.

## Evidence and limitations

- Original geometry, transforms, colors and hierarchy are preserved.
- Independent reparsing verifies all 15,334 retained instances.
- All 617 reference answers pass; 1,606 negative controls are rejected.
- There are 24 set families and no repeated translation-normalized geometry
  fingerprints. Maximum inventory multiset Jaccard is 0.450. Similarity
  screens are not proof of independence.
- Connector catalog coverage is at least 90% per source. Unsupported parts
  remain explicit; coverage does not establish connectedness.
- The audit retains **573 intersection candidates without recognized mating
  pairs**. These require review and are not automatically CAD defects.
- Seventeen sources have usable author STEP metadata. Other sources have
  no generated substitute assembly order.
- No new learned-model inference, physical stability measurement or
  insertion/extraction validation has been performed.

## Artifacts

- `release.json`: actual counts, source locks, exclusions, 276 pairwise screens.
- `sources/`, `configs/`, `acquired.json`: original acquisition and preparation.
- `audits/`: recognized connectors, coverage, components and intersections.
- `dependency-lock.json`, `verification.json`: locked parts and independent checks.
- `capture.json`: complete model loads and four-view/numbered captures.
- `input-renders.json`: numbered image for every visual question.
- `ATTRIBUTION.md`: retained-source authors, licenses, URLs and hashes.
- `PROTOCOL.md`: source, question and reporting rules.
- `../../public/benchmark/ldraw/inputs/`: model-facing JSON and numbered images.
- `../../public/benchmark/ldraw/models/`: review bundles **with answers**.
- `../paper/main.pdf`, `../paper/supplement.pdf`: current English documents.

The public development website is not an answer-secure evaluation server.
For visual evaluation, deliver only the designated question JSON and its
numbered images. The renderer manifest and review bundles contain source
attributes or answers and must not be supplied as image-only observations.

## Reproduction

Node 22 and Python 3.11 are used. From the repository root:

```sh
npm install
# Sources are already retained. Optional acquisition/preparation:
python3 benchmark/suite/ldraw/acquire.py
npx tsx benchmark/suite/ldraw/prepare.ts

# Local connector and inset-mesh audit:
python3 -m pip install bricknet==0.1.0 meshlib==3.1.4.297 numpy==2.4.6 scipy==1.17.1
python3 -m bricknet fetch-meshes
python3 benchmark/suite/ldraw/audit.py

npx tsx benchmark/suite/ldraw/release.ts
npx tsx benchmark/suite/ldraw/verify.ts
npm test
npm run dev
```

With the local site running and Chrome installed, in another terminal:

```sh
npx tsx benchmark/suite/ldraw/capture.ts
npx tsx benchmark/suite/ldraw/capture-inputs.ts
npx tsx benchmark/suite/ldraw/capture-worked.ts
python3 benchmark/suite/ldraw/paper.py
```

Then follow `../paper/BUILD.md`. Browser capture checkpoints resume completed
sources; delete the relevant generated checkpoint if intentionally recapturing
changed rendering code. Capture scripts do not write human review decisions.
