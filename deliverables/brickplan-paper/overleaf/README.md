# BrickPlan CVPR manuscript — Overleaf source

1. In Overleaf, choose **New Project → Upload Project** and select
   `brickplan-cvpr-overleaf.zip`.
2. Set the main document to **main.tex** and the compiler to **XeLaTeX**.
3. Recompile. The main manuscript includes its references.
4. To build the separate supplement, set the main document to
   **supplement.tex** and recompile.

All local TeX inputs, bibliography/style files and actual figure files are
included. No Python runtime, dataset, server, external image download or
local filesystem path is required.

The public draft uses the unmodified official CVPR author-kit in
page-numbered preprint mode. For anonymous review, define `\reviewcopy`
before the document begins in main.tex, and update the actual conference
year and paper ID. The pinned upstream kit labels itself 2026; this is
not a claim that a later year's official kit has been verified.
Replace the draft author line before camera-ready submission.

Main document: main.tex
Supplement: supplement.tex (includes appendix.tex)
References: references.bib, ieeenat_fullname.bst
Template: cvpr.sty
Generated evidence tables: the included *.tex inputs
Figures: figures/
Asset attribution and upstream provenance: included JSON/README files

This is a snapshot of the benchmark manuscript. Edit these source files
freely in Overleaf. To regenerate a fresh upload package from the repository,
run `python benchmark/brickplan-v2.2/export_overleaf.py --check`.
The repository's exporter refreshes its own deliverables folder only;
it does not modify an existing Overleaf project.
