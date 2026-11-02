"""Record HTTP traffic in a separate Prometheus registry per application."""

from time import perf_counter

from flask import Flask, g, request
from prometheus_client import CollectorRegistry, Counter, Histogram


def register_metrics(app: Flask) -> None:
    """Count responses and observe duration without recording raw request URLs."""
    registry = CollectorRegistry()
    app.extensions["metrics_registry"] = registry
    labels = ("method", "path", "status")
    requests = Counter(
        "flask_http_request_total", "HTTP responses by route and status.", labels, registry=registry
    )
    duration = Histogram(
        "flask_http_request_duration_seconds",
        "HTTP request duration in seconds.",
        labels,
        registry=registry,
    )

    @app.before_request
    def start_timer():
        g.request_started = perf_counter()

    @app.after_request
    def record_response(response):
        # Scraping metrics should not count as application traffic.
        if request.endpoint != "main.metrics":
            path = request.url_rule.rule if request.url_rule is not None else "unmatched"
            method = request.method
            if method not in {"GET", "HEAD", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"}:
                method = "OTHER"
            values = (method, path, str(response.status_code))
            requests.labels(*values).inc()
            duration.labels(*values).observe(perf_counter() - g.request_started)
        return response
