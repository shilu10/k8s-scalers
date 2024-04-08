from flask import Flask 
from .routes.auth_route import auth_route
from flask_cors import CORS


def init_app():
    app = Flask(__name__)

    app.register_blueprint(auth_route)
    CORS(app, resources={r"/api/*": {"origins": ["http://localhost:3000", "http://localhost:8000"]}})

    return app 