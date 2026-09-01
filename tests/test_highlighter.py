"""Unit tests for HighlightService."""

from litely.core.document import CodeDocument, VisualizationSettings
from litely.services.highlighter import HighlightService


def test_highlight_python():
    doc = CodeDocument(
        source="def greet(name):\n    return f'Hello, {name}'",
        language="python",
        theme="github-dark",
    )
    result = HighlightService.highlight_document(doc)
    assert result["html"] is not None
    assert "litely-card" in result["html"]
    assert "theme-github-dark" in result["html"]
    assert "litely-line" in result["html"]
    assert result["total_lines"] == 2
    assert "word_html" in result
    assert "<table" in result["word_html"]


def test_highlight_line_numbers_toggle():
    doc_with_lines = CodeDocument(
        source="line1\nline2\nline3",
        visualization=VisualizationSettings(show_line_numbers=True),
    )
    res_with = HighlightService.highlight_document(doc_with_lines)
    assert "litely-gutter" in res_with["html"]
    assert "<table" in res_with["word_html"]

    doc_without_lines = CodeDocument(
        source="line1\nline2\nline3",
        visualization=VisualizationSettings(show_line_numbers=False),
    )
    res_without = HighlightService.highlight_document(doc_without_lines)
    assert "litely-gutter" not in res_without["html"]
    assert "<div style=" in res_without["word_html"]


def test_highlight_line_highlighting():
    doc = CodeDocument(
        source="line1\nline2\nline3",
        visualization=VisualizationSettings(highlight_lines=[2]),
    )
    res = HighlightService.highlight_document(doc)
    assert "litely-line-highlight" in res["html"]


def test_highlight_xss_escaping():
    malicious_code = '<script>alert("XSS")</script>'
    doc = CodeDocument(
        source=malicious_code,
        language="html",
    )
    res = HighlightService.highlight_document(doc)
    # Ensure unescaped tag is strictly absent
    assert "<script>" not in res["html"]
    # Ensure HTML brackets are safely escaped
    assert "&lt;" in res["html"]
    assert "&gt;" in res["html"]
