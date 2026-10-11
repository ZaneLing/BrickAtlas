# V23 Source Construction And Audit Tools

## Scope

Durable copies of the frozen source-intake tools and independent original-MPD
audits. Run from the repository root with the existing Node 22, tsx, Three.js
0.180.0, and Python 3 environment. No package installation is required.

The registered state remains at
`tem/research/20261010-brickplan-v23-diversity/source-intake`.
Its frozen registry SHA256 is
`3518c3357872225b0425ee6bcd2a0aa8350aca0791d7b83dd056d5baec081f0b`.
Never refreeze, replace failed candidates, or change original source bytes.
The main pipeline archives the registered registry and result records.

All eight state-consuming entry points use `source-state.mjs` or
`source_state.py`. When the registered directory is absent, they resolve
`benchmark/brickplan-v2.3/data/source-intake` instead. An existing but incomplete
registered directory is not silently mixed with archive files. This is a
runtime lookup fallback only: frozen paths, registry bytes, hashes, original
source records and failure outcomes are unchanged. `source-state.d.mts` supplies
the shared Node helper's TypeScript declarations.

New audit reports and intermediate artifacts default to
`/tmp/brickplan-v23-work/source-intake`.
Set `SOURCE_INTAKE_OUTPUT` to change the audit output directory.
Intake result records remain at the registered `results/` path, so the main
supervisor can consume them without changing the frozen source plan. A clean
checkout reads the archived `results/` instead; audit outputs still go to the
separate output directory, not the archive.

## Tools

| Tool | Purpose |
| --- | --- |
| `discover.py` | Official HTML snapshots, metadata extraction, original frozen selection workflow |
| `intake.ts` | Exclusive-create original assets, dependencies, manifests and final candidate records |
| `verify-hierarchy.ts` | Independent Three.js original-MPD hierarchy check, legacy-compatible report schema |
| `verify-leaves.mjs` | Strict source-address to leaf-ID proof, independent scalar arithmetic, exact part/color/pose inventory and packed-MPD check |
| `verify-identities.py` | Reparse official snapshots and verify root headers, manifest/site metadata and attribution evidence |
| `summarize.ts` | Full census, license/dependency hashes, protected historical files and source-profile duplicate checks |
| `audit-handoff.mjs` | Hash-bound source-only integration manifest and complete candidate report |
| `test-intake.ts` | Sixteen isolated parser, transform and exclusive-write tests |
| `test-leaf-proof.mjs` | Fourteen tests based on an actual source leaf and deliberate in-memory corruptions |
| `test-source-state.mjs` | Strict TypeScript compile, archive inventory, gzip raw-hash checks and isolated no-`tem` integration tests |
| `source-state.mjs`, `source_state.py` | Consistent legacy-first, archive-second state lookup |
| `download-ranges.py` | Bounded official-source range recovery, strong ETag and contiguous range validation |

The range recovery tool is retained for reproducibility. Do not retry excluded
candidate `21323` in this frozen run: bounded acquisition has concluded.

## Offline Reproduction

These commands do not download successful originals or run benchmark admission.
The summary uses exclusive-create writes: rerun against an empty audit output
directory, or verify the unchanged existing outputs.

```sh
.tools/node-v22.23.2-darwin-arm64/bin/node --import tsx benchmark/brickplan-v2.3/source-tools/test-intake.ts
.tools/node-v22.23.2-darwin-arm64/bin/node --import tsx benchmark/brickplan-v2.3/source-tools/verify-hierarchy.ts
.tools/node-v22.23.2-darwin-arm64/bin/node benchmark/brickplan-v2.3/source-tools/verify-leaves.mjs
PYTHONDONTWRITEBYTECODE=1 python3 benchmark/brickplan-v2.3/source-tools/verify-identities.py
.tools/node-v22.23.2-darwin-arm64/bin/node --import tsx benchmark/brickplan-v2.3/source-tools/summarize.ts --label=final
.tools/node-v22.23.2-darwin-arm64/bin/node benchmark/brickplan-v2.3/source-tools/test-leaf-proof.mjs
```

