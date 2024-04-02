import uuid
import boto3
import redis
import os 
from flask import Blueprint, jsonify, render_template, request
from marshmallow import ValidationError
from werkzeug.utils import secure_filename
from ..schema.metadata_schema import MetadataSchema
from ..configs import Config


producer_bp = Blueprint("producer_bp",  __name__)
metadata_schema = MetadataSchema()
s3_client = boto3.client('s3', 
                        aws_access_key_id=os.environ["ACCESS_KEY"],
                        aws_secret_access_key=os.environ["SECRET_KEY"]
                    )

redis_client = redis.Redis(host = os.environ["REDIS_HOST"], 
                           port=os.environ["REDID_PORT"]
                        )

@producer_bp.route("/post_video", methods=["POST"])
def post_message():
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
            Bucket = 'k8s-scalers-example-bucket',
            Key = filename,
        )

        job_id = str(uuid.uuid4())

        # job status
        status_dict = dict()
        status_dict["job_id"] = job_id
        status_dict["status"] = "Processing"
        status_dict["progress"] = 0

        redis_client.hset(job_id, status_dict)

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
