# Build and verify the evidence revision

Run from the BrickAtlas repository root. These commands preserve original v1/v2
files. Do not run the old v2 publication/experiment generators: they write into
the frozen release.

The checked environment uses the repository Node 22 binary, Python 3.9 for core
analysis, and the existing scientific Python environment for figures/PDF checks
(`Pillow`, `numpy`, `matplotlib`, `PyMuPDF`). Tectonic supplies TeX packages.

## Verify code, data and result states

```sh
python3 benchmark/suite/ldraw-evidence/freeze.py --verify
python3 benchmark/suite/ldraw-evidence/test_adaptation.py
python3 benchmark/suite/ldraw-evidence/test_wire_qa.py
.tools/node-v22.23.2-darwin-arm64/bin/node node_modules/tsx/dist/cli.mjs benchmark/suite/ldraw-evidence/test-receipts.ts benchmark/ldraw-evidence-v1/receipt-test-fixtures.json
.tools/node-v22.23.2-darwin-arm64/bin/node node_modules/typescript/bin/tsc --noEmit --project benchmark/suite/ldraw-evidence/tsconfig.json
python3 benchmark/suite/ldraw-evidence/verify-matched-graphs.py
.tools/node-v22.23.2-darwin-arm64/bin/node node_modules/tsx/dist/cli.mjs benchmark/suite/ldraw-evidence/verify-graph-parity.ts
python3 benchmark/suite/ldraw-evidence/verify-literature.py
python3 benchmark/suite/ldraw-evidence/reporting.py verify
```

`test-receipts.ts` creates temporary synthetic raw receipts and invokes
`test_publication_chain.py` with their directory while they exist. Run that
fixture through its TypeScript parent, not as a standalone unittest discovery
module. Synthetic fixtures cannot enter the real result index.

## Generate and compile

```sh
python3 benchmark/suite/ldraw-evidence/reporting.py publish
env -u PYTHONPATH PYTHONNOUSERSITE=1 benchmark/.runtime/mlx-env/bin/python benchmark/suite/ldraw-evidence/publication.py
benchmark/.runtime/tectonic --keep-logs --keep-intermediates benchmark/paper/evidence-v1/main.tex
benchmark/.runtime/tectonic --keep-logs --keep-intermediates benchmark/paper/evidence-v1/supplement.tex
env -u PYTHONPATH PYTHONNOUSERSITE=1 benchmark/.runtime/mlx-env/bin/python benchmark/suite/ldraw-evidence/verify-publication.py --render
python3 benchmark/suite/ldraw-evidence/package-release.py
env -u PYTHONPATH PYTHONNOUSERSITE=1 benchmark/.runtime/mlx-env/bin/python benchmark/suite/ldraw-evidence/verify-paper-archive.py
```

The source ZIP compiles independently after extraction with `tectonic main.tex`
and `tectonic supplement.tex`. The delivered PDFs have 8 and 182 pages.
The main text occupies 7 pages; references begin on page 8.
The official style's cached `lineno.sty` produces a harmless encoding warning
in a package comment; no replacement glyph occurs in either PDF. Two underfull
supplement paragraphs remain; there are no overfull boxes or undefined references.

`verify-publication.py` checks every page, fonts, English text, bounds, captions,
numeric provenance and the complete task index. Review the exported page images
and record a new `visual-inspection.json` after any manuscript/figure change.
The recorded review is publication QA, not human benchmark answerability.

## Review, future results and local web entry

- Open `/evidence-v1.html` on the existing Vite development server.
- The 3D viewer remains `/ldraw-v2.html`.
- The exact-wire review at `/benchmark/evidence-v1/wrong-image-review.html`
  includes native-size images and an export button that also exposes copyable
  JSON. It has no model predictions or reference answers.
- Its source is `benchmark/ldraw-evidence-v1/qa/wrong-image-export-v1/`.
  The earlier review export remains preserved.
- To create another QA export, use `wire_qa.py --run RUN --out NEW_DIRECTORY`.
  Never reuse an existing output directory.
- To validate returned JSON, use
  `wire_qa.py --run RUN --out EXISTING_QA_DIRECTORY --feedback FEEDBACK_JSON`.
- Register a genuine completed run with
  `reporting.py register --run RUN --out-index NEW_INDEX_JSON`,
  verify that index, then publish it with `--index NEW_INDEX_JSON`.
  No credentials or API calls are needed for the checks above.

After all reports are final, run `package-release.py --seal` followed by
`verify-delivery.py`. The seal hashes the new code/data/paper/site files and
separately binds the original preservation archive.
