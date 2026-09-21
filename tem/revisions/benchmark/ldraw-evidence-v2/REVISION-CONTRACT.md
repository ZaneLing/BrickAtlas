# Revision contract: current visual reference and appearance

Controlling review: `CVPR_EVIDENCE_V1_REVIEW.md`.
Dataset: `brickatlas-display-v2`. Analysis: `ldraw2-evidence-v2`.
All earlier release bytes are preserved separately.

## C1: one model-visible identity semantics

The model answers about **the object currently selected by a display reference
in the supplied image**. B-numbers are image-local reference tokens. They do
not instruct the model to recover the historical color or canonical identity
of a source instance. This rule appears in every new visual wire prompt.

Four concepts remain distinct:

1. Canonical source identity = source hash + instance ID. Evaluator provenance.
2. Display referent = the visible object currently marked by a label (or the
   specified candidate panel in the position-reference control).
3. Source truth = unchanged original source type, color, transform and records.
4. Observation answer = the visual property/reference in the current rendered
   scene. Only this is scored for the new visual task.

Primary questions:

- Color: “What color is the object currently marked Bxxxx in this image?”
- Part-type: “Which displayed candidate label currently marks an object with
  the same visible part geometry as the target marked Bxxxx? Ignore color and
  pose. Answer from this image, not from historical source identities.”

The 140 original visual task IDs remain parent IDs, not transferable response
keys. All 280 primary A/B requests receive new observation IDs, exact input
hashes, prompt hashes and QA records. Old model responses and old QA cannot
be registered as results of the new contract.

## Different family interventions

**Color: explicit rendered-appearance counterfactual.** Keep the same original
geometry, source pose, camera, labels, visibility and material settings in A/B;
change only the rendered body-color parameter between two distinct, named,
opaque palette colors. Both observations are explicitly declared potentially
edited renders. The canonical source color is preserved in provenance and is
not the question's gold. This replaces the invalid “original color” donor
interpretation with a world-state-explicit observation question. No physical
assembly or geometry is changed.

**Part-type: candidate-reference reassignment.** Preserve the target geometry
and token; exchange the displayed labels on the matching candidate and one
other candidate. The gold changes because the current candidate reference
changes. It is not a changed canonical part type.

These families never share an accuracy total or a common causal interpretation.
Color supports rendered-appearance following at controlled geometry; Part-type
supports displayed-reference following for geometry matching. Neither is
comprehensive assembly intelligence.

The historical donor mechanism may be re-expressed only as a separately named
general-referent control with new prompts. A source inventory found same-type
different-color donors for only 10/73 parents, and identical source linear
transforms for only 3/73. It cannot support a 73-item color-only claim.
The complete donor feasibility inventory is preserved for audit.

A separate position-reference Part-type control uses individual source-part
renders in fixed image panels without B-labels. It measures geometry matching
under a different reference interface; any difference is descriptive because
layout and access also differ. It does not alone identify an OCR causal effect.

## C2: frozen human review rule before model inference

The primary queue has 280 complete A/B observations; source assets are not QA.
Each reviewer sees a shuffled single-observation queue with opaque IDs, exact
wire text and pixels, but no condition name, pair membership, alternate gold,
source identity, model output or other reviewer judgment.

Two distinct independent human reviewers must supply raw decisions and
structured checks: unique visible target reference, unique visually correct
option, sufficient visibility, and absence of reference contradictions.
The imported record retains both reviews. Matching decision, visual choice and
structured checks become final; disagreement on any of these fields requires
a third reviewer's explicit adjudication, without overwriting either raw
judgment. A visually chosen answer that conflicts with the source-derived gold
blocks finalization and requires a dataset revision. Pending decisions remain
pending.

Report raw agreement and multiclass Cohen’s kappa on doubly reviewed units,
with denominators and null statistics for undefined cases; report structured
check agreement separately. A changed wire hash invalidates the old judgment.
Here the QA wire observation is the complete model-visible messages array:
exact system and user text, options, native PNG bytes, resolution and image
detail policy. Provider model/transport envelope fields are separately hashed
in each full HTTP request. The runner must reproduce the reviewed observation
inside that envelope exactly; resizing, prompt changes or image changes
require new QA. This permits identical reviewed observations across pinned
model revisions without claiming the provider's internal image processing is
observable.
The model runner requires final QA for the full planned observation universe
before real visual inference. All-denominator and both-sides-decidable
estimates remain separate, with exclusion reasons and source counts.

No synthetic/agent judgment may be imported as a genuine human review.
Software fixtures can verify the gate, not satisfy it.

## M1: graph scope and baselines

Retain every natural item and the old challenge. Reclassify the 12
degree-sequence-matched answer-changing pairs as the strong proof-of-concept
challenge; report their matched invariances separately. Classify the other 61
changed pairs as degree-visible controls. Do not pool them for a strong-graph
claim or add synthetic node labels merely to inflate source coverage.

Audit node count, edge count, degree histogram, isolates-plus-one, anonymous
1-WL refinement and BFS/union-find. Lookup baselines use held-source-out training
labels; the target source's labels cannot fit its lookup. Expose feature
collisions and per-pair records. No 1-WL-indistinguishable pair is advertised as
solvable by an anonymous message-passing GNN. Source and pair intervals remain
descriptive at the small strong-pair denominator.

## M2 and publication acceptance

For each family, publish A accuracy, B/NewAcc, Both, old-answer retention,
other/invalid outcomes, valid-format rates, counts and source-cluster intervals.
Compare A-accuracy and Both ranks with explicit ties, pairwise changes and
paired uncertainty. Generate traceable case examples only from genuine raw
responses. If unavailable, cases/rank reversals remain unavailable.

Add directly relevant contrast-set, counterfactual/consistency VQA and grounding
literature after primary-source verification. Keep a concise scientific
supplement; publish all 617 original dossiers separately as searchable
machine-readable/HTML artifacts. Stable family IDs map to declared display
names in every new schema and report.

Implementation acceptance and empirical acceptance are separate. This revision
cannot truthfully satisfy “two real nonpending reviews for every observation”
or “real model diagnostic cases” without those people and responses. Final
reports must enumerate those open evidence requirements rather than mark
them solved by tests.
