"""Shared pytest fixtures."""

from __future__ import annotations

import pytest


@pytest.fixture(autouse=True)
def _block_live_github_catalog(monkeypatch):
    """Keep CI/offline tests deterministic — individual tests can override."""
    monkeypatch.setattr(
        "ecosystem.github_catalog.fetch_org_catalog",
        lambda org: ([], "unavailable"),
    )
