# BrickPlan 1.2 technical appendix

## Reproducible bank

Source geometry, original poses, proxy qualification and fixed insertion paths
are byte-identical dependencies on frozen 1.1. The three geometry/source links
resolve within the repository. Original display triangles and attribution are
also inherited. `revise.py` constructs the new tasks deterministically.

| Case | Source group | Mutable/fixed | Reachable states | New reconfiguration start→goal | Optimal actions | Minimum detaches |
|---|---|---|---:|---|---:|---:|
| roadster-body | LEGO-31027 | 17/20 | 14,012 | Private certified masks in task bank | 30 | 14 |
| kart-deck | LEGO-31027 | 18/7 | 44,604 | Private certified masks in task bank | 24 | 8 |
| airframe | LEGO-31028 | 21/3 | 284,088 | Private certified masks in task bank | 34 | 15 |

Five episodes per case retain the full/checkpoint/repair/healthy controls and
add a partial-target reconfiguration. Reconfiguration Hamming lower bounds are
4, 12 and 8. Each selected reconfiguration has a legal goal-directed trap with
conditional cost two actions above the optimum. These are access-order tasks;
the bank has no established support-rerouting or temporary-scaffold mechanism.

`discover.py` exhaustively found distance-from-empty equal to occupied-site
count throughout all three reachable components. `reconfigure.py` searched all
inherited goal tables and 30 seeded additional partial targets per structure
without finding the specified install-before-required-removal penalty.
This is a bounded negative mechanism search, not an impossibility theorem.

## Balanced continuation generation

Random seed is 1200 plus case index. Sample reachable states and legal walks at
lengths 4, 6, 8; require both action types. Swap two interior actions while
preserving the action multiset. Keep only first conflicts caused by
`MOTION_BLOCKED` or `UNSUPPORTED_ASSEMBLY`, covering every interior position.
The unswapped walk is its executable control. There are 12 pairs per case.

The complete public proposal uses stable nominal P-instance references even
after the hypothetical first failure. Proposal generation does not execute
the plan to expose correctness through missing or changed instance IDs.
Same-pair observations and first/last public actions are checked for equality.

Any decision rule seeing only initial observation, first and last actions,
plan length and action multiset cannot distinguish pair members. Therefore its
pairwise exact first-conflict accuracy is at most 1/2. The implemented endpoint
rule scores 36/72. This says nothing about stronger rules using interior order.
Exact replay of a supplied plan is straightforward when private relations are
known. No internal reasoning-depth label is provided.

## Online definitions

For goal `g` and remaining budget `b`:

- Attach-only feasibility: `s ⊆ g` and `C*(s,g) = |g|-|s|`.
- No-rework feasibility: `C*(s,g) = popcount(s XOR g)`.
- Budget feasibility: `C*(s,g) <= b`.
- Eligible decision: successful legal action from a feasible state that has
  both safe and unsafe legal alternatives for that predicate.
- Loss numerator: eligible chosen action causes the predicate to become false.
- Bellman excess: `1 + C*(after,g) - C*(before,g)`.

All structural attempts appear in per-episode online decision records.
Invalid attempts are excluded from legal-choice denominators but may cause
budget loss. An online rate has null value when its denominator is zero.
One-step static choice probes remain separately reported.

A self-induced event starts only at legal no-rework loss. While that event is
active, the first diagnosis is frozen and the first return to no-rework
feasibility closes it. Costs count subsequent structural attempts and
successful detachments through restoration, excluding the trigger itself.
Recurrence creates a separate event. First false diagnoses cannot be replaced
with later true diagnoses. An unfinished active event is censored; a terminal
active event is unrestored. Restoration and detection are separate outcomes.

Injected repair/healthy diagnosis retains its original first-answer-before-
successful-action protocol. It is not pooled with self-induced events.
Event prefix excess is measured at its restoration endpoint. Costs at
unfinished endpoints are retained without pretending they are successful
completion regret. Successful episode regret obeys
`actionRegret = 2 * detachRegret + failedAttempts`.

`lookahead.distanceCurve` groups matched controls with their corresponding
actual conflict position; `planLengthCurve` groups by total proposal length.
Both retain exact accuracy, coverage, conflict recall and control false alarms.

Survival is stratified by case, mode, optimal length and budget. All missing
episodes are censored at time zero. Successful termination is absorbing;
historical first loss is never erased by later recovery. A one-run curve is a
descriptive trace; repeated participant/model runs are required for uncertainty.

## Renderer and visual boundary

`visual.py` reads original recursive LDraw triangles from the frozen display
asset, transforms them with unchanged source matrices and applies deterministic
two-sided lighting. `raster.c` uses orthographic barycentric triangle depth
testing, without a browser-side mesh or scene graph.

Panels contain visible-instance callouts and a pixel catalog. The image-ID
payload gives all P/S IDs but no inventory membership, site occupancy, target
flags, type labels, coordinates, motion vectors, graph edges, depth or masks
as machine-readable fields. Inventory membership and target occupancy must
be inferred from rendered images. Structured controls receive these public
structured fields explicitly alongside the same raster images.

An all-site reference includes sites absent from the target. Exploded-reference
is a diagram of those sites; it does not alter physical scenes or qualification.
Paper figures use 1520×1160 original-geometry raster frames. Their provenance
contains source/geometry hashes, exact task, seed, action index and PNG hashes.

## Software baselines and interpretation

| Control | Information allowed | Action selection |
|---|---|---|
| Exact oracle | Private complete costs and transition graph | Descending exact cost |
| Static relations | Private support/blocker relations and local validity | Blocker closure, removals, greedy target install |
| Search 1/2/4 | Private transition model | Bounded BFS, Hamming leaves, visited-state tie breaks |
| Public greedy | Structured observations only | Goal mismatch, compatible parts, rejection memory |
| Legal random | Private legal-action set | Uniform legal move |
| Blind random | Public ID lists only | Random attach/detach, ignores pixels |

The static relation policy solves all 15 cases without state search. Search
depths 1, 2 and 4 each solve 9/15. Public greedy solves 2, 2, 3 cases across
three seeds; both random controls solve 0. The oracle scores all assigned
probes correctly and incurs zero episode regret. These results do not compare
VLMs, humans, or equal-information policies. Deterministic repeated search
runs do not count as independent evidence.

## External validity

Known poses, fixed paths, rigid stud holds, proxy inset, source-family reuse
and absent physical trials remain material limitations. The renderer is a
visual observation mechanism, not a new physics engine. The release makes no
claims about clutch forces, gravity, rotations, alternative insertion paths,
hands, D2–D4 difficulty or human-level planning.
