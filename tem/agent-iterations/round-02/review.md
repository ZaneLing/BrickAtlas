# BrickAtlas Independent CVPR Review: Round 02

## Decision and Binding

**Recommendation: 5/10. Verdict: `weak_reject`. Confidence: 4/5.**

One major issue remains open, BA-004. One new minor issue, BA-006, concerns
failure diagnostics. BA-001, BA-002, BA-003, and BA-005 are closed for the
actual revised scope. The fixed acceptance condition is not met.
This is an internal simulated review, not an official CVPR decision.

- Base commit: `72db15006cfa89f80922857e2b29b79d342fdd0e`.
- Snapshot: `580e214fab9f003b887a643a26ebba8b5cd13f1c18d020971300bd57ebfe8d54`.
- Independently verified: 24,697 research files.
- Study lock: `072c17c0a09681d719f87cf2273252ebc70e36c8f83e744fe63e9c388b3b49ac`.
- Reviewed family: `visual-repair-v1`, not the historical atomic benchmark.

The substantial implementation earns substantive issue closures, but does not
determine the recommendation. The remaining objection is specifically that
the implemented analysis does not yet realize the paper's central
binding--optimization interface question. It is not a demand for more tasks,
harder-looking images, paid calls, or a favorable experimental effect.

## Review Assumption

For review only, I assume the declared model runs and human collection were
completed competently and could populate the reserved tables. I do not assume
human-visible uniqueness, favorable agreement, successful qualification,
model superiority, an integration deficit, a ranking reversal, or
significance. Missing empirical values and the 147 blank cells are not
rejection grounds. No real model or human collection occurred during this
review. Construction, scoring, estimand definitions, and the executable
analysis contract remain reviewable under the protocol.

I completely read the project reviewer skill, protocol, round01 review in
both formats, response and integration notes, current main and supplement,
and the new constructor, evaluator, study, baseline, portable-adapter,
qualification, rendering and validation code.

## Assessment

| Frozen Criterion | Assessment / 10 | Judgment |
|---|---:|---|
| Contribution and closest work | 6 | A genuine, narrow visual-to-graph composition resource; the interface readout must be completed to make this contribution effective. |
| Construct validity | 7 | Binding and structural inputs each have certified answer consequences; no hidden-topology or physical-repair claim is made. |
| Depth, diversity, dependence | 7 | Actual varied source graphs and pre-search grouped holdout; ten held-out groups support only the stated finite-resource interpretation. |
| GT, scoring, shortcuts | 8 | Independent semantic recomputation and matched controls pass; strong legal shallow performance is disclosed rather than hidden. |
| Experiment design and uncertainty | 5 | Matched conditions permit a useful study, but current outputs omit the joint estimand at its center and executable cross-condition contrasts. |
| Reproducibility and geometry | 8 | Exact native bytes, source/mesh checks, semantic receipts and traceable figures; qualification-to-analysis and failure-diagnostic integration remain incomplete. |
| Presentation and CVPR fit | 7 | Six content pages plus references, centered on actual primary inputs. The contribution is substantially narrower than general visual or physical reasoning. |

These criterion assessments are not an arithmetic recommendation formula.

## Substantive Closures

### BA-001: Closed for the New Primary Construct

The prior objection was not merely answered with more symbolic illustrations.
`build.py:171-210,243-316` implements an actual task family: four-way visual
binding chooses a third terminal, then the supplied graph determines every
minimum restoration. The constructor requires disjoint optimal-set families
when either relevant input changes. A preserving label swap leaves the entire
answer invariant. Removing the image no longer leaves a uniquely specified
full task; binding alone does not enumerate repairs.

There are 84 constructions, 1,008 repair observations, and 504 native images.
Independent checking reproduced all 1,008 semantic answers. The graph
optimization is substantive even though it is small and exhaustively soluble.
Across observations, 598 have one optimum, 298 have two, and 112 have three
or more; 802/1,008 have cost two or three. These are dependent observations,
not independent complexity samples. Ranges alone should not suggest that
cost-eight, ten-optimum cases dominate.

The distinction from VisualFLIP's answer-changing pairs, LEGO-Puzzles'
spatial/sequential tasks, PhyBlock's assembly/planning, and BrickNet's graph
representation is the specific crossed binding/fault contract and complete
solution-set semantics, not bricks, CAD scale, or paired accuracy.
This is a plausible narrow benchmark contribution, not a new optimization
algorithm or difficult perception benchmark. Its scientific utility is still
limited by BA-004's missing joint-condition readout.

