# BrickAtlas English Manuscript

Current manuscript: **Hierarchy-3 expanded**, 144 configurations and 6,912
questions. The eight-page English main PDF includes three actual 3D plates,
five tables, and references. The 152-page English supplement includes all
144 configuration pages, 48 task families, full dismantling and repair
examples, rejected transitions, and answer-concentration diagnostics.
The separate Chinese companion is not embedded in either PDF.

The original application's `/benchmark` and `/benchmark/review` routes render
the models, replay programs, and collect task feedback. Current evidence is
bound by `hierarchy-expanded-evidence.json`, `publication-analysis.json`,
`publication-capture.json`, and `publication-figures.json`;
`verify-hierarchy-expanded.mjs` checks these artifacts and website parity.
Only the archived 7/16 base-48 pilot is a learned-model measurement discussed
in this manuscript. No new model inference was performed.

## Current publication reproduction

From the repository root (Node 22, dependencies installed):

```bash
node node_modules/tsx/dist/cli.mjs benchmark/paper/analyze-publication.ts
# Optional recapture: requires npm run start:local at port 5173 and Chrome.
node node_modules/tsx/dist/cli.mjs benchmark/paper/capture-publication.ts
python3 benchmark/paper/compose-publication.py
cd benchmark/paper
../.runtime/tectonic --keep-logs main.tex
../.runtime/tectonic --keep-logs supplement.tex
python3 check_pdf.py
python3 check_pdf.py --paper supplement
```

PDF checks require the dependencies in `requirements.txt`. They reject CJK
text and bind embedded images to English publication plates or unlabelled
canonical views. The archived frames suffice to compose figures without
recapturing. Capture does not submit human review decisions.

Then, from the repository root:

```bash
npm --prefix benchmark run h3x:sync
node node_modules/tsx/dist/cli.mjs benchmark/suite/hierarchy3-expanded/release.ts --manifest
node benchmark/paper/verify-artifacts.mjs
node benchmark/paper/package.mjs
```

The remaining historical generators and result descriptions below are retained
for earlier versions; they are not additional experiments in the current paper.

`main.tex` is an English current-state research manuscript, not a submitted or
accepted paper. It uses the official CVPR 2026 author kit in **pagenumbers**
technical-report mode. Author/institution metadata is intentionally omitted.
There is no fabricated submission number. Future submission requires checking
the relevant year's rules, setting genuine metadata, and meeting research gates.

## Contents

- `../mechanism-v1/`: six original articulated objects, 48 gap-driven tasks,
  72 audited renders, a complete case browser, raw model runs and scores.
- `mechanism-manual.tex`, `generate-mechanism.mjs`,
  `mechanism-evidence.json`: physics contracts, model/task figures and results.
- `../references/omr-design-reference/`: OMR/LDraw design reference only;
  none of its geometry is a benchmark case or model input.

- `constructibility-manual.tex`: process-aware sequence, accessibility,
  recovery, stockout and calibrated-clarification contracts.
- `../constructibility-v1/`: 78 development conditions on six Frontier sources,
  with public-input solver results and shortcut controls but no learned-model run.
- `../CONSTRUCTIBILITY_UPGRADE.zh-CN.md`: Chinese research plan, implementation
  status, capability mapping and CVPR evidence gates.

- `diagnostic-manual.tex`: Diagnostic-2 revision addressing fixed-answer shortcuts,
  paired visual disclosure, deadline schedules and independent-stage coherence.
- `../diagnostic-v2/index.html`: 138 new conditions on six existing sources,
  with 216 alternative independent-stage request views.
- `../DIAGNOSTIC_UPGRADE.zh-CN.md`: current Chinese change report and remaining gates.

- `frontier-manual.tex`: literature overlap audit and eight new large-structure
  maintenance, resource and finite-observation contracts.
- `tables/frontier-cases.tex`: six 158--408-part objects, all 48 scored control
  pairs. Public-input algorithm runs are measured; learned-model results are not.
- `../FRONTIER_REPORT.zh-CN.md`: Chinese research and upgrade report.
- `../frontier-cases/index.html`: all new objects, views and task inputs.

- `reference-manual.tex`: full input/output contracts, metrics, method-specific
  tracks, revision-2 corrections, resource reporting and contamination limits.
- `tables/review-case-studies.tex`: all 18 authored sources, 36 scored positive/negative
  controls with images. These are evaluator checks, not learned-model results.
