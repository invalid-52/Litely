"""Security and edge case validation tests."""

import pytest
from litely import create_app
from litely.config import Config


@pytest.fixture
def client():
    app = create_app("testing")
    with app.test_client() as client:
        yield client


def test_oversized_code_rejection(client):
    oversized = "a" * (Config.MAX_CODE_LENGTH + 100)
    payload = {
        "code": oversized,
        "language": "python",
    }
    res = client.post("/api/v1/highlight", json=payload)
    assert res.status_code == 400
    data = res.get_json()
    assert data["success"] is False
    assert "exceeds maximum allowed limit" in data["error"]["message"]


def test_malformed_json_payload(client):
    res = client.post(
        "/api/v1/highlight",
        data="not a json string",
        content_type="application/json",
    )
    assert res.status_code == 400
    data = res.get_json()
    assert data["success"] is False


def test_html_and_css_injection_safety(client):
    malicious = '</pre><script>alert("xss")</script><style>body{display:none;}</style>'
    payload = {
        "code": malicious,
        "language": "html",
    }
    res = client.post("/api/v1/highlight", json=payload)
    assert res.status_code == 200
    html_out = res.get_json()["data"]["html"]
    assert "<script>" not in html_out
    assert "&lt;" in html_out
    assert "&gt;" in html_out