Evidence: `paper/main.tex:55-95,123-155,160-209`;
`benchmark/visual-repair-v1/build.py:171-210,243-316`;
`benchmark/visual-repair-v1/verify.py:17-76`.

### BA-002: Closed, With the Shallow-Solvability Limit Retained

Actual changing and preserving PNGs edit exactly two label rectangles while
holding all other pixels fixed. Fault partners reuse the same image and
exchange exactly one missing-list element. The verifier checks full optimum
sets, private mapping-back equivariance, and source/split relationships.
I reran its image/source audit with only report writing suppressed.

The legal silhouette rule reads pixels and a generic font atlas, not capture
labels, source meshes, or GT. Composing it with the public exact solver gives
624/684 held-out correct repairs, 91.23% micro and 78.29% equal-group. Its
changing, preserving, structural and All-six micro scores also equal 91.23%.
These controls therefore do not create extra difficulty for that modular
system. This is a real limitation, but the paper explicitly narrows its claim
after the frozen .80 gate fires. I do not require the baseline to fail.

No-image deterministic rules have zero changing-both-correct as expected from
identical text with incompatible gold repairs. Their individual accuracy is
not evidence that visual information is unnecessary. The highest tested
text-only repair-cost rule reaches 41.23% micro.

Native packets and the portable adapter exclude source identities, original
IDs, coordinates, arm metadata and GT from ordinary model input. Oracle
binding is explicitly separate. "Private" here means evaluator-only under the
declared input contract, not a confidential test server: the repository ships
gold and provenance. Future adapters must remain closed-book and must not
give the model repository or cross-condition lookup access. I found no actual
gold leakage in the supplied pixel baseline or native packet path.

Evidence: `build.py:243-306`; `baselines.py:14-124`;
`verify.py:33-66,120-168`; `study.py:33-50,150-170`;
`portable.py:79-88`; `paper/main.tex:267-284`;
`baseline-report.json` (independently recomputed).

### BA-003: Closed Under the Explicit Finite-Resource Scope

The ledger retains the census, coverage/intersection screens, overlapping and
duplicate-design exclusions, and bounded-search failures. Grouping precedes
search. Actual selected sources, contributor groups, design signatures and
topology signatures do not cross the split; selected instance sets within
each source are disjoint. The independent audit reproduced these checks and
the induced source graphs.

The 84 constructions come from 17 sources and 15 selected dependence groups;
held-out evaluation has 57 constructions in ten groups, not 684 independent
samples. The paper explicitly says its 25-group precision illustration is
unattained and avoids broad unseen-design inference. The signatures are
imperfect similarity controls, and search is gold-conditioned, but these
limitations are now stated accurately. No arbitrary larger item count is
required to close the old overclaim.

Evidence: `build.py:90-168,214-242,319-350`;
`verify.py:77-118`; `paper/main.tex:231-265,330-339,412-417`.

### BA-005: Closed

Read-only paper validation and direct PDF inspection confirm seven main PDF
pages: six content pages and a separate reference page. The supplement has
six pages. Both main figures now show the actual primary development
construction, with source context and evaluator GT labeled outside model
input. Provenance checks match the native packet and complete optimum sets.
The validator enforces the content-page limit and archived style provenance.

I inspected the original native PNG, both figure PNGs, and a rendered final
PDF figure page. The factorial figure's embedded native labels are very small
at print size, but its larger bound-ID and solution annotations convey the
comparison. Enlarged label insets would improve readability; this no longer
amounts to the previous workload/figure mismatch.

Evidence: `paper/main.tex:97-109,211-222`;
`paper/verify.py:37-119`; `paper/repair-figure-provenance.json`;
`paper/main.pdf:pages 3-4,7`.

## Remaining Major Issue

### BA-004: The Scorer Is Repaired, but the Interface Study Still Lacks Its Joint Readout

**Severity: major. Status: open, substantially narrowed from round01.**

The old missing-semantic-scorer objection is closed. `evaluate.py:64-135`
checks binding, membership, duplicates, feasibility, minimum cost, completeness,
budget, and component sizes independently of ordering. The native study and
portable run lock also replace the former manuscript-only conditions.
All 31 focused tests pass. The remaining issue is not an allegation that the
existing exact-repair or within-condition paired formulas are wrong.

