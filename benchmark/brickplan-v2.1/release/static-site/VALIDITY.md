# Task validity and scope in BrickPlan 2.1

The release contains 145 interactive episodes and 739 diagnostic questions.
The main taxonomy is task mechanism. D1–D4 are **optimal-operation-length bins**
(1–8, 9–16, 17–24, 25+) and do not measure necessary reasoning depth.

## Future-sequence controls

The 72 interior-order pairs use an exact legal completion and a reordered
sequence with the same first action, last action and action multiset. Both
sequences have an identical legal prefix before the first conflict. No no-op
padding or repeated-state walks are used. The 2–5, 6–10 and 11+ conflict-position
bins each contain 24 pairs.

A control that executes only the first two operations and otherwise predicts
“all legal” scores **80/144 (55.6%)**; the corresponding five-operation control
scores **96/144 (66.7%)**. Frozen v2 scored 73/98 (74.5%) and 92/98 (93.9%).
These are software shortcut audits, not language-model results.

## Source sampling

Eight development source groups are 10001, 10156, 10159, 10220, 31009, 31027,
31028 and 5867. The three new-source groups are 10014, 10128 and 31031.
Alternate builds and geometry variants stay within their source group.
Previously used sources are no longer described as held out.

`source-plan.json` records source candidates and seeded task sampling before
new-source geometry and solver discovery. After an initial all-or-nothing
geometric pass failed on source collisions, the qualification procedure was
refined to remove conflicting source instances in deterministic source order
and retain a stud-connected component. This refinement occurred before any
new-source solver or policy result. It does not move or invent bricks.
The first pass and refinement must not be described as an unchanged,
fully preregistered geometry algorithm.

Task starts, goals and work orders on these sources use seeded sampling;
admission depends on geometric qualification and solvability, not policy
performance, heuristic gap or expansion count. Easy cases are retained.
Geometry rejection reasons and the exact retained source indices are released.
New-source sampling does not imply that the source models were absent from
foundation-model pretraining.

## Visual context and appearance controls

Four answer-changing future-sequence pairs (eight questions) hold registered
pieces, source poses, initial occupancy, goals, capacity, work orders and the
proposed plan constant. Only an induced subset of the original fixed support
context changes. Both contexts are independently requalified against collision
meshes and straight-motion paths. The first conflict occurs after a shared
legal prefix of at least two actions.

These retained contrasts currently come from **one development source group**.
Their fixed-context part counts differ, so they are not count-matched visual
counterfactuals. Equal-count/type candidates from other sources were qualified
but did not yield an answer-changing retained sequence. The full census is
reported, including zero-yield candidates.

Twelve additional appearance pairs (24 questions) compare original-color and
grayscale observations of the exact same state and plan. Answers must remain
unchanged. These are diagnostic controls, not independent source examples.

## Delayed repair

The 333 delayed-repair questions start after a certified legal but avoidably
costly action and a fixed lag of 1, 3 or 5 subsequent legal operations.
The executed history visits distinct states and remains outside the pre-error
optimal corridor. Repair means reaching a **nonterminal** state on any optimal
completion from the pre-error checkpoint. Reaching the goal alone does not
count. Exact checkpoint-specific minimum repair costs range from 1 to 6.

The evaluator separately tracks spontaneous errors, immediate return, and
delayed cohorts at lags 1/3/5. Earlier errors remain active when later errors
occur. Successful completion, conditional excess and optimal completion are
primary outcomes; immediate inverse-operation repair efficiency is secondary.

## Qualification and unresolved empirical claims

`audit_v21.py` replays every retained contrast, checks identical prefixes and
action multisets, verifies source-group separation, and checks delayed repair
against an independent forward BFS. `validate.py` covers exact oracle
trajectories, all diagnostic answers, assignment denominators, state tampering,
recovery, action budgets and observation isolation.

The geometry contract is conservative stud connectivity plus prescribed
straight translations over guarded inset meshes. It is not a force simulator,
free-pose assembly or unrestricted robotics benchmark. A depth-one heuristic
can remain competitive; finite-horizon tie bounds do not establish a model's
internal reasoning depth. Population VLM and human experiments remain pending.
