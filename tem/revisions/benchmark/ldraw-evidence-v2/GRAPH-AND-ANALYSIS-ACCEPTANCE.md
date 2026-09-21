# Graph and diagnostic analysis acceptance

Controlling review: `CVPR_EVIDENCE_V1_REVIEW.md`, C2, M1 and M2.

## Computed graph evidence

The preserved 219 hypothetical observations form four distinct reporting
partitions. Their 73 anchors are shared by change and invariance pairs;
the partitions must not be added as independent observations.

| Partition | Pairs | Sources | Degree histogram Both | Anonymous 1-WL Both | Isolates + one Both | BFS / union-find Both |
|---|---:|---:|---:|---:|---:|---:|
| Strong change, primary proof of concept | 12 | 8 | 0/12 | 0/12 | 0/12 | 12/12 |
| Degree-visible change control | 61 | 23 | 61/61 | 61/61 | 61/61 | 61/61 |
| Strong invariance | 12 | 8 | 6/12 | 6/12 | 6/12 | 12/12 |
| Degree-visible invariance | 61 | 23 | 61/61 | 61/61 | 61/61 | 61/61 |

All strong pairs have identical surviving nodes, edge count, target degree,
complete surviving degree multiset and isolate count. Their anonymous 1-WL
signatures also match. The primary construction is a six-cycle versus two
triangles, with the same extra isolates. It cannot establish broad graph
reasoning, and cannot be solved by a deterministic predictor of only those
anonymous 1-WL features. Unique-ID, positional, spectral or higher-order
methods are outside that impossibility claim.

Lookups use labels only from other sources. Training uses each changed
observation once; invariance observations do not duplicate the training
distribution. Unseen features abstain and count as incorrect; ties choose the
smaller answer. Node-count, edge-count, degree-histogram and 1-WL lookup folds,
predictions, support, feature collisions and every pair are released in
`graph-audit.json`. Natural tasks have a separate held-source-out fit:
isolates-plus-one obtains 72/73, compared with 73/73 for BFS/union-find.
This is computed algorithmic evidence, not a learned-model result.

Strong change directions are balanced, six increases and six decreases.
Stored per-answer frequencies are not exactly equal between A/B; their full
histograms are disclosed. The primary metrics are unordered Both and symmetric
endpoint accuracy. Swapping endpoint roles gives equal weighted arm histograms
without generating extra trials or inflating the 12-pair/8-source denominator.

Whole-source bootstrap intervals and approximate pair Wilson intervals are
both supplied. For 0/12 and 12/12 Both, Wilson intervals are [0, 0.2425] and
[0.7575, 1]. Wilson assumes independent pairs despite source reuse; source
bootstrap intervals can degenerate at boundary outcomes. Neither is population
validation for this small template family.

## C2/M2 implementation

`analyze.py` accepts only completed new visual live runs that `run.verify`
reconstructs from exact requests and raw responses, with one common finalized
human-QA snapshot. Old visual runs, dry runs and fixtures cannot register.

- Separate Color and Part-type tables include A accuracy, B/NewAcc, Both,
  unconditional old-gold retention, other wrong answers, invalid output,
  A/B/both format-valid rates, conditional adaptation, and conditional retention.
- Every estimate exposes item/source counts, micro accuracy and source-macro
  accuracy. Conditional denominators are explicit. Missing/failed responses
  remain incorrect observations; null denotes an undefined statistic.
- Full and both-decidable estimates retain source coverage and overlapping
  exclusion reasons. QA-minus-full intervals resample the same source weights
  for both estimates, including source-composition changes.
- Ordinary-A, NewAcc and Both rankings use exact rational point comparisons
  and midranks for ties. Pairwise model differences use paired source
  intervals; reversals, ties, and full/subset direction agreement remain
  separate. Intervals are descriptive and unadjusted.
- Case selection uses only genuine responses in QA-decidable pairs, separately
  by family: correct-to-new, correct-to-old, and same-valid-wrong. Both raw
  provider responses, output text, request/wire/receipt hashes accompany each
  available case. Absent case types stay absent.
- The 67 Part-type position-reference controls have a separate descriptive
  analysis. Layout and visual access change along with the reference interface;
  its difference from label-based accuracy does not identify an OCR effect.

`graph_run.py` independently snapshots all 219 text-graph requests under a new
strict integer contract, saves raw provider receipts and validates them before
reporting the four partitions. It recomputes graph gold and partition membership
from the preserved inputs. `runs/graph-wire-audit-final/validation.json` verifies
219 requests and zero model calls. `runs/graph-wire-audit` is a superseded
offline snapshot from before JSON-canonical audit validation was finalized.

Twelve analysis/graph tests pass in addition to the fourteen visual protocol
tests. They cover failure denominators, undefined conditionals, source balance,
QA selection, rank reversals versus exact ties, boundary uncertainty, graph
feature collisions, held-source exclusion, strict integer responses, tampering,
and rejection of dry runs as empirical results.

## Current empirical acceptance

Current visual report: `reports/protocol-ready.json`.
`reports/initial.json` is a superseded protocol snapshot.

Real independent human reviews: 0. Final primary decisions: 0/280.
QA-comparable pairs: 0/140. Real visual or graph model runs: 0.
Accordingly, no model rankings, empirical rank reversals, raw model case examples,
or full-versus-QA-subset agreement are claimed. These requirements remain open.

## Commands

Run from the repository root with the isolated scientific Python environment:

```sh
env -u PYTHONPATH PYTHONNOUSERSITE=1 benchmark/.runtime/mlx-env/bin/python benchmark/suite/ldraw-evidence-v2/graph_audit.py
env -u PYTHONPATH PYTHONNOUSERSITE=1 benchmark/.runtime/mlx-env/bin/python -m unittest discover -s benchmark/suite/ldraw-evidence-v2 -p 'test_*.py' -v
```

After actual visual inference, pass fresh run directories to
`analyze.py NEW_REPORT.json --run RUN_A --run RUN_B`. The command verifies
receipts and human QA before producing statistics. For graph inference use
`graph_run.py run NEW_RUN --adapter PINNED_ADAPTER.json --live`, followed by
`graph_run.py analyze NEW_RUN NEW_REPORT.json`. The API key is supplied only
through `BRICKATLAS_API_KEY`, never a saved artifact.
