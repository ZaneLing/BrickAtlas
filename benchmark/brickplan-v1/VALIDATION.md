# BrickPlan 1.0 — Release Acceptance

Release: 2026-09-30. **All checks below passed. No VLM or human experiment was run.**

## Evidence

| Check | Observed result | Reproduction |
| --- | --- | --- |
| Source poses and geometry | 2 source subassemblies; unchanged original poses; complete endpoint/path coverage | `build.py --geometry` |
| Finite graphs and costs | 58,616 states; 568,648 directed transitions; 12 goal tables checked | `build.py`, `validate.py` |
| Semantic/adversarial checks | 14 tests passed | `validate.py` |
| Actual HTTP execution | 8 completed episodes; 26 probe responses; collection and all seven score sections | `validate_http.py` |
| Persistence and API contracts | 8 sessions restored; duplicate requests idempotent; stale revisions rejected; probe answers frozen | `validate_http.py` |
| Browser full build | 17 successful actions + 1 charged incompatible-part failure; success, action regret 1 | `validate_arena.mjs` |
| Browser repair | 3 detaches + 4 attaches; success, both regrets 0 | `validate_arena.mjs` |
| Browser review | Correct frame revisions, trajectory download, feedback JSON, probe identity, desktop/mobile layout | `validate_arena.mjs` |
| Browser console | No page errors in the tested Chrome flows | `arena-summary.json` |
| Manuscript | English PDF, detailed appendix, four source-mesh replay frames | `paper.tex`, `render_paper.mjs` |

Full reports are generated in
[`tem/brickplan-v1/validation/`](../../tem/brickplan-v1/validation/):
[`summary.json`](../../tem/brickplan-v1/validation/summary.json),
[`http-summary.json`](../../tem/brickplan-v1/validation/http-summary.json), and
[`arena-summary.json`](../../tem/brickplan-v1/validation/arena-summary.json).
The acceptance snapshot is packaged in [`release-check.json`](release-check.json).

The IDE browser loaded the Arena and reported no console errors, but its capture/
tab bridge failed. Screenshots and the complete button-driven flows were therefore
verified in local headless Chrome using the repository's Playwright installation.
This is an automated browser test, not a human study.

## Software controls

| Control | All episodes | Repair completion | Choice no-undo dead ends |
| --- | ---: | ---: | ---: |
| Privileged optimal oracle | 8/8 | 2/2 | 0/2 |
| Injected fault + optimal recovery | 8/8 | 2/2 | 0/2 |
| Deliberate trap + attach only | 2/8 | 0/2 | 2/2 |

These controls use private certificates intentionally. The fault/recovery
controller introduces a bad episode action but gives optimal independent probe
responses; the columns measure different assigned tasks. Its successful repair
does not erase its earlier first-loss survival event.

This contrast confirms intended software behavior. It does not establish task
discrimination among real models, human superiority, or generalization.

## Adversarial cases covered

- Removing, duplicating, or relabeling geometry coverage blocks certification.
- Changing an optimal-cost entry violates the exhaustive Bellman checks.
- Equivalent same-type/color instances can fill a site without private identity matching.
- Unknown IDs, incompatible parts, blocked moves, and invalid actions are charged.
- Duplicate request IDs do not perform or charge the same action twice.
- Reused request IDs with different content and stale revisions are rejected.
- Authoritative replay rejects altered results or duplicated exported events.
- Empty submissions retain all eight episode and all probe denominators.
- Failed episodes have null regret rather than a favorable zero cost.
- Early stopping produces survival bounds; it is not perpetual survival.
- Successful recovery does not reset the first-loss clock.
- Switching to the wrong answer in both counterfactual members scores zero joint correctness.
- Boolean/out-of-range probe answers are invalid, not silently coerced.
- Later or contradictory diagnoses cannot replace the first checkpoint diagnosis.
- Private task/cost files and active-episode scoring are unavailable through HTTP.
- Changing the task selector does not submit a response to an undisplayed probe.
- Reloaded sessions retain their authoritative public task identity.

## Release boundary

| Validated | Not established in 1.0 |
| --- | --- |
| Original source geometry/poses, qualified proxy paths | Physical construction, clutch force, grasp/tool clearance |
| Exact costs inside the declared action domain | Optimality over all continuous assembly motions |
| 17/18-action full tasks, four-part dependency chains | D2–D4 or hundred-step reasoning |
| Conflict prediction at distances 1/2/4/8 | Four levels of causal depth or maximum internal search depth |
| Two structures from one source kit | Independent topology/provenance generalization |
| Shared structured executor and human practice UI | Matched image-only VLM/human observation protocol |
| Reproducible software checks | Empirical model/human performance |

The original 12-case/six-family platform proposal remains an expansion roadmap.
It is superseded by [PROTOCOL.md](PROTOCOL.md) for this release.
