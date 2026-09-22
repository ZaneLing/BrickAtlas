# Main integration and BA-005

The current manuscript is rewritten around visual-repair-v1's actual primary
contract. Color/Part-type and the three symbolic demonstrations are explicitly
historical and do not inflate new task counts.

- Main: 6 content pages plus 1 reference page, unmodified archived CVPR style.
- Supplement: 6 pages.
- Main figures show an actual development input, complete graph and all
  optima, plus its matched six-cell design. Counts and GT come from generated
  benchmark artifacts, not manually invented tables.
- Model inventory retains 15 names/classes. Current primary and decomposed
  result schemas contain 147 null fields. Old atomic 306-field matrices are
  not relabeled as results for the new task.
- Main explicitly reports the fired silhouette gate: 91.2% held-out micro
  exact repair, 78.3% group macro, 684 observations/10 groups, oracle 100%.
  It disclaims hard visual recognition and broad population generalization.
- Six reviewer slots assign two people per visual arm; repeated ID/fault views
  within an arm are dependent, correcting an overstrong independence phrase.
- Native packets, images, GT, source records and algorithm output hashes are
  bound in `paper/repair-figure-provenance.json`.
- `paper/verify.py` enforces the current version, null cells, provenance,
  citation resolution, no overfull boxes and no more than eight content pages.

Main independently ran the paper build/verification and visually inspected
the PDFs and figures. A detected overlapping solution-list layout was repaired
before final compilation; the final current figures have separated solution
rows. Old reviewer files remain unchanged.

These integration changes address BA-005's explicit closure tests. Final
scientific closure, including novelty after the strong shallow baseline,
remains the independent round-02 reviewer's decision.
