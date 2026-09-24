# Repository layout migration — 2026-09-24

| Canonical directory | Contents |
|---|---|
| [`paper/`](../../paper/README.md) | Current manuscript, supplement, final PDFs, required figures/TeX inputs and publication build tools |
| [`web/`](../../web/README.md) | Website source, public assets, HTML entries, frontend configuration, tests and documentation |
| [`benchmark/`](../../benchmark/DATASETS.md) | Versioned data, evaluators, native packets and reproducible study packages |
| [`tem/`](../README.md) | Reviews, previous manuscripts/assets, validation reports, build output and local working artifacts |

Shared source acquisition tools, original licensed models, the catalog config
and npm command launcher remain at the root. Existing local runtimes stay in
place because their executables contain absolute paths.

[plan.md](plan.md) records the decisions. [moves.json](moves.json) records 95
moves, original hashes, compatibility mounts and rebased archive links.
Root `src`, `public` and `assets-built` are compatibility links used by frozen
scripts. Root `vite.config.ts` delegates to `web/`; root deployment config
links allow platform discovery. Root CODEX/CVPR/debug aliases are removed.

The exact old `package.json`, `vite.ldraw-v2.config.ts` and nine
`dist-ldraw-v2/` build files are retained under `original/` because the historical baseline locks their
bytes. Current build configuration is under
`web/`. Historical publication builders in `tem/paper/previous-assets/` are
archival; the current build command is `npm run paper:build`.

The current benchmark, manuscript sources, final PDFs, figure source evidence,
and three original reviewer rounds retain their original bytes. The accepted
review remains bound to research commit
`39e92789f2b64f34dbcfc118a2feb9e4439c951b`; it is not a new acceptance decision
for this layout change. The one pre-existing uncommitted e2e report was moved
without changing its bytes and is excluded from the migration commit.

Validation artifacts:

- [validation-summary.json](validation-summary.json): 94 frontend tests,
  56 repair tests, three existing browser tests, five route checks, both
  frontend builds and both manuscript compilations.
- [layout-verification.json](layout-verification.json): file hashes, explicit
  path edits, publication protection, unchanged study packages and links.
- [browser-verification.json](browser-verification.json): homepage, interactive
  numbered source model, historical native canvas, blind qualification queue
  and native packet/PNG, historical source renderer.
- [archived-review-verification.json](archived-review-verification.json):
  exact accepted Git snapshot, separately from the current workspace.
- [archive-index-verification.json](archive-index-verification.json):
  historical baseline and archive bytes checked against the staged Git index.
- [paper verification](../verification/paper/verification.json): publication
  provenance, 212 null result fields, ground truth and document checks.

Verification commands from the repository root:

```sh
npm test
npm run build
npm run build:ldraw-v2
npm run test:e2e -- web/tests/e2e/benchmark-review.spec.ts --project=desktop-chrome
python3 paper/build.py --check-only
python3 tem/repository-layout-20260924/verify.py
python3 scripts/organize-research.py --verify
python3 scripts/verify-research-sync.py
python3 tem/agent-iterations/audit.py --require-accept --archived-commit 39e92789f2b64f34dbcfc118a2feb9e4439c951b
```

Python research checks use the environment documented in `plan.md`.
`migrate.py` is a one-shot provenance record and refuses to run again.
Build logs and browser attachments stay under ignored `tem/build/` and
`tem/verification/` subdirectories. No dataset regeneration or model/human
collection is part of this migration.
