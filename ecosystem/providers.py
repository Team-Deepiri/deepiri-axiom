"""LLM / model provider detection from env, binaries, and local services."""

from __future__ import annotations

import json
import os
import shutil
import subprocess
import urllib.error
import urllib.request
from dataclasses import dataclass, field


@dataclass
class ProviderStatus:
    name: str
    available: bool
    detail: str = ""
    models: list[str] = field(default_factory=list)
    endpoint: str = ""

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "available": self.available,
            "detail": self.detail,
            "models": self.models,
            "endpoint": self.endpoint,
        }


def _env_set(*keys: str) -> bool:
    return any(os.environ.get(k, "").strip() for k in keys)


def _http_json(url: str, timeout: float = 2.0) -> dict | list | None:
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "deepiri-axiom/1.0"})
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except (urllib.error.URLError, json.JSONDecodeError, TimeoutError, OSError):
        return None


def _probe_ollama(host: str = "http://127.0.0.1:11434") -> ProviderStatus:
    data = _http_json(f"{host}/api/tags")
    models: list[str] = []
    if isinstance(data, dict) and isinstance(data.get("models"), list):
        for m in data["models"]:
            if isinstance(m, dict) and isinstance(m.get("name"), str):
                models.append(m["name"])
    available = bool(models) or _http_json(f"{host}/api/version") is not None
    detail = f"{len(models)} model(s)" if models else ("reachable" if available else "not running")
    return ProviderStatus("ollama", available, detail, models, host)


def _probe_openai_compatible(name: str, env_keys: tuple[str, ...], default_base: str) -> ProviderStatus:
    has_key = _env_set(*env_keys)
    base = os.environ.get(f"{name.upper()}_BASE_URL", default_base).rstrip("/")
    available = has_key
    detail = "API key in env" if has_key else "no API key"
    return ProviderStatus(name, available, detail, endpoint=base)


def detect_providers() -> list[ProviderStatus]:
    """Detect configured model providers on this machine."""
    providers: list[ProviderStatus] = []

    # Local Ollama
    providers.append(_probe_ollama())

    # Cloud API keys (presence only — never read secret values)
    cloud = [
        ("openai", ("OPENAI_API_KEY",)),
        ("anthropic", ("ANTHROPIC_API_KEY",)),
        ("google", ("GOOGLE_API_KEY", "GEMINI_API_KEY")),
        ("groq", ("GROQ_API_KEY",)),
        ("together", ("TOGETHER_API_KEY",)),
        ("mistral", ("MISTRAL_API_KEY",)),
        ("cohere", ("COHERE_API_KEY",)),
        ("deepseek", ("DEEPSEEK_API_KEY",)),
        ("xai", ("XAI_API_KEY",)),
    ]
    for name, keys in cloud:
        providers.append(_probe_openai_compatible(name, keys, f"https://api.{name}.com"))

    # Cursor / IDE hints (not model providers but routing context)
    if shutil.which("cursor"):
        providers.append(ProviderStatus("cursor-ide", True, "cursor CLI on PATH"))
    if os.path.isdir(os.path.expanduser("~/.cursor")):
        providers.append(ProviderStatus("cursor-config", True, "~/.cursor present"))

    # vLLM / TGI local servers (common ports)
    for port, label in ((8000, "vllm-8000"), (8080, "tgi-8080")):
        ping = _http_json(f"http://127.0.0.1:{port}/v1/models")
        if isinstance(ping, dict) and isinstance(ping.get("data"), list):
            models = [m.get("id", "") for m in ping["data"] if isinstance(m, dict)]
            providers.append(
                ProviderStatus(label, True, f"{len(models)} model(s)", models, f"http://127.0.0.1:{port}")
            )

    # HuggingFace token
    if _env_set("HF_TOKEN", "HUGGING_FACE_HUB_TOKEN"):
        providers.append(ProviderStatus("huggingface", True, "token in env"))

    return providers


def recommended_local_stack(device_has_gpu: bool) -> list[str]:
    """Suggest providers suited to detected hardware."""
    if device_has_gpu:
        return ["ollama", "vllm-8000"]
    return ["ollama", "openai", "anthropic"]
