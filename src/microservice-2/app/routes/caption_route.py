import uuid, redis
from flask import current_app
from flask import request, jsonify, Blueprint
from flask_socketio import emit, join_room, leave_room
from flask import current_app as app
from ..schema.caption_schema import CaptionSchema
from ..core.response_builder import error_response, success_response
from ..core.clients.rabbitmq import get_rabbitmq_client


caption_bp = Blueprint("caption_bp", __name__)
caption_schema = CaptionSchema()


@caption_bp.route("/request", methods=["POST"])
def request_new_generation():
    request_data = request.get_json()
    headers = request.headers
    current_user = headers["X-User-Email"]

    try:
        caption_schema.load(request_data)
        app.logger.info("Caption Schema Validation Successful, %s", current_user)
    
    except Exception as err:
        app.logger.error("Caption schema validation failed: %s", str(err))
        return error_response(str(err), 400)
    
    job_id = str(uuid.uuid4())
    worker_message = {
        "job_id": job_id,
        "user": current_user,
        "video_url": request_data.get("video_url"),
    }

    rabbitmq_client = get_rabbitmq_client()
    rabbitmq_client.publish_message(worker_message)

    return success_response(data={"job_id": job_id}, status_code=200)


@caption_bp.route("/caption/status/<job_id>")
def get_caption_status(job_id):
    try:
        status = app.redis_client.get(str(job_id))
        if status is not None:
            status = status.decode("utf-8")
        return success_response(data={"status": status}, status_code=200)

    except Exception as err:
        return error_response(message={"err": str(err)}, status_code=500)


@caption_bp.route("/caption/result/<job_id>")
def get_caption_result(job_id):
    pass


# WebSocket: Events
from flask_socketio import SocketIO

@caption_bp.record_once
def setup_socketio(state):
    socketio: SocketIO = state.app.extensions["socketio"]

    @socketio.on("connect")
    def on_connect():
        emit("status_update", {"message": "Connected!"})
        print("Client connected")

    @socketio.on("disconnect")
    def on_disconnect():
        print("Client disconnected")

    @socketio.on("subscribe_job")
    def on_subscribe_job(data):
        job_id = data.get("job_id")
        if not job_id:
            emit("status_update", {"message": "Job ID is required!"})
            return
        join_room(job_id)
        print(f"Client joined room: {job_id}")
        status = app.redis_client.get(job_id)
        if status:
            emit("status_update", {"job_id": job_id, "status": status.decode("utf-8")}, room=job_id)

    @socketio.on("unsubscribe_job")
    def on_unsubscribe_job(data):
        job_id = data.get("job_id")
        if job_id:
            leave_room(job_id)
            print(f"Client left room: {job_id}")


