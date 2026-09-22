# Visual Repair v1

One source-backed family: **visually bound minimum terminal repair**. This is an
explicitly versioned extension. No sealed historical benchmark is modified.

## Task and Scope

An exact recognized-connector graph, missing vertices, two fixed terminals,
four candidate IDs, unit restoration costs, and a budget are public. Match an
unlabeled source-part reference to one labeled candidate geometry. That card's
**current** ID becomes the third graph terminal. Restore the fewest missing
vertices to connect all three terminals. Return **every** optimal restoration
set and its own final component sizes. Isolated vertices count as components.

Native PNGs use original source meshes and poses, neutral opaque gray display
materials, a common scale across five cards, and different reference/candidate
cameras. The image does not contain graph topology. No part names, source IDs,
original instance IDs, coordinates, or gold bindings are supplied. Current
display labels, not permanent physical identities, define graph referents.
Provenance-only subassembly views are not native evidence.

This task measures a visual-binding plus exact-graph optimization composition.
It does **not** infer hidden topology from pixels or certify physical repair,
collision-free extraction, insertion, stability, or dynamics.

## Frozen Construction

| Unit | Count |
|---|---:|
| Connected, fully covered 12--100-part candidates including descendants | 177 |
| Without recorded internal unmatched intersections | 162 |
| After nested/overlap and aligned-design signature deduplication | 125 |
| Passing bounded structural search | 84 |
| Selected source models | 17 |
| Selected dependence groups | 15 |
| Development constructions / groups | 27 / 5 |
| Held-out constructions / groups | 57 / 10 |
| Repair observations | 1,008 |
| Native PNGs / provenance-only PNGs | 504 / 84 |

Each construction has two missing-vertex conditions, three visual arms, and two
independently randomized ID/option-order replicates: 12 related observations.
Graphs have 12--52 vertices and 11--74 edges; requested optima cost 2--8
restorations, with 1--10 alternative optimum sets. The whole graph, budget,
terminal order, candidate order, and all other serialization stay fixed across
fault conditions. The second fault exchanges exactly one missing/present
vertex in the same list position.

`sampling-ledger.json` records every size-eligible candidate, source/contributor
provenance, design signature, topology-template signature, exclusion, proposal
count, selected proposal, and private original-ID mapping. There are 41
bounded-search failures, not quietly removed model failures. Candidate ordering
and a maximum 512 seeded proposals per deduplicated candidate were specified
before construction and before any baseline evaluation. The first qualifying
proposal is retained. This is a gold-conditioned challenge construction, not a
uniform sample of source faults.

Typed pairwise source-origin distances, rounded to 0.01 mm, conservatively
identify duplicate designs. Iterated unlabeled graph refinement conservatively
groups topology templates; collisions merge rather than separate groups. Sources
sharing any credited contributor, design signature, or topology signature form
transitive groups. Groups are frozen before fault search; every replicate and
intervention stays within its construction and split. These signatures do not
prove semantic independence of every possible design similarity.

The precision illustration targets a worst-case normal 95% half-width of 0.20
for bounded independent group means, requiring 25 groups even before
small-sample corrections. There are only ten held-out groups. More views cannot
fix that limitation. Claims are restricted to this finite checked-in source
resource, with group-conditional bootstrap sensitivity and leave-one-group-out
values, not broad unseen-design population inference.

## Controls and Conditions

- `anchor`: original randomized candidate labels.
- `changing`: transpose target and one distractor label. Complete optimum sets
  are disjoint from anchor under each fault.
- `preserving`: transpose the other two distractor labels. Complete answers,
  including all component results, equal anchor.
- `fault_0` / `fault_1`: identical image and all text except one missing-vertex
  exchange. Complete optimum sets are disjoint under every visual arm.
- ID replicates: independently randomized vertex IDs and ordering. Private
  mapping-back checks full optimum-set equivariance.

The two visual interventions edit exactly two label boxes, with no other pixel
changes. Matched PNGs are reused across faults. There are 336 semantic changing
pairs, 336 preserving pairs and 504 structural pairs, but only 168 unique PNG
pairs per visual intervention type. Counts are not independent sample sizes.

Native condition IDs:

| Condition | Supplied Input | Required Output |
|---|---|---|
| `multimodal` | Graph/fault packet + native PNG | Binding + every optimum |
| `no_image` | Identical graph/fault packet, image withheld | Binding + every optimum |
| `oracle_binding` | Graph/fault packet + explicit true binding, no PNG | Binding + every optimum |
| `atomic_binding` | Same PNG and candidate IDs; graph/fault withheld | Binding only |

Full symbolic graph information is privileged relative to an image-only
assembly task, but not sufficient here without a binding. The oracle condition
explicitly completes that missing information. An atomic match is not a repair.

```json
{
  "bound_terminal": "V1234",
  "minimum_cost": 2,
  "budget_sufficient": true,
  "solutions": [
    {"restored": ["V2345", "V3456"], "component_sizes": [10, 3]}
  ]
}
```

