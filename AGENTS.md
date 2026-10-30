# Project instructions

## Current experiment batch — Ark only, 2026-10-30

- The user's latest instruction restricts the new small-batch experiment to Ark API using `ARK_API_KEY`. This overrides the older provider preferences below for this batch, including DeepSeek and Qwen if selected.
- Use `https://ark.cn-beijing.volces.com/api/v3` for Sol, Seed Pro and DeepSeek in this batch. The user's later instruction explicitly adds Qwen through Aliyun, with the same cases and budgets. No OpenRouter or DeepSeek direct fallback. Preserve older experiments and their original provider labels.
- A model appearing in the Ark catalogue is not proof of enabled image inference. Verify image/JSON compatibility before task runs. The user explicitly authorized Sol without an Ark price on 2026-10-30 ("ark别管价格，用就行了"). Record its token usage and label any monetary conversion as provisional, not an Ark invoice or guaranteed monetary cap.

## Model API routing — explicit user preference, 2026-10-30

- Call DeepSeek through its official API using `DEEPSEEK_API_KEY` from the project `.env` or process environment.
- Call Qwen through Alibaba Cloud / DashScope using `ALIYUN_API_KEY` from the project `.env` or process environment (`DASHSCOPE_API_KEY` is an optional fallback).
- Do not route either family through OpenRouter, including when a legacy model name starts with `qwen/` or `deepseek/`. Do not silently switch providers after an error.
- Other providers may use the existing OpenRouter configuration.
- Never print, commit, or put credentials in command arguments, logs, or reports. Reports contain model IDs, endpoint hosts, usage, and credential variable **names** only.
- The versioned implementation is `benchmark/brickplan-repair/unified_agent/providers.py`. Preserve old experiment artifacts and label new provider routes explicitly.

## Experiment readiness — 2026-10-30

- The expanded batch uses `unified_agent.experiment_batch` and `deliverables/brick-atlas-experiments-v3/plan.json`: each of the same four backbones has 50 static checkpoints and 50 normal builds, plus qualified incidents and separately labelled prior missing conditions. Current input protocol is `/5`, profile `visual-memory-pull-v5`; use the current per-model certificates and cumulative ledgers in that directory. v4 found ambiguous camera/page documentation and is retained only as interface-diagnostic evidence; all conditions including successes are rerun under v5, never merged across versions or success-selected. See `RUN.zh-CN.md` and `revisions.json`. The earlier v2/v3 notes below describe historical batches.

- The Ark/Aliyun pilot in `deliverables/brick-atlas-ark-pilot-v1` is complete and uses the historical v2 input. Preserve its original scores and receipts. Its `completed.json` prevents new paid requests in that directory.
- New shared visual-agent experiments use `unified_agent.run` and the v3 profile, with static manuals restricted to the public target stage. Use a new output directory and current interface certificate; never reuse the v2 scores as v3 results. For Ark batch tools, set `BRICK_ARK_PILOT_OUT` to a new directory under this project's `deliverables/` and supply its plan. See `deliverables/brick-atlas-ark-pilot-v1/RUN.zh-CN.md`.
- Every run requires a current API certificate from `unified_agent.readiness` and a fresh case check before spending on a task.
- Keep model inputs, defaults, memory and per-case budgets identical across backbones within a condition. Record provider-specific generation settings. Never silently enlarge one failed run's budget.
- Never execute or guess a truncated action. Keep service failures, output truncation, schema errors, budget rejections and physical rejections separately observable; technical interruptions are not assembly failures.
- Preserve raw requests/responses, image hashes and cost ledgers. Do not delete or reset a ledger to bypass its cumulative budget, and do not silently retry an uncertain request.
- V1 reports and ledgers are historical artifacts. New runs belong in the v2 output directory and must not rewrite old scores under new settings.
