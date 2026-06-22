"""Tests for ecosystem.apps."""

from ecosystem.apps import AppStatus, detect_apps, tools_for_install


def test_detect_apps():
    apps = detect_apps()
    assert any(a.name == "python3" for a in apps)


def test_tools_for_install_includes_cursor():
    apps = [AppStatus("python3", True)]
    tools = tools_for_install(apps)
    assert "cursor" in tools
    assert "copilot" in tools
