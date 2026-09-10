<p align="center">
  <img src="docs/media/brick-atlas-mark.svg" width="760" alt="Brick Atlas animated brick mark">
</p>

<h1 align="center">Brick Atlas</h1>

<p align="center">
  An unofficial desktop workspace for exploring LDraw models, inspecting individual bricks, and following animated build instructions.
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
- Compose original scenes from verified aircraft, boats, vehicles, buildings, characters, animals, baseplates, and loose bricks with stud-grid snapping and collision checks.
- Free-build in the DIY studio: choose a shape and color, preview it under the mouse, click to snap, and keep stacking on an extending baseplate.
- Export printable PDF build guides, BOM CSV files, LDraw files, and images up to 12K.
- Crop one to three reference views and generate a budget-aware relief, hollow sculpture, or solid brick model with build steps and a material list.
- Use tactile brick controls with lightweight stud bursts, full-card shatter feedback and color-matched placement effects; reduced-motion preferences disable them.
- Switch the complete interface between Chinese and English.

Brick Atlas is designed for desktop browsers with a workspace width of at least 1180 px.

## Routes

- `/` model catalog and automatic 3D feature showcase
- `/explore/:modelId` model explorer
- `/build/:modelId` build instructions
- `/compose` reusable component, baseplate, and loose-part scene composer
- `/diy` direct mouse-driven brick building on an extending stud grid
- `/create` image-to-bricks studio and LDraw file preflight

## Composition

The Compose workspace turns catalog models into reusable components while retaining source attribution. Components snap to a selected baseplate on a stud grid, rotate in 90-degree increments, and are checked for bounds and footprint collisions. Loose bricks can be positioned at custom levels. A composition is saved locally and can be replayed as build steps, exploded in 3D, or exported as project JSON and LDraw.

Catalog components retain their original geometry and transforms. Composition steps currently place whole components; connection strength, stud compatibility and physical buildability are not certified. Procedural character and loose-part previews remain simplified.

Build controls animate only the central model. Guide accordions stay user-controlled and contain clickable parts plus one high-resolution start-to-install diagram. Both information sidebars can collapse to expand the model canvas. See [Build Workspace](docs/BUILD_WORKSPACE.md).

## Free DIY

The independent DIY studio provides 78 traceable parts across ten categories, 18 colors and 12 reusable small assemblies. It supports continuous mouse placement, 90-degree rotation, automatic stacking, collision and support checks, painting, removal, undo/redo, local autosave, JSON import/export, BOM CSV, LDraw and PNG export.

The ground follows the camera instead of allocating an enormous board. Projects are currently limited to 5,000 bricks. Support checks prevent floating placements and unsupported deletion, but do not certify physical stability. DIY uses procedural brick geometry; it does not replace the source-model Compose workspace.

## Run Locally

Use Node.js 22 or newer:

```bash
npm ci
npm run dev
```

Open `http://127.0.0.1:5173`. The app runs locally without a backend, database, or API key.

On macOS, `Start.command` and `npm run start:local` are also available.

## Image Conversion

The Creator supports manual square crops plus front, top, and side silhouette fusion. A single image still produces a relief; additional views can produce a hollow or solid visual hull. Recovering truly hidden geometry still requires a dedicated image-to-3D backend. See [Image-to-Bricks Pipeline](docs/IMAGE_TO_BRICKS.md) for that extended design.

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
