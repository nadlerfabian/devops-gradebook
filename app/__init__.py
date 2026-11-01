"""Create and configure the Gradebook application."""

import os

from flask import Flask

from app.routes import bp


def create_app() -> Flask:
    """Build a new application instance."""
    app = Flask(__name__)
    app.config["APP_VERSION"] = os.environ.get("APP_VERSION", "0.0.0-dev")
    app.register_blueprint(bp)
    return app
