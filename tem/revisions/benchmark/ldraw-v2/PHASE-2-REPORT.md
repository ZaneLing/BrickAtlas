# Phase 2 report

Status: automated gates passed; external human review remains pending.

Added `analyze.py`, eleven machine-readable and Markdown contract cards,
deterministic descriptive JSON/CSV, two v2 TeX tables and a human review queue.
No questions or semantic answers were changed in this phase.

`python3 benchmark/suite/ldraw-v2/analyze.py --help` documents the CLI.
The initial run and `--verify` reproduction passed byte-for-byte.
Independent per-source aggregation agrees with the task-level cross-tab:

| Band | V | S | G | E | Total |
|---|---:|---:|---:|---:|---:|
| D1 | 17 | 21 | 33 | 12 | 83 |
| D2 | 34 | 47 | 69 | 25 | 175 |
| D3 | 14 | 15 | 23 | 7 | 59 |
| D4 | 75 | 86 | 108 | 31 | 300 |

D4 contains 194/300 S/G tasks. Source size is not measured item difficulty.
Graph-deletion's majority is 4 (44/73, 60.27%). Evidence-limit is constant
(24/24); the source-sequence six-action program is also constant (17/17).
The latter additional limitation is explicitly marked in contracts and tables.
Interface, coverage, step lookup and distance are evidence/arithmetic controls.
Instance-valued answers are source-scoped; the same label in different sets
does not denote the same physical instance.

148/593 nonempty-operand tasks share an exact operand set with another task
in the same source (24.96%; 74 matching pairs among 8,648 source-local pairs).
All 271 color/type/distance/restoration tasks share focal targets across
families, using only 73 distinct source-local targets.
Source-size/task-count Pearson r=0.949814, Spearman rho=0.904947. This reflects
size-dependent sampling and applicability, not evidence of cognitive difficulty.

The renamed graph-internal layer contains 73 G-only tasks. No family chains
observation contracts. Agent checked distance, interface and source-sequence
cards against actual inputs and independent oracles; all eleven cards were
read for consistency. This does not count as human review.

The queue includes all 140 visual items and 111 additional flagged items,
251 total. Reviewer, decision and rationale remain null. Physical candidate
review remains separate (573 pairs). No ambiguity is silently removed.
`freeze.py --verify`: all 2,131 protected files unchanged.

No machine failures remain. The documented constant program is a controlled
baseline limitation preserved under this phase's no-answer-change rule.
