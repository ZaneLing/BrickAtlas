# BrickAtlas Independent CVPR Review: Round 03

## Decision and Binding

**Recommendation: 7/10. Verdict: `accept`. Confidence: 4/5.**

BA-004 and BA-006 are closed on this snapshot. BA-001, BA-002, BA-003,
and BA-005 remain closed for the explicitly restricted research scope.
There are **zero unresolved critical or major issues** and no new blocking
regression in the reviewed evidence. Minor presentation and interpretation
limitations remain below. This is an internal simulated scientific review,
not an official CVPR decision.

- Base commit: `39e92789f2b64f34dbcfc118a2feb9e4439c951b`.
- Research snapshot: `6a52785ffaaae16e4e14b249289759a36243c15b94f2aa23a1b481230dc355e7`.
- Independently verified research inventory: 24,702 files.
- Study lock: `d1edb0a10b83abba434dc202a18c17570b89a992706ab2384380e20fc13fddc2`.
- Eligibility lock: `2a424617a365608f4d157f10cd91166942158ca75225219de2229fc4cb83507e`.
- Reviewed contribution: `visual-repair-v1`, not pooled historical studies.

The score is an independent assessment of scientific utility and validity.
It is not a reward for iteration count, an average of criterion scores, or
an inference from Main's integrity audit. The central interface diagnostic
is now defined and executable, which changes the scientific assessment from
round02. Correct code alone would not establish sufficient novelty.

## Assumption and Scope

For this review only, I apply the instructed assumption that the declared
model runs and human collection have been completed competently and could
populate reserved tables. I do not penalize the 212 blank model fields or
the absence of collected human receipts. I do not assume successful
qualification, favorable agreement, any model ranking, a positive interface
deficit, statistical significance, or empirical superiority.

Actual workspace evidence remains algorithmic and constructional: 84
constructions are pending human qualification, none is qualified or rejected,
and no learned-model results are supplied. No human or model collection was
performed during this review. In-memory tests are not empirical judgments.
Acceptance concerns the implemented, narrowly scoped benchmark and analysis
design under the review assumption, not a certificate of eventual outcomes.

I fully read the assigned reviewer skill, protocol, prior round02 review in
both formats, response and integration, current main and supplement, and
the relevant constructor, scorer, renderer, baseline, study, joint-analysis,
qualification, adapter, test and publication-validation code. The complete
snapshot inventory was parsed and its research digest independently checked.

## Frozen Rubric

| Criterion | Assessment / 10 | Scientific Judgment |
|---|---:|---|
| Contribution and closest work | 7 | A useful, narrow controlled visual-to-symbolic interface benchmark; not a new optimizer, visual-pair metric, or assembly representation. |
| Construct validity | 7 | Both binding and fault information have certified answer consequences. Observed joint failure is now distinguished from nonoverlapping isolated competence, without a causal mechanism claim. |
| Task depth, diversity and dependence | 7 | Real source-induced graph variation and pre-search grouped holdout; small exhaustive problems and only ten held-out groups limit scope. |
| GT, scoring, failures and shortcuts | 8 | Independent semantic enumeration, all-optima coverage, matched controls and failure denominators withstand the focused audit. Strong legal shallow performance is disclosed. |
| Experiment design and uncertainty | 8 | Same-task contingency, signed paired contrasts, common qualification and shared-group sensitivity are implemented, including empty and failed cases. |
| Reproducibility and faithful geometry | 8 | Native-byte locks, source/mesh checks, complete replayable algorithm evidence, qualification lineage and retained failed-call diagnostics. |
| Presentation and CVPR fit | 7 | Six main content pages plus references; actual primary-task figures and explicit claim boundaries. Small figure labels and an older closest-work version remain minor limitations. |

## Scientific Contribution and Closest Work

