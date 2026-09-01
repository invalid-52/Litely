"""Unit tests for deterministic LanguageDetectionService."""

from litely.services.detector import LanguageDetectionService


def test_detect_by_file_extension():
    res = LanguageDetectionService.detect("let x = 1;", filename="test.ts")
    assert res["detected"] is True
    assert res["language_id"] == "typescript"
    assert res["confidence"] >= 0.9


def test_detect_by_shebang():
    code = "#!/usr/bin/env python3\nprint('Hello from script')"
    res = LanguageDetectionService.detect(code)
    assert res["detected"] is True
    assert res["language_id"] == "python"


def test_detect_by_keywords_python():
    code = "def calculate_sum(a, b):\n    return a + b\n\nif __name__ == '__main__':\n    import sys"
    res = LanguageDetectionService.detect(code)
    assert res["detected"] is True
    assert res["language_id"] == "python"


def test_detect_by_keywords_sql():
    code = "SELECT id, email, created_at FROM users WHERE active = true GROUP BY id;"
    res = LanguageDetectionService.detect(code)
    assert res["detected"] is True
    assert res["language_id"] == "sql"


def test_detect_by_keywords_rust():
    code = "fn main() {\n    let mut count = 0;\n    println!(\"Count: {}\", count);\n}"
    res = LanguageDetectionService.detect(code)
    assert res["detected"] is True
    assert res["language_id"] == "rust"


def test_detect_empty_or_whitespace():
    res = LanguageDetectionService.detect("   \n\t  ")
    assert res["detected"] is False
    assert res["language_id"] is None
