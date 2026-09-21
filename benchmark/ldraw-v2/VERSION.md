# BrickAtlas LDraw-2

Freeze: 2026-09-18T07:55:48.388196+00:00

v1 remains immutable. `v1-frozen-manifest.json` records every protected file, SHA256 and the distinct model_input / internal_scoring roles (24 each).

Original sources are referenced through `sources -> ../ldraw-v1/sources`; they must never be written through this link. New questions, evidence, experiments and publication artifacts use the ldraw-v2 namespace.

Phase 0 copied the v1 question generator and scorer byte for byte. The v1 build is exercised only in a disposable copy because its CLI unconditionally rewrites frozen outputs.
