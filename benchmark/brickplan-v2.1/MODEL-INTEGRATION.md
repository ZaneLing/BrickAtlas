# Real model calls and case study

Open `http://127.0.0.1:8769/#case` for the archived case. The default example
is `kart-deck-08`, public ID `E069` at identity seed 0. Four actual
SmolVLM-256M-Instruct calls produce the same descriptive text instead of a
JSON action. Each is preserved and charged as `INVALID_ACTION`. The controller
then finishes at the four-call limit. This is a failed integration case,
not evidence of population planning performance. No oracle actions replace
model outputs. Local API cost is zero.

The trace contains raw output, exact formatted prompt, public observation,
PNG hashes/URLs, latency, MLX input/output token counts, parsed action,
feedback and before/after frames. The source weight hash is in
`cases/provenance.json`. `cases/local-vlm.authoritative.json` supports exact
executor replay. Every call is retained; this is the first run on the
default demonstration, not a selected successful sample.

## Live local inference

In **Model runs**, select a task, provider and call limit, click **Create**,
then use **Step**, **Run** or **Stop**. Creation does not invoke inference.
The timeline exposes every call's input, original output, executor response,
latency and tokens; use **Input / After** to inspect the corresponding state.
The runner supports
1–32 calls, at most 192 output tokens per call and a 150-second timeout.
Stop prevents further actions after the current provider request returns;
it does not cancel a provider's already billed request. Only one inference
job runs at a time.

The local adapter uses a separate Python process with `mlx-vlm`. Defaults:

```text
BRICKPLAN_LOCAL_MODEL=benchmark/.runtime/models/smolvlm-256m
BRICKPLAN_MODEL_PYTHON=benchmark/.runtime/mlx-env/bin/python
```

These defaults resolve relative to the repository, not your shell directory.
Use absolute paths when overriding them. MLX requires Apple silicon.
The available local model is `HuggingFaceTB/SmolVLM-256M-Instruct`.
Weights are not redistributed. Install `mlx-vlm` in the selected runtime
and obtain model weights from their publisher to reproduce elsewhere.

Five native PNGs are provided in this order: current, target, rack, site
reference, catalog. The local model's image processor explicitly resizes
to longest edge 512 with splitting disabled; the browser and saved
stimuli remain 1920 pixels wide. This preprocessing is recorded, not
presented as full-resolution model vision. Temperature and MLX seed are 0.
The prompt includes the latest four response/feedback records. Earlier
acquired images remain in the public observation archive but this demo
policy sends only the five current-view images on each call.

## OpenAI-compatible vision API

Configure on the **server**, then restart:

```bash
export BRICKPLAN_API_BASE='https://your-provider.example/v1'
export BRICKPLAN_MODEL='your-vision-model-id'
# Set BRICKPLAN_API_KEY in the server environment if required.
python benchmark/brickplan-v2.1/server.py serve --port 8769
```

Select the configured provider in the model run panel. The adapter calls
`/chat/completions`, sends the native PNGs as image content, and uses the
same public prompt and executor. Credentials never enter browser inputs,
trace exports or case assets. Model name, provider request ID and reported
token usage are retained. Remote dollar cost is `null` because no universal
pricing API is assumed. Set provider-side spend limits before collecting
large runs. Some providers require a different output-token parameter;
those providers need an explicit adapter change rather than silent retries.

The live UI is a practice demonstration and does not implement the strict
currency-reservation contract of `study.py`. Use the existing external-policy
study runner for preregistered population experiments. Its adapter and budget
manifest are separate from this demonstration.

## Persistence and reproduction

Run records live in `<store>/model-runs/<id>.json`; pixels live in
`<store>/media/<sha256>.png`. Raw responses are saved before execution.
On a server restart, an unresolved running call becomes `interrupted` and
is never automatically charged or executed again. Failed parsing is
explicitly represented as `invalid-model-output`, consuming one action
through the same public session protocol.

Archive a completed real local run:

```bash
python benchmark/brickplan-v2.1/export_case.py \
  --store tem/brickplan-v2.1/practice --run RUN_ID
```

The model adapter receives no costs, witness plans, legal-action list,
relations or source-group metadata. In image mode it receives no matrices
or installed-site flags. It has no need to read evaluator files. Formal
remote-agent studies should still isolate the policy host from the
evaluator filesystem; an application convention is not a sandbox.
