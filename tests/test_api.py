"""Integration tests for REST API v1 endpoints and legacy compatibility."""

import pytest
import json
from litely import create_app


@pytest.fixture
def client():
    app = create_app("testing")
    with app.test_client() as client:
        yield client


def test_health_endpoint(client):
    res = client.get("/api/v1/health")
    assert res.status_code == 200
    data = res.get_json()
    assert data["success"] is True
    assert data["data"]["status"] == "healthy"
    assert data["data"]["languages_count"] > 20


def test_languages_endpoint(client):
    res = client.get("/api/v1/languages")
    assert res.status_code == 200
    data = res.get_json()
    assert data["success"] is True
    assert len(data["data"]["languages"]) > 0


def test_themes_endpoint(client):
    res = client.get("/api/v1/themes")
    assert res.status_code == 200
    data = res.get_json()
    assert data["success"] is True
    assert "dark" in data["data"]
    assert "light" in data["data"]


def test_highlight_endpoint(client):
    payload = {
        "code": "def test():\n    return 42",
        "language": "python",
        "theme": "dracula",
        "filename": "test.py",
        "visualization": {
            "show_line_numbers": True,
            "font_size": 15,
        }
    }
    res = client.post("/api/v1/highlight", json=payload)
    assert res.status_code == 200
    data = res.get_json()
    assert data["success"] is True
    assert "litely-card" in data["data"]["html"]
    assert data["data"]["total_lines"] == 2


def test_detect_language_endpoint(client):
    payload = {
        "code": "SELECT * FROM orders WHERE total > 100;",
    }
    res = client.post("/api/v1/detect-language", json=payload)
    assert res.status_code == 200
    data = res.get_json()
    assert data["success"] is True
    assert data["data"]["detected"] is True
    assert data["data"]["language_id"] == "sql"


def test_export_endpoint_html(client):
    payload = {
        "code": "console.log('test')",
        "language": "javascript",
        "format": "html",
    }
    res = client.post("/api/v1/export", json=payload)
    assert res.status_code == 200
    data = res.get_json()
    assert data["success"] is True
    assert "<!DOCTYPE html>" in data["data"]["content"]


def test_export_endpoint_svg(client):
    payload = {
        "code": "console.log('test')",
        "language": "javascript",
        "format": "svg",
    }
    res = client.post("/api/v1/export", json=payload)
    assert res.status_code == 200
    data = res.get_json()
    assert data["success"] is True
    assert "<svg" in data["data"]["content"]


def test_invalid_export_format(client):
    payload = {
        "code": "test",
        "format": "invalid_format",
    }
    res = client.post("/api/v1/export", json=payload)
    assert res.status_code == 400
    data = res.get_json()
    assert data["success"] is False
    assert data["error"]["code"] == "INVALID_PAYLOAD"


def test_legacy_api_compatibility(client):
    res = client.get("/api?code=print('hello')&lexer=python")
    assert res.status_code == 200
    assert "litely-card" in res.get_data(as_text=True)


def test_web_index_loads(client):
    res = client.get("/")
    assert res.status_code == 200
    text = res.get_data(as_text=True)
    assert "LITELY" in text
    assert "Beautiful code. Instantly." in text


def test_security_headers(client):
    res = client.get("/")
    assert res.status_code == 200
    assert "Content-Security-Policy" in res.headers
    assert res.headers["X-Content-Type-Options"] == "nosniff"


def test_malicious_visualization_is_sanitized(client):
    payload = {
        "code": "print(42)",
        "language": "python",
        "visualization": {
            "font_family": "JetBrains Mono; color:red;",
            "font_size": "9999",
            "padding": -50,
            "background_value": "red; background-image:url(javascript:alert(1))",
        },
    }
    res = client.post("/api/v1/highlight", json=payload)
    assert res.status_code == 200
    data = res.get_json()["data"]
    assert "javascript:" not in data["html"].lower()
    assert "9999px" not in data["html"]


def test_404_error_contract(client):
    res = client.get("/api/v1/nonexistent_route")
    assert res.status_code == 404
    data = res.get_json()
    assert data["success"] is False
    assert data["data"] is None
    assert data["error"]["code"] == "NOT_FOUND"


def test_all_themes_highlight(client):
    from litely.core.themes import ThemeRegistry
    for theme in ThemeRegistry.list_all():
        res = client.post("/api/v1/highlight", json={
            "code": "print('theme test')",
            "language": "python",
            "theme": theme.id,
        })
        assert res.status_code == 200
        data = res.get_json()
        assert data["success"] is True
        assert theme.id in data["data"]["theme"]


def test_highlight_auto_detect(client):
    res = client.post("/api/v1/highlight", json={
        "code": "package main\nimport \"fmt\"\nfunc main() { fmt.Println(1) }",
        "language": "auto",
    })
    assert res.status_code == 200
    data = res.get_json()
    assert data["success"] is True
    assert data["data"]["language"] == "go"

