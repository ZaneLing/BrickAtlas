# Reproducing the current paper (29 October 2026)

## Compile the checked release

```bash
benchmark/.runtime/mlx-env/bin/python paper/brickplan-cvpr/build.py
```

The build requires Tectonic, PyMuPDF, Pillow, and the current checked dataset. It regenerates release-derived counts and unmeasured table schemas, compiles both PDFs, verifies dependencies/layout/fonts/images, and creates the portable Overleaf ZIP. Formal measurements belong in separate run artifacts; the paper templates are intentionally null.

## Refresh publication figures

```bash
benchmark/.runtime/mlx-env/bin/python paper/brickplan-cvpr/build.py --refresh-figures
```

1. `release_tables.py` reads only `deliverables/brick-atlas-dataset-v1/` and writes current counts, a complete object inventory, and thirty-two unmeasured result sheets.
2. `release_assets.py --scenes` loads selected admitted cases through the real session adapter, replays reference actions, and exports exact geometry and state hashes.
3. `arena_assets.py` verifies four archived v2 API traces and legal GT continuations. `render_publication.mjs --release` renders 36 current-release states; `--arena` renders 40 archived states at 3200 × 2400 with Three.js and headless Chrome. This is publication-only lighting; model observations remain unchanged.
4. `release_figures.py` composes twelve explanatory figures (including an additional wide I/O illustration for Markdown) and eight complete-inventory panels. All figure labels use embedded Comic Sans MS; SVG labels are paths.
5. `verify.py` checks the current release, selected IDs, source hashes, blank results, native image dimensions, embedded fonts, minimum effective image resolution, citations, and the requested ten-page draft body.

Rendering requires the existing project geometry environment: NumPy, MeshLib, the connector/collision resources, pinned LDraw definitions, source certificates, Node 22+, Playwright/Chrome, Three.js, Matplotlib, and both Comic Sans MS faces. No font files or private runtime binaries are redistributed in the ZIP.

## Standalone LaTeX

The ZIP includes main/supplement TeX, their referenced figures, table sources, bibliography, and the recorded official CVPR style. Select `main.tex` or `supplement.tex` in Overleaf. The current draft deliberately has ten body pages; this is not a submission-length compliance claim. No geometry engine or model API is needed to compile those included assets.

The style files are unchanged from the repository's recorded CVPR 2026 source. The 2027 venue label and Draft ID remain provisional. The published 2027 rules require an eight-page main paper and a separate LLM Usage Statement; template migration and submission-length editing remain pending.

## Historical scripts

`update_current.py`, `make_current_tables.py`, `publication_scenes.py`, `design_figures.py`, and `protocol_study.py` describe earlier snapshots. They are retained for provenance, are not invoked by the current build, and must not overwrite present evidence. `--study` now refuses to imply that the historical route study is a current release audit. Current checks live in `scaling_release` and `bench_design.test_metrics`.

`publication_plate.py` exports the same white studded plate patch used by the Arena sensor, preserving its grid, board transform, stud radius and height. It changes only publication geometry. Archived inputs remain byte-identical; the two actual RGB images in the supplement are not relit or enlarged.

`pilot_analysis.py` re-audits all 19 archived provider attempts, keeps service failures separate, and exports the 15 latest-condition ledger and descriptive error counts. It makes no provider calls. `MODEL-ERRORS-AND-MODALITIES.zh-CN.md` contains the normal-run decision ledger and the proposed T/I/TI study contract; strict modality adapters remain pending.

## Standalone capability dossier

`CAPABILITY-ATLAS-AND-REVIEW.zh-CN.md` links the six-case visual dossier and its internal readiness review. It combines explicitly labeled historical v2 runs, one current static run interrupted by a billing receipt error, and two reference-only tasks. These are not a current-release aggregate score.

```bash
PYTHONPATH=benchmark/brickplan-repair benchmark/.runtime/mlx-env/bin/python paper/brickplan-cvpr/capability_assets.py
.tools/node-v22.23.2-darwin-arm64/bin/node paper/brickplan-cvpr/render_publication.mjs --capability
benchmark/.runtime/mlx-env/bin/python paper/brickplan-cvpr/capability_atlas.py
PYTHONPATH=benchmark/brickplan-repair benchmark/.runtime/mlx-env/bin/python paper/brickplan-cvpr/verify_capability_atlas.py
```

These commands make no model API calls. `capability_pilot.py` is a separate paid runner, refuses to overwrite its existing report, and uses the existing capped ledger. The new run's confirmed charge and unresolved reservation are recorded separately; an unavailable receipt is neither zero cost nor a model failure.
