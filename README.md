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

- `/` animated model store and project overview
- `/explore/:modelId` model explorer
- `/build/:modelId` animated build mode and printable guide
- `/create` local LDraw preflight

## Capabilities

- Deterministic `brick_000001` identities for every physical brick instance.
- A standalone `BrickModel` domain layer containing part ID, transform, color, dimensions, source path, and assembly ownership.
- A persisted Zustand viewer store for selection, visibility, isolation, explosion, X-Ray, quality, and build progress.
- Orbit controls, zoom, five preset views, auto rotation, exploded structure, and per-instance inventory layout.
- Part search, direct selection, hide, isolate, Where Used, dimensions, subassemblies, and source traceability.
- Animated build steps with playback, pause, previous/next navigation, static step views, and per-step parts lists.
- Landscape A4 PDF build-guide export with cover, step number, required parts, quantities, rendered assembly view, and provenance disclosure.
- Independent Full HD, 4K, 8K, and 12K image export.
- Physically based plastic materials, clearcoat highlights, environment lighting, soft ground shadows, and up to 4x render density.
- Chinese and English interfaces with a persisted language preference.
- Desktop-only product layout with a minimum 1180 px workspace width.
- Recoverable errors for missing assets, invalid geometry, unavailable WebGL, and lost WebGL contexts.

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
src/model/                       BrickModel and semantic types
src/store/                       Persisted viewer state
src/scene/                       Three.js rendering, picking, and part preview
src/instructions/                Step aggregation and PDF guide generation
tests/                           Unit, browser, accessibility, and visual checks
```
