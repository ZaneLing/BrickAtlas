# Direct-neighbor evidence matrix

Fetched from arXiv HTML **v1** on 2026-09-20:
<https://arxiv.org/html/2606.07872v1>.
Metadata cross-check: <https://arxiv.org/abs/2606.07872>.
Retained HTML: `benchmark/ldraw-evidence-v4-draft/work/literature/visualflip-v1.html`.
This is a research working note, not an empirical benchmark result.

| Field | Verified VisualFLIP v1 content | Location |
|---|---|---|
| Title | VisualFLIP: Do Predictions Depend on Task-Critical Visual Evidence in Multimodal Reasoning? | Header / abstract page |
| Authors | Didi Zhu; Changrui Chen; Stefanos Zafeiriou; Jiankang Deng | Header / abstract page |
| Version/date | arXiv:2606.07872v1, 5 June 2026 | Version header and submission history |
| Publication status used here | arXiv preprint; no venue inferred | Abstract page has arXiv metadata, no journal reference inspected |
| Intervention | Same question; minimal task-critical image change deterministically changes gold. Synthetic state editing/rendering and local edits to existing images | §3.1, §3.3 |
| Pair metric | Pair accuracy, Acc_p: both images answered correctly | §3.2 |
| Failure metric | Collapse Rate (CR): among pairs correct on at least one side, fraction with identical nonempty answers | §3.2 |
| Perturbation families | Four: Cardinality, Attribute, Spatial, Logic. These are not four color/shape attributes | §3.1, §4.1 |
| Image/pair count | 1,374 images / 687 pairs | Abstract, §4.1 |
| Model count | 24 MLLMs, as reported in abstract | Abstract |
| Main inference relationship | Two independent calls; no cross-image context. It is not a single joint two-image request | §4.6, Appendix A.4 |
| Sequential diagnostic | Additional two-turn evaluation: original answer then perturbed image in the same conversation; SeqCR reports persistence | §4.6 |

All rows above refer to the fetched arXiv HTML v1 on 2026-09-20.
No model result values from that paper are reproduced here.

## Comparison that the inspected text supports

| Axis | VisualFLIP: what is specified in inspected text | BrickAtlas: actual current evidence | Wording boundary |
|---|---|---|---|
| Paired answer change | Explicit same-question answer-flip contract; independent calls and pair accuracy | Color and Part-type changed-answer pairs; Both | Pairing, minimal edits and joint correctness are prior art |
| Source/display identity | Synthetic symbolic states include objects, labels and deterministic answers; real-image symbolic maps are manually inspected | Source hash + instance identity, separate source truth and image-local display map in LDraw | Inspected sections do not specify the same CAD provenance/display-reference distinction; do not claim absence of all identity modeling |
| Shortcut design | Real-image visual-necessity filtering via whole-image masking; synthetic tasks have controlled rendering | Frozen full-set Part-type assignment with 13 privileged oracle-A rules, declared bounds and transition matrix | Do not say VisualFLIP has no shortcut control. The inspected sections do not describe an equivalent finite joint assignment and rule-bound audit |
| Human audit | Final pairs manually audited; symbolic maps checked/corrected; unclear edits excluded | Two exact-observation judgments, six reviewers with parent-disjoint exposure, retained adjudication and conflict blocking | Do not imply VisualFLIP lacks manual QA. The inspected sections do not specify the same exposure/hash/receipt audit contract |
| Response statistics | Pair accuracy and competence-conditioned symmetric CR; separate SeqCR | AAcc, NewAcc, Both, unconditional old-gold retention, format/failure denominators, source/author sensitivity | CR and old-gold retention have different denominators and should not be equated |
| Prior-answer exposure | Independent main evaluation plus sequential diagnostic | Independent calls only in frozen three-model plan | Oracle-A analysis is privileged construction auditing, not an implemented sequential model condition |

The defensible contribution is the integration of an explicit LDraw
source/display referent contract, a pre-inference restricted shortcut audit,
and exact-observation human/receipt lineage. Neither priority nor superiority
to VisualFLIP is inferred from the comparison.

## Independent main-executor check

The main executor read the original HTML header, abstract, §3.2, §3.3,
§4.1, §4.6 and Appendix A.4, plus the relevant Appendix B.1 construction
description. Bibliographic spelling and v1 date match the abstract page.
Numerical fields above appear in those inspected sections. The comparison
uses “not specified in inspected sections,” never unsupported claims about
the complete external code release.
