# Issue 4 — report roles and traceable publication

Analysis version: `ldraw2-evidence-v1`.
Status: reporting implementation and end-to-end validation complete; model/human
numeric results remain unavailable.

The four disjoint roles are recomputed from the frozen task manifest:

| Report role | Families | Items |
|---|---|---:|
| Core visual | Color 73; Part-type 67 | 140 |
| Structural evidence | Neighbors 73; Graph deletion 73 | 146 |
| Nonconstant controls | Distance 73; Interface 87; Coverage 17; Step lookup 55; Restoration 58 | 290 |
| Constant controls | Evidence limit 24; Step sequence 17 | 41 |

Their union is all 617 tasks. Family estimates average only sources containing that
family and report both item and source denominators. No task is deleted, no composite
weight is invented, and constant controls cannot decide a primary capability ranking.
The combined score is explicitly named `all_task_descriptive`.

## Files and operation

- `report-selection.json`: selected dataset, original plan hash, families and conditions.
- `results-index.json`: 84 planned model/condition entries, all currently `not-run`.
- `benchmark/suite/ldraw-evidence/reporting.py`: registration, validation and TeX generation.
- `generated/`: four role tables, visual/structural paired tables, graph baselines,
  all-task descriptive table, per-source coverage and provenance.
- `benchmark/suite/ldraw-evidence/wire_qa.py`: exact-input review export and QA validation.
- `qa/wrong-image/review.html`: blinded, native-resolution review of 140 actual
  offline wire observations; JSON feedback export.
- `publication-test-report.json`, `wire-qa-test-report.json`: synthetic tests only.

All files are new; old publication scripts and their null-only assertions remain
frozen as historical v2 artifacts. The new revision uses this state-driven publisher.
Run registration writes a **new** index path, never overwrites an existing result:

```text
python3 benchmark/suite/ldraw-evidence/reporting.py register \
  --run NEW_COMPLETED_RUN_DIRECTORY --out-index NEW_INDEX_JSON
python3 benchmark/suite/ldraw-evidence/reporting.py verify --index NEW_INDEX_JSON
python3 benchmark/suite/ldraw-evidence/reporting.py publish --index NEW_INDEX_JSON
```

Each key binds model revision, condition, dataset, adapter and analysis version.
Completed records point to hashed manifests and analyses. Validation reconstructs
requests, parses raw receipts, recomputes item scores, family statistics and paired
analyses, and compares them to the index. Unrun records require null values; zero
is never substituted. Plan/selection membership determines denominators.

## Validation and quality handling

The synthetic receipt chain exercises all eleven task families, including executable
actions. It produces numeric TeX from complete receipts and `--` from unrun records.
Tampering with numbers, denominators, state, IDs or hashes fails validation.
Synthetic records are rejected by production ingestion; the fixture pathway requires
an explicit flag and an independently labelled test index.

Missing responses, timeouts, API errors, refusals, invalid JSON and invalid formats
remain failures in the full denominator. Format validity and accuracy conditional
on valid format are auxiliary fields. Graph deletion additionally reports paired
differences against node count, always-four and graph algorithms, plus deficit strata.

QA decisions bind task, condition, request hash, actual image hashes and dimensions.
They require reviewer/date and native-size/blinding attestations. Only two independently
decidable observations qualify a visual pair; pending/access-difference pairs remain
listed alongside the preserved full result. No source screenshot or extra view
certifies a compressed request.

Browser checks confirmed loaded 1280-by-800 pixels are displayed at 1280-by-800,
navigation changes the task and counter, and judgments remain pending without an
attestation. No human judgment was entered. Exact JSON feedback validation is tested
separately; a browser-session reset prevented checking the native download dialog.

Original items: 617 / 24 sources; exclusions: 0. Registered real results: 0/84.
The code is ready for complete receipts; no model performance or human agreement is
claimed. Full-file hashes and final PDF table checks are included at final delivery.

## Final integration addendum

The final exact-wire UI export is `qa/wrong-image-export-v1/review.html`.
It adds a copyable JSON preview and prepared download link while retaining the
original review export. Browser validation confirms 140 observations exactly
matching the pending template, zero entered judgments, native 1280×800 pixels
and working Next navigation. OS-level download persistence remains unverified;
the visible export content provides a verified fallback. The revised paper uses
the state-driven tables, and every original item is present in the 182-page
supplement.
