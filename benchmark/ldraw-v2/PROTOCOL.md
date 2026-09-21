# LDraw-2 evaluation protocol

Status: proposed, no model inference run. The 617-item release measures modular
competencies across V/S/G/E, not within-item cross-module integration.

## Observation and request boundary

Only `public/benchmark/ldraw-v2/inputs/*.json` may enter the runner. Its realpath
loader rejects internal scoring paths. `models/*.json` is for offline scoring
and human review. `serializeModelRequest` is the only request constructor:
fixed system prompt; English question; response format; family-specific public
input; anonymous choice IDs and labels; and PNG bytes for visual conditions.
References, targetModule, capabilities, answer, evidence and evidenceDetail
are excluded. Source-data, graph and edit tasks receive no scene image.

V sees images only; S sees required coordinates/coverage/steps/evidence scope;
G sees connector records or local edges; E sees public facts/actions/budget.
An execution engine may maintain a complete scene that the model does not see.
Source records and rendering geometry are unavailable to V-model inference.

All images are encoded as PNG/base64 and deterministically letterboxed with
bilinear interpolation to the adapter's 1280 by 800 viewport. Every actual wire
body, including resized image bytes, is saved and SHA256 hashed before any
network call. Transport conversion to OpenAI or Anthropic schemas does not
introduce task metadata. API secrets are read only from environment variables
and are never saved with requests. Adapter version, exact model ID, endpoint,
checkpoint/API revision, system-prompt hash, decoding, tools (none), timeout,
image resolution, code hashes, git commit and dependency hash are recorded.

## Conditions and eligible items

`ldraw-v2-experiments.json` and its explicit task lists are the preregistration.

- Standard: all 617 items. Existing 140 visual images isolate operands at
  source poses; this is the actual legacy observation, not a full scene.
- Full scene: all 140 visual items, newly rendered original assembly.
- Background mask: identical camera, lighting and operand labels, with all
  non-operands hidden. Keep operand poses unchanged. This isolates background
  visibility without changing scale.
- Operand crop: original poses, same view direction, camera fitted to operands.
  This changes visibility and scale; it is an access comparison, not a pure
  estimate of background contribution.
- Text without image: 140 visual items; question/options retained.
- Wrong image: 140 controls with identical B-number labels but mismatched
  visual evidence. Log donor/alteration and mismatch semantics; retain original
  task answer for dependence analysis.
- Camera perturbation: 140 visual items with a fixed alternative direction.
- Color nuisance: 67 type items with image desaturation, labels unchanged.
- Two-view access: 140 items receive the crop and alternative-camera image.
  This is fixed multi-view access, not an adaptive rotate/zoom agent.
- Edge withholding: 146 edge-based items. The 87 interface tasks lack an edge
  list and are excluded. Missing evidence changes solvability.
- Equivalent edge ordering: reverse all edge records, 146 items.
- Choice ordering: reverse presentation while retaining IDs, 469 items.
- ID permutation: 576 items with B-labels, renamed in question, options, public
  evidence, action labels and pixels. Inverse-map action outputs for scoring.
  The 41 unlabeled evidence-limit/sequence items are ineligible.
- Graph intervention: 146 items. Remove a complete target-neighbor pair for
  neighbors; join two surviving components for deletion. Recompute answers
  independently. These are hypothetical input graphs, not source repairs.

The public action solver is an algorithmic control (75 items), reported
separately from API models. The 24 evidence-limit answers and 17 six-step
programs are constant controls. Their accuracy is not independent reasoning
evidence. Majority priors are estimated from this corpus and not held-out.

## Scoring and accounting

Single choice requires the exact choiceId; multiple choice the exact set
without duplicates; graph deletion an exact safe JSON integer. Actions require
legal complete execution and every goal with no prohibited facts. Valid format
and goal success are different metrics; Goal is not evidence of mechanical
planning. Missing, malformed, HTTP-error and timeout outputs score as failure.
There is one attempt per item and no automatic retries or JSON repair.
Provider receipt, raw response, token usage, latency and call counts are saved.
USD is null unless both pricing and token counts are available.

Micro is item accuracy. Primary macro is the mean of source accuracies, first
within each family. Do not aggregate away family-specific failures. This pure
evaluation release has no train/test split; any learned extension must group
all views, instances and questions from a source into the same fold.

## Paired estimators and interpretation

For every preregistered comparison, retain the intersection of eligible task
IDs, require both complete expected lists, and compare the same items. Report
A-minus-B source-macro difference (primary), micro difference (secondary),
10,000-resample source-cluster bootstrap percentile 95% intervals, and the
counts correct-to-wrong and wrong-to-correct. Use fixed seed 20260918. Resample
sources, carrying all their paired items together; never bootstrap views or
questions as independent observations. Report results per family before any
predefined all-family aggregate. D3 has only two sources.

A confidence interval containing zero permits only "no stable gain detected".
It does not establish zero contribution, equivalence, or the absence of all
scale effects. No equivalence margin is preregistered in this release; stronger
equivalence claims are therefore unavailable. A future margin needs an
independent scientific justification before results are inspected.

Compare correct, absent and mismatched visual evidence. Compare full, masked,
cropped and text-only inputs by source. If their intervals contain zero, the
claim that large background assemblies increase current item difficulty is
unsupported, not disproven universally. Edge withholding checks information
dependence; changed-answer interventions plus invariance under edge ordering
provide stronger evidence. Isolated scores cannot establish diagnostic
localization: non-target-module stability and evidence-restoration experiments
are still needed. Do not use score products, linear combinations or R-squared
to infer unmeasured within-item integration.

## Historical requests

`legacy-replay.ts` audits only a supplied manifest of authentic saved v1 wire
requests and receipt provenance. Without one, historical replay is ineligible.
Do not rebuild a deliberately leaky baseline and describe it as an old run.
Only snapshots actually containing the field/template support paired stripping
attribution. Numerical option-format changes must be declared as such.
Even a performance drop demonstrates sensitivity; shortcut use requires
item-level output transitions and competing explanations.

## Human adjudication and release status

The 251-item queue includes all 140 visual items and 111 additional flagged
items. Review label readability, color/shape ambiguity, unsupported operands
and incident intersections, recording reviewer, decision and rationale. There
are 573 physical intersection candidates. Source/oracle checks do not certify
perception, load capacity, gravitational stability, or insertion feasibility.
All full/crop images must remain paired and hash-indexed. These development
artifacts are reviewable; publication certification awaits real adjudication.
