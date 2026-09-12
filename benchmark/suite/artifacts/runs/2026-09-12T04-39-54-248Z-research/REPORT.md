# Composition grammar controlled evaluation

Status: complete; no infrastructure error.
Version: composition-grammar-v1; 112 cases; 112 calls.
Actual API cost: $0.20204040.
Campaign cumulative: $0.40104878 / $4.50.

The SAME four heldout objects are used across eight tasks. Visual reconstruction,
completion and repair have ordinary RGB+BOM, layer-revealed, and privileged symbolic
conditions. Other tasks have their task-default symbolic or isolated-part input.
This is a small paired development study, not a statistically powered leaderboard.

| Model | Task | Condition | n | Errors | Success | Full structure | Surface F1 | Cost |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| openai/gpt-4.1-mini | parts | ordinary | 4 | 0 | 0.25 | N/A | N/A | $0.003318 |
| openai/gpt-4.1-mini | relations | ordinary | 4 | 0 | 0.5 | N/A | N/A | $0.002510 |
| openai/gpt-4.1-mini | reconstruct | ordinary | 4 | 0 | 0 | 0 | 0.15288548002165808 | $0.007972 |
| openai/gpt-4.1-mini | reconstruct | layers | 4 | 0 | 0 | 0 | 0.2372020619609044 | $0.011957 |
| openai/gpt-4.1-mini | reconstruct | symbolic | 4 | 0 | 1 | 1 | 1 | $0.005673 |
| openai/gpt-4.1-mini | generate | ordinary | 4 | 0 | 0 | N/A | N/A | $0.005954 |
| openai/gpt-4.1-mini | complete | ordinary | 4 | 0 | 0 | 0 | 0.688936995417841 | $0.008586 |
| openai/gpt-4.1-mini | complete | layers | 4 | 0 | 0 | 0 | 0.7111193223553678 | $0.012323 |
| openai/gpt-4.1-mini | complete | symbolic | 4 | 0 | 1 | 1 | 1 | $0.006238 |
| openai/gpt-4.1-mini | edit | ordinary | 4 | 0 | 0 | N/A | N/A | $0.005182 |
| openai/gpt-4.1-mini | plan | ordinary | 4 | 0 | 0.25 | N/A | N/A | $0.002934 |
| openai/gpt-4.1-mini | repair | ordinary | 4 | 0 | 0 | 0 | 0.9345930456708513 | $0.008899 |
| openai/gpt-4.1-mini | repair | layers | 4 | 0 | 0.25 | 0.25 | 0.9293688434812404 | $0.012627 |
| openai/gpt-4.1-mini | repair | symbolic | 4 | 0 | 0.75 | 0.75 | 1 | $0.006504 |
| google/gemini-2.5-flash | parts | ordinary | 4 | 0 | 0.5 | N/A | N/A | $0.002137 |
| google/gemini-2.5-flash | relations | ordinary | 4 | 0 | 0.25 | N/A | N/A | $0.002122 |
| google/gemini-2.5-flash | reconstruct | ordinary | 4 | 0 | 0 | 0 | 0.2507936806915161 | $0.007441 |
| google/gemini-2.5-flash | reconstruct | layers | 4 | 0 | 0 | 0 | 0.2696175816649417 | $0.008801 |
| google/gemini-2.5-flash | reconstruct | symbolic | 4 | 0 | 1 | 1 | 1 | $0.007474 |
| google/gemini-2.5-flash | generate | ordinary | 4 | 0 | 0 | N/A | N/A | $0.008398 |
| google/gemini-2.5-flash | complete | ordinary | 4 | 0 | 0 | 0 | 0.7866836324435137 | $0.008470 |
| google/gemini-2.5-flash | complete | layers | 4 | 0 | 0 | 0 | 0.7933401869078828 | $0.009761 |
| google/gemini-2.5-flash | complete | symbolic | 4 | 0 | 1 | 1 | 1 | $0.008405 |
| google/gemini-2.5-flash | edit | ordinary | 4 | 0 | 0 | N/A | N/A | $0.006589 |
| google/gemini-2.5-flash | plan | ordinary | 4 | 0 | 0.5 | N/A | N/A | $0.003048 |
| google/gemini-2.5-flash | repair | ordinary | 4 | 0 | 0.5 | 0.5 | 0.9498090950535674 | $0.009095 |
| google/gemini-2.5-flash | repair | layers | 4 | 0 | 0 | 0 | 0.8924503686897334 | $0.010434 |
| google/gemini-2.5-flash | repair | symbolic | 4 | 0 | 0.75 | 0.75 | 1 | $0.009186 |

## Interpretation

- Primary visual score uses colored first-hit grid surfaces along positive X/Y/Z,
  legal geometry, BOM and preservation; hidden-layout alternatives are not forced
  to match one private reference. Full-structure correctness is separate.
- Generation uses envelope, anchoring, branching, connectivity and color-count
  constraints, not a supplied target voxel mask. It is not aesthetic text-to-3D.
- Editing is a whole-assembly spatial rotation; this is not arbitrary semantic editing.
- Geometry uses supported grid parts. Imported BrickNet catalog coverage is not
  equivalent to validated general connector or force simulation.
- No model receives a prior task's answer. Cases and source hashes were frozen before calls.
- Model, visibility condition and task remain separate; do not average conditions
  into one alleged visual-intelligence score.
- Human audit and broad external-data transfer have not been completed.

Dataset hash: 02d84a1db9d8b6ffc8cb126b87d71c6c78b581156a5653d86e513f4389ac8358
Selection hash: 646641c8600b1d5bb2e61d4505da85baf33d798d19056c1c3887e9e7f119bdf4
Source hashes and full responses: run.json. Actual receipts: ledger.json.
