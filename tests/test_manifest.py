"""Tests for ecosystem.manifest."""

import json
from pathlib import Path

from ecosystem.manifest import EcosystemManifest, load_manifest, manifest_path, save_manifest


def test_manifest_roundtrip(tmp_path: Path):
    m = EcosystemManifest(device={"arch": "x86_64"}, repos=[{"name": "deepiri-axiom"}])
    path = save_manifest(tmp_path, m)
    assert path.is_file()
    loaded = load_manifest(tmp_path)
    assert loaded is not None
    assert loaded.device["arch"] == "x86_64"
    assert loaded.repos[0]["name"] == "deepiri-axiom"


def test_manifest_path_location(tmp_path: Path):
    assert manifest_path(tmp_path) == tmp_path / ".axiom" / "ecosystem.json"
