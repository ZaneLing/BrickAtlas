# Project instructions

## Model API routing — explicit user preference, 2026-10-30

- Call DeepSeek through its official API using `DEEPSEEK_API_KEY` from the project `.env` or process environment.
- Call Qwen through Alibaba Cloud / DashScope using `ALIYUN_API_KEY` from the project `.env` or process environment (`DASHSCOPE_API_KEY` is an optional fallback).
- Do not route either family through OpenRouter, including when a legacy model name starts with `qwen/` or `deepseek/`. Do not silently switch providers after an error.
- Other providers may use the existing OpenRouter configuration.
- Never print, commit, or put credentials in command arguments, logs, or reports. Reports contain model IDs, endpoint hosts, usage, and credential variable **names** only.
- The versioned implementation is `benchmark/brickplan-repair/unified_agent/providers.py`. Preserve old experiment artifacts and label new provider routes explicitly.
