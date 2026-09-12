# Research Development Release

Read `../ACCEPTANCE.md` for the outcome and remaining research gates.
This release is a runnable research pilot, not a submission-ready benchmark claim.
No robotics or VLA. Existing Grid v1 and CARE-mini results retain their own rules.

## Offline Reproduction

Node 22+, parent repository dependencies installed. From `benchmark/`:

```bash
npm test
npm run check
npm run research:prepare
npm run research:baselines
npm run suite:replay
npm run suite:traces
npm run research:statistics
npm run research:clean-replay
npm run suite:build
npm run suite:start
```

The clean replay copies source/artifacts without `.runtime`, `.env`, or API keys.
It reuses installed dependencies; it is not a fresh OS/npm-install validation.
Scoring, source hashes, images, adapter hashes and portable training histories
are checked without rerunning model generation or training.

Open `http://127.0.0.1:5175` (or the launcher's reported free port).
Each recorded case has input/output/reference scenes, event actors, original
responses, source-state hashes and JSONL export. Collection unfolding is explicitly
not a model assembly plan. Historical timestamps and hidden reasoning are absent.
Training dashboards fall back to committed bundles when `.runtime` is absent.

```bash
npm run suite:ui
npm run suite:trace-ui
npm run research:ui
```

These browser checks incur no API calls and create no real human review records.
CARE-mini's older interactive action traces remain available on port 5174.

## External Models

With the suite server running:

```bash
npm run research:export
npm run research:score -- --predictions=/absolute/path/predictions.jsonl
```

Export: `.runtime/research-exports/inputs.jsonl` and `images/`, 56 frozen cases.
Each input includes system/user data, image paths, condition and task ID.
Symbolic inputs explicitly contain privileged reference geometry.
Submit `{"taskId":"...","answer":{...}}` per line. Missing cases fail; duplicates
and unknown IDs are rejected. Results: `artifacts/research/external-scores.json`.
Do not compare these scores with old `suite:score` without separating versions.

## Paid Runs

The following are OPTIONAL NEW requests, not needed for reproduction:

```bash
npm run research:run -- --paid
npm run research:paired -- --paid
```

Only the two approved small models are tested. All historical charges count toward
the persistent $4.50 cap; uncertain receipts stop the campaign. Never reset the
ledger to make a rerun fit. The paired control reuses one exact first answer and
images, then adds reflection or target-blind validation. Historical first-call
receipts remain intact, but they are excluded from new-call costs.
The arms are sequential, not counterbalanced; repeated runs are new experiments.

## Real Local Training

The committed bundles include four LoRA adapters, five prediction sets and 480
optimizer-step records. Base model is public Qwen3-0.6B at fixed revision
`c1899de289a04d12100db370d81485cdf75e47ca`.

```bash
python3 -m venv .runtime/train-env
.runtime/train-env/bin/pip install -r suite/research/requirements.txt
.runtime/train-env/bin/python suite/research/prepare_training.py
npm run suite:prepare
npm run suite:export
.runtime/train-env/bin/python suite/research/train_matrix.py
npm run research:import-local
```

The base-model download uses network and disk, not OpenRouter. Training consumes
real local resources. MPS was tested; CPU fallback is implemented but not timed.
The recipe refuses to overwrite completed jobs. Run it in a fresh checkout to
repeat training. Different hardware/kernels can produce different weights.
Training uses old Grid v1 symbolic/text tasks, not image rows or new composition
targets. Same optimizer steps do not imply equal token budget or compute.
Only multi has three seeds; base/single each have one.

## Connector Resources

```bash
.runtime/train-env/bin/python suite/research/vendor_catalog.py
npm run research:connectors
```

Only the public MIT bundled BrickNet catalog is downloaded at pinned revision.
No gated dataset access is implied. Without this optional resource, connector
tests explicitly skip and the UI reports absent ports; geometry scoring still works.

## Licensing

- BrickNet catalog: Peter Kulits, MIT; fixed revision and file hashes recorded
  in `artifacts/research/connector-import.json`. Full license: `BRICKNET_LICENSE.txt`.
- Qwen3-0.6B: Qwen, Apache-2.0; full upstream license: `QWEN_LICENSE.txt`.
  LoRA files are modified parameters trained on BrickAtlas procedural text data,
  not a redistribution of the full base model.
- Procedural structures: CC0-1.0 provenance; no licensed external model designs
  or real human review records are bundled.
- Existing repository dependencies retain their respective licenses.
