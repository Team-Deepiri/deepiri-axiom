"""Health checks and doctor diagnostics."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from ecosystem.manifest import load_manifest
from ecosystem.scanner import scan_ecosystem


@dataclass
class CheckResult:
    name: str
    ok: bool
    message: str

    def to_dict(self) -> dict:
        return {"name": self.name, "ok": self.ok, "message": self.message}


def run_doctor(anchor: Path) -> list[CheckResult]:
    """Run lightweight health checks for axiom + ecosystem setup."""
    anchor = anchor.resolve()
    results: list[CheckResult] = []

    # Python version
    import sys

    py_ok = sys.version_info >= (3, 10)
    results.append(
        CheckResult(
            "python-version",
            py_ok,
            f"Python {sys.version_info.major}.{sys.version_info.minor}"
            + (" (ok)" if py_ok else " — need 3.10+"),
        )
    )

    # Manifest
    manifest = load_manifest(anchor)
    results.append(
        CheckResult(
            "ecosystem-manifest",
            manifest is not None,
            ".axiom/ecosystem.json present"
            if manifest
            else "missing — run ./setup.sh or `setup.py detect --write`",
        )
    )

    # Cursor agent
    cursor_agent = anchor / ".cursor" / "agents" / "deepiri-axiom.md"
    global_agent = Path.home() / ".cursor" / "agents" / "deepiri-axiom.md"
    has_agent = cursor_agent.is_file() or global_agent.is_file()
    results.append(
        CheckResult(
            "axiom-agent",
            has_agent,
            "deepiri-axiom agent installed"
            if has_agent
            else "not installed — run ./setup.sh",
        )
    )

    # Fresh scan sanity
    try:
        scan = scan_ecosystem(anchor, write=False)
        results.append(
            CheckResult(
                "ecosystem-scan",
                True,
                f"{len(scan.repos)} local repo(s), {sum(1 for p in scan.providers if p.get('available'))} provider(s)",
            )
        )
    except Exception as exc:  # noqa: BLE001 — doctor should report, not crash
        results.append(CheckResult("ecosystem-scan", False, str(exc)))

    return results


def doctor_exit_code(results: list[CheckResult]) -> int:
    return 0 if all(r.ok for r in results) else 1
