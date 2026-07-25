import app as app_module


def test_home_page_returns_200():
    app_module.app.config["TESTING"] = True
    client = app_module.app.test_client()

    response = client.get("/")

    assert response.status_code == 200


def test_analyze_endpoint_returns_json(monkeypatch):
    app_module.app.config["TESTING"] = True
    client = app_module.app.test_client()

    def fake_analyze(url):
        return {
            "status": 200,
            "response_time": "0.12 sec",
            "title": "Example",
            "meta_description": "Example description",
            "h1_count": 1,
            "missing_alt_images": 0,
            "word_count": 120,
            "favicon": "https://example.com/favicon.ico",
            "seo_score": 95,
        }

    monkeypatch.setattr(app_module, "analyze_website", fake_analyze)

    response = client.post(
        "/analyze",
        json={"url": "https://example.com"},
    )

    assert response.status_code == 200
    data = response.get_json()
    assert data["title"] == "Example"
    assert data["seo_score"] == 95
