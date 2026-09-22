# Round 01 Research-Refiner Response

Implementation owner: research-refiner run. Reviewer-owned `review.md/json`,
the protocol, all historical sealed data, source model files, manuscript files,
and git were not edited by this implementation run. Main owns paper integration,
BA-005, snapshots and git. This is an implementation response, **not a replacement
review verdict or a claim of acceptance**.

## BA-001: One Substantive Visual-Grounded Family

Implemented `benchmark/visual-repair-v1/`, family
`visually-bound-minimum-terminal-repair`. Exact public recognized-connector
graphs and missing vertices are coupled to a visually withheld third terminal.
The reference must be matched to one of four neutral-material source-geometry
cards, whose current randomized label supplies that terminal. The required
answer enumerates every minimum restoration set and its component sizes.
The family does not infer topology from pixels and makes no physical-removal,
stability, insertion, or dynamics claim.

`build.py`, `public.json`, `gold.json`, `render-specs.json`, `render.ts`,
`capture.ts`, `captures.json`, and `native/` provide executable construction,
source-faithful geometry, exact input wires and separate certificates.
There are 84 constructions, not three illustrations: 12--52 vertices,
11--74 edges, optimal cost 2--8, and 1--10 optima. Each construction crosses two
fault sets with anchor/changing/preserving visual arms and two independent ID
replicates, yielding 1,008 observations and 504 native images.

Dependency certification checks **complete optimum sets**, not only a selected
answer. Visual changing sets are disjoint at fixed text; preserving complete
answers are identical. Structural changing sets are disjoint at fixed image
and all text except one missing/present exchange. Every actual optimum requires
at least two restorations. Independent union-find evaluation agrees on all
1,008 answers. `multimodal`, `no_image`, `oracle_binding`, and `atomic_binding`
are implemented native conditions, not manuscript-only labels.

**Important measured limitation.** The frozen silhouette baseline achieves
91.23% held-out micro binding and exact repair when composed with the exhaustive
solver (78.29% group macro). The predeclared 0.80 micro gate fires. No tasks were
removed or reselected after this result. Claims are narrowed to composition
with a readily solved visual-binding stage, not hard visual recognition or
superiority over shallow algorithms. README's closest-work boundary distinguishes
the exact graph/binding/intervention/certification contract from VisualFLIP,
LEGO-Puzzles, PhyBlock and BrickNet without claiming that brick images or paired
accuracy are novel. Main must preserve this limitation in the paper.

Disposition: substantive implementation provided; novelty sufficiency remains
an independent reviewer judgment. No favorable neural/human result is assumed.

## BA-002: Matched Controls and Legal Shortcut Audit

Every visual arm uses the same graph packet, prompt, scale, images of the same
source geometry and camera positions. Changing transposes the target and one
distractor label; preserving transposes the other two distractor labels.
The 336 unique PNG pairs pass a full-image difference check: exactly two label
rectangles change, and no other pixel changes. Shared images across faults and
anchors across contrasts remain tied to construction/dependence groups.
Preserving scores require both semantic answers correct, not answer equality.

Vertex IDs, card order, candidate order, task names and image names use separate
randomization domains. No source IDs, original IDs, coordinates, part names,
arm names or binding keys enter native model text. All six cells preserve
semantic equivariance after mapping the second ID replicate back privately.
Structural serialization and budget are held constant except for exactly one
missing-list element, correcting the initial constructor's unnecessary
fault-dependent ordering before final input locking.

`baselines.py` executes legal first-card/location, silhouette, RGB appearance,
first-text candidate, sorted ID, `+12`, nearest ID, degree, minimum/maximum
repair-cost and seeded rules. Pixel rules receive only native pixels, public
text and an independently rendered generic font calibration atlas; they do not
read capture metadata, source meshes or gold. Oracle binding is a separately
declared privileged condition. Results are fully preserved:

- Silhouette: 0.912281 held-out micro; 0.782909 group macro.
- Appearance: 0.631579 micro; 0.546141 group macro.
- First-card/location: 0.228070 micro.
- Strongest tested text-only rule, maximum repair cost: 0.412281 micro.
- Oracle binding plus public exhaustive solver: 1.0.
- All tested deterministic no-image rules have zero changing-both-correct,
  as expected from identical text and disjoint correct optimum sets.

The gate aggregation is explicitly held-out **micro** binding OR exact repair.
Since exact repair includes binding correctness, it cannot exceed binding.
Group macro is reported alongside the gate, never substituted afterward.
The strong shallow baseline is disclosed and the perception claim narrowed.
No old Part-type invariance implementation is claimed: old atomic tasks remain
historical diagnostics under main's revised scope.

## BA-003: Sampling, Grouped Holdout, and Finite-Resource Claims

The census independently reproduces 177 connected, fully covered non-root
subassemblies including descendants, and 162 without recorded internal unmatched
intersections. Deduplication retains 125 candidates; 84 satisfy the fixed search
contract and 41 exhaust the 512-proposal budget. `sampling-ledger.json` retains
all candidates, exclusions, proposal/rejection counts, selected proposals and
source/contributor/design/topology-template fields.

