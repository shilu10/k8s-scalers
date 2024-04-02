from flask import Flask
from .routes.home_route import home_bp
from .routes.stress_route import stress_bp


def create_app():
    app = Flask(__name__)

    app.register_blueprint(home_bp)
    app.register_blueprint(stress_bp)

    return app 