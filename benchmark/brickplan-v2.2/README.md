# BrickPlan 2.2

Visual assembly planning with exact future-cost and delayed-repair labels.
377 interactive episodes, 1,952 diagnostic questions, 16 source groups.

[CVPR paper](paper.pdf) · [Supplement](supplement.pdf) ·
[Dataset card](DATASET-CARD.md) · [Model integration](MODEL-INTEGRATION.md) ·
[Validity](VALIDITY.md) · [Protocol](PROTOCOL.md) ·
[Validation](VALIDATION.md) · [Review response](REVIEW-RESPONSE.md)

## Explore questions and watch a model

From the repository root, use Python 3.11+ and a C compiler.
The compiled React/Three.js frontend is included:

```bash
python3 -m venv benchmark/.runtime/brickplan-v22-env
benchmark/.runtime/brickplan-v22-env/bin/pip install -r benchmark/brickplan-v2.2/requirements.txt
benchmark/.runtime/brickplan-v22-env/bin/python benchmark/brickplan-v2.2/server.py serve --port 8769
```

In this workspace, the prepared runtime is:

```bash
env -u PYTHONPATH PYTHONNOUSERSITE=1 benchmark/.runtime/mlx-env/bin/python benchmark/brickplan-v2.2/server.py serve --port 8769
```

- **Question explorer:** http://127.0.0.1:8769/
- **Actual model case:** http://127.0.0.1:8769/#case
- **Paper and downloads:** http://127.0.0.1:8769/#release

The homepage lists seven task families with complete inputs, questions,
answer formats and scoring. Filter all questions by stable ID, family,
source, split and operation-length bin. A preview does not start an attempt.
Each question opens the corresponding workcell or frozen-checkpoint test.
Submitted practice answers unlock review. Practice provides live original
source 3D orbit/zoom/selection and explicitly labeled exploded diagrams.
Ended episodes add scored trajectory replay and feedback JSON export.

The frontend source is in `web/brickplan/`: React 19, TypeScript, Vite,
Radix Dialog/Tabs and CSS Modules. An imperative Three.js controller owns
camera updates, buffers and on-demand WebGL2 rendering; React never updates
per animation frame. Both local and static editions use the same build.

```bash
cd web/brickplan
npm ci
npm run build
```

Build output is `benchmark/brickplan-v2.2/arena/app/`. Restart the Python
server after rebuilding its explicit asset allowlist. `npm run dev` serves
port 5174 and proxies the running API on 8769.

The separate [paper folder](../../deliverables/brickplan-paper/) contains
[the Overleaf ZIP](../../deliverables/brickplan-paper/brickplan-cvpr-overleaf.zip),
editable source and both PDFs. Upload the ZIP, choose `main.tex` and XeLaTeX.
Set `supplement.tex` as the main file to compile the supplement separately.

Main images are **1920×1440 native pixels**, rendered at 2× and antialiased.
Piece tiles are 480×360; high-DPI canvases and native zoom preserve detail.
No source pieces are moved to create executable states.

On an episode, create a model run and use **One step / Run remaining / Stop**.
The bundled historical version-2.1 case preserves the first four actual local SmolVLM calls on
`kart-deck-08`. All four returned prose instead of JSON and received
`INVALID_ACTION`. This is a failed integration case, not a model benchmark
score. The raw prompts, outputs, images, usage and feedback are viewable.
Local MLX and an OpenAI-compatible API adapter are implemented; see
[MODEL-INTEGRATION.md](MODEL-INTEGRATION.md).

## Evidence and scope

| Evidence | Result |
|---|---:|
| Episodes / diagnostic questions / pairs | 377 / 1,952 / 188 |
| Development / held-out source groups | 8 / 8 |
| D1 / D2 / D3 / D4 episode counts | 97 / 152 / 83 / 45 |
| Next-action / continuation / delayed-repair questions | 653 / 288 / 943 |
| Geometry / appearance questions | 20 / 48 |
| Exact oracle tables | 130 |
| Product-state / directed-transition entries across tables | 6,836,215 / 72,954,915 |
| Two-step / five-step prefix control | 158/288 / 192/288 |
| Delayed-repair minimum cost | 1–7 operations |
| Calibration / discriminative questions | 26 / 1,926 |
| Canonical diagnostic problems / excess repeated rows | 1,819 / 133 |

D1–D4 mean optimal-operation-length bins **1–8 / 9–16 / 17–24 / 25+**.
They are not necessary reasoning-depth labels. The balanced continuation
pairs share exact legal prefixes and action multisets. Repair excludes
the terminal goal. Ten answer-changing geometry pairs cover three source
groups and four interventions, with unequal fixed-context part counts.
Static diagnostics supply four fixed initial views; active diagnostics start
with isometric and charge inspections. Every geometry pair has a distinct
static input, although three have identical initial isometric images.
Pixel distinction is not a human/model answerability certificate.

