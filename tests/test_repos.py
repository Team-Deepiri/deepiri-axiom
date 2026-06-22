"""Tests for ecosystem.repos."""

from pathlib import Path

from ecosystem.repos import repo_links, scan_sibling_repos


def test_scan_finds_axiom_repo(tmp_path: Path):
    axiom = tmp_path / "deepiri-axiom"
    axiom.mkdir()
    (axiom / "setup.py").write_text("# stub")
    repos = scan_sibling_repos(axiom)
    names = [r.name for r in repos]
    assert "deepiri-axiom" in names


def test_scan_finds_sibling(tmp_path: Path):
    parent = tmp_path / "Deepiri"
    parent.mkdir()
    (parent / "deepiri-axiom").mkdir()
    (parent / "diri-cyrex").mkdir()
    (parent / "diri-cyrex" / "pyproject.toml").write_text("[project]\nname='x'\n")
    repos = scan_sibling_repos(parent / "deepiri-axiom")
    names = {r.name for r in repos}
    assert "deepiri-axiom" in names
    assert "diri-cyrex" in names


def test_repo_links_only_when_both_present():
    from ecosystem.repos import LocalRepo

    repos = [
        LocalRepo("deepiri-web-frontend", "/a"),
        LocalRepo("deepiri-api-gateway", "/b"),
    ]
    links = repo_links(repos)
    kinds = {lnk["kind"] for lnk in links}
    assert "http" in kinds