`audit-handoff.mjs` additionally consumes the recovery run's
`protected-byte-verification.json`, which binds the original 7,678-file baseline.
That historical recovery evidence is archived, not regenerated from a later
checkout. `summarize.ts` independently checks the historical manifest hashes,
protected tracked source files and all newly introduced locked dependencies.

Strict source-tool compilation uses the repository's Bundler resolution:

```sh
.tools/node-v22.23.2-darwin-arm64/bin/node node_modules/typescript/bin/tsc --noEmit --strict --skipLibCheck --module ESNext --moduleResolution Bundler --target ES2022 --allowImportingTsExtensions --resolveJsonModule --esModuleInterop benchmark/brickplan-v2.3/source-tools/intake.ts benchmark/brickplan-v2.3/source-tools/summarize.ts benchmark/brickplan-v2.3/source-tools/verify-hierarchy.ts benchmark/brickplan-v2.3/source-tools/test-intake.ts
```

After the audit outputs above are available, run the archive integration test
and refresh the source-only handoff:

```sh
.tools/node-v22.23.2-darwin-arm64/bin/node benchmark/brickplan-v2.3/source-tools/test-source-state.mjs
.tools/node-v22.23.2-darwin-arm64/bin/node benchmark/brickplan-v2.3/source-tools/audit-handoff.mjs
```

The test stages byte-identical metadata in a temporary checkout without `tem/`;
it never hides, moves or edits live state. Python identity replay forbids
network calls. Its fixture pass is separate from `archiveReady`, which reports
whether the real archive already contains every required input.

## Clean-Checkout Inputs

Under `benchmark/brickplan-v2.3/data/source-intake`, the frozen audit needs these
438 exact-byte state files, including records for excluded candidates:

| Relative path | Count | Required evidence |
| --- | ---: | --- |
| `candidate-registry.frozen.json` | 1 | Unmodified frozen candidate registry |
| `candidate-registry.frozen.sha256` | 1 | Original digest sidecar consumed by intake and summary |
| `results/v23-<kit>.json` | 100 | Final intake outcomes, including all four failures |
| `details/<kit>.json` | 100 | Saved official model choices, page hashes and author/completeness fields |
| `snapshots/index-<page>.html` | 18 | Frozen candidate index pages |
| `snapshots/index-<page>.fetch.json` | 18 | Index URL, retrieval timestamp, byte count and digest |
| `snapshots/set-<token>.html` | 100 | Original official set-detail pages |
| `snapshots/set-<token>.fetch.json` | 100 | Detail URL, retrieval timestamp, byte count and digest |

Index pages are `01` through `14`, plus `18`, `41`, `42`, `44`.
Each set token is the final path segment of the frozen candidate's `sourceUrl`;
it is not the kit number. Every kit in the registry needs its detail record.
`archive-requirements.json` enumerates all 438 source/archive paths, raw SHA256
digests and missing entries. Never regenerate HTML or fetch timestamps to fill
an archive gap. Additional `index/*.json` and `selection.json` are useful
discovery-history records, but are not inputs to the frozen audit replay;
`discover.py freeze` must not be rerun.

Keep the original assets and dependency closure at their recorded repository
paths: `assets-source/brickplan-v23/`, locked LDraw files and license documents,
the locked library archive referenced by `assets-source/provenance.json`,
and all referenced historical/new `web/public/models/` artifacts. These are
separate from the 438 state files. Historical recovery/protected-byte reports
must be retained: a later checkout cannot reconstruct the original untracked
file baseline merely by rerunning `git ls-files`.

The 96 archived `leaf-proofs/<id>.json.gz` files preserve raw JSON bytes.
The handoff's `proofSha256` hashes the decompressed JSON, not the gzip stream.
For unchanged report replay, materialize those bytes at
`SOURCE_INTAKE_OUTPUT/leaf-proofs/<id>.json`, or regenerate proofs using
`verify-leaves.mjs` and compare the raw hashes. The integration test verifies
every gzip/raw pair before using it. Historical absolute paths describe the
original run; path relocation must not be implemented by editing archived
report bytes or replacing their recorded hashes.

## Results Integration Contract

The main pipeline owns durable result archiving and all benchmark data changes.
Archive these final outputs together, retaining their SHA256 relationships:

