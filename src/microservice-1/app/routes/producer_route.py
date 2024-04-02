import uuid
import boto3
import redis
import os 
import pika
import json
from flask import Blueprint, jsonify, render_template, request, current_app
from marshmallow import ValidationError
from werkzeug.utils import secure_filename
from ..schema.metadata_schema import MetadataSchema
from ..core.s3 import get_s3_client
from ..core.redis import get_redis_client
from ..core.rabbitmq import get_rabbitmq_channel


# blueprint
producer_bp = Blueprint("producer_bp",  __name__)

# schema validation
metadata_schema = MetadataSchema()

@producer_bp.route("/post_video", methods=["POST"])
def post_message():
    try:
        s3_client = get_s3_client()
        redis_client = get_redis_client()
        rabbitmq_channel = get_rabbitmq_channel()

    except Exception as err:
        return jsonify({
            "success": False,
            "reason": err
        }), 500

    # 1. check the schema
    try:
        video_metadata = request.form
        data = metadata_schema.load(video_metadata)

    except ValidationError as err:
        return jsonify(err.messages), 400
    
    # 2. Get the file
    video_file = request.files.get('video')
    if not video_file:
        return jsonify({"error": "No video file provided"}), 400
    
    # 3. Save it (or upload to S3, etc.)
    filename = secure_filename(video_file.filename)
    #save_path = os.path.join(Config.video_directory, filename)
    #video_file.save(save_path)

    # saving it into s3
    try:
        response = s3_client.put_object(
            Body = video_file,
            Bucket = current_app.config["OBJECT_STORE_BUCKET_NAME"], # 'k8s-scalers-example-bucket'
            Key = filename,
        )

        job_id = str(uuid.uuid4())

        # job status
        status_dict = dict()
        status_dict["job_id"] = job_id
        status_dict["status"] = "Processing"
        status_dict["progress"] = 0

        redis_client.hset(job_id, mapping=status_dict)

        rabbitmq_body = dict()
        rabbitmq_body["job_id"] = job_id
        rabbitmq_body["filename"] = filename

        rabbitmq_channel.basic_publish(exchange='', 
                              routing_key=os.environ["RABBITMQ_QUEUE_NAME"], 
                              body=json.dumps(rabbitmq_body)
                            )

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
