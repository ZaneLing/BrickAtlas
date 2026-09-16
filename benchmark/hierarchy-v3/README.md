# Hierarchy-3

48 original digital layouts × 48 shared task families = 2,304 questions.
Four levels contain 12 layouts and 576 questions each; total geometry is
6,339 parts, 546 rigid modules, and 503 joints. Forty previous layouts are
corrected and eight new layouts are added. Shared constructors remain correlated.

Open the original website at `http://127.0.0.1:5173/benchmark`.
Every model supports orbit, zoom, pan, four views, explosion, isolation,
and submitted-action replay with the same interpreter as offline scoring.

- [中文报告](REPORT.zh-CN.md), [完整问答库](QUESTION_BANK.zh-CN.md), [校正记录](ERRATA.zh-CN.md).
- `models/*.json`: complete geometry, tasks, physics and validation records.
- `public.json` / `answers.json`: separated public inputs and answers.
- `quality.json`: all-pair contact checks, anchors and nominal motion.
- `answer-distributions.json`: semantic answer frequencies and majority baselines.
- `historical-ambiguities.json`: corrected acceptance rules for 11 old ambiguous questions.
- `pilot/run.json`: a fixed, receipted, low-cost model smoke test; no population ranking.
- `render-audit.json`, `web-verification/report.json`, `manifest.json`: receipts and hashes.

All 48 layouts pass the declared nominal protocol: representative-point displacement
<0.35, rotation <0.15 rad, non-spring joint residual <0.02. Every inter-module
pair, including directly joined modules, has initial cuboid penetration ≤0.005.
Contacts stay enabled. Revolute limits are checked on instantiated Rapier joints.
The 120 Hz/64-iteration protocol uses finite-force position servos (60000/1500/20000).
This is not passive stability, commercial LEGO connector certification, material
calibration, or robot trajectory validation. Individual modules remain compound bodies.

From the repository root (Node 22 and installed dependencies):

```bash
npm --prefix benchmark run h3:release
npm run start:local
npm --prefix benchmark run h3:render
npm --prefix benchmark run h3:ui
npm --prefix benchmark run h3:docs
npm test
npm --prefix benchmark test
npm --prefix benchmark run check
npm run build
npm --prefix benchmark run h3:score -- predictions.json
```

Compile `benchmark/paper/main.tex` and `supplement.tex` with Tectonic.
Then run `h3:sync`, regenerate the manifest with
`node --import tsx benchmark/suite/hierarchy3/release.ts --manifest`, and run
`node benchmark/paper/verify-hierarchy3.mjs`.

The separately billed `h3:pilot` command refuses to overwrite its archived run.
Historical raw records stay in `hierarchy-v2`; their scores are not relabeled as new results.
The viewer exposes references deliberately; `public.json` is the model-evaluation input.
