# BrickPlan 2.1 validation

This evidence describes software behavior and release consistency. It does
not establish population model performance, human usability or hardware validity.

| Layer | Evidence | File / command |
|---|---|---|
| Exact oracles | 70 tables; 4,053,285 product-state and 39,989,367 directed-transition entries; Bellman, runtime, inverse and lower-bound checks | `data/certificate.json` |
| Semantic evaluation | 145 optimal episode replays and 739 diagnostic answers; budget, overlapping-error, censoring, missing-assignment and tamper checks | `validate.py`; `data/semantic-validation.json` |
| New task validity | Balanced conflict positions, exact prefixes/multisets, source separation, geometry/appearance pairs and independent repair BFS | `audit_v21.py`; `data/upgrade-audit.json` |
| Protocol | 10 unit/integration tests, including real offline adapter → HTTP → collection, restart, idempotence and rollback | `test_protocol.py` |
| Live model manager | 4 tests including an actual HTTP provider fixture; raw output, invalid-action charging and adapter image delivery | `test_models.py` |
| Source scene boundary | 3 tests: original meshes/poses, session and recorded-case frames, study isolation and side-effect-free previews | `test_scenes.py` |
| Raster loading | 2 tests: pixel equality with the frozen renderer across sources/views/explosion, and scene/tasks responding during a cold preview | `test_visual_loading.py` |
| React workbench | 9 Firefox checks: categories, native WebGL2 orbit, 1920px zoom, preview isolation, history guards, a five-operation optimal UI replay, frozen probes, model trace and mobile downloads; source/build hashes | `data/workbench-validation.json` |
| Hover and HD loading | Desktop and touch piece details, clean default scenes, native HD switch timing and immutable request deduplication | `test_hover_loading.mjs` |
| Integrated publication | Real local one-call run through UI, controlled-study raster and denied routes, seven static 3D samples and case/downloads under a URL subpath | `data/workbench-integration.json` |
| Software measurements | All 4,060 raw records reconcile with all policy/tier/source/seed aggregates | `data/software-control-records.json.gz`; `release.py check` |
| Real model case | 4 actual local SmolVLM calls, weight/trace/image hashes and independently replayable executor transcript | `cases/provenance.json`; `cases/local-vlm.authoritative.json` |
| CVPR publication | Official pinned template, English main/supplement, generated tables, source-rendered figures | `cvpr-template-provenance.json`; `figures/provenance.json` |
| Independent Overleaf | 21 source files; extracted main and supplement independently compile and match published PDF text | `../../deliverables/brickplan-paper/manifest.json` |
| Core release | Claims, figures, archived browser evidence, native images and frozen predecessor hashes | `release-check.json` |
| Portable publication | 884 public records, 7 HD examples, archive inventory and download hashes | `package_release.py check`; `release/manifest.json` |

Current React screenshots and detailed outputs are retained under
`tem/research/20261009-react-workbench/`. Prior UI evidence under
`tem/brickplan-v2.1/validation/` is historical and is not the acceptance evidence
for the rebuilt frontend. The source-admission first-pass failures
and the geometric pruning refinement are retained with the new-source plan.
No old release is regenerated to make this release pass.

Loading and hover measurements/screenshots are under
`tem/research/20261009-hover-performance/`. On the same local E001 preview,
HTTP time changed from 10.355/10.179 seconds on successive requests to
2.075/0.004 seconds for cold/cached requests; all five PNG hashes and public
metadata matched. The preloaded HD tab switch measured 42ms in Firefox.
These are local integration measurements, not hardware-independent guarantees.

The release checker validates stored evidence and file hashes. It does not
rerun geometric qualification or browser interactions each time.
Re-execution commands are in [README.md](README.md).
The portable bundle verifier performs native rendering, an oracle lookup,
catalog loading, recorded-case loading, and all extracted-file hashes without
requiring the original workspace.

Hugging Face upload and a hosted Docker build have not been performed.
Local runtime/browser verification does not assert external deployment success.
