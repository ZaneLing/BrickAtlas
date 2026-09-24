# Retired publication assets

These are byte-preserved figures, tables, raw captures and builders from
earlier manuscript iterations. The current manuscript consumes only the
`repair-*` TeX inputs and the repair-task, repair-factorial and source-atlas
figures under `paper/`.

Historical builders are retained as evidence; their original relative paths
describe the pre-migration workspace. They are not current build entry points.
Reproduce that historical layout from commit
`d7e2ea0a7c10ee153ff29a5839511b6b18882492` when needed.
Use `npm run paper:build` for the current manuscript.

`paper/build_tables.py` keeps inherited, unused assets here and records their
new locations in `paper/asset-provenance.json`, preserving source hashes.
The source-geometry capture page itself lives in `web/paper/`.
See [the relocation manifest](../../repository-layout-20260924/moves.json)
for every original path and SHA-256.
