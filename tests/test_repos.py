"""Tests for ecosystem.repos discovery."""

import subprocess
from pathlib import Path

from ecosystem.link_inference import infer_repo_links
from ecosystem.repos import LocalRepo, discover_local_repos, repo_name_from_remote, scan_sibling_repos


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


def test_repo_name_from_remote_nonstandard_folder(tmp_path: Path, monkeypatch):
    clone = tmp_path / "my-axiom-fork"
    clone.mkdir()
    subprocess.run(["git", "init"], cwd=clone, check=True, capture_output=True)
    subprocess.run(
        [
            "git",
            "remote",
            "add",
            "origin",
            "https://github.com/Team-Deepiri/deepiri-axiom.git",
        ],
        cwd=clone,
        check=True,
        capture_output=True,
    )
    monkeypatch.setenv("DEEPIRI_CLONE_ROOTS", str(tmp_path))
    repos = discover_local_repos(clone)
    assert len(repos) == 1
    assert repos[0].name == "deepiri-axiom"
    assert repos[0].path == str(clone.resolve())


def test_repo_links_from_package_json(tmp_path: Path):
    front = tmp_path / "deepiri-web-frontend"
    gate = tmp_path / "deepiri-api-gateway"
    front.mkdir()
    gate.mkdir()
    (front / "package.json").write_text(
        '{"dependencies":{"@deepiri/gateway":"github:Team-Deepiri/deepiri-api-gateway"}}'
    )
    repos = [
        LocalRepo("deepiri-web-frontend", str(front)),
        LocalRepo("deepiri-api-gateway", str(gate)),
    ]
    links = infer_repo_links(repos)
    assert any(
        lnk["from"] == "deepiri-web-frontend"
        and lnk["to"] == "deepiri-api-gateway"
        and lnk["kind"] == "npm-dep"
        for lnk in links
    )


def test_repo_links_wrapper():
    repos = [
        LocalRepo("deepiri-web-frontend", "/a"),
        LocalRepo("deepiri-api-gateway", "/b"),
    ]
    from ecosystem.repos import repo_links

    links = repo_links(repos)
    assert isinstance(links, list)


def test_repo_name_from_remote():
    assert repo_name_from_remote("git@github.com:Team-Deepiri/deepiri-axiom.git") == "deepiri-axiom"
    assert repo_name_from_remote("https://github.com/Team-Deepiri/diri-cyrex") == "diri-cyrex"
    assert repo_name_from_remote("https://github.com/other/foo.git") is None
