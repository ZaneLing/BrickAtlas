# Issue 2: node prior and structural evidence

Analysis version: `ldraw2-evidence-v1`.
Implementation/data acceptance: passed. Model comparisons: not run; no raw
v2 model responses exist in the inspected workspace.

## Replication on the unchanged natural distribution

The predictor accepts only the public node-label list and writes its
predictions before the scoring code loads any internal answers. All 73 frozen
standard request hashes are checked against the original snapshot manifest.

- Node-only successes: 63/73, micro 86.3014%.
- Source macro: 83.75%, 24 sources.
- Source-cluster bootstrap 95% interval: 72.9167% to 93.125%.
  This interval describes source sampling of the algorithmic baseline, not
  uncertainty in the exact census count.
- Deficit zero: 63 items across 23 sources.
- Positive deficit: 10 items across 9 sources. Every item is retained and the
  failure list is explicit in `node-prior-audit.json`.
- Both BFS and independently implemented union-find agree with each stored
  original gold and every intervened gold.
- The independent Python intervention exactly matches the frozen TypeScript
  `alteredGraph()` edge list on all 73 deletion items.

| Algorithmic control | Natural micro | Original/intervened both-correct |
|---|---:|---:|
| Node count minus one | 86.3014% | 0% |
| Fixed answer 4 | 60.2740% | 0% |
| Graph connected components | 100% | 100% |

All use the same 73 parents and 24 sources. These are implemented baseline
results, not learned-model results. The five-issue guide already identified
the node prior; this is a post-hoc replication, not a newly preregistered
discovery. Old scores and golds remain unchanged.

## Independent challenge and feasibility limits

The ten positive-deficit items and one-direction original intervention cannot
establish broad topology sensitivity. A bounded extension therefore uses
exact parent node labels with hypothetical edges, separately from all 73
natural items.

- 219 observations from 73 parents / 24 existing sources.
- Three observations per parent and at most 15 per source.
- 146 pairs: 37 answer increases, 36 decreases, 73 answer-preserving changes.
- Every pair matches node set, unique edge count and target degree.
- Twelve answer-changing pairs additionally match surviving degree sequence.
- For the 61 parents with only four/five survivors, the declared path/triangle
  templates do not match surviving degrees. The 61 gaps are recorded.
- The 73 answer-preserving pairs are isomorphic survivor relabelings.
- Hypothetical edge counts/topologies do not pretend to match the original
  source graph or describe physical connections.
- No new source is counted. Original tasks are not replaced or filtered.

Opaque observation IDs are shuffled with a fixed seed; each request has no
history and no parent, transformation or answer-direction metadata.
The model input says explicitly that the supplied graph is hypothetical.
The rules and extension manifest were frozen before any new model response.
The executable runner created 219 actual offline requests with zero API calls.
New model inference is necessary to obtain model performance on this extension;
old natural results cannot be reused as new challenge results.

## Verification and traceability

Commands from the repository root:

```sh
python3 benchmark/suite/ldraw-evidence/node-prior-audit.py
python3 benchmark/suite/ldraw-evidence/matched-graphs.py
python3 benchmark/suite/ldraw-evidence/verify-matched-graphs.py
.tools/node-v22.23.2-darwin-arm64/bin/node node_modules/tsx/dist/cli.mjs benchmark/suite/ldraw-evidence/verify-graph-parity.ts
.tools/node-v22.23.2-darwin-arm64/bin/node node_modules/tsx/dist/cli.mjs benchmark/suite/ldraw-evidence/run-matched-graphs.ts --adapter benchmark/suite/ldraw-v2/model-adapters/gpt41.json --out benchmark/ldraw-evidence-v1/matched-graphs-v1/dry-run-gpt41
```

The last directory already exists; never overwrite it. A repeated offline
capture must use a fresh directory. `--execute` is the explicit network mode.

All commands passed. The independent cycle/two-triangles fixture verifies
different answers despite identical node/edge/degree statistics; duplicate
edges, reverse directions and isolated vertices are also checked.
No task/source exclusions occurred. Human visual and physical status did not
change.

Original file hashes and actual bytes: `baseline-lock.json` and
`v2-before-five-issues.tar.gz`. New inputs/results and their hashes:
`node-only-predictions.json`, `node-prior-audit.json`,
`graph-parity-verification.json`, `graph-challenge-rules.json`,
`matched-graphs-v1/manifest.json`, `inputs.json`, `verification.json`,
`independent-verification.json` and `dry-run-gpt41/manifest.json`.
All implementation changes are new files under `benchmark/suite/ldraw-evidence/`.

The next issue can proceed: paired gold and baseline definitions are concrete.
It must add semantic evidence-following metrics without reinterpreting
zero accuracy difference as zero evidence use.
