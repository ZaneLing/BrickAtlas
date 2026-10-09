# BrickPlan 1.2 protocol

The wire schemas are `brickplan-observation/1.2`, private
`brickplan-trajectory/1.2`, public `brickplan-public-trajectory/1.2`,
`brickplan-submission/1.2` and `brickplan-evaluation/1.2`.
Version 1.0/1.1 submissions require their frozen executors.

## Observation and actions

Both tracks receive four PNG base64 panels: `current`, `target`,
`siteReference`, and `catalog`. PNG bytes are scientific renders of the
original LDraw geometry. `image-id` receives only opaque site/piece ID lists,
budgets, revision, view, status, action schemas and explanatory text.
`known-pose-structured` additionally receives calibrated matrices, part types,
directions, inventory, occupancy and target flags.

All P and S IDs are selectable; there is no legal-action mask.
Same-type/color pieces are interchangeable. IDs remain stable within a
session; geometry/site permutations do not alter physical instance poses.

An action uses this envelope:

```json
{
  "requestId": "unique-client-request",
  "revision": 0,
  "action": {"type": "attach", "partId": "P001", "siteId": "S003"}
}
```

Actions:

- `attach(partId, siteId)` or `detach(partId)`: one structural attempt.
- `inspect(view)`: one inspection, independently budgeted.
- `diagnose(needsRework: boolean)`: one diagnosis, independently budgeted.
- `finish`: terminal; success requires exact target occupancy.

`needsRework` means temporary reversals beyond changing each mismatched site
once. Required removal of an unwanted piece alone is not temporary rework.
Invalid structural requests consume one action. Malformed envelopes, stale
revisions, conflicting request IDs and post-terminal requests are rejected
without a committed action. Identical request ID/content retries return the
same result without double spending.

Default inspection quota is 32 and diagnosis quota is 8. Views are isometric,
front, rear, left, right, top, bottom, and exploded-reference. Initial isometric
is free. Every inspect request counts, including reselecting the current view.
Exploded-reference changes only the all-site diagram. Live current and target
images remain assembled. There is no uncharged free orbit in the scored UI.

## HTTP routes

| Route | Contract |
|---|---|
| `GET /api/tasks` | Opaque task IDs, release, track, study flag, action budgets |
| `POST /api/sessions` | `{taskId, seed?}` creates a run; seed is unsigned 32-bit |
| `GET /api/sessions/{id}` | Current public observation |
| `POST /api/sessions/{id}/actions` | Revision-checked action envelope |
| `GET /api/sessions/{id}/history` | Public actions, attempt/revision, result codes |
| `GET /api/sessions/{id}/export` | Terminal public history; no private state masks |
| `GET /api/sessions/{id}/score` | Terminal practice only |
| `GET /api/sessions/{id}/replay` | Terminal practice frame metadata |
| `GET /api/sessions/{id}/frame/{n}` | Terminal practice raster observation at frame |
| `GET /api/probes` | Opaque probe IDs and kinds |
| `GET /api/probes/{id}` | Public observation and question/proposal |
| `POST /api/probes/{id}/inspect` | `{view}`; persistent inspection quota |
| `POST /api/probes/{id}/answer` | One frozen answer |

Probe answers are `{"firstConflict": integer-or-null}` or `{"choice": index}`.
Indices are 1-based plan steps and 0-based offered choices, respectively.
Inspection after an answer is rejected. Reloading a probe does not reset
its view quota. Pairs are presented under opaque IDs in shuffled order.
Continuation-pair scene seeds match; candidate positions are randomized.

Private meshes, source files, costs, geometry, labels and certificates have no
HTTP download routes. A local process with repository access is still privileged;
the HTTP allowlist is not a substitute for separating policy/evaluator hosts.

## Collection and accountability

Each store binds release, observation track, probe seed and practice/study mode.
Restarting under another configuration is rejected. Study mode rejects repeated
episode starts and hides scores/replay. Practice permits repeats and review.

The server writes authoritative private events atomically. The offline collector
normalizes shuffled probe choices and requires explicit selection when more
than one episode exists for the same task. Offline evaluation replays every
private request and checks every supplied result, transition hash and task hash.
No scored result is trusted merely because it appears in an export.

The public browser export omits private bitmasks and is for review. Obtain
certified submissions through administrative collection from the run store.
Reports with mixed observation tracks are rejected. Provider errors or
interrupted external policies leave unfinished runs for explicit censoring;
do not silently replace them with successful retries.
