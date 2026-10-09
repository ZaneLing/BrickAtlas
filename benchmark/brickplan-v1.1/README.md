# BrickPlan 1.1

Executable assembly-order diagnostics: **3 structures, 2 source groups, 12 episodes, 39 probe responses**. Adds a certified original LEGO 31028 airframe with 21 full-build actions and a 5-part mandatory chain. Frozen 1.0 remains unchanged.

| Case | Fixed / movable | Reachable states | Directed edges | Full optimum | Chain parts / edges |
| --- | ---: | ---: | ---: | ---: | ---: |
| roadster-body | 20 / 17 | 14,012 | 131,824 | 17 | 4 / 3 |
| kart-deck | 7 / 18 | 44,604 | 436,824 | 18 | 4 / 3 |
| airframe | 3 / 21 | 284,088 | 2,274,432 | 21 | 5 / 4 |

All three repair starts require three removals. Seven dimensions retain the [metric contract](PROTOCOL.md): dead-end choice, lookahead, survival, regret, recovery, replanning efficiency and counterfactual consistency. This is a known-pose, straight-path D1 diagnostic release; no model/human performance is reported.

[Paper PDF](paper.pdf) · [Paper source](paper.tex) · [Appendix](APPENDIX.md) · [Validation](VALIDATION.md) · [Release certificate](data/release.json)

## Run

From the repository root, Python 3.11+:

```bash
python3 benchmark/brickplan-v1.1/run.py serve --port 8767
```

Open **http://127.0.0.1:8767**. Select a task, assemble or detach by stable IDs, diagnose, then finish for scoring, trajectory export, feedback JSON and stepwise 3D replay. Only the target reference can be exploded. The installed assembly uses original source poses.

In this workspace, replace `python3` with `env -u PYTHONPATH PYTHONNOUSERSITE=1 benchmark/.runtime/mlx-env/bin/python`.

The [1.0 Client](../brickplan-v1/client.py) works with `Client('http://127.0.0.1:8767')`; the [API/action contract](../brickplan-v1/README.md#model-api) is unchanged. Use the 1.1 launcher for collection/evaluation:

```bash
python3 benchmark/brickplan-v1.1/run.py collect --store RUN_DIRECTORY --metadata METADATA_JSON --output SUBMISSION_JSON
python3 benchmark/brickplan-v1.1/run.py evaluate SUBMISSION_JSON --output REPORT_JSON
```

Use a fresh store per controller. Repeated runs require explicit `--selection`. Policies must be isolated from local private certificates and post-trial review tools.

## Reproduce

```bash
python3 benchmark/brickplan-v1.1/prepare.py assets
python3 benchmark/brickplan-v1.1/run.py build --geometry
python3 benchmark/brickplan-v1.1/run.py render
python3 benchmark/brickplan-v1.1/prepare.py assets
python3 benchmark/brickplan-v1.1/checks.py
python3 benchmark/brickplan-v1.1/run.py evaluate tem/brickplan-v1.1/validation/oracle.submission.json --output tem/brickplan-v1.1/validation/oracle.cli-report.json
python3 benchmark/brickplan-v1.1/check_http.py
# Start a fresh 1.1 server on port 8767, then:
python3 benchmark/brickplan-v1.1/prepare.py fixtures
BRICKPLAN_BROWSER=firefox node benchmark/brickplan-v1.1/check_browser.mjs
python3 benchmark/brickplan-v1.1/documents.py
python3 benchmark/brickplan-v1.1/freeze.py
```

The shared runtime is imported from `../brickplan-v1`; keep both directories together. Only new cases are rebuilt. Existing 1.0 data are read-only references. A running process caches its certified bank; restart it after rebuilding.

Original LDraw geometry/attributions: [ASSET-LICENSES.json](ASSET-LICENSES.json). Kinematic proxy certificates do not certify clutch force, gravity, hand access, or all continuous assembly paths. Free-camera browser practice is not a matched vision-only trial.
