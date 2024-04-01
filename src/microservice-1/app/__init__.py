from flask import Flask
from .routes.home_route import home_bp
from .routes.producer_route import producer_bp


def create_app():
    app = Flask(__name__)

    app.register_blueprint(home_bp)
    app.register_blueprint(producer_bp)

    return app 