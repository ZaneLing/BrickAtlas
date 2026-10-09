# BrickPlan workbench

React 19, TypeScript, Vite, Radix Dialog/Tabs and CSS Modules. Three.js uses
WebGL 2. No full UI component library or experimental renderer is required.

```sh
cd web/brickplan
npm ci
npm run build
npm run dev
```

The production build lives in `benchmark/brickplan-v2.1/arena/app/`.
Start the Python server as documented in the benchmark README. Restart it
after rebuilding: the HTTP asset allowlist is captured at server startup.
Vite development runs on port 5174 and proxies the Python API on port 8769.

`App`, `Library`, `Workcell` and `ModelPanel` manage navigation, contracts,
explicit actions and durable observations. `Visuals` hosts the renderer.
`BrickSceneController` owns cameras, picking, transforms, labels, GPU
resources and on-demand animation; pointer movement and rendering do not
update React state every frame. Disposal releases listeners and GPU buffers.
Scene meshes and transforms come directly from the benchmark's LDraw assets.
Exploded inspection is explicitly marked as a diagram.

Practice permits free 3D inspection. Controlled study mode serves only
native images and the existing acquisition budget; scene, catalogue,
download and model-demo routes are denied. Model calls continue using
public raster observations and the authoritative JSON action protocol.
Remote provider credentials are configured in the Python environment only.

The static site uses this same build with a `brickplan-mode=static` meta
tag and a relative-URL data adapter. Seven category samples are rotatable,
the archived model case is replayable, and all 884 question contracts are
listed. Human submissions and live inference require the Python runtime.
The release exporter also supplies a portable runtime and an independent
Overleaf ZIP; no `node_modules`, model weights or secrets are bundled.

Browser acceptance scripts live in `benchmark/brickplan-v2.1/`.
They exercise actual visible controls and separately label software fixtures
and integration calls; these are not human or population-model results.
