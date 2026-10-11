# Frozen source evidence

This directory preserves the 100-candidate source registry, original intake
outcomes, official-page snapshots, and independent representation checks.
The final source/question admission decision is separate:
`../source-admission.json` and `../source-question-audit.json`.

`source-audit-handoff.json` is the source-only entry point. Its
`admissionStateIncluded` field is false. `archive-verification.json` verifies
the archived bytes, all 438 required metadata files, and all 96 original-leaf
proof hashes. The upstream `archive-requirements.json` records the state
*before* archival and is preserved unchanged; the later archive verification
records completion.

Original report paths remain unchanged to preserve their hashes. Resolve:

- `tem/research/20261010-brickplan-v23-diversity/source-intake/<path>` to
  `<path>` in this directory.
- `/tmp/brickplan-v23-work/source-intake/<path>` to `<path>` here.
- `leaf-proofs/<model>.json` to the decompressed bytes of
  `leaf-proofs/<model>.json.gz`. Compare the decompressed SHA256 with the
  handoff's `proofSha256`; compressed-byte hashes are also recorded.
- Repository-relative original models and dependency files to their unchanged
  paths under `assets-source/` and `web/public/models/`.

The source tools in `../../source-tools/` automatically use this archive when
the original local research directory is absent. The original-state registry
and archived registry must agree when both are present. The isolated checkout
test, parser tests, corruption tests, and their actual command results are
retained in the corresponding `*-test-results.json` files.

Six preliminary geometry admissions fail the subsequent whole-source gate:
five part-only manifests omit direct model geometry (`10124`, `10226`,
`10261`, `10262`, `21318`), and `30312` has conflicting original root
identification. Their files and proofs are retained without correction.
Acquisition failures and geometric exclusions also remain in the denominator;
no failed candidate was replaced.

These proofs concern source identity, representation and provenance. They do
not establish physical force balance, human answerability, or population model
performance.
