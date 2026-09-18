# Hierarchy-3 expanded

**Retired historical release.** Human review found imitation geometry,
repeated constructors and ambiguous references. This dataset is no longer
served at `/benchmark`. Its nominal servo passes do not establish authentic
LEGO connectivity. Use [LDraw-1](../ldraw-v1/README.md); the counts and links
below describe the archived release only. Historical source data and review
records remain available for tracing corrections.

144 original digital model configurations, four levels of 36 models each.
Every model has 48 task families: 6,912 questions, including 4,608 newly
generated instances. Total: 42,617 visible parts, 2,040 modules, 1,938 joints.

Original site: <http://127.0.0.1:5173/benchmark>

Human review: <http://127.0.0.1:5173/benchmark/review>

The 48 base models and their tasks are byte-identical to `../hierarchy-v3`.
Existing review decisions and exported batches keep their task IDs and remain
usable; the review denominator comes from the live catalog. Newly added tasks
start unreviewed. No script invents human review decisions.

The 96 additions use twelve construction families, two configurations each,
crossed with four structural levels. They have distinct geometric fingerprints
after removing names, colors, and whole-object translation. A retained pair
(indexed latch / orthogonal probe) has matching geometry with different joint
configuration, so 144 configurations correspond to 143 geometric fingerprints.
Shared constructors and station compositions remain correlated sources.

The physical protocol is unchanged: Rapier 0.20.0 at 120 Hz, 64 solver iterations,
force-based position motors with stiffness/damping/maximum force 60000/1500/20000.
All models satisfy the published nominal displacement, rotation and joint
residual thresholds. Contacts between every module pair are checked, including
directly joined modules. These are compound digital primitives, not calibrated
commercial connectors, passive stability or robot trajectories.

No new paid model calls were made. The base-48 7/16 pilot stays archived separately
and is not a measurement on the 96 new layouts.

- [中文扩容报告](REPORT.zh-CN.md)
- [完整6,912题问答库](QUESTION_BANK.zh-CN.md), or individual `questions/<model-id>.md`
- [原48模型兼容性清单](retained-compatibility.json)
- [各级规模](audit.json), [答案分布](answer-distributions.json), [质量记录](quality.json)
- [D1图册](library-D1.png), [D2图册](library-D2.png), [D3图册](library-D3.png), [D4图册](library-D4.png)
- [覆盖矩阵](matrix.png), [全库图册](library.png)
- [论文](../paper/main.pdf), [中文对照](../paper/main.zh-CN.md), [附录](../paper/supplement.pdf)

Reproduce from the repository root, with Node 22 and installed dependencies:

```bash
npm --prefix benchmark run h3x:release
npm run start:local
npm --prefix benchmark run h3x:browser
npm --prefix benchmark run h3x:docs
npm test
npm --prefix benchmark run check
npm run build
npm --prefix benchmark run h3x:score -- predictions.json
```

Browser verification saves a per-model checkpoint; pass `-- --resume` to continue
the same capture/verification run. Compile `main.tex` and `supplement.tex` using
Tectonic, run `check_pdf.py` for both, then `h3x:sync`. Finally:

```bash
node --import tsx benchmark/suite/hierarchy3-expanded/release.ts --manifest
node benchmark/paper/verify-hierarchy-expanded.mjs
```

`h3x` commands publish the current expanded site; `h3` commands refer to the
base-48 archive. Keep the old archive unchanged to preserve existing receipts.
