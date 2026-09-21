# LDraw-2 staged upgrade ledger

The controlling document is `CODEX_BENCHMARK_UPGRADE_PLAN.md` (read only).
All phases are executed in dependency order. Automated checks are not human
certification. No model inference or training has been run for LDraw-2.

## Phase 0 — passed, with documented legacy build prerequisites

- Frozen 2,131 existing files, including 24 model-input JSON files, 24 internal
  scoring bundles, original sources, v1 implementation and publication assets.
- Generator and scorer copied byte for byte into `benchmark/suite/ldraw-v2/`.
- `sources` is a read-only-by-policy reference to the original source directory.
- Examined runtime locks with nonblocking lock acquisition and relevant process
  listings: no active experiment writer found. Historical result files and
  their manifests backed up; they are not LDraw experimental evidence.
- Ran the unchanged `npm run --prefix benchmark ldraw:build` in a disposable
  copy. All 75 generated site files equal frozen v1 bytes.
- Ran independent source reparse: 24 sources, 15,334 instances, 617 tasks,
  1,606 negative controls, 75 public-action solves, 2,317 dependency hashes.
- Original v1 CLI has two pre-existing environment defects: retired candidate
  manifests were moved out of `public/models`, and the verifier's parser reads
  `assets-source` relative to npm's working directory. Only the temporary copy
  supplies links for these dependencies. The original CLI/files remain unchanged.
- Evidence: `phase-0-checks.json`, `phase-0-runtime.json`,
  `phase-0-v1-build.txt`, `phase-0-v1-verify.txt`, `v1-frozen-manifest.json`.
- Repeat preservation check: `python3 benchmark/suite/ldraw-v2/freeze.py --verify`.

## Evidence-based interpretations of conflicting checklist requirements

1. The guide asks for 10 sampled questions covering 11 families. Use at least
   11 (one per family). Agent inspection must not be labeled human review.
2. Evidence-reading controls intentionally expose their operand evidence.
   “Cannot derive answers from public input” means no non-target answer encoding;
   it cannot prohibit solving the task from its declared evidence.
3. A constant predictor can guess individual items correctly by chance.
   A shortcut is a reliable non-target generation rule, not any correct guess.
   Report hit counts and remaining answer priors, never pretend they are zero.
4. Graph-removal options have an unsatisfiable constraint: 63/73 frozen answers
   equal the maximum legal component count. Four distinct legal numeric options
   force these correct answers to be maximal, so semantic rank cannot be balanced
   while preserving graphs and answers. The least invasive repair is integer
   response for all 73 graph-removal items, preserving every graph, target and
   semantic answer. This is an explicit deviation from Phase 1.1's four-option
   recipe, required to avoid replacing the second-smallest shortcut with a
   largest-option shortcut. Source-step retains four legal numeric options and
   balanced semantic ranks. The corpus remains 617 items / 11 families.
5. Actual v1 visual PNGs use `isolated-original-poses-numbered` rendering
   (`capture-inputs.ts` and `input-renders.json`), contrary to the guide's
   full-scene description. Full-scene and operand-only paired images must be
   newly defined in v2, and experiments must name the actual observation.
6. A confidence interval containing zero does not establish equivalence or
   absence of contribution. Implement the requested operational no-detected-
   contribution reporting, but reserve equivalence/absence claims for an
   explicitly preregistered equivalence margin and adequately narrow interval.
7. Related-work table claims use the conservative rules in Sections 1.4/9:
   unverified capabilities remain “to verify”, even where later instructions
   suggest categorical negative claims. Diagnostic localization remains a
   prospective validity question without intervention experiments.

## Phase 1 — automated gates passed; human visual adjudication pending

- 617 items, 11 families, 24 sources and every semantic answer preserved.
  Formats are now 396 single-choice, 73 multiple-choice, 73 integer and 75 actions.
- S1: graph-removal integer responses remove option-rank/offset encoding by
  construction. The documented boundary conflict above required this deviation.
- S2: source-step semantic ranks are 14/14/14/13; all four distinct candidates
  lie within the actual author-step range. Chi-square 0.054545, p=0.996667.
  These statistics describe the balancing, not a leakage proof.
