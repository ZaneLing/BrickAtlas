# Protocol evidence for the evidence-following revision

Audit date: 2026-09-19. Page numbers below are PDF pages, including appendices.
All three PDFs were read in full: BrickNet 10 pages, LEGO-Puzzles 11 pages,
PhyBlock 40 pages. The local `.txt` files mark every PDF page. PDF hashes are
in `download-manifest.json`; official implementation hashes and exact URLs
are in `official/download-manifest.json`. No neighboring model was rerun.

## Version boundaries

| Work | Paper used for manuscript claims | Separately inspected official implementation |
|---|---|---|
| BrickNet | CVPR 2026 proceedings, June 2026, pp. 39252–39261; PDF pp. 1–10 | `kulits/BrickNet` at `b09a689c4929bd27f59c9bb9446237967aa332c9`, committed 2026-08-19 |
| LEGO-Puzzles | arXiv:2503.19990v3, 2025-06-20; PDF pp. 1–11 | `Tangkexian/LEGO-Puzzles` at `1413d2c236879573cc0afff646bae5e3d04023bd`, committed 2025-06-20 |
| PhyBlock | arXiv:2506.08708v2, 2025-11-21, bearing NeurIPS 2025 Datasets and Benchmarks attribution; PDF pp. 1–40 | `PhyBlock/PhyBlock` at `da81ed9cad8184509aadb6f01af83d53e5c9d6fa`, committed 2025-08-20 |

BrickNet's paper describes overlapping PT/SFT sets and 4,096-token training
(pp. 4–6); the later `DATA.md` describes disjoint distributed model splits,
combining PT/SFT path pools for training, and 6,400/2,816-token packing.
The paper names Qwen2.5-VL-7B for VQAScore (p. 7); the later
`eval/README.md` names Qwen2-VL-7B. We do not substitute the later recipes
into the paper's reported experiment. Our comparison does not rely on any
of those changing settings.

LEGO-Puzzles v3 states up to seven intermediate stages (pp. 3–4) and
Next-k-Step with k=1,…,5 (pp. 7–8). No step counts from its later OpenReview
revision are imported. The PhyBlock code snapshot predates the pinned v2
paper; code-specific observations below are labeled as such, not claimed
as a reconstruction of every v2 result.

## BrickNet: verified protocol

| Dimension | Evidence and interpretation |
|---|---|
| Unit and research question | Generated object/build sequence; unconditional and caption-conditioned generation, pp. 5–7, §5. Also held-out sequence perplexity. This is not a per-instance VQA score. |
| Visible evidence | Unconditional model receives a beginning-of-sequence token; conditional model receives a caption (pp. 5, 7). Graph-backed part/connector instructions are the generated representation. Eight renders per object are used for captioning (p. 4); image–text metrics evaluate generated renders (p. 7). |
| Identity and repeated parts | Graph vertices are placed part instances; spanning-tree text names them with letters, and connector names select part-local sites (pp. 3–4, Fig. 4). `core.Graph`, `core.Edge`, `tree.id2i` and `DATA.md`'s graph-local `edge_idx` preserve distinct repeated instances. Thus we do not claim that BrickNet lacks instance identity. |
| Evidence integration | Executable graph programs reconstruct poses from typed connections (§3.4, p. 4). This is an integrated generative representation, not separate visual/source/graph question families. |
| Sources | Human-designed online LDraw objects/scenes; 320,808 samples and 9,743 part variants in the paper (pp. 2, 4–5). SFT filtering includes part diversity and collision filtering; evaluation uses 512 held-out single-object source files. |
| Oracle/review boundary | Connector annotations combine procedural and manual authoring, all reviewed; inset meshes address collision estimation, with non-watertightness and physical deformation discussed explicitly (pp. 3–4). Prefix parse/connectivity validity and collision checks evaluate generation (pp. 5–7). This is not a human VQA answerability certificate. |
| Controlled conditions | Graph vs pose representation, sampling, model size and training-data/stage ablations are reported (pp. 5–7). Same-target answer-changing/answer-preserving VQA pairs with two semantic golds are **not reported** in this pinned paper. This does not imply that its assets could not support such an extension. |
| Outputs and executable checks | `score.score_text` returns number of actions, first invalid action and collision indices. `score.check_tree` decodes and checks placements. The paper regenerates unparseable caption-conditioned outputs before perceptual scoring (p. 7); this differs from our fixed-denominator failure policy. |

