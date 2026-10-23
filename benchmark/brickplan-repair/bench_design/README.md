# Current organization and evaluation specification

Authoritative task view: `deliverables/brickplan-benchmark-spec/questions.jsonl`.
Historical raw banks and stored answers remain unchanged. `canonicalId` maps
physical aliases within a task contract; retain execution conditions for paired
prefix evaluation. Never sum raw conditions as independent tasks.

Read the illustrated Chinese overview and evaluation document in that output
folder. The current object-dynamic runner rejects arbitrary crops and legacy
mechanism diagnostics unless `--diagnostic` is explicitly provided.

Rebuild with `PYTHONPATH=benchmark/brickplan-repair` and the project's
`benchmark/.runtime/mlx-env/bin/python`:

1. `-m bench_design.audit` — fresh physical reference replay, no model calls.
2. `-m bench_design.visibility` — new complete-object reference pixel checks.
3. `-m bench_design.catalogue` — canonical task view, taxonomy, structural grades.
4. `-m bench_design.illustrate` — native comparison examples.
5. `-m bench_design.write_docs` — overview and model catalogue.
6. `-m unittest bench_design.test_metrics -v` — metric attribution regressions.

`-m bench_design.run_episode --id <canonical-or-retained-id>` starts a local
one-action environment. It calls no model. Its `inputVersion` records the unified
direct-action envelope; old measured input formats must stay separate.

`-m bench_design.score results.jsonl` aggregates explicit normalized result
records. Actual API collection, event-damage qualification, source-cluster CIs,
standalone detection and checkpoint tasks still require integration. The paired
metric functions refuse incomplete eligibility evidence.
