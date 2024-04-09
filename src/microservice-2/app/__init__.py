from flask import Flask
from flask_socketio import SocketIO
from .core.clients.rabbitmq import init_rabbitmq_connection, close_rabbitmq_connection
from .routes.caption_route import caption_bp
from .core.config import Config  # or your config class

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize WebSocket
    #socketio = SocketIO(app)

    # Initialize Redis and RabbitMQ
    with app.app_context():
        init_rabbitmq_connection()

    # Register Blueprints
    app.register_blueprint(caption_bp, url_prefix='/api/v1')

    # Teardown RabbitMQ and Redis on app context end
    @app.teardown_appcontext
    def shutdown_services(exception=None):
        close_rabbitmq_connection()

    # Return the app and socketio
    return app#, socketio
