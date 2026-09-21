# Five-issue upgrade: phase tracker

Controlling instructions: `CODEX_EVIDENCE_V3_FIVE_ISSUES_UPGRADE_PLAN.md`.
Working version: `ldraw2-evidence-v4-draft`.
Manuscript: `benchmark/paper/evidence-v4-draft/`.
New audit code: `benchmark/suite/ldraw-evidence-v4-draft/`.

## Version and authorization

The main executor selects a new **draft** version as directed by Phase 0.
Evidence-v3 is a sealed input, not an editable working directory.
Historical inputs, v3 observations, assignment, identity contract, reviewer
queues, roster and 27 tests remain byte-identical.
New draft artifacts do not establish a new empirical dataset or model result.

Prior model-budget/MVP proposals are separate from this upgrade. They do not
change the frozen three-model roster used by this plan.
No paid inference or messages to other people are authorized by this task.

The A/B decision in Phase 2.4 requires a concrete 67-parent feasibility
report before asking the user; neither route has been selected.
No later phase is marked passed based on assumed human feedback or receipts.

## Phase 0 — isolation and baseline

status: PASS

- Entry branch: `main`.
- New branch: `codex/v3-five-issues`.
- HEAD: `05e9d2e2e77dda096da86f3f2d2d03c9a3d16143`.
- Entry tree was **not clean**: `assets-built/e2e-report.json` was modified,
  with existing untracked release, review and experiment-plan artifacts.
  All were retained. No reset, deletion, cleanup or blanket commit was run.
- Baseline tests: actual run reports **27 tests in 4.605s, OK**.
- Main PDF SHA-256:
  `48cb6fc0c58dfad94d0d051aa4a8dea4eda0e26ef26b275d561b83a756e46703`.
- Supplement PDF SHA-256:
  `65f4ef85ce4808b1445cb10c95dd13cf2ee19dcd6b3c60e3d9f66489a4ab8fc2`.
- Recovery: incremental v3 content archive plus the three existing ancestor
  archives, all recorded in `baseline-lock.json`. All **8,377 locked files
  and four archives** verified; baseline_modified=false.
- Machine verification:
  `env -u PYTHONPATH PYTHONNOUSERSITE=1 benchmark/.runtime/mlx-env/bin/python -m unittest discover -s benchmark/suite/ldraw-evidence-v3 -p 'test*.py'`.
  Exit status 0; retained log: `work/phase-0-baseline-tests.txt`.
- Human visual qualification: unchanged, pending actual judgments.
- Failures and rollback: none; archived v3 and previous working tree remain available.
- Next stage: Phase 1.

## Subsequent phases

| Phase | Status | Gate |
|---|---|---|
| 1: literature and contribution | PASS | Original HTML checked; 14 citations; 8-page main and 7-page supplement verified |
| 2: full observation audits | Machine PASS; decision open | 347 + 219 rows verified; legal baseline 141/146; complete 67-parent feasibility |
| 2.4: route A/B | Ready for user decision | Concrete coverage, 66/67-parent costs and eight-reviewer requirement in PHASE_2_ROUTE_DECISION.md |
| 3A: subset-prior implementation | Not started | Synthetic counterexamples and denominator checks |
| 4 / 3B: actual human QA and subset integration | Pending genuine feedback | No manufactured judgments; every endpoint nonpending |
| 5: all model receipts | Pending human gate and user execution | No paid calls from this executor |
| 6: scientific manuscript integration | Not started | Use only actual analysis evidence |
| 7: reproduction delivery | Not started | Separate PDF, offline-wire and full-asset scopes |

## Interpretation constraints

- Oracle-A rules receive privileged A gold. They are construction audits,
  not protocol-legal independent single-observation model attacks.
- Neither 23/67 Part-type nor 32/73 Color oracle results are model ceilings.
- The .40 bound is a full-design constraint; no new subset or rejection
  threshold is inferred from it.
- No arbitrary invalid-rate, exclusion-rate, CI-overlap or rank-reversal
  criterion is an acceptance requirement.
- Identical no-image A/B requests force Both=0 only for identical
  deterministic responses; this is an image-content floor.

## Phase 1 — direct neighbor and contribution

status: PASS

- Inputs: fetched arXiv HTML 2606.07872v1 and abstract metadata; sealed v3
  manuscript, generator, verifier, source bibliography and replay figure.
- Allowed scope: new draft manuscript and its generating/verification code.
- Changes: VisualFLIP entry added once through `additions.bib`; all 13 prior
  references retained. Intro states three integration contributions and
  explicitly excludes novelty of pair accuracy, Both or minimal editing.
  Earlier oracle-assisted 67/67 example moved to limitations and calibrated.
