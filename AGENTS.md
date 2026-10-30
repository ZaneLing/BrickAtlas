# Project instructions

## Model API routing — explicit user preference, 2026-10-30

- Call DeepSeek through its official API using `DEEPSEEK_API_KEY` from the project `.env` or process environment.
- Call Qwen through Alibaba Cloud / DashScope using `ALIYUN_API_KEY` from the project `.env` or process environment (`DASHSCOPE_API_KEY` is an optional fallback).
- Do not route either family through OpenRouter, including when a legacy model name starts with `qwen/` or `deepseek/`. Do not silently switch providers after an error.
- Other providers may use the existing OpenRouter configuration.
- Never print, commit, or put credentials in command arguments, logs, or reports. Reports contain model IDs, endpoint hosts, usage, and credential variable **names** only.
- The versioned implementation is `benchmark/brickplan-repair/unified_agent/providers.py`. Preserve old experiment artifacts and label new provider routes explicitly.

## Experiment readiness — 2026-10-30

- For new shared visual-agent experiments, use `unified_agent.run` and the v2 profile. It requires a current API certificate from `unified_agent.readiness` and a fresh case check before spending on a task. See `deliverables/brick-atlas-experiment-readiness-v2/RUN.zh-CN.md`.
- Keep model inputs, defaults, memory and per-case budgets identical across backbones within a condition. Record provider-specific generation settings. Never silently enlarge one failed run's budget.
- Never execute or guess a truncated action. Keep service failures, output truncation, schema errors, budget rejections and physical rejections separately observable; technical interruptions are not assembly failures.
- Preserve raw requests/responses, image hashes and cost ledgers. Do not delete or reset a ledger to bypass its cumulative budget, and do not silently retry an uncertain request.
- V1 reports and ledgers are historical artifacts. New runs belong in the v2 output directory and must not rewrite old scores under new settings.
