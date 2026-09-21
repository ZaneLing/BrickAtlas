# Stimulus and QA implementation acceptance

Controlling review: `CVPR_EVIDENCE_V1_REVIEW.md`.

| Requirement | Implementation evidence | Acceptance state |
|---|---|---|
| C1: current display reference | New identity contract, 347 new requests, immutable parent provenance | Implemented |
| C1/M3: controlled Color mechanism | 73 same-geometry, same-pose appearance pairs; no donor replacement | Implemented |
| Pixel control | All 73 pairs share camera, label projections and body mask; zero changed pixels outside the body mask plus one antialiasing pixel | Machine verified |
| Part-type mechanism | 67 candidate-label reassignment pairs; original pixels retained under new current-display questions | Implemented |
| Independent gold check | All 347 answers independently derived from palette instructions or source part types and current candidate references | Machine verified; visual answerability still requires humans |
| Part-type auxiliary control | 67 position-panel observations with no text in images | Implemented; access/layout confounded |
| Both-side QA universe | Every reviewer receives 280 primary observations and 67 auxiliary observations | Exported |
| Independent reviews | Two distinct reviewer slots, per-reviewer opaque random order, no gold/arm/source/model output | Implemented |
| Disagreements | Raw reviews retained; decision, choice or check disagreement requires a third reviewer; oracle conflicts block finalization | Implemented |
| Agreement | Raw agreement, multiclass Cohen's kappa, confusion counts and check agreement; primary/auxiliary denominators separate | Implemented |
| Inference gate | Recompute final decisions from retained files; reject pending, old hashes and synthetic reviews before creating a live run | Machine verified |
| Exact requests | 347 offline HTTP request snapshots independently reconstructed and verified | Verified; zero model calls |
| Browser review page | Loads all 347 units, native pixels match, navigation and hash-bound empty export pass | Machine verified; zero human judgments created |
| Actual independent human QA | 0 / 560 primary reviews and 0 / 134 auxiliary reviews | **Open empirical requirement** |
| Real model results | No new model receipt | **Open empirical requirement** |

Fourteen regression tests in `benchmark/suite/ldraw-evidence-v2/test_protocol.py`
pass, including B-only coverage, repeated reviewer identity, duplicate review,
changed wire, third-person adjudication, conflicting choices, oracle conflict,
synthetic-evidence rejection, known kappa values, invalid raw response formats,
model-revision mismatch, tampered requests and gate-before-network behavior.
Synthetic judgments exist only inside temporary test directories.

`stimulus-validation.json`, `observation-index.json`, `qa/ui-validation.json`,
`qa/initial/pending-summary.json`, and
`runs/wire-audit-final/validation.json` are the current machine artifacts.
The earlier `runs/wire-audit` is a superseded offline snapshot from before the
QA implementation was finalized; it is not a model result or the current
code-bound verification.

The claim supported now is an implemented, machine-checked stimulus/QA
protocol. Human decidability, stable model rank changes, genuine failure cases
and full-versus-QA-subset empirical agreement remain unestablished.