IDs above are format examples, not a released task answer. `evaluate.py`
independently recomputes optimum sets using union-find. Constructor certificates
use bitset reachability. Output order is irrelevant; duplicates, unknown or
present restoration IDs, infeasibility, nonminimal sets, missing optima,
incorrect costs, incorrect component sizes, and malformed values fail.

## Execution and Traceability

Run from repository root with the existing no-network environment:

```sh
env -u PYTHONPATH PYTHONNOUSERSITE=1 benchmark/.runtime/mlx-env/bin/python benchmark/visual-repair-v1/build.py
.tools/node-v22.23.2-darwin-arm64/bin/node node_modules/tsx/dist/cli.mjs benchmark/visual-repair-v1/capture.ts
env -u PYTHONPATH PYTHONNOUSERSITE=1 benchmark/.runtime/mlx-env/bin/python benchmark/visual-repair-v1/verify.py
env -u PYTHONPATH PYTHONNOUSERSITE=1 benchmark/.runtime/mlx-env/bin/python benchmark/visual-repair-v1/study.py all
env -u PYTHONPATH PYTHONNOUSERSITE=1 benchmark/.runtime/mlx-env/bin/python -m unittest discover -s benchmark/visual-repair-v1 -p 'test_*.py' -v
```

Python uses NumPy and Pillow, with the exact tested versions in
`requirements.txt`. The renderer uses the root locked Node dependencies and
installed Chrome. Capture starts and stops its own Vite server on port 5187
(`CAPTURE_PORT` overrides it), checkpoints per construction, and resumes only
when render/spec hashes match. `--restart` deliberately rerenders this new
version only. GPU/browser changes can alter pixels; record and refreeze new
capture hashes rather than claiming cross-platform pixel identity.

`native/{condition}/{task-id}.json` contains `version`, `condition`, `question`,
`input`, `images`, `output_schema`. Task ID is the filename stem, never an
extra model-facing token. The index and `study-manifest.json` map tasks to
construction/split/dependence metadata. `captures.json` records source poses,
cameras, reference/card rectangles, source hashes, renderer hash and PNG hashes.
`dependency-audit.json` checks all public answers, original induced graphs,
source/mesh hashes, split disjointness, ID equivariance, clipping/nonblank
cards, and pixel intervention masks.

`study.py freeze` produces 4,032 native packets and a content-locked manifest
for 15 executable deterministic local configurations, one attempt per task.
`run` reads only allowed native inputs and pixels. `analyze` reads separate gold
and verifies exact packet/image hashes, study lock, code revision, settings,
condition, repeat and evidence kind. Missing, invalid, refusal and transport
failure outputs remain in planned denominators. Duplicate, synthetic, and
off-version receipts are rejected, not silently included. Synthetic unit
fixtures never write empirical receipt files.

`all` also freezes the pending qualification queue and validated eligibility
artifact before analysis. Do not use the empty-queue regeneration workflow
after real human judgments have been collected. The source lock now includes
the joint estimator; changing locked sources requires refreeze and a real
algorithm rerun, not manual receipt-hash replacement.

`planned-models.json` retains 15 historical planning model names: 13 multimodal
models with four native conditions and two text models with only no-image and
oracle conditions. No backend revision is invented and no effort comparison
is claimed. These are **uncollected planning rows**, not executed provider
configurations. All model/human results remain null.

`portable.py` supplies the common manifest-to-analysis contract for future
explicit local adapters. `lock` requires a stable model revision, adapter file
hash, all settings and validated construction eligibility before collection;
`collect` additionally requires
`--execute-local-adapter`. The adapter consumes one JSON object on stdin with
model/revision/settings, native text and full PNG base64 bytes and emits raw
model JSON on stdout. No source index or gold is sent. Timeout/nonzero exit and
malformed stdout remain planned failures. The package contains no vendor SDK,
credentials, paid call, or fabricated model adapter. Unsupported providers
remain pending until a real adapter/revision is authorized and locked.
Versioned `diagnostics` retain stdout/stderr, exact stream bytes in base64,
return code and partial timeout output, including unsuccessful attempts.
No successful-only retries are used.

## Metrics and Observed Baselines

`repair_exact` requires correct binding AND the complete semantic solution.
Report `binding_accuracy`, changing/preserving/structural `*_both_correct`,
and `factorial_all_correct` over all six cells within one ID replicate.
Preserving scores require two correct answers, not mere answer equality.
`repair_given_binding` is undefined for an empty correct-binding denominator.
Micro and equal-dependence-group means are separate; intervals resample
dependence groups, retaining all shared-anchor cells. Atomic binding does not
receive repair credit. Its duplicated fault packets are not independent visual
exposures. Failure rates and received/planned counts are always explicit.

