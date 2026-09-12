# Composition Grammar v1

## Identity And Scope

- Release: `composition-grammar-v1`; public procedural development data.
- 576 samples, 576 colorless translation/yaw-normalized geometry groups.
- 576 current three-round part-labeled WL-style contact signatures. These are
  implementation signatures, not a proof of graph non-isomorphism or semantic diversity.
- 8-28 pieces per sample; 15 observed types from the 25-type grid catalog.
- Grid: X/Z studs (8 mm), Y plates (3.2 mm); min-corner positions, four yaw turns.
- Splits: train 340, validation 44, test_id 96, test_ood 96.
- Eight base tasks: 4,608 instances; the declared experiment conditions yield
  8,064 task-condition instances (14 per object). Other nominal conditions on
  nonvisual tasks are aliases, not additional independent tasks.
- Generated structures have CC0-1.0 provenance metadata. No independent human
  authored models are included. This is not the gated BrickNet model dataset.

## Important Sampling Limitation

Twelve family labels do NOT represent twelve independent mechanisms.
`vertical-chain/offset-chain`, `low-terraces/wide-canopy`,
`cross-beams/forked-canopy`, and `branching-frame/mixed-grid/stepped-frame`
share geometry sampling policies within each listed group. Seeds and color schedules
can differ. In particular, a held-out `forked-canopy` label shares the cross-beam
policy with training. Report `test_ood` as the frozen label-holdout split, NOT as
verified out-of-distribution physical-mechanism generalization.

The v1 generator is frozen to preserve actual experiments. Correcting policy-level
holdouts requires v2 and new experiments; do not relabel existing scores silently.
The new release is not jointly deduplicated against all pretraining corpora or the
old Grid v1 release. Its train/test isolation is internal to this release.

## Quality Evidence

Every ordered structure passed both the main AABB checker and a separately
implemented integer-voxel checker, with contact-count agreement on all 576 models.
This is algorithmic cross-checking, not independent human review. The 200-object
human review queue has zero real submissions as of this release.

Imported BrickNet MIT annotations: 14,603 annotated part identifiers, with stud,
hole, axle, fixed, hinge and ball rows normalized without invented orientation
fields. Only 25 grid types and 576 assemblies were cross-checked for nominal
stud/hole coordinates. No general CAD collision, force, clutch or load analysis.
See `../artifacts/research/connector-import.json` and `connector-audit.json`.

## Tasks And Information

`parts` uses isolated-part images; `relations`, `edit`, `plan` use supplied
symbolic structures; `generate` uses controlled design constraints.
`reconstruct`, `complete`, `repair` compare ordinary RGB+BOM, additional layer
images, and privileged full-symbolic conditions. They are separate settings.

The visible-surface metric is a nominal colored first-hit integer-grid surface
proxy along positive X/Y/Z, not pixel similarity or an exact visibility/raytracing
proof. Alternative hidden arrangements may pass; full Part/BOM/Edge correctness
is also reported. A high surface F1 alone is not success: geometry, BOM,
preservation and repair localization must satisfy the task contract.

Generation accepts multiple envelopes/branching/connectivity/color-compliant
solutions. It is constrained design, not free-form aesthetic text-to-3D.
Editing is a fixed whole-assembly quarter-turn, not unrestricted semantic editing.
Planning is collision/support/vertical-corridor execution, not robotic motion.

## Training And Evaluation Separation

The bundled Qwen3 LoRA runs use the OLD `grid-v1` train/validation split and eight
text/structure test cases. They were not trained on these 576 composition models
and have not been evaluated as a composition generalization baseline.
The new API experiment uses four held-out objects, two models, 112 cases.
The extra same-first-answer control adds 24 requests, not 24 new objects.

Do not claim private-test contamination resistance, human design coverage,
mechanical validity, broad model ranking, or confirmatory significance.
All data, task factories and reference structures are intentionally public.
