"""Verify the public liveness response and configured application version."""

from app import create_app


def test_health_returns_ok_with_default_version(monkeypatch):
    monkeypatch.delenv("APP_VERSION", raising=False)
    app = create_app()
    app.config["TESTING"] = True
    client = app.test_client()

    response = client.get("/health")

    assert response.status_code == 200
    assert response.is_json
    assert response.get_json() == {"status": "ok", "version": "0.0.0-dev"}


def test_health_reports_version_from_environment(monkeypatch):
    monkeypatch.setenv("APP_VERSION", "1.2.3")
    app = create_app()
    app.config["TESTING"] = True
    client = app.test_client()

    response = client.get("/health")

    assert response.status_code == 200
    assert response.get_json() == {"status": "ok", "version": "1.2.3"}
