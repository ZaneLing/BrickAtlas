# Verified Build

- Compiler: Tectonic 0.17.0, macOS aarch64.
- Official binary archive SHA256:
  `a3f1cac7c5678f01661a92212f58480ae3b0634115d880dbc59e2953ded45667`.
- Archive source:
  `https://github.com/tectonic-typesetting/tectonic/releases/download/tectonic%400.17.0/tectonic-0.17.0-aarch64-apple-darwin.tar.gz`.
- Official CVPR author-kit revision:
  `291758547e923160eb4d37079b7b9f0dfce82355`.
- Template files are unmodified; their hashes are recorded in `evidence.json`.
- Output: eight US Letter main-content pages and one separate reference page;
  sixteen supplementary pages. No margin or negative-spacing modifications.
- TeX log: no unresolved citations/references or overfull boxes.
- PDF inspection: text on every page, no text outside page boundaries.
- All-page contact sheet and detailed formula/result pages inspected visually:
  two-column text, actual rendered structures, tables and equations remain legible
  and do not overlap.
- The first-page teaser, task/ground-truth figure, and execution figure come
  from 12 explicitly authored curated models, not random procedural samples.
  The review directory contains 264 generated per-case files plus contact sheets.
- The hidden-layout plate remains a separate 60-layout finite-grammar audit.
- New full-casebank audit: 35,840 copy controls on 5,120 sources reproduced
  exactly with `paper-audit.ts --verify`; assembled catalog coverage is 19/25.
- Eight-model matrix: 312 responses on the same three sources; four new models
  add 156 settled calls at $0.523093880. Cumulative spend is $3.620504454.
- Ambiguity extension: 600 paired conditions, nine finite-grammar families,
  60 admissible layouts, and 240 renderer checks with pixel-identical exteriors.
- Runtime-free, key-free copied-environment replay passes 23 commands, including
  the expanded model receipts and ambiguity ground-truth verifier.
- Benchmark regression: 146 tests pass; TypeScript check passes.
- Twelve prospective result tables retain 460 blank cells (JSON null).
- `verify-artifacts.mjs` checks model/audit/figure/PDF hashes, 3D render framing,
  ambiguity counts, and blank-table accounting.

`pdf-verification.json` and `supplement-verification.json` record the output PDF hashes.
The compiler and TeX caches are runtime dependencies, not committed project files.
The paper uses report mode with page numbers, not a fabricated anonymous submission.
No author identity or submission number was invented.
Historical pilots and engineering details are in `supplement.tex`.
The page count does not establish submission readiness: scientific gates,
metadata, anonymization and the actual target-year rules remain outstanding.
