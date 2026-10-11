# BrickPlan 2.3 final review evidence

Three independent simulated review stages are preserved here: design/construction
(`round-01`), final publication/release (`round-02`), and the targeted correction
of the supplementary chart legend (`round-03`). The final review recommends
**7/10, accept**, with no open critical or major issues.
This is not an official CVPR decision. Read `PROTOCOL.md` for the stated
experiment-completion assumption and the limits of the recommendation.

The accepted research snapshot is `bbd92607ce3a379cd891a0a6655574c55960d65726db754eab5a3eac7b8bb12f`.
The bank is `8a1260a450300adb4693fafad8f59e1b7473316bf1d20f004981090008df1058`.

- 97 active source groups; 1,421 episodes and 7,020 probes.
- All 8,441 source/question bindings and independent answers pass.
- 650 exact cost tables, 61,093,730 entries, zero mismatches.
- 36 primary inventory-matched pairs, 18 interventions, 12 source groups.
- The held-out primary cohort has 24 pairs from nine source groups.
- Primary geometric conflicts concern stud support with motion blockers fixed.
- CVPR main PDF: seven pages; supplement: 64 pages.
- Overleaf independently compiles; runtime archive and final HTTP bytes pass.

The publication review and snapshots are exact copies of the reviewer-owned
files. Original `/tmp/brickplan-v23-work/review-round-NN/` references in those
files map to `round-NN/` here. Other `/tmp/` references denote the original
execution locations, not source files required to run the benchmark.
The source checkout contains the complete permanent construction/audit evidence.

`validation.json` and `staged-validation.json` record the pre-commit state.
The final commit/push receipt is recorded separately because a file cannot
contain the hash of the commit that includes its own bytes.
Population VLM and human results remain unmeasured.
