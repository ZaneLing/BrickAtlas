# Brick Atlas

Brick Atlas is an unofficial desktop workspace for exploring and building traceable LDraw models. It provides per-brick inspection, animated building steps, exploded views, high-resolution rendering, and printable PDF build guides.

## Run Locally

Node.js 22.23.2 is bundled for macOS development:

```bash
export PATH="$PWD/.tools/node-v22.23.2-darwin-arm64/bin:$PATH"
npm ci
npm run dev
```

The default URL is `http://127.0.0.1:5173`. You can also double-click `Start.command` or run `npm run start:local`.

The application must be served through HTTP or HTTPS. It does not require a backend, database, API key, or third-party CDN at runtime.

## Routes

- `/` animated model store, floating brick hero, and auto-looping live 3D build/explode story
- `/explore/:modelId` model explorer
- `/build/:modelId` animated build mode and printable guide
- `/create` local image-to-brick studio and LDraw preflight

## Capabilities

- Deterministic `brick_000001` identities for every physical brick instance.
- A standalone `BrickModel` domain layer containing part ID, transform, color, dimensions, source path, and assembly ownership.
- A persisted Zustand viewer store for selection, visibility, isolation, explosion, X-Ray, quality, and build progress.
- Orbit controls, zoom, five preset views, auto rotation, exploded structure, and per-instance inventory layout.
- Part search, direct selection, hide, isolate, Where Used, dimensions, subassemblies, and source traceability.
- Animated build steps with playback, pause, previous/next navigation, focused looping step previews, and per-step parts lists.
- Editorial instructions build independent subassemblies separately and add explicit final-placement steps for scene models.
- Landscape A4 PDF build-guide export with cover, step number, required parts, quantities, rendered assembly view, and provenance disclosure.
- Independent Full HD, 4K, 8K, and 12K image export.
- Physically based plastic materials, clearcoat highlights, environment lighting, soft ground shadows, color-aware edges, and up to 4x render density.
- Local image conversion into a color-quantized, layered brick relief with a live 3D preview, build animation, exploded view, BOM CSV, and LDraw export.
- Chinese and English interfaces with a persisted language preference.
- Desktop-only product layout with a minimum 1180 px workspace width.
- Recoverable errors for missing assets, invalid geometry, unavailable WebGL, and lost WebGL contexts.

## Image to Bricks

The Creator route provides a deterministic browser-only pipeline:

1. Resize the image to a configurable stud grid.
2. Estimate and optionally remove the background.
3. Quantize visible pixels to a practical LDraw color palette.
4. Infer a shallow relief from image contrast and luminance.
5. Merge occupied cells into 1x1, 1x2, 1x3, and 1x4 bricks.
6. Generate layer-based build steps, a material list, an interactive 3D model, and export files.

This local mode is a buildable single-view relief, not a claim of recovering hidden geometry from one photograph. A full volumetric product pipeline should use image segmentation followed by a dedicated image-to-3D backend such as [TripoSR](https://github.com/VAST-AI-Research/TripoSR) or [Hunyuan3D 2.1](https://github.com/Tencent-Hunyuan/Hunyuan3D-2.1), then voxelize the watertight mesh, pack voxels into supported brick sizes, and validate support and connectivity before generating instructions. BrickLink Studio follows the same practical separation: images become mosaics, while OBJ/STL meshes become 3D sculptures.

See [Image-to-Bricks Pipeline](docs/IMAGE_TO_BRICKS.md) for the implementation boundary, research references, and recommended volumetric service contract.

## Model Catalog

The catalog contains 12 traceable OMR projects with 2,972 brick instances, including:

- 5867 Super Speedster
- 31027 Blue Racer and Kart
- 31028 Sea Plane and Sailboat
- 31009 Small Cottage
- 10014 Caboose
- 10156 LEGO Truck
- 10001 Metroliner
- 10128 Train Level Crossing
- 10036 Pizza To Go
- 10159 City Airport

Models with author-provided `STEP` metadata preserve that sequence. Models without `STEP` metadata are explicitly labeled as editorial structural walkthroughs and are not presented as official LEGO instructions.

## Model and License Policy

Models come from the [LDraw Official Model Repository](https://library.ldraw.org/omr/sets). Each model source, author, license, download URL, and SHA-256 hash is recorded in `atlas.config.ts` and in its published `provenance.json`.

The LDraw parts library is pinned to a verified snapshot. Per-file authorship and license headers are retained. Code is MIT licensed; model and parts licenses remain separate.

Brick Atlas is an unofficial community project and is not affiliated with, sponsored, or endorsed by the LEGO Group. LEGO is a trademark of the LEGO Group.

## Asset Pipeline

```bash
npm run acquire
npm run assets:build
npm run assets:validate
npm run assets:reference
npm run assets:repro
```

The pipeline verifies source hashes, computes the licensed dependency closure, preserves source lines and transforms, assigns stable identities, builds instruction coverage, batches geometry, and writes checksummed gzip chunks under `public/models/<modelId>/`.

Unknown licenses, missing parts, circular references, malformed transforms, unsupported TEXMAP content, incomplete instruction coverage, and identity mismatches stop the build.

## Verification

```bash
npm run check
npm run test:e2e
npm run benchmark
npm audit --omit=dev
```

The suite covers source and geometry integrity, unit behavior, desktop Chrome, Firefox, WebKit, keyboard accessibility, error recovery, every-instance picking, build animation, PDF export, and nonblank canvas pixel checks.

## Project Structure

```text
atlas.config.ts                  Model catalog and immutable source metadata
assets-source/                   Original MPDs, licenses, hashes, and locked dependencies
assets-built/                    Build, reference, reproducibility, and test reports
public/models/<modelId>/         Deployable manifests, geometry chunks, previews, and credits
scripts/                         Acquisition, build, validation, and benchmark pipeline
src/app/                         Pages, localization, UI state integration, and diagnostics
src/creator/                     Image sampling, color quantization, brick packing, BOM, and studio UI
src/model/                       BrickModel and semantic types
src/store/                       Persisted viewer state
src/scene/                       Three.js rendering, picking, and part preview
src/instructions/                Step aggregation and PDF guide generation
tests/                           Unit, browser, accessibility, and visual checks
```
