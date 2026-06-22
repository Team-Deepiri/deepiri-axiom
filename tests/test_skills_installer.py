"""Tests for cli.skills_installer."""

from pathlib import Path

from cli.skills_installer import list_skill_dirs, skill_body, skill_install_operations


def test_list_skill_dirs_nonempty():
    skills = list_skill_dirs()
    assert len(skills) >= 40
    names = {n for n, _ in skills}
    assert "deepiri-axiom" in names
    assert "diri-cyrex" in names
    assert "axiom-scan" in names


def test_skill_body_static():
    skills = dict(list_skill_dirs())
    body = skill_body("diri-cyrex", skills["diri-cyrex"], {})
    assert "diri-cyrex" in body
    assert "FastAPI" in body or "8000" in body


def test_skill_body_j2_template():
    skills = dict(list_skill_dirs())
    mapping = {
        "DEEPIRI_CONTEXT": "CTX",
        "TARGET_REPO_CARTOGRAPHY": "CARTO",
        "ECOSYSTEM_CONTEXT": "ECO",
        "AXIOM_BRANCH_TOOLS": "BRANCH",
        "AXIOM_CONDENSED": "COND",
    }
    body = skill_body("deepiri-axiom", skills["deepiri-axiom"], mapping)
    assert "CTX" in body
    assert "ECO" in body


def test_skill_install_operations(tmp_path: Path):
    mapping = {
        "DEEPIRI_CONTEXT": "x",
        "TARGET_REPO_CARTOGRAPHY": "y",
        "ECOSYSTEM_CONTEXT": "z",
        "AXIOM_BRANCH_TOOLS": "b",
        "AXIOM_CONDENSED": "c",
    }
    ops = skill_install_operations(tmp_path, mapping, tools={"cursor", "claude"})
    assert len(ops) == len(list_skill_dirs()) * 2
    paths = [p for _, p, _ in ops]
    assert tmp_path / ".cursor" / "skills" / "deepiri-gateway-auth" / "SKILL.md" in paths
    assert tmp_path / ".claude" / "skills" / "axiom-debug" / "SKILL.md" in paths
