# BrickPlan 1.0 — Certified Assembly-Order Diagnostics

Status: implemented and validated, 2026-09-30. No model or human performance has been measured.

## Scope

Version 1.0 prioritizes correct cases and executable evaluation over a large gallery.
It isolates assembly-order reasoning with known placement geometry. Parts retain
their original LDraw geometry and source poses. The workcell supplies a finite set
of calibrated insertion sites and straight insertion/extraction paths. All sites,
including sites that are unnecessary for a particular goal, remain available.

This is a **kinematic, fixed-placement diagnostic track**, not unrestricted LEGO
manipulation, calibrated clutch-force simulation, or a robot benchmark. In
particular, the agent does not receive credit for estimating a placement pose.
This explicit control removes pose precision as a confound in planning evaluation.

The transition function does not consult the goal, reference order, future
feasibility, or shortest-path tables. A current legal but costly choice executes.
Changing only the goal must leave every local transition unchanged.

Two source subassemblies are qualified within this declared action domain:

| Case | Source | Intended diagnostic |
| --- | --- | --- |
| roadster-body | 31027, body subassembly | Side mudguards, overlapping body panels, nested removal |
| kart-deck | 31027 alternate kart, deck subassembly | Independent front/rear closures and alternative support |

| Certificate | roadster-body | kart-deck |
| --- | ---: | ---: |
| Original parts / fixed parts / mutable sites | 37 / 20 / 17 | 25 / 7 / 18 |
| Exhaustively reachable states | 14,012 | 44,604 |
| Directed legal transitions | 131,824 | 436,824 |
| Full optimal actions | 17 | 18 |
| Mandatory chain, parts / edges | 4 / 3 | 4 / 3 |
| Repair minimum detaches | 3 | 3 |
| Endpoint pairs / motion pairs | 666 / 612 | 300 / 432 |
| Blocked motion pairs / unknown geometry | 30 / 0 | 19 / 0 |

The release has 8 episodes (full, checkpoint, repair, healthy per structure),
2 choice probes, 16 lookahead probes, and 8 counterfactual responses (one switch
pair and one invariance pair per structure). The choice probes offer 6 and 10
currently legal candidates; counterfactual probes offer exactly 2.

These share a source kit and must stay in one provenance group for any future
train/test split. They are two structures, not independent evidence of broad
generalization. Random IDs and rollout probes do not increase this count.

## State and actions

The state records which calibrated sites are occupied, the identity of each
installed part, unused inventory, attempts, inspection count, and termination.
Fixed parts form an explicitly clamped, connected initial subassembly.
Every accepted state must remain connected to that subassembly through audited
connectors under the declared rigid-connection abstraction.

An `attach` or `detach` moves one part along its declared path. The operation
includes transfer from/to an external magazine; its insertion/extraction segment
is collision audited. The magazine and transfer outside the workcell do not claim
to model a human hand or general robot motion. No free teleportation through the
assembled structure is allowed.

One attach/detach attempt costs one action, including failure. `inspect` changes
only the view. `diagnose` records an agent's explicit claim without revealing its
truth. `finish` ends the run and scores once. Fresh resets create new runs.

Available sites are public task geometry, not a next-step mask. Observations do
not include collision blocker tables, viability, optimal actions, or repair
answers. Stable episode-local part IDs identify objects; source line/step indices
are not policy inputs. Equivalent part instances must not be distinguished by a
private source identity.

Full runs begin at the qualified initial subassembly. Repair runs begin at a
reachable, certified no-undo dead end. Counterfactual runs use the same state and
local dynamics with different visible future goals.

## Ground truth

For occupied-site state `s`, goal `g`, and permitted action domain:

- `C*(s,g)` is the minimum remaining number of successful attach/detach actions.
- `D*(s,g)` is the minimum number of detach actions in any completion.
- `V+(s,g)` is true iff completion is possible without detach.
- `VB(s,g,b)` is true iff `C*(s,g) <= b`.

The finite transition graph is exhaustively enumerated. Reverse shortest-path
search gives exact costs within this graph. Certificates record graph/task hashes,
reachable state counts, goal states, costs, and completion witnesses.

