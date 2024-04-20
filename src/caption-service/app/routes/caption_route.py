import uuid, redis
from flask import current_app
from flask import request, jsonify, Blueprint
from flask_socketio import emit, join_room, leave_room
from flask import current_app as app
from ..schema.caption_schema import CaptionSchema
from ..core.response_builder import error_response, success_response
from ..core.clients.rabbitmq import get_rabbitmq_client
from pymongo.errors import PyMongoError


caption_bp = Blueprint("caption_bp", __name__)
caption_schema = CaptionSchema()


@caption_bp.route("/caption/request", methods=["POST"])
def request_new_generation():
    """
    Endpoint to request a new caption generation job.

    - Validates the incoming request using the CaptionSchema.
    - Generates a unique job ID.
    - Publishes the job to a RabbitMQ worker.
    - Returns the job ID to the client.

    Returns:
        JSON response with job ID or error message.
    """
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

    #rabbitmq_client = get_rabbitmq_client()
    app.rabbitmq_client.publish_message(worker_message)

    return success_response(data={"job_id": job_id}, status_code=200)


@caption_bp.route("/caption/status/<job_id>")
def get_caption_status(job_id):
    """
    Endpoint to get the status of a caption job.

    Args:
        job_id (str): Unique identifier of the caption job.

    Returns:
        JSON response with the current status or error.
    """
    try:
        status = app.redis_client.get(str(job_id))
        if status is not None:
            status = status.decode("utf-8")
        return success_response(data={"status": status}, status_code=200)

    except Exception as err:
        return error_response(message={"err": str(err)}, status_code=500)


@caption_bp.route("/caption/result/<job_id>")
def get_caption_result(job_id):
    """
    Endpoint to retrieve the result (transcript) of a processed caption job.

    Args:
        job_id (str): Unique identifier of the caption job.

    Returns:
        JSON response with the transcript or appropriate error message.
    """
    try:
        current_status = app.redis_client.get(job_id)
        current_status = current_status.decode('utf-8')
        app.logger.info("current_status, %s", current_status)
        
        if str(current_status).upper() != "PROCESSED":
            return error_response(message="Processing of video is not completed", status_code=400)
        
        app.logger.info("job_id, %s", job_id)
        mongo_client = app.mongo_client
        database = mongo_client.get_database(app.config["MONGO_DB"])
        collection = database.get_collection(app.config["MONGO_COLLECTION"])

        transcript = collection.find_one({"job_id": str(job_id)})

        if not transcript:
            return error_response(message="Transcript not found", status_code=404)
        
        data = transcript.get("transcript")
        app.logger.info("transcript, %s", data)

        return success_response(data={"transcript": data}, status_code=200)

    except PyMongoError as e:
        app.logger.error(f"MongoDB Error: {e}")
        return error_response(message="Database error", status_code=500)

    except Exception as e:
        app.logger.exception(f"Unhandled error: {e}")
        return error_response(message="Internal server error", status_code=500)


# WebSocket: Events
from flask_socketio import SocketIO

@caption_bp.record_once
def setup_socketio(state):
    """
    Initializes and registers WebSocket event handlers for caption job status updates.

    Events:
        - connect: Client successfully connects.
        - disconnect: Client disconnects.
        - subscribe_job: Client subscribes to a specific job room.
        - unsubscribe_job: Client leaves a specific job room.

    Args:
        state: The application state, providing access to the app instance.
    """
    socketio: SocketIO = state.app.extensions["socketio"]

    @socketio.on("connect")
    def on_connect():
        """Handles a new WebSocket connection."""
        emit("status_update", {"message": "Connected!"})
        print("Client connected")

    @socketio.on("disconnect")
    def on_disconnect():
        """Handles WebSocket disconnection."""
        print("Client disconnected")

    @socketio.on("subscribe_job")
    def on_subscribe_job(data):
        """
        Handles subscription to a specific job's WebSocket room.

        Args:
            data (dict): Contains the job_id to subscribe to.
        """
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
        """
        Handles unsubscription from a job's WebSocket room.

        Args:
            data (dict): Contains the job_id to unsubscribe from.
        """
        job_id = data.get("job_id")
        if job_id:
            leave_room(job_id)
            print(f"Client left room: {job_id}")