The additive `visual-repair-interface-v1` schema joins isolated atomic binding
(A), oracle exact repair (O), and multimodal exact repair (M) on the **same
task/cell/ID replicate/attempt** under one compatible run lock. It records all
eight A/O/M contingency counts, eligible task/group counts, and
`P(M=0 | A=1,O=1)`, not a product of marginal accuracies. It also implements
same-task multimodal-minus-oracle repair and multimodal-minus-atomic binding
contrasts. Equal-group weighting is primary; micro weighting is separate.
All three readouts use shared whole-group bootstrap draws. Empty eligible
sets give null estimates. This diagnostic is operational, not proof of an
internal causal mechanism.

Both full and common construction-qualified sets are emitted. Existing
full-set configuration keys are retained; qualified counterparts and new
`interface` records carry denominators. See [ANALYSIS.md](ANALYSIS.md) for
exact machine fields, eligibility provenance, zero-eligible resampling,
failure handling, and the paper-table mapping.

The frozen shortcut threshold is **0.80 held-out micro binding OR exact-repair
accuracy**. Exact repair cannot exceed binding, so the implementation checks
binding. Group-macro values are also reported, not used to move the gate.

All 15,120 local algorithmic responses were executed and retained, with no
invalid/missing outputs:

| Rule | Held-out Micro Binding | Group Macro |
|---|---:|---:|
| First card/location | 0.2281 | 0.2364 |
| Shape/silhouette descriptor | 0.9123 | 0.7829 |
| RGB histogram/area | 0.6316 | 0.5461 |
| Highest repair-cost candidate, text only | 0.4123 | 0.3921 |
| Oracle binding | 1.0000 | 1.0000 |

Each repair baseline composes its predicted binding with an exhaustive public
graph solver, so its exact-repair score equals its binding score. This is a
decomposition baseline, not a learned-reasoning result. Sorted-ID, +12 offset,
nearest-ID, degree, lowest-repair-cost and seeded rules are also fully reported.
Pixel label reading uses only an independently rendered generic font atlas and
legal image crops, never capture-label metadata. Appearance and silhouette
rules use simple foreground descriptors, not source meshes or gold.

**The silhouette gate fired.** All tasks are retained and no held-out-based
reselection was performed. This release must not claim a difficult visual
recognition stage. Its remaining falsifiable question is whether a system
correctly composes the readily available binding with full graph optimization,
and preserves correctness under the independently controlled interventions.
This limitation can still constrain novelty; code completion does not dictate
the independent review verdict.

## Human Qualification

`qualification.py queue` creates six real-reviewer slots, not six invented
people. Every construction assigns two distinct slots to each visual arm.
Each reviewer sees four packets within that arm: both ID replicates and both
faults. No reviewer sees another visual arm of that construction. Thus 504
assignments cover 2,016 packet judgments and 1,008 distinct-image judgments.
Repeated fault images share binding evidence and prompt hashes remain exact.

Open `/benchmark/visual-repair-v1/review.html` with the root Vite server to
review an assigned queue and export raw human receipts. All fields start
unanswered. The validator checks reviewer identity/slot consistency, prompt
and PNG hashes, no cross-arm exposure, four quality flags, repeated-image
consistency, binding agreement, and complete assignment denominators.
Any negative flag or wrong binding requests adjudication. The adjudicator
must be distinct from both original reviewers; an additional audit person
is allowed. Adjudication requires exact prompt hashes and a reason.

```sh
env -u PYTHONPATH PYTHONNOUSERSITE=1 benchmark/.runtime/mlx-env/bin/python benchmark/visual-repair-v1/qualification.py validate --receipts path/to/real-receipts.json --adjudications path/to/real-adjudications.json
```

All current human assignments are pending; zero constructions are
human-qualified. Machine nonblank/clipping checks and a different part number
do not prove unique human-visible geometry. Any later qualification exclusion
must be disclosed at construction level with full-machine and qualified-subset
denominators. No measured model outcome may determine exclusion.

Validation also produces `qualification-eligibility.json` from the raw
receipts/adjudications, queue lock and base study lock. It distinguishes
pending, needs-adjudication, rejected and qualified constructions.
`study.py analyze --eligibility ...` validates the artifact before producing
both branches. Portable `lock --eligibility ...` embeds it before collection;
the full set is still collected, and later analysis cannot replace that
run's qualification snapshot. Pending constructions are not called rejected.

## Closest-Work Boundary

VisualFLIP already studies answer-changing image pairs; LEGO-Puzzles already
studies multistep brick reasoning; PhyBlock studies assembly/diagnosis/planning;
BrickNet supplies graph-backed source designs at much larger scale. Source
realism, paired accuracy and brick imagery are not novelty claims here.
The implemented distinction is an exact public graph with deliberately withheld
visual terminal binding, complete optimal repair-set semantics, crossed visual
and fault interventions, explicit atomic/oracle withdrawal conditions, and
source/contributor/design/template-held-out finite-resource accounting.
Whether that distinction is scientifically sufficient remains for review,
especially given the strong shallow decomposition result.
