"""Tests for ecosystem.providers."""

from ecosystem.providers import ProviderStatus, detect_providers


def test_detect_providers_returns_list():
    providers = detect_providers()
    assert isinstance(providers, list)
    assert len(providers) >= 1


def test_provider_status_to_dict():
    p = ProviderStatus("test", True, "ok", ["m1"], "http://localhost")
    d = p.to_dict()
    assert d["name"] == "test"
    assert d["available"] is True
    assert d["models"] == ["m1"]
