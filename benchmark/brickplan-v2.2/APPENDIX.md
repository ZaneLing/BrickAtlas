# Supplement and evidence index

The English [supplement](supplement.pdf) is separate from the
[CVPR main paper](paper.pdf). Sources are `supplement.tex` and `appendix.tex`.

It covers exact-label certification, sampling and geometric admission,
prefix controls, shallow-choice ties, metric denominators, delayed recovery,
regret conservation, source attribution, real model calls and the complete
377-episode census.

| Evidence | File |
|---|---|
| All task definitions, probes, pairs and witnesses | [tasks.private.json](data/tasks.private.json) |
| 130 oracle certificates | [certificate.json](data/certificate.json) |
| New task-validity audit | [upgrade-audit.json](data/upgrade-audit.json) |
| All policy aggregates | [software-controls.json](data/software-controls.json) |
| All 10,556 policy task-run records | [software-control-records.json.gz](data/software-control-records.json.gz) |
| Static initial-view certificate | [observation-certificate.json](data/observation-certificate.json) |
| Calibration, inverse-last and canonical-problem census | [quality.json](data/quality.json) |
| Publication statistics | [publication-statistics.json](data/publication-statistics.json) |
| Source geometry/mesh provenance | [render-provenance.json](data/render-provenance.json) |
| Figure states and hashes | [provenance.json](figures/provenance.json) |
| Real model trace provenance | [provenance.json](cases/provenance.json) |
| Core release verification | [release-check.json](release-check.json) |
| Download hashes | [manifest.json](release/manifest.json) |

Evaluator answers are included for reproducibility in the downloadable
practice release, and excluded from study HTTP routes.
