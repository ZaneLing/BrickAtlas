# Evidence-v3 response to the fourth CVPR review

Controlling review: `CVPR_EVIDENCE_V2_REVIEW.md`.
New analysis: `ldraw2-evidence-v3`; dataset: `brickatlas-display-v3`.
The review itself and all earlier release bytes remain unchanged.

**Status: the design and implementation revision is complete. Empirical
acceptance remains open.** There are zero genuine human judgments and zero
completed live model runs. No score, rank reversal, agreement statistic or
learned-model case is inferred from fixtures or offline requests.

## Item-by-item disposition

| Review item | Implemented change and evidence | Acceptance boundary |
|---|---|---|
| §3 / P0: deterministic Part-type swap leak | `assignment.py`, `assignment-contract.json`, `part-type-assignment.json`: all 4,824 admissible configurations, 2,412 constraint-equivalent variables, 67 selections; HiGHS optimum 1,007,668, zero gap. | The declared construction leak is repaired; visual answerability and diagnostic value still need actual evidence. |
| §3.3: priors as a hard gate | `priors.py` independently reconstructs source golds/features. Gate runs before wire sealing, live inference, protocol analysis and publication. `answer-prior-audit.json` includes all predictions/errors and micro/source intervals. | Bounds concern the declared rules only, not arbitrary shortcuts or statistical significance. |
| §3.3: regenerate and freeze | All 134 primary Part-type images, options, endpoint IDs, golds, wires and review lineage rebuilt. `stimulus-validation.json`, `render-regeneration-validation.json`, `observation-index.json`. | Old Part-type QA/responses cannot transfer. New human qualification and inference remain required. |
| §4 / P0: complete model inclusion | `model-roster.json` commits three exact snapshots and nine run IDs/adapters. `roster.py`, `run.py`, `analyze.py` reject missing/extra runs, altered adapters and unregistered repeats. | Completed live runs: 0/9. Official model documentation was checked; live account access was not tested. |
| §4.2: failure-preserving provenance | Immutable run initialization, pre-call intents, raw receipts, terminal receipt/attempt hashes, explicit interruption closure and one-to-one model-run index. | All 2,739 scheduled requests remain in denominators. Unattempted closure records are not provider responses. |
| §5 / P1: pair memory independence | Six initial reviewers; every observation assigned twice; no reviewer sees multiple views of one parent, including panels. Up to three additional adjudicators have the same restriction. | Actual reviewer identities/exposure must be supervised; hashes do not certify human identity or behavior. |
| §6 / P1: repeated authors | `source-dependence.json`, `authors.py`: 18 primary authors, 17 contributor-connected clusters, all 276 source-pair inventory overlaps; author-macro, cluster bootstrap and leave-one-author-out differences. | Equal-source remains primary. Inventory similarity is not aligned geometry. Learned-model stability is unmeasured. |
| §7 / P2: single-call stability | Chose option A: one complete frozen invocation set per model/condition, no retries or best-of selection. Rank policy rejects directional claims from intervals containing zero. | No cross-call stability claim; temperature zero is not provider determinism. |
| §8–9: paper and baselines | English main paper, short scientific supplement, regenerated Part-type illustration, main-text choice marginals/shortcut baselines and full roster status. No-image control planned for every model. | Both families and graph evidence stay separate. No pooled assembly-intelligence score. |
| §10 / P2: graph enhancement | Preserve the reviewed 12 strong / 61 degree-visible partitions and algorithmic audit. | Extra graph templates are optional and were not added; 12 pairs remain a one-template proof of concept. |

## Quantitative design acceptance

Part-type gold choice marginals:

| Arm | A | B | C | D |
|---|---:|---:|---:|---:|
| A | 16 | 17 | 17 | 17 |
| B | 17 | 17 | 17 | 16 |

The complete transition matrix is:

| A gold → B gold | A | B | C | D |
|---|---:|---:|---:|---:|
| A | 0 | 6 | 5 | 5 |
| B | 6 | 0 | 6 | 5 |
| C | 5 | 6 | 0 | 6 |
| D | 6 | 5 | 6 | 0 |

- The old oracle-A first-alternative rule had Both = 67/67.
  It now has 23/67 = 34.33% micro and 26.94% equal-source.
