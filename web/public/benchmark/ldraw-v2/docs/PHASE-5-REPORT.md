# Phase 5 report

Status: automated publication, synchronization, browser and preservation
gates passed. Independent human adjudication and model experiments are pending.

## Manuscript rewrite checklist

| Requirement | Delivered and checked |
|---|---|
| Title, abstract and contributions | Instance-grounded modular evaluation; no validated diagnostic or integration claim |
| Related work | Research question / observation contract / evidence table; diagnostic vs capability distinction |
| Unsupported external capabilities | Explicitly "to verify"; no negative capability claims inferred from missing evidence |
| Complete task decomposition | All 11 families with count, layer, observation, measurement, necessary input and shortcut control |
| Elementary and constant controls | Evidence controls marked; both evidence-limit and the six-step program marked constant |
| Integrative label | Replaced by graph-internal in v2 data, manuscript and review UI |
| Descriptive analysis | Generated size-band/modality table, source-qualified answer concentration and operand reuse |
| Ablation interpretation | Paired family-first source-macro/micro deltas; clustered intervals; no equivalence inference from zero-containing intervals |
| Missing cross-module chaining | Explicit in abstract, tasks, protocol and limitations |
| Experiment tables | 14 conditions; 9 prospective tables with 264 blank/null result cells |
| Complete appendix | All 617 IDs, English prompts, options, reference outputs, operand mappings, derivations and equivalence statements |

`main-v2.pdf` is 6 pages including references. `supplement-v2.pdf` is 181 pages.
Both compile with the retained Tectonic toolchain. Automated inspection checks
every PDF page for CJK, unresolved references, overfull boxes and text outside
the page. Every embedded raster is bound to the actual source-geometry image
or its recorded print derivative. Main pages and representative supplement
pages were also visually inspected by the agent; this is not independent
human acceptance.

## Figures and publication artifacts

- Source montage, six-state original-pose replay and full/mask/crop plate.
- New vector answer-concentration figure for all eleven families, with CSV.
- Supplement: accepted/rejected restoration and 24 original-source plates.
- New `figures-v2/`, `tables-v2/`, `references-v2.bib`, `BUILD-v2.md`.
- `publication.py` generates every numeric table and complete question index.
- `publication-manifest.json` binds generator, inputs, outputs and render copies.
- `verify-publication.py` checks data/contracts/counts/options/answers, blank
  results, shared scoring, source hashes, PDF geometry and image provenance.
- Source archive and website document copies are produced by
  `package-publication.py`; compile-time dependencies are checked.

All seven cited URLs have verified content. Six were retrieved directly by
urllib. The OpenReview URL redirected that client to a challenge; a separate
read-only WebFetch returned the actual title, authors and abstract. Both the
challenge and alternate content evidence are recorded. This is high-level
topic verification, not a completed full-text capability comparison.

## Review website

New standalone entry: `ldraw-v2.html`. Protected v1 routes are unchanged.
The v2 production build uses `vite.ldraw-v2.config.ts`, with a read-only static
server combining `dist-ldraw-v2` and the repository's original public assets.

The UI supports the original geometry, camera rotation/zoom/view controls,
single-instance and operand isolation, expansion, author STEP playback,
legal/illegal action replay and exact integer scoring. The CLI and UI import
the same v2 scoring function. New runner manifests hash the shared scorer,
legacy action engine and independent oracle as well as request/transport code.

The review index has 1,190 addressable units: 617 tasks plus 573 source-local
pairs. Required review is 251 tasks (140 visual plus 111 other flags) and all
573 pairs, totaling 824 units. The UI displays recorded progress, not a
certified-pass rate. Every record requires reviewer, rationale and timestamp.
Source, version, content hash and operands are validated on import. Separate
reviewers remain separate; conflicting edits from the same reviewer cannot
silently overwrite one another.

Production-browser verification passed:

- 24/24 sources loaded their full 15,334 instances.
- Integer scoring accepts the reference and rejects non-integer outputs.
- Isolation, explosion, camera changes and zoom operate on source geometry.
- Restoration shows 128 initial, 129 restored and 128 after rejected action.
- Six-step execution, source replay and pair isolation work.
- Twelve feedback validation scenarios, local persistence and JSON
  export/undo/import round trip pass in a temporary browser context.
- All five displayed visual conditions load their original pixels.
- Desktop and 390-pixel mobile layouts have no horizontal overflow.
- No browser page errors were observed.

No real human decisions were created by these tests.

## Commands and evidence

See `benchmark/paper/BUILD-v2.md` for full commands and environment.
Executed: publication generator; reference verifier; both Tectonic builds;
publication verification; TypeScript check; v2 production Vite build; UI
verification against port 5175; full `ldraw:verify`; experiment verification;
fresh 14-condition offline runner canaries; v1 freeze verification.

Evidence files:
`publication-verification.json`, `ui-verification.json`,
`reference-verification.json`, `phase-5-publication-checks.txt`,
`phase-5-ui.txt`, `phase-5-typecheck.txt`, `phase-5-runner.txt`,
`phase-5-preservation.txt`, `paper-inspection/`, `ui-captures/`.

The independent oracle still passes 617/617, public-action solver 75/75,
negative controls 5,154/5,154. Experiment checks still cover 3,147 requests,
146 answer-changing graph interventions, 576 ID round trips and 907 image
hashes. All 2,131 protected v1 hashes remain unchanged.

## Failures corrected and limits retained

- Browser testing initially requested an absent Playwright bundled browser;
  it now uses the installed Chrome channel, matching the existing renderer.
- A test initially assumed the standard visual PNGs were 1280 pixels wide.
  Original v1-derived standard PNGs can be 2760 pixels wide; the test now reads
  each source PNG's true dimensions. Actual API images are separately resized
  by the existing adapter. Original image bytes were not altered.
- The first publication-verifier attempt preceded completion of the updated
  reference report. It was rerun after the dependency completed and passed.
- Harmless underfull paragraph warnings in long adapter/table text remain;
  there are no overfull boxes or clipped text.
- No model inference/training, independent human pass rate, physical
  certification or diagnostic-localization result is claimed.
