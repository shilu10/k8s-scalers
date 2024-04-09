from flask import Flask
from .routes.health_route import health_bp
from .routes.login_route import login_bp
from .routes.signup_route import signup_bp
from .routes.logout_route import logout_bp
from .routes.refresh_route import  refresh_bp
from .routes.validate_route import validate_bp
from .core.config import Config
from .core.extensions import db, jwt
from flask_cors import CORS
from .core.middleware import jwt_middleware
from .core.logger import setup_logger


def init_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    #app.before_request(jwt_middleware)

    CORS(app, resources={r"/api/*": {"origins": ["http://localhost:3000", "http://localhost:8000"]}})

    setup_logger(app)

    db.init_app(app)
    jwt.init_app(app)

    with app.app_context():
        db.create_all()

    app.register_blueprint(login_bp, url_prefix="/api/v1")
    app.register_blueprint(health_bp, url_prefix="/api/v1")
    app.register_blueprint(signup_bp, url_prefix="/api/v1")
    app.register_blueprint(logout_bp, url_prefix="/api/v1")
    app.register_blueprint(refresh_bp, url_prefix="/api/v1")
    app.register_blueprint(validate_bp, url_prefix="/api/v1")

    return app 