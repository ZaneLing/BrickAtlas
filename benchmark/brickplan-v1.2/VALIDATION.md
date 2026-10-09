# BrickPlan 1.2 acceptance evidence

All results here are software validation, not model or human performance.
Evidence is in `tem/brickplan-v1.2/validation/`, with immutable release hashes
recorded by `release-check.json`.

## Certified data

- 3 structures / 2 provenance groups / 15 episodes / 87 probe responses.
- 342,704 reachable states, 2,843,080 directed transitions.
- All inherited goal tables rechecked against the complete reachable graph.
- Geometry and source poses unchanged; no new unknown geometry admitted.
- All 15 optimal episode witnesses replay successfully in both observation tracks.
- New reconfiguration optimal action counts: roadster 30, kart 24, airframe 34.

## Shortcut and metric validation

- 36 matched continuation pairs, 72 responses, spanning plan lengths 4/6/8.
- Same-pair public observation, first/last action and action multiset are identical.
- Defined conflicts are geometric motion/support conflicts at interior positions.
- First/last shortcut: 36/72 exact; full private replay: 72/72.
- Data-derived evaluation census, missing-episode censoring at time zero.
- Invalid attempts affect budget but do not inflate legal-choice denominators.
- Self-induced event detection after prior successful actions, restoration,
  recurrence, first-diagnosis freezing, terminal unrestored and censored outcomes.
- Forged state results and changed task budgets rejected by authoritative replay.

See `semantic-summary.json`. Eleven acceptance groups contain multiple assertions.

## HTTP and browser

Real HTTP checks run in both `image-id` and `known-pose-structured` study servers:
all probe types, idempotent retries, stale revisions, private-route rejection,
cross-origin rejection, persisted inspection budgets, answer freezing and
post-trial score/replay restrictions. Public exports contain no private bitmasks.

Firefox 141.0 executes six complete sessions through visible DOM controls:
injected repair and reconfiguration for each structure. Every session reaches
the exact goal with zero action regret, performs a charged inspection and
diagnosis, and validates replay, public trajectory download and feedback JSON.
Displayed-probe identity remains stable when the selector changes before opening
another probe. Desktop and 390px mobile layouts have no horizontal overflow;
no page errors were recorded.

See `http-summary.json`, `browser-summary.json`, screenshots and public exports.
These browser sessions follow evaluator reference actions and are not human trials.

## Honest controls

| Control | Episode success |
|---|---:|
| Exact oracle | 15/15 |
| Privileged static relation rule | 15/15 |
| Privileged bounded search depth 1 | 9/15 per seed |
| Privileged bounded search depth 2 | 9/15 per seed |
| Privileged bounded search depth 4 | 9/15 per seed |
| Public structured greedy | 2/15, 2/15, 3/15 |
| Privileged legal-action random | 0/15 per seed |
| Blind public-ID random | 0/15 per seed |

Oracle and static rules have one run; other controls have three seed runs.
No random control is instructed to choose a known trap. Private relation access
is not comparable to a public image observation. Repeated seeds do not increase
source diversity. The static rule's success remains a substantive difficulty
limitation, explicitly included in the paper.

## Release integrity

`freeze.py` checks the original 1.0 and 1.1 artifact manifests, acceptance
summaries, oracle success/regret, release/report census, manuscript existence,
replay-figure hashes and private task certificates before recording the 1.2
artifact hashes. The external evidence paths and hashes are also recorded.

No VLM/human data, physical construction validation, new support-rerouting
mechanism or publication acceptance is asserted by these checks.
