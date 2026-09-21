# Display-v3 human review and complete-roster inference

Run repository commands from the BrickAtlas root. The checked Python runtime
is `benchmark/.runtime/mlx-env/bin/python` with inherited `PYTHONPATH` cleared.
Do not edit an earlier release or regenerate the immutable assignment to
obtain a preferred score.

## Independent human exposure

Six initial reviewer packages are in `qa/initial/reviewer-1.zip` through
`reviewer-6.zip`. They contain 115, 116, 114, 115, 115 and 119 observations.
Distribute each package to a different person. Every endpoint is assigned
twice, but a person sees at most one observation from a parent, including
auxiliary panels. Reviewers must not open the evaluator site, the source
viewer, another package or answer files before completing their assignment.

Unzip the assigned package and serve that folder with a local HTTP server,
for example `python3 -m http.server 8000`. Open `http://localhost:8000/`.
Use a stable pseudonym, inspect the full native 1280×800 image, choose the
visual answer, complete the four checks and give a reason. Export the feedback
JSON. The coordinator retains the unmodified export. Browser-local work is
not collected until the JSON has been exported.

Both endpoint decisions and their raw reviews are retained. The initial
schema requires genuine human evidence. Test fixtures never satisfy this gate.
There are currently zero actual human judgments.

Combine one export per reviewer slot:

```sh
env -u PYTHONPATH PYTHONNOUSERSITE=1 benchmark/.runtime/mlx-env/bin/python benchmark/suite/ldraw-evidence-v3/qa.py combine benchmark/ldraw-evidence-v3/qa/initial benchmark/ldraw-evidence-v3/qa/round-1.json --feedback /path/reviewer-1-feedback.json /path/reviewer-2-feedback.json /path/reviewer-3-feedback.json /path/reviewer-4-feedback.json /path/reviewer-5-feedback.json /path/reviewer-6-feedback.json
```

Missing judgments remain pending. The validator reconstructs the assignment,
checks every displayed queue record against the exact frozen wire, prohibits
one identity occupying multiple slots, and verifies visual choices/checks.
Matching decidable choices that conflict with generated gold also stay pending
and require a dataset revision; they are not silently re-keyed.

## Independent adjudication

For categorical decision, choice or structured-check disagreements:

```sh
env -u PYTHONPATH PYTHONNOUSERSITE=1 benchmark/.runtime/mlx-env/bin/python benchmark/suite/ldraw-evidence-v3/qa.py adjudication-export benchmark/ldraw-evidence-v3/qa/round-1.json benchmark/ldraw-evidence-v3/qa/adjudication-round-1
```

The export creates up to three `adjudicator-N` packages. Give each to a
different additional person who was not an initial reviewer. No adjudicator
sees multiple observations of the same parent. They see the single observation
and its two judgments, without gold, counterpart or model output. Their
attestation explicitly permits only those displayed judgments.

Import all available adjudicator exports together:

```sh
env -u PYTHONPATH PYTHONNOUSERSITE=1 benchmark/.runtime/mlx-env/bin/python benchmark/suite/ldraw-evidence-v3/qa.py adjudication-import benchmark/ldraw-evidence-v3/qa/adjudication-round-1 benchmark/ldraw-evidence-v3/qa/adjudication-import.json --feedback /path/adjudicator-1-feedback.json /path/adjudicator-2-feedback.json /path/adjudicator-3-feedback.json
```

Omit paths for packages that were not needed. Re-run `qa.py combine` to a
fresh final snapshot using the original six `--feedback` paths and
`--adjudication benchmark/ldraw-evidence-v3/qa/adjudication-import.json`.
The final verifier reconstructs imported adjudication from the original raw
exports and checks that the reviewer never saw a counterpart.

```sh
env -u PYTHONPATH PYTHONNOUSERSITE=1 benchmark/.runtime/mlx-env/bin/python benchmark/suite/ldraw-evidence-v3/qa.py verify benchmark/ldraw-evidence-v3/qa/final.json --role all
```

All 347 endpoints need final nonpending decisions before visual inference.
Nondecidable items remain in the full denominator; only both-decidable
primary pairs enter the additional QA subset.

## Frozen model roster

