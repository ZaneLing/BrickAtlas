# Evidence-v3: frozen design before assignment, QA and inference

Controlling review: `CVPR_EVIDENCE_V2_REVIEW.md`.
Version: `ldraw2-evidence-v3` / `brickatlas-display-v3`.

## Preserved and changed components

Preserve every earlier release byte. Color's 73 pairs, exact image/text
observations and geometry remain the display-v2 component. The graph inputs,
12/61 partitions and historical 617-item dossier remain frozen components.
No existing genuine human or model result is present or transferred.

Part-type's 67 primary pairs receive new option order, candidate swap
assignment, endpoint IDs, render metadata, native images, wire records and
human lineage. Rebuild both primary arms. The 67 auxiliary position-panel
observations retain their exact display-v2 image/text content and separate
reference-interface interpretation.

Canonical identity remains evaluator provenance. All visual questions select
the current image referent. New image rendering changes labels only within a
fixed family pair; source geometry, pose, camera and underlying pixels are fixed.

## Part-type assignment: preregistered finite optimization

Enumerate every permutation of the four candidate options and every
source-type-nonmatching swap candidate. Candidates must already belong to the
visible operand set, have an on-screen anchor, and preserve exactly one
source-type match. Visual answerability still requires human QA.

Select exactly one configuration per parent using mixed-integer optimization.
The following acceptance bounds are frozen before assignment is solved:

1. A and B gold differ on all 67 pairs.
2. Each arm's four choice counts is 16 or 17.
3. Every off-diagonal A→B transition count is 5 or 6; diagonal counts are zero.
4. Every fixed-choice predictor's equal-source endpoint accuracy is at most
   0.30 for either arm.
5. Each declared oracle-A-conditioned shortcut has B micro and equal-source
   accuracy at most 0.40. The oracle supplies the correct A answer but no B
   image. Rules are first/last alternative option, cyclic next/previous/two-ahead
   choice, smallest/largest alternate label, closest/farthest alternate label
   number relative to target, nearest/farthest alternate source bounding-box
   center, and nearest/farthest alternate projected anchor.

The objective is minimum sum of integer SHA-256-derived configuration costs.
Configurations and variables are sorted by parent ID, option-label tuple and
swap instance ID. Solver version, objective, optimality status and complete
assignment are recorded. The solver is deterministic in the checked runtime;
the immutable assignment file is the cross-runtime authority. If no feasible
assignment is found, stop and revise the versioned design with an explicit
record; never relax a bound silently or choose a seed based on model results.

These bounds are design checks, not statistical significance thresholds or
a claim to rule out all shortcuts. The joint matrix implies a global
in-sample ceiling of at most 24/67 for any deterministic B predictor using
only the A choice ID. It does not bound arbitrary models with more features.

Audit every family/arm's marginals, transition matrix, fixed-choice scores,
declared rule predictions, source-macro intervals and per-item errors.
For Part-type, rederive the audited features independently of the chosen
assignment and enforce the bounds before wire sealing and live inference.
Report frozen Color's audit separately; do not retroactively optimize Color
or claim that a Part-type design bound is a Color acceptance threshold.

## Human exposure independence

Use six distinct initial reviewers. Every endpoint receives two judgments,
and no reviewer sees more than one observation from a parent, including its
auxiliary position panel. Thus A/B reviewer sets have empty intersection.
Distribute different arms across reviewer combinations; no slot denotes an arm.
Validate exposure on assignments and on imported reviewer identities.

Preserve raw judgments, native-size attestations, checks, agreement and
oracle-conflict blocking. Up to three additional adjudicator slots are used
only for disagreements. An adjudicator cannot be an initial reviewer and
cannot see multiple observations of a parent. Validate this in exports,
imports and final reconstruction. Actual human judgments remain required.

## Model inclusion and single-call estimand

Freeze a nonempty model roster and adapter files before inference. Include
exact requested and expected served revisions, provider/API endpoint, native
image/detail policy, temperature, token/time budget, single-attempt policy,
run IDs and inclusion reasons. Primary visual, no-image dependency control
and graph runs are planned explicitly per model.

The final analyzer requires exact equality between planned and observed run
sets, validates all adapters, requests, receipts, QA and roster hashes, and
produces a one-to-one model-run index. Missing/extra models or runs block
empirical paper tables. All scheduled attempts, including API errors,
timeouts, refusals and malformed outputs, stay in the denominators.
Interrupted runs must be explicitly closed with immutable missing-attempt
records; they cannot be removed or replaced by a favorable repeat.

Choose the review's single-call option: one complete frozen invocation set
per model and condition, no retries, no best-of selection. Temperature zero
does not imply provider determinism. Source intervals concern source
variation within this evaluation, not cross-call ranking stability. An
interval containing zero does not support a directional ranking claim.

## Author dependence and geometry inventory

Keep equal-source estimates primary. Freeze primary-author grouping from
the recorded credits and report author-macro, author-cluster bootstrap and
leave-one-author-out sensitivity. Explicitly retain secondary OMR editor
credits and add contributor-connected grouping as a sensitivity check.
Publish all source-pair part-inventory weighted/set Jaccard similarities.
These are transparent overlap diagnostics, not a new source split or a
claim that matching part inventories imply identical geometry.

## Publication acceptance

Keep Color, Part-type and text-graph results separate. Put answer-position
audits, actual denominators and roster completeness next to main experiment
tables. Preserve bounded two-family claims. No human/model results, favorable
rank changes or completed empirical criteria may be inferred from fixtures.
Update the English paper, short supplement and evaluator site after
implementation and verification. Real QA and provider collection remain
separate empirical acceptance requirements.
