from flask import Flask
from .routes.auth_route import auth_bp
from .routes.upload_route import upload_bp
from .routes.caption_route import caption_bp
from flask_cors import CORS
from .core.middelware import jwt_middleware
from .core.config import Config


def init_app():
    app = Flask(__name__)

    app.config.from_object(Config)

    app.register_blueprint(upload_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(caption_bp)
    CORS(app, resources={r"/api/*": {"origins": ["http://localhost:3000"]}})
    app.before_request(jwt_middleware)

    
    return app 