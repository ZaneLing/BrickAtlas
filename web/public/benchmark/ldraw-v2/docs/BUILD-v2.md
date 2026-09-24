# LDraw-2 publication and review build

All commands below are run from the repository root unless noted. They write
only the v2 namespace. Do not use the v1 publication generators or the root
`assets:catalog` build during a publication-only update.

## Environment

- Node 22: `.tools/node-v22.23.2-darwin-arm64/bin`
- Python: `benchmark/.runtime/mlx-env/bin/python`, launched with
  `env -u PYTHONPATH PYTHONNOUSERSITE=1`
- Tectonic: `benchmark/.runtime/tectonic`
- Browser tests use installed Google Chrome through Playwright.
- Existing root `package-lock.json` and `benchmark/paper/requirements.txt`
  describe the retained dependencies.

```sh
export PATH="$PWD/.tools/node-v22.23.2-darwin-arm64/bin:$PATH"
env -u PYTHONPATH PYTHONNOUSERSITE=1 benchmark/.runtime/mlx-env/bin/python benchmark/suite/ldraw-v2/publication.py
python3 benchmark/suite/ldraw-v2/references.py
cd benchmark/paper
../.runtime/tectonic --keep-logs main-v2.tex
../.runtime/tectonic --keep-logs supplement-v2.tex
cd ../..
env -u PYTHONPATH PYTHONNOUSERSITE=1 benchmark/.runtime/mlx-env/bin/python benchmark/suite/ldraw-v2/verify-publication.py
npm run --prefix benchmark/suite/ldraw-v2 check
npm run --prefix benchmark/suite/ldraw-v2 ldraw:verify
npm run --prefix benchmark/suite/ldraw-v2 ldraw:verify-experiments
python3 benchmark/suite/ldraw-v2/verify-runner.py
python3 benchmark/suite/ldraw-v2/freeze.py --verify
```

`references.py` detects challenge redirects. The OpenReview entry was verified
through a separate read-only WebFetch retrieval; its evidence note is retained.
Abstract-level access does not justify fine-grained capability comparisons.

The generator derives 617 dossiers, all eleven contract cards, band/modality
counts, answer-prior CSV/vector plot, fourteen conditions and nine prospective
result tables. Their 264 result cells remain blank/null. It binds every input,
render and output by SHA256. All brick plates are real source-geometry captures.

## Independent v2 review application

The dev page is `http://127.0.0.1:5173/ldraw-v2.html`. It uses the existing
Vite server if running. The built site has its own entry and output directory:

```sh
node node_modules/vite/bin/vite.js build --config vite.ldraw-v2.config.ts
python3 benchmark/suite/ldraw-v2/serve.py --port 5175
```

Open `http://127.0.0.1:5175/ldraw-v2.html`. The server combines
`dist-ldraw-v2` with the repository `public` assets. Build output alone is not
a standalone geometry archive. No v1 route or source asset is rewritten.

In another terminal:

```sh
npm run --prefix benchmark/suite/ldraw-v2 ldraw:verify-ui -- --base-url http://127.0.0.1:5175
```

Tests use an isolated temporary browser context. They verify all 24 complete
models; integer scoring; isolation, explosion and cameras; source/action
replay; invalid-action rejection; physical-pair selection; feedback validation,
export/import; paired input images; and mobile layout. Test records are
software fixtures, never human decisions.

Feedback is local to the browser and exportable as a versioned JSON batch.
Every decision requires reviewer and rationale. Different reviewers remain
separate; conflicting edits from the same reviewer are rejected on import.
Version, source hash, content hash and operand identity must match. Keep the
exported file for batch correction; the app does not silently rewrite datasets.

## Publication package

```sh
python3 benchmark/suite/ldraw-v2/package-publication.py
```

This copies verified PDFs into `public/benchmark/ldraw-v2/docs` and creates
`brickatlas-ldraw-v2-source.zip`. Extract the archive and compile
`main-v2.tex` / `supplement-v2.tex` with Tectonic in its root. The archive
contains every TeX dependency, figure and generated table required for
compilation. Regeneration and full audit require the original repository.

No model inference or training is needed by these commands. Model, human,
diagnostic-localization and physical-certification evidence remain separate.
