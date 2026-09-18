# BrickAtlas LDraw-1 manuscript

The current English manuscript and supplement describe **24 unchanged
original OMR models, 15,334 numbered part instances and 617 tasks**.
They replace the Hierarchy-3 paper after source-quality review.

- `main.tex`, `main.pdf`: task definition, source selection, connector evidence,
  numbering, scoring, measured software controls and explicit limitations.
- `supplement.tex`, `supplement.pdf`: complete source attribution, four views,
  numbered input examples, and every English question prompt and answer.
- `ldraw-*.tex`: tables and source pages generated from the current release.
- `figures/ldraw/`: real application canvas renders, with no generated imitation
  geometry or Chinese annotations.
- `../ldraw-v1/`: source locks, exclusions, audits, input renders and verification.
- `BUILD.md`: reproduction commands.

The software checks do not establish physical stability or model accuracy.
No new model inference was run. The 573 intersection candidates without
recognized mating pairs remain review items.

The original project's benchmark and review routes use this dataset.
Earlier generators, evidence records and data directories are historical
only. Their physics passes and model scores are not evidence for LDraw-1.
Previous publication files remain recoverable through Git history.
