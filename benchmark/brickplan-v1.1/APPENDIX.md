# BrickPlan 1.1 — Technical appendix

Generated from certified tasks and executed validation evidence, 2026-10-02.

## Source bank and exact graph

| Case | Fixed / movable | Reachable states | Directed edges | Full optimum | Chain parts / edges |
| --- | ---: | ---: | ---: | ---: | ---: |
| roadster-body | 20 / 17 | 14,012 | 131,824 | 17 | 4 / 3 |
| kart-deck | 7 / 18 | 44,604 | 436,824 | 18 | 4 / 3 |
| airframe | 3 / 21 | 284,088 | 2,274,432 | 21 | 5 / 4 |

Total: 342,704 reachable states and 2,843,080 directed transitions, across 2 source groups. Roadster and kart share LEGO 31027; airframe uses LEGO 31028. No independent sample count is inferred from state counts.

Airframe mandatory source-index chain: 3 → 8 → 16 → 30 → 32. This is private audit notation. Public part/site IDs are randomized.

## Geometry contract

All selected source poses and original render geometry are preserved. The airframe includes 0–34 except 11–14 and 21–27; its fixed connected base is 1, 2, 5. It excludes the propeller, float/clip assemblies, and main wing plates. The upstream 54383/54384 wing proxies have extensive nonmanifold and boundary edges; they are excluded without repair. Their dependent top plate 27 is also excluded. Sources 9, 10 and 15 remain at their original poses but now belong to the mutable task. Each included motion and endpoint pair is requalified using the frozen 1.0 geometry algorithm, not the old sampled discovery record.

Airframe: 276 endpoint pairs, 483 motion pairs, 43 blocked paths, 0 unknowns, 52 stud connector edges, 5 checked goal tables.

The [1.0 appendix](../brickplan-v1/APPENDIX.md) remains normative for coordinate conversion, connector support, inset meshes, clearance covers, the source-verified 3022 repair, exact cost proofs, observation fields, and metric edge cases. Inset is 0.25 LDU per surface; guard is 0.002 LDU. No force, hand access, free rotation, or gravity claim is added.

## Episode ledger

| Case | Mode | Installed | Optimal actions | Minimum detaches | Budget |
| --- | --- | ---: | ---: | ---: | ---: |
| roadster-body | full | 0 | 17 | 0 | 26 |
| roadster-body | checkpoint | 3 | 14 | 0 | 21 |
| roadster-body | repair | 11 | 12 | 3 | 18 |
| roadster-body | healthy | 11 | 6 | 0 | 18 |
| kart-deck | full | 0 | 18 | 0 | 27 |
| kart-deck | checkpoint | 3 | 15 | 0 | 23 |
| kart-deck | repair | 17 | 7 | 3 | 11 |
| kart-deck | healthy | 17 | 1 | 0 | 11 |
| airframe | full | 0 | 21 | 0 | 32 |
| airframe | checkpoint | 3 | 18 | 0 | 27 |
| airframe | repair | 17 | 10 | 3 | 15 |
| airframe | healthy | 17 | 4 | 0 | 15 |

Each start has a reachability witness. Every completion witness is replayed and cost-certified. Healthy/repair pairs match installed count and action budget.

## Counterfactual conditional costs

| Case | Goal member | Conditional costs | Optimal offered index |
| --- | --- | --- | ---: |
| roadster-body | a | 16 / 18 | 0 |
| roadster-body | b | 18 / 16 | 1 |
| roadster-body | control-0 | 15 / 17 | 0 |
| roadster-body | control-1 | 15 / 17 | 0 |
| kart-deck | a | 3 / 5 | 0 |
| kart-deck | b | 5 / 3 | 1 |
| kart-deck | control-0 | 8 / 10 | 0 |
| kart-deck | control-1 | 10 / 12 | 0 |
| airframe | a | 17 / 19 | 0 |
| airframe | b | 19 / 17 | 1 |
| airframe | control-0 | 18 / 20 | 0 |
| airframe | control-1 | 18 / 20 | 0 |

Indices above are canonical private candidate indices. Public positions are independently permuted. Both candidates are required in paired goals. The optimum is over the two offered closures, not all available actions.

## Release binding and reproducibility

`runtime.activate()` binds one process to the combined bank before importing executor modules. Original data and frontend code are relative read-only symlink dependencies. Banks are verified on first load and shared in memory; restart after rebuilding. The 1.0 files retain their frozen hashes. New data, figures, documents, and meshes are stored here. The freeze records both extension artifact hashes and the base manifest hash.

Runtime: Python 3.11+ standard library; geometry/render generation additionally uses the same NumPy, meshlib, BrickNet, locked LDraw assets, Three.js and Playwright versions as 1.0. Document generation uses Pillow for margin-only crops of native replay screenshots. All source licenses are in ASSET-LICENSES.json.

## Study boundary

Supplied-plan conflict distances remain 1/2/4/8 with causal depth one. The larger mandatory assembly chain does not redefine that metric. This is still D1 diagnostic coverage. Software controls, browser replays and exhaustive states are not measured model or human trials.
