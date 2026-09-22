# BrickAtlas Independent CVPR Review: Round 01

## Decision

**Recommendation: 3/10. Verdict: `reject`. Confidence: 4/5.**

This is an internal simulated academic review, not an official CVPR decision.
There are **five open major issues and no critical issues**. The rejection is
about the scientific contribution, measurement design, and submission contract,
not missing model calls, human responses, or numeric table entries.

- Snapshot SHA256: `3549a54124753f0822cdd50dc29c88497e7fd733b09c9b599cc3f5f56b2a935e`.
- Base commit: `9099166328ee911d70dc785a81b918959e487ca2`.
- Snapshot verification: all 20,026 research files matched using
  `tem/agent-iterations/snapshot.py 1 --verify`.
- Prior issue disposition: none; this is the first review under this protocol.

## Review Assumption

I assume, for review only, that the declared model runs and human-review
collection were completed competently and could populate the reserved tables.
I do not assume favorable performance, agreement, answerability, ranking
reversals, significance, visual necessity, or empirical superiority. References
below to an absent task family, scorer, control, or study specification concern
construction and reproducibility, not the collection waived by this assumption.
Nothing in this review asserts that real collection occurred.

## Assessment

| Frozen Criterion | Assessment / 10 | Judgment |
|---|---:|---|
| Contribution and closest prior work | 3 | Careful provenance, but an incremental atomic paired-evidence resource; no demonstrated distinctive compositional visual construct in the primary task. |
| Construct validity | 4 | Display-local semantics are explicit. Color is a sanity check; label swapping is restricted reference selection. The complex examples are fully specified symbolic problems. |
| Depth, diversity, dependence, held-out evaluation | 4 | Genuine source diversity, but sparse tasks, reused graph templates, two-source complex coverage, and no construction-held-out primary evaluation. |
| GT, scoring, denominators, shortcuts | 6 | Existing atomic metrics and checked complex GT are strong. Complex GT verification is not a prediction scorer, and shortcut coverage is incomplete. |
| Experimental design and uncertainty | 5 | Full denominators and clustered descriptive inference are appropriate. Missing matched visual controls prevent important interpretations even with completed runs. |
| Reproducibility and source-faithful figures | 7 | Exact wires, source hashes, independent certificates, and preserved geometry are substantial strengths. The new study is not the executable sealed study. |
| Narrative, examples, CVPR format/fit | 3 | Main figures emphasize unevaluated symbolic cases rather than the primary visual task; the PDF has ten content pages before references. |

These assessments are not an arithmetic formula for the recommendation.

### Strengths

The paper accurately distinguishes 73 Color pairs, 67 Part-type pairs, 67
auxiliary panels, 219 distinct graph observations, and 617 historical dossiers.
It does not quietly count the three complex examples as primary data. It also
correctly distinguishes source identity from a current display referent.

The atomic scorer preserves failures, partitions B outcomes, leaves empty
conditional estimates undefined, and computes source-conditional means rather
than dividing two macro averages. Author/contributor sensitivity and explicit
limits on single-invocation uncertainty are useful. I found no failure in the
focused atomic parsing/statistics tests.

The complex examples contain real composition: subset optimization in CX1,
branch-dependent diagnosis in CX2, and typed correspondence plus rigid geometry
in CX3. Independent verification reproduced their certificates. The renders
retain source poses; the text explicitly avoids interpreting graph deletion as
physical extraction. These are credible examples, not evidence of a mature
compositional visual benchmark.

## Major Issues

### BA-001: The Scientific Core Is Too Narrow and the Complex Cases Do Not Repair It

**Severity: major. Status: open. Priority: 1.**

