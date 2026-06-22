"""AI coding tool and app detection."""

from __future__ import annotations

import os
import shutil
from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class AppStatus:
    name: str
    installed: bool
    path: str = ""
    version: str = ""
    config_paths: list[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "installed": self.installed,
            "path": self.path,
            "version": self.version,
            "config_paths": self.config_paths,
        }


def _which_version(binary: str, flag: str = "--version") -> tuple[str, str]:
    path = shutil.which(binary)
    if not path:
        return "", ""
    try:
        import subprocess

        out = subprocess.run(
            [path, flag],
            capture_output=True,
            text=True,
            timeout=5,
            check=False,
        )
        ver = (out.stdout or out.stderr).strip().splitlines()[0] if out.stdout or out.stderr else ""
        return path, ver
    except (OSError, subprocess.TimeoutExpired):
        return path, ""


def _config_if_exists(*paths: str) -> list[str]:
    return [p for p in paths if Path(p).expanduser().exists()]


def detect_apps() -> list[AppStatus]:
    """Detect AI assistant apps and CLIs on PATH / standard config dirs."""
    home = Path.home()
    apps: list[AppStatus] = []

    cli_tools = [
        ("cursor", "cursor"),
        ("claude", "claude"),
        ("gemini", "gemini"),
        ("opencode", "opencode"),
        ("gh", "gh"),
        ("docker", "docker"),
        ("kubectl", "kubectl"),
        ("skaffold", "skaffold"),
        ("ollama", "ollama"),
        ("poetry", "poetry"),
        ("node", "node"),
        ("python3", "python3"),
    ]
    for name, binary in cli_tools:
        path, ver = _which_version(binary)
        apps.append(AppStatus(name, bool(path), path, ver))

    # IDE config dirs
    cursor_cfg = _config_if_exists(
        str(home / ".cursor"),
        str(home / ".config" / "Cursor"),
    )
    if cursor_cfg:
        apps.append(AppStatus("cursor-ui", True, config_paths=cursor_cfg))

    claude_cfg = _config_if_exists(str(home / ".claude"))
    if claude_cfg:
        apps.append(AppStatus("claude-code-ui", True, config_paths=claude_cfg))

    gemini_cfg = _config_if_exists(str(home / ".gemini"))
    if gemini_cfg:
        apps.append(AppStatus("gemini-cli-ui", True, config_paths=gemini_cfg))

    # Deepiri-specific tools if cloned nearby
    for tool in ("deepiri-wooven", "deepiri-vizult", "deepiri-conduit"):
        path = shutil.which(tool.replace("deepiri-", ""))
        if path:
            apps.append(AppStatus(tool, True, path))

    return apps


def tools_for_install(apps: list[AppStatus]) -> set[str]:
    """Map detected apps to axiom ``--tools`` names."""
    names = {a.name for a in apps if a.installed}
    tools: set[str] = {"cursor", "copilot"}  # cursor rules + copilot instructions always safe
    if "claude" in names or "claude-code-ui" in names:
        tools.add("claude")
    if "gemini" in names or "gemini-cli-ui" in names:
        tools.add("gemini")
    if "opencode" in names:
        tools.add("opencode")
    return tools
