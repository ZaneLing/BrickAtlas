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