Geometry evidence and finite-graph evidence are separate. Collision checking uses
versioned inset meshes, an explicit clearance guard, and the stated path domain.
A numerical clearance certificate does not certify real clutch forces or all
continuous six-degree-of-freedom assembly paths.

`UNKNOWN` must remain distinct from infeasible. Incomplete geometry coverage or
incomplete graph search cannot produce an infeasibility certificate.

## Seven primary diagnostic dimensions

### 1. Dead-end choice rate

At preselected checkpoints, evaluate a legal action only when its predecessor
has a completion:

`DECR+ = count(V+(s)=1 and V+(T(s,a))=0) / eligible legal choices`.

Report separately:

`DECR_B = count(VB(s,b)=1 and VB(T(s,a),b-1)=0) / eligible legal choices`.

Also report checkpoint decision coverage, invalid-action rate, and unknown-label
coverage. Missing/invalid choices do not count as successful avoidance. Do not
repeatedly count ordinary actions while already inside a dead end as new entries.

`DECR+` concerns mandatory rework, not absolute impossibility. After a true
budget dead end, success is impossible under the original remaining budget;
additional-budget rescue is a separately labeled experiment.

### 2. Lookahead depth

Present a state and a proposed action continuation. Before execution, the agent
predicts the first failing action index, or `null` if the whole continuation is
executable. Ground truth comes from replaying that exact continuation.

Use distance bins such as 1, 2, 4, and 8, with executable controls of matched
length. Score exact first-conflict accuracy, conflict recall, false-alarm rate,
and optional blocker identification, separately for each distance.

The reported distance is **conflict-prediction horizon on supplied plans**.
It is not a direct measurement of the model's internal search depth. Report
causal dependency depth and intervening action types; adding irrelevant actions
must not be sold as deeper causal reasoning.

A supported-depth summary requires a preregistered accuracy/false-alarm threshold,
sufficient independent structures, and performance at all shorter tested
distances. With a tiny 1.0 bank, report the distance curve and sample counts; do
not infer a population-level maximum reasoning depth from one correct example.

These probes complement actual execution; they do not replace full episodes.

### 3. Plan survival curve

Let `tau+` be the first attempted structural-action index after which `V+` becomes
false, and `tauB` the corresponding first budget-feasibility loss.

Report first-loss curves separately. Recovery later does not erase the first
failure or restart the survival clock. A successfully completed run stays a
successful absorbing outcome.

At index `t`, report known survivors, first-loss failures, and early-stopped
unresolved runs. For `N` initially eligible runs:

- lower survival bound = known survivors / N;
- upper survival bound = (known survivors + unresolved censored runs) / N.

Do not treat early abandonment as indefinite survival or silently drop it.
Mixed task lengths are stratified; raw action index and reference-normalized
progress are not interchangeable.

### 4. Regret

For successful episodes:

- action regret = actual attempted actions − `C*(s0,g)`;
- detach regret = actual detach count − `D*(s0,g)`.

Failed episodes have `null` regret, an explicit failure outcome, and consumed
costs; they cannot win by doing nothing. If only a reference plan is known, report
reference-relative cost rather than optimal regret.

With one-part unit-cost actions, these quantities are related:
successful action regret = 2 × detach regret + failed attempts.
Report this dependence instead of presenting them as independent abilities.

### 5. Recovery rate

Use prevalidated reachable repair starts with `V+=0` and finite `C*`.
Report:

- detection recall: a correct explicit `needsRework` diagnosis before recovery;
- detection precision/false-alarm rate using matched healthy checkpoints;
- recovery completion rate within the fixed rescue budget;
- joint detection-and-completion rate.

Successful recovery without an explicit diagnosis is behavioral recovery, not
evidence that a diagnosis was explicitly made. A positive statement alone is not
successful recovery. Detection timing distinguishes anticipation from reacting
after the first failed insertion.

