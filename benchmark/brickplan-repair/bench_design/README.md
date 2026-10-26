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

The active `Session` adapter is `brick-atlas-direct-actions-full-context/2`.
The published task catalogue still records the earlier `/1` snapshot; the new
runtime version is separate from task identity. Version two adds neutral full
position cards on inspect-part and visible-piece point inspection on module
tracks, using the same public interface for people and models. It explicitly
states the held-fixture / ideal rigid manipulation assumptions.

`-m bench_design.score results.jsonl` accepts normalized run records, new private
records containing `normalizedResult`, and paired evaluation JSONL. It reports
run groups and qualified pair groups separately. `session.py` records every
decision, the state after the actor's move and before any intervention, a
verified incident ledger, public-packet/image hashes and snapshots, and recovery
windows ending before the next event. Untriggered/unverified repair is N/A.

`-m bench_design.run_pair --id ... --prefix prefix.jsonl --control-actions normal.jsonl
--fault-actions fault.jsonl --output ...` executes an explicit shared prefix and
two continuations without a model API. Non-scripted actors additionally need
matching actual full-request-context hashes before formal pair eligibility.
Provider collection/billing, source-cluster CIs, independent detection and
checkpoint task banks remain separate work; scripts are never model scores.

## Current independent quality round

`-m bench_design.launch_review` opens persistent local A/B/C click-only operation
and mechanical-review pages. `--no-open` starts the server without opening a tab.
`--manager` opens the private aggregate view. Participants can submit one task
at a time; independent answers are not copied between identities.

The additive targeted conditions, independent Manifold Boolean spotchecks,
scripted execution evidence, and human protocol are documented under
`deliverables/brickplan-quality-round/README.zh-CN.md`. New conditions remain
outside the published count until independently admitted. `quality_validate`
replays them through the actual unified judge. `test_quality_ui.mjs` must use
an isolated `/tmp` participant directory, never real human storage.
