# BrickPlan 2.2 protocol

## Workcell

The physical state is the occupancy of registered original source sites.
Each movable `P` piece fits exactly one `S` site. Original source meshes,
transforms, stud support, and qualified straight paths are retained. Fixed `F`
pieces form one connected clamped assembly. This is a known-site assembly
abstraction, not free-pose manipulation, force simulation, or measured hardware.

A detached registered piece occupies one universal oversized rack holder.
Rack occupancy may never exceed the declared capacity. An `audit` operation
completes one pending inspection only while that piece is detached. The visible
completion ledger persists after reattachment. Neither legality nor public
observations consult optimal cost tables.

All attach, detach, audit and rejected operation attempts cost one operation.
Valid camera acquisition, diagnosis and finish cost zero operations and advance
the request revision. There are 12 additional camera acquisitions and 12
diagnoses per episode. The default isometric view is free. Successful completion
requires explicit `finish` at the target occupancy with every work order done.
Using the final operation without finishing ends the episode by budget.

## Tracks and observations

`image-id` exposes PNG pixels for current assembly, target assembly, all-site
reference, registered piece catalog and rack. Public fields include P/S
registration, rack capacity and occupancy, work orders, budgets, request
revision and inspection history. It does not expose matrices, installed site
bits, blocker/support graphs, legal action lists, depth buffers, oracle costs,
tiers, or pair membership.

`structured` adds source matrices, part numbers, colors, path directions and
lengths, and current/target occupancy per site. The served human interface also
displays the same raster observations. It does not expose the private relation
graph. Software search controls have privileged relations and are reported
separately from this public track.

For frozen-checkpoint probes, `image-id` and `structured` supply isometric,
left, rear and right views at revision zero and disallow later `inspect`.
`image-id-active` supplies isometric initially and allows up to 12 billed
view acquisitions. These are distinct diagnostic conditions. Interactive
episodes retain the shared active-view protocol for all three tracks.
Initial supplied views do not count as acquired views; revisiting any
stored view is free.
Acquired public frame IDs contain only the revision and camera name
(`view-<revision>-<view>`). They must never hash private occupancy or the
ledger; small state spaces make such hashes enumerable. Private replay
certificates remain evaluator-side. Image URLs hash the supplied image
bytes, not hidden state.

Views: `isometric`, `front`, `rear`, `left`, `right`, `top`, `bottom`,
`exploded-reference`. An exploded view changes only the reference image; current
and target assemblies retain source poses. Every acquired view persists as a
snapshot of that revision, including all five rasters. Revisiting stored pixels
costs no view. Historical images never become executable state.

IDs are randomized consistently using the run seed. Matched pair members keep
the same registration. Episode/probe presentation order and candidate order are
permuted. Study catalogs reveal opaque IDs, available sessions, probe kind and
answer status. Assignment subsets do not change public IDs. Practice catalogs
add taxonomy, stable IDs, source/split and operation-length filters, plus full
previews without starting a session. Main images are 1920×1440; catalog tiles
are 480×360. HTTP images use content-addressed `/media/<sha256>.png` references.

## HTTP

The default server binds to loopback. It supports one participant, condition and
seed per store. For remote studies, deploy a separate authenticated instance per
participant behind an appropriate gateway; the development server is not a
multi-tenant authentication service.

| Method / path | Behavior |
|---|---|
| `GET /api/tasks` | Run identity, seed, bank/assignment hashes, assigned episode IDs and resumed sessions |
| `POST /api/sessions` | `{taskId, requestId}`; server fixes seed and condition |
| `GET /api/sessions/{id}` | Current observation |
| `POST /api/sessions/{id}/actions` | `{requestId, revision, action}` |
| `GET /api/sessions/{id}/history` | Public action/result journal |
| `GET /api/sessions/{id}/export` | Public journal, without private state |
| `GET /api/probes` | Assigned diagnostic IDs, kinds and frozen-answer status |
| `GET /api/probes/{id}` | Checkpoint observation, question, candidate actions or complete proposed plan |
| `POST /api/probes/{id}/actions` | Revisioned `inspect` or `answer`; returns immutable acknowledgment |

