# BrickPlan 2.3: Independent P2 Follow-Up

## Verdict

**7/10, accept; confidence 4/5. P2 closed. Zero open critical, major, or minor issues; no regression found within the verified delta.**

This is a narrow independent follow-up to the completed publication review `20b50572-6eb6-42e5-ba50-33d93df0fc6b`, not a duplicate scientific review or an official CVPR decision. The recommendation applies to snapshot mapping SHA256 `bbd92607ce3a379cd891a0a6655574c55960d65726db754eab5a3eac7b8bb12f`.

The protocol's experiment-complete assumption is unchanged: competent declared model/human collection is assumed for design assessment, not favorable results, significance, answerability, human agreement, or empirical superiority. No new model calls or human collection occurred.

## P2 Closure

The actual [supplement page 37](file:///tmp/brickplan-v23-work/p2-review/supplement-page-37.png) and [chart](file:///Users/bytedance/Documents/trae_projects/brick-atlas/benchmark/brickplan-v2.3/figures/mechanism-evidence.png) were visually inspected. Both legend entries now occupy one row above the bars: **Completed = `#bdd0c7`; Optimal completion = `#276649`**. Neither swatches nor legend-label bounds intersect the bars. The supplied full-page raster was independently reproduced pixel-for-pixel from the current PDF.

The complete source diff against the archived, hash-verified pre-fix `documents.py` is confined to [lines 771-780](file:///Users/bytedance/Documents/trae_projects/brick-atlas/benchmark/brickplan-v2.3/documents.py#L771-L780): label the first actual bar container of each series, remove the two empty legend-only containers, and set `ncol=2`. No plotting formula, color, denominator, or other source statement changed. The archived source hash is `b0a82ac58fa8685be7d5c956acc7a2b46e704db2cb90bcc6756f19b53ebaa485`, matching round 02.

All ten rectangles in the chart PDF retain exactly their prior geometry and fill colors. Values recovered independently from vector heights in both the chart PDF and actual supplement page agree with the unchanged [control summary](file:///Users/bytedance/Documents/trae_projects/brick-atlas/benchmark/brickplan-v2.3/data/software-controls.json) and [table](file:///Users/bytedance/Documents/trae_projects/brick-atlas/benchmark/brickplan-v2.3/controls-table.tex):

| Control | Completed / 4,263 | Optimal / 4,263 | Completed % | Optimal % |
| --- | ---: | ---: | ---: | ---: |
| Greedy | 4,163 | 3,642 | 97.6542 | 85.4328 |
| Dispatch | 4,132 | 3,642 | 96.9270 | 85.4328 |
| A* 100 | 4,075 | 4,075 | 95.5900 | 95.5900 |
| A* 1,000 | 4,199 | 4,199 | 98.4987 | 98.4987 |
| Full A* | 4,263 | 4,263 | 100.0000 | 100.0000 |

Maximum vector-coordinate rounding error is below 0.000032 percentage points. The 2,244 x 726 chart PNG differs only inside pixel box `(1266, 79, 1826, 139)`, the legend region. Figure provenance changes only the two chart hashes. P2's actual-render, correct-color, and unchanged-value closure requirements are satisfied.

## Verified Scope

- Both snapshot mapping digests were recomputed. All **7,911 current file hashes** match; exactly **23 files** changed, with no additions/removals, agreeing with [changes.json](file:///tmp/brickplan-v23-work/review-round-02/changes.json). Bank, GT, geometry, scorers, control records, manuscript text, main PDF, and every other figure remain hash-identical. The bank identity remains `8a1260a450300adb4693fafad8f59e1b7473316bf1d20f004981090008df1058`.
- Old PDF/chart copies were bound to round-02 hashes before comparison. Fresh comparison of all **64 supplement pages** found identical extracted text and dimensions; at 1.5x raster scale, **only page 37 differs**, and the other 63 pages are pixel-identical. These are automated equivalence checks, not a repeated gallery review.
- The runtime ZIP has **2,985 inventory entries / 2,986 members**, all inventory hashes correct, no duplicate/unlisted members, and 2,984 available workspace counterparts byte-identical. Its generated root README has no workspace counterpart. The editable Overleaf ZIP has **59 source/resource entries / 60 members**, all matching the editable directory. All 64 deliverable-manifest hashes match.
- Current code, chart, provenance, and both canonical PDFs are present in the runtime archive; its nested Overleaf ZIP is byte-identical to the standalone archive and contains the corrected chart. All exported PDF/ZIP copies and both release-manifest copies match. Seven fresh read-only local HTTP GETs return status 200 and the recorded lengths/SHA256 values.
- All five snapshot-listed external evidence hashes match. The completed release freeze, independent Overleaf compilation/text comparison, and extracted-runtime verification were inspected as existing evidence, **not rerun**. Release-record differences are confined to the affected artifact bindings; scientific counts and claims are unchanged.

| Corrected Artifact | SHA256 |
| --- | --- |
| Supplement PDF | `b30f55c68568b0e5c9eb770ea1c9320007349750c31c54dd974451234a0b0d64` |
| Overleaf ZIP | `0a67a8dca01bc193337ec06e16611ee48c2be0475a25b172b3ed41a1e91c7db7` |
| Runtime ZIP, 85,684,478 bytes | `ca78ea560022d96fcc46310749ddcef4665ed2ca958a7df223dc5d9409e8b76b` |

## Scientific Disposition

[Round-02 scientific findings](file:///tmp/brickplan-v23-work/review-round-02/review.json) are reused only on verified unchanged inputs. R1-R6 and P1 remain closed. No full 61M-state audit, source reconstruction, regression suite, browser suite, gallery inspection, or literature survey was repeated.

| Frozen Criterion | Score | Follow-Up Assessment |
| --- | ---: | --- |
| Contribution / closest work | 6 | Useful exact diagnostic composition; novelty remains incremental. |
| Construct validity | 7 | Bounded matched support-context interpretation is unchanged. |
| Dataset depth / diversity | 7 | Source-conditioned replication limits remain. |
| GT / scoring / shortcuts | 8 | Prior independent correctness findings and strong controls remain applicable. |
| Experiment design / uncertainty | 7 | Interpretable outcomes without assuming favorable empirical results. |
| Reproducibility / fidelity | 8 | Corrected artifacts propagate consistently; original evidence is unchanged. |
| Narrative / presentation / fit | 7 | P2 is resolved; no new presentation defect observed in the delta. |

The overall 7 is an independent judgment, not an arithmetic mean. A legend correction removes a defect but does not strengthen the scientific contribution enough to raise the recommendation.

Residual limits remain: only nine held-out primary sources, with 18/116 qualified interventions yielding contrasts; support-only conflicts at operations 3-7 do not establish required long-horizon or path-clearance reasoning. Strong shallow and inverse-last controls constrain difficulty claims. Restricted deterministic ceilings do not rule out local cues, template recognition, stochastic strategies, or routing memorization. Registered sites and collision/support proxies omit general mechanics; public CAD may overlap pretraining. Pixel distinction does not establish empirical answerability, human-model gaps, or active-view benefit. Runtime-only packaging still needs the matching construction checkout and a separately isolated policy host. The long supplement and future venue preflight remain limitations.

Only this round's `review.md` and `review.json` were written. Research artifacts, prior reviews, response/validation files, git index, commits, and remote state were not modified. The recommendation threshold is met for the frozen snapshot; final staged/committed-byte checks and authorized push remain the parent's responsibility.