## LEGO-Puzzles: verified protocol

| Dimension | Evidence and interpretation |
|---|---|
| Unit and research question | VQA sample across 11 spatial and sequential task families, 100 per family; 1,100 questions from 407 building instructions (pp. 3–4). Ordering predicts a permutation, not executable low-level placement. |
| Visible evidence | Task-dependent multiple rendered images, text and answer options (Fig. 1, p. 2; §3.2, p. 4). Current/target states, next pieces and candidate states are visible when required. Official `LEGO.split_LEGO` interleaves `<image n>` tokens with images; `build_prompt_sort` asks for a letter sequence. Structured CAD records are used in curation, not supplied by these prompt builders. |
| Identity and repeated parts | Figure 1 uses red/blue arrows for Height and Adjacency, and image/option letters for states and pieces (p. 2). Source metadata has unified asset naming (p. 4). A stable scene-instance ID shared across image, record, graph and action contracts is **not reported** in this version. We do not infer inability to add IDs or handle repeated pieces. |
| Evidence integration | Several questions jointly require current/target images and part/step images; see Position, Next-Step and Ordering in Fig. 1. It would be incorrect to describe all neighboring tasks as single-image independent lookups. |
| Sources and controls | Public LEGO source projects with detailed building instructions; Studio rendering fixes the camera across steps; types, quantity, colors, positions and viewpoints can be edited for task construction (p. 4). This already supplies substantial reusable assets for controlled experiments. |
| Oracle/review boundary | Duplicate/image checks and three-annotator QA verification with unresolved cases revised or removed (p. 4). VQA accuracy uses rule-based extraction and ChatGPT fallback; image generation has five expert raters on appearance/instruction following (pp. 5, 7). These checks differ from source-derived connector oracles. |
| Paired conditions | Next-k-Step varies k=1,…,5 and compares prompts with/without CoT (pp. 7–8). Render transformations and erroneous choices construct tasks (p. 4). Same-target new-gold accuracy and both-correct adaptation under answer-changing/answer-preserving observations are **not reported** in v3. |
| Outputs and executable checks | `LEGO` in `image_mcq.py` builds MCQ/ordering prompts. `extract_answer_from_item` in `utils/multiple_choice.py` calls `can_infer_lego`; exact matching can return `Z`, and an enabled judge uses up to three retries with a random-option fallback after exhausted matching. These are code-snapshot policies, not rerun measurements. |

## PhyBlock: verified protocol

| Dimension | Evidence and interpretation |
|---|---|
| Unit and research question | Assembly plan and physical-understanding VQA are two branches; 400 assembly tasks and 2,200 VQA samples over 16 categories (§3, pp. 5–6). Planning has four complexity tiers. |
| Visible evidence | Planning takes target and candidate-block images plus instructions; interactive planning adds observations/history (§4.1, pp. 7–8; prompts pp. 25–27). The high-level output selects candidate IDs in order, without rotating them; exact pose prediction is deferred (§E.4, pp. 39–40). AOV dependencies and target poses are evaluator-side facts. |
| Identity and repeated parts | Scene JSON has unique `order`, `type`, `color`, `depend`, position and orientation fields (§A.3, pp. 17–18). Thus PhyBlock already has scene-instance identity. Model-visible dictionary IDs denote reusable candidate variants: “The same block index may be used multiple times” (pp. 25–26). They are not necessarily unique target-instance IDs. The official sample `data/SCENEs_400_Goal_Jsons/000.json` confirms the `order`/`depend`/`euler` schema. |
| Evidence integration | Planning jointly selects visually matching candidates and orders placements under structural constraints (§B.1–B.2, pp. 22–23). The VQA branch separately probes attributes, relations, scenes and dynamics (§3.3, pp. 5–6). |
| Sources | Eight modeled geometries, five colors, Genesis simulation, manually annotated scenes and geometric/compositional augmentations (§3.4, p. 6; §A.1–A.2, pp. 15–17). Internet images inspire scene construction; these are not an OMR/LDraw source corpus. |
| Oracle/review boundary | AOV evaluation matches unused legal ground-truth blocks and counts TP/FP/FN (Algorithm 1, pp. 22–23). Static VQA uses LLM generation with human verification; dynamic VQA uses simulated perturbations, frames and human verification (p. 19). No real-robot evaluation (§E.5, p. 40). These are positive existing capabilities, not claimed absences. |
| Controlled conditions | Pose-constrained vs topology-oriented scoring, full vs stepwise planning, multiple backgrounds/views and physical perturbation questions are reported (pp. 8, 19, 22–28). Our same-target visual semantic adaptation estimands are **not reported**; PhyBlock's scene and simulation assets could be extended to them. |
| Outputs and executable checks | Official `are_blocks_equal` compares type/color/euler in A and type/color in B; `is_place_legal` checks dependencies. `validate_block_placement` greedily assigns the earliest unused legal GT instance and computes TP/FP/FN. `extract_blocks_sequence` filters invalid dictionary indices. `BlockEnv.move_cube` selects a candidate at the current layer and uses target position/euler; `step` returns a rendered observation and feedback. This is not continuous pose/control synthesis. The code's four named paper error types are not all separately emitted by the top-level evaluator. |

