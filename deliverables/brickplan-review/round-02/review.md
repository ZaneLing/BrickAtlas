# BrickPlan 2.3: Independent Final Simulated CVPR Review

## Recommendation

**7/10, Accept. Confidence: 4/5. Zero open critical or major issues; one open minor presentation issue (P2).**

This recommendation covers the final research and publication snapshot, including the actual PDFs and packaged artifacts. It is an independent simulated academic judgment, not an official CVPR decision or a prediction of acceptance. It does not certify a subsequent commit, external deployment, or empirical results absent from the workspace.

The frozen experiment-complete assumption is applied exactly: competent completion of the declared model and human studies is assumed for evaluating the design, but favorable performance, statistical significance, perceptual answerability, human agreement, ranking reversals, and empirical superiority are not assumed. Missing population measurements are not a rejection reason by themselves. No inference or human collection was performed for this review.

## Open Finding

**P2, minor, open: the supplementary structural-control chart has an incorrect color legend.** On supplement page 37, both "Completed" and "Optimal completion" legend swatches are blue, whereas the bars use light green and dark green. This is visible in both the published PDF and `figures/mechanism-evidence.png`. The two empty bar containers used to construct the legend do not reproduce the colors of the plotted series in the final output.

- Evidence: [documents.py:769-780](file:///Users/bytedance/Documents/trae_projects/brick-atlas/benchmark/brickplan-v2.3/documents.py#L769-L780), [supplement page 37](file:///tmp/brickplan-v23-work/pdf-review/supplement/page-37.png), and [chart image](file:///Users/bytedance/Documents/trae_projects/brick-atlas/benchmark/brickplan-v2.3/figures/mechanism-evidence.png).
- Implication: readers cannot reliably map the legend colors to completion versus optimal completion. This is a presentation defect, not evidence of incorrect counts: the main structural-control table independently labels both quantities, and the source uses the appropriate denominators.
- Testable closure: use the actual plotted handles or explicit correctly colored legend patches; regenerate the chart and supplement in a separately authorized snapshot; inspect the actual PDF and verify the two swatches against the bar colors and the tabulated values.
- Disposition: nonblocking for this recommendation. The frozen artifacts were not edited. This issue was newly identified during final visual inspection; the prior design-only verdict did not certify this rendered chart.

## Snapshot and Independence

| Item | Verified identity |
| --- | --- |
| Round | `v23-publication-02` |
| Snapshot mapping SHA256 | `73fae622dadfb66aaebe1788b2939a8e4b942bd4e041c3c97c121107ea3b154f` |
| Bank SHA256 | `8a1260a450300adb4693fafad8f59e1b7473316bf1d20f004981090008df1058` |
| Main PDF | `7dfa64effee05ad5bd866c3912d94ab4679ce584b57dd14d644d9ff840e03a91` |
| Supplement PDF | `4cf79dea2914939086ce7e55bd32a9769e0d5299f3cd9edf194d41e00064b1f0` |
| Runtime ZIP | `33cad6dd72ff77e5869ea50037be618455d76ba3b309c5f6079896a0b6354f60` |
| Overleaf ZIP | `3126c6b67da98c1eee7aceb7370a5edef433ffaa972040cc020a2913348c9dd0` |

All 7,911 listed research/artifact hashes, the canonical mapping digest, and the three separately listed external evidence hashes matched. Comparison against the prior 717-file design snapshot found exactly the five declared changed files: `appendix.tex`, `documents.py`, `package_release.py`, `paper.tex`, and `supplement.tex`. The bank, construction logic, source evidence, task contracts, scorers, and controls covered by that prior mapping are unchanged. The expanded final snapshot also binds the completed audits, final publication assets, and release evidence.

The prior independent design findings are reused where unchanged, not represented as fresh tests by this reviewer. Only this round's `review.md` and `review.json` were written in the assigned round folder. A temporary standalone checker lives at `/tmp/brickplan-v23-reviewer-02/check_publication.py`. No research files, prior verdicts, response files, validation files, git index, or commits were modified by this reviewer.

## Final Publication Assessment

**Typography and layout.** All seven main-paper pages and 64 supplement pages were inspected as contact sheets, with full-page inspection of the two main figures, metric/source table, representative gallery, structural-control plot, and resource replay. Fresh rendering independently reproduced every one of the 71 supplied page PNGs pixel-for-pixel. All pages are US Letter; text-bound checks found no out-of-page text, unresolved `??` references, replacement characters, or Chinese text. Main body text is predominantly 9.96 PDF points, consistent with nominal 10pt TeX, and uses the intended embedded Nimbus/Times family. No Latin Modern body substitution remains. The supplementary vector chart uses embedded Type 3 DejaVu glyph procedures; these were checked directly, not mistaken for missing fonts because the generic extraction API does not return their font programs. This is not a blanket certification of future conference submission preflight requirements.

**Gallery and census.** There are 25 gallery pages containing all 98 unique base-profile IDs in bank order, four per page except the last two. Unnumbered gallery headings avoid appendix-letter overflow. Profile, kit, split, admitted-part, registered-site, and movable-site information are legible in the inspected examples. The source census explains that admitted subassemblies are not complete kits and that 270 zero-yield profiles are not tasks. The metric-denominator table now shares supplement page 4 with the beginning of the source census rather than consuming an otherwise empty float page. The lengthy supplement remains a reference census rather than a concise narrative; that is a usability limitation, not a construction defect.

**Main geometry figure.** The source-10037 pair is visibly distinct in the certified initial isometric view. Its exact stored labels are `3` and `null` after two shared legal operations. Both members retain 63 pieces, including 47 fixed pieces and 16 registered sites, with matching inventories, state, goal, rack capacity, jobs, and proposed plan. The figure's embedded observation certificate matches the bank-bound certificate, which records 49,716 differing current-view pixels at native resolution. Publication ID overlays are explicitly omitted, and answers are labeled evaluator annotations. This is a faithful illustrative contrast, not a self-contained perceptual-answerability test.

**Repair figure and P1.** The source-10036 lag-5 case now passes final visual inspection: `P002` and `P013` callouts are readable, the complete seven-operation repair is printed, and the nine-operation inverse-first alternative is explicit. The figure's history, pre-error/current states, repair cost, and inverse-control record match the bank. It is clearly an oracle replay, not a model success. P1's closure is therefore retained and extended to the actual final rendered figure. The shortest-path certificate itself is inherited from the unchanged independent construction audit, not recomputed in full here.

Independent image extraction found pixel-identical copies of both main figures and all 25 gallery images plus the resource replay in their respective PDFs. All 31 figure-file hashes, the caption-file hash, and the mesh hash match provenance. Relevant source: [figure construction and provenance](file:///Users/bytedance/Documents/trae_projects/brick-atlas/benchmark/brickplan-v2.3/documents.py#L539-L796).

## Scientific Assessment

The useful contribution is an exact, auditable instrument that composes registered-site assembly with finite storage, persistent off-assembly work, future-cost labels, and nonterminal repair targets. It is not a new search algorithm or the first interactive brick-construction benchmark. The current related-work positioning was checked against the primary abstracts of InstructioNet, LEGO-Puzzles, PhyBlock, and Brick-Composer: interactive construction, multi-step planning, failure diagnosis, and diverse-brick pose estimation already have close precedents. The paper fairly acknowledges these overlaps. Its narrower exact-cost and repair decomposition remains useful, but novelty is incremental. [Related-work text](file:///Users/bytedance/Documents/trae_projects/brick-atlas/benchmark/brickplan-v2.3/paper.tex#L131-L152).

R5 remains substantively closed. The unchanged bank has 1,421 episodes and 7,020 probes from 97 active source groups, but the primary geometry evidence is only 36 matched pairs, 18 interventions, and 12 sources, including 24 pairs from nine held-out sources. Exact inventory matching removes the former global-count/type-color confound. Full-source failures remain excluded without replacement or modification of original evidence. Both exact conflict labels are required, with missing partners and malformed answers receiving zero joint credit; repeated starts and interventions are nested within source-level weighting.

The added support-only wording is scientifically important and correct in scope: all retained primary illegal members fail through unsupported assembly, while their motion-blocker relations match. It narrows interpretation instead of moving the unsupported broader claim into the supplement. These cases support a diagnostic of support-context dependence, not changed path-clearance reasoning or demonstrated long-horizon visual planning. [Main scope](file:///Users/bytedance/Documents/trae_projects/brick-atlas/benchmark/brickplan-v2.3/paper.tex#L317-L341), [supplement scope](file:///Users/bytedance/Documents/trae_projects/brick-atlas/benchmark/brickplan-v2.3/appendix.tex#L308-L389).

Strong controls constrain the interpretation: depth-one uniform-tie next-action accuracy is approximately 97.35%; inverse-last succeeds on 2,260/3,829 repair probes; 100-expansion A* completes 4,075/4,263 seeded runs. Neither long optimal trajectories nor failure of weak policies establishes required cognitive depth. The manuscript retains these cautions. Competently completed matched static/active/structured studies could yield interpretable positive, null, or negative results. Visual answerability, model gaps, and nonlocal recovery benefits must remain result-dependent.

## Artifact Consistency

The runtime archive is exactly 85,685,787 bytes. Fresh verification checked all 2,985 inventory entries, the exact archive-member set, absence of duplicate member names, and correspondence with available frozen workspace files. The canonical benchmark PDFs and complete editable Overleaf ZIP are present. Duplicate loose Overleaf trees and duplicate deliverable PDF copies are absent as intended. The Overleaf ZIP contains 59 source/resource files plus its inventory file; all 60 entries match the editable directory.

Independent Overleaf compilation and extracted-text equality for both PDFs are documented in the snapshot-bound deliverable manifest and were inspected, not repeated in this review. Likewise, the extracted-runtime native-render/oracle/original-scene/historical-case/regenerated-download pass and full browser driver are reused as completed evidence. Fresh checks confirm all 31 browser evidence input hashes, 13 public-export runtime hashes, and 101 export-file hashes match current files. Seven live HTTP routes independently returned status 200 and the exact recorded lengths and SHA256 values, including both PDFs, both ZIPs, questions, manifest, and root page.

The runtime bundle explicitly does not promise a full source-construction checkout. Its README points to the matching source checkout for original source assets, locked LDraw dependencies, and reconstruction audits. This distinction is consistent with the actual contents and does not silently weaken source reproducibility. A blind study still requires a separate policy host: downloadable private evaluator data and practice metadata are not safe policy inputs. [Packaging contract](file:///Users/bytedance/Documents/trae_projects/brick-atlas/benchmark/brickplan-v2.3/package_release.py#L181-L217).

## Evidence and Issue Dispositions

| Evidence | Status in this review |
| --- | --- |
| 7,911 snapshot hashes and three external checks | Freshly verified |
| 71 rendered pages, fonts/glyphs, page bounds, 28 embedded raster figures | Freshly verified; contact sheets and selected full pages visually inspected |
| Figure/caption/mesh bindings and main case records | Freshly compared with bank and certificates |
| Runtime inventory, Overleaf contents, seven HTTP routes | Freshly verified |
| 8,441/8,441 records; 650 tables, 61,093,730 states, zero mismatches; 308 passing pairs | Inspected current bank-bound independent audit; not exhaustively rerun |
| Prior source parsing/corruption tests, 35 regressions, seed-37 controls, bounded exact-cost tests | Prior independent findings reused on unchanged inputs |
| Full browser driver, extracted-runtime execution, Overleaf compilation | Inspected completed evidence; current source/archive bindings freshly checked |

| Issue | Final disposition |
| --- | --- |
| R1 | Closed: static multiview and separately charged active protocol retained; answerability remains conditional |
| R2 | Closed: calibration exclusion, valid ties, and missing-variant denominators unchanged |
| R3 | Closed: inverse-last control and separate recovery cohorts retained, not universal shortcut elimination |
| R4 | Closed: strong privileged controls and operation-length interpretation retained, not required deep reasoning |
| R5 | Closed: replicated inventory-matched support interventions and exact joint scoring; no scientific regression |
| R6 | Closed: repaired acquired-frame metadata channel unchanged; broader routing/memorization caveat retained |
| P1 | Closed: final repair figure, callouts, complete trace, cost comparison, and provenance inspected |
| P2 | Open, minor: supplementary bar-chart legend colors do not match the series |

## Frozen Rubric

| Criterion | Score | Rationale |
| --- | ---: | --- |
| Contribution and closest work | 6 | Useful exact diagnostic composition; incremental relative to close assembly/planning work |
| Construct validity | 7 | Genuine matched support intervention and explicit finite contract; no broader physical or perceptual guarantee |
| Dataset depth, diversity, dependence | 7 | Substantial source extension and explicit attrition; effective primary visual sample remains modest |
| GT, scoring, denominators, shortcuts | 8 | Exact labels, conservative denominators, strong controls, and independent checks |
| Experiment design and uncertainty | 7 | Matched conditions and source-level analyses support interpretable outcomes without assuming favorable results |
| Reproducibility and source fidelity | 8 | Preserved original evidence, traceable figures, complete editable manuscript, and consistent runtime release |
| Narrative, readability, CVPR fit | 7 | Readable final paper and source-bound examples; long census and minor legend defect remain |

The overall 7 is a judgment, not an arithmetic mean. The auditability and coherent narrow task composition justify acceptance under the specified assumption; repaired typography and artifact consistency remove the design round's publication-verification reservation. Limited novelty, narrow support mechanism, modest held-out visual replication, and empirical uncertainty prevent a stronger recommendation.

## Residual Limits

1. Nine held-out primary source groups are the relevant visual replication unit, not 97 sources or thousands of rows. Only 18/116 qualified interventions yield retained contrasts; this is mechanism-conditioned selection.
2. Primary conflicts are early: 24/36 occur at operation three, with none beyond operation seven. Support-only contrast does not establish necessary long-horizon simulation.
3. Restricted deterministic information ceilings do not exclude local support cues, silhouette/framing, source-template recognition, stochastic strategies, or routing-address memorization. Zero deterministic joint ceiling is not a stochastic chance baseline.
4. Registered sites, explicit IDs, known inventories, clamped connectivity, inset collision proxies, and straight translations omit forces, clutch strength, grasping, arbitrary poses, and real rack transport. Public CAD may overlap pretraining.
5. Native pixel distinction and competent collection do not imply empirical answerability, a human-model gap, or a favorable static/active/structured outcome. Source-bootstrap summaries are conditional on retained sources.
6. The artifacts are a public research preprint in the pinned author-kit, not a submission with a real paper ID or a certification of a future venue's requirements. Commit synchronization and external hosting remain outside this independent verdict.

**Final disposition:** the frozen final snapshot meets the rubric's recommendation threshold with no unresolved critical or major issue. The single minor issue is compatible with acceptance as reviewed; its correction would require a new authorized artifact snapshot. Any final committed-byte verification remains the orchestrator's responsibility.

## Primary Literature Checked

- [Learning to Build by Building Your Own Instructions](https://arxiv.org/abs/2410.01111): interactive Break-and-Make, explicit visual instructions, and long construction sequences.
- [LEGO-Puzzles, version 4](https://arxiv.org/abs/2503.19990v4): elementary VQA and a separate multi-step Planning set.
- [PhyBlock](https://arxiv.org/abs/2506.08708): progressive block assembly, VQA, failure diagnosis, and planning robustness.
- [Brick-Composer](https://arxiv.org/abs/2606.05445): diverse-brick selection and pose-estimation benchmark.

These primary abstracts were retrieved during this review; no claim of an exhaustive new literature survey is made.
