# Current BrickAtlas paper

- [Main PDF](main.pdf) and [supplement PDF](supplement.pdf): English manuscript,
  actual native task images, complete GT, condition analysis and source gallery.
- [Main source](main.tex), [supplement source](supplement.tex) and
  [verification](../tem/verification/paper/verification.json).
- [Model/table schema](experiments.json): 15 planned models, 212 genuinely blank
  result fields. Model and human collection have not occurred for this version.
- [Figure provenance](repair-figure-provenance.json): exact native PNGs, graph
  inputs, every optimal restoration, source poses and file hashes.

The primary version is [visual-repair-v1](../benchmark/visual-repair-v1/README.md):
84 constructions, 1,008 dependent observations, 17 source assemblies and 15
dependence groups. The held-out split contains 57 constructions in ten groups.
The task binds a visual candidate to a graph terminal and requires every
minimum-cost restoration. Figures show a real development construction with
multiple optima; the supplement includes all 24 original source models.

The joint analysis aligns atomic binding, oracle repair and multimodal repair
on the same observations. It retains all eight contingency counts, failure
conditional on both isolated conditions succeeding, and two paired contrasts.
Full and construction-qualified subsets retain separate denominators.
Missing calls remain in planned denominators; empty conditional estimates
remain null. Local algorithm outcomes and synthetic test fixtures are
explicitly separate from empirical model results.

## Rebuild

To compile the checked-in manuscript, run `npm run paper:build` from the
repository root. Set `TECTONIC` to select a Tectonic executable; the bundled
local runtime is used when no system executable is found. Compiler files stay
in `tem/build/paper/`; only the two final PDFs are published into `paper/`.

When deliberately updating publication inputs, use the recorded Python
environment after verifying the corresponding benchmark version:

```sh
env -u PYTHONPATH PYTHONNOUSERSITE=1 PYTHONDONTWRITEBYTECODE=1 benchmark/.runtime/mlx-env/bin/python paper/build_tables.py
env -u PYTHONPATH PYTHONNOUSERSITE=1 PYTHONDONTWRITEBYTECODE=1 benchmark/.runtime/mlx-env/bin/python paper/build_repair_assets.py
```

To check compilation without replacing the published PDFs:

```sh
python3 paper/build.py --check-only
```

From the repository root:

```sh
env -u PYTHONPATH PYTHONNOUSERSITE=1 PYTHONDONTWRITEBYTECODE=1 benchmark/.runtime/mlx-env/bin/python paper/verify.py
```

`build_tables.py --refresh-proposal` deliberately updates a changed planning
schema and refuses to overwrite measured results. The validator checks blank
cells, current GT and figure lineage, resolved citations, English-only text,
unchanged archived CVPR style and at most eight main content pages.

Historical drafts and intermediate reviews belong in
[tem/](../tem/README.md). The independent review/refinement history is in
[tem/agent-iterations/](../tem/agent-iterations/README.md).
Unused figures, old generated tables, raw captures and retired figure builders
are in [tem/paper/previous-assets/](../tem/paper/previous-assets/README.md).
The historical capture page is maintained under [web/paper/](../web/paper/),
served at the unchanged `/paper/complex-render.html` URL.
