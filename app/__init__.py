"""Create and configure the Gradebook application."""

import os
from datetime import timedelta

from flask import Flask

from app.accounts import provision_demo_accounts
from app.auth import register_auth
from app.monitoring import register_metrics
from app.repository import InMemoryGradebookRepository
from app.routes import bp


def create_app(*, repository=None, config=None) -> Flask:
    """Build a new application instance."""
    app = Flask(__name__)
    app.config["APP_VERSION"] = os.environ.get("APP_VERSION", "0.0.0-dev")
    app.config.update(
        SECRET_KEY=os.environ.get("SECRET_KEY"),
        SESSION_COOKIE_HTTPONLY=True,
        SESSION_COOKIE_SAMESITE="Lax",
        SESSION_COOKIE_SECURE=os.environ.get("SESSION_COOKIE_SECURE", "false").lower() == "true",
        PERMANENT_SESSION_LIFETIME=timedelta(hours=2),
        MAX_CONTENT_LENGTH=16 * 1024,
        DEMO_LECTURER_PASSWORD=os.environ.get("DEMO_LECTURER_PASSWORD"),
        DEMO_STUDENT_PASSWORD=os.environ.get("DEMO_STUDENT_PASSWORD"),
    )
    if config is not None:
        app.config.update(config)
    app.extensions["repository"] = (
        repository if repository is not None else InMemoryGradebookRepository()
    )
    register_metrics(app)
    if repository is None:
        provision_demo_accounts(app)
    app.register_blueprint(bp)
    register_auth(app)
    return app