**Evidence.** The paper asks whether isolated binding and oracle repair
predict success when combined (`paper/main.tex:20-41,77-95,350-355`) and
promises shared-group paired effects and qualified-subset results
(`330-335`). However:

- `study.py:222-251` computes pairing only among intervention cells **inside
  one condition**. `repair_given_binding` conditions on the multimodal
  response's own binding, not on success in the isolated atomic and oracle
  conditions.
- `study.py:254-295` scores each configuration independently and exports
  per-condition summaries. It never joins atomic, oracle and multimodal
  outcomes for the same task. `paper/build_tables.py:38-43` reserves only
  marginal condition columns and within-multimodal conditional repair.
- Per-group values would permit an additional paired-difference calculation,
  and raw receipts contain enough information for joint analysis. Neither
  calculation is presently implemented or given a frozen joint estimand.
  This is repairable without recollecting data, but is not already supplied
  by marginal bootstrap intervals.
- `qualification.py:141-166` produces construction qualification decisions,
  but `study.analyze` has no qualification input or full/qualified analysis
  branch. The external lock similarly retains all observations without
  binding a qualification-derived eligibility artifact. This is a smaller
  associated completion gap, especially if competent human review rejects
  some constructions; no favorable all-pass outcome may be assumed.

**Direct counterexample.** I constructed only in-memory synthetic outcome
rows for two groups, each containing two constructions and all twelve cells.
Multimodal correctness is fixed on construction zero in each group. In one
pattern, atomic and oracle successes occur on construction zero; in the
other, both occur on construction one. Calling the released `metrics()`
produces identical complete summaries for all three conditions, including
group values, intervals, both-correct metrics, All-six, and conditional repair.
Yet the joint outcome differs:

| Synthetic Pattern | Atomic-Correct AND Oracle-Correct Cells | Multimodal Failures There | Failure Rate |
|---|---:|---:|---:|
| Aligned isolated competence | 24 | 0 | 0% |
| Disjoint from multimodal success | 24 | 24 | 100% |

All three conditions have .5 standalone accuracy in both patterns. The
counterexample is a test of information lost by the current summary, not an
empirical BrickAtlas result. No fixture entered any receipt or report file.

**Why major.** This paper has deliberately relinquished hard vision and broad
physical/generalization claims. Its remaining scientific center is the
binding--optimization interface. Marginal accuracy and within-condition
intervention consistency do not establish whether the *same instances* are
solved in isolation but fail jointly. Low joint accuracy can reflect
nonoverlapping isolated competence rather than an additional combination
failure. The manuscript's cautious wording prevents a false causal claim,
but does not supply the missing central diagnostic. The matched experimental
design is capable of supporting it; the released analysis does not yet do so.

**Minimal scientific and technical closure.**

1. Freeze a task-aligned joint outcome definition. For example, let `A` be
   atomic binding correctness, `O` oracle exact repair, and `M` multimodal
   exact repair for the same task/replicate/cell. Report the joint contingency
   counts and `P(M=0 | A=1 and O=1)`, with its eligible denominator. This is
   an operational joint-condition failure rate, not proof of an internal
   causal reasoning mechanism. An equivalent explicitly justified estimand
   is acceptable. Do not substitute a product of marginal accuracies.
2. Implement joins across compatible model/run locks and construction
   membership. Add paired multimodal-minus-oracle repair and multimodal-
   minus-atomic binding contrasts, using aligned group vectors. Freeze
   micro versus group weighting, zero-eligible-group handling and missing/
   invalid-output treatment. Resample the same groups jointly, retaining
   shared images, anchors and both ID replicates.
3. Bind validated construction qualification to a common subset across
   conditions. Emit full-set and qualified-set analyses without replacing
   the full denominator; distinguish pending from rejected qualification.
   Empty qualified or jointly competent sets must remain undefined rather
   than turn into zero error or perfect performance.
4. Add synthetic regression tests for the aligned/disjoint counterexample,
   empty eligibility, missing one condition, incompatible locks and
   construction-wide exclusions. A no-exclusion case must reproduce the
   current full-set scores. Add the estimand and its conditional interpretation
   to the manuscript and released analysis schema.

No new task family, model purchase, human fabrication, significant effect,
or particular sign of a contrast is required. A zero or adverse interface
effect is a valid outcome. Properly implementing and testing this readout is
the minimal remaining major repair; it is not a promise of automatic acceptance.

## New Minor Issue

