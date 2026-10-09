# BrickPlan 1.0

An executable diagnostic benchmark for assembly-order planning, future feasibility,
and recovery. Release date: 2026-09-30.

**Implemented:** two original LDraw structures, eight episodes, 26 probe responses,
exact finite-state evaluation, a shared human/API workcell, and 3D replay.
**Scope:** known-pose, kinematic, single-part assembly along declared straight paths.
No VLM or human performance has been measured.

| Entry | Purpose |
| --- | --- |
| [PROTOCOL.md](PROTOCOL.md) | Frozen definitions of all seven diagnostics |
| [data/release.json](data/release.json) | Counts, geometry/task/cost hashes, exact graph certificates |
| [paper.pdf](paper.pdf) · [paper.tex](paper.tex) · [APPENDIX.md](APPENDIX.md) | English research manuscript and implementation details |
| [VALIDATION.md](VALIDATION.md) | Acceptance evidence and limitations |
| [client.py](client.py) | Public model adapter; standard library only |
| [arena/](arena/) | Actual source meshes, interactive assembly, replay, feedback export |

## Cases and evaluation

| Case | Source parts | Fixed / movable | Reachable states | Full optimum | Minimum repair detaches |
| --- | ---: | ---: | ---: | ---: | ---: |
| roadster-body | 37 | 20 / 17 | 14,012 | 17 | 3 |
| kart-deck | 25 | 7 / 18 | 44,604 | 18 | 3 |

Both structures derive from LEGO 31027: **one provenance group**. They are not
independent train/test partitions. Each has a four-part mandatory chain, with
three dependency edges. This is a D1 diagnostic release, not evidence of
100-step or deeply nested planning.

Each structure supplies full, checkpoint, repair, and matched healthy episodes.
The probes comprise one legal-action decision, eight first-conflict predictions
(distances 1/2/4/8, each with an executable control), and four counterfactual
members (a switch pair and an invariance pair).

| Dimension | Executable output |
| --- | --- |
| Dead-end choice rate | No-undo and remaining-budget losses, response coverage |
| Lookahead | Exact first-conflict accuracy, conflict recall, false alarms by distance |
| Plan survival | First-loss curves with lower/upper censoring bounds |
| Regret | Attempted-action and detach regret; failures have `null` regret |
| Recovery | Diagnosis recall/precision, completion, joint success |
| Replanning efficiency | Detaches, distinct removed parts, wasted actions, first useful repair |
| Counterfactual consistency | Joint correct switching and correct invariance, position counts |

No weighted composite score is defined. Budgeted complete success remains the
headline outcome. Every metric reports its denominator.

## Run the Arena

From the repository root, use Python 3.11+ and the repository's installed
`three@0.180.0` package:

```bash
python3 benchmark/brickplan-v1/server.py --port 8766
```

Open **http://127.0.0.1:8766**. In this workspace, the isolated Python command is:

```bash
env -u PYTHONPATH PYTHONNOUSERSITE=1 benchmark/.runtime/mlx-env/bin/python benchmark/brickplan-v1/server.py
```

Choose a task and start an episode. Select any public site and inventory ID, then
attach or detach. The executor checks the current path and connection support.
It permits legal actions that cause future rework. Submit a diagnosis before
the first successful structural action if reporting checkpoint detection.
Finish to unlock scoring, stepwise 3D replay, trajectory export, and feedback JSON.

The reference model can be exploded. The actual assembly stays at source poses.
An empty selected site is shown as a wireframe, not an installed brick.
All placements and all available inventory remain selectable, including invalid
combinations. The interface supplies no next-step feasibility mask.

The browser's free camera is a practice/review feature. Human practice results
must not be reported as a matched vision-only comparison to the JSON SDK.
The server binds to loopback and is a local development service.

## Model API

| Method and route | Contract |
| --- | --- |
| `GET /api/tasks` | Opaque episode IDs, visible structure/start type/budget |
| `POST /api/sessions` | `{taskId, seed?}` → session ID, public task ID, observation |
| `GET /api/sessions/{id}` | Current observation and revision |
| `POST /api/sessions/{id}/actions` | `{requestId, revision, action}` |
| `GET /api/sessions/{id}/history` | Public action journal |
| `GET /api/sessions/{id}/score` | Terminal-only episode score |
| `GET /api/sessions/{id}/export` | Terminal-only authoritative trajectory |
| `GET /api/sessions/{id}/replay` | Terminal-only observation frames |
| `GET /api/probes` | Opaque probe IDs and response kinds |
| `GET /api/probes/{id}` | Scene, visible goal, candidates or proposed plan |
| `POST /api/probes/{id}/answer` | One frozen response, no label feedback |

