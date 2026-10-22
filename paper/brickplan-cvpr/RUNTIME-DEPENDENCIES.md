# Reproducing this paper snapshot

## Compile the documents

The Overleaf ZIP is self-contained for LaTeX compilation: select `main.tex` or
`supplement.tex`. It includes the official style, bibliography style, BibTeX
entries, fifteen figure PDFs, the complete static inventory, and all generated `tables/*.tex`. Compiling these sources does not require the
geometry engine or any model API.

For the repository build, install Tectonic and the Python packages in
`requirements-paper.txt`, then run `python paper/brickplan-cvpr/build.py`.
This additionally verifies the recorded benchmark evidence and source hashes.
The existing project environment is `benchmark/.runtime/mlx-env/bin/python`.
The `--skip-verification` option supports compile-only use; it does not certify
the benchmark data.

## Execute the study or render the scenes again

`build.py --study --refresh-figures` also requires:

- BrickNet Python package 0.1.0, including its bundled connector catalog.
- MeshLib 3.1.4.297; the geometry module imports `meshlib.mrmeshpy`.
- NumPy, Pillow, and Matplotlib versions recorded in `requirements-paper.txt`.
- A C compiler (`cc`), which builds `benchmark/brickplan-repair/eval/raster.c`
  into a local shared library. That binary is not versioned.
- BrickNet's inset collision meshes under `$BRICKNET_DATA/inset/`. The project's
  default is `benchmark/.runtime/bricknet-data/inset`, a local link to the
  separately installed collision resources. The runtime directory is not
  bundled with the paper or checked into Git.
- The repository's pinned LDraw part library at
  `assets-source/ldraw-library/locked/`, original source models, and model
  manifests. Source author headers and license metadata are retained.
- The community certificates/manuals/cases, static plate5 bank and its 160
  referenced static-held4 qualification files, plus the dynamic-v6 audit files.
  These paper dependencies are included in this synchronization.

`evidence/runtime-snapshot.json` records installed package versions, relevant
package/catalog hashes, and the collision meshes needed by all S/D/M paper examples
and the community study. It does not redistribute third-party binaries. A fresh
machine must install those upstream resources before rerunning geometry; merely
cloning the repository is sufficient for compiling the supplied figures, but
not for recreating the geometry environment.

## Evidence boundaries

`protocol_study.py` executes the two selected legal routes per object. Its
96 route/condition rows contain a blind replay and a privileged recovery replay.
These are scripted executor diagnostics, not learned-model evaluation.
`verify.py` checks source hashes and the existing full-bank audit results; it
does not rerun all 3,292 + 1,872 geometry cases on every PDF compilation.

The historical pilot summary contains aggregate measurements and source trace
hashes. Raw provider logs and identifiable reviewer records are not bundled.
No new paid API request was made for this paper rewrite.

`prepare_revision.py` regenerates the full model inventory, corrected plate5 source
splits, planned case manifest, participant schedules, and empty results template.
Run it only while preparing the design; it intentionally resets the unmeasured
result template. Collected results should be saved in a separate run artifact.

`prepare_case_figures.py` optionally rebuilds the sanitized qualitative export from
local archived v5 API traces. Those raw logs are not distributed. Normal figure
regeneration reads the bundled `evidence/repair-comparison.json`, which contains
the original certificate, verified state/action records, and source hashes, but
no provider response text. No new API request is needed. The two radar figures
read `evidence/results-template.json`; all current estimates are null and no
model series is drawn. `evidence/radar-spec.json` records their axis definitions.

`evidence/model-roster.json` lists twelve official-documentation-checked candidates.
It does not verify account access or served revisions. `expand_experiments.py`,
called by `prepare_revision.py`, generates fourteen unmeasured result tables and
the model roster table. The paired API runner, perception probe adapter,
observation/strategy variants, and cross-model recovery state bank remain planned.
No source file in this paper build invokes a model API.
