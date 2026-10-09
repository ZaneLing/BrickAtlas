# BrickPlan 1.0 — Technical Appendix

This appendix describes the executed 2026-09-30 release. It is not the unrestricted
manipulation roadmap. The normative metric contract is [PROTOCOL.md](PROTOCOL.md).

## A. Artifact map and versions

| Artifact | Role |
| --- | --- |
| `cases.py` | Original model selections and mutable source instances |
| `geometry.py` | Source transforms, connector extraction, endpoint and path qualification |
| `engine.py` | Goal-independent transitions and exact finite-graph solvers |
| `build.py` | Deterministic episode/probe construction and certificate checks |
| `session.py` | Instance identity, quotas, requests, and authoritative event replay |
| `probes.py` | Opaque probe IDs and shuffled candidate positions |
| `evaluate.py` | All seven dimensions, denominators, and survival bounds |
| `server.py`, `client.py`, `collect.py` | HTTP workcell, policy adapter, run collection |
| `render_assets.py`, `arena/` | Original source meshes and human/review interface |
| `validate.py`, `validate_http.py`, `validate_arena.mjs` | Semantic, transport, and browser verification |

Validation environment: Python 3.11.16; NumPy 2.4.6; meshlib 3.1.4.297;
BrickNet 0.1.0; Three.js 0.180.0; Playwright 1.55.1. Python's standard library is
sufficient to run the server, rebuild from frozen geometry, and evaluate.
Requalifying geometry additionally requires the locked model manifests, LDraw
parts, BrickNet alias/connector catalog, and inset meshes already in this repository.

## B. Source geometry and coordinate contract

`data/*/source.json` records model provenance, author/license, selected source
indices, source/manifest hashes, and detected connector edges. These source indices
are private audit information, never policy inputs. Both subassemblies are selected
from the LEGO 31027 source family; no source placement is edited.

The source manifest stores a column-major viewer transform in scaled coordinates.
The audit recovers LDraw coordinates by:

`rawMatrix = diag(2.5, -2.5, -2.5, 1) @ reshape(originalMatrix, 4, 4).T`.

The canonical collision transform is `rawMatrix @ aliasTransform`. Rotations
must have orthogonality error and determinant error at most `1e-5`.
Public `matrix` fields are nested, row-major 4×4 **raw LDraw** transforms in LDU.
The browser applies a 180-degree X rotation for its Y-up display. Original part
numbers are used for display; canonical aliases plus color define exchangeable
inventory classes. Public path directions are in raw LDraw world coordinates.

The default extraction direction is the negative canonical local Y axis.
Two underside sites use the explicitly reversed direction specified in
`cases.py`; their source poses are unchanged. Attach follows the reverse of the
extraction path. Path lengths exceed the model extent and include a margin of
64 LDU; every outside endpoint must be separated from each obstacle.

## C. Geometry certificates

All unordered final-pose pairs must be CLEAR. For a movable part, every other
included part is covered by a path-pair record. Permanent blockage against a
fixed part excludes the site. The release has 966 endpoint pairs and 1,044
motion pairs; 49 motion pairs are BLOCKED, none UNKNOWN.

Collision proxies have a declared 0.25 LDU inset per surface. Reflected mesh
orientation is corrected for containment checks. The 3022 proxy repair fills
one triangular hole in the stud cap at `y=-3.75`; its three vertices must lie
within radius 5.8 about `(-10,10)` in the XZ plane. Otherwise qualification
fails. Source evidence is `parts/3022.dat → p/stud.dat → p/4-4disc.dat`, with
hashes included in `proxyRepairs`. No vertex or original render triangle moves.

Endpoint qualification uses separating bounds, triangle intersection,
containment, and guarded mesh distance. Path qualification uses:

1. A separating swept AABB, if available.
2. A triangle-intersection witness at an interior sample, certifying BLOCKED.
3. Otherwise interval subdivision with midpoint surface distance `d`.
   An interval `[l,h]` is CLEAR when `d > (h-l)/2 + 0.002`.