Only the **first** diagnosis before the first successful structural action is
scored against the injected checkpoint. Failed attempts may precede it; this is
reported separately. Later diagnoses cannot replace a wrong first answer.
Repair and healthy starts have equal installed counts and equal action budgets
within each structure; their public task labels are both `continuation`.

### 6. Replanning efficiency

From the same repair start, report successful repair suffix:

- attempted actions and action regret against `C*`;
- detach operations, distinct removed parts, and detach regret against `D*`;
- failed attempts and time to first appropriate repair action.

Report completion rate beside conditional efficiency. Compare controllers from
the same injected state; self-induced repair states have different severity.
Repeatedly removing the same part counts repeatedly as work and once as a
distinct removed part.

### 7. Counterfactual consistency

Use paired goals with the same current state, inventory, calibrated sites,
candidate current actions, and transition graph. Both candidate closure parts
must be required in both goals. Change a future interior requirement so that
the optimal current closure changes.

Certify the eligible current action sets using exact conditional costs:

`Q*(s,a,g) = 1 + C*(T(s,a),g)`.

The minimum is taken over the two **offered candidates**, not all possible
current actions. Installing an interior part first may be globally better.
Only pairs with different certified minimizing choices are switch-required
pairs. Score joint correctness on both members, then choice-change rate.
Changing the answer in both members incorrectly is not consistency.

Also include a goal-change control where the certified optimum stays the
same. Report correct invariance and position/ID bias. Goal size, local legality,
and candidate final poses are matched within each pair. An invariance goal change
may change completion cost; it is irrelevant to which offered action is best.
Public candidates are permuted independently. Scoring compares physical choices
after normalization, not their displayed list positions.

## Budgets and reporting

Default full/repair action budget: `C*(start,goal) + max(4, ceil(C*/2))`.
Checkpoint runs use the same rule; matched healthy controls inherit the repair
budget rather than exposing their smaller optimal cost through the budget.
Budget-feasibility probes explicitly specify tighter budgets and certify their
predecessors as feasible. Observation budgets are separate. Exhausting inspection
does not terminate an otherwise operable run.

The headline remains complete success rate at the frozen budget. Seven
diagnostic dimensions are a profile, not a weighted aggregate leaderboard score.
Always include denominators, missing responses, invalid responses, censored
runs, geometry/solver coverage, and exact model/version/compute budgets.

Reference, greedy, deliberately myopic, and scripted recovery policies are
software validation controls. They are not measured VLM or human results.

## Interpretation limits

Both full tasks are in the proposed D1 range. The mandatory dependency chain is
four parts (three edges), rather than 17 or 18 causal levels. The lookahead bank
has first-conflict distances 1, 2, 4, and 8, with causal depth **one**: later bins
include intervening legal attachments. Executable controls share each conflicting
prefix and differ at the last action; executable does not imply globally viable.
No maximum internal reasoning depth or D2–D4 coverage is claimed.

The browser renders raw LDraw triangles and unchanged source poses. Its exploded
reference is an inspection aid, never a physical state. The workcell support
plate depicts the abstract fixed-base fixture; tool geometry and clutch forces
are not certified. Collision certificates use closed proxy meshes inset by
0.25 LDU and a 0.002 LDU guard. A documented 3022 proxy repair fills one missing
triangular stud-cap face without moving vertices; original source/render
triangles are unchanged. See `geometry.py`, provenance, and the appendix.

The HTTP SDK is the structured track. The browser adds unrestricted camera
inspection for practice/review; screenshots are not a matched vision-only
observation protocol. A human study or VLM vision-only comparison still requires
frozen cameras, observation budgets, and an isolated evaluation service.

## Release acceptance

- [x] Qualified original geometry and preserved poses/hashes.
- [x] Complete path-pair coverage for included movable parts.
- [x] Connected, explicitly clamped initial state and connected accepted states.
- [x] Exhaustive reachable graph and checked exact-cost certificates.
- [x] Legal dead-end choices, successful optimal recovery, and nontrivial paired goals.
- [x] Seven executable metrics with adversarial/missing/failure controls.
- [x] Shared human/API execution and step-by-step review.
- [x] Reproducible validation report and honest limitations.
