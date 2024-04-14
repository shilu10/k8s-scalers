import boto3
from flask import current_app

_s3_client = None

def get_s3_client():
    global _s3_client
    if _s3_client is None:
        _s3_client = boto3.client(
            "s3",
            region_name=current_app.config["S3_REGION"],
            verify=True
        )
    return _s3_client
