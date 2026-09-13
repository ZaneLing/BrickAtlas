# V2 Study And Reproduction

This extension leaves the released casebank generator, legacy scorer, paid API
runner, and paid control scripts unchanged. See `OVERVIEW.zh-CN.md` for the
capability narrative and `REPORT.zh-CN.md` for evidence and outstanding work.

## Offline Commands

Run from the repository root, using Node 22:

```bash
node node_modules/tsx/dist/cli.mjs benchmark/suite/study/cli.ts replay
node node_modules/tsx/dist/cli.mjs benchmark/suite/study/cli.ts strict-audit
node node_modules/tsx/dist/cli.mjs benchmark/suite/study/cli.ts verify-training
node node_modules/tsx/dist/cli.mjs benchmark/suite/study/cli.ts replay-local
node node_modules/tsx/dist/cli.mjs benchmark/suite/study/cli.ts local-statistics
node node_modules/tsx/dist/cli.mjs benchmark/suite/study/cli.ts diagnose
node node_modules/tsx/dist/cli.mjs benchmark/suite/study/cli.ts observability
node node_modules/tsx/dist/cli.mjs benchmark/suite/study/cli.ts replay-probes
node node_modules/tsx/dist/cli.mjs benchmark/suite/v2/cli.ts replay
```

These commands make no model API requests. API execution requires explicit
`run --paid` or `controls --paid`, a credential in the environment, and the
original cumulative budget ledger. Never reset a ledger to rerun experiments.

`v2:score` now uses `v2-strict-schema-1`. `score-legacy` retains historical
semantics solely for reproduction. Both require frozen selection manifests.
The strict scorer rejects non-string IDs/colors before the frozen decoder can
coerce singleton arrays to property names. Stored historical results are unchanged.
The schema regression run is a fixture, not a model baseline.

## Local Training

Reference environment:

- Python 3.9, torch 2.8.0, transformers 4.57.6, peft 0.17.1, accelerate 1.10.1.
- Separate Python 3.11 environment: mlx-vlm 0.7.0, transformers 4.57.6.
- Apple Silicon/MPS training and unquantized MLX inference. Local compute is not free.

The scripts currently resolve environment binaries below `benchmark/.runtime/`;
create `train-env` and `mlx-env` there when reproducing. The public base model is
downloaded by `download_vlm.py` at a pinned revision. No gated data is required.

```bash
node node_modules/tsx/dist/cli.mjs benchmark/suite/study/cli.ts restore-training
benchmark/.runtime/train-env/bin/python benchmark/suite/study/download_vlm.py
benchmark/.runtime/train-env/bin/python -u benchmark/suite/study/vlm_matrix.py
node node_modules/tsx/dist/cli.mjs benchmark/suite/study/cli.ts import-local
node node_modules/tsx/dist/cli.mjs benchmark/suite/study/cli.ts replay-local
node node_modules/tsx/dist/cli.mjs benchmark/suite/study/cli.ts local-statistics
```

The matrix is serial and refuses to overwrite completed jobs. An incomplete job
requires explicit recovery; an interrupted run must not be silently replaced.
Restarting the matrix preserves console logs and refuses an incomplete manifest
before launching the trainer. It does not implement optimizer-state recovery.
Nine trained jobs have 120 updates and 61,440 loss-bearing answer tokens each.
Base has no updates. This does not match image tokens, input tokens, or compute.
Validation NLL uses two fixed examples per task. Test predictions use all 337
fixed cases and all supplied images, with 2,200 new tokens per case.

The portable bundle has 840 train/validation rows and 480 unique PNGs, source
case IDs, and SHA256 checks. Published adapters contain portable base-model
identifiers rather than machine-specific directories. Full base weights and
merged checkpoints are runtime files, not included in the source repository.
Upstream SmolVLM declares Apache-2.0; adapter users must retain upstream notices.
Procedural training examples retain the casebank CC0 declaration.

## Interrupted Sessions

A disconnected chat does not imply the training process stopped. Do not launch a
second matrix while the original owns `.runtime/vlm-training/matrix.lock`.
To attach a detached validator to a running matrix, from the repository root:

```bash
node benchmark/suite/study/watch-local.mjs
```

It holds a separate validation lock, imports only complete jobs, audits merged
weights, replays raw predictions, and regenerates statistics, the Chinese report,
paper tables and the release manifest. It never runs training or paid requests.
Each new job is validated before atomic publication; repeated imports reject
changes to manifests, predictions, steps, adapter configuration or weights.