The useful contribution is not recognizing four part categories, solving a
small graph, or showing large source assemblies. The task binds a visual
referent into an exact structural problem and requires every optimal
restoration and its component outcomes. Crossed visual-binding and fault
interventions each change complete optimal-set families; a matched label edit
preserves the answer. Atomic and oracle conditions expose the two operations
separately, and the same-task joint readout now tests where their observed
successes do and do not coincide with combined success.

This is scientifically useful as controlled diagnosis even when binding is
easy, all learned systems compose it successfully, or the measured differences
are null. It supplies a reproducible way to distinguish those outcomes, not
evidence that composition must fail. Its source-based graph variation and
all-solution semantics provide more task substance than another atomic
part-recognition collection. The scope is sufficiently coherent for acceptance
as a diagnostic benchmark, but too narrow for a stronger recommendation.

I checked these verifiable closest-work sources:

1. VisualFLIP v1, https://arxiv.org/abs/2606.07872v1: same-question
   answer-changing pairs, pair accuracy and competence-conditioned collapse
   are established. BrickAtlas does not receive novelty credit for those
   ideas. Its distinction is the separately controlled graph/fault input,
   visually selected terminal and complete repair-set semantics.
2. LEGO-Puzzles cited v3, https://arxiv.org/abs/2503.19990v3, and current
   v4 overview, https://arxiv.org/html/2503.19990v4: spatial and sequential
   brick reasoning are prior work; v4 explicitly includes planning horizons
   up to eight steps. The manuscript should eventually update its v3
   reference and comparison row. That update does not remove the particular
   binding/fault/all-optima distinction.
3. PhyBlock v2, https://arxiv.org/abs/2506.08708v2: progressive assembly,
   completion, diagnosis and planning robustness are already studied.
   BrickAtlas's supplied-graph restoration is not a substitute for these
   physical or planning evaluations.
4. BrickNet, CVPR 2026,
   https://openaccess.thecvf.com/content/CVPR2026/html/Kulits_BrickNet_Graph-Backed_Generative_Brick_Assembly_CVPR_2026_paper.html:
   large-scale human-designed LDraw data and graph-backed assembly programs
   are prior work. CAD provenance or connector graphs alone are not novelty.

These checks cover the abstract/proceedings pages and the returned
LEGO-Puzzles v4 introduction/task overview, not a full independent audit of
every prior paper. The manuscript's distinction at `paper/main.tex:115-159`
is defensible at that scope.

## Prior Issue Disposition

### BA-004: Closed

The central round02 objection is substantively resolved, not merely renamed.

**Same-task outcomes.** `joint.py:10-31,68-112` defines A as isolated atomic
binding correctness, O as oracle exact repair and M as multimodal exact
repair. Alignment checks task ID, construction, group, split, ID replicate,
fault arm, visual arm and attempt. All eight A/O/M cells are retained.
J uses `n110 / (n110 + n111)`, with task and group eligibility, failure
counts, zero-eligible groups and per-group contingencies. It is not a
product of marginals or the old within-multimodal `repair_given_binding`.

**Compatible runs and failures.** `joint.py:35-65`, `study.py:192-217,274-316`
and `portable.py:33-86` require an explicit comparison under one run lock,
matching system, revision, settings, evidence kind and attempt contract.
External adapter bytes, eligibility and complete native membership are
checked. Independently locked receipts are rejected rather than pooled.
The analyzer creates rows for every planned task/configuration before
joining. A missing M response with A=O=1 increases J's failure numerator.
Missing A or O gives false isolated correctness, remains in the eight-cell
and paired-effect denominators, and is naturally outside J's conditional
eligibility. An unplanned condition is unavailable, not imputed as a
complete comparison. Only one attempt is supported and enforced.

**Paired estimands and resampling.** `joint.py:115-164` computes M-exact
minus O-exact and M-binding minus A-binding on the same tasks, without J's
competence filter. Equal-group means and micro estimates are distinct.
One 2,000-draw matrix, seed 20260922, indexes all numerator, denominator and
contrast vectors. Complete dependence groups retain shared images, anchors,
faults and both ID replicates. Zero-eligible groups remain in draws;
all-ineligible draws are omitted from J percentiles and counted. J intervals
require two eligible groups; contrast intervals require two planned groups.
Empty populations or eligibility yield null, not perfect performance.
Leave-one-group-out values also preserve undefined cases.

