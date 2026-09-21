# LDraw-1 CVPR manuscript revision

The 2026-09-18 request is to turn the current report and data into a complete
CVPR-style English manuscript, learning from BrickNet and similar papers,
with attractive real 3D brick imagery, explicit step-by-step task taxonomy,
Matplotlib plots, comprehensive tables, and empty cells for experiments not run.

## Presentation decisions

- Keep both PDFs entirely English.
- Brick presentation plates contain only rendered geometry; no Chinese or
  English explanatory annotations or captions underneath. Preserve B-number
  identifiers only where the figure demonstrates task grounding. Put detailed
  descriptions and step mappings in body text and tables.
- Statistical plots retain necessary English axes, ticks and legends. Do not
  make fake performance curves or plot unmeasured methods as zero.
- Table captions and explanatory prose remain English. Prospective numeric
  cells are visually blank and encoded as null in a dedicated experiment plan.
- Structure the main scientific argument as problem, related work, benchmark
  representation/task design, dataset, evaluation, analysis and limitations.
  Move the synthetic-release replacement chronology to the supplement.
- Target the standard eight-page main-content budget, without layout hacks;
  references may follow. This is a development draft, not an accepted paper.

## Sources read

BrickNet, CVPR 2026, Peter Kulits and Cordelia Schmid, pp. 39252--39261.
Official page verified:
https://openaccess.thecvf.com/content/CVPR2026/html/Kulits_BrickNet_Graph-Backed_Generative_Brick_Assembly_CVPR_2026_paper.html
Local full PDF/text: `../.runtime/paper-reference/bricknet.{pdf,txt}`.
Organization: introduction and motivation, related work, representation,
typed connectors and graph serialization, dataset, evaluations, discussion.
Figures 5--6 present source distributions and part frequency; evaluation
tables distinguish exact metrics and conditions. Adopt that clarity, not its
generation task, training claims, dataset size or numerical model results.
Its discussion explicitly explains why stress-based mating and non-watertight
meshes complicate collision detection. The public tool is cited as prior work.

GQA, CVPR 2019, Drew A. Hudson and Christopher D. Manning, pp. 6700--6709.
Official page:
https://openaccess.thecvf.com/content_CVPR_2019/html/Hudson_GQA_A_New_Dataset_for_Real-World_Visual_Reasoning_and_Compositional_CVPR_2019_paper.html
Local full PDF/text: `../.runtime/paper-reference/gqa.{pdf,txt}`.
Read question-engine, functional-program, balancing, dataset-analysis and
baseline sections. Useful patterns: per-type functional programs, image-group
splits, answer-distribution diagnostics, and separate metrics. LDraw-1 does not
inherit GQA's balancing, learned baselines or human-validation results.

Break and Make, ECCV 2022, local PDF/text retained alongside the above.
Interactive reconstruction and assembly-edit measures provide related-work
context; a visibility restoration task is not its robotic reconstruction task.

## Frozen current evidence

- 24 original OMR source files / 24 set families / 15,334 source instances.
- 1,002 unique source part-type strings and 49 source color codes; these are
  representation vocabularies, not canonicalized mechanical equivalence classes.
- D1/D2/D3/D4 sources: 5/9/2/8. These are count bands, not calibrated difficulty.
- 617 tasks: atomic 213, metacognitive 201, procedural 130, integrative 73.
- Modalities: visual 140, source-data 169, connector-graph 233, scene-edit 75.
- Formats: single-choice 469, multiple-choice 73, actions 75.
- 34,877 raw connector records: stud 27,132; axle 6,976; hinge 411;
  fixed 326; ball 32. Multiple records can describe one part pair.
- 17 sources have usable author STEP metadata.
- Reference solutions 617/617; public-precondition action solver 75/75;
  1,606 invalid controls rejected. These are software controls, not MLLM results.
- Always-A choice control 26.652%; uniform expected accuracy 27.342%, both
  restricted to 469 single-choice items. Do not confuse semantic majority
  concentration with a trained baseline.
- 573 intersection candidates without recognized mating pairs remain unresolved.
  Source fidelity, connector coverage and physical stability are distinct.
- No learned-model, human, ablation, force or dynamic results on this release.

For source 42102, author-step actions 1--6 add numbered instances
B0001--B0003, B0004--B0005, B0006--B0008, B0009--B0010,
B0011--B0012, B0013--B0014. Cumulative visible counts: 3,5,8,10,12,14.
Restoration task targets B0094; initial/accepted/rejected visible counts:
128/129/128. These are source-coordinate visibility operations.

## Implementation plan

Generate publication analysis from `../ldraw-v1` and unchanged website bundles.
Add source-distribution, family-by-scale, connector-diversity and answer-prior
plots as vector PDFs plus PNG previews; retain the plotted numeric tables.
Add an eleven-family functional decomposition table and a six-action worked
example with each prerequisite, newly shown IDs, outcome and applicable task
family. Keep source-step and graph-deletion semantics distinct.

Create `ldraw-experiments.json` with null results and generated tables for
multimodal model comparisons, per-family scores, scale bands, information/tool
ablations, numbering/option/camera robustness, human review, physical validation,
and resource cost. Clearly mark their proposed status. Do not modify the old
historical `experiments.json` or transfer old pilot scores.

Update main and supplement, current generators, PDF/artifact checks, source ZIP,
English build docs and separate Chinese companion. Sync only current paper and
report links to the website. Preserve original dataset geometry, questions,
source locks and human feedback.

## Tooling and verification

Node 22: `.tools/node-v22.23.2-darwin-arm64/bin`.
Python: `benchmark/.runtime/mlx-env/bin/python`; Matplotlib 3.10.6 installed.
This environment also has NumPy 2.4.6, Pillow and PyMuPDF 1.26.4.
Use `env -u PYTHONPATH PYTHONNOUSERSITE=1`; the old PDF PYTHONPATH workaround
points at an incompatible Pillow and must not be used.
Tectonic: `benchmark/.runtime/tectonic`, invoke from `benchmark/paper`.
Load TRAE-browseruse before recapturing model views. Browser service is at 5173.
Extend current checks to bind the new figures/plots, confirm all prospective
cells stay null/blank, verify no CJK, no below-image captions, valid references,
page bounds, figure provenance and site/PDF parity. Commit and push the result.

Exclude unrelated dirty files: `assets-built/e2e-report.json`, `.dbg/`,
`benchmark/suite/RESEARCH_MASTER_PLAN.zh-CN.md`, `RESEARCH_ROADMAP.md`,
`debug-assemble-drag-errors.md`.

## Delivered revision

- Main manuscript: 9 PDF pages; main content ends on page 8, followed by
  references. English CVPR format, scientific representation/task/data/
  evaluation narrative, with no displayed figure captions.
- Supplement: 116 pages, 24 source dossiers, all 617 prompts and reference
  outputs, all 542 choice-option sets, compact evidence and extended protocols.
- Four vector Matplotlib plots with CSV data and hashes; instance-valued answers
  have no cross-source semantic-majority bar.
- Nine new raw 3D captures: six source-window states and three restoration
  states, with source hashes, visibility counts and zero scene offsets checked.
- Nine proposed experiment tables, 258 null JSON result fields rendered as
  empty cells. Historical pilot scores and physical claims remain excluded.
- Both PDFs pass CJK, citation/reference, overflow, image-provenance and page
  checks. The source package resolves all 149 TeX input/image dependencies.
- Website document downloads match the current local files byte-for-byte;
  the library includes a source-and-figures ZIP link. Production build passes.
