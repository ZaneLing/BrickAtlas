# Research Contract

Version: `structural-measurement-1`. Established after observing the published
pilots and pose probes. Those results are development evidence, not a
preregistration or independent confirmation of this contract.

## 1. Question And Position

The central question is whether measurements under different observation,
representation and output protocols on the same brick object support the same
conclusions about structural ability. Eight task families organize the resource;
their count alone is not the novelty claim.

| Prior work | Established contribution | BrickAtlas difference to investigate | Not claimed |
| --- | --- | --- | --- |
| BrickGPT, ICCV 2025 | Text-conditioned brick generation, stability-aware checks/rollback, StableText2Brick | Protocol-level evaluation across generation, local understanding and downstream edits/plans | First brick generation or physical stability method |
| BrickNet, CVPR 2026 | Human-designed LDraw dataset, broad typed connectors, graph-backed generative programs | Input/output and evaluator validity, rather than a replacement connector representation | Richer geometry or equivalent coverage |
| Break and Make, ECCV 2022 | Interactive inspection, disassembly and reconstruction in LTRON | Separate static submissions, fixed feedback, candidate queries and executable plans | First interactive structural understanding |

Verified primary abstracts on 2026-09-13:

- https://arxiv.org/abs/2505.05469
- https://openaccess.thecvf.com/content/CVPR2026/html/Kulits_BrickNet_Graph-Backed_Generative_Brick_Assembly_CVPR_2026_paper.html
- https://arxiv.org/abs/2207.13738

This is the closest-work core, not a systematic completeness claim. A final
literature survey must add task-specific reconstruction, program synthesis and
spatial-reasoning benchmarks before claiming an unstudied problem.

## 2. Falsifiable Claims

| ID | Testable statement | Supporting evidence required | Failure interpretation |
| --- | --- | --- | --- |
| H1 | Output protocol changes per-object success patterns | Paired objects, consistent information accounting, independent replication | No stable effect means no protocol advantage claim |
| H2 | Candidate reordering adds instability beyond repeated sampling | Same-order repeat and reordered conditions, shared candidates, balanced order/labels | Reordering no worse than repeats means do not attribute instability to order |
| H3 | Visual acceptance need not determine internal graph relations | Constructive equivalent-observation witnesses plus independently calibrated acceptance | Witness establishes possibility only, never prevalence |
| H4 | Global similarity may overstate editing/completion ability | Copy-input baseline, changed-region metrics, correct/incorrect human judgments | No improvement over copy prevents treating high F1 as task competence |
| H5 | Multi-task training transfers to excluded tasks | Effective baseline, matched budget, disjoint source groups, repeated seeds | Existing negative leave-edit result stays negative; loss reduction is insufficient |

H1 and H2 are the immediate measurement study. H3/H4 support interpretation.
H5 is a secondary hypothesis, not a prerequisite positive result. No result is
required to rank models by size or by a preconceived order.

## 3. Data And Information

Procedural grid data controls geometry, not semantic realism. Human-designed
data is a separate generalization layer requiring permission and actual assets.
Use source objects as the split/statistical unit, including all derived prefixes.
Record trained, validation-observed, test-observed and merely prepared objects
separately. Public pilot/test data cannot be relabeled a hidden confirmatory test.

RGB+BOM, symbolic geometry, candidate lists, decomposition and tools provide
different information. Never pool them. Candidate success cannot be causally
attributed solely to a shorter output. Two-piece generation does not establish
a long-sequence bottleneck. Camera conventions and origin semantics must agree
with images, instructions and scoring.

## 4. Statistical Contract

- Primary endpoints: task success, paired object-level agreement and changes.
- H2 endpoint: permutation mismatch minus same-order-repeat mismatch, paired
  within each object/model. Return null for missing pairs, not invented zeros.
- Report individual seeds/models, actual groups, missing responses and truncation.
- Cluster all derivatives by source. Do not manufacture sample size from colors,
  views, task variants, option permutations or model responses.
- Report uncertainty without claiming power from a small sample. Plan a new
  confirmation using effect size and precision, not a universal sample quota.
- Additional protocols after inspecting outcomes remain adaptive development.
  Freeze selection and analysis before calling models, retain all outcomes.

## 5. Independent Validation

Two implementations sharing geometry assumptions do not prove human validity.
Human review must cover alternative correct answers, malformed answers, local
edits and no-op baselines. Version-specific blinded labels, disagreement,
adjudication and uncertain outcomes are retained. Templates and UI are not labels.
Copied-runtime-free checks and external independent reproduction are distinct.

## 6. Delivery Decision

Public reports must show separate gates for technical verification, construct
validity, source permissions, model coverage, independent confirmation and human
review. All required gates must pass before a submission-ready claim. The
readiness gate is an internal evidence check, never an acceptance predictor.
Preserve the full report and move historical pilots to supplement for a concise
main paper; verify venue rules at actual submission time.
