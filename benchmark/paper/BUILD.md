# Hierarchy-2 Verified Build

- Compiler: Tectonic 0.17.0, macOS aarch64.
- Official compiler archive SHA256:
  `a3f1cac7c5678f01661a92212f58480ae3b0634115d880dbc59e2953ded45667`.
- Official CVPR author-kit revision: `291758547e923160eb4d37079b7b9f0dfce82355`.
- Template files are unchanged; report mode includes page numbers.
- Main: five content pages plus one reference page, US Letter.
- Supplement: 43 pages, including four website renders and 35 task entries
  for each of all 40 objects.
- PDF checks: no undefined references, overfull boxes, page-boundary text
  violations, or empty pages.
- Figures use actual original-site canvas renders and archived pilot results.
- Dataset: 40 layouts, 5,070 parts, 355 modules, 318 joints, 1,400 tasks.
- Quality boundary: 17/40 layouts pass the declared nominal-drift threshold.
  The complete library is not certified as physically stable or LEGO compatible.
- Pilot: GPT-4.1 mini, 14/16, $0.0113044. All 16 receipts are archived;
  one response per cell does not establish population accuracy.
- Website: all 40 models pass load/orbit/explosion/assembly-replay checks;
  four mobile cases pass rendering and overflow checks.
- Regression: 212 benchmark tests and 69 original-site unit tests pass.
  Both TypeScript projects and the production Vite build pass.
- `verify-hierarchy2.mjs` binds the release manifest, run, paper, and
  original-site model/document copies.
- `verify-artifacts.mjs` also preserves checks on older versioned evidence.

Reproduction commands are in `../hierarchy-v2/README.md`.
The source ZIP includes current TeX, generated tables and figures. Regeneration
requires the full repository; the ZIP is a manuscript source package.

The previous Mechanism-1 manuscript is retained in Git at commit `865b583`.
Historical data and source generators remain versioned separately. They are
not counted in Hierarchy-2's 1,400 questions or 16-response pilot.

Paper hashes are recorded in `pdf-verification.json` and
`supplement-verification.json`. The page limit and software checks do not
establish submission readiness, human difficulty, or independent replication.
