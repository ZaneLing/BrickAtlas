# BrickAtlas Hierarchy-1

Hierarchy-1 is the four-level BrickAtlas development benchmark.

- 18 original brick objects
- 1,773 visible parts
- 121 rigid modules
- 106 declared joints
- 90 balanced core questions
- 48 additional Mechanism-1 questions at D3
- 138 unique questions in the combined release

## Difficulty Levels

| Level | Scope | Models | Core questions |
|---|---|---:|---:|
| D1 | component | 4 | 20 |
| D2 | assembly | 4 | 20 |
| D3 | mechanism | 6 | 30 |
| D4 | system | 4 | 20 |

Each object contributes two atomic single-choice questions and one
metacognitive/physical, procedural, and integrative question. The fixed
16-case pilot samples one question from every difficulty-by-layer cell.

The final low-cost OpenRouter pipeline run uses GPT-4.1 mini and scores 13/16
at a new-call cost of $0.006553. It is a workflow check with one case per
matrix cell, not a model ranking. Two pre-generation Gemini HTTP 429 responses
were reconciled at zero cost and are retained as excluded attempt evidence.

Open `index.html` for the visual browser, `QUESTION_BANK.zh-CN.md` for every
question and answer, and `HIERARCHY_REPORT.zh-CN.md` for the design report.

OMR/LDraw assets are references only. They are not models, questions, prompts,
or scored samples in this release.
