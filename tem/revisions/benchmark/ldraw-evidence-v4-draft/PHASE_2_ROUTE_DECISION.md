# Phase 2.4: decision on Part-type invariance controls

Status: **ready for user decision; no route selected**.
Authority: `CODEX_EVIDENCE_V3_FIVE_ISSUES_UPGRADE_PLAN.md`, Phase 2.4.
All counts below are derived audits or explicitly labeled workload assumptions.
No new stimuli, human judgments, paid calls or model responses have been created.

## Completed evidence

- All **347 visual + 219 graph observations** have unique, complete derived ledger
  rows. Every gold is independently reconstructed. Graph golds agree under BFS
  and union-find; graph rows contain no invented image or human-review fields.
- All 146 Color endpoints have one rendered operand and one label.
  The frozen legal single-image program gives **141/146 correct, 5 abstentions**;
  A accuracy is 71/73, B accuracy 70/73, and Both is **68/73**.
  Equal-source Both is **91.875%**. All five abstentions are `no-color-region`:
  no color component survives the frozen filter. Thresholds were not tuned after
  these results. This supports an appearance sanity interpretation, not
  reference selection among multiple candidates.
- Removing images leaves **140/140 primary pairs** with identical request text
  and different golds. Identical deterministic responses force Both=0 and
  symmetric endpoint accuracy at most one half. This is an image-content floor.
- The feasibility enumeration covers **67/67 Part-type parents**, **24 sources**,
  **18 primary authors** and **17 contributor clusters**, without sampling.
  Each parent has three unordered wrong-candidate swaps; all **201** preserve
  the unique source-derived gold and pass operand and projection bounds.
  No swap has been selected.
- **192/201** swaps exchange different source part types. Sixty parents have
  three such choices, six have two, and one has zero. The 66-parent subset still
  covers all 24 sources, 18 authors and 17 clusters. Source counts remain 1--5
  parents; the one-parent loss affects `omr-42061` (2 to 1).
- The exception is `ld2-omr-42061-shape-match-1`: its three incorrect candidates
  all have source type `2780`. Different poses/colors may still distinguish
  them. Conversely, different source types need not look distinguishable.
  Neither proxy certifies visual feasibility. Blind visual judgments remain
  pending for **every** parent.

The JSON report retains all parents, all candidates, checks, projected
coordinates, failure reasons and coverage by source/author. Its structural
zero-eligible list is empty; its different-type proxy zero list contains the
single parent above. Recorded on-screen anchors and conservative text boxes do
not establish unobstructed geometry or readable label leaders.

## Options and concrete workload

The minimal B design adds one invariance partner I per accepted existing A:
swap two wrong-candidate labels, keep the correct choice, target, camera,
geometry, option order and other text fixed. Existing A is shared between the
changing A/B and preserving A/I analyses; it is not counted twice as a unique
observation. All existing visual and graph observations remain.

| Item | Route A: narrower claim | Route B: 67 partners | B sensitivity: 66 partners |
|---|---:|---:|---:|
| Added PNGs / visual observations | 0 | 67 | 66 |
| Total unique visual observations | 347 | 414 | 413 |
| Added two-rater judgments | 0 | 134 | 132 |
| Total initial judgments | 694 | 828 | 826 |
| Minimum distinct initial reviewer slots | 6 | 8 | 8 |
| Added visual calls, three frozen models | 0 | 201 | 198 |
| Added no-image calls, three frozen models | 0 | 201 | 198 |
| Added graph calls | 0 | 0 | 0 |
| Total calls across nine runs | 2,739 | 3,141 | 3,135 |
| Runs needing a new visual/no-image scope | 0 | 6 | 6 |

These B counts are conditional engineering scenarios, not a claim that 66 or 67
parents have passed visual QA. More exclusions after review would change the
qualified subset, not erase scheduled failures or excluded items.

Six initial reviewer slots are insufficient for a Part-type parent with A, B,
the existing panel and I: four observations times two distinct reviewers
requires **eight distinct people for that parent**. Preserve the sealed six-slot
v3 queues; a new study protocol can extend them with two disjoint slots or
reissue the full allocation with eight slots. It must audit exposure across
versions and auxiliary controls. If all four observations require independent
adjudication, up to four additional adjudicator slots are needed.

At an assumed **2--4 minutes per judgment**, the additional 134 judgments
require **4.5--8.9 person-hours**; 132 require 4.4--8.8 hours. The complete
828-judgment round is 27.6--55.2 hours. These are planning assumptions, not
measured reviewer speeds. Candidate screening, recruitment, disagreements,
adjudication and repeated QA after stimulus changes are additional.
At an agreed reviewer rate R/hour, added initial-review cost is 4.47R--8.93R.

Inference workload increases by 402 calls (14.68%) in the 67-partner case,
with native PNGs on 201 of them. Monetary cost requires the frozen snapshots'
actual account rates and token usage; the separate all-model MVP budget does
not price this three-model study. No provider quote is invented here.
Since **0/9 runs have been collected**, there are currently no completed paid
runs to discard. Re-freezing changes the six visual/no-image run plans and
their receipt bindings; graph inputs and the three model identities stay fixed.

## Claim and implementation consequences

**A**: explicitly claim paired correctness under answer-changing candidate-label
reassignment. Without an answer-preserving nuisance control, erroneous updating
when the answer should stay fixed cannot be estimated separately. No general
reference-robustness claim follows. No additional stimulus generation or QA
protocol extension is needed.

**B**: jointly measure correct updating on A/B and answer preservation on A/I.
Report preservation among valid and A-correct answers with their denominators,
joint correctness, invalid outcomes and stable wrong responses separately.
Shared anchors and source/author dependence remain explicit. This adds
behavioral evidence, not access to model internals or general grounding.

Before B can run, the new study must select swaps without seeing model results,
audit label/choice/source coverage and shortcuts, render and verify label-only
changes, freeze IDs/hashes and the unchanged model set with expanded run scopes,
extend parent-disjoint review to eight slots, and complete genuine QA.
The full 67-parent A-gold histogram can be retained by one partner per A;
that fact alone does not establish balanced swap positions or absence of new
shortcuts. No old .40 gate is imposed on an invariance or QA subset.

**Recommendation for the decision: B**, because structural coverage is broad
and no paid experiments have yet been collected. The main cost is expanded
human review and protocol/renderer work. A remains appropriate if those costs
cannot be supported; it requires the narrower claim above.

## Reproduction and next gate

New suite: `benchmark/suite/ldraw-evidence-v4-draft/`.
Run its Python modules using the isolated `benchmark/.runtime/mlx-env/bin/python`
with `PYTHONPATH` unset and `PYTHONNOUSERSITE=1`.

1. `measurement_audit.py freeze-color` verifies the existing immutable contract.
2. `measurement_audit.py build` reconstructs ledgers and feasibility, reusing
   predictions only if contract, complete input and result hashes match.
3. `verify_measurement_audit.py` checks coverage, joins, scoring and pending QA.
4. `publication.py`, TeX compilation and `verify_publication.py --render`
   regenerate and verify the manuscript and actual baseline numbers.
5. `preserve.py` verifies all 8,377 locked files and four recovery archives.

The initial build stopped after Color because JSON stringifies integer
histogram keys in graph audits. Canonical-hash comparison resolves this
representation mismatch; every graph prediction matched. The error log,
original evaluator, completed Color result hash and unchanged predictor
contract are retained under `work/`. No result was discarded or retuned.

Phase 2 machine work is complete. Phase 2.4 remains open for the user/main
choice. Phases 3--7 have not been advanced through that gate. Genuine human
feedback and provider receipts remain absent.
