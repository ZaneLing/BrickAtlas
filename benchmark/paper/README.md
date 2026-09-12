# BrickAtlas English Manuscript

`main.tex` is an English current-state research manuscript, not a submitted or
accepted paper. It uses the official CVPR 2026 author kit in **pagenumbers**
technical-report mode. Author/institution metadata is intentionally omitted.
There is no fabricated submission number. Future submission requires checking
the relevant year's rules, setting genuine metadata, and meeting research gates.

## Contents

- `main.tex`: abstract, motivation, related work, data, ground truth, metrics,
  auditable replay, complete v2 algorithmic results, earlier neural pilots, limitations.
- `main.pdf`: compiled readable manuscript.
- `references.bib`: verified core references; not an exhaustive related-work survey.
- `tables/*.tex`: tables generated from actual artifacts, not manually invented values.
- `figures/*.png`: actual benchmark renders from the largest-case-per-policy audit.
- `evidence.json`: source paths/hashes for numerical evidence and upstream template.
- `generate-tables.mjs`: table generation and evidence assertions.

## Compile

From the repository root, regenerate tables:

```bash
node benchmark/paper/generate-tables.mjs
```

From `benchmark/paper/`, with a normal TeX Live installation:

```bash
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
```

Or use Tectonic, which also runs BibTeX and reference passes:

```bash
tectonic --keep-logs --keep-intermediates main.tex
```

Tectonic may download public TeX/font resources on first use. No API model calls
are involved. The local verified binary, when installed for this workspace, is
`benchmark/.runtime/tectonic`; it is not part of the published source.

Optional PDF inspection uses Python 3.11, PyMuPDF 1.26.4 and Pillow 11.3.0:

```bash
python check_pdf.py
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
algorithmic baseline. **No large neural study has been run on v2.**
The 112-call two-model study, 24-call paired control, and five Qwen LoRA/base runs
belong to earlier releases and are explicitly separated.

Independent human review, rich human-designed data, broader model baselines,
matched-token multi-task training and confirmatory experiments are outstanding.
The original local `RESEARCH_ROADMAP.md` remains excluded from publication.

Chinese companion: `../suite/v2/REPORT.zh-CN.md`.
