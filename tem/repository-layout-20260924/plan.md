# Repository organization

User request: “整理仓库，论文是论文部分，中间产物放中间产物，网页放网页。”

## Intended layout

- `paper/`: current English manuscript, supplement, PDFs, required figures and
  generated TeX inputs, build tools and publication provenance.
- `web/`: main frontend source, public assets, HTML entry points, frontend
  configuration, tests and maintained website documentation.
- `benchmark/`: versioned datasets, evaluators, native packets, source lineage
  and reproducible experiment packages. Frozen experiment packages must keep
  their bytes and working references; their embedded review/render pages are
  linked from the website index.
- `tem/`: reviews, old manuscripts, obsolete figures/tables, raw captures,
  validation reports, compiler output, previews and temporary build output.
- `scripts/`, `assets-source/`, root package files and `atlas.config.ts`:
  shared acquisition, repository tools, original licensed source assets and
  shared model catalog. Installed runtimes stay in their existing ignored
  locations; moving virtual environments would break executable paths.

## Main moves and integration

1. Move root `src/`, `public/`, `tests/`, maintained `docs/`, all root HTML
   files and frontend configs into `web/`. Root package.json remains the shared
   command launcher; `npm run dev/build/test` must still work from the root.
   Keep only necessary compatibility entries for frozen code:
   root `src -> web/src`, `public -> web/public`, and a thin root
   `vite.config.ts` exporting the canonical web configuration (capture scripts
   launch Vite directly with the root cwd).
2. Prefer preserving main frontend source bytes. Its imports assume adjacent
   `atlas.config.ts`, `benchmark/` and `scripts/`. These can be documented
   shared mounts inside `web/`, or carefully updated where not hash-locked.
   Main Vite root becomes `web/`; existing URLs including `/benchmark/...`
   must remain usable. Shared benchmark mount provides native JSON and sealed
   experimental pages. Rebase the six existing public/benchmark archive
   symlinks after moving the public tree.
3. Move `assets-built/` into `tem/assets-built/`, retaining a documented root
   compatibility link if required by frozen/shared asset scripts. Preserve the
   user's pre-existing e2e-report working change EXACTLY and leave it
   uncommitted at its new path. Its initial SHA256 is
   `8692b48342732c2aa1371057d96ec4e9d8fd59bb99a9b3d09b5d04fb922965a7`.
4. Move root `dist/`, `dist-ldraw-v2/`, `test-results/`, `playwright-report/`,
   local `.preview/`, `.dbg/`, `.recording/`, and compiler caches into
   appropriate ignored `tem/build`, `tem/verification`, `tem/local` locations.
   Set future Vite, Playwright and TS output paths accordingly. Configure
   frontend cacheDir under tem. No data deletion or paid calls.
5. Move `paper/*.aux`, `.log`, `.bbl`, `.blg`, `.brf`, `.out`, Python caches
   into `tem/build/paper/`. Move paper verification.json into
   `tem/verification/paper/`. Add a paper build command that directs Tectonic
   output to tem and publishes only final PDFs into paper. Update verify.py
   to use these paths. Keep manuscript and PDF bytes unchanged in this move.
6. Paper currently uses only repair-task.pdf, repair-factorial.pdf and
   source-atlas.pdf; corresponding PNGs are useful inspection outputs.
   TeX inputs in both current manuscripts all start `generated/repair-`.
   Archive unused figures/tables and complex raw captures under tem/paper.
   Inspect build_tables.py before changing its inherited-copy output:
   asset-provenance.json currently binds old unused figures/tables and
   verify.py validates them. Update relocation targets and builder output
   consistently; preserve source hashes. Do not regenerate task data.
   Paper build scripts and current provenance legitimately belong with paper.
   Move the complex-render HTML/TS to web/paper if feasible with source-byte
   compatibility and old capture URL; avoid invalidating provenance.
7. Remove root CODEX/CVPR/debug review aliases (their actual files already
   live in tem/revisions), updating current indexes. Old archived documents
   must not be rewritten. Existing organize-research.py and
   verify-research-sync.py currently demand those old links: adapt them to
   validate canonical archived targets instead, with explicit relocation
   lookup and strict content checks.
8. Keep a relocation manifest, before/after file hashes, validation outcomes
   and README in this directory. Distinguish the original accepted snapshot
   from a layout change: never overwrite the three historical review records,
   snapshots or scientific verdicts. An archival acceptance check may verify
   the original Git commit rather than falsely label the changed working tree
   as the old snapshot. Update snapshot/audit tooling explicitly if needed.

## Validation

- Root npm scripts, TypeScript/unit tests and Vite builds.
- Browser smoke check: root app, source 3D view, historical evidence page,
  current visual-repair blind-review entry and native image/packet loading.
  Load TRAE-browseruse skill before browser tooling.
- Paper read-only provenance/GT/table/PDF verification using relocated logs.
- Frozen visual-repair study manifest and analysis replay/56 focused tests;
  don't rerun generation/freeze or rewrite retained research evidence.
- Check moves against before-hashes, document links, old archive hashes,
  source poses/IDs and preservation of the pre-existing dirty e2e report.
- Commit/push organization and verify remote. Preserve the user's dirty
  e2e-report contents outside the commit.

## State at start

Branch `codex/v3-five-issues`, HEAD and origin
`d7e2ea0a7c10ee153ff29a5839511b6b18882492`.
Only pre-existing change: `assets-built/e2e-report.json`.
Prior accepted research commit: `39e92789f2b64f34dbcfc118a2feb9e4439c951b`.
Prior accepted digest:
`6a52785ffaaae16e4e14b249289759a36243c15b94f2aa23a1b481230dc355e7`.

Python: `env -u PYTHONPATH PYTHONNOUSERSITE=1 PYTHONDONTWRITEBYTECODE=1 benchmark/.runtime/mlx-env/bin/python`.
Node: `.tools/node-v22.23.2-darwin-arm64/bin/node`.
Tectonic: `benchmark/.runtime/tectonic`.

No project AGENTS.md found. No agent has been spawned for this organization
task. No research files have been modified yet.
