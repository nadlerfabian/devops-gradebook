"""Check readiness failures, application isolation, and observable HTTP traffic."""

import pytest
from prometheus_client.parser import text_string_to_metric_families

from app import create_app


def samples(response):
    """Parse the public exposition rather than inspecting private counter state."""
    return [
        sample
        for family in text_string_to_metric_families(response.get_data(as_text=True))
        for sample in family.samples
    ]


def test_default_storage_is_ready_and_shared_within_app():
    app = create_app()
    repository = app.extensions["repository"]
    client = app.test_client()

    response = client.get("/ready")

    assert response.status_code == 200
    assert response.get_json() == {"status": "ready"}
    assert app.extensions["repository"] is repository
    assert create_app().extensions["repository"] is not repository


@pytest.mark.parametrize("raises", [False, True])
def test_unavailable_storage_returns_503_but_health_remains_ok(raises):
    class UnavailableRepository:
        def healthy(self):
            if raises:
                raise ConnectionError("private dependency details")
            return False

    app = create_app(repository=UnavailableRepository())
    app.config["TESTING"] = True
    client = app.test_client()

    response = client.get("/ready")

    assert response.status_code == 503
    assert response.get_json() == {"status": "not_ready"}
    assert "private" not in response.get_data(as_text=True)
    assert client.get("/health").status_code == 200

    measurements = samples(client.get("/metrics"))
    assert any(
        item.name == "flask_http_request_total"
        and item.labels == {"method": "GET", "path": "/ready", "status": "503"}
        and item.value == 1
        for item in measurements
    )


def test_metrics_expose_request_count_and_duration_and_exclude_scrapes():
    client = create_app().test_client()
    client.get("/health")
    client.get("/health")
    client.get("/metrics")

    response = client.get("/metrics")
    measurements = samples(response)
    expected_labels = {"method": "GET", "path": "/health", "status": "200"}

    assert response.status_code == 200
    assert response.content_type.startswith("text/plain;")
    for name in ("flask_http_request_total", "flask_http_request_duration_seconds_count"):
        assert any(
            item.name == name and item.labels == expected_labels and item.value == 2
            for item in measurements
        )
    assert any(
        item.name == "flask_http_request_duration_seconds_sum"
        and item.labels == expected_labels
        and item.value >= 0
        for item in measurements
    )
    assert any(item.name == "flask_http_request_duration_seconds_bucket" for item in measurements)
    assert all(item.labels.get("path") != "/metrics" for item in measurements)


def test_metrics_group_missing_urls_and_unknown_methods():
    client = create_app().test_client()
    client.get("/missing/student-one?password=private")
    client.get("/missing/student-two")
    client.open("/missing", method="CUSTOM")

    response = client.get("/metrics")
    measurements = samples(response)

    assert any(
        item.name == "flask_http_request_total"
        and item.labels == {"method": "GET", "path": "unmatched", "status": "404"}
        and item.value == 2
        for item in measurements
    )
    assert any(item.labels.get("method") == "OTHER" for item in measurements)
    assert "student-one" not in response.get_data(as_text=True)
    assert "private" not in response.get_data(as_text=True)


def test_metrics_use_route_templates_and_record_server_errors():
    app = create_app()
    app.config.update(TESTING=True, PROPAGATE_EXCEPTIONS=False)

    @app.get("/example/<int:record_id>")
    def example(record_id):
        raise RuntimeError("Example failure")

    client = app.test_client()
    assert client.get("/example/12345").status_code == 500
    measurements = samples(client.get("/metrics"))

    assert any(
        item.name == "flask_http_request_total"
        and item.labels == {"method": "GET", "path": "/example/<int:record_id>", "status": "500"}
        and item.value == 1
        for item in measurements
    )


def test_metrics_are_isolated_between_app_instances():
    first = create_app().test_client()
    second = create_app().test_client()
    first.get("/health")

    assert any(item.name == "flask_http_request_total" for item in samples(first.get("/metrics")))
    assert not any(
        item.name == "flask_http_request_total" for item in samples(second.get("/metrics"))
    )
