from flask import Flask
from .routes.health_route import health_bp
from .routes.login_route import login_bp
from .routes.signup_route import signup_bp
from .core.config import Config
from .core.extensions import db
from flask_cors import CORS


def init_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)

    with app.app_context():
        db.create_all()

    app.register_blueprint(login_bp)
    app.register_blueprint(health_bp)
    app.register_blueprint(signup_bp)

    return app 