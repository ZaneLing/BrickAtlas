# Human review and model inference

The release has **280 primary observations** (both sides of 140 pairs) and
**67 auxiliary position-reference observations**. Every observation is present
in each independent reviewer queue. Primary evidence requires 560 raw human
reviews; the auxiliary control requires 134 more. No real human reviews or
model results have been supplied.

## Distribute the blind queues

Give `qa/initial/reviewer-1.zip` and `qa/initial/reviewer-2.zip` to two different
people. Do not distribute `private-mapping.json`, the scoring manifest, gold,
pair membership, condition names or model outputs. A reviewer receives only
their own package. After extracting, they can run:

```sh
python3 -m http.server 8130 --bind 127.0.0.1 --directory /path/to/extracted/reviewer-folder
```

Open `http://127.0.0.1:8130/`. The page presents exactly the system text, user
question/options, and 1280 × 800 PNG sent to models. The native image remains
scrollable rather than being silently resized. Each reviewer provides their
own stable pseudonym, visual choice, decision, four checks, reason, timestamp
and native-size/independence attestations. It saves locally and exports JSON.
Use the latest complete export per reviewer; overlapping partial exports are
rejected as duplicate raw reviews.

## Combine and adjudicate

From the repository root:

```sh
python3 benchmark/suite/ldraw-evidence-v2/qa.py combine \
  benchmark/ldraw-evidence-v2/qa/initial /new/path/qa-first-pass.json \
  --feedback /path/reviewer-1-feedback.json /path/reviewer-2-feedback.json
```

The report retains both raw judgments, decision/choice/check agreement,
multiclass Cohen's kappa, disagreements, and final decisions. The full 280
primary denominator never shrinks. Equal categorical records become final;
any disagreement requires a third person. Equal free-text reasons are not
required. A human answer conflicting with gold remains pending and requires
a dataset revision and new QA.

For disagreements:

```sh
python3 benchmark/suite/ldraw-evidence-v2/qa.py adjudication-export \
  /new/path/qa-first-pass.json /new/path/third-review
```

Serve only the third-review folder. Its page shows one observation and the
two original judgments, without model outputs, gold or the other arm. The
third person's reason and judgment must address the disagreement. After
exporting:

```sh
python3 benchmark/suite/ldraw-evidence-v2/qa.py adjudication-import \
  /new/path/third-review /path/adjudicator-feedback.json /new/path/adjudication.json
python3 benchmark/suite/ldraw-evidence-v2/qa.py combine \
  benchmark/ldraw-evidence-v2/qa/initial /new/path/qa-final.json \
  --feedback /path/reviewer-1-feedback.json /path/reviewer-2-feedback.json \
  --adjudication /new/path/adjudication.json
python3 benchmark/suite/ldraw-evidence-v2/qa.py verify /new/path/qa-final.json
```

Never overwrite reviews. Final summaries are recomputed from retained raw
files; editing a summary cannot bypass the gate. Any changed prompt, option,
system instruction, image, resolution or image-detail policy changes the
wire observation and invalidates its review. The observations are independent
trials and are not sent as a conversation containing both arms.

## Pin a model, inspect requests, then run

Copy `adapter.example.json` to a new file and fill all fields with a real
provider, endpoint and pinned model/API revision. The current adapter supports
OpenAI-compatible chat completions with **native base64 PNGs**. Other provider
transports require a new, validated adapter; no implicit resizing is allowed.
The `response_model` must equal the actual model identifier in raw receipts.

```sh
python3 benchmark/suite/ldraw-evidence-v2/run.py run /new/path/dry-run \
  --adapter /path/pinned-adapter.json --role all
python3 benchmark/suite/ldraw-evidence-v2/run.py verify \
  /new/path/dry-run /new/path/dry-run-validation.json
```

Inspect the saved requests. Only the reviewed messages enter the provider
envelope. Provenance, source truth, pair IDs, conditions, gold and QA do not
enter the prompt. Model envelopes have separate full-request hashes; the
complete model-visible observation must exactly reproduce the reviewed
messages and image bytes. Provider-internal image preprocessing is outside
the evaluator's observation boundary.

With real completed QA and `BRICKATLAS_API_KEY` set outside artifact files:

```sh
python3 benchmark/suite/ldraw-evidence-v2/run.py run /new/path/live-run \
  --adapter /path/pinned-adapter.json --qa /new/path/qa-final.json --live --role all
python3 benchmark/suite/ldraw-evidence-v2/run.py verify \
  /new/path/live-run /new/path/live-validation.json
```

`--role primary` requires final QA on all 280 primary observations.
`--role all` additionally requires all 67 auxiliary observations. Ambiguous,
unanswerable and contradictory final decisions remain in the full score;
only both-decidable pairs enter the additional QA subset. Raw judgments are
frozen before inference. Missing receipts, failed calls, refusals and invalid
formats remain failures in the planned denominator. No automatic retry or
old-response transfer is performed.

The gate verifies recorded provenance and attestations; it cannot
cryptographically prove a person's identity or that a local receipt was
actually produced by a remote provider. Coordinator oversight and retained
provider records remain necessary.
