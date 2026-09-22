# Interface Analysis Contract v1

This is an additive analysis repair for visual-repair-v1, not a new task
family. The content-locked `analysis_contract` has schema
`visual-repair-interface-v1`; implementation is in `joint.py` and `study.py`.
No model or human measurements are supplied by synthetic regression tests.

## Same-Task Events and Effects

For each planned task and attempt, define A as atomic binding correctness,
O as oracle exact-repair correctness, M as multimodal exact-repair correctness.
The join key is `(id, construction_id, dependence_group, split, replicate,
structural_arm, visual_arm, repeat)`. The public task ID already identifies
its construction/cell/ID replicate; the extra fields explicitly check alignment.
One attempt, repeat 0, is currently supported.

The eight `contingency` keys are the strings `000`, `001`, `010`, `011`,
`100`, `101`, `110`, `111`, in A/O/M order. Their counts sum to the full
planned task count for that analysis set and split, not three times that count.
For each dependence group g, let e_g count A=O=1 slots and f_g count
A=O=1,M=0 slots. The operational conditional interface failure is
J = P(M=0 | A=1,O=1).

- Primary J: equal-weight mean of f_g/e_g over groups with e_g > 0.
- Secondary micro J: sum(f_g)/sum(e_g).
- `eligible_n` is sum(e_g); `eligible_groups` counts e_g > 0 groups;
  `failure_n` is sum(f_g). Counts are reported even when J is undefined.
- Groups with no jointly competent slots have null group J. They are excluded
  from the macro J average, explicitly counted, and retained in resampling.
- No eligible slots gives null J, not zero error or perfect performance.

The paired effects are `delta_repair = M_exact - O_exact` and
`delta_binding = M_binding - A_binding`, first differenced on the same task.
Primary effects equally weight the means of all planned dependence groups;
secondary micro effects equally weight planned task slots. They do not use
J's competency filter. An empty analysis set has null effects.

This is an operational comparison of supplied conditions, not evidence of an
internal causal reasoning mechanism. Neither isolated marginal accuracy nor
its product substitutes for J. J may be zero, positive or undefined; effects
may be positive, zero or negative. No particular empirical outcome is assumed.

## Dependence and Failures

For each comparison/set/split, one seeded matrix of 2,000 bootstrap draws
resamples the sorted complete dependence-group vectors with replacement
(NumPy default_rng seed 20260922). The identical draws apply to J and both
contrasts, retaining all conditions, shared anchors, faults and both ID
replicates together. The primary interval recomputes the mean of defined
group values; the secondary interval recomputes the pooled numerator over
pooled denominator. This is not subtraction of independent marginal intervals.

A draw containing no J-eligible group is undefined, omitted from J's
percentiles, and counted through `bootstrap_defined_draws`. J intervals are
null with fewer than two eligible groups. Effect intervals are null with fewer
than two planned groups. Leave-one-group-out means also preserve null empty
cases. These intervals describe finite-source sensitivity, not broad population
inference or a remedy for having only ten held-out groups.

Missing planned receipts, malformed/invalid responses, refusals and adapter
errors score false for all corresponding success events; their slots remain
in contingency counts and effects. An absent receipt is not an absent planned
condition. Absent required configurations or incomplete/mismatched planned
task membership cannot produce a comparison. A graph-only model has
`interface: []` and `interface_status: not_planned_missing_required_conditions`.
Missing responses for a planned condition instead contribute failures.

## Compatible Locks

The manifest explicitly declares `comparison_groups`, each containing `id`,
`system_id` and `config_ids` for atomic, oracle and multimodal conditions.
All three configurations must have identical system identity, evidence kind,
revision, settings and repeats under one run lock. Model identity must also
equal the run's model ID. Adapter bytes and native packets/images are hashed
under that lock. Cross-run receipts, even from identically named models, are
rejected; independently locked runs are not silently pooled. Cross-condition
joining occurs only inside the explicit common run lock.

The three local algorithm comparisons are **modular references**, pairing
each pixel rule's atomic and composed conditions with the shared exact oracle.
They are not learned-model interface results or three independent oracle runs.
The existing fifteen configurations and their actual responses are retained.

## Qualification and Collection

