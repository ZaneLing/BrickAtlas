# Full-Casebank Paper Audit

This additive audit leaves the frozen v2 generator, task definitions, scoring
contracts and historical predictions unchanged. It makes two paper claims
reproducible without model API calls.

## Source Census

The census reads the committed `casebank-v2/structures.jsonl.gz` after checking its
manifest hash and the frozen generator/scorer source hashes. It records one row
per source, catalog instances, containing objects, split counts, piece counts,
height, colors, type counts and contact-edge counts.

The population contains 5,120 sources and 19 assembled types out of the 25-type
catalog. Zero-frequency catalog types are explicitly retained. Source counts
must not be replaced by task, color, image or part-instance counts.

## Copy-Current Control

The predictor is `copyInputAnswer(publicTask)`. It returns only public `current`,
unchanged; repair additionally returns an empty fault-ID array. It does not read
reference images, hidden targets, changed IDs, or oracle answers.

Scoring covers seven endpoints, each once per source:

- Ordinary suffix completion.
- Symbolic rotation, recoloring and removal.
- Ordinary no-fault, color-fault and shift-fault repair.

There are 35,840 cases but only 5,120 sources. Copying gets 87.1% global part F1
on completion and 97.4% on removal with zero success. No-fault repair succeeds
unchanged by design. The whole-source population includes training data; this is
a descriptive control census, not a held-out neural comparison.

## Reproduce

From the repository root with Node 22 and installed repository dependencies:

```bash
node node_modules/tsx/dist/cli.mjs benchmark/suite/study/paper-audit.ts
node node_modules/tsx/dist/cli.mjs benchmark/suite/study/paper-audit.ts --verify
node node_modules/tsx/dist/cli.mjs --test benchmark/tests/paper-audit.test.ts
```

The first command regenerates `../artifacts/study/paper-audit/`. The second
recomputes and compares all records and the census without writing outputs.
`audit.json` binds the selection, compressed control records, source inventory,
frozen source hashes and strict evaluator version. `copy-controls.jsonl.gz`
retains each case's metrics and source/policy/split for further stratification.

Paper tables and figures are generated from this evidence using the commands in
`../../paper/README.md`. The seven future experiment matrices live in
`../../paper/experiments.json`; they are proposed, not frozen or measured.
No census or regression test substitutes for independent human metric calibration,
external-domain evaluation, or a newly frozen confirmation study.
