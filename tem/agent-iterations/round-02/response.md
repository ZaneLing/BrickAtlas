# Round 02 Research-Refiner Response

Assigned issues: BA-004 (major) and BA-006 (minor). This implementation addresses
their benchmark-side closure tests without introducing a new task family.
It does not change the reviewer's 5/10 weak-reject verdict or declare acceptance.
Main owns paper/index integration, publication validation, snapshots and git.
This run wrote only `benchmark/visual-repair-v1/` and this round's
`response.md` / `changes.json`.

## BA-004: Same-Task Interface Analysis and Qualification

### Joint and Paired Readout

`joint.py` implements the content-locked `visual-repair-interface-v1` contract.
A is isolated atomic binding correctness, O is oracle exact repair, and M is
multimodal exact repair on the same task, construction, cell, ID replicate and
attempt. Each split and analysis set reports all eight A/O/M contingency counts,
per-group counts, and J = P(M=0 | A=1,O=1), with eligible task/group denominators
and the failure numerator. This is operational and noncausal, not a product of
marginal scores or a claim about an internal mechanism.

Paired effects are multimodal-minus-oracle exact repair and
multimodal-minus-atomic binding, differenced on the same planned tasks.
Primary estimates equally weight dependence-group means; micro estimates are
separate. J's macro estimate includes only groups with eligible tasks, with
zero-eligible groups explicitly recorded as null. All readouts use the same
2,000 whole-group bootstrap draws, seed 20260922, keeping all conditions,
shared anchors, faults and ID replicates together. Zero-eligible groups remain
in draws. All-ineligible J draws are omitted from percentiles and counted;
J's interval is null with fewer than two eligible groups. Empty sets and
empty joint eligibility produce null estimates, never zero error by convention.

The manifest declares explicit comparison groups. Joins require the same run
lock, system/model identity, revision, settings, evidence kind and repeat
contract. Exact task/cell membership is checked. Independently locked runs are
not pooled, even for identically named models. Missing receipts in a planned
condition remain failed slots; absent or incompatible planned conditions cannot
yield a fabricated complete-case comparison. Invalid responses, refusals and
adapter errors also stay in the contingency/effect denominators as failures.

### Common Qualification

`qualification.py` derives `qualification-eligibility.json` from validated
raw receipts/adjudications and the frozen queue/base-study locks. Validation
recomputes its decisions; rehashing an edited summary or membership list is
insufficient. Construction statuses distinguish rejected, pending,
needs-adjudication and qualified, with arm-level states retained.

`study.analyze` emits both full and qualified branches, without replacing any
full denominator. Qualification retains or excludes all twelve observations
of a construction together, identically across conditions. Existing full-set
configuration fields remain available. Portable locking embeds the validated
eligibility snapshot before collection; collection still plans the full set,
and later analysis cannot substitute different eligibility for that run.
Current human evidence is empty: 84 pending, zero rejected, zero qualified.
Thus all qualified-set performance estimates are null.

The exact integration contract is
`benchmark/visual-repair-v1/ANALYSIS.md`. Main was given:
`interface[].{full,qualified}.{dev,heldout,all}`, with `contingency`,
`joint_failure_given_atomic_oracle`, `delta_repair`, and `delta_binding`.
The five paper columns map to J's `group_macro`, `eligible_n`,
`eligible_groups`, and the two contrasts' `group_macro` fields. Main reports
updating its proposed interface table to 13 VLM rows and 212 total null cells.
Publication regeneration/compilation/verification is Main's remaining handoff,
not an action claimed by this refiner.

### Regression and Preserved Evidence

The synthetic aligned/disjoint regression has identical complete marginal
reports but J failures of 0/24 versus 24/24. Additional tests cover zero
eligibility, null intervals, unequal group sizes, shared bootstrap draws,
missing conditions/attempts, malformed outputs, incompatible locks, duplicate
cells, off-study or edited qualification, and construction-wide exclusions.

The no-exclusion integration test uses the actual retained algorithm receipts
and a strictly in-memory qualification fixture. Every configuration and
interface full/qualified branch matches, including nonzero performance.
No synthetic judgment is saved as human evidence.

An additional read-only comparison against reviewed commit
`72db15006cfa89f80922857e2b29b79d342fdd0e` confirmed:

- All 15,120 actual algorithm responses are identical, except the newly
  required study-lock hash in their envelopes.
- All 45 existing configuration/split metric blocks are exactly unchanged.
- Silhouette remains 624/684 held-out exact repairs, 0.9122807017543859 micro
  and 0.7829090909090909 group macro; its shallow-solvability gate still fires.

The newly measured **modular algorithmic reference**, not a learned model,
has silhouette J=0 with 624 eligible held-out tasks in eight groups,
deltaRepair=-0.21709090909090908 group macro, and deltaBind=0.
J=0 follows the shared exact-solver composition and is not evidence of learned
integration competence or a favorable human/model result.

Disposition: benchmark implementation and tests supplied; independent review
of the integrated paper/research snapshot remains required.

## BA-006: Retained Failed-Adapter Diagnostics

Portable receipts now include `visual-repair-adapter-diagnostics-v1`:
stdout/stderr text, lossless base64 stream bytes, return code, timeout status
and limit, exception type and message. Available partial timeout streams are
retained. Unavailable streams or return codes are null. Nonzero exits/timeouts
still have a null response and error, even if partial stdout resembles an
answer. Successful malformed stdout remains available to the semantic parser.
There are no retries or successful-only selection.

Five mocked tests cover nonzero exits (including non-UTF-8 bytes), partial
timeouts, timeouts without streams, launch errors, and successful malformed
stdout with stderr. No adapter or model was executed by those tests.

Disposition: implementation and mocked closure tests supplied; independent
review, not this response, determines issue closure.

## Verification and Handoff

Executed once after locked code stabilized:

```sh
env -u PYTHONPATH PYTHONDONTWRITEBYTECODE=1 PYTHONNOUSERSITE=1 benchmark/.runtime/mlx-env/bin/python benchmark/visual-repair-v1/validate_all.py
```

All seven stages passed: byte-identical constructor regeneration, independent
graph/pixel/source audit, refreeze and actual local study replay with pending
qualification and analysis, 56 Python tests (42.798 seconds), TypeScript,
and the no-judgment browser canary. The audit reproduced 1,008 semantic answers,
336 visual pairs, 2,520 native card views and 144 mesh files.
`benchmark/visual-repair-v1/validation.json` retains commands and raw outcomes.

New study lock:
`d1edb0a10b83abba434dc202a18c17570b89a992706ab2384380e20fc13fddc2`.
Eligibility lock:
`2a424617a365608f4d157f10cd91166942158ca75225219de2229fc4cb83507e`.
Code and generated artifacts are stable for Main's publication rebuild.

All external model/human results remain uncollected/null. No purchases, human
calls, model calls, commits or pushes occurred. Reviewer files, rubric,
historical sealed datasets, source assets and unrelated
`assets-built/e2e-report.json` were not edited by this run.

Remaining scientific limits are unchanged: shallow-solvable binding, ten
held-out groups, finite-source sensitivity, pending human-visible uniqueness,
possible public-CAD contamination, small exhaustive graphs, and no physical
repair guarantee. Local zero J does not predict model J. Continue honest
independent iterations until the protocol's score-at-least-seven and
zero-unresolved-major/critical criteria are actually met; code completion is
not an instruction to raise the review score.
