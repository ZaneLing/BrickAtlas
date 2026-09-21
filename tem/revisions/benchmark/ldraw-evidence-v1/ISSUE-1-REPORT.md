# Issue 1 — research-centered manuscript and final integration

Analysis version: `ldraw2-evidence-v1`.
Status: code/data/manuscript integration accepted within the guide's
method/resource scope. Learned-model and human evidence remain unavailable.

## Concrete changes

The new manuscript is `benchmark/paper/evidence-v1/main.tex`, with its own
supplement, bibliography, unchanged official CVPR style, generated tables and
vector figures. Original v2 manuscripts remain byte-identical.

The introduction now starts with a positive, falsifiable visual question:
answers about the same identified part should correctly follow changed
evidence and remain correct under specified semantic invariances.
Background/view access and graph evidence beyond priors are the two supporting
questions. Source lookups, graph operations and display edits remain separate
contracts; no within-item multimodal chain is invented.

The manuscript is supported by measured algorithmic evidence: node-only
63/73, micro 86.30%, source macro 83.75% [72.92, 93.12], but zero both-correct
on the 73 natural/intervened pairs; graph algorithms are both-correct on all
pairs. The known prior and its reanalysis are explicitly post-hoc. The visual
experiment is a research protocol, not a reported finding.

Four figures now have standard captions, panel labels and cross-references:

1. OMR 42004 B0035 linked to real pixels, its record, recognized graph and an
   independent visibility action.
2. Six actual LDraw frames labeled as given-order visibility replay.
3. Separate panels and scales for global semantic priors and source-scoped
   exact-answer repetition.
4. Full/Mask/Crop context plus enlarged details; Full/Mask use the same pixel
   rectangle. Extra boxes/zooms are paper-only and never alter model inputs.

The supplement contains verified protocol-level literature evidence, raw
binding/scoring rules, all reporting groups, all node-only failures, per-source
counts and the verbatim complete 617-question original dossier.

## Generation and verification

- `benchmark/suite/ldraw-evidence/publication.py` generates 34 numeric macros,
  role tables, graph failure/source tables and five figures (four main and one
  supplement). Every input and paper crop is recorded in `asset-provenance.json`.
- `verify-publication.py --render` passes on all 8 main-paper and 182 supplement
  pages. Main text occupies 7 pages; references begin on page 8. Every original
  task appears once as a dossier heading. Fonts are embedded, pages are US
  Letter, and no Chinese, private machine path, missing reference, missing
  glyph or overfull box appears in the PDFs.
- The official current-year CVPR 2026 baseline is documented and used unchanged
  in anonymous review mode with a nonregistered draft ID. This is not a claim
  of an actual submission or acceptance.
- Main pages were inspected individually; every supplement page was inspected
  in the 16 contact sheets, with per-page text/font/bounds checks.
  `visual-inspection.json` binds that review to the final PDF hashes.
- `package-release.py` generates a standalone, deterministic paper source ZIP.
  Fresh extraction compilation reproduces both documents' page counts and
  every page's extracted text.
- The local `/evidence-v1.html` page links the paper, complete appendix,
  source ZIP, measured graph audit, exact-wire review and preserved 3D viewer.
  HTTP retrieval of every principal artifact succeeds.

The exact-wire review adds a visible, copyable JSON preview on export.
Browser checks confirm 1280×800 native display, navigation from item 1 to 2,
140 exported observations, zero reviewed judgments, a prepared download Blob,
and byte-equivalent structured content to the pending QA template.
OS-level download persistence is not claimed; the visible JSON fallback is
verified. The updated review export lives separately under
`qa/wrong-image-export-v1/`; old exports remain preserved.

## Final code/data checks

The 13 adaptation tests, 11 raw-receipt fixtures and all-family
receipt-to-publication chain pass. Null and numeric table states, tampering
rejection, missing-response denominators, exact-wire QA, isolated TypeScript
compilation, 219-observation dual-oracle challenge and 25 pinned literature
assets pass. The publication-chain fixture is a CLI helper invoked by
`test-receipts.ts`; attempting generic unittest discovery was an incorrect
invocation, corrected using the documented entry points.

No original task, source, gold or score is excluded or overwritten.
New model requests remain offline captures with zero inference calls.
The final preservation check covers 2,616 v2 entries, 2,131 v1 files and the
original content archive. New-file hashes are sealed in `delivery-manifest.json`.

## Acceptance boundaries

All five guide issues have concrete implemented and reviewable resolutions.
The revision materially improves the research question, estimands, controls,
reporting and literature argument. It does not close the unrun visual model
study, certify all original physical connections or establish broad
diagnostic validity. Pending human work remains 140 visual items, 111 other
flagged items and 573 physical candidates. No result is fabricated to conceal
those limits.