**Evidence.** `paper/main.tex:89-119,195-284,324-350` identifies the primary
families as atomic and the three cases as separate. The legal Color baseline
achieves 141/146 endpoints and 68/73 pairs without locating the target label
(`paper/main.tex:336-341`;
`benchmark/ldraw-evidence-v4-draft/single-image-color-baseline.json`).
`benchmark/complex-examples-v1/build.py:84-97,150-160,176-188` supplies the entire
graph/fault worlds or exact anchor coordinates, types, and probe axis.
`public.json` contains exactly these three cases. CX1 and CX2 share the same
36-node graph from OMR 42004; CX3 uses OMR 42061.

VisualFLIP already evaluates same-question answer-changing pairs and paired
correctness; LEGO-Puzzles already studies multistep brick-based visual
reasoning. BrickNet already supplies graph-backed human-authored LDraw data at
much greater source scale. BrickAtlas acknowledges these distinctions, but
acknowledgment does not create a new scientific contribution.

**Why it matters.** The distinctive engineering is provenance and reference
bookkeeping. The evaluated task does not require assembly composition, repair,
diagnosis, or pose recovery. Conversely, all three richer examples can be
solved after removing every render: the graph or coordinates are sufficient.
Their source realism does not establish visual necessity. An excellent score,
a poor score, or a ranking reversal on the atomic pairs would not by itself
resolve this contribution gap.

**Testable closure.** Establish one coherent, substantive primary family with
a falsifiable contribution beyond paired atomic recognition. A minimal viable
direction is source-backed compositional repair/diagnosis with a genuinely
required visual component: independently vary a visually identified
target/terminal/observation and a structural constraint, such that neither
text alone nor local part matching solves the full task. Keep complete
graph/coordinate inputs as an explicitly privileged symbolic condition.
Alternatively, adopt a different comparably substantive construct and justify
its distinction from the cited work. Require:

1. A versioned task contract, executable constructor, exact public inputs, and
   independent semantic GT, not only three manually chosen illustrations.
2. A dependency audit identifying the necessary visual and structural
   operations, with controlled instances where changing either changes the
   correct solution while the other is fixed.
3. Atomic-only, symbolic-oracle, and multimodal conditions that can distinguish
   perception failure from composition failure; conclusions must allow null
   effects and follow the observed results.
4. An explicit related-work comparison on actual inputs, operations,
   interventions, and certification, not source part count or figure quality.

Expanding the three symbolic templates, adding ornate renders, or renaming
Color/Part-type as complex reasoning does not close BA-001. No physical
simulation claim is required to close it.

### BA-002: The Controls Do Not Isolate Relevant Evidence Use or Exclude Simple Shortcuts

**Severity: major. Status: open. Priority: 2.**

**Evidence.** `paper/main.tex:343-379,542-559` describes answer-changing label
swaps, privileged oracle-A rules, no-image requests, and a panel comparison
that changes layout and visibility. It explicitly lacks a qualified
answer-preserving Part-type intervention.
`benchmark/ldraw-evidence-v4-draft/part-type-invariance-feasibility.json` reports
201 structurally eligible swaps over 67 parents, but `route_selected` and all
`selected_swap` fields are null; this is not an implemented control.
`benchmark/suite/ldraw-evidence-v3/assignment.py:67-94` audits alternate choices
after supplying A's correct answer, not legal single-image geometry selection.

A reviewer-side metadata diagnostic selecting the candidate nearest the target
in recorded projected-anchor distance identifies the matching object in 30/67
parents (44.78% micro, 45.07% source-macro); nearest 3D center gives 29/67.
Following that object's current label would preserve those successes across
both arms. These are **privileged-coordinate diagnostics, not measured legal
PNG baselines or evidence that any learned model uses this shortcut**.
The distinction matters because the existing alternate-candidate audits test
a different question. The inspected OMR 42004 native pair is one such
nearest-target success.

CX3 also has an exact numeric-ID shortcut for its four correct
correspondences: B0024 to B0036, B0025 to B0037, B0026 to B0038, and B0035 to
B0047 are all `ID + 12`
(`benchmark/complex-examples-v1/build.py:168-188`;
`paper/supplement.tex:255-266`). Telling a model that IDs supply no matching
rule does not remove that regularity.