- `../review-gallery/index.html`: authored calibration sources and the retired
  5,120-source procedural regression gallery.

- `main.tex`: current crossed design, task contracts, Rapier protocol,
  structural/control tables, historical pilot, and explicit research limits.
- `main.pdf`: eight pages including references.
- `supplement.tex`, `supplement.pdf`: detailed task schemas, catalog counts,
  model variants, ambiguity controls, historical experiments, and future designs.
- `REVIEW.zh-CN.md`: reviewer-oriented gap analysis and remaining evidence gates.
- `RESEARCH_UPDATE.zh-CN.md`: updated nearest-work audit (including BC-Bench,
  TreeSBA and SpatialBabel), figure rationale, contribution and remaining gaps.
- `references.bib`: brick generation, manual parsing, interactive assembly,
  visual programs, diagnostic VQA, BLINK, selection bias, and baseline references.
- `tables/*.tex`: tables generated from actual artifacts, not manually invented values.
- `../curated-cases/`: reviewer-facing case directory with 12 original structures,
  per-case JSON, four views, occupied layers, exploded views, legal steps,
  eight task input/ground-truth folders, contact sheets, and a static HTML index.
- `../challenge-cases-v2/`: six connected 49--63-part structures and twelve advanced
  task contracts. Oracle checks are complete; model result cells remain blank.
  Original `../challenge-cases/` is retained but deprecated for new evaluation.
- `figures/publication-*`: English plates and raw replay frames for the current paper.
  Historical OMR and procedural assets are not current benchmark figures.
- `evidence.json`: source paths/hashes for numerical evidence and upstream template.
- `generate-tables.mjs`: table generation and evidence assertions.
- `generate-study.mjs`, `study-evidence.json`: new study tables and source hashes.
- `generate-audit.mjs`, `audit-evidence.json`: full-population census/copy tables.
- `generate-figures.py`, `figure-evidence.json`: source-bound overview, distributions,
  hidden-layout witness, score diagnostics, and paired-order plots.
- `experiments.json`: twelve prospective experiment tables, 460 null result cells.
  No future result is treated as zero or filled from a pilot.
- `verify-artifacts.mjs`: figure/source hashes, blank-table and PDF-check consistency.
- `generate-expanded.ts`, `expanded-evidence.json`: eight-model main/diagnostic
  tables, five public-input algorithmic baselines, and finite-grammar task results.
- `render-structures.ts`, `compose-structures.py`: historical procedural and
  hidden-layout audit plates; these no longer provide the paper teaser/task examples.
- `../suite/curated/{cases,tasks,render}.ts`, `../suite/curated/compose.py`:
  explicit curated geometry, task contracts, case-folder export, and paper plates.
- `generate-curated.ts`, `curated-evidence.json`: verify the 264 generated curated
  files and produce the exact specification table.
- `../suite/challenge/`, `generate-challenge.ts`, `challenge-evidence.json`:
  advanced models, evaluators, renders, tables, and evidence hashes.

## Historical generators and general TeX setup

From the repository root, regenerate tables:

```bash
node benchmark/paper/generate-tables.mjs
node benchmark/paper/generate-study.mjs
node benchmark/paper/generate-audit.mjs
node node_modules/tsx/dist/cli.mjs benchmark/suite/study/paper-models.ts replay
node node_modules/tsx/dist/cli.mjs benchmark/paper/generate-expanded.ts
node benchmark/paper/generate-constructibility.mjs
node node_modules/tsx/dist/cli.mjs benchmark/suite/mechanism/release.ts
node benchmark/paper/generate-mechanism.mjs
```

Regenerate or independently rescore the new full-casebank audit:

```bash
node node_modules/tsx/dist/cli.mjs benchmark/suite/study/paper-audit.ts
node node_modules/tsx/dist/cli.mjs benchmark/suite/study/paper-audit.ts --verify
```

The second command is read-only and compares all 35,840 case records and the
source inventory to the stored artifacts. Neither command calls model APIs.
The predictor only copies public `current`; evaluation uses the frozen scorer.

Figures and PDF checks use Python 3.11. Install the pinned dependencies in a
virtual environment, then generate figures before compiling:

