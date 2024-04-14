import threading
import redis
import json


def redis_listener_worker(socketio, redis_client):
    """
    Worker function that listens to a Redis pub/sub channel and emits status updates via WebSocket.

    Args:
        socketio (SocketIO): Flask-SocketIO instance for emitting events.
        redis_client (redis.Redis): Redis client instance connected to the correct DB.

    Listens to:
        "my_channel" Redis channel for messages in the format:
        {
            "job_id": "some-uuid",
            "status": "Processed" | "Failed" | etc.
        }
    """
    pubsub = redis_client.pubsub()
    pubsub.subscribe("my_channel")

    for message in pubsub.listen():
        if message["type"] != "message":
            continue  # Skip non-message types like subscription confirmation

        try:
            # Parse message and emit it via SocketIO to the appropriate room
            data = json.loads(message["data"].decode("utf-8"))
            job_id = data.get("job_id")
            status = data.get("status")

            if job_id and status:
                socketio.emit("status_update", {"job_id": job_id, "status": status}, room=job_id)

        except json.JSONDecodeError as e:
            print("Failed to decode Redis message JSON:", e)
        except Exception as e:
            print("Unexpected error handling Redis message:", e)


def start_redis_listener(socketio, app):
    """
    Starts a background thread that runs the Redis listener.

    Args:
        socketio (SocketIO): Flask-SocketIO instance.
        app (Flask): Flask app instance to provide context.
    """
    def run():
        # Ensure app context is available inside thread
        with app.app_context():
            try:
                # Create Redis client with Flask config
                client = redis.Redis(
                    host=app.config["REDIS_HOST"],
                    port=app.config["REDIS_PORT"],
                    db=app.config["REDIS_DB"]
                )
                redis_listener_worker(socketio, client)
            except redis.RedisError as err:
                print("Redis connection error:", err)
            except Exception as e:
                print("Unhandled error in Redis listener thread:", e)

    # Launch thread as daemon so it exits with the app
    thread = threading.Thread(target=run, daemon=True)
    thread.start()
