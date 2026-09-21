# Evidence-v1 review response and evidence-v2 acceptance

Controlling review: `CVPR_EVIDENCE_V1_REVIEW.md`.
New visual dataset: `brickatlas-display-v2`.
New analysis and delivery: `ldraw2-evidence-v2`.

**Disposition:** the implementable protocol, stimulus, graph, analysis and
publication changes are complete and machine checked. The review's human
and learned-model acceptance criteria are **not complete**. The release
does not claim that all grounds for rejection have been empirically resolved.

## C1 — Current display reference and condition-specific gold

**Implementation complete; human/empirical confirmation open.**

- Every new visual prompt selects the object/reference in the current image.
  Canonical identity, current display referent, historical source truth and
  observation-conditioned answer are explicitly distinct.
- Replaced the invalid original-color/donor interpretation with 73 pairs of
  explicit rendered-appearance edits at identical geometry, pose, camera,
  labels, visibility and material settings. Both arms permit edited appearance.
  No donor geometry is substituted.
- Retained 67 candidate-reference-change Part-type pairs under new prompts.
  Target geometry/token stay fixed; current candidate labels determine gold.
- Generated 280 new primary wire observations and 67 auxiliary observations.
  All golds are independently recomputed, and every observation is hash bound.
  Old prompts, QA and model responses cannot enter this version's analysis.
- All 73 Color changes stay inside the common body mask plus one antialiasing
  pixel. Three regeneration canaries are byte-identical.

Evidence: `REVISION-CONTRACT.md`, `identity-contract.json`,
`visual-manifest.json`, `observation-index.json`, `stimulus-validation.json`;
main paper Sections 3–4 and Figure 1.

**Boundary:** machine/source checks cannot establish that an arbitrary pair
is uniquely decidable to an independent reader. That part requires actual QA.

## C2 — Complete A/B, independent dual review and adjudication

**Workflow complete; the review's final human acceptance is open.**

- Both reviewer packages cover all 280 primary endpoints and all 67 auxiliary
  observations, in independent opaque shuffled queues.
- Retain `reviews[]`, decision/choice/check agreement, multiclass Cohen's
  kappa, adjudication and computed final decisions.
- Ask for unique target reference, unique visual option, sufficient visibility,
  no reference contradiction, visual choice, reasons and native-size attestation.
- Decision, choice or check disagreements require a third distinct person.
  A final decidable choice conflicting with gold requires dataset revision.
- New wire hashes invalidate prior judgments. The runner recomputes the gate
  before directory creation or network calls.
- Full and both-decidable estimates preserve counts, source coverage,
  overlapping exclusion reasons and paired full/subset uncertainty.

Evidence: `qa.py`, `qa-review.html`, `run.py`, `analyze.py`, `estimates.py`,
`QA-AND-RUN.md`, `qa/ui-validation.json`; main Section 5.

**Actual state:** 0/560 primary raw human reviews; 0/134 auxiliary reviews;
0/280 primary final decisions; 0/140 comparable pairs.
No agent or synthetic judgment is counted as human evidence.

## M1 — Strong graph challenge and shallow baselines

**Implemented and algorithmically verified within the stated small scope.**

- Primary strong change: 12 pairs / eight sources. The other 61 pairs /
  23 sources are degree-visible controls. Invariances are separate; shared
  anchors cannot inflate observation or source counts.
- Match surviving nodes, edge count, target degree, full degree multiset and
  isolate count for strong pairs.
- Include source-held-out node/edge/degree/anonymous-1-WL lookups,
  isolates-plus-one, BFS and union-find. Expose per-pair outcomes, lookup
  support, training source IDs, feature collisions and intervals.
- Natural isolates-plus-one: 72/73 correct. Weak change Both: 61/61.
  Strong change Both: 0/12. BFS and union-find solve all these cases.
- Strong direction counts are 6 increases and 6 decreases; raw arm answer
  histograms are not identical and are disclosed. Unordered Both and symmetric
  endpoint accuracy avoid an arm-direction interpretation. Symmetrization
  does not generate extra trials.
- All strong pairs are anonymous uniform-feature 1-WL indistinguishable.
  No claim says a simple anonymous message-passing GNN should solve them.
  Unique-ID, positional, spectral and higher-order methods are outside that
  restriction. This is a proof of concept, not broad graph validation.
- Approximate pair Wilson intervals and source-bootstrap limits are reported.
  All 12 pairs appear in the short supplement.

Evidence: `graph_audit.py`, `graph_run.py`, `graph-audit.json`,
`graph-partitions.json`, `GRAPH-AND-ANALYSIS-ACCEPTANCE.md`;
main Section 6, Table 4, supplement Section 5.

