# Task validity and scope in BrickPlan 2.2

The release contains 377 interactive episodes and 1,952 diagnostic questions.
The main taxonomy is task mechanism. D1–D4 are **optimal-operation-length bins**
(1–8, 9–16, 17–24, 25+) and do not measure necessary reasoning depth.

## Future-sequence controls

The 144 interior-order pairs use an exact legal completion and a reordered
sequence with the same first action, last action and action multiset. Both
sequences have an identical legal prefix before the first conflict. No no-op
padding or repeated-state walks are used. The 2–5, 6–10 and 11+ conflict-position
bins each contain 48 pairs.

A control that executes only the first two operations and otherwise predicts
“all legal” scores **158/288 (54.9%)**; the corresponding five-operation control
scores **192/288 (66.7%)**. Frozen v2 scored 73/98 (74.5%) and 92/98 (93.9%).
These are software shortcut audits, not language-model results.

## Source sampling

Eight development source groups are 10001, 10156, 10159, 10220, 31009, 31027,
31028 and 5867. The eight held-out source groups are 10014, 10036, 10128,
10213, 10242, 10265, 10269 and 31031.
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
Version 2.2 preserves all earlier records, adding 232 episodes and 1,213
diagnostics. Five of eleven frozen additional candidates were admitted;
the six rejected candidates remain in the census. Sixteen sources remain
below the proposed 30–50-source scale. Two- and four-site subassemblies
are retained transparently rather than described as complex new assemblies.

## Visual context and appearance controls

Ten answer-changing future-sequence pairs (twenty questions) hold registered
pieces, source poses, initial occupancy, goals, capacity, work orders and the
proposed plan constant. Only an induced subset of the original fixed support
context changes. Both contexts are independently requalified against collision
meshes and straight-motion paths. The first conflict occurs after a shared
legal prefix of at least two actions.

These retained contrasts cover **three source groups and four interventions**.
Their fixed-context part counts differ, so they are not count-matched visual
counterfactuals. Equal-count/type candidates from other sources were qualified
but did not yield an answer-changing retained sequence. Of 41 qualified
context pairs, 37 yielded none. The full census is reported.

Twenty-four additional appearance pairs (48 questions) compare original-color and
grayscale observations of the exact same state and plan. Answers must remain
unchanged. These are diagnostic controls, not independent source examples.

Static diagnostic inputs supply isometric, left, rear and right views at
revision zero. Active inputs start with isometric and charge later views.
The native certificate compares all five panels in each view: all ten
geometry pairs differ in at least one initial static view, while three
pairs are isometric-identical. This removes the known identical-input
confound in static mode, but does not establish perceptual answerability.

## Delayed repair

The 943 delayed-repair questions start after a certified legal but avoidably
costly action and a fixed lag of 1, 3 or 5 subsequent legal operations.
The executed history visits distinct states and remains outside the pre-error
optimal corridor. Repair means reaching a **nonterminal** state on any optimal
completion from the pre-error checkpoint. Reaching the goal alone does not
count. Exact checkpoint-specific minimum repair costs range from 1 to 7.

The evaluator separately tracks spontaneous errors, immediate return, and
delayed cohorts at lags 1/3/5. Earlier errors remain active when later errors
occur. Successful completion, conditional excess and optimal completion are
primary outcomes; immediate inverse-operation repair efficiency is secondary.

The public inverse-last control solves 547/943 questions (58.0%).
On 368 questions the inverse is suboptimal; on 28 it is unavailable.
These are separate reporting cohorts. The 26 all-correct-choice rows
remain calibration only and are excluded from discriminative accuracy.
Canonical identities cluster the 1,952 probe rows into 1,819 problems.
Primary accuracy averages assigned variants within problems, then problems
within sources, then sources, retaining zero credit for missing responses.

## Qualification and unresolved empirical claims

`audit_v21.py` replays every retained contrast, checks identical prefixes and
action multisets, verifies source-group separation, and checks delayed repair
against an independent forward BFS. `validate.py` covers exact oracle
trajectories, all diagnostic answers, assignment denominators, state tampering,
recovery, action budgets and observation isolation.

The geometry contract is conservative stud connectivity plus prescribed
straight translations over guarded inset meshes. It is not a force simulator,
free-pose assembly or unrestricted robotics benchmark. A depth-one heuristic
achieves 94.0% expected accuracy under uniform ties across 653 next-action
questions; these privileged relations are not visual performance.
Finite-horizon bounds do not establish internal reasoning depth.
Population VLM and human experiments remain pending.
