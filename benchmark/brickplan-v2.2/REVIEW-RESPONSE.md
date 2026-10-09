# Response to the 2026-10-09 instance review

Version 2.2 addresses `tem/research/20261009-cvpr-instance-review/feedback.json`.
Earlier releases and the original four-call model trace remain immutable.
The record count is 377 episodes plus 1,952 diagnostic questions.

| Issue | Implemented change | Verification and remaining limit |
|---|---|---|
| R1: identical default inputs with different answers | Static diagnostics supply four initial views; active mode starts isometric and bills acquisition; structured diagnostics match the static views | `observation-certificate.json` checks all five panels × four views for ten pairs. All static inputs differ; three isometric inputs do not. This is pixel distinguishability, not empirical answerability. |
| R2: all candidates correct | Keep valid ties, mark 26 rows calibration, exclude from discriminative accuracy | `quality.json`, `test_quality.py`, and complete oracle submission. 1,926 discriminative rows remain; calibration is reported separately. |
| R3: inverse-last shortcut | Implement public-history inverse control and three recovery cohorts | 547/943 solved; 368 inverse-suboptimal, 28 unavailable. Lag-one/three/five results are 235/337, 162/307, 150/299. Lag alone is not a nonlocal-reasoning claim. |
| R4: shallow structural heuristic | Publish depth-one tie distribution, uniform tie and all-candidate controls; match static image/structured views | All 653 checkpoints contain a correct minimizer; expected uniform-tie accuracy is 94.0% vs 36.9% for uniform candidates. No required cognitive depth is claimed. |
| R5: correlated rows and limited source diversity | Canonical problem scoring, source-macro reporting, five admitted additional source groups and 36 new qualified context candidates | 1,819 canonical diagnostic problems; 133 excess repeated rows. 16 sources (8/8 partitions), ten answer-changing pairs from three sources/four interventions. The requested 30–50-source scale is not reached; every retained visual contrast still has a part-count confound. |
| R6: acquired-frame hash exposes enumerable private occupancy | Public acquired-frame IDs now use only public revision and camera name | Regression checks compare metadata-equivalent private states across image tracks and seeds, active probes, replay, restart and retries. Private task/mission hashes remain only in evaluator exports. |
| P1: decisive repair IDs absent from figure | Add two sparse original-piece ID callouts plus exact seven-step repair and seven-versus-nine cost comparison | The main repair figure remains an explicitly labeled oracle replay, with unchanged source poses. |

The extension preserves all 145 prior episodes and 739 diagnostic definitions.
It adds 232 episodes and 1,213 questions. Eleven additional source candidates
were frozen; five passed geometry admission and six are retained as rejected
entries. Some admitted subassemblies have only two or four registered sites.
The 99 profiles include 82 fixed-context candidates, not 99 independent sources.
Of 41 qualified context pairs, 37 yield no retained answer-changing plan.

The software controls use exact structural relations, with 10,556 raw runs
including one oracle seed and three seeds for nine other policies. Full
closure A* solves all 1,131 assigned repeats optimally (maximum 12,578
expansions). Greedy completes 1,061, with 873 optimal. These are measured
software outcomes, never VLM or human substitutes.

The English paper and supplement use the unmodified pinned official CVPR
template. Figures show original LDraw poses, an initially supplied revealing
geometry view, and a certified inverse-suboptimal repair case. Source galleries
are split into readable pages. The Overleaf exporter includes all dependencies
and independently compiles the extracted ZIP.

The historical SmolVLM trace keeps its version-2.1 task, bank hash, public ID,
image bytes, raw outputs, and failure feedback. It is labeled historical in
the paper and interface. Population model/human studies remain unmeasured.

R5 remains partially unresolved at research scale. This revision does not
claim CVPR acceptance, count-matched geometry, human/model answerability,
force simulation, or immunity to every shortcut.
