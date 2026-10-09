# BrickPlan 2.2 verification

These checks establish software consistency, not population model performance,
human usability, perceptual sufficiency, or real-world mechanical validity.

| Layer | Evidence | Artifact or command |
|---|---|---|
| Exact labels | 130 tables, 6,836,215 product-state entries, 72,954,915 directed transitions | `data/certificate.json` |
| Independent recomputation | 2,329/2,329 records; 130 tables with zero cost mismatches; 188/188 pairs | `audit_independent.py`, `data/independent-audit/summary.json` |
| Semantic replay | 377 optimal episode replays, 1,952 diagnostic answers; missing/tampered assignments, budgets and overlapping errors | `validate.py`, `data/semantic-validation.json` |
| Diagnostic rules | Sequence prefixes and multisets, source separation, geometry/appearance controls, independent forward repair BFS | `audit_v21.py`, `data/upgrade-audit.json` |
| Initial observations | Ten geometry pairs × four fixed views × five panels; every static pair differs, three isometric pairs do not | `audit_observations.py`, `data/observation-certificate.json` |
| Scoring units | Calibration exclusion, canonical problem/source averaging, missing responses, inverse-last cohorts | `quality.py`, `test_quality.py`, `data/quality.json` |
| Frame metadata isolation | State-independent acquired-frame IDs across image tracks, active probes, seeds, replay, restart and retries | `test_quality.py` |
| Public protocol | Restart, idempotence, atomic rollback, adapter-to-HTTP collection, static/active acquisition | `test_protocol.py` |
| Model manager | Offline provider fixture, raw outputs, invalid-action charging and image delivery | `test_models.py` |
| Practice scenes | Exact original poses, authoritative frames, historical task replay, study isolation | `test_scenes.py` |
| Native raster | Pixel identity with frozen renderer; cold preview does not block other HTTP routes | `test_visual_loading.py` |
| Measured policies | 10,556 task-runs, reconciled per policy, source, tier, split and seed | `data/software-control-records.json.gz`, `release.py check` |
| Historical model case | Four actual version-2.1 SmolVLM calls with original task/bank/image provenance | `cases/historical-release.json`, `cases/task.v2.1.json` |
| CVPR manuscript | Unmodified pinned author kit, evidence-derived tables and original-source figures | `cvpr-template-provenance.json`, `figures/provenance.json` |
| Independent Overleaf build | Extracted ZIP compiles main and supplement and matches PDF text | `../../deliverables/brickplan-paper/manifest.json` |
| Current workbench | Versioned frontend source/build hashes and browser evidence | `data/workbench-validation.json`, `data/workbench-integration.json` |
| Portable package | 2,329 public records, seven HD samples, runtime and inventory checks | `package_release.py check`, `release/manifest.json` |

Current revision logs and independent-review material are retained in
`tem/research/20261009-brickplan-v22-revision/`. Historical 2.1 browser timings
are not treated as new 2.2 measurements. Native rendering and hover-only
part details remain regression requirements.

All 145 predecessor episodes and 739 diagnostic definitions are retained;
private scoring annotations are added without changing their answers.
The previous release's exact bytes are checked against the pre-revision
snapshot. The independent discrete audit preserves the original reviewer's
transition, cost, and answer rules. Only input/output paths and the
release-size assertion are adapted; both source hashes and the exact
one-line adaptation are recorded.
The unchanged reviewer rule source, per-record audit, and table/pair reports
are archived under `data/independent-audit/` for rechecking after checkout.

Pixel-difference certificates use native images and identity seed zero.
They do not prove human agreement, model accuracy, or robustness under
all preprocessing and identity choices. Additional seed/preprocessing
conditions require corresponding checks.

Release checking validates recorded evidence and hashes; it does not rerun
geometry qualification or browser actions each time. Use the reproduction
commands in `README.md` for those checks. No hosted Docker build or external
Dataset/Space upload is claimed.
