from flask import Flask
from .core.config import Config
from .routes.home_route import home_bp
from .routes.producer_route import producer_bp
from .routes.stress_route import stress_bp


def create_app():
    app = Flask(__name__, template_folder="templates")

    app.config.from_object(Config)
    
    app.register_blueprint(home_bp)
    app.register_blueprint(producer_bp)
    app.register_blueprint(stress_bp)

    return app 