## M2 — Added diagnostic value beyond ordinary accuracy

**Analysis implementation complete; empirical requirement open.**

- Family-specific A Acc, NewAcc, Both, old-gold retention, other/invalid,
  format validity, conditional metrics, source counts and intervals.
- Exact-rational A/NewAcc/Both rankings with midrank ties; paired model
  differences, rank reversals versus ties and full/QA direction agreement.
- Genuine receipt-derived case extraction for correct-to-new,
  correct-to-old and same-valid-wrong. Missing case types remain absent.
- Family × model × condition outputs and separate position-control results.
- Dry runs, old-version responses and fixtures cannot register as model results.

Evidence: `analyze.py`, `estimates.py`, `test_analysis.py`,
`reports/protocol-ready.json`; main Section 5.4.

**Actual state:** zero completed visual or graph model runs. No real model
ranking, rank reversal, response example, format-effect conclusion or
full-versus-QA agreement is available. Graph algorithm results do not
substitute for the requested learned-model visual diagnosis.

## M3 — Separate mechanisms and bounded visual claim

**Implemented; the resulting model effects remain unmeasured.**

- Color and Part-type never share a visual total or causal interpretation.
- Color tests a rendered body-color change at fixed geometry/pose.
  The old donor inventory (10/73 same type; 3/73 same linear transform)
  is retained and cannot support a 73-item donor-based color-only claim.
- Part-type tests the current candidate-reference binding for geometry matching.
- Added 67 unlabeled-image position-panel controls. Their layout/access
  changes are disclosed, so they are not presented as a causal OCR ablation.
- Claims are limited to two atomic visual attributes, numeric reference
  interfaces and 24 sources, without end-to-end assembly claims.

Evidence: `donor-feasibility.json`, `visual-manifest.json`;
main Sections 2–4 and 7; supplement Figure 1.

## Minor comments

| Item | Disposition |
|---|---|
| 1. Replace unavailable results with real findings | **Empirically open.** Abstract now leads with the bounded contract and measured graph/stimulus findings. It explicitly states the missing human/model evidence. No fictional scores replace blanks. |
| 2. Relevant literature and sparse bibliography | **Complete.** Added seven primary-source-verified references, 13 total: contrast sets, complementary-image VQA, consistency, referring expressions, Winoground/construct validity and GNN expressivity. Full Gardner author list retained. |
| 3. Misleading scale/prior graphic | **Complete.** Replaced the prior side-by-side chart with an explicitly labeled source-scale table; no difficulty inference from unlike quantities. |
| 4. Overlong supplement | **Complete.** Main paper: 8 pages. Scientific supplement: 6 pages. All 617 historical dossiers are independently searchable in JSON/HTML with source and new-version links. Old 182-page supplement is preserved. |
| 5. Family name consistency | **Complete.** Stable `shape-match` → `Part-type` mapping in the registry, exported schema, website, tables and report. |

Literature evidence: `literature/PRIMARY-SOURCE-AUDIT.md`.

## Delivery and validation

- English main paper: `benchmark/paper/evidence-v2/main.pdf`.
- English scientific supplement: `benchmark/paper/evidence-v2/supplement.pdf`.
- Independent paper source ZIP:
  `benchmark/paper/evidence-v2/brickatlas-evidence-v2-source.zip`.
- Local web entry: `http://localhost:5173/evidence-v2.html`.
- Searchable historical records: `public/benchmark/evidence-v2/dossiers.json`.
- Two blind reviewer packages: `qa/initial/reviewer-1.zip` and
  `qa/initial/reviewer-2.zip`. Distribute each to a different person.
- 26 protocol/analysis tests pass. Native inputs, English PDF text, references,
  figure provenance, full dossier coverage and web interactions are checked.
- Source package compilation, download routes and final hashes are recorded
  in `package-validation.json` and `delivery-verification.json`.
- 5,529 earlier release files and 420 source render assets remain unchanged;
  original bytes also remain in their verified preservation archives.

Publication page review and browser QA are machine/agent delivery checks,
not independent human judgments about benchmark answerability.

## Remaining acceptance sequence

1. Complete independent raw human reviews and necessary third-person
   adjudications. Any genuine gold conflict requires a new dataset revision.
2. Run pinned models on the new observations after the complete QA gate.
   Collect native requests and genuine raw provider receipts.
3. Publish both full and QA-decidable family tables, paired uncertainty,
   format rates, rank comparisons and actual response cases. Revise claims
   if no stable diagnostic value emerges.
4. Keep the historical 111 flagged tasks and 573 physical intersection
   candidates in their separate human-review process; this revision has not
   adjudicated or physically repaired them.

These steps are not marked complete by the software tests or the manuscript.