```bash
python -m pip install -r benchmark/paper/requirements.txt
python benchmark/paper/generate-figures.py
python benchmark/suite/curated/compose.py
python benchmark/paper/compose-structures.py
node node_modules/tsx/dist/cli.mjs benchmark/paper/generate-curated.ts
python benchmark/suite/challenge/compose.py
node node_modules/tsx/dist/cli.mjs benchmark/paper/generate-challenge.ts
```

The archived curated images are sufficient to compose all review and paper
plates. To rerender every per-case view/layer/step image, start the suite server,
set `BRICKATLAS_URL` if it is not `http://127.0.0.1:5175`, and run:

```bash
node node_modules/tsx/dist/cli.mjs benchmark/suite/curated/render.ts
python benchmark/suite/curated/compose.py
node node_modules/tsx/dist/cli.mjs benchmark/suite/challenge/render.ts
python benchmark/suite/challenge/compose.py
```

This uses a separate display renderer and does not change historical model images.
It checks nonblank pixels, framing, 12 structures, all task oracles, legal
assembly orders, and a designed planning dead end. Exploded layers are display-only.
`benchmark/curated-cases/index.html` can be opened directly.

Build or verify the new ambiguity track without network requests:

```bash
node node_modules/tsx/dist/cli.mjs benchmark/suite/study/ambiguity.ts
node node_modules/tsx/dist/cli.mjs benchmark/suite/study/ambiguity.ts --verify
node node_modules/tsx/dist/cli.mjs benchmark/suite/study/ambiguity-score.ts predictions.jsonl report.json
```

The public schema and scoring contract are in `../suite/study/AMBIGUITY.md`.
Do not run `paper-models.ts run` to reproduce results: that is the explicitly
paid execution entry point. Use `replay` for offline verification.

From `benchmark/paper/`, with a normal TeX Live installation:

```bash
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
latexmk -pdf -interaction=nonstopmode -halt-on-error supplement.tex
```

Or use Tectonic, which also runs BibTeX and reference passes:

```bash
tectonic --keep-logs --keep-intermediates main.tex
tectonic --keep-logs --keep-intermediates supplement.tex
```

Tectonic may download public TeX/font resources on first use. No API model calls
are involved. The local verified binary, when installed for this workspace, is
`benchmark/.runtime/tectonic`; it is not part of the published source.

Optional PDF inspection uses Python 3.11, PyMuPDF 1.26.4 and Pillow 11.3.0:

```bash
python check_pdf.py
python check_pdf.py --paper=supplement
```

It checks US Letter dimensions, text bounds, unresolved references, overfull
boxes, English image provenance, and an actual eight-page content bound (not merely
where references start). It renders pages into `.runtime/paper-inspection/`.

After PDF checks, from the repository root:

```bash
node benchmark/paper/verify-artifacts.mjs
node benchmark/paper/package.mjs
```

The source ZIP includes generated figures/tables and compiles without the full
benchmark checkout. Recomputing figures, audits, or provenance checks needs the
full repository and its archived evidence; the ZIP is not a standalone dataset.

## Official Template Provenance

Upstream: https://github.com/cvpr-org/author-kit

Pinned revision: `291758547e923160eb4d37079b7b9f0dfce82355`.

`cvpr.sty` and `ieeenat_fullname.bst` are copied unchanged; authorship notices remain.
The upstream README identifies this as the official CVPR/ICCV/3DV template,
updated for CVPR 2026. The manuscript does not change margins or use negative
spacing to force a page count. Template provenance is not a claim of acceptance.

## Evidence Boundaries

The primary Mechanism-1 layer has six original articulated objects, 542
visible parts, 36 rigid modules, 33 joints and 48 paired tasks. OMR/LDraw
models are design references only. The former v2 layer has 5,120
random-growth structures and 117,910 task conditions; it is retained only
for historical model/scorer reproduction and excluded from current scale.
Mechanism-1 measures 96 image-conditioned cloud-model calls at $0.069454:
GPT-4.1 mini scores 29/48 and Gemini 2.5 Flash 27/48. A local text-only
Qwen3-0.6B baseline scores 3/48. These are six-source descriptive results,
not a powered population ranking.
The new v2 study contains 674 one-shot and 56 control API calls on 24 shared
held-out objects and 25 catalog questions; it remains exploratory, not powered.
All ten planned SmolVLM jobs are complete: 3,370 predictions, 1,080 updates and
552,960 supervised answer tokens. `study-evidence.json` links their evidence.
Exact successes occur only in relation tasks; no positive edit-transfer result
was observed in the leave-edit conditions.
The 112-call two-model study, 24-call paired control, and five Qwen LoRA/base runs
belong to earlier releases and are explicitly separated.