The distance-cover condition follows from 1-Lipschitz surface separation under
unit-direction translation. The accepted intervals must cover the full path
without gaps. Intervals below `0.0005` LDU without a clearance certificate,
or searches beyond 8,192 nodes, produce UNKNOWN. All proxy meshes must be
closed. These conditions qualify the declared proxy/path model; they do not
certify real-world hand access, clutch force, tolerances, or all 6-DoF paths.

The runtime never runs a future-goal search to decide if an action is legal.
Pairwise motion blockers are compiled into occupancy bit masks. This compilation
is valid because only one part moves and every obstacle stays at its fixed
calibrated pose for the duration of the action.

## D. Graph and cost certificates

For `n` mutable sites, states are occupancy bitsets in `[0,2^n)`. A valid state
must be connected to the fixed base via the audited stud graph. Fixed parts
themselves must form one connected component.

An attach is legal when its site is empty, its path has no occupied blocker, and
the resulting state is supported. A detach is legal when the site is occupied,
its extraction path is clear, and the remaining state stays supported.
All terminal-pose pairs were already audited. These rules are goal independent.

Each legal transition has a verified inverse. Breadth-first search from the
empty mutable state enumerates the component; search from each target gives
exact unit-action costs. Verification checks:

- The goal has cost zero and is the unique zero-cost reachable state.
- Every reachable state has a finite cost.
- Every legal edge satisfies `|C(s)-C(s')| <= 1`.
- Every non-goal state has a successor of cost `C(s)-1`.
- The goal table covers exactly the initial reachable component.
- Reversing each edge restores the predecessor.

The inequalities lower-bound every path, and descending witnesses attain the
bound. Together they certify optimality within the finite domain. Five goal
tables are frozen for roadster and seven for kart.

For a successful path, let `A` and `D` be successful attachments and detachments.
Then `A-D=|g|-|s|` and `A+D=C`. Minimizing `C` therefore also minimizes `D`;
`D*=(C*-(|g|-|s|))/2`. This equivalence relies on single-part unit actions.
It would need revision for subassembly moves, unequal costs, or force penalties.

Mandatory precedence is computed over **all no-detach completions** of the full
task. Both longest chains have four parts, hence three edges. This does not
equate full action count with causal dependency depth.

## E. Frozen task ledger

`C` below means optimal remaining actions; `D` means minimum remaining detach
operations. Installed counts exclude the fixed base.

| Structure | Mode | Installed | C | D | Action budget |
| --- | --- | ---: | ---: | ---: | ---: |
| roadster-body | full | 0 | 17 | 0 | 26 |
| roadster-body | checkpoint | 3 | 14 | 0 | 21 |
| roadster-body | repair | 11 | 12 | 3 | 18 |
| roadster-body | healthy | 11 | 6 | 0 | 18 |
| kart-deck | full | 0 | 18 | 0 | 27 |
| kart-deck | checkpoint | 3 | 15 | 0 | 23 |
| kart-deck | repair | 17 | 7 | 3 | 11 |
| kart-deck | healthy | 17 | 1 | 0 | 11 |

Every episode includes an initial-state reachability witness and an optimal
completion witness. Full and checkpoint budgets use `C + max(4, ceil(C/2))`.
Repair and healthy budget matching is deliberate.

Choice probes start after three attachments and use budgets 14 and 15. Their
6/10 candidates are locally legal and include both future-safe and rework
branches. Lookahead probes have matched executable/conflicting continuations
of lengths 1, 2, 4, 8. For lengths above one, the blocking closure is installed
before intervening legal actions; causal depth remains one. At distance one
the obstruction is already present. Control executability is not a label of
global viability.

Counterfactual conditional costs for the two canonical candidates:

| Structure | Switch goal A | Switch goal B | Invariance A | Invariance B |
| --- | --- | --- | --- | --- |
| roadster-body | 16 / 18 | 18 / 16 | 15 / 17 | 15 / 17 |
| kart-deck | 3 / 5 | 5 / 3 | 8 / 10 | 10 / 12 |

