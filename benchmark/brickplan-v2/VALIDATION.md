# BrickPlan 2.0 validation

The implementation and evidence checks passed. This file reports software
acceptance, not model/human performance or physical hardware validation.

| Layer | Observed result | Reproduction / evidence |
|---|---|---|
| Predecessor simplicity audit | 1,802,728 labels equal the static formula, no exceptions | `audit_predecessor.py`; `data/predecessor-static-audit.json` |
| Oracle qualification | 35 tables, 1,420,363 product-state entries, 11,230,303 directed transition entries; complete Bellman, runtime-edge, inverse and lower-bound checks | `build.py`; `data/certificate.json` |
| Semantic evaluation | All checks pass, including 69 optimal episode transcripts and 196 probe transcripts | `validate.py`; `data/semantic-validation.json` |
| Metrics | Mandatory-rework errors, overlapping recovery, censoring, audit-inclusive regret, missing census and altered-record rejection pass | `validate.py`; `metrics.py`; `evaluate.py` |
| Protocol | 10 tests pass | `python -m unittest discover -s benchmark/brickplan-v2 -p test_protocol.py` |
| External adapter | Actual offline subprocess → HTTP → private collection passes; missing usage and unknown calls stop execution | Protocol tests; no paid provider invocation |
| Browser | 10 Firefox checks pass, no page errors | `test_browser.mjs`; `data/browser-validation.json` |
| Control claims | Every aggregate agrees with the archived 1,932 raw task-run records, including all tier/source/seed summaries | `release.py check`; `data/software-control-records.json.gz` |
| Publication | English PDF with appendix, no unresolved references; source-raster figures and tables tied to bank hashes | `paper.pdf`; `figures/provenance.json`; `data/publication-statistics.json` |
| Frozen predecessors | Every file in the pre-change snapshot is byte-identical | `release.py check`; `data/predecessor-hashes.json` |
| Release integrity | All release and declared dependency digests agree | `release-check.json`; `data/release.json` |

The original predecessor snapshot covers 47 files in v1.0, 42 in v1.1 and
58 in v1.2, including files outside their earlier release manifests.
No older release is regenerated or overwritten.

Browser validation covers source rasters, image-track separation, acquired
view history, historical-frame action guards, operations and diagnosis,
ended replay, free 3D orbit/explosion, probe view/answer freezing, persisted
reload and mobile layout. Screenshots remain in
`tem/brickplan-v2/validation/arena-{desktop,3d-review,mobile}.png`.

The full control set comprises one oracle seed and three tie-order seeds
for each of nine other policies. Seeds reuse the same source structures
and are not independent population samples. Oracle and search controls
receive privileged relations; public structured and image policies are
unmeasured.

The release checker verifies stored evidence and byte integrity. It does
not rerun expensive geometry certification or browser interaction on every
invocation. The rebuild and test commands in [README.md](README.md) are the
separate procedures for executing those checks again.
