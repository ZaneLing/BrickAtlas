# Outstanding Validation Contract

This document specifies remaining work, not evidence that it happened. Current
development results remain available regardless of future positive or negative
findings. The six-package readiness report is authoritative about missing gates.

## 1. Licensed Semantic Sources

The data coordinator must supply actual structure files, source revision,
content hashes, applicable license or written permission, and permitted uses.
Training, evaluation, derived-data redistribution and original-file redistribution
must be distinguished. Do not publish permission correspondence containing
private contact details. A public paper, code license or connector annotation
does not establish rights over a separate human-designed model collection.

BrickNet's available DATA.md describes a gated dataset request:
https://forms.gle/dm4eYSa5gh4DqzRT6 .
Submitting an application is not a grant. No application is submitted on behalf
of an unnamed institution. StableText2Brick is also a candidate, not a licensed
integrated asset in this release.

After permission, the implementation still needs an audited importer, units and
connector mapping, explicit unsupported-part rejection, family-level provenance,
cross-split duplicate checks, and rendered/structural spot checks. Do not silently
flatten unsupported human designs into the 25-type grid domain and claim coverage.
Semantic labels need their own provenance and review. Source-policy checks only
validate declared fields; a responsible person must verify the underlying rights.

## 2. Human Review

The review coordinator assigns at least two genuinely independent people.
Packet: `../artifacts/study/human-audit/packet.json`; images are relative to
`../artifacts/study/inputs/`. The packet contains 96 candidates from 48 cases,
not 96 independent objects, and does not cover all task variants.

Reviewers inspect the public input, images, candidate and reference without
consulting automatic scores. A reference is not necessarily the sole valid
answer. Each submits the packet's output schema, including its actual hash,
pseudonymous reviewer code, accept/reject/uncertain judgment and specific reason.
Do not ask an LLM to impersonate reviewers or fill the human-attestation fields.
The coordinator preserves separately submitted originals and documents genuine
independence; the public source code can unblind this development packet.

Private ingestion path, relative to the repository:
`benchmark/.runtime/study-human-audit/labels.jsonl`.
`human-audit-status` validates the records, version and duplicates. It deliberately
does not certify identities or automatically resolve disagreement. Adjudication
requires a new versioned record retaining both original labels, an adjudicator,
the decision, reason and evidence. Adjudication ingestion is not implemented yet.

Before claiming metric calibration, extend the packet to cover alternative
correct answers, near-correct outputs, all key variants and the external domain.
Then compare human decisions with frozen automatic judgments, reporting false
acceptance/rejection counts and denominators, reviewer agreement, uncertainty,
source-cluster intervals and adjudications. Do not discard uncertain judgments
silently or infer a zero population error from a small error-free sample.

## 3. Confirmation Freeze

The current 12-source order experiment is adaptive development, not confirmation.
After source licensing and measurement calibration, freeze a new manifest before
model calls: independent source families, exclusions/exposure history, tasks,
candidate construction, actual camera convention, model revisions, routing,
decoding, request order, missing-data policy, endpoints and analysis code hashes.
All derivatives of a source stay in one split and one statistical cluster.

For H2, predeclare per-model mean
`D = mismatch(original, permuted) - mismatch(original, repeat)`, with D in [-1,1].
Use actual selected poses, not option letters. Share sources across models but
do not count models as extra independent sources. Counterbalance request order
and correct-option positions. Retain no-image controls and report format/missing
rates separately; an incomplete primary pair is not fabricated as D=0.
Predeclare complete-pair estimates plus worst-case missing-outcome bounds and a
minimum coverage criterion. A service failure is not a cognitive failure.

Choose sample size from the desired precision and independent-family variation,
not the desired significance. A conservative illustration for four simultaneous
means, independent bounded observations and total alpha=0.05 is Hoeffding plus
union bound: `n >= ceil(2*ln(2*4/0.05)/epsilon^2)`. At epsilon=0.10 this requires
1,016 independent sources and 16,256 four-arm/four-model calls. This is a
distribution-free planning bound, not a claim that so many suitable assets exist
or a universal required quota. Stratified/variance-based designs may need fewer,
but their assumptions and selection rule must be frozen and justified first.

The latest 192-call run cost $0.282100356; that rate is not a price guarantee for
different images, outputs or providers. Any approved design must fit the original
cumulative $4.50 cap and the shared additional $2 validation allocation.
A larger budget requires explicit new authorization, never a ledger reset.
Effective task-specific baselines and broader model coverage remain engineering
and experimental work, not tasks that human reviewers can substitute for.

## 4. Independent Reproduction

A second executor should use a clean checkout of the published commit and a
separately installed Node 22 environment, without copying the original runtime
or its API key. Follow README offline commands, including order-study replay,
type checking and tests. Record commit, OS/architecture, Node/dependency versions,
exact commands, exit codes, artifact hashes, discrepancies and date.

Share a redacted receipt and logs with no credentials or personal filesystem
paths. Separate offline rescoring, re-rendering, retraining and fresh paid model
replication: success at one level does not certify the others. Current clean-copy
checks share installed dependencies and are not this independent receipt.

## 5. Final Decision

Update gates only after inspecting actual evidence and validating new importers,
review/adjudication analysis and confirmation outputs. Final manuscript work
also includes a broader full-text literature check, justified claim scope,
target-year rules, genuine metadata and anonymization. Build success and an
eight-page main-content bound alone do not clear these requirements.
