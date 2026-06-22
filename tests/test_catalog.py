"""Tests for ecosystem.catalog."""

from ecosystem.catalog import CATALOG_BY_NAME, is_deepiri_repo_name


def test_is_deepiri_repo_name():
    assert is_deepiri_repo_name("deepiri-axiom")
    assert is_deepiri_repo_name("diri-cyrex")
    assert not is_deepiri_repo_name("random-repo")


def test_catalog_has_axiom():
    assert "deepiri-axiom" in CATALOG_BY_NAME
    assert CATALOG_BY_NAME["deepiri-axiom"].category == "infra"


def test_catalog_has_platform():
    assert "deepiri-platform" in CATALOG_BY_NAME
    assert CATALOG_BY_NAME["deepiri-platform"].stack == "node"
