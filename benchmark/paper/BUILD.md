# Hierarchy-3 Expanded Publication Build

- Compiler: Tectonic 0.17.0, macOS aarch64.
- CVPR author-kit revision: `291758547e923160eb4d37079b7b9f0dfce82355`.
- Template files are unchanged; report mode includes page numbers.
- Main: eight pages including references; substantive content ends on page 7.
- Supplement: 152 pages, including four views and 48 task entries for all
  144 configurations, plus complete worked dismantling/repair examples.
- Main figures: actual 3D model gallery, six-action dismantling, seven-action
  service repair. English labels only.
- Tables: related settings, structural coverage, crossed task design,
  constant/uniform choice controls, historical pilot; additional appendix
  contracts, per-step mappings, physical measurements, and family diagnostics.
- PDF checks: no CJK text, undefined references, overfull boxes, out-of-page
  text, or empty pages. Embedded rasters match English plates or raw views.
- Data: 144 configurations, 143 geometric fingerprints, 42,617 primitives,
  2,040 modules, 1,938 joints, 6,912 tasks, 576 canonical views.
- All 144 configurations pass the declared nominal-state protocol. This
  does not certify passive stability, commercial connectors, or robot paths.
- Historical base-48 pilot: GPT-4.1 mini, 7/16, $0.013621. No new paid calls.
- All 212 benchmark tests pass. Publication changes do not change task data,
  the application, the scorer, or existing human-review decisions.
- `verify-hierarchy-expanded.mjs` checks current data, source-image hashes,
  analysis tables, pilot, PDF checks, and website document parity.
- `verify-artifacts.mjs` also preserves older versioned evidence checks.

Reproduction commands are in `README.md` and the English supplement.
The source ZIP contains the current manuscript and its generated dependencies;
it is not a standalone benchmark dataset. Recomputing analysis or browser
captures requires the full repository. Archived frames suffice for composition.

Paper hashes are recorded in `pdf-verification.json` and
`supplement-verification.json`. Passing software and page-layout checks does
not establish submission readiness, human difficulty, or independent replication.
