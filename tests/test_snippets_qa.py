"""Comprehensive QA tests covering real-world language scenarios, large files, and exports."""

import pytest
from litely.core.document import CodeDocument, VisualizationSettings
from litely.services.highlighter import HighlightService
from litely.services.detector import LanguageDetectionService
from litely.services.exporter import ExportService


def test_qa_python_snippet():
    code = 'def hello():\n    print("Hello, LITELY!")'
    doc = CodeDocument(source=code, language="python", theme="github-dark")
    res = HighlightService.highlight_document(doc)
    assert res["html"] is not None
    assert "Hello, LITELY!" in res["html"]
    assert res["word_html"] is not None


def test_qa_javascript_snippet():
    code = 'const greet = name => `Hello, ${name}!`;'
    doc = CodeDocument(source=code, language="javascript", theme="dracula")
    res = HighlightService.highlight_document(doc)
    assert res["html"] is not None
    assert "greet" in res["html"]


def test_qa_typescript_snippet():
    code = 'interface User {\n  name: string;\n}'
    doc = CodeDocument(source=code, language="typescript", theme="tokyo-night")
    res = HighlightService.highlight_document(doc)
    assert res["html"] is not None
    assert "User" in res["html"]


def test_qa_rust_snippet():
    code = 'fn main() {\n    let mut map = std::collections::HashMap::new();\n    println!("Rust in LITELY");\n}'
    doc = CodeDocument(source=code, language="rust", theme="monokai")
    res = HighlightService.highlight_document(doc)
    assert "HashMap" in res["html"]
    assert res["total_lines"] == 4


def test_qa_go_snippet():
    code = 'package main\nimport "fmt"\nfunc main() {\n    fmt.Println("Go Worker Pool")\n}'
    doc = CodeDocument(source=code, language="go", theme="colorful")
    res = HighlightService.highlight_document(doc)
    assert "package" in res["html"]
    assert res["total_lines"] == 5


def test_qa_sql_snippet():
    code = 'SELECT id, name\nFROM users\nWHERE active = true;'
    doc = CodeDocument(source=code, language="sql", theme="nord")
    res = HighlightService.highlight_document(doc)
    assert res["html"] is not None
    assert "SELECT" in res["html"]


def test_qa_unicode_and_emojis():
    code = '# 🚀 Litely supports unicode: 你好，世界！ café naïve 🐍\nname = "Antigravity ✨"'
    doc = CodeDocument(source=code, language="python", theme="one-dark")
    res = HighlightService.highlight_document(doc)
    assert "🚀" in res["html"]
    assert "你好，世界！" in res["html"]
    assert "✨" in res["html"]


def test_qa_500_plus_lines():
    lines = [f"// Line {i}: function process_{i}() {{ return {i} * 2; }}" for i in range(500)]
    code = "\n".join(lines)
    doc = CodeDocument(
        source=code,
        language="javascript",
        theme="github-dark",
        visualization=VisualizationSettings(word_wrap=True),
    )
    res = HighlightService.highlight_document(doc)
    assert res["total_lines"] == 500
    assert "litely-wrap" in res["html"]


def test_qa_svg_and_html_exports():
    import xml.etree.ElementTree as ET
    
    test_cases = [
        ("def test_export():\n    pass", "python", "github-dark"),
        ("const x = 1;\n\n// empty line above\nconsole.log(x);", "javascript", "dracula"),
        ("SELECT * FROM users\nWHERE age > 21\n  AND status = 'active';", "sql", "nord"),
        ("# 🚀 Unicode & Emojis: 你好 <tag> &amp; 'quote'", "python", "one-dark"),
        ("fn main() {\n\n\n    println!(\"Rust\");\n}", "rust", "colorful"),
    ]

    for source, lang, theme in test_cases:
        doc = CodeDocument(
            source=source,
            language=lang,
            filename=f"export_{lang}.test",
            theme=theme,
        )
        html_out = ExportService.export_standalone_html(doc)
        assert "<!DOCTYPE html>" in html_out
        assert f"export_{lang}.test" in html_out

        svg_out = ExportService.export_svg(doc)
        assert "<svg" in svg_out
        assert f"export_{lang}.test" in svg_out

        # Parse with strict XML parser to guarantee 100% valid XML
        tree = ET.fromstring(svg_out)
        assert tree.tag.endswith("svg")
        assert tree.attrib["width"] == "800"
