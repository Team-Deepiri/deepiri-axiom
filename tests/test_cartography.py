"""Tests for cli.repo_cartography."""

import json
from pathlib import Path

from cli.repo_cartography import build_target_cartography


def test_cartography_for_empty_dir(tmp_path: Path):
    md = build_target_cartography(tmp_path)
    assert "Target repo snapshot" in md


def test_cartography_with_package_json(tmp_path: Path):
    (tmp_path / "package.json").write_text(
        json.dumps({"workspaces": ["packages/*"]})
    )
    (tmp_path / "packages").mkdir()
    (tmp_path / "packages" / "a").mkdir()
    (tmp_path / "packages" / "a" / "package.json").write_text(
        json.dumps({"name": "@deepiri/a"})
    )
    md = build_target_cartography(tmp_path)
    assert "npm workspaces" in md
