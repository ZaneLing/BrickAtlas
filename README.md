<p align="center">
  <img src="docs/media/brick-atlas-mark.svg" width="760" alt="Brick Atlas animated brick mark">
</p>

<h1 align="center">Brick Atlas</h1>

<p align="center">
  An unofficial desktop workspace for exploring LDraw models, inspecting individual bricks, and following animated build instructions.
</p>

<p align="center">
  <strong>English</strong> · <a href="README.zh-CN.md">简体中文</a>
</p>

## Feature Videos

### 1. 3D Explode: 0% to 100% to 0%

https://github.com/user-attachments/assets/77e02f26-285b-4b47-a3f5-080b395bf07f

### 2. Guided Build

https://github.com/user-attachments/assets/8f964a18-3408-4908-aced-dff1d4d4a31e

### 3. Create: Multi-view Image to Bricks

https://github.com/user-attachments/assets/46452ae9-0480-4387-ad05-a8f0d9dddd14

### 4. Free DIY

https://github.com/user-attachments/assets/175498ed-8c62-4598-a748-9ffaaef4f89b

## Features

- Browse 15 traceable models with high-resolution, physically based 3D rendering.
- Rotate, zoom, pan, switch views, auto-rotate, and inspect exploded assemblies.
- Select any brick to view its part number, color, dimensions, subassembly, and 3D shape.
- Search, hide, isolate, highlight matching parts, and use X-Ray mode to inspect internal structure.
- Follow step-by-step assembly in the central 3D canvas. Manually opened guide blocks show clickable parts and one high-resolution start-to-install placement diagram.
- Play the manual assembly game: inspect and orbit real parts, move them with the pointer onto the 3D build, choose their position and quarter-turn, then pass an end-of-step position/orientation audit.
- Compose original scenes from verified aircraft, boats, vehicles, buildings, characters, animals, baseplates, and loose bricks with stud-grid snapping and collision checks.
- Free-build in the DIY studio: choose a shape and color, rotate previews or already placed bricks by 90 degrees, click to snap, and keep stacking on an extending baseplate.
- Export printable PDF build guides, BOM CSV files, LDraw files, and images up to 12K.
- Send one real-object photo to a public TripoSR or Stable Fast 3D endpoint, inspect the returned GLB mesh, then voxelize and pack it into a brick sculpture. A clearly labeled local depth/multi-view fallback remains available.
- Use tactile brick controls with lightweight stud bursts, full-card shatter feedback and color-matched placement effects; reduced-motion preferences disable them.
- Switch the complete interface between Chinese and English.

Desktop browsers retain the three-column workspaces. Phone and tablet layouts place the 3D canvas before the controls and material library.

### Workspace Upgrade

- Opening split-screen build/explode animations, with varied translucent floating bricks behind the page.
- A playable space lobby with model search, category/difficulty filters, favorites, and resume links.
- Persistent Explore display preferences and adjustable Build playback speed.
- Assembly undo-last-placement, restart confirmation, paused guides, and validated progress recovery.
- DIY coordinate editing, validated duplication, and local project snapshots.
- Compose undo/redo, validated JSON import, component search, snapshots, and BOM export.
- Local embedded GLB import in Create, with cancellable reconstruction, resource cleanup, and JSON export.
- Bounded project sizes, protected corrupt saves, and immediate autosave flushing when leaving a page.

See the [module-by-module upgrade report](docs/WORKSPACE_UPGRADE.md) for implementation details, verification, and remaining boundaries.

## Routes

- `/` opening split-screen build/explode animations, playable space lobby, and searchable model catalog
- `/explore/:modelId` model explorer
- `/build/:modelId` build instructions
- `/assemble` difficulty-ranked manual assembly catalog
- `/assemble/:modelId` validated drag-and-drop assembly game
- `/compose` reusable component, baseplate, and loose-part scene composer
- `/diy` direct mouse-driven brick building on an extending stud grid
- `/create` image-to-bricks studio and LDraw file preflight

## Composition

The Compose workspace turns catalog models into reusable components while retaining source attribution. Components snap to a selected baseplate on a stud grid, rotate in 90-degree increments, and are checked for bounds and footprint collisions. Loose bricks can be positioned at custom levels. A composition is saved locally and can be replayed as build steps, exploded in 3D, or exported as project JSON and LDraw.

Catalog components retain their original geometry and transforms. Composition steps currently place whole components; connection strength, stud compatibility and physical buildability are not certified. Procedural character and loose-part previews remain simplified.

Build controls animate only the central model. Guide accordions stay user-controlled and contain clickable parts plus one high-resolution start-to-install diagram. Both information sidebars can collapse to expand the model canvas. See [Build Workspace](docs/BUILD_WORKSPACE.md).

The separate [Assembly Game](docs/ASSEMBLY_GAME.md) starts from zero, validates
part type, color, quantity, and step order, and persists partial or completed
models locally.

## Free DIY

The independent DIY studio provides 78 traceable parts across ten categories, 18 colors and 12 reusable small assemblies. It supports continuous mouse placement, 90-degree rotation, automatic stacking, collision and support checks, painting, removal, undo/redo, local autosave, JSON import/export, BOM CSV, LDraw and PNG export.

The ground follows the camera instead of allocating an enormous board. Projects are currently limited to 5,000 bricks. Support checks prevent floating placements and unsupported deletion, but do not certify physical stability. DIY uses procedural brick geometry; it does not replace the source-model Compose workspace.

## Run Locally

Use Node.js 22 or newer:

```bash
npm ci
npm run dev
```

Open `http://127.0.0.1:5173`. The app runs without a database or private backend. Local tools need no API key. The default public TripoSR CPU endpoint works anonymously; official ZeroGPU providers accept an optional session-only Hugging Face token for additional quota.

On macOS, `Start.command` and `npm run start:local` are also available.

## Image Conversion

The Creator now uses an explicit two-stage workflow by default: a public Hugging Face Space turns the front image into a real GLB triangle mesh, then a Web Worker voxelizes that mesh and packs the occupied volume into supported bricks. The original GLB can be inspected and downloaded before viewing the brick result. Photos are sent to the selected public provider only after the user presses Generate. The local Depth Anything V2 and multi-view silhouette pipeline remains available as an offline fallback and is never labeled as a real mesh reconstruction. See [Image-to-Bricks Pipeline](docs/IMAGE_TO_BRICKS.md) for limitations and implementation details.

## Models and Licenses

Model assets come from the [LDraw Official Model Repository](https://library.ldraw.org/omr/sets). Source, author, license, download URL, and hash records are retained with each model.

Code is MIT licensed. Model and LDraw part licenses remain separate. Brick Atlas is an unofficial community project and is not affiliated with, sponsored, or endorsed by the LEGO Group.

## Verification

```bash
npm run check
npm run test:e2e -- --project=desktop-chrome
npm audit
```

See [Engineering Audit](docs/ENGINEERING_AUDIT.md) for test coverage, measured performance and remaining limitations.
