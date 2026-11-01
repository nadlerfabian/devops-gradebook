"""HTTP endpoints for Gradebook."""
import os
from flask import Blueprint, current_app, jsonify

bp = Blueprint("main", __name__)


@bp.get("/health")
def health():
    """Report process liveness without checking external dependencies."""
    return jsonify(status="ok", version=current_app.config["APP_VERSION"])
