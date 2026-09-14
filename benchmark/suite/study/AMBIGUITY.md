# Observation-Conditioned Support Relations

Version: `ambiguity-1`. This is an additive development extension, not a
replacement for the frozen `brickatlas-casebank-2.0` leaderboard.

## Task

Given a declared finite grammar, the known part geometry and two blue query
parts, determine whether they share a directly supporting red brick.
Return exactly `{"answer":"yes"}`, `{"answer":"no"}`, or
`{"answer":"undetermined"}`. The final answer is justified only if all layouts
consistent with the supplied observation and grammar agree.

Unknown geometry is a complete domino tiling of a 2-by-W interior, W=2,4,6,
using identical red 1x2 bricks. All lower layers, exterior walls, roof and blue
part poses are fixed. Three support heights give nine parameterized families.
The 2,5,13 tilings per width are exhaustive within this grammar, independently
checked against Fibonacci recurrence counts. They are not all possible LEGO
interiors, semantic objects, or arbitrary LDraw connector configurations.

Two paired conditions use the same query and source family:

- `exterior`: the top red support layer is hidden; all grammar layouts remain possible.
- `support-disclosed`: the exact red support placements are provided.

Public records are symbolic known-geometry inputs, not a pure image-perception
test. Paper renders illustrate identical exterior observations and hidden ground
truth; they are not a substitute for a separately frozen RGB model protocol.

## Population and Metrics

The 9 families contain 60 layout states. All pairs of blue parts produce
300 questions in each information condition, 600 task conditions total.
Widths and heights are related constructions, not independent semantic samples.
All derivatives must remain in the same family cluster; cross-domain
confirmation requires genuinely new sources.

Exterior labels: 210 no, 90 undetermined, 0 yes.
Disclosed labels: 264 no, 36 yes, 0 undetermined.
Always-no accuracy is therefore 70% / 88%, while class-balanced accuracy is
50% in either condition. A classifier that merely guesses the majority should
not be called a successful ambiguity reasoner.

Report exact success, format success, accuracy per answer class,
class-balanced accuracy (over present classes), source-macro accuracy,
false certainty conditional on ambiguous inputs, and unnecessary abstention
conditional on determinate inputs. Inapplicable conditional denominators are null.
Malformed answers fail exact success and receive a separate format flag.

The public-input enumeration baseline solves all 600 cases without reading
private labels or candidate structures. Always-no, always-undetermined and
single-witness controls are also recorded. Their results are algorithmic
census facts, not model or human outcomes.

## Artifacts and Verification

```bash
node node_modules/tsx/dist/cli.mjs benchmark/suite/study/ambiguity.ts
node node_modules/tsx/dist/cli.mjs benchmark/suite/study/ambiguity.ts --verify
node node_modules/tsx/dist/cli.mjs --test benchmark/tests/paper-expansion.test.ts
node node_modules/tsx/dist/cli.mjs benchmark/suite/study/ambiguity-score.ts predictions.jsonl report.json
```

External prediction lines use `{"caseId":"...","answer":{"answer":"yes"}}`.
The batch scorer rejects unknown/duplicate IDs and keeps missing submissions
as explicit failed rows. Conditional error rates must be read with returned and
format-valid coverage: a missing output makes neither a definite claim nor an
explicit abstention, but always fails exact success. Do not optimize a
conditional rate by withholding answers.

Artifacts under `../artifacts/study/ambiguity/`:

- `public.jsonl`: model-facing inputs, with no expected labels, candidate programs
  or answer sets. The hidden layer appears only in the disclosed arm.
- `audit.json`: exact private answer sets, candidate states, oracle and control scores,
  source digest and public-input hash.
- `render-verification.json`: 240 frames across 60 layouts and four views;
  36 reference frames plus 204 nontrivial alternative comparisons.

Every layout passes independent cell geometry and contact checks.
The rendered alternative layouts are pixel-identical under the same fixed
paper renderer/GPU/cameras. This is not a proof for arbitrary cameras,
transparent materials, photorealistic renderers, or physical photographs.
The renderer is separate from the historical benchmark renderer.

## Research Boundary

This implements an evidence-consistency endpoint missing from the original
single-witness relation contract. It does not prove that BrickAtlas is the first
ambiguity benchmark, replace human metric calibration, or certify broad semantic
generalization. VLM evaluation on this new track is explicitly unrun and has its
own blank results table. The previous v2 relation tasks remain symbolic,
fully specified questions with unchanged answers.
