"""HTTP endpoints for Gradebook."""

from flask import Blueprint, Response, current_app, jsonify
from prometheus_client import CONTENT_TYPE_LATEST, generate_latest

bp = Blueprint("main", __name__)


@bp.get("/health")
def health():
    """Report process liveness without checking external dependencies."""
    return jsonify(status="ok", version=current_app.config["APP_VERSION"])


@bp.get("/ready")
def ready():
    """Check storage availability, returning 503 when it cannot serve requests."""
    try:
        available = current_app.extensions["repository"].healthy()
    except Exception:
        # Dependency exceptions may contain credentials; expose no details.
        current_app.logger.error("Storage readiness check failed")
        available = False
    if not available:
        return jsonify(status="not_ready"), 503
    return jsonify(status="ready")


@bp.get("/metrics")
def metrics():
    """Expose this application's HTTP measurements in Prometheus text format."""
    return Response(
        generate_latest(current_app.extensions["metrics_registry"]),
        content_type=CONTENT_TYPE_LATEST,
    )
