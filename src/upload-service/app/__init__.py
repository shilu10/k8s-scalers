from flask import Flask
from .core.config import Config
from .routes.stress_route import stress_bp
from .routes.health_route import health_bp
from .routes.presigned_url_route import presigned_url_bp
from .routes.multipart_complete_route import multipart_complete_bp
from .core.logger import setup_logger


def create_app():
    app = Flask(__name__)

    app.config.from_object(Config)

    setup_logger(app)

    app.register_blueprint(health_bp, url_prefix="/api/v1")
    app.register_blueprint(stress_bp, url_prefix="/api/v1")
    app.register_blueprint(presigned_url_bp, url_prefix="/api/v1")
    app.register_blueprint(multipart_complete_bp, url_prefix="/api/v1")
    
    return app 