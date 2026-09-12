# Local Qwen3 training baseline

Model: local/qwen3-0.6b-single-seed17. Condition: single, seed 17.
Base revision: c1899de289a04d12100db370d81485cdf75e47ca. Dataset and script hashes are in run.json.
This is a **text/structure-only, short LoRA pilot**, not a trained multimodal model.
Optimization steps: 120; processed training tokens: 195292.
Adapter SHA256: 62087ebc3e64beab077c344a41b6ec5cb4baf0e96da107b380a962b0b9cd1102.
Adapter weights and a portable base-model reference are bundled in this run's adapter/ directory.
API cost: $0. Local compute is NOT free; inference took 66.26 seconds.
Prompt-token count was not recorded; stored normalized zeros must not be interpreted as measurements.
Results: 2/8. Raw outputs and all eight applicable/absent task rows are visible in the app.

| Task | n | Success |
| --- | ---: | ---: |
| relations | 2 | 0 |
| generate | 2 | 0 |
| edit | 2 | 2 |
| plan | 2 | 0 |

Validation loss before: {"edit":0.2736103029354759,"generate":1.12632155418396,"plan":0.7173622027039528,"relations":1.395993322134018}

Validation loss after: {"edit":0.0003296187481981284,"generate":1.150269091129303,"plan":0.8718846142292023,"relations":1.012256696820259}

Training only uses the frozen train split; validation groups are disjoint. Loss reduction does not imply general task success.
Single/multi conditions match optimizer steps but not tokens or data diversity, so this is not a causal transfer result.
