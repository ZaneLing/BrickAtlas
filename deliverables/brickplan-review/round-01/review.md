# BrickPlan 2.3: Independent Design and Construction Review

## Recommendation

**7/10, accept for the explicitly limited design/construction scope. Confidence: 4/5. R5 is closed in that scope. No unresolved critical or major construction issues were found.**

This is a simulated academic assessment, not an official CVPR decision. It is **not final publication acceptance** and does not satisfy the protocol's final verified-release stop condition. Missing new PDFs were not penalized. The subsequently reported gallery-section overflow and font-encoding warnings belong to the forthcoming publication review.

The recommendation applies the experiment-complete assumption in `tem/agent-iterations/PROTOCOL.md`: competent completion of declared model/human collection is assumed for design assessment, but no favorable performance, answerability, significance, human agreement, or empirical superiority is assumed or asserted.

## Snapshot and Scope

- Round: `v23-design-01`.
- Snapshot SHA256: `1d7a6af66619499384ceaa05cc7f0edfa4213bf86dc7df4e61455d836b550ef8`.
- Bank SHA256: `8a1260a450300adb4693fafad8f59e1b7473316bf1d20f004981090008df1058`.
- All **717/717** listed file hashes and the canonical mapping digest matched at both the initial and final design checks.
- The final design check preceded explicit handoff allowing the main agent's typography changes. This verdict does not certify those later edits.
- Only this round's `review.md` and `review.json` were written in the assigned directory. Test scripts and generated test evidence were confined to `/tmp/brickplan-v23-reviewer-01/`. No research code, paper, source assets, or previous verdicts were edited.

## R5 Disposition

The repair is substantive, not merely a larger row count or revised wording.

**Construction and replication.** Independent recount gives 1,421 episodes, 7,020 probes, 97 active source groups, and 142 active profiles. The 100-candidate extension admits 81 sources, each contributing exactly 12 seeded source episodes. The bank has 34 development and 63 held-out source groups. Its 412 qualified profiles include 270 without active episodes; these must not be counted as independent task evidence. Sampling uses declared geometry/reachability criteria and seeded starts rather than selecting new source episodes by policy difficulty. The frozen-plan equality is verified; hashes alone do not independently establish the historical timing of preregistration.

**The former count confound is removed.** All 36 primary pairs match the complete part-number/color multiset, registered part records and poses, start, goal, capacity, jobs, and proposed plan. They span 18 interventions and 12 sources; 24 pairs span nine held-out sources. Eight of the 12 sources are newly admitted, including six of the nine held-out sources. The remaining sources are reused legacy sources with new matched interventions, not new independent acquisitions. All pairs change an exact first-conflict label after a genuine common legal prefix. The ten historical unmatched pairs remain separate.

**Source fidelity is enforced before final inclusion.** All six post-qualification failures are absent from active profiles: 10124, 10226, 10261, 10262, and 21318 omit direct model geometry; 30312 has conflicting original root identity. Their prior admissions and original evidence remain preserved. Checking only ordinary leaves would have been insufficient; the whole-source gate correctly retains this distinction. There is no evidence of source repair or replacement to obtain these closures.

**The metric measures the claimed contrast.** Primary credit requires both exact labels. Missing partners, absent responses, malformed answers, and incorrect conflict indices cannot obtain joint credit. Repeats, starts, interventions, and sources receive the declared nested weights. The implementation provides source bootstrap and leave-one-source-out summaries without manufacturing intervals for a single source. Fresh seed-37 controls reproduce zero deterministic joint ceilings for count, global type/color presence, multiset, sequence, and address-normalized metadata, while retaining a ceiling of one for metadata with routing addresses. The latter is finite-bank memorization capacity, not a demonstrated held-out prediction attack.

**Judgment.** These changes satisfy the prior request for independently replicated, count/type-matched, answer-changing geometry with exact scoring and explicit shortcuts. They support a bounded visual support-connectivity diagnostic. They do not establish broad mechanical intelligence, long-horizon visual reasoning, or immunity to richer spatial shortcuts. Within the revised claims, those limitations no longer justify keeping R5 major/open.

