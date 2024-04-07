from flask import Flask
from .routes.health_route import health_bp
from .routes.login_route import login_bp
from .routes.signup_route import signup_bp
from .routes.logout_route import logout_bp
from .core.config import Config
from .core.extensions import db, jwt
from flask_cors import CORS
from .core.middleware import jwt_middleware
from .core.logger import setup_logger


def init_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    app.before_request(jwt_middleware)

    CORS(app, resources={r"/api/*": {"origins": ["http://localhost:3000", "https://yourfrontend.com"]}})

    setup_logger(app)

    # sqlalchemy initialization
    db.init_app(app)
    # jwt initialization
    jwt.init_app(app)

    with app.app_context():
        db.create_all()

    app.register_blueprint(login_bp)
    app.register_blueprint(health_bp)
    app.register_blueprint(signup_bp)
    app.register_blueprint(logout_bp)

    return app 