# Build the display-v3 scientific delivery

Run repository commands from the BrickAtlas root. Earlier releases are
immutable; run only the evidence-v3 generators below.

## Checked tools

- Python: `benchmark/.runtime/mlx-env/bin/python`, clearing inherited
  `PYTHONPATH`; Pillow, NumPy, Matplotlib, SciPy 1.17.1 and PyMuPDF.
- TeX: `benchmark/.runtime/tectonic`.
- Node: `.tools/node-v22.23.2-darwin-arm64/bin/node`.
- Site: `http://localhost:5173/evidence-v3.html`.
- Static site entry: `/benchmark/evidence-v3/index.html`.

## Generate and compile

```sh
env -u PYTHONPATH PYTHONNOUSERSITE=1 benchmark/.runtime/mlx-env/bin/python benchmark/suite/ldraw-evidence-v3/publication.py
benchmark/.runtime/tectonic --keep-logs --keep-intermediates benchmark/paper/evidence-v3/main.tex
benchmark/.runtime/tectonic --keep-logs --keep-intermediates benchmark/paper/evidence-v3/supplement.tex
env -u PYTHONPATH PYTHONNOUSERSITE=1 benchmark/.runtime/mlx-env/bin/python benchmark/suite/ldraw-evidence-v3/verify_publication.py --render
```

The generator independently checks the Part-type prior gate and frozen
roster, then derives tables, scientific figures and the evaluator site
from the manifests. It publishes no model scores. Color and graph
components remain frozen. The 617-item dossier is copied byte-for-byte;
`parent-mapping.json` supplies current links without rewriting old records.
The new Part-type figure uses actual regenerated native PNGs with
paper-only crops and gold annotations in `figure-provenance.json`.

The verifier checks dossier equality, all current mappings and image links,
publication input hashes, English-only PDF text, references, page bounds
and TeX overflow. Inspect all exported page previews and record the
reviewed PDF hashes in `visual-inspection.json`. Layout inspection is not
benchmark human qualification. The cached TeX `lineno.sty` warning concerns
an invalid byte in a package comment; neither PDF may contain a replacement
character.

## Protocol tests and preserved content

```sh
env -u PYTHONPATH PYTHONNOUSERSITE=1 benchmark/.runtime/mlx-env/bin/python -m unittest discover -s benchmark/suite/ldraw-evidence-v3 -p 'test_*.py' -v
.tools/node-v22.23.2-darwin-arm64/bin/node node_modules/typescript/bin/tsc -b --pretty false
env -u PYTHONPATH PYTHONNOUSERSITE=1 benchmark/.runtime/mlx-env/bin/python benchmark/suite/ldraw-evidence-v3/preserve.py
```

The 27 new tests exercise independent source-gold reconstruction, priors,
exposure-disjoint assignment, retained adjudication, oracle conflicts,
roster completeness, request/receipt gates, interrupted schedules and
author sensitivity. Existing evidence-v2 tests remain frozen separately.
`wire-audit-validation.json` records all nine offline run envelopes and
2,739 requests, with zero provider calls.

The assignment is an immutable data artifact. Reproducing paper tables
does not rerun optimization or silently replace it. Changes to frozen
measurement code invalidate old dry-run code hashes and require a fresh
explicit audit directory before sealing.

## Package and seal

```sh
env -u PYTHONPATH PYTHONNOUSERSITE=1 benchmark/.runtime/mlx-env/bin/python benchmark/suite/ldraw-evidence-v3/package_release.py --source-check
env -u PYTHONPATH PYTHONNOUSERSITE=1 benchmark/.runtime/mlx-env/bin/python benchmark/suite/ldraw-evidence-v3/package_release.py --seal
env -u PYTHONPATH PYTHONNOUSERSITE=1 benchmark/.runtime/mlx-env/bin/python benchmark/suite/ldraw-evidence-v3/package_release.py --verify
```

After extracting `brickatlas-evidence-v3-source.zip`, run
`tectonic main.tex` and `tectonic supplement.tex`. Precomputed figures and
tables make compilation independent of the repository and scientific
Python environment. Independent compilation must reproduce extracted
text and page counts; PDF bytes can vary with build metadata.

The delivery manifest binds new code, data, papers and site. Caches,
intermediate TeX files, page previews and offline wire directories are
excluded; their validation and manifest/code hashes remain auditable.
The preservation lock separately binds the 7,468 earlier files and three
content archives.

## Empirical acceptance

Follow `benchmark/ldraw-evidence-v3/QA-AND-RUN.md`. Six distinct initial
reviewers must supply 560 primary and 134 auxiliary genuine judgments,
with independent adjudication as necessary. Current actual judgments
are zero. No person may inspect this gold-revealing evaluator site before
their blind review.

The immutable model roster requires GPT-4.1, GPT-4o and GPT-4o mini at the
specified dated revisions, each in visual, no-image and graph conditions.
There are zero completed live runs. Analysis requires all nine terminal
runs, including failures. Author/source sensitivity, image dependency and
paired diagnostic value are empirical questions, not completed findings.