**Common qualification.** `qualification.py:145-211` derives construction
statuses and membership from raw receipts/adjudications, queue and study
locks, then recomputes those decisions during validation. Rehashing an
edited retained-ID list does not pass. Status precedence distinguishes
rejected, pending, needs-adjudication and qualified, while retaining arm
statuses. `study.py:318-357` emits full and qualified configuration and
interface branches. All twelve observations enter or leave together across
conditions. `portable.py:44-65,69-86` embeds eligibility before collection,
retains full collection, and rejects later substitution for that run.

**Regression evidence.** All 56 tests passed, including
`test_interface.py:51-166,187-309`. The prior aligned/disjoint counterexample
still has identical complete marginal reports, but the new analysis correctly
distinguishes 0/24 from 24/24 joint failures. Tests cover empty eligibility,
missing planned calls, absent conditions, duplicate/off-cell rows,
incompatible locks, edited qualification and construction-wide exclusions.
With in-memory all-qualified fixtures, actual nonzero algorithm metrics
and every interface full/qualified branch agree exactly. Excluding one
construction retains 1,008 full slots and 996 qualified slots per condition.
No fixture was saved as human evidence.

I additionally checked a nondegenerate three-group synthetic example with
unequal sizes and one zero-eligibility group against an independent scalar
bootstrap calculation. J was 1/3 micro and 1/4 macro; signed contrasts and
both interval types matched, with 1,939/2,000 defined J draws. An initial
hand-calculated binding-contrast expectation in my fixture was incorrect;
correcting that expectation, not research code, resolved the assertion.
A separate ephemeral text-only lock produced 2,016 planned failed slots
and an unavailable interface, not a fabricated A/O/M comparison.

**Paper mapping.** `paper/main.tex:338-378,415-428` and
`paper/supplement.tex:207-263,321-347,369-381` match the implemented
estimands, exclusions and noncausal interpretation. The five interface
columns map to actual `interface[].full.heldout` fields in
`paper/build_tables.py:43-71` and `ANALYSIS.md:120-158`, with qualified
counterparts retained. `paper/verify.py:84-103` checks field existence and
contingency arithmetic. No missing result is interpreted as zero.

Closure concerns the analysis contract. It does not certify empirical
integration failure, positive model effects, or successful human qualification.

### BA-006: Closed

`portable.py:89-135` retains readable stdout/stderr, lossless base64 bytes,
return code, timeout status/limit and exception details in
`visual-repair-adapter-diagnostics-v1`. Nonzero exits and timeouts remain
failed responses even if partial stdout resembles an answer. Successful
malformed output is retained for semantic parsing. No retry or
successful-only selection is introduced.

The five mocked tests at `test_interface.py:312-369` pass for nonzero exits,
non-UTF-8 bytes, partial and empty timeouts, launch errors and malformed
successful stdout. No real adapter or model was executed.

### BA-001, BA-002, BA-003 and BA-005: Remain Closed

- **BA-001:** `build.py:171-210,243-316` and `evaluate.py:29-135` implement
  genuine visual selection followed by complete minimum restoration, with
  two independent answer-changing inputs. The independent audit reproduced
  all 1,008 answers. This remains a narrow interface task, not general
  physical or visual reasoning.
- **BA-002:** `verify.py:35-62,110-158` verifies matched text/image controls,
  disjoint changed optimum sets, preserving answers and ID equivariance.
  `baselines.py:11-115` uses permitted pixels/text, including pixel-based
  label reading. Native ordinary payloads omit gold and provenance.
  The high silhouette result and fired .80 gate remain disclosed in
  `paper/main.tex:275-292`; tasks were not reselected to hide it.