**Why it matters.** A positive image-minus-no-image gap shows use of some image
information, not successful selection of task-relevant geometry or robustness
to irrelevant changes. Pair accuracy alone can mix geometry, label reading,
layout priors, and generic instability. This is a design limitation regardless
of whether the eventual results are favorable.

**Testable closure.** Implement matched answer-changing and answer-preserving
visual interventions with the same image access and comparable edit mechanism.
For retained Part-type, swapping two distractor labels is a concrete candidate,
subject to independent qualification. Share anchors in the manifest and retain
their dependence in uncertainty estimates. Add frozen, legal single-image
baselines using only allowed pixels/text, including a target-label/location
heuristic and a simple appearance/shape matcher; keep oracle diagnostics
separate. For any promoted complex family, independently randomize public IDs,
query/world names, option order, and output serialization while preserving
semantics; explicitly test numeric offsets, sorted-ID mappings, and fixed
query roots. Preserve original physical IDs privately for provenance.
Require semantic correctness on the preserving condition, not merely equal
answers. Thresholds and interpretation rules must be fixed before inspecting
held-out model results; unexpectedly strong shortcuts require construction
repair or narrowed claims, not suppression.

### BA-003: Source Counts and Bootstrap Intervals Do Not Establish Task Generalization

**Severity: major. Status: open. Priority: 3.**

**Evidence.** The manifest covers 24 sources, but Part-type has only 1-5 parents
per source. Reconstructing its candidate inventory gives 67 distinct source
targets and 50 target part numbers. These are useful coverage facts, not 67
independent constructions. Source/author analysis measures inventory overlap
and credit groups, not aligned subassembly or task-template duplication
(`benchmark/suite/ldraw-evidence-v3/authors.py:17-61`;
`paper/supplement.tex:395-402`).
The 12 strong graph pairs repeat six-cycle versus two-triangle constructions;
the other 61 use a weaker construction
(`paper/supplement.tex:425-488`). CX1/CX2 use one source graph, and CX3 repeats
one axle design. The primary construction jointly optimizes the full
67-parent inventory (`assignment.py:148-201`); the documented source-held-out
fits apply to graph feature lookups, not a held-out primary task study.

**Why it matters.** Source resampling and leave-one-author-out analyses are
appropriate sensitivity analyses for this fixed collection. They cannot
manufacture unseen construction diversity, rule out shared subassembly
templates, or establish robustness to new mechanisms. Public CAD contamination
is possible but not demonstrated; that risk must not be mislabeled as a
confirmed leak.

**Testable closure.** Before evaluating the revised substantive family, define
the target population and an independent construction unit. Produce a sampling
and exclusion ledger with source, contributor, subassembly-design, and
task-template groups. Freeze development and held-out construction groups;
keep all views/interventions and duplicated designs together. Demonstrate that
held-out instances vary relevant topology/constraints/solution structure, not
only IDs, colors, or source decoration. Choose the number of independent
groups from a stated precision or sensitivity target, and report uncertainty
at the appropriate grouping level with actual eligible counts. Restrict
generalization claims if the available independent groups are insufficient.
There is no arbitrary required item count and no requirement to manufacture a
significant difference.

The refiner's communicated inventory of 177 candidate subassemblies across 19
sources, including 162 without recorded unmatched intersection candidates, is
feasibility context only. I have not independently reproduced those counts.
Candidates, connector coverage, and absence of a recorded candidate collision
are not qualified independent tasks or physical certificates.

### BA-004: The Released Scoring/Study Contract Does Not Cover the Intended Scientific Upgrade

**Severity: major. Status: open. Priority: 4.**

