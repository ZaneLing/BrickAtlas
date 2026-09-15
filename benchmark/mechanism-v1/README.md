# BrickAtlas Mechanism-1

Mechanism-1 is the new publication-facing benchmark layer. It contains six
original, whole, articulated brick-system designs rather than imported OMR
geometry or random-growth structures.

## Original Objects

1. Orbital Service Rover
2. Harbor Container Crane
3. Bascule Canal Gate
4. Adaptive Radio Observatory
5. Wildfire Tiltrotor
6. Polar Research Station

The designs contain cabins, wheels, axles, gears, rotating assemblies,
sliding carriages, service bays, payloads, sloped surfaces and moving joints.
OMR/LDraw models are used only as visual-complexity references and are not
benchmark cases.

## Eight Task Families

| Family | Capability |
|---|---|
| Prefix Dynamics | stability of every construction prefix |
| Insertion Access | continuous swept-volume service access |
| Fault Recovery | causal joint diagnosis and minimum repair |
| Inventory Substitution | finite-stock structural replacement |
| Dynamic Robustness | transient and residual displacement under impulse |
| Functional Kinematics | revolute/prismatic mechanism operation |
| Active Inspection | information gain per inspection cost |
| Multiobjective Design | Pareto cost/mass/stiffness reasoning |

There are 48 tasks: every family is paired across all six source designs.

## Engine

Rigid-body dynamics, fixed/revolute/prismatic joints, motor actuation and
shape casts use `@dimforge/rapier3d-compat` 0.20.0. The engine is an external
Apache-2.0 dependency. Simulator results do not claim calibrated LEGO clutch
forces, material failure or robot execution.

## Files

- `index.html`: visual browser for every model, task, capability and question.
- `CASEBOOK.zh-CN.md`: all 48 questions, abilities, oracles and model outcomes.
- `MODEL_REPORT.zh-CN.md`: model-level summary.
- `ALL_MODELS.png` / `TASK_MATRIX.png`: complete visual overviews.
- `models.json`: original model geometry, modules and joints.
- `public.json`: model-visible task records.
- `oracle-private.json`: evaluator answers.
- `audit.json`: counts, engine configuration and claim boundaries.
- `frozen-protocol.json`: task contracts and reporting rules.

## Development Results

| Model | Exact success |
|---|---:|
| Qwen3-0.6B local text | 3/48 |
| GPT-4.1 mini | 28/48 |
| Gemini 2.5 Flash | 31/48 |

The two cloud models receive one task render plus the same structured
evidence. The local baseline is text-only. These six-source results are
descriptive and do not support a population ranking.
