# BrickAtlas Constructibility-1

Version: `brickatlas-constructibility-1`

This development release evaluates whether a proposed brick-construction
process remains nominally supported and tool-accessible, can recover from a
blocked action, adapts to a finite-inventory stockout, and avoids false
certainty under finite hidden-world ambiguity.

## Scope

The release contains 78 conditions derived from six previously public
Frontier structures:

| Family | Conditions | Required output |
|---|---:|---|
| `sequence-audit` | 18 | first failure, reason, legal-prefix length, decision |
| `blocked-recovery` | 18 | diagnosis, minimum rollback, legal continuation |
| `stockout-replan` | 6 | minimum stock-valid replacement, legal continuation |
| `clarify-or-commit` | 36 | admissible set, posterior, decision, next query |

The six structures, not the 78 derived conditions, are the independent source
groups. This is a public development set and not an independent confirmation
set.

## Geometry Contract

- Integer `X/Z` stud coordinates and `Y` plate-height coordinates.
- Top-down insertion and removal.
- Every elevated part needs at least one directly supporting stud.
- The brick body must have a clear vertical path.
- A named `west`, `east`, `north`, or `south` one-stud side strip must remain
  clear for tool release.

The last rule is a deterministic accessibility proxy. This release does not
measure force balance, clutch, tolerance, continuous robot motion, grasp
success, human ergonomics, or mechanism function.

## Files

- `public.json`: model-visible records.
- `oracle-private.json`: evaluator references.
- `algorithm-results.json`: public-information solver controls.
- `audit.json`: counts, process certificates, shortcut controls, claim limits.
- `frozen-protocol.json`: endpoints and reporting rules.
- `manifest.json`: release hashes.

## Commands

```bash
npm --prefix benchmark run constructibility:export
npm --prefix benchmark run constructibility:score -- predictions.json scores.json
```

Submission format:

```json
[
  {"id": "c1-...", "answer": {}}
]
```

Missing and malformed answers remain in the denominator. Report task families
separately and keep raw-model, fixed-harness, and tool-assisted results in
different tables.