**Evidence.** `benchmark/complex-examples-v1/verify.py:38-169` verifies stored
GT, including 256 repair subsets, 27 depth-two query assignments, and four
typed registrations. It is not an evaluator of submitted model repairs,
policies, or transforms. Searching `benchmark/suite/` finds no implementation
of these three family identifiers. The existing analyzer is roster-bound and
consumes atomic choices and integer graph answers
(`benchmark/suite/ldraw-evidence-v3/analyze.py:205-260`;
`transport.py:7-10,40-54`). The manuscript explicitly separates the sealed
three-model study from the new 15-model/mode proposal and leaves the latter's
versioned adapters and selected-input contract unspecified
(`paper/main.tex:457-466,619-646`;
`paper/supplement.tex:498-509`).

**Why it matters.** Correct GT certificates do not establish that semantically
equivalent model solutions receive correct credit. Promoting these examples
without a semantic scorer would create exact-string, alternative-optimum, and
unvisited-policy-branch errors. Competently completed hypothetical runs also
do not make an absent published execution specification reproducible. This
finding is not a request to purchase calls or populate blank cells, and I do
not allege a discovered bug in the present atomic pair formulas.

**Testable closure.** Release semantic prediction evaluators for whichever
family BA-001 makes primary, and one versioned study manifest connecting
manuscript conditions to those evaluators and exact input hashes. For repair,
check membership/duplicates, feasibility, minimality, all requested optima, and
component results independently of ordering. For diagnosis, simulate every
compatible world, verify the identified world and path cost, reject unknown or
cyclic/nonterminating policies, and allow equivalent optimal trees. For
registration, validate bijections/type constraints, proper rotations,
geometric residuals, and probe origin/direction with explicit tolerances.
Only selected families need implementation.

Add labeled synthetic unit fixtures for valid alternatives and adversarial
invalid outputs, including a correct-looking root with an incorrect hidden
branch and a reflection masquerading as a rotation where applicable. These
fixtures must never enter empirical tables. Freeze provider/model revisions,
image policy, supported effort settings, repeat/failure handling, and study
denominators; implement the manifest-to-analysis path or remove unsupported
conditions from the paper. Preserve, rather than weaken, the existing sealed
study. Verify missing/invalid planned outputs stay in the denominator and
synthetic/off-version responses are rejected.

### BA-005: The Main Paper Is Overlength and Its Visual Emphasis Misrepresents the Primary Workload

**Severity: major. Status: open. Priority: 5.**

**Evidence.** Direct PyMuPDF inspection of `paper/main.pdf` finds 11 pages:
content/tables occupy pages 1-10 and references begin on page 11. Thus this is
**ten content pages**, not an eight-page CVPR paper with extra references.
`paper/verify.py:143-159` checks content and assets but imposes no page limit.
All four main figures are a source montage and CX1-CX3
(`paper/main.tex:19-26,217-278`); the evaluated atomic visual pair is relegated
to `paper/supplement.tex:80-124`. This mismatch is disclosed in prose, so it is
not an allegation of fabricated task counts.

**Why it matters.** Readers primarily see large assemblies and complex
problems, although the primary measured visual workload is isolated color and
candidate-label matching. The layout spends scarce main-paper space on
separate examples and multiple large study-planning tables, while exceeding
the requested submission limit.

**Testable closure.** Compile an eight-content-page-or-shorter main paper under
the applicable unmodified CVPR style, with references after the main content.
Add an automated content-page check and inspect readability at final size.
Show an exact representative input, required output, and intervention for the
actual primary family in the main paper. Keep a compact explicit accounting
of primary, control, historical, and illustrative units. Move nonprimary
examples, exhaustive certificates, full inventories, and secondary result
matrices to the supplement. Reconcile both PDFs and their provenance manifests
with the same reviewed task version. Filling blank cells alone is not closure.

## Minimal Scientific Revision Set

1. **Choose and build one substantive primary family** with a required visual
   dependency and a structural/compositional dependency. Reuse genuine source
   assemblies and existing independent graph/geometry validators. Keep the
   current atomic pairs as diagnostics; do not implement all three complex
   families merely to increase breadth. Closes the core of BA-001.
