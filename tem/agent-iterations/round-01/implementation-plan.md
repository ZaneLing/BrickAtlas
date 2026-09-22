# Round 01 Implementation Contract

Owner: implementation run of research-refiner. Main owns manuscript, integration,
protocol, snapshots, and git. This run only writes `benchmark/visual-repair-v1/`,
`public/benchmark/visual-repair-v1/`, and round-01 implementation/response records.

## Primary Family and Counts

One family: **visually bound minimum terminal repair**. An exact source-induced
recognized-connector graph and unavailable vertex set are public. Two terminals
are explicit. The third is the current graph ID on the candidate whose geometry
matches an unlabeled reference. Four isolated source-part views use actual
meshes and original poses; the reference camera differs from candidate cameras.
No part names, source IDs, original instance IDs, coordinates, or binding keys
are present in the native task input. Context views remain provenance assets,
not required evidence or privileged coordinates.

For each qualifying construction:

- Two missing-vertex conditions, differing by one missing/present exchange.
- Three matched visual arms: anchor, target/distractor label transposition
  (answer-changing), and distractor/distractor transposition (answer-preserving).
- Two independently drawn ID/option-order replicates for equivariance auditing.
- Thus 12 repair observations per construction, grouped as one construction,
  never 12 independent sources.
- Four native conditions: multimodal repair; no-image repair; oracle-binding
  repair; atomic binding only. Atomic-only cannot receive full repair credit.

Final construction counts are outputs of the ledger, not promised quotas.
All complete optimal repair sets must differ for a visual-changing pair and
for the structural pair; preserving pairs must have identical complete sets.
Every selected base problem must require at least two restorations. A binding
plus exhaustive symbolic solver is an explicit decomposition baseline, not
evidence of learned compositional competence.

## Frozen Sampling and Search

Population: the finite checked-in LDraw source collection, not arbitrary LEGO
designs. Reproduce the 177-candidate preparation census. Include descendants,
12--100 parts, connected recognized graph, full recorded connector coverage;
exclude any recorded unmatched intersection inside the selected induced set.
Absence of recorded intersection is not physical certification.

Order eligible candidates by a seeded content hash. Greedily keep disjoint
instance sets within each source and discard repeated aligned design signatures.
Design signatures include typed pairwise source-origin distances; unlabeled
graph-refinement signatures conservatively group repeated graph templates.
Sources sharing any contributor, design signature, or graph-template signature
form transitive dependence groups. Freeze dev/held-out groups by content hash
before structural search. Never optimize on held-out model or human outcomes.

Bounded seeded structural search: at most 512 proposals per deduplicated
candidate, up to eight missing vertices, exactly two explicit terminals and
four geometry-distinct candidate vertices; two faults exchange one vertex.
Enumerate all subsets for exact certificates. Select the first proposal
satisfying the declared visual and structural dependency tests. Log attempts,
rejection counts, selected proposal, and all excluded candidate identities.
No post-baseline suppression.

Precision rationale: for independent bounded group means the worst-case normal
95% half-width target 0.20 would require ceil((1.96/0.40)^2)=25 groups, before
small-sample corrections. If the finite resource supplies fewer, publish its
actual groups, broad sensitivity intervals and leave-one-group-out values;
do not manufacture independence by adding views. No claim of population-wide
generalization or precise effect estimation is authorized.

## Evaluation and Execution

Independent union-find semantic evaluator recomputes every restoration subset;
constructor uses reachability. Validate IDs, duplicates, feasibility, minimal
cost, complete optimum enumeration, and component sizes per optimum. Accept
arbitrary output ordering. Invalid and missing responses stay in denominators.

Versioned native JSON+PNG inputs and SHA256 receipts connect manifests to
analysis. Publish executable local deterministic baselines without paid calls.
Use a reduced roster of frozen algorithmic configurations rather than claiming
support for unimplemented model APIs. Model/human results remain uncollected.
Any retained external-run interface is provider-neutral with explicit revisions,
image policy and failure handling; no claimed results are synthesized.

Frozen legal baselines: fixed/sorted ID, numeric offset, graph-degree and
graph-repair heuristics, card-location, pixel silhouette and RGB appearance.
Oracle binding is separate. Threshold: if any legal shallow baseline achieves
>=0.80 held-out binding or full-repair accuracy, narrow claims explicitly to a
shallow-solvable binding stage and report that outcome without dropping tasks.
No hypothesis of neural-model advantage is assumed.

## Deliverables for Main

`public.json`, private `gold.json`, `sampling-ledger.json`, `dependency-audit.json`,
`study-manifest.json`, native inputs, PNGs with capture hashes, semantic scorer,
local runner/analyzer, baseline report, tests, and `README.md` in the new version.
Final counts and exact representative paths will be supplied after verification.
BA-005 and related-work manuscript integration remain main's ownership.

## Exact Integration Schema (Main May Implement Against This)

Version and folder: `visual-repair-v1`.
Family: `visually-bound-minimum-terminal-repair`.
Condition IDs: `multimodal`, `no_image`, `oracle_binding`, `atomic_binding`.
Visual arms: `anchor`, `changing`, `preserving`.
Structural arms: `fault_0`, `fault_1`. These arm names and provenance are
index-only metadata, never model-facing fields. Opaque task IDs are independently
hashed; vertex IDs are independent random four-digit values with a `V` prefix.

