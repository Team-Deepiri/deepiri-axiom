"""Tests for ecosystem.scanner."""

from pathlib import Path

from ecosystem.scanner import scan_ecosystem


def test_scan_ecosystem_write(tmp_path: Path):
    (tmp_path / "deepiri-axiom").mkdir()
    manifest = scan_ecosystem(tmp_path / "deepiri-axiom", write=True)
    assert manifest.device
    assert (tmp_path / "deepiri-axiom" / ".axiom" / "ecosystem.json").is_file()
