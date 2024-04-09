import uuid
import os 
import json
from flask import Blueprint, jsonify, render_template, request, current_app
from marshmallow import ValidationError
from werkzeug.utils import secure_filename
from ..schema.metadata_schema import MetadataSchema
from ..services.s3_service import upload_to_bucket
from ..services.redis_service import put_object
from ..services.rabbitmq_service import publish_message

# blueprint
producer_bp = Blueprint("producer_bp",  __name__)

# schema validation
metadata_schema = MetadataSchema()

@producer_bp.route("/api/v1/upload_video", methods=["POST"])
def post_message():

    # 1. check the schema
    try:
        video_metadata = request.form
        schema_validation = metadata_schema.load(video_metadata)

    except ValidationError as err:
        return jsonify(err.messages), 400
    
    # 2. Get the file
    video_file = request.files.get('video')
    if not video_file:
        return jsonify({"error": "No video file provided"}), 400
    
    filename = secure_filename(video_file.filename)

    # saving it into s3
    try:
        bucket_response = upload_to_bucket(filename, video_file)
        if not bucket_response.get("success"):
            return jsonify({
                "err": bucket_response.get("reason")
            }), 500

        job_id = str(uuid.uuid4())

        # job status
        redis_response = put_object(job_id=job_id)
        if not redis_response.get("success"):
            return jsonify({
                "err": redis_response.get("reason")
            }), 500

        rabbitmq_response = publish_message(job_id, filename)
        if not rabbitmq_response.get("success"):
            return jsonify({
                "err": rabbitmq_response.get("reason")
            }), 500

    except Exception as err:
        return jsonify(
            {
                "sucsess": False,
                "reason": err
            }
        ), 400

    return jsonify({
        "message": "success",
        "job_id": job_id
    }), 200
