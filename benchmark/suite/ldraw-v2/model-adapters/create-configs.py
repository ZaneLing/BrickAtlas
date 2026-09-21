#!/usr/bin/env python3
"""Write candidate adapters once; never silently overwrite a frozen adapter."""
import argparse
import json
from pathlib import Path

parser = argparse.ArgumentParser(description=__doc__)
parser.parse_args()
configs = [
    ("smolvlm", "SmolVLM", "HuggingFaceTB/SmolVLM-256M-Instruct", "local-openai-compatible", "http://127.0.0.1:8000/v1/chat/completions", None),
    ("qwen3-vl", "Qwen3-VL", "Qwen/Qwen3-VL-8B-Instruct", "local-openai-compatible", "http://127.0.0.1:8000/v1/chat/completions", None),
    ("llama4", "Llama 4 Scout", "meta-llama/Llama-4-Scout-17B-16E-Instruct", "local-openai-compatible", "http://127.0.0.1:8000/v1/chat/completions", None),
    ("gpt41", "GPT-4.1", "gpt-4.1-2025-04-14", "OpenAI", "https://api.openai.com/v1/chat/completions", "2025-04-14"),
    ("gemini", "Gemini", "gemini-2.5-pro", "Google OpenAI compatibility", "https://generativelanguage.googleapis.com/v1beta/openai/chat/completions", None),
    ("claude", "Claude", "claude-sonnet-4-20250514", "Anthropic", "https://api.anthropic.com/v1/messages", "2025-05-14"),
]
for slug, family, model, provider, endpoint, revision in configs:
    path = Path(__file__).parent / f"{slug}.json"
    if path.exists():
        continue
    config = {
        "schemaVersion": 1, "family": family, "modelId": model, "provider": provider,
        "endpoint": endpoint, "transport": "anthropic" if slug == "claude" else "openai",
        "apiRevision": revision, "checkpointSha256": None,
        "providerApiVersion": "2023-06-01" if slug == "claude" else "endpoint-contract-v1",
        "executionStatus": "candidate-not-contacted",
        "apiKeyEnv": {"gpt41": "OPENAI_API_KEY", "claude": "ANTHROPIC_API_KEY", "gemini": "GEMINI_API_KEY"}.get(slug, "LOCAL_MODEL_API_KEY"),
        "systemPrompt": "SYSTEM_PROMPT in publish.ts (validated and hashed at run time)",
        "decoding": {"temperature": 0, "top_p": 1, "max_tokens": 2048},
        "tools": [], "imageEncoding": "base64-png",
        "imageResolution": {"width": 1280, "height": 800, "resize": "contain on white, never crop"},
        "outputParser": "strict-json-object; no prose or markdown repair",
        "timeoutMs": 120000, "maxAttempts": 1,
        "pricingUsdPerMillion": {"input": None, "output": None},
        "revisionPolicy": "Before live execution, freeze API revision or checkpoint SHA256. Moving aliases without either are rejected.",
    }
    path.write_text(json.dumps(config, indent=2) + "\n")
print("Candidate adapter files ready; no model contacted.")
