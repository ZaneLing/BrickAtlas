# Issue 5: protocol-level positioning

Analysis version: `ldraw2-evidence-v1`.
Status: literature verification and novelty scope resolved; integration into
the revised PDF is included in Issue 1's final acceptance.

## Changes and evidence

- Read all 10/11/40 pages of the pinned BrickNet/LEGO-Puzzles/PhyBlock PDFs.
  `literature/download-manifest.json` records paper URLs and hashes.
- Inspected official schemas, prompt builders, parsers, graph types and
  evaluators at exact commits. Twenty code/document/sample files are pinned
  by `literature/official/download-manifest.json`.
- Wrote `literature/protocol-evidence.md`, covering evaluation unit, visible
  evidence, identity/repeated parts, evidence integration, sources,
  oracle/review boundaries, paired conditions, outputs and executable checks.
  Every comparison cites a paper page/section or code symbol.
- Identified version differences instead of silently merging them:
  BrickNet's released code has updated split/training/metric settings;
  LEGO-Puzzles is explicitly v3 (up to seven intermediate stages);
  the inspected PhyBlock code predates its v2 manuscript.
- Added a reproducible worked example from original OMR 42004: B0035,
  image-conditioned gold C→A under the documented label swap, unchanged source
  CAD, graph links and independent restoration action. No predictions or
  human judgments were fabricated.
- Downloaded current-year official CVPR author rules and template; recorded
  them in `literature/format-policy.md`.

## Verification

`python3 benchmark/suite/ldraw-evidence/verify-literature.py`

Result: **PASS**, 25 pinned assets (three papers, twenty implementation
artifacts, two format artifacts) and the real-source example. The verification
checks image bytes, full/mask camera/projection equality, source part types,
choice mappings, swapped labels, alternate gold, recognized edges,
restoration action and the offline request hash.

Outputs: `literature/worked-example.json`, `literature/verification.json`.
The final delivery manifest records hashes of all new code/reports; no
original v1/v2 source, result, render or paper has been replaced.

## Scientific conclusion and limits

Real LDraw, graph representation, IDs, controlled renders and interactive
planning all have relevant precedents. They are not presented as individually
new here. The contribution is the explicit same-target evidence-following
experiment, with pair-specific semantics/golds and response-aware estimands,
on unchanged original assemblies. Templates alone do not provide the bound
requests, altered-evidence golds or the joint response record.

The measured node-only 63/73 vs 0/73 both-correct contrast establishes why
ordinary graph accuracy is insufficient in this corpus. No new learned-model
or human conclusion follows from literature inspection. “Not reported”
always refers to the pinned protocol and never means “cannot be supported.”
No external baseline percentages are compared across incompatible contracts.

No additional model inference was needed. No external data-access request
or message was submitted. Issue 1 can now use verified comparisons and
properly limited resource/method claims.
