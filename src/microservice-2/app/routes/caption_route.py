import uuid
from flask import request, jsonify, Blueprint
from flask import current_app as app
from ..schema.caption_schema import CaptionSchema
from ..core.response_builder import error_response, success_response
from ..core.clients.rabbitmq import get_rabbitmq_client
from ..core.clients.redis import get_redis_client


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
        redis_client = get_redis_client(
            app.config["REDIS_HOST"],
            app.config["REDIS_PORT"],
            app.config["REDIS_DB"]
        )
        status = redis_client.get(str(job_id))
        if status is not None:
            status = status.decode("utf-8")
        return success_response(data={"status": status}, status_code=200)

    except Exception as err:
        return error_response(message={"err": str(err)}, status_code=500)



@caption_bp.route("/caption/result/<job_id>")
def get_caption_result(job_id):
    pass



