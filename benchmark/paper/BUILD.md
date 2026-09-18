# LDraw-1 publication build

Current source: 24 unchanged original OMR models, 15,334 instances, 617 tasks.
Both PDFs are English. Figures are actual source-geometry canvas renders.
The old Hierarchy-3 claims and pilot are excluded from the current manuscript.

From the repository root, generate and verify the dataset as described in
`benchmark/ldraw-v1/README.md`, then:

```sh
python3 benchmark/suite/ldraw/paper.py
cd benchmark/paper
../.runtime/tectonic --keep-logs main.tex
../.runtime/tectonic --keep-logs supplement.tex
python3 check_pdf.py
python3 check_pdf.py --paper supplement
cd ../..
npx tsx benchmark/suite/ldraw/publish.ts
node benchmark/paper/verify-artifacts.mjs
node benchmark/paper/package.mjs
npm run build
```

Tectonic 0.17.0 and the Python packages in `requirements.txt` are used.
The unchanged CVPR report style applies to the main manuscript; the supplement
uses US Letter with readable one-column source and question pages.
PDF checks reject CJK, unresolved references, overfull boxes, out-of-page
text and untracked raster images. Current verification files record page
counts and PDF hashes.

`verify-artifacts.mjs` checks LDraw-1 and website parity. Earlier evidence
files remain historical artifacts and are not current-release attestations.
No learned-model evaluation or physical-stability result is claimed.
