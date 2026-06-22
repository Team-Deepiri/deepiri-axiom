"""Tests for ecosystem.link_inference."""

from pathlib import Path

from ecosystem.link_inference import infer_repo_links
from ecosystem.repos import LocalRepo


def test_gitmodules_link(tmp_path: Path):
    platform = tmp_path / "deepiri-platform"
    synapse = tmp_path / "deepiri-synapse"
    platform.mkdir()
    synapse.mkdir()
    (platform / ".gitmodules").write_text(
        '[submodule "synapse"]\n\tpath = services/synapse\n\turl = https://github.com/Team-Deepiri/deepiri-synapse.git\n'
    )
    repos = [
        LocalRepo("deepiri-platform", str(platform)),
        LocalRepo("deepiri-synapse", str(synapse)),
    ]
    links = infer_repo_links(repos)
    assert any(l["kind"] == "submodule" and l["to"] == "deepiri-synapse" for l in links)


def test_pyproject_reference(tmp_path: Path):
    cyrex = tmp_path / "diri-cyrex"
    kit = tmp_path / "deepiri-modelkit"
    cyrex.mkdir()
    kit.mkdir()
    (cyrex / "pyproject.toml").write_text(
        'dependencies = ["deepiri-modelkit @ git+https://github.com/Team-Deepiri/deepiri-modelkit.git"]\n'
    )
    repos = [
        LocalRepo("diri-cyrex", str(cyrex)),
        LocalRepo("deepiri-modelkit", str(kit)),
    ]
    links = infer_repo_links(repos)
    assert any(l["to"] == "deepiri-modelkit" for l in links)