- Machine verification: `publication.py` exit 0; one-way bibliography
  composition byte-identical on two generations; bibtexparser 2.0.1 parsed
  14 unique entries, zero failed blocks; TeX/BibTeX compilation exit 0;
  adapted `verify_publication.py --render` passed 8/7 pages and 14 unique
  compiled bibitem keys, no missing citations or off-page text.
- Original §3.2 identity-contract paragraph is byte-identical.
- Main executor verified metadata, counts, metric definitions and independent
  versus sequential protocols against the fetched text. Comparison only says
  the particular contracts are not specified in inspected sections.
- Retained evidence: `work/phase-1-validation.json`, build logs,
  `work/phase-1-source-diff-stat.txt`, new paper `related-work-matrix.md`.
- Failures and recovery: first layout was nine pages; redundant introductory
  prose shortened. No font/margin changes and no limitation removed.
- Input closure: base bibliography and historical figure copied from
  hash-verified inputs into the draft so its generator never reads its output.
  Full Phase 7 reproduction has not been claimed.
- Next stage: Phase 2, then the required concrete route decision.

## Phase 2 — full measurement audit

status: MACHINE PASS; PHASE 2.4 USER DECISION PENDING

- Full derived ledgers: **347 visual + 219 graph = 566 unique observations**.
  Wire/image hashes and source/author attribution match sealed authorities.
  All visual golds independently reconstructed; graph golds agree under BFS and
  union-find, and every recomputed graph baseline matches canonical audit bytes.
  Graphs retain multiple pair memberships for shared anchors, with no invented
  images, choices or human judgments.
- Color interface: predictor accepts only one model-visible PNG and its text.
  Five synthetic tests passed before the algorithm was locally hash-locked.
  Full evaluation used 146 fresh isolated processes with empty working
  directories. No source, mask, pair or gold was passed to the predictor.
- Actual Color results: **141/146 correct; five abstentions**, all due to
  `no-color-region`; **71/73 A, 70/73 B, 68/73 Both**. Both is 93.15% micro
  and 91.875% equal-source. Every outcome, support count and source interval
  is retained. No threshold tuning followed the full run.
- No-image audit: **140/140 primary pairs** have byte-identical stripped
  messages and different golds. Draft analysis helper and manuscript explain
  the deterministic Both=0 / endpoint<=1/2 implication as an image-content
  floor, not reference-selection evidence.
- Feasibility: all **67 parents**, **24 sources**, **18 authors**, **17 credit
  clusters** included. **201/201** wrong-candidate swaps pass structural,
  unique-gold and conservative projection bounds. All visual judgments remain
  pending. Different source types occur in 192 swaps across **66 parents**,
  still covering all sources/authors. The exception
  `ld2-omr-42061-shape-match-1` has three wrong candidates of type `2780`;
  it is retained, not silently excluded.
- Decision document: `PHASE_2_ROUTE_DECISION.md`. Route B with 67 added
  partners requires 134 additional judgments and 402 additional calls
  across the unchanged three-model set. Four views per Part-type parent
  require **eight distinct initial reviewers**, versus the sealed six-slot v3
  allocation. Current 0/9 completed runs means no paid results to discard.
  Route recommendation is B; **no route or swap has been selected**.
- Manuscript: Color is now an appearance sanity track; auxiliary panels are
  explicitly descriptive. Algorithm/threshold details and actual measured
  results are generated from the audit in the supplement.
  Main **8 pages**, supplement **8 pages**; 14 compiled citations;
  publication verification passes, with no missing references or page overflow.
  Main executor inspected main pages 3--4/7--8 and supplement pages 1--2.
  Source §3.2 identity contract remains unchanged.
- Tests: **11 new tests pass**; baseline 27 tests and all previous files remain
  unchanged. Preservation recheck passes **8,377 files and four archives**.
- Failure and recovery: the first build completed Color then stopped on Python
  integer keys versus JSON string keys in graph label histograms. Canonical
  hashes were already equal. Comparison was corrected; original code/error log
  and completed Color predictions were retained with hashes, without retuning
  or rerunning predictions. The first expanded main layout was nine pages;
  redundant prose was shortened, without font/margin changes.
- Evidence: `work/phase-2-machine-validation.json`,
  `work/phase-2-verification.json`, `work/phase-2-tests.txt`,
  `work/phase-2-paper-verify.log`, `work/phase-2-preservation-check.txt`.
- Pending genuine reviews: **694 original initial judgments**, not a synthetic
  completed QA set. Zero human judgments or model receipts were added.
- Next: user/main selects A or B under Phase 2.4 before stimulus expansion or
  advancing Phases 3--7. Updated website/release packaging remains downstream.