- S3: shape-match internal answer-reference positions are 14/13/13/13/14.
  Chi-square 0.089552, p=0.999027. A global hash permutation was chosen to meet
  the aggregate balance constraint; it never assigns slots by answer role.
- S4: no references enter requests. On internal objects the original slice
  coincides by chance on 5/73, and the most successful preregistered fixed
  slice coincides on 8/73. Neither is a deterministic answer rule.
- Additional repair: interface items always offer all five connector families;
  v1's answer-dependent 4/5 option count exposed stud answers.
- Strict requests retain English question, response format, necessary input,
  anonymous option IDs/labels and image bytes. Removed references,
  targetModule, capabilities, evidence, evidenceDetail, answer, option.value,
  redundant missingInstanceIds, render-only full-scene state and internal
  source-path metadata. The public-precondition execution contract remains.
- 617 independent source/evidence oracle checks passed; 75/75 actions solved
  from public facts. 5,154 negative controls passed; all 24 internal paths
  rejected by the model-input loader; 617 canaries blocked and snapshots checked.
- Rebuilding reproduces all 666 compared files byte for byte, including 617
  actual message snapshots with base64 PNGs. TypeScript check passed.
- Agent inspected one public request from each of the 11 families:
  `ld2-31028-{color,shape-match,distance,interface,neighbors,graph-removal,
  evidence-limit,restore-instance}-1` and
  `ld2-10156-{coverage,source-step,source-sequence}-1`. The observed operations
  match their declared evidence. Source fields for controls intentionally
  permit direct lookup; they are not called visual reasoning.
- Pixel spot-check: `ld2-31028-shape-match-1.png` loads and contains five
  B-number labels without answer attributes. Occlusion of stacked plates
  illustrates why source-oracle agreement is not human perceptual approval.
- Evidence: `verification.json`, `shortcut-report.json`, `task-audit.json`,
  `source-audit.json`, `request-snapshots/manifest.json`, `reproducibility.json`.
- v1 preservation rechecked: all 2,131 hashes unchanged.

## Phase 2 — automated gates passed; human review pending

- Eleven contract cards and four deterministic descriptive analyses completed.
- D1 V/S/G/E=17/21/33/12; D2=34/47/69/25; D3=14/15/23/7;
  D4=75/86/108/31. Graph-deletion majority=44/73 (60.27%).
- Additional measured limitation: all 17 source-sequence responses are the
  same six-action program. Marked as a fixed-program control, alongside the
  24 constant evidence-limit answers.
- 148/593 nonempty-operand items share an exact source-local operand set;
  271 focal-family tasks use 73 source-local targets across families.
- Size/count Pearson r=.949814, Spearman rho=.904947; no difficulty inference.
- Queue: 140 visual plus 111 additional flagged items, all pending.
- Reproduction and preservation checks passed; `PHASE-2-REPORT.md`.

## Phase 3 — optional extension skipped by the guide's default

- Scope: modular competencies, no within-item V/S/G/E chaining.
- Diagnostic localization remains unvalidated, not established by aligned IDs.
- No integration-residual or score-product analysis. `PHASE-3-REPORT.md`.

## Final stages

- Phase 4: automated gates passed — 14 executable conditions, 3,147 request
  checks, 146 changed-answer graph interventions, 576 ID round trips, 907
  paired/perturbed images with all 140 items independently rerendered byte for
  byte. Sole runner saved 617 actual standard wire requests plus 14 canaries;
  model API calls remain zero. Six candidate adapters; moving aliases require
  a frozen revision before live use. `PHASE-4-REPORT.md`.
- Phase 5: automated gates passed — 6-page English main manuscript,
  181-page complete supplement, all 617 dossiers, generated tables/vector
  figure and 264 blank model-result cells. Independent v2 review site passed
  production-browser checks for all 24 models and versioned feedback.
  Shared UI/CLI scoring, publication parity and all 2,131 v1 hashes verified.
  `PHASE-5-REPORT.md`, `DELIVERY.md`, and `benchmark/paper/BUILD-v2.md`.

## Human/external evidence that automation cannot invent

The 140 visual questions need independent human review of label readability,
color and near-identical shape ambiguity. The 573 non-mating intersection pairs
remain physical review candidates. Neither source reparse nor answer-oracle
agreement certifies physical stability or perceptual validity.
