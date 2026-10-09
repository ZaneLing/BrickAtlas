# Response to the BrickPlan 1.1 review

The revision is released as 1.2. Frozen 1.0 and 1.1 remain intact.
“Resolved” below refers to a concrete implementation defect, not paper acceptance.

| Review concern | Change / evidence | Status |
|---|---|---|
| Three-structure report claims two structures and one source group | Census and certificates derive from loaded banks; report says 3/2; missing episodes remain explicit | Resolved |
| DCR is based only on three isolated questions | Online legal eligible decisions, safe/unsafe alternatives, no-undo/no-rework/budget rates; invalid attempts separate | Resolved |
| Injected repair is conflated with autonomous recovery | Self-induced events have entry, first diagnosis, restoration, recurrence, cost and censoring records; injected repair remains separate | Resolved |
| Diagnosis stops after the first successful action | Event diagnosis begins after each self-induced trigger, even later in the trajectory; regression checked | Resolved |
| Missing episodes survive at time zero | Missing observations are censored, with lower/upper survival bounds | Resolved |
| “Lookahead” can be solved from first and last actions | 36 pairs preserve first/last, scene, length and action multiset; interior order changes validity; endpoint rule 36/72 | Demonstrated shortcut resolved |
| Supplied-plan length is mistaken for internal depth | Separate actual-conflict-position and plan-length curves; internal depth remains null | Claim corrected |
| Action regret and detach regret are presented as independent | Conservation identity included in evaluator, appendix and paper | Claim corrected |
| Browser/API “vision” exposes occupancy and exact poses | Image-ID server sends PNG pixels/opaque IDs only; separate structured track; no mesh/source routes | Implemented and protocol-tested |
| Humans receive free views unavailable to API agents | Both use the same inspect action, eight view options and persistent quota; no free scored orbit | Resolved |
| Static-rule baseline is missing | Explicit private-relation rule, bounded search, honest public/valid-random/blind-random controls | Implemented |
| Baseline is forced into known bad moves | Random and public policies select from their declared information; no injected trap actions in performance controls | Resolved |
| More steps do not establish hard planning | New reconfiguration tasks are certified but still solved by the static relation rule | **Unresolved mechanism limitation** |
| Temporary support replacement/scaffolding is proposed without proof | Exhaustive empty-to-state census and bounded partial-goal search found no qualifying mechanism; no such claim is made | **Not established** |
| Too few independent sources | Original three structures/two source groups retained; no padded “independent” cases | **Unresolved** |
| No VLM/human evidence | Matched tracks, study server, preregistration manifest, public adapter, collection and descriptive analysis added | Infrastructure complete; **empirical study pending** |
| Physical validity beyond fixed paths is unclear | Original geometry and qualification preserved; proxy/path/rigid-support boundary stated explicitly | Boundary clarified; **physical validation pending** |
| Counterfactual offered optimum may differ from global optimum | Definition remains best offered action; current inherited members were audited and had no positive offered-optimum gap | No unsupported defect claim |

## What the revision can support

- Exact fixed-path access-order diagnostics and reversible assembly costs.
- A concrete matched-probe shortcut test and visual/structured observation comparison protocol.
- Trajectory-level separation of invalid moves, legal future losses, diagnosis and restoration.
- Reproducible original-geometry human practice and evaluator-side software validation.

## What it cannot support yet

- A claim that the episode bank requires deep search given accurate relations.
- Measured VLM shortsightedness, a human advantage, or generalization to new source families.
- General assembly dynamics, arbitrary insertion paths, or D2–D4 physical difficulty.
- A claim that software corrections alone make the paper ready for CVPR acceptance.

The remaining research priorities are independently qualified mechanisms that
challenge the static rule, additional source groups, and preregistered
VLM/human experiments. These were not replaced with synthetic evidence.
