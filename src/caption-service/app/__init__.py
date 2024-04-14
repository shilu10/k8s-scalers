from flask import Flask
from flask_socketio import SocketIO
from .core.clients.rabbitmq import init_rabbitmq_connection, close_rabbitmq_connection
from .routes.caption_route import caption_bp
from .routes.healthz_route import healthz_bp
from .routes.stress_route import stress_bp
from .core.config import Config
from .core.redis_listener import start_redis_listener
from .core.clients.mongo import get_mongo_client
from .core.logger import setup_logger
from pymongo import MongoClient
from redis import Redis
import atexit


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Setup logger
    setup_logger(app)

    # Initialize WebSocket
    socketio = SocketIO(app, cors_allowed_origins="*")

    # Initialize RabbitMQ
    with app.app_context():
        init_rabbitmq_connection()

    # Register Blueprints
    app.register_blueprint(caption_bp, url_prefix='/api/v1')
    app.register_blueprint(healthz_bp, url_prefix="/api/v1")
    app.register_blueprint(stress_bp, url_prefix="/api/v1")

    # Teardown RabbitMQ only
    @app.teardown_appcontext
    def shutdown_services(exception=None):
        close_rabbitmq_connection()

    # Start Redis pub-sub listener in background
    start_redis_listener(socketio, app)

    # Redis client
    app.redis_client = Redis(
        host=app.config["REDIS_HOST"],
        port=app.config["REDIS_PORT"],
        db=app.config["REDIS_DB"]
    )

    # MongoDB client
    app.mongo_client = get_mongo_client(app.config.get("MONGO_URI"))

    if not isinstance(app.mongo_client, MongoClient):
        raise RuntimeError("MongoDB client is not initialized properly")

    # Ensure MongoDB client is closed only when the app fully exits
    atexit.register(lambda: app.mongo_client.close())

    # Logging
    app.logger.info("MongoDB client initialized properly")
    app.logger.info("RabbitMQ and Redis clients initialized")

    return app, socketio
