# BrickAtlas English Manuscript

`main.tex` is an English current-state research manuscript, not a submitted or
accepted paper. It uses the official CVPR 2026 author kit in **pagenumbers**
technical-report mode. Author/institution metadata is intentionally omitted.
There is no fabricated submission number. Future submission requires checking
the relevant year's rules, setting genuine metadata, and meeting research gates.

## Contents

- `main.tex`: three research questions, closest-work comparison, eight-task contract,
  source coverage, information conditions, accepted-answer semantics, full-casebank
  copy controls, measured model diagnostics, and explicit research limits.
- `main.pdf`: eight main-content pages plus a separate reference page.
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
- `figures/`: the main teaser, task/ground-truth and execution figures are generated
  from the curated directory. Historical procedural figures remain separately named.
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

## Compile

From the repository root, regenerate tables:

```bash
node benchmark/paper/generate-tables.mjs
node benchmark/paper/generate-study.mjs
node benchmark/paper/generate-audit.mjs
node node_modules/tsx/dist/cli.mjs benchmark/suite/study/paper-models.ts replay
node node_modules/tsx/dist/cli.mjs benchmark/paper/generate-expanded.ts
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
```

The archived curated images are sufficient to compose all review and paper
plates. To rerender every per-case view/layer/step image, start the suite server,
set `BRICKATLAS_URL` if it is not `http://127.0.0.1:5175`, and run:

```bash
node node_modules/tsx/dist/cli.mjs benchmark/suite/curated/render.ts
python benchmark/suite/curated/compose.py
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
boxes, five main figures, and an actual eight-page content bound (not merely
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

V2 has 5,120 objects, 117,910 task-condition cases, and one complete public-input
algorithmic baseline plus complete height-sorted planning audits.
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
