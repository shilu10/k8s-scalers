from flask import Flask
from .core.config import Config
from .routes.home_route import home_bp
from .routes.upload_route import upload_bp
from .routes.stress_route import stress_bp
from .routes.health_route import health_bp
from .routes.presigned_url_route import presigned_url_bp
from .routes.multi_part_upload_route import multipart_upload_bp
from .core.logger import setup_logger


def create_app():
    app = Flask(__name__, template_folder="templates")

    app.config.from_object(Config)

    
    
    app.register_blueprint(health_bp, url_prefix="/api/v1")
    #app.register_blueprint(home_bp)
    #app.register_blueprint(producer_bp)
    #app.register_blueprint(stress_bp)
    app.register_blueprint(presigned_url_bp, url_prefix="/api/v1")
    app.register_blueprint(multipart_upload_bp, url_prefix="/api/v1")
    setup_logger(app)

    return app 