Progress and failures persist in
`benchmark/.runtime/vlm-training/validation-status.json`; console output appends
to `benchmark/.runtime/matrix-validation.log`. A past successful validation is not
proof that the watcher or training process is still alive.
The final job additionally triggers a runtime-free replay check.

For a finite validation of the current partial matrix:

```bash
benchmark/.runtime/train-env/bin/python benchmark/suite/study/follow-matrix.py --once
```

This requires the validator lock to be free. For release, the exact ten declared
condition/seed pairs, full test IDs, training budgets and merge-audit coverage
must pass; directory count alone is not sufficient:

```bash
node node_modules/tsx/dist/cli.mjs benchmark/suite/study/release-check.ts --require-complete
```

Without `--require-complete`, the manifest explicitly lists pending jobs.
Paper tables update automatically, but `main.pdf` remains a build snapshot until
the paper compilation and PDF inspection commands are run.

## Evidence Boundaries

- 337 cases contain 24 structural source objects and 25 catalog queries.
- 730 new API calls comprise 674 main and 56 control calls, not 730 objects.
- Source-group bootstrap does not establish semantic coverage or causal transfer.
- Height sorting completely solves this nominal vertical planning domain.
- Public ground-truth artifacts are a protocol boundary, not a hidden test server.
- No arbitrary CAD, force, clutch, human preference, or real-robot claim is made.
- Only jobs with a complete manifest and all predictions are imported or reported.

## Development Diagnostics

`failure-diagnostics.json` classifies 4,100 existing responses by the first
observable rejection gate, without changing scores or dropping failures.
These stages are not cognitive explanations. Base SmolVLM fails JSON/schema
on every main-study response, so zero success does not isolate perception.

`interface-probes/` stores 36 additional local text-only calls and their replay:
three tiny towers, three operations, two metadata formats, two checkpoints.
They are post-hoc calibration, excluded from the main matrix and its 4,100-row
browser audit. `observability-witness.json` supplies a hidden-tiling counterexample:
equal BOM/colored occupancy/surface signatures need not imply the same graph.
It makes no claim of identical rendered pixels.

`freeze-calibration` freezes 468 questions on 36 unused validation objects.
It does not run inference. `export-calibration` renders their permitted images
using the running suite server; `verify-calibration` checks the portable inputs
offline. The exported bundle contains 720 image uses and 144 nonblank PNGs,
with public fields, case order, recipe associations and hashes checked.
The verification report explicitly counts missing policy/size bins.

```bash
node node_modules/tsx/dist/cli.mjs benchmark/suite/study/cli.ts export-calibration
node node_modules/tsx/dist/cli.mjs benchmark/suite/study/cli.ts verify-calibration
```

Use only `calibration/inputs/public.jsonl` and its `images/` directory as model
inputs. Manifests, reviewer packets and diagnostic witnesses are evaluator
material. A complete input manifest is not a completed evaluation.
The reviewer packet contains zero completed reviews. None of these development
artifacts is a new independent confirmatory test. The clean-copy test now
replays diagnostics and probes and checks calibration inputs without `.runtime`
or a model API key; rendering and fresh inference are not repeated there.

## OpenRouter Validation Screen

The separate `model-validation/` artifacts compare GPT-4.1 mini, GPT-4.1,
Gemini 2.5 Flash and Qwen3-VL-32B on the same three calibration objects.
There are 39 primary questions per model and six reconstruction controls,
180 planned calls in total. The protocol is frozen before outcomes are observed.
This does not change the earlier 730-call study or its published scores.

```bash
node node_modules/tsx/dist/cli.mjs benchmark/suite/study/cli.ts prepare-model-validation
node node_modules/tsx/dist/cli.mjs benchmark/suite/study/cli.ts run-model-validation --paid
node node_modules/tsx/dist/cli.mjs benchmark/suite/study/cli.ts replay-model-validation
node node_modules/tsx/dist/cli.mjs benchmark/suite/study/cli.ts report-model-validation
```

Only `run-model-validation --paid` makes model requests. It shares the original
campaign ledger and exclusive `pilot.lock`, limits new validation spend to $2,
and never resets the $4.50 cumulative cap. Each request reserves a conservative
ceiling, then settles actual cost. HTTP/ambiguous billing errors stop the run
without retry; partial results and missing comparisons remain visible.
Price and supported-parameter checks precede execution. JSON mode, decoding
settings, raw replies and actual provider routing are recorded.

