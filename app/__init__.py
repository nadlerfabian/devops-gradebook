"""Create and configure the Gradebook application."""

import os

from flask import Flask

from app.monitoring import register_metrics
from app.repository import InMemoryGradebookRepository
from app.routes import bp


def create_app(*, repository=None) -> Flask:
    """Build a new application instance."""
    app = Flask(__name__)
    app.config["APP_VERSION"] = os.environ.get("APP_VERSION", "0.0.0-dev")
    app.extensions["repository"] = (
        repository if repository is not None else InMemoryGradebookRepository()
    )
    register_metrics(app)
    app.register_blueprint(bp)
    return app