## What labels and templates alone can and cannot establish

Adding IDs/templates to any of these assets could already support attribute
questions and connect question records to a scene. BrickNet can supply
instance/connector graphs; LEGO-Puzzles can supply step-consistent renders;
PhyBlock can supply scene IDs, dependencies and simulated perturbations.
We therefore do not claim exclusivity or that these projects could not
implement our experiment.

The extra measurement assets are a *bound pair*: canonical target/answer
semantics, exact model-visible images and text, each condition's gold,
truth-change policy, and condition-specific answerability decisions. Raw
responses are needed to tell correct adaptation from disruption. An aggregate
accuracy or a source JSON alone lacks that joint record. The contribution
is making this experiment explicit and auditable on unchanged human-authored
assemblies, with modular controls that expose elementary graph priors.

### Real-source example: OMR 42004, B0035

The original **Mini Backhoe Loader** source has 246 part instances; its hash is
`a32b924f302a1c028c1131f78e438ad2d78e70a041999690a1e4285e851f7dbf`.
In `public/benchmark/ldraw-v2/models/omr-42004.json`, B0035 is
`brick_000035`, part 32250, Black, from `42004 - front right side.ldr`,
source line 206. B0036 is another 32250 instance, Yellow, line 207.
B0196 is a Black 2780 Technic pin, from another submodel.

For `ld2-omr-42004-shape-match-1`, the question asks which numbered instance
has B0035's part type while ignoring color/pose. Its options map
A→B0196, B→B0116, C→B0036, D→B0060. The operand image's gold is C.
The wrong-image condition swaps displayed labels B0036 and B0196, leaving
the question/options fixed. In that image the matching geometry is labeled
B0196, so the image-conditioned gold is A. This is a visual binding
intervention, not a change to the source CAD truth.

| Asset | SHA-256 |
|---|---|
| Operand/crop image | `cc2826da13f55fd9234010d860f3894f9f7ffb692502d9018f3368fcb1551852` |
| Wrong image | `cd27939fd7988f8ab534a5115347cca2b6b0e0afa06195141f49c613605f59c1` |
| Offline materialized B request | `16bbda47009ab11e28c7fe37d18bcf464a6f606ab6b9fe6c3d765f45318c30fc` |

The pair would score correct adaptation only for C→A; C→C is stale
evidence and C→B is another legal error. These are scoring examples,
**not observed model predictions**. Existing source-gold scoring of the
wrong-image run remains intact as a separate dependency statistic.
The serialized B request and image/alternate-gold mapping were validated;
human visual answerability remains pending.

The same canonical identity also points to recognized axle connections
from B0035 to B0034/B0037/B0038/B0051 and to the independent
`restore-B0035` visibility action. Those links permit inspection; they
do not turn this visual item into a graph-and-action inference chain.
Their rendering must never depict physically new placements.

## Evidence that closes the present contribution argument

On unchanged natural graph-deletion questions, the node-only algorithm
answers 63/73 correctly, yet answers neither side jointly correctly on any
of the 73 fixed-node answer-changing pairs. BFS answers both correctly
on all pairs. These are measured algorithmic controls, with source-cluster
statistics in `node-prior-audit.json`. They show why ordinary accuracy
cannot establish structural evidence following under this distribution.
They do not establish a learned-model failure.

No validated learned-model responses are available for this revision.
The visual question therefore remains an explicitly measurable research
objective. The manuscript is a method/resource contribution with empirical
corpus/algorithm audits, not a completed VLM capability ranking.
