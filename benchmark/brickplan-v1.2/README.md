# BrickPlan 1.2

Auditable assembly-order diagnostics with matched image+ID and structured tracks.
This is a research diagnostic release, **not a completed VLM/human study or a
claim of deep-search hardness**. Frozen 1.0 and 1.1 are unchanged.

- 3 original-source structures, 2 provenance groups.
- 15 episodes: full, checkpoint, injected repair, healthy, reconfiguration.
- 87 probe responses: 3 choices, 72 continuations, 12 counterfactual members.
- 36 matched continuation pairs resist the demonstrated first/last shortcut.
- 342,704 reachable states and 2,843,080 directed transitions.
- The privileged static relation rule still completes all 15 episodes.

Read [paper.pdf](paper.pdf), [APPENDIX.md](APPENDIX.md),
[PROTOCOL.md](PROTOCOL.md), [VALIDATION.md](VALIDATION.md) and
[REVIEW-RESPONSE.md](REVIEW-RESPONSE.md).

## Start the workcell

From the repository root:

```bash
env -u PYTHONPATH PYTHONNOUSERSITE=1 benchmark/.runtime/mlx-env/bin/python \
  benchmark/brickplan-v1.2/server.py --port 8768 \
  --track image-id --store tem/brickplan-v1.2/sessions
```

Open http://127.0.0.1:8768. Images are rasterized from the locked original LDraw
triangles, with assembly poses unchanged. The first render compiles the tiny
C z-buffer with `cc`; Python requires NumPy and Pillow. No network image or
provider service is used.

The same four image panels are presented to people and API clients. Select
P-piece and S-site IDs. Rejected structural actions also cost an action.
Inspect changes the camera and costs one inspection. Exploded reference is
a reference diagram; installed assemblies never explode.

For the structured control, use another port and a separate store:

```bash
env -u PYTHONPATH PYTHONNOUSERSITE=1 benchmark/.runtime/mlx-env/bin/python \
  benchmark/brickplan-v1.2/server.py --port 8769 \
  --track known-pose-structured --store tem/brickplan-v1.2/structured
```

Add `--study` and use a fresh store for scored collection. Study mode blocks
repeated task starts and post-trial scores/replay. Keep the policy host separate
from evaluator files and other observation-track servers. Practice scores are
intentionally visible after an episode; practice data are not hidden evaluation.

## Evaluate a collected run

```bash
env -u PYTHONPATH PYTHONNOUSERSITE=1 benchmark/.runtime/mlx-env/bin/python \
  benchmark/brickplan-v1.2/collect.py --store tem/brickplan-v1.2/study-run \
  --metadata my-study-metadata.json --output my-submission.json
env -u PYTHONPATH PYTHONNOUSERSITE=1 benchmark/.runtime/mlx-env/bin/python \
  benchmark/brickplan-v1.2/evaluate.py my-submission.json --output my-report.json
```

If practice has multiple runs of a task, pass `--selection` with an explicit
private task-ID → session-ID mapping; collection refuses silent best-of-N.
Do not combine image and structured records in one report.

Browser downloads contain public action/result history without occupancy
bitmasks. Administrative collection reads the authoritative private run store.
The public download is for user review, not a substitute for server-side
certified submission collection.

## Model-study adapter

`client.py` supplies public episode/probe calls, including budgeted inspections.
`study.py template manifest.json` writes an unfilled preregistration manifest.
`study.py run manifest.json` invokes a user-specified JSON-over-stdin adapter:
input contains public observations, prompt, history and declared settings;
stdout must contain one action JSON object (or one probe answer).
Image bytes must be placed into the provider's image-message fields by the
adapter. The adapter must enforce provider token/currency limits. No paid
provider was invoked during this release.

For probes, pass `--probes`; a response `{"type":"inspect","view":"top"}` requests
a budgeted view before answering. `study.py analyze ... --output summary.json`
produces descriptive repeated-run summaries without unsupported confidence
claims from two source groups.

## Reproduce software evidence

Use the Python interpreter shown above for these scripts:

1. `build.py` deterministically reconstructs tasks and checks every goal table.
2. `validate.py` checks semantics, public pair matching, online events and isolation.
3. `controls.py` runs exact, static, bounded-search and public/random controls.
4. Start a **fresh validation server** on 8768, then run `check_http.py`.
5. Run `.tools/node-v22.23.2-darwin-arm64/bin/node benchmark/brickplan-v1.2/check_browser.mjs`.
6. `documents.py` regenerates tables and original-geometry replay figures.
7. Compile `paper.tex` with `benchmark/.runtime/tectonic`.
8. `freeze.py` records hashes only after acceptance evidence is present.

Evidence lives under `tem/brickplan-v1.2/validation/`. Discovery and negative
mechanism findings are archived under
`tem/research/20261005-brickplan-revision/`.

## What remains open

New mechanisms challenging the static relation rule, additional independent
source families, physical construction validation, and preregistered VLM/human
studies remain open. Longer repair traces and deeper mandatory assembly chains
do not establish internal reasoning depth. See the explicit response ledger
before using the release to support a publication claim.