### BA-006: Failed Adapter Calls Discard Available Raw Diagnostics

**Severity: minor. Status: open.**

`portable.py:90-101` captures stdout/stderr, but a nonzero exit stores only
`response: null` and `adapter_exit_N`; timeout handling stores only the
exception class. Available partial stdout, stderr and timeout output are
discarded. An in-memory mocked subprocess returning nonzero with both streams
reproduced this loss. No adapter or model was actually executed.

Failure denominators remain correct, so this does not invalidate the present
algorithmic results. It does weaken the advertised raw-output retention and
prevents distinguishing malformed generation from transport or adapter
failure during audit.

**Closure:** retain raw stdout/stderr, return code and available partial
timeout output in a versioned diagnostic field while keeping the attempt
unsuccessful. Test nonzero exits and timeouts without actual model calls.
Do not add successful-only retries.

## Verification and Limits

- `snapshot.py 2 --verify`: passed, all 24,697 research hashes matched.
- All 31 `test_visual_repair.py` tests passed without report writes or bytecode
  generation.
- Reran `verify.verify()` with only its final report write suppressed:
  1,008 semantic answers, 336 unique visual intervention pairs, 2,520 native
  card views, 144 mesh files, induced graphs and split checks passed.
- Reran `study.analyze` on all 15,120 retained algorithmic receipts with
  `write_output=False`; the complete returned report exactly matched the
  checked-in baseline report. Native hashes and study source hashes passed.
- Reran `paper/verify.py` with only its final `verification.json` write
  suppressed: both PDFs, provenance, 15 planning models, and 147 null cells
  passed. No PDF rebuild was performed.
- Reviewed the recorded eight-stage validation. Did not rerun constructor
  generation, capture, TypeScript or browser qualification checks, since
  those commands normally write artifacts. Their recorded success is not
  presented as a fresh independent execution.
- Visually inspected native images `image-c934719659508d474833.png`
  (development), `image-53718c498709db7e16fc.png` (held-out 31028), and
  `image-5f205ebb28cfb21cc8f5.png` (held-out OMR 42066), plus both primary
  figures and the final-size factorial PDF page. The held-out examples were
  selected from silhouette failures, not asserted to be human-ambiguous.
- The cross-condition counterexample and adapter-failure checks were
  ephemeral synthetic tests only. PDF inspection rasterizations were
  written only to an operating-system temporary directory.
- No research artifacts, validator outputs, source hashes, prior reviews,
  responses, protocol, or orchestrator state were edited.

Residual limits remain: finite and dependent source coverage; public CAD
contamination risk without evidence of actual contamination; small exhaustive
graphs; no physical feasibility guarantee; potentially difficult visibility
in small common-scale cards; and a readily solved visual-binding stage.
Human qualification and model comparisons remain conditional under the review
assumption. This review does not infer those outcomes from machine checks.

## Closest Work Checked

1. VisualFLIP v1, https://arxiv.org/abs/2606.07872v1 .
   Same-question answer-changing pairs and pair accuracy are established.
2. LEGO-Puzzles cited v3, https://arxiv.org/abs/2503.19990v3 .
   The current v4 introduction/task overview,
   https://arxiv.org/html/2503.19990v4 , additionally describes an explicit
   planning set up to eight steps. Updating the discussion to this version
   would improve currency; it does not eliminate the particular BrickAtlas
   binding/fault/all-optima distinction.
3. PhyBlock v2, https://arxiv.org/abs/2506.08708v2 .
   Progressive assembly, diagnosis and planning are not new to this paper.
4. BrickNet, CVPR 2026,
   https://openaccess.thecvf.com/content/CVPR2026/html/Kulits_BrickNet_Graph-Backed_Generative_Brick_Assembly_CVPR_2026_paper.html .
   Graph-backed source assemblies at much greater scale are prior work.

The abstract/proceedings pages and the indicated v4 overview were checked
directly. I do not claim a complete independent audit of those works.

## Acceptance Rationale

Not accepted on this snapshot. The revised family, controls, semantic scorer,
grouping and presentation resolve most of round01. The high silhouette result
is appropriately disclosed and is not itself the reason for rejection.
One central major gap remains: an interface benchmark must supply the
task-aligned joint and paired analysis that distinguishes isolated competence
from success on the same items when combined. The data design already makes
that repair possible. Complete that narrow scientific/technical readout,
preserve the unfavorable-result interpretations, and submit the resulting
new snapshot for independent review.