Actions:

```json
{"type":"attach","partId":"P001","siteId":"S003"}
{"type":"detach","partId":"P001"}
{"type":"inspect","view":"isometric"}
{"type":"diagnose","needsRework":true}
{"type":"finish"}
```

The IDs above illustrate the schema; use IDs from the current observation.
An attach/detach or malformed action costs one attempt, including failures.
Inspections and diagnoses have separate quotas. `finish` costs no structural
attempt. Inspection views: isometric, front, rear, left, right, top, bottom.
The goal is exact occupied-site equality; an extra installed part is not success.

Retries use the same `requestId`, revision, and action. They are idempotent.
A stale revision is rejected without charge. Reusing an ID for another request
is rejected. Journals are atomically persisted and replayed after server restart.

Import `Client` from `client.py` and call:

```python
client = Client("http://127.0.0.1:8766")
result = client.run_episode(task_id, policy, seed=31)
client.run_probes(probe_policy)
```

`policy(observation, history)` returns one action; `probe_policy(public_probe)`
returns `{"choice": integer}` (zero-based) or `{"firstConflict": integer_or_null}`
(one-based). Each policy receives only public information. A production trial
must isolate the policy process from local private task/cost files and from
post-trial review tools. Seeds randomize stable instance/site IDs and candidate
positions; they do not create new structures.

## Collect and score a run

Start each controller in a fresh `--store` directory. Record model/provider/version,
prompt, seed, token/context/observation budgets, reasoning settings, retry policy,
cost, and whether the run used images or JSON.

```bash
python3 benchmark/brickplan-v1/collect.py \
  --store tem/brickplan-v1/my-run --metadata metadata.json \
  --output tem/brickplan-v1/my-submission.json
python3 benchmark/brickplan-v1/evaluate.py \
  tem/brickplan-v1/my-submission.json --output tem/brickplan-v1/my-report.json
```

Multiple attempts on the same task require an explicit `--selection` JSON map
from private task ID to session ID; the collector never silently picks the best
run. Preregister that selection rule. Unfinished/missing episodes remain in
denominators. Early stops appear as unresolved censoring in survival bounds.
Probe order is privately normalized before scoring.

## Reproduce validation

These commands run software controls, not paid model experiments:

```bash
python3 benchmark/brickplan-v1/validate.py
python3 benchmark/brickplan-v1/validate_http.py
```

The first command checks all frozen goal tables and adversarial metric/runtime
cases. The second uses an isolated temporary server and tests eight complete
HTTP episodes, all 26 probe responses, frozen answers, replay, persistence,
collection, and evaluation.

For UI validation, run a server on port 8766 with a **fresh** store, then:

```bash
python3 benchmark/brickplan-v1/prepare_ui_validation.py
node benchmark/brickplan-v1/validate_arena.mjs
```

The UI control executes one full build (including a rejected wrong part) and one
three-detach repair through actual buttons, checks replay/downloads, probe
identity, desktop/mobile layout, and saves screenshots. It requires installed
Playwright and Chrome. Reports and screenshots go to `tem/brickplan-v1/validation/`.
Do not mix these labelled oracle controls with model submissions.

To regenerate the four manuscript frames from the completed UI session, compile
the English PDF with Tectonic, and package the acceptance snapshot:

```bash
node benchmark/brickplan-v1/render_paper.mjs
python3 benchmark/brickplan-v1/build_paper.py
python3 benchmark/brickplan-v1/freeze_release.py
```

## Rebuild certification

`build.py` rebuilds graph costs/tasks from frozen geometry using only Python's
standard library:

```bash
python3 benchmark/brickplan-v1/build.py
```

`build.py --geometry` also requalifies source poses, connections, endpoints, and
paths. It additionally needs NumPy, meshlib, BrickNet's connector catalog/inset
meshes, the locked LDraw library, and the source manifests in this repository.
`render_assets.py` regenerates the browser's original source triangles with NumPy.
Exact dependency versions and source references appear in the appendix.

## Attribution

Models and parts retain their upstream provenance; see each `data/*/source.json`,
`data/render-provenance.json`, and [ASSET-LICENSES.json](ASSET-LICENSES.json).
The bundled browser triangles are derived from the locked LDraw parts library.
Part author/license notices are preserved in that attribution file. Source
geometry is unchanged; collision proxies are separate, declared approximations.
LEGO and LDraw names identify the source assets, not sponsorship.