Selection follows a seeded candidate order, disjoint instance-set selection,
and aligned typed-distance design signatures. Sources sharing contributors,
design signatures or unlabeled topology-refinement signatures are transitively
grouped before search. Final 84 constructions cover 17 sources and 15 selected
dependence groups: 27 development constructions in five groups, and 57 held-out
constructions in ten groups. No source, contributor, design signature or graph
template crosses the split. All 12 variants remain together. Source graph
reconstruction verifies the exact descendant instance sets and induced edges.

Held-out topology genuinely varies: 12--52 nodes and cycle ranks
0,1,2,3,4,5,6,7,8,9,10,12,13,23, with varying repair costs and optimum counts.
It is not only source decoration or ID renaming. Signatures are conservative
grouping diagnostics, not a proof of every possible semantic design difference.
Search is explicitly gold-conditioned challenge construction, not uniform
random sampling of real faults.

The precision illustration would require 25 independent bounded groups for
a worst-case normal 95% half-width 0.20, even before small-sample corrections.
Only ten held-out groups exist. The target is **not attained**; the study
reports finite-source group sensitivity and leave-one-group-out values rather
than claiming broad unseen-design generalization. No arbitrary item threshold
is imposed and repeated images never increase independent group counts.

## BA-004: Semantic Scorer and Manifest-to-Analysis Path

`evaluate.py` accepts arbitrary output ordering and independently recomputes
all feasible subsets and minimum solutions using union-find, separate from
constructor bitset reachability. It validates membership, duplicate vertices,
duplicate solution sets, feasibility, minimum cost, every requested optimum,
per-optimum component sizes, binding, and budget decisions. Missing or malformed
responses retain denominators. Only the selected repair family is promoted;
there is no unsupported diagnosis or registration scoring claim.

`study.py` freezes 4,032 native packets and 15 executable local algorithmic
configurations, with 15,120 planned invocations. All were executed without
purchases and retained. There are zero missing or malformed algorithm outputs.
Input packets, PNGs, implementation revisions, manifest lock, configuration,
settings, conditions and repeats are checked during collection/analysis.
Synthetic, off-version, wrong-hash, wrong-settings and duplicate receipts are
rejected. `algorithmic-receipts.json`, `algorithmic-scores.json`, and
`baseline-report.json` are actual deterministic outcomes, not model stand-ins.

The 15 historical model names remain in `planned-models.json` with one native
contract, no unsupported effort comparisons, and null results. Thirteen
multimodal models have four planned conditions; the two text models have only
no-image and oracle conditions. No immutable provider revision was fabricated.
`portable.py` supplies revision/adapter/settings locking, full-PNG stdin transport,
raw-output retention, timeout handling, and the same analysis path for an
explicit future local adapter. Unpinned models remain planning rows, not
executed provider configurations. No paid/model calls were made.

Qualification is executable, not merely a six-reviewer prose pledge:
`qualification.py`, `qualification-queue.json`, `review.html`, and
`qualification-status.json`. Six real-person slots assign two reviewers per
visual arm within each construction. A reviewer sees both ID replicates and
both fault packets within that arm, never another visual arm of the construction.
The 504 assignments plan 2,016 packet judgments and 1,008 distinct-image
judgments, with dependence explicitly retained. Exact prompt/PNG hashes,
complete assignment responses, repeated-image consistency, stable distinct
reviewer slots, and independent adjudication are validated. The adjudicator
cannot be either original reviewer. Human judgments remain pending and zero
constructions are human-qualified. Synthetic UI checks saved no judgments.

## Verification

`benchmark/visual-repair-v1/validate_all.py` reproduces construction and all
nonpaid verification. `validation.json` records commands and actual outcomes.

- Byte-identical regeneration of public/gold/summary/ledger/render specs.
- 1,008 independently recomputed semantic answers.
- 336 unique visual PNG pairs, complete image-difference masks.
- 2,520 card views nonblank and unclipped; smallest foreground 466 pixels.
- 144 source mesh hashes, original source manifests and induced graphs.
- Source/contributor/design/template split and two-replicate equivariance.
- 15,120 retained algorithmic runs; model/human/purchase counts zero.
- 31 focused semantic, receipt, denominator, OCR and qualification tests.
- TypeScript checks for renderer, capture and UI canary.
- Browser canary: six slots, exact 1600x900 PNG and graph packet, four quality
  flags and binding unanswered, receipt export disabled until real judgments.

The transient canary's material tint was corrected before the full capture.
The initial TypeScript invocation lacked Vite ambient types; adding the
repository's existing `vite/client` types passed without changing shared code.

## Remaining Limits and Ownership

The silhouette shortcut is real and disclosed. Human-visible uniqueness,
answerability and qualification outcomes remain unmeasured. Public CAD
contamination risk and unmodeled design dependence remain possible, not proven
leaks. Recognized graphs and source-preserved meshes are not physical
certificates. External model adapters/revisions still require real precollection
locking; no external configuration is falsely marked complete.

Main owns BA-005, both PDFs, paper figures, model-result blank-cell integration,
protocol state, immutable snapshots and git. This run makes no claim that BA-005
or overall acceptance is closed. The next independent review must assess the
actual implementation and narrowed scientific claim.
