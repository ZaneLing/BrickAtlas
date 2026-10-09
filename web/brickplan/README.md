# BrickPlan workbench

React 19, TypeScript, Vite, Radix Dialog/Tabs and CSS Modules. Three.js uses
WebGL 2. No full UI component library or experimental renderer is required.

```sh
cd web/brickplan
npm ci
npm run build
npm run dev
```

The production build lives in `benchmark/brickplan-v2.2/arena/app/`.
Start the Python server as documented in the benchmark README. Restart it
after rebuilding: the HTTP asset allowlist is captured at server startup.
Vite development runs on port 5174 and proxies the Python API on port 8792.
Start the current server with `--port 8792`; older 8769/8780 services remain separate.

`App`, `Library`, `Workcell` and `ModelPanel` manage navigation, contracts,
explicit actions and durable observations. `Visuals` hosts the renderer.
`BrickSceneController` owns cameras, picking, transforms, hover details, GPU
resources and on-demand animation; pointer movement and rendering do not
update React state every frame. Disposal releases listeners and GPU buffers.
Scene meshes and transforms come directly from the benchmark's LDraw assets.
Exploded inspection is explicitly marked as a diagram.
Part/site labels do not cover the assembly. Hover reveals one piece's ID,
registered site and LDraw part number; touch users tap to inspect. Dragging
or leaving the canvas dismisses the mouse tooltip. Keyboard users can focus
the canvas, use left/right to inspect, Enter to select and Escape to dismiss.

Immutable previews and scene requests are deduplicated in a bounded browser
cache. The two main PNGs preload while the 3D view is visible; auxiliary sheets
load lazily. The backend reuses encoded rasters across matching states and
identity mappings, and aggregates labelled pixels in one pass. Supersampling,
PNG encoding and native resolution remain unchanged. Cold practice preview
rendering no longer blocks scene or authoritative session requests.

Practice permits free 3D inspection. Static `image-id` probes provide
isometric, left, rear and right views at revision zero without acquisition
cost. Switching these views does not disable answer submission; repair
checkpoints expose the matching supplied view. `image-id-active` probes
start isometric and charge one view-budget unit per acquisition.
The condition is fixed by the server run configuration, not a client toggle;
`structured` remains the third supported condition.
Controlled study mode serves only native images; scene, catalogue,
download and model-demo routes are denied. Model calls continue using
public raster observations and the authoritative JSON action protocol.
Remote provider credentials are configured in the Python environment only.

The static site uses this same build with a `brickplan-mode=static` meta
tag and a relative-URL data adapter. Seven category samples are rotatable,
the archived model case is replayable, and question counts are read from
the current catalogue. The case preserves historical 2.1 task, response and
image bytes and is not a new 2.2 model measurement. Static media URLs are
resolved in the frontend without rewriting the archived trace.
Human submissions and live inference require the Python runtime.
The release exporter also supplies a portable runtime and an independent
Overleaf ZIP; no `node_modules`, model weights or secrets are bundled.

The v2.2 integration checks live in `web/brickplan/tests/`.
They exercise actual visible controls and separately label software fixtures
and integration calls; these are not human or population-model results.

From the repository root, generate public records without rendering or PDFs:

```sh
python benchmark/brickplan-v2.2/package_release.py questions
```

For full frontend acceptance, build the app, run `package_release.py export`,
then `python web/brickplan/tests/verify_v22.py`. The test uses port 8792 plus
ephemeral loopback ports for isolated active/study/static conditions and
shuts them down afterward. Evidence and screenshots are written under
`tem/research/20261009-brickplan-v22-revision/frontend/`.
Final PDF, Overleaf and runtime archive verification follows manuscript
publication; this frontend test does not run new inference or freeze a release.