- `source-audit-handoff.json`, the entry point and all-100-candidate census.
- `leaf-proofs/<id>.json`, complete original reference chains and per-leaf matrices.
- `identity-verification.json`, all official URLs, snapshot hashes, actual author
  and license headers, manifest metadata checks and explicit conflicts.
- `summary-final.json`, `dependency-lock-final.json`, `full-source-verification.json`.
- `hierarchy-checks/`, `unit-test-results.json`, `leaf-proof-test-results.json`.
- `protected-byte-verification.json` and the matching `recovery-baseline.json`.
- `archive-requirements.json` and `source-state-test-results.json`.
- Failed-transfer logs and `ranges/v23-21323/`, if preserving acquisition evidence.

`source-audit-handoff.json` is schema `brickplan-source-audit-handoff/1.0`.
Each candidate record contains its original and manifest hashes, detailed proof
path/hash and source identity evidence. `admissionStateIncluded` is `false`:
there are no main-admission counts, statuses, paths or hashes. The generator
does not read admission records, so main-owned corrections cannot stale this
source evidence. Previous handoff revisions are retained in `handoff-history/`.
Its absolute report paths describe this run; an archive resolver may relocate
those paths but must verify the same artifact bytes. Never rewrite hashes to
make an inconsistent report pass.

| Relative artifact path | Schema |
| --- | --- |
| `source-audit-handoff.json` | `brickplan-source-audit-handoff/1.0` |
| `leaf-proofs/<id>.json` | `brickplan-original-hierarchy-leaf-proof/1.0` |
| `identity-verification.json` | `brickplan-source-identity-verification/1.0` |
| `summary-final.json` | `brickplan-v23-source-intake-summary/1.0` |
| `full-source-verification.json` | Legacy unversioned census: `candidateRegistrySha256`, `denominator`, `statuses`, `candidates` |
| `dependency-lock-final.json` | Array of per-file path, SHA256, author, license and origin records |
| `archive-requirements.json` | `brickplan-source-archive-requirements/1.0` |
| `source-state-test-results.json` | `brickplan-source-state-test/1.0` |

For a whole-source fidelity gate require:

1. `intakeStatus == "manifest-ready"`.
2. `ordinaryLeafStatus == "pass"` and `packedHierarchyStatus == "pass"`.
3. `fullHierarchyStatus == "pass"`.
4. `sourceIdentity.status == "pass"` and
   `sourceIdentity.manifestMetadataStatus == "pass"`.
5. Manifest/original/dependency hashes match the admitted source, with no
   unresolved locked-path conflict.

The convenient `sourceFidelityGatePass` field implements those source checks.
The main-owned fail-closed gate must reject missing rows/evidence, hash
mismatches, unknown statuses and any value other than explicit pass. Apply it
before fresh qualification, cached-positive reuse and final aggregation; a
previous geometry admission must not bypass source fidelity. Preserve previous
geometry admission evidence separately from the final taskbank exclusion.
Main-owned subassembly policy must not relabel full-source failures as passes.
For a selected subassembly, bind each `includedSourceIndices` entry to the
corresponding proof leaf's `index`, exact `instanceId`, part, color and original
matrix; preserve the distinct whole-source gate result.

Author strings remain unchanged. `authorHeaderMatchesPage == false` is not
automatically unexplained attribution: normalized display-name variants and an
original author versus a named MPD history contributor have separate evidence.
Use the hash-bound `authorAttributionEvidence` and actual history, never a
blanket override or a modified author header.

## Known Findings

- `6912` and `31153`: recorded official download 404 failures.
- `10252`: original dependency lacks an author; excluded without header repair.
- `21323`: bounded full-file and range-transfer failures; acquisition exclusion,
  not a claim that the published model is defective.
- `10124`, `10226`, `10261`, `10262`, `21318`: ordinary leaves match, but direct
  model geometry is omitted from the part-only manifests. Full hierarchy fails.
- `30312`: official catalog and URL identify 30312, while the original root
  says `30212 - Demolition Driller.ldr`; child sections identify 30312. The
  conflict remains explicit and original bytes are unchanged.

These checks establish source representation and publication evidence only.
They do not certify physical connections, collision freedom, LEGO endorsement,
independent author identity, retail-set inventory completeness, or benchmark
question correctness.
