from flask import Flask
from .routes.auth_route import auth_bp
from .routes.upload_route import upload_bp
from .routes.caption_route import caption_bp
from flask_cors import CORS
from .core.middelware import jwt_middleware
from .core.config import Config
from .core.logger import setup_logger


def init_app():
    app = Flask(__name__)

    app.config.from_object(Config)

    setup_logger(app)
    
    app.register_blueprint(upload_bp, url_prefix="/api/v1")
    app.register_blueprint(auth_bp, url_prefix="/api/v1")
    app.register_blueprint(caption_bp, url_prefix="/api/v1")

    CORS(app, resources={r"/api/*": {"origins": ["http://localhost:3000"]}})
    app.before_request(jwt_middleware)

    return app 