- Every fixed-choice predictor satisfies source accuracy ≤ .30 on both
  Part-type arms. Every one of the 13 declared oracle-A attacks satisfies
  B micro/source accuracy ≤ .40.
- Any one deterministic mapping from A choice ID alone to B choice ID has
  in-sample micro ceiling 24/67. This is not a bound for models using
  source IDs, numeric labels, geometry or additional features.
- Within every Part-type pair, base geometry render bytes match and
  changed pixels remain inside label masks. Two regenerated canaries match
  byte-for-byte. All original source geometry and transforms are preserved.
- Color remains frozen: choice marginals A=(13,22,19,19),
  B=(16,15,20,22). Its last-alternative and cyclic-previous oracle-A rules
  reach 32/73; semantic color balance does not eliminate choice priors.

The local immutable design commitment precedes optimization/inference.
It is not represented as a timestamped external preregistration.

## Human and model handoff

The six initial packages contain 115, 116, 114, 115, 115 and 119 observations.
Total initial judgments required: **694 = 560 primary + 134 auxiliary**.
Every one of the 347 observations needs a final nonpending decision,
with raw judgments and any adjudication exports retained.
Decidable choices conflicting with generated gold remain blocked.
Nondecidable outcomes remain in full denominators.

The three model snapshots are:

| Model | Exact requested and expected served revision | Conditions |
|---|---|---|
| GPT-4.1 | `gpt-4.1-2025-04-14` | visual, no-image, graph |
| GPT-4o | `gpt-4o-2024-08-06` | visual, no-image, graph |
| GPT-4o mini | `gpt-4o-mini-2024-07-18` | visual, no-image, graph |

All use OpenAI Chat Completions, temperature 0, 128 output tokens,
90-second timeout, one attempt and no automatic retry. Visual requests
retain native 1280×800 PNGs and high detail. The scope is a fixed
three-snapshot single-provider study, not a current comprehensive leaderboard.

Use `QA-AND-RUN.md` for distribution, feedback import, independent
adjudication and complete-roster inference. No review packages have been
sent to other people and no live provider calls were made by this revision.

## Verification and delivery

- `validation-tests.txt`: 27 new protocol/analysis tests pass, including
  interrupted full-schedule closure. The 26 earlier tests are preserved.
- `typecheck-validation.json`: TypeScript compiler exit status.
- `wire-audit-validation.json`: all nine planned offline runs and 2,739
  exact requests; provider calls = 0.
- `qa/ui-validation.json`: six independent review queues, exact images,
  navigation and empty-feedback exports; human judgments created = 0.
- `site-validation.json`: evaluator search, current pair mapping, native
  pixels, source-viewer controls, responsive layout and native image routes.
- `benchmark/paper/evidence-v3/verification.json` and
  `visual-inspection.json`: all paper pages, references, figure provenance
  and reviewed PDF hashes. Main paper is 8 pages; supplement is 7 pages.
- `package-validation.json`: independent compilation of both PDFs from
  the extracted source ZIP, plus HTTP download checks.
- `delivery-manifest.json` / `delivery-verification.json`: final content
  hashes and preservation checks for 7,468 earlier files and three archives.

The evaluator entry is `/evidence-v3.html`. The historical 617-item dossier
is byte-identical to evidence-v2; `parent-mapping.json` supplies current
links separately. All 347 observation image routes use the correct versioned
scientific PNGs, including the 213 retained Color/panel observations.

## Remaining scientific acceptance

- [ ] Obtain 694 genuine initial judgments and necessary independent adjudication.
- [ ] Complete all nine frozen live runs, retaining every failure.
- [ ] Report actual full/both-decidable counts, source coverage, raw
  agreement, oracle conflicts, invalid/format rates and exclusion reasons.
- [ ] Evaluate whether Both adds diagnostic information beyond ordinary-A
  accuracy, fixed/option-order priors and no-image controls.
- [ ] Check source/author/contributor and leave-one-author-out sensitivity;
  restrict conclusions when directions or effective coverage change.
- [ ] Publish only receipt-derived genuine cases where available.

The 111 other historical task flags and 573 intersection candidates still
require separate physical/human decisions. This revision neither edits
source assemblies nor certifies gravity stability, continuous insertion,
or complete connector truth. Submission readiness and a favorable reviewer
recommendation cannot be inferred from engineering acceptance.