All-correct-choice rows remain calibration only. Scores average variants
within canonical problems, then problems within sources, then sources.
The inverse-last control solves 547/943 repair questions; 368 have a
suboptimal inverse and 28 have none. These cohorts are reported separately.

Structural controls use private relations and three seeds per episode:

| Policy | Completed / 1,131 | Optimal / 1,131 |
|---|---:|---:|
| Closure greedy | 1,061 | 873 |
| Capacity dispatch | 1,039 | 873 |
| Closure A*, 100 expansions | 1,008 | 1,008 |
| Closure A*, 1,000 expansions | 1,079 | 1,079 |
| Full closure A* | 1,131 | 1,131 |

Full closure A* needs at most 12,578 expansions; Hamming A* needs up to
75,454. All 653 next-action checkpoints admit a correct depth-one
heuristic choice; uniform tied minimizer accuracy is 94.0%.
Population VLM and human experiments remain pending.
The geometry contract is rigid stud support and prescribed straight motion,
not force simulation or free-pose construction. See [VALIDITY.md](VALIDITY.md)
for source-selection, counterfactual and recovery limits.

## Portable data and hosting

The [download archive](release/brickplan-v2.2-release.zip) includes the
evaluator, exact task/oracle data, source geometry, frozen runtime dependencies,
Three.js, public question table and seven HD examples. After extraction,
install the included Python requirements and run the same server command.
`verify_bundle.py` verifies inventory hashes and a native-rendering smoke check
without requiring predecessor checkouts.

The prepared [Dataset](release/huggingface-dataset/),
[Docker Space](release/huggingface-space/) and
[static site](release/static-site/) folders have not been uploaded.
The static site shows categorized examples and all real model calls.
[DATASET-CARD.md](DATASET-CARD.md) explains fields, deployment and licensing.

## Studies and reproduction

Use a fresh store per participant and condition:

```bash
python benchmark/brickplan-v2.2/server.py configure /tmp/brickplan-run.json --run-id pilot-001 --participant participant-001 --track image-id --seed 31
python benchmark/brickplan-v2.2/server.py serve --config /tmp/brickplan-run.json --store tem/brickplan-v2.2/pilot-001 --port 8772
python benchmark/brickplan-v2.2/server.py collect --store tem/brickplan-v2.2/pilot-001 --output tem/brickplan-v2.2/pilot-001-collected.json
python benchmark/brickplan-v2.2/study.py template /tmp/brickplan-manifest.json
```

Study mode restricts catalogs, replay and downloads. Model policies should
run on a separate host without private evaluator files. The budget-accounted
study adapter and practice demonstration have distinct contracts.

Core checks and publication builds:

```bash
python benchmark/brickplan-v2.2/audit_v21.py
python benchmark/brickplan-v2.2/validate.py
python benchmark/brickplan-v2.2/audit_observations.py
python benchmark/brickplan-v2.2/audit_independent.py
python -m unittest discover -s benchmark/brickplan-v2.2 -p 'test_*.py'
python benchmark/brickplan-v2.2/release.py check
python benchmark/brickplan-v2.2/package_release.py check
```

To regenerate after a deliberate revision, run `controls.py`, `documents.py`,
then compile `paper.tex` and `supplement.tex` with Tectonic or a current
LaTeX distribution and BibTeX. Next run `package_release.py export`,
`export_overleaf.py --check`, and the browser verification below.
The browser driver stages static samples without final archives.
After it passes, run `release.py freeze` followed by
`package_release.py build` and `package_release.py check`.
Regeneration changes timings/PDF metadata; compare differences before freezing.

`cvpr.sty` and `ieeenat_fullname.bst` are unmodified official author-kit
files with pinned provenance. The retrieved kit is labeled 2026, not a
verified 2027 template. The public PDF uses the template's page-numbered
preprint mode, 10-point two-column US Letter, without custom margin or
body-font compression. Set actual submission identifiers and define
`\reviewcopy` for anonymous review mode.

Current browser verification uses Playwright Firefox:

```bash
env -u PYTHONPATH PYTHONNOUSERSITE=1 \
  benchmark/.runtime/mlx-env/bin/python web/brickplan/tests/verify_v22.py
```

This driver creates temporary practice, static, active, and study servers.
It verifies four-digit IDs, supplied views, acquisition cost, answer freezing,
study isolation, native zoom, historical replay, static subpaths, and mobile
layout. It makes no new model calls. Evidence is written to
`tem/research/20261009-brickplan-v22-revision/frontend/` and installed on freeze.
Source and build hashes bind it to the tested frontend. Final download
verification follows archive construction separately.
See [frontend architecture](../../web/brickplan/README.md).

Frozen v1/v1.1/v1.2/v2/v2.1 files remain unchanged. Sixteen source groups
remain below the proposed 30–50-source target; expansion is partial.
Code and source-asset licenses
are separate; exact model authors and terms are in
[ASSET-LICENSES.json](ASSET-LICENSES.json).