2. **Design its controls and independent sampling at construction time.**
   Couple relevant changes, irrelevant changes, symbolic-oracle inputs, and
   ID randomization; freeze source/design/template-disjoint development and
   held-out groups. Include legal shallow baselines and a precision-based
   sampling rationale. Addresses BA-002 and BA-003 while making BA-001 testable.
3. **Implement semantic evaluation and one reproducible study contract.**
   Evaluate alternative solutions and all policy worlds; retain invalid and
   missing outputs; bind exact inputs, settings, and scorers. Only the chosen
   primary family and honestly retained conditions need support. Closes BA-004.
4. **Rebuild the narrative within eight pages.** Put the actual primary
   workload and conditional scientific questions first. Keep documented
   limitations and separate symbolic/physical interpretations. Closes BA-005.

This set is intended to remove every current major objection, not to guarantee
a future accept recommendation. A reviewer must still assess the resulting
task, controls, data, and claims on their actual merits. More iterations,
larger candidate counts, or optimistic placeholder conclusions do not change
the standard.

## Verification and Limits

- Read the complete reviewer skill, protocol, main paper, supplement, complex
  builder/verifier, atomic analyzer/statistics/transport, and relevant
  assignment, source-dependence, and measurement code.
- Parsed primary manifest/index data and inspected complex public/GT contracts.
  Examined CX1-CX3 figures, the exact Part-type figure, and native Color and
  Part-type stimuli, including the OMR 42061 repeated-pin example.
- Passed 11 selected assignment/parsing/statistics tests and 10 measurement/
  single-image-baseline tests. No paid API calls or human judgments were made.
- Re-executed the independent complex verifier read-only: suppressed only its
  final `verification.json` write. All 256 CX1 subsets, 27 CX2 query trees,
  four CX3 assignments, 12 full source transforms, and five capture bindings
  passed. Research files were not edited.
- Read and verified the snapshot digest; did not regenerate it. Did not
  rebuild PDFs or run browser/physical simulation. Visual inspection was a
  sample, not full human qualification of 347 observations.

Residual limitations even after repair include public-source contamination
risk, CAD-to-render visibility, dependence among reused part designs, and the
gap between a recognized connector graph and physical buildability. In
particular, the refiner reports an unresolved B0150-B0159 intersection in the
backhoe; I do not treat that report as independently revalidated here. Neither
preserved poses nor the graph certificate certifies mating, stability,
collision-free extraction, or insertion.

Human answerability rates, model advantages, rank changes, and robustness of
effects remain result-dependent under the review assumption. Null or adverse
findings must be reported; acceptance does not require inventing favorable
results.

## Closest Work Checked

1. VisualFLIP, arXiv:2606.07872v1:
   https://arxiv.org/abs/2606.07872v1 .
   Same-question answer-changing pairs, pair accuracy, and evidence dependence;
   the abstract reports 1,374 images and 24 MLLMs.
2. LEGO-Puzzles, cited version arXiv:2503.19990v3:
   https://arxiv.org/abs/2503.19990v3 .
   The abstract reports 1,100 VQA examples across 11 spatial/multistep tasks.
   The landing page also identifies a later v4; this review does not attribute
   unchecked v4 contents to v3.
3. PhyBlock, arXiv:2506.08708v2:
   https://arxiv.org/abs/2506.08708v2 .
   Progressive block assembly, diagnosis, and planning; 400 assembly and
   2,200 VQA tasks in the abstract.
4. BrickNet, CVPR 2026:
   https://openaccess.thecvf.com/content/CVPR2026/html/Kulits_BrickNet_Graph-Backed_Generative_Brick_Assembly_CVPR_2026_paper.html .
   Graph-backed assembly programs and over 100,000 human-designed LDraw objects
   and scenes. This is a different task, but it limits source provenance or
   complex CAD alone as a novelty argument.

These public abstract/proceedings pages were checked directly. They support
the comparisons above, not a claim that their complete experimental protocols
were independently audited.
