from flask import Flask

from .views import github_blueprint


def create_app():
    """Factory for creating app instances."""

    app = Flask(__name__)
    app.config.from_pyfile('config.py')
    app.register_blueprint(github_blueprint,
                           url_prefix='/api/v1/github')

    return app
