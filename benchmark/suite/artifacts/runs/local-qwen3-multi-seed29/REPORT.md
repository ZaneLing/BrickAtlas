# Local Qwen3 training baseline

Model: local/qwen3-0.6b-multi-seed29. Condition: multi, seed 29.
Base revision: c1899de289a04d12100db370d81485cdf75e47ca. Dataset and script hashes are in run.json.
This is a **text/structure-only, short LoRA pilot**, not a trained multimodal model.
Optimization steps: 120; processed training tokens: 176765.
Adapter SHA256: dad8f62e2a660537290792534c48cbf04d4f6949fb074e25f69c4e17712d6021.
Adapter weights and a portable base-model reference are bundled in this run's adapter/ directory.
API cost: $0. Local compute is NOT free; inference took 100.58 seconds.
Prompt-token count was not recorded; stored normalized zeros must not be interpreted as measurements.
Results: 1/8. Raw outputs and all eight applicable/absent task rows are visible in the app.

| Task | n | Success |
| --- | ---: | ---: |
| relations | 2 | 0 |
| generate | 2 | 0 |
| edit | 2 | 1 |
| plan | 2 | 0 |

Validation loss before: {"edit":0.2736103029354759,"generate":1.12632155418396,"plan":0.7173622027039528,"relations":1.395993322134018}

Validation loss after: {"edit":0.01697803518154483,"generate":0.6142889708280563,"plan":0.13852334767580032,"relations":0.15267287008464336}

Training only uses the frozen train split; validation groups are disjoint. Loss reduction does not imply general task success.
Single/multi conditions match optimizer steps but not tokens or data diversity, so this is not a causal transfer result.