- **BA-003:** `build.py:90-168,214-242,319-350` retains census, exclusions,
  pre-search source/contributor/design/template grouping and bounded search.
  `verify.py:73-107` checks induced graphs, disjoint selected source parts,
  split boundaries and mesh hashes. There are 57 held-out constructions in
  ten groups, not 684 independent samples. The paper now explicitly reports
  that 802/1,008 observations cost two or three and 598 have one optimum.
- **BA-005:** Main PDF validation gives six content pages plus references on
  page seven; the supplement has seven pages. Both actual primary figures
  separate model input, source context and evaluator GT. Native and figure
  inspection confirms their task correspondence. In the factorial PDF,
  each native panel is only about 156 points wide, so embedded labels remain
  very small; larger bound-ID and solution annotations convey the comparison.
  This is not a recurrence of the former nonprimary-figure/length defect.

## Actual Algorithm Evidence

All 15,120 retained algorithm responses were independently replayed in memory
from native packets and allowed pixels, with 7,896 distinct packet/rule
evaluations; every response matched. Reanalysis with `write_output=False`
exactly reproduced the entire stored `baseline-report.json`.
Comparison against reviewed commit `72db15006cfa89f80922857e2b29b79d342fdd0e`
also confirmed unchanged response contents except study-lock envelopes and
unchanged values in all 45 prior configuration/split metric blocks.

| Held-out Modular Reference | Exact Micro | Exact Group Mean | AO-Eligible Tasks / Groups | J |
|---|---:|---:|---:|---:|
| First-card plus exact search | 156/684 | 23.64% | 156 / 7 | 0 |
| Silhouette plus exact search | 624/684 | 78.29% | 624 / 8 | 0 |
| Appearance plus exact search | 432/684 | 54.61% | 432 / 7 | 0 |

For silhouette, the only nonzero contingency cells are `010=60` and
`111=624`. Its group-mean repair contrast is -0.21709090909090908
(-21.709 percentage points), micro contrast is -0.08771929824561403,
and binding contrast is zero. Its group sensitivity interval for the
repair contrast is [-0.5, -0.00909090909090909].

These are deterministic modular references sharing an exact oracle.
Their zero J follows the matched binding rule and exact-solver composition;
it is not evidence about learned-model integration or humans. Their degenerate
[0,0] J intervals are finite-reference resampling summaries, not proof of zero
population error. Qualified estimates remain null because actual qualification
is pending. The strong shallow result limits difficulty and novelty claims
but does not invalidate the narrower controlled diagnostic.

## Remaining Limitations and Conditional Conclusions

- **Limited generalization:** 84 constructions from 17 sources and 15 groups,
  only ten held-out groups. Search is gold-conditioned, latent design
  similarities can remain, and most optimization instances are small.
  Group bootstrap and leave-one-out summaries do not provide calibrated
  broad-population inference or meet the stated 25-group precision illustration.
- **Restricted visual and physical construct:** simple silhouette matching
  already reaches 91.23% held-out micro repair. All paired and All-six micro
  scores for that modular rule are also 91.23%. It does not establish hard
  perception, hidden-topology inference, insertion/extraction feasibility,
  stability or physical repair. Actual source geometry is provenance, not
  proof of those abilities.
- **Qualification is not assumed favorable:** native cards can be small and
  superficially similar; source part identity and nonblank pixels do not
  establish unique human-visible matches. If competent qualification excludes
  many constructions, the qualified interpretation must narrow accordingly.
  If no credible population remains, no human-answerable interface claim is
  supported; null qualified statistics are not a substitute for such evidence.
- **J is outcome-dependent and noncausal:** each system's A=O=1 subset may
  differ even with common construction eligibility. J alone should not rank
  general competence across models. One attempt cannot identify latent stable
  abilities, and nonzero J may reflect stochasticity, prompting or output
  format as well as composition. Invalid repair output also forfeits binding
  credit by the declared scoring rule. Counts, contingencies, unconditional
  contrasts and failure rates must accompany interpretation.