Additional development diagnostics comprise a four-model 180-call screen,
two separately versioned 24-call reconstruction ladders, and 96 local-pose
and candidate-selection calls on four unused source groups. The main text
reports coordinate-origin confounds, copy-input baselines, output-protocol
differences and permutation sensitivity rather than a pooled leaderboard.
`tables/study-pose.tex` is generated from the frozen pose-probe evidence.
These adaptive experiments do not establish a stable model ranking or a
causal attribution of errors to perception, reasoning or output generation.

The subsequent 192-call development replication uses 12 new source groups,
four models and original/repeat/permuted/no-image conditions. Paired excess
permutation mismatch is 0.50-0.75; source-bootstrap intervals exclude zero in
this selected small sample. This is not independent population confirmation.
`tables/study-order.tex` is generated from its archived analysis. Total historical
API accounting before the expanded matrix is 1,609 calls and $3.097410574,
not the size of a single study.

The eight-model matrix adds Claude Haiku 4.5, Gemini 3 Flash preview,
Qwen3-VL-8B and Llama 4 Maverick on the same 39 tasks used by the four-model
screen, with three shared source objects and no new hidden test set.
All 156 additional calls complete at $0.523093880. Cumulative accounting is
1,765 calls and $3.620504454, under the unchanged $4.50 cap. The new allocation
was $0.75. Endpoint, provider and time differences are recorded, not normalized
away; the main table is descriptive rather than a stable model ranking.

The separate ambiguity extension contains 600 task conditions from nine
parameterized grammar families and 60 admissible layout states. Ground truth
is exhaustive only within the explicit domino grammar. Public-input enumeration
solves all cases; VLM experiments on this new track remain unrun.
Its paired observations produce 90 exterior `undetermined` labels that become
determinate with support disclosure. Under the fixed paper renderer, all 204
nontrivial alternative-view comparisons match the 36 reference frames exactly.
These are symbolic known-geometry reasoning inputs, not a pure visual benchmark.

The curated layer is deliberately separate from v2. It has four easy, four
medium, and four hard structures across furniture, architecture, infrastructure,
and landmark styles. Each object uses two to four role-based colors rather than
independent random colors. These are original CC0 BrickAtlas structures, not
copies of official sets. They improve qualitative/task calibration but do not
replace independent semantic data or human recognition judgments.

The additional renderer-aware baseline uses only public BOM/candidates, three
RGB views and the known simulator. It solves all 16 original-source choices
and preserves all 16 after permutation. Across repeated/permuted conditions
the image total is 44/44, not 44 independent objects. All 16 no-image cases
abstain. Replacing the source images yields one abstention and 9/15 changed
jointly answered selections. The run generates 384 template views in 29.7
seconds without API calls; its results are in `tables/study-visual-choice.tex`.
This post-hoc, canonical-color control is not a general learned baseline,
independent human validity check or new confirmation dataset.

Independent human review, rich human-designed data, broader model baselines,
and confirmatory experiments remain outstanding.
Constructibility-1 adds 78 process conditions across the same six public Frontier
sources. Public-information controls pass all cases; named shortcuts pass
6/18 sequence audits, 0/18 recoveries, 0/6 stockouts, and 5/36 clarification
conditions. These are task-mechanism checks, not learned-model results or new
independent sources.
The 2026-09-14 audit adds no API calls or new source objects. It measures 19/25
catalog types in assembled sources and 35,840 copy-current controls across seven
endpoints. Copying yields 87.1% part F1 on completion and 97.4% on removal, both
with zero task success. Normal no-fault repair correctly succeeds unchanged.
Per-case records are in `../suite/artifacts/study/paper-audit/`.
All prospective result tables appear together in the supplement, with per-table
input conditions, baselines, denominators, statistical endpoints and dependencies.
Both local research plans remain excluded from publication. The public
`../suite/artifacts/study/governance/SUMMARY.zh-CN.md` tracks evidence gates.

Chinese companions: `../suite/study/OVERVIEW.zh-CN.md` and `../suite/study/REPORT.zh-CN.md`.
