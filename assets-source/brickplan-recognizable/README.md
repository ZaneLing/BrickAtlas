# Original LDraw OMR sources

`original/` preserves the downloaded files byte for byte, including author and
CCAL version 2.0 license headers. `downloads.json` records exact URLs and SHA256
hashes. Source leaf instances and transforms are exported to
`web/public/models/r-omr-*/manifest.json` without dropping parts.

These are source candidates, not all admitted dynamic models. The screening
results are in `deliverables/brickplan-recognizable-models/admission-screen.json`.
Whole-source coverage does not imply that the official retail parts inventory
has been independently checked. The physical executor supports qualified rigid
connections and straight insertion/extraction, not general articulated motion.

Dependencies use the repository's pinned LDraw library. Their file hashes are
recorded in the collection's `source-dependencies/` directory. Author, source
links, selection scope, and original hashes are retained in every admitted model.