- **Collection integrity remains operational:** future models require real
  pinned adapters/revisions and common qualification populations. Public CAD,
  gold and provenance permit lookup/contamination risks; native inputs and
  no-tool contracts exclude them but cannot authenticate closed-book conduct
  or a person's identity by hash alone.
- **Minor presentation:** enlarge factorial label insets for print and update
  the LEGO-Puzzles discussion to v4 planning. Neither changes the accepted
  task contract or constitutes an unresolved major issue.

Any claim of model superiority, ranking reversal, human agreement or excess
joint failure requires the eventual measured evidence. Zero J, negative or
positive paired differences, and undefined conditional estimates are valid
outcomes. They must not be rewritten as a favorable story to preserve this
recommendation.

## Verification and Ownership

Independent read-only checks completed:

- `snapshot.py 3 --verify`: all 24,702 research files match the specified
  SHA256; snapshot file count and base commit also match HEAD.
- `python -m unittest discover -s benchmark/visual-repair-v1 -p 'test_*.py' -v`:
  56 tests passed in 23.290 seconds.
- `verify.verify()` with only its final report writer suppressed: all
  1,008 semantic answers, 336 unique visual pairs, 2,520 card views and
  144 mesh files checked; complete returned audit equals stored evidence.
- `study.analyze(..., write_output=False)`: complete report equality, locks,
  failure denominators, pending qualification and all three interfaces.
- All 15,120 algorithm responses replayed in memory; prior-response and
  45-block metric preservation independently checked.
- Independent nondegenerate bootstrap and graph-only unplanned-condition
  tests, with no synthetic receipt/eligibility files written.
- `paper/verify.py` with only final `verification.json` writing suppressed:
  15-model schema, 212 null fields, interface paths/arithmetic, figure
  provenance, style, citations, logs and both PDF limits passed.
- Inspected both primary figure PNGs and native development, held-out
  31028 and held-out OMR 42066 examples previously identified among
  silhouette failures. This is visual inspection, not human qualification.
- Read PDF text and image placement directly without rebuilding or
  rasterizing files; `git diff --check` passed.

All Python checks used
`env -u PYTHONPATH PYTHONNOUSERSITE=1 PYTHONDONTWRITEBYTECODE=1 benchmark/.runtime/mlx-env/bin/python`.
Recorded seven-stage generation/TypeScript/browser validation was inspected,
not reexecuted. No `validate_all`, regeneration, freeze, builder, capture,
paid call, PDF/GT/study/result modification, commit or push was performed.

Verified PDF hashes:

- Main: `a3856a34c135750fc4d3ebcd73344f479ff534201effea31f0e637b075ef9467`.
- Supplement: `ca7f2a87607bc0a7750f247bb90966bb016487cdc88c7285167197d8eaf87c8b`.

Main separately reported that all snapshot Git HEAD blob identities and
14 retained validation-evidence hashes also match. That governance result
is attributed to Main, not represented as my own full Git-blob audit.
Concurrent changes to iteration governance files are outside this review's
ownership. The only reviewer-owned outputs are this file and `review.json`;
the unrelated `assets-built/e2e-report.json` is preserved.

## Acceptance Rationale

Accept at 7/10 under the stated completion assumption. The crossed task,
complete-answer certificates, controlled information conditions and honest
shallow baseline together form a modest but useful CVPR diagnostic resource.
Round03 now supplies the same-task joint and paired analysis necessary to
make its central question observable, including unfavorable and empty cases,
with qualification common across conditions and failures retained.
BA-004 and BA-006 satisfy their testable closure requirements; earlier
closures survive regression checks.

This is not acceptance of a hard-vision benchmark, a physical-repair system,
population-wide generalization, or an empirical claim about learned models.
The remaining limits reduce breadth and confidence but do not leave an
unimplemented central scientific contract on this snapshot. Final repository
and evidence governance remains Main's responsibility.