Key implementation evidence: [source admission](file:///Users/bytedance/Documents/trae_projects/brick-atlas/benchmark/brickplan-v2.3/qualify_sources.py#L55-L168), [failure preservation](file:///Users/bytedance/Documents/trae_projects/brick-atlas/benchmark/brickplan-v2.3/qualify_sources.py#L197-L230), [context selection](file:///Users/bytedance/Documents/trae_projects/brick-atlas/benchmark/brickplan-v2.3/qualify_contrasts.py#L45-L107), [requalification](file:///Users/bytedance/Documents/trae_projects/brick-atlas/benchmark/brickplan-v2.3/qualify_contrasts.py#L157-L206), [answer-changing construction](file:///Users/bytedance/Documents/trae_projects/brick-atlas/benchmark/brickplan-v2.3/diagnostics.py#L97-L167), [source/question bindings](file:///Users/bytedance/Documents/trae_projects/brick-atlas/benchmark/brickplan-v2.3/audit_v23.py#L45-L185), [pair scoring](file:///Users/bytedance/Documents/trae_projects/brick-atlas/benchmark/brickplan-v2.3/matched_metrics.py#L201-L300), and [restricted controls](file:///Users/bytedance/Documents/trae_projects/brick-atlas/benchmark/brickplan-v2.3/matched_controls.py#L188-L233).

## Evidence Ledger

| Check | Evidence status | Observed result |
| --- | --- | --- |
| Snapshot integrity | Reproduced | 717 hashes match; canonical digest matches |
| Source archive/proof links | Independent recount | 96 gzip/raw proof hashes; 54,978 ordinary leaves match manifests; 7,573 retained new-profile leaf links checked |
| Original hierarchy | Fresh rerun of separate source-audit implementation | 21004 passes; 10261 retains direct-geometry failure despite passing ordinary leaves; both regenerated proofs byte-match archived raw proofs |
| Source corruption controls | Reproduced | All 14 leaf/identity/matrix/path mutation tests pass |
| `audit_v23` | Fresh production-audit rerun, outputs redirected to `/tmp` | 142 active profiles, 8,441 questions, 36 primary pairs pass, including fresh source parsing and reachable-site checks |
| Episode and sequence execution | New independent adjacency/occupancy/rack/job implementation | All 1,421 witnesses and all 596 sequence-probe first-conflict labels match |
| Exact costs and choice labels | Bounded rerun of archived independent rules | Eight tables, 64,886 costs, 16 episodes, and 66 probes pass, including 34 delayed-repair probes |
| Scoring/protocol regressions | Reproduced | 35 selected tests pass; 12 additional inverse-permutation checks cover both seeds and all repair cohorts across both splits |
| Reduced-input controls | Fresh generation at seed 37 | Six restricted joint ceilings are zero; full-address ceiling is one; both label-free inventory rules have zero held-out joint credit |
| Complete independent audit | Inspected after completion, not wholly rerun by this reviewer | Bank-bound 650 tables, 61,093,730 cost entries, zero mismatches or length discrepancies; 8,441/8,441 records and 308/308 pairs pass |
| Semantic, upgrade, observation evidence | Inspected, not fully rerun | Semantic and upgrade reports pass on this bank; snapshot-native observation certificate is complete for all 46 visual pairs at seed zero |
| Software policy controls | Inspected after completion | Full closure A* solves all 4,263 seeded runs optimally; depth-one uniform-tie next-action accuracy is 97.35% |

The initial broader unit invocation was deliberately interrupted during the expensive full-bank inverse-permutation loop. It is not reported as a completed suite. The explicitly bounded 35-test suite and 12-case replacement sample completed successfully.

These checks do not independently remeasure every mesh/path clearance, certify real-world mechanics, or demonstrate perceptual sufficiency. The full audit and final controls arrived outside the original 717-file mapping; their exact hashes and bank bindings are recorded separately in `review.json`.

## Remaining Limits

1. **Visual replication remains modest.** The primary visual inference unit is nine held-out sources, not 97 sources or thousands of rows. Only 18 of 116 qualified matched interventions yield a retained contrast. This mechanism-conditioned yield is informative but not a representative prevalence estimate.
2. **The primary geometry mechanism is narrow and early.** Every primary illegal member fails through unsupported assembly, not a changed motion blocker. Conflict positions are 3:24, 4:1, 5:3, 6:2, and 7:6. Thus 24/36 pairs conflict at operation three. This is meaningful support-context discrimination, not evidence that lengthy simulation is necessary.
3. **Strong shallow controls remain important.** The inspected full results give depth-one uniform-tie accuracy of 97.35%, inverse-last accuracy of 2,260/3,829, and 100-expansion A* success of 4,075/4,263. Long optimum lengths or weak-control failures still cannot establish required cognitive depth.
4. **Information ceilings have a restricted scope.** Equality of global inventory representations does not rule out local support-presence, silhouette, framing, source-template, stochastic, or routing-ID-assisted strategies. Separate-policy-host isolation and the full-address caveat remain necessary. A deterministic zero joint ceiling is not a stochastic chance baseline.
5. **Physical and empirical scope stays bounded.** Known-site registration, clamped stud connectivity, guarded inset collision meshes, and straight translations exclude force balance, clutch strength, grasping, arbitrary poses, and real rack transfer. Public CAD can overlap pretraining. Pixel differences alone do not establish human/model answerability.

These are residual limitations compatible with the current narrow contribution, not newly demonstrated major defects. Stronger future claims would reopen the corresponding validity questions.

## Prior Issues and Rubric

| Issue | Disposition |
| --- | --- |
| R1 | Closed in its prior static/active protocol scope; new bank-bound observation evidence inspected; general answerability remains conditional |
| R2 | Closed; calibration, ties, and missing-variant denominators retained and regression-tested |
| R3 | Closed for inverse-control/cohort reporting, not shortcut elimination |
| R4 | Closed for privileged shallow controls and length-bin interpretation, not demonstrated deep planning |
| R5 | Newly closed for the bounded matched-support construction and scoring contribution |
| R6 | Closed; acquired-frame metadata noninterference and restart/retry regressions pass |
| P1 | Prior closure retained; no claim that the new final figure/PDF has been re-certified |

| Criterion | Score | Assessment |
| --- | ---: | --- |
| Contribution and closest work | 6 | Useful exact-cost/repair diagnostic instrument; incremental relative to interactive brick construction and spatial-planning benchmarks |
| Construct validity | 7 | Count-matched support interventions and controlled task inputs are genuine; broad physical/visual-depth claims remain excluded |
| Dataset and dependence | 7 | Substantial new source admission and explicit attrition; modest effective visual sample and conditional selection remain |
| Ground truth and scoring | 8 | Exact labels, conservative pair denominators, corruption tests, and independent discrete checks are strong |
| Experimental design | 7 | Matched conditions, source-level uncertainty, and meaningful negative outcomes are interpretable without assuming favorable results |
| Reproducibility and fidelity | 8 | Whole-source gates and exact leaf bindings materially strengthen construction; final packaging is not certified here |
| Narrative and CVPR fit | 7 | The bounded diagnostic narrative is defensible; this score excludes final typography/layout and publication readiness |

The overall score is an independent judgment, not an arithmetic mean. Closest-work assessment is retained from the earlier review and checked against the current related-work positioning, without a new literature search: [Learning to Build by Building Your Own Instructions](https://arxiv.org/abs/2410.01111), [LEGO-Puzzles](https://arxiv.org/abs/2503.19990), and [PhyBlock](https://arxiv.org/abs/2506.08708). Interactive assembly and long sequences are not claimed as novel; the useful distinction is exact future-cost, resource/work coupling, and nonterminal repair under a deliberately finite contract.

## Concrete Closure and Finalization Tests

1. **Preserve R5 closure:** on any changed bank, rerun exact inventories, registered original poses, start/goal/jobs/capacity/plan equality, shared legal prefixes, both conflict labels, and source/intervention/start recounts. Historical unmatched pairs must never enter the primary score.
2. **Preserve source fidelity:** keep all 100 candidates and six post-qualification exclusions; verify original, manifest, dependency, and decompressed proof hashes. A direct-geometry or identity failure must reject cached-positive admission as well as fresh admission.
3. **Preserve scoring:** retain exact-index, wrong-index, boolean/malformed-answer, missing-response, one-sided-pair, duplicate-start, cohort/split, and source-bootstrap regressions. Report address-inclusive ceilings alongside normalized ones.
4. **Close final publication verification:** generate a new complete snapshot after typography fixes; bind the final tables, captions, figures, public questions, PDFs, and archives to the same final bank and completed audit reports. Review actual compiled pages for appendix overflow, intended fonts, readable callouts, and correspondence with provenance. No successful render is assumed here.
5. **Constrain empirical interpretation:** report matched static/active/structured outcomes, preprocessing, assignment coverage, source-level uncertainty, and leave-source-out sensitivity. Require actual answerability and cohort evidence before claiming visual reasoning depth, nonlocal recovery superiority, or human/model gaps. A negative result is allowed; favorable results are not required for construction validity.

**Bottom line:** R5's original global-count confound and inadequate construction-level replication have been repaired sufficiently for this bounded instrument. The design can proceed to a separate final rendered-publication review without another scientific construction repair being required by this round.
