# BrickAtlas LDraw-1 manuscript

The current English manuscript and supplement describe **24 unchanged
original OMR models, 15,334 numbered part instances and 617 tasks**.
They replace the Hierarchy-3 paper after source-quality review.

- `main.tex`, `main.pdf`: CVPR-format development manuscript, with representation,
  eleven functional task families, a six-step source example, descriptive
  analyses, metrics, measured controls and proposed experiments.
- `supplement.tex`, `supplement.pdf`: complete source attribution, four views,
  numbered inputs, all 617 English prompts, all 542 sets of choice options,
  compact input evidence, reference outputs and extended evaluation tables.
- `ldraw-*.tex`: tables and source pages generated from the current release.
- `ldraw-experiments.json`: nine proposed experiment tables with 258 null result
  cells. PDF numeric result cells remain blank; known dataset sizes are filled.
- `analysis/`: four vector Matplotlib plots, PNG previews, numerical CSV tables
  and measured statistics. No unmeasured model score is plotted.
- `ldraw-publication.json`: hashes binding plot data, source bundles and generator.
- `figures/ldraw/`: real application canvas renders, with no generated imitation
  geometry or explanatory captions underneath. Numbered inputs retain B IDs.
- `../ldraw-v1/`: source locks, exclusions, audits, input renders and verification.
- `BUILD.md`: reproduction commands.

The software checks do not establish physical stability or model accuracy.
No new model inference was run. The 573 intersection candidates without
recognized mating pairs remain review items.

The organization draws on BrickNet's representation/data/evaluation separation
and GQA's functional task analysis. Both are cited; their scores, validation
claims and training protocols are not transferred to this release.

The original project's benchmark and review routes use this dataset.
Earlier generators, evidence records and data directories are historical
only. Their physics passes and model scores are not evidence for LDraw-1.
Previous publication files remain recoverable through Git history.
