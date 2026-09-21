# Build the display-v2 paper and artifacts

This is a new release. Do not run historical publication generators: they
write into preserved releases. Run these commands from the repository root.

## Checked environment

- Python: `benchmark/.runtime/mlx-env/bin/python`, with Pillow, NumPy,
  Matplotlib and PyMuPDF. Clear inherited Python package paths as below.
- TeX: `benchmark/.runtime/tectonic`.
- Node: `.tools/node-v22.23.2-darwin-arm64/bin/node`.
- Web entry: `http://localhost:5173/evidence-v2.html` on the existing Vite server.
  The static artifact also lives at `/benchmark/evidence-v2/index.html`.

## Reproduce data-derived figures and tables

```sh
env -u PYTHONPATH PYTHONNOUSERSITE=1 benchmark/.runtime/mlx-env/bin/python benchmark/suite/ldraw-evidence-v2/publication.py
benchmark/.runtime/tectonic --keep-logs --keep-intermediates benchmark/paper/evidence-v2/main.tex
benchmark/.runtime/tectonic --keep-logs --keep-intermediates benchmark/paper/evidence-v2/supplement.tex
env -u PYTHONPATH PYTHONNOUSERSITE=1 benchmark/.runtime/mlx-env/bin/python benchmark/suite/ldraw-evidence-v2/verify_publication.py --render
```

`publication.py` derives corpus tables, graph tables, paired figures,
617 full historical dossier records, 140 new pair records and web exports
from the checked manifests. It does not insert model results. A future
empirical manuscript requires an explicit update using receipt-validated
analysis, rather than silent insertion into this protocol-only release.

The two papers use actual scientific LDraw renders. Paper crops and gold
annotations are disclosed in `figure-provenance.json`. Native model images
are not cropped. All earlier source poses and geometry remain preserved.

`verify_publication.py` verifies table-input hashes, the complete dossier,
family names, all paired payload/gold mappings, figure hashes, bibliography
count, English PDF text, text bounds and nonempty pages. It exports every
page to `inspection/`. Review every page and record `visual-inspection.json`
after changes. Publication inspection is not human benchmark QA.

## Tests and preservation

```sh
env -u PYTHONPATH PYTHONNOUSERSITE=1 benchmark/.runtime/mlx-env/bin/python -m unittest discover -s benchmark/suite/ldraw-evidence-v2 -p 'test_*.py' -v
env -u PYTHONPATH PYTHONNOUSERSITE=1 benchmark/.runtime/mlx-env/bin/python benchmark/suite/ldraw-evidence-v2/preserve.py --verify
```

The 26 tests cover the human gate, both-side denominators, independent
reviewer identities, adjudication, stale wires, genuine-evidence gates,
strict response parsing, source-balanced estimates, rank ties/reversals,
graph feature collisions, source-held-out lookup and boundary intervals.

The cached `lineno.sty` has an invalid byte in a package comment and Tectonic
prints a replacement warning. The PDF verifier checks that no replacement
character appears in either delivered PDF. This does not require changing
the preserved CVPR style.

## Package and verify

```sh
env -u PYTHONPATH PYTHONNOUSERSITE=1 benchmark/.runtime/mlx-env/bin/python benchmark/suite/ldraw-evidence-v2/package_release.py --source-check
env -u PYTHONPATH PYTHONNOUSERSITE=1 benchmark/.runtime/mlx-env/bin/python benchmark/suite/ldraw-evidence-v2/package_release.py --seal
env -u PYTHONPATH PYTHONNOUSERSITE=1 benchmark/.runtime/mlx-env/bin/python benchmark/suite/ldraw-evidence-v2/package_release.py --verify
```

The paper source ZIP compiles after extraction with `tectonic main.tex`
and `tectonic supplement.tex`; the repository and scientific Python packages
are not needed to compile its precomputed figures and tables.
The source package is separate from the full historical dossier.

The delivery manifest binds new code, data, paper and site files, while
separately checking the earlier release and source-asset archives.
Build logs, Python caches, page-raster previews and superseded dry snapshots
are excluded from the compact delivery manifest.

## Human and empirical acceptance

Use `benchmark/ldraw-evidence-v2/QA-AND-RUN.md` for reviewer distribution,
feedback import, third-person adjudication and pinned model inference.
The two packages require 560 primary and 134 auxiliary genuine human reviews.
Each reviewer receives only their own blind package. Neither the evaluator
site nor the source viewer qualifies as an independent blinded judgment.

After genuine runs, `analyze.py NEW_REPORT.json --run RUN_A --run RUN_B`
verifies receipts and the common QA snapshot before reporting family-specific
scores, format validity, rank comparisons, source intervals and genuine cases.
No real model score or human answerability result is supplied in this release.
