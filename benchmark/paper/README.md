# BrickAtlas English Manuscript

`main.tex` is an English current-state research manuscript, not a submitted or
accepted paper. It uses the official CVPR 2026 author kit in **pagenumbers**
technical-report mode. Author/institution metadata is intentionally omitted.
There is no fabricated submission number. Future submission requires checking
the relevant year's rules, setting genuine metadata, and meeting research gates.

## Contents

- `main.tex`: abstract, motivation, related work, data, ground truth, metrics,
  auditable replay, v2 algorithmic audits and neural study, protocol diagnostics, limitations.
- `main.pdf`: nine pages; references begin on page eight.
- `supplement.tex`, `supplement.pdf`: two pages of historical pilots and implementation details.
- `references.bib`: verified core references; not an exhaustive related-work survey.
- `tables/*.tex`: tables generated from actual artifacts, not manually invented values.
- `figures/*.png`: actual benchmark renders from the largest-case-per-policy audit.
- `evidence.json`: source paths/hashes for numerical evidence and upstream template.
- `generate-tables.mjs`: table generation and evidence assertions.
- `generate-study.mjs`, `study-evidence.json`: new study tables and source hashes.

## Compile

From the repository root, regenerate tables:

```bash
node benchmark/paper/generate-tables.mjs
node benchmark/paper/generate-study.mjs
```

From `benchmark/paper/`, with a normal TeX Live installation:

```bash
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
latexmk -pdf -interaction=nonstopmode -halt-on-error supplement.tex
```

Or use Tectonic, which also runs BibTeX and reference passes:

```bash
tectonic --keep-logs --keep-intermediates main.tex
tectonic --keep-logs --keep-intermediates supplement.tex
```

Tectonic may download public TeX/font resources on first use. No API model calls
are involved. The local verified binary, when installed for this workspace, is
`benchmark/.runtime/tectonic`; it is not part of the published source.

Optional PDF inspection uses Python 3.11, PyMuPDF 1.26.4 and Pillow 11.3.0:

```bash
python check_pdf.py
python check_pdf.py --paper=supplement
```

It checks US Letter dimensions, text bounds, unresolved references and overfull
boxes, and renders pages into `.runtime/paper-inspection/` for visual inspection.

## Official Template Provenance

Upstream: https://github.com/cvpr-org/author-kit

Pinned revision: `291758547e923160eb4d37079b7b9f0dfce82355`.

`cvpr.sty` and `ieeenat_fullname.bst` are copied unchanged; authorship notices remain.
The upstream README identifies this as the official CVPR/ICCV/3DV template,
updated for CVPR 2026. The manuscript does not change margins or use negative
spacing to force a page count. Template provenance is not a claim of acceptance.

## Evidence Boundaries

V2 has 5,120 objects, 117,910 task-condition cases, and one complete public-input
algorithmic baseline plus complete height-sorted planning audits.
The new v2 study contains 674 one-shot and 56 control API calls on 24 shared
held-out objects and 25 catalog questions; it remains exploratory, not powered.
All ten planned SmolVLM jobs are complete: 3,370 predictions, 1,080 updates and
552,960 supervised answer tokens. `study-evidence.json` links their evidence.
Exact successes occur only in relation tasks; no positive edit-transfer result
was observed in the leave-edit conditions.
The 112-call two-model study, 24-call paired control, and five Qwen LoRA/base runs
belong to earlier releases and are explicitly separated.

Additional development diagnostics comprise a four-model 180-call screen,
two separately versioned 24-call reconstruction ladders, and 96 local-pose
and candidate-selection calls on four unused source groups. The main text
reports coordinate-origin confounds, copy-input baselines, output-protocol
differences and permutation sensitivity rather than a pooled leaderboard.
`tables/study-pose.tex` is generated from the frozen pose-probe evidence.
These adaptive experiments do not establish a stable model ranking or a
causal attribution of errors to perception, reasoning or output generation.

The subsequent 192-call development replication uses 12 new source groups,
four models and original/repeat/permuted/no-image conditions. Paired excess
permutation mismatch is 0.50-0.75; source-bootstrap intervals exclude zero in
this selected small sample. This is not independent population confirmation.
`tables/study-order.tex` is generated from its archived analysis. Total historical
API accounting is 1,609 calls and $3.097410574, not the size of a single study.

Independent human review, rich human-designed data, broader model baselines,
and confirmatory experiments remain outstanding.
Both local research plans remain excluded from publication. The public
`../suite/artifacts/study/governance/SUMMARY.zh-CN.md` tracks evidence gates.

Chinese companions: `../suite/study/OVERVIEW.zh-CN.md` and `../suite/study/REPORT.zh-CN.md`.
