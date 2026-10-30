# Brick Atlas

A benchmark connecting static brick repair with autonomous recovery during continuous assembly.

[简体中文](README.zh-CN.md) · [Repository map](REPOSITORY-MAP.zh-CN.md) · [Historical versions](REPOSITORY-HISTORY.md)

## Current release

**310 runnable object configurations; 4,685 checked questions: 1,600 static and 3,085 dynamic.** There are 57 complete builds and 253 contextual finishing tasks. The 437 acquired source objects are a source pool, not the runnable-model count. Retired and withheld records remain discoverable outside the published denominator.

| Artifact | Entry point |
|---|---|
| Release status and question bank | [Dataset guide](deliverables/brick-atlas-dataset-v1/README.zh-CN.md) · [manifest](deliverables/brick-atlas-dataset-v1/release.json) |
| Final case audit and exclusions | [Final report](deliverables/brick-atlas-dataset-v1/FINAL-CHECK.zh-CN.md) |
| Models, errors, question counts | [Full list](deliverables/brick-atlas-dataset-v1/MODEL-AND-QUESTION-LIST.zh-CN.md) |
| Current states, targets, and GT | [Local review page](http://127.0.0.1:8810/dataset/) · [illustrated examples](deliverables/brick-atlas-dataset-v1/EXAMPLES.zh-CN.md) |
| Input/output and metrics | [Protocol guide](deliverables/brick-atlas-dataset-v1/INPUT-OUTPUT-AND-METRICS.zh-CN.md) |
| Paged sensing, matched-state comparison and portable runtime | [2026-10-30 implementation and checks](deliverables/brick-atlas-reliability-v1/README.zh-CN.md) |
| API, truncation, tool schema and case checks | [Experiment readiness fixes and evidence](deliverables/brick-atlas-experiment-readiness-v2/README.zh-CN.md) · [run commands](deliverables/brick-atlas-experiment-readiness-v2/RUN.zh-CN.md) |
| Shared visual agent and real API pilot | [Results, replay, scorer correction and costs](deliverables/brick-atlas-unified-agent-v1/README.zh-CN.md) · [experiment groups](deliverables/brick-atlas-unified-agent-v1/EXPERIMENTS.zh-CN.md) |
| Paper | [Main PDF](paper/brickplan-cvpr/main.pdf) · [supplement](paper/brickplan-cvpr/supplement.pdf) · [Overleaf ZIP](paper/brickplan-cvpr/brickplan-cvpr-overleaf.zip) |
| Build instructions and pending study | [Paper guide](paper/brickplan-cvpr/README.zh-CN.md) |
| Historical count reconciliation | [Count changes](deliverables/brick-atlas-dataset-v1/COUNT-CHANGES.zh-CN.md) |

Dynamic agents explicitly request observations, inspect parts/instructions, attach, detach, recall, and finish. One physical part moves per action. Final physical equivalence accepts alternative legal orders. Service failures and untriggered incidents are not mislabeled as repair failures.

**Status: machine checked; independent human qualification, independent physical validation, and full current-interface model experiments remain pending.** A selected paid visual-agent pilot is now archived separately; it is not a full ranking. Scripted reference success is not model performance. Qwen uses Aliyun and DeepSeek uses its native API, as specified in `AGENTS.md`.

## Local use

From the repository root, using the existing project environment:

```bash
PYTHONPATH=benchmark/brickplan-repair benchmark/.runtime/mlx-env/bin/python -m dynamic_arena.server --port 8810
```

Open the [current dataset](http://127.0.0.1:8810/dataset/). The [historical directory](http://127.0.0.1:8810/dataset/all-questions.html) separates active, withheld, retired, and unchecked records.

```bash
PYTHONPATH=benchmark/brickplan-repair benchmark/.runtime/mlx-env/bin/python -m scaling_release.release_check
PYTHONPATH=benchmark/brickplan-repair benchmark/.runtime/mlx-env/bin/python -m unittest scaling_release.test_contract bench_design.test_metrics
npm run paper:build
```

Force a complete replay with `scaling_release.check --force` and `scaling_release.legacy_check --force`, then regenerate catalogues and rerun the release gate. See the final audit report for the full sequence.

The active manuscript is `paper/brickplan-cvpr/`. Earlier dataset, interface, and manuscript versions remain separate historical artifacts; their counts and model results do not extend this release. See [web development](web/README.md) and the [historical guide](REPOSITORY-HISTORY.md) for earlier workbench features.
