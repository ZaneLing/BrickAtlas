# BrickPlan 2.0: mechanism overhaul and evidence ledger

The underlying issue was that the predecessor's planning cost collapsed
to a static relation formula. This release changes the mission semantics
and tests the change against competent structural controls.
Earlier frozen releases remain intact.

| Review concern | Implemented correction | Evidence and remaining limit |
|---|---|---|
| Long plans mistaken for deep planning | Exhaustive static audit of every preceding stored label | 1,802,728/1,802,728 equal the closure formula; `audit_predecessor.py` is read-only |
| Unlimited inventory removes scheduling | Finite rack; every detached registered piece occupies one holder | Exact bound gaps up to 18 operations; capacity-aware dispatch completes 170/207 |
| Occupancy is the complete state | Persistent visible off-assembly inspection ledger | Five matched history pairs have identical occupancy and disjoint optimal next actions; no hidden-memory claim |
| Final shape determines all work | Explicit future inspection obligations | Five changed-work pairs share assembly and physical goal but switch optimal actions |
| Weak baseline creates apparent difficulty | Closure lower bound, resource dispatch, full and bounded A*, Hamming ablation | Full closure A* solves 207/207 with at most 2,555 expansions; general search hardness is not claimed |
| First/last-action shortcut | 49 legal/corrupted continuation pairs with identical endpoints and action multisets | Interior order determines validity; other possible shortcuts remain open |
| Supplied-plan length called lookahead | Actual finite-horizon action values with tie bounds | Depth 1 includes a correct action at all 98 checkpoints; this release does not establish a required internal reasoning depth |
| Missing errors during mandatory rework | Conditional Bellman excess for every attempted operation | Semantic regression includes an error when rework was already mandatory |
| Misleading dead-end terminology | Separate avoidable cost, budget viability and true unreachability | Retained components have no genuine irreversible dead ends; the corresponding rate is undefined |
| Recovery only after initially clean states | A new event per legal positive-excess action; pre-error optimal corridor | Overlapping errors, first diagnosis, restoration lag and censored outcomes retained |
| Invalid regret decomposition with jobs | Derive the conservation identity including required audits | `C*=2D*+occupancy_balance+unfinished_audits`; successful regret reconciles exactly |
| Too few source families | Add truck, cottage and sports car through unchanged qualification | Five source kits; sports car is explicitly easy and only 10/22 registered sites move |
| Floating or shifted geometry | Preserve source matrices, stud support and qualified paths | No executable pose shifts; rack and inspection are explicit workcell abstractions, not dynamics |
| Visual track absent or privileged | Five raster panels; separate structured observation | Image track omits matrices/occupancy flags/relations/costs; public registration and rack inventory simplify perception |
| UI differs from agent input | Shared observation API, persistent acquired rasters and budgets | Human UI and agent interface use the same camera options and operation contract |
| Free 3D leaks geometry during studies | Free orbit/explosion only after ended practice episodes | Study static/API allowlists block review modules, scene data and score endpoints |
| Adapter budgets merely descriptive | Pre-call reservations, complete usage verification and fail-closed handling | Trusted adapter/provider accounting is required; unavailable mode is explicit |
| Missing/repeated/cross-condition trials bias scores | Fixed assignment/identity, one study start, frozen answers, complete census | Collector independently replays episode and probe requests, including view history |
| Fragile recovery after server restart | Revisioned idempotence and atomic persistence with rollback | Protocol tests cover retries, stale IDs, restart and simulated persistence failure |
| Manuscript/code/UI drift | Generated tables, source-raster figures, complete episode census and release digests | English 12-page paper including appendix; recorded controls only |

## What is now established

The prior analytic cost formula is no longer exact. Resource scheduling
and persistent work obligations alter optimal costs and actions on unchanged
source geometry. Simple adapted policies lose optimality and sometimes fail
within generous size-based budgets. Exact oracles permit evaluation of legal
but costly choices and subsequent recovery.

## What is still not established

- Full structural A* remains fast. Tiers are conditioned on mechanisms and
  one declared algorithm, rather than universally ordered difficulty levels.
- Many greedy runs still complete; optimality exposes more errors than
  success alone. Depth-one optimistic ties already contain the right action.
- No VLM or human baseline has been collected. No human–model gap or
  visual-model planning deficit is measured.
- The held-out-source labels describe a public challenge partition used
  during design. Independent source replication is still needed.
- This is known-site geometry with rigid stud support and a resource rack.
  Free poses, forces, physical rack transfers and hardware assembly are
  outside its certification.
- The manuscript is an executable research release, not a claim that the
  current evidence is sufficient for CVPR acceptance.

The next empirical step is a small format/cost pilot using the external
adapter, followed by preregistered matched image/structured model and human
conditions. No paid provider calls were made for this release.
