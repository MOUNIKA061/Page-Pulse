import requests
import website_parser


def test_invalid_url_returns_error():
    result = website_parser.analyze_website("not-a-url")
    assert result["error"] == "Invalid URL"


def test_non_html_response_returns_error(monkeypatch):
    class DummyResponse:
        headers = {"Content-Type": "application/json"}

    def fake_get(*args, **kwargs):
        return DummyResponse()

    monkeypatch.setattr(website_parser.requests, "get", fake_get)
    result = website_parser.analyze_website("https://example.com")
    assert result["error"] == "This is not an HTML page"


def test_timeout_returns_error(monkeypatch):
    def fake_get(*args, **kwargs):
        raise requests.exceptions.Timeout("timed out")

    monkeypatch.setattr(website_parser.requests, "get", fake_get)
    result = website_parser.analyze_website("https://example.com")
    assert result["error"] == "Request Timed Out"
