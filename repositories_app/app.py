from flask import Flask


def create_app():
    """Factory for creating app instances."""

    app = Flask(__name__)
    app.config.from_pyfile('config.py')

    return app
