# Casebank v2 Evaluation Contract

Version: `brickatlas-casebank-2.0`. Frozen dataset and scorer hashes live in
`artifacts/casebank-v2/manifest.json`. These scores are not interchangeable with v1.

## Per-Case Ground Truth

Every case has an evaluator record, not merely a text answer:

| Field | Meaning |
| --- | --- |
| `caseId`, `spec`, `inputHash` | Case identity, source group, policy, split, condition and exact public-input hash |
| `answerSemantics` | Exact fields, symmetric parts, nonunique visible reconstruction, nonunique plan or constraint witness |
| `oracle` | One verified answer; a witness rather than the only accepted solution for nonunique tasks |
| `target`, `source` | Expected geometry and supplied starting structure, when applicable |
| `billOfMaterials`, `extents` | Type/color counts and nominal grid dimensions |
| `connections`, `nominalStudMates` | Piece pairs, stud counts, and world-space mating positions |
| `changedIds`, `preservedIds` | Edited/faulty and protected current pieces; evaluator-only |
| `symmetry` | Square yaw group {0,1,2,3}; rectangular yaw group {0,2} |
| `assemblyWitness`, `disassemblyWitness` | One executable order; alternatives are evaluated as submitted |
| `independentCheck` | Separate integer-cell occupancy/support/insertion certificate |
| `metrics`, `oracleEvaluation` | Applicable metric names and fully evaluated witness |
| `annotationProvenance`, `humanReviewed` | Procedural annotation, never falsely claimed human-reviewed |

Public `inputs-*.jsonl.gz` contains only `caseId,input`, with no spec/fault labels.
The external-model exporter adds the fixed system prompt and actual PNG paths.
The case index, GT shards and private render recipes are **not model input**.
Symbolic condition explicitly discloses the complete reference by design.

## Metric Definitions

All scores are in [0,1]. Empty/unparseable submissions remain in the selected-case
denominator. `null` means not applicable, not omitted error. Missing structure metrics
are zero. QA retains correct-field partial credit even if another required field is
malformed; exact success still requires valid types and all fields correct.

For multiset matches TP, expected count E and actual count A:
precision = TP/A, recall = TP/E, F1 = 2TP/(E+A).
If both collections are empty all three are 1. If no predictions but E>0, precision
and F1 are 0. Recall is 1 when E=0; a false positive still gives F1=0.

| Task | Metrics beyond format/valid/success | Primary success rule |
| --- | --- | --- |
| parts | partId/color/studs accuracy, field accuracy | All three typed fields match |
| relations | connected/above/contactStuds/shortestPath accuracy, field accuracy | All four typed fields match |
| reconstruct | Structure metrics below | Ordinary: visible surface + BOM + legality; layers/symbolic: full structure |
| generate | Extent, anchor, piece budget, color count, connectivity, branching, constraint accuracy | Every declared constraint AND legality |
| complete | Structure metrics, preservation, addition precision/recall/F1 | Reconstruction rule AND preservation |
| edit | Structure metrics, preservation, editTargetSuccess | Full target AND preservation |
| plan | legalPrefix, coverage, submittedCoverage, lengthAccuracy, duplicateFree | Exactly all IDs in an executable order |
| repair | Structure metrics, preservation, localization P/R/F1, restorationSuccess, trueNegative/falseAlarm | Reconstruction rule AND preservation AND exact localization |

### Structure Metrics

- `partPrecision/Recall/F1`: exact type/color/min-corner/body-footprint matches,
  multiset-safe, arbitrary IDs and yaw-symmetric orientations accepted.
- `bomPrecision/Recall/F1`: type/color count multiset overlap, ignores pose.
- `edgeF1`: exact matched endpoint pairs with matching stud count. Endpoint matching
  requires type/color/pose agreement; this is not graph-isomorphism scoring.
- `occupancyIoU`: intersection/union of nominal occupied integer cells, ignoring color.
- `coloredOccupancyIoU`: intersection/union of cell-and-color tuples.
- `surfacePrecision/Recall/F1`: positive X/Y/Z first-hit colored grid surface sets.
  This is a nominal geometry proxy, not pixel similarity or exact perspective visibility.
- `fullStructureSuccess`: exact symmetric-part multiset match and valid geometry.
- `visibleSurfaceSuccess`: valid geometry, exact BOM and exact colored surface set.
  It is a diagnostic before preservation/localization gates; not the final success.
- `countAccuracy`: 1 - |E-A|/max(E,A,1).
- `collisionFree`, `supported`, `withinBounds`: corresponding nominal geometry checks.
- `preservation`: fraction of protected source-part multiset retained exactly.
  No protected pieces means 1.
- `additionPrecision/Recall/F1`: after removing protected source matches, compare
  remaining submitted pieces with expected additions. Diagnostic only for ordinary
  images that allow alternative hidden layouts.

No part/BOM/edge similarity to a unique reference is reported as generation quality.
Constraint generation's GT is one satisfying witness. Different legal constructions
can earn full success.

### Plans

Plans are evaluated from the submitted order without a repairing sort. First
unknown/duplicate/blocked/unsupported action stops execution. `firstInvalidStep` is
zero-based, or null if no attempted step was illegal (including an incomplete plan).
`legalPrefix` and `coverage` divide accepted steps by the required number of pieces.
`submittedCoverage` counts unique known submitted IDs even beyond a failed prefix.
`lengthAccuracy` is 1-|submitted-required|/max(submitted,required).

An apparently legal greedy placement can block a later piece. The public-input
greedy baseline intentionally exposes this failure and is not replaced by GT order.
Support means at least one nominal mating stud, not load-bearing physical stability.

### Repair

Normal/changed examples are separate strata and are not disclosed in model inputs.
Fault ID arrays must contain unique strings. Modified-color and shifted topmost
pieces are exposed. Shift generation rejects poses indistinguishable from another
same-type/color current piece, preventing an arbitrary duplicate-ID labeling target.
`falseAlarm/trueNegative` apply only to normal examples; changed examples store null.
Missing responses are failures, not true negatives.

## Aggregation

The selection manifest fixes all case IDs before scoring. Duplicate predictions,
unknown IDs and changed selection filters fail closed. Missing selected cases get
explicit rows, not removal from the denominator.

Reports separate task/variant/condition/split, policy and piece-count difficulty.
Each metric includes its actual denominator. An object-cluster bootstrap (1,000
resamples, fixed seed 731) samples source-group means for success intervals.
No total blends ordinary RGB, layer disclosure and privileged symbolic conditions.
Catalog colors share their part-type cluster. Repeated variants are not independent
source objects. Intervals describe this procedural sample, not population validity.

## Known Boundaries

25 grid catalog types, no generic hinge/axle/ball, CAD surface collision, clutch
force or robot motion. Difficulty bins use piece count, not human difficulty.
Real human review is outstanding. Public-source and approximate-near-duplicate
screening do not establish contamination resistance or semantic OOD.
External submission replay proves the scorer applied to submitted JSON, not that a
claimed provider actually generated it. No missing token usage or receipts are invented.
