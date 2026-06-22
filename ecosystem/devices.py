"""Hardware and runtime environment detection."""

from __future__ import annotations

import os
import platform
import shutil
import subprocess
from dataclasses import dataclass, field


@dataclass
class DeviceProfile:
    os_name: str
    os_release: str
    machine: str
    arch: str
    is_wsl: bool = False
    is_container: bool = False
    has_nvidia_gpu: bool = False
    gpu_names: list[str] = field(default_factory=list)
    gpu_vram_mb: list[int] = field(default_factory=list)
    has_apple_silicon: bool = False
    cpu_count: int = 1
    total_ram_gb: float | None = None

    def to_dict(self) -> dict:
        return {
            "os_name": self.os_name,
            "os_release": self.os_release,
            "machine": self.machine,
            "arch": self.arch,
            "is_wsl": self.is_wsl,
            "is_container": self.is_container,
            "has_nvidia_gpu": self.has_nvidia_gpu,
            "gpu_names": self.gpu_names,
            "gpu_vram_mb": self.gpu_vram_mb,
            "has_apple_silicon": self.has_apple_silicon,
            "cpu_count": self.cpu_count,
            "total_ram_gb": self.total_ram_gb,
        }


def _detect_wsl() -> bool:
    if platform.system() != "Linux":
        return False
    try:
        with open("/proc/version", encoding="utf-8", errors="replace") as f:
            return "microsoft" in f.read().lower()
    except OSError:
        return False


def _detect_container() -> bool:
    if os.path.exists("/.dockerenv"):
        return True
    try:
        with open("/proc/1/cgroup", encoding="utf-8", errors="replace") as f:
            content = f.read()
            return "docker" in content or "kubepods" in content or "containerd" in content
    except OSError:
        return False


def _read_mem_gb() -> float | None:
    if platform.system() != "Linux":
        return None
    try:
        with open("/proc/meminfo", encoding="utf-8") as f:
            for line in f:
                if line.startswith("MemTotal:"):
                    kb = int(line.split()[1])
                    return round(kb / 1024 / 1024, 1)
    except (OSError, ValueError):
        pass
    return None


def _probe_nvidia() -> tuple[bool, list[str], list[int]]:
    if shutil.which("nvidia-smi") is None:
        return False, [], []
    try:
        out = subprocess.run(
            [
                "nvidia-smi",
                "--query-gpu=name,memory.total",
                "--format=csv,noheader,nounits",
            ],
            capture_output=True,
            text=True,
            timeout=8,
            check=False,
        )
        if out.returncode != 0:
            return False, [], []
        names: list[str] = []
        vrams: list[int] = []
        for line in out.stdout.strip().splitlines():
            parts = [p.strip() for p in line.split(",")]
            if not parts:
                continue
            names.append(parts[0])
            if len(parts) > 1:
                try:
                    vrams.append(int(float(parts[1])))
                except ValueError:
                    vrams.append(0)
        return bool(names), names, vrams
    except (OSError, subprocess.TimeoutExpired):
        return False, [], []


def detect_device() -> DeviceProfile:
    """Return a snapshot of the local machine capabilities."""
    uname = platform.uname()
    arch = uname.machine.lower()
    has_apple = uname.system == "Darwin" and arch in ("arm64", "aarch64")
    has_nvidia, gpu_names, gpu_vram = _probe_nvidia()
    return DeviceProfile(
        os_name=uname.system,
        os_release=uname.release,
        machine=uname.machine,
        arch=arch,
        is_wsl=_detect_wsl(),
        is_container=_detect_container(),
        has_nvidia_gpu=has_nvidia,
        gpu_names=gpu_names,
        gpu_vram_mb=gpu_vram,
        has_apple_silicon=has_apple,
        cpu_count=os.cpu_count() or 1,
        total_ram_gb=_read_mem_gb(),
    )
