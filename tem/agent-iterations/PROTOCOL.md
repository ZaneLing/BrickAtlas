# BrickAtlas two-agent review and revision protocol

Requested by the user on 2026-09-22. These are internal simulated academic
reviews, not official CVPR decisions or guarantees of acceptance.

## Roles and ownership

- **CVPR reviewer** independently reviews the current research snapshot.
  Owns only `round-NN/review.md` and `round-NN/review.json`.
- **Research refiner** implements benchmark and manuscript repairs from the
  independent review. Owns research edits and `round-NN/response.md`,
  `round-NN/changes.json`.
- **Orchestrator** fixes integration defects, checks evidence and figures,
  records snapshots and validation, communicates every round and commits/pushes
  each completed iteration. It does not override a scientific recommendation.

Agent instructions are persisted at `.trae/skills/cvpr-reviewer/SKILL.md`
and `.trae/skills/research-refiner/SKILL.md`.
Review and revision phases operate sequentially on research artifacts.
Independent preparation may run concurrently without overlapping writes.

## User's experiment-complete assumption

For review, assume the declared model runs and human-review collection have
been completed competently and can fill reserved tables. Do not reject solely
because numeric cells or human judgments are not present in the workspace.
Do not assume any particular favorable score, ranking reversal, visual
answerability, statistical significance or empirical superiority.
Judge whether the actual design could support the stated claims across
plausible outcomes, and state result-dependent conclusions conditionally.

This assumption does not authorize fabricated results, synthetic human
responses, paid API calls, or statements that real collection occurred.
It does not waive missing task definitions, ground-truth defects, trivial
shortcuts, incorrect metrics, dataset dependence, unsupported physical claims
or an incoherent contribution. Implementation and construction work remains
in scope for the refiner.

## Fixed rubric and stop condition

Use a 1--10 recommendation scale:
1--3 reject, 4--5 weak reject/borderline, 6 weak accept, 7--8 accept,
9--10 strong accept. Record confidence on 1--5.

Independently assess:
1. Scientific contribution and distinction from closest prior work.
2. Construct validity and the relation between inputs and claimed abilities.
3. Dataset task depth, sampling, diversity, dependence and held-out evaluation.
4. Ground truth, scoring, edge cases, failure denominators and shortcuts.
5. Experiment design and uncertainty under the stated completion assumption.
6. Reproducibility, traceable figures and faithful source geometry.
7. Clear benchmark narrative, readable examples and CVPR format/fit.

Stop successfully only after at least two review/revision interactions,
the independent reviewer gives **accept or strong accept (score >= 7)**,
and there are **zero unresolved critical or major issues** on the latest
verified research snapshot. A final audit checks that the accepted snapshot
matches committed research files and that all required verification passes.
Minor limitations may remain if explicitly documented and compatible with
acceptance. No fixed iteration cap; iteration count does not affect scoring.

If an unavoidable external blocker prevents meaningful progress, record it
honestly; do not weaken the rubric or fabricate closure to stop.

## Review schema

`review.json` contains `round`, `snapshot_sha256`, `assumption`,
`score`, `confidence`, `verdict`, `criteria`, `issues`, `closed_prior_issues`,
`residual_limitations`, and `acceptance_rationale`.
Each issue has `id`, `severity` (critical/major/minor), `status` (open/closed),
`summary`, `evidence`, `why_it_matters`, and `closure_test`.

## Per-round records

For round NN, preserve:

- `snapshot.json`: file paths and SHA256 before review, plus base commit.
- `review.md/json`: immutable independent scientific assessment.
- `response.md`, `changes.json`: issue-specific repairs and unresolved points.
- `validation.json`: verification commands and observed pass/fail outcomes.
- `report.md`: Chinese user report with verdict, changes, evidence and next action.

Track iteration state in `state.json`. Store intermediate material only here;
current paper stays in `paper/`, current datasets/evaluators in `benchmark/`.
Preserve the unrelated dirty `assets-built/e2e-report.json`.
Push without force to the existing authorized branch `codex/v3-five-issues`.
