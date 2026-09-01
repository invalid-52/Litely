"""Unit tests for CodeDocument and VisualizationSettings."""

import pytest
from litely.core.document import CodeDocument, VisualizationSettings
from litely.core.languages import LanguageRegistry
from litely.core.themes import ThemeRegistry


def test_code_document_initialization():
    doc = CodeDocument(
        source="def hello():\n    print('world')",
        language="python",
        filename="hello.py",
        theme="dracula",
    )
    assert doc.source.startswith("def hello():")
    assert doc.language == "python"
    assert doc.filename == "hello.py"
    assert doc.theme == "dracula"
    assert doc.metadata["line_count"] == 2
    assert doc.metadata["char_count"] > 0
    assert doc.visualization.font_family == "JetBrains Mono"
    assert doc.visualization.show_line_numbers is True


def test_code_document_serialization():
    doc = CodeDocument(
        source="const x = 10;",
        language="typescript",
        visualization=VisualizationSettings(
            font_size=16,
            window_chrome="windows",
            padding=40,
        ),
    )
    d = doc.to_dict()
    assert d["source"] == "const x = 10;"
    assert d["language"] == "typescript"
    assert d["visualization"]["font_size"] == 16
    assert d["visualization"]["window_chrome"] == "windows"

    # Deserialize back
    restored = CodeDocument.from_dict(d)
    assert restored.source == doc.source
    assert restored.language == doc.language
    assert restored.visualization.font_size == 16


def test_language_registry():
    py = LanguageRegistry.get("python")
    assert py is not None
    assert py.display_name == "Python"
    assert ".py" in py.extensions

    # Test alias lookup
    ts = LanguageRegistry.get("ts")
    assert ts is not None
    assert ts.id == "typescript"

    # Test extension lookup
    rs = LanguageRegistry.get_by_extension(".rs")
    assert rs is not None
    assert rs.id == "rust"


def test_theme_registry():
    gh_dark = ThemeRegistry.get("github-dark")
    assert gh_dark is not None
    assert gh_dark.category == "dark"
    assert len(gh_dark.swatches) > 0

    # Test fallback resolve
    unknown = ThemeRegistry.resolve("non-existent-theme-id")
    assert unknown.id == "github-dark"
