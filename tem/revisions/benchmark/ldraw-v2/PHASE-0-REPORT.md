# Phase 0 report

Status: automated preservation and isolation gates passed.

Added `freeze.py`, `VERSION.md`, `v1-frozen-manifest.json`, source references,
copied generator/scorer, historical-result backup and runtime inspection logs.
The manifest protects 2,131 existing files, including 24 model inputs and 24
internal scoring bundles, original sources, implementation and publications.
Runtime lock inspection found no active experiment writer.

Commands and evidence:

- `python3 benchmark/suite/ldraw-v2/freeze.py --verify`: 2,131 unchanged files.
- Unchanged `npm run --prefix benchmark ldraw:build` in a disposable copy:
  75 generated site files equal frozen bytes (`phase-0-v1-build.txt`).
- Independent source reparse: 24 sources, 15,334 instances, 617 tasks,
  1,606 negative controls and 75 public-action solves
  (`source-reparse-verification.json`, `phase-0-v1-verify.txt`).

Legacy build prerequisites: archived candidate manifests and cwd-relative
`assets-source` links were supplied only in the disposable copy. No v1 file was
patched. Historical results were backed up, not relabeled as v2 evidence.
No preservation failures remain. These are agent checks, not human approval.
