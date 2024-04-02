import boto3
from flask import current_app

_s3_client = None

def get_s3_client():
    global _s3_client
    if _s3_client is None:
        _s3_client = boto3.client(
            "s3",
            aws_access_key_id=current_app.config["AWS_ACCESS_KEY"],
            aws_secret_access_key=current_app.config["AWS_SECRET_ACCESS_KEY"],
            region_name=current_app.config["S3_REGION"]
        )
    return _s3_client
