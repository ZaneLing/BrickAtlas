# BrickPlan 1.1 protocol

This extension preserves the seven metric definitions, action/observation wire
schemas, budgets, diagnosis timing, counterfactual scoring, and censoring rules
in [the frozen 1.0 protocol](../brickplan-v1/PROTOCOL.md).
Its implementation imports the unchanged 1.0 executor and scorer.

The **case census and interpretation of coverage** below supersede the 1.0
case census. The complete numeric ledger is generated in
[APPENDIX.md](APPENDIX.md) and [data/release.json](data/release.json).

- The combined bank adds `airframe`, an original LEGO 31028 subassembly.
- Roadster and kart remain one LEGO 31027 provenance group. Airframe is the
  second group. Keep roadster and kart together in any train/test split.
- Every structure has full, checkpoint, repair, and matched healthy episodes,
  one choice probe, eight lookahead probes, and four counterfactual members.
- Full action count, mandatory no-detach dependency chain, and supplied-plan
  first-conflict distance are separate quantities.
- The new mandatory chain is certified across all no-detach completions.
  Supplied-plan conflict probes still have causal depth **one**. Their longer
  distances do not establish deeper causal reasoning or internal search.
- This remains a D1, known-pose, straight-path, rigid-stud diagnostic track.
  No 100-step, free-manipulation, vision-only, clutch-force, or population-level
  performance claim is introduced.

Use the **1.1 launcher** for serving, collecting and evaluating this bank:

```bash
python3 benchmark/brickplan-v1.1/run.py serve --port 8767
python3 benchmark/brickplan-v1.1/run.py collect --store RUN_DIRECTORY \
  --metadata METADATA_JSON --output SUBMISSION_JSON
python3 benchmark/brickplan-v1.1/run.py evaluate SUBMISSION_JSON --output REPORT_JSON
```

The public 1.0 `Client` class remains compatible with port 8767. Wire schemas
retain `/1.0` because their meaning has not changed. Collected metadata and
launcher evaluation reports explicitly record `benchmarkRelease: "1.1"`.
The original 1.0 evaluator covers only its original bank and must not be used
to report combined-bank scores.

The model process must not read the local private task/cost certificates or
post-trial oracle views. Browser camera controls are practice/review features;
they do not constitute a matched image-only human/model observation protocol.
Software oracle, attach-only and recovery controls are implementation tests,
never model or human benchmark results.