`model-roster.json` contains three primary OpenAI snapshots:
GPT-4.1 `gpt-4.1-2025-04-14`, GPT-4o `gpt-4o-2024-08-06`,
and GPT-4o mini `gpt-4o-mini-2024-07-18`.
Their official documentation was checked for snapshot IDs, image input and
Chat Completions support. Live account availability has not been checked.
This is a fixed three-snapshot study using one provider and one transport;
it is not a latest-model or cross-provider leaderboard.

Each model has one visual run (347 observations), one no-image dependency
control (347) and one graph run (219). The expected run universe is exactly
nine directories and 2,739 scheduled requests. No-image controls remove only
the image content while retaining text; their interpretation is evidence
withdrawal, not independent visual answerability.

Every adapter pins the requested and expected returned revision, API path,
temperature zero, 128-token output budget, 90-second timeout, native resolution
and high image detail. Each observation has exactly one scheduled attempt,
with no retries or best-of selection. Temperature zero does not establish
cross-call determinism.

After actual human qualification, supply `BRICKATLAS_API_KEY` through the
environment without saving it in any artifact. For each model ID `gpt41`,
`gpt4o`, `gpt4o-mini`, run the three planned conditions:

```sh
env -u PYTHONPATH PYTHONNOUSERSITE=1 benchmark/.runtime/mlx-env/bin/python benchmark/suite/ldraw-evidence-v3/run.py run --model gpt41 --condition visual --qa benchmark/ldraw-evidence-v3/qa/final.json --live
env -u PYTHONPATH PYTHONNOUSERSITE=1 benchmark/.runtime/mlx-env/bin/python benchmark/suite/ldraw-evidence-v3/run.py run --model gpt41 --condition no-image --qa benchmark/ldraw-evidence-v3/qa/final.json --live
env -u PYTHONPATH PYTHONNOUSERSITE=1 benchmark/.runtime/mlx-env/bin/python benchmark/suite/ldraw-evidence-v3/run.py run --model gpt41 --condition graph --live
```

Live runs always use `benchmark/ldraw-evidence-v3/model-runs/`. Existing run
IDs cannot be overwritten or resumed. The initial manifest and every
pre-call intent are saved before the network request. Raw HTTP responses
and terminal receipt/attempt hash sets are retained.

If a process is interrupted, stop any surviving worker before explicitly
closing the existing run:

```sh
env -u PYTHONPATH PYTHONNOUSERSITE=1 benchmark/.runtime/mlx-env/bin/python benchmark/suite/ldraw-evidence-v3/run.py close benchmark/ldraw-evidence-v3/model-runs/gpt41-visual-r1 --reason "Actual interruption reason"
```

The closure preserves the old checkpoint, marks unattempted and
attempted-without-receipt requests separately, and keeps all scheduled items
in the denominator. These records are not fabricated provider responses.
HTTP failures, refusals, timeouts and invalid output also remain failures.
Changing an adapter, replacing an unavailable model or repeating a run
requires an explicit new study version before collecting replacement results.

## Full-roster analysis

```sh
env -u PYTHONPATH PYTHONNOUSERSITE=1 benchmark/.runtime/mlx-env/bin/python benchmark/suite/ldraw-evidence-v3/analyze.py benchmark/ldraw-evidence-v3/reports/complete-model-results.json
```

The analyzer reads the frozen roster and the complete dedicated run root.
Missing/extra directories, mismatched adapter hashes, stale inputs, changed
receipts, invalid QA lineage and dry runs block empirical output. Each
planned run must be terminal, including explicitly closed failures.
The companion `complete-model-results-model-run-index.json` binds all nine
roster entries to request/receipt hashes, QA, run dates and report rows.

Color and Part-type remain separate. Report A accuracy, NewAcc, Both,
old-gold retention, invalid/format rates, full and both-decidable counts,
source intervals and author/contributor sensitivities. Author leave-one-out
changes constrain any cross-source stability statement. Graph partitions
remain supporting text-graph evidence, never a pooled visual score.
Point rank reversals are descriptive; differences whose intervals contain
zero do not establish a ranking. No cross-call stability claim is supported.

For offline checking, `wire_audit.py` verifies all 2,739 planned requests
without network calls. Its dry runs cannot enter empirical analysis.
`analyze.py OUTPUT --protocol-only` produces an explicitly nonempirical report
with no model scores and incomplete roster status.