`model-validation/REPORT.zh-CN.md` is the generated report; `analysis.json`
contains task/variant, object-size, failure-stage and paired-control summaries.
Three independent objects cannot establish stable model rankings, and size is
confounded with geometry/policy. Conditional controls never enter primary totals.

The `prepare-ladder`, `run-ladder --paid`, and `replay-ladder` commands supply an
adaptive 2/4/8-piece reconstruction follow-up, with ordinary RGB+BOM and
privileged-symbolic tracks. It uses one other source object and shares the same
$2 validation allocation. Its 24 planned responses are not part of the fixed
180-call screen; nested prefixes are not independent samples. Preparation
renders the six task inputs and verifies oracle validity, not model ability.

The first ladder exposed an origin confound: cropping a prefix left minimum
Z=1 in the 2/4-piece scenes while the inherited image footer described a
minimum-corner origin. `originAudit` records translation-only matches without
changing any original score. `prepare-normalized-ladder`,
`run-normalized-ladder --paid`, and `replay-normalized-ladder` preserve v1
and create a separate revision with each prefix anchored at XYZ=0 and explicit
origin wording. This revision also shares the $2 allocation. Re-rendering,
wording changes and re-sampling are joint interventions, not a clean causal
estimate of normalization alone.

## Pose And Choice Diagnostics

`pose-probes/` contains 96 further calls on four unused source groups, using
distinct normalized two-piece geometries and canonical gray/blue colors.
Six conditions share each scene: full RGB structure, local RGB pose, RGB
candidate choice, permuted choice, no-image choice and privileged symbolic pose.
All candidates pass independent geometry checks, have the same part/yaw/height,
and differ in position. Correct labels are balanced across scenes; chance
expectation is 25%. Known types/BOM and explicit camera conventions narrow the
interpretation: this is not part recognition or a broad reconstruction test.

```bash
node node_modules/tsx/dist/cli.mjs benchmark/suite/study/cli.ts prepare-pose-probes
node node_modules/tsx/dist/cli.mjs benchmark/suite/study/cli.ts run-pose-probes --paid
node node_modules/tsx/dist/cli.mjs benchmark/suite/study/cli.ts replay-pose-probes
node node_modules/tsx/dist/cli.mjs benchmark/suite/study/cli.ts report-pose-probes
```

Preparation uses the running renderer. Only the `--paid` execution sends model
requests, with the existing client, ledger and lock, a $0.60 subcap, the shared
$2 validation cap and the unchanged $4.50 campaign cap. Existing runs cannot be
silently overwritten. Replay and report need no credential or runtime models.
Reports preserve X/Y/Z/yaw errors and compare actual selected poses after
permutation. Candidate information differs from generation; consistency is not
correctness and the four source groups do not establish stable model rankings.
The experiment remains separate from the historical 4,100-response UI audit.

## Six-Package Research Validation

`RESEARCH_CONTRACT.md` fixes the claims, negative-result policy and statistical
unit. `EXTERNAL_VALIDATION.md` specifies the outstanding source, reviewer,
confirmation and independent-reproduction evidence. The cumulative summary is
`../artifacts/study/governance/SUMMARY.zh-CN.md`; it explicitly remains incomplete.

```bash
node node_modules/tsx/dist/cli.mjs benchmark/suite/study/cli.ts replay-order-study
node node_modules/tsx/dist/cli.mjs benchmark/suite/study/cli.ts exposure-audit
node node_modules/tsx/dist/cli.mjs benchmark/suite/study/cli.ts prepare-human-audit
node node_modules/tsx/dist/cli.mjs benchmark/suite/study/cli.ts human-audit-status
node node_modules/tsx/dist/cli.mjs benchmark/suite/study/cli.ts research-readiness
node node_modules/tsx/dist/cli.mjs benchmark/suite/study/clean-test.ts
```

The 192-call order study pairs original/repeat/permuted/no-image conditions on
12 new sources. Its complete original answers, inputs, receipts and analysis
remain in `order-study/`, outside the historical UI audit. Excess permutation
mismatch is 0.50-0.75 across four models, with source-bootstrap intervals above
zero in this development sample. The run cost $0.282100356; cumulative API spend
is $3.097410574. It shares the existing $2 allocation and $4.50 campaign cap.
No additional paid execution is needed to reproduce the scores.

The clean-copy check runs 19 commands without runtime models or an API key;
installed dependencies are shared. Technical release checks include order replay
and record research readiness separately. A technical pass never supplies absent
human labels, data rights, effective baselines or independent confirmation.
The reviewer packet has 96 candidates and zero submitted human reviews.