Episode actions:

```json
{"type":"attach","partId":"P001","siteId":"S005"}
{"type":"detach","partId":"P001"}
{"type":"audit","partId":"P001"}
{"type":"inspect","view":"top"}
{"type":"diagnose","avoidableError":true}
{"type":"finish"}
```

The diagnosis question asks whether a **legal operation has added avoidable
future cost since the last diagnosis or episode start**. Mandatory rework that
was already required does not itself constitute an error.

Probe answers are `{"type":"answer","answer":{"choice":0}}` for a zero-based
candidate index, or `{"type":"answer","answer":{"firstConflict":3}}` for the
one-based first illegal operation. `firstConflict:null` means every supplied
operation executes. Active probes allow 12 camera acquisitions; static
probes allow none. All probes forbid physical actions.
Candidates may be tied for optimal cost; any optimal candidate is correct.

Requests are idempotent under an unchanged `requestId` and payload, including
after restart. A changed payload under a used ID or a stale revision is rejected.
Probe acknowledgments are immutable; fetch the current probe after an
acknowledgment. Episode retries return the original revision's observation.
Study assignments may start once, and answers freeze on their first accepted
submission. The UI resumes an existing study session. Practice permits repeats.

Authoritative exports persist atomically after each mutation. If persistence
fails, in-memory state is rolled back. The original run configuration must
match on restart. These files are experiment records, not cryptographically
tamper-proof storage; operate and preserve them on the evaluator host.

## Collection and separation

`server.py collect` runs locally on the evaluator host and emits a private
submission plus a report. No HTTP collection endpoint exists. Scoring replays
every episode and probe request, validates the registered run/seed and
certificates, and rejects altered outcomes, candidate normalization and
view transcripts. Unstarted, unanswered and unfinished assignments remain in
the census and relevant denominators.

Only ended practice episodes expose `/score`, `/replay`, `/frame/{revision}`
and `/review3d`. Unscored practice also exposes `/api/scene/preview/{id}`,
`/api/sessions/{id}/scene`, and `/api/model-runs/{id}/scene` for live original
triangles and transforms, orbit, zoom, piece selection and annotated explosion.
Previews never create attempts; scenes contain no oracle costs or action labels.
Model inputs still use public raster observations. Study mode blocks all scene,
preview, model-demo and score endpoints; the common React shell uses controlled
images only. Static routes are an explicit allowlist, never
a filesystem directory. Private tasks, sources, meshes and oracle files are
not individually exposed by static URLs. Practice additionally offers a
complete evaluator archive, paper, public JSONL and data card. Those downloads,
rich catalogs and previews are blocked in study mode.

Practice collection retains the latest attempt per task and is for debugging,
not a preregistered participant result. Scored studies require separate stores.

## External policy adapter

`study.py template` writes a manifest with empty model/participant fields.
Fill them before use. This population runner uses an external adapter.
The separate practice model manager bundles local MLX and OpenAI-compatible
vision calls; see `MODEL-INTEGRATION.md`. `policyCommand` is an
argv list receiving one JSON object on stdin and returning one JSON object on
stdout. Stderr is logged. The working directory must be outside this repository.
This directory rule is **not a sandbox**: use a separate policy host without
evaluator files for a defensible information boundary.

Each request contains run/assignment identity, complete prompt, public input,
public action history and declared settings. The adapter must convert every PNG
to the provider's native image-message input, preserving current and historic
views. It must not silently replace image data with text descriptions.

The adapter returns:

```json
{
  "action": {"type":"finish"},
  "limitsEnforced": true,
  "usage": {
    "inputTokens": 1234,
    "outputTokens": 56,
    "costUSD": 0.012,
    "providerRequestId": "provider-issued-request-id"
  }
}
```

For `budgetMode:"reported-usage"`:

1. Before each invocation, the runner reserves `maxInputTokens +
   maxOutputTokens` and `maxRequestCostUSD` from the remaining aggregate limits.
   Insufficient remaining budget prevents the invocation.
2. The adapter must count the **complete provider input including images**,
   enforce input/context/output limits, and reject overlarge inputs before a
   provider call. It must bound the request cost from provider pricing and
   output limits. `limitsEnforced:true` is its explicit attestation.
3. Returned usage must be complete, finite and within the reserved limits.
   Accepted actual usage replaces the reservation. Missing usage, timeout,
   malformed output, provider error or a limit violation stops the runner.
4. Currency and tokens rely on a trusted adapter/provider report. The runner
   cannot independently verify billing or prevent a dishonest external process
   from spending beyond its declared limits. These are not hard provider quotas.

For `budgetMode:"unavailable"`, `totalTokensLimit`, `maxRequestCostUSD` and
`providerCostLimitUSD` must be null. Only request counts and local process
timeouts are enforced by the runner. Report token/currency accounting as
unavailable, never as enforced or zero.

Every invocation has a durable pre-call record and post-call record, full input
and raw output, input/output/prompt/configuration hashes, run/task/probe/session/
request IDs, model settings, provider request ID, usage, latency and errors.
The runner has no automatic provider retry. A log with an unresolved or rejected
call blocks restart; reconcile unknown provider usage separately. Reusing a
different prompt, configuration or assignment certificate with the same log is
rejected. Never erase failed calls to report a complete run.

## Reporting unit

There are sixteen source kit groups. Roadster and kart share kit 31027 and must
be grouped together. Development groups are 10001, 10156, 10159, 10220, 31009,
31027, 31028 and 5867. Held-out source groups are 10014, 10036, 10128,
10213, 10242, 10265, 10269 and 31031
(stored split label `heldout-source`). Legacy tasks used solver evidence.
New-source tasks use seeded sampling and geometry/solvability admission;
geometry pruning was refined after initial qualification failures, before
new-source solver results. This is a public partition. ID seeds,
pair members and repeated runs are correlated observations, not new independent
structures. Report participants, conditions, assignments, coverage and source
group summaries separately. Do not pool structurally privileged software
controls with image policies or use them as fabricated VLM/human measurements.

The 1,952 probe rows map to 1,819 canonical problems. Twenty-six all-correct
choice rows are calibration only; discriminative accuracy excludes them.
For primary source-macro accuracy, average assigned variants in each problem,
then problems in each source, then sources equally. Missing variants score
zero before averaging. Report raw-row and problem-macro accuracy too.
Recovery results are separated into inverse-solvable, inverse-suboptimal,
and inverse-unavailable cohorts. These are private scoring annotations.

## New diagnostics and practice endpoints

The 943 `delayed-repair` probes include `repairContext.checkpointObservation`,
`executedHistory`, `lagAfterError` and the nonterminal-corridor rule. They
use the same candidate-index answer envelope as `next-action`.
`geometry-continuation` and `appearance-continuation` use the same
first-conflict answer envelope as `continuation`. All diagnostic answers
freeze on the first accepted submission.

Practice adds `GET /api/catalogue`, `GET /api/preview/{id}` and
`GET /api/probes/{id}/review` after submission. Model demonstrations use
`GET /api/models`, `POST /api/model-runs`, `GET /api/model-runs/{id}`,
and `POST /api/model-runs/{id}/{step|run|stop}`. Their call limits,
timeouts and interrupted-call semantics are in `MODEL-INTEGRATION.md`.
`case-local` is an archived actual version-2.1 model run. The original task,
bank identity and image bytes remain unchanged; it is not a version-2.2 result.

The seven task families are presentation categories. D1–D4 mean optimum-length
bins 1–8/9–16/17–24/25+, not required reasoning depth. Primary outcomes remain
assigned completion, optimal completion and conditional excess. The evaluator
tracks overlapping errors and delayed cohorts without treating the terminal
goal as corridor repair.
