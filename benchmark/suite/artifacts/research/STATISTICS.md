# Exploratory statistics

Same four source objects; eight task-default inputs. Conditions are NEVER pooled.
Intervals are exact empirical object-cluster bootstrap percentiles (256 resamples),
not evidence of adequate population coverage; zero-width intervals are possible at n=4.

| Model | Task | Ordinary success / 4 | Layers / 4 | Symbolic / 4 |
| --- | --- | ---: | ---: | ---: |
| openai/gpt-4.1-mini | parts | 1 | N/A | N/A |
| openai/gpt-4.1-mini | relations | 2 | N/A | N/A |
| openai/gpt-4.1-mini | reconstruct | 0 | 0 | 4 |
| openai/gpt-4.1-mini | generate | 0 | N/A | N/A |
| openai/gpt-4.1-mini | complete | 0 | 0 | 4 |
| openai/gpt-4.1-mini | edit | 0 | N/A | N/A |
| openai/gpt-4.1-mini | plan | 1 | N/A | N/A |
| openai/gpt-4.1-mini | repair | 0 | 1 | 3 |
| google/gemini-2.5-flash | parts | 2 | N/A | N/A |
| google/gemini-2.5-flash | relations | 1 | N/A | N/A |
| google/gemini-2.5-flash | reconstruct | 0 | 0 | 4 |
| google/gemini-2.5-flash | generate | 0 | N/A | N/A |
| google/gemini-2.5-flash | complete | 0 | 0 | 4 |
| google/gemini-2.5-flash | edit | 0 | N/A | N/A |
| google/gemini-2.5-flash | plan | 2 | N/A | N/A |
| google/gemini-2.5-flash | repair | 2 | 0 | 3 |

## Same-first-response control

| Arm | Task | n | Before | After | Gained | Lost | New USD |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| validation | all | 12 | 2 | 2 | 0 | 0 | 0.02261893 |
| validation | generate | 4 | 0 | 0 | 0 | 0 | 0.00875505 |
| validation | reconstruct | 4 | 0 | 0 | 0 | 0 | 0.00697504 |
| validation | repair | 4 | 2 | 2 | 0 | 0 | 0.00688884 |
| reflection | all | 12 | 2 | 2 | 0 | 0 | 0.02735740 |
| reflection | generate | 4 | 0 | 0 | 0 | 0 | 0.00925740 |
| reflection | reconstruct | 4 | 0 | 0 | 0 | 0 | 0.00801340 |
| reflection | repair | 4 | 2 | 2 | 0 | 0 | 0.01008660 |

## Training

Three multi-task seeds: mean 16.7%, sample SD 7.2%.
All successes are editing cases; no evidence of broad task transfer.
NLL decreases are separate from execution success. Base/single have only one seed.
Local text tasks use the original grid-v1 split, not the composition experiment.

## Limits

- Four source objects, correlated tasks; bootstrap is descriptive and can be degenerate.
- No p-values or confirmatory significance claims. Public procedural pilot.
- Twelve generator labels are not twelve independent mechanisms; OOD label is not proof of mechanism OOD.
- Paired arms run sequentially, no counterbalanced provider-time control; refinement is not autonomous tool use.
- Training uses the old grid-v1 split, not the new composition dataset. Step-matched, not token-matched.

Full per-object vectors, visibility contrasts, validation-minus-reflection contrasts,
failure counts, latency, output tokens and training data are in statistics.json.
