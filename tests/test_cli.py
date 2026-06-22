"""Tests for cli.main commands."""

from pathlib import Path

from cli.main import cmd_detect, cmd_status


def test_cmd_detect_writes_manifest(tmp_path: Path):
    repo = tmp_path / "deepiri-axiom"
    repo.mkdir()
    args = type("A", (), {"target": repo, "write": True})()
    assert cmd_detect(args) == 0
    assert (repo / ".axiom" / "ecosystem.json").is_file()


def test_cmd_status_missing_manifest(tmp_path: Path):
    args = type("A", (), {"target": tmp_path})()
    assert cmd_status(args) == 1
