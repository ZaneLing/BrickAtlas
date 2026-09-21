# Issue 3 — evidence adaptation

Analysis version: `ldraw2-evidence-v1`.
Status: implementation and offline validation complete; model effects remain unmeasured.

The new read-only adapter validates actual wire bytes against the frozen serializer,
condition, input files, image encoder, prompt, package lock and code hashes. It parses
provider raw responses again, checks submissions against those responses, and reverses
ID renaming before semantic comparison. Distinct model revisions, adapters, datasets,
conditions, duplicate pairs and altered receipts are rejected.

Fact changes receive separate original and current-evidence golds. Wrong-image
predictions have four exhaustive categories. Both-correct, current-evidence accuracy
and the conditional adaptation denominator are explicit; zero conditional denominators
return null. Five transitions distinguish correct stability from stable errors.
Invalid repeated set members are rejected; actions retain the frozen execution
contract. Withholding and changes in observation access are separate policies.

## Files and provenance

- `benchmark/suite/ldraw-evidence/validate-run.ts`
- `benchmark/suite/ldraw-evidence/evidence_adaptation.py`
- `benchmark/suite/ldraw-evidence/test-receipts.ts`
- `benchmark/suite/ldraw-evidence/test_adaptation.py`
- `evidence-adaptation-readiness.json`
- `qa/wrong-image/validated-run.json`
- `receipt-test-fixtures.json` and `adaptation-test-report.json` (test evidence only)

All changes are new files. Frozen `scores.json`, generators and v2 data remain
unchanged. The final delivery manifest records new-file hashes.

## Actual validation

Using the pinned Node binary and `node_modules/tsx/dist/cli.mjs`:

```text
benchmark/suite/ldraw-evidence/test-receipts.ts
  benchmark/ldraw-evidence-v1/receipt-test-fixtures.json
python3 benchmark/suite/ldraw-evidence/test_adaptation.py
```

Eleven end-to-end receipt fixtures and thirteen interpretation/statistics tests pass.
They cover zero accuracy delta with both answers correct, old-answer persistence,
other legal answers, invalid output, timeout, missing B, zero conditional denominator,
set order/repetition, wrong consistency, incompatible provenance and duplicate pairs.
Parent-balanced source-cluster intervals and paired model-minus-baseline differences
are implemented for both natural accuracy and paired success.

All 140 wrong-image requests were materialized offline in the new analysis directory
and validated: 73 Color, 67 Part-type, 24 original sources, 140 distinct alternate
golds. For Color, the donor part's recorded color, displayed ID and visible operand
are checked. For Part-type, both swapped labels are checked. Actual image bytes,
dimensions and renderer metadata are bound to every record.

## Counts and limits

- Original universe: 617 items / 24 sources; no exclusion.
- Wrong-image universe: 140 pairs / 24 sources; no exclusion.
- Graph interventions: 146 pairs; deletion subset 73, retained in full.
- Actual new API calls: 0. Authentic v2 model responses available: 0.
- Visual decidability at wire resolution: pending independent review.

The readiness artifact therefore contains null model metrics, not zero scores.
The test fixtures do not constitute model results or human review. Metadata/oracle
agreement verifies answer construction, not perception or physical truth. Color
wrong images may also change shape; ID renaming changes label length/layout.
The next reporting phase can consume complete receipts without changing the original
scoring protocol. Real model claims require completing the versioned inference plan.
