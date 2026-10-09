# BrickPlan 2.1: response to six research concerns

This independent release preserves v1/v1.1/v1.2/v2. The revised paper centers
on visual future-cost prediction and delayed error recovery.

| Concern | Implemented change | Evidence and remaining limit |
|---|---|---|
| Early-conflict shortcut dominates continuation tests | 72 pairs balanced across conflict positions 2–5, 6–10 and 11+; identical legal prefix, endpoints and action multiset | Prefix@2 is 80/144 (55.6%); @5 is 96/144 (66.7%), versus 74.5%/93.9% in v2. This addresses the measured shortcut, not every possible shortcut. |
| Solver-conditioned tiers imply cognitive depth | D1–D4 now exclusively mean optimal-operation-length bins 1–8/9–16/17–24/25+; separate capacity/jobs/gap/search descriptors | 16/47/46/36 episodes. All 230 next-action probes still admit a correct depth-one heuristic choice; no required internal depth claim. |
| Too few sources and reused “held-out” structures | Eleven source groups, with all previously used groups marked development; 36 seeded episodes from three new groups | Eight development / three new-source groups. Geometric pruning was refined after initial collisions, before new-source solver results; this deviation and the first-pass census are disclosed. |
| Recovery collapses to immediate undo or reaching the goal | 333 delayed checkpoints after 1/3/5 operations, exact nonterminal optimal-corridor return distance, overlapping event retention | Minimum repair costs 1–6; independent BFS verification. Immediate recovery remains a secondary diagnostic. |
| Vision is incidental to textual scheduling rules | Four geometry pairs preserve registered pieces/poses, start/goal, rack/jobs and plan while changing qualified fixed support context; 12 appearance pairs preserve answers | All four answer-changing geometry pairs currently use one development source and unequal fixed-part counts. Equal-count/type zero-yield candidates are published. |
| Manuscript reads as revision history, not a benchmark paper | Official CVPR main/supplement; explicit taxonomy and reporting design; related work covers LTRON, InstructioNet, LEGO-Puzzles including Planning, PhyBlock and BC-Bench | Updated tables and original-source figures are hash-bound to the 145-episode/739-question bank. Population model and human cells remain unmeasured. |

## Presentation, integration, and publishing

- Native 1920×1440 main views, 480×360 piece tiles, 2× supersampling,
  high-DPI canvases and native zoom replace low-resolution raster enlargement.
- The bilingual homepage lists seven categories with full question previews,
  stable IDs, inputs, output format and scoring before an attempt starts.
- Actual local MLX and OpenAI-compatible vision adapters support run/step/stop.
  The first local four-call SmolVLM case is preserved, including every raw
  response and `INVALID_ACTION` feedback. It is a failed integration case.
- Portable evaluator/data ZIP, public JSONL, seven HD examples, Dataset card,
  Docker Space and static-site folders are provided. No public upload or
  deployment URL is claimed.
- The official template is pinned and unmodified. The retrieved author-kit
  labels itself 2026; it is not represented as a verified future-year kit.

## What the measured evidence supports

Full closure A* solves all 435 repeated runs with a maximum of 4,372
expansions. Closure greedy completes 384 but is optimal in 266; capacity
dispatch completes 367 and is optimal in 266. These structural controls
demonstrate measurable cost and constraint effects under the abstraction.
They also show that exact structural planning remains modest in size.

The package supports a concrete model-format/cost pilot and then a matched
image/structured study. It does not establish CVPR acceptance, a human–model
gap, general computational hardness, unrestricted physical realism, or
shortcut immunity. Those empirical and scope limits are explicit throughout.
