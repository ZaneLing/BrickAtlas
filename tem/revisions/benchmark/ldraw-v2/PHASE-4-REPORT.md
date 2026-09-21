# Phase 4 report

Status: automated infrastructure and image-reproduction gates passed.
No model API calls or training were performed.

Added the executable v2 experiment plan, explicit task lists, protocol,
OpenAI/Anthropic transports, six concrete candidate adapter configs, strict
runner, condition transformations, paired statistics, historical-request
eligibility audit, rendering page/capture CLI and review queues.

## Experiment coverage and corrections

Fourteen executable conditions cover 3,147 eligible item-condition pairs.
New conditions include full-scene/background-mask/operand-crop, wrong-image,
changed-answer graph interventions and fixed two-view access. Full and masked
images share the exact camera, label projection and source poses; the crop
separately changes scale. Every visual item has paired images.

V1 plan corrections are explicit:

- Original standard visual images were already operand-isolated.
- Edge withholding/reordering applies to 146 items, not all 233 G items:
  87 interface items have a record and no edge list.
- Choice order applies to 469 items, not 542 after the integer-format repair.
- ID permutation applies to 576 items with B-labels, not the 41 unlabeled
  evidence-limit/sequence controls.
- Fixed two-view access is executable; adaptive interactive tool use is not
  implemented or claimed as an equivalent condition.
- No authentic v1 model-run manifest was available. Historical replay remains
  ineligible, with a supplied-manifest auditor ready. No artificial historical
  leaky baseline was constructed.

## Verification

Commands use `npm run --prefix benchmark/suite/ldraw-v2` with the repository's
Node 22 directory on PATH:

- `ldraw:experiments`, `ldraw:run -- --help`, `ldraw:legacy -- --help`, `check`.
- `ldraw:render`, then `ldraw:render -- --verify`: 907 images generated, all
  140 tasks independently rerendered with exact byte matches.
- `ldraw:verify-experiments`: 3,147 condition requests, 146 answer-changing
  graph interventions, 576 label round trips, 907 image hashes, 617 actual
  resized wire-body snapshots and two local mock transport fixtures passed.
- `python3 .../verify-runner.py`: all 14 conditions generated actual offline
  wire bodies; internal path rejected before any request/output.
- `python3 .../verify-statistics.py`: source-macro/micro distinction, paired
  transitions, clustered intervals and fixed-seed reproduction passed on
  isolated synthetic implementation fixtures, not benchmark model results.
- `ldraw:verify`: all 617 original source/evidence oracle checks still pass.
- `freeze.py --verify`: all 2,131 v1 files unchanged.

Evidence: `phase-4-checks.json`, `runner-verification.json`,
`statistics-verification.json`, `paired-renders.json`,
`paired-render-reproduction.txt`, `dry-runs/gpt41-standard/manifest.json`.
The actual 617 standard wire snapshots embed resized image bytes. Every live
run additionally saves raw responses, usage, latency, code/config hashes and
strict scores. Failed calls remain in the denominator; no hidden retries.

An initial render reproduction failed because the ground ShadowMaterial could
reuse a stale shadow map even with shadow updates disabled. The v2 renderer
now explicitly hides this display plane. Every image was regenerated and
rerendered successfully. Source meshes, colors and poses were not repaired.

## Evidence limits

Results remain null. Dated candidate IDs are configured; moving local/remote
aliases need a real frozen checkpoint/API revision before live use. Provider
availability has not been tested. Unknown pricing remains null.

The protocol preregisters family-first paired source-macro and micro deltas,
10,000 source-cluster bootstrap samples (seed 20260918), 95% intervals and
correct/wrong transitions. No equivalence margin is invented. Intervals
including zero imply no stable gain detected, not zero contribution.

The queues contain all 140 visual items, 111 other flagged items, and 573
source-local physical intersection candidates. Human reviewer/decision/reason
fields remain empty. Automated label geometry and source-oracle checks do not
certify perceptual legibility, near-type discrimination or physical stability.
