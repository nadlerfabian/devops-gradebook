"""Entry point for Flask locally and Gunicorn in the container."""

from app import create_app

app = create_app()
