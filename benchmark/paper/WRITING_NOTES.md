# Manuscript revision evidence

User request: write a complete paper from the current report/data, learn the
presentation from BrickNet and related papers, use attractive brick 3D figures,
no Chinese anywhere in the paper figures or PDF, explain dismantling steps and
task types, and provide complete tables. This is a paper revision, not a new
dataset release or an authorization for extra paid model calls.

## Sources inspected on 2026-09-17

- BrickNet (CVPR 2026), official PDF:
  https://openaccess.thecvf.com/content/CVPR2026/papers/Kulits_BrickNet_Graph-Backed_Generative_Brick_Assembly_CVPR_2026_paper.pdf
  Local reading copy: `../.runtime/paper-reference/bricknet.pdf` and `.txt`.
  Ten pages, presentation: representative model teaser, motivation illustration,
  five connector families, graph and program example, dataset statistics,
  explicit evaluation metrics, limitations.
  Section 4: 320,808 PT samples, 40,549,969 placed parts, 9,743 part variants;
  SFT 67,185 samples, 1,774,387 instances, 4–100 parts, 512 held-out test samples.
  Samples and source objects are not interchangeable denominators.
  Section 5: mean valid prefix length for connectivity and collisions;
  graph parametrization improves connectivity while collision remains difficult.
  These are their reported results, not BrickAtlas measurements.
- Break and Make (ECCV 2022), official PDF:
  https://www.ecva.net/papers/eccv_2022/papers_ECCV/papers/136880089.pdf
  Local `.runtime/paper-reference/break-and-make.pdf` and `.txt`.
  Inspect/disassemble then reconstruct from empty scene; LTRON visual actions.
  Section 3.4: 1,727 OMR source files, 1,790 brick shapes, 5–7,302 bricks.
  Section 3.3: F1 over shape/color, pose-aligned assembly F1, iterative Assembly
  Edit Distance, edge F1. Do not imply our symbolic repair reproduces this task.
- PhyBlock:
  https://arxiv.org/html/2506.08708 (v2, 2025-11-21).
  Read abstract, introduction, organization and dataset description.
  400 assembly tasks, 2,200 VQA tasks, eight geometries/five colors, Genesis.
  AOV dependencies and four planning tiers. Its paper has inconsistent 21/23
  model counts; avoid importing that count into our comparison.

## Immutable evidence

Current data: `../hierarchy-v3-expanded`, revision hierarchy3-expanded-144.
144 model configurations, 36/level, 48 task families/object, 6,912 questions.
42,617 primitives, 2,040 rigid modules, 1,938 joints, 576 canonical views.
96 added geometric layouts; base48 files and 2,304 questions byte-preserved.
143 geometric fingerprints overall: retained indexed-toggle-latch and
orthogonal-probe-stage have same geometry with different joints.
12 added constructor families ×2 configurations ×4 levels; correlated instances.
All public reference answers accepted; 1,152 public-rule action solutions.
144 nominal protocol passes do not certify commercial LEGO, passive stability,
joint coupling, or collision-free robot paths.
Historical base48 mini pilot: 7/16, $0.013621. Four malformed action fields,
four expected-loss mistakes, one coordinate mistake. Recheck raw pilot before
using more detailed diagnostic results. No learned-model study on added96.

## Planned manuscript and figures

Use a clear scientific problem→representation→tasks→dataset→evaluation structure.
Primary contribution: hold object and task identities fixed across a crossed
evaluation; executable symbolic intervention contracts and explicit evidence
boundaries. Do not claim a new generator or superiority to BrickNet.
Move release changelog, implementation details and old correction chronology
out of main scientific narrative into reproducibility appendix.
Generate data-derived source statistics, task taxonomy/coverage, protocol limits,
constant-choice vs semantic-majority baselines, historical pilot and errors.
No fabricated human, ablation, leaderboard or significance results.

Replace Chinese-captioned teaser in main. Existing raw `images/*-iso.png` are
text-free and safe for clean 3D montages. Keep website Chinese catalog figures
separate from publication figures, using their own generator/output names.
Add actual replay-based dismantling and repair strips (native canvas captures,
not UI screenshots), and a task-by-task English worked-example mapping.
Teaser should show diverse retained and added mechanisms across levels, not only
near-identical bases. Crop unused canvas margins consistently and use legible
English panel IDs/captions. All 144 per-object appendix pages should remain.
Check CJK in PDF text AND ensure figure generation contains only English labels;
PDF text extraction alone cannot detect Chinese baked into PNGs.

## Reproduction constraints

Node22 path `.tools/node-v22.23.2-darwin-arm64/bin`.
Tectonic `benchmark/.runtime/tectonic`; compile from benchmark/paper.
PDF Python: `PYTHONNOUSERSITE=1 PYTHONPATH=/tmp/brickatlas-pdfcheck-clean python3`.
`check_pdf.py` checks no overfulls, page bounds, references, ≤8 content pages.
After changes sync webpage docs, regenerate expanded manifest, update artifact
verifier to bind new figures/tables, and run `verify-artifacts.mjs`.
Do not change retained base data or human reviews. Do not stage user's
assets-built/e2e-report.json, .dbg/, RESEARCH_MASTER_PLAN.zh-CN.md,
RESEARCH_ROADMAP.md, or debug-assemble-drag-errors.md.
