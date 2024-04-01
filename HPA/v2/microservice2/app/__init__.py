from flask import Flask
#from ..config import * 
from .routes.home_route import home_bp
from .routes.cpu_route import cpu_bp
from .routes.memory_route import memory_bp
from .routes.replica_route import replica_bp


def create_app():
    app = Flask(__name__)


    # Register Blueprints
    app.register_blueprint(home_bp)
    app.register_blueprint(cpu_bp)
    app.register_blueprint(memory_bp)
    app.register_blueprint(replica_bp)

    return app