# Primary-source literature audit

Checked on 2026-09-19 through scholarly search followed by primary proceedings,
ACL Anthology or OpenReview records. Statements below are the claims used in
the revised manuscript; they do not imply a systematic literature review.
The six previously verified references remain in the preserved evidence-v1
bibliography. These seven additions address contrastive evaluation, VQA
consistency, visual reference grounding, construct validity and graph limits.

| BibTeX key | Verified primary publication | Claim supported and boundary |
|---|---|---|
| gardner2020contrast | Matt Gardner et al. *Evaluating Models' Local Decision Boundaries via Contrast Sets*. Findings of EMNLP 2020, 1307–1323. [ACL record](https://aclanthology.org/2020.findings-emnlp.117/) | Small meaningful changes, typically changing gold, probe local decision boundaries. BrickAtlas must not claim to originate contrast sets. The cited work concerns NLP datasets. |
| goyal2017vqa | Yash Goyal, Tejas Khot, Douglas Summers-Stay, Dhruv Batra, Devi Parikh. *Making the v in VQA Matter: Elevating the Role of Image Understanding in Visual Question Answering*. CVPR 2017, 6904–6913. [CVF record](https://openaccess.thecvf.com/content_cvpr_2017/html/Goyal_Making_the_v_CVPR_2017_paper.html) | Complementary similar images have different answers to the same question, reducing language-only shortcuts. This precedes paired image-dependent answer evaluation; the present addition is an explicit display-reference contract with reviewed exact observations. |
| shah2019cycle | Meet Shah, Xinlei Chen, Marcus Rohrbach, Devi Parikh. *Cycle-Consistency for Robust Visual Question Answering*. CVPR 2019, 6649–6658. [CVF record](https://openaccess.thecvf.com/content_CVPR_2019/html/Shah_Cycle-Consistency_for_Robust_Visual_Question_Answering_CVPR_2019_paper.html) | VQA-Rephrasings supplies three human rephrasings for 40k question–image pairs and studies answer consistency under linguistic variation. Invariance is distinct from required answer change. |
| mao2016refexp | Junhua Mao, Jonathan Huang, Alexander Toshev, Oana Camburu, Alan L. Yuille, Kevin Murphy. *Generation and Comprehension of Unambiguous Object Descriptions*. CVPR 2016, 11–20. [CVF record](https://www.cv-foundation.org/openaccess/content_cvpr_2016/html/Mao_Generation_and_Comprehension_CVPR_2016_paper.html) | Referring expressions identify an object/region in an image; ambiguity depends on surrounding alternatives. Numeric display tokens are a narrower reference interface, not a replacement for natural-language grounding. |
| thrush2022winoground | Tristan Thrush, Ryan Jiang, Max Bartolo, Amanpreet Singh, Adina Williams, Douwe Kiela, Candace Ross. *Winoground: Probing Vision and Language Models for Visio-Linguistic Compositionality*. CVPR 2022, 5238–5248 in the CVF open-access proceedings. [CVF record](https://openaccess.thecvf.com/content/CVPR2022/html/Thrush_Winoground_Probing_Vision_and_Language_Models_for_Visio-Linguistic_Compositionality_CVPR_2022_paper.html) | Joint matching of two images/two captions with identical word sets is an existing paired grounding evaluation. Our two atomic families do not establish comparable compositional breadth. |
| diwan2022winoground | Anuj Diwan, Layne Berry, Eunsol Choi, David Harwath, Kyle Mahowald. *Why is Winoground Hard? Investigating Failures in Visuolinguistic Compositionality*. EMNLP 2022, 2236–2250. [ACL record](https://aclanthology.org/2022.emnlp-main.143/) | Dataset failure can involve low-resolution/small objects and abilities beyond the nominal construct. This motivates explicit visual answerability and caution about attributing a control difference to OCR or internal reasoning. |
| xu2019gnn | Keyulu Xu, Weihua Hu, Jure Leskovec, Stefanie Jegelka. *How Powerful are Graph Neural Networks?* ICLR 2019. [OpenReview record](https://openreview.net/forum?id=ryGs6iA5Km) | Neighborhood-aggregation expressivity is analyzed against the Weisfeiler–Lehman test. The present cycle/triangles blind spot applies to anonymous uniform-feature 1-WL-equivalent methods; it does not cover unique-ID, positional, spectral or higher-order graph methods. |

## Metadata choices

- The Winoground IEEE Computer Society search result listed 5228–5238, whereas
  the CVF accepted-paper record lists 5238–5248. Use the CVF record consistently,
  link that record, and do not merge page ranges from different records.
- CVF's Goyal URL contains lowercase `v`; an uppercase `V` URL returned 404.
- The Gardner paper has 26 authors. The bibliography should retain the complete
  list from ACL rather than treating “et al.” as an author name.
- ICLR's record was initially posted in December 2018; cite the 2019 conference.

## Positioning to preserve in the paper

Paired evaluation, both-correct criteria, invariance testing and visual grounding
are established ideas. The bounded contribution is a versioned observation
contract that makes the selected visual referent and answer explicit, binds
both independent human judgments to the exact model-visible text and pixels,
and reconstructs family-specific adaptation statistics from real responses.
The graph audit demonstrates why controlling only node/edge counts is
insufficient; it is a small proof of concept, not a new GNN theorem or a
comprehensive graph-reasoning benchmark.
