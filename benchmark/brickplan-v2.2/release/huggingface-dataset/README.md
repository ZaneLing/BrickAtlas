---
language:
- en
- zh
task_categories:
- visual-question-answering
tags:
- visual-planning
- lego
- ldraw
- benchmark
size_categories:
- 1K<n<10K
configs:
- config_name: questions
  data_files:
  - split: all
    path: questions.jsonl
- config_name: examples
  data_files:
  - split: examples
    path: samples.jsonl
---

# BrickPlan 2.2

An executable benchmark of future action cost, resource scheduling and
delayed error recovery using original LDraw source geometry.

**Release status:** local versioned artifacts and hosting packages are
prepared. No Hugging Face Dataset, Space, or public site has been uploaded
by this release. The paper uses the official CVPR author-kit; this is not
a claim of conference acceptance.

## Contents and units

- 377 interactive episodes; 1,952 frozen-checkpoint diagnostic questions.
- 16 source groups: 8 development, 8 held-out source groups.
- 188 matched pairs: 144 sequence-order, 5 history, 5 changed-work,
  10 visual-geometry, 24 appearance-invariant.
- 26 calibration rows; 1,926 discriminative rows; 1,819 canonical problems.
- D1/D2/D3/D4 are optimum-length bins 1–8 / 9–16 / 17–24 / 25+.
- Seven presentation families have explicit given information, question,
  response format and scoring. IDs identify exact questions and pieces.

The 2,329 rows are correlated tasks, not 2,329 independent structures.
Alternate builds, geometry variants and identity seeds remain grouped by
source. `heldout-source` is the stored label for newly sampled source groups
10014, 10036, 10128, 10213, 10242, 10265, 10269 and 31031;
it does not imply a private test or unseen pretraining.

## Files and schemas

| File | Contents |
|---|---|
| `questions.jsonl` | All 2,329 public question records at identity seed 0 |
| `catalogue.json` | Bilingual taxonomy, counts and stable metadata |
| `samples.jsonl`, `samples.json` | Seven representative examples, one per family |
| `samples/E*.json`, `samples/Q*.json` | Full example observations, candidates/plans and repair checkpoints |
| `samples/media/*.png` | Native HD observation pixels for those examples |
| `cases/local-vlm.json` | Four historical version-2.1 model calls, prompts, outputs, feedback and images |
| `cases/task.v2.1.json`, `cases/historical-release.json` | Original task and provenance of the preserved case |
| `cases/local-vlm.authoritative.json` | Exact private executor replay of that recorded case |
| `cases/provenance.json` | Weight, bank, trace and image digests |
| `brickplan-v2.2-release.zip` | Portable runtime, all task/oracle/geometry data and evaluator code |
| `paper.pdf`, `supplement.pdf` | English CVPR-format research manuscript and supplement |
| `ASSET-LICENSES.json` | Source models, original authors, URLs and per-asset terms |

Each question row includes `id` (public, seed-specific), `stableId`
(version-stable), `category`, `form`, `kind`, `source`, `profile`, `split`,
`tier`, `lengthBin`, `question`, `given`, `answerFormat` and `scoring`.
`publicInputJSON` is serialized public input, including P/S registration,
work orders, rack, budgets, and proposed plan or candidates when applicable.
This JSON-string column avoids heterogeneous nested schemas in table viewers.
`stimulusRecipe` identifies the seed, image track and API preview route.
Correct answers, oracle costs and private relation matrices are excluded
from this public question table.

The seven sample rows reference `currentImage` and `targetImage` files.
The full example JSON additionally references rack, site-reference and
piece-catalog pixels; delayed repair includes the pre-error checkpoint.
The first question in each family's public seed-0 order is selected,
using an answer-changing geometry question for the geometry family.
This is a presentation sample, not a selected performance result.
The JSONL dataset viewer displays metadata and paths; the static site and
interactive Space provide the visual question experience.

