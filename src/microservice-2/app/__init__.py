from flask import Flask
from flask_socketio import SocketIO
from .core.clients.rabbitmq import init_rabbitmq_connection, close_rabbitmq_connection
from .routes.caption_route import caption_bp
from .core.config import Config  # or your config class
from .core.redis_listener import start_redis_listener


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize WebSocket
    socketio = SocketIO(app, cors_allowed_origins="*")

    # Initialize Redis and RabbitMQ
    with app.app_context():
        init_rabbitmq_connection()

    # Register Blueprints
    app.register_blueprint(caption_bp, url_prefix='/api/v1')

    # Teardown RabbitMQ and Redis on app context end
    @app.teardown_appcontext
    def shutdown_services(exception=None):
        close_rabbitmq_connection()

    # Start Redis pub-sub listener in background
    start_redis_listener(socketio, app)


    from redis import Redis
    app.redis_client = Redis(
        host=app.config["REDIS_HOST"],
        port=app.config["REDIS_PORT"],
        db=app.config["REDIS_DB"]
    )

    # Return the app and socketio
    return app, socketio
