# Model adapters

These six configurations select concrete candidate variants, not model-family
placeholders. They have not been contacted. IDs do not guarantee current
provider availability. GPT-4.1 and Claude use dated IDs; local models and the
Gemini alias require a checkpoint hash or verified API revision before live
execution. The runner refuses moving aliases with no frozen revision.

Every JSON specifies model family/ID, provider, transport and endpoint,
checkpoint/API revision, base64 PNG format, fixed system prompt, temperature,
top-p, token ceiling, empty tools, image resolution, parser, timeout, attempts,
credential environment-variable name and pricing. Unknown pricing stays null.
Do not store keys in files.

From this directory's parent:

```sh
npm run ldraw:run -- --adapter model-adapters/gpt41.json --out ../../ldraw-v2/runs/my-dry-run
```

This is an offline dry run. Add `--execute` only to intentionally perform API
inference after freezing the exact revision and reviewable task list.
The caller must supply provider access; this upgrade does not train or run a
model. Local SmolVLM, Qwen3-VL and Llama 4 endpoints must implement the OpenAI
chat-completions image contract. Endpoint setup is external to this release.

Receipts preserve raw provider payloads, token usage, latency and request IDs.
No automatic retries or prose/Markdown repairs are allowed. The exact wire
JSON is saved before sending, for both OpenAI and Anthropic transports.
