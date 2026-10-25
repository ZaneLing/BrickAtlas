# Reproducing the current paper (25 October 2026)

## Compile

The Overleaf ZIP contains main/supplement TeX, unmodified official CVPR style,
BibTeX/style files, 15 referenced figure PDFs, current static/dynamic inventories,
and result-table sources. Select `main.tex` or `supplement.tex`. No geometry
engine or model API is needed for standalone LaTeX compilation.

Repository build:

```bash
benchmark/.runtime/mlx-env/bin/python paper/brickplan-cvpr/build.py
```

Tectonic and `requirements-paper.txt` are required. The normal repository build
also verifies current organized dataset/code hashes, recorded replay evidence,
empty results, source splits, historical diagnostics, and PDF layout/fonts/images.
`--skip-verification` compiles without this evidence check.

## Current asset generation

```bash
PYTHONPATH=benchmark/brickplan-repair benchmark/.runtime/mlx-env/bin/python paper/brickplan-cvpr/build.py --refresh-figures
```

`update_current.py` reads the organized catalogue, renders native new scenes,
relabels retained galleries, and writes current inventories and dataset evidence.
`make_current_tables.py` writes 19 unmeasured result panels and candidate task
assignments. It resets only the paper's unmeasured template; save collected
results in separate run artifacts.

Next, `publication_scenes.py` exports the certified scene geometry and states,
`render_publication.mjs` renders 152 publication scenes, and `design_figures.py`
composes 14 annotated publication figures. The fifteenth referenced figure is
the native catalogue-distribution chart retained in the supplement. Publication
rendering dependencies and the distinction from benchmark inputs are below.

Native rendering also needs the project's BrickNet/connector and collision
resources, MeshLib, NumPy/Pillow/Matplotlib, pinned LDraw library, source models,
certificates, and the locally compiled rasterizer. The project Python environment
and `benchmark/.runtime/bricknet-data/inset` supply these resources locally.
Third-party runtime binaries are not redistributed by the paper ZIP.
`evidence/runtime-snapshot.json` is historical environment provenance; newly added
assets and dependencies are pinned by `evidence/current-dataset.json` and the
organized dataset data/code manifests.

## Historical diagnostic reproduction

```bash
PYTHONPATH=benchmark/brickplan-repair benchmark/.runtime/mlx-env/bin/python paper/brickplan-cvpr/protocol_study.py
```

This replays the original twelve modules, two routes, and four conditions (96
scripted trials). It was rechecked on 25 October; 9/36 versus 36/36 remains a
protocol diagnostic, not a learned-model result. Current verify checks the
recorded 5,922-condition replay audit rather than rerunning all physics on every
compile. Metric regression tests are in `bench_design.test_metrics`.

`prepare_revision.py`, `expand_experiments.py`, `build_figures.py`, and the old
experiment/results/budget manifests describe earlier snapshots. They are retained
for history and are no longer invoked by `build.py --refresh-figures`. Do not use
them to overwrite current plans. The old qualitative comparison reads the bundled
sanitized replay export; raw provider responses and identified human records are
not redistributed. No paper build script calls a model API.

## Unfinished empirical components

Candidate model IDs remain a roster rather than verified availability. Exact
API/checkpoint revisions, vision support, image processing, account access, and
costs must be checked before a run. Current-interface human qualification,
paired API execution/logging, source bootstrap, C/detection banks, and alternative
state/coordinate adapters remain outstanding; the paper explicitly labels them.

## Publication rendering revision

Current figures use `publication_scenes.py`, `render_publication.mjs`, and
`design_figures.py`. The first exports certified triangles/states; the second
renders with Three.js 0.180.0 and headless Chrome through local Playwright; the
third composes native scenes and vector annotations. Node 22+ and the repository's
Three.js/Playwright dependencies are needed only to regenerate publication scenes.
The default Chrome executable is the installed macOS Google Chrome. Native exports
and the portable ZIP compile without Node or Chrome.

Scene PNG caches bind the state, geometry, shared frame and rendering policy.
`BRICKPLAN_FORCE_RENDER=1` forces repainting. Publication framing/materials do not
change the benchmark observation adapter. Sidecars and the publication manifest
record source and output hashes. The current viewports preserve shared comparison
scale while trimming canvas whitespace; thickness/pose detail views are disclosed.