The full release renders every question and acquired camera on demand.
It does not store all possible histories as a finite image corpus.
Main rasters are 1920×1440, rendered at 2× and downsampled with Lanczos.
Catalogs are 1920 pixels wide; each piece tile is 480×360.
Model preprocessing must be recorded independently of browser resolution.
Static diagnostics supply all five panels at each of four fixed initial
views (isometric, left, rear, right) and disable later acquisition.
`image-id-active` starts with isometric and charges each inspect. Structured
diagnostics use the same four initial views as static image diagnostics.
The native certificate finds pixel-distinct initial inputs for all ten
geometry pairs; three pairs have identical isometric panels alone.
This is not an empirical human/model answerability study.

## Use

From this repository:

```bash
python benchmark/brickplan-v2.2/server.py serve --port 8769
# Open http://127.0.0.1:8769/ ; model case: /#case
```

For the portable archive, extract it, enter `brickplan-v2.2`, install Python
3.11+ dependencies from `benchmark/brickplan-v2.2/requirements.txt`, and
run the same command. A C compiler is required for the triangle raster;
Three.js files and the frozen geometry engine are already included.
Verify extracted bytes with:

```bash
python benchmark/brickplan-v2.2/verify_bundle.py
```

The archive contains evaluator answers and oracle data. During a blind study,
run the policy on a separate host, configure the server in study mode,
and expose only public observations. Practice answers are intentionally
reviewable. See `PROTOCOL.md` for assignment and scoring contracts.

## Publishing

Generated folders under `release/` are ready to upload:

1. **Hugging Face Dataset:** upload `huggingface-dataset/` to a chosen dataset
   repository. Its README front matter configures `questions` and `examples`.
2. **Hugging Face Space:** upload `huggingface-space/` to a Docker Space.
   The included README describes provider configuration and storage.
3. **Static site:** serve `static-site/` through GitHub Pages or another
   static host. It includes seven visual question examples, all four model
   calls, paper and dataset downloads. Live actions use the Python server.

For a local static preview:

```bash
python -m http.server 8780 --directory benchmark/brickplan-v2.2/release/static-site
```

The final owner, repository name and visibility are not predetermined.
No credentials or invented external URLs are included. Docker deployment
has not been executed on a hosted Space.

## Evidence and limitations

Structural full A* solves all 1,131 repeated runs optimally; closure greedy
completes 1,061, with 873 optimal. These controls receive private relations.
All 653 next-action questions admit an optimal action among depth-one
closure-heuristic minimizers; uniform tie accuracy is 94.0%.
No necessary model reasoning depth is claimed.

The balanced continuation bank reduces a five-step prefix control from
92/98 in frozen v2 to 192/288. Delayed repair costs are independently
verified by BFS, with the terminal goal excluded from the return corridor.
Ten geometry pairs cover three source groups and four interventions,
all differing in fixed-context part counts. They are not count-matched
counterfactuals. Of 41 qualified context pairs, 37 yield no retained
answer-changing plan.
The geometry-only source pruning algorithm was refined after initial
qualification failures, before new-source solver evaluation.

The inverse-last control solves 547/943 repair questions; 368 have a
suboptimal inverse and 28 have none. All-correct-choice questions remain
calibration only. Primary scores average assigned variants within canonical
problems, problems within sources, then sources; missing variants score zero.
The source expansion admitted five of eleven additional candidates.
Sixteen groups remain below the desired 30–50-source scale.

The historical version-2.1 four-call SmolVLM case fails to produce JSON actions. It is a real
integration demonstration, not a population result. The local processor
resizes to longest edge 512; native HD observations are preserved.
Population VLM, human and physical hardware studies remain pending.
There are no irreversible geometric dead ends in the retained components.
The known-site, rigid stud-connectivity and finite-rack abstraction omits
forces, free poses, hand access, and actual rack-transfer geometry.

## Licensing and attribution

Code follows the repository `LICENSE`. LDraw source model and part licenses
remain separate; consult `ASSET-LICENSES.json` for exact authors and terms
rather than applying a single license to every payload. CVPR template
provenance and upstream notices are preserved. Model weights are not
redistributed. Source geometry is neither synthetic replacement art nor
an assertion of LEGO endorsement.
