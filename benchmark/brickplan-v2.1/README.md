# BrickPlan 2.1

Visual assembly planning with exact future-cost and delayed-repair labels.
145 interactive episodes, 739 diagnostic questions, 11 source groups.

[CVPR paper](paper.pdf) · [Supplement](supplement.pdf) ·
[Dataset card](DATASET-CARD.md) · [Model integration](MODEL-INTEGRATION.md) ·
[Validity](VALIDITY.md) · [Protocol](PROTOCOL.md) ·
[Validation](VALIDATION.md) · [Review response](REVIEW-RESPONSE.md)

## Explore questions and watch a model

From the repository root, use Python 3.11+ and a C compiler.
The compiled React/Three.js frontend is included:

```bash
python3 -m venv benchmark/.runtime/brickplan-v21-env
benchmark/.runtime/brickplan-v21-env/bin/pip install -r benchmark/brickplan-v2.1/requirements.txt
benchmark/.runtime/brickplan-v21-env/bin/python benchmark/brickplan-v2.1/server.py serve --port 8769
```

In this workspace, the prepared runtime is:

```bash
env -u PYTHONPATH PYTHONNOUSERSITE=1 benchmark/.runtime/mlx-env/bin/python benchmark/brickplan-v2.1/server.py serve --port 8769
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

Build output is `benchmark/brickplan-v2.1/arena/app/`. Restart the Python
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
The bundled case preserves the first four actual local SmolVLM calls on
`kart-deck-08`. All four returned prose instead of JSON and received
`INVALID_ACTION`. This is a failed integration case, not a model benchmark
score. The raw prompts, outputs, images, usage and feedback are viewable.
Local MLX and an OpenAI-compatible API adapter are implemented; see
[MODEL-INTEGRATION.md](MODEL-INTEGRATION.md).

## Evidence and scope

| Evidence | Result |
|---|---:|
| Episodes / diagnostic questions / pairs | 145 / 739 / 98 |
| Development / newly sampled source groups | 8 / 3 |
| D1 / D2 / D3 / D4 episode counts | 16 / 47 / 46 / 36 |
| Next-action / continuation / delayed-repair questions | 230 / 144 / 333 |
| Geometry / appearance questions | 8 / 24 |
| Exact oracle tables | 70 |
| Product-state / directed-transition entries across tables | 4,053,285 / 39,989,367 |
| Two-step / five-step prefix control | 80/144 / 96/144 |
| Delayed-repair minimum cost | 1–6 operations |

D1–D4 mean optimal-operation-length bins **1–8 / 9–16 / 17–24 / 25+**.
They are not necessary reasoning-depth labels. The balanced continuation
pairs share exact legal prefixes and action multisets. Repair excludes
the terminal goal. All four answer-changing geometry pairs come from one
development source and have unequal fixed-context part counts.

Structural controls use private relations and three seeds per episode:

| Policy | Completed / 435 | Optimal / 435 |
|---|---:|---:|
| Closure greedy | 384 | 266 |
| Capacity dispatch | 367 | 266 |
| Closure A*, 100 expansions | 362 | 362 |
| Closure A*, 1,000 expansions | 404 | 404 |
| Full closure A* | 435 | 435 |

Full closure A* needs at most 4,372 expansions; Hamming A* needs up to
75,454. All 230 next-action checkpoints admit a correct depth-one
heuristic choice. Population VLM and human experiments remain pending.
The geometry contract is rigid stud support and prescribed straight motion,
not force simulation or free-pose construction. See [VALIDITY.md](VALIDITY.md)
for source-selection, counterfactual and recovery limits.

## Portable data and hosting

The [download archive](release/brickplan-v2.1-release.zip) includes the
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
python benchmark/brickplan-v2.1/server.py configure /tmp/brickplan-run.json --run-id pilot-001 --participant participant-001 --track image-id --seed 31
python benchmark/brickplan-v2.1/server.py serve --config /tmp/brickplan-run.json --store tem/brickplan-v2.1/pilot-001 --port 8772
python benchmark/brickplan-v2.1/server.py collect --store tem/brickplan-v2.1/pilot-001 --output tem/brickplan-v2.1/pilot-001-collected.json
python benchmark/brickplan-v2.1/study.py template /tmp/brickplan-manifest.json
```

Study mode restricts catalogs, replay and downloads. Model policies should
run on a separate host without private evaluator files. The budget-accounted
study adapter and practice demonstration have distinct contracts.

Core checks and publication builds:

```bash
python benchmark/brickplan-v2.1/audit_v21.py
python benchmark/brickplan-v2.1/validate.py
python -m unittest discover -s benchmark/brickplan-v2.1 -p 'test_*.py'
python benchmark/brickplan-v2.1/release.py check
python benchmark/brickplan-v2.1/package_release.py check
```

To regenerate after a deliberate revision, run `controls.py`, `documents.py`,
then compile `paper.tex` and `supplement.tex` with Tectonic or a current
LaTeX distribution and BibTeX. Next run `package_release.py export`,
`export_overleaf.py --check`, and the browser suites below.
Use `package_release.py build` to stage static artifacts for the integration
suite. After both suites pass, run `release.py freeze` followed by
`package_release.py build` again to bind the final archive to the new manifest.
Regeneration changes timings/PDF metadata; compare differences before freezing.

`cvpr.sty` and `ieeenat_fullname.bst` are unmodified official author-kit
files with pinned provenance. The retrieved kit is labeled 2026, not a
verified 2027 template. The public PDF uses the template's page-numbered
preprint mode, 10-point two-column US Letter, without custom margin or
body-font compression. Set actual submission identifiers and define
`\reviewcopy` for anonymous review mode.

Browser suites use Playwright Firefox:

```bash
BRICKPLAN_TEST_URL=http://127.0.0.1:8771 node benchmark/brickplan-v2.1/test_workbench.mjs
BRICKPLAN_TEST_URL=http://127.0.0.1:8771 \
BRICKPLAN_STUDY_URL=http://127.0.0.1:8772 \
BRICKPLAN_STATIC_URL=http://127.0.0.1:8781/static-site/ \
node benchmark/brickplan-v2.1/test_workbench_integration.mjs
```

The second suite requires a fresh study store, a static server rooted at
`release/`, and the local MLX model. It explicitly creates and steps one real
local call; it never invokes a remote provider. Browser evidence is written to
`tem/research/20261009-react-workbench/` and copied into the release on freeze.
Source and build hashes tie the evidence to the tested frontend.
See [frontend architecture](../../web/brickplan/README.md).

Frozen v1/v1.1/v1.2/v2 files remain unchanged. Code and source-asset licenses
are separate; exact model authors and terms are in
[ASSET-LICENSES.json](ASSET-LICENSES.json).
