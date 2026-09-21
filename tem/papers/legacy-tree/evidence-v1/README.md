# Evidence-following manuscript

This is the separate `ldraw2-evidence-v1` revision. Original LDraw-2 files are
preserved. The manuscript reports a method/resource contribution and measured
algorithmic controls. Learned-model and human study results are unavailable.

Compile this directory with Tectonic:

```sh
tectonic main.tex
tectonic supplement.tex
```

The source ZIP is self-contained for compilation. It contains the unchanged
official CVPR 2026 style, references, generated numeric tables, vector figures
and the complete 617-question dossiers and source images.

Recomputing analyses or regenerating figures requires the full BrickAtlas
repository and its frozen source assets. Follow `BUILD.md` in that checkout.
`asset-provenance.json` binds every original image, paper-only crop and
generated table. The Python figure source is
`benchmark/suite/ldraw-evidence/publication.py`.

The main manuscript uses anonymous review mode and an unregistered draft ID.
The current-year official style is a format baseline, not a registered submission.
Third-party source authors in the appendix are asset attributions.

`pdf-verification.json` records automated page, font, language, caption and
question-coverage checks. `visual-inspection.json` separately records page
inspection. Inspection of illustrations does not constitute human answerability
approval of benchmark questions.
