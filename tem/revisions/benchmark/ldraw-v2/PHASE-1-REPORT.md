# Phase 1 report

Status: automated gates passed; full human visual adjudication pending.

Changed only the isolated v2 generator, publisher, release builder, scorer and
types; added independent oracle, verifier, shortcut and reproducibility scripts.
All 617 semantic answers and original graphs remain unchanged.

- S1: 73 graph-deletion items now accept integers. In 63 items the answer is
  the legal maximum, making balanced four-option semantic ranks impossible.
  This necessary, documented deviation avoids creating a maximum-option rule.
- S2: 55 step-lookup items have four legal options and rank counts 14/14/14/13.
- S3: internal reference positions are 14/13/13/13/14; no references are sent.
- S4: internal references use an answer-role-independent global hash
  permutation; no references are sent. Incidental rule matches are reported,
  not misrepresented as zero (original slice 5/73; best registered slice 8/73).
- Additional correction: interface always supplies all five connector labels.
- The sole serializer whitelists necessary fields and embeds actual PNG bytes.
  It removes internal metadata and redundant missingInstanceIds. Loader
  realpath checks reject internal bundles, including path aliases.

Commands: v2 package scripts `ldraw:build`, `ldraw:verify`,
`ldraw:shortcuts`, `check`; `reproducibility.py`; `freeze.py --verify`.
Use the repository's Node 22 binary on PATH.

Results: 617 independent oracle passes, 5,154 negative controls, 75 public
action solves, 24 forbidden paths rejected, 617 canaries blocked and 617
request snapshots checked. Rebuild reproduced 666 files. TypeScript passed.
All 2,131 protected v1 hashes remain unchanged.

Evidence: `verification.json`, `shortcut-report.json`, `task-audit.json`,
`source-audit.json`, `request-snapshots/manifest.json`, `reproducibility.json`.
Agent inspected one request per family and one real image. This is not full
human perceptual review. Existing images are operand-isolated, not full scenes.
Remaining semantic priors are measured in Phase 2; repaired positional rules
do not establish universal absence of shortcuts.
