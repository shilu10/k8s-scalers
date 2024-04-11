import threading
import redis
import json

def redis_listener_worker(socketio, redis_client):
    pubsub = redis_client.pubsub()
    pubsub.subscribe("my_channel")

    for message in pubsub.listen():
        if message["type"] != "message":
            continue
        try:
            data = json.loads(message["data"].decode("utf-8"))
            job_id = data.get("job_id")
            status = data.get("status")
            if job_id and status:
                socketio.emit("status_update", {"job_id": job_id, "status": status}, room=job_id)
        except Exception as e:
            print("Error handling Redis message:", e)


def start_redis_listener(socketio, app):
    def run():
        with app.app_context():
            client = redis.Redis(
                host=app.config["REDIS_HOST"],
                port=app.config["REDIS_PORT"],
                db=app.config["REDIS_DB"]
            )
            redis_listener_worker(socketio, client)

    thread = threading.Thread(target=run, daemon=True)
    thread.start()