`qualification-eligibility.json`, schema
`visual-repair-construction-eligibility-v1`, binds the base study lock, queue
lock, validated raw human receipts/adjudications, recomputed qualification
report, and sorted `sets.full` / `sets.qualified` construction IDs. Its
`lock_sha256` hashes the entire artifact except that hash field. Verification
reruns the strict qualification validator; an edited summary or list is not
sufficient, even if rehashed.

Construction status precedence is `rejected`, `pending`, `needs_adjudication`,
then `qualified`. A rejected arm rejects the construction, even if other arms
are pending. Otherwise any pending arm keeps the construction pending; any
unadjudicated concern prevents qualification. All arm states remain visible.
Counts for these construction statuses are mutually exclusive.

Only fully qualified constructions enter the qualified set. All twelve
observations, conditions and ID replicates of each retained construction enter
together. The full set is never replaced. The currently empty qualified set
means pending human review, **not rejection of 84 constructions**.

Portable `lock` embeds this validated artifact before collection; `collect`
and `analyze` verify it, and analysis cannot substitute later eligibility for
that run. The lock retains **all full-set observations for collection**, even
for rejected or pending constructions, so both denominator branches remain
available. A different qualification snapshot requires a separately declared
run lock, not post-outcome filtering of an existing run. Qualification evidence
is evaluator-side and never enters the model payload. Hash/provenance checks
cannot by themselves authenticate that a claimed human is a real person.

Local `study.py all` freezes packets, executes deterministic algorithms,
freezes the empty qualification queue/eligibility, then analyzes both sets.
After real qualification, use `qualification.py validate` to create the
validated eligibility artifact and supply `--eligibility` to analysis or
portable locking. Do not rerun the empty queue command over collected evidence.

## Paper/Machine Schema

`baseline-report.json` and portable analysis use the same report schema.
Existing `configurations[].{dev,heldout,all}` remain full-set metrics.
Their qualified counterparts are
`configurations[].qualified.{dev,heldout,all}`. `analysis_sets` reports
construction IDs/counts and task counts, and `qualification` reports all
statuses. `model_results` and `human_results` remain null in the local report.

Each `interface[]` record retains its comparison IDs and contains
`{full,qualified}.{dev,heldout,all}` with:

| Field | Meaning |
|---|---|
| `planned_count`, `groups` | Task slots and dependence groups in this branch |
| `contingency` | All eight integer A/O/M counts |
| `group_counts` | Per-group planned, eligible, failure counts and all eight cells |
| `joint_failure_given_atomic_oracle` | J estimates and eligibility below |
| `delta_repair`, `delta_binding` | Same-task contrast estimates |
| `bootstrap` | Seed, draw count, sorted group order and null-draw policy |

Each estimate contains `n`, `micro`, `group_macro`, `groups`, `group_values`,
`ci95_group_sensitivity`, `ci95_micro_group_sensitivity`,
`bootstrap_defined_draws`, and `leave_one_group_out`. J additionally contains
`eligible_n`, `eligible_groups`, `failure_n`, `zero_eligible_groups`.
Zero-eligible groups appear as null values in J's `group_values`.

The five proposed paper interface columns for the full held-out set map to:

1. Jgroup: `joint_failure_given_atomic_oracle.group_macro`
2. eligibleN: `joint_failure_given_atomic_oracle.eligible_n`
3. eligibleG: `joint_failure_given_atomic_oracle.eligible_groups`
4. deltaRepair: `delta_repair.group_macro`
5. deltaBind: `delta_binding.group_macro`

Use the identical paths under `qualified` for the common qualified counterpart,
with its construction/task and qualification counts alongside. Planned model
table cells, including eventual count cells, stay null until actual collection;
machine algorithm counts are not model measurements.

## Adapter Diagnostics

Each portable receipt includes `diagnostics.schema =
visual-repair-adapter-diagnostics-v1`, `stdout`, `stderr`, `stdout_base64`,
`stderr_base64`, `returncode`, `timed_out`, `timeout_seconds`,
`exception_type`, and `exception_message`. Text streams decode UTF-8 with
replacement for readability; base64 streams retain exact bytes. Unavailable
streams/return codes are null, and empty captured streams remain empty strings.
Timeouts retain available partial streams. Nonzero exits/timeouts keep null
response and an error, even when their partial stdout resembles a valid answer.
Successful malformed stdout remains available to the semantic parser. No retry
or successful-only selection is introduced.
