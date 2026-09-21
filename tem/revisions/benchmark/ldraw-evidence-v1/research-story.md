# Research story: following evidence about an identified part

Analysis version: `ldraw2-evidence-v1`. This revision is frozen before examining
any new model responses. The node-count concern was already observed in the
guide; its replication and stratification are post-hoc corpus audits, not a
new preregistered discovery.

## Main question

For the same identified part in an original assembly, do model answers follow
task-relevant visual evidence correctly, and remain correct under specified
answer-preserving changes to labels, views and color appearance?

Scope: Color and Part-type, reported separately. S/G/E provide independently
scored modular controls. Sharing an instance never implies a within-item
cross-modal inference chain.

## Two supporting questions

1. What is the total effect of hiding non-operands with a fixed camera?
   Compare full-scene and background-mask. Camera, scale, lighting and label
   placement are fixed. Visibility/occlusion can change; this is not a pure
   attention intervention.
2. Does graph performance exceed simple surface statistics and follow
   changed relational evidence? Retain all natural deletion items and compare
   the node-count baseline, a fixed-count baseline and a graph algorithm.
   Report surviving-edge strata and matched original/intervention success.

## Evidence-to-claim contract

| Existing comparison | Estimand | Potential falsification / boundary |
|---|---|---|
| operand-only / wrong-image | Accuracy against new-image gold; paired both-correct | Lower old-gold accuracy alone can be confusion. Donor color images also change shape. |
| operand-only / id-permutation | Both correct; same semantic error; two directional failures | Current labels have different lengths/layout; no pure identity-only attribution. |
| operand-only / camera or color nuisance | Correct retention with condition-specific QA | Semantic invariance does not certify a view remains perceptually decidable. |
| full-scene / background-mask | Source-cluster paired accuracy difference | CI including zero is not equivalence; intervention also reveals occluded geometry. |
| operand-only / multi-view | Fixed two-view access effect | Not adaptive tool exploration. |
| standard / graph-intervention | Both-correct against two independently derived golds | Mean accuracy difference can be zero when both answers are correct. |

No occlusion percentage or projected object area will be inferred from an
unsegmented screenshot. Any later performance-informed subgroup will be
labeled exploratory. No failed responses are removed from the denominator.

## Maximum justified contribution

The resource supplies instance-linked controlled observations, paired golds,
immutable requests and falsifiable adaptation measures. We can report measured
algorithmic controls and corpus properties immediately. Learned-model
findings require validated raw responses. Without them, the paper remains a
method/resource contribution and a concrete research protocol, not a completed
model comparison, physical certification or guarantee of CVPR acceptance.

## Manuscript responsibilities

Introduction states the questions and the measurable distinction between
evidence-following and disturbance. Benchmark documents instances/contracts.
Measurement validity reports simple priors and independent oracles.
Experiments follow the three questions above. Controls and all-task descriptive
scores remain visible in the supplement. Historical generator repairs and
request-security implementation move to supporting documentation.
