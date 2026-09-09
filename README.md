<p align="center">
  <img src="docs/media/brick-atlas-mark.svg" width="760" alt="Brick Atlas animated brick mark">
</p>

<h1 align="center">Brick Atlas</h1>

<p align="center">
  An unofficial desktop workspace for exploring LDraw models, inspecting individual bricks, and following animated build instructions.
</p>

https://github.com/user-attachments/assets/1761f41d-e016-40c3-85f9-06102f5acc66

## Features

- Browse 15 traceable models with high-resolution, physically based 3D rendering.
- Rotate, zoom, pan, switch views, auto-rotate, and inspect exploded assemblies.
- Select any brick to view its part number, color, dimensions, subassembly, and 3D shape.
- Search, hide, isolate, highlight matching parts, and use X-Ray mode to inspect internal structure.
- Follow step-by-step assembly with playback controls, focused placement animations, parts lists, and subassembly placement.
- Export printable PDF build guides, BOM CSV files, LDraw files, and images up to 12K.
- Crop one to three reference views and generate a budget-aware relief, hollow sculpture, or solid brick model with build steps and a material list.
- Switch the complete interface between Chinese and English.

Brick Atlas is designed for desktop browsers with a workspace width of at least 1180 px.

## Routes

- `/` model catalog and automatic 3D feature showcase
- `/explore/:modelId` model explorer
- `/build/:modelId` build instructions
- `/create` image-to-bricks studio and LDraw file preflight

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
npm run test:e2e
npm audit --omit=dev
```
