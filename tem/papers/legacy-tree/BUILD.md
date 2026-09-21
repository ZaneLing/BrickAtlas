# LDraw-1 publication build

Current source: 24 unchanged original OMR models, 15,334 instances, 617 tasks.
Both PDFs are English. Figures are actual source-geometry canvas renders.
The old Hierarchy-3 claims and pilot are excluded from the current manuscript.

The source corpus and task bundles are frozen for this publication revision.
For publication-only changes, do not regenerate the dataset. From the
repository root, use a Python environment installed from `requirements.txt`
and Node 22 or later:

```sh
python3 benchmark/suite/ldraw/paper.py
python3 benchmark/suite/ldraw/publication.py
cd benchmark/paper
../.runtime/tectonic --keep-logs main.tex
../.runtime/tectonic --keep-logs supplement.tex
python3 check_pdf.py
python3 check_pdf.py --paper supplement
cd ../..
node benchmark/paper/sync-docs.mjs
node benchmark/paper/verify-artifacts.mjs
node benchmark/paper/package.mjs
node benchmark/paper/sync-docs.mjs
npm run build
```

To recapture the nine captionless worked frames, start the local site at
`http://127.0.0.1:5173`, then run
`npx tsx benchmark/suite/ldraw/capture-publication.ts` before `paper.py`.
The capture uses real source meshes, UI actions and read-only canvas export.
Canonical source and numbered input images are already versioned.

In the current workspace, Python is available at
`benchmark/.runtime/mlx-env/bin/python`; launch it with
`env -u PYTHONPATH PYTHONNOUSERSITE=1` to avoid unrelated package overrides.
Node is under `.tools/node-v22.23.2-darwin-arm64/bin`.
Publication statistics and plot data must be regenerated when their generator
changes. The analysis manifest binds the current generator and all inputs.

Tectonic 0.17.0 and the Python packages in `requirements.txt` are used.
The unchanged CVPR report style applies to the main manuscript; the supplement
uses US Letter with readable one-column source and question pages.
PDF checks reject CJK, unresolved references, overfull boxes, out-of-page
text and untracked raster images. Current verification files record page
counts and PDF hashes. Figure environments contain no displayed captions.
The four statistics plots are vector PDFs with English axes and legends.

`verify-artifacts.mjs` checks LDraw-1 and website parity. Earlier evidence
files remain historical artifacts and are not current-release attestations.
It also checks all nine prospective tables: 258 result fields must remain
null in JSON and empty in LaTeX. It verifies all 617 appendix entries and
542 option sets, real-frame hashes and the source-data hashes of every plot.
No learned-model evaluation or physical-stability result is claimed.

`brickatlas-cvpr-source.zip` contains both manuscripts, generated tables,
all print assets, vector plots, numerical CSV files, experiment specification,
CVPR style and build/check scripts. It can compile without the full model
corpus; regeneration and full artifact verification require the repository.
