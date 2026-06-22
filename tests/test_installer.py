"""Tests for cli.installer."""

from cli.installer import merge_json_fill_missing, parse_tools_arg, render_template


def test_render_template():
    out = render_template("Hello {{NAME}}", {"NAME": "axiom"})
    assert out == "Hello axiom"


def test_parse_tools_all():
    tools = parse_tools_arg("all", {})
    assert tools == {"cursor", "claude", "copilot", "gemini", "opencode"}


def test_merge_json_fill_missing():
    merged = merge_json_fill_missing({"a": 1}, {"a": 2, "b": 3})
    assert merged["a"] == 1
    assert merged["b"] == 3
