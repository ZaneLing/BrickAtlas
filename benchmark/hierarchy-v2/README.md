# Hierarchy-2

Current BrickAtlas development release: 40 original layouts, 35 task families
per layout, 1,400 questions. Each of four levels contains ten objects and
350 questions. The 18 previous layouts remain available alongside 22 new
compositions; shared constructors do not count as independent design families.

The original website at `http://127.0.0.1:5173/` includes the full benchmark
library. Open `/benchmark` to filter the 40 models, or `/benchmark/<model-id>`
for orbit, zoom, pan, exploded view, module isolation, and action replay.
Reference or model-submitted JSON executes the same state machine as scoring.

- `REPORT.zh-CN.md`: design, counts, limitations and all objects.
- `QUESTION_BANK.zh-CN.md`: every question, option, input and answer.
- `models/*.json`: model geometry, 35 tasks and actual Rapier observations.
- `public.json`: tasks without reference answers.
- `answers.json`: separately indexed reference answers.
- `quality.json`: envelope-overlap and nominal-drift diagnostics.
- `controls.json`: reference checks, public action solver and trivial controls.
- `pilot/run.json`: the fixed 16-question GPT-4.1 mini pilot (14/16).
- `web-verification/report.json`: all 40 desktop models and four mobile cases.
- `manifest.json`: source and artifact hashes.

Only 17/40 objects have nominal drift below 0.35 under this simulator
configuration. Unstable layouts remain explicitly flagged diagnostic sources.
This is not physical LEGO assembly, material, clutch-force or robot validation.
Choice tasks often disclose symbolic attributes. Difficulty levels are
structural design strata, not human-calibrated item difficulty.

From the repository root (Node 22+, installed dependencies):

```bash
npm --prefix benchmark run h2:release
npm run start:local
npm --prefix benchmark run h2:render
npm --prefix benchmark run h2:docs
npm --prefix benchmark run h2:score -- predictions.json
npm --prefix benchmark test
npm run build
```

Compile `benchmark/paper/main.tex` and `supplement.tex`, then run:

```bash
npm --prefix benchmark run h2:sync
node node_modules/tsx/dist/cli.mjs benchmark/suite/hierarchy2/release.ts --manifest
node benchmark/paper/verify-artifacts.mjs
```

The paid pilot command refuses to overwrite the archived run. Offline replay
does not make API calls. Older Hierarchy-1 and Mechanism-1 scores are separate.
