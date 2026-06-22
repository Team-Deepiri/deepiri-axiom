"""Tests for ecosystem.doctor."""

from pathlib import Path

from ecosystem.doctor import run_doctor


def test_doctor_runs(tmp_path: Path):
    results = run_doctor(tmp_path)
    names = {r.name for r in results}
    assert "python-version" in names
    assert "ecosystem-scan" in names
