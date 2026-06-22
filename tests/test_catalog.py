"""Tests for ecosystem.catalog and github_catalog."""

import json
import time
from pathlib import Path

from ecosystem.catalog import RepoEntry, get_catalog, get_catalog_by_name, is_deepiri_repo_name
from ecosystem.github_catalog import load_cached_catalog, refresh_org_catalog


def test_is_deepiri_repo_name():
    assert is_deepiri_repo_name("deepiri-axiom")
    assert is_deepiri_repo_name("diri-cyrex")
    assert not is_deepiri_repo_name("random-repo")


def test_catalog_from_cache_fixture(tmp_path: Path):
    import time

    fixture = json.loads(
        (Path(__file__).parent / "fixtures" / "org-catalog-sample.json").read_text()
    )
    fixture["fetched_at"] = time.time()
    cache_dir = tmp_path / ".axiom"
    cache_dir.mkdir()
    (cache_dir / "org-catalog.json").write_text(json.dumps(fixture))
    entries, source = get_catalog(tmp_path)
    assert source.startswith("cache:")
    assert "deepiri-axiom" in {e.name for e in entries}
    axiom = get_catalog_by_name(tmp_path)["deepiri-axiom"]
    assert axiom.category == "infra"
    assert axiom.stack == "python"


def test_refresh_uses_stale_cache_when_fetch_fails(tmp_path: Path, monkeypatch):
    fixture = json.loads(
        (Path(__file__).parent / "fixtures" / "org-catalog-sample.json").read_text()
    )
    fixture["fetched_at"] = time.time() - 999_999
    (tmp_path / ".axiom").mkdir()
    (tmp_path / ".axiom" / "org-catalog.json").write_text(json.dumps(fixture))

    monkeypatch.setattr(
        "ecosystem.github_catalog.fetch_org_catalog",
        lambda org: ([], "unavailable"),
    )
    rows, source = refresh_org_catalog(tmp_path, force=True)
    assert source.startswith("stale-cache:")
    assert any(r["name"] == "deepiri-platform" for r in rows)


def test_repo_entry_from_dict():
    e = RepoEntry.from_dict(
        {"name": "x", "category": "platform", "role": "test", "stack": "node", "default_port": None}
    )
    assert e.name == "x"