Both closure parts are required in both switch goals. Goal sizes match within
each pair; inventory and available sites do not change. The invariance goal
change is irrelevant to the **best offered choice**, not necessarily total cost.
An offered closure need not be globally optimal among all possible actions.

## F. Public observation and response contract

`brickplan-observation/1.0` includes revision, view, quotas, termination, fixture,
sites, inventory, fixed parts, and action schemas. Each site provides stable ID,
required part type/number/color, raw transform, path direction/length, required
goal flag, and installed instance ID. Inventory provides instance ID and type.
Fixed parts have stable `F...` IDs. Mutable instance IDs (`P...`) and site IDs
(`S...`) are independently randomized. An equivalent part may fill any matching
site regardless of its private source instance.

It excludes reference order, original instruction indices, connector/blocker
tables, costs, viability, correct diagnosis, and optimal actions. Goal matrices
are public because this track intentionally controls placement estimation.
The free-camera frontend additionally renders this public geometry.

Each action request has exactly `requestId`, integer `revision`, and `action`.
Malformed envelopes and revision conflicts are rejected without charge.
Once a valid envelope is accepted, an invalid action costs one structural
attempt. Structural error codes include unknown part/site, occupied site,
incompatible part, part not in inventory/installed, blocked motion, and unsupported
assembly. Inspection/diagnosis quota rejections do not consume structural budget.
The SDK caps total calls and finishes policies that fail to terminate.

Successful actions, rejections, inspection, diagnosis, and finish advance the
revision. Identical retries do not. The export stores authoritative before/after
states and results; the scorer replays every request and requires exact event
agreement. Duplicated/tampered events are rejected.

The server stores opaque task/probe presentation separately from private
conditions. Counterfactual member scene seeds match; candidate positions are
independently shuffled. Responses are frozen once, then privately normalized
by the collector. Missing answers and malformed answers remain distinct.

## G. Metric edge cases

- **Dead ends:** Count a new no-undo loss only from a no-undo-feasible predecessor.
  Budget loss uses the decremented remaining budget. These are different labels.
- **Lookahead:** Exact first index has an all-assigned denominator. Conflict
  recall accepts any non-null prediction on a conflicting probe; exact accuracy
  separately penalizes a wrong index. False alarms use valid control responses,
  accompanied by control coverage.
- **Survival:** The clock counts structural attempts, including rejected
  attempts. Store the first loss permanently. Repair starts are excluded from
  no-undo survival because they already fail that predicate. Missing and
  abandoned runs become unresolved beyond observed progress.
- **Regret:** Only a terminated run at the exact goal is successful. Failed or
  unfinished runs have null regret. For success, action regret equals twice
  detach regret plus failed attempts.
- **Detection:** Freeze the first diagnosis before the first successful
  structural action. A prior failed attempt is recorded separately. Answering
  both true and false, or diagnosing after a repair, cannot gain late credit.
- **Efficiency:** Count actual successful detaches and distinct instance IDs.
  The first appropriate repair attempt is the first successful detach that
  lowers the exact remaining minimum detach count.
- **Counterfactuals:** Score physical choices after depermutation. Joint correct
  switching requires both answers correct. Report correct invariance separately.
  Presented-position counts are stored in collection metadata; canonical counts
  are not mislabeled as presentation bias.

## H. Reproducibility and study boundary

The release scripts produce three labelled software controls and validation
reports. They intentionally access private oracles; they are unsuitable as
model benchmark results. The browser validation's full run includes one
incompatible-part failure, producing action regret one. Its kart repair has
three detaches and four attachments, producing action and detach regret zero.

`render_paper.mjs` exports original-mesh frames from this authoritative repair
session. `figures/provenance.json` identifies seed, revisions, and session.
The selected empty-site wireframe is a visual locator, not a physical part.

The current bank is too small for broad confidence intervals or a maximum
reasoning-depth estimate. Larger studies need independent source/topology
groups, real variation in causal depth, preregistered repeat selection, and
matched observation interfaces. Fixed camera screenshots, empirical human
trials, paid model runs, free manipulation, gravity, and physical construction
are not part of the validated 1.0 claim.
