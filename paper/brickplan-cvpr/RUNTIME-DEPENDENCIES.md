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

1. `release_tables.py` reads only `deliverables/brick-atlas-dataset-v1/` and writes current counts, a complete object inventory, and thirty unmeasured result sheets.
2. `release_assets.py --scenes` loads selected admitted cases through the real session adapter, replays reference actions, and exports exact geometry and state hashes.
3. `arena_assets.py` verifies two archived v2 API traces and legal GT continuations. `render_publication.mjs --release` renders 36 current-release states; `--arena` renders 24 archived states at 3200 × 2400 with Three.js and headless Chrome. This is publication-only lighting; model observations remain unchanged.
4. `release_figures.py` composes nine explanatory figures (including an additional wide I/O illustration for Markdown) and eight complete-inventory panels. All figure labels use embedded Comic Sans MS; SVG labels are paths.
5. `verify.py` checks the current release, selected IDs, source hashes, blank results, native image dimensions, embedded fonts, minimum effective image resolution, citations, and the requested ten-page draft body.

Rendering requires the existing project geometry environment: NumPy, MeshLib, the connector/collision resources, pinned LDraw definitions, source certificates, Node 22+, Playwright/Chrome, Three.js, Matplotlib, and both Comic Sans MS faces. No font files or private runtime binaries are redistributed in the ZIP.

## Standalone LaTeX

The ZIP includes main/supplement TeX, their referenced figures, table sources, bibliography, and the recorded official CVPR style. Select `main.tex` or `supplement.tex` in Overleaf. The current draft deliberately has ten body pages; this is not a submission-length compliance claim. No geometry engine or model API is needed to compile those included assets.

The style files are unchanged from the repository's recorded CVPR 2026 source. The 2027 venue label and Draft ID remain provisional; check the actual submission rules when preparing an upload.

## Historical scripts

`update_current.py`, `make_current_tables.py`, `publication_scenes.py`, `design_figures.py`, and `protocol_study.py` describe earlier snapshots. They are retained for provenance, are not invoked by the current build, and must not overwrite present evidence. `--study` now refuses to imply that the historical route study is a current release audit. Current checks live in `scaling_release` and `bench_design.test_metrics`.

`publication_plate.py` exports the same white studded plate patch used by the Arena sensor, preserving its grid, board transform, stud radius and height. It changes only publication geometry. Archived inputs remain byte-identical; the two actual RGB images in the supplement are not relit or enlarged.
