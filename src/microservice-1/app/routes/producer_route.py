from flask import Blueprint, jsonify, render_template, request
from marshmallow import ValidationError
from werkzeug.utils import secure_filename
import boto3
import os 
from ..schema.metadata_schema import MetadataSchema
from ..configs import Config


producer_bp = Blueprint("producer_bp",  __name__)
metadata_schema = MetadataSchema()
s3_client = boto3.client('s3', 
                         aws_access_key_id=os.environ["ACCESS_KEY"],
                        aws_secret_access_key=os.environ["SECRET_KEY"]
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
    save_path = os.path.join(Config.video_directory, filename)
    video_file.save(save_path)

    # saving it into s3
    response = s3_client.create_bucket(
        Bucket = filename,
        CreateBucketConfiguration = {
            'AZ': 'private',
            'LocationConstraint': 'eu-west-1',
        },
    )

    
    return jsonify({
        "message": "success"
    }), 200