`public.json` is an index with `version`, `tasks`; each task has `id`,
`construction_id`, `source_id`, `dependence_group`, `split` (`dev`/`heldout`),
`replicate`, `visual_arm`, `structural_arm`, `input`, `image`.
`input` contains `graph: {nodes, edges}`, `missing`, `fixed_terminals`,
`candidate_ids` (independently ordered), `budget`, and `cost_per_vertex: 1`.
The model-facing native packet strips all index metadata, includes a fixed
question and output schema, and attaches only allowed PNG bytes and input.
`oracle_binding` adds `bound_terminal` and omits the image.
`no_image` omits both image and `bound_terminal`.
`atomic_binding` has the same image and candidate IDs but no graph or faults.

Repair output:
`{"bound_terminal":"V1234","minimum_cost":2,"budget_sufficient":true,
"solutions":[{"restored":["V2345","V3456"],"component_sizes":[10,3]}]}`.
The `solutions` array must enumerate **every** optimal restoration set.
Component sizes are checked separately for each optimum, sorted only by scorer.
Atomic output is only `{"bound_terminal":"V1234"}`.

`summary.json` supplies generated counts:
`candidate_count`, `eligible_count`, `deduplicated_count`, `construction_count`,
`source_count`, `dependence_group_count`, `dev_constructions`,
`heldout_constructions`, `dev_groups`, `heldout_groups`, `observation_count`,
`visual_changing_pairs`, `visual_preserving_pairs`, `structural_pairs`,
`node_range`, `edge_range`, `minimum_cost_range`, `optimum_count_range`.
A construction is one selected disjoint source subassembly with one
counterfactual fault pair; a dependence group is the transitive source,
contributor, design and topology-template grouping, frozen before search.
All task variants and replicates stay together.

Primary metrics: `repair_exact` (binding AND complete semantic repair correct),
`binding_accuracy`; `changing_both_correct`, `preserving_both_correct`,
`structural_both_correct`, and `factorial_all_correct` (all six cells within
an ID replicate correct). Report `repair_given_binding` only when its
denominator is nonzero; unconditional repair uses every planned observation.
`invalid_rate`, `missing_rate`, and `received_count` are explicit.
Micro scores and equal-dependence-group means are both exposed; uncertainty
is group-conditional sensitivity, not a broad-population confidence claim.

Figure input: native 1600x900 PNG with an unlabeled reference at left and
four equally sized labeled candidate cards at right. Candidate IDs are printed
only in image cards; the reference is a second camera view of the same source
part, without text naming its shape. Show anchor/changing/preserving strips
plus the exact graph/fault JSON excerpt and full output example. The changing
and preserving PNGs differ from anchor only inside two label rectangles.
Optional original-pose assembly context is clearly marked provenance-only.

The historical **15 model names** remain in `planned-models.json`, imported
from the existing roster, with one native condition contract and no unsupported
effort-mode comparisons. Unpinned provider revisions are explicitly unresolved;
they cannot submit empirical receipts until a separate run lock pins revision
and adapter details. The executable no-purchase study uses local baselines.
Planning rows are not completed or executable paid-provider claims.

## Implemented Results and Integration Notes

Construction reproduced 177 connected/full-coverage candidates and 162 without
recorded internal unmatched intersections. Greedy nested/design dedup retained
125. Bounded search selected 84 constructions from 17 sources, with 27 dev/57
held-out constructions in 5 dev/10 held-out dependence groups (15 total).
There are 1,008 repair observations, 504 native PNGs and 84 context PNGs.
Costs span 2--8 and complete optimum counts span 1--10.

Structural controls now preserve all serialization and budget. Only one element
of the missing-vertex list changes. Geometry and source poses are unchanged;
display materials are neutral gray. No recapture was needed for the text-only
structural serialization correction.

`native/{condition}/{task-id}.json` has `version`, `condition`, `question`,
`input`, `images`, `output_schema`; **no `task_id` field inside the packet**.
Use the filename stem or `study-manifest.json` observations' `task_id` and
`packet.path`. No source/group/arm metadata crosses the model adapter boundary.
There are 4,032 packets and 15,120 planned and executed local algorithmic runs.

`baseline-report.json` exposes `configurations[].{dev,heldout,all}` and metric
objects containing `micro`, `group_macro`, `groups`, `group_values`,
`ci95_group_sensitivity`, and `leave_one_group_out`.
**The predeclared held-out micro 0.80 shortcut gate fired.** Silhouette+exact
solver gets 0.9122807 micro binding/repair, 0.7829091 group macro. Appearance is
0.6315789 micro; strongest tested text-only rule is 0.4122807; oracle is 1.0.
All 15,120 receipts are algorithmic, none synthetic/model/human, no failures.
Do not suppress this result or claim a difficult visual-recognition stage.
The claim is finite-source visual-to-graph composition with readily solved
binding. Scientific novelty sufficiency remains the reviewer's decision.

Qualification is executable at `review.html` and `qualification.py`.
Six distinct reviewer slots: two per visual arm within a construction; each
reviews both ID replicates and both fault packets within that arm only.
There are 504 assignments / 2,016 packet judgments / 1,008 distinct-image
judgments planned. All remain pending. Independent adjudication rejects either
original reviewer, and exact prompt/PNG hashes and repeated-image consistency
are enforced. No human identity or response was invented.

Full machine audit: 1,008 independent union-find answers, 336 unique PNG
intervention pairs, 2,520 card views (nonblank/unclipped), 144 source mesh hashes,
all original induced graphs and source/contributor/design/template split checks.
31 focused tests and renderer/capture TypeScript checking passed. The UI canary
loaded exact native pixels and graph packets, leaving all judgments blank.
`validate_all.py` regenerates the final reproducibility record in `validation.json`.
