# BrickPlan 2.0

Certified resource and inspection planning with matched visual observations.
This independent release preserves BrickPlan 1.0, 1.1 and 1.2.

[Paper + appendix](paper.pdf) · [Protocol](PROTOCOL.md) ·
[Revision response](REVIEW-RESPONSE.md) · [Evidence](VALIDATION.md) ·
[Full episode census](data/tasks.private.json)

## What changed

An exhaustive audit found that **all 1,802,728 preceding state–goal cost
labels equal a static blocker-closure formula**. Longer plans and more
rework had not established deeper planning.

Version 2 adds a finite rack and persistent off-assembly inspection jobs.
Each registered physical P piece fits one original S site; each detached
piece occupies a holder. Inspections must occur in the rack and remain
completed after reattachment. The original source poses, stud connectivity
and qualified straight insertion paths are retained.

| Release evidence | Result |
|---|---:|
| Source profiles / distinct source kits | 6 / 5 |
| Interactive episodes | 69 |
| D1 / D2 / D3 / D4 | 13 / 16 / 34 / 6 |
| Diagnostic responses | 196 |
| Matched pairs: interior order / history / changed work | 49 / 5 / 5 |
| Maximum exact cost above the strong static bound | 18 operations |
| Certified oracle tables | 35 |
| Product-state entries / directed transition entries across tables | 1,420,363 / 11,230,303 |

The state/transition totals repeat physical configurations under different
missions. The bank is selected using mechanism and solver evidence; it is
not an unbiased or blind test sample. Roadster and kart share source kit 31027.

## Measured controls

All rows below use privileged structural information and three tie-order
seeds over the same 69 tasks. These are software measurements, not VLM or
human results.

| Policy | Completed / 207 | Optimal / 207 | Successful mean regret |
|---|---:|---:|---:|
| Static-closure greedy | 189 | 91 | 12.39 |
| Resource-aware dispatch | 170 | 91 | 12.14 |
| Closure A*, 100 expansions | 162 | 162 | 0 |
| Closure A*, 1,000 expansions | 183 | 183 | 0 |
| Full closure A* | 207 | 207 | 0 |

Full closure A* needs at most **2,555 expansions**; weaker Hamming A*
needs up to 75,454. The task remains tractable given perfect relations.
At every selected next-action checkpoint, the depth-one heuristic's
minimizing set already includes an optimal action; tie ambiguity remains.
The release makes no claim of required internal model reasoning depth.
Raw plans and counts are in [software-control-records.json.gz](data/software-control-records.json.gz).

## Run the Arena

From the repository root, with Python 3.11+, a C compiler and the root Node
dependencies installed:

```bash
python3 -m venv benchmark/.runtime/brickplan-v2-env
benchmark/.runtime/brickplan-v2-env/bin/pip install -r benchmark/brickplan-v2/requirements.txt
npm ci
benchmark/.runtime/brickplan-v2-env/bin/python benchmark/brickplan-v2/server.py serve --port 8769
```

Open **http://127.0.0.1:8769/**. In this workspace, the existing Python runtime
can also be used:

```bash
env -u PYTHONPATH PYTHONNOUSERSITE=1 benchmark/.runtime/mlx-env/bin/python benchmark/brickplan-v2/server.py serve --port 8769
```

Choose an episode, inspect the current/target/reference/catalog/rack rasters,
and issue actions using the registered P/S IDs. Complete off-assembly work
with `audit`, acquire another camera using `inspect`, and explicitly finish
after satisfying the target and all jobs.

Saved camera views remain available. Ended practice episodes unlock scoring,
source-pose replay, free 3D orbit/zoom/explosion, and feedback JSON export.
Historical frames do not become executable states. Study mode restricts
these review features and uses a fixed observation condition.

## Run an isolated study

```bash
python benchmark/brickplan-v2/server.py configure /tmp/brickplan-run.json --run-id pilot-001 --participant participant-001 --track image-id --seed 31
python benchmark/brickplan-v2/server.py serve --config /tmp/brickplan-run.json --store tem/brickplan-v2/pilot-001 --port 8771
```

The configuration assigns the complete bank by default. `--assignments`
accepts a JSON object with `episodes` and `probes` lists containing internal
bank IDs. Partial pairs are omitted from pair denominators; missed assigned
members remain failures for joint correctness. Use a fresh store per
participant/condition/run. The server fixes IDs, assignments and seed.

On the evaluator host, collect authoritative records:

```bash
python benchmark/brickplan-v2/server.py collect --store tem/brickplan-v2/pilot-001 --output tem/brickplan-v2/pilot-001-collected.json
python benchmark/brickplan-v2/study.py template /tmp/brickplan-manifest.json
```

Fill the manifest's model/participant, server, prompt and external adapter
fields before `study.py run`. No provider adapter or paid call is bundled.
The adapter must actually send PNGs as images, enforce its declared limits,
and report complete usage, or declare accounting unavailable.
The policy working-directory rule is not a sandbox. See the
[trust and budget contract](PROTOCOL.md).

## Reproduce and verify

Use the configured Python environment. Runtime requires the frozen
`brickplan-v1.2/engine.py`, `visual.py` and `raster.c`; mesh regeneration
additionally uses the frozen v1 flattener and locked LDraw library.
Exact dependency hashes are in `data/release.json`.

```bash
python benchmark/brickplan-v2/audit_predecessor.py
python benchmark/brickplan-v2/build.py
python benchmark/brickplan-v2/validate.py
python -m unittest discover -s benchmark/brickplan-v2 -p test_protocol.py
python benchmark/brickplan-v2/controls.py
python benchmark/brickplan-v2/documents.py
benchmark/.runtime/tectonic -k --outdir benchmark/brickplan-v2 benchmark/brickplan-v2/paper.tex
python benchmark/brickplan-v2/release.py check
```

Rebuilding changes measured timings and may change PDF metadata; the frozen
manifest is expected to flag changed bytes. Inspect differences before
deliberately generating a new manifest with `release.py freeze`.
Use `release.py check` alone to validate an unchanged release.

For UI checks, start a separate practice store and run:

```bash
python benchmark/brickplan-v2/server.py serve --store tem/brickplan-v2/ui-test-fresh --port 8770
BRICKPLAN_TEST_URL=http://127.0.0.1:8770 node benchmark/brickplan-v2/test_browser.mjs
```

The browser suite uses the repository's Playwright Firefox installation.
Source requalification scripts and discovery logs remain archived under
`tem/research/20261008-brickplan-overhaul/`; admitted `source.json` and
`geometry.json` are included in this release.

## Scope and remaining empirical work

The seven measurement dimensions distinguish avoidable cost, budget loss,
choice horizons, survival, regret, recovery, replanning and matched
consistency as detailed in the paper. **Genuine irreversible dead ends are
absent**, so that rate is undefined.

D1–D4 are operational mechanism tiers. D4 is conditioned on a specific A*
threshold, and some D2 instances are computationally harder. Inspections
and their ledger are visible. This is known-site planning with rigid stud
support and an abstract rack, not a force simulator, free-pose manipulation
or a physical-construction experiment. Sports-car 5867 has only 10 movable
registered sites and remains an easy control.

VLM performance, human performance and physical validation are unmeasured.
The source partition has been used in task design. The paper retains these
limits and unfilled empirical slots.

Code follows the repository license. Source model/part licenses and authors
remain separate in [ASSET-LICENSES.json](ASSET-LICENSES.json).
